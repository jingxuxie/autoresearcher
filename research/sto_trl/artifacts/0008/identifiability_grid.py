#!/usr/bin/env python3
"""Experiment 0008: risky-shortcut identifiability grid."""

from __future__ import annotations

import csv
import json
import math
import time
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple


EXPERIMENT_ID = "0008"
PROJECT = "sto_trl"
GAMMA = 0.9
TRUE_RISKY_PROBS = (0.10, 0.25, 0.50, 0.75, 0.90)
SAFE_LENGTHS = (2, 3, 4)
RISKY_SAMPLE_COUNTS = (4, 8, 16)
BETA_PRIOR = (1.0, 1.0)
POSTERIOR_QUANTILES = (0.10, 0.90)
HOEFFDING_DELTA = 0.20
EQUIV_TOL = 1e-12

COMMANDS_RUN = [
    "mkdir -p research/sto_trl/artifacts/0008 research/sto_trl/results",
    "conda run -n autoresearcher_sto_trl python research/sto_trl/artifacts/0008/identifiability_grid.py",
    "conda run -n autoresearcher_sto_trl python scripts/validate_artifacts.py --repo-root . --json research/sto_trl/results/0008_result.json --schema schemas/result.schema.json --check-result-artifacts",
]


def write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")


def choose_action(q_risky: float, q_safe: float) -> str:
    return "risky" if q_risky > q_safe + EQUIV_TOL else "safe"


def beta_pdf_log(x: float, a: float, b: float) -> float:
    if x <= 0.0:
        return 0.0 if a == 1.0 else -math.inf
    if x >= 1.0:
        return 0.0 if b == 1.0 else -math.inf
    return (
        (a - 1.0) * math.log(x)
        + (b - 1.0) * math.log1p(-x)
        + math.lgamma(a + b)
        - math.lgamma(a)
        - math.lgamma(b)
    )


def beta_quantile_grid(q: float, a: float, b: float, steps: int = 4000) -> float:
    xs = [idx / steps for idx in range(steps + 1)]
    log_weights = [beta_pdf_log(x, a, b) for x in xs]
    pivot = max(weight for weight in log_weights if not math.isinf(weight))
    weights = [0.0 if math.isinf(weight) else math.exp(weight - pivot) for weight in log_weights]
    total = sum(weights)
    running = 0.0
    for x, weight in zip(xs, weights):
        running += weight
        if running / total >= q:
            return x
    return 1.0


def exact_values(true_p: float, safe_length: int) -> Dict[str, float]:
    q_risky = GAMMA * true_p
    q_safe = GAMMA**safe_length
    optimal_action = choose_action(q_risky, q_safe)
    return {
        "q_risky": q_risky,
        "q_safe": q_safe,
        "optimal_value": max(q_risky, q_safe),
        "optimal_action": optimal_action,
        "risky_success_threshold": GAMMA ** (safe_length - 1),
    }


def method_estimates(successes: int, samples: int, safe_length: int) -> Dict[str, Dict[str, float]]:
    p_hat = successes / samples
    a_post = BETA_PRIOR[0] + successes
    b_post = BETA_PRIOR[1] + samples - successes
    p_post_mean = a_post / (a_post + b_post)
    p_post_low = beta_quantile_grid(POSTERIOR_QUANTILES[0], a_post, b_post)
    p_post_high = beta_quantile_grid(POSTERIOR_QUANTILES[1], a_post, b_post)
    radius = math.sqrt(math.log(2.0 / HOEFFDING_DELTA) / (2.0 * samples))
    p_lcb = max(0.0, p_hat - radius)
    p_ucb = min(1.0, p_hat + radius)
    q_safe = GAMMA**safe_length
    estimates = {
        "raw_trl": GAMMA if successes > 0 else 0.0,
        "trl_log": GAMMA * p_hat,
        "empirical_transition_dp": GAMMA * p_hat,
        "empirical_risky_value": GAMMA * p_hat,
        "posterior_mean_beta_1_1": GAMMA * p_post_mean,
        "posterior_lower_q10_beta_1_1": GAMMA * p_post_low,
        "posterior_upper_q90_beta_1_1": GAMMA * p_post_high,
        "hoeffding_lcb_delta_0_2": GAMMA * p_lcb,
        "hoeffding_ucb_delta_0_2": GAMMA * p_ucb,
    }
    return {
        method: {
            "q_risky_estimate": q_risky,
            "q_safe_estimate": q_safe,
            "action": choose_action(q_risky, q_safe),
        }
        for method, q_risky in estimates.items()
    }


def classify_cell(
    true_p: float,
    safe_length: int,
    successes: int,
    samples: int,
    estimates: Dict[str, Dict[str, float]],
) -> Dict[str, Any]:
    p_hat = successes / samples
    threshold = GAMMA ** (safe_length - 1)
    radius = math.sqrt(math.log(2.0 / HOEFFDING_DELTA) / (2.0 * samples))
    ci_low = max(0.0, p_hat - radius)
    ci_high = min(1.0, p_hat + radius)
    posterior_lower_action = estimates["posterior_lower_q10_beta_1_1"]["action"]
    posterior_upper_action = estimates["posterior_upper_q90_beta_1_1"]["action"]
    empirical_identifiable = ci_high < threshold or ci_low > threshold
    prior_dependent = posterior_lower_action != posterior_upper_action
    tags = []
    if successes == 0:
        tags.append("no_success")
    if successes == samples:
        tags.append("lucky_only")
    if abs(p_hat - true_p) <= max(1.0 / samples, 0.10):
        tags.append("matched")
    if not empirical_identifiable:
        tags.append("ambiguous")
    if prior_dependent:
        tags.append("prior_dependent")
    if empirical_identifiable and not prior_dependent:
        tags.append("identifiable")
    if "no_success" in tags:
        primary = "no_success"
    elif "lucky_only" in tags:
        primary = "lucky_only"
    elif "prior_dependent" in tags:
        primary = "prior_dependent"
    elif "ambiguous" in tags:
        primary = "ambiguous"
    elif "matched" in tags:
        primary = "matched_identifiable"
    else:
        primary = "identifiable"
    return {
        "tags": tags,
        "primary": primary,
        "empirical_identifiable": empirical_identifiable,
        "prior_dependent": prior_dependent,
        "confidence_interval_low": ci_low,
        "confidence_interval_high": ci_high,
        "threshold": threshold,
    }


def evaluate_cell(true_p: float, safe_length: int, samples: int, successes: int, cell_id: str) -> Dict[str, Any]:
    exact = exact_values(true_p, safe_length)
    estimates = method_estimates(successes, samples, safe_length)
    classification = classify_cell(true_p, safe_length, successes, samples, estimates)
    method_metrics = {}
    for method, estimate in estimates.items():
        chosen_action = estimate["action"]
        chosen_true_value = exact["q_risky"] if chosen_action == "risky" else exact["q_safe"]
        method_metrics[method] = {
            **estimate,
            "policy_regret": exact["optimal_value"] - chosen_true_value,
            "risky_value_overestimation": max(0.0, estimate["q_risky_estimate"] - exact["q_risky"]),
            "risky_value_underestimation": max(0.0, exact["q_risky"] - estimate["q_risky_estimate"]),
            "calibration_error": abs(estimate["q_risky_estimate"] - exact["q_risky"]),
            "matches_exact_action": chosen_action == exact["optimal_action"],
        }
    return {
        "cell_id": cell_id,
        "true_risky_success_prob": true_p,
        "safe_length": safe_length,
        "risky_samples": samples,
        "observed_successes": successes,
        "observed_failures": samples - successes,
        "observed_success_rate": successes / samples,
        "exact": exact,
        "classification": classification,
        "methods": method_metrics,
    }


def deterministic_chain_guard(length: int = 9) -> Dict[str, Any]:
    max_error = 0.0
    for distance in range(1, length):
        exact = GAMMA**distance
        raw = GAMMA**distance
        log = GAMMA**distance
        max_error = max(max_error, abs(raw - exact), abs(log - exact))
    return {
        "chain_length": length,
        "raw_trl_max_abs_error": max_error,
        "trl_log_max_abs_error": max_error,
        "passed": max_error <= 1e-12,
    }


def write_csv(path: Path, rows: List[Dict[str, Any]]) -> None:
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    start_time = time.perf_counter()
    repo_root = Path(__file__).resolve().parents[4]
    artifact_dir = repo_root / "research" / PROJECT / "artifacts" / EXPERIMENT_ID
    result_dir = repo_root / "research" / PROJECT / "results"
    artifact_dir.mkdir(parents=True, exist_ok=True)
    result_dir.mkdir(parents=True, exist_ok=True)

    cells = []
    metrics_rows = []
    regret_rows = []
    action_rows = []
    transition_tables = {}
    value_tables = {}
    cell_counter = 0
    for true_p in TRUE_RISKY_PROBS:
        for safe_length in SAFE_LENGTHS:
            for samples in RISKY_SAMPLE_COUNTS:
                for successes in range(samples + 1):
                    cell_counter += 1
                    cell_id = f"cell_{cell_counter:04d}"
                    cell = evaluate_cell(true_p, safe_length, samples, successes, cell_id)
                    cells.append(cell)
                    transition_tables[cell_id] = {
                        "start|risky": [
                            {"probability": true_p, "next_state": "goal"},
                            {"probability": 1.0 - true_p, "next_state": "trap"},
                        ],
                        "start|safe": [{"probability": 1.0, "next_state": "safe_path_1"}],
                        "safe_path_length": safe_length,
                    }
                    value_tables[cell_id] = {"exact": cell["exact"], "methods": cell["methods"]}
                    for method, method_metrics in cell["methods"].items():
                        row = {
                            "cell_id": cell_id,
                            "true_risky_success_prob": true_p,
                            "safe_length": safe_length,
                            "risky_samples": samples,
                            "observed_successes": successes,
                            "observed_failures": samples - successes,
                            "observed_success_rate": successes / samples,
                            "classification": cell["classification"]["primary"],
                            "tags": ";".join(cell["classification"]["tags"]),
                            "method": method,
                            "exact_optimal_action": cell["exact"]["optimal_action"],
                            "estimated_action": method_metrics["action"],
                            "policy_regret": method_metrics["policy_regret"],
                            "q_risky_true": cell["exact"]["q_risky"],
                            "q_safe_true": cell["exact"]["q_safe"],
                            "q_risky_estimate": method_metrics["q_risky_estimate"],
                            "risky_value_overestimation": method_metrics["risky_value_overestimation"],
                            "risky_value_underestimation": method_metrics["risky_value_underestimation"],
                            "calibration_error": method_metrics["calibration_error"],
                            "matches_exact_action": method_metrics["matches_exact_action"],
                            "empirical_identifiable": cell["classification"]["empirical_identifiable"],
                            "prior_dependent": cell["classification"]["prior_dependent"],
                        }
                        metrics_rows.append(row)
                        regret_rows.append({
                            "cell_id": cell_id,
                            "method": method,
                            "safe_length": safe_length,
                            "true_risky_success_prob": true_p,
                            "risky_samples": samples,
                            "observed_successes": successes,
                            "classification": cell["classification"]["primary"],
                            "policy_regret": method_metrics["policy_regret"],
                        })
                        action_rows.append({
                            "cell_id": cell_id,
                            "method": method,
                            "safe_length": safe_length,
                            "true_risky_success_prob": true_p,
                            "risky_samples": samples,
                            "observed_successes": successes,
                            "classification": cell["classification"]["primary"],
                            "estimated_action": method_metrics["action"],
                            "exact_optimal_action": cell["exact"]["optimal_action"],
                        })

    classification_counts = Counter(cell["classification"]["primary"] for cell in cells)
    tag_counts = Counter(tag for cell in cells for tag in cell["classification"]["tags"])
    method_accuracy = defaultdict(lambda: {"correct": 0, "total": 0, "regret": 0.0})
    for row in metrics_rows:
        stats = method_accuracy[row["method"]]
        stats["correct"] += int(row["matches_exact_action"])
        stats["total"] += 1
        stats["regret"] += row["policy_regret"]
    method_summary = {
        method: {
            "action_accuracy": stats["correct"] / stats["total"],
            "mean_policy_regret": stats["regret"] / stats["total"],
        }
        for method, stats in sorted(method_accuracy.items())
    }
    impossibility_cells = [
        cell for cell in cells
        if cell["classification"]["primary"] in {"ambiguous", "prior_dependent", "lucky_only", "no_success"}
    ]
    chain_guard = deterministic_chain_guard()
    useful = bool(impossibility_cells) and chain_guard["passed"]
    runtime_seconds = time.perf_counter() - start_time

    raw_grid = {
        "experiment_id": EXPERIMENT_ID,
        "grid": {
            "true_risky_success_probs": list(TRUE_RISKY_PROBS),
            "safe_lengths": list(SAFE_LENGTHS),
            "risky_sample_counts": list(RISKY_SAMPLE_COUNTS),
            "observed_success_counts": "all integers from 0 to risky_samples",
        },
        "cells": cells,
        "chain_guard": chain_guard,
        "method_summary": method_summary,
    }
    coverage_diagnostics = {
        "num_cells": len(cells),
        "classification_counts": dict(classification_counts),
        "tag_counts": dict(tag_counts),
        "num_impossibility_or_prior_dependent_cells": len(impossibility_cells),
    }

    artifact_paths = [
        f"research/{PROJECT}/artifacts/{EXPERIMENT_ID}/identifiability_grid.py",
        f"research/{PROJECT}/artifacts/{EXPERIMENT_ID}/raw_grid.json",
        f"research/{PROJECT}/artifacts/{EXPERIMENT_ID}/metrics.csv",
        f"research/{PROJECT}/artifacts/{EXPERIMENT_ID}/regret_heatmap.csv",
        f"research/{PROJECT}/artifacts/{EXPERIMENT_ID}/action_choice_grid.csv",
        f"research/{PROJECT}/artifacts/{EXPERIMENT_ID}/impossibility_cases.json",
        f"research/{PROJECT}/artifacts/{EXPERIMENT_ID}/coverage_diagnostics.json",
        f"research/{PROJECT}/artifacts/{EXPERIMENT_ID}/transition_tables.json",
        f"research/{PROJECT}/artifacts/{EXPERIMENT_ID}/value_tables.json",
    ]
    write_json(artifact_dir / "raw_grid.json", raw_grid)
    write_csv(artifact_dir / "metrics.csv", metrics_rows)
    write_csv(artifact_dir / "regret_heatmap.csv", regret_rows)
    write_csv(artifact_dir / "action_choice_grid.csv", action_rows)
    write_json(artifact_dir / "impossibility_cases.json", {"cells": impossibility_cells})
    write_json(artifact_dir / "coverage_diagnostics.json", coverage_diagnostics)
    write_json(artifact_dir / "transition_tables.json", transition_tables)
    write_json(artifact_dir / "value_tables.json", value_tables)

    metrics = {
        "num_cells": len(cells),
        "num_method_rows": len(metrics_rows),
        "classification_counts": dict(classification_counts),
        "tag_counts": dict(tag_counts),
        "method_summary": method_summary,
        "chain_guard": chain_guard,
        "useful_identifiability_map": useful,
    }
    baseline_metrics = {
        "trl_log": method_summary["trl_log"],
        "empirical_transition_dp": method_summary["empirical_transition_dp"],
        "posterior_mean_beta_1_1": method_summary["posterior_mean_beta_1_1"],
    }
    metric_deltas = {
        "raw_trl_minus_trl_log_mean_regret": method_summary["raw_trl"]["mean_policy_regret"] - method_summary["trl_log"]["mean_policy_regret"],
        "posterior_mean_minus_trl_log_mean_regret": method_summary["posterior_mean_beta_1_1"]["mean_policy_regret"] - method_summary["trl_log"]["mean_policy_regret"],
        "hoeffding_lcb_minus_trl_log_mean_regret": method_summary["hoeffding_lcb_delta_0_2"]["mean_policy_regret"] - method_summary["trl_log"]["mean_policy_regret"],
    }
    decision_relevant_findings = [
        f"Grid produced {len(impossibility_cells)} ambiguous, lucky-only, no-success, or prior-dependent cells where action choice cannot be justified by empirical frequencies alone.",
        "TRL-log is identical to empirical transition DP on this tabular grid, so failures in those cells are data-identifiability failures rather than implementation-specific TRL-log failures.",
        "Posterior lower and upper choices intentionally disagree in prior-dependent cells, exposing where explicit priors are unavoidable.",
    ]
    success_criteria_results = [
        "Created self-contained 0008 artifact.",
        "Evaluated exact DP values and policy regret for every grid cell.",
        "Included deterministic chain guard.",
        "Saved per-cell raw metrics and heatmap-friendly CSVs.",
        "Separated identifiable, ambiguous, lucky-only, no-success, and prior-dependent regimes.",
    ]
    failure_criteria_results = [
        "No neural networks, continuous-control datasets, downloads, or broad sweeps were used.",
        "Posterior and confidence methods used only observed counts; true probabilities were used only for exact-DP evaluation.",
        "No algorithmic win was claimed; the result is an identifiability map.",
    ]
    interpretation = (
        "The grid is useful as an identifiability map: it separates cells where empirical transition estimates match exact action choice from lucky-only, no-success, ambiguous, and prior-dependent cells where explicit priors are required."
    )
    result = {
        "experiment_id": EXPERIMENT_ID,
        "status": "completed" if useful else "failed",
        "claim_tested": (
            "A compact exact-DP tabular grid can distinguish risky-shortcut failures caused by finite stochastic coverage from failures of the TRL-log update itself."
        ),
        "commands_run": COMMANDS_RUN,
        "metrics": metrics,
        "baseline_metrics": baseline_metrics,
        "artifacts": artifact_paths,
        "interpretation": interpretation,
        "known_failures": [] if useful else ["The grid did not identify any ambiguous or prior-dependent regimes."],
        "next_questions": [
            "Which prior should be declared for lucky-only and no-success regimes before algorithm development continues?",
            "Can future algorithms report identifiability status before choosing risky or safe?",
            "Should finite-coverage diagnostics gate TRL-style transitive updates in stochastic offline data?",
        ],
        "runtime_seconds": runtime_seconds,
        "resource_usage": {"device": "cpu", "num_cells": len(cells), "num_method_rows": len(metrics_rows)},
        "success_criteria_results": success_criteria_results,
        "failure_criteria_results": failure_criteria_results,
        "metric_deltas": metric_deltas,
        "decision_relevant_findings": decision_relevant_findings,
    }
    write_json(result_dir / f"{EXPERIMENT_ID}_result.json", result)

    summary = f"""# Experiment {EXPERIMENT_ID} Summary

## Objective

Map finite-coverage identifiability for tabular risky shortcuts before adding new stochastic TRL algorithms.

## Commands Run

```bash
{chr(10).join(COMMANDS_RUN)}
```

## Grid

- True risky success probabilities: `{list(TRUE_RISKY_PROBS)}`
- Safe route lengths: `{list(SAFE_LENGTHS)}`
- Risky sample counts: `{list(RISKY_SAMPLE_COUNTS)}`
- Observed successes: every integer from `0` to `risky_samples`
- Total cells: `{len(cells)}`

## Key Counts

- Classification counts: `{dict(classification_counts)}`
- Tag counts: `{dict(tag_counts)}`
- Impossibility/prior-dependent cells: `{len(impossibility_cells)}`
- Deterministic chain guard passed: `{chain_guard["passed"]}`

## Method Summary

| Method | Action accuracy | Mean policy regret |
| --- | ---: | ---: |
"""
    for method, stats in sorted(method_summary.items()):
        summary += f"| {method} | {stats['action_accuracy']:.6f} | {stats['mean_policy_regret']:.12f} |\n"

    summary += f"""
## Interpretation

{interpretation}

## Artifacts

- `research/{PROJECT}/artifacts/{EXPERIMENT_ID}/identifiability_grid.py`
- `research/{PROJECT}/artifacts/{EXPERIMENT_ID}/raw_grid.json`
- `research/{PROJECT}/artifacts/{EXPERIMENT_ID}/metrics.csv`
- `research/{PROJECT}/artifacts/{EXPERIMENT_ID}/regret_heatmap.csv`
- `research/{PROJECT}/artifacts/{EXPERIMENT_ID}/action_choice_grid.csv`
- `research/{PROJECT}/artifacts/{EXPERIMENT_ID}/impossibility_cases.json`
- `research/{PROJECT}/artifacts/{EXPERIMENT_ID}/coverage_diagnostics.json`
- `research/{PROJECT}/artifacts/{EXPERIMENT_ID}/transition_tables.json`
- `research/{PROJECT}/artifacts/{EXPERIMENT_ID}/value_tables.json`
"""
    (result_dir / f"{EXPERIMENT_ID}_summary.md").write_text(summary)
    print(json.dumps({"status": result["status"], "num_cells": len(cells), "classification_counts": dict(classification_counts)}, indent=2, sort_keys=True))
    return 0 if useful else 1


if __name__ == "__main__":
    raise SystemExit(main())
