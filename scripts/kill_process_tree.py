#!/usr/bin/env python3
"""Run a command with process-group timeout enforcement."""

from __future__ import annotations

import argparse
import os
import signal
import subprocess
from dataclasses import dataclass
from typing import List, Optional, Sequence


@dataclass
class TimedCommandResult:
    command: List[str]
    return_code: int
    timed_out: bool
    stdout: str
    stderr: str


def terminate_process_group(proc: subprocess.Popen, grace_seconds: float = 10.0) -> None:
    """Terminate a process group, then kill it if it ignores SIGTERM."""
    if proc.poll() is not None:
        return

    try:
        os.killpg(proc.pid, signal.SIGTERM)
    except ProcessLookupError:
        return

    try:
        proc.wait(timeout=grace_seconds)
    except subprocess.TimeoutExpired:
        try:
            os.killpg(proc.pid, signal.SIGKILL)
        except ProcessLookupError:
            return


def run_with_timeout(
    command: Sequence[str],
    timeout_seconds: float,
    input_text: Optional[str] = None,
    grace_seconds: float = 10.0,
) -> TimedCommandResult:
    """Run command in a new process group and kill descendants on timeout."""
    proc = subprocess.Popen(
        list(command),
        stdin=subprocess.PIPE if input_text is not None else None,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        start_new_session=True,
    )
    timed_out = False
    try:
        stdout, stderr = proc.communicate(input=input_text, timeout=timeout_seconds)
    except subprocess.TimeoutExpired:
        timed_out = True
        terminate_process_group(proc, grace_seconds=grace_seconds)
        try:
            stdout, stderr = proc.communicate(timeout=1)
        except subprocess.TimeoutExpired:
            stdout, stderr = "", "Process did not exit after SIGKILL."

    return TimedCommandResult(
        command=list(command),
        return_code=proc.returncode if proc.returncode is not None else -signal.SIGKILL,
        timed_out=timed_out,
        stdout=stdout or "",
        stderr=stderr or "",
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Run a command with a hard process-tree timeout.")
    parser.add_argument("--timeout-seconds", type=float, required=True)
    parser.add_argument("command", nargs=argparse.REMAINDER)
    args = parser.parse_args()

    if not args.command:
        parser.error("missing command")

    command = args.command
    if command and command[0] == "--":
        command = command[1:]

    result = run_with_timeout(command, timeout_seconds=args.timeout_seconds)
    if result.stdout:
        print(result.stdout, end="")
    if result.stderr:
        print(result.stderr, end="", file=os.sys.stderr)
    return result.return_code


if __name__ == "__main__":
    raise SystemExit(main())

