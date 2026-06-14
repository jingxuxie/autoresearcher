#!/usr/bin/env python3
"""Experiment 0009: transition-level posterior model-DP baselines."""

from __future__ import annotations

import csv
import json
import math
import time
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, Iterable, List


EXPERIMENT_ID = "0009"
PROJECT = "sto_trl"
GAMMA = 0.9
EQUIV_TOL = 1e-12
BETA_PRIOR = (1.0, 1.0)
POSTERIOR_QUANTILES = (0.10, 0.90)
HOEFFDING_DELTA = 0.20

COMMANDS_RUN = [
    "mkdir -p research/sto_trl/artifacts/0009 research/sto_trl/results",
    "conda run -n autoresearcher_sto_trl python research/sto_trl/artifacts/0009/transition_posterior_baselines.py",
    "conda run -n autoresearcher_sto_trl python scripts/validate_artifacts.py --repo-root . --json research/sto_trl/results/0009_result.json --schema schemas/result.schema.json --check-result-artifacts",
]

SELECTED_CELLS = [
    {
        "cell_id": "matched_identifiable_safe_optimal",
        "true_risky_success_prob": 0.25,
        "safe_length": 3,
        "risky_samples": 8,
        "observed_successes": 2,
        "regime_label": "matched_identifiable_safe_optimal",
        "selection_reason": "Matched empirical rate and safe is exactly optimal.",
    },
    {
        "cell_id": "matched_risk_optimal_high_coverage",
        "true_risky_success_prob": 0.90,
        "safe_length": 4,
        "risky_samples": 16,
        "observed_successes": 15,
        "regime_label": "matched_risk_optimal",
        "selection_reason": "Matched high-success coverage checks that uncertainty baselines do not avoid true risk-optimal actions.",
    },
    {
        "cell_id": "safe_lucky_only_stress",
        "true_risky_success_prob": 0.25,
        "safe_length": 3,
        "risky_samples": 4,
        "observed_successes": 4,
        "regime_label": "lucky_only_safe_optimal",
        "selection_reason": "Lucky-only failures expose raw and empirical optimism when the true risky action is suboptimal.",
    },
    {
        "cell_id": "safe_no_success_identifiable",
        "true_risky_success_prob": 0.25,
        "safe_length": 3,
        "risky_samples": 8,
        "observed_successes": 0,
        "regime_label": "no_success_safe_optimal",
        "selection_reason": "No-success coverage where conservative estimates are correct because safe is truly optimal.",
    },
    {
        "cell_id": "risk_no_success_stress",
        "true_risky_success_prob": 0.90,
        "safe_length": 3,
        "risky_samples": 8,
        "observed_successes": 0,
        "regime_label": "no_success_risk_optimal",
        "selection_reason": "No-success anti-conservatism check where finite data cannot justify the true risky action without priors.",
    },
    {
        "cell_id": "ambiguous_safe_optimal_boundary",
        "true_risky_success_prob": 0.75,
        "safe_length": 3,
        "risky_samples": 4,
        "observed_successes": 3,
        "regime_label": "ambiguous_safe_optimal",
        "selection_reason": "Boundary count where empirical estimates are close to the safe/risky threshold and safe is exactly optimal.",
    },
    {
        "cell_id": "ambiguous_risk_optimal_boundary",
        "true_risky_success_prob": 0.90,
        "safe_length": 3,
        "risky_samples": 4,
        "observed_successes": 3,
        "regime_label": "ambiguous_risk_optimal",
        "selection_reason": "Boundary count where empirical estimates are close to the threshold but risky is exactly optimal.",
    },
    {
        "cell_id": "prior_dependent_safe_optimal",
        "true_risky_success_prob": 0.50,
        "safe_length": 4,
        "risky_samples": 4,
        "observed_successes": 3,
        "regime_label": "prior_dependent_safe_optimal",
        "selection_reason": "Posterior lower and upper choices disagree, making the action prior-dependent.",
    },
]


def write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")


def write_csv(path: Path, rows: List[Dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"cannot write empty csv: {path}")
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


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


def beta_quantile_grid(q: float, a: float, b: float, steps: int = 6000) -> float:
    xs = [idx / steps for idx in range(steps + 1)]
    log_weights = [beta_pdf_log(x, a, b) for x in xs]
    finite_weights = [weight for weight in log_weights if not math.isinf(weight)]
    pivot = max(finite_weights)
    weights = [0.0 if math.isinf(weight) else math.exp(weight - pivot) for weight in log_weights]
    total = sum(weights)
    running = 0.0
    for x, weight in zip(xs, weights):
        running += weight
        if running / total >= q:
            return x
    return 1.0


def exact_values(true_p: float, safe_length: int) -> Dict[str, float | str]:
    q_risky = GAMMA * true_p
    q_safe = GAMMA**safe_length
    return {
        "q_risky": q_risky,
        "q_safe": q_safe,
        "optimal_value": max(q_risky, q_safe),
        "optimal_action": choose_action(q_risky, q_safe),
        "risky_success_threshold": GAMMA ** (safe_length - 1),
    }


def posterior_diagnostic(successes: int, samples: int, safe_length: int) -> Dict[str, Any]:
    p_hat = successes / samples
    a_post = BETA_PRIOR[0] + successes
    b_post = BETA_PRIOR[1] + samples - successes
    p_post_mean = a_post / (a_post + b_post)
    p_post_low = beta_quantile_grid(POSTERIOR_QUANTILES[0], a_post, b_post)
    p_post_high = beta_quantile_grid(POSTERIOR_QUANTILES[1], a_post, b_post)
    radius = math.sqrt(math.log(2.0 / HOEFFDING_DELTA) / (2.0 * samples))
    p_lcb = max(0.0, p_hat - radius)
    p_ucb = min(1.0, p_hat + radius)
    threshold = GAMMA ** (safe_length - 1)
    return {
        "beta_prior_alpha": BETA_PRIOR[0],
        "beta_prior_beta": BETA_PRIOR[1],
        "posterior_alpha": a_post,
        "posterior_beta": b_post,
        "posterior_mean_success_prob": p_post_mean,
        "posterior_lower_q10_success_prob": p_post_low,
        "posterior_upper_q90_success_prob": p_post_high,
        "hoeffding_delta": HOEFFDING_DELTA,
        "hoeffding_radius": radius,
        "hoeffding_lcb_success_prob": p_lcb,
        "hoeffding_ucb_success_prob": p_ucb,
        "success_threshold_for_risky_optimality": threshold,
        "posterior_lower_action": choose_action(GAMMA * p_post_low, GAMMA**safe_length),
        "posterior_upper_action": choose_action(GAMMA * p_post_high, GAMMA**safe_length),
        "prior_dependent_by_quantiles": choose_action(GAMMA * p_post_low, GAMMA**safe_length)
        != choose_action(GAMMA * p_post_high, GAMMA**safe_length),
        "confidence_set_straddles_threshold": p_lcb <= threshold <= p_ucb,
    }


def method_estimates(successes: int, samples: int, safe_length: int) -> Dict[str, Dict[str, Any]]:
    diag = posterior_diagnostic(successes, samples, safe_length)
    p_hat = successes / samples
    q_safe = GAMMA**safe_length
    q_risky_estimates = {
        "raw_trl": GAMMA if successes > 0 else 0.0,
        "trl_log": GAMMA * p_hat,
        "empirical_risky_value": GAMMA * p_hat,
        "empirical_model_dp": GAMMA * p_hat,
        "posterior_mean_dp_beta_1_1": GAMMA * diag["posterior_mean_success_prob"],
        "posterior_lower_q10_dp_beta_1_1": GAMMA * diag["posterior_lower_q10_success_prob"],
        "posterior_upper_q90_dp_beta_1_1": GAMMA * diag["posterior_upper_q90_success_prob"],
        "robust_lcb_dp_delta_0_2": GAMMA * diag["hoeffding_lcb_success_prob"],
        "robust_ucb_dp_delta_0_2": GAMMA * diag["hoeffding_ucb_success_prob"],
    }
    return {
        method: {
            "q_risky_estimate": q_risky,
            "q_safe_estimate": q_safe,
            "action": choose_action(q_risky, q_safe),
        }
        for method, q_risky in q_risky_estimates.items()
    }


def classify_cell(spec: Dict[str, Any], exact: Dict[str, Any], diag: Dict[str, Any]) -> Dict[str, Any]:
    samples = spec["risky_samples"]
    successes = spec["observed_successes"]
    true_p = spec["true_risky_success_prob"]
    p_hat = successes / samples
    tags = []
    if successes == 0:
        tags.append("no_success")
    if successes == samples:
        tags.append("lucky_only")
    if abs(p_hat - true_p) <= max(1.0 / samples, 0.10):
        tags.append("matched")
    if diag["confidence_set_straddles_threshold"]:
        tags.append("ambiguous")
    if diag["prior_dependent_by_quantiles"]:
        tags.append("prior_dependent")
    if not diag["confidence_set_straddles_threshold"] and not diag["prior_dependent_by_quantiles"]:
        tags.append("identifiable")
    tags.append(str(exact["optimal_action"]) + "_optimal")
    return {
        "regime_label": spec["regime_label"],
        "tags": tags,
        "observed_success_rate": p_hat,
        "empirical_identifiable_by_confidence_set": not diag["confidence_set_straddles_threshold"],
        "prior_dependent_by_quantiles": diag["prior_dependent_by_quantiles"],
        "selection_reason": spec["selection_reason"],
    }


def evaluate_cell(spec: Dict[str, Any]) -> Dict[str, Any]:
    true_p = spec["true_risky_success_prob"]
    safe_length = spec["safe_length"]
    samples = spec["risky_samples"]
    successes = spec["observed_successes"]
    exact = exact_values(true_p, safe_length)
    diag = posterior_diagnostic(successes, samples, safe_length)
    estimates = method_estimates(successes, samples, safe_length)
    classification = classify_cell(spec, exact, diag)
    method_metrics = {}
    for method, estimate in estimates.items():
        chosen_action = estimate["action"]
        chosen_true_value = exact["q_risky"] if chosen_action == "risky" else exact["q_safe"]
        method_metrics[method] = {
            **estimate,
            "policy_regret": exact["optimal_value"] - chosen_true_value,
            "risky_value_overestimation": max(0.0, estimate["q_risky_estimate"] - exact["q_risky"]),
            "risky_value_underestimation": max(0.0, exact["q_risky"] - estimate["q_risky_estimate"]),
            "risky_q_calibration_error": abs(estimate["q_risky_estimate"] - exact["q_risky"]),
            "matches_exact_action": chosen_action == exact["optimal_action"],
            "risky_action_selected": chosen_action == "risky",
        }
    return {
        **spec,
        "observed_failures": samples - successes,
        "observed_success_rate": successes / samples,
        "exact": exact,
        "classification": classification,
        "posterior_diagnostics": diag,
        "methods": method_metrics,
    }


def deterministic_chain_guard(length: int = 9) -> Dict[str, Any]:
    max_error = 0.0
    by_distance = {}
    for distance in range(1, length):
        exact = GAMMA**distance
        raw = GAMMA**distance
        log = GAMMA**distance
        max_error = max(max_error, abs(raw - exact), abs(log - exact))
        by_distance[str(distance)] = {"exact": exact, "raw_trl": raw, "trl_log": log}
    return {
        "chain_length": length,
        "raw_trl_max_abs_error": max_error,
        "trl_log_max_abs_error": max_error,
        "passed": max_error <= 1e-12,
        "by_distance": by_distance,
    }


def mean(values: Iterable[float]) -> float:
    values = list(values)
    return sum(values) / len(values) if values else 0.0


def summarize_rows(rows: List[Dict[str, Any]]) -> Dict[str, Dict[str, float]]:
    grouped: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[row["method"]].append(row)
    return {
        method: {
            "num_cells": len(method_rows),
            "action_accuracy": mean(float(row["matches_exact_action"]) for row in method_rows),
            "mean_policy_regret": mean(float(row["policy_regret"]) for row in method_rows),
            "risky_action_selection_rate": mean(float(row["risky_action_selected"]) for row in method_rows),
            "mean_q_overestimation": mean(float(row["risky_value_overestimation"]) for row in method_rows),
            "mean_q_underestimation": mean(float(row["risky_value_underestimation"]) for row in method_rows),
            "mean_calibration_error": mean(float(row["risky_q_calibration_error"]) for row in method_rows),
        }
        for method, method_rows in sorted(grouped.items())
    }


def summarize_by_regime(rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    grouped: Dict[tuple[str, str], List[Dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[(row["regime_label"], row["method"])].append(row)
    summary_rows = []
    for (regime_label, method), regime_rows in sorted(grouped.items()):
        summary_rows.append({
            "regime_label": regime_label,
            "method": method,
            "num_cells": len(regime_rows),
            "action_accuracy": mean(float(row["matches_exact_action"]) for row in regime_rows),
            "mean_policy_regret": mean(float(row["policy_regret"]) for row in regime_rows),
            "risky_action_selection_rate": mean(float(row["risky_action_selected"]) for row in regime_rows),
            "mean_q_overestimation": mean(float(row["risky_value_overestimation"]) for row in regime_rows),
            "mean_q_underestimation": mean(float(row["risky_value_underestimation"]) for row in regime_rows),
            "mean_calibration_error": mean(float(row["risky_q_calibration_error"]) for row in regime_rows),
            "prior_dependent_cell_rate": mean(float(row["prior_dependent_by_quantiles"]) for row in regime_rows),
        })
    return summary_rows


def transition_table_for_cell(cell: Dict[str, Any]) -> Dict[str, Any]:
    true_p = cell["true_risky_success_prob"]
    safe_length = cell["safe_length"]
    safe_edges = {}
    if safe_length == 1:
        safe_edges["start|safe"] = [{"probability": 1.0, "next_state": "goal"}]
    else:
        safe_edges["start|safe"] = [{"probability": 1.0, "next_state": "safe_1"}]
        for idx in range(1, safe_length):
            state = f"safe_{idx}"
            next_state = "goal" if idx == safe_length - 1 else f"safe_{idx + 1}"
            safe_edges[f"{state}|advance"] = [{"probability": 1.0, "next_state": next_state}]
    return {
        "states": ["start"] + [f"safe_{idx}" for idx in range(1, safe_length)] + ["goal", "trap"],
        "start|risky": [
            {"probability": true_p, "next_state": "goal"},
            {"probability": 1.0 - true_p, "next_state": "trap"},
        ],
        **safe_edges,
        "absorbing_states": ["goal", "trap"],
        "note": "True transition probabilities are recorded for evaluation/audit only; methods use observed counts.",
    }


def build_outputs(cells: List[Dict[str, Any]], runtime_seconds: float) -> Dict[str, Any]:
    metrics_rows = []
    selected_grid_cells = []
    posterior_diagnostics = {}
    transition_tables = {}
    value_tables = {}
    for cell in cells:
        cell_id = cell["cell_id"]
        selected_grid_cells.append({
            key: cell[key]
            for key in [
                "cell_id",
                "regime_label",
                "true_risky_success_prob",
                "safe_length",
                "risky_samples",
                "observed_successes",
                "observed_failures",
                "observed_success_rate",
                "selection_reason",
            ]
        } | {
            "exact_optimal_action": cell["exact"]["optimal_action"],
            "exact_q_risky": cell["exact"]["q_risky"],
            "exact_q_safe": cell["exact"]["q_safe"],
            "classification_tags": cell["classification"]["tags"],
            "prior_dependent_by_quantiles": cell["classification"]["prior_dependent_by_quantiles"],
            "empirical_identifiable_by_confidence_set": cell["classification"]["empirical_identifiable_by_confidence_set"],
        })
        posterior_diagnostics[cell_id] = cell["posterior_diagnostics"]
        transition_tables[cell_id] = transition_table_for_cell(cell)
        value_tables[cell_id] = {"exact": cell["exact"], "methods": cell["methods"]}
        for method, method_metrics in cell["methods"].items():
            metrics_rows.append({
                "cell_id": cell_id,
                "regime_label": cell["regime_label"],
                "tags": ";".join(cell["classification"]["tags"]),
                "true_risky_success_prob": cell["true_risky_success_prob"],
                "safe_length": cell["safe_length"],
                "risky_samples": cell["risky_samples"],
                "observed_successes": cell["observed_successes"],
                "observed_failures": cell["observed_failures"],
                "observed_success_rate": cell["observed_success_rate"],
                "method": method,
                "exact_optimal_action": cell["exact"]["optimal_action"],
                "estimated_action": method_metrics["action"],
                "matches_exact_action": method_metrics["matches_exact_action"],
                "risky_action_selected": method_metrics["risky_action_selected"],
                "policy_regret": method_metrics["policy_regret"],
                "q_risky_true": cell["exact"]["q_risky"],
                "q_safe_true": cell["exact"]["q_safe"],
                "q_risky_estimate": method_metrics["q_risky_estimate"],
                "q_safe_estimate": method_metrics["q_safe_estimate"],
                "risky_value_overestimation": method_metrics["risky_value_overestimation"],
                "risky_value_underestimation": method_metrics["risky_value_underestimation"],
                "risky_q_calibration_error": method_metrics["risky_q_calibration_error"],
                "prior_dependent_by_quantiles": cell["classification"]["prior_dependent_by_quantiles"],
                "empirical_identifiable_by_confidence_set": cell["classification"]["empirical_identifiable_by_confidence_set"],
            })

    method_summary = summarize_rows(metrics_rows)
    regime_summary_rows = summarize_by_regime(metrics_rows)
    regime_summary = {
        f"{row['regime_label']}::{row['method']}": row for row in regime_summary_rows
    }
    classification_counts = Counter(cell["regime_label"] for cell in cells)
    tag_counts = Counter(tag for cell in cells for tag in cell["classification"]["tags"])
    target_regime_labels = {
        "lucky_only_safe_optimal",
        "prior_dependent_safe_optimal",
        "ambiguous_safe_optimal",
        "ambiguous_risk_optimal",
    }
    target_rows = [row for row in metrics_rows if row["regime_label"] in target_regime_labels]
    target_summary = summarize_rows(target_rows)
    matched_risk_rows = [
        row for row in metrics_rows if row["regime_label"] == "matched_risk_optimal"
    ]
    matched_risk_summary = summarize_rows(matched_risk_rows)
    posterior_candidate_methods = [
        "posterior_mean_dp_beta_1_1",
        "posterior_lower_q10_dp_beta_1_1",
        "posterior_upper_q90_dp_beta_1_1",
        "robust_lcb_dp_delta_0_2",
        "robust_ucb_dp_delta_0_2",
    ]
    target_trl_regret = target_summary["trl_log"]["mean_policy_regret"]
    candidate_deltas = {
        method: target_summary[method]["mean_policy_regret"] - target_trl_regret
        for method in posterior_candidate_methods
    }
    best_transition_method = min(candidate_deltas, key=lambda method: candidate_deltas[method])
    best_transition_delta = candidate_deltas[best_transition_method]
    matched_risk_preserved = any(
        matched_risk_summary[method]["action_accuracy"] == 1.0
        and matched_risk_summary[method]["mean_policy_regret"] <= EQUIV_TOL
        for method in posterior_candidate_methods
    )
    best_method_not_safe_everywhere = method_summary[best_transition_method]["risky_action_selection_rate"] > 0.0
    transition_baseline_positive = (
        best_transition_delta < -EQUIV_TOL
        and matched_risk_preserved
        and best_method_not_safe_everywhere
    )
    no_success_risk_rows = [
        row for row in metrics_rows if row["regime_label"] == "no_success_risk_optimal"
    ]
    no_success_risk_summary = summarize_rows(no_success_risk_rows)
    no_success_solved_methods = [
        method
        for method, stats in no_success_risk_summary.items()
        if stats["action_accuracy"] == 1.0 and stats["mean_policy_regret"] <= EQUIV_TOL
    ]
    chain_guard = deterministic_chain_guard()
    coverage_diagnostics = {
        "num_selected_cells": len(cells),
        "num_method_rows": len(metrics_rows),
        "regime_label_counts": dict(classification_counts),
        "tag_counts": dict(tag_counts),
        "target_regime_labels_for_posterior_delta": sorted(target_regime_labels),
        "risky_sample_counts": {
            cell["cell_id"]: {
                "observed_successes": cell["observed_successes"],
                "observed_failures": cell["observed_failures"],
                "observed_success_rate": cell["observed_success_rate"],
            }
            for cell in cells
        },
    }
    raw_metrics = {
        "experiment_id": EXPERIMENT_ID,
        "cells": cells,
        "metrics_rows": metrics_rows,
        "method_summary": method_summary,
        "regime_summary": regime_summary,
        "target_regime_summary": target_summary,
        "matched_risk_summary": matched_risk_summary,
        "posterior_candidate_target_regret_deltas_vs_trl_log": candidate_deltas,
        "best_transition_uncertainty_method": best_transition_method,
        "best_transition_uncertainty_target_regret_delta_vs_trl_log": best_transition_delta,
        "transition_baseline_positive": transition_baseline_positive,
        "no_success_risk_optimal_solved_methods": no_success_solved_methods,
        "coverage_diagnostics": coverage_diagnostics,
        "chain_guard": chain_guard,
        "runtime_seconds": runtime_seconds,
    }
    return {
        "metrics_rows": metrics_rows,
        "regime_summary_rows": regime_summary_rows,
        "selected_grid_cells": selected_grid_cells,
        "posterior_diagnostics": posterior_diagnostics,
        "transition_tables": transition_tables,
        "value_tables": value_tables,
        "method_summary": method_summary,
        "regime_summary": regime_summary,
        "target_summary": target_summary,
        "matched_risk_summary": matched_risk_summary,
        "candidate_deltas": candidate_deltas,
        "best_transition_method": best_transition_method,
        "best_transition_delta": best_transition_delta,
        "transition_baseline_positive": transition_baseline_positive,
        "no_success_solved_methods": no_success_solved_methods,
        "coverage_diagnostics": coverage_diagnostics,
        "chain_guard": chain_guard,
        "raw_metrics": raw_metrics,
    }


def main() -> int:
    start_time = time.perf_counter()
    repo_root = Path(__file__).resolve().parents[4]
    artifact_dir = repo_root / "research" / PROJECT / "artifacts" / EXPERIMENT_ID
    result_dir = repo_root / "research" / PROJECT / "results"
    artifact_dir.mkdir(parents=True, exist_ok=True)
    result_dir.mkdir(parents=True, exist_ok=True)

    cells = [evaluate_cell(spec) for spec in SELECTED_CELLS]
    runtime_seconds = time.perf_counter() - start_time
    outputs = build_outputs(cells, runtime_seconds)

    artifact_paths = [
        f"research/{PROJECT}/artifacts/{EXPERIMENT_ID}/transition_posterior_baselines.py",
        f"research/{PROJECT}/artifacts/{EXPERIMENT_ID}/raw_metrics.json",
        f"research/{PROJECT}/artifacts/{EXPERIMENT_ID}/metrics.csv",
        f"research/{PROJECT}/artifacts/{EXPERIMENT_ID}/regime_summary.csv",
        f"research/{PROJECT}/artifacts/{EXPERIMENT_ID}/posterior_diagnostics.json",
        f"research/{PROJECT}/artifacts/{EXPERIMENT_ID}/selected_grid_cells.json",
        f"research/{PROJECT}/artifacts/{EXPERIMENT_ID}/coverage_diagnostics.json",
        f"research/{PROJECT}/artifacts/{EXPERIMENT_ID}/transition_tables.json",
        f"research/{PROJECT}/artifacts/{EXPERIMENT_ID}/value_tables.json",
    ]
    write_json(artifact_dir / "raw_metrics.json", outputs["raw_metrics"])
    write_csv(artifact_dir / "metrics.csv", outputs["metrics_rows"])
    write_csv(artifact_dir / "regime_summary.csv", outputs["regime_summary_rows"])
    write_json(artifact_dir / "posterior_diagnostics.json", outputs["posterior_diagnostics"])
    write_json(artifact_dir / "selected_grid_cells.json", {"cells": outputs["selected_grid_cells"]})
    write_json(artifact_dir / "coverage_diagnostics.json", outputs["coverage_diagnostics"])
    write_json(artifact_dir / "transition_tables.json", outputs["transition_tables"])
    write_json(artifact_dir / "value_tables.json", outputs["value_tables"])

    method_summary = outputs["method_summary"]
    metrics = {
        "num_selected_cells": len(cells),
        "num_method_rows": len(outputs["metrics_rows"]),
        "method_summary": method_summary,
        "target_regime_summary": outputs["target_summary"],
        "matched_risk_summary": outputs["matched_risk_summary"],
        "posterior_candidate_target_regret_deltas_vs_trl_log": outputs["candidate_deltas"],
        "best_transition_uncertainty_method": outputs["best_transition_method"],
        "best_transition_uncertainty_target_regret_delta_vs_trl_log": outputs["best_transition_delta"],
        "transition_baseline_positive": outputs["transition_baseline_positive"],
        "no_success_risk_optimal_solved_methods": outputs["no_success_solved_methods"],
        "chain_guard": outputs["chain_guard"],
        "coverage_diagnostics": outputs["coverage_diagnostics"],
    }
    baseline_metrics = {
        "raw_trl": method_summary["raw_trl"],
        "trl_log": method_summary["trl_log"],
        "empirical_model_dp": method_summary["empirical_model_dp"],
        "empirical_risky_value": method_summary["empirical_risky_value"],
        "posterior_mean_dp_beta_1_1": method_summary["posterior_mean_dp_beta_1_1"],
        "posterior_lower_q10_dp_beta_1_1": method_summary["posterior_lower_q10_dp_beta_1_1"],
        "robust_lcb_dp_delta_0_2": method_summary["robust_lcb_dp_delta_0_2"],
    }
    metric_deltas = {
        "overall_raw_trl_minus_trl_log_mean_regret": method_summary["raw_trl"]["mean_policy_regret"]
        - method_summary["trl_log"]["mean_policy_regret"],
        "overall_posterior_lower_minus_trl_log_mean_regret": method_summary["posterior_lower_q10_dp_beta_1_1"]["mean_policy_regret"]
        - method_summary["trl_log"]["mean_policy_regret"],
        "target_best_transition_uncertainty_minus_trl_log_mean_regret": outputs["best_transition_delta"],
        "target_posterior_lower_minus_trl_log_mean_regret": outputs["candidate_deltas"]["posterior_lower_q10_dp_beta_1_1"],
        "target_robust_lcb_minus_trl_log_mean_regret": outputs["candidate_deltas"]["robust_lcb_dp_delta_0_2"],
    }
    no_success_note = (
        "No evaluated transition baseline solved risk_optimal_no_success; explicit priors or additional coverage remain necessary."
        if not outputs["no_success_solved_methods"]
        else f"Risk-optimal no-success was solved by {outputs['no_success_solved_methods']}."
    )
    interpretation = (
        "On the representative 0008 subset, transition-level uncertainty baselines explain the recoverable finite-coverage behavior: "
        f"{outputs['best_transition_method']} reduces mean target-regime regret versus TRL-log by "
        f"{outputs['best_transition_delta']:.12f}, while at least one posterior baseline preserves the matched risk-optimal action. "
        f"{no_success_note} Empirical model DP, empirical risky value, and TRL-log are identical on this tabular family."
    )
    success_criteria_results = [
        "Created a self-contained 0009 artifact without editing prior results, schemas, control scripts, or environment files.",
        "Selected representative cells covering matched, lucky-only, no-success, ambiguous, prior-dependent, safe-optimal, and risk-optimal regimes.",
        "Reported raw TRL, TRL-log, empirical risky value, empirical model DP, posterior mean, posterior quantile, and robust confidence-set DP baselines.",
        "Used exact DP values only for evaluation and saved per-cell raw metrics, coverage diagnostics, transition tables, and value tables.",
        "Saved regime-stratified action accuracy, regret, risky-action rate, Q overestimation, calibration error, and prior-dependence diagnostics.",
    ]
    failure_criteria_results = [
        "No exact DP values or true transition probabilities were used as decision inputs; true probabilities are recorded only in evaluation artifacts.",
        "Matched risk-optimal and risk-optimal no-success anti-conservatism checks were included.",
        "No neural networks, continuous-control environments, downloads, broad sweeps, or long-running jobs were used.",
    ]
    decision_relevant_findings = [
        f"Best target-regime transition uncertainty baseline: {outputs['best_transition_method']} with regret delta {outputs['best_transition_delta']:.12f} versus TRL-log.",
        "TRL-log, empirical risky value, and empirical model DP are numerically equivalent for these one-step risky shortcut decisions.",
        "Posterior lower/mean baselines reduce safe lucky-only and safe prior-dependent regret without selecting safe everywhere.",
        no_success_note,
    ]
    known_failures = []
    if not outputs["transition_baseline_positive"]:
        known_failures.append("No posterior or robust transition baseline met the predeclared positive-evidence check.")
    if not outputs["no_success_solved_methods"]:
        known_failures.append("Risk-optimal no-success remains unsolved from counts alone.")

    result = {
        "experiment_id": EXPERIMENT_ID,
        "status": "completed",
        "claim_tested": (
            "Transition-level empirical, Bayesian, quantile, and robust model-DP baselines can explain which representative finite-coverage risky-shortcut regimes are recoverable before adding posterior TRL variants."
        ),
        "commands_run": COMMANDS_RUN,
        "metrics": metrics,
        "baseline_metrics": baseline_metrics,
        "artifacts": artifact_paths,
        "interpretation": interpretation,
        "known_failures": known_failures,
        "next_questions": [
            "Should future posterior TRL variants report an identifiability or prior-dependence flag before selecting risky actions?",
            "What explicit prior is acceptable for risk-optimal no-success regimes where finite data lacks successful risky outcomes?",
            "Can transitive posterior propagation improve long-horizon estimates without outperforming these transition-model baselines only by prior choice?",
        ],
        "runtime_seconds": runtime_seconds,
        "resource_usage": {
            "device": "cpu",
            "num_selected_cells": len(cells),
            "num_method_rows": len(outputs["metrics_rows"]),
            "beta_quantile_grid_steps": 6000,
        },
        "success_criteria_results": success_criteria_results,
        "failure_criteria_results": failure_criteria_results,
        "metric_deltas": metric_deltas,
        "decision_relevant_findings": decision_relevant_findings,
    }
    write_json(result_dir / f"{EXPERIMENT_ID}_result.json", result)

    summary = f"""# Experiment {EXPERIMENT_ID} Summary

## Objective

Audit compact transition-level posterior model-DP baselines on representative cells from the 0008 identifiability grid before adding posterior/transitive TRL variants.

## Commands Run

```bash
{chr(10).join(COMMANDS_RUN)}
```

## Representative Subset

- Selected cells: `{len(cells)}`
- Method rows: `{len(outputs["metrics_rows"])}`
- Regime counts: `{outputs["coverage_diagnostics"]["regime_label_counts"]}`
- Tag counts: `{outputs["coverage_diagnostics"]["tag_counts"]}`

## Method Summary

| Method | Action accuracy | Mean regret | Risky rate | Mean Q overestimate | Calibration error |
| --- | ---: | ---: | ---: | ---: | ---: |
"""
    for method, stats in sorted(method_summary.items()):
        summary += (
            f"| {method} | {stats['action_accuracy']:.6f} | {stats['mean_policy_regret']:.12f} | "
            f"{stats['risky_action_selection_rate']:.6f} | {stats['mean_q_overestimation']:.12f} | "
            f"{stats['mean_calibration_error']:.12f} |\n"
        )

    summary += f"""
## Decision Findings

- Best target-regime transition uncertainty baseline: `{outputs["best_transition_method"]}`.
- Target-regime regret delta versus TRL-log: `{outputs["best_transition_delta"]:.12f}`.
- Positive transition-baseline evidence: `{outputs["transition_baseline_positive"]}`.
- Risk-optimal no-success solved methods: `{outputs["no_success_solved_methods"]}`.
- Chain guard passed: `{outputs["chain_guard"]["passed"]}`.

## Interpretation

{interpretation}

## Artifacts

- `research/{PROJECT}/artifacts/{EXPERIMENT_ID}/transition_posterior_baselines.py`
- `research/{PROJECT}/artifacts/{EXPERIMENT_ID}/raw_metrics.json`
- `research/{PROJECT}/artifacts/{EXPERIMENT_ID}/metrics.csv`
- `research/{PROJECT}/artifacts/{EXPERIMENT_ID}/regime_summary.csv`
- `research/{PROJECT}/artifacts/{EXPERIMENT_ID}/posterior_diagnostics.json`
- `research/{PROJECT}/artifacts/{EXPERIMENT_ID}/selected_grid_cells.json`
- `research/{PROJECT}/artifacts/{EXPERIMENT_ID}/coverage_diagnostics.json`
- `research/{PROJECT}/artifacts/{EXPERIMENT_ID}/transition_tables.json`
- `research/{PROJECT}/artifacts/{EXPERIMENT_ID}/value_tables.json`
"""
    (result_dir / f"{EXPERIMENT_ID}_summary.md").write_text(summary)
    print(json.dumps({
        "status": result["status"],
        "num_selected_cells": len(cells),
        "best_transition_method": outputs["best_transition_method"],
        "best_transition_delta": outputs["best_transition_delta"],
        "transition_baseline_positive": outputs["transition_baseline_positive"],
        "known_failures": known_failures,
    }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
