# Supervisor Context: sto_trl

## Requested action

Choose continue, pivot, stop, or needs_human. If this is iteration 0 with no prior result, propose the first small experiment when the charter is specific enough. If continuing, propose exactly one small experiment.


## Project charter

# Stochastic TRL Charter

## Research Goal

Rapidly test whether a stochastic extension of Transitive RL is worth pursuing.

The core question is whether calibrated stochastic successor distances plus TRL-style divide-and-conquer path relaxation can improve long-horizon offline goal-conditioned RL under stochastic dynamics, especially in environments with risky shortcuts or stochastic teleporters.

The full prototype plan is in `research/sto_trl/stochastic_trl_fast_prototype_plan.md`. This charter is the compact source of truth for the autoresearcher loop.

## Main Hypothesis

A stochastic-calibrated log or successor-distance TRL variant can reduce optimistic bias on risky stochastic paths while preserving TRL-style horizon generalization.

More concretely:

- Raw deterministic-style TRL may overestimate lucky stochastic paths.
- Log-space TRL should be numerically safer for long horizons than raw probability products.
- Adding a calibrated stochastic distance or successor-distance term should improve value calibration at stochastic branch points.
- A useful method should reduce overestimation without simply becoming conservative everywhere.

## Initial Scope

Start with tabular experiments only. Do not start with OGBench, PointMaze, AntMaze, or large neural-network training.

The first autoresearcher iterations should implement and test:

1. A deterministic chain sanity check.
2. A risky shortcut versus safe route stochastic MDP.
3. Exact DP ground truth for discounted reachability.
4. Small offline trajectory generation with lucky and unlucky stochastic outcomes.
5. Baselines: MC supervised, TRL-raw, TRL-log, and MC + TRL-log.

Only after deterministic and stochastic tabular diagnostics are clean should later iterations consider learned tabular models, tiny MLPs, continuous point mazes, or OGBench teleport tasks.

## Primary Metrics

Use exact DP ground truth wherever possible.

Primary metrics:

- Overestimation error: mean `max(0, U_hat - U_star)`.
- Policy regret versus exact DP policy.
- Long-horizon value MSE.
- Risky action selection rate.
- Calibration error for discounted reachability.

Secondary metrics:

- Underestimation error.
- Triangle violation rate for learned distance-like quantities.
- Greedy policy success rate.
- Median steps to goal.
- Coverage diagnostics for states, actions, goals, and risky success/failure outcomes.

## Success Criteria

Early evidence is positive only if a small tabular experiment shows at least one of:

- Raw TRL has a measurable overoptimism region on stochastic risky paths.
- TRL-log or MC + TRL-log improves long-horizon estimates over MC-only without breaking deterministic sanity checks.
- A stochastic-calibrated variant reduces risky-path overestimation while preserving safe-route value estimates.
- The greedy policy improves regret or risky-action choice versus raw TRL under exact DP evaluation.

The first iteration should be considered successful if it creates a reproducible tabular harness and produces a valid result table for at least the deterministic chain and one risky-shortcut configuration.

## Failure Criteria

Pause or stop before larger experiments if:

- Raw/log TRL cannot recover deterministic shortest-path behavior in a simple chain.
- There is no exact DP ground truth for the stochastic diagnostic.
- The experiment only reports training loss and no value/policy calibration metrics.
- The stochastic variant wins only by being conservative and avoiding all risky paths, including cases where risk is optimal.
- The loop attempts OGBench, AntMaze, large downloads, or long training before tabular diagnostics pass.
- The result omits exact commands, raw metrics, or coverage diagnostics.

## Runtime And Compute Budget

Initial experiments should complete in minutes on CPU or GPU.

Use the project conda environment `autoresearcher_sto_trl`. JAX/GPU is allowed and preferred when available, but the first tabular experiments must remain small enough to run without expensive training.

Treat step counts in offline diagnostics as optimizer/update steps unless the experiment explicitly reports environment rollouts. For this project, early runtime should mostly come from JAX/XLA compilation, repeated updates, pair sampling, and scoring rather than environment interaction.

## First Experiment Guidance

The supervisor should propose exactly one small experiment for iteration 1:

- Build a minimal tabular prototype under `research/sto_trl/artifacts/0001/`.
- Implement deterministic chain and risky shortcut MDPs.
- Implement exact discounted reachability DP.
- Compare MC supervised, TRL-raw, TRL-log, and MC + TRL-log on a tiny configuration.
- Save raw metrics to JSON or CSV.
- Produce `research/sto_trl/results/0001_result.json` and `research/sto_trl/results/0001_summary.md`.

Do not optimize for benchmark performance in the first run. Optimize for a correct diagnostic that can reveal whether the idea has a real failure mode to target.


## Environment state

```json
{
  "blocker": null,
  "commands_run": [
    "conda env create -f research/sto_trl/environment.yaml",
    "nvidia-smi -L",
    "conda run -n autoresearcher_sto_trl python scripts/probe_jax_gpu.py --require-gpu --output research/sto_trl/setup_logs/jax_gpu_probe.json",
    "conda run -n autoresearcher_sto_trl python -c \"import sys, yaml, jsonschema, jax; print(sys.version.split()[0]); print(yaml.__version__); print(jsonschema.__version__); print(jax.__version__)\""
  ],
  "conda_env_name": "autoresearcher_sto_trl",
  "conda_env_path": "/home/eston/anaconda3/envs/autoresearcher_sto_trl",
  "environment_file": "research/sto_trl/environment.yaml",
  "gpu_available": true,
  "gpu_checks": [
    "nvidia-smi -L reported GPU 0: NVIDIA GeForce RTX 4090",
    "JAX default_backend reported gpu",
    "JAX devices reported cuda:0",
    "Tiny JAX compute returned 140.0"
  ],
  "gpu_requested": true,
  "packages_verified": [
    "python 3.11.15",
    "pyyaml 6.0.3",
    "jsonschema 4.26.0",
    "jax 0.10.1",
    "jaxlib 0.10.1",
    "jax[cuda12]"
  ],
  "project": "sto_trl",
  "status": "ready",
  "summary": "Conda environment autoresearcher_sto_trl was created from environment.yaml. JAX imports successfully, sees cuda:0, uses gpu as the default backend, and completed a tiny GPU computation."
}
```


## Current state

```json
{
  "best_primary_metric": null,
  "human_review_required": false,
  "iteration": 1,
  "last_decision": "continue",
  "last_pro_review_iteration": 0,
  "no_progress_rounds": 1,
  "notes": [],
  "primary_metric": null,
  "status": "active"
}
```


## Latest result JSON

```json
{
  "artifacts": [
    "research/sto_trl/artifacts/0001/run_tabular_sto_trl.py",
    "research/sto_trl/artifacts/0001/raw_metrics.json",
    "research/sto_trl/artifacts/0001/metrics.csv",
    "research/sto_trl/artifacts/0001/offline_dataset.json",
    "research/sto_trl/artifacts/0001/transition_tables.json",
    "research/sto_trl/artifacts/0001/value_tables.json"
  ],
  "baseline_metrics": {
    "deterministic_chain": {
      "calibration_error": 0.2638688400000001,
      "eval_goal": "c5",
      "eval_greedy_action": "right",
      "eval_start": "c0",
      "eval_start_exact_q": {
        "right": 0.5904900000000002
      },
      "eval_start_exact_value": 0.5904900000000002,
      "eval_start_learned_q": {
        "right": 0.5904900000000001
      },
      "eval_start_learned_value": 0.5904900000000001,
      "long_horizon_value_mse": 3.697785493223493e-33,
      "max_policy_regret": 0.0,
      "mean_policy_regret": 0.0,
      "policy_regret": 0.0,
      "q_calibration_error": 0.2638688400000001,
      "q_overestimation_error": 0.0,
      "q_underestimation_error": 0.7290000000000001,
      "risky_action_selection_rate": 0.0,
      "value_mse": 2.0543252740130515e-33,
      "value_overestimation_error": 0.0,
      "value_underestimation_error": 1.1102230246251565e-16
    },
    "method": "mc_supervised",
    "risky_shortcut": {
      "calibration_error": 0.0,
      "eval_goal": "goal",
      "eval_greedy_action": "safe",
      "eval_start": "start",
      "eval_start_exact_q": {
        "risky": 0.225,
        "safe": 0.7290000000000001
      },
      "eval_start_exact_value": 0.7290000000000001,
      "eval_start_learned_q": {
        "risky": 0.225,
        "safe": 0.7290000000000001
      },
      "eval_start_learned_value": 0.7290000000000001,
      "long_horizon_value_mse": 0.0,
      "max_policy_regret": 0.0,
      "mean_policy_regret": 0.0,
      "policy_regret": 0.0,
      "q_calibration_error": 0.0,
      "q_overestimation_error": 0.0,
      "q_underestimation_error": 0.0,
      "risky_action_selection_rate": 0.0,
      "value_mse": 0.0,
      "value_overestimation_error": 0.0,
      "value_underestimation_error": 0.0
    }
  },
  "claim_tested": "A tiny stochastic risky-shortcut MDP exposes overestimation by deterministic raw TRL backups, while log-space stochastic backups preserve deterministic-chain behavior and improve risky-action calibration relative to raw TRL.",
  "commands_run": [
    "mkdir -p research/sto_trl/artifacts/0001 research/sto_trl/results",
    "conda run -n autoresearcher_sto_trl python research/sto_trl/artifacts/0001/run_tabular_sto_trl.py",
    "conda run -n autoresearcher_sto_trl python scripts/validate_artifacts.py --repo-root . --json research/sto_trl/results/0001_result.json --schema schemas/result.schema.json --check-result-artifacts"
  ],
  "experiment_id": "0001",
  "interpretation": "The deterministic chain sanity check was recovered by both raw and log TRL. On the risky-shortcut MDP, raw deterministic-style TRL treated the observed lucky risky edge as reliable and selected risky with Q=0.900000 versus exact Q=0.225000. The empirical log backup and MC+TRL-log selected the safe route and had zero start-goal policy regret in this tiny dataset. MC supervised was also calibrated here because the offline set deliberately included both lucky and unlucky risky outcomes.",
  "known_failures": [],
  "metrics": {
    "experiment_id": "0001",
    "gamma": 0.9,
    "mdps": {
      "deterministic_chain": {
        "coverage_diagnostics": {
          "action_counts": {
            "left": 5,
            "right": 5
          },
          "future_goal_coverage_fraction": 1.0,
          "future_goals_seen": [
            "c0",
            "c1",
            "c2",
            "c3",
            "c4",
            "c5"
          ],
          "num_episodes": 2,
          "num_transitions": 10,
          "outcome_counts": {
            "deterministic": 10
          },
          "risky_failure_count": 0,
          "risky_success_count": 0,
          "risky_success_rate_observed": null,
          "state_action_coverage_fraction": 1.0,
          "state_action_pairs_seen": [
            [
              "c0",
              "right"
            ],
            [
              "c1",
              "left"
            ],
            [
              "c1",
              "right"
            ],
            [
              "c2",
              "left"
            ],
            [
              "c2",
              "right"
            ],
            [
              "c3",
              "left"
            ],
            [
              "c3",
              "right"
            ],
            [
              "c4",
              "left"
            ],
            [
              "c4",
              "right"
            ],
            [
              "c5",
              "left"
            ]
          ],
          "state_coverage_fraction": 1.0,
          "states_seen": [
            "c0",
            "c1",
            "c2",
            "c3",
            "c4",
            "c5"
          ],
          "transition_counts": {
            "c0|right|c1": 1,
            "c1|left|c0": 1,
            "c1|right|c2": 1,
            "c2|left|c1": 1,
            "c2|right|c3": 1,
            "c3|left|c2": 1,
            "c3|right|c4": 1,
            "c4|left|c3": 1,
            "c4|right|c5": 1,
            "c5|left|c4": 1
          }
        },
        "methods": {
          "mc_plus_trl_log": {
            "calibration_error": 0.13193442000000005,
            "eval_goal": "c5",
            "eval_greedy_action": "right",
            "eval_start": "c0",
            "eval_start_exact_q": {
              "right": 0.5904900000000002
            },
            "eval_start_exact_value": 0.5904900000000002,
            "eval_start_learned_q": {
              "right": 0.5904900000000002
            },
            "eval_start_learned_value": 0.5904900000000002,
            "long_horizon_value_mse": 0.0,
            "max_policy_regret": 0.0,
            "mean_policy_regret": 0.0,
            "policy_regret": 0.0,
            "q_calibration_error": 0.13193442000000005,
            "q_overestimation_error": 0.0,
            "q_underestimation_error": 0.36450000000000005,
            "risky_action_selection_rate": 0.0,
            "value_mse": 0.0,
            "value_overestimation_error": 0.0,
            "value_underestimation_error": 0.0
          },
          "mc_supervised": {
            "calibration_error": 0.2638688400000001,
            "eval_goal": "c5",
            "eval_greedy_action": "right",
            "eval_start": "c0",
            "eval_start_exact_q": {
              "right": 0.5904900000000002
            },
            "eval_start_exact_value": 0.5904900000000002,
            "eval_start_learned_q": {
              "right": 0.5904900000000001
            },
            "eval_start_learned_value": 0.5904900000000001,
            "long_horizon_value_mse": 3.697785493223493e-33,
            "max_policy_regret": 0.0,
            "mean_policy_regret": 0.0,
            "policy_regret": 0.0,
            "q_calibration_error": 0.2638688400000001,
            "q_overestimation_error": 0.0,
            "q_underestimation_error": 0.7290000000000001,
            "risky_action_selection_rate": 0.0,
            "value_mse": 2.0543252740130515e-33,
            "value_overestimation_error": 0.0,
            "value_underestimation_error": 1.1102230246251565e-16
          },
          "trl_log": {
            "calibration_error": 0.0,
            "eval_goal": "c5",
            "eval_greedy_action": "right",
            "eval_start": "c0",
            "eval_start_exact_q": {
              "right": 0.5904900000000002
            },
            "eval_start_exact_value": 0.5904900000000002,
            "eval_start_learned_q": {
              "right": 0.5904900000000002
            },
            "eval_start_learned_value": 0.5904900000000002,
            "long_horizon_value_mse": 0.0,
            "max_policy_regret": 0.0,
            "mean_policy_regret": 0.0,
            "policy_regret": 0.0,
            "q_calibration_error": 0.0,
            "q_overestimation_error": 0.0,
            "q_underestimation_error": 0.0,
            "risky_action_selection_rate": 0.0,
            "value_mse": 0.0,
            "value_overestimation_error": 0.0,
            "value_underestimation_error": 0.0
          },
          "trl_raw": {
            "calibration_error": 0.0,
            "eval_goal": "c5",
            "eval_greedy_action": "right",
            "eval_start": "c0",
            "eval_start_exact_q": {
              "right": 0.5904900000000002
            },
            "eval_start_exact_value": 0.5904900000000002,
            "eval_start_learned_q": {
              "right": 0.5904900000000002
            },
            "eval_start_learned_value": 0.5904900000000002,
            "long_horizon_value_mse": 0.0,
            "max_policy_regret": 0.0,
            "mean_policy_regret": 0.0,
            "policy_regret": 0.0,
            "q_calibration_error": 0.0,
            "q_overestimation_error": 0.0,
            "q_underestimation_error": 0.0,
            "risky_action_selection_rate": 0.0,
            "value_mse": 0.0,
            "value_overestimation_error": 0.0,
            "value_underestimation_error": 0.0
          }
        }
      },
      "risky_shortcut": {
        "coverage_diagnostics": {
          "action_counts": {
            "forward": 8,
            "risky": 8,
            "safe": 4
          },
          "future_goal_coverage_fraction": 0.8,
          "future_goals_seen": [
            "goal",
            "safe1",
            "safe2",
            "trap"
          ],
          "num_episodes": 12,
          "num_transitions": 20,
          "outcome_counts": {
            "risky_failure": 6,
            "risky_success": 2,
            "safe_goal": 4,
            "safe_step": 8
          },
          "risky_failure_count": 6,
          "risky_success_count": 2,
          "risky_success_rate_observed": 0.25,
          "state_action_coverage_fraction": 1.0,
          "state_action_pairs_seen": [
            [
              "safe1",
              "forward"
            ],
            [
              "safe2",
              "forward"
            ],
            [
              "start",
              "risky"
            ],
            [
              "start",
              "safe"
            ]
          ],
          "state_coverage_fraction": 1.0,
          "states_seen": [
            "goal",
            "safe1",
            "safe2",
            "start",
            "trap"
          ],
          "transition_counts": {
            "safe1|forward|safe2": 4,
            "safe2|forward|goal": 4,
            "start|risky|goal": 2,
            "start|risky|trap": 6,
            "start|safe|safe1": 4
          }
        },
        "methods": {
          "mc_plus_trl_log": {
            "calibration_error": 0.0,
            "eval_goal": "goal",
            "eval_greedy_action": "safe",
            "eval_start": "start",
            "eval_start_exact_q": {
              "risky": 0.225,
              "safe": 0.7290000000000001
            },
            "eval_start_exact_value": 0.7290000000000001,
            "eval_start_learned_q": {
              "risky": 0.225,
              "safe": 0.7290000000000001
            },
            "eval_start_learned_value": 0.7290000000000001,
            "long_horizon_value_mse": 0.0,
            "max_policy_regret": 0.0,
            "mean_policy_regret": 0.0,
            "policy_regret": 0.0,
            "q_calibration_error": 0.0,
            "q_overestimation_error": 0.0,
            "q_underestimation_error": 0.0,
            "risky_action_selection_rate": 0.0,
            "value_mse": 0.0,
            "value_overestimation_error": 0.0,
            "value_underestimation_error": 0.0
          },
          "mc_supervised": {
            "calibration_error": 0.0,
            "eval_goal": "goal",
            "eval_greedy_action": "safe",
            "eval_start": "start",
            "eval_start_exact_q": {
              "risky": 0.225,
              "safe": 0.7290000000000001
            },
            "eval_start_exact_value": 0.7290000000000001,
            "eval_start_learned_q": {
              "risky": 0.225,
              "safe": 0.7290000000000001
            },
            "eval_start_learned_value": 0.7290000000000001,
            "long_horizon_value_mse": 0.0,
            "max_policy_regret": 0.0,
            "mean_policy_regret": 0.0,
            "policy_regret": 0.0,
            "q_calibration_error": 0.0,
            "q_overestimation_error": 0.0,
            "q_underestimation_error": 0.0,
            "risky_action_selection_rate": 0.0,
            "value_mse": 0.0,
            "value_overestimation_error": 0.0,
            "value_underestimation_error": 0.0
          },
          "trl_log": {
            "calibration_error": 0.0,
            "eval_goal": "goal",
            "eval_greedy_action": "safe",
            "eval_start": "start",
            "eval_start_exact_q": {
              "risky": 0.225,
              "safe": 0.7290000000000001
            },
            "eval_start_exact_value": 0.7290000000000001,
            "eval_start_learned_q": {
              "risky": 0.225,
              "safe": 0.7290000000000001
            },
            "eval_start_learned_value": 0.7290000000000001,
            "long_horizon_value_mse": 0.0,
            "max_policy_regret": 0.0,
            "mean_policy_regret": 0.0,
            "policy_regret": 0.0,
            "q_calibration_error": 0.0,
            "q_overestimation_error": 0.0,
            "q_underestimation_error": 0.0,
            "risky_action_selection_rate": 0.0,
            "value_mse": 0.0,
            "value_overestimation_error": 0.0,
            "value_underestimation_error": 0.0
          },
          "trl_raw": {
            "calibration_error": 0.05625,
            "eval_goal": "goal",
            "eval_greedy_action": "risky",
            "eval_start": "start",
            "eval_start_exact_q": {
              "risky": 0.225,
              "safe": 0.7290000000000001
            },
            "eval_start_exact_value": 0.7290000000000001,
            "eval_start_learned_q": {
              "risky": 0.9,
              "safe": 0.7290000000000001
            },
            "eval_start_learned_value": 0.9,
            "long_horizon_value_mse": 0.01996649999999999,
            "max_policy_regret": 0.5040000000000001,
            "mean_policy_regret": 0.07200000000000002,
            "policy_regret": 0.5040000000000001,
            "q_calibration_error": 0.05625,
            "q_overestimation_error": 0.675,
            "q_underestimation_error": 0.0,
            "risky_action_selection_rate": 1.0,
            "value_mse": 0.0031946399999999986,
            "value_overestimation_error": 0.22499999999999998,
            "value_underestimation_error": 0.0
          }
        }
      }
    },
    "success_checks": {
      "chain_log_recovers_discounted_reachability": true,
      "chain_raw_recovers_discounted_reachability": true,
      "risky_dataset_has_lucky_and_unlucky_outcomes": true,
      "success_criteria_met": true,
      "trl_log_prefers_safe_route": true,
      "trl_raw_overestimates_risky_action": true,
      "trl_raw_prefers_risky_shortcut": true
    },
    "update_steps": 32
  },
  "next_questions": [
    "Does MC-only lose calibration when the lucky/unlucky risky outcome ratio is intentionally imbalanced or lower coverage?",
    "Can the log-space stochastic backup remain stable with function approximation instead of exact tabular counts?",
    "Which coverage diagnostic best predicts when raw deterministic TRL will overestimate stochastic shortcuts?"
  ],
  "status": "completed"
}
```


## Latest summary

# Experiment 0001 Summary

## Objective

Build a minimal tabular diagnostic for stochastic TRL with exact discounted-reachability DP ground truth.

## Commands Run

```bash
mkdir -p research/sto_trl/artifacts/0001 research/sto_trl/results
conda run -n autoresearcher_sto_trl python research/sto_trl/artifacts/0001/run_tabular_sto_trl.py
conda run -n autoresearcher_sto_trl python scripts/validate_artifacts.py --repo-root . --json research/sto_trl/results/0001_result.json --schema schemas/result.schema.json --check-result-artifacts
```

## Setup

- Discount: `0.9`
- Fixed backup iterations: `32`
- MDPs: deterministic 6-state chain and 5-state risky-shortcut MDP.
- Offline risky coverage: `2` lucky risky successes and `6` unlucky risky failures.

## Key Raw Metrics

| MDP | Method | Long-horizon value MSE | Q calibration error | Policy regret | Risky selection |
| --- | --- | ---: | ---: | ---: | ---: |
| deterministic_chain | mc_supervised | 0.000000000000 | 0.263868840000 | 0.000000000000 | 0.0 |
| deterministic_chain | trl_raw | 0.000000000000 | 0.000000000000 | 0.000000000000 | 0.0 |
| deterministic_chain | trl_log | 0.000000000000 | 0.000000000000 | 0.000000000000 | 0.0 |
| deterministic_chain | mc_plus_trl_log | 0.000000000000 | 0.131934420000 | 0.000000000000 | 0.0 |
| risky_shortcut | mc_supervised | 0.000000000000 | 0.000000000000 | 0.000000000000 | 0.0 |
| risky_shortcut | trl_raw | 0.019966500000 | 0.056250000000 | 0.504000000000 | 1.0 |
| risky_shortcut | trl_log | 0.000000000000 | 0.000000000000 | 0.000000000000 | 0.0 |
| risky_shortcut | mc_plus_trl_log | 0.000000000000 | 0.000000000000 | 0.000000000000 | 0.0 |

## Diagnostic Outcome

- Chain raw TRL recovered exact discounted reachability: `True`.
- Chain log TRL recovered exact discounted reachability: `True`.
- Risky dataset covered lucky and unlucky outcomes: `True`.
- Raw TRL chose the risky shortcut: `True`.
- Log TRL chose the safe route: `True`.

The most decisive risky-start numbers are:

- Exact risky Q: `0.225000`
- Raw TRL risky Q: `0.900000`
- Log TRL risky Q: `0.225000`
- Exact safe Q: `0.729000`
- Raw TRL safe Q: `0.729000`
- Log TRL safe Q: `0.729000`

## Artifacts

- `research/sto_trl/artifacts/0001/run_tabular_sto_trl.py`
- `research/sto_trl/artifacts/0001/raw_metrics.json`
- `research/sto_trl/artifacts/0001/metrics.csv`
- `research/sto_trl/artifacts/0001/offline_dataset.json`
- `research/sto_trl/artifacts/0001/transition_tables.json`
- `research/sto_trl/artifacts/0001/value_tables.json`

## Interpretation

The deterministic chain sanity check was recovered by both raw and log TRL. On the risky-shortcut MDP, raw deterministic-style TRL treated the observed lucky risky edge as reliable and selected risky with Q=0.900000 versus exact Q=0.225000. The empirical log backup and MC+TRL-log selected the safe route and had zero start-goal policy regret in this tiny dataset. MC supervised was also calibrated here because the offline set deliberately included both lucky and unlucky risky outcomes.

## Known Failures

- None.


## Latest review JSON

```json
{
  "allows_auto_continue": true,
  "evidence_checked": [
    "research/sto_trl/results/0001_result.json",
    "research/sto_trl/results/0001_summary.md",
    "research/sto_trl/artifacts/0001/run_tabular_sto_trl.py",
    "research/sto_trl/artifacts/0001/raw_metrics.json",
    "research/sto_trl/artifacts/0001/metrics.csv",
    "research/sto_trl/artifacts/0001/offline_dataset.json",
    "research/sto_trl/artifacts/0001/transition_tables.json",
    "research/sto_trl/artifacts/0001/value_tables.json",
    "research/sto_trl/env_state.json",
    "schemas/result.schema.json",
    "schemas/review.schema.json",
    "python scripts/validate_artifacts.py --repo-root . --json research/sto_trl/results/0001_result.json --schema schemas/result.schema.json --check-result-artifacts"
  ],
  "experiment_id": "0001",
  "reasons": [
    "Required result, summary, and artifact files are present under research/sto_trl/results and research/sto_trl/artifacts/0001.",
    "Result JSON validates against schemas/result.schema.json, and artifact existence validation returned validation ok.",
    "The prototype implements exact discounted-reachability DP over explicit transition tables for both deterministic_chain and risky_shortcut.",
    "All four methods are evaluated on the same tiny offline datasets, and raw metrics report value errors, Q calibration, policy regret, risky action selection, and coverage diagnostics.",
    "Failure criteria are not triggered: chain raw/log recover discounted reachability, risky data includes 2 lucky and 6 unlucky outcomes, no large training or dataset dependency is used, and raw value/policy metrics are saved.",
    "Interpretation is appropriately bounded for this tiny diagnostic and notes that MC supervised is also calibrated in the balanced risky dataset."
  ],
  "required_fixes": [],
  "risk_flags": [
    "Evidence is intentionally small-scale and balanced: risky outcome coverage exactly matches the true 0.25 success probability, so MC supervised is perfect here and the experiment mainly supports the raw-TRL overestimation diagnostic.",
    "/home/eston/autoresearcher is not a git repository, so unrelated modifications could not be audited with git status."
  ],
  "verdict": "pass"
}
```


## Last decisions

## 0001_decision.json

```json
{
  "confidence": 0.89,
  "decision": "continue",
  "evidence": [
    "research/sto_trl/state.json reports iteration 0, status active, and no prior primary metric.",
    "research/sto_trl/env_state.json reports status ready for conda environment autoresearcher_sto_trl with JAX GPU probe completed.",
    "The charter explicitly scopes early work to tabular experiments and requires exact DP ground truth, deterministic chain sanity, risky shortcut MDP, offline data, and MC/TRL baselines.",
    "No result JSON exists yet, which is allowed by the first-iteration rule."
  ],
  "next_experiment": {
    "estimated_runtime_minutes": 20,
    "experiment_id": "0001",
    "failure_criteria": [
      "No exact DP ground truth is implemented for the stochastic diagnostic.",
      "The deterministic chain does not recover shortest-path or discounted-reachability structure for raw/log variants.",
      "The result only reports training loss or prose without raw value and policy metrics.",
      "The risky-shortcut dataset lacks coverage of lucky and unlucky stochastic outcomes.",
      "The run requires large downloads, OGBench, AntMaze, neural-network training, or exceeds the 30 minute executor budget."
    ],
    "hypothesis": "A small tabular risky-shortcut MDP with offline lucky/unlucky outcomes will reveal whether raw deterministic-style TRL overestimates risky stochastic paths, while log-space or MC+TRL-log variants preserve deterministic behavior and improve calibration relative to MC-only or raw TRL.",
    "objective": "Build and run a minimal tabular diagnostic for stochastic TRL covering deterministic chain sanity and one risky-shortcut stochastic MDP, with exact discounted-reachability DP ground truth and raw metrics saved.",
    "required_outputs": [
      "research/sto_trl/artifacts/0001/tabular_sto_trl_prototype.py or equivalent self-contained source",
      "research/sto_trl/artifacts/0001/raw_metrics.json or raw_metrics.csv",
      "research/sto_trl/artifacts/0001/coverage_diagnostics.json",
      "research/sto_trl/results/0001_result.json",
      "research/sto_trl/results/0001_summary.md"
    ],
    "success_criteria": [
      "Creates a reproducible prototype under research/sto_trl/artifacts/0001/ without modifying repository control scripts or schemas.",
      "Produces exact DP ground truth for the deterministic chain and risky-shortcut MDP.",
      "Compares MC supervised, TRL-raw, TRL-log, and MC+TRL-log on the same tiny offline datasets.",
      "Saves raw numeric metrics including overestimation error, underestimation error, long-horizon value MSE, policy regret, risky action selection rate, calibration error, and coverage diagnostics.",
      "Writes valid research/sto_trl/results/0001_result.json and research/sto_trl/results/0001_summary.md with exact commands run."
    ],
    "tasks_for_codex": [
      "Create a small self-contained tabular prototype in research/sto_trl/artifacts/0001/.",
      "Implement deterministic chain and one risky-shortcut versus safe-route stochastic MDP with exact transition tables.",
      "Implement exact discounted reachability DP and greedy policy evaluation from the DP values.",
      "Generate tiny offline trajectories with explicit coverage diagnostics for states, actions, goals, and risky success/failure outcomes.",
      "Implement MC supervised, TRL-raw product backup, TRL-log additive backup, and MC+TRL-log using simple tabular tables and fixed small update counts.",
      "Run the experiment in conda environment autoresearcher_sto_trl with deterministic seeds and save raw metrics as JSON or CSV under research/sto_trl/artifacts/0001/.",
      "Write research/sto_trl/results/0001_result.json matching schemas/result.schema.json and research/sto_trl/results/0001_summary.md, including exact commands run."
    ]
  },
  "progress_score": 1,
  "rationale": "This is project start: iteration is 0, no latest result is expected, the environment is ready, and the charter gives a specific, cheap first experiment. The next step should be one small tabular harness that tests deterministic sanity and a risky-shortcut stochastic diagnostic against exact DP ground truth.",
  "risks": [
    "A first harness can appear to make progress while only testing training loss; require exact DP value and policy calibration metrics.",
    "TRL-raw, TRL-log, and MC+TRL-log may be implemented inconsistently unless the result saves raw per-method metrics and coverage diagnostics.",
    "The risky shortcut can be under-specified; include both lucky and unlucky stochastic outcomes in offline coverage and evaluate risky action selection under exact DP.",
    "Avoid expanding to neural networks, OGBench, or long sweeps before the tabular diagnostic is reproducible."
  ]
}
```


## Stop, pivot, continue rules

- For iteration 0, a missing latest result is expected and is not by itself a reason to stop.
- After iteration 0, stop or choose needs_human on missing or invalid result files.
- Stop on repeated invalid, negative, or low-value results.
- Pivot only when evidence weakens the original idea but reveals a nearby testable idea.
- Continue only for one cheap, high-information experiment.
- Choose needs_human for ambiguity, expensive work, missing artifacts, or risky pivots.


## Next experiment id

Use `0002` as the exact `next_experiment.experiment_id` if you choose continue.
