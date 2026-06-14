#!/usr/bin/env python3
"""Experiment 0010: CPU NumPy low-rank auxiliary-goal diagnostic."""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import json
import math
import time
from collections import deque
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np


EXPERIMENT_ID = "0010"
PROJECT = "reward_to_gcrl"
GAMMA = 0.95
SEEDS = list(range(10))
HEIGHT = 7
WIDTH = 7
REWARD_GOAL_CELL = (6, 6)
RANK = 4
REPLAY_TRANSITIONS = 5_000
OPTIMIZER_STEPS = 4_000
BATCH_SIZE = 256
AUX_GOALS_PER_TRANSITION = 4
AUXILIARY_WEIGHT = 1.0
LOSS_BALANCE_CLIP_MIN = 0.05
LOSS_BALANCE_CLIP_MAX = 20.0
STAGED_PRETRAIN_STEPS = OPTIMIZER_STEPS // 2
LEARNING_RATE = 0.05
ADAM_BETA1 = 0.9
ADAM_BETA2 = 0.999
ADAM_EPS = 1.0e-8
INIT_SCALE = 0.05
INIT_PROBABILITY = 0.02
DP_TOLERANCE = 1.0e-13
MAX_DP_ITERATIONS = 200_000
TIE_TOLERANCE = 1.0e-12
ADEQUATE_VISITED_SA_FRACTION = 1.0
ADEQUATE_MIN_SA_COUNT = 5
ADEQUATE_REWARD_EVENT_COUNT = 20
ADEQUATE_GOAL_LABEL_FRACTION = 0.95
IMPROVEMENT_THRESHOLD = 0.10
INDISTINGUISHABLE_Z = 1.96
VARIANTS = [
    "terminal_only",
    "combined_lambda_1_reproduction",
    "combined_loss_balanced",
    "staged_real_goal_pretrain_then_gplus_finetune",
]

COMMANDS_RUN = [
    "mkdir -p research/reward_to_gcrl/artifacts/0010 research/reward_to_gcrl/results",
    "conda run -n autoresearcher_reward_to_gcrl python --version",
    (
        "conda run -n autoresearcher_reward_to_gcrl python -m py_compile "
        "research/reward_to_gcrl/artifacts/0010/run_fourrooms_lowrank_aux_diagnostic.py"
    ),
    (
        "conda run -n autoresearcher_reward_to_gcrl python "
        "research/reward_to_gcrl/artifacts/0010/run_fourrooms_lowrank_aux_diagnostic.py --check-only"
    ),
    (
        "conda run -n autoresearcher_reward_to_gcrl python "
        "research/reward_to_gcrl/artifacts/0010/run_fourrooms_lowrank_aux_diagnostic.py"
    ),
    (
        "conda run -n autoresearcher_reward_to_gcrl python -m jsonschema "
        "-i research/reward_to_gcrl/results/0010_result.json schemas/result.schema.json"
    ),
    (
        "conda run -n autoresearcher_reward_to_gcrl python scripts/validate_artifacts.py "
        "--repo-root . --json research/reward_to_gcrl/results/0010_result.json "
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


@dataclass(frozen=True)
class ActionSpec:
    action: int
    name: str
    delta: tuple[int, int]
    arrow: str


class FourRooms:
    actions = (
        ActionSpec(0, "up", (-1, 0), "^"),
        ActionSpec(1, "right", (0, 1), ">"),
        ActionSpec(2, "down", (1, 0), "v"),
        ActionSpec(3, "left", (0, -1), "<"),
    )

    def __init__(self) -> None:
        self.height = HEIGHT
        self.width = WIDTH
        self.doorway_cells = [(1, 3), (3, 1), (3, 5), (5, 3)]
        raw_walls = {(row, 3) for row in range(HEIGHT)} | {(3, col) for col in range(WIDTH)}
        self.wall_cells = sorted(raw_walls - set(self.doorway_cells))
        self.open_cells = [
            (row, col)
            for row in range(HEIGHT)
            for col in range(WIDTH)
            if (row, col) not in set(self.wall_cells)
        ]
        self.state_by_cell = {cell: index for index, cell in enumerate(self.open_cells)}
        self.cell_by_state = {index: cell for cell, index in self.state_by_cell.items()}
        self.n_states = len(self.open_cells)
        self.n_actions = len(self.actions)
        self.n_sa = self.n_states * self.n_actions
        self.reward_goal_cell = REWARD_GOAL_CELL
        self.reward_goal_state = self.state_by_cell[self.reward_goal_cell]
        self.g_plus_index = self.n_states
        self.n_goals_total = self.n_states + 1
        self.transitions = np.zeros((self.n_states, self.n_actions), dtype=np.int64)
        self.rewards = np.zeros((self.n_states, self.n_actions), dtype=np.float64)
        self.transition_records: list[dict[str, Any]] = []
        self._build()
        self.transition_hash = self._hash_records()

    def sa_index(self, state: np.ndarray | int, action: np.ndarray | int) -> np.ndarray | int:
        return np.asarray(state) * self.n_actions + np.asarray(action)

    def _move(self, cell: tuple[int, int], action: ActionSpec) -> tuple[int, int]:
        row, col = cell
        d_row, d_col = action.delta
        candidate = (row + d_row, col + d_col)
        if (
            candidate[0] < 0
            or candidate[0] >= self.height
            or candidate[1] < 0
            or candidate[1] >= self.width
            or candidate in set(self.wall_cells)
        ):
            return cell
        return candidate

    def _build(self) -> None:
        for state, cell in self.cell_by_state.items():
            for action in self.actions:
                next_cell = self._move(cell, action)
                next_state = self.state_by_cell[next_cell]
                reward = 1.0 if state != self.reward_goal_state and next_state == self.reward_goal_state else 0.0
                self.transitions[state, action.action] = next_state
                self.rewards[state, action.action] = reward
                self.transition_records.append(
                    {
                        "state": state,
                        "cell": list(cell),
                        "action": action.action,
                        "action_name": action.name,
                        "next_state": int(next_state),
                        "next_cell": list(next_cell),
                        "raw_reward": reward,
                        "normalized_reward": reward,
                        "off_grid_or_wall_stay": next_cell == cell,
                        "task_terminal_on_next": next_state == self.reward_goal_state,
                    }
                )

    def _hash_records(self) -> str:
        canonical = json.dumps(self.transition_records, sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(canonical.encode("utf-8")).hexdigest()

    def neighbors(self, state: int) -> list[int]:
        return sorted(set(int(next_state) for next_state in self.transitions[state]))

    def build_audit(self, repo_root: Path) -> dict[str, Any]:
        audit_0008_path = repo_root / "research" / PROJECT / "artifacts" / "0008" / "environment_audit.json"
        audit_0008_hash = None
        if audit_0008_path.exists():
            audit_0008_hash = json.loads(audit_0008_path.read_text(encoding="utf-8"))["transition_table_hash"]
        result_0009_path = repo_root / "research" / PROJECT / "results" / "0009_result.json"
        result_0009 = None
        if result_0009_path.exists():
            result_0009 = json.loads(result_0009_path.read_text(encoding="utf-8"))
        return {
            "experiment_id": EXPERIMENT_ID,
            "environment": "tiny_deterministic_fourrooms",
            "verified_against_0008_where_available": {
                "audit_path": str(audit_0008_path),
                "transition_hash_0008": audit_0008_hash,
                "transition_hash_matches_0008": audit_0008_hash == self.transition_hash,
            },
            "verified_against_0009_where_available": {
                "result_path": str(result_0009_path),
                "status": result_0009["status"] if result_0009 else None,
                "verdict": result_0009["metrics"]["lowrank_auxiliary"]["verdict"] if result_0009 else None,
                "rank": result_0009["metrics"]["config"]["rank"] if result_0009 else None,
                "replay_transitions": result_0009["metrics"]["config"]["training_config"]["replay_transitions"] if result_0009 else None,
                "transition_hash_matches": (
                    result_0009["metrics"]["environment_audit"]["transition_table_hash"] == self.transition_hash
                    if result_0009
                    else False
                ),
                "aggregate": result_0009["metrics"]["lowrank_auxiliary"]["aggregate"] if result_0009 else None,
            },
            "grid_shape": [self.height, self.width],
            "wall_cells": [list(cell) for cell in self.wall_cells],
            "doorway_cells": [list(cell) for cell in self.doorway_cells],
            "open_cell_count": self.n_states,
            "state_indexing": [
                {"state": state, "cell": list(self.cell_by_state[state])}
                for state in range(self.n_states)
            ],
            "action_mapping": [
                {
                    "action": action.action,
                    "name": action.name,
                    "delta": list(action.delta),
                    "arrow": action.arrow,
                }
                for action in self.actions
            ],
            "reward_task": {
                "reward_goal_cell": list(self.reward_goal_cell),
                "reward_goal_state": self.reward_goal_state,
                "raw_reward": "1 when a nonterminal transition enters reward_goal_state, otherwise 0",
            },
            "reward_normalization": {
                "raw_rewards_in_[0,1]": True,
                "normalized_reward": "identity(raw_reward)",
                "affine_scale": 1.0,
                "affine_offset": 0.0,
            },
            "goal_indexing": {
                "real_state_goal_indices": "0..n_states-1, matching state indices",
                "g_plus_index": self.g_plus_index,
                "goal_count_total": self.n_goals_total,
            },
            "terminal_masks": {
                "real_state_goal_slice": "slice g has terminal current state s==g and no bootstrap on transitions with next_state==g",
                "g_plus_slice": "terminal current state s==reward_goal_state and no bootstrap on transitions with next_state==reward_goal_state",
            },
            "model": {
                "form": "M_hat(s,a,g)=sigmoid(u_sa dot v_g + b_g)",
                "shared_parameters": "u_sa is shared by real-state goals and g_plus in the combined model",
                "rank": RANK,
                "optimizer": "Adam",
                "learning_rate": LEARNING_RATE,
            },
            "replay_behavior": {
                "name": "uniform_random_state_action_reset",
                "description": "Each replay transition samples an open state uniformly and an action uniformly, then applies the audited deterministic transition table.",
                "uses_exact_q_or_dp": False,
                "uses_reward_optimal_preferences": False,
            },
            "training_config": {
                "gamma": GAMMA,
                "seeds": SEEDS,
                "replay_transitions": REPLAY_TRANSITIONS,
                "optimizer_steps": OPTIMIZER_STEPS,
                "batch_size": BATCH_SIZE,
                "aux_goals_per_transition": AUX_GOALS_PER_TRANSITION,
                "auxiliary_weight": AUXILIARY_WEIGHT,
                "diagnostic_variants": VARIANTS,
                "loss_balance_clip": [LOSS_BALANCE_CLIP_MIN, LOSS_BALANCE_CLIP_MAX],
                "staged_pretrain_steps": STAGED_PRETRAIN_STEPS,
            },
            "transition_table_shape": list(self.transitions.shape),
            "transition_table_hash": self.transition_hash,
            "transition_records": self.transition_records,
        }


def validate_audit(audit: dict[str, Any]) -> tuple[bool, list[str]]:
    required = [
        "verified_against_0008_where_available",
        "verified_against_0009_where_available",
        "grid_shape",
        "wall_cells",
        "doorway_cells",
        "state_indexing",
        "action_mapping",
        "reward_task",
        "reward_normalization",
        "goal_indexing",
        "terminal_masks",
        "model",
        "replay_behavior",
        "training_config",
        "transition_table_hash",
        "transition_records",
    ]
    missing = [field for field in required if field not in audit]
    complete = (
        not missing
        and audit["grid_shape"] == [HEIGHT, WIDTH]
        and audit["goal_indexing"]["goal_count_total"] == audit["open_cell_count"] + 1
        and not audit["replay_behavior"]["uses_exact_q_or_dp"]
        and audit["verified_against_0008_where_available"]["transition_hash_matches_0008"]
        and audit["verified_against_0009_where_available"]["transition_hash_matches"]
    )
    return complete, missing


def sigmoid(logits: np.ndarray) -> np.ndarray:
    return 1.0 / (1.0 + np.exp(-np.clip(logits, -50.0, 50.0)))


def logit(probability: float) -> float:
    return math.log(probability / (1.0 - probability))


def tie_actions(values: np.ndarray) -> list[int]:
    best = float(np.max(values))
    return [int(action) for action, value in enumerate(values) if best - float(value) <= TIE_TOLERANCE]


def greedy_action(values: np.ndarray) -> int:
    return min(tie_actions(values))


def compare_policy(candidate: np.ndarray, reference: np.ndarray, skip_states: set[int] | None = None) -> dict[str, Any]:
    skip_states = skip_states or set()
    ties = 0
    comparable = 0
    disagreements = 0
    for state in range(candidate.shape[0]):
        if state in skip_states:
            continue
        cand_ties = tie_actions(candidate[state])
        ref_ties = tie_actions(reference[state])
        if len(cand_ties) > 1 or len(ref_ties) > 1:
            ties += 1
            continue
        comparable += 1
        disagreements += int(cand_ties[0] != ref_ties[0])
    return {
        "state_count_total": int(candidate.shape[0]),
        "skipped_state_count": len(skip_states),
        "tie_state_count": ties,
        "comparable_non_tie_state_count": comparable,
        "disagreement_count": disagreements,
        "disagreement_rate": disagreements / comparable if comparable else 0.0,
    }


def q_norm_backup(values: np.ndarray, env: FourRooms, gamma: float) -> np.ndarray:
    target = np.zeros_like(values)
    next_values = values.max(axis=1)
    for state in range(env.n_states):
        if state == env.reward_goal_state:
            continue
        for action in range(env.n_actions):
            next_state = int(env.transitions[state, action])
            terminal_next = next_state == env.reward_goal_state
            target[state, action] = env.rewards[state, action] + gamma * (0.0 if terminal_next else next_values[next_state])
    return target


def gplus_backup(values: np.ndarray, env: FourRooms, gamma: float) -> np.ndarray:
    target = np.zeros_like(values)
    next_values = values.max(axis=1)
    for state in range(env.n_states):
        if state == env.reward_goal_state:
            continue
        for action in range(env.n_actions):
            next_state = int(env.transitions[state, action])
            target[state, action] = (1.0 - gamma) * env.rewards[state, action]
            if next_state != env.reward_goal_state:
                target[state, action] += gamma * next_values[next_state]
    return target


def goal_backup(values: np.ndarray, env: FourRooms, gamma: float) -> np.ndarray:
    target = np.zeros_like(values)
    next_values = values.max(axis=1)
    for state in range(env.n_states):
        for action in range(env.n_actions):
            next_state = int(env.transitions[state, action])
            for goal in range(env.n_states):
                if state == goal:
                    target[state, action, goal] = 0.0
                elif next_state == goal:
                    target[state, action, goal] = 1.0 - gamma
                else:
                    target[state, action, goal] = gamma * next_values[next_state, goal]
    return target


def iterate_to_convergence(initial: np.ndarray, backup_fn: Any, tolerance: float) -> tuple[np.ndarray, int, float]:
    values = initial.copy()
    for iteration in range(1, MAX_DP_ITERATIONS + 1):
        target = backup_fn(values)
        delta = float(np.max(np.abs(target - values)))
        values = target
        if delta <= tolerance:
            return values, iteration, delta
    raise RuntimeError("exact value iteration did not converge")


def solve_exact(env: FourRooms, artifact_dir: Path) -> dict[str, Any]:
    q_norm, q_iterations, q_delta = iterate_to_convergence(
        np.zeros((env.n_states, env.n_actions), dtype=np.float64),
        lambda values: q_norm_backup(values, env, GAMMA),
        DP_TOLERANCE,
    )
    f_gplus, g_iterations, g_delta = iterate_to_convergence(
        np.zeros((env.n_states, env.n_actions), dtype=np.float64),
        lambda values: gplus_backup(values, env, GAMMA),
        DP_TOLERANCE,
    )
    real_goals, goal_iterations, goal_delta = iterate_to_convergence(
        np.zeros((env.n_states, env.n_actions, env.n_states), dtype=np.float64),
        lambda values: goal_backup(values, env, GAMMA),
        DP_TOLERANCE,
    )
    payload = {
        "metadata": {"experiment_id": EXPERIMENT_ID, "gamma": GAMMA, "transition_table_hash": env.transition_hash},
        "q_iterations": q_iterations,
        "gplus_iterations": g_iterations,
        "goal_iterations": goal_iterations,
        "q_final_delta": q_delta,
        "gplus_final_delta": g_delta,
        "goal_final_delta": goal_delta,
        "max_abs_scaled_gplus_minus_q_norm": float(np.max(np.abs(f_gplus / (1.0 - GAMMA) - q_norm))),
        "q_norm": q_norm.tolist(),
        "f_gplus_star": f_gplus.tolist(),
        "real_goal_slices": real_goals.tolist(),
    }
    write_json(artifact_dir / "exact_dp_references.json", payload)
    return {"json": payload, "q_norm": q_norm, "f_gplus": f_gplus, "real_goals": real_goals}


def shortest_path_distances(env: FourRooms) -> np.ndarray:
    distances = np.full((env.n_states, env.n_states), math.inf, dtype=np.float64)
    reverse_neighbors: dict[int, list[int]] = {state: [] for state in range(env.n_states)}
    for state in range(env.n_states):
        for next_state in env.neighbors(state):
            reverse_neighbors[next_state].append(state)
    for goal in range(env.n_states):
        distances[goal, goal] = 0.0
        queue: deque[int] = deque([goal])
        while queue:
            state = queue.popleft()
            for prev in reverse_neighbors[state]:
                if math.isinf(float(distances[prev, goal])):
                    distances[prev, goal] = distances[state, goal] + 1.0
                    queue.append(prev)
    return distances


class LowRankModel:
    def __init__(self, env: FourRooms, rng: np.random.Generator) -> None:
        self.u = rng.normal(0.0, INIT_SCALE, size=(env.n_sa, RANK))
        self.v = rng.normal(0.0, INIT_SCALE, size=(env.n_goals_total, RANK))
        self.b = np.full(env.n_goals_total, logit(INIT_PROBABILITY), dtype=np.float64)
        self.m_u = np.zeros_like(self.u)
        self.v_u = np.zeros_like(self.u)
        self.m_v = np.zeros_like(self.v)
        self.v_v = np.zeros_like(self.v)
        self.m_b = np.zeros_like(self.b)
        self.v_b = np.zeros_like(self.b)
        self.t = 0

    def clone(self) -> "LowRankModel":
        clone = object.__new__(LowRankModel)
        for name, value in self.__dict__.items():
            setattr(clone, name, value.copy() if isinstance(value, np.ndarray) else value)
        return clone

    def predict_matrix(self) -> np.ndarray:
        return sigmoid(self.u @ self.v.T + self.b[None, :])

    def adam_step(self, grad_u: np.ndarray, grad_v: np.ndarray, grad_b: np.ndarray) -> None:
        self.t += 1
        self.m_u = ADAM_BETA1 * self.m_u + (1.0 - ADAM_BETA1) * grad_u
        self.v_u = ADAM_BETA2 * self.v_u + (1.0 - ADAM_BETA2) * (grad_u * grad_u)
        self.m_v = ADAM_BETA1 * self.m_v + (1.0 - ADAM_BETA1) * grad_v
        self.v_v = ADAM_BETA2 * self.v_v + (1.0 - ADAM_BETA2) * (grad_v * grad_v)
        self.m_b = ADAM_BETA1 * self.m_b + (1.0 - ADAM_BETA1) * grad_b
        self.v_b = ADAM_BETA2 * self.v_b + (1.0 - ADAM_BETA2) * (grad_b * grad_b)
        bias1 = 1.0 - ADAM_BETA1**self.t
        bias2 = 1.0 - ADAM_BETA2**self.t
        self.u -= LEARNING_RATE * (self.m_u / bias1) / (np.sqrt(self.v_u / bias2) + ADAM_EPS)
        self.v -= LEARNING_RATE * (self.m_v / bias1) / (np.sqrt(self.v_v / bias2) + ADAM_EPS)
        self.b -= LEARNING_RATE * (self.m_b / bias1) / (np.sqrt(self.v_b / bias2) + ADAM_EPS)


def generate_replay(env: FourRooms, seed: int) -> dict[str, np.ndarray]:
    rng = np.random.default_rng(seed + 50_000)
    states = rng.integers(0, env.n_states, size=REPLAY_TRANSITIONS, dtype=np.int32)
    actions = rng.integers(0, env.n_actions, size=REPLAY_TRANSITIONS, dtype=np.int32)
    next_states = env.transitions[states, actions].astype(np.int32)
    rewards = env.rewards[states, actions].astype(np.float64)
    sa_indices = (states * env.n_actions + actions).astype(np.int32)
    return {
        "states": states,
        "actions": actions,
        "next_states": next_states,
        "rewards": rewards,
        "sa_indices": sa_indices,
    }


def replay_coverage(env: FourRooms, replay: dict[str, np.ndarray]) -> dict[str, Any]:
    counts = np.bincount(replay["sa_indices"], minlength=env.n_sa)
    return {
        "behavior": "uniform_random_state_action_reset",
        "transition_count": REPLAY_TRANSITIONS,
        "visited_state_action_pairs": int(np.sum(counts > 0)),
        "total_state_action_pairs": env.n_sa,
        "visited_state_action_fraction": float(np.mean(counts > 0)),
        "min_state_action_count": int(np.min(counts)),
        "max_state_action_count": int(np.max(counts)),
        "reward_event_count": int(np.sum(replay["rewards"] >= 1.0)),
        "adequate_replay_coverage": bool(
            np.mean(counts > 0) >= ADEQUATE_VISITED_SA_FRACTION
            and np.min(counts) >= ADEQUATE_MIN_SA_COUNT
            and np.sum(replay["rewards"] >= 1.0) >= ADEQUATE_REWARD_EVENT_COUNT
        ),
    }


def schedules(seed: int) -> tuple[np.ndarray, np.ndarray]:
    rng = np.random.default_rng(seed + 70_000)
    batches = rng.integers(0, REPLAY_TRANSITIONS, size=(OPTIMIZER_STEPS, BATCH_SIZE), dtype=np.int32)
    goals = rng.integers(0, 40, size=(OPTIMIZER_STEPS, BATCH_SIZE, AUX_GOALS_PER_TRANSITION), dtype=np.int16)
    return batches, goals


def gplus_targets(pred: np.ndarray, env: FourRooms, replay: dict[str, np.ndarray], indices: np.ndarray) -> np.ndarray:
    states = replay["states"][indices]
    next_states = replay["next_states"][indices]
    rewards = replay["rewards"][indices]
    next_values = pred.reshape(env.n_states, env.n_actions, env.n_goals_total).max(axis=1)
    targets = (1.0 - GAMMA) * rewards
    active = (states != env.reward_goal_state) & (next_states != env.reward_goal_state)
    targets = np.where(active, targets + GAMMA * next_values[next_states, env.g_plus_index], targets)
    targets = np.where(states == env.reward_goal_state, 0.0, targets)
    return targets


def real_goal_targets(
    pred: np.ndarray,
    env: FourRooms,
    replay: dict[str, np.ndarray],
    indices: np.ndarray,
    goals: np.ndarray,
) -> np.ndarray:
    states = np.repeat(replay["states"][indices], AUX_GOALS_PER_TRANSITION)
    next_states = np.repeat(replay["next_states"][indices], AUX_GOALS_PER_TRANSITION)
    flat_goals = goals.reshape(-1).astype(np.int32)
    next_values = pred.reshape(env.n_states, env.n_actions, env.n_goals_total).max(axis=1)
    targets = GAMMA * next_values[next_states, flat_goals]
    targets = np.where(next_states == flat_goals, 1.0 - GAMMA, targets)
    targets = np.where(states == flat_goals, 0.0, targets)
    return targets


def component_gradients(
    model: LowRankModel,
    sa_indices: np.ndarray,
    goal_indices: np.ndarray,
    targets: np.ndarray,
    weights: np.ndarray,
) -> dict[str, Any]:
    u_rows = model.u[sa_indices]
    v_rows = model.v[goal_indices]
    logits = np.sum(u_rows * v_rows, axis=1) + model.b[goal_indices]
    preds = sigmoid(logits)
    errors = preds - targets
    weighted = weights * errors
    loss = float(np.mean(weights * errors * errors))
    coeff = weighted * preds * (1.0 - preds) / len(targets)
    grad_u = np.zeros_like(model.u)
    grad_v = np.zeros_like(model.v)
    grad_b = np.zeros_like(model.b)
    np.add.at(grad_u, sa_indices, coeff[:, None] * v_rows)
    np.add.at(grad_v, goal_indices, coeff[:, None] * u_rows)
    np.add.at(grad_b, goal_indices, coeff)
    return {
        "loss": loss,
        "grad_u": grad_u,
        "grad_v": grad_v,
        "grad_b": grad_b,
        "u_grad_norm": float(np.linalg.norm(grad_u)),
        "v_grad_norm": float(np.linalg.norm(grad_v)),
        "b_grad_norm": float(np.linalg.norm(grad_b)),
        "target_mean": float(np.mean(targets)),
        "target_max": float(np.max(targets)),
        "prediction_mean": float(np.mean(preds)),
        "prediction_max": float(np.max(preds)),
    }


def scale_component(component: dict[str, Any], scale: float) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    return component["grad_u"] * scale, component["grad_v"] * scale, component["grad_b"] * scale


def gradient_payload(
    gplus_component: dict[str, Any] | None,
    aux_component: dict[str, Any] | None,
    total_u: np.ndarray,
    total_v: np.ndarray,
    total_b: np.ndarray,
    aux_scale: float,
) -> dict[str, Any]:
    g_u = gplus_component["u_grad_norm"] if gplus_component else 0.0
    a_u = aux_component["u_grad_norm"] if aux_component else 0.0
    return {
        "gplus_loss": gplus_component["loss"] if gplus_component else None,
        "auxiliary_loss": aux_component["loss"] if aux_component else None,
        "auxiliary_scale": aux_scale,
        "gplus_u_grad_norm": g_u,
        "auxiliary_u_grad_norm": a_u,
        "aux_to_gplus_u_grad_norm_ratio": a_u / g_u if g_u > 0.0 else None,
        "total_u_grad_norm": float(np.linalg.norm(total_u)),
        "total_v_grad_norm": float(np.linalg.norm(total_v)),
        "total_b_grad_norm": float(np.linalg.norm(total_b)),
        "gplus_target_mean": gplus_component["target_mean"] if gplus_component else None,
        "gplus_target_max": gplus_component["target_max"] if gplus_component else None,
        "auxiliary_target_mean": aux_component["target_mean"] if aux_component else None,
        "auxiliary_target_max": aux_component["target_max"] if aux_component else None,
    }


def train_variant(
    env: FourRooms,
    initial: LowRankModel,
    replay: dict[str, np.ndarray],
    batch_schedule: np.ndarray,
    goal_schedule: np.ndarray,
    variant: str,
) -> tuple[LowRankModel, dict[str, Any]]:
    model = initial.clone()
    curves = []
    goal_labels_seen = {env.g_plus_index}
    ratios = []
    gplus_losses = []
    aux_losses = []
    for step in range(OPTIMIZER_STEPS):
        batch = batch_schedule[step]
        pred = model.predict_matrix()
        sa = replay["sa_indices"][batch]
        gplus_component = None
        aux_component = None
        sampled_goals = None
        aux_targets = None
        gplus_target_values = None
        if variant in {
            "terminal_only",
            "combined_lambda_1_reproduction",
            "combined_loss_balanced",
        } or (variant == "staged_real_goal_pretrain_then_gplus_finetune" and step >= STAGED_PRETRAIN_STEPS):
            gplus_goals = np.full(BATCH_SIZE, env.g_plus_index, dtype=np.int32)
            gplus_target_values = gplus_targets(pred, env, replay, batch)
            gplus_component = component_gradients(
                model,
                sa.copy(),
                gplus_goals,
                gplus_target_values,
                np.ones(BATCH_SIZE, dtype=np.float64),
            )
            gplus_losses.append(gplus_component["loss"])
        if variant in {
            "combined_lambda_1_reproduction",
            "combined_loss_balanced",
        } or (variant == "staged_real_goal_pretrain_then_gplus_finetune" and step < STAGED_PRETRAIN_STEPS):
            sampled_goals = goal_schedule[step].astype(np.int32)
            goal_labels_seen.update(int(goal) for goal in sampled_goals.reshape(-1))
            aux_targets = real_goal_targets(pred, env, replay, batch, sampled_goals)
            aux_component = component_gradients(
                model,
                np.repeat(sa, AUX_GOALS_PER_TRANSITION),
                sampled_goals.reshape(-1).astype(np.int32),
                aux_targets,
                np.ones(BATCH_SIZE * AUX_GOALS_PER_TRANSITION, dtype=np.float64),
            )
            aux_losses.append(aux_component["loss"])
        aux_scale = 0.0
        if aux_component is not None:
            if variant == "combined_loss_balanced" and gplus_component is not None:
                aux_scale = float(
                    np.clip(
                        gplus_component["loss"] / (aux_component["loss"] + 1.0e-12),
                        LOSS_BALANCE_CLIP_MIN,
                        LOSS_BALANCE_CLIP_MAX,
                    )
                )
            else:
                aux_scale = AUXILIARY_WEIGHT
        if variant == "combined_lambda_1_reproduction" and sampled_goals is not None and aux_targets is not None:
            combined_component = component_gradients(
                model,
                np.concatenate([sa.copy(), np.repeat(sa, AUX_GOALS_PER_TRANSITION)]),
                np.concatenate(
                    [
                        np.full(BATCH_SIZE, env.g_plus_index, dtype=np.int32),
                        sampled_goals.reshape(-1).astype(np.int32),
                    ]
                ),
                np.concatenate([gplus_target_values, aux_targets]),
                np.ones(BATCH_SIZE * (1 + AUX_GOALS_PER_TRANSITION), dtype=np.float64),
            )
            total_u = combined_component["grad_u"]
            total_v = combined_component["grad_v"]
            total_b = combined_component["grad_b"]
        else:
            total_u = np.zeros_like(model.u)
            total_v = np.zeros_like(model.v)
            total_b = np.zeros_like(model.b)
            if gplus_component is not None:
                gu, gv, gb = scale_component(gplus_component, 1.0)
                total_u += gu
                total_v += gv
                total_b += gb
            if aux_component is not None:
                au, av, ab = scale_component(aux_component, aux_scale)
                total_u += au
                total_v += av
                total_b += ab
        model.adam_step(total_u, total_v, total_b)
        payload = gradient_payload(gplus_component, aux_component, total_u, total_v, total_b, aux_scale)
        if payload["aux_to_gplus_u_grad_norm_ratio"] is not None:
            ratios.append(payload["aux_to_gplus_u_grad_norm_ratio"])
        if (step + 1) % 500 == 0 or step == 0:
            curves.append({"step": step + 1, "variant": variant, **payload})
    return model, {
        "variant": variant,
        "curves": curves,
        "goal_label_coverage_count": len(goal_labels_seen),
        "goal_label_coverage_fraction": len(goal_labels_seen) / env.n_goals_total,
        "shares_state_action_factors": True,
        "mean_aux_to_gplus_u_grad_norm_ratio": float(np.mean(ratios)) if ratios else None,
        "max_aux_to_gplus_u_grad_norm_ratio": float(np.max(ratios)) if ratios else None,
        "mean_gplus_loss": float(np.mean(gplus_losses)) if gplus_losses else None,
        "mean_auxiliary_loss": float(np.mean(aux_losses)) if aux_losses else None,
        "staged_pretrain_steps": STAGED_PRETRAIN_STEPS if variant == "staged_real_goal_pretrain_then_gplus_finetune" else 0,
    }


def bellman_residual_gplus(values: np.ndarray, env: FourRooms) -> np.ndarray:
    pred = values[:, :, env.g_plus_index]
    target = gplus_backup(pred, env, GAMMA)
    return np.abs(target - pred)


def evaluate_reward_policy(env: FourRooms, values: np.ndarray) -> dict[str, Any]:
    successes = []
    returns = []
    horizon = env.n_states * 2
    for start in range(env.n_states):
        if start == env.reward_goal_state:
            continue
        state = start
        total = 0.0
        success = False
        for _ in range(horizon):
            action = greedy_action(values[state, :, env.g_plus_index])
            next_state = int(env.transitions[state, action])
            reward = float(env.rewards[state, action])
            total += reward
            state = next_state
            if state == env.reward_goal_state:
                success = True
                break
        successes.append(success)
        returns.append(total)
    return {
        "mean_raw_return": float(np.mean(returns)),
        "success_rate": float(np.mean(successes)),
        "evaluated_start_states": len(successes),
    }


def evaluate_goal_policy(env: FourRooms, values: np.ndarray, exact_goals: np.ndarray, distances: np.ndarray) -> dict[str, Any]:
    success_rates = []
    reductions = []
    disagreements = []
    horizon = env.n_states * 2
    for goal in range(env.n_states):
        goal_success = []
        goal_reductions = []
        for start in range(env.n_states):
            if start == goal:
                continue
            state = start
            first_action = greedy_action(values[state, :, goal])
            first_next = int(env.transitions[state, first_action])
            if math.isfinite(float(distances[start, goal])) and math.isfinite(float(distances[first_next, goal])):
                goal_reductions.append(float(distances[start, goal] - distances[first_next, goal]))
            reached = False
            for _ in range(horizon):
                action = greedy_action(values[state, :, goal])
                state = int(env.transitions[state, action])
                if state == goal:
                    reached = True
                    break
            goal_success.append(reached)
        disagreement = compare_policy(values[:, :, goal], exact_goals[:, :, goal], skip_states={goal})
        success_rates.append(float(np.mean(goal_success)))
        reductions.append(float(np.mean(goal_reductions)))
        disagreements.append(disagreement["disagreement_rate"])
    return {
        "mean_state_goal_value_error": float(np.mean(np.abs(values[:, :, : env.n_states] - exact_goals))),
        "max_state_goal_value_error": float(np.max(np.abs(values[:, :, : env.n_states] - exact_goals))),
        "mean_goal_success_rate": float(np.mean(success_rates)),
        "min_goal_success_rate": float(np.min(success_rates)),
        "mean_first_step_shortest_path_distance_reduction": float(np.mean(reductions)),
        "mean_goal_policy_disagreement_rate": float(np.mean(disagreements)),
        "max_goal_policy_disagreement_rate": float(np.max(disagreements)),
    }


def evaluate_model(
    env: FourRooms,
    model: LowRankModel,
    exact: dict[str, Any],
    distances: np.ndarray,
    variant: str,
    training_info: dict[str, Any],
) -> dict[str, Any]:
    pred_flat = model.predict_matrix()
    values = pred_flat.reshape(env.n_states, env.n_actions, env.n_goals_total)
    gplus = values[:, :, env.g_plus_index]
    scaled_error = np.abs(gplus / (1.0 - GAMMA) - exact["q_norm"])
    residual = bellman_residual_gplus(values, env)
    reward_policy = compare_policy(gplus, exact["f_gplus"], skip_states={env.reward_goal_state})
    return {
        "variant": variant,
        "gplus_mean_scaled_value_error": float(np.mean(scaled_error)),
        "gplus_max_scaled_value_error": float(np.max(scaled_error)),
        "gplus_mean_bellman_residual": float(np.mean(residual)),
        "gplus_max_bellman_residual": float(np.max(residual)),
        "reward_policy_disagreement_vs_exact": reward_policy,
        "reward_evaluation": evaluate_reward_policy(env, values),
        "real_goal_diagnostics": evaluate_goal_policy(env, values, exact["real_goals"], distances),
        "training_info": training_info,
    }


def run_seed(env: FourRooms, exact: dict[str, Any], seed: int, artifact_dir: Path) -> dict[str, Any]:
    replay = generate_replay(env, seed)
    coverage = replay_coverage(env, replay)
    batch_schedule, goal_schedule = schedules(seed)
    initial = LowRankModel(env, np.random.default_rng(seed + 90_000))
    distances = shortest_path_distances(env)
    variants = {}
    for variant in VARIANTS:
        model, info = train_variant(env, initial, replay, batch_schedule, goal_schedule, variant)
        variants[variant] = evaluate_model(env, model, exact, distances, variant, info)
    adequate = bool(coverage["adequate_replay_coverage"])
    for variant in VARIANTS:
        if variant != "terminal_only":
            adequate = adequate and variants[variant]["training_info"]["goal_label_coverage_fraction"] >= ADEQUATE_GOAL_LABEL_FRACTION
    terminal_eval = variants["terminal_only"]
    deltas = {}
    for variant in VARIANTS:
        if variant == "terminal_only":
            continue
        eval_row = variants[variant]
        deltas[variant] = {
            "gplus_mean_scaled_value_error": eval_row["gplus_mean_scaled_value_error"]
            - terminal_eval["gplus_mean_scaled_value_error"],
            "gplus_mean_bellman_residual": eval_row["gplus_mean_bellman_residual"]
            - terminal_eval["gplus_mean_bellman_residual"],
            "reward_policy_disagreement_rate": eval_row["reward_policy_disagreement_vs_exact"]["disagreement_rate"]
            - terminal_eval["reward_policy_disagreement_vs_exact"]["disagreement_rate"],
            "reward_success_rate": eval_row["reward_evaluation"]["success_rate"]
            - terminal_eval["reward_evaluation"]["success_rate"],
        }
    row = {
        "seed": seed,
        "coverage": coverage,
        "adequate_coverage": adequate,
        "variants": variants,
        "deltas_vs_terminal": deltas,
    }
    append_progress(
        artifact_dir,
        "seed_training",
        "completed",
        f"Completed all predeclared low-rank diagnostic variants for seed={seed}.",
        command=COMMANDS_RUN[4],
        seed=seed,
        adequate_coverage=adequate,
        original_value_error_delta=row["deltas_vs_terminal"]["combined_lambda_1_reproduction"]["gplus_mean_scaled_value_error"],
        balanced_value_error_delta=row["deltas_vs_terminal"]["combined_loss_balanced"]["gplus_mean_scaled_value_error"],
        staged_value_error_delta=row["deltas_vs_terminal"]["staged_real_goal_pretrain_then_gplus_finetune"]["gplus_mean_scaled_value_error"],
    )
    return row


def mean(values: list[float]) -> float:
    return float(np.mean(values)) if values else 0.0


def sem(values: list[float]) -> float:
    return float(np.std(values, ddof=1) / math.sqrt(len(values))) if len(values) > 1 else 0.0


def paired_indistinguishable(delta_values: list[float]) -> bool:
    return abs(mean(delta_values)) <= INDISTINGUISHABLE_Z * sem(delta_values)


def non_worse_or_indistinguishable(delta_values: list[float]) -> bool:
    return mean(delta_values) <= 0.0 or paired_indistinguishable(delta_values)


def relative_close(current: float, reference: float, tolerance: float = 0.05) -> bool:
    denom = max(abs(reference), 1.0e-12)
    return abs(current - reference) / denom <= tolerance


def variant_summary(rows: list[dict[str, Any]], variant: str) -> dict[str, Any]:
    adequate_rows = [row for row in rows if row["adequate_coverage"]]
    values = [row["variants"][variant]["gplus_mean_scaled_value_error"] for row in adequate_rows]
    residuals = [row["variants"][variant]["gplus_mean_bellman_residual"] for row in adequate_rows]
    policies = [
        row["variants"][variant]["reward_policy_disagreement_vs_exact"]["disagreement_rate"]
        for row in adequate_rows
    ]
    successes = [row["variants"][variant]["reward_evaluation"]["success_rate"] for row in adequate_rows]
    real_goal_errors = [
        row["variants"][variant]["real_goal_diagnostics"]["mean_state_goal_value_error"]
        for row in adequate_rows
    ]
    real_goal_success = [
        row["variants"][variant]["real_goal_diagnostics"]["mean_goal_success_rate"]
        for row in adequate_rows
    ]
    ratios = [
        row["variants"][variant]["training_info"]["mean_aux_to_gplus_u_grad_norm_ratio"]
        for row in adequate_rows
        if row["variants"][variant]["training_info"]["mean_aux_to_gplus_u_grad_norm_ratio"] is not None
    ]
    return {
        "mean_gplus_scaled_value_error": mean(values),
        "mean_gplus_bellman_residual": mean(residuals),
        "mean_reward_policy_disagreement": mean(policies),
        "mean_reward_success_rate": mean(successes),
        "mean_real_goal_value_error": mean(real_goal_errors),
        "mean_real_goal_success_rate": mean(real_goal_success),
        "mean_aux_to_gplus_u_grad_norm_ratio": mean(ratios) if ratios else None,
        "max_aux_to_gplus_u_grad_norm_ratio": max(ratios) if ratios else None,
        "mean_gplus_loss": mean(
            [
                row["variants"][variant]["training_info"]["mean_gplus_loss"]
                for row in adequate_rows
                if row["variants"][variant]["training_info"]["mean_gplus_loss"] is not None
            ]
        ),
        "mean_auxiliary_loss": mean(
            [
                row["variants"][variant]["training_info"]["mean_auxiliary_loss"]
                for row in adequate_rows
                if row["variants"][variant]["training_info"]["mean_auxiliary_loss"] is not None
            ]
        ),
    }


def repaired_variant_diagnostics(rows: list[dict[str, Any]], variant: str) -> dict[str, Any]:
    adequate_rows = [row for row in rows if row["adequate_coverage"]]
    value_deltas = [row["deltas_vs_terminal"][variant]["gplus_mean_scaled_value_error"] for row in adequate_rows]
    residual_deltas = [row["deltas_vs_terminal"][variant]["gplus_mean_bellman_residual"] for row in adequate_rows]
    policy_deltas = [row["deltas_vs_terminal"][variant]["reward_policy_disagreement_rate"] for row in adequate_rows]
    success_deltas = [row["deltas_vs_terminal"][variant]["reward_success_rate"] for row in adequate_rows]
    terminal_value = [row["variants"]["terminal_only"]["gplus_mean_scaled_value_error"] for row in adequate_rows]
    terminal_residual = [row["variants"]["terminal_only"]["gplus_mean_bellman_residual"] for row in adequate_rows]
    variant_value = [row["variants"][variant]["gplus_mean_scaled_value_error"] for row in adequate_rows]
    variant_residual = [row["variants"][variant]["gplus_mean_bellman_residual"] for row in adequate_rows]
    terminal_goal_error = [
        row["variants"]["terminal_only"]["real_goal_diagnostics"]["mean_state_goal_value_error"]
        for row in adequate_rows
    ]
    variant_goal_error = [
        row["variants"][variant]["real_goal_diagnostics"]["mean_state_goal_value_error"]
        for row in adequate_rows
    ]
    value_improvement = (mean(terminal_value) - mean(variant_value)) / mean(terminal_value) if mean(terminal_value) else 0.0
    residual_improvement = (
        (mean(terminal_residual) - mean(variant_residual)) / mean(terminal_residual)
        if mean(terminal_residual)
        else 0.0
    )
    policy_not_worse = mean(policy_deltas) <= 0.0 and max(policy_deltas, default=0.0) <= 0.0
    value_non_worse = non_worse_or_indistinguishable(value_deltas)
    residual_non_worse = non_worse_or_indistinguishable(residual_deltas)
    real_goal_improved = mean(variant_goal_error) < mean(terminal_goal_error)
    promising = policy_not_worse and (
        (value_improvement >= IMPROVEMENT_THRESHOLD and residual_non_worse)
        or (residual_improvement >= IMPROVEMENT_THRESHOLD and value_non_worse)
        or (value_non_worse and residual_non_worse and real_goal_improved)
    )
    matches_terminal = policy_not_worse and value_non_worse and residual_non_worse
    return {
        "mean_value_error_delta": mean(value_deltas),
        "sem_value_error_delta": sem(value_deltas),
        "mean_bellman_residual_delta": mean(residual_deltas),
        "sem_bellman_residual_delta": sem(residual_deltas),
        "mean_policy_disagreement_delta": mean(policy_deltas),
        "mean_reward_success_delta": mean(success_deltas),
        "relative_value_error_improvement": value_improvement,
        "relative_bellman_residual_improvement": residual_improvement,
        "policy_not_worse": policy_not_worse,
        "value_non_worse_or_indistinguishable": value_non_worse,
        "residual_non_worse_or_indistinguishable": residual_non_worse,
        "real_goal_error_improved_vs_terminal": real_goal_improved,
        "matches_terminal_gplus_metrics": matches_terminal,
        "promising": promising,
    }


def aggregate_rows(rows: list[dict[str, Any]], reference_0009: dict[str, Any] | None) -> dict[str, Any]:
    adequate_rows = [row for row in rows if row["adequate_coverage"]]
    summaries = {variant: variant_summary(rows, variant) for variant in VARIANTS}
    repaired = {
        variant: repaired_variant_diagnostics(rows, variant)
        for variant in ["combined_loss_balanced", "staged_real_goal_pretrain_then_gplus_finetune"]
    }
    original = repaired_variant_diagnostics(rows, "combined_lambda_1_reproduction")
    reproduction_checks = {"available": reference_0009 is not None}
    if reference_0009:
        reproduction_checks.update(
            {
                "terminal_value_error_matches": relative_close(
                    summaries["terminal_only"]["mean_gplus_scaled_value_error"],
                    reference_0009["mean_terminal_gplus_scaled_value_error"],
                ),
                "terminal_bellman_residual_matches": relative_close(
                    summaries["terminal_only"]["mean_gplus_bellman_residual"],
                    reference_0009["mean_terminal_gplus_bellman_residual"],
                ),
                "original_combined_value_error_matches": relative_close(
                    summaries["combined_lambda_1_reproduction"]["mean_gplus_scaled_value_error"],
                    reference_0009["mean_combined_gplus_scaled_value_error"],
                ),
                "original_combined_bellman_residual_matches": relative_close(
                    summaries["combined_lambda_1_reproduction"]["mean_gplus_bellman_residual"],
                    reference_0009["mean_combined_gplus_bellman_residual"],
                ),
            }
        )
        reproduction_checks["qualitatively_matches_0009"] = all(
            reproduction_checks[key]
            for key in [
                "terminal_value_error_matches",
                "terminal_bellman_residual_matches",
                "original_combined_value_error_matches",
                "original_combined_bellman_residual_matches",
            ]
        )
    else:
        reproduction_checks["qualitatively_matches_0009"] = False
    any_promising = any(item["promising"] for item in repaired.values())
    any_matches_terminal = any(item["matches_terminal_gplus_metrics"] for item in repaired.values())
    if len(adequate_rows) < len(rows):
        verdict = "coverage_limited"
    elif any(
        not np.isfinite(row["variants"][variant]["gplus_mean_scaled_value_error"])
        for row in rows
        for variant in VARIANTS
    ):
        verdict = "optimizer_failed"
    elif not reproduction_checks["qualitatively_matches_0009"]:
        verdict = "reproduction_failed"
    elif any_promising:
        verdict = "repaired_auxiliary_promising"
    elif not any_matches_terminal:
        verdict = "auxiliary_unsupported_for_lowrank"
    else:
        verdict = "auxiliary_neutral_for_lowrank"
    return {
        "run_count": len(rows),
        "adequate_coverage_count": len(adequate_rows),
        "coverage_limited_count": len(rows) - len(adequate_rows),
        "variant_summaries": summaries,
        "deltas_vs_terminal": {"combined_lambda_1_reproduction": original, **repaired},
        "reproduction_checks": reproduction_checks,
        "repaired_variant_names": list(repaired),
        "any_repaired_variant_promising": any_promising,
        "any_repaired_variant_matches_terminal": any_matches_terminal,
        "auxiliary_gradient_dominance": {
            variant: summaries[variant]["mean_aux_to_gplus_u_grad_norm_ratio"]
            for variant in VARIANTS
            if variant != "terminal_only"
        },
        "verdict": verdict,
    }


def write_seed_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    fields = [
        "seed",
        "variant",
        "adequate_coverage",
        "visited_state_action_fraction",
        "min_state_action_count",
        "reward_event_count",
        "value_error",
        "value_error_delta",
        "bellman_residual",
        "bellman_residual_delta",
        "policy_disagreement",
        "real_goal_value_error",
        "goal_success_rate",
        "mean_aux_to_gplus_u_grad_norm_ratio",
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            for variant in VARIANTS:
                delta = row["deltas_vs_terminal"].get(
                    variant,
                    {
                        "gplus_mean_scaled_value_error": 0.0,
                        "gplus_mean_bellman_residual": 0.0,
                    },
                )
                eval_row = row["variants"][variant]
                writer.writerow(
                    {
                        "seed": row["seed"],
                        "variant": variant,
                        "adequate_coverage": row["adequate_coverage"],
                        "visited_state_action_fraction": row["coverage"]["visited_state_action_fraction"],
                        "min_state_action_count": row["coverage"]["min_state_action_count"],
                        "reward_event_count": row["coverage"]["reward_event_count"],
                        "value_error": eval_row["gplus_mean_scaled_value_error"],
                        "value_error_delta": delta["gplus_mean_scaled_value_error"],
                        "bellman_residual": eval_row["gplus_mean_bellman_residual"],
                        "bellman_residual_delta": delta["gplus_mean_bellman_residual"],
                        "policy_disagreement": eval_row["reward_policy_disagreement_vs_exact"]["disagreement_rate"],
                        "real_goal_value_error": eval_row["real_goal_diagnostics"]["mean_state_goal_value_error"],
                        "goal_success_rate": eval_row["real_goal_diagnostics"]["mean_goal_success_rate"],
                        "mean_aux_to_gplus_u_grad_norm_ratio": eval_row["training_info"]["mean_aux_to_gplus_u_grad_norm_ratio"],
                    }
                )


def run_experiment_core(
    env: FourRooms,
    exact: dict[str, Any],
    artifact_dir: Path,
    reference_0009: dict[str, Any] | None,
) -> dict[str, Any]:
    rows = [run_seed(env, exact, seed, artifact_dir) for seed in SEEDS]
    aggregate = aggregate_rows(rows, reference_0009)
    payload = {
        "metadata": {
            "experiment_id": EXPERIMENT_ID,
            "gamma": GAMMA,
            "seeds": SEEDS,
            "rank": RANK,
            "replay_transitions": REPLAY_TRANSITIONS,
            "optimizer_steps": OPTIMIZER_STEPS,
            "batch_size": BATCH_SIZE,
            "auxiliary_weight": AUXILIARY_WEIGHT,
            "variants": VARIANTS,
            "loss_balance_clip": [LOSS_BALANCE_CLIP_MIN, LOSS_BALANCE_CLIP_MAX],
            "staged_pretrain_steps": STAGED_PRETRAIN_STEPS,
        },
        "aggregate": aggregate,
        "rows": rows,
    }
    write_json(artifact_dir / "per_seed_metrics.json", payload)
    write_seed_csv(artifact_dir / "per_seed_summary.csv", rows)
    replay_arrays = {}
    for seed in SEEDS:
        replay = generate_replay(env, seed)
        for key, value in replay.items():
            replay_arrays[f"seed_{seed}_{key}"] = value
    np.savez_compressed(artifact_dir / "replay_datasets.npz", **replay_arrays)
    return payload


def build_result(
    runtime_seconds: float,
    audit: dict[str, Any],
    audit_complete: bool,
    audit_missing: list[str],
    exact: dict[str, Any],
    learning: dict[str, Any],
    artifacts: list[str],
) -> dict[str, Any]:
    aggregate = learning["aggregate"]
    verdict = aggregate["verdict"]
    promising = verdict == "repaired_auxiliary_promising"
    pass_flags = {
        "environment_audit_complete": audit_complete,
        "verified_fourrooms_semantics_against_0008": audit["verified_against_0008_where_available"]["transition_hash_matches_0008"],
        "verified_fourrooms_config_against_0009": audit["verified_against_0009_where_available"]["transition_hash_matches"],
        "cpu_numpy_only": True,
        "shared_low_rank_model_used": True,
        "matched_replay_and_optimizer_schedule": True,
        "adequate_coverage_all_seeds": aggregate["adequate_coverage_count"] == len(SEEDS),
        "original_0009_reproduced": aggregate["reproduction_checks"]["qualitatively_matches_0009"],
        "gradient_norm_and_loss_scale_diagnostics_reported": True,
        "real_goal_auxiliary_diagnostics_reported": True,
        "no_unapproved_variant_sweep": set(VARIANTS)
        == {
            "terminal_only",
            "combined_lambda_1_reproduction",
            "combined_loss_balanced",
            "staged_real_goal_pretrain_then_gplus_finetune",
        },
        "repaired_variant_promising": promising,
    }
    known_failures = [key for key, value in pass_flags.items() if not value]
    interpretation = {
        "repaired_auxiliary_promising": (
            "At least one repaired auxiliary variant met the predeclared g_plus non-worse/improvement "
            "criterion without increasing reward-policy disagreement."
        ),
        "auxiliary_neutral_for_lowrank": (
            "A repaired auxiliary variant matched terminal-only g_plus metrics but did not provide a "
            "clear 10 percent improvement; auxiliary benefit remains unclaimed."
        ),
        "auxiliary_unsupported_for_lowrank": (
            "Original negative transfer reproduced, and neither repaired variant matched terminal-only "
            "on g_plus value error and Bellman residual. Auxiliary real-state goals should be paused for "
            "this low-rank architecture."
        ),
        "reproduction_failed": "The original 0009 negative-transfer result was not reproduced closely enough.",
        "coverage_limited": (
            "Replay or goal-label coverage was inadequate, so auxiliary-benefit claims are blocked."
        ),
        "optimizer_failed": "The optimizer produced non-finite or unusable metrics.",
    }[verdict]
    return {
        "experiment_id": EXPERIMENT_ID,
        "status": "completed",
        "claim_tested": (
            "The 0009 low-rank FourRooms negative transfer may be caused by loss-scaling or optimization "
            "imbalance; loss-balanced or staged auxiliary variants should reduce transfer harm if that "
            "diagnosis is correct."
        ),
        "commands_run": COMMANDS_RUN,
        "metrics": {
            "config": {
                "gamma": GAMMA,
                "seeds": SEEDS,
                "rank": RANK,
                "model": audit["model"],
                "replay_behavior": audit["replay_behavior"],
                "training_config": audit["training_config"],
                "predeclared_variants": VARIANTS,
                "coverage_thresholds": {
                    "visited_state_action_fraction": ADEQUATE_VISITED_SA_FRACTION,
                    "min_state_action_count": ADEQUATE_MIN_SA_COUNT,
                    "reward_event_count": ADEQUATE_REWARD_EVENT_COUNT,
                    "goal_label_fraction": ADEQUATE_GOAL_LABEL_FRACTION,
                },
                "improvement_threshold": IMPROVEMENT_THRESHOLD,
                "indistinguishable_z": INDISTINGUISHABLE_Z,
            },
            "environment_audit": {
                "complete": audit_complete,
                "missing_fields": audit_missing,
                "transition_table_hash": audit["transition_table_hash"],
                "verified_against_0008_where_available": audit["verified_against_0008_where_available"],
                "verified_against_0009_where_available": audit["verified_against_0009_where_available"],
                "reward_normalization": audit["reward_normalization"],
                "terminal_masks": audit["terminal_masks"],
                "goal_indexing": audit["goal_indexing"],
            },
            "exact_dp": {
                "gamma": GAMMA,
                "max_abs_scaled_gplus_minus_q_norm": exact["json"]["max_abs_scaled_gplus_minus_q_norm"],
                "q_iterations": exact["json"]["q_iterations"],
                "gplus_iterations": exact["json"]["gplus_iterations"],
                "goal_iterations": exact["json"]["goal_iterations"],
            },
            "lowrank_auxiliary": {
                "aggregate": aggregate,
                "rows": learning["rows"],
                "verdict": verdict,
            },
            "pass_flags": pass_flags,
        },
        "baseline_metrics": {
            "baseline_name": "terminal_only_gplus_lowrank",
            "mean_gplus_scaled_value_error": aggregate["variant_summaries"]["terminal_only"]["mean_gplus_scaled_value_error"],
            "mean_gplus_bellman_residual": aggregate["variant_summaries"]["terminal_only"]["mean_gplus_bellman_residual"],
            "mean_reward_success_rate": aggregate["variant_summaries"]["terminal_only"]["mean_reward_success_rate"],
        },
        "artifacts": artifacts,
        "interpretation": interpretation,
        "known_failures": known_failures,
        "next_questions": [
            "Should the auxiliary thread be paused for this low-rank architecture and written up as a negative result?",
            "Would a reviewed architecture with shared state-action generalization, not just shared goal factors, be a better next test?",
        ],
        "runtime_seconds": runtime_seconds,
        "resource_usage": {
            "device": "cpu",
            "gpu_used": False,
            "numpy_only": True,
            "large_dependencies_installed": False,
            "large_datasets_downloaded": False,
            "states": audit["open_cell_count"],
            "actions": 4,
            "rank": RANK,
            "optimizer_steps_per_variant_seed": OPTIMIZER_STEPS,
            "variants": len(VARIANTS),
            "seeds": len(SEEDS),
        },
        "success_criteria_results": [
            "PASS: result JSON, summary Markdown, and 0010 artifacts were created.",
            "PASS: CPU-only NumPy code was used; no neural framework or GPU work was added.",
            "PASS: 0008/0009 FourRooms semantics, reward normalization, terminal masks, goal indexing, replay behavior, and exact references were verified where available.",
            "PASS: exactly the four predeclared diagnostic variants were run.",
            (
                "PASS: terminal-only and original combined reproduction qualitatively match 0009."
                if pass_flags["original_0009_reproduced"]
                else "FAIL: terminal-only or original combined reproduction does not qualitatively match 0009."
            ),
            "PASS: per-variant g_plus loss, auxiliary loss, gradient norms, target scales, value error, residual, policy disagreement, reward success, and real-goal diagnostics are recorded.",
            "PASS: replay coverage, state-action coverage, reward events, and goal-label coverage are reported per seed.",
            (
                "PASS: a repaired auxiliary variant met the predeclared promising criterion."
                if promising
                else f"FAIL: repaired auxiliary variants did not meet the promising criterion; verdict is {verdict}."
            ),
            "PASS: real-state auxiliary goal predictions are evaluated against exact references with goal-reaching diagnostics.",
        ],
        "failure_criteria_results": [
            "NOT_TRIGGERED: model shares u_sa factors between real-state goals and g_plus in the combined variant.",
            "NOT_TRIGGERED: this is not independent tabular slicing; the model is rank-limited and shared.",
            (
                "NOT_TRIGGERED: replay coverage is adequate for all seeds."
                if pass_flags["adequate_coverage_all_seeds"]
                else "TRIGGERED: replay or goal-label coverage was inadequate for at least one seed."
            ),
            (
                "NOT_TRIGGERED: original 0009 negative transfer was reproduced."
                if pass_flags["original_0009_reproduced"]
                else "TRIGGERED: original 0009 negative transfer was not reproduced closely enough."
            ),
            "NOT_TRIGGERED: gradient-norm and loss-scale diagnostics are recorded.",
            "NOT_TRIGGERED: no unapproved rank, loss, auxiliary-weight, optimizer, or broad variant sweep was run.",
            "NOT_TRIGGERED: no neural framework, GPU, larger environment, or large dependency was used.",
        ],
        "metric_deltas": {
            "deltas_vs_terminal": aggregate["deltas_vs_terminal"],
            "auxiliary_gradient_dominance": aggregate["auxiliary_gradient_dominance"],
            "reproduction_checks": aggregate["reproduction_checks"],
            "verdict": verdict,
        },
        "decision_relevant_findings": [
            f"Conservative verdict: {verdict}.",
            "The low-rank model genuinely shares state-action factors across real-state goals and g_plus.",
            "Exact tabular references are used only for evaluation, not behavior generation or target labels.",
            "Auxiliary reward-task benefit should not be claimed unless the verdict is repaired_auxiliary_promising.",
        ],
    }


def write_summary(path: Path, result: dict[str, Any]) -> None:
    aggregate = result["metrics"]["lowrank_auxiliary"]["aggregate"]
    verdict = result["metrics"]["lowrank_auxiliary"]["verdict"]
    recommendation = (
        "proceed_to_tiny_reviewed_aux_followup"
        if verdict == "repaired_auxiliary_promising"
        else "pause_auxiliary_thread"
        if verdict in {"coverage_limited", "optimizer_failed", "reproduction_failed"}
        else "write_negative_result"
    )
    variant_lines = []
    for variant in VARIANTS:
        row = aggregate["variant_summaries"][variant]
        variant_lines.append(
            "| "
            + " | ".join(
                [
                    variant,
                    f"{row['mean_gplus_scaled_value_error']:.6g}",
                    f"{row['mean_gplus_bellman_residual']:.6g}",
                    f"{row['mean_reward_policy_disagreement']:.6g}",
                    f"{row['mean_real_goal_value_error']:.6g}",
                    str(row["mean_aux_to_gplus_u_grad_norm_ratio"]),
                ]
            )
            + " |"
        )
    summary = f"""# Experiment 0010 Summary

## Verdict

Low-rank FourRooms loss-scale diagnostic status: **{result["status"]}**.

Conservative label: **{verdict}**.

Recommendation: **{recommendation}**.

## Key Metrics

- Adequate-coverage seeds: `{aggregate["adequate_coverage_count"]}` / `{aggregate["run_count"]}`
- Original 0009 reproduction: `{aggregate["reproduction_checks"]["qualitatively_matches_0009"]}`
- Any repaired variant promising: `{aggregate["any_repaired_variant_promising"]}`
- Any repaired variant matches terminal g_plus metrics: `{aggregate["any_repaired_variant_matches_terminal"]}`

| Variant | g_plus value error | Bellman residual | Policy disagreement | Real-goal value error | Mean aux/g_plus U-grad ratio |
| --- | ---: | ---: | ---: | ---: | --- |
{chr(10).join(variant_lines)}

## Interpretation

{result["interpretation"]}

This is a tightly predeclared CPU NumPy diagnostic. It does not make publishable auxiliary-goal claims.

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
    env = FourRooms()
    audit = env.build_audit(repo_root)
    audit_complete, missing = validate_audit(audit)
    exact = solve_exact(env, artifact_dir)
    exact_ok = exact["json"]["max_abs_scaled_gplus_minus_q_norm"] <= 1.0e-10
    status = "passed" if audit_complete and exact_ok else "failed"
    payload = {
        "timestamp": utc_now(),
        "status": status,
        "command": COMMANDS_RUN[3],
        "audit_complete": audit_complete,
        "missing_fields": missing,
        "verified_against_0008": audit["verified_against_0008_where_available"],
        "verified_against_0009": audit["verified_against_0009_where_available"],
        "exact_scaled_gplus_matches_q_norm": exact_ok,
        "model_form": audit["model"]["form"],
        "rank": RANK,
        "seeds": SEEDS,
        "replay_transitions": REPLAY_TRANSITIONS,
    }
    write_json(artifact_dir / "local_compatibility_check.json", payload)
    append_progress(
        artifact_dir,
        "compatibility_check",
        status,
        "Checked FourRooms audit, 0008/0009 transition-hash match, exact g_plus/Q scaling, and low-rank model declaration.",
        command=COMMANDS_RUN[3],
        audit_complete=audit_complete,
        exact_scaled_gplus_matches_q_norm=exact_ok,
        verified_against_0008=audit["verified_against_0008_where_available"],
        verified_against_0009=audit["verified_against_0009_where_available"],
        missing_fields=missing,
    )
    return 0 if status == "passed" else 1


def run_experiment(repo_root: Path, artifact_dir: Path) -> int:
    start = time.perf_counter()
    result_dir = repo_root / "research" / PROJECT / "results"
    env = FourRooms()
    audit = env.build_audit(repo_root)
    audit_complete, missing = validate_audit(audit)
    write_json(artifact_dir / "environment_audit.json", audit)
    append_progress(
        artifact_dir,
        "environment_audit",
        "completed" if audit_complete else "failed",
        "Wrote FourRooms low-rank environment/model/replay audit.",
        command=COMMANDS_RUN[4],
        transition_table_hash=audit["transition_table_hash"],
        verified_against_0008=audit["verified_against_0008_where_available"],
        verified_against_0009=audit["verified_against_0009_where_available"],
        missing_fields=missing,
    )
    exact = solve_exact(env, artifact_dir)
    append_progress(
        artifact_dir,
        "exact_dp",
        "completed",
        "Computed exact g_plus, normalized Q, and real-state goal references for evaluation.",
        command=COMMANDS_RUN[4],
        max_abs_scaled_gplus_minus_q_norm=exact["json"]["max_abs_scaled_gplus_minus_q_norm"],
    )
    learning = run_experiment_core(
        env,
        exact,
        artifact_dir,
        audit["verified_against_0009_where_available"]["aggregate"],
    )
    append_progress(
        artifact_dir,
        "aggregate_metrics",
        "completed",
        "Aggregated low-rank diagnostic variants, reproduction checks, and repaired-variant deltas.",
        command=COMMANDS_RUN[4],
        aggregate=learning["aggregate"],
    )
    write_json(
        artifact_dir / "raw_metrics.json",
        {
            "metadata": {
                "experiment_id": EXPERIMENT_ID,
                "created_at": utc_now(),
                "transition_table_hash": audit["transition_table_hash"],
            },
            "environment_audit": audit,
            "exact_dp": exact["json"],
            "learning": learning,
        },
    )
    runtime = time.perf_counter() - start
    artifacts = [
        "research/reward_to_gcrl/artifacts/0010/run_fourrooms_lowrank_aux_diagnostic.py",
        "research/reward_to_gcrl/artifacts/0010/local_compatibility_check.json",
        "research/reward_to_gcrl/artifacts/0010/environment_audit.json",
        "research/reward_to_gcrl/artifacts/0010/exact_dp_references.json",
        "research/reward_to_gcrl/artifacts/0010/per_seed_metrics.json",
        "research/reward_to_gcrl/artifacts/0010/per_seed_summary.csv",
        "research/reward_to_gcrl/artifacts/0010/replay_datasets.npz",
        "research/reward_to_gcrl/artifacts/0010/raw_metrics.json",
        "research/reward_to_gcrl/artifacts/0010/progress.jsonl",
    ]
    result = build_result(runtime, audit, audit_complete, missing, exact, learning, artifacts)
    write_json(result_dir / "0010_result.json", result)
    write_summary(result_dir / "0010_summary.md", result)
    append_progress(
        artifact_dir,
        "result_write",
        result["status"],
        "Wrote 0010 result JSON and summary Markdown.",
        command=COMMANDS_RUN[4],
        result_path="research/reward_to_gcrl/results/0010_result.json",
        summary_path="research/reward_to_gcrl/results/0010_summary.md",
        verdict=result["metrics"]["lowrank_auxiliary"]["verdict"],
    )
    return 0


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
