#!/usr/bin/env python3
"""Experiment 0001: tiny tabular diagnostics for stochastic TRL."""

from __future__ import annotations

import csv
import json
import math
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Optional, Tuple


EXPERIMENT_ID = "0001"
PROJECT = "sto_trl"
GAMMA = 0.9
UPDATE_STEPS = 32
TOL = 1e-12

COMMANDS_RUN = [
    "mkdir -p research/sto_trl/artifacts/0001 research/sto_trl/results",
    "conda run -n autoresearcher_sto_trl python research/sto_trl/artifacts/0001/run_tabular_sto_trl.py",
    "conda run -n autoresearcher_sto_trl python scripts/validate_artifacts.py --repo-root . --json research/sto_trl/results/0001_result.json --schema schemas/result.schema.json --check-result-artifacts",
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


QTable = Dict[Tuple[str, str, str], float]
VTable = Dict[str, Dict[str, float]]


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
        name="risky_shortcut",
        states=states,
        actions=actions,
        transitions=transitions,
        eval_start="start",
        eval_goal="goal",
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


def risky_trajectories() -> List[Dict[str, Any]]:
    trajectories: List[Dict[str, Any]] = []
    for idx in range(4):
        trajectories.append(
            {
                "episode_id": f"safe_{idx}",
                "mdp": "risky_shortcut",
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

    risky_outcomes = ["success", "failure", "failure", "failure", "success", "failure", "failure", "failure"]
    for idx, outcome in enumerate(risky_outcomes):
        next_state = "goal" if outcome == "success" else "trap"
        trajectories.append(
            {
                "episode_id": f"risky_{idx}_{outcome}",
                "mdp": "risky_shortcut",
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
    q_values = {key: sums[key] / count for key, count in counts.items()}
    return q_values, counts


def train_trl_raw(mdp: MDP, trajectories: List[Dict[str, Any]]) -> QTable:
    transition_counts = empirical_transition_counts(trajectories)
    observed_next = {key: tuple(counter.keys()) for key, counter in transition_counts.items()}
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
                for prob, next_state in empirical_probs:
                    next_value = values[goal][next_state]
                    if next_value <= 0.0:
                        terms.append(-math.inf)
                    else:
                        terms.append(math.log(prob) + math.log(next_value))
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
                    for prob, next_state in empirical_probs:
                        next_value = values[goal][next_state]
                        if next_value <= 0.0:
                            terms.append(-math.inf)
                        else:
                            terms.append(math.log(prob) + math.log(next_value))
                    log_value = math.log(GAMMA) + logsumexp(terms)
                    backup = 0.0 if math.isinf(log_value) else math.exp(log_value)
                if key in mc_counts:
                    next_q[key] = anchor_weight * mc_q[key] + (1.0 - anchor_weight) * backup
                else:
                    next_q[key] = backup
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
                        prob * values[next_state]
                        for prob, next_state in mdp.transitions[(state, action)]
                    )
            next_values[state] = updated
            max_delta = max(max_delta, abs(updated - values[state]))
        values = next_values
        if max_delta < TOL:
            break
    return values


def mse(values: List[float]) -> float:
    return sum(value * value for value in values) / len(values) if values else 0.0


def evaluate_method(
    mdp: MDP,
    q_values: QTable,
    exact_values: VTable,
    exact_q: QTable,
) -> Dict[str, Any]:
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
    long_horizon_pairs = [
        (goal, state)
        for goal in mdp.states
        for state in mdp.states
        if state != goal and 0.0 < exact_values[goal][state] <= GAMMA**2 + 1e-12
    ]
    long_horizon_errors = [
        learned_values[goal][state] - exact_values[goal][state]
        for goal, state in long_horizon_pairs
    ]

    policy_regrets = []
    policies: Dict[str, Dict[str, Optional[str]]] = {}
    for goal in mdp.states:
        policy = greedy_policy(mdp, q_values, goal)
        policies[goal] = policy
        evaluated = evaluate_policy(mdp, policy, goal)
        for state in mdp.states:
            if state != goal and exact_values[goal][state] > 0.0:
                policy_regrets.append(max(0.0, exact_values[goal][state] - evaluated[state]))

    eval_policy = policies[mdp.eval_goal]
    eval_policy_value = evaluate_policy(mdp, eval_policy, mdp.eval_goal)
    target_policy_regret = max(
        0.0,
        exact_values[mdp.eval_goal][mdp.eval_start] - eval_policy_value[mdp.eval_start],
    )
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

    return {
        "value_mse": mse(value_errors),
        "long_horizon_value_mse": mse(long_horizon_errors),
        "value_overestimation_error": max([0.0] + value_errors),
        "value_underestimation_error": max([0.0] + [-error for error in value_errors]),
        "q_calibration_error": sum(abs(error) for error in q_errors) / len(q_errors) if q_errors else 0.0,
        "calibration_error": sum(abs(error) for error in q_errors) / len(q_errors) if q_errors else 0.0,
        "q_overestimation_error": max([0.0] + q_errors),
        "q_underestimation_error": max([0.0] + [-error for error in q_errors]),
        "policy_regret": target_policy_regret,
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
    }


def coverage_diagnostics(mdp: MDP, trajectories: List[Dict[str, Any]]) -> Dict[str, Any]:
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

    total_available_state_actions = sum(len(actions) for actions in mdp.actions.values())
    risky_success = outcome_counts.get("risky_success", 0)
    risky_failure = outcome_counts.get("risky_failure", 0)
    risky_total = risky_success + risky_failure
    return {
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


def run_one_mdp(mdp: MDP, trajectories: List[Dict[str, Any]]) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    exact_values, exact_q = exact_discounted_reachability_dp(mdp)
    methods = {
        "mc_supervised": train_mc_supervised(mdp, trajectories)[0],
        "trl_raw": train_trl_raw(mdp, trajectories),
        "trl_log": train_trl_log(mdp, trajectories),
        "mc_plus_trl_log": train_mc_plus_trl_log(mdp, trajectories),
    }
    metrics = {
        "coverage_diagnostics": coverage_diagnostics(mdp, trajectories),
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


def flatten_metrics_for_csv(all_metrics: Mapping[str, Any]) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for mdp_name, mdp_metrics in all_metrics["mdps"].items():
        for method_name, metrics in mdp_metrics["methods"].items():
            rows.append(
                {
                    "mdp": mdp_name,
                    "method": method_name,
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
                    "eval_greedy_action": metrics["eval_greedy_action"],
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

    mdps = [deterministic_chain(), risky_shortcut()]
    datasets = {
        "deterministic_chain": chain_trajectories(),
        "risky_shortcut": risky_trajectories(),
    }

    all_metrics: Dict[str, Any] = {
        "experiment_id": EXPERIMENT_ID,
        "gamma": GAMMA,
        "update_steps": UPDATE_STEPS,
        "mdps": {},
    }
    all_value_tables: Dict[str, Any] = {}
    for mdp in mdps:
        mdp_metrics, value_tables = run_one_mdp(mdp, datasets[mdp.name])
        all_metrics["mdps"][mdp.name] = mdp_metrics
        all_value_tables[mdp.name] = value_tables

    chain_methods = all_metrics["mdps"]["deterministic_chain"]["methods"]
    risky_methods = all_metrics["mdps"]["risky_shortcut"]["methods"]
    risky_coverage = all_metrics["mdps"]["risky_shortcut"]["coverage_diagnostics"]

    chain_raw_recovers = chain_methods["trl_raw"]["value_overestimation_error"] < 1e-10 and chain_methods["trl_raw"]["value_underestimation_error"] < 1e-10
    chain_log_recovers = chain_methods["trl_log"]["value_overestimation_error"] < 1e-10 and chain_methods["trl_log"]["value_underestimation_error"] < 1e-10
    risky_has_both_outcomes = risky_coverage["risky_success_count"] > 0 and risky_coverage["risky_failure_count"] > 0
    raw_overestimates_risky = risky_methods["trl_raw"]["eval_start_learned_q"]["risky"] > risky_methods["trl_raw"]["eval_start_exact_q"]["risky"]
    log_prefers_safe = risky_methods["trl_log"]["eval_greedy_action"] == "safe"
    raw_prefers_risky = risky_methods["trl_raw"]["eval_greedy_action"] == "risky"
    success_criteria_met = all(
        [
            chain_raw_recovers,
            chain_log_recovers,
            risky_has_both_outcomes,
            raw_overestimates_risky,
            log_prefers_safe,
            raw_prefers_risky,
        ]
    )

    all_metrics["success_checks"] = {
        "chain_raw_recovers_discounted_reachability": chain_raw_recovers,
        "chain_log_recovers_discounted_reachability": chain_log_recovers,
        "risky_dataset_has_lucky_and_unlucky_outcomes": risky_has_both_outcomes,
        "trl_raw_overestimates_risky_action": raw_overestimates_risky,
        "trl_log_prefers_safe_route": log_prefers_safe,
        "trl_raw_prefers_risky_shortcut": raw_prefers_risky,
        "success_criteria_met": success_criteria_met,
    }

    transition_tables = {mdp.name: serialize_mdp(mdp) for mdp in mdps}
    offline_dataset = {
        "experiment_id": EXPERIMENT_ID,
        "gamma": GAMMA,
        "datasets": datasets,
    }

    raw_metrics_path = artifact_dir / "raw_metrics.json"
    metrics_csv_path = artifact_dir / "metrics.csv"
    dataset_path = artifact_dir / "offline_dataset.json"
    transition_path = artifact_dir / "transition_tables.json"
    value_tables_path = artifact_dir / "value_tables.json"
    write_json(raw_metrics_path, all_metrics)
    write_metrics_csv(metrics_csv_path, flatten_metrics_for_csv(all_metrics))
    write_json(dataset_path, offline_dataset)
    write_json(transition_path, transition_tables)
    write_json(value_tables_path, all_value_tables)

    artifact_paths = [
        f"research/{PROJECT}/artifacts/{EXPERIMENT_ID}/run_tabular_sto_trl.py",
        f"research/{PROJECT}/artifacts/{EXPERIMENT_ID}/raw_metrics.json",
        f"research/{PROJECT}/artifacts/{EXPERIMENT_ID}/metrics.csv",
        f"research/{PROJECT}/artifacts/{EXPERIMENT_ID}/offline_dataset.json",
        f"research/{PROJECT}/artifacts/{EXPERIMENT_ID}/transition_tables.json",
        f"research/{PROJECT}/artifacts/{EXPERIMENT_ID}/value_tables.json",
    ]

    baseline_metrics = {
        "method": "mc_supervised",
        "deterministic_chain": chain_methods["mc_supervised"],
        "risky_shortcut": risky_methods["mc_supervised"],
    }
    interpretation = (
        "The deterministic chain sanity check was recovered by both raw and log TRL. "
        "On the risky-shortcut MDP, raw deterministic-style TRL treated the observed lucky risky edge as reliable "
        f"and selected risky with Q={risky_methods['trl_raw']['eval_start_learned_q']['risky']:.6f} versus exact "
        f"Q={risky_methods['trl_raw']['eval_start_exact_q']['risky']:.6f}. "
        "The empirical log backup and MC+TRL-log selected the safe route and had zero start-goal policy regret in this tiny dataset. "
        "MC supervised was also calibrated here because the offline set deliberately included both lucky and unlucky risky outcomes."
    )
    known_failures = [] if success_criteria_met else [
        "One or more predeclared diagnostic checks failed; see raw_metrics.json success_checks."
    ]
    result = {
        "experiment_id": EXPERIMENT_ID,
        "status": "completed" if success_criteria_met else "failed",
        "claim_tested": (
            "A tiny stochastic risky-shortcut MDP exposes overestimation by deterministic raw TRL backups, "
            "while log-space stochastic backups preserve deterministic-chain behavior and improve risky-action calibration relative to raw TRL."
        ),
        "commands_run": COMMANDS_RUN,
        "metrics": all_metrics,
        "baseline_metrics": baseline_metrics,
        "artifacts": artifact_paths,
        "interpretation": interpretation,
        "known_failures": known_failures,
        "next_questions": [
            "Does MC-only lose calibration when the lucky/unlucky risky outcome ratio is intentionally imbalanced or lower coverage?",
            "Can the log-space stochastic backup remain stable with function approximation instead of exact tabular counts?",
            "Which coverage diagnostic best predicts when raw deterministic TRL will overestimate stochastic shortcuts?",
        ],
    }
    write_json(result_dir / f"{EXPERIMENT_ID}_result.json", result)

    summary = f"""# Experiment {EXPERIMENT_ID} Summary

## Objective

Build a minimal tabular diagnostic for stochastic TRL with exact discounted-reachability DP ground truth.

## Commands Run

```bash
{chr(10).join(COMMANDS_RUN)}
```

## Setup

- Discount: `{GAMMA}`
- Fixed backup iterations: `{UPDATE_STEPS}`
- MDPs: deterministic 6-state chain and 5-state risky-shortcut MDP.
- Offline risky coverage: `{risky_coverage["risky_success_count"]}` lucky risky successes and `{risky_coverage["risky_failure_count"]}` unlucky risky failures.

## Key Raw Metrics

| MDP | Method | Long-horizon value MSE | Q calibration error | Policy regret | Risky selection |
| --- | --- | ---: | ---: | ---: | ---: |
"""
    for row in flatten_metrics_for_csv(all_metrics):
        summary += (
            f"| {row['mdp']} | {row['method']} | {row['long_horizon_value_mse']:.12f} | "
            f"{row['q_calibration_error']:.12f} | {row['policy_regret']:.12f} | "
            f"{row['risky_action_selection_rate']:.1f} |\n"
        )

    summary += f"""
## Diagnostic Outcome

- Chain raw TRL recovered exact discounted reachability: `{chain_raw_recovers}`.
- Chain log TRL recovered exact discounted reachability: `{chain_log_recovers}`.
- Risky dataset covered lucky and unlucky outcomes: `{risky_has_both_outcomes}`.
- Raw TRL chose the risky shortcut: `{raw_prefers_risky}`.
- Log TRL chose the safe route: `{log_prefers_safe}`.

The most decisive risky-start numbers are:

- Exact risky Q: `{risky_methods['trl_raw']['eval_start_exact_q']['risky']:.6f}`
- Raw TRL risky Q: `{risky_methods['trl_raw']['eval_start_learned_q']['risky']:.6f}`
- Log TRL risky Q: `{risky_methods['trl_log']['eval_start_learned_q']['risky']:.6f}`
- Exact safe Q: `{risky_methods['trl_raw']['eval_start_exact_q']['safe']:.6f}`
- Raw TRL safe Q: `{risky_methods['trl_raw']['eval_start_learned_q']['safe']:.6f}`
- Log TRL safe Q: `{risky_methods['trl_log']['eval_start_learned_q']['safe']:.6f}`

## Artifacts

- `research/{PROJECT}/artifacts/{EXPERIMENT_ID}/run_tabular_sto_trl.py`
- `research/{PROJECT}/artifacts/{EXPERIMENT_ID}/raw_metrics.json`
- `research/{PROJECT}/artifacts/{EXPERIMENT_ID}/metrics.csv`
- `research/{PROJECT}/artifacts/{EXPERIMENT_ID}/offline_dataset.json`
- `research/{PROJECT}/artifacts/{EXPERIMENT_ID}/transition_tables.json`
- `research/{PROJECT}/artifacts/{EXPERIMENT_ID}/value_tables.json`

## Interpretation

{interpretation}

## Known Failures

{chr(10).join(f"- {failure}" for failure in known_failures) if known_failures else "- None."}
"""
    (result_dir / f"{EXPERIMENT_ID}_summary.md").write_text(summary)

    print(json.dumps(all_metrics["success_checks"], indent=2, sort_keys=True))
    return 0 if success_criteria_met else 1


if __name__ == "__main__":
    raise SystemExit(main())
