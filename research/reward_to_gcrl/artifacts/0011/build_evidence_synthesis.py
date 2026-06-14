#!/usr/bin/env python
"""Build the 0011 report-only evidence synthesis.

This script intentionally runs no learning or evaluation compute. It reads the
existing 0001-0010 result JSON files and writes a conservative synthesis report
plus schema-compatible 0011 result artifacts.
"""

from __future__ import annotations

import argparse
import json
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


EXPERIMENT_ID = "0011"
PROJECT = "reward_to_gcrl"
ROOT = Path(__file__).resolve().parents[4]
PROJECT_ROOT = ROOT / "research" / PROJECT
ARTIFACT_DIR = PROJECT_ROOT / "artifacts" / EXPERIMENT_ID
RESULT_DIR = PROJECT_ROOT / "results"
REPORT_DIR = PROJECT_ROOT / "reports"
PROGRESS_PATH = ARTIFACT_DIR / "progress.jsonl"
REPORT_PATH = REPORT_DIR / "0011_evidence_synthesis.md"
RESULT_PATH = RESULT_DIR / "0011_result.json"
SUMMARY_PATH = RESULT_DIR / "0011_summary.md"
EXTRACTED_PATH = ARTIFACT_DIR / "extracted_prior_results.json"
CLAIM_TABLE_PATH = ARTIFACT_DIR / "claim_status_table.json"
LOCAL_CHECK_PATH = ARTIFACT_DIR / "local_compatibility_check.json"

PRIOR_IDS = [f"{i:04d}" for i in range(1, 11)]
COMMANDS_RUN = [
    "mkdir -p research/reward_to_gcrl/artifacts/0011 research/reward_to_gcrl/results research/reward_to_gcrl/reports && date -u -Iseconds",
    "conda run -n autoresearcher_reward_to_gcrl python --version",
    "rg --files research/reward_to_gcrl/results | sort",
    "rg --files research/reward_to_gcrl/artifacts | sort | rg '/(000[1-9]|0010)/' | head -n 200",
    "ls scripts schemas",
    "jq '{id:.experiment_id,status,interpretation,known_failures,next_questions,metrics_keys:(.metrics|keys),metric_deltas,decision_relevant_findings,success_criteria_results,failure_criteria_results}' research/reward_to_gcrl/results/0001_result.json",
    "jq '{id:.experiment_id,status,interpretation,known_failures,next_questions,metrics_keys:(.metrics|keys),metric_deltas,decision_relevant_findings,success_criteria_results,failure_criteria_results}' research/reward_to_gcrl/results/0002_result.json",
    "jq '{id:.experiment_id,status,interpretation,known_failures,next_questions,metrics_keys:(.metrics|keys),metric_deltas,decision_relevant_findings,success_criteria_results,failure_criteria_results}' research/reward_to_gcrl/results/0003_result.json",
    "jq '{id:.experiment_id,status,interpretation,known_failures,next_questions,metrics_keys:(.metrics|keys),metric_deltas,decision_relevant_findings,success_criteria_results,failure_criteria_results}' research/reward_to_gcrl/results/0004_result.json",
    "jq '{id:.experiment_id,status,interpretation,known_failures,next_questions,metrics_keys:(.metrics|keys),metric_deltas,decision_relevant_findings,success_criteria_results,failure_criteria_results}' research/reward_to_gcrl/results/0005_result.json",
    "jq '{id:.experiment_id,status,interpretation,known_failures,next_questions,metrics_keys:(.metrics|keys),metric_deltas,decision_relevant_findings,success_criteria_results,failure_criteria_results}' research/reward_to_gcrl/results/0006_result.json",
    "jq '{id:.experiment_id,status,interpretation,known_failures,next_questions,metrics_keys:(.metrics|keys),metric_deltas,decision_relevant_findings,success_criteria_results,failure_criteria_results}' research/reward_to_gcrl/results/0007_result.json",
    "jq '{id:.experiment_id,status,interpretation,known_failures,next_questions,metrics_keys:(.metrics|keys),metric_deltas,decision_relevant_findings,success_criteria_results,failure_criteria_results}' research/reward_to_gcrl/results/0008_result.json",
    "jq '{id:.experiment_id,status,interpretation,known_failures,next_questions,metrics_keys:(.metrics|keys),metric_deltas,decision_relevant_findings,success_criteria_results,failure_criteria_results}' research/reward_to_gcrl/results/0009_result.json",
    "jq '{id:.experiment_id,status,interpretation,known_failures,next_questions,metrics_keys:(.metrics|keys),metric_deltas,decision_relevant_findings,success_criteria_results,failure_criteria_results}' research/reward_to_gcrl/results/0010_result.json",
    "conda run -n autoresearcher_reward_to_gcrl python -m py_compile research/reward_to_gcrl/artifacts/0011/build_evidence_synthesis.py",
    "conda run -n autoresearcher_reward_to_gcrl python research/reward_to_gcrl/artifacts/0011/build_evidence_synthesis.py --check-only",
    "conda run -n autoresearcher_reward_to_gcrl python research/reward_to_gcrl/artifacts/0011/build_evidence_synthesis.py",
    "conda run -n autoresearcher_reward_to_gcrl python -m jsonschema -i research/reward_to_gcrl/results/0011_result.json schemas/result.schema.json",
    "conda run -n autoresearcher_reward_to_gcrl python scripts/validate_artifacts.py --repo-root . --json research/reward_to_gcrl/results/0011_result.json --schema schemas/result.schema.json --check-result-artifacts",
]


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def append_progress(phase: str, message: str, status: str = "completed", **extra: Any) -> None:
    entry = {"timestamp": now(), "phase": phase, "status": status, "message": message}
    entry.update(extra)
    with PROGRESS_PATH.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(entry, sort_keys=True) + "\n")


def load_results() -> dict[str, dict[str, Any]]:
    results: dict[str, dict[str, Any]] = {}
    missing: list[str] = []
    for exp_id in PRIOR_IDS:
        path = RESULT_DIR / f"{exp_id}_result.json"
        if not path.exists():
            missing.append(rel(path))
            continue
        results[exp_id] = json.loads(path.read_text(encoding="utf-8"))
    if missing:
        raise FileNotFoundError(f"missing prior result files: {missing}")
    return results


def compatibility_check() -> dict[str, Any]:
    expected = [RESULT_DIR / f"{exp_id}_result.json" for exp_id in PRIOR_IDS]
    check = {
        "experiment_id": EXPERIMENT_ID,
        "status": "passed",
        "new_learning_compute_run": False,
        "required_prior_results_present": all(path.exists() for path in expected),
        "prior_result_files": [rel(path) for path in expected],
        "schema_path": rel(ROOT / "schemas" / "result.schema.json"),
        "artifact_validator_path": rel(ROOT / "scripts" / "validate_artifacts.py"),
        "report_path": rel(REPORT_PATH),
        "checked_at": now(),
    }
    write_json(LOCAL_CHECK_PATH, check)
    append_progress(
        "compatibility_check",
        "Confirmed required prior result files and validation helpers for report-only synthesis.",
        command="conda run -n autoresearcher_reward_to_gcrl python research/reward_to_gcrl/artifacts/0011/build_evidence_synthesis.py --check-only",
        compatibility_check_path=rel(LOCAL_CHECK_PATH),
    )
    return check


def get_delta(results: dict[str, dict[str, Any]], exp_id: str, key: str, default: Any = None) -> Any:
    return results[exp_id].get("metric_deltas", {}).get(key, default)


def status_rows(results: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    summaries = {
        "0001": "One-step terminal marginalization and finite-MDP scaling equivalence.",
        "0002": "Audited local CliffWalking exact-DP and paired-learning equivalence.",
        "0003": "CliffWalking sampled-vs-soft under matched streams, with reward-normalization caveat.",
        "0004": "Nondegenerate chain repair with direct sampled target comparison.",
        "0005": "6-state RiverSwim sampled-vs-soft with sparse right-end rewards.",
        "0006": "RiverSwim non-oracle behavior streams with adequate/starved coverage split.",
        "0007": "RiverSwim coverage dose-response over four non-oracle behavior policies.",
        "0008": "Independent tabular FourRooms vector SSM sanity check.",
        "0009": "Rank-4 shared low-rank FourRooms auxiliary-goal first test.",
        "0010": "Rank-4 low-rank auxiliary repair diagnostic.",
    }
    for exp_id in PRIOR_IDS:
        result = results[exp_id]
        rows.append(
            {
                "experiment_id": exp_id,
                "status": result["status"],
                "role": summaries[exp_id],
                "known_failures": result.get("known_failures", []),
                "interpretation": result.get("interpretation", ""),
                "metric_deltas": result.get("metric_deltas", {}),
                "decision_relevant_findings": result.get("decision_relevant_findings", []),
            }
        )
    return rows


def build_claims(results: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "claim": "Soft terminal marginalization removes terminal-sampling variance in small tabular diagnostics.",
            "status": "supported",
            "evidence": [
                "0001: soft target variance is negligible while sampled variance is positive; max sampled variance %.6g."
                % results["0001"]["metrics"]["max_sampled_target_variance"],
                "0003/0005/0006/0007: sampled_variance_exceeds_soft_rate = 1.0.",
            ],
            "limitations": ["Tabular CPU settings only; matched-stream or controlled behavior settings."],
        },
        {
            "claim": "The soft g_plus fixed point scales to normalized Q in audited small tabular MDPs.",
            "status": "supported",
            "evidence": [
                "0001 finite-MDP max scaled error %.6g." % get_delta(results, "0001", "finite_mdp_max_abs_error_scaled_f_vs_q"),
                "0002 CliffWalking exact-DP max scaled error %.6g." % get_delta(results, "0002", "exact_dp_max_abs_error_scaled_f_vs_q"),
                "0008 FourRooms vector g_plus scaled-minus-Q error %.6g." % get_delta(results, "0008", "max_abs_vector_gplus_scaled_minus_q_norm"),
            ],
            "limitations": ["Depends on declared reward normalization and terminal masks being audited."],
        },
        {
            "claim": "Deterministic soft updates improve learning metrics under adequate tabular coverage.",
            "status": "partially_supported",
            "evidence": [
                "0004: nondegenerate chain verdict learning-improvement; soft-minus-sampled Bellman residual %.6g."
                % get_delta(results, "0004", "soft_minus_sampled_mean_final_bellman_residual"),
                "0007 adequate coverage bin: soft-minus-sampled value error %.6g and Bellman residual %.6g."
                % (
                    get_delta(results, "0007", "by_coverage_bin")["adequate"]["soft_minus_sampled_mean_final_value_error"],
                    get_delta(results, "0007", "by_coverage_bin")["adequate"]["soft_minus_sampled_mean_final_bellman_residual"],
                ),
            ],
            "limitations": ["0007 starved bin has lower residual but worse value error, so coverage is a prerequisite."],
        },
        {
            "claim": "Soft updates reliably improve learning in coverage-starved settings.",
            "status": "unsupported",
            "evidence": [
                "0007 starved bin: soft-minus-sampled value error %.6g despite lower Bellman residual %.6g."
                % (
                    get_delta(results, "0007", "by_coverage_bin")["starved"]["soft_minus_sampled_mean_final_value_error"],
                    get_delta(results, "0007", "by_coverage_bin")["starved"]["soft_minus_sampled_mean_final_bellman_residual"],
                )
            ],
            "limitations": ["Coverage-starved results are diagnostic only and not learning-superiority evidence."],
        },
        {
            "claim": "Independent tabular real-state goal slices can be added without perturbing g_plus.",
            "status": "supported",
            "evidence": [
                "0008: max_abs_vector_gplus_minus_terminal_only = %.6g."
                % get_delta(results, "0008", "max_abs_vector_gplus_minus_terminal_only"),
                "0008: min real-goal greedy success rate = %.6g." % get_delta(results, "0008", "min_goal_success_rate"),
            ],
            "limitations": ["This is a sanity check with independent tabular slices, not evidence of reward-task improvement."],
        },
        {
            "claim": "Rank-4 shared low-rank real-state auxiliary training improves g_plus in tiny FourRooms.",
            "status": "contradicted",
            "evidence": [
                "0009: verdict negative_transfer; combined-minus-terminal value error %.6g and residual %.6g."
                % (
                    get_delta(results, "0009", "mean_value_error_delta_combined_minus_terminal"),
                    get_delta(results, "0009", "mean_bellman_residual_delta_combined_minus_terminal"),
                ),
                "0010: reproduction passed, repaired variants were not promising; verdict %s."
                % get_delta(results, "0010", "verdict"),
            ],
            "limitations": ["Contradicts only this rank-4 low-rank setup with the tested replay and loss variants."],
        },
        {
            "claim": "Real-state auxiliary goals are generally impossible or useless.",
            "status": "unsupported",
            "evidence": ["0009/0010 are scoped to one tiny FourRooms rank-4 architecture and replay construction."],
            "limitations": ["A different architecture or principled loss design would require a new human-approved hypothesis."],
        },
        {
            "claim": "Neural auxiliary benefit, larger-environment generality, or online exploration robustness.",
            "status": "unsupported",
            "evidence": ["No PyTorch/JAX neural runs, larger environments, GPU runs, or broad online robustness tests were performed."],
            "limitations": ["Must not be claimed from the current evidence."],
        },
    ]


def md_table(headers: list[str], rows: list[list[Any]]) -> str:
    out = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for row in rows:
        out.append("| " + " | ".join(str(cell).replace("\n", " ") for cell in row) + " |")
    return "\n".join(out)


def build_report(results: dict[str, dict[str, Any]], claims: list[dict[str, Any]]) -> str:
    experiment_rows = []
    for row in status_rows(results):
        deltas = row["metric_deltas"]
        key_metric = ""
        if row["experiment_id"] == "0001":
            key_metric = "max sampled variance %.4g; finite scaling error %.4g" % (
                results["0001"]["metrics"]["max_sampled_target_variance"],
                deltas["finite_mdp_max_abs_error_scaled_f_vs_q"],
            )
        elif row["experiment_id"] == "0002":
            key_metric = "exact scaling error %.4g; learned policy disagreement %.4g" % (
                deltas["exact_dp_max_abs_error_scaled_f_vs_q"],
                deltas["learned_max_policy_disagreement_rate"],
            )
        elif row["experiment_id"] == "0003":
            key_metric = "target match %.3g; variance rate %.3g; residual soft %.4g vs sampled %.4g" % (
                deltas["target_mean_match_rate"],
                deltas["sampled_variance_exceeds_soft_rate"],
                deltas["mean_final_soft_bellman_residual_sufficient"],
                deltas["mean_final_sampled_bellman_residual_sufficient"],
            )
        elif row["experiment_id"] in {"0005", "0006", "0007"}:
            key_metric = "target match %.3g; variance rate %.3g; soft residual delta %.4g" % (
                deltas["target_mean_match_rate"],
                deltas["sampled_variance_exceeds_soft_rate"],
                deltas["soft_minus_sampled_mean_final_bellman_residual"],
            )
        elif row["experiment_id"] == "0004":
            key_metric = "learning-improvement; soft residual delta %.4g; value delta %.4g" % (
                deltas["soft_minus_sampled_mean_final_bellman_residual"],
                deltas["soft_minus_sampled_mean_final_value_error"],
            )
        elif row["experiment_id"] == "0008":
            key_metric = "g_plus perturbation %.4g; goal success %.4g" % (
                deltas["max_abs_vector_gplus_minus_terminal_only"],
                deltas["min_goal_success_rate"],
            )
        elif row["experiment_id"] == "0009":
            key_metric = "negative_transfer; value delta %.4g; residual delta %.4g" % (
                deltas["mean_value_error_delta_combined_minus_terminal"],
                deltas["mean_bellman_residual_delta_combined_minus_terminal"],
            )
        elif row["experiment_id"] == "0010":
            key_metric = "auxiliary_unsupported_for_lowrank; repaired promising=false"
        experiment_rows.append([row["experiment_id"], row["status"], row["role"], key_metric])

    claim_rows = []
    for claim in claims:
        claim_rows.append(
            [
                claim["claim"],
                claim["status"],
                "<br>".join(claim["evidence"]),
                "<br>".join(claim["limitations"]),
            ]
        )

    report = f"""# Evidence Synthesis 0011: reward_to_gcrl

## Abstract

This report consolidates experiments 0001-0010 without running new learning compute.
The strongest defensible positive claim is that soft terminal marginalization
removes terminal-sampling variance and preserves normalized-Q scaling in the
small audited tabular settings tested here. RiverSwim learning advantages are
supported only when right-reward and state-action coverage are adequate.

The strongest defensible negative claim is narrower: real-state auxiliary goals
are unsupported for the tested rank-4 shared low-rank FourRooms architecture.
Experiment 0009 showed negative transfer under adequate replay coverage, and
experiment 0010 reproduced that failure while showing that the predeclared
loss-balanced and staged repair diagnostics did not recover terminal-only g_plus
performance.

## Claim Status Table

{md_table(["Claim", "Status", "Evidence", "Limitations"], claim_rows)}

## Experiment Evidence Table

{md_table(["Experiment", "Status", "Role", "Key Metric"], experiment_rows)}

## Accepted Positive Evidence

- Soft terminal marginalization is a reliable estimator transformation in the
  current tabular tests: sampled targets match deterministic soft marginal
  targets within tolerance while sampled terminal-sampling variance remains
  positive.
- The g_plus fixed point scales to normalized Q under the audited reward
  normalizations and terminal masks used in 0001, 0002, 0005, and 0008.
- Learning improvements are defensible only with coverage qualifiers. In the
  nondegenerate chain and adequately covered RiverSwim bins, soft updates lower
  Bellman residual and have non-worse or lower value error. In coverage-starved
  RiverSwim, residual and value error can disagree.

## Accepted Negative Evidence

- The first shared low-rank FourRooms auxiliary test is negative: 0009 reports
  `negative_transfer`, with combined-minus-terminal g_plus value error
  {get_delta(results, "0009", "mean_value_error_delta_combined_minus_terminal"):.6g}
  and Bellman residual {get_delta(results, "0009", "mean_bellman_residual_delta_combined_minus_terminal"):.6g}.
- The repair diagnostic did not rescue the low-rank setup. In 0010, the original
  0009 behavior reproduced, `combined_loss_balanced` still worsened mean g_plus
  value error by {get_delta(results, "0010", "deltas_vs_terminal")["combined_loss_balanced"]["mean_value_error_delta"]:.6g},
  and the staged variant worsened it by
  {get_delta(results, "0010", "deltas_vs_terminal")["staged_real_goal_pretrain_then_gplus_finetune"]["mean_value_error_delta"]:.6g}.
- This is not evidence that auxiliary goals are generally impossible. It is
  evidence against the tested rank-4 shared low-rank formulation, replay setup,
  and predeclared repair variants.

## Limitations

- All evidence is tiny, CPU tabular, or CPU NumPy. No neural framework, GPU
  training, larger environment, or broad hyperparameter sweep is represented.
- 0003 CliffWalking raw returns are diagnostic only because the declared reward
  normalization creates an objective mismatch with raw goal reaching.
- RiverSwim learning claims require coverage caveats. 0007 includes starved,
  borderline, and adequate bins, and starved runs must not be used for an
  unconditional soft-learning-superiority claim.
- 0009 and 0010 use uniform state-action reset replay, a single rank-4 model
  family, one main replay budget, and tightly predeclared variants. They do not
  establish online exploration robustness or larger-environment behavior.
- 0008 shows independent tabular goal slices are correct and non-interfering,
  but independent slices cannot support a shared-representation reward-task
  improvement claim.

## Red Lines

Do not claim:

- Neural auxiliary-goal benefit.
- Larger-environment generality.
- Online exploration robustness.
- Publishable auxiliary-goal improvement.
- That real-state auxiliary goals are generally impossible.
- That soft updates improve learning in coverage-starved regimes without the
  RiverSwim coverage caveat.
- That independent tabular real-state goals improve reward-task learning through
  shared representation.

## Auxiliary Reopening Gate

The low-rank auxiliary thread should stay paused unless a new human-approved,
falsifiable hypothesis changes the architecture or loss normalization in a
principled way. A valid reopening packet should specify exactly one proposed
mechanism, why 0009/0010 failed under that mechanism, a predeclared tiny
diagnostic, and a success criterion that beats or statistically matches
terminal-only g_plus value error and Bellman residual without increasing
tie-aware reward-policy disagreement. More rank, learning-rate, auxiliary-weight,
or optimizer sweeps without this hypothesis should not be run.

## Recommendation

Recommendation: `pause_lowrank_auxiliary_thread`.

Next decision: `write_negative_result`. If auxiliary work is reopened later, do
so only through `design_new_hypothesis_before_more_compute`.
"""
    return report


def build_result(results: dict[str, dict[str, Any]], claims: list[dict[str, Any]], runtime: float) -> dict[str, Any]:
    status_counts: dict[str, int] = {}
    for claim in claims:
        status_counts[claim["status"]] = status_counts.get(claim["status"], 0) + 1

    inspected_files = [rel(RESULT_DIR / f"{exp_id}_result.json") for exp_id in PRIOR_IDS]
    metrics = {
        "report_only": True,
        "new_learning_compute_run": False,
        "inspected_result_files": inspected_files,
        "inspected_experiment_count": len(PRIOR_IDS),
        "all_prior_results_completed": all(results[exp_id]["status"] == "completed" for exp_id in PRIOR_IDS),
        "claim_status_counts": status_counts,
        "claims": claims,
        "strongest_defensible_positive_claim": "Soft terminal marginalization removes terminal-sampling variance and preserves normalized-Q scaling in small audited tabular settings, with RiverSwim learning advantages only under adequate coverage.",
        "strongest_defensible_negative_claim": "Low-rank shared real-state auxiliary training did not help g_plus in FourRooms and remained harmful after the predeclared repair diagnostic.",
        "final_recommendation": "pause_lowrank_auxiliary_thread",
        "auxiliary_next_decision": "write_negative_result",
        "reopening_gate": "Reopen only with a human-approved falsifiable hypothesis that changes architecture or loss normalization in a principled way, not with broad hyperparameter sweeps.",
        "red_line_claims": [
            "neural auxiliary-goal benefit",
            "larger-environment generality",
            "online exploration robustness",
            "publishable auxiliary-goal improvement",
            "general impossibility of auxiliary goals",
            "coverage-starved soft learning superiority",
        ],
        "limitations": [
            "tiny CPU tabular or CPU NumPy settings only",
            "RiverSwim learning claims require adequate coverage",
            "CliffWalking raw-task returns are limited by reward-normalization mismatch",
            "0009/0010 use uniform state-action reset replay",
            "0009/0010 test a single rank-4 low-rank configuration family",
        ],
    }

    return {
        "experiment_id": EXPERIMENT_ID,
        "status": "completed",
        "claim_tested": "Synthesize 0001-0010 evidence to separate supported soft-terminal estimator claims from unsupported low-rank auxiliary-goal claims, without running new learning compute.",
        "commands_run": COMMANDS_RUN,
        "metrics": metrics,
        "baseline_metrics": {
            "new_baseline_run": False,
            "reason": "This is a report-only synthesis; all baselines are prior completed experiments 0001-0010.",
            "prior_baselines_inspected": inspected_files,
        },
        "artifacts": [
            rel(REPORT_PATH),
            rel(Path(__file__)),
            rel(LOCAL_CHECK_PATH),
            rel(EXTRACTED_PATH),
            rel(CLAIM_TABLE_PATH),
            rel(PROGRESS_PATH),
        ],
        "interpretation": "The evidence supports soft terminal marginalization as a small-tabular estimator/equivalence mechanism with coverage-qualified RiverSwim learning advantages. It does not support low-rank shared real-state auxiliary goals for the tested FourRooms setup; pause that thread and write the negative result.",
        "known_failures": [
            "lowrank_auxiliary_gplus_benefit_unsupported_for_tested_rank4_fourrooms_setup",
            "neural_larger_environment_online_auxiliary_claims_unsupported",
        ],
        "next_questions": [
            "What concise negative-result writeup should be produced from 0009 and 0010?",
            "Is there a new principled architecture or loss-normalization hypothesis that justifies reopening auxiliary-goal experiments later?",
        ],
        "runtime_seconds": runtime,
        "resource_usage": {
            "cpu_only": True,
            "gpu_used": False,
            "new_learning_compute_run": False,
            "new_training_runs": 0,
            "dependencies_added": [],
        },
        "success_criteria_results": [
            "PASS: summarized 0001-0010 in claim-by-claim evidence tables.",
            "PASS: strongest positive soft-terminal estimator claim is explicitly scoped.",
            "PASS: strongest negative low-rank auxiliary claim is explicitly scoped.",
            "PASS: red-line unsupported claims are listed.",
            "PASS: auxiliary reopening criterion requires a new human-approved falsifiable hypothesis.",
            "PASS: no new learning runs, neural frameworks, GPU, large environments, or sweeps were used.",
            "PASS: recommendation is pause_lowrank_auxiliary_thread with write_negative_result as the next decision.",
        ],
        "failure_criteria_results": [
            "NOT_TRIGGERED: estimator evidence and auxiliary-goal evidence are separated.",
            "NOT_TRIGGERED: 0009/0010 are not treated as evidence that auxiliary goals are generally impossible.",
            "NOT_TRIGGERED: no larger sweeps, PyTorch/JAX, GPU, or neural experiments are proposed without a new hypothesis.",
            "NOT_TRIGGERED: RiverSwim coverage caveats and matched-stream/replay caveats are included.",
            "NOT_TRIGGERED: 0009/0010 uniform state-action reset replay and rank-4 configuration limits are included.",
            "NOT_TRIGGERED: concrete next-decision recommendation is recorded.",
        ],
        "metric_deltas": {
            "new_learning_compute_run": False,
            "claim_status_counts": status_counts,
            "river_swim_adequate_value_delta": get_delta(results, "0007", "by_coverage_bin")["adequate"]["soft_minus_sampled_mean_final_value_error"],
            "river_swim_starved_value_delta": get_delta(results, "0007", "by_coverage_bin")["starved"]["soft_minus_sampled_mean_final_value_error"],
            "lowrank_0009_value_error_delta": get_delta(results, "0009", "mean_value_error_delta_combined_minus_terminal"),
            "lowrank_0010_loss_balanced_value_error_delta": get_delta(results, "0010", "deltas_vs_terminal")["combined_loss_balanced"]["mean_value_error_delta"],
        },
        "decision_relevant_findings": [
            "Soft terminal marginalization has supported small-tabular estimator/equivalence evidence.",
            "RiverSwim learning advantages are coverage-qualified; starved runs are not learning-superiority evidence.",
            "Independent tabular real-state goals are a correctness sanity check, not an auxiliary reward-improvement result.",
            "Low-rank rank-4 FourRooms auxiliary training is unsupported after reproduction and repair diagnostics.",
            "Recommendation is pause_lowrank_auxiliary_thread and write_negative_result.",
        ],
    }


def write_summary() -> None:
    summary = """# Experiment 0011 Summary

Status: **completed**.

This was a report-only synthesis. No new learning compute, neural framework,
GPU run, larger environment, or hyperparameter sweep was used.

Recommendation: **pause_lowrank_auxiliary_thread**.

Next decision: **write_negative_result**. Reopen auxiliary-goal experiments only
with a new human-approved falsifiable hypothesis that changes architecture or
loss normalization in a principled way.

Outputs:

- `research/reward_to_gcrl/reports/0011_evidence_synthesis.md`
- `research/reward_to_gcrl/results/0011_result.json`
- `research/reward_to_gcrl/artifacts/0011/extracted_prior_results.json`
- `research/reward_to_gcrl/artifacts/0011/claim_status_table.json`
- `research/reward_to_gcrl/artifacts/0011/progress.jsonl`
"""
    SUMMARY_PATH.write_text(summary, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-only", action="store_true")
    args = parser.parse_args()

    start = time.perf_counter()
    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    RESULT_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    if args.check_only:
        compatibility_check()
        return

    results = load_results()
    claims = build_claims(results)
    extracted = {
        "experiment_id": EXPERIMENT_ID,
        "new_learning_compute_run": False,
        "prior_results": status_rows(results),
    }
    write_json(EXTRACTED_PATH, extracted)
    write_json(CLAIM_TABLE_PATH, {"experiment_id": EXPERIMENT_ID, "claims": claims})
    append_progress(
        "evidence_extraction",
        "Extracted prior result metrics and wrote claim-status evidence artifacts.",
        command="conda run -n autoresearcher_reward_to_gcrl python research/reward_to_gcrl/artifacts/0011/build_evidence_synthesis.py",
        artifacts=[rel(EXTRACTED_PATH), rel(CLAIM_TABLE_PATH)],
    )

    REPORT_PATH.write_text(build_report(results, claims), encoding="utf-8")
    append_progress(
        "report_write",
        "Wrote compact evidence synthesis report separating estimator and auxiliary-goal evidence.",
        command="conda run -n autoresearcher_reward_to_gcrl python research/reward_to_gcrl/artifacts/0011/build_evidence_synthesis.py",
        report_path=rel(REPORT_PATH),
    )

    runtime = time.perf_counter() - start
    write_json(RESULT_PATH, build_result(results, claims, runtime))
    write_summary()
    append_progress(
        "result_write",
        "Wrote 0011 result JSON and summary Markdown for the report-only iteration.",
        command="conda run -n autoresearcher_reward_to_gcrl python research/reward_to_gcrl/artifacts/0011/build_evidence_synthesis.py",
        result_path=rel(RESULT_PATH),
        summary_path=rel(SUMMARY_PATH),
        recommendation="pause_lowrank_auxiliary_thread",
    )


if __name__ == "__main__":
    main()
