# Reviewer Context: sto_trl

## Latest plan

# Experiment 0004

## Objective

Implement and test the first tabular stochastic-calibrated successor-distance variant, comparing calibration-only against successor-distance + TRL-log on the existing horizon-holdout and risky-shortcut diagnostics.

## Hypothesis

A self-normalized successor-distance calibration with a log-space transitive relaxation will improve held-out long-horizon value estimates over calibration-only while preserving matched stochastic branch calibration, reducing raw TRL overestimation, and not simply avoiding risky actions when risk is truly optimal.

## Success criteria

- Creates a self-contained prototype under research/sto_trl/artifacts/0004/ without editing prior results, schemas, AGENTS.md, scripts/autoresearcher.py, or environment files.
- Implements at least two new ablations: successor_calibration_only with lambda_tr=0 and successor_distance_trl_log with a small predeclared transitive weight or equivalent tabular update.
- Evaluates exact DP ground truth on a deterministic chain horizon-holdout scenario, a matched safe-optimal risky shortcut, and a matched risk-optimal risky shortcut.
- Includes one small biased-coverage boundary case, such as safe-optimal lucky-only, but labels it as a stress case rather than the sole success criterion.
- Compares against existing mc_supervised, trl_raw, trl_log, and mc_plus_trl_log on the same constructed datasets.
- Reports raw metrics by scenario and method, including held-out long-horizon value MSE, calibration error, overestimation, underestimation, policy regret, risky action selection rate, triangle violation rate or distance consistency diagnostics, and coverage diagnostics.
- Counts the result as positive only if successor_distance_trl_log improves held-out long-horizon MSE versus successor_calibration_only and does not increase matched risky-branch overestimation or policy regret versus calibration-only.
- Produces valid research/sto_trl/results/0004_result.json and research/sto_trl/results/0004_summary.md with exact commands run.

## Failure criteria

- The successor-distance variant is not separately reported from existing trl_log or mc_plus_trl_log.
- Exact DP ground truth is missing for any evaluated scenario.
- The transitive term improves deterministic long-horizon MSE only by increasing risky-branch overestimation or by choosing safe in the matched risk-optimal scenario.
- The result omits calibration-only versus calibrated+transitive ablation metrics.
- The experiment relies on true transition probabilities, DP labels, neural networks, OGBench, large sweeps, downloads, or runtime over 30 minutes.

## Estimated runtime

<= 25 minutes

## Tasks for Codex

- Create research/sto_trl/artifacts/0004/ and adapt the 0003 harness into a successor-distance ablation script.
- Define the self-normalized successor score and distance tables explicitly in the artifact source and save learned score, distance, value, and Q tables.
- Run the chain horizon-holdout, matched safe-optimal risky shortcut, matched risk-optimal risky shortcut, and one biased safe-optimal boundary case.
- Evaluate mc_supervised, trl_raw, trl_log, mc_plus_trl_log, successor_calibration_only, and successor_distance_trl_log with fixed seeds or constructed trajectories.
- Save raw_metrics.json, metrics.csv, successor_distance_tables.json, distance_diagnostics.json, label_or_pair_coverage.json, offline_datasets.json, transition_tables.json, and value_tables.json under research/sto_trl/artifacts/0004/.
- Write research/sto_trl/results/0004_result.json and research/sto_trl/results/0004_summary.md, then validate the result JSON against schemas/result.schema.json with artifact checks.

## Required outputs

- `research/sto_trl/results/0004_result.json`
- `research/sto_trl/results/0004_summary.md`
- `research/sto_trl/artifacts/0004/`


## Latest plan JSON

```json
{
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
    "research/sto_trl/results/0004_result.json",
    "research/sto_trl/results/0004_summary.md",
    "research/sto_trl/artifacts/0004/"
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
}
```


## Latest result JSON

```json
{
  "artifacts": [
    "research/sto_trl/artifacts/0004/run_successor_distance.py",
    "research/sto_trl/artifacts/0004/raw_metrics.json",
    "research/sto_trl/artifacts/0004/metrics.csv",
    "research/sto_trl/artifacts/0004/successor_distance_tables.json",
    "research/sto_trl/artifacts/0004/distance_diagnostics.json",
    "research/sto_trl/artifacts/0004/label_or_pair_coverage.json",
    "research/sto_trl/artifacts/0004/offline_datasets.json",
    "research/sto_trl/artifacts/0004/transition_tables.json",
    "research/sto_trl/artifacts/0004/value_tables.json"
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
  "claim_tested": "A self-normalized successor-distance calibration with log-space transitive relaxation improves held-out reachability versus calibration-only without increasing matched risky overestimation or avoiding truly optimal risky actions.",
  "commands_run": [
    "mkdir -p research/sto_trl/artifacts/0004 research/sto_trl/results && cp research/sto_trl/artifacts/0003/run_horizon_holdout.py research/sto_trl/artifacts/0004/run_successor_distance.py",
    "conda run -n autoresearcher_sto_trl python research/sto_trl/artifacts/0004/run_successor_distance.py",
    "conda run -n autoresearcher_sto_trl python scripts/validate_artifacts.py --repo-root . --json research/sto_trl/results/0004_result.json --schema schemas/result.schema.json --check-result-artifacts"
  ],
  "experiment_id": "0004",
  "interpretation": "The successor-distance transitive relaxation improved main held-out long-horizon value MSE over calibration-only. On matched safe-optimal risky coverage it selected safe with no policy-regret increase versus calibration-only, and on matched risk-optimal coverage it selected risky, so the effect was not simple conservative avoidance. The lucky-only stress case remains a biased-coverage failure case rather than a success criterion.",
  "known_failures": [],
  "metrics": {
    "aggregate": {
      "risk_matched_successor_calibration_only_policy_regret": 0.0,
      "risk_matched_successor_distance_trl_log_policy_regret": 0.0,
      "safe_lucky_stress_successor_distance_action": "risky",
      "safe_matched_successor_calibration_only_policy_regret": 0.5040000000000001,
      "safe_matched_successor_distance_trl_log_policy_regret": 0.0,
      "successor_calibration_only_main_mean_heldout_mse": 0.21524060774329223,
      "successor_distance_trl_log_main_mean_heldout_mse": 9.782501304824055e-35
    },
    "experiment_id": "0004",
    "gamma": 0.9,
    "label_horizon_cutoff": 2,
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
          "successor_distance_trl_log": {
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
          "successor_distance_trl_log": {
            "anchor": "self_normalized_censored_successor_calibration",
            "lambda_tr": 0.75,
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
          "successor_distance_trl_log": {
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
          "successor_distance_trl_log": {
            "anchor": "self_normalized_censored_successor_calibration",
            "lambda_tr": 0.75,
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
          "successor_distance_trl_log": {
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
          "successor_distance_trl_log": {
            "anchor": "self_normalized_censored_successor_calibration",
            "lambda_tr": 0.75,
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
          "successor_distance_trl_log": {
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
          "successor_distance_trl_log": {
            "anchor": "self_normalized_censored_successor_calibration",
            "lambda_tr": 0.75,
            "relaxation": "distance_space_geometric_interpolation"
          }
        }
      }
    },
    "success_checks": {
      "chain_raw_exact": true,
      "chain_trl_log_exact": true,
      "success_criteria_met": true,
      "successor_distance_improves_main_heldout_mse_vs_calibration_only": true,
      "successor_distance_no_matched_policy_regret_increase_vs_calibration_only": true,
      "successor_distance_no_matched_q_overestimation_increase_vs_calibration_only": true,
      "successor_distance_selects_risky_when_risk_optimal": true,
      "successor_distance_selects_safe_when_safe_optimal_matched": true
    },
    "successor_lambda_tr": 0.75,
    "update_steps": 32
  },
  "next_questions": [
    "How sensitive is the successor-distance result to lambda_tr?",
    "Can biased lucky-only coverage be detected by uncertainty diagnostics before applying transitive relaxation?",
    "Does distance-space interpolation remain stable with sampled goals and function approximation?"
  ],
  "status": "completed"
}
```


## Latest summary

# Experiment 0004 Summary

## Objective

Test successor-distance calibration-only versus successor-distance + TRL-log on horizon holdout and stochastic risky shortcuts.

## Commands Run

```bash
mkdir -p research/sto_trl/artifacts/0004 research/sto_trl/results && cp research/sto_trl/artifacts/0003/run_horizon_holdout.py research/sto_trl/artifacts/0004/run_successor_distance.py
conda run -n autoresearcher_sto_trl python research/sto_trl/artifacts/0004/run_successor_distance.py
conda run -n autoresearcher_sto_trl python scripts/validate_artifacts.py --repo-root . --json research/sto_trl/results/0004_result.json --schema schemas/result.schema.json --check-result-artifacts
```

## Setup

- Discount: `0.9`
- Label horizon cutoff: `2`
- Fixed backup iterations: `32`
- Successor transitive weight: `0.75`
- Main scenarios: chain holdout, matched safe-optimal risky shortcut, matched risk-optimal risky shortcut.
- Stress scenario: safe-optimal lucky-only risky shortcut.

## Main Metrics

| Scenario | Method | Held-out MSE | Q calibration | Policy regret | Action | Triangle violation |
| --- | --- | ---: | ---: | ---: | --- | ---: |
| chain_len9_holdout | mc_supervised | 0.391705823230 | 0.465607869047 | 0.000000000000 | right | 0.166667 |
| chain_len9_holdout | trl_raw | 0.000000000000 | 0.000000000000 | 0.000000000000 | right | 0.000000 |
| chain_len9_holdout | trl_log | 0.000000000000 | 0.000000000000 | 0.000000000000 | right | 0.000000 |
| chain_len9_holdout | mc_plus_trl_log | 0.000000000000 | 0.131258278195 | 0.000000000000 | right | 0.000000 |
| chain_len9_holdout | successor_calibration_only | 0.391705823230 | 0.465607869047 | 0.000000000000 | right | 0.166667 |
| chain_len9_holdout | successor_distance_trl_log | 0.000000000000 | 0.000000000000 | 0.000000000000 | right | 0.000000 |
| safe_optimal_matched | mc_supervised | 0.254016000000 | 0.045562500000 | 0.504000000000 | risky | 0.375000 |
| safe_optimal_matched | trl_raw | 0.029241000000 | 0.056250000000 | 0.504000000000 | risky | 0.000000 |
| safe_optimal_matched | trl_log | 0.000000000000 | 0.000000000000 | 0.000000000000 | safe | 0.250000 |
| safe_optimal_matched | mc_plus_trl_log | 0.000000000000 | 0.000000000000 | 0.000000000000 | safe | 0.250000 |
| safe_optimal_matched | successor_calibration_only | 0.254016000000 | 0.045562500000 | 0.504000000000 | risky | 0.375000 |
| safe_optimal_matched | successor_distance_trl_log | 0.000000000000 | 0.000000000000 | 0.000000000000 | safe | 0.250000 |
| risk_optimal_matched | mc_supervised | 0.000000000000 | 0.045562500000 | 0.000000000000 | risky | 0.250000 |
| risk_optimal_matched | trl_raw | 0.000000000000 | 0.056250000000 | 0.000000000000 | risky | 0.000000 |
| risk_optimal_matched | trl_log | 0.000000000000 | 0.000000000000 | 0.000000000000 | risky | 0.250000 |
| risk_optimal_matched | mc_plus_trl_log | 0.000000000000 | 0.000000000000 | 0.000000000000 | risky | 0.250000 |
| risk_optimal_matched | successor_calibration_only | 0.000000000000 | 0.045562500000 | 0.000000000000 | risky | 0.250000 |
| risk_optimal_matched | successor_distance_trl_log | 0.000000000000 | 0.000000000000 | 0.000000000000 | risky | 0.250000 |
| safe_optimal_lucky_only_stress | mc_supervised | 0.029241000000 | 0.129937500000 | 0.504000000000 | risky | 0.000000 |
| safe_optimal_lucky_only_stress | trl_raw | 0.029241000000 | 0.084375000000 | 0.504000000000 | risky | 0.000000 |
| safe_optimal_lucky_only_stress | trl_log | 0.029241000000 | 0.084375000000 | 0.504000000000 | risky | 0.000000 |
| safe_optimal_lucky_only_stress | mc_plus_trl_log | 0.029241000000 | 0.084375000000 | 0.504000000000 | risky | 0.000000 |
| safe_optimal_lucky_only_stress | successor_calibration_only | 0.029241000000 | 0.129937500000 | 0.504000000000 | risky | 0.000000 |
| safe_optimal_lucky_only_stress | successor_distance_trl_log | 0.029241000000 | 0.084375000000 | 0.504000000000 | risky | 0.000000 |

## Success Checks

- Chain raw exact: `True`
- Chain TRL-log exact: `True`
- Successor-distance improves main held-out MSE vs calibration-only: `True`
- No matched policy-regret increase vs calibration-only: `True`
- No matched Q-overestimation increase vs calibration-only: `True`
- Risk-optimal matched scenario selects risky: `True`
- Safe-optimal matched scenario selects safe: `True`

## Interpretation

The successor-distance transitive relaxation improved main held-out long-horizon value MSE over calibration-only. On matched safe-optimal risky coverage it selected safe with no policy-regret increase versus calibration-only, and on matched risk-optimal coverage it selected risky, so the effect was not simple conservative avoidance. The lucky-only stress case remains a biased-coverage failure case rather than a success criterion.

## Artifacts

- `research/sto_trl/artifacts/0004/run_successor_distance.py`
- `research/sto_trl/artifacts/0004/raw_metrics.json`
- `research/sto_trl/artifacts/0004/metrics.csv`
- `research/sto_trl/artifacts/0004/successor_distance_tables.json`
- `research/sto_trl/artifacts/0004/distance_diagnostics.json`
- `research/sto_trl/artifacts/0004/label_or_pair_coverage.json`
- `research/sto_trl/artifacts/0004/offline_datasets.json`
- `research/sto_trl/artifacts/0004/transition_tables.json`
- `research/sto_trl/artifacts/0004/value_tables.json`

## Known Failures

- None.


## Artifact paths

- `/home/eston/autoresearcher/research/sto_trl/artifacts/0001`
- `/home/eston/autoresearcher/research/sto_trl/artifacts/0002`
- `/home/eston/autoresearcher/research/sto_trl/artifacts/0003`
- `/home/eston/autoresearcher/research/sto_trl/artifacts/0004`


## Review schema

```json
{
  "type": "object",
  "properties": {
    "experiment_id": { "type": "string" },
    "verdict": {
      "type": "string",
      "enum": ["pass", "weak_pass", "fail", "needs_human"]
    },
    "allows_auto_continue": {
      "type": "boolean"
    },
    "reasons": {
      "type": "array",
      "items": { "type": "string" }
    },
    "evidence_checked": {
      "type": "array",
      "items": { "type": "string" }
    },
    "required_fixes": {
      "type": "array",
      "items": { "type": "string" }
    },
    "risk_flags": {
      "type": "array",
      "items": { "type": "string" }
    }
  },
  "required": [
    "experiment_id",
    "verdict",
    "allows_auto_continue",
    "reasons",
    "evidence_checked",
    "required_fixes",
    "risk_flags"
  ],
  "additionalProperties": false
}
```
