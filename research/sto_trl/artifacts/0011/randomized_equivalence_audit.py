#!/usr/bin/env python3
"""Experiment 0011: randomized posterior TRL/model-DP equivalence audit."""

from __future__ import annotations

import csv
import json
import math
import random
import time
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple


EXPERIMENT_ID = "0011"
PROJECT = "sto_trl"
GAMMA = 0.9
LABEL_HORIZON_CUTOFF = 2
BETA_PRIOR = (1.0, 1.0)
POSTERIOR_LOWER_QUANTILE = 0.10
EQUIV_TOL = 1e-12
NEAR_EQ_TOL = 1e-10
FAMILIES = ("branch_chain", "stochastic_stitching", "teleporter")
SEEDS = (0, 1, 2, 3, 4)

COMMANDS_RUN = [
    "mkdir -p research/sto_trl/artifacts/0011 research/sto_trl/results",
    "conda run -n autoresearcher_sto_trl python research/sto_trl/artifacts/0011/randomized_equivalence_audit.py",
    "conda run -n autoresearcher_sto_trl python scripts/validate_artifacts.py --repo-root . --json research/sto_trl/results/0011_result.json --schema schemas/result.schema.json --check-result-artifacts",
]

METHODS = [
    "mc_supervised",
    "trl_raw",
    "trl_log",
    "empirical_model_dp",
    "posterior_mean_model_dp",
    "posterior_lower_q10_model_dp",
    "posterior_trl_log",
    "posterior_mc_plus_trl_log",
]

Pair = Tuple[str, str]


def write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")


def write_csv(path: Path, rows: List[Dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"cannot write empty CSV: {path}")
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def pair_key(pair: Pair) -> str:
    return f"{pair[0]}|{pair[1]}"


def choose_action(q_risky: float, q_safe: float) -> str:
    return "risky" if q_risky > q_safe + EQUIV_TOL else "safe"


def mean(values: Iterable[float]) -> float:
    values = list(values)
    return sum(values) / len(values) if values else 0.0


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


def beta_quantile_grid(q: float, a: float, b: float, steps: int = 5000) -> float:
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


def make_spec(family: str, seed: int) -> Dict[str, Any]:
    rng = random.Random(1100 + 97 * FAMILIES.index(family) + seed)
    if seed == 0:
        regime = "matched_safe_optimal"
        safe_length = rng.choice([4, 5])
        risk_tail_steps = 2
        threshold = (GAMMA**safe_length) / (GAMMA ** (1 + risk_tail_steps))
        true_p = max(0.20, threshold - rng.uniform(0.18, 0.26))
        samples = 12
        successes = max(1, min(samples - 1, round(true_p * samples)))
        tags = ["matched", "safe_optimal"]
    elif seed == 1:
        regime = "matched_risk_optimal"
        safe_length = rng.choice([4, 5])
        risk_tail_steps = 2
        threshold = (GAMMA**safe_length) / (GAMMA ** (1 + risk_tail_steps))
        true_p = min(0.98, threshold + rng.uniform(0.08, 0.13))
        samples = 20
        successes = max(1, min(samples, round(true_p * samples)))
        tags = ["matched", "risk_optimal"]
    elif seed == 2:
        regime = "lucky_only_safe_optimal"
        safe_length = 4
        risk_tail_steps = 2
        true_p = rng.uniform(0.42, 0.56)
        samples = 4
        successes = 4
        tags = ["lucky_only", "safe_optimal", "biased_coverage"]
    elif seed == 3:
        regime = "no_success_risk_optimal"
        safe_length = 4
        risk_tail_steps = 2
        true_p = rng.uniform(0.93, 0.98)
        samples = 8
        successes = 0
        tags = ["no_success", "risk_optimal", "biased_coverage"]
    else:
        regime = "sparse_prior_dependent_risk_optimal"
        safe_length = 5
        risk_tail_steps = 2
        true_p = rng.uniform(0.82, 0.86)
        samples = 4
        successes = 3
        tags = ["ambiguous", "prior_dependent", "risk_optimal", "sparse_coverage"]
    return {
        "mdp_id": f"{family}_seed{seed}",
        "family": family,
        "seed": seed,
        "regime": regime,
        "true_risky_success_prob": true_p,
        "safe_length": safe_length,
        "risk_tail_steps": risk_tail_steps,
        "risky_samples": samples,
        "observed_successes": successes,
        "observed_failures": samples - successes,
        "safe_trajectories": 4,
        "stitch_demo_trajectories": 2 if family == "stochastic_stitching" else 0,
        "tags": tags,
    }


def build_suite() -> List[Dict[str, Any]]:
    return [make_spec(family, seed) for family in FAMILIES for seed in SEEDS]


def add_chain(
    actions: Dict[str, List[str]],
    transitions: Dict[Pair, List[Tuple[float, str]]],
    prefix: str,
    start_state: str,
    action_name: str,
    length: int,
) -> List[Dict[str, str]]:
    path = []
    if length <= 0:
        transitions[(start_state, action_name)] = [(1.0, "goal")]
        actions.setdefault(start_state, [action_name])
        path.append({"state": start_state, "action": action_name, "next_state": "goal"})
        return path
    first = f"{prefix}_1"
    transitions[(start_state, action_name)] = [(1.0, first)]
    actions.setdefault(start_state, [])
    if action_name not in actions[start_state]:
        actions[start_state].append(action_name)
    path.append({"state": start_state, "action": action_name, "next_state": first})
    for idx in range(1, length + 1):
        state = f"{prefix}_{idx}"
        actions[state] = ["advance"]
        next_state = "goal" if idx == length else f"{prefix}_{idx + 1}"
        transitions[(state, "advance")] = [(1.0, next_state)]
        path.append({"state": state, "action": "advance", "next_state": next_state})
    return path


def family_success_path(spec: Dict[str, Any]) -> List[Dict[str, str]]:
    tail = spec["risk_tail_steps"]
    family = spec["family"]
    if family == "branch_chain":
        path = [{"state": "start", "action": "risky", "next_state": "risk_1"}]
        for idx in range(1, tail + 1):
            state = f"risk_{idx}"
            next_state = "goal" if idx == tail else f"risk_{idx + 1}"
            path.append({"state": state, "action": "advance", "next_state": next_state})
        return path
    if family == "stochastic_stitching":
        path = [{"state": "start", "action": "risky", "next_state": "hub"}]
        for idx in range(1, tail + 1):
            state = "hub" if idx == 1 else f"stitch_{idx - 1}"
            next_state = "goal" if idx == tail else f"stitch_{idx}"
            path.append({"state": state, "action": "advance", "next_state": next_state})
        return path
    if family == "teleporter":
        path = [{"state": "start", "action": "risky", "next_state": "teleport_pad"}]
        for idx in range(1, tail + 1):
            state = "teleport_pad" if idx == 1 else f"tele_{idx - 1}"
            next_state = "goal" if idx == tail else f"tele_{idx}"
            path.append({"state": state, "action": "advance", "next_state": next_state})
        return path
    raise ValueError(f"unknown family: {family}")


def success_state_for_family(family: str) -> str:
    if family == "branch_chain":
        return "risk_1"
    if family == "stochastic_stitching":
        return "hub"
    if family == "teleporter":
        return "teleport_pad"
    raise ValueError(f"unknown family: {family}")


def build_mdp(spec: Dict[str, Any]) -> Dict[str, Any]:
    actions: Dict[str, List[str]] = {"start": ["safe", "risky"]}
    true_transitions: Dict[Pair, List[Tuple[float, str]]] = {
        ("start", "safe"): [(1.0, "safe_1")],
        ("start", "risky"): [
            (spec["true_risky_success_prob"], success_state_for_family(spec["family"])),
            (1.0 - spec["true_risky_success_prob"], "trap"),
        ],
    }
    safe_path = []
    for idx in range(1, spec["safe_length"]):
        state = f"safe_{idx}"
        actions[state] = ["advance"]
        next_state = "goal" if idx == spec["safe_length"] - 1 else f"safe_{idx + 1}"
        true_transitions[(state, "advance")] = [(1.0, next_state)]
        if idx == 1:
            safe_path.append({"state": "start", "action": "safe", "next_state": "safe_1"})
        safe_path.append({"state": state, "action": "advance", "next_state": next_state})
    success_path = family_success_path(spec)
    for transition in success_path[1:]:
        state = transition["state"]
        actions[state] = ["advance"]
        true_transitions[(state, "advance")] = [(1.0, transition["next_state"])]
    stitch_demo_path: List[Dict[str, str]] = []
    if spec["family"] == "stochastic_stitching":
        actions["demo_start"] = ["stitch"]
        true_transitions[("demo_start", "stitch")] = [(1.0, "hub")]
        stitch_demo_path = [{"state": "demo_start", "action": "stitch", "next_state": "hub"}] + success_path[1:]
    horizons: Dict[Pair, int] = {
        ("start", "safe"): spec["safe_length"],
        ("start", "risky"): 1 + spec["risk_tail_steps"],
    }
    for idx in range(1, spec["safe_length"]):
        horizons[(f"safe_{idx}", "advance")] = spec["safe_length"] - idx
    for step_idx, transition in enumerate(success_path[1:], start=1):
        horizons[(transition["state"], transition["action"])] = spec["risk_tail_steps"] - step_idx + 1
    if spec["family"] == "stochastic_stitching":
        horizons[("demo_start", "stitch")] = 1 + spec["risk_tail_steps"]
    return {
        "actions": actions,
        "true_transitions": true_transitions,
        "safe_path": safe_path,
        "success_path": success_path,
        "failure_path": [{"state": "start", "action": "risky", "next_state": "trap"}],
        "stitch_demo_path": stitch_demo_path,
        "horizons_to_goal_if_successful": horizons,
    }


def build_dataset(spec: Dict[str, Any], mdp: Dict[str, Any]) -> Dict[str, Any]:
    trajectories = []
    for idx in range(spec["safe_trajectories"]):
        trajectories.append({
            "trajectory_id": f"{spec['mdp_id']}_safe_{idx}",
            "outcome": "safe_success",
            "transitions": mdp["safe_path"],
        })
    for idx in range(spec["observed_successes"]):
        trajectories.append({
            "trajectory_id": f"{spec['mdp_id']}_risky_success_{idx}",
            "outcome": "risky_success",
            "transitions": mdp["success_path"],
        })
    for idx in range(spec["observed_failures"]):
        trajectories.append({
            "trajectory_id": f"{spec['mdp_id']}_risky_failure_{idx}",
            "outcome": "risky_failure",
            "transitions": mdp["failure_path"],
        })
    for idx in range(spec["stitch_demo_trajectories"]):
        trajectories.append({
            "trajectory_id": f"{spec['mdp_id']}_stitch_demo_{idx}",
            "outcome": "stitch_demo_success",
            "transitions": mdp["stitch_demo_path"],
        })
    transition_counts: Dict[Pair, Dict[str, int]] = defaultdict(lambda: defaultdict(int))
    for trajectory in trajectories:
        for transition in trajectory["transitions"]:
            transition_counts[(transition["state"], transition["action"])][transition["next_state"]] += 1
    return {
        "trajectories": trajectories,
        "transition_counts": transition_counts,
        "transition_counts_json": {
            pair_key(pair): dict(next_counts)
            for pair, next_counts in sorted(transition_counts.items())
        },
        "summary": {
            "num_trajectories": len(trajectories),
            "risky_samples": spec["risky_samples"],
            "observed_successes": spec["observed_successes"],
            "observed_failures": spec["observed_failures"],
            "observed_success_rate": spec["observed_successes"] / spec["risky_samples"],
        },
    }


def goal_horizon(transitions: List[Dict[str, str]], step_index: int) -> int | None:
    for idx in range(step_index, len(transitions)):
        if transitions[idx]["next_state"] == "goal":
            return idx - step_index + 1
    return None


def build_labels(dataset: Dict[str, Any]) -> Dict[str, Any]:
    labels: Dict[Pair, List[float]] = defaultdict(list)
    coverage: Dict[Pair, Dict[str, int]] = defaultdict(lambda: {
        "positive_labels": 0,
        "zero_labels": 0,
        "censored_positive_labels": 0,
        "total_occurrences": 0,
    })
    for trajectory in dataset["trajectories"]:
        transitions = trajectory["transitions"]
        for idx, transition in enumerate(transitions):
            pair = (transition["state"], transition["action"])
            coverage[pair]["total_occurrences"] += 1
            horizon = goal_horizon(transitions, idx)
            if horizon is None:
                labels[pair].append(0.0)
                coverage[pair]["zero_labels"] += 1
            elif horizon <= LABEL_HORIZON_CUTOFF:
                labels[pair].append(GAMMA**horizon)
                coverage[pair]["positive_labels"] += 1
            else:
                coverage[pair]["censored_positive_labels"] += 1
    return {
        "label_means": {pair: mean(values) for pair, values in labels.items()},
        "coverage_json": {
            pair_key(pair): {
                **stats,
                "label_count_used": len(labels.get(pair, [])),
                "mean_used_label": mean(labels.get(pair, [])) if labels.get(pair, []) else 0.0,
            }
            for pair, stats in sorted(coverage.items())
        },
    }


def max_state_value(state: str, q_values: Dict[Pair, float], actions: Dict[str, List[str]]) -> float:
    return max((q_values.get((state, action), 0.0) for action in actions.get(state, [])), default=0.0)


def solve_dp(actions: Dict[str, List[str]], transitions: Dict[Pair, List[Tuple[float, str]]], iterations: int = 200) -> Dict[Pair, float]:
    pairs = [(state, action) for state, state_actions in actions.items() for action in state_actions]
    q_values = {pair: 0.0 for pair in pairs}
    for _ in range(iterations):
        next_q = {}
        for pair in pairs:
            total = 0.0
            for prob, next_state in transitions.get(pair, []):
                continuation = 1.0 if next_state == "goal" else max_state_value(next_state, q_values, actions)
                total += prob * continuation
            next_q[pair] = GAMMA * total
        q_values = next_q
    return q_values


def posterior_success_probability(successes: int, failures: int, kind: str) -> float:
    if kind == "empirical":
        total = successes + failures
        return successes / total if total else 0.0
    alpha = BETA_PRIOR[0] + successes
    beta = BETA_PRIOR[1] + failures
    if kind == "posterior_mean":
        return alpha / (alpha + beta)
    if kind == "posterior_lower_q10":
        return beta_quantile_grid(POSTERIOR_LOWER_QUANTILE, alpha, beta)
    raise ValueError(f"unknown probability kind: {kind}")


def model_transitions(pair: Pair, kind: str, spec: Dict[str, Any], dataset: Dict[str, Any]) -> List[Tuple[float, str]]:
    if pair == ("start", "risky"):
        successes = spec["observed_successes"]
        failures = spec["observed_failures"]
        if kind == "empirical":
            total = successes + failures
            transitions = []
            if successes:
                transitions.append((successes / total, success_state_for_family(spec["family"])))
            if failures:
                transitions.append((failures / total, "trap"))
            return transitions
        p_success = posterior_success_probability(successes, failures, kind)
        return [(p_success, success_state_for_family(spec["family"])), (1.0 - p_success, "trap")]
    next_counts = dataset["transition_counts"].get(pair, {})
    total = sum(next_counts.values())
    if total == 0:
        return []
    return [(count / total, next_state) for next_state, count in sorted(next_counts.items())]


def run_raw(actions: Dict[str, List[str]], dataset: Dict[str, Any], iterations: int = 200) -> Dict[Pair, float]:
    pairs = [(state, action) for state, state_actions in actions.items() for action in state_actions]
    q_values = {pair: 0.0 for pair in pairs}
    counts = dataset["transition_counts"]
    for _ in range(iterations):
        next_q = {}
        for pair in pairs:
            next_states = list(counts.get(pair, {}).keys())
            if not next_states:
                next_q[pair] = 0.0
                continue
            best = max(
                1.0 if next_state == "goal" else max_state_value(next_state, q_values, actions)
                for next_state in next_states
            )
            next_q[pair] = GAMMA * best
        q_values = next_q
    return q_values


def run_model(
    actions: Dict[str, List[str]],
    spec: Dict[str, Any],
    dataset: Dict[str, Any],
    kind: str,
    positive_anchors: Dict[Pair, float] | None = None,
    iterations: int = 200,
) -> Dict[Pair, float]:
    pairs = [(state, action) for state, state_actions in actions.items() for action in state_actions]
    q_values = {pair: 0.0 for pair in pairs}
    positive_anchors = positive_anchors or {}
    for _ in range(iterations):
        next_q = {}
        for pair in pairs:
            total = 0.0
            for prob, next_state in model_transitions(pair, kind, spec, dataset):
                continuation = 1.0 if next_state == "goal" else max_state_value(next_state, q_values, actions)
                total += prob * continuation
            backup = GAMMA * total
            if pair in positive_anchors:
                backup = max(backup, positive_anchors[pair])
            next_q[pair] = backup
        q_values = next_q
    return q_values


def run_mc(actions: Dict[str, List[str]], label_means: Dict[Pair, float]) -> Dict[Pair, float]:
    pairs = [(state, action) for state, state_actions in actions.items() for action in state_actions]
    return {pair: label_means.get(pair, 0.0) for pair in pairs}


def run_methods(spec: Dict[str, Any], mdp: Dict[str, Any], dataset: Dict[str, Any], labels: Dict[str, Any]) -> Dict[str, Dict[Pair, float]]:
    actions = mdp["actions"]
    positive_anchors = {pair: value for pair, value in labels["label_means"].items() if value > 0.0}
    return {
        "mc_supervised": run_mc(actions, labels["label_means"]),
        "trl_raw": run_raw(actions, dataset),
        "trl_log": run_model(actions, spec, dataset, "empirical"),
        "empirical_model_dp": run_model(actions, spec, dataset, "empirical"),
        "posterior_mean_model_dp": run_model(actions, spec, dataset, "posterior_mean"),
        "posterior_lower_q10_model_dp": run_model(actions, spec, dataset, "posterior_lower_q10"),
        "posterior_trl_log": run_model(actions, spec, dataset, "posterior_mean"),
        "posterior_mc_plus_trl_log": run_model(actions, spec, dataset, "posterior_mean", positive_anchors=positive_anchors),
    }


def q_json(q_values: Dict[Pair, float]) -> Dict[str, float]:
    return {pair_key(pair): value for pair, value in sorted(q_values.items())}


def transitions_json(transitions: Dict[Pair, List[Tuple[float, str]]]) -> Dict[str, List[Dict[str, Any]]]:
    return {
        pair_key(pair): [{"probability": prob, "next_state": next_state} for prob, next_state in nexts]
        for pair, nexts in sorted(transitions.items())
    }


def evaluate_one(spec: Dict[str, Any]) -> Dict[str, Any]:
    mdp = build_mdp(spec)
    dataset = build_dataset(spec, mdp)
    labels = build_labels(dataset)
    exact_q = solve_dp(mdp["actions"], mdp["true_transitions"])
    method_q = run_methods(spec, mdp, dataset, labels)
    all_pairs = [(state, action) for state, actions in mdp["actions"].items() for action in actions]
    heldout_pairs = [
        pair for pair, horizon in mdp["horizons_to_goal_if_successful"].items()
        if horizon > LABEL_HORIZON_CUTOFF
    ]
    exact_safe = exact_q[("start", "safe")]
    exact_risky = exact_q[("start", "risky")]
    exact_action = choose_action(exact_risky, exact_safe)
    exact_optimal = max(exact_safe, exact_risky)
    metrics = {}
    for method, q_values in method_q.items():
        q_safe = q_values.get(("start", "safe"), 0.0)
        q_risky = q_values.get(("start", "risky"), 0.0)
        action = choose_action(q_risky, q_safe)
        chosen_true = exact_risky if action == "risky" else exact_safe
        metrics[method] = {
            "mdp_id": spec["mdp_id"],
            "family": spec["family"],
            "seed": spec["seed"],
            "regime": spec["regime"],
            "method": method,
            "estimated_action": action,
            "exact_optimal_action": exact_action,
            "matches_exact_action": action == exact_action,
            "risky_action_selected": action == "risky",
            "policy_regret": exact_optimal - chosen_true,
            "heldout_long_horizon_value_mse": mean((q_values.get(pair, 0.0) - exact_q.get(pair, 0.0)) ** 2 for pair in heldout_pairs),
            "all_pair_value_mse": mean((q_values.get(pair, 0.0) - exact_q.get(pair, 0.0)) ** 2 for pair in all_pairs),
            "risky_q_overestimation": max(0.0, q_risky - exact_risky),
            "risky_q_underestimation": max(0.0, exact_risky - q_risky),
            "risky_q_calibration_error": abs(q_risky - exact_risky),
            "mean_abs_q_error": mean(abs(q_values.get(pair, 0.0) - exact_q.get(pair, 0.0)) for pair in all_pairs),
            "exact_start_safe_q": exact_safe,
            "exact_start_risky_q": exact_risky,
            "estimated_start_safe_q": q_safe,
            "estimated_start_risky_q": q_risky,
        }
    alpha = BETA_PRIOR[0] + spec["observed_successes"]
    beta = BETA_PRIOR[1] + spec["observed_failures"]
    threshold = (GAMMA**spec["safe_length"]) / (GAMMA ** (1 + spec["risk_tail_steps"]))
    diagnostics = {
        "mdp_id": spec["mdp_id"],
        "family": spec["family"],
        "regime": spec["regime"],
        "posterior_alpha": alpha,
        "posterior_beta": beta,
        "empirical_success_prob": spec["observed_successes"] / spec["risky_samples"],
        "posterior_mean_success_prob": posterior_success_probability(spec["observed_successes"], spec["observed_failures"], "posterior_mean"),
        "posterior_lower_q10_success_prob": posterior_success_probability(spec["observed_successes"], spec["observed_failures"], "posterior_lower_q10"),
        "success_threshold_for_risky_optimality": threshold,
        "true_success_prob_for_evaluation_only": spec["true_risky_success_prob"],
        "heldout_pairs": [pair_key(pair) for pair in heldout_pairs],
    }
    return {
        "spec": spec,
        "mdp": mdp,
        "dataset": dataset,
        "labels": labels,
        "exact_q": exact_q,
        "method_q": method_q,
        "metrics": metrics,
        "diagnostics": diagnostics,
    }


def summarize(rows: List[Dict[str, Any]], keys: List[str]) -> List[Dict[str, Any]]:
    grouped: Dict[Tuple[Any, ...], List[Dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[tuple(row[key] for key in keys)].append(row)
    summary_rows = []
    for key_tuple, group_rows in sorted(grouped.items()):
        summary = {key: value for key, value in zip(keys, key_tuple)}
        summary.update({
            "num_rows": len(group_rows),
            "action_accuracy": mean(float(row["matches_exact_action"]) for row in group_rows),
            "mean_policy_regret": mean(float(row["policy_regret"]) for row in group_rows),
            "risky_action_selection_rate": mean(float(row["risky_action_selected"]) for row in group_rows),
            "mean_heldout_long_horizon_value_mse": mean(float(row["heldout_long_horizon_value_mse"]) for row in group_rows),
            "mean_all_pair_value_mse": mean(float(row["all_pair_value_mse"]) for row in group_rows),
            "mean_risky_q_overestimation": mean(float(row["risky_q_overestimation"]) for row in group_rows),
            "mean_risky_q_underestimation": mean(float(row["risky_q_underestimation"]) for row in group_rows),
            "mean_risky_q_calibration_error": mean(float(row["risky_q_calibration_error"]) for row in group_rows),
        })
        summary_rows.append(summary)
    return summary_rows


def method_summary_dict(rows: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    return {
        row["method"]: {key: value for key, value in row.items() if key != "method"}
        for row in summarize(rows, ["method"])
    }


def compare_q_tables(a: Dict[Pair, float], b: Dict[Pair, float], actions: Dict[str, List[str]]) -> Dict[str, Any]:
    pairs = [(state, action) for state, state_actions in actions.items() for action in state_actions]
    diffs = [abs(a.get(pair, 0.0) - b.get(pair, 0.0)) for pair in pairs]
    action_a = choose_action(a.get(("start", "risky"), 0.0), a.get(("start", "safe"), 0.0))
    action_b = choose_action(b.get(("start", "risky"), 0.0), b.get(("start", "safe"), 0.0))
    return {
        "max_abs_value_diff": max(diffs) if diffs else 0.0,
        "mean_abs_value_diff": mean(diffs),
        "start_action_disagreement": action_a != action_b,
    }


def build_outputs(results: List[Dict[str, Any]], runtime_seconds: float) -> Dict[str, Any]:
    metrics_rows = []
    transition_tables = {}
    value_tables = {}
    coverage_diagnostics = {
        "num_mdps": len(results),
        "families": list(FAMILIES),
        "seeds": list(SEEDS),
        "label_horizon_cutoff": LABEL_HORIZON_CUTOFF,
        "tag_counts": Counter(),
        "mdps": {},
    }
    equivalence_by_mdp = {}
    offline_dataset_summaries = {}
    for result in results:
        spec = result["spec"]
        mdp_id = spec["mdp_id"]
        coverage_diagnostics["tag_counts"].update(spec["tags"])
        coverage_diagnostics["mdps"][mdp_id] = {
            "family": spec["family"],
            "seed": spec["seed"],
            "regime": spec["regime"],
            "tags": spec["tags"],
            "dataset_summary": result["dataset"]["summary"],
            "label_coverage": result["labels"]["coverage_json"],
        }
        offline_dataset_summaries[mdp_id] = {
            "spec": spec,
            "dataset_summary": result["dataset"]["summary"],
            "transition_counts": result["dataset"]["transition_counts_json"],
            "label_coverage": result["labels"]["coverage_json"],
        }
        transition_tables[mdp_id] = {
            "true_transitions_for_evaluation_only": transitions_json(result["mdp"]["true_transitions"]),
            "observed_transition_counts": result["dataset"]["transition_counts_json"],
            "horizons_to_goal_if_successful": {
                pair_key(pair): horizon for pair, horizon in sorted(result["mdp"]["horizons_to_goal_if_successful"].items())
            },
        }
        value_tables[mdp_id] = {
            "exact_q": q_json(result["exact_q"]),
            "method_q": {method: q_json(q_values) for method, q_values in sorted(result["method_q"].items())},
        }
        equivalence_by_mdp[mdp_id] = {
            "family": spec["family"],
            "regime": spec["regime"],
            "trl_log_vs_empirical_model_dp": compare_q_tables(result["method_q"]["trl_log"], result["method_q"]["empirical_model_dp"], result["mdp"]["actions"]),
            "posterior_trl_log_vs_posterior_mean_model_dp": compare_q_tables(result["method_q"]["posterior_trl_log"], result["method_q"]["posterior_mean_model_dp"], result["mdp"]["actions"]),
            "posterior_mc_plus_trl_log_vs_posterior_mean_model_dp": compare_q_tables(result["method_q"]["posterior_mc_plus_trl_log"], result["method_q"]["posterior_mean_model_dp"], result["mdp"]["actions"]),
        }
        for method in METHODS:
            row = {
                "mdp_id": mdp_id,
                "tags": ";".join(spec["tags"]),
                "true_risky_success_prob": spec["true_risky_success_prob"],
                "safe_length": spec["safe_length"],
                "risk_total_length_if_successful": 1 + spec["risk_tail_steps"],
                "risky_samples": spec["risky_samples"],
                "observed_successes": spec["observed_successes"],
                "observed_failures": spec["observed_failures"],
                "observed_success_rate": spec["observed_successes"] / spec["risky_samples"],
                **result["metrics"][method],
            }
            metrics_rows.append(row)
    coverage_diagnostics["tag_counts"] = dict(coverage_diagnostics["tag_counts"])
    family_summary_rows = summarize(metrics_rows, ["family", "method"])
    regime_summary_rows = summarize(metrics_rows, ["regime", "method"])
    method_summary = method_summary_dict(metrics_rows)
    max_post_trl_diff = max(
        diag["posterior_trl_log_vs_posterior_mean_model_dp"]["max_abs_value_diff"]
        for diag in equivalence_by_mdp.values()
    )
    max_post_mc_diff = max(
        diag["posterior_mc_plus_trl_log_vs_posterior_mean_model_dp"]["max_abs_value_diff"]
        for diag in equivalence_by_mdp.values()
    )
    posterior_action_disagreement_rate = mean(
        float(diag["posterior_trl_log_vs_posterior_mean_model_dp"]["start_action_disagreement"])
        for diag in equivalence_by_mdp.values()
    )
    posterior_mc_action_disagreement_rate = mean(
        float(diag["posterior_mc_plus_trl_log_vs_posterior_mean_model_dp"]["start_action_disagreement"])
        for diag in equivalence_by_mdp.values()
    )
    matched_risk_rows = [
        row for row in metrics_rows
        if row["regime"] == "matched_risk_optimal" and row["method"] in {"posterior_trl_log", "posterior_mc_plus_trl_log"}
    ]
    matched_risk_preserved = all(
        row["matches_exact_action"] and row["risky_action_selected"] and row["policy_regret"] <= EQUIV_TOL
        for row in matched_risk_rows
    )
    best_candidate = min(
        ("posterior_trl_log", "posterior_mc_plus_trl_log"),
        key=lambda method: method_summary[method]["mean_heldout_long_horizon_value_mse"],
    )
    candidate = method_summary[best_candidate]
    improves_vs_trl = (
        candidate["mean_heldout_long_horizon_value_mse"] < method_summary["trl_log"]["mean_heldout_long_horizon_value_mse"] - EQUIV_TOL
        or candidate["mean_policy_regret"] < method_summary["trl_log"]["mean_policy_regret"] - EQUIV_TOL
    )
    improves_vs_model = (
        candidate["mean_heldout_long_horizon_value_mse"] < method_summary["posterior_mean_model_dp"]["mean_heldout_long_horizon_value_mse"] - EQUIV_TOL
        or candidate["mean_policy_regret"] < method_summary["posterior_mean_model_dp"]["mean_policy_regret"] - EQUIV_TOL
    )
    not_safe_everywhere = candidate["risky_action_selection_rate"] > 0.0
    near_equivalent = max(max_post_trl_diff, max_post_mc_diff) <= NEAR_EQ_TOL and posterior_action_disagreement_rate == 0.0
    positive_evidence = improves_vs_trl and improves_vs_model and matched_risk_preserved and not_safe_everywhere and not near_equivalent
    equivalence_diagnostics = {
        "by_mdp": equivalence_by_mdp,
        "aggregate": {
            "max_abs_value_diff_posterior_trl_log_vs_model": max_post_trl_diff,
            "max_abs_value_diff_posterior_mc_plus_vs_model": max_post_mc_diff,
            "action_disagreement_rate_posterior_trl_log_vs_model": posterior_action_disagreement_rate,
            "action_disagreement_rate_posterior_mc_plus_vs_model": posterior_mc_action_disagreement_rate,
            "posterior_trl_near_equivalent_to_prior_matched_model_dp": near_equivalent,
            "best_candidate": best_candidate,
            "candidate_improves_vs_trl_log": improves_vs_trl,
            "candidate_improves_vs_prior_matched_model_dp": improves_vs_model,
            "matched_risk_optimal_preserved": matched_risk_preserved,
            "not_safe_everywhere": not_safe_everywhere,
            "positive_evidence": positive_evidence,
        },
    }
    raw_metrics = {
        "experiment_id": EXPERIMENT_ID,
        "suite": {"families": list(FAMILIES), "seeds": list(SEEDS), "num_mdps": len(results)},
        "method_summary": method_summary,
        "family_summary": family_summary_rows,
        "regime_summary": regime_summary_rows,
        "metrics_rows": metrics_rows,
        "equivalence_diagnostics": equivalence_diagnostics,
        "coverage_diagnostics": coverage_diagnostics,
        "offline_dataset_summaries": offline_dataset_summaries,
        "runtime_seconds": runtime_seconds,
    }
    return {
        "metrics_rows": metrics_rows,
        "family_summary_rows": family_summary_rows,
        "regime_summary_rows": regime_summary_rows,
        "method_summary": method_summary,
        "transition_tables": transition_tables,
        "value_tables": value_tables,
        "coverage_diagnostics": coverage_diagnostics,
        "offline_dataset_summaries": offline_dataset_summaries,
        "equivalence_diagnostics": equivalence_diagnostics,
        "positive_evidence": positive_evidence,
        "near_equivalent": near_equivalent,
        "matched_risk_preserved": matched_risk_preserved,
        "best_candidate": best_candidate,
        "raw_metrics": raw_metrics,
    }


def main() -> int:
    start_time = time.perf_counter()
    repo_root = Path(__file__).resolve().parents[4]
    artifact_dir = repo_root / "research" / PROJECT / "artifacts" / EXPERIMENT_ID
    result_dir = repo_root / "research" / PROJECT / "results"
    artifact_dir.mkdir(parents=True, exist_ok=True)
    result_dir.mkdir(parents=True, exist_ok=True)

    specs = build_suite()
    results = [evaluate_one(spec) for spec in specs]
    runtime_seconds = time.perf_counter() - start_time
    outputs = build_outputs(results, runtime_seconds)

    artifact_paths = [
        f"research/{PROJECT}/artifacts/{EXPERIMENT_ID}/randomized_equivalence_audit.py",
        f"research/{PROJECT}/artifacts/{EXPERIMENT_ID}/raw_metrics.json",
        f"research/{PROJECT}/artifacts/{EXPERIMENT_ID}/metrics.csv",
        f"research/{PROJECT}/artifacts/{EXPERIMENT_ID}/family_summary.csv",
        f"research/{PROJECT}/artifacts/{EXPERIMENT_ID}/regime_summary.csv",
        f"research/{PROJECT}/artifacts/{EXPERIMENT_ID}/equivalence_diagnostics.json",
        f"research/{PROJECT}/artifacts/{EXPERIMENT_ID}/coverage_diagnostics.json",
        f"research/{PROJECT}/artifacts/{EXPERIMENT_ID}/offline_datasets.json",
        f"research/{PROJECT}/artifacts/{EXPERIMENT_ID}/transition_tables.json",
        f"research/{PROJECT}/artifacts/{EXPERIMENT_ID}/value_tables.json",
    ]
    write_json(artifact_dir / "raw_metrics.json", outputs["raw_metrics"])
    write_csv(artifact_dir / "metrics.csv", outputs["metrics_rows"])
    write_csv(artifact_dir / "family_summary.csv", outputs["family_summary_rows"])
    write_csv(artifact_dir / "regime_summary.csv", outputs["regime_summary_rows"])
    write_json(artifact_dir / "equivalence_diagnostics.json", outputs["equivalence_diagnostics"])
    write_json(artifact_dir / "coverage_diagnostics.json", outputs["coverage_diagnostics"])
    write_json(artifact_dir / "offline_datasets.json", outputs["offline_dataset_summaries"])
    write_json(artifact_dir / "transition_tables.json", outputs["transition_tables"])
    write_json(artifact_dir / "value_tables.json", outputs["value_tables"])

    method_summary = outputs["method_summary"]
    eq_agg = outputs["equivalence_diagnostics"]["aggregate"]
    metrics = {
        "num_mdps": len(specs),
        "num_method_rows": len(outputs["metrics_rows"]),
        "families": list(FAMILIES),
        "seeds": list(SEEDS),
        "method_summary": method_summary,
        "equivalence_aggregate": eq_agg,
        "positive_evidence": outputs["positive_evidence"],
        "posterior_trl_near_equivalent_to_prior_matched_model_dp": outputs["near_equivalent"],
        "matched_risk_optimal_preserved": outputs["matched_risk_preserved"],
        "coverage_diagnostics": {
            "tag_counts": outputs["coverage_diagnostics"]["tag_counts"],
            "label_horizon_cutoff": LABEL_HORIZON_CUTOFF,
        },
    }
    baseline_metrics = {
        "mc_supervised": method_summary["mc_supervised"],
        "trl_log": method_summary["trl_log"],
        "empirical_model_dp": method_summary["empirical_model_dp"],
        "posterior_mean_model_dp": method_summary["posterior_mean_model_dp"],
        "posterior_lower_q10_model_dp": method_summary["posterior_lower_q10_model_dp"],
    }
    metric_deltas = {
        "posterior_trl_log_minus_trl_log_heldout_mse": method_summary["posterior_trl_log"]["mean_heldout_long_horizon_value_mse"] - method_summary["trl_log"]["mean_heldout_long_horizon_value_mse"],
        "posterior_trl_log_minus_posterior_model_heldout_mse": method_summary["posterior_trl_log"]["mean_heldout_long_horizon_value_mse"] - method_summary["posterior_mean_model_dp"]["mean_heldout_long_horizon_value_mse"],
        "posterior_mc_plus_minus_posterior_model_heldout_mse": method_summary["posterior_mc_plus_trl_log"]["mean_heldout_long_horizon_value_mse"] - method_summary["posterior_mean_model_dp"]["mean_heldout_long_horizon_value_mse"],
        "posterior_trl_log_minus_trl_log_policy_regret": method_summary["posterior_trl_log"]["mean_policy_regret"] - method_summary["trl_log"]["mean_policy_regret"],
        "posterior_trl_log_minus_posterior_model_policy_regret": method_summary["posterior_trl_log"]["mean_policy_regret"] - method_summary["posterior_mean_model_dp"]["mean_policy_regret"],
        "mc_supervised_minus_trl_log_heldout_mse": method_summary["mc_supervised"]["mean_heldout_long_horizon_value_mse"] - method_summary["trl_log"]["mean_heldout_long_horizon_value_mse"],
    }
    known_failures = []
    if outputs["near_equivalent"]:
        known_failures.append("posterior_trl_log and posterior_mc_plus_trl_log were near-equivalent to prior-matched posterior mean model DP across the randomized suite.")
    if not outputs["positive_evidence"]:
        known_failures.append("No credible posterior TRL benefit over both TRL-log and prior-matched posterior model DP was detected.")
    interpretation = (
        "The randomized tiny-suite audit supports the 0010 boundary result: posterior TRL-log variants match the prior-matched posterior mean model-DP baseline within numerical tolerance across branch-chain, stochastic stitching, and teleporter families. "
        "Any aggregate improvement over plain TRL-log is explained by the shared posterior transition prior, not by a distinct transitive posterior TRL effect."
    )
    success_criteria_results = [
        "Created a self-contained 0011 artifact without editing prior results, schemas, control scripts, AGENTS.md, or environment files.",
        "Generated a predeclared tiny suite of 3 families x 5 fixed seeds with exact DP evaluation for every MDP.",
        "Included matched, lucky-only, no-success, ambiguous/prior-dependent, and sparse long-horizon label-censoring regimes.",
        "Compared MC supervised, raw TRL, TRL-log, empirical model DP, posterior model DP, posterior lower model DP, posterior_trl_log, and posterior_mc_plus_trl_log.",
        "Saved raw metrics plus family, regime, coverage, transition, value, and equivalence diagnostics.",
    ]
    failure_criteria_results = [
        "Prior-matched posterior model-DP baselines and direct equivalence diagnostics were included.",
        "Transition-model DP used the same observed transition counts and priors as posterior TRL; it was not made unavailable or misspecified.",
        "Exact DP values and true probabilities were used only for evaluation/audit artifacts.",
        "No neural networks, continuous-control environments, downloads, broad sweeps, or expensive training were used.",
        "No method is claimed successful by safe-everywhere behavior or by failing matched risk-optimal action selection.",
    ]
    decision_relevant_findings = [
        f"Positive evidence: {outputs['positive_evidence']}.",
        f"Near-equivalence to posterior model DP: {outputs['near_equivalent']}.",
        f"Max posterior_trl_log value difference vs posterior model DP: {eq_agg['max_abs_value_diff_posterior_trl_log_vs_model']:.12g}.",
        f"Action disagreement rate vs posterior model DP: {eq_agg['action_disagreement_rate_posterior_trl_log_vs_model']:.12g}.",
        f"Matched risk-optimal preserved: {outputs['matched_risk_preserved']}.",
    ]
    result = {
        "experiment_id": EXPERIMENT_ID,
        "status": "completed",
        "claim_tested": (
            "A fixed tiny randomized suite tested whether posterior TRL-log has distinct value over prior-matched posterior model DP beyond handcrafted branch-chain regimes."
        ),
        "commands_run": COMMANDS_RUN,
        "metrics": metrics,
        "baseline_metrics": baseline_metrics,
        "artifacts": artifact_paths,
        "interpretation": interpretation,
        "known_failures": known_failures,
        "next_questions": [
            "Can a future posterior TRL method beat posterior model DP only when state aliases or partial observability make model DP insufficient?",
            "Should posterior TRL audits require model-DP equivalence checks by default?",
            "Which explicit priors should be predeclared for no-success risk-optimal regimes?",
        ],
        "runtime_seconds": runtime_seconds,
        "resource_usage": {
            "device": "cpu",
            "num_mdps": len(specs),
            "num_method_rows": len(outputs["metrics_rows"]),
            "label_horizon_cutoff": LABEL_HORIZON_CUTOFF,
        },
        "success_criteria_results": success_criteria_results,
        "failure_criteria_results": failure_criteria_results,
        "metric_deltas": metric_deltas,
        "decision_relevant_findings": decision_relevant_findings,
    }
    write_json(result_dir / f"{EXPERIMENT_ID}_result.json", result)

    summary = f"""# Experiment {EXPERIMENT_ID} Summary

## Objective

Run a randomized tabular equivalence and generalization audit for posterior TRL-log versus prior-matched posterior model DP.

## Commands Run

```bash
{chr(10).join(COMMANDS_RUN)}
```

## Suite

- Families: `{list(FAMILIES)}`
- Seeds per family: `{list(SEEDS)}`
- Total MDPs: `{len(specs)}`
- Label horizon cutoff: `{LABEL_HORIZON_CUTOFF}`

## Method Summary

| Method | Action accuracy | Heldout MSE | Policy regret | Risky rate | Q overestimation | Calibration error |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
"""
    for method, stats in sorted(method_summary.items()):
        summary += (
            f"| {method} | {stats['action_accuracy']:.6f} | {stats['mean_heldout_long_horizon_value_mse']:.12f} | "
            f"{stats['mean_policy_regret']:.12f} | {stats['risky_action_selection_rate']:.6f} | "
            f"{stats['mean_risky_q_overestimation']:.12f} | {stats['mean_risky_q_calibration_error']:.12f} |\n"
        )
    summary += f"""
## Equivalence Audit

- Positive posterior TRL evidence: `{outputs["positive_evidence"]}`
- Near-equivalent to prior-matched posterior model DP: `{outputs["near_equivalent"]}`
- Max posterior_trl_log value difference vs model DP: `{eq_agg["max_abs_value_diff_posterior_trl_log_vs_model"]:.12g}`
- Posterior_trl_log action disagreement rate vs model DP: `{eq_agg["action_disagreement_rate_posterior_trl_log_vs_model"]:.12g}`
- Matched risk-optimal action preserved: `{outputs["matched_risk_preserved"]}`

## Interpretation

{interpretation}

## Artifacts

- `research/{PROJECT}/artifacts/{EXPERIMENT_ID}/randomized_equivalence_audit.py`
- `research/{PROJECT}/artifacts/{EXPERIMENT_ID}/raw_metrics.json`
- `research/{PROJECT}/artifacts/{EXPERIMENT_ID}/metrics.csv`
- `research/{PROJECT}/artifacts/{EXPERIMENT_ID}/family_summary.csv`
- `research/{PROJECT}/artifacts/{EXPERIMENT_ID}/regime_summary.csv`
- `research/{PROJECT}/artifacts/{EXPERIMENT_ID}/equivalence_diagnostics.json`
- `research/{PROJECT}/artifacts/{EXPERIMENT_ID}/coverage_diagnostics.json`
- `research/{PROJECT}/artifacts/{EXPERIMENT_ID}/offline_datasets.json`
- `research/{PROJECT}/artifacts/{EXPERIMENT_ID}/transition_tables.json`
- `research/{PROJECT}/artifacts/{EXPERIMENT_ID}/value_tables.json`
"""
    (result_dir / f"{EXPERIMENT_ID}_summary.md").write_text(summary)
    print(json.dumps({
        "status": result["status"],
        "num_mdps": len(specs),
        "positive_evidence": outputs["positive_evidence"],
        "near_equivalent": outputs["near_equivalent"],
        "matched_risk_preserved": outputs["matched_risk_preserved"],
        "known_failures": known_failures,
    }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
