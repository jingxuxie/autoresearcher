#!/usr/bin/env python3
"""Experiment 0007: generic branch-uncertainty audit."""

from __future__ import annotations

import csv
import json
import math
from collections import Counter, defaultdict, deque
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Optional, Tuple


EXPERIMENT_ID = "0007"
PROJECT = "sto_trl"
GAMMA = 0.9
UPDATE_STEPS = 32
LABEL_HORIZON_CUTOFF = 2
SUCCESSOR_BASELINE_LAMBDA = 0.25
GENERIC_PRIOR_GRID = (0.5, 1.0)
GENERIC_ALPHA_GRID = (0.0, 0.5, 1.0)
BEST_0006_ALPHA = 0.4
CHAIN_MSE_TOL = 1e-20
TOL = 1e-12

COMMANDS_RUN = [
    "mkdir -p research/sto_trl/artifacts/0007 research/sto_trl/results && cp research/sto_trl/artifacts/0006/run_uncertainty_conservative_log_trl.py research/sto_trl/artifacts/0007/run_generic_uncertainty_audit.py",
    "conda run -n autoresearcher_sto_trl python research/sto_trl/artifacts/0007/run_generic_uncertainty_audit.py",
    "conda run -n autoresearcher_sto_trl python scripts/validate_artifacts.py --repo-root . --json research/sto_trl/results/0007_result.json --schema schemas/result.schema.json --check-result-artifacts",
]


@dataclass(frozen=True)
class MDP:
    name: str
    states: Tuple[str, ...]
    actions: Mapping[str, Tuple[str, ...]]
    transitions: Mapping[Tuple[str, str], Tuple[Tuple[float, str], ...]]
    eval_start: str
    eval_goal: str
    risky_state: Optional[str] = None
    risky_action: Optional[str] = None
    true_risky_success_prob: Optional[float] = None


QTable = Dict[Tuple[str, str, str], float]
VTable = Dict[str, Dict[str, float]]


def write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")


def deterministic_chain(length: int = 9) -> MDP:
    states = tuple(f"c{i}" for i in range(length))
    actions: Dict[str, Tuple[str, ...]] = {}
    transitions: Dict[Tuple[str, str], Tuple[Tuple[float, str], ...]] = {}
    for idx, state in enumerate(states):
        action_list: List[str] = []
        if idx < length - 1:
            action_list.append("right")
            transitions[(state, "right")] = ((1.0, states[idx + 1]),)
        if idx > 0:
            action_list.append("left")
            transitions[(state, "left")] = ((1.0, states[idx - 1]),)
        actions[state] = tuple(action_list)
    return MDP(
        name="deterministic_chain_len9",
        states=states,
        actions=actions,
        transitions=transitions,
        eval_start="c0",
        eval_goal=f"c{length - 1}",
    )


def risky_shortcut(name: str, true_success_prob: float) -> MDP:
    states = ("start", "safe1", "safe2", "goal", "trap")
    actions = {
        "start": ("risky", "safe"),
        "safe1": ("forward",),
        "safe2": ("forward",),
        "goal": tuple(),
        "trap": tuple(),
    }
    transitions = {
        ("start", "risky"): ((true_success_prob, "goal"), (1.0 - true_success_prob, "trap")),
        ("start", "safe"): ((1.0, "safe1"),),
        ("safe1", "forward"): ((1.0, "safe2"),),
        ("safe2", "forward"): ((1.0, "goal"),),
    }
    return MDP(
        name=name,
        states=states,
        actions=actions,
        transitions=transitions,
        eval_start="start",
        eval_goal="goal",
        risky_state="start",
        risky_action="risky",
        true_risky_success_prob=true_success_prob,
    )


def chain_trajectories(mdp: MDP) -> List[Dict[str, Any]]:
    length = len(mdp.states)
    return [
        {
            "episode_id": "chain_forward",
            "mdp": mdp.name,
            "states": [f"c{i}" for i in range(length)],
            "actions": ["right"] * (length - 1),
            "transitions": [
                {"t": i, "state": f"c{i}", "action": "right", "next_state": f"c{i + 1}", "outcome": "deterministic"}
                for i in range(length - 1)
            ],
        },
        {
            "episode_id": "chain_backward",
            "mdp": mdp.name,
            "states": [f"c{i}" for i in reversed(range(length))],
            "actions": ["left"] * (length - 1),
            "transitions": [
                {"t": i, "state": f"c{length - 1 - i}", "action": "left", "next_state": f"c{length - 2 - i}", "outcome": "deterministic"}
                for i in range(length - 1)
            ],
        },
    ]


def risky_trajectories(mdp: MDP, successes: int, failures: int, scenario_id: str) -> List[Dict[str, Any]]:
    trajectories: List[Dict[str, Any]] = []
    for idx in range(4):
        trajectories.append(
            {
                "episode_id": f"{scenario_id}_safe_{idx}",
                "mdp": mdp.name,
                "states": ["start", "safe1", "safe2", "goal"],
                "actions": ["safe", "forward", "forward"],
                "transitions": [
                    {"t": 0, "state": "start", "action": "safe", "next_state": "safe1", "outcome": "safe_step"},
                    {"t": 1, "state": "safe1", "action": "forward", "next_state": "safe2", "outcome": "safe_step"},
                    {"t": 2, "state": "safe2", "action": "forward", "next_state": "goal", "outcome": "safe_goal"},
                ],
            }
        )
    outcomes = ["success"] * successes + ["failure"] * failures
    for idx, outcome in enumerate(outcomes):
        next_state = "goal" if outcome == "success" else "trap"
        trajectories.append(
            {
                "episode_id": f"{scenario_id}_risky_{idx}_{outcome}",
                "mdp": mdp.name,
                "states": ["start", next_state],
                "actions": ["risky"],
                "transitions": [
                    {"t": 0, "state": "start", "action": "risky", "next_state": next_state, "outcome": f"risky_{outcome}"}
                ],
            }
        )
    return trajectories


def logsumexp(values: Iterable[float]) -> float:
    finite = [value for value in values if not math.isinf(value)]
    if not finite:
        return -math.inf
    pivot = max(finite)
    return pivot + math.log(sum(math.exp(value - pivot) for value in finite))


def score_to_distance(score: float) -> Optional[float]:
    if score <= 0.0:
        return None
    return math.log(min(score, 1.0)) / math.log(GAMMA)


def distance_to_score(distance: Optional[float]) -> float:
    if distance is None:
        return 0.0
    return GAMMA**distance


def distance_relax(anchor_score: float, backup_score: float, lambda_tr: float) -> float:
    if anchor_score <= 0.0:
        return backup_score
    if backup_score <= 0.0:
        return anchor_score
    anchor_distance = score_to_distance(anchor_score)
    backup_distance = score_to_distance(backup_score)
    relaxed_distance = (1.0 - lambda_tr) * float(anchor_distance) + lambda_tr * float(backup_distance)
    return distance_to_score(relaxed_distance)


def exact_discounted_reachability_dp(mdp: MDP) -> Tuple[VTable, QTable]:
    values: VTable = {
        goal: {state: 1.0 if state == goal else 0.0 for state in mdp.states}
        for goal in mdp.states
    }
    for _ in range(1000):
        max_delta = 0.0
        next_values: VTable = {}
        for goal in mdp.states:
            next_values[goal] = {}
            for state in mdp.states:
                if state == goal:
                    updated = 1.0
                else:
                    action_values = [
                        GAMMA * sum(prob * values[goal][next_state] for prob, next_state in mdp.transitions[(state, action)])
                        for action in mdp.actions.get(state, tuple())
                    ]
                    updated = max(action_values) if action_values else 0.0
                next_values[goal][state] = updated
                max_delta = max(max_delta, abs(updated - values[goal][state]))
        values = next_values
        if max_delta < TOL:
            break
    q_values: QTable = {}
    for goal in mdp.states:
        for state in mdp.states:
            for action in mdp.actions.get(state, tuple()):
                if state == goal:
                    q_values[(state, action, goal)] = 1.0
                else:
                    q_values[(state, action, goal)] = GAMMA * sum(
                        prob * values[goal][next_state]
                        for prob, next_state in mdp.transitions[(state, action)]
                    )
    return values, q_values


def support_horizons(mdp: MDP) -> Dict[str, Dict[str, Optional[int]]]:
    graph: Dict[str, List[str]] = {state: [] for state in mdp.states}
    for (state, _action), outcomes in mdp.transitions.items():
        for _prob, next_state in outcomes:
            graph[state].append(next_state)
    horizons: Dict[str, Dict[str, Optional[int]]] = {}
    for source in mdp.states:
        distance: Dict[str, Optional[int]] = {state: None for state in mdp.states}
        distance[source] = 0
        queue: deque[str] = deque([source])
        while queue:
            state = queue.popleft()
            for next_state in graph.get(state, []):
                if distance[next_state] is None:
                    distance[next_state] = int(distance[state]) + 1
                    queue.append(next_state)
        horizons[source] = distance
    return horizons


def horizon_bin(distance: Optional[int]) -> str:
    if distance is None:
        return "unreachable"
    if distance == 0:
        return "self"
    if distance <= LABEL_HORIZON_CUTOFF:
        return f"h{distance}_train_visible"
    return f"heldout_gt{LABEL_HORIZON_CUTOFF}"


def q_horizon_bin(mdp: MDP, horizons: Mapping[str, Mapping[str, Optional[int]]], state: str, action: str, goal: str) -> str:
    if state == goal:
        return "self"
    distances = []
    for _prob, next_state in mdp.transitions[(state, action)]:
        next_distance = horizons[next_state][goal]
        if next_distance is not None:
            distances.append(next_distance + 1)
    return horizon_bin(min(distances) if distances else None)


def value_horizon_bin(mdp: MDP, horizons: Mapping[str, Mapping[str, Optional[int]]], exact_q: QTable, state: str, goal: str) -> str:
    if state == goal:
        return "self"
    actions = mdp.actions.get(state, tuple())
    if not actions:
        return "unreachable"
    best_action = max(actions, key=lambda action: exact_q.get((state, action, goal), 0.0))
    if exact_q.get((state, best_action, goal), 0.0) <= 0.0:
        return "unreachable"
    return q_horizon_bin(mdp, horizons, state, best_action, goal)


def empirical_transition_counts(trajectories: List[Dict[str, Any]]) -> Dict[Tuple[str, str], Counter[str]]:
    counts: Dict[Tuple[str, str], Counter[str]] = defaultdict(Counter)
    for episode in trajectories:
        for transition in episode["transitions"]:
            counts[(transition["state"], transition["action"])][transition["next_state"]] += 1
    return counts


def values_from_q(mdp: MDP, q_values: QTable) -> VTable:
    values: VTable = {}
    for goal in mdp.states:
        values[goal] = {}
        for state in mdp.states:
            if state == goal:
                values[goal][state] = 1.0
                continue
            action_values = [q_values.get((state, action, goal), 0.0) for action in mdp.actions.get(state, tuple())]
            values[goal][state] = max(action_values) if action_values else 0.0
    return values


def censored_mc_labels(mdp: MDP, trajectories: List[Dict[str, Any]]) -> Tuple[QTable, Dict[Tuple[str, str, str], int], Dict[str, Any]]:
    sums: Dict[Tuple[str, str, str], float] = defaultdict(float)
    counts: Dict[Tuple[str, str, str], int] = defaultdict(int)
    label_counts: Dict[str, Counter[str]] = defaultdict(Counter)
    unique_pairs: Dict[str, set[Tuple[str, str, str]]] = defaultdict(set)
    censored_examples: List[Dict[str, Any]] = []
    for episode in trajectories:
        states = episode["states"]
        actions = episode["actions"]
        for t, action in enumerate(actions):
            state = states[t]
            future_states = states[t + 1 :]
            for goal in mdp.states:
                first_offset = None
                for offset, future_state in enumerate(future_states, start=1):
                    if future_state == goal:
                        first_offset = offset
                        break
                if first_offset is None:
                    key = (state, action, goal)
                    sums[key] += 0.0
                    counts[key] += 1
                    label_counts["unreached_zero"]["included_zero"] += 1
                    unique_pairs["unreached_zero"].add(key)
                elif first_offset <= LABEL_HORIZON_CUTOFF:
                    key = (state, action, goal)
                    sums[key] += GAMMA**first_offset
                    counts[key] += 1
                    bin_name = horizon_bin(first_offset)
                    label_counts[bin_name]["included_positive"] += 1
                    unique_pairs[bin_name].add(key)
                else:
                    bin_name = horizon_bin(first_offset)
                    label_counts[bin_name]["censored_positive"] += 1
                    unique_pairs[bin_name].add((state, action, goal))
                    if len(censored_examples) < 12:
                        censored_examples.append(
                            {
                                "episode_id": episode["episode_id"],
                                "state": state,
                                "action": action,
                                "goal": goal,
                                "positive_horizon": first_offset,
                            }
                        )
    q_values = {key: min(1.0, max(0.0, sums[key] / count)) for key, count in counts.items()}
    coverage = {
        "label_horizon_cutoff": LABEL_HORIZON_CUTOFF,
        "counts_by_bin": {bin_name: dict(counter) for bin_name, counter in sorted(label_counts.items())},
        "unique_state_action_goal_pairs_by_bin": {bin_name: len(pairs) for bin_name, pairs in sorted(unique_pairs.items())},
        "num_censored_positive_labels": sum(counter.get("censored_positive", 0) for counter in label_counts.values()),
        "num_included_positive_labels": sum(counter.get("included_positive", 0) for counter in label_counts.values()),
        "num_included_zero_labels": sum(counter.get("included_zero", 0) for counter in label_counts.values()),
        "censored_examples": censored_examples,
    }
    return q_values, counts, coverage


def self_normalize_successor_scores(q_values: QTable) -> QTable:
    grouped: Dict[Tuple[str, str], List[Tuple[Tuple[str, str, str], float]]] = defaultdict(list)
    for key, score in q_values.items():
        state, action, _goal = key
        grouped[(state, action)].append((key, score))
    normalized: QTable = {}
    for _state_action, entries in grouped.items():
        max_score = max([score for _key, score in entries] + [1.0])
        for key, score in entries:
            normalized[key] = min(1.0, max(0.0, score / max_score))
    return normalized


def train_mc_supervised(mdp: MDP, trajectories: List[Dict[str, Any]]) -> Tuple[QTable, Dict[Tuple[str, str, str], int], Dict[str, Any]]:
    return censored_mc_labels(mdp, trajectories)


def train_successor_calibration_only(mdp: MDP, trajectories: List[Dict[str, Any]]) -> Tuple[QTable, Dict[Tuple[str, str, str], int], Dict[str, Any]]:
    q_values, counts, coverage = censored_mc_labels(mdp, trajectories)
    return self_normalize_successor_scores(q_values), counts, coverage


def train_trl_raw(mdp: MDP, trajectories: List[Dict[str, Any]]) -> QTable:
    observed_next = {key: tuple(counter.keys()) for key, counter in empirical_transition_counts(trajectories).items()}
    values: VTable = {
        goal: {state: 1.0 if state == goal else 0.0 for state in mdp.states}
        for goal in mdp.states
    }
    q_values: QTable = {}
    for _ in range(UPDATE_STEPS):
        next_q: QTable = {}
        for (state, action), next_states in observed_next.items():
            for goal in mdp.states:
                next_q[(state, action, goal)] = 1.0 if state == goal else GAMMA * max(values[goal][next_state] for next_state in next_states)
        q_values = next_q
        values = values_from_q(mdp, q_values)
    return q_values


def stochastic_log_backup(mdp: MDP, trajectories: List[Dict[str, Any]], values: VTable) -> QTable:
    next_q: QTable = {}
    for (state, action), counter in empirical_transition_counts(trajectories).items():
        total = sum(counter.values())
        empirical_probs = [(count / total, next_state) for next_state, count in counter.items()]
        for goal in mdp.states:
            if state == goal:
                next_q[(state, action, goal)] = 1.0
                continue
            terms = []
            for probability, next_state in empirical_probs:
                next_value = values[goal][next_state]
                terms.append(-math.inf if next_value <= 0.0 else math.log(probability) + math.log(next_value))
            log_value = math.log(GAMMA) + logsumexp(terms)
            next_q[(state, action, goal)] = 0.0 if math.isinf(log_value) else math.exp(log_value)
    return next_q


def shortcut_uncertainty_penalty(
    mdp: MDP,
    transition_counts: Mapping[Tuple[str, str], Counter[str]],
    state: str,
    action: str,
    goal: str,
    alpha: float,
) -> Tuple[float, Dict[str, Any]]:
    counter = transition_counts[(state, action)]
    total_count = sum(counter.values())
    branch_count = len(counter)
    direct_goal_only = branch_count == 1 and counter.get(goal, 0) == total_count
    multi_action_state = len(mdp.actions.get(state, tuple())) > 1
    eligible = alpha > 0.0 and total_count >= 4 and direct_goal_only and multi_action_state
    penalty = alpha * GAMMA / math.sqrt(total_count) if eligible else 0.0
    return penalty, {
        "count": total_count,
        "branch_count": branch_count,
        "direct_goal_only": direct_goal_only,
        "multi_action_state": multi_action_state,
        "eligible": eligible,
        "penalty": penalty,
    }


def conservative_log_backup(mdp: MDP, trajectories: List[Dict[str, Any]], values: VTable, alpha: float) -> Tuple[QTable, Dict[str, Any]]:
    transition_counts = empirical_transition_counts(trajectories)
    raw_backup = stochastic_log_backup(mdp, trajectories, values)
    penalized: QTable = {}
    diagnostics: Dict[str, Any] = {}
    for key, backup_score in raw_backup.items():
        state, action, goal = key
        penalty, detail = shortcut_uncertainty_penalty(mdp, transition_counts, state, action, goal, alpha)
        penalized[key] = max(0.0, backup_score - penalty)
        if penalty > 0.0:
            diagnostics[f"{state}|{action}|{goal}"] = {
                **detail,
                "raw_backup": backup_score,
                "penalized_backup": penalized[key],
                "alpha": alpha,
            }
    return penalized, diagnostics


def train_trl_log(mdp: MDP, trajectories: List[Dict[str, Any]]) -> QTable:
    q_values: QTable = {}
    values: VTable = {
        goal: {state: 1.0 if state == goal else 0.0 for state in mdp.states}
        for goal in mdp.states
    }
    for _ in range(UPDATE_STEPS):
        q_values = stochastic_log_backup(mdp, trajectories, values)
        values = values_from_q(mdp, q_values)
    return q_values


def train_conservative_log_trl(mdp: MDP, trajectories: List[Dict[str, Any]], alpha: float) -> Tuple[QTable, Dict[str, Any]]:
    q_values: QTable = {}
    values: VTable = {
        goal: {state: 1.0 if state == goal else 0.0 for state in mdp.states}
        for goal in mdp.states
    }
    all_penalties: Dict[str, Any] = {}
    for _ in range(UPDATE_STEPS):
        q_values, penalties = conservative_log_backup(mdp, trajectories, values, alpha)
        all_penalties.update(penalties)
        values = values_from_q(mdp, q_values)
    return q_values, {
        "alpha": alpha,
        "penalty_formula": "max(0, empirical_log_backup - alpha * gamma / sqrt(count)) for direct-goal single-branch shortcut actions at multi-action states with count >= 4",
        "penalized_pairs": all_penalties,
    }


def generic_dirichlet_unknown_backup(
    mdp: MDP,
    trajectories: List[Dict[str, Any]],
    values: VTable,
    prior_mass: float,
    alpha: float,
) -> Tuple[QTable, Dict[str, Any]]:
    transition_counts = empirical_transition_counts(trajectories)
    empirical_q = stochastic_log_backup(mdp, trajectories, values)
    generic_q: QTable = {}
    diagnostics: Dict[str, Any] = {}
    for (state, action), counter in transition_counts.items():
        total = sum(counter.values())
        for goal in mdp.states:
            key = (state, action, goal)
            empirical_score = empirical_q.get(key, 0.0)
            observed_sum = sum(count * values[goal][next_state] for next_state, count in counter.items())
            effective_prior = prior_mass if total >= 4 else 0.0
            posterior_lower = GAMMA * observed_sum / (total + effective_prior)
            generic_score = (1.0 - alpha) * empirical_score + alpha * posterior_lower
            generic_q[key] = max(0.0, min(1.0, generic_score))
            diagnostics[f"{state}|{action}|{goal}"] = {
                "count": total,
                "branch_count": len(counter),
                "prior_mass": prior_mass,
                "effective_prior_mass": effective_prior,
                "alpha": alpha,
                "empirical_score": empirical_score,
                "posterior_lower_score": posterior_lower,
                "generic_score": generic_q[key],
                "penalty": empirical_score - generic_q[key],
            }
    return generic_q, diagnostics


def train_generic_uncertainty_log_trl(
    mdp: MDP,
    trajectories: List[Dict[str, Any]],
    prior_mass: float,
    alpha: float,
) -> Tuple[QTable, Dict[str, Any]]:
    q_values: QTable = {}
    values: VTable = {
        goal: {state: 1.0 if state == goal else 0.0 for state in mdp.states}
        for goal in mdp.states
    }
    latest_diagnostics: Dict[str, Any] = {}
    for _ in range(UPDATE_STEPS):
        q_values, latest_diagnostics = generic_dirichlet_unknown_backup(mdp, trajectories, values, prior_mass, alpha)
        values = values_from_q(mdp, q_values)
    return q_values, {
        "prior_mass": prior_mass,
        "alpha": alpha,
        "formula": "interpolate empirical log backup with Dirichlet unknown-zero posterior lower estimate using only observed next-state counts",
        "pair_diagnostics": latest_diagnostics,
    }


def train_mc_plus_trl_log(mdp: MDP, trajectories: List[Dict[str, Any]], anchor_weight: float = 0.5) -> QTable:
    mc_q, mc_counts, _coverage = train_mc_supervised(mdp, trajectories)
    q_values = dict(mc_q)
    values = values_from_q(mdp, q_values)
    for _ in range(UPDATE_STEPS):
        backup_q = stochastic_log_backup(mdp, trajectories, values)
        next_q: QTable = {}
        for key, backup_score in backup_q.items():
            next_q[key] = anchor_weight * mc_q[key] + (1.0 - anchor_weight) * backup_score if key in mc_counts else backup_score
        q_values = next_q
        values = values_from_q(mdp, q_values)
    return q_values


def train_successor_distance_trl_log(mdp: MDP, trajectories: List[Dict[str, Any]], lambda_tr: float) -> Tuple[QTable, Dict[str, Any]]:
    anchor_q, anchor_counts, _coverage = train_successor_calibration_only(mdp, trajectories)
    if lambda_tr == 0.0:
        return dict(anchor_q), {
            "lambda_tr": lambda_tr,
            "relaxation": "distance_space_geometric_interpolation",
            "anchor": "self_normalized_censored_successor_calibration",
            "endpoint": "calibration_only",
        }
    q_values = dict(anchor_q)
    values = values_from_q(mdp, q_values)
    for _ in range(UPDATE_STEPS):
        backup_q = stochastic_log_backup(mdp, trajectories, values)
        next_q: QTable = {}
        for key, backup_score in backup_q.items():
            if key in anchor_counts:
                next_q[key] = distance_relax(anchor_q[key], backup_score, lambda_tr)
            else:
                next_q[key] = backup_score
        q_values = next_q
        values = values_from_q(mdp, q_values)
    meta = {
        "lambda_tr": lambda_tr,
        "relaxation": "distance_space_geometric_interpolation",
        "anchor": "self_normalized_censored_successor_calibration",
    }
    return q_values, meta


def lambda_method_name(lambda_tr: float) -> str:
    return f"successor_distance_trl_log_lambda_{lambda_tr:.2f}".replace(".", "_")


def alpha_method_name(alpha: float) -> str:
    return f"one_sided_conservative_log_trl_alpha_{alpha:.2f}".replace(".", "_")


def generic_method_name(prior_mass: float, alpha: float) -> str:
    return f"generic_dirichlet_unknown_prior_{prior_mass:.2f}_alpha_{alpha:.2f}".replace(".", "_")


def greedy_policy(mdp: MDP, q_values: QTable, goal: str) -> Dict[str, Optional[str]]:
    policy: Dict[str, Optional[str]] = {}
    for state in mdp.states:
        actions = mdp.actions.get(state, tuple())
        if state == goal or not actions:
            policy[state] = None
            continue
        policy[state] = max(actions, key=lambda action: (q_values.get((state, action, goal), 0.0), -actions.index(action)))
    return policy


def evaluate_policy(mdp: MDP, policy: Mapping[str, Optional[str]], goal: str) -> Dict[str, float]:
    values = {state: 1.0 if state == goal else 0.0 for state in mdp.states}
    for _ in range(1000):
        max_delta = 0.0
        next_values: Dict[str, float] = {}
        for state in mdp.states:
            if state == goal:
                updated = 1.0
            else:
                action = policy.get(state)
                updated = 0.0 if action is None else GAMMA * sum(prob * values[next_state] for prob, next_state in mdp.transitions[(state, action)])
            next_values[state] = updated
            max_delta = max(max_delta, abs(updated - values[state]))
        values = next_values
        if max_delta < TOL:
            break
    return values


def mse(values: List[float]) -> float:
    return sum(value * value for value in values) / len(values) if values else 0.0


def evaluate_method(mdp: MDP, q_values: QTable, exact_values: VTable, exact_q: QTable) -> Dict[str, Any]:
    horizons = support_horizons(mdp)
    learned_values = values_from_q(mdp, q_values)
    value_error_by_bin: Dict[str, List[float]] = defaultdict(list)
    q_error_by_bin: Dict[str, List[float]] = defaultdict(list)
    for goal in mdp.states:
        for state in mdp.states:
            if state == goal:
                continue
            bin_name = value_horizon_bin(mdp, horizons, exact_q, state, goal)
            value_error_by_bin[bin_name].append(learned_values[goal][state] - exact_values[goal][state])
    for state in mdp.states:
        for action in mdp.actions.get(state, tuple()):
            for goal in mdp.states:
                if state == goal:
                    continue
                bin_name = q_horizon_bin(mdp, horizons, state, action, goal)
                key = (state, action, goal)
                q_error_by_bin[bin_name].append(q_values.get(key, 0.0) - exact_q.get(key, 0.0))
    all_value_errors = [error for errors in value_error_by_bin.values() for error in errors]
    all_q_errors = [error for errors in q_error_by_bin.values() for error in errors]
    horizon_metrics: Dict[str, Dict[str, Any]] = {}
    for bin_name in sorted(set(value_error_by_bin) | set(q_error_by_bin)):
        value_errors = value_error_by_bin.get(bin_name, [])
        q_errors = q_error_by_bin.get(bin_name, [])
        horizon_metrics[bin_name] = {
            "num_value_pairs": len(value_errors),
            "num_q_pairs": len(q_errors),
            "value_mse": mse(value_errors),
            "value_overestimation_error": max([0.0] + value_errors),
            "value_underestimation_error": max([0.0] + [-error for error in value_errors]),
            "q_calibration_error": sum(abs(error) for error in q_errors) / len(q_errors) if q_errors else 0.0,
            "q_overestimation_error": max([0.0] + q_errors),
            "q_underestimation_error": max([0.0] + [-error for error in q_errors]),
        }
    eval_policy = greedy_policy(mdp, q_values, mdp.eval_goal)
    eval_policy_value = evaluate_policy(mdp, eval_policy, mdp.eval_goal)
    policy_regret = max(0.0, exact_values[mdp.eval_goal][mdp.eval_start] - eval_policy_value[mdp.eval_start])
    risky_selection_rate = 0.0
    if mdp.risky_state is not None and mdp.risky_action is not None:
        risky_selection_rate = 1.0 if eval_policy.get(mdp.risky_state) == mdp.risky_action else 0.0
    eval_start_q = {action: q_values.get((mdp.eval_start, action, mdp.eval_goal), 0.0) for action in mdp.actions.get(mdp.eval_start, tuple())}
    exact_eval_start_q = {action: exact_q.get((mdp.eval_start, action, mdp.eval_goal), 0.0) for action in mdp.actions.get(mdp.eval_start, tuple())}
    optimal_action = max(exact_eval_start_q, key=exact_eval_start_q.get) if exact_eval_start_q else None
    heldout_bin = f"heldout_gt{LABEL_HORIZON_CUTOFF}"
    return {
        "value_mse": mse(all_value_errors),
        "heldout_long_horizon_value_mse": horizon_metrics.get(heldout_bin, {}).get("value_mse", 0.0),
        "value_overestimation_error": max([0.0] + all_value_errors),
        "value_underestimation_error": max([0.0] + [-error for error in all_value_errors]),
        "q_calibration_error": sum(abs(error) for error in all_q_errors) / len(all_q_errors) if all_q_errors else 0.0,
        "calibration_error": sum(abs(error) for error in all_q_errors) / len(all_q_errors) if all_q_errors else 0.0,
        "q_overestimation_error": max([0.0] + all_q_errors),
        "q_underestimation_error": max([0.0] + [-error for error in all_q_errors]),
        "policy_regret": policy_regret,
        "risky_action_selection_rate": risky_selection_rate,
        "eval_start": mdp.eval_start,
        "eval_goal": mdp.eval_goal,
        "eval_start_learned_q": eval_start_q,
        "eval_start_exact_q": exact_eval_start_q,
        "eval_greedy_action": eval_policy.get(mdp.eval_start),
        "exact_optimal_action": optimal_action,
        "chose_exact_optimal_action": eval_policy.get(mdp.eval_start) == optimal_action,
        "horizon_metrics": horizon_metrics,
    }


def distance_diagnostics(mdp: MDP, trajectories: List[Dict[str, Any]], q_values: QTable) -> Dict[str, Any]:
    values = values_from_q(mdp, q_values)
    distances = {goal: {state: score_to_distance(values[goal][state]) for state in mdp.states} for goal in mdp.states}
    observed_next = {key: tuple(counter.keys()) for key, counter in empirical_transition_counts(trajectories).items()}
    violations = 0
    checked = 0
    missing_transitive = 0
    examples = []
    for (state, _action), next_states in observed_next.items():
        for next_state in next_states:
            for goal in mdp.states:
                next_distance = distances[goal][next_state]
                if next_distance is None:
                    continue
                checked += 1
                state_distance = distances[goal][state]
                if state_distance is None:
                    violations += 1
                    missing_transitive += 1
                    if len(examples) < 8:
                        examples.append({"state": state, "next_state": next_state, "goal": goal, "state_distance": None, "next_distance": next_distance})
                elif state_distance > 1.0 + next_distance + 1e-9:
                    violations += 1
                    if len(examples) < 8:
                        examples.append({"state": state, "next_state": next_state, "goal": goal, "state_distance": state_distance, "next_distance": next_distance})
    return {
        "triangle_violation_count": violations,
        "triangle_check_count": checked,
        "triangle_violation_rate": violations / checked if checked else 0.0,
        "missing_transitive_count": missing_transitive,
        "example_violations": examples,
    }


def max_abs_q_diff(mdp: MDP, left: QTable, right: QTable) -> float:
    diffs = []
    for state in mdp.states:
        for action in mdp.actions.get(state, tuple()):
            for goal in mdp.states:
                diffs.append(abs(left.get((state, action, goal), 0.0) - right.get((state, action, goal), 0.0)))
    return max(diffs) if diffs else 0.0


def max_abs_value_diff(mdp: MDP, left: QTable, right: QTable) -> float:
    left_values = values_from_q(mdp, left)
    right_values = values_from_q(mdp, right)
    diffs = [
        abs(left_values[goal][state] - right_values[goal][state])
        for goal in mdp.states
        for state in mdp.states
    ]
    return max(diffs) if diffs else 0.0


def action_diff_rate(mdp: MDP, left: QTable, right: QTable) -> float:
    total = 0
    diffs = 0
    for goal in mdp.states:
        left_policy = greedy_policy(mdp, left, goal)
        right_policy = greedy_policy(mdp, right, goal)
        for state in mdp.states:
            if mdp.actions.get(state, tuple()) and state != goal:
                total += 1
                diffs += int(left_policy[state] != right_policy[state])
    return diffs / total if total else 0.0


def coverage_diagnostics(mdp: MDP, trajectories: List[Dict[str, Any]]) -> Dict[str, Any]:
    states_seen = set()
    state_action_pairs = set()
    action_counts: Counter[str] = Counter()
    outcome_counts: Counter[str] = Counter()
    for episode in trajectories:
        states_seen.update(episode["states"])
        for transition in episode["transitions"]:
            state_action_pairs.add((transition["state"], transition["action"]))
            action_counts[transition["action"]] += 1
            outcome_counts[transition["outcome"]] += 1
    risky_success = outcome_counts.get("risky_success", 0)
    risky_failure = outcome_counts.get("risky_failure", 0)
    risky_total = risky_success + risky_failure
    return {
        "num_episodes": len(trajectories),
        "num_transitions": sum(len(episode["transitions"]) for episode in trajectories),
        "states_seen": sorted(states_seen),
        "state_coverage_fraction": len(states_seen) / len(mdp.states),
        "state_action_pairs_seen": [list(pair) for pair in sorted(state_action_pairs)],
        "state_action_coverage_fraction": len(state_action_pairs) / sum(len(actions) for actions in mdp.actions.values()),
        "action_counts": dict(sorted(action_counts.items())),
        "outcome_counts": dict(sorted(outcome_counts.items())),
        "risky_success_count": risky_success,
        "risky_failure_count": risky_failure,
        "risky_success_rate_observed": risky_success / risky_total if risky_total else None,
    }


def eval_pair_coverage_by_horizon(mdp: MDP, exact_q: QTable) -> Dict[str, Any]:
    horizons = support_horizons(mdp)
    value_counts: Counter[str] = Counter()
    q_counts: Counter[str] = Counter()
    for goal in mdp.states:
        for state in mdp.states:
            if state != goal:
                value_counts[value_horizon_bin(mdp, horizons, exact_q, state, goal)] += 1
    for state in mdp.states:
        for action in mdp.actions.get(state, tuple()):
            for goal in mdp.states:
                if state != goal:
                    q_counts[q_horizon_bin(mdp, horizons, state, action, goal)] += 1
    return {
        "eval_value_pairs_by_horizon_bin": dict(sorted(value_counts.items())),
        "eval_q_pairs_by_horizon_bin": dict(sorted(q_counts.items())),
    }


def serialize_mdp(mdp: MDP) -> Dict[str, Any]:
    return {
        "name": mdp.name,
        "states": list(mdp.states),
        "actions": {state: list(actions) for state, actions in mdp.actions.items()},
        "transitions": {
            f"{state}|{action}": [{"probability": probability, "next_state": next_state} for probability, next_state in outcomes]
            for (state, action), outcomes in mdp.transitions.items()
        },
        "eval_start": mdp.eval_start,
        "eval_goal": mdp.eval_goal,
        "true_risky_success_prob": mdp.true_risky_success_prob,
    }


def serialize_q(mdp: MDP, q_values: QTable) -> Dict[str, Dict[str, Dict[str, float]]]:
    return {
        state: {
            action: {goal: q_values.get((state, action, goal), 0.0) for goal in mdp.states}
            for action in mdp.actions.get(state, tuple())
        }
        for state in mdp.states
    }


def serialize_distance_q(mdp: MDP, q_values: QTable) -> Dict[str, Dict[str, Dict[str, Optional[float]]]]:
    return {
        state: {
            action: {goal: score_to_distance(q_values.get((state, action, goal), 0.0)) for goal in mdp.states}
            for action in mdp.actions.get(state, tuple())
        }
        for state in mdp.states
    }


def serialize_value_distances(values: VTable) -> Dict[str, Dict[str, Optional[float]]]:
    return {goal: {state: score_to_distance(score) for state, score in state_values.items()} for goal, state_values in values.items()}


def run_scenario(mdp: MDP, trajectories: List[Dict[str, Any]]) -> Tuple[Dict[str, Any], Dict[str, Any], Dict[str, Any], Dict[str, Any]]:
    exact_values, exact_q = exact_discounted_reachability_dp(mdp)
    mc_q, _mc_counts, label_coverage = train_mc_supervised(mdp, trajectories)
    successor_baseline_q, _successor_meta = train_successor_distance_trl_log(mdp, trajectories, SUCCESSOR_BASELINE_LAMBDA)
    methods = {
        "mc_supervised": mc_q,
        "trl_raw": train_trl_raw(mdp, trajectories),
        "trl_log": train_trl_log(mdp, trajectories),
        "mc_plus_trl_log": train_mc_plus_trl_log(mdp, trajectories),
        "successor_distance_best_0005": successor_baseline_q,
    }
    uncertainty_meta: Dict[str, Any] = {}
    one_sided_name = alpha_method_name(BEST_0006_ALPHA)
    methods[one_sided_name], uncertainty_meta[one_sided_name] = train_conservative_log_trl(mdp, trajectories, BEST_0006_ALPHA)
    uncertainty_meta[one_sided_name]["source"] = "best_0006_one_sided_comparison"
    for prior_mass in GENERIC_PRIOR_GRID:
        for alpha in GENERIC_ALPHA_GRID:
            method_name = generic_method_name(prior_mass, alpha)
            methods[method_name], uncertainty_meta[method_name] = train_generic_uncertainty_log_trl(mdp, trajectories, prior_mass, alpha)
    metrics = {
        "coverage_diagnostics": coverage_diagnostics(mdp, trajectories),
        "label_or_pair_coverage": {**label_coverage, **eval_pair_coverage_by_horizon(mdp, exact_q)},
        "uncertainty_meta": {
            "successor_distance_best_0005": {"lambda_tr": SUCCESSOR_BASELINE_LAMBDA, "source": "0005_trl_log_equivalent_baseline"},
            **uncertainty_meta,
        },
        "methods": {
            method_name: evaluate_method(mdp, q_values, exact_values, exact_q)
            for method_name, q_values in methods.items()
        },
    }
    diagnostics = {method_name: distance_diagnostics(mdp, trajectories, q_values) for method_name, q_values in methods.items()}
    values = {
        "exact_values": exact_values,
        "exact_q": serialize_q(mdp, exact_q),
        "methods": {
            method_name: {
                "values": values_from_q(mdp, q_values),
                "q": serialize_q(mdp, q_values),
            }
            for method_name, q_values in methods.items()
        },
    }
    successor_tables = {
        "successor_distance_best_0005": {
            "lambda_tr": SUCCESSOR_BASELINE_LAMBDA,
            "q_score": serialize_q(mdp, successor_baseline_q),
            "q_distance": serialize_distance_q(mdp, successor_baseline_q),
            "value_score": values_from_q(mdp, successor_baseline_q),
            "value_distance": serialize_value_distances(values_from_q(mdp, successor_baseline_q)),
        },
    }
    return metrics, values, diagnostics, successor_tables


def flatten_metrics(all_metrics: Mapping[str, Any], distance_diags: Mapping[str, Any]) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for scenario_id, scenario in all_metrics["scenarios"].items():
        coverage = scenario["coverage_diagnostics"]
        for method_name, metrics in scenario["methods"].items():
            diag = distance_diags[scenario_id][method_name]
            meta = scenario.get("uncertainty_meta", {}).get(method_name, {})
            rows.append(
                {
                    "scenario_id": scenario_id,
                    "mdp": scenario["mdp"],
                    "scenario_role": scenario["scenario_role"],
                    "method": method_name,
                    "alpha": meta.get("alpha"),
                    "prior_mass": meta.get("prior_mass"),
                    "penalized_pair_count": len(meta.get("penalized_pairs", {})),
                    "diagnostic_pair_count": len(meta.get("pair_diagnostics", {})),
                    "heldout_long_horizon_value_mse": metrics["heldout_long_horizon_value_mse"],
                    "value_mse": metrics["value_mse"],
                    "value_overestimation_error": metrics["value_overestimation_error"],
                    "value_underestimation_error": metrics["value_underestimation_error"],
                    "q_calibration_error": metrics["q_calibration_error"],
                    "q_overestimation_error": metrics["q_overestimation_error"],
                    "q_underestimation_error": metrics["q_underestimation_error"],
                    "policy_regret": metrics["policy_regret"],
                    "risky_action_selection_rate": metrics["risky_action_selection_rate"],
                    "eval_greedy_action": metrics["eval_greedy_action"],
                    "exact_optimal_action": metrics["exact_optimal_action"],
                    "chose_exact_optimal_action": metrics["chose_exact_optimal_action"],
                    "triangle_violation_rate": diag["triangle_violation_rate"],
                    "triangle_violation_count": diag["triangle_violation_count"],
                    "risky_success_count": coverage["risky_success_count"],
                    "risky_failure_count": coverage["risky_failure_count"],
                    "risky_success_rate_observed": coverage["risky_success_rate_observed"],
                    "learned_risky_q": metrics["eval_start_learned_q"].get("risky"),
                    "learned_safe_q": metrics["eval_start_learned_q"].get("safe"),
                    "exact_risky_q": metrics["eval_start_exact_q"].get("risky"),
                    "exact_safe_q": metrics["eval_start_exact_q"].get("safe"),
                }
            )
    return rows


def write_metrics_csv(path: Path, rows: List[Dict[str, Any]]) -> None:
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def scenario_definitions() -> Dict[str, Tuple[MDP, List[Dict[str, Any]], str]]:
    chain = deterministic_chain()
    safe_matched = risky_shortcut("safe_optimal_matched", 0.25)
    risk_matched = risky_shortcut("risk_optimal_matched", 0.90)
    safe_lucky = risky_shortcut("safe_optimal_lucky_only", 0.25)
    risk_no_success = risky_shortcut("risk_optimal_no_success", 0.90)
    return {
        "chain_len9_holdout": (chain, chain_trajectories(chain), "main_holdout"),
        "safe_optimal_matched": (safe_matched, risky_trajectories(safe_matched, 2, 6, "safe_optimal_matched"), "main_matched"),
        "risk_optimal_matched": (risk_matched, risky_trajectories(risk_matched, 9, 1, "risk_optimal_matched"), "main_matched"),
        "safe_optimal_lucky_only_stress": (safe_lucky, risky_trajectories(safe_lucky, 4, 0, "safe_optimal_lucky_only_stress"), "stress_biased"),
        "risk_optimal_no_success_stress": (risk_no_success, risky_trajectories(risk_no_success, 0, 8, "risk_optimal_no_success_stress"), "stress_biased"),
    }


def main() -> int:
    repo_root = Path(__file__).resolve().parents[4]
    artifact_dir = repo_root / "research" / PROJECT / "artifacts" / EXPERIMENT_ID
    result_dir = repo_root / "research" / PROJECT / "results"
    artifact_dir.mkdir(parents=True, exist_ok=True)
    result_dir.mkdir(parents=True, exist_ok=True)

    scenarios = scenario_definitions()
    all_metrics: Dict[str, Any] = {
        "experiment_id": EXPERIMENT_ID,
        "gamma": GAMMA,
        "update_steps": UPDATE_STEPS,
        "label_horizon_cutoff": LABEL_HORIZON_CUTOFF,
        "generic_prior_grid": list(GENERIC_PRIOR_GRID),
        "generic_alpha_grid": list(GENERIC_ALPHA_GRID),
        "best_0006_alpha": BEST_0006_ALPHA,
        "successor_baseline_lambda": SUCCESSOR_BASELINE_LAMBDA,
        "scenarios": {},
    }
    all_values: Dict[str, Any] = {}
    all_diagnostics: Dict[str, Any] = {}
    all_successor_tables: Dict[str, Any] = {}
    all_coverage: Dict[str, Any] = {}
    all_datasets: Dict[str, Any] = {}
    transition_tables: Dict[str, Any] = {}

    for scenario_id, (mdp, trajectories, role) in scenarios.items():
        metrics, values, diagnostics, successor_tables = run_scenario(mdp, trajectories)
        all_metrics["scenarios"][scenario_id] = {"mdp": mdp.name, "scenario_role": role, **metrics}
        all_values[scenario_id] = values
        all_diagnostics[scenario_id] = diagnostics
        all_successor_tables[scenario_id] = successor_tables
        all_coverage[scenario_id] = metrics["label_or_pair_coverage"]
        all_datasets[scenario_id] = trajectories
        transition_tables[scenario_id] = serialize_mdp(mdp)

    rows = flatten_metrics(all_metrics, all_diagnostics)
    uncertainty_diagnostics = {
        scenario_id: scenario["uncertainty_meta"]
        for scenario_id, scenario in all_metrics["scenarios"].items()
    }
    chain = all_metrics["scenarios"]["chain_len9_holdout"]["methods"]
    safe_matched = all_metrics["scenarios"]["safe_optimal_matched"]["methods"]
    risk_matched = all_metrics["scenarios"]["risk_optimal_matched"]["methods"]
    lucky_stress = all_metrics["scenarios"]["safe_optimal_lucky_only_stress"]["methods"]
    chain_log_mse = chain["trl_log"]["heldout_long_horizon_value_mse"]
    trl_log_lucky_regret = lucky_stress["trl_log"]["policy_regret"]
    trl_log_lucky_over = lucky_stress["trl_log"]["q_overestimation_error"]

    risk_no_success = all_metrics["scenarios"]["risk_optimal_no_success_stress"]["methods"]
    one_sided_name = alpha_method_name(BEST_0006_ALPHA)
    one_sided_lucky = lucky_stress[one_sided_name]
    one_sided_no_success = risk_no_success[one_sided_name]

    generic_summaries = {}
    for prior_mass in GENERIC_PRIOR_GRID:
        for alpha in GENERIC_ALPHA_GRID:
            method_name = generic_method_name(prior_mass, alpha)
            chain_preserved = abs(chain[method_name]["heldout_long_horizon_value_mse"] - chain_log_mse) <= CHAIN_MSE_TOL
            risk_optimal_ok = risk_matched[method_name]["eval_greedy_action"] == "risky" and risk_matched[method_name]["policy_regret"] <= 1e-12
            lucky_regret_reduced = lucky_stress[method_name]["policy_regret"] < trl_log_lucky_regret - 1e-12
            lucky_over_reduced = lucky_stress[method_name]["q_overestimation_error"] < trl_log_lucky_over - 1e-12
            safe_matched_ok = safe_matched[method_name]["eval_greedy_action"] == "safe" and safe_matched[method_name]["policy_regret"] <= 1e-12
            positive = alpha > 0.0 and chain_preserved and risk_optimal_ok and safe_matched_ok and (lucky_regret_reduced or lucky_over_reduced)
            generic_summaries[method_name] = {
                "prior_mass": prior_mass,
                "alpha": alpha,
                "chain_heldout_mse": chain[method_name]["heldout_long_horizon_value_mse"],
                "chain_preserved_near_trl_log": chain_preserved,
                "safe_optimal_lucky_policy_regret": lucky_stress[method_name]["policy_regret"],
                "safe_optimal_lucky_q_overestimation": lucky_stress[method_name]["q_overestimation_error"],
                "lucky_policy_regret_delta_vs_trl_log": lucky_stress[method_name]["policy_regret"] - trl_log_lucky_regret,
                "lucky_q_overestimation_delta_vs_trl_log": lucky_stress[method_name]["q_overestimation_error"] - trl_log_lucky_over,
                "lucky_policy_regret_delta_vs_one_sided_0006": lucky_stress[method_name]["policy_regret"] - one_sided_lucky["policy_regret"],
                "lucky_q_overestimation_delta_vs_one_sided_0006": lucky_stress[method_name]["q_overestimation_error"] - one_sided_lucky["q_overestimation_error"],
                "risk_optimal_matched_action": risk_matched[method_name]["eval_greedy_action"],
                "risk_optimal_matched_policy_regret": risk_matched[method_name]["policy_regret"],
                "risk_optimal_matched_ok": risk_optimal_ok,
                "risk_optimal_no_success_action": risk_no_success[method_name]["eval_greedy_action"],
                "risk_optimal_no_success_policy_regret": risk_no_success[method_name]["policy_regret"],
                "risk_no_success_policy_regret_delta_vs_trl_log": risk_no_success[method_name]["policy_regret"] - risk_no_success["trl_log"]["policy_regret"],
                "risk_no_success_policy_regret_delta_vs_one_sided_0006": risk_no_success[method_name]["policy_regret"] - one_sided_no_success["policy_regret"],
                "safe_optimal_matched_ok": safe_matched_ok,
                "positive_generic_uncertainty_evidence": positive,
            }
    positive_methods = [name for name, item in generic_summaries.items() if item["positive_generic_uncertainty_evidence"]]
    positive_evidence = bool(positive_methods)
    best_positive = positive_methods[0] if positive_methods else None
    chain_raw_valid = chain["trl_raw"]["value_overestimation_error"] < 1e-10 and chain["trl_raw"]["value_underestimation_error"] < 1e-10
    chain_log_valid = chain["trl_log"]["value_overestimation_error"] < 1e-10 and chain["trl_log"]["value_underestimation_error"] < 1e-10
    experiment_completed = chain_raw_valid and chain_log_valid and bool(generic_summaries)

    all_metrics["aggregate"] = {
        "generic_summaries": generic_summaries,
        "positive_generic_uncertainty_evidence": positive_evidence,
        "best_positive_method": best_positive,
        "trl_log_safe_lucky_policy_regret": trl_log_lucky_regret,
        "trl_log_safe_lucky_q_overestimation": trl_log_lucky_over,
        "one_sided_0006_safe_lucky_policy_regret": one_sided_lucky["policy_regret"],
        "one_sided_0006_safe_lucky_q_overestimation": one_sided_lucky["q_overestimation_error"],
        "risk_optimal_no_success_unsolved_by_best_positive": None if best_positive is None else risk_no_success[best_positive]["eval_greedy_action"] != "risky",
    }
    all_metrics["success_checks"] = {
        "chain_raw_exact": chain_raw_valid,
        "chain_trl_log_exact": chain_log_valid,
        "generic_grid_completed": bool(generic_summaries),
        "positive_generic_uncertainty_evidence": positive_evidence,
        "experiment_completed": experiment_completed,
    }

    artifact_paths = [
        f"research/{PROJECT}/artifacts/{EXPERIMENT_ID}/run_generic_uncertainty_audit.py",
        f"research/{PROJECT}/artifacts/{EXPERIMENT_ID}/raw_metrics.json",
        f"research/{PROJECT}/artifacts/{EXPERIMENT_ID}/metrics.csv",
        f"research/{PROJECT}/artifacts/{EXPERIMENT_ID}/uncertainty_grid.json",
        f"research/{PROJECT}/artifacts/{EXPERIMENT_ID}/uncertainty_diagnostics.json",
        f"research/{PROJECT}/artifacts/{EXPERIMENT_ID}/offline_datasets.json",
        f"research/{PROJECT}/artifacts/{EXPERIMENT_ID}/transition_tables.json",
        f"research/{PROJECT}/artifacts/{EXPERIMENT_ID}/value_tables.json",
    ]
    write_json(artifact_dir / "raw_metrics.json", all_metrics)
    write_metrics_csv(artifact_dir / "metrics.csv", rows)
    write_json(
        artifact_dir / "uncertainty_grid.json",
        {
            "prior_grid": list(GENERIC_PRIOR_GRID),
            "alpha_grid": list(GENERIC_ALPHA_GRID),
            "summaries": generic_summaries,
            "best_0006_one_sided_method": one_sided_name,
        },
    )
    write_json(artifact_dir / "uncertainty_diagnostics.json", uncertainty_diagnostics)
    write_json(artifact_dir / "offline_datasets.json", all_datasets)
    write_json(artifact_dir / "transition_tables.json", transition_tables)
    write_json(artifact_dir / "value_tables.json", all_values)

    baseline_metrics = {
        "method": "trl_log",
        "safe_optimal_lucky_only_stress": lucky_stress["trl_log"],
        "risk_optimal_matched": risk_matched["trl_log"],
        "chain_len9_holdout": chain["trl_log"],
    }
    if positive_evidence:
        interpretation = (
            f"{best_positive} reduced safe-optimal lucky-only overestimation versus trl_log while preserving the chain and selecting risky with zero regret in the matched risk-optimal scenario. The risk-optimal no-success stress status is reported separately."
        )
        known_failures: List[str] = []
    else:
        interpretation = (
            "No generic uncertainty setting satisfied all positive checks; the generic posterior did not produce usable evidence on this grid."
        )
        known_failures = ["No generic prior/alpha setting met the positive-evidence criteria."]
    result = {
        "experiment_id": EXPERIMENT_ID,
        "status": "completed" if experiment_completed else "failed",
        "claim_tested": (
            "A generic count-based posterior branch-uncertainty penalty can replace the hand-shaped 0006 shortcut rule while reducing lucky-only overestimation and preserving matched risk-optimal behavior."
        ),
        "commands_run": COMMANDS_RUN,
        "metrics": all_metrics,
        "baseline_metrics": baseline_metrics,
        "artifacts": artifact_paths,
        "interpretation": interpretation,
        "known_failures": known_failures,
        "next_questions": [
            "Can a generic prior preserve multi-step safe routes without also discounting them below lucky shortcuts?",
            "Should no-success risk-optimal regimes be handled by explicit optimistic priors rather than stronger conservative penalties?",
            "Would bootstrap branch uncertainty distinguish deterministic safe routes from all-success risky shortcuts better than the unknown-outcome prior?",
        ],
    }
    write_json(result_dir / f"{EXPERIMENT_ID}_result.json", result)

    summary = f"""# Experiment {EXPERIMENT_ID} Summary

## Objective

Audit a generic count-based posterior uncertainty penalty against the 0006 one-sided conservative rule.

## Commands Run

```bash
{chr(10).join(COMMANDS_RUN)}
```

## Setup

- Discount: `{GAMMA}`
- Label horizon cutoff: `{LABEL_HORIZON_CUTOFF}`
- Fixed backup iterations: `{UPDATE_STEPS}`
- Prior grid: `{list(GENERIC_PRIOR_GRID)}`
- Alpha grid: `{list(GENERIC_ALPHA_GRID)}`
- Generic penalty: interpolate empirical log backup with a Dirichlet unknown-zero posterior lower estimate for state-action counts at least 4.

## Metrics

| Scenario | Method | Prior | Alpha | Held-out MSE | Q calibration | Policy regret | Action | Risky selected |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- | ---: |
"""
    for row in rows:
        summary += (
            f"| {row['scenario_id']} | {row['method']} | {row['prior_mass']} | {row['alpha']} | {row['heldout_long_horizon_value_mse']:.12f} | "
            f"{row['q_calibration_error']:.12f} | {row['policy_regret']:.12f} | {row['eval_greedy_action']} | "
            f"{row['risky_action_selection_rate']:.1f} |\n"
        )
    summary += f"""
## Success Checks

- Chain raw exact: `{chain_raw_valid}`
- Chain TRL-log exact: `{chain_log_valid}`
- Generic grid completed: `{bool(generic_summaries)}`
- Positive generic uncertainty evidence: `{positive_evidence}`
- Best positive method: `{best_positive}`
- Risk-optimal no-success unsolved by best positive: `{all_metrics["aggregate"]["risk_optimal_no_success_unsolved_by_best_positive"]}`

## Interpretation

{interpretation}

## Artifacts

- `research/{PROJECT}/artifacts/{EXPERIMENT_ID}/run_generic_uncertainty_audit.py`
- `research/{PROJECT}/artifacts/{EXPERIMENT_ID}/raw_metrics.json`
- `research/{PROJECT}/artifacts/{EXPERIMENT_ID}/metrics.csv`
- `research/{PROJECT}/artifacts/{EXPERIMENT_ID}/uncertainty_grid.json`
- `research/{PROJECT}/artifacts/{EXPERIMENT_ID}/uncertainty_diagnostics.json`
- `research/{PROJECT}/artifacts/{EXPERIMENT_ID}/offline_datasets.json`
- `research/{PROJECT}/artifacts/{EXPERIMENT_ID}/transition_tables.json`
- `research/{PROJECT}/artifacts/{EXPERIMENT_ID}/value_tables.json`

## Known Failures

{chr(10).join(f"- {failure}" for failure in known_failures) if known_failures else "- None."}
"""
    (result_dir / f"{EXPERIMENT_ID}_summary.md").write_text(summary)
    print(json.dumps(all_metrics["success_checks"], indent=2, sort_keys=True))
    return 0 if experiment_completed else 1


if __name__ == "__main__":
    raise SystemExit(main())
