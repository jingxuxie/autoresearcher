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
  "failure_streak": 0,
  "human_review_required": false,
  "iteration": 3,
  "last_decision": "continue",
  "last_failure": null,
  "last_pro_review_iteration": 0,
  "no_progress_rounds": 0,
  "notes": [],
  "primary_metric": null,
  "status": "active"
}
```


## Latest result JSON

```json
{
  "artifacts": [
    "research/sto_trl/artifacts/0003/run_horizon_holdout.py",
    "research/sto_trl/artifacts/0003/raw_metrics.json",
    "research/sto_trl/artifacts/0003/metrics.csv",
    "research/sto_trl/artifacts/0003/label_coverage_by_horizon.json",
    "research/sto_trl/artifacts/0003/offline_datasets.json",
    "research/sto_trl/artifacts/0003/transition_tables.json",
    "research/sto_trl/artifacts/0003/value_tables.json"
  ],
  "baseline_metrics": {
    "chain_len9": {
      "calibration_error": 0.4656078690468753,
      "chose_exact_optimal_action": true,
      "eval_goal": "c8",
      "eval_greedy_action": "right",
      "eval_start": "c0",
      "eval_start_exact_q": {
        "right": 0.43046721000000016
      },
      "eval_start_learned_q": {
        "right": 0.0
      },
      "exact_optimal_action": "right",
      "heldout_long_horizon_value_mse": 0.3917058232298766,
      "horizon_metrics": {
        "h1_train_visible": {
          "num_q_pairs": 16,
          "num_value_pairs": 16,
          "q_calibration_error": 0.0,
          "q_overestimation_error": 0.0,
          "q_underestimation_error": 0.0,
          "value_mse": 0.0,
          "value_overestimation_error": 0.0,
          "value_underestimation_error": 0.0
        },
        "h2_train_visible": {
          "num_q_pairs": 14,
          "num_value_pairs": 14,
          "q_calibration_error": 0.0,
          "q_overestimation_error": 0.0,
          "q_underestimation_error": 0.0,
          "value_mse": 0.0,
          "value_overestimation_error": 0.0,
          "value_underestimation_error": 0.0
        },
        "heldout_gt2": {
          "num_q_pairs": 98,
          "num_value_pairs": 42,
          "q_calibration_error": 0.6081408901836739,
          "q_overestimation_error": 0.0,
          "q_underestimation_error": 0.7290000000000001,
          "value_mse": 0.3917058232298766,
          "value_overestimation_error": 0.0,
          "value_underestimation_error": 0.7290000000000001
        }
      },
      "policy_regret": 0.0,
      "q_calibration_error": 0.4656078690468753,
      "q_overestimation_error": 0.0,
      "q_underestimation_error": 0.7290000000000001,
      "risky_action_selection_rate": 0.0,
      "value_mse": 0.22849506355076135,
      "value_overestimation_error": 0.0,
      "value_underestimation_error": 0.7290000000000001
    },
    "method": "mc_supervised",
    "risky_matched": {
      "calibration_error": 0.045562500000000006,
      "chose_exact_optimal_action": false,
      "eval_goal": "goal",
      "eval_greedy_action": "risky",
      "eval_start": "start",
      "eval_start_exact_q": {
        "risky": 0.225,
        "safe": 0.7290000000000001
      },
      "eval_start_learned_q": {
        "risky": 0.225,
        "safe": 0.0
      },
      "exact_optimal_action": "safe",
      "heldout_long_horizon_value_mse": 0.25401600000000013,
      "horizon_metrics": {
        "h1_train_visible": {
          "num_q_pairs": 5,
          "num_value_pairs": 4,
          "q_calibration_error": 0.0,
          "q_overestimation_error": 0.0,
          "q_underestimation_error": 0.0,
          "value_mse": 0.0,
          "value_overestimation_error": 0.0,
          "value_underestimation_error": 0.0
        },
        "h2_train_visible": {
          "num_q_pairs": 2,
          "num_value_pairs": 2,
          "q_calibration_error": 0.0,
          "q_overestimation_error": 0.0,
          "q_underestimation_error": 0.0,
          "value_mse": 0.0,
          "value_overestimation_error": 0.0,
          "value_underestimation_error": 0.0
        },
        "heldout_gt2": {
          "num_q_pairs": 1,
          "num_value_pairs": 1,
          "q_calibration_error": 0.7290000000000001,
          "q_overestimation_error": 0.0,
          "q_underestimation_error": 0.7290000000000001,
          "value_mse": 0.25401600000000013,
          "value_overestimation_error": 0.0,
          "value_underestimation_error": 0.5040000000000001
        },
        "unreachable": {
          "num_q_pairs": 8,
          "num_value_pairs": 13,
          "q_calibration_error": 0.0,
          "q_overestimation_error": 0.0,
          "q_underestimation_error": 0.0,
          "value_mse": 0.0,
          "value_overestimation_error": 0.0,
          "value_underestimation_error": 0.0
        }
      },
      "policy_regret": 0.5040000000000001,
      "q_calibration_error": 0.045562500000000006,
      "q_overestimation_error": 0.0,
      "q_underestimation_error": 0.7290000000000001,
      "risky_action_selection_rate": 1.0,
      "value_mse": 0.012700800000000007,
      "value_overestimation_error": 0.0,
      "value_underestimation_error": 0.5040000000000001
    }
  },
  "claim_tested": "Censoring long-horizon MC labels makes MC-only underpredict held-out discounted reachability, while log transitive backups recover longer horizons and keep matched risky-branch calibration.",
  "commands_run": [
    "mkdir -p research/sto_trl/artifacts/0003 research/sto_trl/results && cp research/sto_trl/artifacts/0002/run_coverage_stress.py research/sto_trl/artifacts/0003/run_horizon_holdout.py",
    "conda run -n autoresearcher_sto_trl python research/sto_trl/artifacts/0003/run_horizon_holdout.py",
    "conda run -n autoresearcher_sto_trl python scripts/validate_artifacts.py --repo-root . --json research/sto_trl/results/0003_result.json --schema schemas/result.schema.json --check-result-artifacts"
  ],
  "experiment_id": "0003",
  "interpretation": "With positive labels beyond horizon 2 censored, MC-supervised underpredicted held-out long-horizon reachability. TRL-log and MC+TRL-log propagated through observed transitions and reduced held-out value MSE on the longer chain and the matched risky MDP. In the matched risky MDP, TRL-log and MC+TRL-log selected the safe action, while raw TRL selected the risky shortcut from support alone.",
  "known_failures": [],
  "metrics": {
    "aggregate": {
      "chain_mc_heldout_value_mse": 0.3917058232298766,
      "chain_mc_plus_trl_log_heldout_value_mse": 2.9347503914472164e-34,
      "chain_trl_log_heldout_value_mse": 2.9347503914472164e-34,
      "risky_mc_heldout_value_mse": 0.25401600000000013,
      "risky_mc_plus_trl_log_heldout_value_mse": 0.0,
      "risky_mc_plus_trl_log_policy_regret": 0.0,
      "risky_trl_log_heldout_value_mse": 0.0,
      "risky_trl_log_policy_regret": 0.0,
      "risky_trl_raw_policy_regret": 0.5040000000000001
    },
    "experiment_id": "0003",
    "gamma": 0.9,
    "label_horizon_cutoff": 2,
    "scenarios": {
      "chain_len9": {
        "coverage_diagnostics": {
          "action_counts": {
            "left": 8,
            "right": 8
          },
          "num_episodes": 2,
          "num_transitions": 16,
          "outcome_counts": {
            "deterministic": 16
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
            ],
            [
              "c5",
              "right"
            ],
            [
              "c6",
              "left"
            ],
            [
              "c6",
              "right"
            ],
            [
              "c7",
              "left"
            ],
            [
              "c7",
              "right"
            ],
            [
              "c8",
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
            "c5",
            "c6",
            "c7",
            "c8"
          ]
        },
        "label_coverage_by_horizon": {
          "censored_examples": [
            {
              "action": "right",
              "episode_id": "chain_forward",
              "goal": "c3",
              "positive_horizon": 3,
              "state": "c0"
            },
            {
              "action": "right",
              "episode_id": "chain_forward",
              "goal": "c4",
              "positive_horizon": 4,
              "state": "c0"
            },
            {
              "action": "right",
              "episode_id": "chain_forward",
              "goal": "c5",
              "positive_horizon": 5,
              "state": "c0"
            },
            {
              "action": "right",
              "episode_id": "chain_forward",
              "goal": "c6",
              "positive_horizon": 6,
              "state": "c0"
            },
            {
              "action": "right",
              "episode_id": "chain_forward",
              "goal": "c7",
              "positive_horizon": 7,
              "state": "c0"
            },
            {
              "action": "right",
              "episode_id": "chain_forward",
              "goal": "c8",
              "positive_horizon": 8,
              "state": "c0"
            },
            {
              "action": "right",
              "episode_id": "chain_forward",
              "goal": "c4",
              "positive_horizon": 3,
              "state": "c1"
            },
            {
              "action": "right",
              "episode_id": "chain_forward",
              "goal": "c5",
              "positive_horizon": 4,
              "state": "c1"
            },
            {
              "action": "right",
              "episode_id": "chain_forward",
              "goal": "c6",
              "positive_horizon": 5,
              "state": "c1"
            },
            {
              "action": "right",
              "episode_id": "chain_forward",
              "goal": "c7",
              "positive_horizon": 6,
              "state": "c1"
            },
            {
              "action": "right",
              "episode_id": "chain_forward",
              "goal": "c8",
              "positive_horizon": 7,
              "state": "c1"
            },
            {
              "action": "right",
              "episode_id": "chain_forward",
              "goal": "c5",
              "positive_horizon": 3,
              "state": "c2"
            }
          ],
          "counts_by_bin": {
            "h1_train_visible": {
              "included_positive": 16
            },
            "h2_train_visible": {
              "included_positive": 14
            },
            "heldout_gt2": {
              "censored_positive": 42
            },
            "unreached_zero": {
              "included_zero": 72
            }
          },
          "eval_q_pairs_by_horizon_bin": {
            "h1_train_visible": 16,
            "h2_train_visible": 14,
            "heldout_gt2": 98
          },
          "eval_value_pairs_by_horizon_bin": {
            "h1_train_visible": 16,
            "h2_train_visible": 14,
            "heldout_gt2": 42
          },
          "label_horizon_cutoff": 2,
          "num_censored_positive_labels": 42,
          "num_included_positive_labels": 30,
          "num_included_zero_labels": 72,
          "unique_state_action_goal_pairs_by_bin": {
            "h1_train_visible": 16,
            "h2_train_visible": 14,
            "heldout_gt2": 42,
            "unreached_zero": 72
          }
        },
        "mdp": "deterministic_chain_len9",
        "methods": {
          "mc_plus_trl_log": {
            "calibration_error": 0.13125827819531247,
            "chose_exact_optimal_action": true,
            "eval_goal": "c8",
            "eval_greedy_action": "right",
            "eval_start": "c0",
            "eval_start_exact_q": {
              "right": 0.43046721000000016
            },
            "eval_start_learned_q": {
              "right": 0.43046721000000016
            },
            "exact_optimal_action": "right",
            "heldout_long_horizon_value_mse": 2.9347503914472164e-34,
            "horizon_metrics": {
              "h1_train_visible": {
                "num_q_pairs": 16,
                "num_value_pairs": 16,
                "q_calibration_error": 0.0,
                "q_overestimation_error": 0.0,
                "q_underestimation_error": 0.0,
                "value_mse": 0.0,
                "value_overestimation_error": 0.0,
                "value_underestimation_error": 0.0
              },
              "h2_train_visible": {
                "num_q_pairs": 14,
                "num_value_pairs": 14,
                "q_calibration_error": 0.0,
                "q_overestimation_error": 0.0,
                "q_underestimation_error": 0.0,
                "value_mse": 0.0,
                "value_overestimation_error": 0.0,
                "value_underestimation_error": 0.0
              },
              "heldout_gt2": {
                "num_q_pairs": 98,
                "num_value_pairs": 42,
                "q_calibration_error": 0.17143938376530607,
                "q_overestimation_error": 5.551115123125783e-17,
                "q_underestimation_error": 0.36450000000000005,
                "value_mse": 2.9347503914472164e-34,
                "value_overestimation_error": 5.551115123125783e-17,
                "value_underestimation_error": 0.0
              }
            },
            "policy_regret": 0.0,
            "q_calibration_error": 0.13125827819531247,
            "q_overestimation_error": 5.551115123125783e-17,
            "q_underestimation_error": 0.36450000000000005,
            "risky_action_selection_rate": 0.0,
            "value_mse": 1.7119377283442096e-34,
            "value_overestimation_error": 5.551115123125783e-17,
            "value_underestimation_error": 0.0
          },
          "mc_supervised": {
            "calibration_error": 0.4656078690468753,
            "chose_exact_optimal_action": true,
            "eval_goal": "c8",
            "eval_greedy_action": "right",
            "eval_start": "c0",
            "eval_start_exact_q": {
              "right": 0.43046721000000016
            },
            "eval_start_learned_q": {
              "right": 0.0
            },
            "exact_optimal_action": "right",
            "heldout_long_horizon_value_mse": 0.3917058232298766,
            "horizon_metrics": {
              "h1_train_visible": {
                "num_q_pairs": 16,
                "num_value_pairs": 16,
                "q_calibration_error": 0.0,
                "q_overestimation_error": 0.0,
                "q_underestimation_error": 0.0,
                "value_mse": 0.0,
                "value_overestimation_error": 0.0,
                "value_underestimation_error": 0.0
              },
              "h2_train_visible": {
                "num_q_pairs": 14,
                "num_value_pairs": 14,
                "q_calibration_error": 0.0,
                "q_overestimation_error": 0.0,
                "q_underestimation_error": 0.0,
                "value_mse": 0.0,
                "value_overestimation_error": 0.0,
                "value_underestimation_error": 0.0
              },
              "heldout_gt2": {
                "num_q_pairs": 98,
                "num_value_pairs": 42,
                "q_calibration_error": 0.6081408901836739,
                "q_overestimation_error": 0.0,
                "q_underestimation_error": 0.7290000000000001,
                "value_mse": 0.3917058232298766,
                "value_overestimation_error": 0.0,
                "value_underestimation_error": 0.7290000000000001
              }
            },
            "policy_regret": 0.0,
            "q_calibration_error": 0.4656078690468753,
            "q_overestimation_error": 0.0,
            "q_underestimation_error": 0.7290000000000001,
            "risky_action_selection_rate": 0.0,
            "value_mse": 0.22849506355076135,
            "value_overestimation_error": 0.0,
            "value_underestimation_error": 0.7290000000000001
          },
          "trl_log": {
            "calibration_error": 4.336808689942018e-18,
            "chose_exact_optimal_action": true,
            "eval_goal": "c8",
            "eval_greedy_action": "right",
            "eval_start": "c0",
            "eval_start_exact_q": {
              "right": 0.43046721000000016
            },
            "eval_start_learned_q": {
              "right": 0.43046721000000016
            },
            "exact_optimal_action": "right",
            "heldout_long_horizon_value_mse": 2.9347503914472164e-34,
            "horizon_metrics": {
              "h1_train_visible": {
                "num_q_pairs": 16,
                "num_value_pairs": 16,
                "q_calibration_error": 0.0,
                "q_overestimation_error": 0.0,
                "q_underestimation_error": 0.0,
                "value_mse": 0.0,
                "value_overestimation_error": 0.0,
                "value_underestimation_error": 0.0
              },
              "h2_train_visible": {
                "num_q_pairs": 14,
                "num_value_pairs": 14,
                "q_calibration_error": 0.0,
                "q_overestimation_error": 0.0,
                "q_underestimation_error": 0.0,
                "value_mse": 0.0,
                "value_overestimation_error": 0.0,
                "value_underestimation_error": 0.0
              },
              "heldout_gt2": {
                "num_q_pairs": 98,
                "num_value_pairs": 42,
                "q_calibration_error": 5.664403186863044e-18,
                "q_overestimation_error": 5.551115123125783e-17,
                "q_underestimation_error": 0.0,
                "value_mse": 2.9347503914472164e-34,
                "value_overestimation_error": 5.551115123125783e-17,
                "value_underestimation_error": 0.0
              }
            },
            "policy_regret": 0.0,
            "q_calibration_error": 4.336808689942018e-18,
            "q_overestimation_error": 5.551115123125783e-17,
            "q_underestimation_error": 0.0,
            "risky_action_selection_rate": 0.0,
            "value_mse": 1.7119377283442096e-34,
            "value_overestimation_error": 5.551115123125783e-17,
            "value_underestimation_error": 0.0
          },
          "trl_raw": {
            "calibration_error": 0.0,
            "chose_exact_optimal_action": true,
            "eval_goal": "c8",
            "eval_greedy_action": "right",
            "eval_start": "c0",
            "eval_start_exact_q": {
              "right": 0.43046721000000016
            },
            "eval_start_learned_q": {
              "right": 0.43046721000000016
            },
            "exact_optimal_action": "right",
            "heldout_long_horizon_value_mse": 0.0,
            "horizon_metrics": {
              "h1_train_visible": {
                "num_q_pairs": 16,
                "num_value_pairs": 16,
                "q_calibration_error": 0.0,
                "q_overestimation_error": 0.0,
                "q_underestimation_error": 0.0,
                "value_mse": 0.0,
                "value_overestimation_error": 0.0,
                "value_underestimation_error": 0.0
              },
              "h2_train_visible": {
                "num_q_pairs": 14,
                "num_value_pairs": 14,
                "q_calibration_error": 0.0,
                "q_overestimation_error": 0.0,
                "q_underestimation_error": 0.0,
                "value_mse": 0.0,
                "value_overestimation_error": 0.0,
                "value_underestimation_error": 0.0
              },
              "heldout_gt2": {
                "num_q_pairs": 98,
                "num_value_pairs": 42,
                "q_calibration_error": 0.0,
                "q_overestimation_error": 0.0,
                "q_underestimation_error": 0.0,
                "value_mse": 0.0,
                "value_overestimation_error": 0.0,
                "value_underestimation_error": 0.0
              }
            },
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
      "risky_matched": {
        "coverage_diagnostics": {
          "action_counts": {
            "forward": 8,
            "risky": 8,
            "safe": 4
          },
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
          ]
        },
        "label_coverage_by_horizon": {
          "censored_examples": [
            {
              "action": "safe",
              "episode_id": "safe_0",
              "goal": "goal",
              "positive_horizon": 3,
              "state": "start"
            },
            {
              "action": "safe",
              "episode_id": "safe_1",
              "goal": "goal",
              "positive_horizon": 3,
              "state": "start"
            },
            {
              "action": "safe",
              "episode_id": "safe_2",
              "goal": "goal",
              "positive_horizon": 3,
              "state": "start"
            },
            {
              "action": "safe",
              "episode_id": "safe_3",
              "goal": "goal",
              "positive_horizon": 3,
              "state": "start"
            }
          ],
          "counts_by_bin": {
            "h1_train_visible": {
              "included_positive": 20
            },
            "h2_train_visible": {
              "included_positive": 8
            },
            "heldout_gt2": {
              "censored_positive": 4
            },
            "unreached_zero": {
              "included_zero": 68
            }
          },
          "eval_q_pairs_by_horizon_bin": {
            "h1_train_visible": 5,
            "h2_train_visible": 2,
            "heldout_gt2": 1,
            "unreachable": 8
          },
          "eval_value_pairs_by_horizon_bin": {
            "h1_train_visible": 4,
            "h2_train_visible": 2,
            "heldout_gt2": 1,
            "unreachable": 13
          },
          "label_horizon_cutoff": 2,
          "num_censored_positive_labels": 4,
          "num_included_positive_labels": 28,
          "num_included_zero_labels": 68,
          "unique_state_action_goal_pairs_by_bin": {
            "h1_train_visible": 5,
            "h2_train_visible": 2,
            "heldout_gt2": 1,
            "unreached_zero": 14
          }
        },
        "mdp": "risky_shortcut_matched",
        "methods": {
          "mc_plus_trl_log": {
            "calibration_error": 0.0,
            "chose_exact_optimal_action": true,
            "eval_goal": "goal",
            "eval_greedy_action": "safe",
            "eval_start": "start",
            "eval_start_exact_q": {
              "risky": 0.225,
              "safe": 0.7290000000000001
            },
            "eval_start_learned_q": {
              "risky": 0.225,
              "safe": 0.7290000000000001
            },
            "exact_optimal_action": "safe",
            "heldout_long_horizon_value_mse": 0.0,
            "horizon_metrics": {
              "h1_train_visible": {
                "num_q_pairs": 5,
                "num_value_pairs": 4,
                "q_calibration_error": 0.0,
                "q_overestimation_error": 0.0,
                "q_underestimation_error": 0.0,
                "value_mse": 0.0,
                "value_overestimation_error": 0.0,
                "value_underestimation_error": 0.0
              },
              "h2_train_visible": {
                "num_q_pairs": 2,
                "num_value_pairs": 2,
                "q_calibration_error": 0.0,
                "q_overestimation_error": 0.0,
                "q_underestimation_error": 0.0,
                "value_mse": 0.0,
                "value_overestimation_error": 0.0,
                "value_underestimation_error": 0.0
              },
              "heldout_gt2": {
                "num_q_pairs": 1,
                "num_value_pairs": 1,
                "q_calibration_error": 0.0,
                "q_overestimation_error": 0.0,
                "q_underestimation_error": 0.0,
                "value_mse": 0.0,
                "value_overestimation_error": 0.0,
                "value_underestimation_error": 0.0
              },
              "unreachable": {
                "num_q_pairs": 8,
                "num_value_pairs": 13,
                "q_calibration_error": 0.0,
                "q_overestimation_error": 0.0,
                "q_underestimation_error": 0.0,
                "value_mse": 0.0,
                "value_overestimation_error": 0.0,
                "value_underestimation_error": 0.0
              }
            },
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
            "calibration_error": 0.045562500000000006,
            "chose_exact_optimal_action": false,
            "eval_goal": "goal",
            "eval_greedy_action": "risky",
            "eval_start": "start",
            "eval_start_exact_q": {
              "risky": 0.225,
              "safe": 0.7290000000000001
            },
            "eval_start_learned_q": {
              "risky": 0.225,
              "safe": 0.0
            },
            "exact_optimal_action": "safe",
            "heldout_long_horizon_value_mse": 0.25401600000000013,
            "horizon_metrics": {
              "h1_train_visible": {
                "num_q_pairs": 5,
                "num_value_pairs": 4,
                "q_calibration_error": 0.0,
                "q_overestimation_error": 0.0,
                "q_underestimation_error": 0.0,
                "value_mse": 0.0,
                "value_overestimation_error": 0.0,
                "value_underestimation_error": 0.0
              },
              "h2_train_visible": {
                "num_q_pairs": 2,
                "num_value_pairs": 2,
                "q_calibration_error": 0.0,
                "q_overestimation_error": 0.0,
                "q_underestimation_error": 0.0,
                "value_mse": 0.0,
                "value_overestimation_error": 0.0,
                "value_underestimation_error": 0.0
              },
              "heldout_gt2": {
                "num_q_pairs": 1,
                "num_value_pairs": 1,
                "q_calibration_error": 0.7290000000000001,
                "q_overestimation_error": 0.0,
                "q_underestimation_error": 0.7290000000000001,
                "value_mse": 0.25401600000000013,
                "value_overestimation_error": 0.0,
                "value_underestimation_error": 0.5040000000000001
              },
              "unreachable": {
                "num_q_pairs": 8,
                "num_value_pairs": 13,
                "q_calibration_error": 0.0,
                "q_overestimation_error": 0.0,
                "q_underestimation_error": 0.0,
                "value_mse": 0.0,
                "value_overestimation_error": 0.0,
                "value_underestimation_error": 0.0
              }
            },
            "policy_regret": 0.5040000000000001,
            "q_calibration_error": 0.045562500000000006,
            "q_overestimation_error": 0.0,
            "q_underestimation_error": 0.7290000000000001,
            "risky_action_selection_rate": 1.0,
            "value_mse": 0.012700800000000007,
            "value_overestimation_error": 0.0,
            "value_underestimation_error": 0.5040000000000001
          },
          "trl_log": {
            "calibration_error": 0.0,
            "chose_exact_optimal_action": true,
            "eval_goal": "goal",
            "eval_greedy_action": "safe",
            "eval_start": "start",
            "eval_start_exact_q": {
              "risky": 0.225,
              "safe": 0.7290000000000001
            },
            "eval_start_learned_q": {
              "risky": 0.225,
              "safe": 0.7290000000000001
            },
            "exact_optimal_action": "safe",
            "heldout_long_horizon_value_mse": 0.0,
            "horizon_metrics": {
              "h1_train_visible": {
                "num_q_pairs": 5,
                "num_value_pairs": 4,
                "q_calibration_error": 0.0,
                "q_overestimation_error": 0.0,
                "q_underestimation_error": 0.0,
                "value_mse": 0.0,
                "value_overestimation_error": 0.0,
                "value_underestimation_error": 0.0
              },
              "h2_train_visible": {
                "num_q_pairs": 2,
                "num_value_pairs": 2,
                "q_calibration_error": 0.0,
                "q_overestimation_error": 0.0,
                "q_underestimation_error": 0.0,
                "value_mse": 0.0,
                "value_overestimation_error": 0.0,
                "value_underestimation_error": 0.0
              },
              "heldout_gt2": {
                "num_q_pairs": 1,
                "num_value_pairs": 1,
                "q_calibration_error": 0.0,
                "q_overestimation_error": 0.0,
                "q_underestimation_error": 0.0,
                "value_mse": 0.0,
                "value_overestimation_error": 0.0,
                "value_underestimation_error": 0.0
              },
              "unreachable": {
                "num_q_pairs": 8,
                "num_value_pairs": 13,
                "q_calibration_error": 0.0,
                "q_overestimation_error": 0.0,
                "q_underestimation_error": 0.0,
                "value_mse": 0.0,
                "value_overestimation_error": 0.0,
                "value_underestimation_error": 0.0
              }
            },
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
            "chose_exact_optimal_action": false,
            "eval_goal": "goal",
            "eval_greedy_action": "risky",
            "eval_start": "start",
            "eval_start_exact_q": {
              "risky": 0.225,
              "safe": 0.7290000000000001
            },
            "eval_start_learned_q": {
              "risky": 0.9,
              "safe": 0.7290000000000001
            },
            "exact_optimal_action": "safe",
            "heldout_long_horizon_value_mse": 0.029240999999999975,
            "horizon_metrics": {
              "h1_train_visible": {
                "num_q_pairs": 5,
                "num_value_pairs": 4,
                "q_calibration_error": 0.18,
                "q_overestimation_error": 0.675,
                "q_underestimation_error": 0.0,
                "value_mse": 0.012656249999999997,
                "value_overestimation_error": 0.22499999999999998,
                "value_underestimation_error": 0.0
              },
              "h2_train_visible": {
                "num_q_pairs": 2,
                "num_value_pairs": 2,
                "q_calibration_error": 0.0,
                "q_overestimation_error": 0.0,
                "q_underestimation_error": 0.0,
                "value_mse": 0.0,
                "value_overestimation_error": 0.0,
                "value_underestimation_error": 0.0
              },
              "heldout_gt2": {
                "num_q_pairs": 1,
                "num_value_pairs": 1,
                "q_calibration_error": 0.0,
                "q_overestimation_error": 0.0,
                "q_underestimation_error": 0.0,
                "value_mse": 0.029240999999999975,
                "value_overestimation_error": 0.17099999999999993,
                "value_underestimation_error": 0.0
              },
              "unreachable": {
                "num_q_pairs": 8,
                "num_value_pairs": 13,
                "q_calibration_error": 0.0,
                "q_overestimation_error": 0.0,
                "q_underestimation_error": 0.0,
                "value_mse": 0.0,
                "value_overestimation_error": 0.0,
                "value_underestimation_error": 0.0
              }
            },
            "policy_regret": 0.5040000000000001,
            "q_calibration_error": 0.05625,
            "q_overestimation_error": 0.675,
            "q_underestimation_error": 0.0,
            "risky_action_selection_rate": 1.0,
            "value_mse": 0.003993299999999998,
            "value_overestimation_error": 0.22499999999999998,
            "value_underestimation_error": 0.0
          }
        }
      }
    },
    "success_checks": {
      "chain_raw_exact_under_censoring": true,
      "chain_trl_log_exact_under_censoring": true,
      "heldout_mse_improved_vs_mc_on_chain_and_risky": true,
      "matched_risky_mc_plus_trl_log_selects_safe": true,
      "matched_risky_trl_log_selects_safe": true,
      "matched_risky_trl_raw_selects_wrong_risky": true,
      "mc_plus_improves_chain_heldout_mse_vs_mc": true,
      "success_criteria_met": true
    },
    "update_steps": 32
  },
  "next_questions": [
    "How sensitive is the held-out recovery to the MC anchor weight in MC+TRL-log?",
    "What horizon cutoff is the smallest one that still allows stable long-horizon propagation?",
    "Can uncertainty penalties preserve risky calibration under matched coverage while avoiding raw support optimism?"
  ],
  "status": "completed"
}
```


## Latest summary

# Experiment 0003 Summary

## Objective

Test whether transitive log backups recover held-out long-horizon discounted reachability when MC labels are censored beyond horizon `2`.

## Commands Run

```bash
mkdir -p research/sto_trl/artifacts/0003 research/sto_trl/results && cp research/sto_trl/artifacts/0002/run_coverage_stress.py research/sto_trl/artifacts/0003/run_horizon_holdout.py
conda run -n autoresearcher_sto_trl python research/sto_trl/artifacts/0003/run_horizon_holdout.py
conda run -n autoresearcher_sto_trl python scripts/validate_artifacts.py --repo-root . --json research/sto_trl/results/0003_result.json --schema schemas/result.schema.json --check-result-artifacts
```

## Setup

- Discount: `0.9`
- Fixed backup iterations: `32`
- Label cutoff: positive MC labels with horizon `>2` are censored.
- MDPs: deterministic chain length 9 and matched-coverage risky shortcut with risky success/failure counts `2/6`.

## Key Metrics

| Scenario | Method | Held-out value MSE | Policy regret | Chosen action | Risky selected |
| --- | --- | ---: | ---: | --- | ---: |
| chain_len9 | mc_supervised | 0.391705823230 | 0.000000000000 | right | 0.0 |
| chain_len9 | trl_raw | 0.000000000000 | 0.000000000000 | right | 0.0 |
| chain_len9 | trl_log | 0.000000000000 | 0.000000000000 | right | 0.0 |
| chain_len9 | mc_plus_trl_log | 0.000000000000 | 0.000000000000 | right | 0.0 |
| risky_matched | mc_supervised | 0.254016000000 | 0.504000000000 | risky | 1.0 |
| risky_matched | trl_raw | 0.029241000000 | 0.504000000000 | risky | 1.0 |
| risky_matched | trl_log | 0.000000000000 | 0.000000000000 | safe | 0.0 |
| risky_matched | mc_plus_trl_log | 0.000000000000 | 0.000000000000 | safe | 0.0 |

## Success Checks

- Chain raw exact under censoring: `True`
- Chain TRL-log exact under censoring: `True`
- MC+TRL-log improves chain held-out MSE vs MC: `True`
- Held-out MSE improves vs MC on chain and risky: `True`
- Matched risky TRL-log selects safe: `True`
- Matched risky MC+TRL-log selects safe: `True`
- Matched risky raw TRL selects wrong risky: `True`

## Interpretation

With positive labels beyond horizon 2 censored, MC-supervised underpredicted held-out long-horizon reachability. TRL-log and MC+TRL-log propagated through observed transitions and reduced held-out value MSE on the longer chain and the matched risky MDP. In the matched risky MDP, TRL-log and MC+TRL-log selected the safe action, while raw TRL selected the risky shortcut from support alone.

## Artifacts

- `research/sto_trl/artifacts/0003/run_horizon_holdout.py`
- `research/sto_trl/artifacts/0003/raw_metrics.json`
- `research/sto_trl/artifacts/0003/metrics.csv`
- `research/sto_trl/artifacts/0003/label_coverage_by_horizon.json`
- `research/sto_trl/artifacts/0003/offline_datasets.json`
- `research/sto_trl/artifacts/0003/transition_tables.json`
- `research/sto_trl/artifacts/0003/value_tables.json`

## Known Failures

- None.


## Latest review JSON

```json
{
  "allows_auto_continue": true,
  "evidence_checked": [
    "research/sto_trl/results/0003_result.json",
    "research/sto_trl/results/0003_summary.md",
    "research/sto_trl/artifacts/0003/run_horizon_holdout.py",
    "research/sto_trl/artifacts/0003/raw_metrics.json",
    "research/sto_trl/artifacts/0003/metrics.csv",
    "research/sto_trl/artifacts/0003/label_coverage_by_horizon.json",
    "research/sto_trl/artifacts/0003/offline_datasets.json",
    "research/sto_trl/artifacts/0003/transition_tables.json",
    "research/sto_trl/artifacts/0003/value_tables.json",
    "research/sto_trl/plans/0003_plan.json",
    "research/sto_trl/packets/0003_executor_packet.md",
    "research/sto_trl/env_state.json",
    "python scripts/validate_artifacts.py --repo-root . --json research/sto_trl/results/0003_result.json --schema schemas/result.schema.json --check-result-artifacts",
    "git status --short"
  ],
  "experiment_id": "0003",
  "reasons": [
    "Required outputs are present: research/sto_trl/results/0003_result.json, research/sto_trl/results/0003_summary.md, and populated artifacts under research/sto_trl/artifacts/0003.",
    "Result JSON validates against schemas/result.schema.json with artifact checks.",
    "The harness includes exact DP ground truth for both evaluated MDPs: deterministic_chain_len9 and risky_shortcut_matched.",
    "MC targets and MC+TRL-log anchors use censored_mc_labels, which excludes positive labels with horizon greater than the cutoff of 2; TRL methods use observed transition counts rather than DP labels.",
    "The four methods are compared on the same constructed trajectories, and metrics.csv/raw_metrics.json report per-method horizon-bin metrics plus policy regret, calibration, risky selection, and coverage diagnostics.",
    "The matched risky dataset has controlled branch coverage with 2 risky successes and 6 failures, and TRL-log/MC+TRL-log select safe while raw TRL selects risky.",
    "The interpretation is mostly bounded and consistent with the saved metrics: MC underpredicts held-out long horizons, log backups recover in this tabular setting, and raw TRL remains support-optimistic on the risky shortcut."
  ],
  "required_fixes": [],
  "risk_flags": [
    "git status shows modified control files including scripts/autoresearcher.py, autoresearcher.yaml, tests/test_phase1.py, and research/sto_trl/state.json. Their mtimes precede the 0003 plan, so they appear pre-existing to this executor run, but this means the no-control-script-edit criterion cannot be proven from artifacts alone.",
    "commands_run records setup, execution, and validation commands, but not the manual edit operation that adapted the copied 0002 script into the 0003 harness.",
    "TRL-log and raw TRL are transitive model-based tabular backups over observed transitions, so they do not consume the same supervised label budget as MC-only; this is intended by the plan but should be kept in mind when interpreting fairness."
  ],
  "verdict": "weak_pass"
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

## 0002_decision.json

```json
{
  "confidence": 0.86,
  "decision": "continue",
  "evidence": [
    "Artifact validation for research/sto_trl/results/0001_result.json completed successfully against schemas/result.schema.json with artifact checks.",
    "The 0001 result reports deterministic-chain sanity passed for trl_raw and trl_log with zero value error and zero policy regret.",
    "On risky_shortcut, trl_raw learned risky Q=0.9 versus exact risky Q=0.225, selected risky, and incurred policy_regret=0.504.",
    "On the same risky_shortcut dataset, trl_log, mc_supervised, and mc_plus_trl_log were perfect because the offline risky outcomes exactly matched the true 2/8 success rate.",
    "The 0001 code shows train_trl_raw maximizes over observed next states while train_trl_log uses empirical transition counts, making coverage imbalance the obvious next confound to test."
  ],
  "next_experiment": {
    "estimated_runtime_minutes": 20,
    "experiment_id": "0002",
    "failure_criteria": [
      "Training methods use true transition probabilities or exact DP labels beyond evaluation.",
      "The experiment only repeats the matched 2/6 risky outcome setting from 0001.",
      "No risk-optimal configuration is included, making conservatism impossible to diagnose.",
      "The result reports only aggregate prose or training loss instead of raw numeric metrics by method, MDP setting, and coverage regime.",
      "The run expands to neural networks, OGBench, large sweeps, downloads, or runtime over 30 minutes."
    ],
    "hypothesis": "Raw TRL overestimation is support-driven and will select risky whenever a lucky risky transition is observed, while empirical TRL-log and MC variants will be calibrated only when observed risky success/failure frequencies approximate the true stochastic branch; adding a risk-optimal setting will detect whether apparent improvements are merely conservative avoidance.",
    "objective": "Run a small tabular coverage-sensitivity stress test for the risky shortcut diagnostic, including both risk-suboptimal and risk-optimal settings, to check whether raw TRL overestimation and log/MC calibration claims survive biased or sparse stochastic outcome coverage.",
    "required_outputs": [
      "research/sto_trl/artifacts/0002/run_tabular_coverage_stress.py",
      "research/sto_trl/artifacts/0002/raw_metrics.json",
      "research/sto_trl/artifacts/0002/metrics.csv",
      "research/sto_trl/artifacts/0002/dataset_specs.json",
      "research/sto_trl/results/0002_result.json",
      "research/sto_trl/results/0002_summary.md"
    ],
    "success_criteria": [
      "Reuses or copies the 0001 tabular harness into research/sto_trl/artifacts/0002/ without editing prior results or control scripts.",
      "Evaluates exact DP ground truth for deterministic chain plus two risky-shortcut configurations: one where safe is optimal and one where risky is optimal.",
      "Runs a tiny predeclared set of offline risky coverage regimes, such as matched, lucky-biased, lucky-only, unlucky-biased, and no-risky-success, with fixed deterministic seeds or explicit constructed counts.",
      "Compares the same methods as 0001: mc_supervised, trl_raw, trl_log, and mc_plus_trl_log, using exact DP only for evaluation.",
      "Saves raw per-regime metrics including overestimation error, underestimation error, long-horizon value MSE, policy regret, risky action selection rate, calibration error, and coverage diagnostics.",
      "Produces valid research/sto_trl/results/0002_result.json and research/sto_trl/results/0002_summary.md with exact commands run."
    ],
    "tasks_for_codex": [
      "Create research/sto_trl/artifacts/0002/ and a self-contained coverage stress script, preferably by adapting the 0001 prototype.",
      "Keep the deterministic chain sanity check as a regression guard.",
      "Define two risky-shortcut MDP configurations with exact DP: safe-optimal and risky-optimal.",
      "Construct a tiny set of offline datasets with explicit risky success/failure counts for each coverage regime and save their specifications.",
      "Run mc_supervised, trl_raw, trl_log, and mc_plus_trl_log on each MDP/configuration/regime combination.",
      "Write raw_metrics.json, metrics.csv, coverage_diagnostics.json or equivalent structured artifacts under research/sto_trl/artifacts/0002/.",
      "Validate research/sto_trl/results/0002_result.json against schemas/result.schema.json with artifact checks."
    ]
  },
  "progress_score": 3,
  "rationale": "Experiment 0001 is valid and tests the main early hypothesis, but it is still a matched-coverage toy case: the risky dataset used 2 successes and 6 failures, exactly matching the true 0.25 risky success probability. The next high-information step is a small tabular coverage-sensitivity stress test to determine whether the raw-TRL failure is robust and whether empirical log/MC methods only look good when observed stochastic outcomes match ground truth.",
  "risks": [
    "A larger sweep could become activity without insight; keep the grid tiny and predeclared.",
    "Empirical log-space backups may fail under lucky-only or biased coverage, which would be a useful boundary rather than a reason to hide the result.",
    "Do not introduce oracle access to true transition probabilities in training methods; exact DP should remain evaluation-only ground truth.",
    "A method that avoids all risky actions is not enough; the next test must include a configuration where the risky action is truly optimal."
  ]
}
```

## 0003_decision.json

```json
{
  "confidence": 0.84,
  "decision": "continue",
  "evidence": [
    "research/sto_trl/results/0002_result.json validates against schemas/result.schema.json with artifact checks.",
    "0002 success checks report deterministic chain raw/log recovery, all predeclared risky regimes present, raw_policy_is_support_driven=true, and trl_log_is_optimal_on_matched_regimes=true.",
    "0002 aggregate metrics show raw TRL selected risky in 8/8 scenarios with observed risky success and 0/2 scenarios with no observed success, confirming the support-driven failure mode.",
    "0002 shows empirical MC/log methods are only calibrated in matched regimes: they choose risky incorrectly in safe_optimal__lucky_only and choose safe incorrectly in risk_optimal__unlucky_biased and risk_optimal__no_risky_success.",
    "The charter still requires evidence that log or MC+TRL-log improves long-horizon estimates over MC-only without breaking deterministic sanity checks before moving beyond tabular diagnostics."
  ],
  "next_experiment": {
    "estimated_runtime_minutes": 20,
    "experiment_id": "0003",
    "failure_criteria": [
      "Long-horizon labels are accidentally used in MC supervised targets or calibration anchors.",
      "The experiment lacks exact DP ground truth for every evaluated MDP.",
      "The result reports aggregate metrics without horizon-bin breakdown or train/eval coverage diagnostics.",
      "TRL-log or MC+TRL-log fails the deterministic chain sanity check under the censored-label setup.",
      "The stochastic risky evaluation uses biased coverage only, making calibration failures ambiguous rather than controlled.",
      "The run expands to neural networks, OGBench, large sweeps, downloads, or exceeds 30 minutes."
    ],
    "hypothesis": "With only short-horizon MC labels, MC-supervised estimates will underpredict held-out long-horizon goals, while log-space transitive backups, especially MC+TRL-log, will propagate calibrated short-horizon information to longer horizons without raw TRL's stochastic risky-path optimism under matched branch coverage.",
    "objective": "Run a small tabular horizon-holdout experiment that censors long-horizon goal labels during training and tests whether TRL-log or MC+TRL-log can recover long-horizon discounted reachability better than MC-only while retaining matched stochastic risky-branch calibration.",
    "required_outputs": [
      "research/sto_trl/artifacts/0003/run_horizon_holdout.py",
      "research/sto_trl/artifacts/0003/raw_metrics.json",
      "research/sto_trl/artifacts/0003/metrics.csv",
      "research/sto_trl/artifacts/0003/label_coverage_by_horizon.json",
      "research/sto_trl/artifacts/0003/offline_datasets.json",
      "research/sto_trl/results/0003_result.json",
      "research/sto_trl/results/0003_summary.md"
    ],
    "success_criteria": [
      "Creates a self-contained prototype under research/sto_trl/artifacts/0003/ without editing prior experiment artifacts, schemas, AGENTS.md, or scripts/autoresearcher.py.",
      "Includes a deterministic chain longer than 0001 plus at least one matched-coverage risky-shortcut MDP with exact DP ground truth.",
      "Explicitly censors MC/calibration training labels beyond a small horizon cutoff, such as 2 or 3 steps, and saves train/eval state-action-goal pair coverage by horizon bin.",
      "Compares mc_supervised, trl_raw, trl_log, and mc_plus_trl_log using the same trajectories and the same censored label budget.",
      "Reports raw metrics by method and horizon bin, including held-out long-horizon value MSE, overestimation, underestimation, calibration error, policy regret, risky action selection rate, and coverage diagnostics.",
      "Counts the experiment as positive only if trl_log or mc_plus_trl_log improves held-out long-horizon value MSE versus MC-only while raw/log deterministic chain sanity remains valid and matched risky calibration does not select the wrong risky action.",
      "Produces valid research/sto_trl/results/0003_result.json and research/sto_trl/results/0003_summary.md with exact commands run."
    ],
    "tasks_for_codex": [
      "Create research/sto_trl/artifacts/0003/ and adapt the 0002 harness into a horizon-holdout script.",
      "Implement a longer deterministic chain and a matched-coverage risky-shortcut scenario with exact discounted-reachability DP evaluation.",
      "Add a predeclared horizon cutoff for training labels, while still allowing transitive/log backups to use observed short transitions from trajectories.",
      "Run mc_supervised, trl_raw, trl_log, and mc_plus_trl_log on the censored-label datasets with fixed update counts and deterministic seeds or constructed trajectories.",
      "Save raw_metrics.json, metrics.csv, label_coverage_by_horizon.json, offline_datasets.json, transition_tables.json, and value_tables.json under research/sto_trl/artifacts/0003/.",
      "Write research/sto_trl/results/0003_result.json and research/sto_trl/results/0003_summary.md, then validate the result JSON against schemas/result.schema.json with artifact checks."
    ]
  },
  "progress_score": 5,
  "rationale": "Experiment 0002 is valid and informative: it confirms raw TRL's support-driven stochastic overestimation, and it also weakens the simpler empirical MC/log story by showing those methods depend heavily on branch coverage and can be overoptimistic or too conservative. The next cheap decisive test should isolate the other core claim: whether TRL-style log transitive backups actually improve long-horizon generalization over MC calibration when long-horizon labels are withheld, while preserving the stochastic branch behavior under matched coverage.",
  "risks": [
    "Do not treat 0002 as proving stochastic calibration; it shows empirical log/MC calibration is coverage-dependent.",
    "A horizon-holdout test can leak labels if the script computes MC targets from all future states; it must explicitly censor long-horizon training labels and save train/eval pair coverage.",
    "If the next experiment only repeats matched risky coverage without long-horizon label withholding, it will not test the remaining TRL horizon-generalization claim.",
    "Exact DP must remain evaluation-only ground truth, not a training target."
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

Use `0004` as the exact `next_experiment.experiment_id` if you choose continue.
