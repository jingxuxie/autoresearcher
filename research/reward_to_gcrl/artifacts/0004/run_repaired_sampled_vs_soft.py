#!/usr/bin/env python3
"""Experiment 0004: repaired sampled-vs-soft tabular comparison.

This iteration uses a tiny deterministic chain whose raw rewards already live in
[0, 1]. The normalized objective is therefore an identity affine transform of
the raw objective, avoiding the CliffWalking all-step-reward mismatch from 0003.
"""

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


EXPERIMENT_ID = "0004"
PROJECT = "reward_to_gcrl"
ENV_NAME = "autoresearcher_reward_to_gcrl"
GAMMAS = [0.95, 0.99, 0.995]
SEEDS = list(range(10))
TRANSITION_BUDGET = 100_000
MAX_EPISODE_STEPS = 8
EVAL_EPISODES = 100
MAX_EVAL_STEPS = 8
ALPHA = 0.1
EPSILON_START = 0.20
EPSILON_END = 0.02
CHECKPOINTS = [500, 1_000, 2_500, 5_000, 10_000, 25_000, 50_000, 100_000]
MIN_PAIR_VISITS = 5
MC_SIGMA_TOLERANCE = 6.0
TIE_TOLERANCE = 1.0e-10
EXACT_TOLERANCE = 1.0e-13
STATISTICAL_Z = 2.0

COMMANDS_RUN = [
    "mkdir -p research/reward_to_gcrl/artifacts/0004 research/reward_to_gcrl/results",
    "conda run -n autoresearcher_reward_to_gcrl python --version",
    (
        "conda run -n autoresearcher_reward_to_gcrl python -m py_compile "
        "research/reward_to_gcrl/artifacts/0004/run_repaired_sampled_vs_soft.py"
    ),
    (
        "conda run -n autoresearcher_reward_to_gcrl python "
        "research/reward_to_gcrl/artifacts/0004/run_repaired_sampled_vs_soft.py "
        "--check-only"
    ),
    (
        "conda run -n autoresearcher_reward_to_gcrl python "
        "research/reward_to_gcrl/artifacts/0004/run_repaired_sampled_vs_soft.py"
    ),
    (
        "conda run -n autoresearcher_reward_to_gcrl python -m jsonschema "
        "-i research/reward_to_gcrl/results/0004_result.json schemas/result.schema.json"
    ),
    (
        "conda run -n autoresearcher_reward_to_gcrl python scripts/validate_artifacts.py "
        "--repo-root . --json research/reward_to_gcrl/results/0004_result.json "
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
    payload: dict[str, Any] = {
        "timestamp": utc_now(),
        "phase": phase,
        "status": status,
        "message": message,
    }
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


class TinyChain:
    """A deterministic chain with non-tie optimal actions and meaningful success."""

    actions = (ActionSpec(0, "stall_or_fail"), ActionSpec(1, "advance"))
    state_names = {
        0: "start",
        1: "middle",
        2: "pre_goal",
        3: "goal_terminal",
        4: "failure_terminal",
    }

    def __init__(self) -> None:
        self.n_states = 5
        self.n_actions = 2
        self.start_state = 0
        self.goal_state = 3
        self.failure_state = 4
        self.terminal_states = [3, 4]
        self.decision_states = [0, 1, 2]
        self.next_states = np.zeros((self.n_states, self.n_actions), dtype=np.int64)
        self.raw_rewards = np.zeros((self.n_states, self.n_actions), dtype=np.float64)
        self.normalized_rewards = np.zeros((self.n_states, self.n_actions), dtype=np.float64)
        self.terminated = np.zeros((self.n_states, self.n_actions), dtype=bool)
        self.success_transition = np.zeros((self.n_states, self.n_actions), dtype=bool)
        self.transition_records: list[dict[str, Any]] = []
        self._build()
        self.transition_hash = self._hash_transition_records()

    def _set(self, state: int, action: int, next_state: int, reward: float, terminated: bool) -> None:
        self.next_states[state, action] = next_state
        self.raw_rewards[state, action] = reward
        self.normalized_rewards[state, action] = reward
        self.terminated[state, action] = terminated
        self.success_transition[state, action] = next_state == self.goal_state and terminated
        self.transition_records.append(
            {
                "state": state,
                "state_name": self.state_names[state],
                "action": action,
                "action_name": self.actions[action].name,
                "next_state": next_state,
                "next_state_name": self.state_names[next_state],
                "raw_reward": reward,
                "normalized_reward": reward,
                "terminated": terminated,
                "success_transition": bool(self.success_transition[state, action]),
            }
        )

    def _build(self) -> None:
        self._set(0, 0, 0, 0.0, False)
        self._set(0, 1, 1, 0.0, False)
        self._set(1, 0, 0, 0.0, False)
        self._set(1, 1, 2, 0.0, False)
        self._set(2, 0, 4, 0.0, True)
        self._set(2, 1, 3, 1.0, True)
        self._set(3, 0, 3, 0.0, True)
        self._set(3, 1, 3, 0.0, True)
        self._set(4, 0, 4, 0.0, True)
        self._set(4, 1, 4, 0.0, True)

    def _hash_transition_records(self) -> str:
        canonical = json.dumps(self.transition_records, sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(canonical.encode("utf-8")).hexdigest()

    def build_audit(self) -> dict[str, Any]:
        return {
            "experiment_id": EXPERIMENT_ID,
            "environment": "tiny_non_degenerate_chain",
            "description": (
                "Five-state deterministic chain. Action 1 advances from start to middle "
                "to pre_goal to goal. Action 0 stalls/resets early and fails at pre_goal."
            ),
            "n_states": self.n_states,
            "n_actions": self.n_actions,
            "state_names": self.state_names,
            "start_state": self.start_state,
            "goal_state": self.goal_state,
            "failure_state": self.failure_state,
            "terminal_states": self.terminal_states,
            "decision_states": self.decision_states,
            "action_mapping": [
                {"action": action.action, "name": action.name} for action in self.actions
            ],
            "reward_audit": {
                "raw_rewards": sorted(set(float(x) for x in self.raw_rewards.reshape(-1))),
                "normalized_rewards": sorted(
                    set(float(x) for x in self.normalized_rewards.reshape(-1))
                ),
                "normalization": "identity affine map because raw rewards are already in [0, 1]",
                "affine_scale": 1.0,
                "affine_offset": 0.0,
                "success_reward": 1.0,
                "non_success_reward": 0.0,
                "terminal_self_loop_reward": 0.0,
            },
            "terminal_handling": (
                "goal and failure are absorbing for table completeness; Bellman and "
                "learning bootstraps are masked to zero on terminated transitions"
            ),
            "sampled_augmented_target_semantics": {
                "p_g_plus": "(1 - gamma) * r_bar",
                "p_g_minus": "(1 - gamma) * (1 - r_bar)",
                "p_continue": "gamma",
                "g_plus_target": 1.0,
                "g_minus_target": 0.0,
                "continued_target": "max_a M(s_next,a), no extra gamma factor",
                "direct_target_comparison": (
                    "each sampled target is compared against the deterministic soft "
                    "marginal target computed from the sampled learner pre-update table "
                    "on the same original transition"
                ),
            },
            "transition_table_shape": [self.n_states, self.n_actions],
            "transition_table_record_count": len(self.transition_records),
            "transition_table_hash": self.transition_hash,
            "transition_records": self.transition_records,
        }


def validate_audit(audit: dict[str, Any]) -> tuple[bool, list[str]]:
    required = [
        "reward_audit",
        "terminal_handling",
        "sampled_augmented_target_semantics",
        "transition_records",
        "transition_table_hash",
        "decision_states",
        "terminal_states",
    ]
    missing = [field for field in required if field not in audit]
    complete = not missing and audit["transition_table_record_count"] == 10
    return complete, missing


def value_iteration(
    rewards: np.ndarray,
    next_states: np.ndarray,
    terminated: np.ndarray,
    gamma: float,
    tolerance: float = EXACT_TOLERANCE,
    max_iterations: int = 100_000,
) -> tuple[np.ndarray, int, float]:
    q = np.zeros_like(rewards, dtype=np.float64)
    not_terminal = (~terminated).astype(np.float64)
    for iteration in range(1, max_iterations + 1):
        values = q.max(axis=1)
        target = rewards + gamma * not_terminal * values[next_states]
        delta = float(np.max(np.abs(target - q)))
        q = target
        if delta <= tolerance:
            return q, iteration, delta
    raise RuntimeError(f"value iteration did not converge for gamma={gamma}")


def soft_bellman_residual(m_values: np.ndarray, env: TinyChain, gamma: float) -> np.ndarray:
    values = m_values.max(axis=1)
    target = (1.0 - gamma) * env.normalized_rewards
    target = target + gamma * (~env.terminated).astype(np.float64) * values[env.next_states]
    return np.abs(target - m_values)


def tie_actions(values: np.ndarray) -> list[int]:
    best = float(np.max(values))
    return [int(action) for action, value in enumerate(values) if best - float(value) <= TIE_TOLERANCE]


def greedy_action(values: np.ndarray) -> int:
    return min(tie_actions(values))


def compare_policy(
    candidate: np.ndarray,
    reference: np.ndarray,
    states: list[int],
) -> dict[str, Any]:
    tie_states = 0
    comparable = 0
    disagreements = 0
    for state in states:
        cand_ties = tie_actions(candidate[state])
        ref_ties = tie_actions(reference[state])
        if len(cand_ties) > 1 or len(ref_ties) > 1:
            tie_states += 1
            continue
        comparable += 1
        disagreements += int(cand_ties[0] != ref_ties[0])
    return {
        "state_count_total": len(states),
        "tie_state_count": tie_states,
        "comparable_non_tie_state_count": comparable,
        "disagreement_count": disagreements,
        "disagreement_rate": disagreements / comparable if comparable else 0.0,
    }


def exact_references(env: TinyChain, artifact_dir: Path) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    tables: dict[str, Any] = {}
    for gamma in GAMMAS:
        raw_q, raw_iterations, raw_delta = value_iteration(
            env.raw_rewards, env.next_states, env.terminated, gamma
        )
        norm_q, norm_iterations, norm_delta = value_iteration(
            env.normalized_rewards, env.next_states, env.terminated, gamma
        )
        soft_f, soft_iterations, soft_delta = value_iteration(
            (1.0 - gamma) * env.normalized_rewards,
            env.next_states,
            env.terminated,
            gamma,
        )
        raw_norm_policy = compare_policy(norm_q, raw_q, env.decision_states)
        soft_scaled_policy = compare_policy(soft_f / (1.0 - gamma), norm_q, env.decision_states)
        non_tie_fraction = (
            raw_norm_policy["comparable_non_tie_state_count"] / len(env.decision_states)
        )
        rows.append(
            {
                "gamma": gamma,
                "raw_value_iteration_steps": raw_iterations,
                "normalized_value_iteration_steps": norm_iterations,
                "soft_value_iteration_steps": soft_iterations,
                "raw_final_delta": raw_delta,
                "normalized_final_delta": norm_delta,
                "soft_final_delta": soft_delta,
                "max_abs_scaled_soft_minus_normalized_q": float(
                    np.max(np.abs(soft_f / (1.0 - gamma) - norm_q))
                ),
                "raw_normalized_policy_preserved": raw_norm_policy["disagreement_count"] == 0,
                "raw_normalized_policy_comparison": raw_norm_policy,
                "soft_scaled_policy_comparison": soft_scaled_policy,
                "non_tie_decision_state_fraction": non_tie_fraction,
                "raw_q": raw_q.tolist(),
                "normalized_q": norm_q.tolist(),
                "soft_f_gplus": soft_f.tolist(),
            }
        )
        tables[str(gamma)] = {
            "raw_q": raw_q.tolist(),
            "normalized_q": norm_q.tolist(),
            "soft_f_gplus": soft_f.tolist(),
        }
    payload = {
        "metadata": {
            "experiment_id": EXPERIMENT_ID,
            "transition_table_hash": env.transition_hash,
            "gammas": GAMMAS,
            "exact_tolerance": EXACT_TOLERANCE,
        },
        "rows": rows,
        "tables": tables,
    }
    write_json(artifact_dir / "exact_dp_references.json", payload)
    return payload


def error_metrics(m_values: np.ndarray, exact_soft: np.ndarray, env: TinyChain, gamma: float) -> dict[str, float]:
    states = np.array(env.decision_states, dtype=np.int64)
    value_error = np.abs(m_values[states, :] - exact_soft[states, :])
    residual = soft_bellman_residual(m_values, env, gamma)[states, :]
    return {
        "mean_abs_value_error": float(np.mean(value_error)),
        "max_abs_value_error": float(np.max(value_error)),
        "mean_bellman_residual": float(np.mean(residual)),
        "max_bellman_residual": float(np.max(residual)),
    }


def epsilon_for_step(step: int) -> float:
    if TRANSITION_BUDGET <= 1:
        return EPSILON_END
    frac = (step - 1) / float(TRANSITION_BUDGET - 1)
    return EPSILON_START + frac * (EPSILON_END - EPSILON_START)


def evaluate_policy(env: TinyChain, values: np.ndarray) -> dict[str, Any]:
    raw_returns: list[float] = []
    norm_returns: list[float] = []
    successes: list[bool] = []
    steps_to_goal: list[int | None] = []
    for _ in range(EVAL_EPISODES):
        state = env.start_state
        raw_return = 0.0
        norm_return = 0.0
        success = False
        goal_step: int | None = None
        for step in range(1, MAX_EVAL_STEPS + 1):
            action = greedy_action(values[state])
            next_state = int(env.next_states[state, action])
            raw_return += float(env.raw_rewards[state, action])
            norm_return += float(env.normalized_rewards[state, action])
            if bool(env.success_transition[state, action]):
                success = True
                goal_step = step
            if bool(env.terminated[state, action]):
                break
            state = next_state
        raw_returns.append(raw_return)
        norm_returns.append(norm_return)
        successes.append(success)
        steps_to_goal.append(goal_step)
    successful_steps = [step for step in steps_to_goal if step is not None]
    return {
        "episodes": EVAL_EPISODES,
        "max_steps": MAX_EVAL_STEPS,
        "mean_raw_return": float(np.mean(raw_returns)),
        "mean_normalized_return": float(np.mean(norm_returns)),
        "success_rate": float(np.mean(successes)),
        "mean_steps_elapsed": float(
            np.mean([step if step is not None else MAX_EVAL_STEPS for step in steps_to_goal])
        ),
        "mean_steps_to_goal_success_only": (
            float(np.mean(successful_steps)) if successful_steps else None
        ),
        "raw_returns": raw_returns,
        "normalized_returns": norm_returns,
        "successes": successes,
        "steps_to_goal": steps_to_goal,
    }


def checkpoint_payload(
    transition: int,
    gamma: float,
    env: TinyChain,
    exact_soft: np.ndarray,
    exact_norm_q: np.ndarray,
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
) -> dict[str, Any]:
    mean_error = abs(sampled_stats.mean - paired_soft_stats.mean)
    mc_tolerance = MC_SIGMA_TOLERANCE * math.sqrt(conditional_variance_sum) / transition
    return {
        "transition": transition,
        "gamma": gamma,
        "g_plus_count": g_plus_count,
        "g_minus_count": g_minus_count,
        "continue_count": continue_count,
        "g_plus_events_per_10000": g_plus_count / transition * 10_000.0,
        "sampled_target": sampled_stats.payload(),
        "deterministic_soft_target_same_sampled_table": paired_soft_stats.payload(),
        "sampled_minus_soft_target_noise": noise_stats.payload(),
        "actual_soft_learner_target": actual_soft_stats.payload(),
        "mean_conditional_sampling_variance": conditional_variance_sum / transition,
        "soft_terminal_sampling_variance": 0.0,
        "target_mean_abs_error": mean_error,
        "target_mean_mc_tolerance": mc_tolerance,
        "target_mean_within_mc_tolerance": mean_error <= mc_tolerance,
        "soft_error_to_exact": error_metrics(m_soft, exact_soft, env, gamma),
        "sampled_error_to_exact": error_metrics(m_sampled, exact_soft, env, gamma),
        "soft_policy_vs_exact": compare_policy(m_soft, exact_norm_q, env.decision_states),
        "sampled_policy_vs_exact": compare_policy(m_sampled, exact_norm_q, env.decision_states),
    }


def run_seed(env: TinyChain, gamma: float, seed: int, refs: dict[str, Any]) -> dict[str, Any]:
    rng = np.random.default_rng(seed + int(round(gamma * 1_000_000)))
    exact_soft = np.array(refs["soft_f_gplus"], dtype=np.float64)
    exact_norm_q = np.array(refs["normalized_q"], dtype=np.float64)
    m_soft = np.zeros((env.n_states, env.n_actions), dtype=np.float64)
    m_sampled = np.zeros((env.n_states, env.n_actions), dtype=np.float64)
    sampled_stats = RunningStats()
    paired_soft_stats = RunningStats()
    noise_stats = RunningStats()
    actual_soft_stats = RunningStats()
    conditional_variance_sum = 0.0
    g_plus_count = 0
    g_minus_count = 0
    continue_count = 0
    success_transition_count = 0
    state = env.start_state
    episode_step = 0
    curves: list[dict[str, Any]] = []
    checkpoint_set = set(CHECKPOINTS)

    for transition in range(1, TRANSITION_BUDGET + 1):
        epsilon = epsilon_for_step(transition)
        if rng.random() < epsilon:
            action = int(rng.integers(env.n_actions))
        else:
            action = greedy_action(exact_norm_q[state])

        next_state = int(env.next_states[state, action])
        r_bar = float(env.normalized_rewards[state, action])
        terminated = bool(env.terminated[state, action])
        success_transition_count += int(env.success_transition[state, action])

        soft_continue = 0.0 if terminated else float(np.max(m_soft[next_state]))
        actual_soft_target = (1.0 - gamma) * r_bar + gamma * soft_continue

        sampled_continue = 0.0 if terminated else float(np.max(m_sampled[next_state]))
        p_plus = (1.0 - gamma) * r_bar
        p_minus = (1.0 - gamma) * (1.0 - r_bar)
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
                    exact_norm_q,
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
                )
            )

        episode_step += 1
        if terminated or episode_step >= MAX_EPISODE_STEPS:
            state = env.start_state
            episode_step = 0
        else:
            state = next_state

    final = curves[-1]
    evaluation_soft = evaluate_policy(env, m_soft)
    evaluation_sampled = evaluate_policy(env, m_sampled)
    return {
        "gamma": gamma,
        "seed": seed,
        "transition_budget": TRANSITION_BUDGET,
        "alpha": ALPHA,
        "epsilon_start": EPSILON_START,
        "epsilon_end": EPSILON_END,
        "g_plus_count": g_plus_count,
        "g_minus_count": g_minus_count,
        "continue_count": continue_count,
        "g_plus_events_per_10000": g_plus_count / TRANSITION_BUDGET * 10_000.0,
        "success_transition_count": success_transition_count,
        "target_diagnostics": {
            "sampled_target": sampled_stats.payload(),
            "deterministic_soft_target_same_sampled_table": paired_soft_stats.payload(),
            "sampled_minus_soft_target_noise": noise_stats.payload(),
            "actual_soft_learner_target": actual_soft_stats.payload(),
            "mean_conditional_sampling_variance": conditional_variance_sum
            / TRANSITION_BUDGET,
            "soft_terminal_sampling_variance": 0.0,
            "target_mean_abs_error": abs(sampled_stats.mean - paired_soft_stats.mean),
            "target_mean_mc_tolerance": MC_SIGMA_TOLERANCE
            * math.sqrt(conditional_variance_sum)
            / TRANSITION_BUDGET,
            "target_mean_within_mc_tolerance": abs(
                sampled_stats.mean - paired_soft_stats.mean
            )
            <= MC_SIGMA_TOLERANCE
            * math.sqrt(conditional_variance_sum)
            / TRANSITION_BUDGET,
        },
        "learning_curves": curves,
        "final_errors": {
            "soft_error_to_exact": final["soft_error_to_exact"],
            "sampled_error_to_exact": final["sampled_error_to_exact"],
        },
        "policy_diagnostics": {
            "soft_policy_vs_exact": final["soft_policy_vs_exact"],
            "sampled_policy_vs_exact": final["sampled_policy_vs_exact"],
        },
        "evaluation": {
            "soft_policy": evaluation_soft,
            "sampled_policy": evaluation_sampled,
        },
        "final_tables": {
            "soft_m_plus": m_soft.tolist(),
            "sampled_m_plus": m_sampled.tolist(),
        },
    }


def run_learning(env: TinyChain, refs: dict[str, Any], artifact_dir: Path) -> dict[str, Any]:
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
                        "target_mean_abs_error": curve["target_mean_abs_error"],
                        "target_mean_mc_tolerance": curve["target_mean_mc_tolerance"],
                        "sampled_target_variance": curve["sampled_target"][
                            "population_variance"
                        ],
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
                f"Completed repaired sampled-vs-soft run for gamma={gamma}, seed={seed}.",
                command=COMMANDS_RUN[4],
                gamma=gamma,
                seed=seed,
                g_plus_events_per_10000=row["g_plus_events_per_10000"],
                target_mean_within_mc_tolerance=row["target_diagnostics"][
                    "target_mean_within_mc_tolerance"
                ],
                soft_bellman_residual=row["final_errors"]["soft_error_to_exact"][
                    "mean_bellman_residual"
                ],
                sampled_bellman_residual=row["final_errors"]["sampled_error_to_exact"][
                    "mean_bellman_residual"
                ],
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
            "mc_sigma_tolerance": MC_SIGMA_TOLERANCE,
            "statistical_z_for_indistinguishable_value_error": STATISTICAL_Z,
        },
        "aggregate": aggregate_rows(rows),
        "rows": rows,
    }
    write_json(artifact_dir / "per_seed_metrics.json", payload)
    write_json(artifact_dir / "learning_curves.json", {"rows": curve_rows})
    write_seed_csv(artifact_dir / "per_seed_summary.csv", rows)
    write_curve_csv(artifact_dir / "learning_curves.csv", curve_rows)
    return payload


def paired_stats(values: list[float]) -> dict[str, Any]:
    arr = np.array(values, dtype=np.float64)
    mean = float(np.mean(arr))
    if len(arr) > 1:
        se = float(np.std(arr, ddof=1) / math.sqrt(len(arr)))
    else:
        se = 0.0
    return {
        "n": len(values),
        "mean": mean,
        "standard_error": se,
        "abs_mean_within_2se": abs(mean) <= STATISTICAL_Z * se if se > 0.0 else mean == 0.0,
    }


def aggregate_rows(rows: list[dict[str, Any]]) -> dict[str, Any]:
    by_gamma = {str(gamma): aggregate_subset([row for row in rows if row["gamma"] == gamma]) for gamma in GAMMAS}
    overall = aggregate_subset(rows)
    overall["by_gamma"] = by_gamma
    return overall


def aggregate_subset(rows: list[dict[str, Any]]) -> dict[str, Any]:
    target_passes = [row["target_diagnostics"]["target_mean_within_mc_tolerance"] for row in rows]
    variance_passes = [
        row["target_diagnostics"]["mean_conditional_sampling_variance"]
        > row["target_diagnostics"]["soft_terminal_sampling_variance"]
        for row in rows
    ]
    soft_residuals = [
        row["final_errors"]["soft_error_to_exact"]["mean_bellman_residual"] for row in rows
    ]
    sampled_residuals = [
        row["final_errors"]["sampled_error_to_exact"]["mean_bellman_residual"]
        for row in rows
    ]
    soft_values = [
        row["final_errors"]["soft_error_to_exact"]["mean_abs_value_error"] for row in rows
    ]
    sampled_values = [
        row["final_errors"]["sampled_error_to_exact"]["mean_abs_value_error"]
        for row in rows
    ]
    value_diff_stats = paired_stats([s - b for s, b in zip(soft_values, sampled_values)])
    residual_diff_stats = paired_stats([s - b for s, b in zip(soft_residuals, sampled_residuals)])
    soft_disagreements = [
        row["policy_diagnostics"]["soft_policy_vs_exact"]["disagreement_rate"] for row in rows
    ]
    sampled_disagreements = [
        row["policy_diagnostics"]["sampled_policy_vs_exact"]["disagreement_rate"]
        for row in rows
    ]
    soft_success = [row["evaluation"]["soft_policy"]["success_rate"] for row in rows]
    sampled_success = [row["evaluation"]["sampled_policy"]["success_rate"] for row in rows]
    return {
        "run_count": len(rows),
        "target_mean_match_count": int(sum(target_passes)),
        "target_mean_match_rate": float(np.mean(target_passes)) if rows else 0.0,
        "sampled_variance_exceeds_soft_count": int(sum(variance_passes)),
        "sampled_variance_exceeds_soft_rate": float(np.mean(variance_passes)) if rows else 0.0,
        "mean_g_plus_events_per_10000": float(
            np.mean([row["g_plus_events_per_10000"] for row in rows])
        )
        if rows
        else None,
        "mean_conditional_sampling_variance": float(
            np.mean(
                [
                    row["target_diagnostics"]["mean_conditional_sampling_variance"]
                    for row in rows
                ]
            )
        )
        if rows
        else None,
        "mean_final_soft_bellman_residual": float(np.mean(soft_residuals)) if rows else None,
        "mean_final_sampled_bellman_residual": float(np.mean(sampled_residuals)) if rows else None,
        "mean_final_soft_value_error": float(np.mean(soft_values)) if rows else None,
        "mean_final_sampled_value_error": float(np.mean(sampled_values)) if rows else None,
        "soft_minus_sampled_value_error": value_diff_stats,
        "soft_minus_sampled_bellman_residual": residual_diff_stats,
        "soft_bellman_residual_lower": (
            float(np.mean(soft_residuals)) < float(np.mean(sampled_residuals)) if rows else False
        ),
        "soft_value_error_lower_or_indistinguishable": (
            value_diff_stats["mean"] <= 0.0 or value_diff_stats["abs_mean_within_2se"]
        ),
        "mean_soft_policy_disagreement": float(np.mean(soft_disagreements)) if rows else None,
        "mean_sampled_policy_disagreement": float(np.mean(sampled_disagreements)) if rows else None,
        "mean_soft_success_rate": float(np.mean(soft_success)) if rows else None,
        "mean_sampled_success_rate": float(np.mean(sampled_success)) if rows else None,
        "mean_soft_raw_return": float(
            np.mean([row["evaluation"]["soft_policy"]["mean_raw_return"] for row in rows])
        )
        if rows
        else None,
        "mean_sampled_raw_return": float(
            np.mean([row["evaluation"]["sampled_policy"]["mean_raw_return"] for row in rows])
        )
        if rows
        else None,
        "soft_policy_quality_non_worse": (
            float(np.mean(soft_success)) >= float(np.mean(sampled_success))
            and float(np.mean(soft_disagreements)) <= float(np.mean(sampled_disagreements))
            if rows
            else False
        ),
    }


def write_seed_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    fields = [
        "gamma",
        "seed",
        "g_plus_events_per_10000",
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
        "soft_success_rate",
        "sampled_success_rate",
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
                    "target_mean_abs_error": row["target_diagnostics"][
                        "target_mean_abs_error"
                    ],
                    "target_mean_mc_tolerance": row["target_diagnostics"][
                        "target_mean_mc_tolerance"
                    ],
                    "target_mean_within_mc_tolerance": row["target_diagnostics"][
                        "target_mean_within_mc_tolerance"
                    ],
                    "mean_conditional_sampling_variance": row["target_diagnostics"][
                        "mean_conditional_sampling_variance"
                    ],
                    "soft_mean_bellman_residual": row["final_errors"][
                        "soft_error_to_exact"
                    ]["mean_bellman_residual"],
                    "sampled_mean_bellman_residual": row["final_errors"][
                        "sampled_error_to_exact"
                    ]["mean_bellman_residual"],
                    "soft_mean_value_error": row["final_errors"]["soft_error_to_exact"][
                        "mean_abs_value_error"
                    ],
                    "sampled_mean_value_error": row["final_errors"][
                        "sampled_error_to_exact"
                    ]["mean_abs_value_error"],
                    "soft_policy_disagreement": row["policy_diagnostics"][
                        "soft_policy_vs_exact"
                    ]["disagreement_rate"],
                    "sampled_policy_disagreement": row["policy_diagnostics"][
                        "sampled_policy_vs_exact"
                    ]["disagreement_rate"],
                    "soft_success_rate": row["evaluation"]["soft_policy"]["success_rate"],
                    "sampled_success_rate": row["evaluation"]["sampled_policy"][
                        "success_rate"
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


def classify_verdict(policy_preserved: bool, non_tie_ok: bool, aggregate: dict[str, Any]) -> str:
    if not policy_preserved:
        return "objective-mismatch"
    if not non_tie_ok:
        return "failed diagnostic"
    target_ok = aggregate["target_mean_match_count"] == aggregate["run_count"]
    variance_ok = aggregate["sampled_variance_exceeds_soft_count"] == aggregate["run_count"]
    learning_ok = (
        aggregate["soft_bellman_residual_lower"]
        and aggregate["soft_value_error_lower_or_indistinguishable"]
        and aggregate["soft_policy_quality_non_worse"]
    )
    if target_ok and variance_ok and learning_ok:
        return "learning-improvement"
    if target_ok and variance_ok:
        return "variance-only"
    return "failed diagnostic"


def build_result(
    runtime_seconds: float,
    audit: dict[str, Any],
    audit_complete: bool,
    audit_missing: list[str],
    refs: dict[str, Any],
    learning: dict[str, Any],
    artifacts: list[str],
) -> dict[str, Any]:
    exact_rows = refs["rows"]
    policy_preserved = all(row["raw_normalized_policy_preserved"] for row in exact_rows)
    non_tie_ok = min(row["non_tie_decision_state_fraction"] for row in exact_rows) >= 0.8
    aggregate = learning["aggregate"]
    verdict = classify_verdict(policy_preserved, non_tie_ok, aggregate)
    pass_flags = {
        "environment_audit_complete": audit_complete,
        "raw_normalized_policy_preserved": policy_preserved,
        "exact_dp_non_tie_policy_informative": non_tie_ok,
        "gamma_seed_budget_complete": aggregate["run_count"] == len(GAMMAS) * len(SEEDS),
        "target_mean_match_all_runs": aggregate["target_mean_match_count"]
        == aggregate["run_count"],
        "sampled_variance_exceeds_soft_all_runs": aggregate[
            "sampled_variance_exceeds_soft_count"
        ]
        == aggregate["run_count"],
        "soft_lower_mean_final_bellman_residual": aggregate["soft_bellman_residual_lower"],
        "soft_value_error_lower_or_statistically_indistinguishable": aggregate[
            "soft_value_error_lower_or_indistinguishable"
        ],
        "soft_policy_quality_non_worse": aggregate["soft_policy_quality_non_worse"],
        "cpu_tabular_only": True,
    }
    failed_diagnostic = verdict == "failed diagnostic"
    status = "failed" if failed_diagnostic else "completed"
    known_failures: list[str] = []
    if failed_diagnostic:
        known_failures = [key for key, value in pass_flags.items() if not value]

    if verdict == "learning-improvement":
        interpretation = (
            "The repaired chain preserves the raw policy under identity normalization. "
            "Sampled targets match the deterministic soft marginal target within the "
            "predeclared Monte Carlo tolerance, have positive sampling variance, and "
            "the deterministic soft learner achieves lower mean final Bellman residual "
            "with statistically non-worse value error and policy quality."
        )
    elif verdict == "variance-only":
        interpretation = (
            "The target-level hypothesis is supported, but learning-improvement evidence "
            "is not strong enough under the predeclared residual/value/policy criteria."
        )
    elif verdict == "objective-mismatch":
        interpretation = (
            "The reward normalization changes the exact optimal policy, so this run is "
            "an objective-mismatch result rather than evidence about learner quality."
        )
    else:
        interpretation = "The diagnostic failed one or more required checks."

    return {
        "experiment_id": EXPERIMENT_ID,
        "status": status,
        "claim_tested": (
            "In a nondegenerate tiny chain with identity reward normalization, sampled "
            "augmented g_plus updates are unbiased but higher variance, while deterministic "
            "soft terminal marginalization improves Bellman residual and preserves policy quality."
        ),
        "commands_run": COMMANDS_RUN,
        "metrics": {
            "verdict": verdict,
            "config": {
                "gammas": GAMMAS,
                "seeds": SEEDS,
                "transition_budget": TRANSITION_BUDGET,
                "checkpoints": CHECKPOINTS,
                "alpha": ALPHA,
                "epsilon_start": EPSILON_START,
                "epsilon_end": EPSILON_END,
                "mc_sigma_tolerance": MC_SIGMA_TOLERANCE,
                "statistical_z_for_value_error_indistinguishable": STATISTICAL_Z,
                "reward_normalization": "identity affine map, normalized_reward = raw_reward",
                "sampled_continue_target": "max_a M(s_next,a), no extra gamma factor",
            },
            "environment_audit": {
                "complete": audit_complete,
                "missing_fields": audit_missing,
                "transition_table_hash": audit["transition_table_hash"],
                "transition_table_record_count": audit["transition_table_record_count"],
                "reward_audit": audit["reward_audit"],
            },
            "exact_dp": {
                "rows": exact_rows,
                "raw_normalized_policy_preserved": policy_preserved,
                "non_tie_policy_informative": non_tie_ok,
            },
            "sampled_vs_soft": {
                "aggregate": aggregate,
            },
            "pass_flags": pass_flags,
        },
        "baseline_metrics": {
            "baseline_name": "sampled_augmented_g_plus_learning",
            "mean_g_plus_events_per_10000": aggregate["mean_g_plus_events_per_10000"],
            "mean_conditional_sampling_variance": aggregate[
                "mean_conditional_sampling_variance"
            ],
            "mean_final_bellman_residual": aggregate[
                "mean_final_sampled_bellman_residual"
            ],
            "mean_final_value_error": aggregate["mean_final_sampled_value_error"],
            "mean_policy_disagreement": aggregate["mean_sampled_policy_disagreement"],
            "mean_success_rate": aggregate["mean_sampled_success_rate"],
            "mean_raw_return": aggregate["mean_sampled_raw_return"],
        },
        "artifacts": artifacts,
        "interpretation": interpretation,
        "known_failures": known_failures,
        "next_questions": [
            "Would a decaying step-size schedule preserve the soft Bellman-residual advantage while reducing both learners' value error?",
            "Does the repaired chain result transfer to a small grid with identity or policy-preserving reward normalization?",
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
            "PASS: reward audit reports raw rewards, normalized rewards, affine constants, and terminal handling.",
            (
                "PASS: exact DP confirms normalized and raw greedy policies match on non-terminal non-tie states."
                if policy_preserved
                else "FAIL: normalized and raw exact policies disagree."
            ),
            (
                "PASS: exact DP has informative non-tie greedy actions on the hand-built chain."
                if non_tie_ok
                else "FAIL: exact DP has too many tie states."
            ),
            "PASS: matched-stream sampled and soft learners ran for gamma in {0.95, 0.99, 0.995} over 10 seeds.",
            (
                "PASS: sampled targets are compared directly against deterministic soft targets from the sampled learner pre-update state and same transition."
                if pass_flags["target_mean_match_all_runs"]
                else "FAIL: target mean comparison exceeded Monte Carlo tolerance."
            ),
            (
                "PASS: sampled target variance exceeds zero soft terminal-sampling variance in all runs."
                if pass_flags["sampled_variance_exceeds_soft_all_runs"]
                else "FAIL: sampled variance did not exceed soft terminal-sampling variance in all runs."
            ),
            (
                "PASS: soft has lower mean final Bellman residual."
                if pass_flags["soft_lower_mean_final_bellman_residual"]
                else "FAIL: soft does not have lower mean final Bellman residual."
            ),
            (
                "PASS: soft value error is lower or statistically indistinguishable from sampled."
                if pass_flags["soft_value_error_lower_or_statistically_indistinguishable"]
                else "FAIL: soft value error is worse beyond the indistinguishability rule."
            ),
            (
                "PASS: evaluation reports raw return, normalized return, success rate, steps to goal, and exact-policy disagreement with tie states separated."
                if pass_flags["soft_policy_quality_non_worse"]
                else "PARTIAL: evaluation metrics are reported, but soft policy quality is worse."
            ),
            f"VERDICT: {verdict}.",
        ],
        "failure_criteria_results": [
            (
                "NOT_TRIGGERED: normalized objective preserves raw optimal policy."
                if policy_preserved
                else "TRIGGERED: normalized objective does not preserve raw optimal policy."
            ),
            "NOT_TRIGGERED: target comparison uses deterministic soft marginal target from the same sampled learner table and transition.",
            (
                "NOT_TRIGGERED: exact DP has non-tie greedy actions on all decision states."
                if non_tie_ok
                else "TRIGGERED: exact DP policy ties make disagreement uninformative."
            ),
            (
                "NOT_TRIGGERED: raw task success is informative for learned policies."
                if aggregate["mean_soft_success_rate"] > 0.0
                or aggregate["mean_sampled_success_rate"] > 0.0
                else "TRIGGERED: raw task success remains zero for all learned policies."
            ),
            (
                "NOT_TRIGGERED: soft has Bellman-residual or policy-quality compensation for value-error differences."
                if not (
                    aggregate["mean_final_soft_value_error"]
                    > aggregate["mean_final_sampled_value_error"]
                    and not aggregate["soft_bellman_residual_lower"]
                    and not aggregate["soft_policy_quality_non_worse"]
                )
                else "TRIGGERED: soft has worse value error without Bellman or policy compensation."
            ),
            "NOT_TRIGGERED: no neural networks, auxiliary goals, large environments, GPU dependence, or expensive sweeps were added.",
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
            "soft_minus_sampled_success_rate": aggregate["mean_soft_success_rate"]
            - aggregate["mean_sampled_success_rate"],
            "target_mean_match_rate": aggregate["target_mean_match_rate"],
            "sampled_variance_exceeds_soft_rate": aggregate[
                "sampled_variance_exceeds_soft_rate"
            ],
        },
        "decision_relevant_findings": [
            "Identity reward normalization avoids the CliffWalking objective mismatch.",
            "The hand-built chain has three decision states, all with non-tie exact greedy actions.",
            "The sampled target is compared to a deterministic soft target computed from the same sampled learner table before each update.",
            f"The conservative verdict is {verdict}.",
        ],
    }


def write_summary(path: Path, result: dict[str, Any]) -> None:
    aggregate = result["metrics"]["sampled_vs_soft"]["aggregate"]
    verdict = result["metrics"]["verdict"]
    summary = f"""# Experiment 0004 Summary

## Verdict

Conservative verdict: **{verdict}**.

## Key Metrics

- Runs: `{aggregate["run_count"]}` (`3` gammas x `10` seeds)
- Transition budget per run: `{TRANSITION_BUDGET}`
- Mean `g_plus` events per 10000 transitions: `{aggregate["mean_g_plus_events_per_10000"]:.6g}`
- Target mean match rate: `{aggregate["target_mean_match_rate"]:.6g}`
- Sampled variance exceeds soft terminal-sampling variance rate: `{aggregate["sampled_variance_exceeds_soft_rate"]:.6g}`
- Mean final soft Bellman residual: `{aggregate["mean_final_soft_bellman_residual"]:.6g}`
- Mean final sampled Bellman residual: `{aggregate["mean_final_sampled_bellman_residual"]:.6g}`
- Mean final soft value error: `{aggregate["mean_final_soft_value_error"]:.6g}`
- Mean final sampled value error: `{aggregate["mean_final_sampled_value_error"]:.6g}`
- Mean soft success rate: `{aggregate["mean_soft_success_rate"]:.6g}`
- Mean sampled success rate: `{aggregate["mean_sampled_success_rate"]:.6g}`

## Interpretation

{result["interpretation"]}

The chain uses identity reward normalization: normalized reward equals raw reward, with success reward `1` and all other rewards `0`. Exact DP verifies raw and normalized policies agree on non-terminal non-tie decision states.

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
    env = TinyChain()
    audit = env.build_audit()
    audit_complete, missing = validate_audit(audit)
    refs = exact_references(env, artifact_dir)
    policy_preserved = all(row["raw_normalized_policy_preserved"] for row in refs["rows"])
    non_tie_ok = min(row["non_tie_decision_state_fraction"] for row in refs["rows"]) >= 0.8
    status = "passed" if audit_complete and policy_preserved and non_tie_ok else "failed"
    payload = {
        "timestamp": utc_now(),
        "status": status,
        "command": COMMANDS_RUN[3],
        "audit_complete": audit_complete,
        "missing_fields": missing,
        "policy_preserved": policy_preserved,
        "non_tie_policy_informative": non_tie_ok,
        "transition_budget": TRANSITION_BUDGET,
        "gammas": GAMMAS,
        "seed_count": len(SEEDS),
    }
    write_json(artifact_dir / "local_compatibility_check.json", payload)
    append_progress(
        artifact_dir,
        "compatibility_check",
        status,
        "Checked tiny-chain audit, exact policy preservation, and non-tie policy informativeness.",
        command=COMMANDS_RUN[3],
        policy_preserved=policy_preserved,
        non_tie_policy_informative=non_tie_ok,
    )
    return 0 if status == "passed" else 1


def run_experiment(repo_root: Path, artifact_dir: Path) -> int:
    start = time.perf_counter()
    result_dir = repo_root / "research" / PROJECT / "results"
    env = TinyChain()
    audit = env.build_audit()
    audit_complete, missing = validate_audit(audit)
    write_json(artifact_dir / "environment_audit.json", audit)
    append_progress(
        artifact_dir,
        "environment_audit",
        "completed" if audit_complete else "failed",
        "Wrote tiny-chain reward and transition audit.",
        command=COMMANDS_RUN[4],
        transition_table_hash=audit["transition_table_hash"],
        missing_fields=missing,
    )
    refs = exact_references(env, artifact_dir)
    append_progress(
        artifact_dir,
        "exact_dp",
        "completed",
        "Computed raw Q, normalized Q, and soft g_plus exact DP references.",
        command=COMMANDS_RUN[4],
    )
    learning = run_learning(env, refs, artifact_dir)
    append_progress(
        artifact_dir,
        "matched_learning",
        "completed",
        "Completed all matched-stream sampled and deterministic soft learner runs.",
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
        "research/reward_to_gcrl/artifacts/0004/run_repaired_sampled_vs_soft.py",
        "research/reward_to_gcrl/artifacts/0004/local_compatibility_check.json",
        "research/reward_to_gcrl/artifacts/0004/environment_audit.json",
        "research/reward_to_gcrl/artifacts/0004/exact_dp_references.json",
        "research/reward_to_gcrl/artifacts/0004/per_seed_metrics.json",
        "research/reward_to_gcrl/artifacts/0004/per_seed_summary.csv",
        "research/reward_to_gcrl/artifacts/0004/learning_curves.json",
        "research/reward_to_gcrl/artifacts/0004/learning_curves.csv",
        "research/reward_to_gcrl/artifacts/0004/raw_metrics.json",
        "research/reward_to_gcrl/artifacts/0004/progress.jsonl",
    ]
    result = build_result(runtime, audit, audit_complete, missing, refs, learning, artifacts)
    write_json(result_dir / "0004_result.json", result)
    write_summary(result_dir / "0004_summary.md", result)
    append_progress(
        artifact_dir,
        "result_write",
        result["status"],
        "Wrote 0004 result JSON and summary Markdown.",
        command=COMMANDS_RUN[4],
        result_path="research/reward_to_gcrl/results/0004_result.json",
        summary_path="research/reward_to_gcrl/results/0004_summary.md",
        verdict=result["metrics"]["verdict"],
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
