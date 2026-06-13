#!/usr/bin/env python3
"""Codex-only Phase 1 autoresearcher orchestrator."""

from __future__ import annotations

import argparse
import json
import os
import signal
import subprocess
import sys
import threading
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple

try:
    import yaml  # type: ignore
except ImportError:  # pragma: no cover - exercised only on minimal systems
    yaml = None

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from build_context import ROLE_CHOICES, build_context  # noqa: E402
from validate_artifacts import (  # noqa: E402
    ValidationError,
    load_json,
    validate_json_schema,
    validate_required_result_files,
    validate_result_artifact_paths,
)


ROLE_NAMES = ("setup_env", "supervisor", "executor", "reviewer")
LOCAL_STATE_PATH = Path(".autoresearcher") / "local_state.json"


DEFAULT_STATE: Dict[str, Any] = {
    "iteration": 0,
    "status": "active",
    "last_decision": "start",
    "primary_metric": None,
    "best_primary_metric": None,
    "no_progress_rounds": 0,
    "human_review_required": False,
    "last_pro_review_iteration": 0,
    "notes": [],
}


def conda_env_name_for_project(project: str, prefix: str = "autoresearcher") -> str:
    cleaned = "".join(ch if ch.isalnum() else "_" for ch in project.lower()).strip("_")
    return f"{prefix}_{cleaned or 'project'}"


def default_env_state(project: str, env_name: str) -> Dict[str, Any]:
    return {
        "project": project,
        "status": "pending",
        "conda_env_name": env_name,
        "conda_env_path": None,
        "environment_file": f"research/{project}/environment.yaml",
        "commands_run": [],
        "packages_verified": [],
        "gpu_requested": True,
        "gpu_available": None,
        "gpu_checks": [],
        "summary": "Environment has not been set up yet.",
        "blocker": None,
    }


def default_environment_yaml(env_name: str, python_version: str = "3.11") -> str:
    return (
        f"name: {env_name}\n"
        "channels:\n"
        "  - conda-forge\n"
        "dependencies:\n"
        f"  - python={python_version}\n"
        "  - pip\n"
        "  - pyyaml\n"
        "  - jsonschema\n"
        "  - pip:\n"
        "      - \"jax[cuda12]\"\n"
    )


DEFAULT_CHARTER = """# Project Charter

## Research goal

Replace this file with the research idea you want the autoresearcher to evaluate.

## Main hypothesis

State one falsifiable hypothesis.

## Primary metric

Name the metric that should improve.

## Success criteria

- Define a concrete small-scale pass condition.

## Failure criteria

- Define what would disprove or block the idea.
"""


DEFAULT_CONFIG_TEXT = """project_default: project_001

codex:
  model: gpt-5.5
  reasoning_effort: xhigh
  resume_mode: role-resume
  fail_if_model_unavailable: true

roles:
  setup_env:
    sandbox: workspace-write
    gpu_sandbox: danger-full-access
    output_schema: schemas/env_setup.schema.json
    timeout_minutes: 45

  supervisor:
    sandbox: read-only
    output_schema: schemas/decision.schema.json
    timeout_minutes: 15

  executor:
    sandbox: workspace-write
    gpu_sandbox: danger-full-access
    output_schema: null
    timeout_minutes: 30

  reviewer:
    sandbox: read-only
    output_schema: schemas/review.schema.json
    timeout_minutes: 15

loop:
  max_iterations: 12
  max_no_progress_rounds: 3
  require_environment_ready: true
  require_human_for_pivot: true
  require_human_for_expensive_run: true
  require_human_for_publishable_claim: true
  stop_on_missing_result: true
  stop_on_invalid_schema: true
  stop_on_timeout: true

git:
  enabled: true
  commit: true
  push: false
  remote: origin
  branch: null

chatgpt_pro:
  enabled: false
  backend: codex-chatgpt-control
  cadence_iterations: 3
  allow_cadence_2_or_3: true
  thread_url: null
  existing_tab: true
  require_visible_session: true
  require_user_approved_prompt: true
  require_model: GPT-5.5 Pro
  require_thinking: Heavy
  fail_if_unavailable: true
  allow_model_fallback: false
  max_retries: 0

environment:
  create_new_conda_env_per_project: true
  default_python: "3.11"
  env_name_prefix: autoresearcher
  require_ready_before_run: true
  setup_summary_path: setup_logs/setup_summary.md
  gpu:
    prefer: true
    require_escalation_for_gpu_runs: true
    auto_approve_escalation: true
    use_gpu_sandbox_for_setup: true
    use_gpu_sandbox_for_executor: true
"""


@dataclass
class CodexRunResult:
    role: str
    session_id: Optional[str]
    output_path: Path
    jsonl_log_path: Path
    stderr_log_path: Path
    return_code: int
    timed_out: bool
    stdout_tail: str
    stderr_tail: str


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def json_dump(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")


def repo_root_from(start: Optional[Path] = None) -> Path:
    start = (start or Path.cwd()).resolve()
    if (start / "autoresearcher.yaml").exists():
        return start
    for parent in start.parents:
        if (parent / "autoresearcher.yaml").exists():
            return parent
    return start


def load_config(repo_root: Path) -> Dict[str, Any]:
    config_path = repo_root / "autoresearcher.yaml"
    if not config_path.exists():
        config_path.write_text(DEFAULT_CONFIG_TEXT)
    if yaml is None:
        raise RuntimeError("PyYAML is required to read autoresearcher.yaml. Install it or run from this environment.")
    loaded = yaml.safe_load(config_path.read_text()) or {}
    if not isinstance(loaded, dict):
        raise RuntimeError(f"invalid config root in {config_path}: expected mapping")
    return loaded


def project_dir(repo_root: Path, project: str) -> Path:
    return repo_root / "research" / project


def ensure_project_scaffold(repo_root: Path, project: str) -> None:
    root = project_dir(repo_root, project)
    config = load_config(repo_root)
    env_cfg = config.get("environment", {})
    env_prefix = str(env_cfg.get("env_name_prefix", "autoresearcher"))
    python_version = str(env_cfg.get("default_python", "3.11"))
    env_name = conda_env_name_for_project(project, prefix=env_prefix)
    for subdir in ("plans", "results", "reviews", "decisions", "packets", "artifacts", "setup_logs"):
        (root / subdir).mkdir(parents=True, exist_ok=True)
    charter = root / "charter.md"
    if not charter.exists():
        charter.write_text(DEFAULT_CHARTER)
    env_file = root / "environment.yaml"
    if not env_file.exists():
        env_file.write_text(default_environment_yaml(env_name, python_version=python_version))
    env_state_path = root / "env_state.json"
    if not env_state_path.exists():
        json_dump(env_state_path, default_env_state(project, env_name))
    state_path = root / "state.json"
    if not state_path.exists():
        json_dump(state_path, DEFAULT_STATE)
    ensure_local_state(repo_root, project)


def default_local_project_state() -> Dict[str, Any]:
    return {
        "codex_sessions": {
            role: {"session_id": None, "last_used_at": None}
            for role in ROLE_NAMES
        },
        "chatgpt_pro": {
            "thread_url": None,
            "last_review_iteration": 0,
        },
    }


def ensure_local_state(repo_root: Path, project: str) -> Dict[str, Any]:
    path = repo_root / LOCAL_STATE_PATH
    if path.exists():
        try:
            state = json.loads(path.read_text())
        except json.JSONDecodeError:
            state = {"projects": {}}
    else:
        state = {"projects": {}}
    state.setdefault("projects", {})
    state["projects"].setdefault(project, default_local_project_state())
    for role in ROLE_NAMES:
        state["projects"][project].setdefault("codex_sessions", {})
        state["projects"][project]["codex_sessions"].setdefault(
            role, {"session_id": None, "last_used_at": None}
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    json_dump(path, state)
    return state


def load_local_state(repo_root: Path, project: str) -> Dict[str, Any]:
    return ensure_local_state(repo_root, project)


def save_local_state(repo_root: Path, state: Dict[str, Any]) -> None:
    json_dump(repo_root / LOCAL_STATE_PATH, state)


def load_project_state(repo_root: Path, project: str) -> Dict[str, Any]:
    ensure_project_scaffold(repo_root, project)
    state = load_json(project_dir(repo_root, project) / "state.json")
    if not isinstance(state, dict):
        raise RuntimeError("project state must be a JSON object")
    return state


def save_project_state(repo_root: Path, project: str, state: Dict[str, Any]) -> Path:
    path = project_dir(repo_root, project) / "state.json"
    json_dump(path, state)
    return path


def load_env_state(repo_root: Path, project: str) -> Dict[str, Any]:
    ensure_project_scaffold(repo_root, project)
    state = load_json(project_dir(repo_root, project) / "env_state.json")
    if not isinstance(state, dict):
        raise RuntimeError("environment state must be a JSON object")
    return state


def save_env_state(repo_root: Path, project: str, state: Dict[str, Any]) -> Path:
    path = project_dir(repo_root, project) / "env_state.json"
    json_dump(path, state)
    return path


def env_is_ready(repo_root: Path, project: str) -> bool:
    try:
        return load_env_state(repo_root, project).get("status") == "ready"
    except (ValidationError, RuntimeError, FileNotFoundError):
        return False


def tail_text(text: str, max_chars: int = 4000) -> str:
    if len(text) <= max_chars:
        return text
    return text[-max_chars:]


def extract_thread_id_from_jsonl(stdout: str) -> Optional[str]:
    def from_obj(obj: Any) -> Optional[str]:
        if isinstance(obj, dict):
            values = set(str(value) for value in obj.values() if isinstance(value, str))
            if "thread.started" in values or obj.get("type") == "thread.started":
                for key in ("thread_id", "threadId", "session_id", "sessionId", "id"):
                    value = obj.get(key)
                    if isinstance(value, str) and value:
                        return value
            for value in obj.values():
                found = from_obj(value)
                if found:
                    return found
        elif isinstance(obj, list):
            for item in obj:
                found = from_obj(item)
                if found:
                    return found
        return None

    for line in stdout.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue
        found = from_obj(obj)
        if found:
            return found
    return None


class CodexRunner:
    def __init__(self, repo_root: Path, config: Dict[str, Any], codex_bin: str = "codex") -> None:
        self.repo_root = repo_root
        self.config = config
        self.codex_bin = codex_bin

    def _role_session_id(self, project: str, role: str) -> Optional[str]:
        state = load_local_state(self.repo_root, project)
        return state["projects"][project]["codex_sessions"][role].get("session_id")

    def _store_role_session_id(self, project: str, role: str, session_id: Optional[str]) -> None:
        if not session_id:
            return
        state = load_local_state(self.repo_root, project)
        state["projects"][project]["codex_sessions"][role] = {
            "session_id": session_id,
            "last_used_at": utc_now_iso(),
        }
        save_local_state(self.repo_root, state)

    def _command(
        self,
        session_id: Optional[str],
        output_path: Path,
        schema_path: Optional[Path],
        sandbox: str,
    ) -> List[str]:
        codex_cfg = self.config.get("codex", {})
        model = str(codex_cfg.get("model", "gpt-5.5"))
        reasoning_effort = str(codex_cfg.get("reasoning_effort", "xhigh"))
        cmd = [
            self.codex_bin,
            "exec",
            "--cd",
            str(self.repo_root),
            "--skip-git-repo-check",
            "--json",
            "--model",
            model,
            "-c",
            f"model_reasoning_effort={reasoning_effort}",
            "--sandbox",
            sandbox,
            "--output-last-message",
            str(output_path),
        ]
        if schema_path is not None:
            cmd.extend(["--output-schema", str(schema_path)])
        if session_id:
            cmd.extend(["resume", session_id, "-"])
        else:
            cmd.append("-")
        return cmd

    def run_role(
        self,
        project: str,
        role: str,
        prompt: str,
        output_path: Path,
        schema_path: Optional[Path],
        sandbox: str,
        timeout_minutes: int,
        resume: bool = True,
    ) -> CodexRunResult:
        output_path = output_path.resolve()
        output_path.parent.mkdir(parents=True, exist_ok=True)
        jsonl_log_path = output_path.with_name(output_path.stem + "_events.jsonl")
        stderr_log_path = output_path.with_name(output_path.stem + "_stderr.log")
        prior_session_id = self._role_session_id(project, role) if resume else None
        cmd = self._command(prior_session_id, output_path, schema_path, sandbox)

        stdout_chunks: List[str] = []
        stderr_chunks: List[str] = []

        def stream_pipe(pipe: Any, log_path: Path, chunks: List[str]) -> None:
            try:
                with log_path.open("w") as log_file:
                    while True:
                        line = pipe.readline()
                        if line == "":
                            break
                        chunks.append(line)
                        log_file.write(line)
                        log_file.flush()
            finally:
                pipe.close()

        proc = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            start_new_session=True,
        )
        timed_out = False

        assert proc.stdout is not None
        assert proc.stderr is not None
        stdout_thread = threading.Thread(
            target=stream_pipe,
            args=(proc.stdout, jsonl_log_path, stdout_chunks),
            daemon=True,
        )
        stderr_thread = threading.Thread(
            target=stream_pipe,
            args=(proc.stderr, stderr_log_path, stderr_chunks),
            daemon=True,
        )
        stdout_thread.start()
        stderr_thread.start()

        if proc.stdin is not None:
            try:
                proc.stdin.write(prompt)
                proc.stdin.close()
            except BrokenPipeError:
                pass

        deadline = time.monotonic() + timeout_minutes * 60
        while proc.poll() is None:
            if time.monotonic() >= deadline:
                timed_out = True
                break
            time.sleep(0.2)

        if timed_out:
            timed_out = True
            try:
                os.killpg(proc.pid, signal.SIGTERM)
            except ProcessLookupError:
                pass
            try:
                proc.wait(timeout=10)
            except subprocess.TimeoutExpired:
                try:
                    os.killpg(proc.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
                proc.wait(timeout=10)
        else:
            proc.wait()

        stdout_thread.join(timeout=5)
        stderr_thread.join(timeout=5)

        stdout = "".join(stdout_chunks)
        stderr = "".join(stderr_chunks)

        session_id = extract_thread_id_from_jsonl(stdout) or prior_session_id
        self._store_role_session_id(project, role, session_id)

        return CodexRunResult(
            role=role,
            session_id=session_id,
            output_path=output_path,
            jsonl_log_path=jsonl_log_path,
            stderr_log_path=stderr_log_path,
            return_code=proc.returncode if proc.returncode is not None else -1,
            timed_out=timed_out,
            stdout_tail=tail_text(stdout),
            stderr_tail=tail_text(stderr),
        )


def recursive_contains_string(obj: Any, target: str) -> bool:
    if isinstance(obj, str):
        return obj == target
    if isinstance(obj, dict):
        return any(recursive_contains_string(value, target) for value in obj.values())
    if isinstance(obj, list):
        return any(recursive_contains_string(item, target) for item in obj)
    return False


def check_model_available(repo_root: Path, config: Dict[str, Any], codex_bin: str = "codex") -> None:
    codex_cfg = config.get("codex", {})
    model = str(codex_cfg.get("model", "gpt-5.5"))
    if not codex_cfg.get("fail_if_model_unavailable", True):
        return
    try:
        proc = subprocess.run(
            [codex_bin, "debug", "models"],
            cwd=str(repo_root),
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=30,
        )
    except FileNotFoundError as exc:
        raise RuntimeError("codex CLI was not found on PATH.") from exc
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError("codex debug models timed out; cannot verify configured model.") from exc

    if proc.returncode != 0:
        raise RuntimeError(
            "codex debug models failed; cannot verify configured model.\n"
            f"stderr tail:\n{tail_text(proc.stderr)}"
        )

    try:
        catalog = json.loads(proc.stdout)
    except json.JSONDecodeError as exc:
        raise RuntimeError("codex debug models did not return JSON; cannot verify configured model.") from exc

    if not recursive_contains_string(catalog, model):
        raise RuntimeError(
            f"Configured model {model!r} was not found in `codex debug models` output. "
            "Update autoresearcher.yaml or set codex.fail_if_model_unavailable=false explicitly."
        )


class GitManager:
    def __init__(self, repo_root: Path, config: Dict[str, Any]) -> None:
        self.repo_root = repo_root
        self.config = config.get("git", {})

    def enabled(self) -> bool:
        return bool(self.config.get("enabled", True) and self.config.get("commit", True))

    def _git(self, args: Sequence[str]) -> subprocess.CompletedProcess:
        return subprocess.run(
            ["git"] + list(args),
            cwd=str(self.repo_root),
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

    def is_repo(self) -> bool:
        proc = self._git(["rev-parse", "--is-inside-work-tree"])
        return proc.returncode == 0 and proc.stdout.strip() == "true"

    def commit(self, paths: Iterable[Path], message: str) -> bool:
        if not self.enabled() or not self.is_repo():
            return False
        rel_paths = [str(path.resolve().relative_to(self.repo_root.resolve())) for path in paths if path.exists()]
        if not rel_paths:
            return False
        status = self._git(["status", "--porcelain", "--"] + rel_paths)
        if status.returncode != 0 or not status.stdout.strip():
            return False
        add = self._git(["add", "--"] + rel_paths)
        if add.returncode != 0:
            raise RuntimeError(f"git add failed:\n{add.stderr}")
        commit = self._git(["commit", "-m", message])
        if commit.returncode != 0:
            if "nothing to commit" in commit.stdout.lower() + commit.stderr.lower():
                return False
            raise RuntimeError(f"git commit failed:\n{commit.stderr}")
        if self.config.get("push", False):
            self.push()
        return True

    def push(self) -> None:
        remote = str(self.config.get("remote") or "origin")
        branch = self.config.get("branch")
        args = ["push", remote]
        if branch:
            args.append(str(branch))
        proc = self._git(args)
        if proc.returncode != 0:
            raise RuntimeError(f"git push failed:\n{proc.stderr}")


def prompt_for_role(repo_root: Path, role: str, context: str, iteration_id: str) -> str:
    prompt_path = repo_root / "prompts" / f"{role}.md"
    prompt = prompt_path.read_text()
    return (
        f"{prompt.rstrip()}\n\n"
        f"---\n\n"
        f"Current iteration id: {iteration_id}\n\n"
        f"{context.rstrip()}\n"
    )


def role_config(config: Dict[str, Any], role: str) -> Dict[str, Any]:
    roles = config.get("roles", {})
    if role not in roles:
        raise RuntimeError(f"missing role config: {role}")
    return roles[role] or {}


def schema_for_role(repo_root: Path, role_cfg: Dict[str, Any]) -> Optional[Path]:
    raw = role_cfg.get("output_schema")
    if not raw:
        return None
    return (repo_root / raw).resolve()


def write_packet(repo_root: Path, project: str, iteration_id: str, role: str, packet: str) -> Path:
    path = project_dir(repo_root, project) / "packets" / f"{iteration_id}_{role}_packet.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(packet)
    return path


def decision_markdown(decision: Dict[str, Any]) -> str:
    lines = [
        f"# Decision: {decision['decision']}",
        "",
        f"Confidence: {decision['confidence']}",
        f"Progress score: {decision['progress_score']}",
        "",
        "## Rationale",
        "",
        decision["rationale"],
        "",
        "## Evidence",
        "",
    ]
    lines.extend(f"- {item}" for item in decision.get("evidence", []))
    lines.extend(["", "## Risks", ""])
    lines.extend(f"- {item}" for item in decision.get("risks", []))
    if decision.get("next_experiment"):
        experiment = decision["next_experiment"]
        lines.extend(["", "## Next experiment", "", f"- Experiment id: `{experiment['experiment_id']}`", f"- Objective: {experiment['objective']}"])
    return "\n".join(lines).rstrip() + "\n"


def write_decision_markdown(repo_root: Path, project: str, iteration_id: str, decision: Dict[str, Any]) -> Path:
    path = project_dir(repo_root, project) / "decisions" / f"{iteration_id}_decision.md"
    path.write_text(decision_markdown(decision))
    return path


def write_plan(repo_root: Path, project: str, iteration_id: str, experiment: Dict[str, Any]) -> Tuple[Path, Path]:
    plans_dir = project_dir(repo_root, project) / "plans"
    plan_json = plans_dir / f"{iteration_id}_plan.json"
    plan_md = plans_dir / f"{iteration_id}_plan.md"
    json_dump(plan_json, experiment)

    success = "\n".join(f"- {item}" for item in experiment["success_criteria"])
    failure = "\n".join(f"- {item}" for item in experiment["failure_criteria"])
    tasks = "\n".join(f"- {item}" for item in experiment["tasks_for_codex"])
    outputs = "\n".join(f"- `{item}`" for item in experiment["required_outputs"])
    plan_md.write_text(
        f"# Experiment {iteration_id}\n\n"
        f"## Objective\n\n{experiment['objective']}\n\n"
        f"## Hypothesis\n\n{experiment['hypothesis']}\n\n"
        f"## Success criteria\n\n{success}\n\n"
        f"## Failure criteria\n\n{failure}\n\n"
        f"## Estimated runtime\n\n<= {experiment['estimated_runtime_minutes']} minutes\n\n"
        f"## Tasks for Codex\n\n{tasks}\n\n"
        f"## Required outputs\n\n{outputs}\n"
    )
    return plan_json, plan_md


def normalize_experiment_paths(project: str, iteration_id: str, experiment: Dict[str, Any]) -> Dict[str, Any]:
    normalized = dict(experiment)
    normalized["experiment_id"] = iteration_id
    normalized["required_outputs"] = [
        f"research/{project}/results/{iteration_id}_result.json",
        f"research/{project}/results/{iteration_id}_summary.md",
        f"research/{project}/artifacts/{iteration_id}/",
    ]
    return normalized


def result_paths(repo_root: Path, project: str, iteration_id: str) -> Tuple[Path, Path, Path]:
    root = project_dir(repo_root, project)
    return (
        root / "results" / f"{iteration_id}_result.json",
        root / "results" / f"{iteration_id}_summary.md",
        root / "artifacts" / iteration_id,
    )


def write_timeout_result(repo_root: Path, project: str, iteration_id: str) -> List[Path]:
    result_path, summary_path, artifact_dir = result_paths(repo_root, project, iteration_id)
    artifact_dir.mkdir(parents=True, exist_ok=True)
    data = {
        "experiment_id": iteration_id,
        "status": "timeout",
        "claim_tested": "Executor timed out before completing the experiment.",
        "commands_run": [],
        "metrics": {},
        "baseline_metrics": {},
        "artifacts": [],
        "interpretation": "The executor exceeded the configured timeout. Treat this as a failed or blocked small-scale experiment.",
        "known_failures": ["Executor timeout"],
        "next_questions": ["Can the experiment be reduced to a smaller validation?"],
    }
    json_dump(result_path, data)
    summary_path.write_text(
        f"# Experiment {iteration_id} Timeout\n\n"
        "The executor exceeded the configured timeout. No experimental claim should be accepted from this run.\n"
    )
    return [result_path, summary_path, artifact_dir]


def write_review_markdown(repo_root: Path, project: str, iteration_id: str, review: Dict[str, Any]) -> Path:
    path = project_dir(repo_root, project) / "reviews" / f"{iteration_id}_review.md"
    lines = [
        f"# Review {iteration_id}: {review['verdict']}",
        "",
        f"Allows auto-continue: {review['allows_auto_continue']}",
        "",
        "## Reasons",
        "",
    ]
    lines.extend(f"- {item}" for item in review.get("reasons", []))
    lines.extend(["", "## Required fixes", ""])
    lines.extend(f"- {item}" for item in review.get("required_fixes", []))
    lines.extend(["", "## Risk flags", ""])
    lines.extend(f"- {item}" for item in review.get("risk_flags", []))
    path.write_text("\n".join(lines).rstrip() + "\n")
    return path


def mark_human_required(state: Dict[str, Any], note: str, status: str = "paused") -> None:
    state["human_review_required"] = True
    state["status"] = status
    state.setdefault("notes", []).append(f"{utc_now_iso()}: {note}")


def update_state_after_review(
    state: Dict[str, Any],
    iteration: int,
    decision: Dict[str, Any],
    review: Dict[str, Any],
    max_no_progress_rounds: int,
) -> None:
    state["iteration"] = iteration
    state["last_decision"] = decision["decision"]
    verdict = review["verdict"]
    if verdict in ("pass", "weak_pass") and int(decision.get("progress_score", 0)) >= 5:
        state["no_progress_rounds"] = 0
    else:
        state["no_progress_rounds"] = int(state.get("no_progress_rounds", 0)) + 1

    if verdict in ("fail", "needs_human") or not bool(review.get("allows_auto_continue")):
        mark_human_required(state, f"reviewer verdict {verdict}", status="paused")
    elif int(state.get("no_progress_rounds", 0)) >= max_no_progress_rounds:
        mark_human_required(state, "no-progress limit reached", status="paused")
    else:
        state["status"] = "active"
        state["human_review_required"] = False


def pro_review_due(state: Dict[str, Any], config: Dict[str, Any]) -> bool:
    pro_cfg = config.get("chatgpt_pro", {})
    if not pro_cfg.get("enabled", False):
        return False
    cadence = int(pro_cfg.get("cadence_iterations", 3) or 3)
    if cadence not in (2, 3) and pro_cfg.get("allow_cadence_2_or_3", True):
        cadence = 3
    completed = int(state.get("iteration", 0))
    last = int(state.get("last_pro_review_iteration", 0))
    return completed > 0 and completed - last >= cadence


class Orchestrator:
    def __init__(self, repo_root: Path, config: Dict[str, Any], codex_bin: str = "codex") -> None:
        self.repo_root = repo_root
        self.config = config
        self.runner = CodexRunner(repo_root, config, codex_bin=codex_bin)
        self.git = GitManager(repo_root, config)
        self.codex_bin = codex_bin
        self._printed_gpu_sandbox_warning = False

    def _sandbox_for_role(self, role: str) -> str:
        cfg = role_config(self.config, role)
        sandbox = str(cfg.get("sandbox", "read-only"))
        env_cfg = self.config.get("environment", {})
        gpu_cfg = env_cfg.get("gpu", {}) if isinstance(env_cfg.get("gpu", {}), dict) else {}
        gpu_preferred = bool(gpu_cfg.get("prefer", False))
        escalation_required = bool(gpu_cfg.get("require_escalation_for_gpu_runs", False))
        auto_approve_requested = bool(gpu_cfg.get("auto_approve_escalation", False))
        setup_gpu = role == "setup_env" and bool(gpu_cfg.get("use_gpu_sandbox_for_setup", False))
        executor_gpu = role == "executor" and bool(gpu_cfg.get("use_gpu_sandbox_for_executor", False))
        if gpu_preferred and escalation_required and auto_approve_requested and (setup_gpu or executor_gpu):
            sandbox = str(cfg.get("gpu_sandbox", sandbox))
            if sandbox == "danger-full-access" and not self._printed_gpu_sandbox_warning:
                print(
                    "warning: GPU escalation policy selected Codex sandbox danger-full-access for setup/executor roles. "
                    "Outer approval is still controlled by the active Codex runtime.",
                    file=sys.stderr,
                )
                self._printed_gpu_sandbox_warning = True
        return sandbox

    def _run_role(
        self,
        project: str,
        role: str,
        iteration_id: str,
        packet: str,
        output_path: Path,
    ) -> CodexRunResult:
        cfg = role_config(self.config, role)
        prompt = prompt_for_role(self.repo_root, role, packet, iteration_id)
        return self.runner.run_role(
            project=project,
            role=role,
            prompt=prompt,
            output_path=output_path,
            schema_path=schema_for_role(self.repo_root, cfg),
            sandbox=self._sandbox_for_role(role),
            timeout_minutes=int(cfg.get("timeout_minutes", 15)),
            resume=True,
        )

    def _pause_for_failure(self, project: str, state: Dict[str, Any], note: str, paths: Iterable[Path]) -> None:
        mark_human_required(state, note, status="paused")
        state_path = save_project_state(self.repo_root, project, state)
        self.git.commit(list(paths) + [state_path], f"autoresearcher({project}): paused")

    def setup_environment(self, project: str) -> int:
        ensure_project_scaffold(self.repo_root, project)
        iteration_id = "0000"
        packet = build_context(self.repo_root, project, "setup_env")
        packet_path = write_packet(self.repo_root, project, iteration_id, "setup_env", packet)
        env_state_path = project_dir(self.repo_root, project) / "env_state.json"
        setup_result = self._run_role(project, "setup_env", iteration_id, packet, env_state_path)
        paths: List[Path] = [packet_path, setup_result.jsonl_log_path, setup_result.stderr_log_path, env_state_path]
        summary_path = project_dir(self.repo_root, project) / "setup_logs" / "setup_summary.md"
        if summary_path.exists():
            paths.append(summary_path)

        if setup_result.timed_out or setup_result.return_code != 0:
            print(
                f"stopping: setup_env failed or timed out; stderr log: {setup_result.stderr_log_path}",
                file=sys.stderr,
            )
            if setup_result.stderr_tail:
                print(setup_result.stderr_tail, file=sys.stderr)
            state = load_project_state(self.repo_root, project)
            self._pause_for_failure(
                project,
                state,
                f"setup_env failed or timed out; see {setup_result.stderr_log_path}",
                paths,
            )
            return 1

        try:
            validate_json_schema(env_state_path, self.repo_root / "schemas" / "env_setup.schema.json")
            env_state = load_json(env_state_path)
        except ValidationError as exc:
            state = load_project_state(self.repo_root, project)
            self._pause_for_failure(project, state, f"invalid environment setup output: {exc}", paths)
            return 1

        self.git.commit(paths, f"autoresearcher({project}): setup environment")

        if env_state.get("status") != "ready":
            state = load_project_state(self.repo_root, project)
            mark_human_required(state, f"environment setup status {env_state.get('status')}", status="paused")
            state_path = save_project_state(self.repo_root, project, state)
            self.git.commit(paths + [state_path], f"autoresearcher({project}): setup blocked")
            print(f"stopping: environment setup status {env_state.get('status')}")
            return 2

        print(f"environment ready: {env_state.get('conda_env_name')}")
        return 0

    def run(self, project: str, max_iters: int, skip_model_check: bool = False) -> int:
        ensure_project_scaffold(self.repo_root, project)
        if not skip_model_check:
            check_model_available(self.repo_root, self.config, codex_bin=self.codex_bin)

        env_required = bool(self.config.get("environment", {}).get("require_ready_before_run", True))
        env_required = env_required or bool(self.config.get("loop", {}).get("require_environment_ready", True))
        if env_required and not env_is_ready(self.repo_root, project):
            setup_rc = self.setup_environment(project)
            if setup_rc != 0:
                return setup_rc

        completed_this_run = 0
        for _ in range(max_iters):
            state = load_project_state(self.repo_root, project)
            loop_cfg = self.config.get("loop", {})
            if state.get("status") != "active":
                print(f"stopping: project status is {state.get('status')}")
                break
            if state.get("human_review_required"):
                print("stopping: human_review_required is true")
                break
            if int(state.get("iteration", 0)) >= int(loop_cfg.get("max_iterations", 12)):
                print("stopping: configured max_iterations reached")
                break
            if pro_review_due(state, self.config):
                mark_human_required(state, "ChatGPT Pro review is due, but Phase 2 backend is not implemented.", status="paused")
                state_path = save_project_state(self.repo_root, project, state)
                self.git.commit([state_path], f"autoresearcher({project}): pro review due")
                print("stopping: ChatGPT Pro review due; Phase 2 backend is not implemented")
                break

            iteration = int(state.get("iteration", 0)) + 1
            iteration_id = f"{iteration:04d}"

            supervisor_packet = build_context(self.repo_root, project, "supervisor")
            supervisor_packet += f"\n\n## Next experiment id\n\nUse `{iteration_id}` as the exact `next_experiment.experiment_id` if you choose continue.\n"
            if int(state.get("iteration", 0)) == 0:
                supervisor_packet += (
                    "\n\n## First-iteration rule\n\n"
                    "No prior result is expected for iteration 0. Do not choose needs_human solely because latest result, summary, and review are missing.\n"
                )
            supervisor_packet_path = write_packet(self.repo_root, project, iteration_id, "supervisor", supervisor_packet)
            decision_path = project_dir(self.repo_root, project) / "decisions" / f"{iteration_id}_decision.json"
            supervisor_result = self._run_role(project, "supervisor", iteration_id, supervisor_packet, decision_path)
            if supervisor_result.timed_out or supervisor_result.return_code != 0:
                print(
                    f"stopping: supervisor failed or timed out; stderr log: {supervisor_result.stderr_log_path}",
                    file=sys.stderr,
                )
                if supervisor_result.stderr_tail:
                    print(supervisor_result.stderr_tail, file=sys.stderr)
                self._pause_for_failure(
                    project,
                    state,
                    f"supervisor failed or timed out; see {supervisor_result.stderr_log_path}",
                    [supervisor_packet_path, supervisor_result.jsonl_log_path, supervisor_result.stderr_log_path],
                )
                return 1

            try:
                validate_json_schema(decision_path, self.repo_root / "schemas" / "decision.schema.json")
                decision = load_json(decision_path)
            except ValidationError as exc:
                self._pause_for_failure(project, state, f"invalid supervisor decision: {exc}", [supervisor_packet_path, decision_path])
                return 1

            decision_md = write_decision_markdown(self.repo_root, project, iteration_id, decision)
            self.git.commit(
                [supervisor_packet_path, decision_path, decision_md],
                f"autoresearcher({project}): decision {iteration_id}",
            )

            if decision["decision"] in ("pivot", "stop", "needs_human"):
                state["last_decision"] = decision["decision"]
                if decision["decision"] == "stop":
                    state["status"] = "stopped"
                else:
                    mark_human_required(state, f"supervisor decision {decision['decision']}", status="paused")
                state_path = save_project_state(self.repo_root, project, state)
                self.git.commit([decision_path, decision_md, state_path], f"autoresearcher({project}): pause {iteration_id}")
                print(f"stopping: supervisor decision {decision['decision']}")
                break

            experiment = decision.get("next_experiment")
            if not isinstance(experiment, dict):
                self._pause_for_failure(project, state, "continue decision had no next_experiment", [decision_path])
                return 1
            experiment = normalize_experiment_paths(project, iteration_id, experiment)
            plan_json, plan_md = write_plan(self.repo_root, project, iteration_id, experiment)
            self.git.commit([plan_json, plan_md], f"autoresearcher({project}): plan {iteration_id}")

            executor_packet = build_context(self.repo_root, project, "executor", plan=plan_md)
            executor_packet_path = write_packet(self.repo_root, project, iteration_id, "executor", executor_packet)
            executor_output = self.repo_root / ".autoresearcher" / "runs" / project / f"{iteration_id}_executor_last_message.md"
            executor_result = self._run_role(project, "executor", iteration_id, executor_packet, executor_output)
            result_path, summary_path, artifact_dir = result_paths(self.repo_root, project, iteration_id)

            if executor_result.timed_out:
                written = write_timeout_result(self.repo_root, project, iteration_id)
                validate_json_schema(result_path, self.repo_root / "schemas" / "result.schema.json")
                state["iteration"] = iteration
                state["last_decision"] = "timeout"
                state["no_progress_rounds"] = int(state.get("no_progress_rounds", 0)) + 1
                if self.config.get("loop", {}).get("stop_on_timeout", True):
                    mark_human_required(state, "executor timeout", status="paused")
                state_path = save_project_state(self.repo_root, project, state)
                self.git.commit(written + [executor_packet_path, state_path], f"autoresearcher({project}): timeout {iteration_id}")
                print("stopping: executor timeout")
                break

            try:
                validate_required_result_files(self.repo_root, project, iteration)
                validate_json_schema(result_path, self.repo_root / "schemas" / "result.schema.json")
                validate_result_artifact_paths(self.repo_root, result_path)
            except ValidationError as exc:
                if self.config.get("loop", {}).get("stop_on_missing_result", True):
                    self._pause_for_failure(
                        project,
                        state,
                        f"missing or invalid result for {iteration_id}: {exc}",
                        [executor_packet_path, executor_result.jsonl_log_path, result_path, summary_path],
                    )
                    print(f"stopping: missing or invalid result: {exc}")
                    return 1
                raise

            self.git.commit(
                [executor_packet_path, result_path, summary_path, artifact_dir],
                f"autoresearcher({project}): result {iteration_id}",
            )

            reviewer_packet = build_context(self.repo_root, project, "reviewer")
            reviewer_packet_path = write_packet(self.repo_root, project, iteration_id, "reviewer", reviewer_packet)
            review_path = project_dir(self.repo_root, project) / "reviews" / f"{iteration_id}_review.json"
            reviewer_result = self._run_role(project, "reviewer", iteration_id, reviewer_packet, review_path)
            if reviewer_result.timed_out or reviewer_result.return_code != 0:
                print(
                    f"stopping: reviewer failed or timed out; stderr log: {reviewer_result.stderr_log_path}",
                    file=sys.stderr,
                )
                if reviewer_result.stderr_tail:
                    print(reviewer_result.stderr_tail, file=sys.stderr)
                self._pause_for_failure(
                    project,
                    state,
                    f"reviewer failed or timed out; see {reviewer_result.stderr_log_path}",
                    [reviewer_packet_path, reviewer_result.jsonl_log_path, reviewer_result.stderr_log_path],
                )
                return 1

            try:
                validate_json_schema(review_path, self.repo_root / "schemas" / "review.schema.json")
                review = load_json(review_path)
            except ValidationError as exc:
                self._pause_for_failure(project, state, f"invalid reviewer output: {exc}", [reviewer_packet_path, review_path])
                return 1

            review_md = write_review_markdown(self.repo_root, project, iteration_id, review)
            self.git.commit([reviewer_packet_path, review_path, review_md], f"autoresearcher({project}): review {iteration_id}")

            update_state_after_review(
                state,
                iteration=iteration,
                decision=decision,
                review=review,
                max_no_progress_rounds=int(loop_cfg.get("max_no_progress_rounds", 3)),
            )
            state_path = save_project_state(self.repo_root, project, state)
            self.git.commit([state_path], f"autoresearcher({project}): state after {iteration_id}")
            completed_this_run += 1

            if state.get("human_review_required") or state.get("status") != "active":
                print("stopping: reviewer/state requires pause")
                break

        print(f"completed_iterations_this_run={completed_this_run}")
        return 0


def reset_role_session(repo_root: Path, project: str, role: str) -> None:
    if role not in ROLE_NAMES:
        raise RuntimeError(f"unknown role {role!r}; expected one of {', '.join(ROLE_NAMES)}")
    state = load_local_state(repo_root, project)
    state["projects"][project]["codex_sessions"][role] = {"session_id": None, "last_used_at": None}
    save_local_state(repo_root, state)


def print_status(repo_root: Path, project: str) -> None:
    ensure_project_scaffold(repo_root, project)
    project_state = load_project_state(repo_root, project)
    env_state = load_env_state(repo_root, project)
    local_state = load_local_state(repo_root, project)["projects"][project]
    print(json.dumps({"project": project, "state": project_state, "environment": env_state, "local": local_state}, indent=2, sort_keys=True))


def build_pro_packet(repo_root: Path, project: str) -> Path:
    ensure_project_scaffold(repo_root, project)
    state = load_project_state(repo_root, project)
    iteration_id = f"{int(state.get('iteration', 0)) + 1:04d}"
    packet = build_context(repo_root, project, "chatgpt_pro")
    path = project_dir(repo_root, project) / "packets" / f"{iteration_id}_PRO_REVIEW_PACKET.md"
    path.write_text(packet)
    return path


def pro_smoke(repo_root: Path, project: str, config: Dict[str, Any]) -> int:
    ensure_project_scaffold(repo_root, project)
    if not config.get("chatgpt_pro", {}).get("enabled", False):
        print("chatgpt_pro.enabled=false; Phase 1 does not require Pro bridge dependencies.")
        return 0
    packet_path = build_pro_packet(repo_root, project)
    blocker = project_dir(repo_root, project) / "decisions" / "pro_bridge_not_implemented_blocker.md"
    blocker.write_text(
        "# Pro Bridge Blocker\n\n"
        "ChatGPT Pro support belongs to Phase 2. Phase 1 wrote a packet but did not send it.\n"
        f"Packet: `{packet_path.relative_to(repo_root).as_posix()}`\n"
    )
    state = load_project_state(repo_root, project)
    mark_human_required(state, "ChatGPT Pro bridge requested before Phase 2 implementation", status="paused")
    save_project_state(repo_root, project, state)
    print(f"Phase 2 Pro bridge is not implemented. Wrote {blocker}")
    return 2


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Run the Codex-only autoresearcher loop.")
    parser.add_argument("--repo-root", type=Path, default=None)
    parser.add_argument("--codex-bin", default="codex")
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_p = subparsers.add_parser("init", help="Create project scaffold and local state.")
    init_p.add_argument("--project", default=None)

    setup_p = subparsers.add_parser("setup-env", help="Create and verify the project conda environment.")
    setup_p.add_argument("--project", default=None)
    setup_p.add_argument("--skip-model-check", action="store_true", help="Testing only: skip `codex debug models`.")

    run_p = subparsers.add_parser("run", help="Run supervisor -> executor -> reviewer loop.")
    run_p.add_argument("--project", default=None)
    run_p.add_argument("--max-iters", type=int, default=1)
    run_p.add_argument("--skip-model-check", action="store_true", help="Testing only: skip `codex debug models`.")

    context_p = subparsers.add_parser("build-context", help="Print a role context packet.")
    context_p.add_argument("--project", default=None)
    context_p.add_argument("--role", required=True, choices=ROLE_CHOICES)
    context_p.add_argument("--plan", type=Path)

    reset_p = subparsers.add_parser("reset-role-session", help="Clear stored Codex session id for one role.")
    reset_p.add_argument("--project", default=None)
    reset_p.add_argument("--role", required=True, choices=ROLE_NAMES)

    status_p = subparsers.add_parser("status", help="Print project state and local role sessions.")
    status_p.add_argument("--project", default=None)

    pro_p = subparsers.add_parser("pro-smoke", help="Phase 2 stub: verify Pro is disabled or write blocker.")
    pro_p.add_argument("--project", default=None)

    packet_p = subparsers.add_parser("build-pro-packet", help="Build a ChatGPT Pro review packet.")
    packet_p.add_argument("--project", default=None)

    args = parser.parse_args(argv)
    repo_root = repo_root_from(args.repo_root).resolve() if args.repo_root else repo_root_from().resolve()
    config = load_config(repo_root)
    project = getattr(args, "project", None) or str(config.get("project_default", "project_001"))

    if args.command == "init":
        ensure_project_scaffold(repo_root, project)
        env_state = load_env_state(repo_root, project)
        print(f"initialized {project} with conda env {env_state.get('conda_env_name')}")
        return 0
    if args.command == "setup-env":
        if not args.skip_model_check:
            check_model_available(repo_root, config, codex_bin=args.codex_bin)
        return Orchestrator(repo_root, config, codex_bin=args.codex_bin).setup_environment(project)
    if args.command == "run":
        if args.max_iters < 1:
            parser.error("--max-iters must be >= 1")
        return Orchestrator(repo_root, config, codex_bin=args.codex_bin).run(
            project,
            max_iters=args.max_iters,
            skip_model_check=args.skip_model_check,
        )
    if args.command == "build-context":
        print(build_context(repo_root, project, args.role, plan=args.plan), end="")
        return 0
    if args.command == "reset-role-session":
        reset_role_session(repo_root, project, args.role)
        print(f"reset {project}:{args.role}")
        return 0
    if args.command == "status":
        print_status(repo_root, project)
        return 0
    if args.command == "pro-smoke":
        return pro_smoke(repo_root, project, config)
    if args.command == "build-pro-packet":
        path = build_pro_packet(repo_root, project)
        print(path)
        return 0
    parser.error(f"unknown command {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
