"""Deterministic checkpoint policy for Pro supervision gates."""

from __future__ import annotations

from typing import Any, Dict, Optional, Tuple


TERMINAL_LOCAL_DECISIONS = {"stop", "pivot", "needs_human"}
ESCALATING_REVIEW_VERDICTS = {"fail", "needs_human"}


def _as_dict(value: Any) -> Dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _decision_kind(local_decision: Any) -> Optional[str]:
    if isinstance(local_decision, dict):
        decision = local_decision.get("decision")
        return str(decision) if isinstance(decision, str) else None
    if isinstance(local_decision, str):
        return local_decision
    return None


def _cadence_due(state: Dict[str, Any], config: Dict[str, Any]) -> bool:
    pro_cfg = _as_dict(config.get("chatgpt_pro"))
    if not bool(pro_cfg.get("enabled", False)):
        return False
    cadence = int(pro_cfg.get("cadence_iterations", 3) or 3)
    if cadence not in (2, 3) and pro_cfg.get("allow_cadence_2_or_3", True):
        cadence = 3
    completed = int(state.get("iteration", 0) or 0)
    last = int(state.get("last_pro_review_iteration", 0) or 0)
    return completed > 0 and completed - last >= cadence


def pro_checkpoint_due(
    state: Dict[str, Any],
    config: Dict[str, Any],
    local_decision: Any = None,
    latest_review: Any = None,
    latest_result: Any = None,
) -> Tuple[bool, str]:
    """Return whether a Pro/manual checkpoint should be requested and why.

    Cadence checkpoints only run when ChatGPT Pro is enabled. Critical local
    terminal decisions and invalid evidence gates still request a manual packet
    when Pro is disabled, so local Codex is not the final stop/pivot authority.
    """

    local_kind = _decision_kind(local_decision)
    if local_kind in TERMINAL_LOCAL_DECISIONS:
        return True, f"local_{local_kind}"

    if isinstance(local_decision, dict) and bool(local_decision.get("checkpoint_recommended", False)):
        reason = local_decision.get("checkpoint_reason")
        return True, str(reason or "local_checkpoint_recommended")

    result = _as_dict(latest_result)
    if result.get("status") == "timeout":
        return True, "result_timeout"

    review = _as_dict(latest_review)
    verdict = review.get("verdict")
    if verdict in ESCALATING_REVIEW_VERDICTS:
        return True, f"review_{verdict}"
    if bool(review.get("should_escalate_to_pro", False)):
        return True, str(review.get("escalation_reason") or "review_requested_pro")

    if int(state.get("weak_pass_streak", 0) or 0) >= 2:
        return True, "weak_pass_streak"

    loop_cfg = _as_dict(config.get("loop"))
    max_no_progress = int(loop_cfg.get("max_no_progress_rounds", 3) or 3)
    no_progress = int(state.get("no_progress_rounds", 0) or 0)
    if max_no_progress > 0 and no_progress >= max_no_progress - 1:
        return True, "no_progress_near_limit"

    if bool(state.get("protected_file_drift", False)):
        return True, "protected_file_drift"

    if _cadence_due(state, config):
        return True, "cadence"

    return False, ""


def pro_review_due(state: Dict[str, Any], config: Dict[str, Any]) -> bool:
    """Backward-compatible cadence-only helper."""

    return _cadence_due(state, config)
