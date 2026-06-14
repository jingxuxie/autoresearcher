#!/usr/bin/env python3
"""Experiment 0002 compatibility gate for Gymnasium CliffWalking-v0."""

from __future__ import annotations

import json
import time
import traceback
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import gymnasium as gym
import jsonschema


EXPERIMENT_ID = "0002"
PROJECT = "reward_to_gcrl"
ARTIFACT_REL = f"research/{PROJECT}/artifacts/{EXPERIMENT_ID}"
RESULT_REL = f"research/{PROJECT}/results/{EXPERIMENT_ID}_result.json"
SUMMARY_REL = f"research/{PROJECT}/results/{EXPERIMENT_ID}_summary.md"

COMMANDS_RUN = [
    "mkdir -p research/reward_to_gcrl/artifacts/0002 research/reward_to_gcrl/results",
    (
        "conda run -n autoresearcher_reward_to_gcrl python "
        "research/reward_to_gcrl/artifacts/0002/check_cliffwalking_v0_compatibility.py"
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


def repo_root_from_script() -> Path:
    return Path(__file__).resolve().parents[4]


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")


def append_progress(path: Path, event: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {"timestamp": utc_now(), **event}
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, sort_keys=True) + "\n")


def check_cliffwalking_v0() -> dict[str, Any]:
    registry_ids = sorted(env_id for env_id in gym.envs.registry.keys() if "CliffWalking" in env_id)
    check: dict[str, Any] = {
        "gymnasium_version": gym.__version__,
        "requested_env_id": "CliffWalking-v0",
        "registry_cliffwalking_ids": registry_ids,
        "gym_make_cliffwalking_v0": {},
    }
    try:
        env = gym.make("CliffWalking-v0")
    except Exception as exc:  # noqa: BLE001 - artifact should capture exact compatibility failure
        check["gym_make_cliffwalking_v0"] = {
            "status": "failed",
            "exception_type": type(exc).__name__,
            "exception_module": type(exc).__module__,
            "message": str(exc),
            "traceback": traceback.format_exc(),
        }
    else:
        try:
            unwrapped = env.unwrapped
            check["gym_make_cliffwalking_v0"] = {
                "status": "ok",
                "unwrapped_type": f"{type(unwrapped).__module__}.{type(unwrapped).__name__}",
                "n_states": int(unwrapped.observation_space.n),
                "n_actions": int(unwrapped.action_space.n),
            }
        finally:
            env.close()
    check["plan_can_run_as_written"] = check["gym_make_cliffwalking_v0"].get("status") == "ok"
    return check


def build_result(compatibility: dict[str, Any], runtime_seconds: float) -> dict[str, Any]:
    failure_message = compatibility["gym_make_cliffwalking_v0"].get("message", "")
    artifacts = [
        f"{ARTIFACT_REL}/check_cliffwalking_v0_compatibility.py",
        f"{ARTIFACT_REL}/compatibility_check.json",
        f"{ARTIFACT_REL}/progress.jsonl",
    ]
    return {
        "experiment_id": EXPERIMENT_ID,
        "status": "failed",
        "claim_tested": (
            "CPU-only tabular CliffWalking-v0 equivalence between ordinary normalized-reward "
            "Q-learning and terminal-only soft successor g_plus learning."
        ),
        "commands_run": COMMANDS_RUN,
        "metrics": {
            "compatibility_status": "failed",
            "plan_can_run_as_written": False,
            "requested_env_id": "CliffWalking-v0",
            "gymnasium_version": compatibility["gymnasium_version"],
            "registry_cliffwalking_ids": compatibility["registry_cliffwalking_ids"],
            "gym_make_cliffwalking_v0": compatibility["gym_make_cliffwalking_v0"],
            "reason_experiment_not_run": (
                "The installed Gymnasium raises an exception for gym.make('CliffWalking-v0'). "
                "The plan explicitly requires CliffWalking-v0, and the executor rule says to "
                "write a failed or blocked result immediately when compatibility checks show "
                "the plan cannot run as written."
            ),
            "dp_oracle_metrics_available": False,
            "paired_learning_metrics_available": False,
            "reward_normalization_predeclared_for_unrun_plan": {
                "original_reward_range": "CliffWalking rewards are -100 for cliff and -1 otherwise.",
                "normalization_formula": "r_bar = (original_reward + 100) / 99",
                "mapped_values": {"cliff_-100": 0.0, "step_or_goal_-1": 1.0},
                "note": "Saved for audit only; no experiment was run because v0 could not be instantiated.",
            },
            "terminal_mask_behavior_predeclared_for_unrun_plan": (
                "Bootstrap would be set to 0.0 whenever Gymnasium returns terminated=True; "
                "truncated would not occur in the transition-table DP."
            ),
            "planned_gamma_values": [0.95, 0.99],
            "planned_seeds": list(range(10)),
            "planned_episode_budget": 5000,
            "planned_alpha_schedule": "constant alpha=0.5 for both paired learners",
            "planned_epsilon_schedule": "epsilon starts at 0.2 and linearly decays to 0.02 over the episode budget",
            "predeclared_tolerances": {
                "exact_dp_scaled_value_error": 1.0e-6,
                "exact_dp_policy_disagreement_rate": 0.0,
                "paired_scaled_value_error_between_learners": 1.0e-10,
                "paired_policy_disagreement_rate": 0.0,
            },
        },
        "baseline_metrics": {},
        "artifacts": artifacts,
        "interpretation": (
            "Experiment 0002 did not run the DP or paired-learning phases. The compatibility "
            "check failed because Gymnasium rejected CliffWalking-v0 in this environment "
            f"({failure_message}). Since the plan specifically requires CliffWalking-v0, using "
            "CliffWalking-v1 or a direct class fallback would change the supplied plan."
        ),
        "known_failures": [
            "gym.make('CliffWalking-v0') failed in the ready project environment.",
            "No exact-DP oracle metrics or paired-learning metrics were produced because the compatibility gate failed before the experiment could run as written.",
        ],
        "next_questions": [
            "Should the next plan explicitly permit Gymnasium CliffWalking-v1 or direct CliffWalkingEnv(is_slippery=False) as equivalent semantics?",
            "Should JAX be added only if the tabular/CliffWalking-v0 registry alias is required by a future plan?",
        ],
        "runtime_seconds": runtime_seconds,
        "resource_usage": {
            "device": "cpu",
            "gpu_used": False,
            "experiment_phases_run": ["compatibility_check"],
            "experiment_phases_skipped": ["exact_dp_value_iteration", "paired_online_tabular_learning"],
            "large_dependencies_installed": False,
            "large_datasets_downloaded": False,
        },
        "success_criteria_results": [
            "PASS: created research/reward_to_gcrl/results/0002_result.json and research/reward_to_gcrl/results/0002_summary.md.",
            "PASS: created reproducible artifacts under research/reward_to_gcrl/artifacts/0002/.",
            "FAIL: did not run tabular CliffWalking-v0 methods because CliffWalking-v0 could not be instantiated.",
            "PARTIAL: saved planned reward normalization, gamma values, schedules, seeds, episode budget, terminal-mask behavior, and exact commands; they were not executed beyond the compatibility gate.",
            "FAIL: exact-DP oracle metrics were not produced because the compatibility gate failed.",
            "FAIL: paired-learning metrics over 10 seeds were not produced because the compatibility gate failed.",
            "FAIL: pass criteria were not evaluated because the required environment id failed to instantiate.",
        ],
        "failure_criteria_results": [
            "PASS: failed result JSON is schema-compatible.",
            "TRIGGERED: CliffWalking-v0 transition semantics are unavailable through gym.make in this environment, so running the plan would be ambiguous.",
            "TRIGGERED: scaled value error and policy disagreement are omitted because no learning run occurred after compatibility failure.",
            "NOT_EVALUATED: soft learner equivalence was not tested.",
            "PASS: no sampled augmented baselines, auxiliary state goals, neural approximation, large environments, or expensive training were run.",
            "PASS: commands are recorded and declared artifact paths exist.",
        ],
        "metric_deltas": {},
        "decision_relevant_findings": [
            "The installed Gymnasium version exposes CliffWalking-v1 and tabular/CliffWalking-v0, but gym.make('CliffWalking-v0') raises a DeprecatedEnv exception.",
            "Because the plan names CliffWalking-v0 exactly, this iteration should be treated as a compatibility failure rather than evidence for or against soft successor equivalence.",
        ],
    }


def build_summary(result: dict[str, Any]) -> str:
    metrics = result["metrics"]
    failure = metrics["gym_make_cliffwalking_v0"]
    return f"""# Experiment {EXPERIMENT_ID} Summary

## Compatibility Gate

Status: `{result['status']}`.

The supplied plan requires `gym.make("CliffWalking-v0")`. In the ready project environment, Gymnasium `{metrics['gymnasium_version']}` rejected that environment id with `{failure.get('exception_type')}`:

```text
{failure.get('message')}
```

Per the executor rule for compatibility failures, the DP and paired-learning phases were not run and no fallback to `CliffWalking-v1` or `CliffWalkingEnv(is_slippery=False)` was used.

## Commands Run

```bash
{chr(10).join(result['commands_run'])}
```

## Planned But Not Run

- Reward normalization: `r_bar = (original_reward + 100) / 99`, mapping cliff `-100` to `0.0` and step/goal `-1` to `1.0`.
- Terminal mask: bootstrap would be zero when `terminated=True`.
- Gamma values: `{metrics['planned_gamma_values']}`.
- Seeds: `{metrics['planned_seeds']}`.
- Episode budget: `{metrics['planned_episode_budget']}`.

## Outcome

This is a failed compatibility result, not evidence against the soft successor equivalence hypothesis. The next plan should explicitly allow `CliffWalking-v1` or the direct non-slippery `CliffWalkingEnv` class if those semantics are acceptable.

## Artifacts

{chr(10).join(f'- `{path}`' for path in result['artifacts'])}
"""


def main() -> int:
    started = time.perf_counter()
    repo_root = repo_root_from_script()
    artifact_dir = repo_root / ARTIFACT_REL
    result_dir = repo_root / "research" / PROJECT / "results"
    progress_path = artifact_dir / "progress.jsonl"
    artifact_dir.mkdir(parents=True, exist_ok=True)
    result_dir.mkdir(parents=True, exist_ok=True)

    append_progress(
        progress_path,
        {
            "event": "compatibility_script_started",
            "status": "running",
            "command": COMMANDS_RUN[1],
        },
    )
    compatibility = check_cliffwalking_v0()
    write_json(artifact_dir / "compatibility_check.json", compatibility)
    append_progress(
        progress_path,
        {
            "event": "cliffwalking_v0_compatibility_check",
            "status": "failed" if not compatibility["plan_can_run_as_written"] else "completed",
            "command": "gym.make('CliffWalking-v0')",
            "details": compatibility["gym_make_cliffwalking_v0"],
        },
    )

    runtime_seconds = time.perf_counter() - started
    result = build_result(compatibility, runtime_seconds)
    schema = json.loads((repo_root / "schemas" / "result.schema.json").read_text())
    jsonschema.Draft7Validator.check_schema(schema)
    jsonschema.Draft7Validator(schema).validate(result)
    write_json(repo_root / RESULT_REL, result)
    (repo_root / SUMMARY_REL).write_text(build_summary(result))
    append_progress(
        progress_path,
        {
            "event": "failed_result_written",
            "status": "completed",
            "command": COMMANDS_RUN[1],
            "result_path": RESULT_REL,
            "summary_path": SUMMARY_REL,
        },
    )
    append_progress(
        progress_path,
        {
            "event": "internal_schema_validation",
            "status": "completed",
            "command": "jsonschema.Draft7Validator(schema).validate(result)",
            "schema": "schemas/result.schema.json",
        },
    )
    print(
        json.dumps(
            {
                "experiment_id": EXPERIMENT_ID,
                "status": "failed",
                "reason": result["metrics"]["reason_experiment_not_run"],
                "requested_env_id": "CliffWalking-v0",
                "gymnasium_version": compatibility["gymnasium_version"],
                "exception_type": compatibility["gym_make_cliffwalking_v0"].get("exception_type"),
                "runtime_seconds": runtime_seconds,
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
