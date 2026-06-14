#!/usr/bin/env python3
"""Build compact Markdown context packets for autoresearcher roles."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

try:
    import yaml  # type: ignore
except ImportError:  # pragma: no cover
    yaml = None

from metrics_ledger import build_metric_ledger


ROLE_CHOICES = ("setup_env", "supervisor", "executor", "reviewer", "summarizer", "chatgpt_pro")
DEFAULT_CONTEXT_CONFIG = {
    "max_source_doc_chars": 12000,
    "max_result_chars": 8000,
    "recent_iterations_for_pro": 3,
}


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


def read_json_obj(path: Optional[Path]) -> Any:
    if path is None:
        return None
    try:
        return json.loads(path.read_text())
    except FileNotFoundError:
        return None
    except json.JSONDecodeError as exc:
        return {"_error": f"Invalid JSON in {path}: {exc}"}


def truncate_text(text: str, max_chars: int = 6000) -> str:
    if len(text) <= max_chars:
        return text
    return text[:max_chars].rstrip() + f"\n\n_Trimmed to {max_chars} chars; inspect the source file for full text._\n"


def compact_value(value: Any, depth: int = 0, max_depth: int = 3) -> Any:
    if isinstance(value, (str, int, float, bool)) or value is None:
        if isinstance(value, str) and len(value) > 500:
            return value[:500].rstrip() + "... [trimmed]"
        return value
    if depth >= max_depth:
        if isinstance(value, dict):
            return {"_type": "object", "keys": sorted(str(key) for key in value.keys())[:20], "key_count": len(value)}
        if isinstance(value, list):
            return {"_type": "list", "length": len(value)}
        return str(value)
    if isinstance(value, list):
        if len(value) <= 8 and all(not isinstance(item, (dict, list)) for item in value):
            return value
        return {
            "_type": "list",
            "length": len(value),
            "first_items": [compact_value(item, depth + 1, max_depth) for item in value[:3]],
        }
    if isinstance(value, dict):
        compact: Dict[str, Any] = {}
        for key in sorted(value.keys()):
            compact[str(key)] = compact_value(value[key], depth + 1, max_depth)
        return compact
    return str(value)


def compact_result_summary(path: Optional[Path]) -> str:
    result = read_json_obj(path)
    if result is None:
        return "_Missing._"
    if not isinstance(result, dict):
        return json.dumps(compact_value(result), indent=2, sort_keys=True)

    summary: Dict[str, Any] = {
        "_source": path.as_posix() if path else None,
    }
    for key in (
        "experiment_id",
        "status",
        "claim_tested",
        "interpretation",
        "known_failures",
        "next_questions",
        "artifacts",
    ):
        if key in result:
            summary[key] = compact_value(result[key])
    for key in ("metrics", "baseline_metrics"):
        if key in result:
            summary[key] = compact_value(result[key], max_depth=2)
    return json.dumps(summary, indent=2, sort_keys=True)


def compact_review_summary(path: Optional[Path]) -> str:
    review = read_json_obj(path)
    if review is None:
        return "_Missing._"
    return json.dumps(compact_value(review, max_depth=3), indent=2, sort_keys=True)


def compact_decision_summary(path: Path) -> str:
    decision = read_json_obj(path)
    if not isinstance(decision, dict):
        return json.dumps(compact_value(decision), indent=2, sort_keys=True)
    experiment = decision.get("next_experiment")
    compact_experiment = None
    if isinstance(experiment, dict):
        compact_experiment = {
            "experiment_id": experiment.get("experiment_id"),
            "objective": experiment.get("objective"),
            "hypothesis": experiment.get("hypothesis"),
            "estimated_runtime_minutes": experiment.get("estimated_runtime_minutes"),
            "required_outputs": compact_value(experiment.get("required_outputs", [])),
        }
    summary = {
        "decision": decision.get("decision"),
        "confidence": decision.get("confidence"),
        "progress_score": decision.get("progress_score"),
        "rationale": decision.get("rationale"),
        "evidence": compact_value(decision.get("evidence", [])),
        "risks": compact_value(decision.get("risks", [])),
        "next_experiment": compact_experiment,
    }
    return json.dumps(summary, indent=2, sort_keys=True)


def load_context_config(repo_root: Path) -> Dict[str, int]:
    config = dict(DEFAULT_CONTEXT_CONFIG)
    loaded = load_repo_config(repo_root)
    context_cfg = loaded.get("context", {}) if isinstance(loaded, dict) else {}
    if not isinstance(context_cfg, dict):
        return config
    for key, value in DEFAULT_CONTEXT_CONFIG.items():
        raw = context_cfg.get(key, value)
        try:
            config[key] = int(raw)
        except (TypeError, ValueError):
            config[key] = value
    return config


def load_repo_config(repo_root: Path) -> Dict[str, Any]:
    if yaml is None:
        return {}
    try:
        loaded = yaml.safe_load((repo_root / "autoresearcher.yaml").read_text()) or {}
    except (FileNotFoundError, AttributeError):
        return {}
    return loaded if isinstance(loaded, dict) else {}


def git_output(repo_root: Path, args: List[str]) -> Optional[str]:
    try:
        result = subprocess.run(
            ["git", *args],
            cwd=str(repo_root),
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            timeout=3,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return None
    if result.returncode != 0:
        return None
    value = result.stdout.strip()
    return value or None


def normalize_github_repo_url(remote_url: str) -> Optional[str]:
    value = remote_url.strip()
    if not value:
        return None
    value = value.removesuffix(".git")
    https_match = re.match(r"https://github\.com/([^/\s]+)/([^/\s]+)$", value)
    if https_match:
        return f"https://github.com/{https_match.group(1)}/{https_match.group(2)}"
    ssh_match = re.match(r"git@github\.com:([^/\s]+)/([^/\s]+)$", value)
    if ssh_match:
        return f"https://github.com/{ssh_match.group(1)}/{ssh_match.group(2)}"
    ssh_url_match = re.match(r"ssh://git@github\.com/([^/\s]+)/([^/\s]+)$", value)
    if ssh_url_match:
        return f"https://github.com/{ssh_url_match.group(1)}/{ssh_url_match.group(2)}"
    return None


def github_repo_url(repo_root: Path, config: Dict[str, Any]) -> Optional[str]:
    github_cfg = config.get("github", {}) if isinstance(config.get("github"), dict) else {}
    configured = github_cfg.get("repo_url")
    if isinstance(configured, str):
        normalized = normalize_github_repo_url(configured)
        if normalized:
            return normalized

    git_cfg = config.get("git", {}) if isinstance(config.get("git"), dict) else {}
    remote = str(git_cfg.get("remote") or "origin")
    remote_url = git_output(repo_root, ["remote", "get-url", remote])
    return normalize_github_repo_url(remote_url or "")


def github_branch(repo_root: Path, config: Dict[str, Any]) -> str:
    github_cfg = config.get("github", {}) if isinstance(config.get("github"), dict) else {}
    for value in (github_cfg.get("branch"), (config.get("git", {}) or {}).get("branch") if isinstance(config.get("git"), dict) else None):
        if isinstance(value, str) and value.strip():
            return value.strip()
    return git_output(repo_root, ["branch", "--show-current"]) or "main"


def github_file_url(repo_root: Path, config: Dict[str, Any], path: Path) -> Optional[str]:
    repo_url = github_repo_url(repo_root, config)
    if not repo_url:
        return None
    rel = path.relative_to(repo_root).as_posix()
    return f"{repo_url}/blob/{github_branch(repo_root, config)}/{rel}"


def discover_source_docs(root: Path) -> List[Path]:
    patterns = [
        "*_prototype_plan.md",
        "*_plan.md",
        "project_goal.md",
        "research_goal.md",
        "brief.md",
        "background.md",
    ]
    docs: List[Path] = []
    for pattern in patterns:
        docs.extend(sorted(root.glob(pattern)))
    charter = root / "charter.md"
    if charter.exists():
        docs.insert(0, charter)

    seen = set()
    unique: List[Path] = []
    for path in docs:
        key = path.resolve()
        if key in seen or not path.is_file():
            continue
        seen.add(key)
        unique.append(path)
    return unique


def markdown_headings(text: str) -> str:
    headings = [line for line in text.splitlines() if line.lstrip().startswith("#")]
    if not headings:
        return "_No Markdown headings found._"
    return "\n".join(headings[:80])


def source_doc_section(path: Path, repo_root: Path, max_chars: int) -> str:
    body = read_text(path)
    label = path.relative_to(repo_root).as_posix()
    if len(body) <= max_chars:
        return fenced(label, body, "markdown")
    summary = (
        f"Source document is {len(body)} chars, exceeding max_source_doc_chars={max_chars}.\n\n"
        "Headings:\n\n"
        f"{markdown_headings(body)}\n\n"
        f"Inspect `{label}` for full text."
    )
    return fenced(label, summary, "markdown")


def first_sentence(text: Any, max_chars: int = 240) -> str:
    if not isinstance(text, str):
        return ""
    cleaned = " ".join(text.split())
    if not cleaned:
        return ""
    for marker in (". ", "? ", "! "):
        idx = cleaned.find(marker)
        if 0 <= idx < max_chars:
            return cleaned[: idx + 1]
    if len(cleaned) <= max_chars:
        return cleaned
    return cleaned[:max_chars].rstrip() + "..."


INTERESTING_METRIC_TOKENS = (
    "best",
    "calibration",
    "exact",
    "improvement",
    "mse",
    "overestimation",
    "overoptimism",
    "positive",
    "regret",
    "risk",
    "risky",
    "success",
    "unsolved",
)


def metric_key_is_interesting(key: str) -> bool:
    lowered = key.lower()
    return any(token in lowered for token in INTERESTING_METRIC_TOKENS)


def compact_metric_value_for_ledger(value: Any) -> Any:
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    if isinstance(value, list):
        return {"_type": "list", "length": len(value)}
    if isinstance(value, dict):
        return {"_type": "object", "key_count": len(value), "keys": sorted(str(key) for key in value.keys())[:12]}
    return str(value)


def compact_metrics_for_ledger(metrics: Any) -> Any:
    if not isinstance(metrics, dict):
        return compact_value(metrics, max_depth=1)

    scalar_metrics: Dict[str, Any] = {}
    nested_samples: Dict[str, Any] = {}
    for key in sorted(metrics.keys()):
        value = metrics[key]
        key_str = str(key)
        if isinstance(value, (str, int, float, bool)) or value is None:
            if metric_key_is_interesting(key_str) or len(scalar_metrics) < 8:
                scalar_metrics[key_str] = value
        elif isinstance(value, dict) and len(nested_samples) < 8:
            selected: Dict[str, Any] = {}
            for nested_key in sorted(value.keys()):
                nested_value = value[nested_key]
                nested_key_str = str(nested_key)
                if metric_key_is_interesting(nested_key_str) and not isinstance(nested_value, (dict, list)):
                    selected[nested_key_str] = nested_value
                if len(selected) >= 8:
                    break
            if selected:
                nested_samples[key_str] = selected

    summary: Dict[str, Any] = {
        "_key_count": len(metrics),
        "_keys": sorted(str(key) for key in metrics.keys())[:40],
    }
    if scalar_metrics:
        summary["scalars"] = scalar_metrics
    if nested_samples:
        summary["nested_samples"] = nested_samples
    return summary


def compact_text_list_for_ledger(items: Any, limit: int = 3, max_chars: int = 180) -> Any:
    if not isinstance(items, list):
        return compact_value(items, max_depth=1)
    compact_items = []
    for item in items[:limit]:
        if isinstance(item, str):
            text = " ".join(item.split())
            if len(text) > max_chars:
                text = text[:max_chars].rstrip() + "..."
            compact_items.append(text)
        else:
            compact_items.append(compact_value(item, max_depth=1))
    if len(items) > limit:
        compact_items.append(f"... {len(items) - limit} more; inspect full file")
    return compact_items


def compact_experiment_row(root: Path, iteration: int) -> Dict[str, Any]:
    iteration_id = f"{iteration:04d}"
    plan = read_json_obj(root / "plans" / f"{iteration_id}_plan.json")
    result = read_json_obj(root / "results" / f"{iteration_id}_result.json")
    review = read_json_obj(root / "reviews" / f"{iteration_id}_review.json")
    decision = read_json_obj(root / "decisions" / f"{iteration_id}_decision.json")

    row: Dict[str, Any] = {"iteration": iteration_id}
    if isinstance(decision, dict):
        row["decision"] = decision.get("decision")
    if isinstance(plan, dict):
        row["objective"] = first_sentence(plan.get("objective"))
        row["hypothesis"] = first_sentence(plan.get("hypothesis"))
    if isinstance(result, dict):
        row["status"] = result.get("status")
        row["claim_tested"] = first_sentence(result.get("claim_tested"))
        row["interpretation"] = first_sentence(result.get("interpretation"))
        row["metrics"] = compact_metrics_for_ledger(result.get("metrics", {}))
        row["baseline_metrics"] = compact_metrics_for_ledger(result.get("baseline_metrics", {}))
        failures = result.get("known_failures", [])
        if failures:
            row["known_failures"] = compact_text_list_for_ledger(failures)
    if isinstance(review, dict):
        row["review"] = review.get("verdict")
        row["allows_auto_continue"] = review.get("allows_auto_continue")
        reasons = review.get("reasons", [])
        if reasons:
            row["review_reasons"] = compact_text_list_for_ledger(reasons)
        flags = review.get("risk_flags", [])
        if flags:
            row["risk_flags"] = compact_text_list_for_ledger(flags)
    return row


def compact_project_ledger(root: Path, completed_iteration: int) -> str:
    rows = [compact_experiment_row(root, iteration) for iteration in range(1, completed_iteration + 1)]
    return json.dumps(rows, indent=2, sort_keys=True)


def latest_matching(directory: Path, pattern: str) -> Optional[Path]:
    matches = sorted(directory.glob(pattern))
    return matches[-1] if matches else None


def last_matching(directory: Path, pattern: str, limit: int = 3) -> List[Path]:
    return sorted(directory.glob(pattern))[-limit:]


def iteration_number(path: Path) -> Optional[int]:
    try:
        return int(path.name.split("_", 1)[0])
    except (ValueError, IndexError):
        return None


def last_matching_up_to(directory: Path, pattern: str, max_iteration: int, limit: int = 3) -> List[Path]:
    matches = [
        path
        for path in sorted(directory.glob(pattern))
        if (iteration_number(path) is not None and int(iteration_number(path)) <= max_iteration)
    ]
    return matches[-limit:]


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
    context_cfg = load_context_config(repo_root)
    state_obj = read_json_obj(root / "state.json")
    completed_iteration = int(state_obj.get("iteration", 0)) if isinstance(state_obj, dict) else 0
    if completed_iteration > 0:
        latest_id = f"{completed_iteration:04d}"
        latest_result = root / "results" / f"{latest_id}_result.json"
        latest_summary = root / "results" / f"{latest_id}_summary.md"
        latest_review = root / "reviews" / f"{latest_id}_review.json"
        if not latest_result.exists():
            latest_result = None
        if not latest_summary.exists():
            latest_summary = None
        if not latest_review.exists():
            latest_review = None
    else:
        latest_result = None
        latest_summary = None
        latest_review = None
    latest_decisions = last_matching_up_to(root / "decisions", "*_decision.json", completed_iteration, limit=3)
    metric_ledger = build_metric_ledger(repo_root, project)
    planning_docs = discover_source_docs(root)
    human_pivot_notes = last_matching(root / "progress", "human_pivot_*.md", limit=3)

    sections = [
        f"# Supervisor Context: {project}",
        "## Requested action\n\nChoose continue, pivot, stop, or needs_human. If this is iteration 0 with no prior result, propose the first small experiment when the charter is specific enough. If continuing, propose exactly one small experiment. If a human pivot note or next-step review plan exists, treat it as approved human direction and normally choose continue with the next small experiment from that plan, unless it is unsafe or impossible.\n",
        "## Project charter\n\n" + read_text(root / "charter.md"),
        "## Project planning docs\n\n"
        + (
            "\n".join(
                source_doc_section(path, repo_root, int(context_cfg.get("max_source_doc_chars", 12000)))
                for path in planning_docs
            )
            if planning_docs
            else "_None._"
        ),
        "## Human pivot notes\n\n"
        + (
            "\n".join(
                source_doc_section(path, repo_root, int(context_cfg.get("max_source_doc_chars", 12000)))
                for path in human_pivot_notes
            )
            if human_pivot_notes
            else "_None._"
        ),
        fenced("Environment state", read_json_pretty(root / "env_state.json"), "json"),
        fenced("Current state", read_json_pretty(root / "state.json"), "json"),
        fenced("Latest result summary", compact_result_summary(latest_result), "json"),
        "## Latest summary\n\n" + (truncate_text(read_text(latest_summary), 6000) if latest_summary else "_Missing._"),
        fenced("Latest review summary", compact_review_summary(latest_review), "json"),
        fenced("Metric ledger", json.dumps(metric_ledger, indent=2, sort_keys=True), "json"),
        "## Last decision summaries\n\n" + "\n".join(fenced(path.name, compact_decision_summary(path), "json") for path in latest_decisions),
        "## Full evidence paths\n\n"
        + markdown_list(path.relative_to(repo_root) for path in [latest_result, latest_summary, latest_review] if path)
        + "\nUse these paths if compact summaries are insufficient.\n",
        "## Stop, pivot, continue rules\n\n- For iteration 0, a missing latest result is expected and is not by itself a reason to stop.\n- After iteration 0, stop or choose needs_human on missing or invalid result files.\n- Stop on repeated invalid, negative, or low-value results.\n- Pivot only when evidence weakens the original idea but reveals a nearby testable idea.\n- Continue or pivot only for one cheap, high-information experiment.\n- Choose needs_human for ambiguity, expensive work, missing artifacts, or risky pivots.\n",
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
        fenced("Latest result summary", compact_result_summary(latest_result), "json"),
        "## Latest summary\n\n" + (truncate_text(read_text(latest_summary), 6000) if latest_summary else "_Missing._"),
        "## Full evidence paths\n\n"
        + markdown_list(path.relative_to(repo_root) for path in [latest_result, latest_summary] if path)
        + "\nInspect the full result JSON only when the compact summary and artifact list are insufficient.\n",
        "## Artifact paths\n\n" + markdown_list(artifact_dirs[-5:]),
        fenced("Review schema", read_text(repo_root / "schemas" / "review.schema.json"), "json"),
    ]
    return "\n\n".join(sections).rstrip() + "\n"


def build_summarizer_context(repo_root: Path, project: str) -> str:
    root = project_root(repo_root, project)
    context_cfg = load_context_config(repo_root)
    state_obj = read_json_obj(root / "state.json")
    completed_iteration = int(state_obj.get("iteration", 0)) if isinstance(state_obj, dict) else 0
    latest_decision = latest_matching(root / "decisions", "*_decision.json")
    recent_decisions = last_matching(root / "decisions", "*_decision.json", limit=3)
    recent_reviews = last_matching(root / "reviews", "*_review.json", limit=3)
    progress_summaries = last_matching(root / "progress", "*_summary.md", limit=3)
    planning_docs = discover_source_docs(root)
    human_pivot_notes = last_matching(root / "progress", "human_pivot_*.md", limit=3)

    evidence_paths: List[Path] = []
    for directory, pattern in (
        (root / "plans", "*_plan.md"),
        (root / "results", "*_summary.md"),
        (root / "results", "*_result.json"),
        (root / "reviews", "*_review.md"),
        (root / "decisions", "*_decision.md"),
    ):
        evidence_paths.extend(sorted(directory.glob(pattern)))

    sections = [
        f"# Progress Summarizer Context: {project}",
        "## Requested action\n\nWrite a concise human-readable Markdown progress summary for this project. Use the evidence below; do not overclaim beyond reviewed results.\n",
        "## Project charter\n\n" + read_text(root / "charter.md"),
        "## Project planning docs\n\n"
        + (
            "\n".join(
                source_doc_section(path, repo_root, int(context_cfg.get("max_source_doc_chars", 12000)))
                for path in planning_docs
            )
            if planning_docs
            else "_None._"
        ),
        "## Human pivot notes\n\n"
        + (
            "\n".join(
                source_doc_section(path, repo_root, int(context_cfg.get("max_source_doc_chars", 12000)))
                for path in human_pivot_notes
            )
            if human_pivot_notes
            else "_None._"
        ),
        fenced("Current state", read_json_pretty(root / "state.json"), "json"),
        fenced("Environment state", read_json_pretty(root / "env_state.json"), "json"),
        fenced("Experiment ledger", compact_project_ledger(root, completed_iteration), "json"),
        fenced("Latest supervisor decision", read_json_pretty(latest_decision) if latest_decision else "_Missing._", "json"),
        "## Recent decision summaries\n\n" + "\n".join(fenced(path.name, compact_decision_summary(path), "json") for path in recent_decisions),
        "## Recent review summaries\n\n" + "\n".join(fenced(path.name, compact_review_summary(path), "json") for path in recent_reviews),
        "## Existing progress summaries\n\n" + markdown_list(path.relative_to(repo_root) for path in progress_summaries),
        "## Full evidence paths\n\n" + markdown_list(path.relative_to(repo_root) for path in evidence_paths),
    ]
    return "\n\n".join(sections).rstrip() + "\n"


def build_chatgpt_pro_context(repo_root: Path, project: str, reason: str = "manual") -> str:
    root = project_root(repo_root, project)
    config = load_repo_config(repo_root)
    repo_url = github_repo_url(repo_root, config)
    latest_summary = root / "progress" / "latest_summary.md"
    latest_decision = latest_matching(root / "decisions", "[0-9][0-9][0-9][0-9]_decision.md") or latest_matching(
        root / "decisions",
        "[0-9][0-9][0-9][0-9]_decision.json",
    )
    project_docs = [path for path in discover_source_docs(root) if path.name != "charter.md"]
    latest_summary_url = github_file_url(repo_root, config, latest_summary)
    latest_decision_url = github_file_url(repo_root, config, latest_decision) if latest_decision else None
    charter_url = github_file_url(repo_root, config, root / "charter.md")
    schema_url = github_file_url(repo_root, config, repo_root / "schemas" / "pro_decision.schema.json")

    def link_or_path(url: Optional[str], path: Path) -> str:
        if url:
            return url
        return f"`{path.relative_to(repo_root).as_posix()}`"

    def project_doc_links() -> List[str]:
        if not project_docs:
            return ["- _No broader project planning docs found._"]
        lines: List[str] = []
        for path in project_docs[:8]:
            url = github_file_url(repo_root, config, path)
            lines.append(f"- {path.name}: {link_or_path(url, path)}")
        if len(project_docs) > 8:
            lines.append(f"- _{len(project_docs) - 8} more project docs omitted from this short packet; inspect the repository if needed._")
        return lines

    lines = [
        f"# Check-In: {project}",
        "",
        f"Checkpoint reason: `{reason}`",
        "",
        "Continue from this existing advisor thread and use GitHub for the current evidence and broader project docs.",
        "",
        f"- Repository: {repo_url or '_GitHub remote unavailable; inspect linked paths if available._'}",
        f"- Latest progress summary: {link_or_path(latest_summary_url, latest_summary)}",
        f"- Latest local Codex decision: {link_or_path(latest_decision_url, latest_decision) if latest_decision else '_Missing._'}",
        f"- Charter: {link_or_path(charter_url, root / 'charter.md')}",
        f"- Required output schema: {link_or_path(schema_url, repo_root / 'schemas' / 'pro_decision.schema.json')}",
        "",
        "## Broader Project Context",
        "",
        *project_doc_links(),
        "",
        "Decide the next research direction as the human advisor for this loop:",
        "",
        "1. Choose exactly one: `continue`, `pivot`, or `stop`.",
        "2. If Codex is stopping or pivoting, independently decide whether to stop or propose a better direction.",
        "3. If choosing `continue` or `pivot`, propose small experiments runnable within 30 minutes.",
        "4. Return exactly one fenced JSON block matching `schemas/pro_decision.schema.json`, followed by at most one short paragraph.",
        "",
        "",
    ]
    return "\n".join(lines).rstrip() + "\n"


def build_context(repo_root: Path, project: str, role: str, plan: Optional[Path] = None, reason: str = "manual") -> str:
    if role == "setup_env":
        return build_setup_env_context(repo_root, project)
    if role == "supervisor":
        return build_supervisor_context(repo_root, project)
    if role == "executor":
        return build_executor_context(repo_root, project, plan)
    if role == "reviewer":
        return build_reviewer_context(repo_root, project)
    if role == "summarizer":
        return build_summarizer_context(repo_root, project)
    if role == "chatgpt_pro":
        return build_chatgpt_pro_context(repo_root, project, reason=reason)
    raise ValueError(f"unknown role: {role}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Build an autoresearcher role context packet.")
    parser.add_argument("--project", required=True)
    parser.add_argument("--role", required=True, choices=ROLE_CHOICES)
    parser.add_argument("--plan", type=Path)
    parser.add_argument("--reason", default="manual")
    parser.add_argument("--repo-root", type=Path)
    args = parser.parse_args()

    repo_root = (args.repo_root or repo_root_from()).resolve()
    print(build_context(repo_root, args.project, args.role, args.plan, reason=args.reason), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
