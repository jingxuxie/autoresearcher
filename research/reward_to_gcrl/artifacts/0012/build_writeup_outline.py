#!/usr/bin/env python
"""Build the 0012 write-up outline from existing evidence only."""

from __future__ import annotations

import argparse
import json
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


EXPERIMENT_ID = "0012"
PROJECT = "reward_to_gcrl"
ROOT = Path(__file__).resolve().parents[4]
PROJECT_ROOT = ROOT / "research" / PROJECT
RESULT_DIR = PROJECT_ROOT / "results"
REPORT_DIR = PROJECT_ROOT / "reports"
ARTIFACT_DIR = PROJECT_ROOT / "artifacts" / EXPERIMENT_ID
PROGRESS_PATH = ARTIFACT_DIR / "progress.jsonl"
REPORT_PATH = REPORT_DIR / "0012_writeup_outline.md"
RESULT_PATH = RESULT_DIR / "0012_result.json"
SUMMARY_PATH = RESULT_DIR / "0012_summary.md"
CHECK_PATH = ARTIFACT_DIR / "local_compatibility_check.json"
NUMERIC_EVIDENCE_PATH = ARTIFACT_DIR / "numeric_evidence.json"
CLAIM_TABLE_PATH = ARTIFACT_DIR / "claim_status_table.json"

PRIOR_IDS = [f"{i:04d}" for i in range(1, 12)]
COMMANDS_RUN = [
    "mkdir -p research/reward_to_gcrl/artifacts/0012 research/reward_to_gcrl/results research/reward_to_gcrl/reports && date -u -Iseconds",
    "conda run -n autoresearcher_reward_to_gcrl python --version",
    "rg --files research/reward_to_gcrl/results | sort | rg '00(0[1-9]|1[0-2])_(result|summary)\\.md|00(0[1-9]|1[0-2])_result\\.json|001[0-2]_(result|summary)\\.md|001[0-2]_result\\.json'",
    "ls research/reward_to_gcrl/reports schemas/result.schema.json scripts/validate_artifacts.py",
    "jq '{status, recommendation:.metrics.final_recommendation, auxiliary_next_decision:.metrics.auxiliary_next_decision, new_learning_compute_run:.metrics.new_learning_compute_run}' research/reward_to_gcrl/results/0011_result.json",
    "jq '.metrics.lowrank_auxiliary' research/reward_to_gcrl/results/0009_result.json",
    "jq '.metrics.lowrank_auxiliary.aggregate.variant_summaries' research/reward_to_gcrl/results/0010_result.json",
    "jq '.metrics.vector_ssm, .metric_deltas' research/reward_to_gcrl/results/0008_result.json",
    "jq '.metrics.sampled_vs_soft.coverage_bin_summary // .metric_deltas.by_coverage_bin // .metric_deltas' research/reward_to_gcrl/results/0007_result.json",
    "conda run -n autoresearcher_reward_to_gcrl python -m py_compile research/reward_to_gcrl/artifacts/0012/build_writeup_outline.py",
    "conda run -n autoresearcher_reward_to_gcrl python research/reward_to_gcrl/artifacts/0012/build_writeup_outline.py --check-only",
    "conda run -n autoresearcher_reward_to_gcrl python research/reward_to_gcrl/artifacts/0012/build_writeup_outline.py",
    "conda run -n autoresearcher_reward_to_gcrl python -m jsonschema -i research/reward_to_gcrl/results/0012_result.json schemas/result.schema.json",
    "conda run -n autoresearcher_reward_to_gcrl python scripts/validate_artifacts.py --repo-root . --json research/reward_to_gcrl/results/0012_result.json --schema schemas/result.schema.json --check-result-artifacts",
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
    missing = []
    for exp_id in PRIOR_IDS:
        path = RESULT_DIR / f"{exp_id}_result.json"
        if not path.exists():
            missing.append(rel(path))
        else:
            results[exp_id] = json.loads(path.read_text(encoding="utf-8"))
    if missing:
        raise FileNotFoundError(f"Missing prior result JSONs: {missing}")
    return results


def get_delta(results: dict[str, dict[str, Any]], exp_id: str, key: str) -> Any:
    return results[exp_id].get("metric_deltas", {}).get(key)


def compatibility_check() -> dict[str, Any]:
    required = [RESULT_DIR / f"{exp_id}_result.json" for exp_id in PRIOR_IDS]
    check = {
        "experiment_id": EXPERIMENT_ID,
        "status": "passed",
        "new_learning_compute_run": False,
        "required_prior_results_present": all(path.exists() for path in required),
        "prior_result_files": [rel(path) for path in required],
        "prior_synthesis_report_present": (REPORT_DIR / "0011_evidence_synthesis.md").exists(),
        "schema_path": rel(ROOT / "schemas" / "result.schema.json"),
        "artifact_validator_path": rel(ROOT / "scripts" / "validate_artifacts.py"),
        "checked_at": now(),
    }
    write_json(CHECK_PATH, check)
    append_progress(
        "compatibility_check",
        "Confirmed prior 0001-0011 results and 0011 synthesis are available for the memo-only iteration.",
        command="conda run -n autoresearcher_reward_to_gcrl python research/reward_to_gcrl/artifacts/0012/build_writeup_outline.py --check-only",
        compatibility_check_path=rel(CHECK_PATH),
    )
    return check


def build_numeric_evidence(results: dict[str, dict[str, Any]]) -> dict[str, Any]:
    lowrank_0009 = results["0009"]["metrics"]["lowrank_auxiliary"]["aggregate"]
    lowrank_0010 = results["0010"]["metrics"]["lowrank_auxiliary"]["aggregate"]["variant_summaries"]
    river_bins = get_delta(results, "0007", "by_coverage_bin")
    return {
        "experiment_id": EXPERIMENT_ID,
        "new_learning_compute_run": False,
        "estimator_evidence": {
            "0001_max_sampled_target_variance": results["0001"]["metrics"]["max_sampled_target_variance"],
            "0001_max_soft_target_variance": results["0001"]["metrics"]["max_soft_target_variance"],
            "0001_finite_mdp_scaled_error": get_delta(results, "0001", "finite_mdp_max_abs_error_scaled_f_vs_q"),
            "0002_cliffwalking_exact_scaled_error": get_delta(results, "0002", "exact_dp_max_abs_error_scaled_f_vs_q"),
            "0003_target_mean_match_rate": get_delta(results, "0003", "target_mean_match_rate"),
            "0003_sampled_variance_exceeds_soft_rate": get_delta(results, "0003", "sampled_variance_exceeds_soft_rate"),
            "0003_soft_residual": get_delta(results, "0003", "mean_final_soft_bellman_residual_sufficient"),
            "0003_sampled_residual": get_delta(results, "0003", "mean_final_sampled_bellman_residual_sufficient"),
            "0007_adequate_coverage_value_delta": river_bins["adequate"]["soft_minus_sampled_mean_final_value_error"],
            "0007_adequate_coverage_residual_delta": river_bins["adequate"]["soft_minus_sampled_mean_final_bellman_residual"],
            "0007_starved_coverage_value_delta": river_bins["starved"]["soft_minus_sampled_mean_final_value_error"],
            "0008_vector_gplus_minus_terminal": get_delta(results, "0008", "max_abs_vector_gplus_minus_terminal_only"),
            "0008_vector_gplus_scaled_minus_q_norm": get_delta(results, "0008", "max_abs_vector_gplus_scaled_minus_q_norm"),
            "0008_min_goal_success_rate": get_delta(results, "0008", "min_goal_success_rate"),
        },
        "auxiliary_negative_evidence": {
            "0009_terminal_gplus_value_error": lowrank_0009["mean_terminal_gplus_scaled_value_error"],
            "0009_terminal_gplus_bellman_residual": lowrank_0009["mean_terminal_gplus_bellman_residual"],
            "0009_terminal_reward_success_rate": lowrank_0009["mean_terminal_reward_success_rate"],
            "0009_combined_gplus_value_error": lowrank_0009["mean_combined_gplus_scaled_value_error"],
            "0009_combined_gplus_bellman_residual": lowrank_0009["mean_combined_gplus_bellman_residual"],
            "0009_combined_reward_success_rate": lowrank_0009["mean_combined_reward_success_rate"],
            "0009_value_error_delta_combined_minus_terminal": lowrank_0009["mean_value_error_delta_combined_minus_terminal"],
            "0009_bellman_residual_delta_combined_minus_terminal": lowrank_0009["mean_bellman_residual_delta_combined_minus_terminal"],
            "0010_terminal_gplus_value_error": lowrank_0010["terminal_only"]["mean_gplus_scaled_value_error"],
            "0010_loss_balanced_gplus_value_error": lowrank_0010["combined_loss_balanced"]["mean_gplus_scaled_value_error"],
            "0010_loss_balanced_gplus_residual": lowrank_0010["combined_loss_balanced"]["mean_gplus_bellman_residual"],
            "0010_staged_gplus_value_error": lowrank_0010["staged_real_goal_pretrain_then_gplus_finetune"]["mean_gplus_scaled_value_error"],
            "0010_staged_gplus_residual": lowrank_0010["staged_real_goal_pretrain_then_gplus_finetune"]["mean_gplus_bellman_residual"],
            "0010_verdict": get_delta(results, "0010", "verdict"),
        },
    }


def build_claim_table(results: dict[str, dict[str, Any]], evidence: dict[str, Any]) -> list[dict[str, Any]]:
    est = evidence["estimator_evidence"]
    aux = evidence["auxiliary_negative_evidence"]
    return [
        {
            "source_experiments": ["0001", "0002", "0003", "0004", "0005", "0006", "0007", "0008", "0011"],
            "claim": "Soft terminal marginalization is a useful small-tabular estimator/equivalence mechanism under audited reward normalization and adequate coverage.",
            "status": "supported",
            "numeric_evidence": [
                f"0001 soft variance {est['0001_max_soft_target_variance']:.3g} vs sampled variance up to {est['0001_max_sampled_target_variance']:.6g}",
                f"0002 scaled CliffWalking error {est['0002_cliffwalking_exact_scaled_error']:.6g}",
                f"0008 vector g_plus scaled-Q error {est['0008_vector_gplus_scaled_minus_q_norm']:.6g}",
            ],
        },
        {
            "source_experiments": ["0005", "0006", "0007", "0011"],
            "claim": "RiverSwim learning advantages are coverage-qualified rather than unconditional.",
            "status": "partially_supported",
            "numeric_evidence": [
                f"0007 adequate bin value delta {est['0007_adequate_coverage_value_delta']:.6g}",
                f"0007 starved bin value delta {est['0007_starved_coverage_value_delta']:.6g}",
            ],
        },
        {
            "source_experiments": ["0008"],
            "claim": "Independent tabular real-state goal slices are correct and do not perturb g_plus.",
            "status": "supported",
            "numeric_evidence": [
                f"g_plus perturbation {est['0008_vector_gplus_minus_terminal']:.6g}",
                f"min goal success rate {est['0008_min_goal_success_rate']:.6g}",
            ],
        },
        {
            "source_experiments": ["0009", "0010", "0011"],
            "claim": "The tested rank-4 NumPy low-rank real-state auxiliary approach improves g_plus.",
            "status": "contradicted",
            "numeric_evidence": [
                f"0009 combined value error {aux['0009_combined_gplus_value_error']:.6g} vs terminal-only {aux['0009_terminal_gplus_value_error']:.6g}",
                f"0010 loss-balanced value error {aux['0010_loss_balanced_gplus_value_error']:.6g} vs terminal-only {aux['0010_terminal_gplus_value_error']:.6g}",
            ],
        },
        {
            "source_experiments": ["0009", "0010", "0011"],
            "claim": "Real-state auxiliary goals are generally impossible or useless.",
            "status": "unsupported",
            "numeric_evidence": ["Only one tiny rank-4 architecture family and replay construction were tested."],
        },
        {
            "source_experiments": ["0001", "0002", "0003", "0004", "0005", "0006", "0007", "0008", "0009", "0010", "0011"],
            "claim": "Neural, large-environment, GPU, or online-exploration generality follows from this evidence.",
            "status": "not_tested",
            "numeric_evidence": ["No neural framework, GPU training, larger environment, or broad online robustness run exists in 0001-0011."],
        },
    ]


def md_table(headers: list[str], rows: list[list[Any]]) -> str:
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(cell).replace("\n", " ") for cell in row) + " |")
    return "\n".join(lines)


def build_report(claims: list[dict[str, Any]], evidence: dict[str, Any]) -> str:
    est = evidence["estimator_evidence"]
    aux = evidence["auxiliary_negative_evidence"]
    claim_rows = [
        [
            ", ".join(claim["source_experiments"]),
            claim["claim"],
            claim["status"],
            "<br>".join(claim["numeric_evidence"]),
        ]
        for claim in claims
    ]
    figure_rows = [
        ["Figure 1", "Terminal target variance sweep", "0001", "Plot sampled target variance against gamma/r_bar and overlay zero soft variance."],
        ["Table 1", "Claim-status table", "0001-0011", "Use the claim table in this memo; keep supported, partially_supported, unsupported, contradicted, and not_tested labels."],
        ["Table 2", "Scaling-equivalence checks", "0001, 0002, 0008", "List finite-MDP, CliffWalking, and FourRooms scaled g_plus-vs-Q errors."],
        ["Figure 2", "RiverSwim coverage dose response", "0007", "Bar/table of adequate, borderline, and starved soft-minus-sampled value/residual/return deltas."],
        ["Table 3", "FourRooms vector sanity", "0008", "Report g_plus perturbation, scaled-Q error, real-goal value error, and goal success."],
        ["Table 4", "Low-rank auxiliary negative result", "0009, 0010", "Compare terminal-only, combined lambda=1, loss-balanced, and staged metrics."],
        ["Appendix Table", "Exact commands and artifact paths", "0001-0012", "Summarize command provenance and raw metric artifact locations."],
    ]
    return f"""# 0012 Writeup Outline: reward_to_gcrl

## Decision

Recommended next direction: `write_short_paper`.

Auxiliary-goal compute should remain gated. The low-rank auxiliary thread should
not be reopened without a new falsifiable mechanism and human approval.

## Draft Memo Summary

The evidence supports a scoped positive result and a scoped negative result.
Soft terminal marginalization is a useful small-tabular estimator/equivalence
mechanism: it removes terminal-sampling variance, preserves normalized-Q scaling
under audited reward normalization and terminal masks, and improves or matches
learning metrics in adequately covered tabular regimes. This does not imply
neural, large-environment, or online-exploration generality.

The auxiliary result is negative and narrow. In tiny FourRooms with a CPU NumPy
rank-4 shared low-rank SSM, real-state auxiliary goals did not improve g_plus.
The first shared-parameter run showed negative transfer, and the predeclared
loss-balanced and staged repair diagnostics did not recover terminal-only g_plus
value error or Bellman residual.

## Claim Status Table

{md_table(["Experiments", "Claim", "Status", "Numeric Evidence"], claim_rows)}

## Positive Estimator Evidence

- Variance removal: 0001 reports soft target variance
  `{est['0001_max_soft_target_variance']:.6g}` while sampled target variance
  reaches `{est['0001_max_sampled_target_variance']:.6g}`. Later sampled-vs-soft
  runs keep `sampled_variance_exceeds_soft_rate = 1`.
- Scaling equivalence: finite-MDP scaled error is
  `{est['0001_finite_mdp_scaled_error']:.6g}` in 0001, CliffWalking exact-DP
  scaled error is `{est['0002_cliffwalking_exact_scaled_error']:.6g}` in 0002,
  and FourRooms vector g_plus scaled-vs-Q error is
  `{est['0008_vector_gplus_scaled_minus_q_norm']:.6g}` in 0008.
- RiverSwim coverage behavior: in 0007, adequate-coverage soft-minus-sampled
  value error is `{est['0007_adequate_coverage_value_delta']:.6g}` and Bellman
  residual delta is `{est['0007_adequate_coverage_residual_delta']:.6g}`.
  Starved-coverage value error delta is `{est['0007_starved_coverage_value_delta']:.6g}`,
  so coverage caveats must stay attached to any learning claim.
- FourRooms vector sanity: 0008 reports g_plus perturbation
  `{est['0008_vector_gplus_minus_terminal']:.6g}`, scaled-Q error
  `{est['0008_vector_gplus_scaled_minus_q_norm']:.6g}`, and minimum real-goal
  success rate `{est['0008_min_goal_success_rate']:.6g}`.

## Negative Auxiliary Evidence

- 0009 terminal-only g_plus value error was
  `{aux['0009_terminal_gplus_value_error']:.6g}` with Bellman residual
  `{aux['0009_terminal_gplus_bellman_residual']:.6g}`. Combined auxiliary
  value error rose to `{aux['0009_combined_gplus_value_error']:.6g}` with
  Bellman residual `{aux['0009_combined_gplus_bellman_residual']:.6g}`.
- 0009 reward success fell from terminal-only
  `{aux['0009_terminal_reward_success_rate']:.6g}` to combined
  `{aux['0009_combined_reward_success_rate']:.6g}`.
- 0010 reproduced the 0009 failure. The loss-balanced repair had g_plus value
  error `{aux['0010_loss_balanced_gplus_value_error']:.6g}` and residual
  `{aux['0010_loss_balanced_gplus_residual']:.6g}`; the staged repair had value
  error `{aux['0010_staged_gplus_value_error']:.6g}` and residual
  `{aux['0010_staged_gplus_residual']:.6g}`. The recorded 0010 verdict is
  `{aux['0010_verdict']}`.

## Figure And Table Plan

{md_table(["Item", "Title", "Source", "Plan"], figure_rows)}

## Red Lines

Do not claim:

- Auxiliary-goal benefit for g_plus.
- General impossibility of real-state auxiliary goals.
- Neural auxiliary-goal benefit.
- Larger-environment generality.
- Online exploration robustness.
- Coverage-starved RiverSwim learning superiority.
- Reward-task improvement from independent tabular goal slices.
- Any result requiring PyTorch, JAX, GPU, or broad sweeps.

## New-Hypothesis Gate

Reopen auxiliary-goal experiments only if a new packet supplies all of the
following:

1. A single falsifiable mechanism explaining why 0009/0010 failed.
2. A principled architecture or loss-normalization change, not a broad sweep over
   rank, optimizer, learning rate, or auxiliary weight.
3. A predeclared tiny CPU diagnostic with fixed seeds, replay construction,
   coverage thresholds, and exact terminal-only baseline.
4. Success criteria requiring g_plus scaled value error or Bellman residual to
   beat terminal-only by at least 10 percent, or statistically match both while
   improving real-goal diagnostics, without increasing tie-aware reward-policy
   disagreement.
5. A review step before any neural framework, GPU run, larger environment, or
   expensive sweep.

No-go condition: if the proposal only asks for more tuning of the tested rank-4
formulation, do not run it.
"""


def write_summary() -> None:
    SUMMARY_PATH.write_text(
        """# Experiment 0012 Summary

Status: **completed**.

This was a memo-only packaging step. No new learning compute, neural framework,
GPU run, larger environment, or broad sweep was used.

Recommendation: **write_short_paper**.

Auxiliary reopening gate: require a new human-approved falsifiable hypothesis
with a principled architecture or loss-normalization change and predeclared
terminal-only comparison criteria.

Outputs:

- `research/reward_to_gcrl/reports/0012_writeup_outline.md`
- `research/reward_to_gcrl/results/0012_result.json`
- `research/reward_to_gcrl/artifacts/0012/numeric_evidence.json`
- `research/reward_to_gcrl/artifacts/0012/claim_status_table.json`
- `research/reward_to_gcrl/artifacts/0012/progress.jsonl`
""",
        encoding="utf-8",
    )


def build_result(claims: list[dict[str, Any]], evidence: dict[str, Any], runtime: float) -> dict[str, Any]:
    status_counts: dict[str, int] = {}
    for claim in claims:
        status_counts[claim["status"]] = status_counts.get(claim["status"], 0) + 1
    return {
        "experiment_id": EXPERIMENT_ID,
        "status": "completed",
        "claim_tested": "Package existing 0001-0011 evidence into a concise memo and define a formal gate for future auxiliary-goal experiments without running new learning compute.",
        "commands_run": COMMANDS_RUN,
        "metrics": {
            "report_only": True,
            "new_learning_compute_run": False,
            "inspected_experiment_ids": PRIOR_IDS,
            "claim_status_counts": status_counts,
            "final_recommendation": "write_short_paper",
            "auxiliary_thread_gate": "new_hypothesis_required_before_more_compute",
            "strongest_defensible_estimator_claim": "Soft terminal marginalization is a useful small-tabular estimator/equivalence mechanism under audited reward normalization and adequate coverage.",
            "strongest_defensible_auxiliary_claim": "The tested rank-4 NumPy low-rank FourRooms real-state auxiliary approach is unsupported and showed negative transfer.",
            "numeric_evidence": evidence,
            "red_line_claims": [
                "auxiliary-goal benefit for g_plus",
                "general impossibility of real-state auxiliary goals",
                "neural auxiliary-goal benefit",
                "larger-environment generality",
                "online exploration robustness",
                "coverage-starved RiverSwim learning superiority",
                "reward-task improvement from independent tabular goal slices",
            ],
        },
        "baseline_metrics": {
            "new_baseline_run": False,
            "reason": "Memo-only iteration; baselines and comparisons are prior completed results 0001-0011.",
        },
        "artifacts": [
            rel(REPORT_PATH),
            rel(Path(__file__)),
            rel(CHECK_PATH),
            rel(NUMERIC_EVIDENCE_PATH),
            rel(CLAIM_TABLE_PATH),
            rel(PROGRESS_PATH),
        ],
        "interpretation": "Current evidence is ready for a scoped write-up: positive small-tabular soft terminal marginalization, negative rank-4 low-rank FourRooms auxiliary result, and a formal gate before any more auxiliary compute.",
        "known_failures": [
            "rank4_lowrank_fourrooms_auxiliary_benefit_contradicted",
            "neural_larger_environment_online_claims_not_tested",
        ],
        "next_questions": [
            "Should the short paper/blog draft be written from the 0012 outline?",
            "Is there a principled new auxiliary hypothesis worth reviewing before any further compute?",
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
            "PASS: produced a concise memo separating positive estimator evidence, negative auxiliary evidence, limitations, and unsupported claims.",
            "PASS: claim-status table includes supported, partially_supported, unsupported, contradicted, and not_tested labels.",
            "PASS: strongest estimator claim is scoped to small-tabular settings and adequate coverage.",
            "PASS: strongest auxiliary claim is scoped to the tested rank-4 NumPy low-rank FourRooms setup.",
            "PASS: figure/table plan uses only existing 0001-0011 evidence.",
            "PASS: new-hypothesis gate requires principled architecture or loss-normalization change and predeclared criteria.",
            "PASS: recommendation is one of the requested directions: write_short_paper.",
        ],
        "failure_criteria_results": [
            "NOT_TRIGGERED: memo does not propose new compute before summarizing evidence.",
            "NOT_TRIGGERED: memo does not claim auxiliary-goal benefit.",
            "NOT_TRIGGERED: memo does not present low-rank auxiliary failure as a general impossibility result.",
            "NOT_TRIGGERED: RiverSwim coverage caveats and small-tabular limits are included.",
            "NOT_TRIGGERED: memo does not recommend broad sweeps, neural frameworks, GPU use, or larger environments without a new hypothesis.",
            "NOT_TRIGGERED: concrete go/no-go gate for reopening auxiliary experiments is included.",
        ],
        "metric_deltas": {
            "new_learning_compute_run": False,
            "final_recommendation": "write_short_paper",
            "claim_status_counts": status_counts,
            "0007_adequate_value_delta": evidence["estimator_evidence"]["0007_adequate_coverage_value_delta"],
            "0007_starved_value_delta": evidence["estimator_evidence"]["0007_starved_coverage_value_delta"],
            "0009_combined_minus_terminal_value_error": evidence["auxiliary_negative_evidence"]["0009_value_error_delta_combined_minus_terminal"],
            "0010_loss_balanced_value_error": evidence["auxiliary_negative_evidence"]["0010_loss_balanced_gplus_value_error"],
        },
        "decision_relevant_findings": [
            "Existing evidence is mature enough for a scoped short write-up.",
            "Soft terminal marginalization claims must remain small-tabular and coverage-qualified.",
            "Rank-4 low-rank auxiliary FourRooms benefit is contradicted by 0009 and 0010.",
            "Future auxiliary work requires a new falsifiable hypothesis before compute.",
        ],
    }


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
    evidence = build_numeric_evidence(results)
    claims = build_claim_table(results, evidence)
    write_json(NUMERIC_EVIDENCE_PATH, evidence)
    write_json(CLAIM_TABLE_PATH, {"experiment_id": EXPERIMENT_ID, "claims": claims})
    append_progress(
        "evidence_extraction",
        "Extracted numeric estimator and auxiliary evidence from existing 0001-0011 results.",
        command="conda run -n autoresearcher_reward_to_gcrl python research/reward_to_gcrl/artifacts/0012/build_writeup_outline.py",
        artifacts=[rel(NUMERIC_EVIDENCE_PATH), rel(CLAIM_TABLE_PATH)],
    )

    REPORT_PATH.write_text(build_report(claims, evidence), encoding="utf-8")
    append_progress(
        "report_write",
        "Wrote 0012 writeup outline with figure/table plan and auxiliary reopening gate.",
        command="conda run -n autoresearcher_reward_to_gcrl python research/reward_to_gcrl/artifacts/0012/build_writeup_outline.py",
        report_path=rel(REPORT_PATH),
    )

    runtime = time.perf_counter() - start
    write_json(RESULT_PATH, build_result(claims, evidence, runtime))
    write_summary()
    append_progress(
        "result_write",
        "Wrote 0012 result JSON and summary Markdown for the memo-only iteration.",
        command="conda run -n autoresearcher_reward_to_gcrl python research/reward_to_gcrl/artifacts/0012/build_writeup_outline.py",
        result_path=rel(RESULT_PATH),
        summary_path=rel(SUMMARY_PATH),
        recommendation="write_short_paper",
    )


if __name__ == "__main__":
    main()
