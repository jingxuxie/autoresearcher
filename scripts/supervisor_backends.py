"""Supervisor backend abstraction for local/manual/ChatGPT Pro decisions."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional

from chatgpt_pro_bridge import run_chatgpt_pro_review, run_chatgpt_pro_review_cdp, write_pro_blocker


@dataclass
class SupervisorBackendResult:
    status: str  # completed | blocked | failed
    decision_path: Optional[Path] = None
    markdown_path: Optional[Path] = None
    raw_response_path: Optional[Path] = None
    blocker_path: Optional[Path] = None
    blocker_markdown_path: Optional[Path] = None
    reason: Optional[str] = None


class SupervisorBackend:
    def decide(
        self,
        repo_root: Path,
        project: str,
        config: Dict[str, Any],
        packet_path: Path,
        checkpoint_reason: str,
        iteration_id: str,
    ) -> SupervisorBackendResult:
        raise NotImplementedError


class CodexSupervisorBackend(SupervisorBackend):
    """Placeholder for local Codex supervisor compatibility."""

    def decide(
        self,
        repo_root: Path,
        project: str,
        config: Dict[str, Any],
        packet_path: Path,
        checkpoint_reason: str,
        iteration_id: str,
    ) -> SupervisorBackendResult:
        blocker_json, blocker_md = write_pro_blocker(
            repo_root,
            project,
            iteration_id,
            "manual_review_required",
            "CodexSupervisorBackend is not used for Pro checkpoint authority.",
            packet_path=packet_path,
        )
        return SupervisorBackendResult(
            status="blocked",
            blocker_path=blocker_json,
            blocker_markdown_path=blocker_md,
            reason="manual_review_required",
        )


class ManualProPacketBackend(SupervisorBackend):
    def decide(
        self,
        repo_root: Path,
        project: str,
        config: Dict[str, Any],
        packet_path: Path,
        checkpoint_reason: str,
        iteration_id: str,
    ) -> SupervisorBackendResult:
        blocker_json, blocker_md = write_pro_blocker(
            repo_root,
            project,
            iteration_id,
            "manual_review_required",
            "Automatic ChatGPT Pro review is disabled. Upload the packet manually and ingest the response.",
            packet_path=packet_path,
        )
        return SupervisorBackendResult(
            status="blocked",
            blocker_path=blocker_json,
            blocker_markdown_path=blocker_md,
            reason="manual_review_required",
        )


class ChatGPTProSupervisorBackend(SupervisorBackend):
    def decide(
        self,
        repo_root: Path,
        project: str,
        config: Dict[str, Any],
        packet_path: Path,
        checkpoint_reason: str,
        iteration_id: str,
    ) -> SupervisorBackendResult:
        result = run_chatgpt_pro_review(
            repo_root,
            project,
            config,
            packet_path,
            checkpoint_reason,
            iteration_id,
        )
        return SupervisorBackendResult(
            status=str(result.get("status", "failed")),
            decision_path=result.get("decision_path"),
            markdown_path=result.get("markdown_path"),
            raw_response_path=result.get("raw_response_path"),
            blocker_path=result.get("blocker_path"),
            blocker_markdown_path=result.get("blocker_markdown_path"),
            reason=result.get("reason"),
        )


class ChatGPTCdpSupervisorBackend(SupervisorBackend):
    def decide(
        self,
        repo_root: Path,
        project: str,
        config: Dict[str, Any],
        packet_path: Path,
        checkpoint_reason: str,
        iteration_id: str,
    ) -> SupervisorBackendResult:
        result = run_chatgpt_pro_review_cdp(
            repo_root,
            project,
            config,
            packet_path,
            checkpoint_reason,
            iteration_id,
        )
        return SupervisorBackendResult(
            status=str(result.get("status", "failed")),
            decision_path=result.get("decision_path"),
            markdown_path=result.get("markdown_path"),
            raw_response_path=result.get("raw_response_path"),
            blocker_path=result.get("blocker_path"),
            blocker_markdown_path=result.get("blocker_markdown_path"),
            reason=result.get("reason"),
        )


def supervisor_backend_for_config(config: Dict[str, Any], backend_override: str = "auto") -> SupervisorBackend:
    if backend_override == "manual":
        return ManualProPacketBackend()
    if backend_override == "live":
        return ChatGPTProSupervisorBackend()
    if backend_override == "cdp":
        return ChatGPTCdpSupervisorBackend()
    if backend_override not in ("auto", ""):
        raise RuntimeError(f"unknown Pro backend override {backend_override!r}")

    pro_cfg = config.get("chatgpt_pro", {}) if isinstance(config.get("chatgpt_pro"), dict) else {}
    if bool(pro_cfg.get("enabled", False)) or os.environ.get("FAKE_CHATGPT_PRO") is not None:
        if pro_cfg.get("backend") == "cdp":
            return ChatGPTCdpSupervisorBackend()
        return ChatGPTProSupervisorBackend()
    return ManualProPacketBackend()
