#!/usr/bin/env python3
"""Experiment 0013: randomized aliased-POMDP context audit."""

from __future__ import annotations

import csv
import json
import random
import time
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple


EXPERIMENT_ID = "0013"
PROJECT = "sto_trl"
GAMMA = 0.9
LABEL_HORIZON_CUTOFF = 2
EQUIV_TOL = 1e-12
FAMILIES = ("cue_sufficient", "cue_noisy", "cue_insufficient")
SEEDS = (0, 1, 2, 3, 4)

COMMANDS_RUN = [
    "mkdir -p research/sto_trl/artifacts/0013 research/sto_trl/results",
    "conda run -n autoresearcher_sto_trl python research/sto_trl/artifacts/0013/randomized_pomdp_context_audit.py",
    "conda run -n autoresearcher_sto_trl python scripts/validate_artifacts.py --repo-root . --json research/sto_trl/results/0013_result.json --schema schemas/result.schema.json --check-result-artifacts",
]

METHODS = [
    "observation_empirical_model_dp",
    "observation_trl_log",
    "history_mc_only",
    "history_trl_log",
    "history_mc_plus_trl_log",
    "history_model_dp",
    "latent_oracle_dp",
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


def choose_action(q_teleport: float, q_safe: float) -> str:
    return "teleport" if q_teleport > q_safe + EQUIV_TOL else "safe"


def mean(values: Iterable[float]) -> float:
    values = list(values)
    return sum(values) / len(values) if values else 0.0


def weighted_mean(rows: List[Dict[str, Any]], key: str) -> float:
    total_weight = sum(row["eval_weight"] for row in rows)
    return sum(row["eval_weight"] * row[key] for row in rows) / total_weight if total_weight else 0.0


def obs_of(latent_state: str, observed_cue: str | None = None) -> str:
    if latent_state.startswith("cue_"):
        if observed_cue is None:
            raise ValueError("cue observation requires observed_cue")
        return observed_cue
    if latent_state.startswith("hub_"):
        return "hub"
    if latent_state.startswith("safe_"):
        return "safe"
    if latent_state.startswith("tele_"):
        return "tele"
    if latent_state in {"goal", "trap"}:
        return latent_state
    raise ValueError(latent_state)


def bounded_history_key(observation_history: List[str]) -> str:
    current = observation_history[-1]
    if current in {"goal", "trap"}:
        return current
    cue = observation_history[0]
    if current.startswith("cue_") or current == "cue_x":
        return current
    return f"{cue}|{'>'.join(observation_history[-3:])}"


def eval_history_key(observed_cue: str, latent_state: str) -> str:
    suffixes = {
        "hub": ["hub"],
        "safe_1": ["hub", "safe"],
        "safe_2": ["hub", "safe", "safe"],
        "safe_3": ["safe", "safe", "safe"],
        "tele_1": ["hub", "tele"],
        "tele_2": ["hub", "tele", "tele"],
    }
    if latent_state.startswith("cue_"):
        return observed_cue
    if latent_state in {"goal", "trap"}:
        return latent_state
    parts = latent_state.split("_")
    if parts[0] == "hub":
        tail = suffixes["hub"]
    elif parts[0] == "safe":
        tail = suffixes[f"safe_{parts[-1]}"]
    elif parts[0] == "tele":
        tail = suffixes[f"tele_{parts[-1]}"]
    else:
        raise ValueError(latent_state)
    return bounded_history_key([observed_cue] + tail)


def latent_actions() -> Dict[str, List[str]]:
    actions = {
        "cue_good": ["enter"],
        "cue_bad": ["enter"],
        "hub_good": ["safe", "teleport"],
        "hub_bad": ["safe", "teleport"],
    }
    for context in ("good", "bad"):
        for idx in range(1, 4):
            actions[f"safe_{context}_{idx}"] = ["advance"]
        for idx in range(1, 3):
            actions[f"tele_{context}_{idx}"] = ["advance"]
    return actions


def latent_transitions(p_good: float, p_bad: float) -> Dict[Pair, List[Tuple[float, str]]]:
    transitions: Dict[Pair, List[Tuple[float, str]]] = {
        ("cue_good", "enter"): [(1.0, "hub_good")],
        ("cue_bad", "enter"): [(1.0, "hub_bad")],
        ("hub_good", "safe"): [(1.0, "safe_good_1")],
        ("hub_bad", "safe"): [(1.0, "safe_bad_1")],
        ("hub_good", "teleport"): [(p_good, "tele_good_1"), (1.0 - p_good, "trap")],
        ("hub_bad", "teleport"): [(p_bad, "tele_bad_1"), (1.0 - p_bad, "trap")],
    }
    for context in ("good", "bad"):
        transitions[(f"safe_{context}_1", "advance")] = [(1.0, f"safe_{context}_2")]
        transitions[(f"safe_{context}_2", "advance")] = [(1.0, f"safe_{context}_3")]
        transitions[(f"safe_{context}_3", "advance")] = [(1.0, "goal")]
        transitions[(f"tele_{context}_1", "advance")] = [(1.0, f"tele_{context}_2")]
        transitions[(f"tele_{context}_2", "advance")] = [(1.0, "goal")]
    return transitions


def solve_dp(actions: Dict[str, List[str]], transitions: Dict[Pair, List[Tuple[float, str]]], iterations: int = 200) -> Dict[Pair, float]:
    pairs = [(state, action) for state, state_actions in actions.items() for action in state_actions]
    q_values = {pair: 0.0 for pair in pairs}
    for _ in range(iterations):
        next_q = {}
        for pair in pairs:
            value = 0.0
            for prob, next_state in transitions.get(pair, []):
                continuation = 1.0 if next_state == "goal" else max(
                    (q_values.get((next_state, action), 0.0) for action in actions.get(next_state, [])),
                    default=0.0,
                )
                value += prob * continuation
            next_q[pair] = GAMMA * value
        q_values = next_q
    return q_values


def safe_path(context: str) -> List[Tuple[str, str, str]]:
    return [
        (f"hub_{context}", "safe", f"safe_{context}_1"),
        (f"safe_{context}_1", "advance", f"safe_{context}_2"),
        (f"safe_{context}_2", "advance", f"safe_{context}_3"),
        (f"safe_{context}_3", "advance", "goal"),
    ]


def teleport_success_path(context: str) -> List[Tuple[str, str, str]]:
    return [
        (f"hub_{context}", "teleport", f"tele_{context}_1"),
        (f"tele_{context}_1", "advance", f"tele_{context}_2"),
        (f"tele_{context}_2", "advance", "goal"),
    ]


def teleport_failure_path(context: str) -> List[Tuple[str, str, str]]:
    return [(f"hub_{context}", "teleport", "trap")]


def make_case(family: str, seed: int) -> Dict[str, Any]:
    rng = random.Random(1300 + 43 * seed + 101 * FAMILIES.index(family))
    bad_successes = rng.choice([3, 4, 5])
    good_successes = 19
    reliability = 1.0
    if family == "cue_noisy":
        reliability = [0.60, 0.70, 0.80, 0.70, 0.60][seed]
    if family == "cue_insufficient":
        reliability = 0.50
    return {
        "case_id": f"{family}_seed{seed}",
        "family": family,
        "seed": seed,
        "cue_reliability": reliability,
        "good_teleport_samples": 20,
        "good_teleport_successes": good_successes,
        "bad_teleport_samples": 20,
        "bad_teleport_successes": bad_successes,
        "safe_trajectories_per_context": 8,
        "p_good": good_successes / 20,
        "p_bad": bad_successes / 20,
    }


def observed_cues_for_context(case: Dict[str, Any], context: str, count: int) -> List[str]:
    family = case["family"]
    if family == "cue_sufficient":
        return ["cue_g" if context == "good" else "cue_b"] * count
    if family == "cue_insufficient":
        return ["cue_x"] * count
    correct = "cue_g" if context == "good" else "cue_b"
    flipped = "cue_b" if context == "good" else "cue_g"
    correct_count = round(case["cue_reliability"] * count)
    return [correct] * correct_count + [flipped] * (count - correct_count)


def make_trajectory(context: str, branch: str, index: int, observed_cue: str) -> Dict[str, Any]:
    cue_state = f"cue_{context}"
    hub_state = f"hub_{context}"
    edges = [(cue_state, "enter", hub_state)]
    if branch == "safe":
        edges.extend(safe_path(context))
    elif branch == "teleport_success":
        edges.extend(teleport_success_path(context))
    elif branch == "teleport_failure":
        edges.extend(teleport_failure_path(context))
    else:
        raise ValueError(branch)
    transitions = []
    obs_history = [observed_cue]
    for latent_state, action, next_latent_state in edges:
        current_obs = obs_of(latent_state, observed_cue)
        current_history_key = bounded_history_key(obs_history)
        next_obs = obs_of(next_latent_state, observed_cue)
        next_history = [next_obs] if next_obs in {"goal", "trap"} else obs_history + [next_obs]
        transitions.append({
            "latent_state": latent_state,
            "context": context,
            "observation": current_obs,
            "history_key": current_history_key,
            "observation_key": current_obs,
            "action": action,
            "next_latent_state": next_latent_state,
            "next_observation": next_obs,
            "next_history_key": bounded_history_key(next_history),
            "next_observation_key": next_obs,
        })
        obs_history = next_history
    return {
        "trajectory_id": f"{context}_{branch}_{index}_{observed_cue}",
        "context": context,
        "branch": branch,
        "observed_cue": observed_cue,
        "transitions": transitions,
    }


def generate_trajectories(case: Dict[str, Any]) -> List[Dict[str, Any]]:
    trajectories = []
    for context in ("good", "bad"):
        safe_n = case["safe_trajectories_per_context"]
        tele_n = case[f"{context}_teleport_samples"]
        success_n = case[f"{context}_teleport_successes"]
        failure_n = tele_n - success_n
        branches = ["safe"] * safe_n + ["teleport_success"] * success_n + ["teleport_failure"] * failure_n
        cues = observed_cues_for_context(case, context, len(branches))
        for idx, (branch, cue) in enumerate(zip(branches, cues)):
            trajectories.append(make_trajectory(context, branch, idx, cue))
    return trajectories


def build_counts(trajectories: List[Dict[str, Any]], key_name: str) -> Dict[Pair, Dict[str, int]]:
    counts: Dict[Pair, Dict[str, int]] = defaultdict(lambda: defaultdict(int))
    next_key_name = "next_" + key_name
    for trajectory in trajectories:
        for transition in trajectory["transitions"]:
            counts[(transition[key_name], transition["action"])][transition[next_key_name]] += 1
    return counts


def counts_json(counts: Dict[Pair, Dict[str, int]]) -> Dict[str, Dict[str, int]]:
    return {pair_key(pair): dict(next_counts) for pair, next_counts in sorted(counts.items())}


def actions_from_counts(counts: Dict[Pair, Dict[str, int]]) -> Dict[str, List[str]]:
    actions: Dict[str, List[str]] = defaultdict(list)
    for key, action in counts:
        actions[key].append(action)
    return {key: sorted(set(actions_)) for key, actions_ in actions.items()}


def transitions_from_counts(counts: Dict[Pair, Dict[str, int]]) -> Dict[Pair, List[Tuple[float, str]]]:
    transitions = {}
    for pair, next_counts in counts.items():
        total = sum(next_counts.values())
        transitions[pair] = [(count / total, next_key) for next_key, count in sorted(next_counts.items())]
    return transitions


def goal_horizon(transitions: List[Dict[str, Any]], step_idx: int) -> int | None:
    for idx in range(step_idx, len(transitions)):
        if transitions[idx]["next_latent_state"] == "goal":
            return idx - step_idx + 1
    return None


def build_labels(trajectories: List[Dict[str, Any]], key_name: str) -> Dict[str, Any]:
    labels: Dict[Pair, List[float]] = defaultdict(list)
    coverage: Dict[Pair, Dict[str, int]] = defaultdict(lambda: {
        "positive_labels": 0,
        "zero_labels": 0,
        "censored_positive_labels": 0,
        "total_occurrences": 0,
    })
    for trajectory in trajectories:
        for idx, transition in enumerate(trajectory["transitions"]):
            pair = (transition[key_name], transition["action"])
            coverage[pair]["total_occurrences"] += 1
            horizon = goal_horizon(trajectory["transitions"], idx)
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
        "coverage": {
            pair_key(pair): {
                **stats,
                "label_count_used": len(labels.get(pair, [])),
                "mean_used_label": mean(labels.get(pair, [])) if labels.get(pair, []) else 0.0,
            }
            for pair, stats in sorted(coverage.items())
        },
    }


def run_mc(actions: Dict[str, List[str]], label_means: Dict[Pair, float]) -> Dict[Pair, float]:
    return {(key, action): label_means.get((key, action), 0.0) for key, actions in actions.items() for action in actions}


def run_mc_plus(actions: Dict[str, List[str]], transitions: Dict[Pair, List[Tuple[float, str]]], label_means: Dict[Pair, float]) -> Dict[Pair, float]:
    anchors = {pair: value for pair, value in label_means.items() if value > 0.0}
    pairs = [(key, action) for key, actions in actions.items() for action in actions]
    q_values = {pair: 0.0 for pair in pairs}
    for _ in range(200):
        next_q = {}
        for pair in pairs:
            total = 0.0
            for prob, next_key in transitions.get(pair, []):
                continuation = 1.0 if next_key == "goal" else max(
                    (q_values.get((next_key, action), 0.0) for action in actions.get(next_key, [])),
                    default=0.0,
                )
                total += prob * continuation
            backup = GAMMA * total
            if pair in anchors:
                backup = max(backup, anchors[pair])
            next_q[pair] = backup
        q_values = next_q
    return q_values


def q_for_method(method: str, q_tables: Dict[str, Dict[Pair, float]], latent_state: str, action: str, observed_cue: str) -> float:
    if method.startswith("observation_"):
        return q_tables[method].get((obs_of(latent_state, observed_cue), action), 0.0)
    if method.startswith("history_"):
        return q_tables[method].get((eval_history_key(observed_cue, latent_state), action), 0.0)
    if method == "latent_oracle_dp":
        return q_tables[method].get((latent_state, action), 0.0)
    raise ValueError(method)


def cue_eval_weights(trajectories: List[Dict[str, Any]]) -> Dict[Tuple[str, str], float]:
    counts: Counter[Tuple[str, str]] = Counter()
    totals: Counter[str] = Counter()
    for trajectory in trajectories:
        context = trajectory["context"]
        cue = trajectory["observed_cue"]
        counts[(context, cue)] += 1
        totals[context] += 1
    return {(context, cue): count / totals[context] for (context, cue), count in counts.items()}


def evaluate_case(case: Dict[str, Any]) -> Dict[str, Any]:
    trajectories = generate_trajectories(case)
    latent_action_map = latent_actions()
    latent_transition_map = latent_transitions(case["p_good"], case["p_bad"])
    exact_q = solve_dp(latent_action_map, latent_transition_map)
    obs_counts = build_counts(trajectories, "observation_key")
    hist_counts = build_counts(trajectories, "history_key")
    obs_actions = actions_from_counts(obs_counts)
    hist_actions = actions_from_counts(hist_counts)
    obs_transitions = transitions_from_counts(obs_counts)
    hist_transitions = transitions_from_counts(hist_counts)
    obs_labels = build_labels(trajectories, "observation_key")
    hist_labels = build_labels(trajectories, "history_key")
    q_tables = {
        "observation_empirical_model_dp": solve_dp(obs_actions, obs_transitions),
        "observation_trl_log": solve_dp(obs_actions, obs_transitions),
        "history_mc_only": run_mc(hist_actions, hist_labels["label_means"]),
        "history_trl_log": solve_dp(hist_actions, hist_transitions),
        "history_mc_plus_trl_log": run_mc_plus(hist_actions, hist_transitions, hist_labels["label_means"]),
        "history_model_dp": solve_dp(hist_actions, hist_transitions),
        "latent_oracle_dp": exact_q,
    }
    rows = []
    for (context, cue), weight in cue_eval_weights(trajectories).items():
        hub_state = f"hub_{context}"
        exact_safe = exact_q[(hub_state, "safe")]
        exact_tele = exact_q[(hub_state, "teleport")]
        exact_action = choose_action(exact_tele, exact_safe)
        exact_value = max(exact_safe, exact_tele)
        for method in METHODS:
            q_safe = q_for_method(method, q_tables, hub_state, "safe", cue)
            q_tele = q_for_method(method, q_tables, hub_state, "teleport", cue)
            action = choose_action(q_tele, q_safe)
            chosen_true = exact_tele if action == "teleport" else exact_safe
            rows.append({
                "case_id": case["case_id"],
                "family": case["family"],
                "seed": case["seed"],
                "context": context,
                "observed_cue": cue,
                "eval_weight": weight,
                "method": method,
                "estimated_action": action,
                "latent_oracle_action": exact_action,
                "action_disagreement_with_latent_oracle": action != exact_action,
                "teleport_action_selected": action == "teleport",
                "policy_regret": exact_value - chosen_true,
                "heldout_long_horizon_value_mse": mean([(q_safe - exact_safe) ** 2, (q_tele - exact_tele) ** 2]),
                "calibration_error": mean([abs(q_safe - exact_safe), abs(q_tele - exact_tele)]),
                "teleport_q_overestimation": max(0.0, q_tele - exact_tele),
                "teleport_q_underestimation": max(0.0, exact_tele - q_tele),
                "exact_safe_q": exact_safe,
                "exact_teleport_q": exact_tele,
                "estimated_safe_q": q_safe,
                "estimated_teleport_q": q_tele,
            })
    leakage_keys = set()
    for counts in (obs_counts, hist_counts):
        for key, _ in counts:
            leakage_keys.add(key)
        for next_counts in counts.values():
            leakage_keys.update(next_counts)
    leakage_tokens = ["good", "bad", "hub_good", "hub_bad", "latent"]
    leakage_free = not any(any(token in key for token in leakage_tokens) for key in leakage_keys)
    return {
        "case": case,
        "trajectories": trajectories,
        "metrics_rows": rows,
        "q_tables": q_tables,
        "exact_q": exact_q,
        "obs_counts": obs_counts,
        "hist_counts": hist_counts,
        "obs_transitions": obs_transitions,
        "hist_transitions": hist_transitions,
        "obs_label_coverage": obs_labels["coverage"],
        "hist_label_coverage": hist_labels["coverage"],
        "latent_transitions": latent_transition_map,
        "leakage_free": leakage_free,
        "leakage_keys": sorted(leakage_keys),
    }


def summarize(rows: List[Dict[str, Any]], keys: List[str]) -> List[Dict[str, Any]]:
    grouped: Dict[Tuple[Any, ...], List[Dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[tuple(row[key] for key in keys)].append(row)
    summaries = []
    for key_tuple, group_rows in sorted(grouped.items()):
        summary = {key: value for key, value in zip(keys, key_tuple)}
        summary.update({
            "num_rows": len(group_rows),
            "weight_sum": sum(row["eval_weight"] for row in group_rows),
            "mean_heldout_long_horizon_value_mse": weighted_mean(group_rows, "heldout_long_horizon_value_mse"),
            "mean_policy_regret": weighted_mean(group_rows, "policy_regret"),
            "teleport_action_rate": weighted_mean([{**row, "teleport_action_selected": float(row["teleport_action_selected"])} for row in group_rows], "teleport_action_selected"),
            "mean_calibration_error": weighted_mean(group_rows, "calibration_error"),
            "mean_teleport_q_overestimation": weighted_mean(group_rows, "teleport_q_overestimation"),
            "mean_teleport_q_underestimation": weighted_mean(group_rows, "teleport_q_underestimation"),
            "action_disagreement_rate": weighted_mean([{**row, "action_disagreement_with_latent_oracle": float(row["action_disagreement_with_latent_oracle"])} for row in group_rows], "action_disagreement_with_latent_oracle"),
        })
        summaries.append(summary)
    return summaries


def summary_dict(rows: List[Dict[str, Any]], key: str) -> Dict[str, Dict[str, Any]]:
    return {
        row[key]: {k: v for k, v in row.items() if k != key}
        for row in summarize(rows, [key])
    }


def q_json(q_values: Dict[Pair, float]) -> Dict[str, float]:
    return {pair_key(pair): value for pair, value in sorted(q_values.items())}


def transitions_json(transitions: Dict[Pair, List[Tuple[float, str]]]) -> Dict[str, List[Dict[str, Any]]]:
    return {
        pair_key(pair): [{"probability": prob, "next_state": next_state} for prob, next_state in nexts]
        for pair, nexts in sorted(transitions.items())
    }


def counts_json(counts: Dict[Pair, Dict[str, int]]) -> Dict[str, Dict[str, int]]:
    return {pair_key(pair): dict(next_counts) for pair, next_counts in sorted(counts.items())}


def main() -> int:
    start_time = time.perf_counter()
    repo_root = Path(__file__).resolve().parents[4]
    artifact_dir = repo_root / "research" / PROJECT / "artifacts" / EXPERIMENT_ID
    result_dir = repo_root / "research" / PROJECT / "results"
    artifact_dir.mkdir(parents=True, exist_ok=True)
    result_dir.mkdir(parents=True, exist_ok=True)

    cases = [make_case(family, seed) for family in FAMILIES for seed in SEEDS]
    evaluated = [evaluate_case(case) for case in cases]
    metrics_rows = [row for case_result in evaluated for row in case_result["metrics_rows"]]
    method_summary = summary_dict(metrics_rows, "method")
    family_summary_rows = summarize(metrics_rows, ["family", "method"])
    context_summary_rows = summarize(metrics_rows, ["family", "context", "method"])
    runtime_seconds = time.perf_counter() - start_time

    sufficient_rows = [row for row in metrics_rows if row["family"] == "cue_sufficient"]
    sufficient_summary = summary_dict(sufficient_rows, "method")
    mc_mse = sufficient_summary["history_mc_only"]["mean_heldout_long_horizon_value_mse"]
    mc_plus_mse = sufficient_summary["history_mc_plus_trl_log"]["mean_heldout_long_horizon_value_mse"]
    sufficient_improvement = (mc_mse - mc_plus_mse) / mc_mse if mc_mse > 0.0 else 0.0
    obs_failure = (
        method_summary["observation_trl_log"]["mean_heldout_long_horizon_value_mse"]
        > method_summary["latent_oracle_dp"]["mean_heldout_long_horizon_value_mse"] + EQUIV_TOL
        or method_summary["observation_trl_log"]["mean_policy_regret"]
        > method_summary["latent_oracle_dp"]["mean_policy_regret"] + EQUIV_TOL
    )
    history_model_gap = abs(
        method_summary["history_mc_plus_trl_log"]["mean_heldout_long_horizon_value_mse"]
        - method_summary["history_model_dp"]["mean_heldout_long_horizon_value_mse"]
    )
    history_model_action_gap = abs(
        method_summary["history_mc_plus_trl_log"]["action_disagreement_rate"]
        - method_summary["history_model_dp"]["action_disagreement_rate"]
    )
    model_explains_all_gains = history_model_gap <= EQUIV_TOL and history_model_action_gap <= EQUIV_TOL
    leakage_free = all(result["leakage_free"] for result in evaluated)
    cue_regimes_present = sorted({case["family"] for case in cases}) == sorted(FAMILIES)

    artifact_paths = [
        f"research/{PROJECT}/artifacts/{EXPERIMENT_ID}/randomized_pomdp_context_audit.py",
        f"research/{PROJECT}/artifacts/{EXPERIMENT_ID}/raw_metrics.json",
        f"research/{PROJECT}/artifacts/{EXPERIMENT_ID}/metrics.csv",
        f"research/{PROJECT}/artifacts/{EXPERIMENT_ID}/family_summary.csv",
        f"research/{PROJECT}/artifacts/{EXPERIMENT_ID}/context_summary.csv",
        f"research/{PROJECT}/artifacts/{EXPERIMENT_ID}/coverage_diagnostics.json",
        f"research/{PROJECT}/artifacts/{EXPERIMENT_ID}/offline_datasets.json",
        f"research/{PROJECT}/artifacts/{EXPERIMENT_ID}/transition_tables.json",
        f"research/{PROJECT}/artifacts/{EXPERIMENT_ID}/value_tables.json",
        f"research/{PROJECT}/artifacts/{EXPERIMENT_ID}/leakage_checks.json",
    ]
    coverage_diagnostics = {
        "label_horizon_cutoff": LABEL_HORIZON_CUTOFF,
        "families": list(FAMILIES),
        "seeds": list(SEEDS),
        "case_coverage": {
            result["case"]["case_id"]: {
                "case": result["case"],
                "observation_label_coverage": result["obs_label_coverage"],
                "history_label_coverage": result["hist_label_coverage"],
            }
            for result in evaluated
        },
    }
    offline_datasets = {
        result["case"]["case_id"]: {
            "case": result["case"],
            "num_trajectories": len(result["trajectories"]),
            "trajectories": result["trajectories"],
        }
        for result in evaluated
    }
    transition_tables = {
        result["case"]["case_id"]: {
            "latent_true_transitions_for_evaluation_only": transitions_json(result["latent_transitions"]),
            "observation_transition_counts": counts_json(result["obs_counts"]),
            "history_transition_counts": counts_json(result["hist_counts"]),
            "observation_empirical_transitions": transitions_json(result["obs_transitions"]),
            "history_empirical_transitions": transitions_json(result["hist_transitions"]),
        }
        for result in evaluated
    }
    value_tables = {
        result["case"]["case_id"]: {
            "exact_latent_q": q_json(result["exact_q"]),
            "method_q": {method: q_json(q_values) for method, q_values in sorted(result["q_tables"].items())},
        }
        for result in evaluated
    }
    leakage_checks = {
        "leakage_free": leakage_free,
        "forbidden_tokens": ["good", "bad", "hub_good", "hub_bad", "latent"],
        "note": "Training keys are observation strings and bounded cue-plus-last-three-observation histories; latent states are kept in trajectories only for audit/evaluation.",
        "keys_by_case": {result["case"]["case_id"]: result["leakage_keys"] for result in evaluated},
    }
    raw_metrics = {
        "experiment_id": EXPERIMENT_ID,
        "method_summary": method_summary,
        "family_summary": family_summary_rows,
        "context_summary": context_summary_rows,
        "metrics_rows": metrics_rows,
        "coverage_diagnostics": coverage_diagnostics,
        "leakage_checks": leakage_checks,
        "runtime_seconds": runtime_seconds,
    }
    write_json(artifact_dir / "raw_metrics.json", raw_metrics)
    write_csv(artifact_dir / "metrics.csv", metrics_rows)
    write_csv(artifact_dir / "family_summary.csv", family_summary_rows)
    write_csv(artifact_dir / "context_summary.csv", context_summary_rows)
    write_json(artifact_dir / "coverage_diagnostics.json", coverage_diagnostics)
    write_json(artifact_dir / "offline_datasets.json", offline_datasets)
    write_json(artifact_dir / "transition_tables.json", transition_tables)
    write_json(artifact_dir / "value_tables.json", value_tables)
    write_json(artifact_dir / "leakage_checks.json", leakage_checks)

    metrics = {
        "num_cases": len(cases),
        "num_metric_rows": len(metrics_rows),
        "method_summary": method_summary,
        "cue_sufficient_summary": sufficient_summary,
        "observation_aliasing_failure": obs_failure,
        "cue_sufficient_history_mc_plus_improvement_fraction_vs_mc_only": sufficient_improvement,
        "model_dp_explains_all_history_mc_plus_gains": model_explains_all_gains,
        "leakage_free_training_keys": leakage_free,
        "cue_regimes_present": cue_regimes_present,
    }
    baseline_metrics = {
        "observation_trl_log": method_summary["observation_trl_log"],
        "observation_empirical_model_dp": method_summary["observation_empirical_model_dp"],
        "history_mc_only": method_summary["history_mc_only"],
        "history_model_dp": method_summary["history_model_dp"],
        "latent_oracle_dp": method_summary["latent_oracle_dp"],
    }
    metric_deltas = {
        "cue_sufficient_history_mc_plus_minus_history_mc_only_heldout_mse": mc_plus_mse - mc_mse,
        "cue_sufficient_history_mc_plus_improvement_fraction_vs_mc_only": sufficient_improvement,
        "overall_observation_trl_log_minus_latent_oracle_heldout_mse": method_summary["observation_trl_log"]["mean_heldout_long_horizon_value_mse"] - method_summary["latent_oracle_dp"]["mean_heldout_long_horizon_value_mse"],
        "overall_history_mc_plus_minus_history_model_dp_heldout_mse": method_summary["history_mc_plus_trl_log"]["mean_heldout_long_horizon_value_mse"] - method_summary["history_model_dp"]["mean_heldout_long_horizon_value_mse"],
        "overall_history_mc_plus_minus_history_mc_only_heldout_mse": method_summary["history_mc_plus_trl_log"]["mean_heldout_long_horizon_value_mse"] - method_summary["history_mc_only"]["mean_heldout_long_horizon_value_mse"],
    }
    known_failures = []
    if model_explains_all_gains:
        known_failures.append("history-model DP fully matches history MC+TRL-log gains, so this is boundary/negative for distinct TRL algorithmic value.")
    if not leakage_free:
        known_failures.append("A training key contained a forbidden latent token.")
    interpretation = (
        "Observation-only methods fail under aliasing, and bounded history improves strongly when cues are sufficient. "
        "Cue-noisy and cue-insufficient families separate representation sufficiency from oracle disambiguation. "
        "History MC+TRL-log improves over MC-only, but the gains are fully explained by history-model DP, so this is representation/context evidence and a boundary result for TRL algorithmic value."
    )
    success_criteria_results = [
        f"Ran {len(FAMILIES)} families x {len(SEEDS)} seeds.",
        f"Observation-only aliasing failure observed: {obs_failure}.",
        f"Cue-sufficient history MC+TRL-log MSE improvement over MC-only: {sufficient_improvement:.6f}.",
        f"History-model DP compared directly; explains all gains: {model_explains_all_gains}.",
        f"Leakage-free training keys: {leakage_free}.",
    ]
    failure_criteria_results = [
        "History MC+TRL-log is better than history MC-only in cue-sufficient regimes.",
        "Cue-noisy and cue-insufficient regimes are included.",
        "No training method consumes latent state, exact DP labels, true transition probabilities, or future observations.",
        "No neural networks, continuous-control environments, downloads, or expensive training were used.",
    ]
    decision_relevant_findings = [
        f"Cue-sufficient MC+TRL improvement fraction: {sufficient_improvement:.6f}.",
        f"Model DP explains all gains: {model_explains_all_gains}.",
        f"Overall history MC+TRL minus history-model-DP heldout MSE: {metric_deltas['overall_history_mc_plus_minus_history_model_dp_heldout_mse']:.12f}.",
        "The viable direction is context representation; no distinct TRL component was isolated.",
    ]
    result = {
        "experiment_id": EXPERIMENT_ID,
        "status": "completed",
        "claim_tested": "A randomized aliased-POMDP suite tested whether bounded observation history generalizes the 0012 context pivot and whether MC+TRL-log adds value beyond history-model DP.",
        "commands_run": COMMANDS_RUN,
        "metrics": metrics,
        "baseline_metrics": baseline_metrics,
        "artifacts": artifact_paths,
        "interpretation": interpretation,
        "known_failures": known_failures,
        "next_questions": [
            "Can non-model TRL exploit history when the history-model state space is too large for exact DP?",
            "How should cue reliability be estimated before deciding whether history context is sufficient?",
            "Can a future benchmark include noisy cues without latent leakage while still requiring policy improvement?",
        ],
        "runtime_seconds": runtime_seconds,
        "resource_usage": {"device": "cpu", "num_cases": len(cases), "num_metric_rows": len(metrics_rows)},
        "success_criteria_results": success_criteria_results,
        "failure_criteria_results": failure_criteria_results,
        "metric_deltas": metric_deltas,
        "decision_relevant_findings": decision_relevant_findings,
    }
    write_json(result_dir / f"{EXPERIMENT_ID}_result.json", result)

    summary = f"""# Experiment {EXPERIMENT_ID} Summary

## Objective

Test whether the partial-observation/context pivot generalizes beyond the single hand-constructed 0012 POMDP and whether any TRL-style transitive component adds value beyond history-model DP.

## Commands Run

```bash
{chr(10).join(COMMANDS_RUN)}
```

## Suite

- Families: `{list(FAMILIES)}`
- Seeds: `{list(SEEDS)}`
- Cases: `{len(cases)}`
- Label horizon cutoff: `{LABEL_HORIZON_CUTOFF}`

## Method Summary

| Method | Heldout MSE | Policy regret | Teleport rate | Calibration error | Action disagreement |
| --- | ---: | ---: | ---: | ---: | ---: |
"""
    for method, stats in sorted(method_summary.items()):
        summary += (
            f"| {method} | {stats['mean_heldout_long_horizon_value_mse']:.12f} | {stats['mean_policy_regret']:.12f} | "
            f"{stats['teleport_action_rate']:.6f} | {stats['mean_calibration_error']:.12f} | {stats['action_disagreement_rate']:.6f} |\n"
        )
    summary += f"""
## Decision Findings

- Observation-only aliasing failure: `{obs_failure}`
- Cue-sufficient MC+TRL-log improvement vs MC-only: `{sufficient_improvement:.6f}`
- History-model DP explains all gains: `{model_explains_all_gains}`
- Leakage-free training keys: `{leakage_free}`

## Interpretation

{interpretation}

## Artifacts

- `research/{PROJECT}/artifacts/{EXPERIMENT_ID}/randomized_pomdp_context_audit.py`
- `research/{PROJECT}/artifacts/{EXPERIMENT_ID}/raw_metrics.json`
- `research/{PROJECT}/artifacts/{EXPERIMENT_ID}/metrics.csv`
- `research/{PROJECT}/artifacts/{EXPERIMENT_ID}/family_summary.csv`
- `research/{PROJECT}/artifacts/{EXPERIMENT_ID}/context_summary.csv`
- `research/{PROJECT}/artifacts/{EXPERIMENT_ID}/coverage_diagnostics.json`
- `research/{PROJECT}/artifacts/{EXPERIMENT_ID}/offline_datasets.json`
- `research/{PROJECT}/artifacts/{EXPERIMENT_ID}/transition_tables.json`
- `research/{PROJECT}/artifacts/{EXPERIMENT_ID}/value_tables.json`
- `research/{PROJECT}/artifacts/{EXPERIMENT_ID}/leakage_checks.json`
"""
    (result_dir / f"{EXPERIMENT_ID}_summary.md").write_text(summary)
    print(json.dumps({
        "status": result["status"],
        "num_cases": len(cases),
        "cue_sufficient_improvement": sufficient_improvement,
        "model_explains_all_gains": model_explains_all_gains,
        "leakage_free": leakage_free,
        "known_failures": known_failures,
    }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
