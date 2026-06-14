"""Optional ChatGPT Pro bridge and fake backend helpers."""

from __future__ import annotations

import json
import os
import re
import shlex
import subprocess
import traceback
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

from validate_artifacts import ValidationError, validate_json_schema


BLOCKER_REASONS = {
    "backend_dependency_missing",
    "browser_bridge_unavailable",
    "thread_url_missing",
    "thread_unavailable",
    "login_required",
    "captcha",
    "rate_limit",
    "permission",
    "selector_drift",
    "model_unavailable",
    "thinking_mode_unavailable",
    "upload_failed",
    "response_parse_failed",
    "schema_validation_failed",
    "summary_failed",
    "pro_backend_failed",
    "manual_review_required",
}


def project_dir(repo_root: Path, project: str) -> Path:
    return repo_root / "research" / project


def json_dump(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")


def pro_decision_paths(repo_root: Path, project: str, iteration_id: str) -> Tuple[Path, Path, Path]:
    root = project_dir(repo_root, project) / "decisions"
    return (
        root / f"{iteration_id}_pro_raw_response.md",
        root / f"{iteration_id}_pro_decision.json",
        root / f"{iteration_id}_pro_decision.md",
    )


def pro_blocker_paths(repo_root: Path, project: str, iteration_id: str) -> Tuple[Path, Path]:
    root = project_dir(repo_root, project) / "decisions"
    return root / f"{iteration_id}_pro_blocker.json", root / f"{iteration_id}_pro_blocker.md"


def extract_fenced_json(text: str) -> Dict[str, Any]:
    matches = re.findall(r"```(?:json)?\s*(\{.*?\})\s*```", text, flags=re.DOTALL | re.IGNORECASE)
    stripped = text.strip()
    candidates = list(matches)
    if stripped.lower().startswith("json\n"):
        candidates.append(stripped.split("\n", 1)[1].strip())
    candidates.append(stripped)
    errors = []
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
    detail = "; ".join(errors) if errors else "no JSON object candidates"
    raise RuntimeError(f"no valid fenced JSON object found in Pro response: {detail}")


def render_pro_decision_markdown(decision: Dict[str, Any]) -> str:
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
    if isinstance(decision.get("next_experiment"), dict):
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


def write_pro_blocker(
    repo_root: Path,
    project: str,
    iteration_id: str,
    reason: str,
    message: str,
    packet_path: Optional[Path] = None,
    failed_command: Optional[Iterable[str]] = None,
    details: Optional[Dict[str, Any]] = None,
) -> Tuple[Path, Path]:
    if reason not in BLOCKER_REASONS:
        reason = "pro_backend_failed"
    json_path, md_path = pro_blocker_paths(repo_root, project, iteration_id)
    blocker = {
        "iteration_id": iteration_id,
        "reason": reason,
        "message": message,
        "packet_path": str(packet_path.relative_to(repo_root)) if packet_path else None,
        "failed_command": list(failed_command) if failed_command else None,
        "details": details or {},
    }
    json_dump(json_path, blocker)
    lines = [
        f"# ChatGPT Pro Blocker: {reason}",
        "",
        message,
    ]
    if packet_path:
        lines.extend(["", f"Packet: `{packet_path.relative_to(repo_root).as_posix()}`"])
    if failed_command:
        lines.extend(["", "Failed command:", "", "```bash", " ".join(failed_command), "```"])
    md_path.write_text("\n".join(lines).rstrip() + "\n")
    return json_path, md_path


def save_raw_and_decision(
    repo_root: Path,
    project: str,
    iteration_id: str,
    raw_text: str,
    packet_path: Optional[Path] = None,
) -> Dict[str, Any]:
    raw_path, decision_path, md_path = pro_decision_paths(repo_root, project, iteration_id)
    raw_path.parent.mkdir(parents=True, exist_ok=True)
    raw_path.write_text(raw_text)
    try:
        decision = extract_fenced_json(raw_text)
    except RuntimeError as exc:
        blocker_json, blocker_md = write_pro_blocker(
            repo_root,
            project,
            iteration_id,
            "response_parse_failed",
            str(exc),
            packet_path=packet_path,
        )
        return {
            "status": "blocked",
            "reason": "response_parse_failed",
            "raw_response_path": raw_path,
            "blocker_path": blocker_json,
            "blocker_markdown_path": blocker_md,
        }

    json_dump(decision_path, decision)
    try:
        validate_json_schema(decision_path, repo_root / "schemas" / "pro_decision.schema.json")
    except ValidationError as exc:
        blocker_json, blocker_md = write_pro_blocker(
            repo_root,
            project,
            iteration_id,
            "schema_validation_failed",
            str(exc),
            packet_path=packet_path,
        )
        return {
            "status": "blocked",
            "reason": "schema_validation_failed",
            "raw_response_path": raw_path,
            "decision_path": decision_path,
            "blocker_path": blocker_json,
            "blocker_markdown_path": blocker_md,
        }

    md_path.write_text(render_pro_decision_markdown(decision))
    return {
        "status": "completed",
        "reason": None,
        "raw_response_path": raw_path,
        "decision_path": decision_path,
        "markdown_path": md_path,
        "decision": decision,
    }


def fake_pro_decision(project: str, iteration_id: str, decision_kind: str) -> Dict[str, Any]:
    next_experiment = None
    if decision_kind in ("continue", "pivot"):
        next_experiment = {
            "experiment_id": iteration_id,
            "objective": "Run one more tiny decision-relevant experiment.",
            "hypothesis": "A compact follow-up will clarify the current uncertainty without larger compute.",
            "success_criteria": ["Required result JSON and summary are produced."],
            "failure_criteria": ["Executor times out or required result files are missing."],
            "tasks_for_codex": [
                "Use the existing project environment.",
                "Run a small validation that directly addresses the Pro checkpoint rationale.",
                "Save raw metrics and a concise interpretation.",
            ],
            "required_outputs": [
                f"research/{project}/results/{iteration_id}_result.json",
                f"research/{project}/results/{iteration_id}_summary.md",
                f"research/{project}/artifacts/{iteration_id}/",
            ],
            "estimated_runtime_minutes": 30,
        }
    return {
        "decision": decision_kind,
        "confidence": 0.81,
        "rationale": f"Fake ChatGPT Pro backend selected {decision_kind} for deterministic testing.",
        "evidence": ["FAKE_CHATGPT_PRO was set."],
        "risks": ["Fake backend is not real model evidence."],
        "next_experiment": next_experiment,
    }


def fake_pro_response(project: str, iteration_id: str, mode: str) -> Dict[str, Any]:
    mode = (mode or "1").strip()
    if mode in ("1", "true", "yes"):
        mode = "continue"
    if mode.startswith("blocker:"):
        reason = mode.split(":", 1)[1].strip() or "browser_bridge_unavailable"
        return {
            "status": "blocked",
            "reason": reason,
            "message": f"Fake ChatGPT Pro blocker: {reason}",
        }
    if mode in BLOCKER_REASONS:
        return {"status": "blocked", "reason": mode, "message": f"Fake ChatGPT Pro blocker: {mode}"}
    if mode == "malformed":
        return {"status": "completed", "raw_text": "this response does not contain JSON"}
    if mode == "bad_schema":
        return {
            "status": "completed",
            "raw_text": "```json\n{\"decision\":\"continue\",\"confidence\":0.5}\n```",
        }
    if mode not in ("continue", "pivot", "stop"):
        mode = "continue"
    decision = fake_pro_decision(project, iteration_id, mode)
    raw = "# ChatGPT Pro Decision\n\n```json\n" + json.dumps(decision, indent=2, sort_keys=True) + "\n```\n"
    return {"status": "completed", "raw_text": raw}


def local_state_thread_url(repo_root: Path, project: str) -> Optional[str]:
    path = repo_root / ".autoresearcher" / "local_state.json"
    try:
        state = json.loads(path.read_text())
    except (FileNotFoundError, json.JSONDecodeError):
        return None
    value = (
        state.get("projects", {})
        .get(project, {})
        .get("chatgpt_pro", {})
        .get("thread_url")
    )
    return value if isinstance(value, str) and value.strip() else None


def _path_or_none(value: Any) -> Optional[Path]:
    return Path(value) if isinstance(value, str) and value else None


def _serialize_result(result: Dict[str, Any]) -> Dict[str, Any]:
    output: Dict[str, Any] = {}
    for key, value in result.items():
        if isinstance(value, Path):
            output[key] = str(value)
        elif key != "decision":
            output[key] = value
    return output


def _deserialize_result(result: Dict[str, Any]) -> Dict[str, Any]:
    output = dict(result)
    for key in ("raw_response_path", "decision_path", "markdown_path", "blocker_path", "blocker_markdown_path"):
        output[key] = _path_or_none(output.get(key))
    return output


def _first_existing_path(paths: Iterable[Path]) -> Optional[Path]:
    for path in paths:
        if path.exists():
            return path
    return None


def _plugin_backend_path() -> Optional[Path]:
    home = Path.home()
    plugin_roots = sorted(
        (
            home / ".codex" / "plugins" / "cache" / "codex-chatgpt-control" / "codex-chatgpt-control"
        ).glob("*/runtime/node/codex-chatgpt-control-backend.mjs"),
        reverse=True,
    )
    return _first_existing_path(
        [
            *plugin_roots,
            home
            / "anaconda3"
            / "envs"
            / "python312"
            / "lib"
            / "node_modules"
            / "codex-chatgpt-control"
            / "dist"
            / "codex-chatgpt-control-backend.mjs",
        ]
    )


def _relay_script_path(config: Dict[str, Any]) -> Optional[Path]:
    pro_cfg = config.get("chatgpt_pro", {}) if isinstance(config.get("chatgpt_pro"), dict) else {}
    configured = pro_cfg.get("relay_script")
    if isinstance(configured, str) and configured.strip():
        return Path(configured).expanduser()
    home = Path.home()
    return _first_existing_path(
        [
            home
            / ".codex"
            / ".tmp"
            / "marketplaces"
            / "codex-chatgpt-control"
            / "packages"
            / "python"
            / "scripts"
            / "http_stdio_relay.mjs",
        ]
    )


def _backend_command_and_env(config: Dict[str, Any]) -> Tuple[List[str], Optional[Dict[str, str]]]:
    pro_cfg = config.get("chatgpt_pro", {}) if isinstance(config.get("chatgpt_pro"), dict) else {}
    backend_http_url = (
        os.environ.get("CHATGPT_BROWSER_BACKEND_HTTP_URL")
        or pro_cfg.get("backend_http_url")
        or pro_cfg.get("browser_backend_http_url")
    )
    if isinstance(backend_http_url, str) and backend_http_url.strip():
        relay_script = _relay_script_path(config)
        if relay_script is not None:
            env = dict(os.environ)
            env["CHATGPT_BROWSER_BACKEND_HTTP_URL"] = backend_http_url.strip()
            return ["node", str(relay_script)], env

    configured = os.environ.get("CHATGPT_BROWSER_BACKEND_COMMAND") or pro_cfg.get("backend_command")
    if isinstance(configured, str) and configured.strip():
        return shlex.split(configured), None
    if isinstance(configured, list) and all(isinstance(item, str) for item in configured):
        return list(configured), None

    plugin_backend = _plugin_backend_path()
    if plugin_backend is not None:
        return ["node", str(plugin_backend)], None

    return ["npx", "--yes", "--package", "codex-chatgpt-control", "codex-chatgpt-control-backend"], None


def _delegate_bridge_to_conda(
    repo_root: Path,
    project: str,
    config: Dict[str, Any],
    packet_path: Path,
    reason: str,
    iteration_id: str,
) -> Optional[Dict[str, Any]]:
    if os.environ.get("AUTORESEARCHER_PRO_BRIDGE_DELEGATED") == "1":
        return None
    pro_cfg = config.get("chatgpt_pro", {}) if isinstance(config.get("chatgpt_pro"), dict) else {}
    env_name = (
        os.environ.get("AUTORESEARCHER_PRO_BRIDGE_CONDA_ENV")
        or pro_cfg.get("bridge_conda_env")
        or pro_cfg.get("control_conda_env")
    )
    if not isinstance(env_name, str) or not env_name.strip():
        return None

    child_env = dict(os.environ)
    child_env["AUTORESEARCHER_PRO_BRIDGE_DELEGATED"] = "1"
    child_env.pop("FAKE_CHATGPT_PRO", None)
    cmd = [
        "conda",
        "run",
        "-n",
        env_name,
        "python",
        str(Path(__file__).resolve()),
        "--bridge-review",
        "--repo-root",
        str(repo_root),
        "--project",
        project,
        "--packet-path",
        str(packet_path),
        "--reason",
        reason,
        "--iteration-id",
        iteration_id,
        "--config-json",
        json.dumps(config),
    ]
    try:
        proc = subprocess.run(
            cmd,
            cwd=str(repo_root),
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=120,
            env=child_env,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return None
    if not proc.stdout.strip():
        return None
    try:
        parsed = json.loads(proc.stdout.strip().splitlines()[-1])
    except json.JSONDecodeError:
        return None
    return _deserialize_result(parsed)


def run_chatgpt_pro_review(
    repo_root: Path,
    project: str,
    config: Dict[str, Any],
    packet_path: Path,
    reason: str,
    iteration_id: str,
) -> Dict[str, Any]:
    fake_mode = os.environ.get("FAKE_CHATGPT_PRO")
    if fake_mode is not None:
        fake = fake_pro_response(project, iteration_id, fake_mode)
        if fake["status"] == "blocked":
            blocker_json, blocker_md = write_pro_blocker(
                repo_root,
                project,
                iteration_id,
                str(fake["reason"]),
                str(fake["message"]),
                packet_path=packet_path,
            )
            return {
                "status": "blocked",
                "reason": str(fake["reason"]),
                "blocker_path": blocker_json,
                "blocker_markdown_path": blocker_md,
            }
        return save_raw_and_decision(
            repo_root,
            project,
            iteration_id,
            str(fake["raw_text"]),
            packet_path=packet_path,
        )

    pro_cfg = config.get("chatgpt_pro", {}) if isinstance(config.get("chatgpt_pro"), dict) else {}
    try:
        from codex_chatgpt_control import Agent, BackendClient, Runner, StdioBackendTransport  # type: ignore
    except ImportError as exc:
        delegated = _delegate_bridge_to_conda(repo_root, project, config, packet_path, reason, iteration_id)
        if delegated is not None:
            return delegated
        blocker_json, blocker_md = write_pro_blocker(
            repo_root,
            project,
            iteration_id,
            "backend_dependency_missing",
            f"Python package codex_chatgpt_control is not importable: {exc}",
            packet_path=packet_path,
        )
        return {
            "status": "blocked",
            "reason": "backend_dependency_missing",
            "blocker_path": blocker_json,
            "blocker_markdown_path": blocker_md,
        }

    thread_url = pro_cfg.get("thread_url") or local_state_thread_url(repo_root, project)
    if not isinstance(thread_url, str) or not thread_url.strip():
        blocker_json, blocker_md = write_pro_blocker(
            repo_root,
            project,
            iteration_id,
            "thread_url_missing",
            "chatgpt_pro.thread_url is not configured and no local ChatGPT Pro thread URL is stored.",
            packet_path=packet_path,
        )
        return {
            "status": "blocked",
            "reason": "thread_url_missing",
            "blocker_path": blocker_json,
            "blocker_markdown_path": blocker_md,
        }

    command, backend_env = _backend_command_and_env(config)
    prompt_path = repo_root / "prompts" / "chatgpt_pro_supervisor.md"
    try:
        backend = BackendClient(StdioBackendTransport(command=command, env=backend_env))
        runner = Runner(backend)
        try:
            result = runner.run_sync(
                Agent(name="chatgpt_pro_supervisor", instructions=prompt_path.read_text()),
                {
                    "input": packet_path.read_text(),
                    "thread": {"type": "url", "url": thread_url},
                    "existingTab": bool(pro_cfg.get("existing_tab", True)),
                    "response": {"format": "markdown"},
                    "metadata": {"checkpoint_reason": reason},
                },
            )
        finally:
            close = getattr(backend, "close", None)
            if callable(close):
                close()
    except Exception as exc:  # pragma: no cover - depends on optional browser package
        blocker_json, blocker_md = write_pro_blocker(
            repo_root,
            project,
            iteration_id,
            "browser_bridge_unavailable",
            f"ChatGPT Pro browser bridge failed: {exc}",
            packet_path=packet_path,
            failed_command=command,
            details={"traceback": traceback.format_exc()[-4000:]},
        )
        return {
            "status": "blocked",
            "reason": "browser_bridge_unavailable",
            "blocker_path": blocker_json,
            "blocker_markdown_path": blocker_md,
        }

    status = getattr(result, "status", None)
    if status and status != "completed":
        result_payload = result.to_wire() if hasattr(result, "to_wire") else {}
        sdk_blocker = result_payload.get("blocker") if isinstance(result_payload, dict) else None
        sdk_blocker_kind = sdk_blocker.get("kind") if isinstance(sdk_blocker, dict) else None
        reason_value = str(sdk_blocker_kind or status)
        if reason_value not in BLOCKER_REASONS:
            reason_value = "pro_backend_failed"
        blocker_json, blocker_md = write_pro_blocker(
            repo_root,
            project,
            iteration_id,
            reason_value,
            f"ChatGPT Pro backend returned status {status}.",
            packet_path=packet_path,
            failed_command=command,
            details={
                "sdk_status": status,
                "sdk_ok": result_payload.get("ok") if isinstance(result_payload, dict) else None,
                "sdk_blocker": sdk_blocker,
                "sdk_output_text": result_payload.get("output_text") if isinstance(result_payload, dict) else None,
                "sdk_warnings": result_payload.get("warnings") if isinstance(result_payload, dict) else None,
                "sdk_context": result_payload.get("context") if isinstance(result_payload, dict) else None,
                "sdk_report_path": result_payload.get("reportPath") if isinstance(result_payload, dict) else None,
            },
        )
        return {
            "status": "blocked",
            "reason": reason_value,
            "blocker_path": blocker_json,
            "blocker_markdown_path": blocker_md,
        }

    raw = getattr(result, "output", None) or getattr(result, "text", None) or str(result)
    return save_raw_and_decision(repo_root, project, iteration_id, raw, packet_path=packet_path)


def run_chatgpt_pro_review_cdp(
    repo_root: Path,
    project: str,
    config: Dict[str, Any],
    packet_path: Path,
    reason: str,
    iteration_id: str,
) -> Dict[str, Any]:
    pro_cfg = config.get("chatgpt_pro", {}) if isinstance(config.get("chatgpt_pro"), dict) else {}
    thread_url = pro_cfg.get("thread_url") or local_state_thread_url(repo_root, project)
    if not isinstance(thread_url, str) or not thread_url.strip():
        blocker_json, blocker_md = write_pro_blocker(
            repo_root,
            project,
            iteration_id,
            "thread_url_missing",
            "chatgpt_pro.thread_url is not configured and no local ChatGPT Pro thread URL is stored.",
            packet_path=packet_path,
        )
        return {
            "status": "blocked",
            "reason": "thread_url_missing",
            "blocker_path": blocker_json,
            "blocker_markdown_path": blocker_md,
        }

    try:
        from chatgpt_cdp_bridge import run_cdp_review
    except ImportError as exc:
        blocker_json, blocker_md = write_pro_blocker(
            repo_root,
            project,
            iteration_id,
            "backend_dependency_missing",
            f"CDP backend dependency is not importable: {exc}",
            packet_path=packet_path,
        )
        return {
            "status": "blocked",
            "reason": "backend_dependency_missing",
            "blocker_path": blocker_json,
            "blocker_markdown_path": blocker_md,
        }

    cdp_url = os.environ.get("CHATGPT_CDP_URL") or pro_cfg.get("cdp_url") or "http://127.0.0.1:9222"
    prompt_path = repo_root / "prompts" / "chatgpt_pro_supervisor.md"
    result = run_cdp_review(
        str(cdp_url),
        thread_url.strip(),
        prompt_path.read_text(),
        packet_path.read_text(),
        reason,
        allow_new_tab=bool(pro_cfg.get("allow_new_thread", False)),
        ready_timeout_seconds=int(pro_cfg.get("cdp_ready_timeout_seconds", 120)),
        response_timeout_seconds=int(pro_cfg.get("cdp_response_timeout_seconds", 600)),
    )
    if result.status == "completed" and result.raw_text is not None:
        return save_raw_and_decision(repo_root, project, iteration_id, result.raw_text, packet_path=packet_path)

    reason_value = result.reason or "pro_backend_failed"
    if reason_value not in BLOCKER_REASONS:
        reason_value = "pro_backend_failed"
    blocker_json, blocker_md = write_pro_blocker(
        repo_root,
        project,
        iteration_id,
        reason_value,
        result.message or "ChatGPT CDP backend did not complete.",
        packet_path=packet_path,
        failed_command=["python", "scripts/chatgpt_cdp_bridge.py", "probe", "--cdp-url", str(cdp_url), "--thread-url", thread_url.strip()],
        details=result.details,
    )
    return {
        "status": "blocked",
        "reason": reason_value,
        "blocker_path": blocker_json,
        "blocker_markdown_path": blocker_md,
    }


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(description="Internal ChatGPT Pro bridge runner.")
    parser.add_argument("--bridge-review", action="store_true")
    parser.add_argument("--repo-root", type=Path, required=True)
    parser.add_argument("--project", required=True)
    parser.add_argument("--packet-path", type=Path, required=True)
    parser.add_argument("--reason", required=True)
    parser.add_argument("--iteration-id", required=True)
    parser.add_argument("--config-json", required=True)
    args = parser.parse_args()
    if not args.bridge_review:
        parser.error("--bridge-review is required")
    config = json.loads(args.config_json)
    result = run_chatgpt_pro_review(
        args.repo_root.resolve(),
        args.project,
        config,
        args.packet_path.resolve(),
        args.reason,
        args.iteration_id,
    )
    print(json.dumps(_serialize_result(result), sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
