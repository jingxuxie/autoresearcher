# Reviewer Context: sto_trl

## Latest plan

# Experiment 0001

## Objective

Build and run a minimal tabular diagnostic for stochastic TRL covering deterministic chain sanity and one risky-shortcut stochastic MDP, with exact discounted-reachability DP ground truth and raw metrics saved.

## Hypothesis

A small tabular risky-shortcut MDP with offline lucky/unlucky outcomes will reveal whether raw deterministic-style TRL overestimates risky stochastic paths, while log-space or MC+TRL-log variants preserve deterministic behavior and improve calibration relative to MC-only or raw TRL.

## Success criteria

- Creates a reproducible prototype under research/sto_trl/artifacts/0001/ without modifying repository control scripts or schemas.
- Produces exact DP ground truth for the deterministic chain and risky-shortcut MDP.
- Compares MC supervised, TRL-raw, TRL-log, and MC+TRL-log on the same tiny offline datasets.
- Saves raw numeric metrics including overestimation error, underestimation error, long-horizon value MSE, policy regret, risky action selection rate, calibration error, and coverage diagnostics.
- Writes valid research/sto_trl/results/0001_result.json and research/sto_trl/results/0001_summary.md with exact commands run.

## Failure criteria

- No exact DP ground truth is implemented for the stochastic diagnostic.
- The deterministic chain does not recover shortest-path or discounted-reachability structure for raw/log variants.
- The result only reports training loss or prose without raw value and policy metrics.
- The risky-shortcut dataset lacks coverage of lucky and unlucky stochastic outcomes.
- The run requires large downloads, OGBench, AntMaze, neural-network training, or exceeds the 30 minute executor budget.

## Estimated runtime

<= 20 minutes

## Tasks for Codex

- Create a small self-contained tabular prototype in research/sto_trl/artifacts/0001/.
- Implement deterministic chain and one risky-shortcut versus safe-route stochastic MDP with exact transition tables.
- Implement exact discounted reachability DP and greedy policy evaluation from the DP values.
- Generate tiny offline trajectories with explicit coverage diagnostics for states, actions, goals, and risky success/failure outcomes.
- Implement MC supervised, TRL-raw product backup, TRL-log additive backup, and MC+TRL-log using simple tabular tables and fixed small update counts.
- Run the experiment in conda environment autoresearcher_sto_trl with deterministic seeds and save raw metrics as JSON or CSV under research/sto_trl/artifacts/0001/.
- Write research/sto_trl/results/0001_result.json matching schemas/result.schema.json and research/sto_trl/results/0001_summary.md, including exact commands run.

## Required outputs

- `research/sto_trl/results/0001_result.json`
- `research/sto_trl/results/0001_summary.md`
- `research/sto_trl/artifacts/0001/`


## Latest plan JSON

```json
{
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
    "research/sto_trl/results/0001_result.json",
    "research/sto_trl/results/0001_summary.md",
    "research/sto_trl/artifacts/0001/"
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


## Artifact paths

- `/home/eston/autoresearcher/research/sto_trl/artifacts/0001`


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
