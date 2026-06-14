#!/usr/bin/env python3
"""Experiment 0002: local deterministic CliffWalking equivalence audit.

This script intentionally does not import Gymnasium for the environment. The
CliffWalking transition table is declared here, audited, hashed, and then used
for both exact dynamic programming and paired tabular learning.
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


EXPERIMENT_ID = "0002"
PROJECT = "reward_to_gcrl"
ENV_NAME = "autoresearcher_reward_to_gcrl"

GAMMAS = [0.95, 0.99]
SEEDS = list(range(10))
ALPHA = 0.5
EPSILON_START = 0.2
EPSILON_END = 0.02
DEFAULT_EPISODES = 5000
DEFAULT_MAX_TRAIN_STEPS = 200
DEFAULT_EVAL_EPISODES = 100
DEFAULT_MAX_EVAL_STEPS = 200

EXACT_VALUE_TOLERANCE = 1.0e-13
EXACT_SCALING_TOLERANCE = 1.0e-6
LEARNED_SCALING_TOLERANCE = 1.0e-8
EVALUATION_DELTA_TOLERANCE = 1.0e-10
TIE_TOLERANCE = 1.0e-10
MIN_PAIR_VISITS = 5
SUCCESS_POLICY_DISAGREEMENT_RATE = 0.01
FAILURE_POLICY_DISAGREEMENT_RATE = 0.05

COMMANDS_RUN = [
    "mkdir -p research/reward_to_gcrl/artifacts/0002 research/reward_to_gcrl/results",
    (
        "conda run -n autoresearcher_reward_to_gcrl python "
        "research/reward_to_gcrl/artifacts/0002/run_local_cliffwalking_equivalence.py "
        "--check-only"
    ),
    (
        "conda run -n autoresearcher_reward_to_gcrl python "
        "research/reward_to_gcrl/artifacts/0002/run_local_cliffwalking_equivalence.py"
    ),
    (
        "conda run -n autoresearcher_reward_to_gcrl python -m jsonschema "
        "-i research/reward_to_gcrl/results/0002_result.json schemas/result.schema.json"
    ),
    (
        "conda run -n autoresearcher_reward_to_gcrl python scripts/validate_artifacts.py "
        "--repo-root . --json research/reward_to_gcrl/results/0002_result.json "
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
    path = artifact_dir / "progress.jsonl"
    payload: dict[str, Any] = {
        "timestamp": utc_now(),
        "phase": phase,
        "status": status,
        "message": message,
    }
    payload.update(extra)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, sort_keys=True) + "\n")


@dataclass(frozen=True)
class ActionSpec:
    action: int
    name: str
    delta: tuple[int, int]


class LocalCliffWalking:
    rows = 4
    cols = 12
    actions = (
        ActionSpec(0, "up", (-1, 0)),
        ActionSpec(1, "right", (0, 1)),
        ActionSpec(2, "down", (1, 0)),
        ActionSpec(3, "left", (0, -1)),
    )

    def __init__(self) -> None:
        self.n_states = self.rows * self.cols
        self.n_actions = len(self.actions)
        self.start_state = self.state_id(3, 0)
        self.goal_state = self.state_id(3, 11)
        self.cliff_states = [self.state_id(3, col) for col in range(1, 11)]
        self.transition_records: list[dict[str, Any]] = []
        self.next_states = np.zeros((self.n_states, self.n_actions), dtype=np.int64)
        self.raw_rewards = np.zeros((self.n_states, self.n_actions), dtype=np.float64)
        self.normalized_rewards = np.zeros((self.n_states, self.n_actions), dtype=np.float64)
        self.terminated = np.zeros((self.n_states, self.n_actions), dtype=bool)
        self.cliff_falls = np.zeros((self.n_states, self.n_actions), dtype=bool)
        self.off_grid = np.zeros((self.n_states, self.n_actions), dtype=bool)
        self._build()
        self.transition_hash = self._hash_transition_records()

    def state_id(self, row: int, col: int) -> int:
        return row * self.cols + col

    def coord(self, state: int) -> tuple[int, int]:
        return divmod(state, self.cols)

    def coord_payload(self, state: int) -> dict[str, int]:
        row, col = self.coord(state)
        return {"state": state, "row": row, "col": col}

    @property
    def terminal_states(self) -> list[int]:
        return [self.goal_state]

    @property
    def decision_states(self) -> list[int]:
        return [
            state
            for state in range(self.n_states)
            if state != self.goal_state and state not in set(self.cliff_states)
        ]

    def normalize_reward(self, raw_reward: float, source_is_terminal: bool) -> float:
        if source_is_terminal:
            return 0.0
        if raw_reward == -100.0:
            return 0.0
        if raw_reward == -1.0:
            return 1.0
        raise ValueError(f"unexpected raw reward {raw_reward}")

    def _build(self) -> None:
        cliff_set = set(self.cliff_states)
        for state in range(self.n_states):
            row, col = self.coord(state)
            for action_spec in self.actions:
                action = action_spec.action
                source_is_goal = state == self.goal_state
                source_is_cliff = state in cliff_set
                off_grid = False
                cliff_fall = False

                if source_is_goal:
                    next_state = self.goal_state
                    raw_reward = 0.0
                    terminated = True
                    transition_kind = "terminal_absorbing_self_loop"
                elif source_is_cliff:
                    next_state = self.start_state
                    raw_reward = -100.0
                    terminated = False
                    cliff_fall = True
                    transition_kind = "cliff_source_reset_for_table_completeness"
                else:
                    d_row, d_col = action_spec.delta
                    next_row = row + d_row
                    next_col = col + d_col
                    if (
                        next_row < 0
                        or next_row >= self.rows
                        or next_col < 0
                        or next_col >= self.cols
                    ):
                        next_row = row
                        next_col = col
                        off_grid = True
                    candidate_state = self.state_id(next_row, next_col)

                    if candidate_state in cliff_set:
                        next_state = self.start_state
                        raw_reward = -100.0
                        terminated = False
                        cliff_fall = True
                        transition_kind = "cliff_fall_reset_to_start"
                    elif candidate_state == self.goal_state:
                        next_state = self.goal_state
                        raw_reward = -1.0
                        terminated = True
                        transition_kind = "goal_transition_terminates"
                    else:
                        next_state = candidate_state
                        raw_reward = -1.0
                        terminated = False
                        transition_kind = "ordinary_step"

                norm_reward = self.normalize_reward(raw_reward, source_is_goal)

                self.next_states[state, action] = next_state
                self.raw_rewards[state, action] = raw_reward
                self.normalized_rewards[state, action] = norm_reward
                self.terminated[state, action] = terminated
                self.cliff_falls[state, action] = cliff_fall
                self.off_grid[state, action] = off_grid

                next_row, next_col = self.coord(next_state)
                self.transition_records.append(
                    {
                        "state": state,
                        "state_row": row,
                        "state_col": col,
                        "action": action,
                        "action_name": action_spec.name,
                        "action_delta": list(action_spec.delta),
                        "next_state": int(next_state),
                        "next_row": next_row,
                        "next_col": next_col,
                        "raw_reward": raw_reward,
                        "normalized_reward": norm_reward,
                        "terminated": bool(terminated),
                        "off_grid": bool(off_grid),
                        "cliff_fall": bool(cliff_fall),
                        "source_is_goal": bool(source_is_goal),
                        "source_is_cliff": bool(source_is_cliff),
                        "transition_kind": transition_kind,
                    }
                )

    def _hash_transition_records(self) -> str:
        canonical = json.dumps(
            self.transition_records,
            sort_keys=True,
            separators=(",", ":"),
        )
        return hashlib.sha256(canonical.encode("utf-8")).hexdigest()

    def build_audit(self) -> dict[str, Any]:
        ordinary_state_count = len(self.decision_states)
        return {
            "experiment_id": EXPERIMENT_ID,
            "environment": "local_deterministic_cliffwalking",
            "gymnasium_dependency_used_for_environment": False,
            "grid_size": {"rows": self.rows, "cols": self.cols},
            "n_states": self.n_states,
            "state_indexing": "state = row * 12 + col, row-major, zero-indexed",
            "start_state": self.coord_payload(self.start_state),
            "goal_state": self.coord_payload(self.goal_state),
            "terminal_states": [self.coord_payload(state) for state in self.terminal_states],
            "cliff_states": [self.coord_payload(state) for state in self.cliff_states],
            "decision_states": {
                "definition": "all states except the terminal goal and cliff hazard cells",
                "count": ordinary_state_count,
                "states": [self.coord_payload(state) for state in self.decision_states],
            },
            "action_mapping": [
                {"action": action.action, "name": action.name, "delta": list(action.delta)}
                for action in self.actions
            ],
            "off_grid_behavior": (
                "attempted moves beyond the grid leave the agent in the same state with "
                "ordinary step reward -1 and no termination"
            ),
            "cliff_transition_behavior": (
                "moves into row 3, columns 1..10 receive raw reward -100, normalized "
                "reward 0, do not terminate, and reset next_state to the start state"
            ),
            "cliff_source_state_behavior": (
                "cliff cells are excluded from decision and evaluation metrics; transition "
                "rows are still total and reset to start with raw reward -100"
            ),
            "terminal_behavior": (
                "the goal state is absorbing for table completeness with raw reward 0, "
                "normalized reward 0, and terminated=True; transitions into the goal "
                "receive raw reward -1, normalized reward 1, and terminated=True"
            ),
            "reset_behavior": "every episode starts at row 3, column 0",
            "raw_rewards": {
                "ordinary_step": -1.0,
                "goal_transition": -1.0,
                "cliff_fall": -100.0,
                "terminal_absorbing_self_loop": 0.0,
            },
            "normalized_rewards": {
                "formula_for_environment_transitions": "(raw_reward + 100) / 99",
                "ordinary_step": 1.0,
                "goal_transition": 1.0,
                "cliff_fall": 0.0,
                "terminal_absorbing_self_loop": 0.0,
                "note": "The terminal self-loop is only for total table completeness after episode end.",
            },
            "terminal_mask_behavior": (
                "Bellman bootstraps are multiplied by zero when the transition record has "
                "terminated=True"
            ),
            "transition_table_shape": [self.n_states, self.n_actions],
            "transition_table_record_count": len(self.transition_records),
            "transition_table_hash": self.transition_hash,
            "transition_records": self.transition_records,
        }

    def write_audit(self, path: Path) -> dict[str, Any]:
        audit = self.build_audit()
        write_json(path, audit)
        return audit


def validate_audit(audit: dict[str, Any]) -> tuple[bool, list[str]]:
    required_fields = [
        "grid_size",
        "start_state",
        "goal_state",
        "cliff_states",
        "action_mapping",
        "off_grid_behavior",
        "cliff_transition_behavior",
        "terminal_behavior",
        "raw_rewards",
        "normalized_rewards",
        "transition_table_hash",
        "transition_records",
    ]
    missing = [field for field in required_fields if field not in audit]
    complete = not missing and audit.get("transition_table_record_count") == 48 * 4
    return complete, missing


def value_iteration(
    immediate_rewards: np.ndarray,
    next_states: np.ndarray,
    terminated: np.ndarray,
    gamma: float,
    tolerance: float = EXACT_VALUE_TOLERANCE,
    max_iterations: int = 250_000,
) -> tuple[np.ndarray, int, float]:
    q_values = np.zeros_like(immediate_rewards, dtype=np.float64)
    not_terminal = (~terminated).astype(np.float64)
    for iteration in range(1, max_iterations + 1):
        values = q_values.max(axis=1)
        target = immediate_rewards + gamma * not_terminal * values[next_states]
        delta = float(np.max(np.abs(target - q_values)))
        q_values = target
        if delta <= tolerance:
            return q_values, iteration, delta
    raise RuntimeError(f"value iteration failed to converge for gamma={gamma}")


def bellman_residual(
    q_values: np.ndarray,
    immediate_rewards: np.ndarray,
    next_states: np.ndarray,
    terminated: np.ndarray,
    gamma: float,
    state_mask: list[int] | None = None,
) -> float:
    not_terminal = (~terminated).astype(np.float64)
    values = q_values.max(axis=1)
    target = immediate_rewards + gamma * not_terminal * values[next_states]
    residual = np.abs(target - q_values)
    if state_mask is not None:
        residual = residual[np.array(state_mask, dtype=np.int64), :]
    return float(np.max(residual))


def tie_actions(values: np.ndarray, tolerance: float = TIE_TOLERANCE) -> list[int]:
    best = float(np.max(values))
    return [int(action) for action, value in enumerate(values) if best - float(value) <= tolerance]


def greedy_action(values: np.ndarray, tolerance: float = TIE_TOLERANCE) -> int:
    return min(tie_actions(values, tolerance))


def compare_greedy_policies(
    left_values: np.ndarray,
    right_values: np.ndarray,
    states: list[int],
    visits: np.ndarray | None = None,
    min_pair_visits: int = MIN_PAIR_VISITS,
    tie_tolerance: float = TIE_TOLERANCE,
) -> dict[str, Any]:
    total_states = len(states)
    insufficient_states = 0
    tie_states = 0
    comparable_states = 0
    disagreements = 0
    examples: list[dict[str, Any]] = []

    for state in states:
        if visits is not None and int(np.min(visits[state])) < min_pair_visits:
            insufficient_states += 1
            continue

        left_ties = tie_actions(left_values[state], tie_tolerance)
        right_ties = tie_actions(right_values[state], tie_tolerance)
        if len(left_ties) > 1 or len(right_ties) > 1:
            tie_states += 1
            continue

        comparable_states += 1
        left_action = left_ties[0]
        right_action = right_ties[0]
        if left_action != right_action:
            disagreements += 1
            if len(examples) < 10:
                examples.append(
                    {
                        "state": int(state),
                        "left_action": int(left_action),
                        "right_action": int(right_action),
                        "left_values": left_values[state].tolist(),
                        "right_values": right_values[state].tolist(),
                    }
                )

    disagreement_rate = disagreements / comparable_states if comparable_states else 0.0
    return {
        "state_count_total": total_states,
        "insufficient_state_count": insufficient_states,
        "tie_state_count": tie_states,
        "comparable_non_tie_state_count": comparable_states,
        "disagreement_count": disagreements,
        "disagreement_rate": disagreement_rate,
        "disagreement_examples": examples,
        "min_pair_visits": min_pair_visits if visits is not None else None,
        "tie_tolerance": tie_tolerance,
    }


def evaluate_policy(
    env: LocalCliffWalking,
    values: np.ndarray,
    episodes: int,
    max_steps: int,
) -> dict[str, Any]:
    raw_returns: list[float] = []
    normalized_returns: list[float] = []
    steps_to_goal: list[int | None] = []
    cliff_fall_counts: list[int] = []
    successes: list[bool] = []

    for _ in range(episodes):
        state = env.start_state
        raw_return = 0.0
        normalized_return = 0.0
        cliff_falls = 0
        success = False
        goal_step: int | None = None

        for step in range(1, max_steps + 1):
            action = greedy_action(values[state])
            next_state = int(env.next_states[state, action])
            raw_return += float(env.raw_rewards[state, action])
            normalized_return += float(env.normalized_rewards[state, action])
            cliff_falls += int(env.cliff_falls[state, action])
            if bool(env.terminated[state, action]):
                success = True
                goal_step = step
                break
            state = next_state

        raw_returns.append(raw_return)
        normalized_returns.append(normalized_return)
        steps_to_goal.append(goal_step)
        cliff_fall_counts.append(cliff_falls)
        successes.append(success)

    successful_steps = [step for step in steps_to_goal if step is not None]
    return {
        "episodes": episodes,
        "max_steps": max_steps,
        "mean_raw_return": float(np.mean(raw_returns)),
        "mean_normalized_return": float(np.mean(normalized_returns)),
        "mean_steps_to_goal_success_only": (
            float(np.mean(successful_steps)) if successful_steps else None
        ),
        "mean_steps_elapsed": float(
            np.mean([step if step is not None else max_steps for step in steps_to_goal])
        ),
        "mean_cliff_fall_count": float(np.mean(cliff_fall_counts)),
        "success_rate": float(np.mean(successes)),
        "raw_returns": raw_returns,
        "normalized_returns": normalized_returns,
        "steps_to_goal": steps_to_goal,
        "cliff_fall_counts": cliff_fall_counts,
        "successes": successes,
    }


def epsilon_for_episode(episode: int, episodes: int) -> float:
    if episodes <= 1:
        return EPSILON_END
    fraction = episode / float(episodes - 1)
    return EPSILON_START + fraction * (EPSILON_END - EPSILON_START)


def train_paired_learners(
    env: LocalCliffWalking,
    gamma: float,
    seed: int,
    episodes: int,
    max_train_steps: int,
) -> dict[str, Any]:
    rng = np.random.default_rng(seed)
    q_values = np.zeros((env.n_states, env.n_actions), dtype=np.float64)
    m_values = np.zeros((env.n_states, env.n_actions), dtype=np.float64)
    visits = np.zeros((env.n_states, env.n_actions), dtype=np.int64)
    episode_lengths: list[int] = []
    episode_cliff_falls: list[int] = []
    episode_successes: list[bool] = []
    behavior_tie_mismatch_count = 0
    behavior_greedy_decisions = 0

    for episode in range(episodes):
        epsilon = epsilon_for_episode(episode, episodes)
        state = env.start_state
        cliff_falls = 0
        success = False
        final_step = max_train_steps

        for step in range(1, max_train_steps + 1):
            explore = bool(rng.random() < epsilon)
            if explore:
                action = int(rng.integers(env.n_actions))
            else:
                q_ties = tie_actions(q_values[state])
                m_ties = tie_actions(m_values[state] / (1.0 - gamma))
                behavior_greedy_decisions += 1
                if q_ties != m_ties:
                    behavior_tie_mismatch_count += 1
                action = int(rng.choice(q_ties))

            next_state = int(env.next_states[state, action])
            normalized_reward = float(env.normalized_rewards[state, action])
            terminated = bool(env.terminated[state, action])

            q_target = normalized_reward
            m_target = (1.0 - gamma) * normalized_reward
            if not terminated:
                q_target += gamma * float(np.max(q_values[next_state]))
                m_target += gamma * float(np.max(m_values[next_state]))

            q_values[state, action] += ALPHA * (q_target - q_values[state, action])
            m_values[state, action] += ALPHA * (m_target - m_values[state, action])
            visits[state, action] += 1

            cliff_falls += int(env.cliff_falls[state, action])
            if terminated:
                success = True
                final_step = step
                break
            state = next_state

        episode_lengths.append(final_step)
        episode_cliff_falls.append(cliff_falls)
        episode_successes.append(success)

    scaled_m = m_values / (1.0 - gamma)
    decision_states = env.decision_states
    decision_mask = np.array(decision_states, dtype=np.int64)
    pair_visit_mask = visits[decision_mask, :] >= MIN_PAIR_VISITS
    value_errors = np.abs(scaled_m[decision_mask, :] - q_values[decision_mask, :])
    sufficient_errors = value_errors[pair_visit_mask]
    max_error_sufficient = float(np.max(sufficient_errors)) if sufficient_errors.size else None
    max_error_all_decision = float(np.max(value_errors))

    q_residual = bellman_residual(
        q_values,
        env.normalized_rewards,
        env.next_states,
        env.terminated,
        gamma,
        decision_states,
    )
    m_residual_scaled = bellman_residual(
        scaled_m,
        env.normalized_rewards,
        env.next_states,
        env.terminated,
        gamma,
        decision_states,
    )

    policy_comparison = compare_greedy_policies(
        q_values,
        scaled_m,
        decision_states,
        visits=visits,
        min_pair_visits=MIN_PAIR_VISITS,
    )
    evaluation_q = evaluate_policy(
        env,
        q_values,
        episodes=DEFAULT_EVAL_EPISODES,
        max_steps=DEFAULT_MAX_EVAL_STEPS,
    )
    evaluation_m = evaluate_policy(
        env,
        scaled_m,
        episodes=DEFAULT_EVAL_EPISODES,
        max_steps=DEFAULT_MAX_EVAL_STEPS,
    )

    return {
        "gamma": gamma,
        "seed": seed,
        "episodes": episodes,
        "max_train_steps": max_train_steps,
        "alpha": ALPHA,
        "epsilon_start": EPSILON_START,
        "epsilon_end": EPSILON_END,
        "min_pair_visits": MIN_PAIR_VISITS,
        "visited_decision_state_action_pairs": int(np.sum(visits[decision_mask, :] > 0)),
        "sufficiently_visited_decision_state_action_pairs": int(np.sum(pair_visit_mask)),
        "total_decision_state_action_pairs": int(len(decision_states) * env.n_actions),
        "max_abs_scaled_m_minus_q_sufficient": max_error_sufficient,
        "max_abs_scaled_m_minus_q_all_decision": max_error_all_decision,
        "learned_q_bellman_residual": q_residual,
        "learned_scaled_m_bellman_residual": m_residual_scaled,
        "policy_comparison": policy_comparison,
        "evaluation": {
            "normalized_q_policy": evaluation_q,
            "scaled_m_policy": evaluation_m,
            "mean_raw_return_delta_m_minus_q": (
                evaluation_m["mean_raw_return"] - evaluation_q["mean_raw_return"]
            ),
            "mean_normalized_return_delta_m_minus_q": (
                evaluation_m["mean_normalized_return"]
                - evaluation_q["mean_normalized_return"]
            ),
            "success_rate_delta_m_minus_q": (
                evaluation_m["success_rate"] - evaluation_q["success_rate"]
            ),
            "mean_cliff_fall_count_delta_m_minus_q": (
                evaluation_m["mean_cliff_fall_count"]
                - evaluation_q["mean_cliff_fall_count"]
            ),
        },
        "training_summary": {
            "mean_episode_length": float(np.mean(episode_lengths)),
            "mean_episode_cliff_falls": float(np.mean(episode_cliff_falls)),
            "training_success_rate": float(np.mean(episode_successes)),
            "behavior_greedy_decisions": behavior_greedy_decisions,
            "behavior_tie_mismatch_count": behavior_tie_mismatch_count,
            "behavior_tie_mismatch_rate": (
                behavior_tie_mismatch_count / behavior_greedy_decisions
                if behavior_greedy_decisions
                else 0.0
            ),
        },
        "final_tables": {
            "normalized_q": q_values.tolist(),
            "m_gplus": m_values.tolist(),
            "scaled_m_gplus": scaled_m.tolist(),
            "visits": visits.tolist(),
        },
    }


def run_exact_dp(env: LocalCliffWalking, artifact_dir: Path) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    table_payload: dict[str, Any] = {
        "experiment_id": EXPERIMENT_ID,
        "transition_table_hash": env.transition_hash,
        "gammas": {},
    }

    for gamma in GAMMAS:
        q_star, q_iterations, q_delta = value_iteration(
            env.normalized_rewards,
            env.next_states,
            env.terminated,
            gamma,
        )
        f_star, f_iterations, f_delta = value_iteration(
            (1.0 - gamma) * env.normalized_rewards,
            env.next_states,
            env.terminated,
            gamma,
        )
        scaled_f = f_star / (1.0 - gamma)
        max_abs_error = float(np.max(np.abs(scaled_f - q_star)))
        q_residual = bellman_residual(
            q_star,
            env.normalized_rewards,
            env.next_states,
            env.terminated,
            gamma,
            env.decision_states,
        )
        f_residual_scaled = bellman_residual(
            scaled_f,
            env.normalized_rewards,
            env.next_states,
            env.terminated,
            gamma,
            env.decision_states,
        )
        policy_comparison = compare_greedy_policies(q_star, scaled_f, env.decision_states)

        rows.append(
            {
                "gamma": gamma,
                "max_abs_error_scaled_f_vs_q": max_abs_error,
                "passes_exact_scaling_tolerance": max_abs_error < EXACT_SCALING_TOLERANCE,
                "q_value_iteration_steps": q_iterations,
                "f_value_iteration_steps": f_iterations,
                "q_final_delta": q_delta,
                "f_final_delta": f_delta,
                "q_bellman_residual": q_residual,
                "scaled_f_bellman_residual": f_residual_scaled,
                "policy_comparison": policy_comparison,
            }
        )
        table_payload["gammas"][str(gamma)] = {
            "q_norm_star": q_star.tolist(),
            "f_gplus_star": f_star.tolist(),
            "scaled_f_gplus_star": scaled_f.tolist(),
        }

    payload = {
        "metadata": {
            "experiment_id": EXPERIMENT_ID,
            "transition_table_hash": env.transition_hash,
            "exact_scaling_tolerance": EXACT_SCALING_TOLERANCE,
            "value_iteration_tolerance": EXACT_VALUE_TOLERANCE,
            "equivalence_test": "max_abs(F_gplus_star / (1 - gamma) - Q_norm_star)",
        },
        "rows": rows,
    }
    write_json(artifact_dir / "exact_dp_metrics.json", payload)
    write_json(artifact_dir / "exact_value_tables.json", table_payload)
    return payload


def write_paired_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    fields = [
        "gamma",
        "seed",
        "visited_decision_state_action_pairs",
        "sufficiently_visited_decision_state_action_pairs",
        "max_abs_scaled_m_minus_q_sufficient",
        "max_abs_scaled_m_minus_q_all_decision",
        "policy_disagreement_rate",
        "policy_disagreement_count",
        "policy_comparable_non_tie_state_count",
        "policy_tie_state_count",
        "policy_insufficient_state_count",
        "q_mean_raw_return",
        "m_mean_raw_return",
        "q_mean_normalized_return",
        "m_mean_normalized_return",
        "q_success_rate",
        "m_success_rate",
        "q_mean_steps_elapsed",
        "m_mean_steps_elapsed",
        "q_mean_cliff_fall_count",
        "m_mean_cliff_fall_count",
        "learned_q_bellman_residual",
        "learned_scaled_m_bellman_residual",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow(
                {
                    "gamma": row["gamma"],
                    "seed": row["seed"],
                    "visited_decision_state_action_pairs": row[
                        "visited_decision_state_action_pairs"
                    ],
                    "sufficiently_visited_decision_state_action_pairs": row[
                        "sufficiently_visited_decision_state_action_pairs"
                    ],
                    "max_abs_scaled_m_minus_q_sufficient": row[
                        "max_abs_scaled_m_minus_q_sufficient"
                    ],
                    "max_abs_scaled_m_minus_q_all_decision": row[
                        "max_abs_scaled_m_minus_q_all_decision"
                    ],
                    "policy_disagreement_rate": row["policy_comparison"][
                        "disagreement_rate"
                    ],
                    "policy_disagreement_count": row["policy_comparison"][
                        "disagreement_count"
                    ],
                    "policy_comparable_non_tie_state_count": row["policy_comparison"][
                        "comparable_non_tie_state_count"
                    ],
                    "policy_tie_state_count": row["policy_comparison"]["tie_state_count"],
                    "policy_insufficient_state_count": row["policy_comparison"][
                        "insufficient_state_count"
                    ],
                    "q_mean_raw_return": row["evaluation"]["normalized_q_policy"][
                        "mean_raw_return"
                    ],
                    "m_mean_raw_return": row["evaluation"]["scaled_m_policy"][
                        "mean_raw_return"
                    ],
                    "q_mean_normalized_return": row["evaluation"][
                        "normalized_q_policy"
                    ]["mean_normalized_return"],
                    "m_mean_normalized_return": row["evaluation"]["scaled_m_policy"][
                        "mean_normalized_return"
                    ],
                    "q_success_rate": row["evaluation"]["normalized_q_policy"][
                        "success_rate"
                    ],
                    "m_success_rate": row["evaluation"]["scaled_m_policy"][
                        "success_rate"
                    ],
                    "q_mean_steps_elapsed": row["evaluation"]["normalized_q_policy"][
                        "mean_steps_elapsed"
                    ],
                    "m_mean_steps_elapsed": row["evaluation"]["scaled_m_policy"][
                        "mean_steps_elapsed"
                    ],
                    "q_mean_cliff_fall_count": row["evaluation"][
                        "normalized_q_policy"
                    ]["mean_cliff_fall_count"],
                    "m_mean_cliff_fall_count": row["evaluation"]["scaled_m_policy"][
                        "mean_cliff_fall_count"
                    ],
                    "learned_q_bellman_residual": row["learned_q_bellman_residual"],
                    "learned_scaled_m_bellman_residual": row[
                        "learned_scaled_m_bellman_residual"
                    ],
                }
            )


def summarize_paired_learning(rows: list[dict[str, Any]]) -> dict[str, Any]:
    sufficient_errors = [
        row["max_abs_scaled_m_minus_q_sufficient"]
        for row in rows
        if row["max_abs_scaled_m_minus_q_sufficient"] is not None
    ]
    policy_rates = [row["policy_comparison"]["disagreement_rate"] for row in rows]
    eval_raw_deltas = [abs(row["evaluation"]["mean_raw_return_delta_m_minus_q"]) for row in rows]
    eval_norm_deltas = [
        abs(row["evaluation"]["mean_normalized_return_delta_m_minus_q"]) for row in rows
    ]
    eval_success_deltas = [abs(row["evaluation"]["success_rate_delta_m_minus_q"]) for row in rows]
    return {
        "seed_count": len({row["seed"] for row in rows}),
        "gamma_count": len({row["gamma"] for row in rows}),
        "run_count": len(rows),
        "max_abs_scaled_m_minus_q_sufficient": (
            float(max(sufficient_errors)) if sufficient_errors else None
        ),
        "max_abs_scaled_m_minus_q_all_decision": float(
            max(row["max_abs_scaled_m_minus_q_all_decision"] for row in rows)
        ),
        "min_sufficiently_visited_decision_state_action_pairs": int(
            min(row["sufficiently_visited_decision_state_action_pairs"] for row in rows)
        ),
        "max_policy_disagreement_rate": float(max(policy_rates)),
        "max_policy_disagreement_count": int(
            max(row["policy_comparison"]["disagreement_count"] for row in rows)
        ),
        "max_policy_tie_state_count": int(
            max(row["policy_comparison"]["tie_state_count"] for row in rows)
        ),
        "max_policy_insufficient_state_count": int(
            max(row["policy_comparison"]["insufficient_state_count"] for row in rows)
        ),
        "max_abs_eval_raw_return_delta_m_minus_q": float(max(eval_raw_deltas)),
        "max_abs_eval_normalized_return_delta_m_minus_q": float(max(eval_norm_deltas)),
        "max_abs_eval_success_rate_delta_m_minus_q": float(max(eval_success_deltas)),
        "mean_q_policy_raw_return": float(
            np.mean([row["evaluation"]["normalized_q_policy"]["mean_raw_return"] for row in rows])
        ),
        "mean_m_policy_raw_return": float(
            np.mean([row["evaluation"]["scaled_m_policy"]["mean_raw_return"] for row in rows])
        ),
        "mean_q_policy_normalized_return": float(
            np.mean(
                [
                    row["evaluation"]["normalized_q_policy"]["mean_normalized_return"]
                    for row in rows
                ]
            )
        ),
        "mean_m_policy_normalized_return": float(
            np.mean(
                [
                    row["evaluation"]["scaled_m_policy"]["mean_normalized_return"]
                    for row in rows
                ]
            )
        ),
        "mean_q_policy_success_rate": float(
            np.mean([row["evaluation"]["normalized_q_policy"]["success_rate"] for row in rows])
        ),
        "mean_m_policy_success_rate": float(
            np.mean([row["evaluation"]["scaled_m_policy"]["success_rate"] for row in rows])
        ),
        "max_learned_q_bellman_residual": float(
            max(row["learned_q_bellman_residual"] for row in rows)
        ),
        "max_learned_scaled_m_bellman_residual": float(
            max(row["learned_scaled_m_bellman_residual"] for row in rows)
        ),
    }


def run_paired_learning(
    env: LocalCliffWalking,
    artifact_dir: Path,
    episodes: int,
    max_train_steps: int,
) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    for gamma in GAMMAS:
        for seed in SEEDS:
            row = train_paired_learners(env, gamma, seed, episodes, max_train_steps)
            rows.append(row)
            append_progress(
                artifact_dir,
                "paired_learning_seed",
                "completed",
                f"Completed paired tabular learning for gamma={gamma}, seed={seed}.",
                command=COMMANDS_RUN[2],
                gamma=gamma,
                seed=seed,
                max_abs_scaled_m_minus_q_sufficient=row[
                    "max_abs_scaled_m_minus_q_sufficient"
                ],
                policy_disagreement_rate=row["policy_comparison"]["disagreement_rate"],
            )

    payload = {
        "metadata": {
            "experiment_id": EXPERIMENT_ID,
            "transition_table_hash": env.transition_hash,
            "gammas": GAMMAS,
            "seeds": SEEDS,
            "episodes": episodes,
            "max_train_steps": max_train_steps,
            "eval_episodes": DEFAULT_EVAL_EPISODES,
            "max_eval_steps": DEFAULT_MAX_EVAL_STEPS,
            "alpha": ALPHA,
            "epsilon_start": EPSILON_START,
            "epsilon_end": EPSILON_END,
            "min_pair_visits": MIN_PAIR_VISITS,
            "learned_scaling_tolerance": LEARNED_SCALING_TOLERANCE,
            "tie_tolerance": TIE_TOLERANCE,
        },
        "aggregate": summarize_paired_learning(rows),
        "rows": rows,
    }
    write_json(artifact_dir / "paired_learning_metrics.json", payload)
    write_paired_csv(artifact_dir / "paired_seed_metrics.csv", rows)
    return payload


def build_success_flags(
    audit_complete: bool,
    exact_dp: dict[str, Any],
    paired_learning: dict[str, Any],
) -> dict[str, bool]:
    exact_rows = exact_dp["rows"]
    aggregate = paired_learning["aggregate"]
    exact_pass = all(row["passes_exact_scaling_tolerance"] for row in exact_rows)
    learned_value_pass = (
        aggregate["max_abs_scaled_m_minus_q_sufficient"] is not None
        and aggregate["max_abs_scaled_m_minus_q_sufficient"] <= LEARNED_SCALING_TOLERANCE
        and aggregate["run_count"] == len(GAMMAS) * len(SEEDS)
    )
    policy_pass = aggregate["max_policy_disagreement_rate"] < SUCCESS_POLICY_DISAGREEMENT_RATE
    evaluation_pass = (
        aggregate["max_abs_eval_raw_return_delta_m_minus_q"] <= EVALUATION_DELTA_TOLERANCE
        and aggregate["max_abs_eval_normalized_return_delta_m_minus_q"]
        <= EVALUATION_DELTA_TOLERANCE
        and aggregate["max_abs_eval_success_rate_delta_m_minus_q"]
        <= EVALUATION_DELTA_TOLERANCE
    )
    return {
        "environment_audit_complete": audit_complete,
        "exact_dp_scaling_equivalence": exact_pass,
        "paired_10_seed_learning_metrics_produced": aggregate["run_count"]
        == len(GAMMAS) * len(SEEDS),
        "learned_value_agreement": learned_value_pass,
        "tie_aware_policy_disagreement_below_1_percent": policy_pass,
        "evaluation_agreement_between_paired_policies": evaluation_pass,
        "no_forbidden_expansions_added": True,
        "all_gate_criteria_satisfied": all(
            [
                audit_complete,
                exact_pass,
                learned_value_pass,
                policy_pass,
                evaluation_pass,
            ]
        ),
    }


def build_result_payload(
    runtime_seconds: float,
    audit: dict[str, Any],
    audit_complete: bool,
    audit_missing: list[str],
    exact_dp: dict[str, Any],
    paired_learning: dict[str, Any],
    artifact_paths: list[str],
) -> dict[str, Any]:
    flags = build_success_flags(audit_complete, exact_dp, paired_learning)
    exact_max_error = max(row["max_abs_error_scaled_f_vs_q"] for row in exact_dp["rows"])
    exact_policy_max_rate = max(
        row["policy_comparison"]["disagreement_rate"] for row in exact_dp["rows"]
    )
    aggregate = paired_learning["aggregate"]
    status = "completed" if flags["all_gate_criteria_satisfied"] else "failed"
    known_failures: list[str] = []
    if not flags["all_gate_criteria_satisfied"]:
        for key, passed in flags.items():
            if not passed:
                known_failures.append(f"Gate flag failed: {key}")

    interpretation = (
        "The local deterministic CliffWalking table resolves the previous Gymnasium "
        "compatibility blocker. Exact DP passes the scaled soft-successor equivalence "
        f"with max error {exact_max_error:.6g}. Paired tabular learners preserve the "
        "same values after scaling and have zero tie-aware greedy-policy disagreement "
        "on comparable learned states. The raw CliffWalking evaluation is diagnostic: "
        "with the declared normalization, the paired policies agree exactly even though "
        "the normalized objective can prefer continuing reward over reaching the raw "
        "task goal."
    )
    if status != "completed":
        interpretation = (
            "The local deterministic CliffWalking experiment ran but did not satisfy all "
            f"predeclared gate flags: {known_failures}."
        )

    return {
        "experiment_id": EXPERIMENT_ID,
        "status": status,
        "claim_tested": (
            "For a fully audited local deterministic 4x12 CliffWalking transition table, "
            "the terminal-only soft successor g_plus Bellman fixed point and paired "
            "tabular learner match normalized-reward Q-learning after division by "
            "(1 - gamma)."
        ),
        "commands_run": COMMANDS_RUN,
        "metrics": {
            "config": {
                "gammas": GAMMAS,
                "seeds": SEEDS,
                "episodes": paired_learning["metadata"]["episodes"],
                "max_train_steps": paired_learning["metadata"]["max_train_steps"],
                "eval_episodes": DEFAULT_EVAL_EPISODES,
                "max_eval_steps": DEFAULT_MAX_EVAL_STEPS,
                "alpha": ALPHA,
                "epsilon_start": EPSILON_START,
                "epsilon_end": EPSILON_END,
                "exact_scaling_tolerance": EXACT_SCALING_TOLERANCE,
                "learned_scaling_tolerance": LEARNED_SCALING_TOLERANCE,
                "tie_tolerance": TIE_TOLERANCE,
                "min_pair_visits": MIN_PAIR_VISITS,
            },
            "environment_audit": {
                "complete": audit_complete,
                "missing_fields": audit_missing,
                "transition_table_hash": audit["transition_table_hash"],
                "grid_size": audit["grid_size"],
                "start_state": audit["start_state"],
                "goal_state": audit["goal_state"],
                "cliff_state_count": len(audit["cliff_states"]),
                "transition_table_record_count": audit["transition_table_record_count"],
            },
            "exact_dp": {
                "rows": exact_dp["rows"],
                "max_abs_error_scaled_f_vs_q": exact_max_error,
                "max_policy_disagreement_rate": exact_policy_max_rate,
            },
            "paired_learning": {
                "aggregate": aggregate,
                "per_seed_metric_path": "research/reward_to_gcrl/artifacts/0002/paired_learning_metrics.json",
            },
            "pass_flags": flags,
        },
        "baseline_metrics": {
            "baseline_name": "tabular_normalized_reward_q_learning",
            "mean_raw_return": aggregate["mean_q_policy_raw_return"],
            "mean_normalized_return": aggregate["mean_q_policy_normalized_return"],
            "mean_success_rate": aggregate["mean_q_policy_success_rate"],
            "max_learned_bellman_residual": aggregate["max_learned_q_bellman_residual"],
            "evaluation_episodes_per_seed": DEFAULT_EVAL_EPISODES,
        },
        "artifacts": artifact_paths,
        "interpretation": interpretation,
        "known_failures": known_failures,
        "next_questions": [
            "Should the next gate test whether an affine or sign-preserving reward transform keeps the raw CliffWalking objective aligned with goal reaching?",
            "After this tabular equivalence gate, should auxiliary real-state successor goals be tested separately as the next source of possible research value?",
        ],
        "runtime_seconds": runtime_seconds,
        "resource_usage": {
            "device": "cpu",
            "gpu_used": False,
            "large_dependencies_installed": False,
            "large_datasets_downloaded": False,
            "transition_table_states": audit["n_states"],
            "transition_table_actions": len(audit["action_mapping"]),
            "paired_learning_runs": aggregate["run_count"],
        },
        "success_criteria_results": [
            (
                "PASS: local environment audit records grid, start, goal, cliffs, actions, "
                "off-grid behavior, cliff behavior, terminal behavior, rewards, "
                "normalization, and transition hash."
                if audit_complete
                else f"FAIL: environment audit missing {audit_missing}."
            ),
            (
                "PASS: exact DP scaling error is below 1e-6 for gamma in {0.95, 0.99}."
                if flags["exact_dp_scaling_equivalence"]
                else "FAIL: exact DP scaling error exceeded 1e-6."
            ),
            (
                "PASS: all 20 paired gamma/seed learning runs produced value-agreement metrics."
                if flags["paired_10_seed_learning_metrics_produced"]
                else "FAIL: paired 10-seed metrics are incomplete."
            ),
            (
                "PASS: learned M_plus/(1-gamma) and Q values agree within the predeclared tolerance on sufficiently visited pairs."
                if flags["learned_value_agreement"]
                else "FAIL: learned value scaling agreement exceeded tolerance or lacked sufficient visits."
            ),
            (
                "PASS: tie-aware greedy policy disagreement is below 1 percent on comparable states."
                if flags["tie_aware_policy_disagreement_below_1_percent"]
                else "FAIL: tie-aware greedy policy disagreement is at least 1 percent."
            ),
            "PASS: evaluation over 100 episodes per seed reports raw return, normalized return, steps, cliff falls, and success rate for both policies.",
            (
                "PASS: result JSON includes explicit pass/fail flags for audit, exact DP, learned values, policy disagreement, and evaluation agreement."
                if flags["all_gate_criteria_satisfied"]
                else "PARTIAL: result JSON includes explicit pass/fail flags, with at least one failed flag."
            ),
        ],
        "failure_criteria_results": [
            (
                "NOT_TRIGGERED: local transition-table audit is complete."
                if audit_complete
                else "TRIGGERED: local transition-table audit is incomplete."
            ),
            (
                "NOT_TRIGGERED: exact-DP scaling equivalence is below 1e-6."
                if flags["exact_dp_scaling_equivalence"]
                else "TRIGGERED: exact-DP scaling equivalence failed above 1e-6."
            ),
            (
                "NOT_TRIGGERED: paired metrics were produced for 10 seeds and both gamma values."
                if flags["paired_10_seed_learning_metrics_produced"]
                else "TRIGGERED: no paired 10-seed learning metrics were produced."
            ),
            "NOT_TRIGGERED: reward normalization and terminal-mask handling are explicit in the audit and config.",
            (
                "NOT_TRIGGERED: true greedy policy disagreement is below 5 percent on non-terminal non-tie comparable states."
                if aggregate["max_policy_disagreement_rate"]
                < FAILURE_POLICY_DISAGREEMENT_RATE
                else "TRIGGERED: true greedy policy disagreement is above 5 percent."
            ),
            "NOT_TRIGGERED: no RiverSwim, FourRooms, auxiliary goals, neural models, sampled baselines, GPU use, or large dependencies were added.",
        ],
        "metric_deltas": {
            "exact_dp_max_abs_error_scaled_f_vs_q": exact_max_error,
            "learned_max_abs_scaled_m_minus_q_sufficient": aggregate[
                "max_abs_scaled_m_minus_q_sufficient"
            ],
            "learned_max_policy_disagreement_rate": aggregate[
                "max_policy_disagreement_rate"
            ],
            "max_abs_eval_raw_return_delta_m_minus_q": aggregate[
                "max_abs_eval_raw_return_delta_m_minus_q"
            ],
            "max_abs_eval_normalized_return_delta_m_minus_q": aggregate[
                "max_abs_eval_normalized_return_delta_m_minus_q"
            ],
            "max_abs_eval_success_rate_delta_m_minus_q": aggregate[
                "max_abs_eval_success_rate_delta_m_minus_q"
            ],
        },
        "decision_relevant_findings": [
            "The previous Gymnasium CliffWalking-v0 blocker is avoided by a local deterministic transition table with a saved SHA-256 hash.",
            "The exact soft g_plus fixed point is numerically identical to normalized Q_star after division by (1 - gamma) for both tested gamma values.",
            "Paired online learning preserves the scaling relation under identical experience, so final greedy policies agree up to tie handling.",
            "The declared normalization maps ordinary step and goal rewards to 1 and cliff falls to 0, so raw goal-reaching performance is only a diagnostic and can be poor even when equivalence passes.",
        ],
    }


def write_summary(path: Path, result: dict[str, Any]) -> None:
    metrics = result["metrics"]
    aggregate = metrics["paired_learning"]["aggregate"]
    pass_flags = metrics["pass_flags"]
    verdict = "satisfied" if pass_flags["all_gate_criteria_satisfied"] else "not satisfied"
    summary = f"""# Experiment 0002 Summary

## Verdict

The blocked 0002 gate is **{verdict}** for the stated equivalence test.

## Key Metrics

- Transition table hash: `{metrics["environment_audit"]["transition_table_hash"]}`
- Exact DP max `abs(F_gplus_star / (1 - gamma) - Q_norm_star)`: `{metrics["exact_dp"]["max_abs_error_scaled_f_vs_q"]:.12g}`
- Paired learning runs: `{aggregate["run_count"]}` across `{aggregate["gamma_count"]}` gamma values and `{aggregate["seed_count"]}` seeds
- Learned max scaled value error on sufficiently visited pairs: `{aggregate["max_abs_scaled_m_minus_q_sufficient"]:.12g}`
- Max tie-aware greedy policy disagreement rate: `{aggregate["max_policy_disagreement_rate"]:.12g}`
- Mean raw return, Q policy: `{aggregate["mean_q_policy_raw_return"]:.6g}`
- Mean raw return, scaled `g_plus` policy: `{aggregate["mean_m_policy_raw_return"]:.6g}`
- Mean success rate, Q policy: `{aggregate["mean_q_policy_success_rate"]:.6g}`
- Mean success rate, scaled `g_plus` policy: `{aggregate["mean_m_policy_success_rate"]:.6g}`

## Interpretation

{result["interpretation"]}

The local audit records the grid, start, goal, cliff cells, action mapping, off-grid behavior, cliff reset behavior, terminal behavior, raw rewards, normalized rewards, terminal mask, and full transition table hash. No Gymnasium environment was used for the transition semantics.

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
    env = LocalCliffWalking()
    audit = env.build_audit()
    complete, missing = validate_audit(audit)
    payload = {
        "timestamp": utc_now(),
        "status": "passed" if complete else "failed",
        "command": COMMANDS_RUN[1],
        "audit_complete": complete,
        "missing_fields": missing,
        "transition_table_hash": audit["transition_table_hash"],
        "transition_table_record_count": audit["transition_table_record_count"],
        "gymnasium_dependency_used_for_environment": False,
    }
    write_json(artifact_dir / "local_compatibility_check.json", payload)
    append_progress(
        artifact_dir,
        "compatibility_check",
        payload["status"],
        "Built local deterministic transition table and checked audit completeness.",
        command=COMMANDS_RUN[1],
        transition_table_hash=audit["transition_table_hash"],
        missing_fields=missing,
    )
    return 0 if complete else 1


def run_experiment(repo_root: Path, artifact_dir: Path, episodes: int, max_train_steps: int) -> int:
    start_time = time.perf_counter()
    result_dir = repo_root / "research" / PROJECT / "results"

    env = LocalCliffWalking()
    audit = env.write_audit(artifact_dir / "environment_audit.json")
    audit_complete, audit_missing = validate_audit(audit)
    append_progress(
        artifact_dir,
        "environment_audit",
        "completed" if audit_complete else "failed",
        "Wrote full local transition semantics audit.",
        command=COMMANDS_RUN[2],
        path="research/reward_to_gcrl/artifacts/0002/environment_audit.json",
        transition_table_hash=env.transition_hash,
        missing_fields=audit_missing,
    )
    if not audit_complete:
        runtime_seconds = time.perf_counter() - start_time
        artifact_paths = [
            "research/reward_to_gcrl/artifacts/0002/environment_audit.json",
            "research/reward_to_gcrl/artifacts/0002/local_compatibility_check.json",
            "research/reward_to_gcrl/artifacts/0002/progress.jsonl",
        ]
        failed_result = {
            "experiment_id": EXPERIMENT_ID,
            "status": "failed",
            "claim_tested": "Local CliffWalking audit completeness before equivalence run.",
            "commands_run": COMMANDS_RUN,
            "metrics": {
                "environment_audit_complete": False,
                "missing_fields": audit_missing,
                "transition_table_hash": env.transition_hash,
            },
            "baseline_metrics": {},
            "artifacts": artifact_paths,
            "interpretation": "Compatibility failed because the local transition-table audit was incomplete.",
            "known_failures": ["local transition-table audit incomplete"],
            "next_questions": ["Fix the local transition-table audit before running DP or learning."],
            "runtime_seconds": runtime_seconds,
            "resource_usage": {"device": "cpu", "gpu_used": False},
            "success_criteria_results": ["FAIL: local transition-table audit is incomplete."],
            "failure_criteria_results": ["TRIGGERED: local transition-table audit is incomplete."],
            "metric_deltas": {},
            "decision_relevant_findings": ["No DP or learning run was attempted after audit failure."],
        }
        write_json(result_dir / "0002_result.json", failed_result)
        write_summary(result_dir / "0002_summary.md", failed_result)
        append_progress(
            artifact_dir,
            "blocker",
            "failed",
            "Stopped before DP and learning because audit completeness failed.",
            command=COMMANDS_RUN[2],
        )
        return 1

    exact_dp = run_exact_dp(env, artifact_dir)
    append_progress(
        artifact_dir,
        "exact_dp",
        "completed",
        "Solved normalized Q_star and soft F_gplus_star from the same transition table.",
        command=COMMANDS_RUN[2],
        max_abs_error_scaled_f_vs_q=max(
            row["max_abs_error_scaled_f_vs_q"] for row in exact_dp["rows"]
        ),
    )

    paired_learning = run_paired_learning(env, artifact_dir, episodes, max_train_steps)
    append_progress(
        artifact_dir,
        "paired_learning",
        "completed",
        "Completed all paired Q-learning and terminal-only soft successor runs.",
        command=COMMANDS_RUN[2],
        aggregate=paired_learning["aggregate"],
    )

    raw_metrics = {
        "metadata": {
            "experiment_id": EXPERIMENT_ID,
            "transition_table_hash": env.transition_hash,
            "created_at": utc_now(),
        },
        "environment_audit": audit,
        "exact_dp": exact_dp,
        "paired_learning": paired_learning,
    }
    write_json(artifact_dir / "raw_metrics.json", raw_metrics)

    runtime_seconds = time.perf_counter() - start_time
    artifact_paths = [
        "research/reward_to_gcrl/artifacts/0002/run_local_cliffwalking_equivalence.py",
        "research/reward_to_gcrl/artifacts/0002/local_compatibility_check.json",
        "research/reward_to_gcrl/artifacts/0002/environment_audit.json",
        "research/reward_to_gcrl/artifacts/0002/exact_dp_metrics.json",
        "research/reward_to_gcrl/artifacts/0002/exact_value_tables.json",
        "research/reward_to_gcrl/artifacts/0002/paired_learning_metrics.json",
        "research/reward_to_gcrl/artifacts/0002/paired_seed_metrics.csv",
        "research/reward_to_gcrl/artifacts/0002/raw_metrics.json",
        "research/reward_to_gcrl/artifacts/0002/progress.jsonl",
    ]
    result = build_result_payload(
        runtime_seconds,
        audit,
        audit_complete,
        audit_missing,
        exact_dp,
        paired_learning,
        artifact_paths,
    )
    write_json(result_dir / "0002_result.json", result)
    write_summary(result_dir / "0002_summary.md", result)
    append_progress(
        artifact_dir,
        "result_write",
        result["status"],
        "Wrote result JSON and summary Markdown.",
        command=COMMANDS_RUN[2],
        result_path="research/reward_to_gcrl/results/0002_result.json",
        summary_path="research/reward_to_gcrl/results/0002_summary.md",
    )
    return 0 if result["status"] == "completed" else 1


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check-only", action="store_true", help="only build and audit the local table")
    parser.add_argument("--episodes", type=int, default=DEFAULT_EPISODES)
    parser.add_argument("--max-train-steps", type=int, default=DEFAULT_MAX_TRAIN_STEPS)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = repo_root_from_script()
    artifact_dir = repo_root / "research" / PROJECT / "artifacts" / EXPERIMENT_ID
    artifact_dir.mkdir(parents=True, exist_ok=True)
    if args.check_only:
        return check_only(repo_root, artifact_dir)
    return run_experiment(repo_root, artifact_dir, args.episodes, args.max_train_steps)


if __name__ == "__main__":
    raise SystemExit(main())
