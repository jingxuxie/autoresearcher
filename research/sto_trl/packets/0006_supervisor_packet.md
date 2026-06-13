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
  "iteration": 5,
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
    "research/sto_trl/artifacts/0005/run_lambda_equivalence_audit.py",
    "research/sto_trl/artifacts/0005/raw_metrics.json",
    "research/sto_trl/artifacts/0005/metrics.csv",
    "research/sto_trl/artifacts/0005/lambda_sweep.json",
    "research/sto_trl/artifacts/0005/equivalence_diagnostics.json",
    "research/sto_trl/artifacts/0005/successor_distance_tables.json",
    "research/sto_trl/artifacts/0005/distance_diagnostics.json",
    "research/sto_trl/artifacts/0005/label_or_pair_coverage.json",
    "research/sto_trl/artifacts/0005/offline_datasets.json",
    "research/sto_trl/artifacts/0005/transition_tables.json",
    "research/sto_trl/artifacts/0005/value_tables.json"
  ],
  "baseline_metrics": {
    "main_mean_heldout_long_horizon_value_mse": 0.21524060774329223,
    "main_rows": [
      {
        "chose_exact_optimal_action": true,
        "eval_greedy_action": "right",
        "exact_optimal_action": "right",
        "exact_risky_q": null,
        "exact_safe_q": null,
        "heldout_long_horizon_value_mse": 0.3917058232298766,
        "lambda_tr": 0.0,
        "learned_risky_q": null,
        "learned_safe_q": null,
        "mdp": "deterministic_chain_len9",
        "method": "successor_calibration_only",
        "policy_regret": 0.0,
        "q_calibration_error": 0.4656078690468753,
        "q_overestimation_error": 0.0,
        "q_underestimation_error": 0.7290000000000001,
        "risky_action_selection_rate": 0.0,
        "risky_failure_count": 0,
        "risky_success_count": 0,
        "risky_success_rate_observed": null,
        "scenario_id": "chain_len9_holdout",
        "scenario_role": "main_holdout",
        "triangle_violation_count": 12,
        "triangle_violation_rate": 0.16666666666666666,
        "value_mse": 0.22849506355076135,
        "value_overestimation_error": 0.0,
        "value_underestimation_error": 0.7290000000000001
      },
      {
        "chose_exact_optimal_action": false,
        "eval_greedy_action": "risky",
        "exact_optimal_action": "safe",
        "exact_risky_q": 0.225,
        "exact_safe_q": 0.7290000000000001,
        "heldout_long_horizon_value_mse": 0.25401600000000013,
        "lambda_tr": 0.0,
        "learned_risky_q": 0.225,
        "learned_safe_q": 0.0,
        "mdp": "safe_optimal_matched",
        "method": "successor_calibration_only",
        "policy_regret": 0.5040000000000001,
        "q_calibration_error": 0.045562500000000006,
        "q_overestimation_error": 0.0,
        "q_underestimation_error": 0.7290000000000001,
        "risky_action_selection_rate": 1.0,
        "risky_failure_count": 6,
        "risky_success_count": 2,
        "risky_success_rate_observed": 0.25,
        "scenario_id": "safe_optimal_matched",
        "scenario_role": "main_matched",
        "triangle_violation_count": 3,
        "triangle_violation_rate": 0.375,
        "value_mse": 0.012700800000000007,
        "value_overestimation_error": 0.0,
        "value_underestimation_error": 0.5040000000000001
      },
      {
        "chose_exact_optimal_action": true,
        "eval_greedy_action": "risky",
        "exact_optimal_action": "risky",
        "exact_risky_q": 0.81,
        "exact_safe_q": 0.7290000000000001,
        "heldout_long_horizon_value_mse": 0.0,
        "lambda_tr": 0.0,
        "learned_risky_q": 0.8100000000000002,
        "learned_safe_q": 0.0,
        "mdp": "risk_optimal_matched",
        "method": "successor_calibration_only",
        "policy_regret": 0.0,
        "q_calibration_error": 0.04556250000000001,
        "q_overestimation_error": 1.1102230246251565e-16,
        "q_underestimation_error": 0.7290000000000001,
        "risky_action_selection_rate": 1.0,
        "risky_failure_count": 1,
        "risky_success_count": 9,
        "risky_success_rate_observed": 0.9,
        "scenario_id": "risk_optimal_matched",
        "scenario_role": "main_matched",
        "triangle_violation_count": 2,
        "triangle_violation_rate": 0.25,
        "value_mse": 6.2592723192585165e-34,
        "value_overestimation_error": 1.1102230246251565e-16,
        "value_underestimation_error": 0.0
      }
    ],
    "method": "successor_calibration_only"
  },
  "claim_tested": "A successor-distance lambda sweep can reveal whether successor_distance_trl_log has a distinct effect beyond trl_log while retaining calibration and lower held-out error than calibration-only.",
  "commands_run": [
    "mkdir -p research/sto_trl/artifacts/0005 research/sto_trl/results && cp research/sto_trl/artifacts/0004/run_successor_distance.py research/sto_trl/artifacts/0005/run_lambda_equivalence_audit.py",
    "conda run -n autoresearcher_sto_trl python research/sto_trl/artifacts/0005/run_lambda_equivalence_audit.py",
    "conda run -n autoresearcher_sto_trl python scripts/validate_artifacts.py --repo-root . --json research/sto_trl/results/0005_result.json --schema schemas/result.schema.json --check-result-artifacts"
  ],
  "experiment_id": "0005",
  "interpretation": "The audit found negative successor-distance evidence: improving lambdas reduced held-out error by matching trl_log within the predeclared tolerance, so this variant is not yet distinct from trl_log on these tabular diagnostics.",
  "known_failures": [],
  "metrics": {
    "aggregate": {
      "all_improving_lambdas_equivalent_to_trl_log": true,
      "any_positive_successor_evidence": false,
      "lambda_summaries": {
        "successor_distance_trl_log_lambda_0_00": {
          "equivalent_to_trl_log_all_main": false,
          "improves_vs_calibration_only": false,
          "lambda_tr": 0.0,
          "main_mean_heldout_mse": 0.21524060774329223,
          "matched_no_policy_regret_increase_vs_calibration_only": true,
          "matched_no_q_overestimation_increase_vs_calibration_only": true,
          "non_equivalent_to_trl_log_any_main": true,
          "positive_successor_evidence": false,
          "risk_optimal_selects_risky": true
        },
        "successor_distance_trl_log_lambda_0_25": {
          "equivalent_to_trl_log_all_main": true,
          "improves_vs_calibration_only": true,
          "lambda_tr": 0.25,
          "main_mean_heldout_mse": 9.782501304824055e-35,
          "matched_no_policy_regret_increase_vs_calibration_only": true,
          "matched_no_q_overestimation_increase_vs_calibration_only": true,
          "non_equivalent_to_trl_log_any_main": false,
          "positive_successor_evidence": false,
          "risk_optimal_selects_risky": true
        },
        "successor_distance_trl_log_lambda_0_50": {
          "equivalent_to_trl_log_all_main": true,
          "improves_vs_calibration_only": true,
          "lambda_tr": 0.5,
          "main_mean_heldout_mse": 9.782501304824055e-35,
          "matched_no_policy_regret_increase_vs_calibration_only": true,
          "matched_no_q_overestimation_increase_vs_calibration_only": true,
          "non_equivalent_to_trl_log_any_main": false,
          "positive_successor_evidence": false,
          "risk_optimal_selects_risky": true
        },
        "successor_distance_trl_log_lambda_0_75": {
          "equivalent_to_trl_log_all_main": true,
          "improves_vs_calibration_only": true,
          "lambda_tr": 0.75,
          "main_mean_heldout_mse": 9.782501304824055e-35,
          "matched_no_policy_regret_increase_vs_calibration_only": true,
          "matched_no_q_overestimation_increase_vs_calibration_only": true,
          "non_equivalent_to_trl_log_any_main": false,
          "positive_successor_evidence": false,
          "risk_optimal_selects_risky": true
        },
        "successor_distance_trl_log_lambda_1_00": {
          "equivalent_to_trl_log_all_main": true,
          "improves_vs_calibration_only": true,
          "lambda_tr": 1.0,
          "main_mean_heldout_mse": 9.782501304824055e-35,
          "matched_no_policy_regret_increase_vs_calibration_only": true,
          "matched_no_q_overestimation_increase_vs_calibration_only": true,
          "non_equivalent_to_trl_log_any_main": false,
          "positive_successor_evidence": false,
          "risk_optimal_selects_risky": true
        }
      },
      "negative_equivalence_evidence": true,
      "successor_calibration_only_main_mean_heldout_mse": 0.21524060774329223
    },
    "equivalence_tolerance": 1e-10,
    "experiment_id": "0005",
    "gamma": 0.9,
    "label_horizon_cutoff": 2,
    "lambda_sweep": [
      0.0,
      0.25,
      0.5,
      0.75,
      1.0
    ],
    "scenarios": {
      "chain_len9_holdout": {
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
        "equivalence_diagnostics": {
          "successor_distance_trl_log_lambda_0_00": {
            "lambda_tr": 0.0,
            "versus_successor_calibration_only": {
              "action_diff_rate": 0.0,
              "equivalence_tolerance": 1e-10,
              "heldout_mse_delta": 0.0,
              "is_equivalent": true,
              "max_abs_q_diff": 0.0,
              "max_abs_value_diff": 0.0,
              "policy_regret_delta": 0.0,
              "q_overestimation_delta": 0.0
            },
            "versus_trl_log": {
              "action_diff_rate": 0.20833333333333334,
              "equivalence_tolerance": 1e-10,
              "heldout_mse_delta": 0.3917058232298766,
              "is_equivalent": false,
              "max_abs_q_diff": 1.0,
              "max_abs_value_diff": 0.7290000000000001,
              "policy_regret_delta": 0.0,
              "q_overestimation_delta": -5.551115123125783e-17
            }
          },
          "successor_distance_trl_log_lambda_0_25": {
            "lambda_tr": 0.25,
            "versus_successor_calibration_only": {
              "action_diff_rate": 0.20833333333333334,
              "equivalence_tolerance": 1e-10,
              "heldout_mse_delta": -0.3917058232298766,
              "is_equivalent": false,
              "max_abs_q_diff": 1.0,
              "max_abs_value_diff": 0.7290000000000001,
              "policy_regret_delta": 0.0,
              "q_overestimation_delta": 5.551115123125783e-17
            },
            "versus_trl_log": {
              "action_diff_rate": 0.0,
              "equivalence_tolerance": 1e-10,
              "heldout_mse_delta": 0.0,
              "is_equivalent": true,
              "max_abs_q_diff": 0.0,
              "max_abs_value_diff": 0.0,
              "policy_regret_delta": 0.0,
              "q_overestimation_delta": 0.0
            }
          },
          "successor_distance_trl_log_lambda_0_50": {
            "lambda_tr": 0.5,
            "versus_successor_calibration_only": {
              "action_diff_rate": 0.20833333333333334,
              "equivalence_tolerance": 1e-10,
              "heldout_mse_delta": -0.3917058232298766,
              "is_equivalent": false,
              "max_abs_q_diff": 1.0,
              "max_abs_value_diff": 0.7290000000000001,
              "policy_regret_delta": 0.0,
              "q_overestimation_delta": 5.551115123125783e-17
            },
            "versus_trl_log": {
              "action_diff_rate": 0.0,
              "equivalence_tolerance": 1e-10,
              "heldout_mse_delta": 0.0,
              "is_equivalent": true,
              "max_abs_q_diff": 0.0,
              "max_abs_value_diff": 0.0,
              "policy_regret_delta": 0.0,
              "q_overestimation_delta": 0.0
            }
          },
          "successor_distance_trl_log_lambda_0_75": {
            "lambda_tr": 0.75,
            "versus_successor_calibration_only": {
              "action_diff_rate": 0.20833333333333334,
              "equivalence_tolerance": 1e-10,
              "heldout_mse_delta": -0.3917058232298766,
              "is_equivalent": false,
              "max_abs_q_diff": 1.0,
              "max_abs_value_diff": 0.7290000000000001,
              "policy_regret_delta": 0.0,
              "q_overestimation_delta": 5.551115123125783e-17
            },
            "versus_trl_log": {
              "action_diff_rate": 0.0,
              "equivalence_tolerance": 1e-10,
              "heldout_mse_delta": 0.0,
              "is_equivalent": true,
              "max_abs_q_diff": 0.0,
              "max_abs_value_diff": 0.0,
              "policy_regret_delta": 0.0,
              "q_overestimation_delta": 0.0
            }
          },
          "successor_distance_trl_log_lambda_1_00": {
            "lambda_tr": 1.0,
            "versus_successor_calibration_only": {
              "action_diff_rate": 0.20833333333333334,
              "equivalence_tolerance": 1e-10,
              "heldout_mse_delta": -0.3917058232298766,
              "is_equivalent": false,
              "max_abs_q_diff": 1.0,
              "max_abs_value_diff": 0.7290000000000001,
              "policy_regret_delta": 0.0,
              "q_overestimation_delta": 5.551115123125783e-17
            },
            "versus_trl_log": {
              "action_diff_rate": 0.0,
              "equivalence_tolerance": 1e-10,
              "heldout_mse_delta": 0.0,
              "is_equivalent": true,
              "max_abs_q_diff": 0.0,
              "max_abs_value_diff": 0.0,
              "policy_regret_delta": 0.0,
              "q_overestimation_delta": 0.0
            }
          }
        },
        "label_or_pair_coverage": {
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
          "successor_calibration_only": {
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
          "successor_distance_trl_log_lambda_0_00": {
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
          "successor_distance_trl_log_lambda_0_25": {
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
          "successor_distance_trl_log_lambda_0_50": {
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
          "successor_distance_trl_log_lambda_0_75": {
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
          "successor_distance_trl_log_lambda_1_00": {
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
        },
        "scenario_role": "main_holdout",
        "successor_meta": {
          "successor_calibration_only": {
            "lambda_tr": 0.0,
            "normalization": "per_state_action_max_self_normalization"
          },
          "successor_distance_trl_log_lambda_0_00": {
            "anchor": "self_normalized_censored_successor_calibration",
            "endpoint": "calibration_only",
            "lambda_tr": 0.0,
            "relaxation": "distance_space_geometric_interpolation"
          },
          "successor_distance_trl_log_lambda_0_25": {
            "anchor": "self_normalized_censored_successor_calibration",
            "lambda_tr": 0.25,
            "relaxation": "distance_space_geometric_interpolation"
          },
          "successor_distance_trl_log_lambda_0_50": {
            "anchor": "self_normalized_censored_successor_calibration",
            "lambda_tr": 0.5,
            "relaxation": "distance_space_geometric_interpolation"
          },
          "successor_distance_trl_log_lambda_0_75": {
            "anchor": "self_normalized_censored_successor_calibration",
            "lambda_tr": 0.75,
            "relaxation": "distance_space_geometric_interpolation"
          },
          "successor_distance_trl_log_lambda_1_00": {
            "anchor": "self_normalized_censored_successor_calibration",
            "lambda_tr": 1.0,
            "relaxation": "distance_space_geometric_interpolation"
          }
        }
      },
      "risk_optimal_matched": {
        "coverage_diagnostics": {
          "action_counts": {
            "forward": 8,
            "risky": 10,
            "safe": 4
          },
          "num_episodes": 14,
          "num_transitions": 22,
          "outcome_counts": {
            "risky_failure": 1,
            "risky_success": 9,
            "safe_goal": 4,
            "safe_step": 8
          },
          "risky_failure_count": 1,
          "risky_success_count": 9,
          "risky_success_rate_observed": 0.9,
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
        "equivalence_diagnostics": {
          "successor_distance_trl_log_lambda_0_00": {
            "lambda_tr": 0.0,
            "versus_successor_calibration_only": {
              "action_diff_rate": 0.0,
              "equivalence_tolerance": 1e-10,
              "heldout_mse_delta": 0.0,
              "is_equivalent": true,
              "max_abs_q_diff": 0.0,
              "max_abs_value_diff": 0.0,
              "policy_regret_delta": 0.0,
              "q_overestimation_delta": 0.0
            },
            "versus_trl_log": {
              "action_diff_rate": 0.0,
              "equivalence_tolerance": 1e-10,
              "heldout_mse_delta": 0.0,
              "is_equivalent": false,
              "max_abs_q_diff": 1.0,
              "max_abs_value_diff": 1.1102230246251565e-16,
              "policy_regret_delta": 0.0,
              "q_overestimation_delta": 8.326672684688674e-17
            }
          },
          "successor_distance_trl_log_lambda_0_25": {
            "lambda_tr": 0.25,
            "versus_successor_calibration_only": {
              "action_diff_rate": 0.0,
              "equivalence_tolerance": 1e-10,
              "heldout_mse_delta": 0.0,
              "is_equivalent": false,
              "max_abs_q_diff": 1.0,
              "max_abs_value_diff": 0.0,
              "policy_regret_delta": 0.0,
              "q_overestimation_delta": 0.0
            },
            "versus_trl_log": {
              "action_diff_rate": 0.0,
              "equivalence_tolerance": 1e-10,
              "heldout_mse_delta": 0.0,
              "is_equivalent": true,
              "max_abs_q_diff": 1.1102230246251565e-16,
              "max_abs_value_diff": 1.1102230246251565e-16,
              "policy_regret_delta": 0.0,
              "q_overestimation_delta": 8.326672684688674e-17
            }
          },
          "successor_distance_trl_log_lambda_0_50": {
            "lambda_tr": 0.5,
            "versus_successor_calibration_only": {
              "action_diff_rate": 0.0,
              "equivalence_tolerance": 1e-10,
              "heldout_mse_delta": 0.0,
              "is_equivalent": false,
              "max_abs_q_diff": 1.0,
              "max_abs_value_diff": 4.163336342344337e-17,
              "policy_regret_delta": 0.0,
              "q_overestimation_delta": 0.0
            },
            "versus_trl_log": {
              "action_diff_rate": 0.0,
              "equivalence_tolerance": 1e-10,
              "heldout_mse_delta": 0.0,
              "is_equivalent": true,
              "max_abs_q_diff": 1.1102230246251565e-16,
              "max_abs_value_diff": 1.1102230246251565e-16,
              "policy_regret_delta": 0.0,
              "q_overestimation_delta": 8.326672684688674e-17
            }
          },
          "successor_distance_trl_log_lambda_0_75": {
            "lambda_tr": 0.75,
            "versus_successor_calibration_only": {
              "action_diff_rate": 0.0,
              "equivalence_tolerance": 1e-10,
              "heldout_mse_delta": 0.0,
              "is_equivalent": false,
              "max_abs_q_diff": 1.0,
              "max_abs_value_diff": 1.1102230246251565e-16,
              "policy_regret_delta": 0.0,
              "q_overestimation_delta": -5.551115123125783e-17
            },
            "versus_trl_log": {
              "action_diff_rate": 0.0,
              "equivalence_tolerance": 1e-10,
              "heldout_mse_delta": 0.0,
              "is_equivalent": true,
              "max_abs_q_diff": 2.7755575615628914e-17,
              "max_abs_value_diff": 2.7755575615628914e-17,
              "policy_regret_delta": 0.0,
              "q_overestimation_delta": 2.7755575615628914e-17
            }
          },
          "successor_distance_trl_log_lambda_1_00": {
            "lambda_tr": 1.0,
            "versus_successor_calibration_only": {
              "action_diff_rate": 0.0,
              "equivalence_tolerance": 1e-10,
              "heldout_mse_delta": 0.0,
              "is_equivalent": false,
              "max_abs_q_diff": 1.0,
              "max_abs_value_diff": 1.1102230246251565e-16,
              "policy_regret_delta": 0.0,
              "q_overestimation_delta": -5.551115123125783e-17
            },
            "versus_trl_log": {
              "action_diff_rate": 0.0,
              "equivalence_tolerance": 1e-10,
              "heldout_mse_delta": 0.0,
              "is_equivalent": true,
              "max_abs_q_diff": 2.7755575615628914e-17,
              "max_abs_value_diff": 2.7755575615628914e-17,
              "policy_regret_delta": 0.0,
              "q_overestimation_delta": 2.7755575615628914e-17
            }
          }
        },
        "label_or_pair_coverage": {
          "censored_examples": [
            {
              "action": "safe",
              "episode_id": "risk_optimal_matched_safe_0",
              "goal": "goal",
              "positive_horizon": 3,
              "state": "start"
            },
            {
              "action": "safe",
              "episode_id": "risk_optimal_matched_safe_1",
              "goal": "goal",
              "positive_horizon": 3,
              "state": "start"
            },
            {
              "action": "safe",
              "episode_id": "risk_optimal_matched_safe_2",
              "goal": "goal",
              "positive_horizon": 3,
              "state": "start"
            },
            {
              "action": "safe",
              "episode_id": "risk_optimal_matched_safe_3",
              "goal": "goal",
              "positive_horizon": 3,
              "state": "start"
            }
          ],
          "counts_by_bin": {
            "h1_train_visible": {
              "included_positive": 22
            },
            "h2_train_visible": {
              "included_positive": 8
            },
            "heldout_gt2": {
              "censored_positive": 4
            },
            "unreached_zero": {
              "included_zero": 76
            }
          },
          "eval_q_pairs_by_horizon_bin": {
            "h1_train_visible": 5,
            "h2_train_visible": 2,
            "heldout_gt2": 1,
            "unreachable": 8
          },
          "eval_value_pairs_by_horizon_bin": {
            "h1_train_visible": 5,
            "h2_train_visible": 2,
            "unreachable": 13
          },
          "label_horizon_cutoff": 2,
          "num_censored_positive_labels": 4,
          "num_included_positive_labels": 30,
          "num_included_zero_labels": 76,
          "unique_state_action_goal_pairs_by_bin": {
            "h1_train_visible": 5,
            "h2_train_visible": 2,
            "heldout_gt2": 1,
            "unreached_zero": 14
          }
        },
        "mdp": "risk_optimal_matched",
        "methods": {
          "mc_plus_trl_log": {
            "calibration_error": 8.673617379884035e-19,
            "chose_exact_optimal_action": true,
            "eval_goal": "goal",
            "eval_greedy_action": "risky",
            "eval_start": "start",
            "eval_start_exact_q": {
              "risky": 0.81,
              "safe": 0.7290000000000001
            },
            "eval_start_learned_q": {
              "risky": 0.81,
              "safe": 0.7290000000000001
            },
            "exact_optimal_action": "risky",
            "heldout_long_horizon_value_mse": 0.0,
            "horizon_metrics": {
              "h1_train_visible": {
                "num_q_pairs": 5,
                "num_value_pairs": 5,
                "q_calibration_error": 2.7755575615628915e-18,
                "q_overestimation_error": 1.3877787807814457e-17,
                "q_underestimation_error": 0.0,
                "value_mse": 3.851859888774472e-35,
                "value_overestimation_error": 1.3877787807814457e-17,
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
                "num_value_pairs": 0,
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
            "q_calibration_error": 8.673617379884035e-19,
            "q_overestimation_error": 1.3877787807814457e-17,
            "q_underestimation_error": 0.0,
            "risky_action_selection_rate": 1.0,
            "value_mse": 9.62964972193618e-36,
            "value_overestimation_error": 1.3877787807814457e-17,
            "value_underestimation_error": 0.0
          },
          "mc_supervised": {
            "calibration_error": 0.04556250000000001,
            "chose_exact_optimal_action": true,
            "eval_goal": "goal",
            "eval_greedy_action": "risky",
            "eval_start": "start",
            "eval_start_exact_q": {
              "risky": 0.81,
              "safe": 0.7290000000000001
            },
            "eval_start_learned_q": {
              "risky": 0.8100000000000002,
              "safe": 0.0
            },
            "exact_optimal_action": "risky",
            "heldout_long_horizon_value_mse": 0.0,
            "horizon_metrics": {
              "h1_train_visible": {
                "num_q_pairs": 5,
                "num_value_pairs": 5,
                "q_calibration_error": 2.4980018054066023e-17,
                "q_overestimation_error": 1.1102230246251565e-16,
                "q_underestimation_error": 0.0,
                "value_mse": 2.5037089277034066e-33,
                "value_overestimation_error": 1.1102230246251565e-16,
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
                "num_value_pairs": 0,
                "q_calibration_error": 0.7290000000000001,
                "q_overestimation_error": 0.0,
                "q_underestimation_error": 0.7290000000000001,
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
            "q_calibration_error": 0.04556250000000001,
            "q_overestimation_error": 1.1102230246251565e-16,
            "q_underestimation_error": 0.7290000000000001,
            "risky_action_selection_rate": 1.0,
            "value_mse": 6.2592723192585165e-34,
            "value_overestimation_error": 1.1102230246251565e-16,
            "value_underestimation_error": 0.0
          },
          "successor_calibration_only": {
            "calibration_error": 0.04556250000000001,
            "chose_exact_optimal_action": true,
            "eval_goal": "goal",
            "eval_greedy_action": "risky",
            "eval_start": "start",
            "eval_start_exact_q": {
              "risky": 0.81,
              "safe": 0.7290000000000001
            },
            "eval_start_learned_q": {
              "risky": 0.8100000000000002,
              "safe": 0.0
            },
            "exact_optimal_action": "risky",
            "heldout_long_horizon_value_mse": 0.0,
            "horizon_metrics": {
              "h1_train_visible": {
                "num_q_pairs": 5,
                "num_value_pairs": 5,
                "q_calibration_error": 2.4980018054066023e-17,
                "q_overestimation_error": 1.1102230246251565e-16,
                "q_underestimation_error": 0.0,
                "value_mse": 2.5037089277034066e-33,
                "value_overestimation_error": 1.1102230246251565e-16,
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
                "num_value_pairs": 0,
                "q_calibration_error": 0.7290000000000001,
                "q_overestimation_error": 0.0,
                "q_underestimation_error": 0.7290000000000001,
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
            "q_calibration_error": 0.04556250000000001,
            "q_overestimation_error": 1.1102230246251565e-16,
            "q_underestimation_error": 0.7290000000000001,
            "risky_action_selection_rate": 1.0,
            "value_mse": 6.2592723192585165e-34,
            "value_overestimation_error": 1.1102230246251565e-16,
            "value_underestimation_error": 0.0
          },
          "successor_distance_trl_log_lambda_0_00": {
            "calibration_error": 0.04556250000000001,
            "chose_exact_optimal_action": true,
            "eval_goal": "goal",
            "eval_greedy_action": "risky",
            "eval_start": "start",
            "eval_start_exact_q": {
              "risky": 0.81,
              "safe": 0.7290000000000001
            },
            "eval_start_learned_q": {
              "risky": 0.8100000000000002,
              "safe": 0.0
            },
            "exact_optimal_action": "risky",
            "heldout_long_horizon_value_mse": 0.0,
            "horizon_metrics": {
              "h1_train_visible": {
                "num_q_pairs": 5,
                "num_value_pairs": 5,
                "q_calibration_error": 2.4980018054066023e-17,
                "q_overestimation_error": 1.1102230246251565e-16,
                "q_underestimation_error": 0.0,
                "value_mse": 2.5037089277034066e-33,
                "value_overestimation_error": 1.1102230246251565e-16,
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
                "num_value_pairs": 0,
                "q_calibration_error": 0.7290000000000001,
                "q_overestimation_error": 0.0,
                "q_underestimation_error": 0.7290000000000001,
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
            "q_calibration_error": 0.04556250000000001,
            "q_overestimation_error": 1.1102230246251565e-16,
            "q_underestimation_error": 0.7290000000000001,
            "risky_action_selection_rate": 1.0,
            "value_mse": 6.2592723192585165e-34,
            "value_overestimation_error": 1.1102230246251565e-16,
            "value_underestimation_error": 0.0
          },
          "successor_distance_trl_log_lambda_0_25": {
            "calibration_error": 7.806255641895632e-18,
            "chose_exact_optimal_action": true,
            "eval_goal": "goal",
            "eval_greedy_action": "risky",
            "eval_start": "start",
            "eval_start_exact_q": {
              "risky": 0.81,
              "safe": 0.7290000000000001
            },
            "eval_start_learned_q": {
              "risky": 0.8100000000000002,
              "safe": 0.7290000000000001
            },
            "exact_optimal_action": "risky",
            "heldout_long_horizon_value_mse": 0.0,
            "horizon_metrics": {
              "h1_train_visible": {
                "num_q_pairs": 5,
                "num_value_pairs": 5,
                "q_calibration_error": 2.4980018054066023e-17,
                "q_overestimation_error": 1.1102230246251565e-16,
                "q_underestimation_error": 0.0,
                "value_mse": 2.5037089277034066e-33,
                "value_overestimation_error": 1.1102230246251565e-16,
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
                "num_value_pairs": 0,
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
            "q_calibration_error": 7.806255641895632e-18,
            "q_overestimation_error": 1.1102230246251565e-16,
            "q_underestimation_error": 0.0,
            "risky_action_selection_rate": 1.0,
            "value_mse": 6.2592723192585165e-34,
            "value_overestimation_error": 1.1102230246251565e-16,
            "value_underestimation_error": 0.0
          },
          "successor_distance_trl_log_lambda_0_50": {
            "calibration_error": 1.0408340855860843e-17,
            "chose_exact_optimal_action": true,
            "eval_goal": "goal",
            "eval_greedy_action": "risky",
            "eval_start": "start",
            "eval_start_exact_q": {
              "risky": 0.81,
              "safe": 0.7290000000000001
            },
            "eval_start_learned_q": {
              "risky": 0.8100000000000002,
              "safe": 0.7290000000000001
            },
            "exact_optimal_action": "risky",
            "heldout_long_horizon_value_mse": 0.0,
            "horizon_metrics": {
              "h1_train_visible": {
                "num_q_pairs": 5,
                "num_value_pairs": 5,
                "q_calibration_error": 3.3306690738754695e-17,
                "q_overestimation_error": 1.1102230246251565e-16,
                "q_underestimation_error": 0.0,
                "value_mse": 3.0814879110195774e-33,
                "value_overestimation_error": 1.1102230246251565e-16,
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
                "num_value_pairs": 0,
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
            "q_calibration_error": 1.0408340855860843e-17,
            "q_overestimation_error": 1.1102230246251565e-16,
            "q_underestimation_error": 0.0,
            "risky_action_selection_rate": 1.0,
            "value_mse": 7.703719777548943e-34,
            "value_overestimation_error": 1.1102230246251565e-16,
            "value_underestimation_error": 0.0
          },
          "successor_distance_trl_log_lambda_0_75": {
            "calibration_error": 3.469446951953614e-18,
            "chose_exact_optimal_action": true,
            "eval_goal": "goal",
            "eval_greedy_action": "risky",
            "eval_start": "start",
            "eval_start_exact_q": {
              "risky": 0.81,
              "safe": 0.7290000000000001
            },
            "eval_start_learned_q": {
              "risky": 0.81,
              "safe": 0.7290000000000001
            },
            "exact_optimal_action": "risky",
            "heldout_long_horizon_value_mse": 0.0,
            "horizon_metrics": {
              "h1_train_visible": {
                "num_q_pairs": 5,
                "num_value_pairs": 5,
                "q_calibration_error": 1.1102230246251566e-17,
                "q_overestimation_error": 5.551115123125783e-17,
                "q_underestimation_error": 0.0,
                "value_mse": 6.162975822039155e-34,
                "value_overestimation_error": 5.551115123125783e-17,
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
                "num_value_pairs": 0,
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
            "q_calibration_error": 3.469446951953614e-18,
            "q_overestimation_error": 5.551115123125783e-17,
            "q_underestimation_error": 0.0,
            "risky_action_selection_rate": 1.0,
            "value_mse": 1.5407439555097888e-34,
            "value_overestimation_error": 5.551115123125783e-17,
            "value_underestimation_error": 0.0
          },
          "successor_distance_trl_log_lambda_1_00": {
            "calibration_error": 3.469446951953614e-18,
            "chose_exact_optimal_action": true,
            "eval_goal": "goal",
            "eval_greedy_action": "risky",
            "eval_start": "start",
            "eval_start_exact_q": {
              "risky": 0.81,
              "safe": 0.7290000000000001
            },
            "eval_start_learned_q": {
              "risky": 0.81,
              "safe": 0.7290000000000001
            },
            "exact_optimal_action": "risky",
            "heldout_long_horizon_value_mse": 0.0,
            "horizon_metrics": {
              "h1_train_visible": {
                "num_q_pairs": 5,
                "num_value_pairs": 5,
                "q_calibration_error": 1.1102230246251566e-17,
                "q_overestimation_error": 5.551115123125783e-17,
                "q_underestimation_error": 0.0,
                "value_mse": 6.162975822039155e-34,
                "value_overestimation_error": 5.551115123125783e-17,
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
                "num_value_pairs": 0,
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
            "q_calibration_error": 3.469446951953614e-18,
            "q_overestimation_error": 5.551115123125783e-17,
            "q_underestimation_error": 0.0,
            "risky_action_selection_rate": 1.0,
            "value_mse": 1.5407439555097888e-34,
            "value_overestimation_error": 5.551115123125783e-17,
            "value_underestimation_error": 0.0
          },
          "trl_log": {
            "calibration_error": 1.734723475976807e-18,
            "chose_exact_optimal_action": true,
            "eval_goal": "goal",
            "eval_greedy_action": "risky",
            "eval_start": "start",
            "eval_start_exact_q": {
              "risky": 0.81,
              "safe": 0.7290000000000001
            },
            "eval_start_learned_q": {
              "risky": 0.81,
              "safe": 0.7290000000000001
            },
            "exact_optimal_action": "risky",
            "heldout_long_horizon_value_mse": 0.0,
            "horizon_metrics": {
              "h1_train_visible": {
                "num_q_pairs": 5,
                "num_value_pairs": 5,
                "q_calibration_error": 5.551115123125783e-18,
                "q_overestimation_error": 2.7755575615628914e-17,
                "q_underestimation_error": 0.0,
                "value_mse": 1.5407439555097888e-34,
                "value_overestimation_error": 2.7755575615628914e-17,
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
                "num_value_pairs": 0,
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
            "q_calibration_error": 1.734723475976807e-18,
            "q_overestimation_error": 2.7755575615628914e-17,
            "q_underestimation_error": 0.0,
            "risky_action_selection_rate": 1.0,
            "value_mse": 3.851859888774472e-35,
            "value_overestimation_error": 2.7755575615628914e-17,
            "value_underestimation_error": 0.0
          },
          "trl_raw": {
            "calibration_error": 0.05625,
            "chose_exact_optimal_action": true,
            "eval_goal": "goal",
            "eval_greedy_action": "risky",
            "eval_start": "start",
            "eval_start_exact_q": {
              "risky": 0.81,
              "safe": 0.7290000000000001
            },
            "eval_start_learned_q": {
              "risky": 0.9,
              "safe": 0.7290000000000001
            },
            "exact_optimal_action": "risky",
            "heldout_long_horizon_value_mse": 0.0,
            "horizon_metrics": {
              "h1_train_visible": {
                "num_q_pairs": 5,
                "num_value_pairs": 5,
                "q_calibration_error": 0.18,
                "q_overestimation_error": 0.81,
                "q_underestimation_error": 0.0,
                "value_mse": 0.13284,
                "value_overestimation_error": 0.81,
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
                "num_value_pairs": 0,
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
            "q_calibration_error": 0.05625,
            "q_overestimation_error": 0.81,
            "q_underestimation_error": 0.0,
            "risky_action_selection_rate": 1.0,
            "value_mse": 0.03321,
            "value_overestimation_error": 0.81,
            "value_underestimation_error": 0.0
          }
        },
        "scenario_role": "main_matched",
        "successor_meta": {
          "successor_calibration_only": {
            "lambda_tr": 0.0,
            "normalization": "per_state_action_max_self_normalization"
          },
          "successor_distance_trl_log_lambda_0_00": {
            "anchor": "self_normalized_censored_successor_calibration",
            "endpoint": "calibration_only",
            "lambda_tr": 0.0,
            "relaxation": "distance_space_geometric_interpolation"
          },
          "successor_distance_trl_log_lambda_0_25": {
            "anchor": "self_normalized_censored_successor_calibration",
            "lambda_tr": 0.25,
            "relaxation": "distance_space_geometric_interpolation"
          },
          "successor_distance_trl_log_lambda_0_50": {
            "anchor": "self_normalized_censored_successor_calibration",
            "lambda_tr": 0.5,
            "relaxation": "distance_space_geometric_interpolation"
          },
          "successor_distance_trl_log_lambda_0_75": {
            "anchor": "self_normalized_censored_successor_calibration",
            "lambda_tr": 0.75,
            "relaxation": "distance_space_geometric_interpolation"
          },
          "successor_distance_trl_log_lambda_1_00": {
            "anchor": "self_normalized_censored_successor_calibration",
            "lambda_tr": 1.0,
            "relaxation": "distance_space_geometric_interpolation"
          }
        }
      },
      "safe_optimal_lucky_only_stress": {
        "coverage_diagnostics": {
          "action_counts": {
            "forward": 8,
            "risky": 4,
            "safe": 4
          },
          "num_episodes": 8,
          "num_transitions": 16,
          "outcome_counts": {
            "risky_success": 4,
            "safe_goal": 4,
            "safe_step": 8
          },
          "risky_failure_count": 0,
          "risky_success_count": 4,
          "risky_success_rate_observed": 1.0,
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
          "state_coverage_fraction": 0.8,
          "states_seen": [
            "goal",
            "safe1",
            "safe2",
            "start"
          ]
        },
        "equivalence_diagnostics": {
          "successor_distance_trl_log_lambda_0_00": {
            "lambda_tr": 0.0,
            "versus_successor_calibration_only": {
              "action_diff_rate": 0.0,
              "equivalence_tolerance": 1e-10,
              "heldout_mse_delta": 0.0,
              "is_equivalent": true,
              "max_abs_q_diff": 0.0,
              "max_abs_value_diff": 0.0,
              "policy_regret_delta": 0.0,
              "q_overestimation_delta": 0.0
            },
            "versus_trl_log": {
              "action_diff_rate": 0.0,
              "equivalence_tolerance": 1e-10,
              "heldout_mse_delta": 0.0,
              "is_equivalent": false,
              "max_abs_q_diff": 1.0,
              "max_abs_value_diff": 0.0,
              "policy_regret_delta": 0.0,
              "q_overestimation_delta": 0.0
            }
          },
          "successor_distance_trl_log_lambda_0_25": {
            "lambda_tr": 0.25,
            "versus_successor_calibration_only": {
              "action_diff_rate": 0.0,
              "equivalence_tolerance": 1e-10,
              "heldout_mse_delta": 0.0,
              "is_equivalent": false,
              "max_abs_q_diff": 1.0,
              "max_abs_value_diff": 0.0,
              "policy_regret_delta": 0.0,
              "q_overestimation_delta": 0.0
            },
            "versus_trl_log": {
              "action_diff_rate": 0.0,
              "equivalence_tolerance": 1e-10,
              "heldout_mse_delta": 0.0,
              "is_equivalent": true,
              "max_abs_q_diff": 0.0,
              "max_abs_value_diff": 0.0,
              "policy_regret_delta": 0.0,
              "q_overestimation_delta": 0.0
            }
          },
          "successor_distance_trl_log_lambda_0_50": {
            "lambda_tr": 0.5,
            "versus_successor_calibration_only": {
              "action_diff_rate": 0.0,
              "equivalence_tolerance": 1e-10,
              "heldout_mse_delta": 0.0,
              "is_equivalent": false,
              "max_abs_q_diff": 1.0,
              "max_abs_value_diff": 0.0,
              "policy_regret_delta": 0.0,
              "q_overestimation_delta": 0.0
            },
            "versus_trl_log": {
              "action_diff_rate": 0.0,
              "equivalence_tolerance": 1e-10,
              "heldout_mse_delta": 0.0,
              "is_equivalent": true,
              "max_abs_q_diff": 0.0,
              "max_abs_value_diff": 0.0,
              "policy_regret_delta": 0.0,
              "q_overestimation_delta": 0.0
            }
          },
          "successor_distance_trl_log_lambda_0_75": {
            "lambda_tr": 0.75,
            "versus_successor_calibration_only": {
              "action_diff_rate": 0.0,
              "equivalence_tolerance": 1e-10,
              "heldout_mse_delta": 0.0,
              "is_equivalent": false,
              "max_abs_q_diff": 1.0,
              "max_abs_value_diff": 0.0,
              "policy_regret_delta": 0.0,
              "q_overestimation_delta": 0.0
            },
            "versus_trl_log": {
              "action_diff_rate": 0.0,
              "equivalence_tolerance": 1e-10,
              "heldout_mse_delta": 0.0,
              "is_equivalent": true,
              "max_abs_q_diff": 0.0,
              "max_abs_value_diff": 0.0,
              "policy_regret_delta": 0.0,
              "q_overestimation_delta": 0.0
            }
          },
          "successor_distance_trl_log_lambda_1_00": {
            "lambda_tr": 1.0,
            "versus_successor_calibration_only": {
              "action_diff_rate": 0.0,
              "equivalence_tolerance": 1e-10,
              "heldout_mse_delta": 0.0,
              "is_equivalent": false,
              "max_abs_q_diff": 1.0,
              "max_abs_value_diff": 0.0,
              "policy_regret_delta": 0.0,
              "q_overestimation_delta": 0.0
            },
            "versus_trl_log": {
              "action_diff_rate": 0.0,
              "equivalence_tolerance": 1e-10,
              "heldout_mse_delta": 0.0,
              "is_equivalent": true,
              "max_abs_q_diff": 0.0,
              "max_abs_value_diff": 0.0,
              "policy_regret_delta": 0.0,
              "q_overestimation_delta": 0.0
            }
          }
        },
        "label_or_pair_coverage": {
          "censored_examples": [
            {
              "action": "safe",
              "episode_id": "safe_optimal_lucky_only_stress_safe_0",
              "goal": "goal",
              "positive_horizon": 3,
              "state": "start"
            },
            {
              "action": "safe",
              "episode_id": "safe_optimal_lucky_only_stress_safe_1",
              "goal": "goal",
              "positive_horizon": 3,
              "state": "start"
            },
            {
              "action": "safe",
              "episode_id": "safe_optimal_lucky_only_stress_safe_2",
              "goal": "goal",
              "positive_horizon": 3,
              "state": "start"
            },
            {
              "action": "safe",
              "episode_id": "safe_optimal_lucky_only_stress_safe_3",
              "goal": "goal",
              "positive_horizon": 3,
              "state": "start"
            }
          ],
          "counts_by_bin": {
            "h1_train_visible": {
              "included_positive": 16
            },
            "h2_train_visible": {
              "included_positive": 8
            },
            "heldout_gt2": {
              "censored_positive": 4
            },
            "unreached_zero": {
              "included_zero": 52
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
          "num_included_positive_labels": 24,
          "num_included_zero_labels": 52,
          "unique_state_action_goal_pairs_by_bin": {
            "h1_train_visible": 4,
            "h2_train_visible": 2,
            "heldout_gt2": 1,
            "unreached_zero": 13
          }
        },
        "mdp": "safe_optimal_lucky_only",
        "methods": {
          "mc_plus_trl_log": {
            "calibration_error": 0.084375,
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
                "q_calibration_error": 0.27,
                "q_overestimation_error": 0.675,
                "q_underestimation_error": 0.675,
                "value_mse": 0.11390625000000001,
                "value_overestimation_error": 0.0,
                "value_underestimation_error": 0.675
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
            "q_calibration_error": 0.084375,
            "q_overestimation_error": 0.675,
            "q_underestimation_error": 0.675,
            "risky_action_selection_rate": 1.0,
            "value_mse": 0.024243300000000002,
            "value_overestimation_error": 0.17099999999999993,
            "value_underestimation_error": 0.675
          },
          "mc_supervised": {
            "calibration_error": 0.1299375,
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
              "safe": 0.0
            },
            "exact_optimal_action": "safe",
            "heldout_long_horizon_value_mse": 0.029240999999999975,
            "horizon_metrics": {
              "h1_train_visible": {
                "num_q_pairs": 5,
                "num_value_pairs": 4,
                "q_calibration_error": 0.27,
                "q_overestimation_error": 0.675,
                "q_underestimation_error": 0.675,
                "value_mse": 0.11390625000000001,
                "value_overestimation_error": 0.0,
                "value_underestimation_error": 0.675
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
            "q_calibration_error": 0.1299375,
            "q_overestimation_error": 0.675,
            "q_underestimation_error": 0.7290000000000001,
            "risky_action_selection_rate": 1.0,
            "value_mse": 0.024243300000000002,
            "value_overestimation_error": 0.17099999999999993,
            "value_underestimation_error": 0.675
          },
          "successor_calibration_only": {
            "calibration_error": 0.1299375,
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
              "safe": 0.0
            },
            "exact_optimal_action": "safe",
            "heldout_long_horizon_value_mse": 0.029240999999999975,
            "horizon_metrics": {
              "h1_train_visible": {
                "num_q_pairs": 5,
                "num_value_pairs": 4,
                "q_calibration_error": 0.27,
                "q_overestimation_error": 0.675,
                "q_underestimation_error": 0.675,
                "value_mse": 0.11390625000000001,
                "value_overestimation_error": 0.0,
                "value_underestimation_error": 0.675
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
            "q_calibration_error": 0.1299375,
            "q_overestimation_error": 0.675,
            "q_underestimation_error": 0.7290000000000001,
            "risky_action_selection_rate": 1.0,
            "value_mse": 0.024243300000000002,
            "value_overestimation_error": 0.17099999999999993,
            "value_underestimation_error": 0.675
          },
          "successor_distance_trl_log_lambda_0_00": {
            "calibration_error": 0.1299375,
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
              "safe": 0.0
            },
            "exact_optimal_action": "safe",
            "heldout_long_horizon_value_mse": 0.029240999999999975,
            "horizon_metrics": {
              "h1_train_visible": {
                "num_q_pairs": 5,
                "num_value_pairs": 4,
                "q_calibration_error": 0.27,
                "q_overestimation_error": 0.675,
                "q_underestimation_error": 0.675,
                "value_mse": 0.11390625000000001,
                "value_overestimation_error": 0.0,
                "value_underestimation_error": 0.675
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
            "q_calibration_error": 0.1299375,
            "q_overestimation_error": 0.675,
            "q_underestimation_error": 0.7290000000000001,
            "risky_action_selection_rate": 1.0,
            "value_mse": 0.024243300000000002,
            "value_overestimation_error": 0.17099999999999993,
            "value_underestimation_error": 0.675
          },
          "successor_distance_trl_log_lambda_0_25": {
            "calibration_error": 0.084375,
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
                "q_calibration_error": 0.27,
                "q_overestimation_error": 0.675,
                "q_underestimation_error": 0.675,
                "value_mse": 0.11390625000000001,
                "value_overestimation_error": 0.0,
                "value_underestimation_error": 0.675
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
            "q_calibration_error": 0.084375,
            "q_overestimation_error": 0.675,
            "q_underestimation_error": 0.675,
            "risky_action_selection_rate": 1.0,
            "value_mse": 0.024243300000000002,
            "value_overestimation_error": 0.17099999999999993,
            "value_underestimation_error": 0.675
          },
          "successor_distance_trl_log_lambda_0_50": {
            "calibration_error": 0.084375,
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
                "q_calibration_error": 0.27,
                "q_overestimation_error": 0.675,
                "q_underestimation_error": 0.675,
                "value_mse": 0.11390625000000001,
                "value_overestimation_error": 0.0,
                "value_underestimation_error": 0.675
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
            "q_calibration_error": 0.084375,
            "q_overestimation_error": 0.675,
            "q_underestimation_error": 0.675,
            "risky_action_selection_rate": 1.0,
            "value_mse": 0.024243300000000002,
            "value_overestimation_error": 0.17099999999999993,
            "value_underestimation_error": 0.675
          },
          "successor_distance_trl_log_lambda_0_75": {
            "calibration_error": 0.084375,
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
                "q_calibration_error": 0.27,
                "q_overestimation_error": 0.675,
                "q_underestimation_error": 0.675,
                "value_mse": 0.11390625000000001,
                "value_overestimation_error": 0.0,
                "value_underestimation_error": 0.675
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
            "q_calibration_error": 0.084375,
            "q_overestimation_error": 0.675,
            "q_underestimation_error": 0.675,
            "risky_action_selection_rate": 1.0,
            "value_mse": 0.024243300000000002,
            "value_overestimation_error": 0.17099999999999993,
            "value_underestimation_error": 0.675
          },
          "successor_distance_trl_log_lambda_1_00": {
            "calibration_error": 0.084375,
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
                "q_calibration_error": 0.27,
                "q_overestimation_error": 0.675,
                "q_underestimation_error": 0.675,
                "value_mse": 0.11390625000000001,
                "value_overestimation_error": 0.0,
                "value_underestimation_error": 0.675
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
            "q_calibration_error": 0.084375,
            "q_overestimation_error": 0.675,
            "q_underestimation_error": 0.675,
            "risky_action_selection_rate": 1.0,
            "value_mse": 0.024243300000000002,
            "value_overestimation_error": 0.17099999999999993,
            "value_underestimation_error": 0.675
          },
          "trl_log": {
            "calibration_error": 0.084375,
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
                "q_calibration_error": 0.27,
                "q_overestimation_error": 0.675,
                "q_underestimation_error": 0.675,
                "value_mse": 0.11390625000000001,
                "value_overestimation_error": 0.0,
                "value_underestimation_error": 0.675
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
            "q_calibration_error": 0.084375,
            "q_overestimation_error": 0.675,
            "q_underestimation_error": 0.675,
            "risky_action_selection_rate": 1.0,
            "value_mse": 0.024243300000000002,
            "value_overestimation_error": 0.17099999999999993,
            "value_underestimation_error": 0.675
          },
          "trl_raw": {
            "calibration_error": 0.084375,
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
                "q_calibration_error": 0.27,
                "q_overestimation_error": 0.675,
                "q_underestimation_error": 0.675,
                "value_mse": 0.11390625000000001,
                "value_overestimation_error": 0.0,
                "value_underestimation_error": 0.675
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
            "q_calibration_error": 0.084375,
            "q_overestimation_error": 0.675,
            "q_underestimation_error": 0.675,
            "risky_action_selection_rate": 1.0,
            "value_mse": 0.024243300000000002,
            "value_overestimation_error": 0.17099999999999993,
            "value_underestimation_error": 0.675
          }
        },
        "scenario_role": "stress_biased",
        "successor_meta": {
          "successor_calibration_only": {
            "lambda_tr": 0.0,
            "normalization": "per_state_action_max_self_normalization"
          },
          "successor_distance_trl_log_lambda_0_00": {
            "anchor": "self_normalized_censored_successor_calibration",
            "endpoint": "calibration_only",
            "lambda_tr": 0.0,
            "relaxation": "distance_space_geometric_interpolation"
          },
          "successor_distance_trl_log_lambda_0_25": {
            "anchor": "self_normalized_censored_successor_calibration",
            "lambda_tr": 0.25,
            "relaxation": "distance_space_geometric_interpolation"
          },
          "successor_distance_trl_log_lambda_0_50": {
            "anchor": "self_normalized_censored_successor_calibration",
            "lambda_tr": 0.5,
            "relaxation": "distance_space_geometric_interpolation"
          },
          "successor_distance_trl_log_lambda_0_75": {
            "anchor": "self_normalized_censored_successor_calibration",
            "lambda_tr": 0.75,
            "relaxation": "distance_space_geometric_interpolation"
          },
          "successor_distance_trl_log_lambda_1_00": {
            "anchor": "self_normalized_censored_successor_calibration",
            "lambda_tr": 1.0,
            "relaxation": "distance_space_geometric_interpolation"
          }
        }
      },
      "safe_optimal_matched": {
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
        "equivalence_diagnostics": {
          "successor_distance_trl_log_lambda_0_00": {
            "lambda_tr": 0.0,
            "versus_successor_calibration_only": {
              "action_diff_rate": 0.0,
              "equivalence_tolerance": 1e-10,
              "heldout_mse_delta": 0.0,
              "is_equivalent": true,
              "max_abs_q_diff": 0.0,
              "max_abs_value_diff": 0.0,
              "policy_regret_delta": 0.0,
              "q_overestimation_delta": 0.0
            },
            "versus_trl_log": {
              "action_diff_rate": 0.08333333333333333,
              "equivalence_tolerance": 1e-10,
              "heldout_mse_delta": 0.25401600000000013,
              "is_equivalent": false,
              "max_abs_q_diff": 1.0,
              "max_abs_value_diff": 0.5040000000000001,
              "policy_regret_delta": 0.5040000000000001,
              "q_overestimation_delta": 0.0
            }
          },
          "successor_distance_trl_log_lambda_0_25": {
            "lambda_tr": 0.25,
            "versus_successor_calibration_only": {
              "action_diff_rate": 0.08333333333333333,
              "equivalence_tolerance": 1e-10,
              "heldout_mse_delta": -0.25401600000000013,
              "is_equivalent": false,
              "max_abs_q_diff": 1.0,
              "max_abs_value_diff": 0.5040000000000001,
              "policy_regret_delta": -0.5040000000000001,
              "q_overestimation_delta": 0.0
            },
            "versus_trl_log": {
              "action_diff_rate": 0.0,
              "equivalence_tolerance": 1e-10,
              "heldout_mse_delta": 0.0,
              "is_equivalent": true,
              "max_abs_q_diff": 0.0,
              "max_abs_value_diff": 0.0,
              "policy_regret_delta": 0.0,
              "q_overestimation_delta": 0.0
            }
          },
          "successor_distance_trl_log_lambda_0_50": {
            "lambda_tr": 0.5,
            "versus_successor_calibration_only": {
              "action_diff_rate": 0.08333333333333333,
              "equivalence_tolerance": 1e-10,
              "heldout_mse_delta": -0.25401600000000013,
              "is_equivalent": false,
              "max_abs_q_diff": 1.0,
              "max_abs_value_diff": 0.5040000000000001,
              "policy_regret_delta": -0.5040000000000001,
              "q_overestimation_delta": 0.0
            },
            "versus_trl_log": {
              "action_diff_rate": 0.0,
              "equivalence_tolerance": 1e-10,
              "heldout_mse_delta": 0.0,
              "is_equivalent": true,
              "max_abs_q_diff": 0.0,
              "max_abs_value_diff": 0.0,
              "policy_regret_delta": 0.0,
              "q_overestimation_delta": 0.0
            }
          },
          "successor_distance_trl_log_lambda_0_75": {
            "lambda_tr": 0.75,
            "versus_successor_calibration_only": {
              "action_diff_rate": 0.08333333333333333,
              "equivalence_tolerance": 1e-10,
              "heldout_mse_delta": -0.25401600000000013,
              "is_equivalent": false,
              "max_abs_q_diff": 1.0,
              "max_abs_value_diff": 0.5040000000000001,
              "policy_regret_delta": -0.5040000000000001,
              "q_overestimation_delta": 0.0
            },
            "versus_trl_log": {
              "action_diff_rate": 0.0,
              "equivalence_tolerance": 1e-10,
              "heldout_mse_delta": 0.0,
              "is_equivalent": true,
              "max_abs_q_diff": 0.0,
              "max_abs_value_diff": 0.0,
              "policy_regret_delta": 0.0,
              "q_overestimation_delta": 0.0
            }
          },
          "successor_distance_trl_log_lambda_1_00": {
            "lambda_tr": 1.0,
            "versus_successor_calibration_only": {
              "action_diff_rate": 0.08333333333333333,
              "equivalence_tolerance": 1e-10,
              "heldout_mse_delta": -0.25401600000000013,
              "is_equivalent": false,
              "max_abs_q_diff": 1.0,
              "max_abs_value_diff": 0.5040000000000001,
              "policy_regret_delta": -0.5040000000000001,
              "q_overestimation_delta": 0.0
            },
            "versus_trl_log": {
              "action_diff_rate": 0.0,
              "equivalence_tolerance": 1e-10,
              "heldout_mse_delta": 0.0,
              "is_equivalent": true,
              "max_abs_q_diff": 0.0,
              "max_abs_value_diff": 0.0,
              "policy_regret_delta": 0.0,
              "q_overestimation_delta": 0.0
            }
          }
        },
        "label_or_pair_coverage": {
          "censored_examples": [
            {
              "action": "safe",
              "episode_id": "safe_optimal_matched_safe_0",
              "goal": "goal",
              "positive_horizon": 3,
              "state": "start"
            },
            {
              "action": "safe",
              "episode_id": "safe_optimal_matched_safe_1",
              "goal": "goal",
              "positive_horizon": 3,
              "state": "start"
            },
            {
              "action": "safe",
              "episode_id": "safe_optimal_matched_safe_2",
              "goal": "goal",
              "positive_horizon": 3,
              "state": "start"
            },
            {
              "action": "safe",
              "episode_id": "safe_optimal_matched_safe_3",
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
        "mdp": "safe_optimal_matched",
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
          "successor_calibration_only": {
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
          "successor_distance_trl_log_lambda_0_00": {
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
          "successor_distance_trl_log_lambda_0_25": {
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
          "successor_distance_trl_log_lambda_0_50": {
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
          "successor_distance_trl_log_lambda_0_75": {
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
          "successor_distance_trl_log_lambda_1_00": {
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
        },
        "scenario_role": "main_matched",
        "successor_meta": {
          "successor_calibration_only": {
            "lambda_tr": 0.0,
            "normalization": "per_state_action_max_self_normalization"
          },
          "successor_distance_trl_log_lambda_0_00": {
            "anchor": "self_normalized_censored_successor_calibration",
            "endpoint": "calibration_only",
            "lambda_tr": 0.0,
            "relaxation": "distance_space_geometric_interpolation"
          },
          "successor_distance_trl_log_lambda_0_25": {
            "anchor": "self_normalized_censored_successor_calibration",
            "lambda_tr": 0.25,
            "relaxation": "distance_space_geometric_interpolation"
          },
          "successor_distance_trl_log_lambda_0_50": {
            "anchor": "self_normalized_censored_successor_calibration",
            "lambda_tr": 0.5,
            "relaxation": "distance_space_geometric_interpolation"
          },
          "successor_distance_trl_log_lambda_0_75": {
            "anchor": "self_normalized_censored_successor_calibration",
            "lambda_tr": 0.75,
            "relaxation": "distance_space_geometric_interpolation"
          },
          "successor_distance_trl_log_lambda_1_00": {
            "anchor": "self_normalized_censored_successor_calibration",
            "lambda_tr": 1.0,
            "relaxation": "distance_space_geometric_interpolation"
          }
        }
      }
    },
    "success_checks": {
      "audit_completed": true,
      "chain_raw_exact": true,
      "chain_trl_log_exact": true,
      "lambda_sweep_completed": true,
      "negative_equivalence_evidence": true,
      "positive_successor_evidence": false
    },
    "update_steps": 32
  },
  "next_questions": [
    "What update or regularizer would make successor-distance relaxation differ from pure empirical trl_log in deterministic tabular cases?",
    "Should future variants add uncertainty penalties so biased lucky-only support does not collapse to raw support optimism?",
    "Can a non-tabular setting expose distance-space interpolation differences that are absent in this exact tabular audit?"
  ],
  "status": "completed"
}
```


## Latest summary

# Experiment 0005 Summary

## Objective

Audit whether successor-distance + TRL-log has a distinct tabular effect beyond calibration-only and trl_log.

## Commands Run

```bash
mkdir -p research/sto_trl/artifacts/0005 research/sto_trl/results && cp research/sto_trl/artifacts/0004/run_successor_distance.py research/sto_trl/artifacts/0005/run_lambda_equivalence_audit.py
conda run -n autoresearcher_sto_trl python research/sto_trl/artifacts/0005/run_lambda_equivalence_audit.py
conda run -n autoresearcher_sto_trl python scripts/validate_artifacts.py --repo-root . --json research/sto_trl/results/0005_result.json --schema schemas/result.schema.json --check-result-artifacts
```

## Setup

- Discount: `0.9`
- Label horizon cutoff: `2`
- Fixed backup iterations: `32`
- Lambda sweep: `[0.0, 0.25, 0.5, 0.75, 1.0]`
- Equivalence tolerance: `1e-10`
- Main scenarios: chain holdout, matched safe-optimal risky shortcut, matched risk-optimal risky shortcut.
- Stress scenario: safe-optimal lucky-only risky shortcut.

## Main Metrics

| Scenario | Method | Lambda | Held-out MSE | Q calibration | Policy regret | Action | Triangle violation |
| --- | --- | ---: | ---: | ---: | ---: | --- | ---: |
| chain_len9_holdout | mc_supervised | None | 0.391705823230 | 0.465607869047 | 0.000000000000 | right | 0.166667 |
| chain_len9_holdout | trl_raw | None | 0.000000000000 | 0.000000000000 | 0.000000000000 | right | 0.000000 |
| chain_len9_holdout | trl_log | None | 0.000000000000 | 0.000000000000 | 0.000000000000 | right | 0.000000 |
| chain_len9_holdout | mc_plus_trl_log | None | 0.000000000000 | 0.131258278195 | 0.000000000000 | right | 0.000000 |
| chain_len9_holdout | successor_calibration_only | 0.0 | 0.391705823230 | 0.465607869047 | 0.000000000000 | right | 0.166667 |
| chain_len9_holdout | successor_distance_trl_log_lambda_0_00 | 0.0 | 0.391705823230 | 0.465607869047 | 0.000000000000 | right | 0.166667 |
| chain_len9_holdout | successor_distance_trl_log_lambda_0_25 | 0.25 | 0.000000000000 | 0.000000000000 | 0.000000000000 | right | 0.000000 |
| chain_len9_holdout | successor_distance_trl_log_lambda_0_50 | 0.5 | 0.000000000000 | 0.000000000000 | 0.000000000000 | right | 0.000000 |
| chain_len9_holdout | successor_distance_trl_log_lambda_0_75 | 0.75 | 0.000000000000 | 0.000000000000 | 0.000000000000 | right | 0.000000 |
| chain_len9_holdout | successor_distance_trl_log_lambda_1_00 | 1.0 | 0.000000000000 | 0.000000000000 | 0.000000000000 | right | 0.000000 |
| safe_optimal_matched | mc_supervised | None | 0.254016000000 | 0.045562500000 | 0.504000000000 | risky | 0.375000 |
| safe_optimal_matched | trl_raw | None | 0.029241000000 | 0.056250000000 | 0.504000000000 | risky | 0.000000 |
| safe_optimal_matched | trl_log | None | 0.000000000000 | 0.000000000000 | 0.000000000000 | safe | 0.250000 |
| safe_optimal_matched | mc_plus_trl_log | None | 0.000000000000 | 0.000000000000 | 0.000000000000 | safe | 0.250000 |
| safe_optimal_matched | successor_calibration_only | 0.0 | 0.254016000000 | 0.045562500000 | 0.504000000000 | risky | 0.375000 |
| safe_optimal_matched | successor_distance_trl_log_lambda_0_00 | 0.0 | 0.254016000000 | 0.045562500000 | 0.504000000000 | risky | 0.375000 |
| safe_optimal_matched | successor_distance_trl_log_lambda_0_25 | 0.25 | 0.000000000000 | 0.000000000000 | 0.000000000000 | safe | 0.250000 |
| safe_optimal_matched | successor_distance_trl_log_lambda_0_50 | 0.5 | 0.000000000000 | 0.000000000000 | 0.000000000000 | safe | 0.250000 |
| safe_optimal_matched | successor_distance_trl_log_lambda_0_75 | 0.75 | 0.000000000000 | 0.000000000000 | 0.000000000000 | safe | 0.250000 |
| safe_optimal_matched | successor_distance_trl_log_lambda_1_00 | 1.0 | 0.000000000000 | 0.000000000000 | 0.000000000000 | safe | 0.250000 |
| risk_optimal_matched | mc_supervised | None | 0.000000000000 | 0.045562500000 | 0.000000000000 | risky | 0.250000 |
| risk_optimal_matched | trl_raw | None | 0.000000000000 | 0.056250000000 | 0.000000000000 | risky | 0.000000 |
| risk_optimal_matched | trl_log | None | 0.000000000000 | 0.000000000000 | 0.000000000000 | risky | 0.250000 |
| risk_optimal_matched | mc_plus_trl_log | None | 0.000000000000 | 0.000000000000 | 0.000000000000 | risky | 0.250000 |
| risk_optimal_matched | successor_calibration_only | 0.0 | 0.000000000000 | 0.045562500000 | 0.000000000000 | risky | 0.250000 |
| risk_optimal_matched | successor_distance_trl_log_lambda_0_00 | 0.0 | 0.000000000000 | 0.045562500000 | 0.000000000000 | risky | 0.250000 |
| risk_optimal_matched | successor_distance_trl_log_lambda_0_25 | 0.25 | 0.000000000000 | 0.000000000000 | 0.000000000000 | risky | 0.250000 |
| risk_optimal_matched | successor_distance_trl_log_lambda_0_50 | 0.5 | 0.000000000000 | 0.000000000000 | 0.000000000000 | risky | 0.250000 |
| risk_optimal_matched | successor_distance_trl_log_lambda_0_75 | 0.75 | 0.000000000000 | 0.000000000000 | 0.000000000000 | risky | 0.250000 |
| risk_optimal_matched | successor_distance_trl_log_lambda_1_00 | 1.0 | 0.000000000000 | 0.000000000000 | 0.000000000000 | risky | 0.250000 |
| safe_optimal_lucky_only_stress | mc_supervised | None | 0.029241000000 | 0.129937500000 | 0.504000000000 | risky | 0.000000 |
| safe_optimal_lucky_only_stress | trl_raw | None | 0.029241000000 | 0.084375000000 | 0.504000000000 | risky | 0.000000 |
| safe_optimal_lucky_only_stress | trl_log | None | 0.029241000000 | 0.084375000000 | 0.504000000000 | risky | 0.000000 |
| safe_optimal_lucky_only_stress | mc_plus_trl_log | None | 0.029241000000 | 0.084375000000 | 0.504000000000 | risky | 0.000000 |
| safe_optimal_lucky_only_stress | successor_calibration_only | 0.0 | 0.029241000000 | 0.129937500000 | 0.504000000000 | risky | 0.000000 |
| safe_optimal_lucky_only_stress | successor_distance_trl_log_lambda_0_00 | 0.0 | 0.029241000000 | 0.129937500000 | 0.504000000000 | risky | 0.000000 |
| safe_optimal_lucky_only_stress | successor_distance_trl_log_lambda_0_25 | 0.25 | 0.029241000000 | 0.084375000000 | 0.504000000000 | risky | 0.000000 |
| safe_optimal_lucky_only_stress | successor_distance_trl_log_lambda_0_50 | 0.5 | 0.029241000000 | 0.084375000000 | 0.504000000000 | risky | 0.000000 |
| safe_optimal_lucky_only_stress | successor_distance_trl_log_lambda_0_75 | 0.75 | 0.029241000000 | 0.084375000000 | 0.504000000000 | risky | 0.000000 |
| safe_optimal_lucky_only_stress | successor_distance_trl_log_lambda_1_00 | 1.0 | 0.029241000000 | 0.084375000000 | 0.504000000000 | risky | 0.000000 |

## Audit Classification

- Chain raw exact: `True`
- Chain TRL-log exact: `True`
- Positive successor-distance evidence: `False`
- Negative equivalence evidence: `True`
- All improving lambdas equivalent to trl_log: `True`

## Interpretation

The audit found negative successor-distance evidence: improving lambdas reduced held-out error by matching trl_log within the predeclared tolerance, so this variant is not yet distinct from trl_log on these tabular diagnostics.

## Artifacts

- `research/sto_trl/artifacts/0005/run_lambda_equivalence_audit.py`
- `research/sto_trl/artifacts/0005/raw_metrics.json`
- `research/sto_trl/artifacts/0005/metrics.csv`
- `research/sto_trl/artifacts/0005/lambda_sweep.json`
- `research/sto_trl/artifacts/0005/equivalence_diagnostics.json`
- `research/sto_trl/artifacts/0005/successor_distance_tables.json`
- `research/sto_trl/artifacts/0005/distance_diagnostics.json`
- `research/sto_trl/artifacts/0005/label_or_pair_coverage.json`
- `research/sto_trl/artifacts/0005/offline_datasets.json`
- `research/sto_trl/artifacts/0005/transition_tables.json`
- `research/sto_trl/artifacts/0005/value_tables.json`

## Known Failures

- None.


## Latest review JSON

```json
{
  "allows_auto_continue": true,
  "evidence_checked": [
    "research/sto_trl/results/0005_result.json",
    "research/sto_trl/results/0005_summary.md",
    "research/sto_trl/artifacts/0005/ file listing",
    "research/sto_trl/artifacts/0005/run_lambda_equivalence_audit.py constants and setup",
    "python scripts/validate_artifacts.py --repo-root . --json research/sto_trl/results/0005_result.json --schema schemas/result.schema.json --check-result-artifacts",
    "git status --short"
  ],
  "experiment_id": "0005",
  "reasons": [
    "Required result, summary, and 0005 artifact files were produced, including raw metrics, CSV metrics, lambda sweep, equivalence diagnostics, distance diagnostics, datasets, transitions, and value tables.",
    "The result JSON validates against schemas/result.schema.json with artifact checks.",
    "The lambda sweep uses the predeclared weights [0.0, 0.25, 0.5, 0.75, 1.0] and reports calibration-only, trl_log, mc_plus_trl_log, and successor-distance variants on the same four scenarios.",
    "Equivalence diagnostics versus trl_log include the requested Q/value/action/MSE/regret/overestimation deltas by scenario and lambda.",
    "The interpretation is appropriately negative: improving successor-distance lambdas are reported as equivalent to trl_log within tolerance, so no distinct successor-distance win is claimed."
  ],
  "required_fixes": [],
  "risk_flags": [
    "Working tree contains pre-existing modified control/config/test files, including scripts/autoresearcher.py, so the no-control-file-edit criterion cannot be proven from git status alone.",
    "commands_run records copy, run, and validation commands, but not any manual edit steps used to adapt the copied 0004 script into the 0005 audit.",
    "A generated __pycache__/ directory exists under artifacts/0005; harmless but extra artifact noise.",
    "Supervisor should continue only treating 0005 as negative evidence for distinct successor-distance value, not as support for the prior positive 0004 interpretation."
  ],
  "verdict": "pass"
}
```


## Last decisions

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

## 0004_decision.json

```json
{
  "confidence": 0.82,
  "decision": "continue",
  "evidence": [
    "research/sto_trl/results/0003_result.json validates against schemas/result.schema.json with artifact checks.",
    "0003 status is completed with no known_failures and success_criteria_met=true.",
    "0003 aggregate metrics show chain held-out value MSE improved from MC 0.3917058232298766 to TRL-log and MC+TRL-log 2.9347503914472164e-34.",
    "0003 risky matched metrics show MC selected risky with policy_regret=0.504, raw TRL selected risky with policy_regret=0.504, while TRL-log and MC+TRL-log selected safe with zero policy regret.",
    "The 0003 review allows auto-continue but flags that TRL-log/raw are tabular transitive backups over observed transitions rather than the same supervised label budget as MC-only, so a calibration-only versus calibrated+transitive ablation is the right next test.",
    "The prototype plan's Milestone 3 calls for a first stochastic-calibrated variant: contrastive successor-distance or self-normalized successor score, Successor-distance + TRL-log, and comparison against calibration-only."
  ],
  "next_experiment": {
    "estimated_runtime_minutes": 25,
    "experiment_id": "0004",
    "failure_criteria": [
      "The successor-distance variant is not separately reported from existing trl_log or mc_plus_trl_log.",
      "Exact DP ground truth is missing for any evaluated scenario.",
      "The transitive term improves deterministic long-horizon MSE only by increasing risky-branch overestimation or by choosing safe in the matched risk-optimal scenario.",
      "The result omits calibration-only versus calibrated+transitive ablation metrics.",
      "The experiment relies on true transition probabilities, DP labels, neural networks, OGBench, large sweeps, downloads, or runtime over 30 minutes."
    ],
    "hypothesis": "A self-normalized successor-distance calibration with a log-space transitive relaxation will improve held-out long-horizon value estimates over calibration-only while preserving matched stochastic branch calibration, reducing raw TRL overestimation, and not simply avoiding risky actions when risk is truly optimal.",
    "objective": "Implement and test the first tabular stochastic-calibrated successor-distance variant, comparing calibration-only against successor-distance + TRL-log on the existing horizon-holdout and risky-shortcut diagnostics.",
    "required_outputs": [
      "research/sto_trl/artifacts/0004/run_successor_distance_ablation.py",
      "research/sto_trl/artifacts/0004/raw_metrics.json",
      "research/sto_trl/artifacts/0004/metrics.csv",
      "research/sto_trl/artifacts/0004/successor_distance_tables.json",
      "research/sto_trl/artifacts/0004/distance_diagnostics.json",
      "research/sto_trl/artifacts/0004/label_or_pair_coverage.json",
      "research/sto_trl/results/0004_result.json",
      "research/sto_trl/results/0004_summary.md"
    ],
    "success_criteria": [
      "Creates a self-contained prototype under research/sto_trl/artifacts/0004/ without editing prior results, schemas, AGENTS.md, scripts/autoresearcher.py, or environment files.",
      "Implements at least two new ablations: successor_calibration_only with lambda_tr=0 and successor_distance_trl_log with a small predeclared transitive weight or equivalent tabular update.",
      "Evaluates exact DP ground truth on a deterministic chain horizon-holdout scenario, a matched safe-optimal risky shortcut, and a matched risk-optimal risky shortcut.",
      "Includes one small biased-coverage boundary case, such as safe-optimal lucky-only, but labels it as a stress case rather than the sole success criterion.",
      "Compares against existing mc_supervised, trl_raw, trl_log, and mc_plus_trl_log on the same constructed datasets.",
      "Reports raw metrics by scenario and method, including held-out long-horizon value MSE, calibration error, overestimation, underestimation, policy regret, risky action selection rate, triangle violation rate or distance consistency diagnostics, and coverage diagnostics.",
      "Counts the result as positive only if successor_distance_trl_log improves held-out long-horizon MSE versus successor_calibration_only and does not increase matched risky-branch overestimation or policy regret versus calibration-only.",
      "Produces valid research/sto_trl/results/0004_result.json and research/sto_trl/results/0004_summary.md with exact commands run."
    ],
    "tasks_for_codex": [
      "Create research/sto_trl/artifacts/0004/ and adapt the 0003 harness into a successor-distance ablation script.",
      "Define the self-normalized successor score and distance tables explicitly in the artifact source and save learned score, distance, value, and Q tables.",
      "Run the chain horizon-holdout, matched safe-optimal risky shortcut, matched risk-optimal risky shortcut, and one biased safe-optimal boundary case.",
      "Evaluate mc_supervised, trl_raw, trl_log, mc_plus_trl_log, successor_calibration_only, and successor_distance_trl_log with fixed seeds or constructed trajectories.",
      "Save raw_metrics.json, metrics.csv, successor_distance_tables.json, distance_diagnostics.json, label_or_pair_coverage.json, offline_datasets.json, transition_tables.json, and value_tables.json under research/sto_trl/artifacts/0004/.",
      "Write research/sto_trl/results/0004_result.json and research/sto_trl/results/0004_summary.md, then validate the result JSON against schemas/result.schema.json with artifact checks."
    ]
  },
  "progress_score": 6,
  "rationale": "Experiment 0003 is a valid weak-pass result with useful evidence: log transitive backups recovered censored long-horizon tabular reachability and avoided raw TRL's matched risky-shortcut optimism. The remaining charter-critical question is whether a first stochastic-calibrated successor-distance style variant adds anything beyond empirical log backups and calibration-only baselines, without becoming conservative on risk-optimal cases. That is a small tabular Milestone 3 experiment, still within the initial scope.",
  "risks": [
    "A self-normalized successor variant may collapse to the same empirical log backup already tested; require saved value tables and method definitions that distinguish calibration-only from calibrated+transitive.",
    "No tabular method can infer missing stochastic outcomes without assumptions, so lucky-only or no-success regimes should be reported as boundary cases rather than hidden or overclaimed.",
    "A conservative variant can look good on safe-optimal shortcuts while failing risk-optimal shortcuts; include an anti-conservatism check.",
    "Keep this tabular and small; do not move to OGBench, neural networks, downloads, or broad sweeps yet."
  ]
}
```

## 0005_decision.json

```json
{
  "confidence": 0.8,
  "decision": "continue",
  "evidence": [
    "research/sto_trl/results/0004_result.json validates against schemas/result.schema.json with artifact checks.",
    "0004 success checks report successor_distance_improves_main_heldout_mse_vs_calibration_only=true and no matched policy-regret or Q-overestimation increase versus calibration-only.",
    "0004 aggregate metrics show successor_calibration_only main mean held-out MSE 0.21524060774329223 versus successor_distance_trl_log 9.782501304824055e-35.",
    "0004 matched safe-optimal metrics show successor_distance_trl_log selected safe with zero policy regret, while calibration-only selected risky with policy_regret=0.504.",
    "0004 matched risk-optimal metrics show successor_distance_trl_log selected risky with zero policy regret, so it did not simply avoid risk under matched coverage.",
    "The 0004 review flags two key weaknesses: successor_distance_trl_log is near-identical to trl_log in the main metrics, and self_normalize_successor_scores is an identity transform for scores already in [0,1].",
    "The 0004 lucky-only stress scenario remains a failure case: successor_distance_trl_log selected risky with policy_regret=0.504 under biased safe-optimal coverage."
  ],
  "next_experiment": {
    "estimated_runtime_minutes": 20,
    "experiment_id": "0005",
    "failure_criteria": [
      "The result compares successor_distance_trl_log only to calibration-only and omits equivalence diagnostics versus trl_log.",
      "The lambda sweep uses different trajectories, label censoring, or DP setup across methods.",
      "Exact DP ground truth is missing for any scenario.",
      "The experiment claims a successor-distance win when metrics are numerically identical to trl_log within the predeclared tolerance.",
      "The run expands to neural networks, OGBench, large sweeps, downloads, or exceeds 30 minutes."
    ],
    "hypothesis": "If the successor-distance formulation is meaningful rather than a relabeling of trl_log, then some predeclared lambda_tr value should change Q/value tables or policy behavior relative to trl_log while retaining lower held-out error than calibration-only and avoiding matched risky-branch overestimation. If all lambda_tr values collapse to trl_log or calibration-only, the successor-distance variant is not yet adding distinct evidence.",
    "objective": "Run a small successor-distance lambda and equivalence audit to determine whether successor_distance_trl_log has a distinct effect beyond trl_log and calibration-only on the existing tabular chain and risky-shortcut diagnostics.",
    "required_outputs": [
      "research/sto_trl/artifacts/0005/run_successor_lambda_equivalence.py",
      "research/sto_trl/artifacts/0005/raw_metrics.json",
      "research/sto_trl/artifacts/0005/metrics.csv",
      "research/sto_trl/artifacts/0005/lambda_sweep.json",
      "research/sto_trl/artifacts/0005/equivalence_diagnostics.json",
      "research/sto_trl/artifacts/0005/successor_distance_tables.json",
      "research/sto_trl/results/0005_result.json",
      "research/sto_trl/results/0005_summary.md"
    ],
    "success_criteria": [
      "Creates a self-contained artifact under research/sto_trl/artifacts/0005/ without editing prior results, schemas, AGENTS.md, scripts/autoresearcher.py, or environment files.",
      "Reuses the exact DP tabular scenarios from 0004: chain_len9_holdout, safe_optimal_matched, risk_optimal_matched, and safe_optimal_lucky_only_stress.",
      "Sweeps a tiny predeclared set of successor transitive weights, such as lambda_tr in [0.0, 0.25, 0.5, 0.75, 1.0], with fixed trajectories and update count.",
      "Reports calibration-only, trl_log, mc_plus_trl_log, and successor_distance_trl_log for every lambda on the same datasets.",
      "Saves explicit equivalence diagnostics versus trl_log, including max_abs_q_diff, max_abs_value_diff, action_diff_rate, heldout_mse_delta, policy_regret_delta, and q_overestimation_delta by scenario and lambda.",
      "Counts positive successor-distance evidence only if at least one lambda improves versus calibration-only and is not numerically equivalent to trl_log on the main scenarios, without increasing matched risky policy regret or Q overestimation.",
      "Counts negative evidence explicitly if all successor-distance lambdas are equivalent to trl_log within tolerance or only improve by matching trl_log.",
      "Produces valid research/sto_trl/results/0005_result.json and research/sto_trl/results/0005_summary.md with exact commands run."
    ],
    "tasks_for_codex": [
      "Create research/sto_trl/artifacts/0005/ and adapt the 0004 harness into a lambda/equivalence audit script.",
      "Parameterize successor_distance_trl_log by lambda_tr and run the predeclared small lambda set on the same constructed datasets.",
      "Compute and save per-scenario, per-lambda metrics plus direct table-difference diagnostics versus trl_log and calibration-only.",
      "Save raw_metrics.json, metrics.csv, lambda_sweep.json, equivalence_diagnostics.json, successor_distance_tables.json, distance_diagnostics.json, offline_datasets.json, transition_tables.json, and value_tables.json under research/sto_trl/artifacts/0005/.",
      "Write research/sto_trl/results/0005_result.json and research/sto_trl/results/0005_summary.md, then validate the result JSON against schemas/result.schema.json with artifact checks."
    ]
  },
  "progress_score": 6,
  "rationale": "Experiment 0004 is valid but only a weak positive for the successor-distance direction. It shows calibrated+transitive beats calibration-only on the tabular main scenarios, but the review and code indicate successor_calibration_only is effectively MC-supervised and successor_distance_trl_log is behaviorally near-identical to trl_log. The next cheap decisive experiment should audit whether the successor-distance formulation has any distinct effect across transitive weights before moving to function approximation or larger tasks.",
  "risks": [
    "Continuing without an equivalence audit could mistake ordinary trl_log behavior for evidence supporting a distinct successor-distance method.",
    "A lambda sweep can become low-value if it only repeats calibration-only comparisons; require explicit distance-to-trl_log diagnostics.",
    "No tabular method should be expected to solve missing-outcome lucky-only coverage without an uncertainty assumption, so that stress case should be used as a boundary diagnostic, not a sole success criterion.",
    "Do not move to OGBench, neural networks, or broad sweeps while the tabular method distinction is unresolved."
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

Use `0006` as the exact `next_experiment.experiment_id` if you choose continue.
