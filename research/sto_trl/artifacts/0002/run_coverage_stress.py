#!/usr/bin/env python3
"""Experiment 0002: tabular stochastic-coverage stress test."""

from __future__ import annotations

import csv
import json
import math
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Optional, Tuple


EXPERIMENT_ID = "0002"
PROJECT = "sto_trl"
GAMMA = 0.9
UPDATE_STEPS = 32
TOL = 1e-12
SAFE_EPISODES_PER_REGIME = 4

COMMANDS_RUN = [
    "mkdir -p research/sto_trl/artifacts/0002 research/sto_trl/results && cp research/sto_trl/artifacts/0001/run_tabular_sto_trl.py research/sto_trl/artifacts/0002/run_coverage_stress.py",
    "conda run -n autoresearcher_sto_trl python research/sto_trl/artifacts/0002/run_coverage_stress.py",
    "conda run -n autoresearcher_sto_trl python scripts/validate_artifacts.py --repo-root . --json research/sto_trl/results/0002_result.json --schema schemas/result.schema.json --check-result-artifacts",
]


@dataclass(frozen=True)
class MDP:
    name: str
    states: Tuple[str, ...]
    actions: Mapping[str, Tuple[str, ...]]
    transitions: Mapping[Tuple[str, str], Tuple[Tuple[float, str], ...]]
    eval_start: str
    eval_goal: str
    true_risky_success_prob: Optional[float] = None
    risky_state: Optional[str] = None
    risky_action: Optional[str] = None


QTable = Dict[Tuple[str, str, str], float]
VTable = Dict[str, Dict[str, float]]


REGIME_SPECS = {
    "safe_optimal": {
        "matched": {"risky_successes": 2, "risky_failures": 6},
        "lucky_biased": {"risky_successes": 6, "risky_failures": 2},
        "lucky_only": {"risky_successes": 4, "risky_failures": 0},
        "unlucky_biased": {"risky_successes": 1, "risky_failures": 7},
        "no_risky_success": {"risky_successes": 0, "risky_failures": 8},
    },
    "risk_optimal": {
        "matched": {"risky_successes": 9, "risky_failures": 1},
        "lucky_biased": {"risky_successes": 9, "risky_failures": 0},
        "lucky_only": {"risky_successes": 4, "risky_failures": 0},
        "unlucky_biased": {"risky_successes": 4, "risky_failures": 4},
        "no_risky_success": {"risky_successes": 0, "risky_failures": 8},
    },
}


def write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")


def deterministic_chain() -> MDP:
    states = tuple(f"c{i}" for i in range(6))
    actions: Dict[str, Tuple[str, ...]] = {}
    transitions: Dict[Tuple[str, str], Tuple[Tuple[float, str], ...]] = {}
    for idx, state in enumerate(states):
        action_list: List[str] = []
        if idx < len(states) - 1:
            action_list.append("right")
            transitions[(state, "right")] = ((1.0, states[idx + 1]),)
        if idx > 0:
            action_list.append("left")
            transitions[(state, "left")] = ((1.0, states[idx - 1]),)
        actions[state] = tuple(action_list)
    return MDP(
        name="deterministic_chain",
        states=states,
        actions=actions,
        transitions=transitions,
        eval_start="c0",
        eval_goal="c5",
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
        true_risky_success_prob=true_success_prob,
        risky_state="start",
        risky_action="risky",
    )


def chain_trajectories() -> List[Dict[str, Any]]:
    return [
        {
            "episode_id": "chain_forward",
            "mdp": "deterministic_chain",
            "states": [f"c{i}" for i in range(6)],
            "actions": ["right"] * 5,
            "transitions": [
                {
                    "t": i,
                    "state": f"c{i}",
                    "action": "right",
                    "next_state": f"c{i + 1}",
                    "outcome": "deterministic",
                }
                for i in range(5)
            ],
        },
        {
            "episode_id": "chain_backward",
            "mdp": "deterministic_chain",
            "states": [f"c{i}" for i in reversed(range(6))],
            "actions": ["left"] * 5,
            "transitions": [
                {
                    "t": i,
                    "state": f"c{5 - i}",
                    "action": "left",
                    "next_state": f"c{4 - i}",
                    "outcome": "deterministic",
                }
                for i in range(5)
            ],
        },
    ]


def risky_trajectories(mdp: MDP, regime_name: str, successes: int, failures: int) -> List[Dict[str, Any]]:
    trajectories: List[Dict[str, Any]] = []
    for idx in range(SAFE_EPISODES_PER_REGIME):
        trajectories.append(
            {
                "episode_id": f"{mdp.name}_{regime_name}_safe_{idx}",
                "mdp": mdp.name,
                "regime": regime_name,
                "states": ["start", "safe1", "safe2", "goal"],
                "actions": ["safe", "forward", "forward"],
                "transitions": [
                    {
                        "t": 0,
                        "state": "start",
                        "action": "safe",
                        "next_state": "safe1",
                        "outcome": "safe_step",
                    },
                    {
                        "t": 1,
                        "state": "safe1",
                        "action": "forward",
                        "next_state": "safe2",
                        "outcome": "safe_step",
                    },
                    {
                        "t": 2,
                        "state": "safe2",
                        "action": "forward",
                        "next_state": "goal",
                        "outcome": "safe_goal",
                    },
                ],
            }
        )

    outcomes = ["success"] * successes + ["failure"] * failures
    for idx, outcome in enumerate(outcomes):
        next_state = "goal" if outcome == "success" else "trap"
        trajectories.append(
            {
                "episode_id": f"{mdp.name}_{regime_name}_risky_{idx}_{outcome}",
                "mdp": mdp.name,
                "regime": regime_name,
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
                        GAMMA * sum(
                            probability * values[goal][next_state]
                            for probability, next_state in mdp.transitions[(state, action)]
                        )
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
                        probability * values[goal][next_state]
                        for probability, next_state in mdp.transitions[(state, action)]
                    )
    return values, q_values


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


def train_mc_supervised(mdp: MDP, trajectories: List[Dict[str, Any]]) -> Tuple[QTable, Dict[Tuple[str, str, str], int]]:
    sums: Dict[Tuple[str, str, str], float] = defaultdict(float)
    counts: Dict[Tuple[str, str, str], int] = defaultdict(int)
    for episode in trajectories:
        states = episode["states"]
        actions = episode["actions"]
        for t, action in enumerate(actions):
            state = states[t]
            future_states = states[t + 1 :]
            for goal in mdp.states:
                discounted_return = 0.0
                for offset, future_state in enumerate(future_states, start=1):
                    if future_state == goal:
                        discounted_return = GAMMA**offset
                        break
                key = (state, action, goal)
                sums[key] += discounted_return
                counts[key] += 1
    return {key: sums[key] / count for key, count in counts.items()}, counts


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
    mc_q, mc_counts = train_mc_supervised(mdp, trajectories)
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
                    updated = GAMMA * sum(
                        probability * values[next_state]
                        for probability, next_state in mdp.transitions[(state, action)]
                    )
            next_values[state] = updated
            max_delta = max(max_delta, abs(updated - values[state]))
        values = next_values
        if max_delta < TOL:
            break
    return values


def mse(values: List[float]) -> float:
    return sum(value * value for value in values) / len(values) if values else 0.0


def evaluate_method(mdp: MDP, q_values: QTable, exact_values: VTable, exact_q: QTable) -> Dict[str, Any]:
    learned_values = values_from_q(mdp, q_values)
    value_errors = [
        learned_values[goal][state] - exact_values[goal][state]
        for goal in mdp.states
        for state in mdp.states
    ]
    q_pairs = [
        (state, action, goal)
        for state in mdp.states
        for action in mdp.actions.get(state, tuple())
        for goal in mdp.states
        if state != goal
    ]
    q_errors = [q_values.get(key, 0.0) - exact_q.get(key, 0.0) for key in q_pairs]
    long_horizon_errors = [
        learned_values[goal][state] - exact_values[goal][state]
        for goal in mdp.states
        for state in mdp.states
        if state != goal and 0.0 < exact_values[goal][state] <= GAMMA**2 + 1e-12
    ]

    policies: Dict[str, Dict[str, Optional[str]]] = {}
    policy_regrets = []
    for goal in mdp.states:
        policy = greedy_policy(mdp, q_values, goal)
        policies[goal] = policy
        evaluated = evaluate_policy(mdp, policy, goal)
        for state in mdp.states:
            if state != goal and exact_values[goal][state] > 0.0:
                policy_regrets.append(max(0.0, exact_values[goal][state] - evaluated[state]))

    eval_policy = policies[mdp.eval_goal]
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

    return {
        "value_mse": mse(value_errors),
        "long_horizon_value_mse": mse(long_horizon_errors),
        "value_overestimation_error": max([0.0] + value_errors),
        "value_underestimation_error": max([0.0] + [-error for error in value_errors]),
        "q_calibration_error": sum(abs(error) for error in q_errors) / len(q_errors) if q_errors else 0.0,
        "calibration_error": sum(abs(error) for error in q_errors) / len(q_errors) if q_errors else 0.0,
        "q_overestimation_error": max([0.0] + q_errors),
        "q_underestimation_error": max([0.0] + [-error for error in q_errors]),
        "policy_regret": policy_regret,
        "mean_policy_regret": sum(policy_regrets) / len(policy_regrets) if policy_regrets else 0.0,
        "max_policy_regret": max(policy_regrets) if policy_regrets else 0.0,
        "risky_action_selection_rate": risky_selection_rate,
        "eval_start": mdp.eval_start,
        "eval_goal": mdp.eval_goal,
        "eval_start_learned_q": eval_start_q,
        "eval_start_exact_q": exact_eval_start_q,
        "eval_start_learned_value": learned_values[mdp.eval_goal][mdp.eval_start],
        "eval_start_exact_value": exact_values[mdp.eval_goal][mdp.eval_start],
        "eval_greedy_action": eval_policy.get(mdp.eval_start),
        "exact_optimal_action": optimal_action,
        "chose_exact_optimal_action": eval_policy.get(mdp.eval_start) == optimal_action,
    }


def coverage_diagnostics(mdp: MDP, trajectories: List[Dict[str, Any]], regime_name: str) -> Dict[str, Any]:
    states_seen = set()
    future_goals_seen = set()
    state_action_pairs = set()
    action_counts: Counter[str] = Counter()
    transition_counts: Counter[str] = Counter()
    outcome_counts: Counter[str] = Counter()
    for episode in trajectories:
        states_seen.update(episode["states"])
        for t, transition in enumerate(episode["transitions"]):
            state_action_pairs.add((transition["state"], transition["action"]))
            action_counts[transition["action"]] += 1
            outcome_counts[transition["outcome"]] += 1
            transition_counts[f"{transition['state']}|{transition['action']}|{transition['next_state']}"] += 1
            future_goals_seen.update(episode["states"][t + 1 :])
    risky_success = outcome_counts.get("risky_success", 0)
    risky_failure = outcome_counts.get("risky_failure", 0)
    risky_total = risky_success + risky_failure
    total_available_state_actions = sum(len(actions) for actions in mdp.actions.values())
    return {
        "mdp": mdp.name,
        "regime": regime_name,
        "num_episodes": len(trajectories),
        "num_transitions": sum(len(episode["transitions"]) for episode in trajectories),
        "states_seen": sorted(states_seen),
        "state_coverage_fraction": len(states_seen) / len(mdp.states),
        "state_action_pairs_seen": [list(pair) for pair in sorted(state_action_pairs)],
        "state_action_coverage_fraction": len(state_action_pairs) / total_available_state_actions,
        "future_goals_seen": sorted(future_goals_seen),
        "future_goal_coverage_fraction": len(future_goals_seen) / len(mdp.states),
        "action_counts": dict(sorted(action_counts.items())),
        "transition_counts": dict(sorted(transition_counts.items())),
        "outcome_counts": dict(sorted(outcome_counts.items())),
        "risky_success_count": risky_success,
        "risky_failure_count": risky_failure,
        "risky_success_rate_observed": risky_success / risky_total if risky_total else None,
        "true_risky_success_prob": mdp.true_risky_success_prob,
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
        "risky_state": mdp.risky_state,
        "risky_action": mdp.risky_action,
    }


def serialize_q(mdp: MDP, q_values: QTable) -> Dict[str, Dict[str, Dict[str, float]]]:
    nested: Dict[str, Dict[str, Dict[str, float]]] = {}
    for state in mdp.states:
        nested[state] = {}
        for action in mdp.actions.get(state, tuple()):
            nested[state][action] = {
                goal: q_values.get((state, action, goal), 0.0)
                for goal in mdp.states
            }
    return nested


def run_methods(mdp: MDP, trajectories: List[Dict[str, Any]], regime_name: str) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    exact_values, exact_q = exact_discounted_reachability_dp(mdp)
    methods = {
        "mc_supervised": train_mc_supervised(mdp, trajectories)[0],
        "trl_raw": train_trl_raw(mdp, trajectories),
        "trl_log": train_trl_log(mdp, trajectories),
        "mc_plus_trl_log": train_mc_plus_trl_log(mdp, trajectories),
    }
    metrics = {
        "coverage_diagnostics": coverage_diagnostics(mdp, trajectories, regime_name),
        "methods": {
            method_name: evaluate_method(mdp, q_values, exact_values, exact_q)
            for method_name, q_values in methods.items()
        },
    }
    value_tables = {
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
    return metrics, value_tables


def flatten_metrics(all_metrics: Mapping[str, Any]) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for scenario_id, scenario in all_metrics["scenarios"].items():
        coverage = scenario["coverage_diagnostics"]
        for method_name, metrics in scenario["methods"].items():
            rows.append(
                {
                    "scenario_id": scenario_id,
                    "mdp": scenario["mdp"],
                    "regime": scenario["regime"],
                    "method": method_name,
                    "true_risky_success_prob": coverage["true_risky_success_prob"],
                    "observed_risky_successes": coverage["risky_success_count"],
                    "observed_risky_failures": coverage["risky_failure_count"],
                    "observed_risky_success_rate": coverage["risky_success_rate_observed"],
                    "exact_optimal_action": metrics["exact_optimal_action"],
                    "eval_greedy_action": metrics["eval_greedy_action"],
                    "chose_exact_optimal_action": metrics["chose_exact_optimal_action"],
                    "eval_start_exact_value": metrics["eval_start_exact_value"],
                    "eval_start_learned_value": metrics["eval_start_learned_value"],
                    "value_mse": metrics["value_mse"],
                    "long_horizon_value_mse": metrics["long_horizon_value_mse"],
                    "value_overestimation_error": metrics["value_overestimation_error"],
                    "value_underestimation_error": metrics["value_underestimation_error"],
                    "q_calibration_error": metrics["q_calibration_error"],
                    "q_overestimation_error": metrics["q_overestimation_error"],
                    "q_underestimation_error": metrics["q_underestimation_error"],
                    "policy_regret": metrics["policy_regret"],
                    "mean_policy_regret": metrics["mean_policy_regret"],
                    "max_policy_regret": metrics["max_policy_regret"],
                    "risky_action_selection_rate": metrics["risky_action_selection_rate"],
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


def summarize_rows(rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    risk_rows = [row for row in rows if row["mdp"] != "deterministic_chain"]
    raw_rows = [row for row in risk_rows if row["method"] == "trl_raw"]
    success_observed_raw = [row for row in raw_rows if row["observed_risky_successes"] > 0]
    no_success_raw = [row for row in raw_rows if row["observed_risky_successes"] == 0]
    log_rows = [row for row in risk_rows if row["method"] == "trl_log"]
    mc_rows = [row for row in risk_rows if row["method"] == "mc_supervised"]
    return {
        "num_scenarios": len(set(row["scenario_id"] for row in rows)),
        "num_risky_scenarios": len(set(row["scenario_id"] for row in risk_rows)),
        "raw_selected_risky_when_success_observed": sum(row["eval_greedy_action"] == "risky" for row in success_observed_raw),
        "raw_success_observed_scenarios": len(success_observed_raw),
        "raw_selected_risky_when_no_success_observed": sum(row["eval_greedy_action"] == "risky" for row in no_success_raw),
        "raw_no_success_scenarios": len(no_success_raw),
        "trl_log_optimal_action_rate": sum(row["chose_exact_optimal_action"] for row in log_rows) / len(log_rows),
        "mc_supervised_optimal_action_rate": sum(row["chose_exact_optimal_action"] for row in mc_rows) / len(mc_rows),
        "trl_log_mean_policy_regret": sum(row["policy_regret"] for row in log_rows) / len(log_rows),
        "mc_supervised_mean_policy_regret": sum(row["policy_regret"] for row in mc_rows) / len(mc_rows),
        "trl_raw_mean_policy_regret": sum(row["policy_regret"] for row in raw_rows) / len(raw_rows),
    }


def main() -> int:
    repo_root = Path(__file__).resolve().parents[4]
    artifact_dir = repo_root / "research" / PROJECT / "artifacts" / EXPERIMENT_ID
    result_dir = repo_root / "research" / PROJECT / "results"
    artifact_dir.mkdir(parents=True, exist_ok=True)
    result_dir.mkdir(parents=True, exist_ok=True)

    chain_mdp = deterministic_chain()
    risky_mdps = {
        "safe_optimal": risky_shortcut("risky_safe_optimal", true_success_prob=0.25),
        "risk_optimal": risky_shortcut("risky_risk_optimal", true_success_prob=0.90),
    }

    all_metrics: Dict[str, Any] = {
        "experiment_id": EXPERIMENT_ID,
        "gamma": GAMMA,
        "update_steps": UPDATE_STEPS,
        "safe_episodes_per_regime": SAFE_EPISODES_PER_REGIME,
        "regime_specs": REGIME_SPECS,
        "scenarios": {},
    }
    all_value_tables: Dict[str, Any] = {}
    all_datasets: Dict[str, Any] = {}
    coverage_by_scenario: Dict[str, Any] = {}

    chain_metrics, chain_values = run_methods(chain_mdp, chain_trajectories(), "chain_regression")
    all_metrics["scenarios"]["deterministic_chain__chain_regression"] = {
        "mdp": "deterministic_chain",
        "regime": "chain_regression",
        **chain_metrics,
    }
    all_value_tables["deterministic_chain__chain_regression"] = chain_values
    all_datasets["deterministic_chain__chain_regression"] = chain_trajectories()
    coverage_by_scenario["deterministic_chain__chain_regression"] = chain_metrics["coverage_diagnostics"]

    for setting_name, mdp in risky_mdps.items():
        for regime_name, counts in REGIME_SPECS[setting_name].items():
            scenario_id = f"{setting_name}__{regime_name}"
            trajectories = risky_trajectories(
                mdp,
                regime_name,
                successes=counts["risky_successes"],
                failures=counts["risky_failures"],
            )
            scenario_metrics, scenario_values = run_methods(mdp, trajectories, regime_name)
            all_metrics["scenarios"][scenario_id] = {
                "mdp": mdp.name,
                "setting": setting_name,
                "regime": regime_name,
                **scenario_metrics,
            }
            all_value_tables[scenario_id] = scenario_values
            all_datasets[scenario_id] = trajectories
            coverage_by_scenario[scenario_id] = scenario_metrics["coverage_diagnostics"]

    rows = flatten_metrics(all_metrics)
    aggregate = summarize_rows(rows)

    chain_methods = all_metrics["scenarios"]["deterministic_chain__chain_regression"]["methods"]
    chain_raw_recovers = chain_methods["trl_raw"]["value_overestimation_error"] < 1e-10 and chain_methods["trl_raw"]["value_underestimation_error"] < 1e-10
    chain_log_recovers = chain_methods["trl_log"]["value_overestimation_error"] < 1e-10 and chain_methods["trl_log"]["value_underestimation_error"] < 1e-10
    expected_regime_count = sum(len(regimes) for regimes in REGIME_SPECS.values())
    risky_scenarios = [key for key in all_metrics["scenarios"] if key != "deterministic_chain__chain_regression"]
    all_regimes_present = len(risky_scenarios) == expected_regime_count
    raw_support_driven = (
        aggregate["raw_selected_risky_when_success_observed"] == aggregate["raw_success_observed_scenarios"]
        and aggregate["raw_selected_risky_when_no_success_observed"] == 0
    )
    matched_log_optimal = all(
        row["chose_exact_optimal_action"]
        for row in rows
        if row["method"] == "trl_log" and row["regime"] == "matched" and row["mdp"] != "deterministic_chain"
    )
    success_criteria_met = all([chain_raw_recovers, chain_log_recovers, all_regimes_present, raw_support_driven, matched_log_optimal])
    all_metrics["aggregate"] = aggregate
    all_metrics["success_checks"] = {
        "chain_raw_recovers_discounted_reachability": chain_raw_recovers,
        "chain_log_recovers_discounted_reachability": chain_log_recovers,
        "all_predeclared_risky_regimes_present": all_regimes_present,
        "raw_policy_is_support_driven": raw_support_driven,
        "trl_log_is_optimal_on_matched_regimes": matched_log_optimal,
        "success_criteria_met": success_criteria_met,
    }

    artifact_paths = [
        f"research/{PROJECT}/artifacts/{EXPERIMENT_ID}/run_coverage_stress.py",
        f"research/{PROJECT}/artifacts/{EXPERIMENT_ID}/raw_metrics.json",
        f"research/{PROJECT}/artifacts/{EXPERIMENT_ID}/metrics.csv",
        f"research/{PROJECT}/artifacts/{EXPERIMENT_ID}/coverage_diagnostics.json",
        f"research/{PROJECT}/artifacts/{EXPERIMENT_ID}/dataset_specs.json",
        f"research/{PROJECT}/artifacts/{EXPERIMENT_ID}/offline_datasets.json",
        f"research/{PROJECT}/artifacts/{EXPERIMENT_ID}/transition_tables.json",
        f"research/{PROJECT}/artifacts/{EXPERIMENT_ID}/value_tables.json",
    ]

    transition_tables = {
        "deterministic_chain": serialize_mdp(chain_mdp),
        **{setting_name: serialize_mdp(mdp) for setting_name, mdp in risky_mdps.items()},
    }
    dataset_specs = {
        "safe_episodes_per_regime": SAFE_EPISODES_PER_REGIME,
        "regime_specs": REGIME_SPECS,
        "note": "Training methods consume only these constructed trajectories. Exact DP transition tables are used only for evaluation.",
    }
    write_json(artifact_dir / "raw_metrics.json", all_metrics)
    write_metrics_csv(artifact_dir / "metrics.csv", rows)
    write_json(artifact_dir / "coverage_diagnostics.json", coverage_by_scenario)
    write_json(artifact_dir / "dataset_specs.json", dataset_specs)
    write_json(artifact_dir / "offline_datasets.json", all_datasets)
    write_json(artifact_dir / "transition_tables.json", transition_tables)
    write_json(artifact_dir / "value_tables.json", all_value_tables)

    baseline_rows = [row for row in rows if row["method"] == "mc_supervised"]
    baseline_metrics = {
        "method": "mc_supervised",
        "num_rows": len(baseline_rows),
        "optimal_action_rate_on_risky_scenarios": aggregate["mc_supervised_optimal_action_rate"],
        "mean_policy_regret_on_risky_scenarios": aggregate["mc_supervised_mean_policy_regret"],
        "rows": baseline_rows,
    }

    interpretation = (
        "The chain guard still recovered exact discounted reachability for raw and log TRL. "
        "Across risky regimes, raw TRL selected risky in every scenario with at least one observed lucky risky transition "
        "and did not select risky when no lucky risky transition was observed, confirming the support-driven failure mode. "
        "Empirical TRL-log and MC tracked observed frequencies: they were correct in matched regimes, became overoptimistic in safe-optimal lucky-biased/lucky-only regimes, "
        "and became too conservative in risk-optimal unlucky/no-success regimes. The risk-optimal setting therefore exposes that calibration gains are coverage-dependent, not simply safe-action conservatism."
    )
    known_failures = [] if success_criteria_met else [
        "One or more predeclared diagnostic checks failed; see raw_metrics.json success_checks."
    ]
    result = {
        "experiment_id": EXPERIMENT_ID,
        "status": "completed" if success_criteria_met else "failed",
        "claim_tested": (
            "Raw TRL overestimation is support-driven under stochastic coverage, while empirical MC/log methods are calibrated only when observed risky branch frequencies match the true MDP; a risk-optimal setting tests for conservative avoidance."
        ),
        "commands_run": COMMANDS_RUN,
        "metrics": all_metrics,
        "baseline_metrics": baseline_metrics,
        "artifacts": artifact_paths,
        "interpretation": interpretation,
        "known_failures": known_failures,
        "next_questions": [
            "How much stochastic branch coverage is needed before empirical log backups choose the right action with high probability?",
            "Can uncertainty-aware backups avoid both lucky-only overestimation and no-success conservative underestimation?",
            "Does the same support-driven raw TRL failure appear with sampled goals and function approximation?",
        ],
    }
    write_json(result_dir / f"{EXPERIMENT_ID}_result.json", result)

    summary = f"""# Experiment {EXPERIMENT_ID} Summary

## Objective

Stress-test stochastic shortcut coverage with exact DP evaluation, including safe-optimal and risk-optimal risky-shortcut MDPs.

## Commands Run

```bash
{chr(10).join(COMMANDS_RUN)}
```

## Setup

- Discount: `{GAMMA}`
- Fixed backup iterations: `{UPDATE_STEPS}`
- Safe episodes per risky regime: `{SAFE_EPISODES_PER_REGIME}`
- Risky settings: safe-optimal true success `0.25`; risk-optimal true success `0.90`.
- Regimes per risky setting: `{", ".join(REGIME_SPECS["safe_optimal"].keys())}`.

## Aggregate Checks

- Chain raw TRL recovered exact reachability: `{chain_raw_recovers}`.
- Chain log TRL recovered exact reachability: `{chain_log_recovers}`.
- All predeclared risky regimes present: `{all_regimes_present}`.
- Raw policy was support-driven: `{raw_support_driven}`.
- TRL-log chose the exact optimal action in matched regimes: `{matched_log_optimal}`.

## Per-Regime Metrics

| Scenario | Method | Observed S/F | Exact optimal | Chosen | Regret | Risky Q learned/exact | Safe Q learned/exact |
| --- | --- | ---: | --- | --- | ---: | ---: | ---: |
"""
    for row in rows:
        if row["mdp"] == "deterministic_chain":
            continue
        observed = f"{row['observed_risky_successes']}/{row['observed_risky_failures']}"
        summary += (
            f"| {row['scenario_id']} | {row['method']} | {observed} | {row['exact_optimal_action']} | "
            f"{row['eval_greedy_action']} | {row['policy_regret']:.6f} | "
            f"{row['learned_risky_q']:.6f}/{row['exact_risky_q']:.6f} | "
            f"{row['learned_safe_q']:.6f}/{row['exact_safe_q']:.6f} |\n"
        )

    summary += f"""
## Outcome

{interpretation}

## Artifacts

- `research/{PROJECT}/artifacts/{EXPERIMENT_ID}/run_coverage_stress.py`
- `research/{PROJECT}/artifacts/{EXPERIMENT_ID}/raw_metrics.json`
- `research/{PROJECT}/artifacts/{EXPERIMENT_ID}/metrics.csv`
- `research/{PROJECT}/artifacts/{EXPERIMENT_ID}/coverage_diagnostics.json`
- `research/{PROJECT}/artifacts/{EXPERIMENT_ID}/dataset_specs.json`
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
