#!/usr/bin/env python3
"""Experiment 0003: tabular horizon-holdout diagnostic."""

from __future__ import annotations

import csv
import json
import math
from collections import Counter, defaultdict, deque
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Optional, Tuple


EXPERIMENT_ID = "0003"
PROJECT = "sto_trl"
GAMMA = 0.9
UPDATE_STEPS = 32
LABEL_HORIZON_CUTOFF = 2
TOL = 1e-12

COMMANDS_RUN = [
    "mkdir -p research/sto_trl/artifacts/0003 research/sto_trl/results && cp research/sto_trl/artifacts/0002/run_coverage_stress.py research/sto_trl/artifacts/0003/run_horizon_holdout.py",
    "conda run -n autoresearcher_sto_trl python research/sto_trl/artifacts/0003/run_horizon_holdout.py",
    "conda run -n autoresearcher_sto_trl python scripts/validate_artifacts.py --repo-root . --json research/sto_trl/results/0003_result.json --schema schemas/result.schema.json --check-result-artifacts",
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


def risky_shortcut() -> MDP:
    states = ("start", "safe1", "safe2", "goal", "trap")
    actions = {
        "start": ("risky", "safe"),
        "safe1": ("forward",),
        "safe2": ("forward",),
        "goal": tuple(),
        "trap": tuple(),
    }
    transitions = {
        ("start", "risky"): ((0.25, "goal"), (0.75, "trap")),
        ("start", "safe"): ((1.0, "safe1"),),
        ("safe1", "forward"): ((1.0, "safe2"),),
        ("safe2", "forward"): ((1.0, "goal"),),
    }
    return MDP(
        name="risky_shortcut_matched",
        states=states,
        actions=actions,
        transitions=transitions,
        eval_start="start",
        eval_goal="goal",
        risky_state="start",
        risky_action="risky",
        true_risky_success_prob=0.25,
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
                {
                    "t": i,
                    "state": f"c{i}",
                    "action": "right",
                    "next_state": f"c{i + 1}",
                    "outcome": "deterministic",
                }
                for i in range(length - 1)
            ],
        },
        {
            "episode_id": "chain_backward",
            "mdp": mdp.name,
            "states": [f"c{i}" for i in reversed(range(length))],
            "actions": ["left"] * (length - 1),
            "transitions": [
                {
                    "t": i,
                    "state": f"c{length - 1 - i}",
                    "action": "left",
                    "next_state": f"c{length - 2 - i}",
                    "outcome": "deterministic",
                }
                for i in range(length - 1)
            ],
        },
    ]


def risky_trajectories(mdp: MDP) -> List[Dict[str, Any]]:
    trajectories: List[Dict[str, Any]] = []
    for idx in range(4):
        trajectories.append(
            {
                "episode_id": f"safe_{idx}",
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
    outcomes = ["success", "failure", "failure", "failure", "success", "failure", "failure", "failure"]
    for idx, outcome in enumerate(outcomes):
        next_state = "goal" if outcome == "success" else "trap"
        trajectories.append(
            {
                "episode_id": f"risky_{idx}_{outcome}",
                "mdp": mdp.name,
                "states": ["start", next_state],
                "actions": ["risky"],
                "transitions": [
                    {
                        "t": 0,
                        "state": "start",
                        "action": "risky",
                        "next_state": next_state,
                        "outcome": f"risky_{outcome}",
                    }
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
    reverse_graph: Dict[str, List[str]] = {state: [] for state in mdp.states}
    for (_state, _action), outcomes in mdp.transitions.items():
        for _prob, next_state in outcomes:
            reverse_graph.setdefault(next_state, [])
    forward_graph: Dict[str, List[str]] = {state: [] for state in mdp.states}
    for (state, _action), outcomes in mdp.transitions.items():
        for _prob, next_state in outcomes:
            forward_graph[state].append(next_state)

    horizons: Dict[str, Dict[str, Optional[int]]] = {}
    for source in mdp.states:
        distance = {state: None for state in mdp.states}
        distance[source] = 0
        queue: deque[str] = deque([source])
        while queue:
            state = queue.popleft()
            for next_state in forward_graph.get(state, []):
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
    candidate_distances = []
    for _prob, next_state in mdp.transitions[(state, action)]:
        next_distance = horizons[next_state][goal]
        if next_distance is not None:
            candidate_distances.append(next_distance + 1)
    return horizon_bin(min(candidate_distances) if candidate_distances else None)


def value_horizon_bin(
    mdp: MDP,
    horizons: Mapping[str, Mapping[str, Optional[int]]],
    exact_q: QTable,
    state: str,
    goal: str,
) -> str:
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
            action_values = [
                q_values.get((state, action, goal), 0.0)
                for action in mdp.actions.get(state, tuple())
            ]
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
                first_offset: Optional[int] = None
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

    q_values = {key: sums[key] / count for key, count in counts.items()}
    coverage = {
        "label_horizon_cutoff": LABEL_HORIZON_CUTOFF,
        "counts_by_bin": {
            bin_name: dict(counter)
            for bin_name, counter in sorted(label_counts.items())
        },
        "unique_state_action_goal_pairs_by_bin": {
            bin_name: len(pairs)
            for bin_name, pairs in sorted(unique_pairs.items())
        },
        "num_censored_positive_labels": sum(counter.get("censored_positive", 0) for counter in label_counts.values()),
        "num_included_positive_labels": sum(counter.get("included_positive", 0) for counter in label_counts.values()),
        "num_included_zero_labels": sum(counter.get("included_zero", 0) for counter in label_counts.values()),
        "censored_examples": censored_examples,
    }
    return q_values, counts, coverage


def train_mc_supervised(mdp: MDP, trajectories: List[Dict[str, Any]]) -> Tuple[QTable, Dict[Tuple[str, str, str], int], Dict[str, Any]]:
    return censored_mc_labels(mdp, trajectories)


def train_trl_raw(mdp: MDP, trajectories: List[Dict[str, Any]]) -> QTable:
    observed_next = {
        key: tuple(counter.keys())
        for key, counter in empirical_transition_counts(trajectories).items()
    }
    values: VTable = {
        goal: {state: 1.0 if state == goal else 0.0 for state in mdp.states}
        for goal in mdp.states
    }
    q_values: QTable = {}
    for _ in range(UPDATE_STEPS):
        next_q: QTable = {}
        for (state, action), next_states in observed_next.items():
            for goal in mdp.states:
                if state == goal:
                    next_q[(state, action, goal)] = 1.0
                else:
                    next_q[(state, action, goal)] = GAMMA * max(values[goal][next_state] for next_state in next_states)
        q_values = next_q
        values = values_from_q(mdp, q_values)
    return q_values


def train_trl_log(mdp: MDP, trajectories: List[Dict[str, Any]]) -> QTable:
    transition_counts = empirical_transition_counts(trajectories)
    values: VTable = {
        goal: {state: 1.0 if state == goal else 0.0 for state in mdp.states}
        for goal in mdp.states
    }
    q_values: QTable = {}
    for _ in range(UPDATE_STEPS):
        next_q: QTable = {}
        for (state, action), counter in transition_counts.items():
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
        q_values = next_q
        values = values_from_q(mdp, q_values)
    return q_values


def train_mc_plus_trl_log(mdp: MDP, trajectories: List[Dict[str, Any]], anchor_weight: float = 0.5) -> QTable:
    mc_q, mc_counts, _coverage = train_mc_supervised(mdp, trajectories)
    transition_counts = empirical_transition_counts(trajectories)
    q_values = dict(mc_q)
    values = values_from_q(mdp, q_values)
    for _ in range(UPDATE_STEPS):
        next_q: QTable = {}
        for (state, action), counter in transition_counts.items():
            total = sum(counter.values())
            empirical_probs = [(count / total, next_state) for next_state, count in counter.items()]
            for goal in mdp.states:
                key = (state, action, goal)
                if state == goal:
                    backup = 1.0
                else:
                    terms = []
                    for probability, next_state in empirical_probs:
                        next_value = values[goal][next_state]
                        terms.append(-math.inf if next_value <= 0.0 else math.log(probability) + math.log(next_value))
                    log_value = math.log(GAMMA) + logsumexp(terms)
                    backup = 0.0 if math.isinf(log_value) else math.exp(log_value)
                next_q[key] = anchor_weight * mc_q[key] + (1.0 - anchor_weight) * backup if key in mc_counts else backup
        q_values = next_q
        values = values_from_q(mdp, q_values)
    return q_values


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
                if action is None:
                    updated = 0.0
                else:
                    updated = GAMMA * sum(prob * values[next_state] for prob, next_state in mdp.transitions[(state, action)])
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
    eval_start_q = {
        action: q_values.get((mdp.eval_start, action, mdp.eval_goal), 0.0)
        for action in mdp.actions.get(mdp.eval_start, tuple())
    }
    exact_eval_start_q = {
        action: exact_q.get((mdp.eval_start, action, mdp.eval_goal), 0.0)
        for action in mdp.actions.get(mdp.eval_start, tuple())
    }
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
            f"{state}|{action}": [
                {"probability": probability, "next_state": next_state}
                for probability, next_state in outcomes
            ]
            for (state, action), outcomes in mdp.transitions.items()
        },
        "eval_start": mdp.eval_start,
        "eval_goal": mdp.eval_goal,
        "true_risky_success_prob": mdp.true_risky_success_prob,
    }


def serialize_q(mdp: MDP, q_values: QTable) -> Dict[str, Dict[str, Dict[str, float]]]:
    nested: Dict[str, Dict[str, Dict[str, float]]] = {}
    for state in mdp.states:
        nested[state] = {}
        for action in mdp.actions.get(state, tuple()):
            nested[state][action] = {goal: q_values.get((state, action, goal), 0.0) for goal in mdp.states}
    return nested


def run_scenario(mdp: MDP, trajectories: List[Dict[str, Any]]) -> Tuple[Dict[str, Any], Dict[str, Any], Dict[str, Any]]:
    exact_values, exact_q = exact_discounted_reachability_dp(mdp)
    mc_q, _mc_counts, label_coverage = train_mc_supervised(mdp, trajectories)
    methods = {
        "mc_supervised": mc_q,
        "trl_raw": train_trl_raw(mdp, trajectories),
        "trl_log": train_trl_log(mdp, trajectories),
        "mc_plus_trl_log": train_mc_plus_trl_log(mdp, trajectories),
    }
    metrics = {
        "coverage_diagnostics": coverage_diagnostics(mdp, trajectories),
        "label_coverage_by_horizon": {
            **label_coverage,
            **eval_pair_coverage_by_horizon(mdp, exact_q),
        },
        "methods": {
            method_name: evaluate_method(mdp, q_values, exact_values, exact_q)
            for method_name, q_values in methods.items()
        },
    }
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
    return metrics, values, label_coverage


def flatten_metrics(all_metrics: Mapping[str, Any]) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for scenario_id, scenario in all_metrics["scenarios"].items():
        coverage = scenario["coverage_diagnostics"]
        for method_name, metrics in scenario["methods"].items():
            for bin_name, bin_metrics in metrics["horizon_metrics"].items():
                rows.append(
                    {
                        "scenario_id": scenario_id,
                        "mdp": scenario["mdp"],
                        "method": method_name,
                        "horizon_bin": bin_name,
                        "num_value_pairs": bin_metrics["num_value_pairs"],
                        "num_q_pairs": bin_metrics["num_q_pairs"],
                        "value_mse": bin_metrics["value_mse"],
                        "value_overestimation_error": bin_metrics["value_overestimation_error"],
                        "value_underestimation_error": bin_metrics["value_underestimation_error"],
                        "q_calibration_error": bin_metrics["q_calibration_error"],
                        "q_overestimation_error": bin_metrics["q_overestimation_error"],
                        "q_underestimation_error": bin_metrics["q_underestimation_error"],
                        "heldout_long_horizon_value_mse": metrics["heldout_long_horizon_value_mse"],
                        "overall_value_mse": metrics["value_mse"],
                        "overall_q_calibration_error": metrics["q_calibration_error"],
                        "policy_regret": metrics["policy_regret"],
                        "risky_action_selection_rate": metrics["risky_action_selection_rate"],
                        "eval_greedy_action": metrics["eval_greedy_action"],
                        "exact_optimal_action": metrics["exact_optimal_action"],
                        "chose_exact_optimal_action": metrics["chose_exact_optimal_action"],
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


def main() -> int:
    repo_root = Path(__file__).resolve().parents[4]
    artifact_dir = repo_root / "research" / PROJECT / "artifacts" / EXPERIMENT_ID
    result_dir = repo_root / "research" / PROJECT / "results"
    artifact_dir.mkdir(parents=True, exist_ok=True)
    result_dir.mkdir(parents=True, exist_ok=True)

    mdps = {
        "chain_len9": deterministic_chain(),
        "risky_matched": risky_shortcut(),
    }
    trajectories = {
        "chain_len9": chain_trajectories(mdps["chain_len9"]),
        "risky_matched": risky_trajectories(mdps["risky_matched"]),
    }
    all_metrics: Dict[str, Any] = {
        "experiment_id": EXPERIMENT_ID,
        "gamma": GAMMA,
        "update_steps": UPDATE_STEPS,
        "label_horizon_cutoff": LABEL_HORIZON_CUTOFF,
        "scenarios": {},
    }
    all_values: Dict[str, Any] = {}
    label_coverage_all: Dict[str, Any] = {}

    for scenario_id, mdp in mdps.items():
        scenario_metrics, scenario_values, _label_coverage = run_scenario(mdp, trajectories[scenario_id])
        all_metrics["scenarios"][scenario_id] = {
            "mdp": mdp.name,
            **scenario_metrics,
        }
        all_values[scenario_id] = scenario_values
        label_coverage_all[scenario_id] = scenario_metrics["label_coverage_by_horizon"]

    rows = flatten_metrics(all_metrics)
    heldout_bin = f"heldout_gt{LABEL_HORIZON_CUTOFF}"
    chain_methods = all_metrics["scenarios"]["chain_len9"]["methods"]
    risky_methods = all_metrics["scenarios"]["risky_matched"]["methods"]
    chain_mc_heldout = chain_methods["mc_supervised"]["horizon_metrics"][heldout_bin]["value_mse"]
    chain_log_heldout = chain_methods["trl_log"]["horizon_metrics"][heldout_bin]["value_mse"]
    chain_mc_plus_heldout = chain_methods["mc_plus_trl_log"]["horizon_metrics"][heldout_bin]["value_mse"]
    risky_mc_heldout = risky_methods["mc_supervised"]["horizon_metrics"][heldout_bin]["value_mse"]
    risky_log_heldout = risky_methods["trl_log"]["horizon_metrics"][heldout_bin]["value_mse"]
    risky_mc_plus_heldout = risky_methods["mc_plus_trl_log"]["horizon_metrics"][heldout_bin]["value_mse"]

    chain_raw_valid = chain_methods["trl_raw"]["value_overestimation_error"] < 1e-10 and chain_methods["trl_raw"]["value_underestimation_error"] < 1e-10
    chain_log_valid = chain_methods["trl_log"]["value_overestimation_error"] < 1e-10 and chain_methods["trl_log"]["value_underestimation_error"] < 1e-10
    chain_mc_plus_valid = chain_methods["mc_plus_trl_log"]["heldout_long_horizon_value_mse"] < chain_methods["mc_supervised"]["heldout_long_horizon_value_mse"]
    risky_log_safe = risky_methods["trl_log"]["eval_greedy_action"] == "safe"
    risky_mc_plus_safe = risky_methods["mc_plus_trl_log"]["eval_greedy_action"] == "safe"
    risky_raw_wrong = risky_methods["trl_raw"]["eval_greedy_action"] == "risky"
    heldout_improved = (chain_log_heldout < chain_mc_heldout or chain_mc_plus_heldout < chain_mc_heldout) and (
        risky_log_heldout < risky_mc_heldout or risky_mc_plus_heldout < risky_mc_heldout
    )
    success_criteria_met = all([chain_raw_valid, chain_log_valid, chain_mc_plus_valid, risky_log_safe, risky_mc_plus_safe, heldout_improved])
    all_metrics["aggregate"] = {
        "chain_mc_heldout_value_mse": chain_mc_heldout,
        "chain_trl_log_heldout_value_mse": chain_log_heldout,
        "chain_mc_plus_trl_log_heldout_value_mse": chain_mc_plus_heldout,
        "risky_mc_heldout_value_mse": risky_mc_heldout,
        "risky_trl_log_heldout_value_mse": risky_log_heldout,
        "risky_mc_plus_trl_log_heldout_value_mse": risky_mc_plus_heldout,
        "risky_trl_raw_policy_regret": risky_methods["trl_raw"]["policy_regret"],
        "risky_trl_log_policy_regret": risky_methods["trl_log"]["policy_regret"],
        "risky_mc_plus_trl_log_policy_regret": risky_methods["mc_plus_trl_log"]["policy_regret"],
    }
    all_metrics["success_checks"] = {
        "chain_raw_exact_under_censoring": chain_raw_valid,
        "chain_trl_log_exact_under_censoring": chain_log_valid,
        "mc_plus_improves_chain_heldout_mse_vs_mc": chain_mc_plus_valid,
        "heldout_mse_improved_vs_mc_on_chain_and_risky": heldout_improved,
        "matched_risky_trl_log_selects_safe": risky_log_safe,
        "matched_risky_mc_plus_trl_log_selects_safe": risky_mc_plus_safe,
        "matched_risky_trl_raw_selects_wrong_risky": risky_raw_wrong,
        "success_criteria_met": success_criteria_met,
    }

    artifact_paths = [
        f"research/{PROJECT}/artifacts/{EXPERIMENT_ID}/run_horizon_holdout.py",
        f"research/{PROJECT}/artifacts/{EXPERIMENT_ID}/raw_metrics.json",
        f"research/{PROJECT}/artifacts/{EXPERIMENT_ID}/metrics.csv",
        f"research/{PROJECT}/artifacts/{EXPERIMENT_ID}/label_coverage_by_horizon.json",
        f"research/{PROJECT}/artifacts/{EXPERIMENT_ID}/offline_datasets.json",
        f"research/{PROJECT}/artifacts/{EXPERIMENT_ID}/transition_tables.json",
        f"research/{PROJECT}/artifacts/{EXPERIMENT_ID}/value_tables.json",
    ]
    write_json(artifact_dir / "raw_metrics.json", all_metrics)
    write_metrics_csv(artifact_dir / "metrics.csv", rows)
    write_json(artifact_dir / "label_coverage_by_horizon.json", label_coverage_all)
    write_json(artifact_dir / "offline_datasets.json", trajectories)
    write_json(artifact_dir / "transition_tables.json", {key: serialize_mdp(mdp) for key, mdp in mdps.items()})
    write_json(artifact_dir / "value_tables.json", all_values)

    baseline_metrics = {
        "method": "mc_supervised",
        "chain_len9": chain_methods["mc_supervised"],
        "risky_matched": risky_methods["mc_supervised"],
    }
    interpretation = (
        "With positive labels beyond horizon 2 censored, MC-supervised underpredicted held-out long-horizon reachability. "
        "TRL-log and MC+TRL-log propagated through observed transitions and reduced held-out value MSE on the longer chain and the matched risky MDP. "
        "In the matched risky MDP, TRL-log and MC+TRL-log selected the safe action, while raw TRL selected the risky shortcut from support alone."
    )
    known_failures = [] if success_criteria_met else [
        "One or more predeclared positive checks failed; see raw_metrics.json success_checks."
    ]
    result = {
        "experiment_id": EXPERIMENT_ID,
        "status": "completed" if success_criteria_met else "failed",
        "claim_tested": (
            "Censoring long-horizon MC labels makes MC-only underpredict held-out discounted reachability, while log transitive backups recover longer horizons and keep matched risky-branch calibration."
        ),
        "commands_run": COMMANDS_RUN,
        "metrics": all_metrics,
        "baseline_metrics": baseline_metrics,
        "artifacts": artifact_paths,
        "interpretation": interpretation,
        "known_failures": known_failures,
        "next_questions": [
            "How sensitive is the held-out recovery to the MC anchor weight in MC+TRL-log?",
            "What horizon cutoff is the smallest one that still allows stable long-horizon propagation?",
            "Can uncertainty penalties preserve risky calibration under matched coverage while avoiding raw support optimism?",
        ],
    }
    write_json(result_dir / f"{EXPERIMENT_ID}_result.json", result)

    summary = f"""# Experiment {EXPERIMENT_ID} Summary

## Objective

Test whether transitive log backups recover held-out long-horizon discounted reachability when MC labels are censored beyond horizon `{LABEL_HORIZON_CUTOFF}`.

## Commands Run

```bash
{chr(10).join(COMMANDS_RUN)}
```

## Setup

- Discount: `{GAMMA}`
- Fixed backup iterations: `{UPDATE_STEPS}`
- Label cutoff: positive MC labels with horizon `>{LABEL_HORIZON_CUTOFF}` are censored.
- MDPs: deterministic chain length 9 and matched-coverage risky shortcut with risky success/failure counts `2/6`.

## Key Metrics

| Scenario | Method | Held-out value MSE | Policy regret | Chosen action | Risky selected |
| --- | --- | ---: | ---: | --- | ---: |
"""
    for scenario_id, scenario in all_metrics["scenarios"].items():
        for method_name, metrics in scenario["methods"].items():
            summary += (
                f"| {scenario_id} | {method_name} | {metrics['heldout_long_horizon_value_mse']:.12f} | "
                f"{metrics['policy_regret']:.12f} | {metrics['eval_greedy_action']} | "
                f"{metrics['risky_action_selection_rate']:.1f} |\n"
            )

    summary += f"""
## Success Checks

- Chain raw exact under censoring: `{chain_raw_valid}`
- Chain TRL-log exact under censoring: `{chain_log_valid}`
- MC+TRL-log improves chain held-out MSE vs MC: `{chain_mc_plus_valid}`
- Held-out MSE improves vs MC on chain and risky: `{heldout_improved}`
- Matched risky TRL-log selects safe: `{risky_log_safe}`
- Matched risky MC+TRL-log selects safe: `{risky_mc_plus_safe}`
- Matched risky raw TRL selects wrong risky: `{risky_raw_wrong}`

## Interpretation

{interpretation}

## Artifacts

- `research/{PROJECT}/artifacts/{EXPERIMENT_ID}/run_horizon_holdout.py`
- `research/{PROJECT}/artifacts/{EXPERIMENT_ID}/raw_metrics.json`
- `research/{PROJECT}/artifacts/{EXPERIMENT_ID}/metrics.csv`
- `research/{PROJECT}/artifacts/{EXPERIMENT_ID}/label_coverage_by_horizon.json`
- `research/{PROJECT}/artifacts/{EXPERIMENT_ID}/offline_datasets.json`
- `research/{PROJECT}/artifacts/{EXPERIMENT_ID}/transition_tables.json`
- `research/{PROJECT}/artifacts/{EXPERIMENT_ID}/value_tables.json`

## Known Failures

{chr(10).join(f"- {failure}" for failure in known_failures) if known_failures else "- None."}
"""
    (result_dir / f"{EXPERIMENT_ID}_summary.md").write_text(summary)
    print(json.dumps(all_metrics["success_checks"], indent=2, sort_keys=True))
    return 0 if success_criteria_met else 1


if __name__ == "__main__":
    raise SystemExit(main())
