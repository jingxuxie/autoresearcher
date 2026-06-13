# Reviewer Context: sto_trl

## Latest plan

# Experiment 0003

## Objective

Run a small tabular horizon-holdout experiment that censors long-horizon goal labels during training and tests whether TRL-log or MC+TRL-log can recover long-horizon discounted reachability better than MC-only while retaining matched stochastic risky-branch calibration.

## Hypothesis

With only short-horizon MC labels, MC-supervised estimates will underpredict held-out long-horizon goals, while log-space transitive backups, especially MC+TRL-log, will propagate calibrated short-horizon information to longer horizons without raw TRL's stochastic risky-path optimism under matched branch coverage.

## Success criteria

- Creates a self-contained prototype under research/sto_trl/artifacts/0003/ without editing prior experiment artifacts, schemas, AGENTS.md, or scripts/autoresearcher.py.
- Includes a deterministic chain longer than 0001 plus at least one matched-coverage risky-shortcut MDP with exact DP ground truth.
- Explicitly censors MC/calibration training labels beyond a small horizon cutoff, such as 2 or 3 steps, and saves train/eval state-action-goal pair coverage by horizon bin.
- Compares mc_supervised, trl_raw, trl_log, and mc_plus_trl_log using the same trajectories and the same censored label budget.
- Reports raw metrics by method and horizon bin, including held-out long-horizon value MSE, overestimation, underestimation, calibration error, policy regret, risky action selection rate, and coverage diagnostics.
- Counts the experiment as positive only if trl_log or mc_plus_trl_log improves held-out long-horizon value MSE versus MC-only while raw/log deterministic chain sanity remains valid and matched risky calibration does not select the wrong risky action.
- Produces valid research/sto_trl/results/0003_result.json and research/sto_trl/results/0003_summary.md with exact commands run.

## Failure criteria

- Long-horizon labels are accidentally used in MC supervised targets or calibration anchors.
- The experiment lacks exact DP ground truth for every evaluated MDP.
- The result reports aggregate metrics without horizon-bin breakdown or train/eval coverage diagnostics.
- TRL-log or MC+TRL-log fails the deterministic chain sanity check under the censored-label setup.
- The stochastic risky evaluation uses biased coverage only, making calibration failures ambiguous rather than controlled.
- The run expands to neural networks, OGBench, large sweeps, downloads, or exceeds 30 minutes.

## Estimated runtime

<= 20 minutes

## Tasks for Codex

- Create research/sto_trl/artifacts/0003/ and adapt the 0002 harness into a horizon-holdout script.
- Implement a longer deterministic chain and a matched-coverage risky-shortcut scenario with exact discounted-reachability DP evaluation.
- Add a predeclared horizon cutoff for training labels, while still allowing transitive/log backups to use observed short transitions from trajectories.
- Run mc_supervised, trl_raw, trl_log, and mc_plus_trl_log on the censored-label datasets with fixed update counts and deterministic seeds or constructed trajectories.
- Save raw_metrics.json, metrics.csv, label_coverage_by_horizon.json, offline_datasets.json, transition_tables.json, and value_tables.json under research/sto_trl/artifacts/0003/.
- Write research/sto_trl/results/0003_result.json and research/sto_trl/results/0003_summary.md, then validate the result JSON against schemas/result.schema.json with artifact checks.

## Required outputs

- `research/sto_trl/results/0003_result.json`
- `research/sto_trl/results/0003_summary.md`
- `research/sto_trl/artifacts/0003/`


## Latest plan JSON

```json
{
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
    "research/sto_trl/results/0003_result.json",
    "research/sto_trl/results/0003_summary.md",
    "research/sto_trl/artifacts/0003/"
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


## Artifact paths

- `/home/eston/autoresearcher/research/sto_trl/artifacts/0001`
- `/home/eston/autoresearcher/research/sto_trl/artifacts/0002`
- `/home/eston/autoresearcher/research/sto_trl/artifacts/0003`


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
