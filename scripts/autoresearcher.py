#!/usr/bin/env python3
"""Codex-only Phase 1 autoresearcher orchestrator."""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
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
from chatgpt_pro_bridge import write_pro_blocker  # noqa: E402
from checkpoint_policy import pro_checkpoint_due, pro_review_due  # noqa: E402
from metrics_ledger import write_metric_ledger  # noqa: E402
from supervisor_backends import SupervisorBackendResult, supervisor_backend_for_config  # noqa: E402
from validate_artifacts import (  # noqa: E402
    ValidationError,
    load_json,
    validate_json_schema,
    validate_required_result_files,
    validate_result_artifact_paths,
)
from worktree_guard import protected_file_drift, write_guard_report  # noqa: E402


ROLE_NAMES = ("setup_env", "supervisor", "executor", "reviewer", "summarizer")
LOCAL_STATE_PATH = Path(".autoresearcher") / "local_state.json"


DEFAULT_STATE: Dict[str, Any] = {
    "iteration": 0,
    "status": "active",
    "last_decision": "start",
    "primary_metric": None,
    "best_primary_metric": None,
    "no_progress_rounds": 0,
    "failure_streak": 0,
    "last_failure": None,
    "human_review_required": False,
    "last_pro_review_iteration": 0,
    "last_pro_review_path": None,
    "pro_review_count": 0,
    "pending_checkpoint": None,
    "pending_local_decision_path": None,
    "last_summary_iteration": 0,
    "last_summary_path": None,
    "weak_pass_streak": 0,
    "protected_file_drift": False,
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
  speed: Fast
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

  summarizer:
    sandbox: read-only
    output_schema: null
    timeout_minutes: 15

loop:
  max_iterations: 30
  max_no_progress_rounds: 3
  max_failure_attempts: 3
  require_environment_ready: true
  require_human_for_pivot: false
  require_human_for_expensive_run: true
  require_human_for_publishable_claim: true
  stop_on_missing_result: true
  stop_on_invalid_schema: true
  stop_on_timeout: true

summary:
  enabled: true
  cadence_iterations: 3
  on_stop: true
  write_latest: true

git:
  enabled: true
  commit: true
  push: false
  remote: origin
  branch: null

chatgpt_pro:
  enabled: false
  backend: codex-chatgpt-control
  bridge_conda_env: python312
  backend_command: null
  backend_http_url: null
  relay_script: null
  cdp_url: http://127.0.0.1:9222
  cdp_ready_timeout_seconds: 120
  cdp_response_timeout_seconds: 600
  cadence_iterations: 3
  allow_cadence_2_or_3: true
  thread_url: null
  use_existing_thread: true
  allow_new_thread: false
  existing_tab: true
  require_visible_session: true
  require_user_approved_prompt: true
  require_model: GPT-5.5 Pro
  require_thinking: Extended
  fail_if_unavailable: true
  allow_model_fallback: false
  max_retries: 0

context:
  max_source_doc_chars: 12000
  max_result_chars: 8000
  recent_iterations_for_pro: 3

safety:
  allow_executor_to_modify_orchestrator: false

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


def codex_service_tier(codex_cfg: Dict[str, Any]) -> Optional[str]:
    configured = codex_cfg.get("service_tier")
    if isinstance(configured, str) and configured.strip():
        return configured.strip()
    speed = codex_cfg.get("speed")
    if not isinstance(speed, str) or not speed.strip():
        return None
    normalized = speed.strip().lower()
    if normalized == "fast":
        return "priority"
    if normalized in {"default", "standard", "auto", "none"}:
        return None
    return speed.strip()


def project_dir(repo_root: Path, project: str) -> Path:
    return repo_root / "research" / project


def ensure_project_scaffold(repo_root: Path, project: str) -> None:
    root = project_dir(repo_root, project)
    config = load_config(repo_root)
    env_cfg = config.get("environment", {})
    env_prefix = str(env_cfg.get("env_name_prefix", "autoresearcher"))
    python_version = str(env_cfg.get("default_python", "3.11"))
    env_name = conda_env_name_for_project(project, prefix=env_prefix)
    for subdir in ("plans", "results", "reviews", "decisions", "packets", "pro_packets", "artifacts", "setup_logs", "progress"):
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
    for key, value in DEFAULT_STATE.items():
        if key not in state:
            if isinstance(value, list):
                state[key] = list(value)
            elif isinstance(value, dict):
                state[key] = dict(value)
            else:
                state[key] = value
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

    def clear_role_session_id(self, project: str, role: str) -> None:
        state = load_local_state(self.repo_root, project)
        state["projects"][project]["codex_sessions"][role] = {
            "session_id": None,
            "last_used_at": None,
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
        service_tier = codex_service_tier(codex_cfg)
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
        if service_tier:
            cmd.extend(["-c", f"service_tier={service_tier}"])
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

    def _is_ignored(self, rel_path: str) -> bool:
        proc = self._git(["check-ignore", "-q", "--", rel_path])
        return proc.returncode == 0

    def _trackable_rel_paths(self, paths: Iterable[Path]) -> List[str]:
        root = self.repo_root.resolve()
        rel_paths = []
        seen = set()

        def add_path(path: Path) -> None:
            try:
                rel_path = str(path.resolve().relative_to(root))
            except ValueError:
                return
            if rel_path in seen or self._is_ignored(rel_path):
                return
            seen.add(rel_path)
            rel_paths.append(rel_path)

        for path in paths:
            if not path.exists():
                continue
            if path.is_dir():
                for child in sorted(path.rglob("*")):
                    if child.is_file() or child.is_symlink():
                        add_path(child)
            elif path.is_file() or path.is_symlink():
                add_path(path)
        return rel_paths

    def commit(self, paths: Iterable[Path], message: str) -> bool:
        if not self.enabled() or not self.is_repo():
            return False
        rel_paths = self._trackable_rel_paths(paths)
        if not rel_paths:
            return False
        status = self._git(["status", "--porcelain", "--"] + rel_paths)
        if status.returncode != 0 or not status.stdout.strip():
            return False
        add = self._git(["add", "--"] + rel_paths)
        if add.returncode != 0:
            raise RuntimeError(f"git add failed:\n{add.stderr}")
        commit = self._git(["commit", "-m", message, "--"] + rel_paths)
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


def plan_paths(repo_root: Path, project: str, iteration_id: str) -> Tuple[Path, Path]:
    plans_dir = project_dir(repo_root, project) / "plans"
    return plans_dir / f"{iteration_id}_plan.json", plans_dir / f"{iteration_id}_plan.md"


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


def progress_summary_paths(repo_root: Path, project: str, iteration_id: str, reason: str) -> Tuple[Path, Path]:
    safe_reason = "".join(ch if ch.isalnum() else "_" for ch in reason.lower()).strip("_") or "manual"
    root = project_dir(repo_root, project) / "progress"
    return root / f"{iteration_id}_{safe_reason}_summary.md", root / "latest_summary.md"


def summary_due(state: Dict[str, Any], config: Dict[str, Any], reason: str) -> bool:
    summary_cfg = config.get("summary", {})
    if not summary_cfg.get("enabled", True):
        return False
    completed = int(state.get("iteration", 0))
    if completed <= 0:
        return False
    last_summary = int(state.get("last_summary_iteration", 0) or 0)
    if reason in ("stop", "final"):
        return bool(summary_cfg.get("on_stop", True)) and last_summary < completed
    cadence = int(summary_cfg.get("cadence_iterations", 3) or 0)
    return cadence > 0 and completed - last_summary >= cadence


def write_timeout_result(repo_root: Path, project: str, iteration_id: str) -> List[Path]:
    result_path, summary_path, artifact_dir = result_paths(repo_root, project, iteration_id)
    artifact_dir.mkdir(parents=True, exist_ok=True)
    diagnostic_path = artifact_dir / "timeout_diagnostics.md"
    diagnostic_path.write_text(
        f"# Experiment {iteration_id} Timeout Diagnostics\n\n"
        "Status: timeout.\n\n"
        "The executor exceeded the configured timeout before completing the experiment. "
        "No experimental claim should be accepted from this iteration.\n\n"
        "The orchestrator wrote this artifact so the timeout has a trackable artifact path "
        "and the retry record can be committed even when the executor produced no files.\n"
    )
    diagnostic_rel = str(diagnostic_path.relative_to(repo_root))
    data = {
        "experiment_id": iteration_id,
        "status": "timeout",
        "claim_tested": "Executor timed out before completing the experiment.",
        "commands_run": [],
        "metrics": {},
        "baseline_metrics": {},
        "artifacts": [diagnostic_rel],
        "interpretation": "The executor exceeded the configured timeout. Treat this as a failed or blocked small-scale experiment.",
        "known_failures": ["Executor timeout"],
        "next_questions": ["Can the experiment be reduced to a smaller validation?"],
    }
    json_dump(result_path, data)
    summary_path.write_text(
        f"# Experiment {iteration_id} Timeout\n\n"
        "The executor exceeded the configured timeout. No experimental claim should be accepted from this run.\n"
    )
    return [result_path, summary_path, diagnostic_path]


def should_retry_existing_result(result: Dict[str, Any], state: Dict[str, Any]) -> bool:
    if state.get("last_decision") != "retryable_failure":
        return False
    return result.get("status") in {"timeout", "failed", "blocked"}


def archive_existing_result_for_retry(
    repo_root: Path,
    project: str,
    iteration_id: str,
    state: Dict[str, Any],
) -> List[Path]:
    result_path, summary_path, artifact_dir = result_paths(repo_root, project, iteration_id)
    last_failure = state.get("last_failure") if isinstance(state.get("last_failure"), dict) else {}
    attempt = int(last_failure.get("attempt") or state.get("failure_streak") or 1)
    archive_dir = artifact_dir / "retry_attempts" / f"attempt_{max(1, attempt):02d}"
    archive_dir.mkdir(parents=True, exist_ok=True)

    written: List[Path] = []
    if result_path.exists():
        archived_result = archive_dir / result_path.name
        shutil.copy2(result_path, archived_result)
        written.append(archived_result)
    if summary_path.exists():
        archived_summary = archive_dir / summary_path.name
        shutil.copy2(summary_path, archived_summary)
        written.append(archived_summary)

    manifest_path = archive_dir / "manifest.json"
    manifest = {
        "project": project,
        "iteration_id": iteration_id,
        "archived_at": utc_now_iso(),
        "reason": "retry_existing_result",
        "last_failure": last_failure,
        "archived_paths": [str(path.relative_to(repo_root)) for path in written],
    }
    json_dump(manifest_path, manifest)
    written.append(manifest_path)
    return written


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


def reset_failure_streak(state: Dict[str, Any]) -> None:
    state["failure_streak"] = 0
    state["last_failure"] = None


def record_retryable_failure(state: Dict[str, Any], note: str, max_failure_attempts: int) -> bool:
    max_failure_attempts = max(1, max_failure_attempts)
    failure_streak = int(state.get("failure_streak", 0)) + 1
    state["failure_streak"] = failure_streak
    state["last_decision"] = "retryable_failure"
    state["last_failure"] = {
        "at": utc_now_iso(),
        "attempt": failure_streak,
        "max_attempts": max_failure_attempts,
        "note": note,
    }
    if failure_streak >= max_failure_attempts:
        mark_human_required(
            state,
            f"retry limit reached after {failure_streak}/{max_failure_attempts} failures: {note}",
            status="paused",
        )
        return True

    state["status"] = "active"
    state["human_review_required"] = False
    state.setdefault("notes", []).append(
        f"{utc_now_iso()}: retryable failure {failure_streak}/{max_failure_attempts}: {note}"
    )
    return False


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
    # progress_score belongs to the pre-experiment supervisor turn; the reviewer
    # verdict is the completed experiment's signal for whether the loop advanced.
    made_progress = verdict in ("pass", "weak_pass") and bool(review.get("allows_auto_continue"))
    if made_progress:
        state["no_progress_rounds"] = 0
        reset_failure_streak(state)
    else:
        state["no_progress_rounds"] = int(state.get("no_progress_rounds", 0)) + 1

    if verdict == "weak_pass" and bool(review.get("allows_auto_continue")):
        state["weak_pass_streak"] = int(state.get("weak_pass_streak", 0) or 0) + 1
    elif verdict == "pass":
        state["weak_pass_streak"] = 0

    if verdict in ("fail", "needs_human") or not bool(review.get("allows_auto_continue")):
        mark_human_required(state, f"reviewer verdict {verdict}", status="paused")
    elif int(state.get("no_progress_rounds", 0)) >= max_no_progress_rounds:
        mark_human_required(state, "no-progress limit reached", status="paused")
    else:
        state["status"] = "active"
        state["human_review_required"] = False


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

    def _record_retryable_failure(
        self,
        project: str,
        state: Dict[str, Any],
        iteration_id: str,
        note: str,
        paths: Iterable[Path],
    ) -> bool:
        loop_cfg = self.config.get("loop", {})
        max_attempts = int(loop_cfg.get("max_failure_attempts", 3))
        paused = record_retryable_failure(state, note, max_attempts)
        state_path = save_project_state(self.repo_root, project, state)
        paths_to_commit = list(paths) + [state_path]
        if paused:
            self.git.commit(paths_to_commit, f"autoresearcher({project}): paused after {iteration_id} failure")
            print(
                f"stopping: retry limit reached ({state['failure_streak']}/{max(1, max_attempts)}): {note}"
            )
        else:
            self.git.commit(paths_to_commit, f"autoresearcher({project}): retry {iteration_id}")
            print(f"retrying {iteration_id}: failure {state['failure_streak']}/{max(1, max_attempts)}: {note}")
        return paused

    def _reset_role_session_on_context_overflow(self, project: str, result: CodexRunResult) -> None:
        text = f"{result.stdout_tail}\n{result.stderr_tail}".lower()
        if "context window" not in text and "ran out of room" not in text:
            return
        self.runner.clear_role_session_id(project, result.role)
        print(f"resetting {result.role} Codex session after context-window failure")

    def _run_summary_agent(
        self,
        project: str,
        state: Dict[str, Any],
        reason: str,
        force: bool = False,
    ) -> Optional[Path]:
        if not force and not summary_due(state, self.config, reason):
            return None
        iteration = int(state.get("iteration", 0))
        if iteration <= 0:
            return None
        iteration_id = f"{iteration:04d}"
        output_path, latest_path = progress_summary_paths(self.repo_root, project, iteration_id, reason)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        packet = build_context(self.repo_root, project, "summarizer")
        packet_path = write_packet(self.repo_root, project, iteration_id, "summarizer", packet)
        result = self._run_role(project, "summarizer", iteration_id, packet, output_path)
        if result.timed_out or result.return_code != 0 or not output_path.exists():
            print(
                f"warning: summarizer failed or timed out; stderr log: {result.stderr_log_path}",
                file=sys.stderr,
            )
            self._reset_role_session_on_context_overflow(project, result)
            self.git.commit([packet_path, result.jsonl_log_path, result.stderr_log_path], f"autoresearcher({project}): summary failed {iteration_id}")
            return None

        paths = [packet_path, output_path]
        if bool(self.config.get("summary", {}).get("write_latest", True)):
            latest_path.write_text(output_path.read_text())
            paths.append(latest_path)
        state["last_summary_iteration"] = iteration
        state["last_summary_path"] = str(output_path.relative_to(self.repo_root))
        state_path = save_project_state(self.repo_root, project, state)
        paths.append(state_path)
        self.git.commit(paths, f"autoresearcher({project}): summary {iteration_id}")
        print(f"wrote progress summary: {output_path.relative_to(self.repo_root)}")
        return output_path

    def _block_pro_checkpoint_for_summary_failure(
        self,
        project: str,
        state: Dict[str, Any],
        reason: str,
        message: str,
        details: Optional[Dict[str, Any]] = None,
    ) -> SupervisorBackendResult:
        iteration_id = next_pro_review_id(self.repo_root, project, state)
        blocker_json, blocker_md = write_pro_blocker(
            self.repo_root,
            project,
            iteration_id,
            "summary_failed",
            message,
            details=details,
        )
        mark_human_required(state, message, status="paused")
        state["pending_checkpoint"] = {
            "type": "chatgpt_pro",
            "reason": reason,
            "iteration_id": iteration_id,
            "status": "blocked",
            "manual_fallback": True,
            "blocker_path": str(blocker_json.relative_to(self.repo_root)),
        }
        state.setdefault("notes", []).append(f"{utc_now_iso()}: Pro checkpoint blocked before GPT call: {message}")
        state_path = save_project_state(self.repo_root, project, state)
        try:
            self.git.commit(
                [blocker_json, blocker_md, state_path],
                f"autoresearcher({project}): Pro summary blocker {iteration_id}",
            )
        except RuntimeError as exc:
            print(f"warning: failed to commit/push Pro summary blocker: {exc}", file=sys.stderr)
        return SupervisorBackendResult(
            status="blocked",
            blocker_path=blocker_json,
            blocker_markdown_path=blocker_md,
            reason="summary_failed",
        )

    def _handle_pro_checkpoint(
        self,
        project: str,
        state: Dict[str, Any],
        reason: str,
        local_decision_path: Optional[Path] = None,
    ) -> SupervisorBackendResult:
        if int(state.get("iteration", 0) or 0) > 0:
            summary_reason = f"pre_pro_{reason}"
            try:
                summary_path = self._run_summary_agent(project, state, reason=summary_reason, force=True)
            except RuntimeError as exc:
                return self._block_pro_checkpoint_for_summary_failure(
                    project,
                    state,
                    reason,
                    "Pre-Pro summary could not be committed or pushed; not calling GPT-5.5-Pro.",
                    details={"summary_reason": summary_reason, "error": str(exc)},
                )
            if summary_path is None:
                return self._block_pro_checkpoint_for_summary_failure(
                    project,
                    state,
                    reason,
                    "Pre-Pro summary failed or was not written; not calling GPT-5.5-Pro.",
                    details={"summary_reason": summary_reason},
                )
            print(f"pre-Pro summary ready: {summary_path.relative_to(self.repo_root)}")

        result = run_pro_review(
            self.repo_root,
            project,
            self.config,
            reason=reason,
            backend_override="auto",
            local_decision_path=local_decision_path,
        )
        if result.status == "completed":
            state_path = apply_pro_decision(self.repo_root, project)
            state_after = load_project_state(self.repo_root, project)
            print(
                "Pro decision applied; "
                f"state={state_after.get('status')} path={state_path.relative_to(self.repo_root)}"
            )
        else:
            blocker = result.blocker_path.relative_to(self.repo_root) if result.blocker_path else "unknown"
            print(f"stopping: Pro checkpoint blocked ({result.reason}); blocker: {blocker}")
        return result

    def _review_iteration_result(
        self,
        project: str,
        state: Dict[str, Any],
        iteration: int,
        iteration_id: str,
        decision: Dict[str, Any],
        result_path: Path,
        summary_path: Path,
        artifact_dir: Path,
    ) -> str:
        reviewer_packet = build_context(self.repo_root, project, "reviewer")
        reviewer_packet_path = write_packet(self.repo_root, project, iteration_id, "reviewer", reviewer_packet)
        review_path = project_dir(self.repo_root, project) / "reviews" / f"{iteration_id}_review.json"
        reviewer_result = self._run_role(project, "reviewer", iteration_id, reviewer_packet, review_path)
        if reviewer_result.timed_out or reviewer_result.return_code != 0:
            print(
                f"reviewer failed or timed out; stderr log: {reviewer_result.stderr_log_path}",
                file=sys.stderr,
            )
            if reviewer_result.stderr_tail:
                print(reviewer_result.stderr_tail, file=sys.stderr)
            self._reset_role_session_on_context_overflow(project, reviewer_result)
            paused = self._record_retryable_failure(
                project,
                state,
                iteration_id,
                f"reviewer failed or timed out; see {reviewer_result.stderr_log_path}",
                [reviewer_packet_path, reviewer_result.jsonl_log_path, reviewer_result.stderr_log_path, review_path],
            )
            return "paused" if paused else "retry"

        try:
            validate_json_schema(review_path, self.repo_root / "schemas" / "review.schema.json")
            review = load_json(review_path)
        except ValidationError as exc:
            paused = self._record_retryable_failure(
                project,
                state,
                iteration_id,
                f"invalid reviewer output: {exc}",
                [reviewer_packet_path, reviewer_result.jsonl_log_path, reviewer_result.stderr_log_path, review_path],
            )
            return "paused" if paused else "retry"

        review_md = write_review_markdown(self.repo_root, project, iteration_id, review)
        self.git.commit([reviewer_packet_path, review_path, review_md], f"autoresearcher({project}): review {iteration_id}")

        verdict = review["verdict"]
        if verdict in ("fail", "needs_human") or not bool(review.get("allows_auto_continue")):
            paused = self._record_retryable_failure(
                project,
                state,
                iteration_id,
                f"reviewer verdict {verdict}",
                [reviewer_packet_path, review_path, review_md, result_path, summary_path, artifact_dir],
            )
            return "paused" if paused else "retry"

        update_state_after_review(
            state,
            iteration=iteration,
            decision=decision,
            review=review,
            max_no_progress_rounds=int(self.config.get("loop", {}).get("max_no_progress_rounds", 3)),
        )
        state_path = save_project_state(self.repo_root, project, state)
        self.git.commit([state_path], f"autoresearcher({project}): state after {iteration_id}")
        metric_json, metric_md = write_metric_ledger(self.repo_root, project)
        self.git.commit([metric_json, metric_md], f"autoresearcher({project}): metric ledger after {iteration_id}")
        try:
            latest_result = load_json(result_path)
        except ValidationError:
            latest_result = {}
        checkpoint, reason = pro_checkpoint_due(
            state,
            self.config,
            local_decision=decision,
            latest_review=review,
            latest_result=latest_result,
        )
        if checkpoint:
            self._handle_pro_checkpoint(project, state, reason)
            return "checkpoint"
        self._run_summary_agent(project, state, reason="progress")
        return "completed"

    def _decision_for_existing_result(self, project: str, iteration_id: str) -> Dict[str, Any]:
        decision_path = project_dir(self.repo_root, project) / "decisions" / f"{iteration_id}_decision.json"
        try:
            decision = load_json(decision_path)
        except ValidationError:
            decision = {}
        if isinstance(decision, dict) and decision.get("decision") in ("continue", "pivot"):
            return decision
        return {
            "decision": "continue",
            "progress_score": 0,
            "rationale": "Synthetic decision for retrying review of an existing valid result.",
        }

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
            self._reset_role_session_on_context_overflow(project, setup_result)
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

    def _inactive_checkpoint_reason(self, state: Dict[str, Any]) -> Optional[str]:
        pro_cfg = self.config.get("chatgpt_pro", {}) if isinstance(self.config.get("chatgpt_pro"), dict) else {}
        backend_available = bool(pro_cfg.get("enabled", False)) or os.environ.get("FAKE_CHATGPT_PRO") is not None
        pending = state.get("pending_checkpoint")
        fake_available = os.environ.get("FAKE_CHATGPT_PRO") is not None
        if (
            isinstance(pending, dict)
            and backend_available
            and not pending.get("pro_decision_path")
            and (fake_available or not pending.get("blocker_path"))
        ):
            return str(pending.get("reason") or "pending_checkpoint")

        status = state.get("status")
        last_decision = state.get("last_decision")
        if status == "stopped" and not state.get("last_pro_review_path"):
            return "local_stop"
        if status == "paused" and bool(state.get("human_review_required")) and not state.get("last_pro_review_path"):
            if last_decision in ("stop", "pivot", "needs_human"):
                return f"local_{last_decision}"
        return None

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
        while completed_this_run < max_iters:
            state = load_project_state(self.repo_root, project)
            loop_cfg = self.config.get("loop", {})
            pending = state.get("pending_checkpoint")
            if isinstance(pending, dict) and pending.get("pro_decision_path"):
                state_path = apply_pro_decision(self.repo_root, project)
                print(f"applied pending Pro decision: {state_path.relative_to(self.repo_root)}")
                break
            if state.get("status") != "active":
                checkpoint_reason = self._inactive_checkpoint_reason(state)
                if checkpoint_reason:
                    self._handle_pro_checkpoint(project, state, checkpoint_reason)
                    break
                print(f"stopping: project status is {state.get('status')}")
                break
            if state.get("human_review_required"):
                print("stopping: human_review_required is true")
                break
            if int(state.get("iteration", 0)) >= int(loop_cfg.get("max_iterations", 30)):
                print("stopping: configured max_iterations reached")
                break
            if pro_review_due(state, self.config):
                self._handle_pro_checkpoint(project, state, "cadence")
                break

            iteration = int(state.get("iteration", 0)) + 1
            iteration_id = f"{iteration:04d}"
            result_path, summary_path, artifact_dir = result_paths(self.repo_root, project, iteration_id)

            if result_path.exists() or summary_path.exists() or artifact_dir.exists():
                try:
                    validate_required_result_files(self.repo_root, project, iteration)
                    validate_json_schema(result_path, self.repo_root / "schemas" / "result.schema.json")
                    validate_result_artifact_paths(self.repo_root, result_path)
                except ValidationError:
                    pass
                else:
                    existing_result = load_json(result_path)
                    if should_retry_existing_result(existing_result, state):
                        archived = archive_existing_result_for_retry(self.repo_root, project, iteration_id, state)
                        self.git.commit(
                            archived,
                            f"autoresearcher({project}): archive retry {iteration_id}",
                        )
                        print(f"retrying existing {existing_result.get('status')} result for {iteration_id}")
                    else:
                        print(f"reviewing existing valid result for {iteration_id}")
                        decision = self._decision_for_existing_result(project, iteration_id)
                        review_status = self._review_iteration_result(
                            project,
                            state,
                            iteration,
                            iteration_id,
                            decision,
                            result_path,
                            summary_path,
                            artifact_dir,
                        )
                        if review_status == "completed":
                            completed_this_run += 1
                        elif review_status == "checkpoint":
                            break
                        elif review_status == "paused":
                            return 1
                        continue

            existing_plan_json, existing_plan_md = plan_paths(self.repo_root, project, iteration_id)
            decision: Optional[Dict[str, Any]] = None
            plan_md = existing_plan_md
            if existing_plan_json.exists() and existing_plan_md.exists():
                try:
                    experiment = load_json(existing_plan_json)
                    if not isinstance(experiment, dict):
                        raise ValidationError(f"existing plan is not an object: {existing_plan_json}")
                except ValidationError as exc:
                    print(f"warning: ignoring invalid existing plan for {iteration_id}: {exc}", file=sys.stderr)
                else:
                    print(f"executing existing approved plan for {iteration_id}: {existing_plan_md.relative_to(self.repo_root)}")
                    decision_kind = state.get("last_decision") if state.get("last_decision") in ("continue", "pivot") else "continue"
                    decision = {
                        "decision": decision_kind,
                        "confidence": 1.0,
                        "progress_score": 0,
                        "rationale": "Executing an already approved plan for this iteration without rewriting prior decisions.",
                        "evidence": [str(existing_plan_md.relative_to(self.repo_root))],
                        "risks": ["Plan execution may still fail reviewer validation."],
                        "next_experiment": experiment,
                    }

            if decision is None:
                supervisor_packet = build_context(self.repo_root, project, "supervisor")
                supervisor_packet += f"\n\n## Next experiment id\n\nUse `{iteration_id}` as the exact `next_experiment.experiment_id` if you choose continue or pivot.\n"
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
                        f"supervisor failed or timed out; stderr log: {supervisor_result.stderr_log_path}",
                        file=sys.stderr,
                    )
                    if supervisor_result.stderr_tail:
                        print(supervisor_result.stderr_tail, file=sys.stderr)
                    self._reset_role_session_on_context_overflow(project, supervisor_result)
                    paused = self._record_retryable_failure(
                        project,
                        state,
                        iteration_id,
                        f"supervisor failed or timed out; see {supervisor_result.stderr_log_path}",
                        [supervisor_packet_path, supervisor_result.jsonl_log_path, supervisor_result.stderr_log_path, decision_path],
                    )
                    if paused:
                        return 1
                    continue

                try:
                    validate_json_schema(decision_path, self.repo_root / "schemas" / "decision.schema.json")
                    decision = load_json(decision_path)
                except ValidationError as exc:
                    paused = self._record_retryable_failure(
                        project,
                        state,
                        iteration_id,
                        f"invalid supervisor decision: {exc}",
                        [supervisor_packet_path, supervisor_result.jsonl_log_path, supervisor_result.stderr_log_path, decision_path],
                    )
                    if paused:
                        return 1
                    continue

                decision_md = write_decision_markdown(self.repo_root, project, iteration_id, decision)
                self.git.commit(
                    [supervisor_packet_path, decision_path, decision_md],
                    f"autoresearcher({project}): decision {iteration_id}",
                )

                decision_kind = decision["decision"]
                checkpoint, checkpoint_reason = pro_checkpoint_due(state, self.config, local_decision=decision)
                if checkpoint:
                    self._handle_pro_checkpoint(project, state, checkpoint_reason, local_decision_path=decision_path)
                    break
                if decision_kind == "stop":
                    state["last_decision"] = decision["decision"]
                    state["status"] = "stopped"
                    state_path = save_project_state(self.repo_root, project, state)
                    self.git.commit([decision_path, decision_md, state_path], f"autoresearcher({project}): pause {iteration_id}")
                    self._run_summary_agent(project, state, reason="final")
                    print(f"stopping: supervisor decision {decision_kind}")
                    break
                if decision_kind == "needs_human" or (
                    decision_kind == "pivot" and bool(loop_cfg.get("require_human_for_pivot", False))
                ):
                    state["last_decision"] = decision_kind
                    mark_human_required(state, f"supervisor decision {decision_kind}", status="paused")
                    state_path = save_project_state(self.repo_root, project, state)
                    self.git.commit([decision_path, decision_md, state_path], f"autoresearcher({project}): pause {iteration_id}")
                    print(f"stopping: supervisor decision {decision_kind}")
                    break

                experiment = decision.get("next_experiment")
                if not isinstance(experiment, dict):
                    paused = self._record_retryable_failure(
                        project,
                        state,
                        iteration_id,
                        f"{decision_kind} decision had no next_experiment",
                        [supervisor_packet_path, decision_path, decision_md],
                    )
                    if paused:
                        return 1
                    continue
                experiment = normalize_experiment_paths(project, iteration_id, experiment)
                _plan_json, plan_md = write_plan(self.repo_root, project, iteration_id, experiment)
                self.git.commit([_plan_json, plan_md], f"autoresearcher({project}): plan {iteration_id}")

            executor_packet = build_context(self.repo_root, project, "executor", plan=plan_md)
            executor_packet_path = write_packet(self.repo_root, project, iteration_id, "executor", executor_packet)
            executor_output = self.repo_root / ".autoresearcher" / "runs" / project / f"{iteration_id}_executor_last_message.md"
            executor_result = self._run_role(project, "executor", iteration_id, executor_packet, executor_output)

            if executor_result.timed_out:
                written = write_timeout_result(self.repo_root, project, iteration_id)
                validate_json_schema(result_path, self.repo_root / "schemas" / "result.schema.json")
                state["last_decision"] = "timeout"
                self._reset_role_session_on_context_overflow(project, executor_result)
                paused = self._record_retryable_failure(
                    project,
                    state,
                    iteration_id,
                    "executor timeout",
                    written + [
                        executor_packet_path,
                        executor_result.jsonl_log_path,
                        executor_result.stderr_log_path,
                    ],
                )
                if paused:
                    return 1
                continue

            safety_cfg = self.config.get("safety", {})
            if not bool(safety_cfg.get("allow_executor_to_modify_orchestrator", False)):
                guard = protected_file_drift(self.repo_root, project)
                if guard.drift_detected:
                    guard_json, guard_md = write_guard_report(self.repo_root, project, iteration_id, guard)
                    state["protected_file_drift"] = True
                    state["last_decision"] = "protected_file_drift"
                    state_path = save_project_state(self.repo_root, project, state)
                    self.git.commit(
                        [guard_json, guard_md, state_path],
                        f"autoresearcher({project}): protected drift {iteration_id}",
                    )
                    self._handle_pro_checkpoint(project, state, "protected_file_drift")
                    break

            try:
                validate_required_result_files(self.repo_root, project, iteration)
                validate_json_schema(result_path, self.repo_root / "schemas" / "result.schema.json")
                validate_result_artifact_paths(self.repo_root, result_path)
            except ValidationError as exc:
                if self.config.get("loop", {}).get("stop_on_missing_result", True):
                    paused = self._record_retryable_failure(
                        project,
                        state,
                        iteration_id,
                        f"missing or invalid result for {iteration_id}: {exc}",
                        [
                            executor_packet_path,
                            executor_result.jsonl_log_path,
                            executor_result.stderr_log_path,
                            result_path,
                            summary_path,
                            artifact_dir,
                        ],
                    )
                    if paused:
                        return 1
                    continue
                raise

            self.git.commit(
                [executor_packet_path, result_path, summary_path, artifact_dir],
                f"autoresearcher({project}): result {iteration_id}",
            )

            review_status = self._review_iteration_result(
                project,
                state,
                iteration,
                iteration_id,
                decision,
                result_path,
                summary_path,
                artifact_dir,
            )
            if review_status == "completed":
                completed_this_run += 1
            elif review_status == "checkpoint":
                break
            elif review_status == "paused":
                return 1

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


def run_manual_summary(repo_root: Path, project: str, config: Dict[str, Any], codex_bin: str, skip_model_check: bool = False) -> int:
    ensure_project_scaffold(repo_root, project)
    if not skip_model_check:
        check_model_available(repo_root, config, codex_bin=codex_bin)
    state = load_project_state(repo_root, project)
    path = Orchestrator(repo_root, config, codex_bin=codex_bin)._run_summary_agent(
        project,
        state,
        reason="manual",
        force=True,
    )
    if path is None:
        print("no progress summary written")
        return 1
    print(path)
    return 0


def pro_iteration_id(state: Dict[str, Any]) -> str:
    return f"{int(state.get('iteration', 0)) + 1:04d}"


def pro_review_artifact_paths(repo_root: Path, project: str, review_id: str) -> List[Path]:
    raw_path, decision_path, decision_md_path = pro_decision_paths(repo_root, project, review_id)
    decisions = project_dir(repo_root, project) / "decisions"
    return [
        pro_packet_path(repo_root, project, review_id),
        raw_path,
        decision_path,
        decision_md_path,
        decisions / f"{review_id}_pro_blocker.json",
        decisions / f"{review_id}_pro_blocker.md",
    ]


def next_pro_review_id(repo_root: Path, project: str, state: Dict[str, Any]) -> str:
    base_id = pro_iteration_id(state)
    for attempt in range(1, 100):
        review_id = base_id if attempt == 1 else f"{base_id}_review{attempt}"
        if not any(path.exists() for path in pro_review_artifact_paths(repo_root, project, review_id)):
            return review_id
    raise RuntimeError(f"could not find an unused Pro review id for next experiment {base_id}")


def pro_packet_path(repo_root: Path, project: str, iteration_id: str) -> Path:
    return project_dir(repo_root, project) / "pro_packets" / f"{iteration_id}_PRO_REVIEW_PACKET.md"


def pro_decision_paths(repo_root: Path, project: str, iteration_id: str) -> Tuple[Path, Path, Path]:
    root = project_dir(repo_root, project) / "decisions"
    return (
        root / f"{iteration_id}_pro_raw_response.md",
        root / f"{iteration_id}_pro_decision.json",
        root / f"{iteration_id}_pro_decision.md",
    )


def pro_decision_markdown(decision: Dict[str, Any]) -> str:
    lines = [
        f"# ChatGPT Pro Decision: {decision['decision']}",
        "",
        f"Confidence: {decision['confidence']}",
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
        lines.extend(
            [
                "",
                "## Next experiment",
                "",
                f"- Experiment id: `{experiment['experiment_id']}`",
                f"- Objective: {experiment['objective']}",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def extract_fenced_json(text: str) -> Dict[str, Any]:
    matches = re.findall(r"```(?:json)?\s*(\{.*?\})\s*```", text, flags=re.DOTALL | re.IGNORECASE)
    stripped = text.strip()
    candidates = list(matches)
    if stripped.lower().startswith("json\n"):
        candidates.append(stripped.split("\n", 1)[1].strip())
    candidates.append(stripped)
    errors: List[str] = []
    for candidate in candidates:
        try:
            parsed = json.loads(candidate)
        except json.JSONDecodeError as exc:
            errors.append(str(exc))
            continue
        if isinstance(parsed, dict):
            return parsed
    decoder = json.JSONDecoder()
    for index, character in enumerate(stripped):
        if character != "{":
            continue
        try:
            parsed, _ = decoder.raw_decode(stripped[index:])
        except json.JSONDecodeError as exc:
            errors.append(str(exc))
            continue
        if isinstance(parsed, dict):
            return parsed
    raise RuntimeError("no valid fenced JSON object found in Pro response: " + "; ".join(errors))


def latest_pro_decision_path(repo_root: Path, project: str) -> Optional[Path]:
    paths = sorted((project_dir(repo_root, project) / "decisions").glob("*_pro_decision.json"))
    return paths[-1] if paths else None


def build_pro_packet(repo_root: Path, project: str, reason: str = "manual") -> Path:
    ensure_project_scaffold(repo_root, project)
    state = load_project_state(repo_root, project)
    iteration_id = next_pro_review_id(repo_root, project, state)
    write_metric_ledger(repo_root, project)
    packet = build_context(repo_root, project, "chatgpt_pro", reason=reason)
    path = pro_packet_path(repo_root, project, iteration_id)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(packet)
    return path


def run_pro_review(
    repo_root: Path,
    project: str,
    config: Dict[str, Any],
    reason: str = "manual",
    backend_override: str = "auto",
    local_decision_path: Optional[Path] = None,
) -> SupervisorBackendResult:
    ensure_project_scaffold(repo_root, project)
    state = load_project_state(repo_root, project)
    iteration_id = next_pro_review_id(repo_root, project, state)
    next_experiment_id = pro_iteration_id(state)
    metric_json, metric_md = write_metric_ledger(repo_root, project)
    packet = build_context(repo_root, project, "chatgpt_pro", reason=reason)
    packet_path = pro_packet_path(repo_root, project, iteration_id)
    packet_path.parent.mkdir(parents=True, exist_ok=True)
    packet_path.write_text(packet)
    backend = supervisor_backend_for_config(config, backend_override=backend_override)
    result = backend.decide(repo_root, project, config, packet_path, reason, iteration_id)

    paths: List[Path] = [packet_path, metric_json, metric_md]
    if local_decision_path is not None:
        paths.append(local_decision_path)

    state = load_project_state(repo_root, project)
    checkpoint: Dict[str, Any] = {
        "type": "chatgpt_pro",
        "reason": reason,
        "iteration_id": iteration_id,
        "packet_path": str(packet_path.relative_to(repo_root)),
        "backend": config.get("chatgpt_pro", {}).get("backend", "manual"),
        "status": result.status,
    }
    if local_decision_path is not None:
        state["pending_local_decision_path"] = str(local_decision_path.relative_to(repo_root))

    if result.status == "completed" and result.decision_path is not None:
        paths.extend(path for path in (result.raw_response_path, result.decision_path, result.markdown_path) if path)
        decision = load_json(result.decision_path)
        if isinstance(decision, dict) and isinstance(decision.get("next_experiment"), dict):
            experiment = normalize_experiment_paths(project, next_experiment_id, decision["next_experiment"])
            decision["next_experiment"] = experiment
            json_dump(result.decision_path, decision)
            if result.markdown_path is not None:
                result.markdown_path.write_text(pro_decision_markdown(decision))
            plan_json, plan_md = write_plan(repo_root, project, next_experiment_id, experiment)
            paths.extend([plan_json, plan_md])
        checkpoint["status"] = "pro_decision_ingested"
        checkpoint["pro_decision_path"] = str(result.decision_path.relative_to(repo_root))
        state["last_pro_review_path"] = str(result.decision_path.relative_to(repo_root))
        state["pending_checkpoint"] = checkpoint
        state.setdefault("notes", []).append(
            f"{utc_now_iso()}: Pro decision saved for checkpoint {reason} ({result.decision_path.relative_to(repo_root)})"
        )
    else:
        paths.extend(path for path in (result.blocker_path, result.blocker_markdown_path, result.raw_response_path) if path)
        state["status"] = "paused"
        state["human_review_required"] = True
        checkpoint["manual_fallback"] = True
        if result.blocker_path is not None:
            checkpoint["blocker_path"] = str(result.blocker_path.relative_to(repo_root))
        state["pending_checkpoint"] = checkpoint
        state.setdefault("notes", []).append(
            f"{utc_now_iso()}: Pro checkpoint blocked ({result.reason}); packet {packet_path.relative_to(repo_root)}"
        )

    state_path = save_project_state(repo_root, project, state)
    paths.append(state_path)
    GitManager(repo_root, config).commit(paths, f"autoresearcher({project}): Pro review {iteration_id}")
    return result


def ingest_pro_response(repo_root: Path, project: str, response_file: Path) -> Tuple[Path, Path]:
    ensure_project_scaffold(repo_root, project)
    state = load_project_state(repo_root, project)
    iteration_id = next_pro_review_id(repo_root, project, state)
    next_experiment_id = pro_iteration_id(state)
    raw_path, decision_path, decision_md_path = pro_decision_paths(repo_root, project, iteration_id)
    raw_path.write_text(response_file.read_text())
    decision = extract_fenced_json(raw_path.read_text())
    if isinstance(decision.get("next_experiment"), dict):
        decision["next_experiment"] = normalize_experiment_paths(project, next_experiment_id, decision["next_experiment"])
    json_dump(decision_path, decision)
    validate_json_schema(decision_path, repo_root / "schemas" / "pro_decision.schema.json")
    decision_md_path.write_text(pro_decision_markdown(decision))

    written_paths = [raw_path, decision_path, decision_md_path]
    if isinstance(decision.get("next_experiment"), dict):
        experiment = normalize_experiment_paths(project, next_experiment_id, decision["next_experiment"])
        plan_json, plan_md = write_plan(repo_root, project, next_experiment_id, experiment)
        written_paths.extend([plan_json, plan_md])

    state["pending_checkpoint"] = {
        "status": "pro_decision_ingested",
        "iteration_id": iteration_id,
        "pro_decision_path": str(decision_path.relative_to(repo_root)),
    }
    state["last_pro_review_path"] = str(decision_path.relative_to(repo_root))
    state_path = save_project_state(repo_root, project, state)
    written_paths.append(state_path)
    GitManager(repo_root, load_config(repo_root)).commit(written_paths, f"autoresearcher({project}): ingest Pro decision {iteration_id}")
    return decision_path, decision_md_path


def apply_pro_decision(repo_root: Path, project: str) -> Path:
    ensure_project_scaffold(repo_root, project)
    state = load_project_state(repo_root, project)
    path = latest_pro_decision_path(repo_root, project)
    if path is None:
        raise RuntimeError(f"no Pro decision found for {project}")
    validate_json_schema(path, repo_root / "schemas" / "pro_decision.schema.json")
    decision = load_json(path)
    if not isinstance(decision, dict):
        raise RuntimeError(f"invalid Pro decision root in {path}")

    iteration_id = pro_iteration_id(state)
    paths: List[Path] = [path]
    decision_kind = decision["decision"]
    if decision_kind == "stop":
        state["status"] = "stopped"
        state["human_review_required"] = False
        state["last_decision"] = "stop"
    elif decision_kind in ("continue", "pivot"):
        experiment = decision.get("next_experiment")
        if not isinstance(experiment, dict):
            mark_human_required(state, f"Pro decision {decision_kind} missing next_experiment", status="paused")
        else:
            normalized = normalize_experiment_paths(project, iteration_id, experiment)
            plan_json, plan_md = write_plan(repo_root, project, iteration_id, normalized)
            paths.extend([plan_json, plan_md])
            state["status"] = "active"
            state["human_review_required"] = False
            state["last_decision"] = decision_kind
    else:
        raise RuntimeError(f"unknown Pro decision kind {decision_kind!r}")

    relative_decision_path = str(path.relative_to(repo_root))
    already_applied = (
        state.get("last_pro_review_path") == relative_decision_path
        and state.get("pending_checkpoint") is None
    )
    state["last_pro_review_iteration"] = int(state.get("iteration", 0) or 0)
    state["last_pro_review_path"] = relative_decision_path
    if not already_applied:
        state["pro_review_count"] = int(state.get("pro_review_count", 0) or 0) + 1
    state["weak_pass_streak"] = 0
    state["pending_checkpoint"] = None
    state["pending_local_decision_path"] = None
    if not already_applied:
        state.setdefault("notes", []).append(f"{utc_now_iso()}: applied Pro decision {decision_kind} from {relative_decision_path}")
    state_path = save_project_state(repo_root, project, state)
    paths.append(state_path)
    GitManager(repo_root, load_config(repo_root)).commit(paths, f"autoresearcher({project}): apply Pro decision {iteration_id}")
    return state_path


def resume_project(repo_root: Path, project: str, note: str) -> Path:
    if not note.strip():
        raise RuntimeError("resume requires a non-empty note")
    ensure_project_scaffold(repo_root, project)
    state = load_project_state(repo_root, project)
    state["status"] = "active"
    state["human_review_required"] = False
    state["pending_checkpoint"] = None
    state["pending_local_decision_path"] = None
    state.setdefault("notes", []).append(f"{utc_now_iso()}: resumed: {note.strip()}")
    state_path = save_project_state(repo_root, project, state)
    GitManager(repo_root, load_config(repo_root)).commit([state_path], f"autoresearcher({project}): resume")
    return state_path


def stop_project(repo_root: Path, project: str, note: str) -> Path:
    ensure_project_scaffold(repo_root, project)
    state = load_project_state(repo_root, project)
    state["status"] = "stopped"
    state["human_review_required"] = False
    state.setdefault("notes", []).append(f"{utc_now_iso()}: stopped: {note.strip()}")
    state_path = save_project_state(repo_root, project, state)
    GitManager(repo_root, load_config(repo_root)).commit([state_path], f"autoresearcher({project}): stop")
    return state_path


def pro_smoke(repo_root: Path, project: str, config: Dict[str, Any]) -> int:
    ensure_project_scaffold(repo_root, project)
    if not config.get("chatgpt_pro", {}).get("enabled", False):
        print("chatgpt_pro.enabled=false; Phase 1 does not require Pro bridge dependencies.")
        return 0
    packet_path = build_pro_packet(repo_root, project, reason="pro_smoke")
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
    parser.add_argument("--no-git", action="store_true", help="Do not auto-commit or push generated files for this command.")
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
    context_p.add_argument("--reason", default="manual")

    reset_p = subparsers.add_parser("reset-role-session", help="Clear stored Codex session id for one role.")
    reset_p.add_argument("--project", default=None)
    reset_p.add_argument("--role", required=True, choices=ROLE_NAMES)

    status_p = subparsers.add_parser("status", help="Print project state and local role sessions.")
    status_p.add_argument("--project", default=None)

    summary_p = subparsers.add_parser("summarize", help="Run the summary agent and write a progress summary.")
    summary_p.add_argument("--project", default=None)
    summary_p.add_argument("--skip-model-check", action="store_true", help="Testing only: skip `codex debug models`.")

    pro_p = subparsers.add_parser("pro-smoke", help="Phase 2 stub: verify Pro is disabled or write blocker.")
    pro_p.add_argument("--project", default=None)

    pro_review_p = subparsers.add_parser("pro-review", help="Run a ChatGPT Pro checkpoint review or write a structured blocker.")
    pro_review_p.add_argument("--project", default=None)
    pro_review_p.add_argument("--reason", default="manual")
    pro_review_p.add_argument("--backend", choices=("auto", "manual", "live", "cdp"), default="auto")

    packet_p = subparsers.add_parser("build-pro-packet", help="Build a ChatGPT Pro review packet.")
    packet_p.add_argument("--project", default=None)
    packet_p.add_argument("--reason", default="manual")

    ingest_p = subparsers.add_parser("ingest-pro-response", help="Ingest a Markdown response containing fenced Pro decision JSON.")
    ingest_p.add_argument("--project", default=None)
    ingest_p.add_argument("--file", type=Path, required=True)

    apply_p = subparsers.add_parser("apply-pro-decision", help="Apply the latest validated Pro decision to project state.")
    apply_p.add_argument("--project", default=None)

    resume_p = subparsers.add_parser("resume", help="Resume a paused or stopped project with a required note.")
    resume_p.add_argument("--project", default=None)
    resume_p.add_argument("--note", required=True)

    stop_p = subparsers.add_parser("stop", help="Stop a project with an optional note.")
    stop_p.add_argument("--project", default=None)
    stop_p.add_argument("--note", default="")

    args = parser.parse_args(argv)
    repo_root = repo_root_from(args.repo_root).resolve() if args.repo_root else repo_root_from().resolve()
    config = load_config(repo_root)
    if args.no_git:
        config.setdefault("git", {})
        config["git"]["enabled"] = False
        config["git"]["commit"] = False
        config["git"]["push"] = False
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
        print(build_context(repo_root, project, args.role, plan=args.plan, reason=args.reason), end="")
        return 0
    if args.command == "reset-role-session":
        reset_role_session(repo_root, project, args.role)
        print(f"reset {project}:{args.role}")
        return 0
    if args.command == "status":
        print_status(repo_root, project)
        return 0
    if args.command == "summarize":
        return run_manual_summary(
            repo_root,
            project,
            config,
            codex_bin=args.codex_bin,
            skip_model_check=args.skip_model_check,
        )
    if args.command == "pro-smoke":
        return pro_smoke(repo_root, project, config)
    if args.command == "pro-review":
        result = run_pro_review(
            repo_root,
            project,
            config,
            reason=args.reason,
            backend_override=args.backend,
        )
        if result.status == "completed":
            if result.decision_path:
                print(result.decision_path)
            if result.markdown_path:
                print(result.markdown_path)
            return 0
        if result.blocker_path:
            print(result.blocker_path)
        if result.blocker_markdown_path:
            print(result.blocker_markdown_path)
        return 2 if result.status == "blocked" else 1
    if args.command == "build-pro-packet":
        path = build_pro_packet(repo_root, project, reason=args.reason)
        print(path)
        return 0
    if args.command == "ingest-pro-response":
        decision_path, decision_md_path = ingest_pro_response(repo_root, project, args.file.resolve())
        print(decision_path)
        print(decision_md_path)
        return 0
    if args.command == "apply-pro-decision":
        path = apply_pro_decision(repo_root, project)
        print(path)
        return 0
    if args.command == "resume":
        path = resume_project(repo_root, project, args.note)
        print(path)
        return 0
    if args.command == "stop":
        path = stop_project(repo_root, project, args.note)
        print(path)
        return 0
    parser.error(f"unknown command {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
