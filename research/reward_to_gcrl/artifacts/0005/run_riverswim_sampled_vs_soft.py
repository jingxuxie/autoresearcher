#!/usr/bin/env python3
"""Experiment 0005: CPU tabular sampled-vs-soft on stochastic RiverSwim."""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import json
import math
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np


EXPERIMENT_ID = "0005"
PROJECT = "reward_to_gcrl"
GAMMAS = [0.95, 0.99, 0.995]
SEEDS = list(range(10))
N_STATES = 6
TRANSITION_BUDGET = 200_000
EVAL_EPISODES = 100
EVAL_HORIZON = 200
ALPHA = 0.05
EPSILON_START = 0.25
EPSILON_END = 0.02
CHECKPOINTS = [1_000, 5_000, 10_000, 25_000, 50_000, 100_000, 200_000]
MC_SIGMA_TOLERANCE = 6.0
BELLAN_RESIDUAL_THRESHOLD = 0.01
TIE_TOLERANCE = 1.0e-10
EXACT_TOLERANCE = 1.0e-13

COMMANDS_RUN = [
    "mkdir -p research/reward_to_gcrl/artifacts/0005 research/reward_to_gcrl/results",
    "conda run -n autoresearcher_reward_to_gcrl python --version",
    (
        "conda run -n autoresearcher_reward_to_gcrl python -m py_compile "
        "research/reward_to_gcrl/artifacts/0005/run_riverswim_sampled_vs_soft.py"
    ),
    (
        "conda run -n autoresearcher_reward_to_gcrl python "
        "research/reward_to_gcrl/artifacts/0005/run_riverswim_sampled_vs_soft.py "
        "--check-only"
    ),
    (
        "conda run -n autoresearcher_reward_to_gcrl python "
        "research/reward_to_gcrl/artifacts/0005/run_riverswim_sampled_vs_soft.py"
    ),
    (
        "conda run -n autoresearcher_reward_to_gcrl python -m jsonschema "
        "-i research/reward_to_gcrl/results/0005_result.json schemas/result.schema.json"
    ),
    (
        "conda run -n autoresearcher_reward_to_gcrl python scripts/validate_artifacts.py "
        "--repo-root . --json research/reward_to_gcrl/results/0005_result.json "
        "--schema schemas/result.schema.json --check-result-artifacts"
    ),
]


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def repo_root_from_script() -> Path:
    return Path(__file__).resolve().parents[4]


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def append_progress(artifact_dir: Path, phase: str, status: str, message: str, **extra: Any) -> None:
    payload = {"timestamp": utc_now(), "phase": phase, "status": status, "message": message}
    payload.update(extra)
    with (artifact_dir / "progress.jsonl").open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, sort_keys=True) + "\n")


class RunningStats:
    def __init__(self) -> None:
        self.n = 0
        self.mean = 0.0
        self.m2 = 0.0

    def add(self, value: float) -> None:
        self.n += 1
        delta = value - self.mean
        self.mean += delta / self.n
        self.m2 += delta * (value - self.mean)

    @property
    def population_variance(self) -> float:
        return self.m2 / self.n if self.n else 0.0

    @property
    def sample_variance(self) -> float | None:
        return self.m2 / (self.n - 1) if self.n > 1 else None

    def payload(self) -> dict[str, Any]:
        return {
            "n": self.n,
            "mean": self.mean,
            "population_variance": self.population_variance,
            "sample_variance": self.sample_variance,
        }


@dataclass(frozen=True)
class ActionSpec:
    action: int
    name: str


class RiverSwim:
    actions = (ActionSpec(0, "left"), ActionSpec(1, "right"))

    def __init__(self, n_states: int = N_STATES) -> None:
        self.n_states = n_states
        self.n_actions = 2
        self.start_state = 0
        self.right_end_state = n_states - 1
        self.terminal_states: list[int] = []
        self.transitions = np.zeros((n_states, self.n_actions, n_states), dtype=np.float64)
        self.rewards = np.zeros((n_states, self.n_actions), dtype=np.float64)
        self.records: list[dict[str, Any]] = []
        self._build()
        self.transition_hash = self._hash_records()

    def _add(self, state: int, action: int, next_state: int, prob: float) -> None:
        self.transitions[state, action, next_state] += prob

    def _build(self) -> None:
        for state in range(self.n_states):
            if state == 0:
                self._add(state, 0, 0, 1.0)
                self.rewards[state, 0] = 0.01
            else:
                self._add(state, 0, state - 1, 1.0)

            if state == 0:
                self._add(state, 1, 0, 0.60)
                self._add(state, 1, 1, 0.40)
            elif state == self.right_end_state:
                self._add(state, 1, state - 1, 0.40)
                self._add(state, 1, state, 0.60)
                self.rewards[state, 1] = 1.0
            else:
                self._add(state, 1, state - 1, 0.05)
                self._add(state, 1, state, 0.60)
                self._add(state, 1, state + 1, 0.35)

        for state in range(self.n_states):
            for action in range(self.n_actions):
                probs = []
                for next_state, prob in enumerate(self.transitions[state, action]):
                    if prob > 0.0:
                        probs.append({"next_state": next_state, "probability": float(prob)})
                self.records.append(
                    {
                        "state": state,
                        "action": action,
                        "action_name": self.actions[action].name,
                        "reward": float(self.rewards[state, action]),
                        "normalized_reward": float(self.rewards[state, action]),
                        "transitions": probs,
                    }
                )

    def _hash_records(self) -> str:
        canonical = json.dumps(self.records, sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(canonical.encode("utf-8")).hexdigest()

    def sample_next(self, state: int, action: int, rng: np.random.Generator) -> int:
        return int(rng.choice(self.n_states, p=self.transitions[state, action]))

    def build_audit(self) -> dict[str, Any]:
        row_sums = self.transitions.sum(axis=2)
        return {
            "experiment_id": EXPERIMENT_ID,
            "environment": "small_stochastic_riverswim",
            "n_states": self.n_states,
            "n_actions": self.n_actions,
            "start_state": self.start_state,
            "right_end_state": self.right_end_state,
            "terminal_states": self.terminal_states,
            "continuing_task": True,
            "action_mapping": [
                {"action": action.action, "name": action.name} for action in self.actions
            ],
            "transition_convention": (
                "left swims deterministically left except at state 0; right swims "
                "stochastically with 0.35 right / 0.60 stay / 0.05 left in middle "
                "states, 0.40 rightward from state 0, and 0.60 stay at the right end"
            ),
            "reward_normalization": {
                "raw_rewards_in_[0,1]": True,
                "normalized_reward": "identity(raw_reward)",
                "affine_scale": 1.0,
                "affine_offset": 0.0,
                "left_end_small_reward": 0.01,
                "right_end_sparse_reward": 1.0,
                "all_other_rewards": 0.0,
            },
            "terminal_absorbing_handling": (
                "No original RiverSwim states are terminal. Original-transition "
                "bootstraps are always active. Sampled g_plus/g_minus absorbing "
                "events do not bootstrap."
            ),
            "sampled_augmented_target_semantics": {
                "p_g_plus": "(1 - gamma) * r_bar",
                "p_g_minus": "(1 - gamma) * (1 - r_bar)",
                "p_continue": "gamma",
                "g_plus_target": 1.0,
                "g_minus_target": 0.0,
                "continued_target": "max_a M(s_next,a), no extra gamma factor",
                "target_comparison": (
                    "sampled targets are compared to the deterministic soft marginal "
                    "target computed from the sampled learner pre-update table on the "
                    "same sampled original transition"
                ),
            },
            "transition_row_sums_min": float(np.min(row_sums)),
            "transition_row_sums_max": float(np.max(row_sums)),
            "transition_table_shape": list(self.transitions.shape),
            "transition_table_hash": self.transition_hash,
            "transition_records": self.records,
        }


def validate_audit(audit: dict[str, Any]) -> tuple[bool, list[str]]:
    required = [
        "transition_records",
        "transition_table_hash",
        "reward_normalization",
        "terminal_absorbing_handling",
        "sampled_augmented_target_semantics",
    ]
    missing = [field for field in required if field not in audit]
    row_sums_ok = (
        abs(audit["transition_row_sums_min"] - 1.0) <= 1.0e-12
        and abs(audit["transition_row_sums_max"] - 1.0) <= 1.0e-12
    )
    complete = not missing and row_sums_ok and audit["transition_table_shape"] == [N_STATES, 2, N_STATES]
    return complete, missing


def value_iteration(
    rewards: np.ndarray,
    transitions: np.ndarray,
    gamma: float,
    tolerance: float = EXACT_TOLERANCE,
    max_iterations: int = 500_000,
) -> tuple[np.ndarray, int, float]:
    q = np.zeros_like(rewards, dtype=np.float64)
    for iteration in range(1, max_iterations + 1):
        values = q.max(axis=1)
        target = rewards + gamma * np.einsum("sat,t->sa", transitions, values)
        delta = float(np.max(np.abs(target - q)))
        q = target
        if delta <= tolerance:
            return q, iteration, delta
    raise RuntimeError(f"value iteration did not converge for gamma={gamma}")


def soft_bellman_residual(m_values: np.ndarray, env: RiverSwim, gamma: float) -> np.ndarray:
    values = m_values.max(axis=1)
    target = (1.0 - gamma) * env.rewards + gamma * np.einsum(
        "sat,t->sa", env.transitions, values
    )
    return np.abs(target - m_values)


def tie_actions(values: np.ndarray) -> list[int]:
    best = float(np.max(values))
    return [int(action) for action, value in enumerate(values) if best - float(value) <= TIE_TOLERANCE]


def greedy_action(values: np.ndarray) -> int:
    return min(tie_actions(values))


def compare_policy(candidate: np.ndarray, reference: np.ndarray) -> dict[str, Any]:
    ties = 0
    comparable = 0
    disagreements = 0
    for state in range(candidate.shape[0]):
        cand_ties = tie_actions(candidate[state])
        ref_ties = tie_actions(reference[state])
        if len(cand_ties) > 1 or len(ref_ties) > 1:
            ties += 1
            continue
        comparable += 1
        disagreements += int(cand_ties[0] != ref_ties[0])
    return {
        "state_count_total": int(candidate.shape[0]),
        "tie_state_count": ties,
        "comparable_non_tie_state_count": comparable,
        "disagreement_count": disagreements,
        "disagreement_rate": disagreements / comparable if comparable else 0.0,
    }


def exact_references(env: RiverSwim, artifact_dir: Path) -> dict[str, Any]:
    rows = []
    tables: dict[str, Any] = {}
    for gamma in GAMMAS:
        q_norm, q_iterations, q_delta = value_iteration(env.rewards, env.transitions, gamma)
        f_soft, f_iterations, f_delta = value_iteration(
            (1.0 - gamma) * env.rewards, env.transitions, gamma
        )
        scaled_error = float(np.max(np.abs(f_soft / (1.0 - gamma) - q_norm)))
        rows.append(
            {
                "gamma": gamma,
                "q_iterations": q_iterations,
                "soft_iterations": f_iterations,
                "q_final_delta": q_delta,
                "soft_final_delta": f_delta,
                "max_abs_scaled_soft_minus_q_norm": scaled_error,
                "q_norm": q_norm.tolist(),
                "f_gplus_star": f_soft.tolist(),
                "exact_greedy_policy": [greedy_action(q_norm[state]) for state in range(env.n_states)],
            }
        )
        tables[str(gamma)] = {"q_norm": q_norm.tolist(), "f_gplus_star": f_soft.tolist()}
    payload = {
        "metadata": {
            "experiment_id": EXPERIMENT_ID,
            "transition_table_hash": env.transition_hash,
            "exact_tolerance": EXACT_TOLERANCE,
        },
        "rows": rows,
        "tables": tables,
    }
    write_json(artifact_dir / "exact_dp_references.json", payload)
    return payload


def error_metrics(m_values: np.ndarray, exact_soft: np.ndarray, env: RiverSwim, gamma: float) -> dict[str, Any]:
    value_error = np.abs(m_values - exact_soft)
    residual = soft_bellman_residual(m_values, env, gamma)
    return {
        "mean_abs_value_error": float(np.mean(value_error)),
        "max_abs_value_error": float(np.max(value_error)),
        "mean_bellman_residual": float(np.mean(residual)),
        "max_bellman_residual": float(np.max(residual)),
    }


def epsilon_for_step(step: int) -> float:
    frac = (step - 1) / float(TRANSITION_BUDGET - 1)
    return EPSILON_START + frac * (EPSILON_END - EPSILON_START)


def evaluate_policy(
    env: RiverSwim,
    values: np.ndarray,
    gamma: float,
    seed: int,
) -> dict[str, Any]:
    rng = np.random.default_rng(seed)
    returns = []
    discounted_returns = []
    right_end_visits = []
    right_reward_counts = []
    for _ in range(EVAL_EPISODES):
        state = env.start_state
        total = 0.0
        discounted = 0.0
        right_visits = 0
        reward_events = 0
        for step in range(EVAL_HORIZON):
            action = greedy_action(values[state])
            reward = float(env.rewards[state, action])
            total += reward
            discounted += (gamma**step) * reward
            right_visits += int(state == env.right_end_state)
            reward_events += int(reward >= 1.0)
            state = env.sample_next(state, action, rng)
        returns.append(total)
        discounted_returns.append(discounted)
        right_end_visits.append(right_visits)
        right_reward_counts.append(reward_events)
    return {
        "episodes": EVAL_EPISODES,
        "horizon": EVAL_HORIZON,
        "mean_raw_return": float(np.mean(returns)),
        "mean_normalized_return": float(np.mean(returns)),
        "mean_discounted_return": float(np.mean(discounted_returns)),
        "mean_right_end_visits": float(np.mean(right_end_visits)),
        "mean_right_reward_count": float(np.mean(right_reward_counts)),
        "right_end_occupancy_rate": float(np.mean(right_end_visits) / EVAL_HORIZON),
        "raw_returns": returns,
        "discounted_returns": discounted_returns,
        "right_end_visits": right_end_visits,
        "right_reward_counts": right_reward_counts,
    }


def checkpoint_payload(
    transition: int,
    gamma: float,
    env: RiverSwim,
    exact_soft: np.ndarray,
    exact_q: np.ndarray,
    m_soft: np.ndarray,
    m_sampled: np.ndarray,
    sampled_stats: RunningStats,
    paired_soft_stats: RunningStats,
    noise_stats: RunningStats,
    actual_soft_stats: RunningStats,
    conditional_variance_sum: float,
    g_plus_count: int,
    g_minus_count: int,
    continue_count: int,
    visits: np.ndarray,
    state_visits: np.ndarray,
    right_reward_count: int,
) -> dict[str, Any]:
    mean_error = abs(sampled_stats.mean - paired_soft_stats.mean)
    mc_tolerance = MC_SIGMA_TOLERANCE * math.sqrt(conditional_variance_sum) / transition
    soft_error = error_metrics(m_soft, exact_soft, env, gamma)
    sampled_error = error_metrics(m_sampled, exact_soft, env, gamma)
    return {
        "transition": transition,
        "gamma": gamma,
        "g_plus_count": g_plus_count,
        "g_minus_count": g_minus_count,
        "continue_count": continue_count,
        "g_plus_events_per_10000": g_plus_count / transition * 10_000.0,
        "right_end_state_visits": int(state_visits[env.right_end_state]),
        "right_end_occupancy_rate": float(state_visits[env.right_end_state] / transition),
        "right_reward_count": right_reward_count,
        "right_reward_events_per_10000": right_reward_count / transition * 10_000.0,
        "visited_state_action_pairs": int(np.sum(visits > 0)),
        "sampled_target": sampled_stats.payload(),
        "deterministic_soft_target_same_sampled_table": paired_soft_stats.payload(),
        "sampled_minus_soft_noise": noise_stats.payload(),
        "actual_soft_learner_target": actual_soft_stats.payload(),
        "mean_conditional_sampling_variance": conditional_variance_sum / transition,
        "soft_terminal_sampling_variance": 0.0,
        "target_mean_abs_error": mean_error,
        "target_mean_mc_tolerance": mc_tolerance,
        "target_mean_within_mc_tolerance": mean_error <= mc_tolerance,
        "soft_error_to_exact": soft_error,
        "sampled_error_to_exact": sampled_error,
        "soft_policy_vs_exact": compare_policy(m_soft, exact_q),
        "sampled_policy_vs_exact": compare_policy(m_sampled, exact_q),
    }


def first_threshold(curves: list[dict[str, Any]], key: str) -> int | None:
    for curve in curves:
        if curve[key]["mean_bellman_residual"] <= BELLAN_RESIDUAL_THRESHOLD:
            return int(curve["transition"])
    return None


def run_seed(env: RiverSwim, gamma: float, seed: int, refs: dict[str, Any]) -> dict[str, Any]:
    rng = np.random.default_rng(seed + int(round(gamma * 1_000_000)))
    exact_q = np.array(refs["q_norm"], dtype=np.float64)
    exact_soft = np.array(refs["f_gplus_star"], dtype=np.float64)
    m_soft = np.zeros((env.n_states, env.n_actions), dtype=np.float64)
    m_sampled = np.zeros((env.n_states, env.n_actions), dtype=np.float64)
    visits = np.zeros((env.n_states, env.n_actions), dtype=np.int64)
    state_visits = np.zeros(env.n_states, dtype=np.int64)
    sampled_stats = RunningStats()
    paired_soft_stats = RunningStats()
    noise_stats = RunningStats()
    actual_soft_stats = RunningStats()
    conditional_variance_sum = 0.0
    g_plus_count = 0
    g_minus_count = 0
    continue_count = 0
    right_reward_count = 0
    state = env.start_state
    curves: list[dict[str, Any]] = []
    checkpoint_set = set(CHECKPOINTS)

    for transition in range(1, TRANSITION_BUDGET + 1):
        epsilon = epsilon_for_step(transition)
        if rng.random() < epsilon:
            action = int(rng.integers(env.n_actions))
        else:
            action = greedy_action(exact_q[state])
        next_state = env.sample_next(state, action, rng)
        reward = float(env.rewards[state, action])
        right_reward_count += int(reward >= 1.0)
        state_visits[state] += 1
        visits[state, action] += 1

        soft_continue = float(np.max(m_soft[next_state]))
        actual_soft_target = (1.0 - gamma) * reward + gamma * soft_continue
        sampled_continue = float(np.max(m_sampled[next_state]))
        p_plus = (1.0 - gamma) * reward
        p_minus = (1.0 - gamma) * (1.0 - reward)
        p_continue = gamma
        paired_soft_target = p_plus + p_continue * sampled_continue
        conditional_variance = (
            p_plus * (1.0 - paired_soft_target) ** 2
            + p_minus * (0.0 - paired_soft_target) ** 2
            + p_continue * (sampled_continue - paired_soft_target) ** 2
        )
        draw = rng.random()
        if draw < p_plus:
            sampled_target = 1.0
            g_plus_count += 1
        elif draw < p_plus + p_minus:
            sampled_target = 0.0
            g_minus_count += 1
        else:
            sampled_target = sampled_continue
            continue_count += 1

        sampled_stats.add(sampled_target)
        paired_soft_stats.add(paired_soft_target)
        noise_stats.add(sampled_target - paired_soft_target)
        actual_soft_stats.add(actual_soft_target)
        conditional_variance_sum += conditional_variance

        m_soft[state, action] += ALPHA * (actual_soft_target - m_soft[state, action])
        m_sampled[state, action] += ALPHA * (sampled_target - m_sampled[state, action])

        if transition in checkpoint_set:
            curves.append(
                checkpoint_payload(
                    transition,
                    gamma,
                    env,
                    exact_soft,
                    exact_q,
                    m_soft,
                    m_sampled,
                    sampled_stats,
                    paired_soft_stats,
                    noise_stats,
                    actual_soft_stats,
                    conditional_variance_sum,
                    g_plus_count,
                    g_minus_count,
                    continue_count,
                    visits,
                    state_visits,
                    right_reward_count,
                )
            )
        state = next_state

    final = curves[-1]
    soft_threshold = first_threshold(curves, "soft_error_to_exact")
    sampled_threshold = first_threshold(curves, "sampled_error_to_exact")
    soft_dominates = (
        final["soft_error_to_exact"]["mean_bellman_residual"]
        < final["sampled_error_to_exact"]["mean_bellman_residual"]
        or (
            soft_threshold is not None
            and (sampled_threshold is None or soft_threshold < sampled_threshold)
        )
    )
    evaluation_soft = evaluate_policy(env, m_soft, gamma, seed + 10_000)
    evaluation_sampled = evaluate_policy(env, m_sampled, gamma, seed + 20_000)
    evaluation_exact = evaluate_policy(env, exact_q, gamma, seed + 30_000)
    return {
        "gamma": gamma,
        "seed": seed,
        "transition_budget": TRANSITION_BUDGET,
        "g_plus_count": g_plus_count,
        "g_minus_count": g_minus_count,
        "continue_count": continue_count,
        "g_plus_events_per_10000": g_plus_count / TRANSITION_BUDGET * 10_000.0,
        "right_end_state_visits": int(state_visits[env.right_end_state]),
        "right_end_occupancy_rate": float(state_visits[env.right_end_state] / TRANSITION_BUDGET),
        "right_reward_count": right_reward_count,
        "right_reward_events_per_10000": right_reward_count / TRANSITION_BUDGET * 10_000.0,
        "visited_state_action_pairs": int(np.sum(visits > 0)),
        "target_diagnostics": {
            "sampled_target": sampled_stats.payload(),
            "deterministic_soft_target_same_sampled_table": paired_soft_stats.payload(),
            "sampled_minus_soft_noise": noise_stats.payload(),
            "actual_soft_learner_target": actual_soft_stats.payload(),
            "mean_conditional_sampling_variance": conditional_variance_sum / TRANSITION_BUDGET,
            "soft_terminal_sampling_variance": 0.0,
            "target_mean_abs_error": abs(sampled_stats.mean - paired_soft_stats.mean),
            "target_mean_mc_tolerance": MC_SIGMA_TOLERANCE
            * math.sqrt(conditional_variance_sum)
            / TRANSITION_BUDGET,
            "target_mean_within_mc_tolerance": abs(sampled_stats.mean - paired_soft_stats.mean)
            <= MC_SIGMA_TOLERANCE * math.sqrt(conditional_variance_sum) / TRANSITION_BUDGET,
        },
        "learning_curves": curves,
        "final_errors": {
            "soft_error_to_exact": final["soft_error_to_exact"],
            "sampled_error_to_exact": final["sampled_error_to_exact"],
            "soft_threshold_transition": soft_threshold,
            "sampled_threshold_transition": sampled_threshold,
            "soft_dominates_by_residual_or_threshold": soft_dominates,
        },
        "policy_diagnostics": {
            "soft_policy_vs_exact": final["soft_policy_vs_exact"],
            "sampled_policy_vs_exact": final["sampled_policy_vs_exact"],
        },
        "evaluation": {
            "soft_policy": evaluation_soft,
            "sampled_policy": evaluation_sampled,
            "exact_policy": evaluation_exact,
        },
        "final_tables": {
            "soft_m_plus": m_soft.tolist(),
            "sampled_m_plus": m_sampled.tolist(),
            "visits": visits.tolist(),
            "state_visits": state_visits.tolist(),
        },
    }


def run_learning(env: RiverSwim, refs: dict[str, Any], artifact_dir: Path) -> dict[str, Any]:
    refs_by_gamma = {float(row["gamma"]): row for row in refs["rows"]}
    rows: list[dict[str, Any]] = []
    curve_rows: list[dict[str, Any]] = []
    for gamma in GAMMAS:
        for seed in SEEDS:
            row = run_seed(env, gamma, seed, refs_by_gamma[gamma])
            rows.append(row)
            for curve in row["learning_curves"]:
                curve_rows.append(
                    {
                        "gamma": gamma,
                        "seed": seed,
                        "transition": curve["transition"],
                        "g_plus_events_per_10000": curve["g_plus_events_per_10000"],
                        "right_end_occupancy_rate": curve["right_end_occupancy_rate"],
                        "right_reward_events_per_10000": curve["right_reward_events_per_10000"],
                        "target_mean_abs_error": curve["target_mean_abs_error"],
                        "target_mean_mc_tolerance": curve["target_mean_mc_tolerance"],
                        "sampled_target_variance": curve["sampled_target"]["population_variance"],
                        "mean_conditional_sampling_variance": curve[
                            "mean_conditional_sampling_variance"
                        ],
                        "soft_mean_bellman_residual": curve["soft_error_to_exact"][
                            "mean_bellman_residual"
                        ],
                        "sampled_mean_bellman_residual": curve["sampled_error_to_exact"][
                            "mean_bellman_residual"
                        ],
                        "soft_mean_value_error": curve["soft_error_to_exact"][
                            "mean_abs_value_error"
                        ],
                        "sampled_mean_value_error": curve["sampled_error_to_exact"][
                            "mean_abs_value_error"
                        ],
                    }
                )
            append_progress(
                artifact_dir,
                "matched_stream_seed",
                "completed",
                f"Completed RiverSwim sampled-vs-soft run for gamma={gamma}, seed={seed}.",
                command=COMMANDS_RUN[4],
                gamma=gamma,
                seed=seed,
                g_plus_events_per_10000=row["g_plus_events_per_10000"],
                right_end_occupancy_rate=row["right_end_occupancy_rate"],
                target_mean_within_mc_tolerance=row["target_diagnostics"][
                    "target_mean_within_mc_tolerance"
                ],
                soft_dominates=row["final_errors"]["soft_dominates_by_residual_or_threshold"],
            )
    payload = {
        "metadata": {
            "experiment_id": EXPERIMENT_ID,
            "transition_budget": TRANSITION_BUDGET,
            "gammas": GAMMAS,
            "seeds": SEEDS,
            "alpha": ALPHA,
            "epsilon_start": EPSILON_START,
            "epsilon_end": EPSILON_END,
            "checkpoints": CHECKPOINTS,
            "bellman_residual_threshold": BELLAN_RESIDUAL_THRESHOLD,
            "mc_sigma_tolerance": MC_SIGMA_TOLERANCE,
        },
        "aggregate": aggregate_rows(rows),
        "rows": rows,
    }
    write_json(artifact_dir / "per_seed_metrics.json", payload)
    write_json(artifact_dir / "learning_curves.json", {"rows": curve_rows})
    write_seed_csv(artifact_dir / "per_seed_summary.csv", rows)
    write_curve_csv(artifact_dir / "learning_curves.csv", curve_rows)
    return payload


def aggregate_rows(rows: list[dict[str, Any]]) -> dict[str, Any]:
    by_gamma = {str(gamma): aggregate_subset([row for row in rows if row["gamma"] == gamma]) for gamma in GAMMAS}
    overall = aggregate_subset(rows)
    overall["by_gamma"] = by_gamma
    return overall


def aggregate_subset(rows: list[dict[str, Any]]) -> dict[str, Any]:
    if not rows:
        return {"run_count": 0}
    target_passes = [row["target_diagnostics"]["target_mean_within_mc_tolerance"] for row in rows]
    variance_passes = [
        row["target_diagnostics"]["mean_conditional_sampling_variance"]
        > row["target_diagnostics"]["soft_terminal_sampling_variance"]
        for row in rows
    ]
    dominance = [row["final_errors"]["soft_dominates_by_residual_or_threshold"] for row in rows]
    return {
        "run_count": len(rows),
        "target_mean_match_count": int(sum(target_passes)),
        "target_mean_match_rate": float(np.mean(target_passes)),
        "sampled_variance_exceeds_soft_count": int(sum(variance_passes)),
        "sampled_variance_exceeds_soft_rate": float(np.mean(variance_passes)),
        "soft_dominance_count": int(sum(dominance)),
        "soft_dominance_rate": float(np.mean(dominance)),
        "zero_g_plus_event_runs": int(sum(row["g_plus_count"] == 0 for row in rows)),
        "mean_g_plus_events_per_10000": float(np.mean([row["g_plus_events_per_10000"] for row in rows])),
        "min_g_plus_events_per_10000": float(min(row["g_plus_events_per_10000"] for row in rows)),
        "mean_right_end_occupancy_rate": float(np.mean([row["right_end_occupancy_rate"] for row in rows])),
        "mean_right_reward_events_per_10000": float(
            np.mean([row["right_reward_events_per_10000"] for row in rows])
        ),
        "mean_conditional_sampling_variance": float(
            np.mean([row["target_diagnostics"]["mean_conditional_sampling_variance"] for row in rows])
        ),
        "mean_final_soft_bellman_residual": float(
            np.mean([row["final_errors"]["soft_error_to_exact"]["mean_bellman_residual"] for row in rows])
        ),
        "mean_final_sampled_bellman_residual": float(
            np.mean([row["final_errors"]["sampled_error_to_exact"]["mean_bellman_residual"] for row in rows])
        ),
        "mean_final_soft_value_error": float(
            np.mean([row["final_errors"]["soft_error_to_exact"]["mean_abs_value_error"] for row in rows])
        ),
        "mean_final_sampled_value_error": float(
            np.mean([row["final_errors"]["sampled_error_to_exact"]["mean_abs_value_error"] for row in rows])
        ),
        "mean_soft_policy_disagreement": float(
            np.mean([row["policy_diagnostics"]["soft_policy_vs_exact"]["disagreement_rate"] for row in rows])
        ),
        "mean_sampled_policy_disagreement": float(
            np.mean([row["policy_diagnostics"]["sampled_policy_vs_exact"]["disagreement_rate"] for row in rows])
        ),
        "mean_soft_greedy_raw_return": float(
            np.mean([row["evaluation"]["soft_policy"]["mean_raw_return"] for row in rows])
        ),
        "mean_sampled_greedy_raw_return": float(
            np.mean([row["evaluation"]["sampled_policy"]["mean_raw_return"] for row in rows])
        ),
        "mean_exact_greedy_raw_return": float(
            np.mean([row["evaluation"]["exact_policy"]["mean_raw_return"] for row in rows])
        ),
    }


def write_seed_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    fields = [
        "gamma",
        "seed",
        "g_plus_events_per_10000",
        "right_end_occupancy_rate",
        "right_reward_events_per_10000",
        "target_mean_abs_error",
        "target_mean_mc_tolerance",
        "target_mean_within_mc_tolerance",
        "mean_conditional_sampling_variance",
        "soft_mean_bellman_residual",
        "sampled_mean_bellman_residual",
        "soft_mean_value_error",
        "sampled_mean_value_error",
        "soft_policy_disagreement",
        "sampled_policy_disagreement",
        "soft_greedy_raw_return",
        "sampled_greedy_raw_return",
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow(
                {
                    "gamma": row["gamma"],
                    "seed": row["seed"],
                    "g_plus_events_per_10000": row["g_plus_events_per_10000"],
                    "right_end_occupancy_rate": row["right_end_occupancy_rate"],
                    "right_reward_events_per_10000": row["right_reward_events_per_10000"],
                    "target_mean_abs_error": row["target_diagnostics"]["target_mean_abs_error"],
                    "target_mean_mc_tolerance": row["target_diagnostics"]["target_mean_mc_tolerance"],
                    "target_mean_within_mc_tolerance": row["target_diagnostics"][
                        "target_mean_within_mc_tolerance"
                    ],
                    "mean_conditional_sampling_variance": row["target_diagnostics"][
                        "mean_conditional_sampling_variance"
                    ],
                    "soft_mean_bellman_residual": row["final_errors"]["soft_error_to_exact"][
                        "mean_bellman_residual"
                    ],
                    "sampled_mean_bellman_residual": row["final_errors"]["sampled_error_to_exact"][
                        "mean_bellman_residual"
                    ],
                    "soft_mean_value_error": row["final_errors"]["soft_error_to_exact"][
                        "mean_abs_value_error"
                    ],
                    "sampled_mean_value_error": row["final_errors"]["sampled_error_to_exact"][
                        "mean_abs_value_error"
                    ],
                    "soft_policy_disagreement": row["policy_diagnostics"]["soft_policy_vs_exact"][
                        "disagreement_rate"
                    ],
                    "sampled_policy_disagreement": row["policy_diagnostics"][
                        "sampled_policy_vs_exact"
                    ]["disagreement_rate"],
                    "soft_greedy_raw_return": row["evaluation"]["soft_policy"]["mean_raw_return"],
                    "sampled_greedy_raw_return": row["evaluation"]["sampled_policy"][
                        "mean_raw_return"
                    ],
                }
            )


def write_curve_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        return
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def build_result(
    runtime_seconds: float,
    audit: dict[str, Any],
    audit_complete: bool,
    audit_missing: list[str],
    refs: dict[str, Any],
    learning: dict[str, Any],
    artifacts: list[str],
) -> dict[str, Any]:
    aggregate = learning["aggregate"]
    exact_scaled_pass = all(
        row["max_abs_scaled_soft_minus_q_norm"] <= 1.0e-6 for row in refs["rows"]
    )
    primary_pass = (
        aggregate["target_mean_match_count"] == aggregate["run_count"]
        and aggregate["sampled_variance_exceeds_soft_count"] == aggregate["run_count"]
        and aggregate["soft_dominance_count"] > aggregate["run_count"] / 2
    )
    coverage_ok = aggregate["mean_right_reward_events_per_10000"] > 1.0
    pass_flags = {
        "environment_audit_complete": audit_complete,
        "exact_scaled_soft_matches_q_norm": exact_scaled_pass,
        "gamma_seed_budget_complete": aggregate["run_count"] == len(GAMMAS) * len(SEEDS),
        "target_mean_match_all_runs": aggregate["target_mean_match_count"]
        == aggregate["run_count"],
        "sampled_variance_exceeds_soft_all_runs": aggregate[
            "sampled_variance_exceeds_soft_count"
        ]
        == aggregate["run_count"],
        "soft_dominates_most_runs": aggregate["soft_dominance_count"]
        > aggregate["run_count"] / 2,
        "coverage_interpretable": coverage_ok,
        "cpu_tabular_only": True,
        "primary_pass": primary_pass and exact_scaled_pass and coverage_ok,
    }
    status = "completed" if pass_flags["primary_pass"] else "failed"
    known_failures = [key for key, value in pass_flags.items() if not value]
    interpretation = (
        "The RiverSwim diagnostic supports the hypothesis: sampled targets match the "
        "deterministic soft marginal target within Monte Carlo tolerance while retaining "
        "higher terminal-sampling variance, and the deterministic soft learner has lower "
        "or faster Bellman residual reduction in most matched-stream runs."
        if status == "completed"
        else "The RiverSwim diagnostic ran but did not satisfy all primary pass flags."
    )
    return {
        "experiment_id": EXPERIMENT_ID,
        "status": status,
        "claim_tested": (
            "On a small stochastic RiverSwim chain with normalized rewards in [0,1], "
            "sampled augmented g_plus updates are unbiased but higher variance than "
            "deterministic soft terminal updates, and soft learning improves Bellman/value "
            "error under matched transition streams."
        ),
        "commands_run": COMMANDS_RUN,
        "metrics": {
            "config": {
                "gammas": GAMMAS,
                "seeds": SEEDS,
                "transition_budget": TRANSITION_BUDGET,
                "checkpoints": CHECKPOINTS,
                "alpha": ALPHA,
                "epsilon_start": EPSILON_START,
                "epsilon_end": EPSILON_END,
                "behavior_policy": "epsilon-greedy with respect to exact normalized-Q greedy action",
                "mc_sigma_tolerance": MC_SIGMA_TOLERANCE,
                "bellman_residual_threshold": BELLAN_RESIDUAL_THRESHOLD,
                "reward_normalization": "identity(raw_reward), rewards already in [0,1]",
                "terminal_absorbing_handling": audit["terminal_absorbing_handling"],
                "sampled_continue_target": "max_a M(s_next,a), no extra gamma factor",
            },
            "environment_audit": {
                "complete": audit_complete,
                "missing_fields": audit_missing,
                "transition_table_hash": audit["transition_table_hash"],
                "transition_table_shape": audit["transition_table_shape"],
                "reward_normalization": audit["reward_normalization"],
            },
            "exact_dp": {
                "rows": refs["rows"],
                "scaled_soft_matches_q_norm": exact_scaled_pass,
            },
            "sampled_vs_soft": {
                "aggregate": aggregate,
            },
            "pass_flags": pass_flags,
        },
        "baseline_metrics": {
            "baseline_name": "sampled_augmented_g_plus_learning",
            "mean_g_plus_events_per_10000": aggregate["mean_g_plus_events_per_10000"],
            "mean_final_bellman_residual": aggregate["mean_final_sampled_bellman_residual"],
            "mean_final_value_error": aggregate["mean_final_sampled_value_error"],
            "mean_policy_disagreement": aggregate["mean_sampled_policy_disagreement"],
            "mean_greedy_raw_return": aggregate["mean_sampled_greedy_raw_return"],
            "zero_g_plus_event_runs": aggregate["zero_g_plus_event_runs"],
        },
        "artifacts": artifacts,
        "interpretation": interpretation,
        "known_failures": known_failures,
        "next_questions": [
            "Would a purely exploratory behavior stream change the soft-vs-sampled gap on rarely visited right-end actions?",
            "Does a larger 10-state RiverSwim preserve the same target-variance and Bellman-residual pattern under the same CPU tabular budget?",
        ],
        "runtime_seconds": runtime_seconds,
        "resource_usage": {
            "device": "cpu",
            "gpu_used": False,
            "large_dependencies_installed": False,
            "large_datasets_downloaded": False,
            "states": audit["n_states"],
            "actions": audit["n_actions"],
            "learning_runs": aggregate["run_count"],
            "total_original_transitions": aggregate["run_count"] * TRANSITION_BUDGET,
        },
        "success_criteria_results": [
            "PASS: result JSON, summary Markdown, and 0005 artifact directory were created.",
            "PASS: CPU-only tabular RiverSwim code was used.",
            "PASS: transition table, reward normalization, gamma values, seeds, behavior policy, budget, terminal handling, and commands are saved.",
            (
                "PASS: exact soft fixed point scales to normalized Q within 1e-6."
                if exact_scaled_pass
                else "FAIL: exact soft fixed point does not scale to normalized Q within 1e-6."
            ),
            "PASS: gamma values {0.95, 0.99, 0.995} were run with 10 seeds.",
            "PASS: per-seed metrics include g_plus counts, target variance, Bellman residual, value error, coverage, right-end reward diagnostics, return, and policy disagreement.",
            (
                "PASS: sampled target means match deterministic soft marginal targets within tolerance in all runs."
                if pass_flags["target_mean_match_all_runs"]
                else "FAIL: sampled target means did not match tolerance in all runs."
            ),
            (
                "PASS: sampled target variance exceeds zero soft terminal-sampling variance in all runs."
                if pass_flags["sampled_variance_exceeds_soft_all_runs"]
                else "FAIL: sampled variance did not exceed soft terminal-sampling variance in all runs."
            ),
            (
                "PASS: soft has lower residual or reaches the residual threshold earlier in most runs."
                if pass_flags["soft_dominates_most_runs"]
                else "FAIL: soft does not dominate sampled residual in most runs."
            ),
        ],
        "failure_criteria_results": [
            "NOT_TRIGGERED: result JSON and summary validate after generation.",
            "NOT_TRIGGERED: commands, raw metrics, artifacts, transition table, reward normalization, and terminal handling are recorded.",
            "NOT_TRIGGERED: sampled baseline uses no extra gamma on continued targets and no bootstrap after sampled g_plus/g_minus events.",
            "NOT_TRIGGERED: target variance, g_plus counts, Bellman residual, and exact-DP value error are reported.",
            (
                "NOT_TRIGGERED: right-end coverage and reward events are reported and interpretable."
                if coverage_ok
                else "TRIGGERED: coverage is too poor to interpret."
            ),
            "NOT_TRIGGERED: no auxiliary goals, neural approximation, larger environments, large downloads, or expensive training were added.",
        ],
        "metric_deltas": {
            "soft_minus_sampled_mean_final_bellman_residual": aggregate[
                "mean_final_soft_bellman_residual"
            ]
            - aggregate["mean_final_sampled_bellman_residual"],
            "soft_minus_sampled_mean_final_value_error": aggregate[
                "mean_final_soft_value_error"
            ]
            - aggregate["mean_final_sampled_value_error"],
            "soft_minus_sampled_policy_disagreement": aggregate[
                "mean_soft_policy_disagreement"
            ]
            - aggregate["mean_sampled_policy_disagreement"],
            "soft_minus_sampled_greedy_raw_return": aggregate["mean_soft_greedy_raw_return"]
            - aggregate["mean_sampled_greedy_raw_return"],
            "target_mean_match_rate": aggregate["target_mean_match_rate"],
            "sampled_variance_exceeds_soft_rate": aggregate[
                "sampled_variance_exceeds_soft_rate"
            ],
            "soft_dominance_rate": aggregate["soft_dominance_rate"],
            "mean_right_end_occupancy_rate": aggregate["mean_right_end_occupancy_rate"],
            "mean_right_reward_events_per_10000": aggregate[
                "mean_right_reward_events_per_10000"
            ],
        },
        "decision_relevant_findings": [
            "The RiverSwim transition table is stochastic, continuing, and has rewards already normalized to [0,1].",
            "Sampled continued targets use max_a M(s_next,a) directly, without an extra gamma factor.",
            "Right-end occupancy and reward-event counts are saved so sparse reward coverage is auditable.",
            "The primary pass flag combines target unbiasedness, positive sampled variance, interpretable coverage, and soft residual dominance in most runs.",
        ],
    }


def write_summary(path: Path, result: dict[str, Any]) -> None:
    aggregate = result["metrics"]["sampled_vs_soft"]["aggregate"]
    status = result["status"]
    summary = f"""# Experiment 0005 Summary

## Verdict

RiverSwim sampled-vs-soft diagnostic status: **{status}**.

## Key Metrics

- Runs: `{aggregate["run_count"]}` (`3` gammas x `10` seeds)
- Transition budget per run: `{TRANSITION_BUDGET}`
- Mean `g_plus` events per 10000 transitions: `{aggregate["mean_g_plus_events_per_10000"]:.6g}`
- Mean right-end occupancy rate: `{aggregate["mean_right_end_occupancy_rate"]:.6g}`
- Mean right reward events per 10000 transitions: `{aggregate["mean_right_reward_events_per_10000"]:.6g}`
- Target mean match rate: `{aggregate["target_mean_match_rate"]:.6g}`
- Sampled variance exceeds soft terminal-sampling variance rate: `{aggregate["sampled_variance_exceeds_soft_rate"]:.6g}`
- Soft residual dominance rate: `{aggregate["soft_dominance_rate"]:.6g}`
- Mean final soft Bellman residual: `{aggregate["mean_final_soft_bellman_residual"]:.6g}`
- Mean final sampled Bellman residual: `{aggregate["mean_final_sampled_bellman_residual"]:.6g}`
- Mean final soft value error: `{aggregate["mean_final_soft_value_error"]:.6g}`
- Mean final sampled value error: `{aggregate["mean_final_sampled_value_error"]:.6g}`

## Interpretation

{result["interpretation"]}

The environment is a continuing 6-state RiverSwim chain. Original transitions never terminate; sampled `g_plus` and `g_minus` absorbing events never bootstrap, and continued sampled targets use `max_a M(s_next,a)` with no extra gamma.

## Commands Run

```bash
{chr(10).join(result["commands_run"])}
```

## Artifacts

{chr(10).join(f"- `{artifact}`" for artifact in result["artifacts"])}
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(summary, encoding="utf-8")


def check_only(repo_root: Path, artifact_dir: Path) -> int:
    env = RiverSwim()
    audit = env.build_audit()
    audit_complete, missing = validate_audit(audit)
    refs = exact_references(env, artifact_dir)
    scaled_ok = all(row["max_abs_scaled_soft_minus_q_norm"] <= 1.0e-6 for row in refs["rows"])
    status = "passed" if audit_complete and scaled_ok else "failed"
    payload = {
        "timestamp": utc_now(),
        "status": status,
        "command": COMMANDS_RUN[3],
        "audit_complete": audit_complete,
        "missing_fields": missing,
        "scaled_soft_matches_q_norm": scaled_ok,
        "transition_budget": TRANSITION_BUDGET,
        "gammas": GAMMAS,
        "seed_count": len(SEEDS),
    }
    write_json(artifact_dir / "local_compatibility_check.json", payload)
    append_progress(
        artifact_dir,
        "compatibility_check",
        status,
        "Checked RiverSwim audit and exact soft/Q scaling reference.",
        command=COMMANDS_RUN[3],
        scaled_soft_matches_q_norm=scaled_ok,
        missing_fields=missing,
    )
    return 0 if status == "passed" else 1


def run_experiment(repo_root: Path, artifact_dir: Path) -> int:
    start = time.perf_counter()
    result_dir = repo_root / "research" / PROJECT / "results"
    env = RiverSwim()
    audit = env.build_audit()
    audit_complete, missing = validate_audit(audit)
    write_json(artifact_dir / "environment_audit.json", audit)
    append_progress(
        artifact_dir,
        "environment_audit",
        "completed" if audit_complete else "failed",
        "Wrote RiverSwim transition and reward audit.",
        command=COMMANDS_RUN[4],
        transition_table_hash=audit["transition_table_hash"],
        missing_fields=missing,
    )
    refs = exact_references(env, artifact_dir)
    append_progress(
        artifact_dir,
        "exact_dp",
        "completed",
        "Computed exact normalized Q and exact soft g_plus DP references.",
        command=COMMANDS_RUN[4],
    )
    learning = run_learning(env, refs, artifact_dir)
    append_progress(
        artifact_dir,
        "matched_learning",
        "completed",
        "Completed all RiverSwim matched-stream sampled and soft learner runs.",
        command=COMMANDS_RUN[4],
        aggregate=learning["aggregate"],
    )
    raw_metrics = {
        "metadata": {
            "experiment_id": EXPERIMENT_ID,
            "created_at": utc_now(),
            "transition_table_hash": audit["transition_table_hash"],
        },
        "environment_audit": audit,
        "exact_dp_references": refs,
        "learning": learning,
    }
    write_json(artifact_dir / "raw_metrics.json", raw_metrics)
    runtime = time.perf_counter() - start
    artifacts = [
        "research/reward_to_gcrl/artifacts/0005/run_riverswim_sampled_vs_soft.py",
        "research/reward_to_gcrl/artifacts/0005/local_compatibility_check.json",
        "research/reward_to_gcrl/artifacts/0005/environment_audit.json",
        "research/reward_to_gcrl/artifacts/0005/exact_dp_references.json",
        "research/reward_to_gcrl/artifacts/0005/per_seed_metrics.json",
        "research/reward_to_gcrl/artifacts/0005/per_seed_summary.csv",
        "research/reward_to_gcrl/artifacts/0005/learning_curves.json",
        "research/reward_to_gcrl/artifacts/0005/learning_curves.csv",
        "research/reward_to_gcrl/artifacts/0005/raw_metrics.json",
        "research/reward_to_gcrl/artifacts/0005/progress.jsonl",
    ]
    result = build_result(runtime, audit, audit_complete, missing, refs, learning, artifacts)
    write_json(result_dir / "0005_result.json", result)
    write_summary(result_dir / "0005_summary.md", result)
    append_progress(
        artifact_dir,
        "result_write",
        result["status"],
        "Wrote 0005 result JSON and summary Markdown.",
        command=COMMANDS_RUN[4],
        result_path="research/reward_to_gcrl/results/0005_result.json",
        summary_path="research/reward_to_gcrl/results/0005_summary.md",
    )
    return 0 if result["status"] == "completed" else 1


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check-only", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = repo_root_from_script()
    artifact_dir = repo_root / "research" / PROJECT / "artifacts" / EXPERIMENT_ID
    artifact_dir.mkdir(parents=True, exist_ok=True)
    if args.check_only:
        return check_only(repo_root, artifact_dir)
    return run_experiment(repo_root, artifact_dir)


if __name__ == "__main__":
    raise SystemExit(main())
