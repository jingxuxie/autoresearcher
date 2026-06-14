"""Detect protected-file drift during research executor runs."""

from __future__ import annotations

import json
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Sequence, Tuple


DEFAULT_PROTECTED_PATTERNS = (
    "scripts/autoresearcher.py",
    "scripts/build_context.py",
    "scripts/validate_artifacts.py",
    "schemas/",
    "prompts/",
    "autoresearcher.yaml",
    "AGENTS.md",
)

DEFAULT_ALLOWED_PREFIXES = (
    "research/{project}/results/",
    "research/{project}/artifacts/",
    "research/{project}/packets/",
    "research/{project}/setup_logs/",
    "research/{project}/progress/",
)


@dataclass
class GuardResult:
    drift_detected: bool
    protected_paths: List[str]
    status_lines: List[str]


def _git(repo_root: Path, args: Sequence[str]) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git"] + list(args),
        cwd=str(repo_root),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def _parse_porcelain_line(line: str) -> str:
    raw = line[3:] if len(line) > 3 else line
    if " -> " in raw:
        raw = raw.split(" -> ", 1)[1]
    return raw.strip()


def _matches(path: str, pattern: str) -> bool:
    if pattern.endswith("/"):
        return path.startswith(pattern)
    return path == pattern or path.startswith(pattern.rstrip("/") + "/")


def protected_file_drift(
    repo_root: Path,
    project: str,
    protected_patterns: Iterable[str] = DEFAULT_PROTECTED_PATTERNS,
) -> GuardResult:
    proc = _git(repo_root, ["status", "--porcelain"])
    if proc.returncode != 0:
        return GuardResult(False, [], [])

    protected_paths: List[str] = []
    status_lines = [line for line in proc.stdout.splitlines() if line.strip()]
    for line in status_lines:
        path = _parse_porcelain_line(line)
        if any(_matches(path, pattern) for pattern in protected_patterns):
            protected_paths.append(path)

    return GuardResult(bool(protected_paths), sorted(set(protected_paths)), status_lines)


def write_guard_report(repo_root: Path, project: str, iteration_id: str, result: GuardResult) -> Tuple[Path, Path]:
    root = repo_root / "research" / project / "decisions"
    root.mkdir(parents=True, exist_ok=True)
    json_path = root / f"{iteration_id}_worktree_guard.json"
    md_path = root / f"{iteration_id}_worktree_guard.md"
    data = {
        "iteration": iteration_id,
        "drift_detected": result.drift_detected,
        "protected_paths": result.protected_paths,
        "status_lines": result.status_lines,
    }
    json_path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")
    lines = [
        f"# Worktree Guard {iteration_id}",
        "",
        f"Drift detected: `{result.drift_detected}`",
        "",
        "## Protected Paths",
        "",
    ]
    if result.protected_paths:
        lines.extend(f"- `{path}`" for path in result.protected_paths)
    else:
        lines.append("_None._")
    lines.extend(["", "## Git Status Lines", ""])
    if result.status_lines:
        lines.extend(f"- `{line}`" for line in result.status_lines)
    else:
        lines.append("_None._")
    md_path.write_text("\n".join(lines).rstrip() + "\n")
    return json_path, md_path
