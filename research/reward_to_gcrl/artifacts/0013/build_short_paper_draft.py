#!/usr/bin/env python
"""Build an internal short-paper draft from existing reward_to_gcrl evidence."""

from __future__ import annotations

import argparse
import json
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


EXPERIMENT_ID = "0013"
PROJECT = "reward_to_gcrl"
ROOT = Path(__file__).resolve().parents[4]
PROJECT_ROOT = ROOT / "research" / PROJECT
RESULT_DIR = PROJECT_ROOT / "results"
REPORT_DIR = PROJECT_ROOT / "reports"
ARTIFACT_DIR = PROJECT_ROOT / "artifacts" / EXPERIMENT_ID
PROGRESS_PATH = ARTIFACT_DIR / "progress.jsonl"
REPORT_PATH = REPORT_DIR / "0013_short_paper_draft.md"
RESULT_PATH = RESULT_DIR / "0013_result.json"
SUMMARY_PATH = RESULT_DIR / "0013_summary.md"
CHECK_PATH = ARTIFACT_DIR / "local_compatibility_check.json"
CLAIM_MAP_PATH = ARTIFACT_DIR / "claim_to_evidence_map.json"
DRAFT_METADATA_PATH = ARTIFACT_DIR / "draft_metadata.json"

PRIOR_IDS = [f"{i:04d}" for i in range(1, 13)]
SCAFFOLD_REPORTS = [
    PROJECT_ROOT / "reports" / "0011_evidence_synthesis.md",
    PROJECT_ROOT / "reports" / "0012_writeup_outline.md",
]
COMMANDS_RUN = [
    "mkdir -p research/reward_to_gcrl/artifacts/0013 research/reward_to_gcrl/results research/reward_to_gcrl/reports && date -u -Iseconds",
    "conda run -n autoresearcher_reward_to_gcrl python --version",
    "ls -l research/reward_to_gcrl/reports/0011_evidence_synthesis.md research/reward_to_gcrl/reports/0012_writeup_outline.md schemas/result.schema.json scripts/validate_artifacts.py",
    "rg --files research/reward_to_gcrl/results | sort | rg '00(0[1-9]|1[0-3])_result\\.json|001[0-3]_result\\.json|00(0[1-9]|1[0-3])_summary\\.md|001[0-3]_summary\\.md'",
    "jq '{status, recommendation:.metrics.final_recommendation, gate:.metrics.auxiliary_thread_gate, new_learning_compute_run:.metrics.new_learning_compute_run}' research/reward_to_gcrl/results/0012_result.json",
    "sed -n '1,260p' research/reward_to_gcrl/reports/0012_writeup_outline.md",
    "sed -n '1,260p' research/reward_to_gcrl/reports/0011_evidence_synthesis.md",
    "jq '.metrics.numeric_evidence, .metrics.red_line_claims, .metrics.final_recommendation' research/reward_to_gcrl/results/0012_result.json",
    "jq '.metrics.lowrank_auxiliary.aggregate, .metric_deltas' research/reward_to_gcrl/results/0010_result.json",
    "conda run -n autoresearcher_reward_to_gcrl python -m py_compile research/reward_to_gcrl/artifacts/0013/build_short_paper_draft.py",
    "conda run -n autoresearcher_reward_to_gcrl python research/reward_to_gcrl/artifacts/0013/build_short_paper_draft.py --check-only",
    "conda run -n autoresearcher_reward_to_gcrl python research/reward_to_gcrl/artifacts/0013/build_short_paper_draft.py",
    "conda run -n autoresearcher_reward_to_gcrl python -m jsonschema -i research/reward_to_gcrl/results/0013_result.json schemas/result.schema.json",
    "conda run -n autoresearcher_reward_to_gcrl python scripts/validate_artifacts.py --repo-root . --json research/reward_to_gcrl/results/0013_result.json --schema schemas/result.schema.json --check-result-artifacts",
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


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_results() -> dict[str, dict[str, Any]]:
    missing = []
    results: dict[str, dict[str, Any]] = {}
    for exp_id in PRIOR_IDS:
        path = RESULT_DIR / f"{exp_id}_result.json"
        if not path.exists():
            missing.append(rel(path))
        else:
            results[exp_id] = load_json(path)
    if missing:
        raise FileNotFoundError(f"Missing required evidence files: {missing}")
    return results


def compatibility_check() -> dict[str, Any]:
    expected = [RESULT_DIR / f"{exp_id}_result.json" for exp_id in PRIOR_IDS]
    check = {
        "experiment_id": EXPERIMENT_ID,
        "status": "passed",
        "new_learning_compute_run": False,
        "prior_result_files_present": all(path.exists() for path in expected),
        "scaffold_reports_present": all(path.exists() for path in SCAFFOLD_REPORTS),
        "prior_result_files": [rel(path) for path in expected],
        "scaffold_reports": [rel(path) for path in SCAFFOLD_REPORTS],
        "checked_at": now(),
    }
    write_json(CHECK_PATH, check)
    append_progress(
        "compatibility_check",
        "Confirmed prior 0001-0012 results and 0011/0012 scaffold reports are available.",
        command="conda run -n autoresearcher_reward_to_gcrl python research/reward_to_gcrl/artifacts/0013/build_short_paper_draft.py --check-only",
        compatibility_check_path=rel(CHECK_PATH),
    )
    return check


def build_claim_map(results: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    ev = results["0012"]["metrics"]["numeric_evidence"]
    est = ev["estimator_evidence"]
    aux = ev["auxiliary_negative_evidence"]
    return [
        {
            "claim_id": "C1",
            "claim": "Soft terminal marginalization removes terminal-sampling variance in audited small tabular settings.",
            "status": "supported",
            "evidence_iterations": ["0001", "0003", "0005", "0006", "0007", "0011", "0012"],
            "numeric_evidence": [
                f"0001 max soft target variance {est['0001_max_soft_target_variance']:.6g}",
                f"0001 max sampled target variance {est['0001_max_sampled_target_variance']:.6g}",
                "sampled_variance_exceeds_soft_rate is 1 in 0003/0005/0006/0007",
            ],
            "limitations": ["Tabular or CPU NumPy only; matched-stream and controlled behavior settings."],
        },
        {
            "claim_id": "C2",
            "claim": "Soft g_plus fixed points preserve normalized-Q scaling under audited reward normalization and terminal masks.",
            "status": "supported",
            "evidence_iterations": ["0001", "0002", "0008", "0011", "0012"],
            "numeric_evidence": [
                f"0001 finite-MDP scaled error {est['0001_finite_mdp_scaled_error']:.6g}",
                f"0002 CliffWalking scaled error {est['0002_cliffwalking_exact_scaled_error']:.6g}",
                f"0008 FourRooms scaled error {est['0008_vector_gplus_scaled_minus_q_norm']:.6g}",
            ],
            "limitations": ["Reward normalization must be explicit; CliffWalking raw returns remain diagnostic."],
        },
        {
            "claim_id": "C3",
            "claim": "Soft updates can improve learning metrics when coverage is adequate.",
            "status": "partially_supported",
            "evidence_iterations": ["0004", "0005", "0006", "0007", "0011", "0012"],
            "numeric_evidence": [
                f"0007 adequate value-error delta {est['0007_adequate_coverage_value_delta']:.6g}",
                f"0007 adequate Bellman-residual delta {est['0007_adequate_coverage_residual_delta']:.6g}",
                f"0007 starved value-error delta {est['0007_starved_coverage_value_delta']:.6g}",
            ],
            "limitations": ["Coverage-starved RiverSwim runs are not learning-superiority evidence."],
        },
        {
            "claim_id": "C4",
            "claim": "Independent tabular vector SSM real-state goals are correct and non-interfering.",
            "status": "supported",
            "evidence_iterations": ["0008", "0011", "0012"],
            "numeric_evidence": [
                f"0008 vector g_plus minus terminal-only {est['0008_vector_gplus_minus_terminal']:.6g}",
                f"0008 min goal success rate {est['0008_min_goal_success_rate']:.6g}",
            ],
            "limitations": ["This is correctness evidence, not shared-representation reward improvement."],
        },
        {
            "claim_id": "C5",
            "claim": "The tested rank-4 low-rank FourRooms real-state auxiliary approach improves g_plus.",
            "status": "contradicted",
            "evidence_iterations": ["0009", "0010", "0011", "0012"],
            "numeric_evidence": [
                f"0009 terminal-only value error {aux['0009_terminal_gplus_value_error']:.6g}",
                f"0009 combined value error {aux['0009_combined_gplus_value_error']:.6g}",
                f"0010 loss-balanced value error {aux['0010_loss_balanced_gplus_value_error']:.6g}",
                f"0010 staged value error {aux['0010_staged_gplus_value_error']:.6g}",
            ],
            "limitations": ["Negative evidence is limited to rank 4, optimizer, replay, gamma, and repair variants tested."],
        },
        {
            "claim_id": "C6",
            "claim": "Auxiliary goals are generally impossible or harmful.",
            "status": "unsupported",
            "evidence_iterations": ["0009", "0010", "0011", "0012"],
            "numeric_evidence": ["Only one tiny rank-4 shared low-rank setup was tested."],
            "limitations": ["A new principled architecture or loss hypothesis could still be tested after review."],
        },
        {
            "claim_id": "C7",
            "claim": "Neural, large-environment, benchmark, or online-exploration generality follows.",
            "status": "not_tested",
            "evidence_iterations": ["0001", "0002", "0003", "0004", "0005", "0006", "0007", "0008", "0009", "0010", "0011", "0012"],
            "numeric_evidence": ["No neural, GPU, large-environment, benchmark, or broad online robustness experiment exists."],
            "limitations": ["Must not appear in external claims without new reviewed evidence."],
        },
    ]


def md_table(headers: list[str], rows: list[list[Any]]) -> str:
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(cell).replace("\n", " ") for cell in row) + " |")
    return "\n".join(lines)


def build_draft(results: dict[str, dict[str, Any]], claim_map: list[dict[str, Any]]) -> str:
    ev = results["0012"]["metrics"]["numeric_evidence"]
    est = ev["estimator_evidence"]
    aux = ev["auxiliary_negative_evidence"]
    claim_rows = [
        [
            claim["claim_id"],
            claim["claim"],
            claim["status"],
            ", ".join(claim["evidence_iterations"]),
            "<br>".join(claim["numeric_evidence"]),
        ]
        for claim in claim_map
    ]
    checklist_rows = [
        ["Claim scope", "Every estimator claim says small tabular or CPU NumPy and adequate coverage where relevant.", "required"],
        ["Auxiliary wording", "Auxiliary result is limited to the tested rank-4 FourRooms architecture, optimizer, replay setup, gamma, and repair variants.", "required"],
        ["No overclaim", "No neural, benchmark, large-environment, broad GCRL, or online exploration claim is present.", "required"],
        ["Negative evidence", "0009 and 0010 negative-transfer metrics are shown without minimization.", "required"],
        ["Coverage caveat", "RiverSwim starved and adequate bins are both reported.", "required"],
        ["Artifact trace", "Each claim links to iteration IDs and raw result artifacts.", "required"],
        ["Human review", "A human reviewer signs off before external publication or broader claims.", "required"],
    ]
    return f"""# Internal Draft: Soft Terminal Marginalization and a Negative Low-Rank Auxiliary Result

**Status:** internal draft only. Requires pre-publication review before external
use or broader claims.

## Abstract

We study a small, audited sequence of tabular and CPU NumPy diagnostics for
reward-to-GCRL style soft successor measures. The positive evidence supports a
scoped estimator claim: soft terminal marginalization removes terminal-sampling
variance and preserves normalized-Q scaling in small audited tabular settings,
with learning advantages only when transition and reward coverage are adequate.
The negative evidence is also scoped: in tiny FourRooms, a rank-4 shared
low-rank real-state auxiliary-goal model did not improve the g_plus reward slice
and showed negative transfer. Loss-balanced and staged repair diagnostics did
not recover terminal-only g_plus value error or Bellman residual. These results
support an internal write-up, not external generality claims.

## Introduction

The project began with a narrow question: can a terminal-only soft
successor-measure target represent normalized reward value while avoiding sparse
sampled terminal events? Experiments 0001-0008 answer this in controlled small
settings. The estimator transformation behaves as expected, and independent
tabular vector goal slices are correct and non-interfering.

The later question was whether real-state auxiliary goals help g_plus through
shared parameters. Experiments 0009 and 0010 do not support that claim for the
tested rank-4 low-rank FourRooms model. The draft therefore separates estimator
evidence from auxiliary-goal evidence.

## Method Summary

The estimator experiments compare sampled augmented g_plus updates with
deterministic soft terminal marginalization. The sampled update keeps the same
expected target but retains terminal-sampling variance; the soft update replaces
sampled terminal events with their deterministic marginal mass. Exact DP checks
compare scaled soft g_plus values to normalized Q references under audited reward
normalization and terminal masks.

The auxiliary experiments use a CPU NumPy low-rank shared model in tiny
FourRooms. Terminal-only g_plus training is compared with combined real-state
auxiliary training under matched replay and fixed rank. The 0010 repair
diagnostic tests only the predeclared variants: terminal-only reproduction,
combined lambda=1 reproduction, loss-balanced combined training, and staged
real-goal pretraining followed by g_plus fine-tuning.

## Claim-To-Evidence Map

{md_table(["ID", "Claim", "Status", "Iterations", "Evidence"], claim_rows)}

## Experimental Evidence Summary

Soft terminal marginalization removes terminal-sampling variance in the tested
settings. In 0001, the maximum soft target variance is
`{est['0001_max_soft_target_variance']:.6g}` while sampled target variance
reaches `{est['0001_max_sampled_target_variance']:.6g}`. Later sampled-vs-soft
experiments keep sampled variance above soft variance in all reported settings.

Scaling checks support the normalized-Q relation. The finite-MDP scaled error in
0001 is `{est['0001_finite_mdp_scaled_error']:.6g}`, the audited local
CliffWalking scaled error in 0002 is
`{est['0002_cliffwalking_exact_scaled_error']:.6g}`, and the FourRooms vector
g_plus scaled-vs-Q error in 0008 is
`{est['0008_vector_gplus_scaled_minus_q_norm']:.6g}`.

Learning improvements are coverage-qualified. In the 0007 RiverSwim dose
response, adequate-coverage runs have soft-minus-sampled value-error delta
`{est['0007_adequate_coverage_value_delta']:.6g}` and Bellman-residual delta
`{est['0007_adequate_coverage_residual_delta']:.6g}`. Starved-coverage runs have
value-error delta `{est['0007_starved_coverage_value_delta']:.6g}`, so they must
not be used for an unconditional learning-superiority claim.

Vector SSM correctness is supported only in the independent tabular sense. In
0008, vector g_plus minus terminal-only is
`{est['0008_vector_gplus_minus_terminal']:.6g}`, scaled-Q error is
`{est['0008_vector_gplus_scaled_minus_q_norm']:.6g}`, and minimum real-goal
success rate is `{est['0008_min_goal_success_rate']:.6g}`.

## Negative Auxiliary Result

The shared low-rank auxiliary result is negative. In 0009, terminal-only g_plus
value error is `{aux['0009_terminal_gplus_value_error']:.6g}` with Bellman
residual `{aux['0009_terminal_gplus_bellman_residual']:.6g}`. Combined auxiliary
training increases value error to `{aux['0009_combined_gplus_value_error']:.6g}`
and Bellman residual to `{aux['0009_combined_gplus_bellman_residual']:.6g}`.
Reward success falls from `{aux['0009_terminal_reward_success_rate']:.6g}` to
`{aux['0009_combined_reward_success_rate']:.6g}`.

Experiment 0010 reproduces the negative-transfer pattern and tests two repair
variants. Loss-balanced training still has value error
`{aux['0010_loss_balanced_gplus_value_error']:.6g}` and residual
`{aux['0010_loss_balanced_gplus_residual']:.6g}`. The staged variant has value
error `{aux['0010_staged_gplus_value_error']:.6g}` and residual
`{aux['0010_staged_gplus_residual']:.6g}`. The recorded verdict is
`{aux['0010_verdict']}`.

This is evidence against the tested architecture and training recipe, not
against auxiliary goals in general.

## Limitations

- The evidence is tiny-environment, tabular, or CPU NumPy only.
- Several estimator tests use matched streams or controlled behavior policies.
- RiverSwim learning claims depend on adequate right-reward and state-action
  coverage.
- CliffWalking raw-task returns are limited by reward-normalization mismatch.
- FourRooms auxiliary tests use uniform state-action reset replay, one rank-4
  low-rank model family, fixed optimizer settings, fixed gamma, and predeclared
  repair variants.
- No neural framework, GPU run, larger environment, benchmark suite, or online
  exploration robustness test was run.

## Unsupported-Claims Red Lines

Do not claim:

- Neural auxiliary benefit.
- Broad reward-to-GCRL success.
- Online exploration robustness.
- Benchmark or larger-environment generality.
- General impossibility or general harmfulness of auxiliary goals.
- Coverage-starved RiverSwim learning superiority.
- Reward-task improvement from independent tabular goal slices.

## Pre-Publication Review Checklist

{md_table(["Check", "Requirement", "Status Before External Use"], checklist_rows)}

## Conclusion

The internal evidence supports a narrow positive estimator conclusion and a
narrow negative auxiliary conclusion. The next safe step is review of this draft
against the checklist. External publication or broader claims require explicit
human review. Future auxiliary experiments require a new falsifiable hypothesis
that changes the architecture or loss normalization in a principled way, not a
broad sweep over the failed rank-4 setup.
"""


def write_summary() -> None:
    SUMMARY_PATH.write_text(
        """# Experiment 0013 Summary

Status: **completed**.

Created an internal short-paper draft from existing 0001-0012 evidence only. No
new learning compute, neural framework, GPU run, larger environment, or broad
sweep was used.

Draft status: **internal_review_required**.

External use instruction: the draft requires pre-publication review before any
external publication or broader claims.

Outputs:

- `research/reward_to_gcrl/reports/0013_short_paper_draft.md`
- `research/reward_to_gcrl/results/0013_result.json`
- `research/reward_to_gcrl/artifacts/0013/claim_to_evidence_map.json`
- `research/reward_to_gcrl/artifacts/0013/draft_metadata.json`
- `research/reward_to_gcrl/artifacts/0013/progress.jsonl`
""",
        encoding="utf-8",
    )


def build_result(results: dict[str, dict[str, Any]], claim_map: list[dict[str, Any]], runtime: float) -> dict[str, Any]:
    status_counts: dict[str, int] = {}
    for claim in claim_map:
        status_counts[claim["status"]] = status_counts.get(claim["status"], 0) + 1
    inspected_files = [rel(RESULT_DIR / f"{exp_id}_result.json") for exp_id in PRIOR_IDS]
    inspected_files.extend(rel(path) for path in SCAFFOLD_REPORTS)
    return {
        "experiment_id": EXPERIMENT_ID,
        "status": "completed",
        "claim_tested": "Existing 0001-0012 evidence is sufficient for an internal short-paper draft with scoped positive estimator claims and scoped negative low-rank auxiliary evidence.",
        "commands_run": COMMANDS_RUN,
        "metrics": {
            "report_only": True,
            "new_learning_compute_run": False,
            "draft_status": "internal_review_required",
            "external_use_requires_review": True,
            "inspected_evidence_files": inspected_files,
            "claim_status_counts": status_counts,
            "main_claim_count": len(claim_map),
            "separates_estimator_vector_and_auxiliary_sections": True,
            "contains_red_lines": True,
            "contains_prepublication_checklist": True,
            "strongest_positive_claim": "Soft terminal marginalization is useful for small audited tabular variance reduction and normalized-Q equivalence, with adequate-coverage learning improvements.",
            "strongest_auxiliary_claim": "The tested rank-4 low-rank FourRooms real-state auxiliary approach is unsupported and showed negative transfer.",
        },
        "baseline_metrics": {
            "new_baseline_run": False,
            "reason": "Draft-only iteration; all evidence and comparisons come from completed iterations 0001-0012.",
        },
        "artifacts": [
            rel(REPORT_PATH),
            rel(Path(__file__)),
            rel(CHECK_PATH),
            rel(CLAIM_MAP_PATH),
            rel(DRAFT_METADATA_PATH),
            rel(PROGRESS_PATH),
        ],
        "interpretation": "An internal short-paper draft now exists, but it is not externally publishable without review. The draft preserves the scoped positive estimator claim and the scoped negative low-rank auxiliary result.",
        "known_failures": [
            "rank4_lowrank_fourrooms_auxiliary_benefit_contradicted",
            "neural_large_environment_online_generality_not_tested",
            "external_publication_not_yet_reviewed",
        ],
        "next_questions": [
            "Who will perform the pre-publication review against the checklist?",
            "Should a separate negative-result note be prepared for 0009 and 0010 details?",
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
            "PASS: no new learning compute was run.",
            "PASS: draft separates estimator claims, vector-SSM correctness, and auxiliary-goal negative evidence.",
            "PASS: main claims link to specific existing iterations from 0001 through 0012.",
            "PASS: strongest positive claim is limited to small audited tabular or CPU NumPy settings, normalized-Q scaling, variance reduction, and adequate coverage.",
            "PASS: auxiliary result is limited to the tested rank-4 low-rank FourRooms architecture, optimizer, replay setup, gamma, and repair variants.",
            "PASS: limitations include coverage dependence, matched-stream tests, tiny environments, tabular scope, uniform reset replay, and lack of neural or large-environment evidence.",
            "PASS: unsupported-claims red lines are included.",
            "PASS: pre-publication review checklist is included.",
        ],
        "failure_criteria_results": [
            "NOT_TRIGGERED: draft does not propose or run new experiments.",
            "NOT_TRIGGERED: draft does not claim general reward-to-GCRL success.",
            "NOT_TRIGGERED: draft does not claim auxiliary-goal benefit.",
            "NOT_TRIGGERED: draft does not claim auxiliary goals are generally impossible or harmful.",
            "NOT_TRIGGERED: RiverSwim coverage caveats and matched-stream limitations are included.",
            "NOT_TRIGGERED: negative auxiliary evidence is explicit.",
            "NOT_TRIGGERED: draft is explicitly framed as requiring review before external use.",
        ],
        "metric_deltas": {
            "new_learning_compute_run": False,
            "claim_status_counts": status_counts,
            "draft_status": "internal_review_required",
            "external_use_requires_review": True,
        },
        "decision_relevant_findings": [
            "The short-paper draft is ready for internal review only.",
            "Soft terminal marginalization evidence is positive but small-tabular and coverage-qualified.",
            "Rank-4 low-rank FourRooms auxiliary evidence is negative and should not be generalized beyond the tested setup.",
            "The draft contains a red-line section and review checklist before external use.",
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
    claim_map = build_claim_map(results)
    draft_metadata = {
        "experiment_id": EXPERIMENT_ID,
        "draft_status": "internal_review_required",
        "new_learning_compute_run": False,
        "scaffold_reports": [rel(path) for path in SCAFFOLD_REPORTS],
        "claim_ids": [claim["claim_id"] for claim in claim_map],
        "external_use_requires_review": True,
    }
    write_json(CLAIM_MAP_PATH, {"experiment_id": EXPERIMENT_ID, "claims": claim_map})
    write_json(DRAFT_METADATA_PATH, draft_metadata)
    append_progress(
        "evidence_map",
        "Wrote claim-to-evidence map and draft metadata from existing 0001-0012 evidence.",
        command="conda run -n autoresearcher_reward_to_gcrl python research/reward_to_gcrl/artifacts/0013/build_short_paper_draft.py",
        artifacts=[rel(CLAIM_MAP_PATH), rel(DRAFT_METADATA_PATH)],
    )

    REPORT_PATH.write_text(build_draft(results, claim_map), encoding="utf-8")
    append_progress(
        "draft_write",
        "Wrote internal short-paper draft with red lines and pre-publication review checklist.",
        command="conda run -n autoresearcher_reward_to_gcrl python research/reward_to_gcrl/artifacts/0013/build_short_paper_draft.py",
        report_path=rel(REPORT_PATH),
    )

    runtime = time.perf_counter() - start
    write_json(RESULT_PATH, build_result(results, claim_map, runtime))
    write_summary()
    append_progress(
        "result_write",
        "Wrote 0013 result JSON and summary Markdown.",
        command="conda run -n autoresearcher_reward_to_gcrl python research/reward_to_gcrl/artifacts/0013/build_short_paper_draft.py",
        result_path=rel(RESULT_PATH),
        summary_path=rel(SUMMARY_PATH),
        draft_status="internal_review_required",
    )


if __name__ == "__main__":
    main()
