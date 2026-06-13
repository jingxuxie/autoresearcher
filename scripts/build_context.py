#!/usr/bin/env python3
"""Build compact Markdown context packets for autoresearcher roles."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Iterable, List, Optional


ROLE_CHOICES = ("setup_env", "supervisor", "executor", "reviewer", "chatgpt_pro")


def repo_root_from(start: Optional[Path] = None) -> Path:
    start = (start or Path.cwd()).resolve()
    if (start / "autoresearcher.yaml").exists():
        return start
    for parent in start.parents:
        if (parent / "autoresearcher.yaml").exists():
            return parent
    return start


def project_root(repo_root: Path, project: str) -> Path:
    return repo_root / "research" / project


def read_text(path: Path, default: str = "_Missing._") -> str:
    try:
        return path.read_text()
    except FileNotFoundError:
        return default


def read_json_pretty(path: Path, default: str = "_Missing._") -> str:
    try:
        return json.dumps(json.loads(path.read_text()), indent=2, sort_keys=True)
    except FileNotFoundError:
        return default
    except json.JSONDecodeError as exc:
        return f"_Invalid JSON in {path}: {exc}_"


def latest_matching(directory: Path, pattern: str) -> Optional[Path]:
    matches = sorted(directory.glob(pattern))
    return matches[-1] if matches else None


def last_matching(directory: Path, pattern: str, limit: int = 3) -> List[Path]:
    return sorted(directory.glob(pattern))[-limit:]


def fenced(title: str, body: str, language: str = "") -> str:
    fence = f"```{language}".rstrip()
    return f"## {title}\n\n{fence}\n{body.rstrip()}\n```\n"


def markdown_list(items: Iterable[Path]) -> str:
    paths = list(items)
    if not paths:
        return "_None._\n"
    return "\n".join(f"- `{path.as_posix()}`" for path in paths) + "\n"


def build_supervisor_context(repo_root: Path, project: str) -> str:
    root = project_root(repo_root, project)
    latest_result = latest_matching(root / "results", "*_result.json")
    latest_summary = latest_matching(root / "results", "*_summary.md")
    latest_review = latest_matching(root / "reviews", "*_review.json")
    latest_decisions = last_matching(root / "decisions", "*_decision.json", limit=3)

    sections = [
        f"# Supervisor Context: {project}",
        "## Requested action\n\nChoose continue, pivot, stop, or needs_human. If this is iteration 0 with no prior result, propose the first small experiment when the charter is specific enough. If continuing, propose exactly one small experiment.\n",
        "## Project charter\n\n" + read_text(root / "charter.md"),
        fenced("Environment state", read_json_pretty(root / "env_state.json"), "json"),
        fenced("Current state", read_json_pretty(root / "state.json"), "json"),
        fenced("Latest result JSON", read_json_pretty(latest_result) if latest_result else "_Missing._", "json"),
        "## Latest summary\n\n" + (read_text(latest_summary) if latest_summary else "_Missing._"),
        fenced("Latest review JSON", read_json_pretty(latest_review) if latest_review else "_Missing._", "json"),
        "## Last decisions\n\n" + "\n".join(fenced(path.name, read_json_pretty(path), "json") for path in latest_decisions),
        "## Stop, pivot, continue rules\n\n- For iteration 0, a missing latest result is expected and is not by itself a reason to stop.\n- After iteration 0, stop or choose needs_human on missing or invalid result files.\n- Stop on repeated invalid, negative, or low-value results.\n- Pivot only when evidence weakens the original idea but reveals a nearby testable idea.\n- Continue only for one cheap, high-information experiment.\n- Choose needs_human for ambiguity, expensive work, missing artifacts, or risky pivots.\n",
    ]
    return "\n\n".join(sections).rstrip() + "\n"


def build_setup_env_context(repo_root: Path, project: str) -> str:
    root = project_root(repo_root, project)
    sections = [
        f"# Setup Environment Context: {project}",
        "## Requested action\n\nCreate or verify the project-specific conda environment, then write `research/<project>/env_state.json`.\n",
        "## Project charter\n\n" + read_text(root / "charter.md"),
        fenced("Environment YAML", read_text(root / "environment.yaml"), "yaml"),
        fenced("Current environment state", read_json_pretty(root / "env_state.json"), "json"),
        fenced("Required env state schema", read_text(repo_root / "schemas" / "env_setup.schema.json"), "json"),
        "## Setup requirements\n\n- Use only this project's conda environment.\n- Verify `conda run -n <env> python --version`.\n- GPU is preferred when available. Check `nvidia-smi` if possible.\n- If conda, network, filesystem, or GPU access is blocked, write `status: \"blocked\"` with a blocker object and the exact failed command.\n- Do not run the research experiment.\n",
        "## Setup requirements\n\n- Use only this project's conda environment.\n- Verify `conda run -n <env> python --version`.\n- GPU is preferred when available. Check `nvidia-smi` if possible.\n- For JAX/GPU projects, run `conda run -n <env> python scripts/probe_jax_gpu.py --require-gpu --output research/<project>/setup_logs/jax_gpu_probe.json`.\n- If conda, network, filesystem, or GPU access is blocked, write `status: \"blocked\"` with a blocker object and the exact failed command.\n- Do not run the research experiment.\n",
    ]
    return "\n\n".join(sections).rstrip() + "\n"


def build_executor_context(repo_root: Path, project: str, plan: Optional[Path]) -> str:
    root = project_root(repo_root, project)
    if plan is None:
        plan = latest_matching(root / "plans", "*_plan.md")
    if plan is None:
        plan_body = "_Missing experiment plan._"
    else:
        plan_body = read_text(plan)

    next_id = (plan.name.split("_", 1)[0] if plan else "NNNN")
    required = (
        f"- `research/{project}/results/{next_id}_result.json`\n"
        f"- `research/{project}/results/{next_id}_summary.md`\n"
        f"- `research/{project}/artifacts/{next_id}/`\n"
    )
    sections = [
        f"# Executor Context: {project}",
        "## Current experiment plan\n\n" + plan_body,
        fenced("Environment YAML", read_text(root / "environment.yaml"), "yaml"),
        fenced("Environment state", read_json_pretty(root / "env_state.json"), "json"),
        fenced("Result schema", read_text(repo_root / "schemas" / "result.schema.json"), "json"),
        "## Required output paths\n\n" + required,
        "## Timeout and environment warning\n\nThe orchestrator enforces the configured timeout externally. Run experiment commands inside the project conda environment, normally with `conda run -n <env> ...`. Keep the experiment small and write a failed result JSON if the plan is impossible.\n",
        "## Existing code pointers\n\nThis starter repository has no project code yet. Create only the tiny files needed under the experiment artifact directory unless the plan explicitly asks for repo code changes.\n",
    ]
    return "\n\n".join(sections).rstrip() + "\n"


def build_reviewer_context(repo_root: Path, project: str) -> str:
    root = project_root(repo_root, project)
    latest_plan_md = latest_matching(root / "plans", "*_plan.md")
    latest_plan_json = latest_matching(root / "plans", "*_plan.json")
    latest_result = latest_matching(root / "results", "*_result.json")
    latest_summary = latest_matching(root / "results", "*_summary.md")
    artifact_dirs = sorted((root / "artifacts").glob("*"))

    sections = [
        f"# Reviewer Context: {project}",
        "## Latest plan\n\n" + (read_text(latest_plan_md) if latest_plan_md else "_Missing._"),
        fenced("Latest plan JSON", read_json_pretty(latest_plan_json) if latest_plan_json else "_Missing._", "json"),
        fenced("Latest result JSON", read_json_pretty(latest_result) if latest_result else "_Missing._", "json"),
        "## Latest summary\n\n" + (read_text(latest_summary) if latest_summary else "_Missing._"),
        "## Artifact paths\n\n" + markdown_list(artifact_dirs[-5:]),
        fenced("Review schema", read_text(repo_root / "schemas" / "review.schema.json"), "json"),
    ]
    return "\n\n".join(sections).rstrip() + "\n"


def build_chatgpt_pro_context(repo_root: Path, project: str) -> str:
    root = project_root(repo_root, project)
    latest_result = latest_matching(root / "results", "*_result.json")
    latest_review = latest_matching(root / "reviews", "*_review.json")
    recent = []
    recent.extend(last_matching(root / "decisions", "*_decision.json", limit=3))
    recent.extend(last_matching(root / "results", "*_result.json", limit=3))
    recent.extend(last_matching(root / "reviews", "*_review.json", limit=3))
    recent = sorted(recent)

    sections = [
        f"# ChatGPT Pro Review Packet: {project}",
        "## Explicit question\n\nGiven the evidence below, choose exactly one: continue, pivot, stop, or needs_human.\n",
        "## Compact project charter\n\n" + read_text(root / "charter.md"),
        fenced("Current state", read_json_pretty(root / "state.json"), "json"),
        "## Last 2-3 iteration artifacts\n\n" + "\n".join(fenced(path.relative_to(repo_root).as_posix(), read_json_pretty(path), "json") for path in recent),
        fenced("Latest result", read_json_pretty(latest_result) if latest_result else "_Missing._", "json"),
        fenced("Latest review", read_json_pretty(latest_review) if latest_review else "_Missing._", "json"),
        fenced("Required output JSON schema", read_text(repo_root / "schemas" / "pro_decision.schema.json"), "json"),
    ]
    return "\n\n".join(sections).rstrip() + "\n"


def build_context(repo_root: Path, project: str, role: str, plan: Optional[Path] = None) -> str:
    if role == "setup_env":
        return build_setup_env_context(repo_root, project)
    if role == "supervisor":
        return build_supervisor_context(repo_root, project)
    if role == "executor":
        return build_executor_context(repo_root, project, plan)
    if role == "reviewer":
        return build_reviewer_context(repo_root, project)
    if role == "chatgpt_pro":
        return build_chatgpt_pro_context(repo_root, project)
    raise ValueError(f"unknown role: {role}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Build an autoresearcher role context packet.")
    parser.add_argument("--project", required=True)
    parser.add_argument("--role", required=True, choices=ROLE_CHOICES)
    parser.add_argument("--plan", type=Path)
    parser.add_argument("--repo-root", type=Path)
    args = parser.parse_args()

    repo_root = (args.repo_root or repo_root_from()).resolve()
    print(build_context(repo_root, args.project, args.role, args.plan), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
