# Reviewer Context: sto_trl

## Latest plan

# Experiment 0009

## Objective

Run a compact transition-level posterior model-DP baseline audit on representative regimes from the 0008 identifiability grid, establishing what empirical, Bayesian, quantile, and robust transition models can solve before adding transitive/posterior TRL variants.

## Hypothesis

Transition-level uncertainty baselines will explain most recoverable performance in finite-coverage risky-shortcut regimes: posterior mean, posterior quantile, and robust confidence-set DP should improve regret versus raw TRL and empirical TRL-log in prior-dependent or lucky-only cells while preserving matched safe-optimal and matched risk-optimal choices. Any remaining failures should identify where explicit priors or future transitive propagation are necessary.

## Success criteria

- Creates a self-contained artifact under research/sto_trl/artifacts/0009/ without editing prior results, schemas, AGENTS.md, scripts/autoresearcher.py, or environment files.
- Selects a small representative subset from the 0008 grid covering matched-identifiable, lucky-only, no-success, ambiguous, prior-dependent, safe-optimal, and risk-optimal regimes.
- Implements and reports empirical model DP, Bayesian posterior mean DP, posterior lower and upper quantile DP, and robust confidence-set DP, alongside raw TRL, TRL-log, and empirical risky-value baselines.
- Uses exact DP ground truth only for evaluation, not as a training or decision input.
- Reports regime-stratified action accuracy, mean policy regret, risky-action selection rate, Q overestimation, calibration error, and prior-dependence diagnostics.
- Counts positive evidence only if transition-level posterior or robust baselines reduce regret versus TRL-log in prior-dependent or lucky-only regimes while not simply selecting safe everywhere and while preserving matched risk-optimal action choice.
- Explicitly states whether transition uncertainty alone matches or beats the current stochastic TRL variants, setting a baseline for any future transitive/posterior TRL experiment.
- Produces valid research/sto_trl/results/0009_result.json and research/sto_trl/results/0009_summary.md with exact commands run.

## Failure criteria

- The experiment uses exact DP values or true transition probabilities as decision inputs rather than evaluation ground truth.
- The selected subset omits anti-conservatism checks, especially matched risk-optimal and no-success risk-optimal regimes.
- The result reports only aggregate averages and omits regime-stratified metrics.
- The posterior or robust methods are not compared against both empirical transition DP and TRL-log.
- The experiment claims a stochastic TRL win without beating or matching simple transition-model DP baselines.
- The run expands to neural networks, continuous control, OGBench, large downloads, broad sweeps, or exceeds 30 minutes.

## Estimated runtime

<= 25 minutes

## Tasks for Codex

- Create research/sto_trl/artifacts/0009/ and implement a small transition_posterior_baselines.py script, reusing 0008 grid definitions where practical.
- Select and save a representative evaluation subset from 0008 with explicit regime labels and coverage diagnostics.
- Implement empirical model DP, beta-binomial posterior mean DP, posterior lower and upper quantile DP, and a simple robust confidence-set DP for the risky shortcut family.
- Evaluate raw TRL, TRL-log, empirical risky-value, and the transition-posterior baselines against exact DP ground truth on the same subset.
- Save raw_metrics.json, metrics.csv, regime_summary.csv, posterior_diagnostics.json, selected_grid_cells.json, coverage_diagnostics.json, transition_tables.json, and value_tables.json under research/sto_trl/artifacts/0009/.
- Write research/sto_trl/results/0009_result.json and research/sto_trl/results/0009_summary.md, then validate the result JSON with scripts/validate_artifacts.py and artifact checks.

## Required outputs

- `research/sto_trl/results/0009_result.json`
- `research/sto_trl/results/0009_summary.md`
- `research/sto_trl/artifacts/0009/`


## Latest plan JSON

```json
{
  "estimated_runtime_minutes": 25,
  "experiment_id": "0009",
  "failure_criteria": [
    "The experiment uses exact DP values or true transition probabilities as decision inputs rather than evaluation ground truth.",
    "The selected subset omits anti-conservatism checks, especially matched risk-optimal and no-success risk-optimal regimes.",
    "The result reports only aggregate averages and omits regime-stratified metrics.",
    "The posterior or robust methods are not compared against both empirical transition DP and TRL-log.",
    "The experiment claims a stochastic TRL win without beating or matching simple transition-model DP baselines.",
    "The run expands to neural networks, continuous control, OGBench, large downloads, broad sweeps, or exceeds 30 minutes."
  ],
  "hypothesis": "Transition-level uncertainty baselines will explain most recoverable performance in finite-coverage risky-shortcut regimes: posterior mean, posterior quantile, and robust confidence-set DP should improve regret versus raw TRL and empirical TRL-log in prior-dependent or lucky-only cells while preserving matched safe-optimal and matched risk-optimal choices. Any remaining failures should identify where explicit priors or future transitive propagation are necessary.",
  "objective": "Run a compact transition-level posterior model-DP baseline audit on representative regimes from the 0008 identifiability grid, establishing what empirical, Bayesian, quantile, and robust transition models can solve before adding transitive/posterior TRL variants.",
  "required_outputs": [
    "research/sto_trl/results/0009_result.json",
    "research/sto_trl/results/0009_summary.md",
    "research/sto_trl/artifacts/0009/"
  ],
  "success_criteria": [
    "Creates a self-contained artifact under research/sto_trl/artifacts/0009/ without editing prior results, schemas, AGENTS.md, scripts/autoresearcher.py, or environment files.",
    "Selects a small representative subset from the 0008 grid covering matched-identifiable, lucky-only, no-success, ambiguous, prior-dependent, safe-optimal, and risk-optimal regimes.",
    "Implements and reports empirical model DP, Bayesian posterior mean DP, posterior lower and upper quantile DP, and robust confidence-set DP, alongside raw TRL, TRL-log, and empirical risky-value baselines.",
    "Uses exact DP ground truth only for evaluation, not as a training or decision input.",
    "Reports regime-stratified action accuracy, mean policy regret, risky-action selection rate, Q overestimation, calibration error, and prior-dependence diagnostics.",
    "Counts positive evidence only if transition-level posterior or robust baselines reduce regret versus TRL-log in prior-dependent or lucky-only regimes while not simply selecting safe everywhere and while preserving matched risk-optimal action choice.",
    "Explicitly states whether transition uncertainty alone matches or beats the current stochastic TRL variants, setting a baseline for any future transitive/posterior TRL experiment.",
    "Produces valid research/sto_trl/results/0009_result.json and research/sto_trl/results/0009_summary.md with exact commands run."
  ],
  "tasks_for_codex": [
    "Create research/sto_trl/artifacts/0009/ and implement a small transition_posterior_baselines.py script, reusing 0008 grid definitions where practical.",
    "Select and save a representative evaluation subset from 0008 with explicit regime labels and coverage diagnostics.",
    "Implement empirical model DP, beta-binomial posterior mean DP, posterior lower and upper quantile DP, and a simple robust confidence-set DP for the risky shortcut family.",
    "Evaluate raw TRL, TRL-log, empirical risky-value, and the transition-posterior baselines against exact DP ground truth on the same subset.",
    "Save raw_metrics.json, metrics.csv, regime_summary.csv, posterior_diagnostics.json, selected_grid_cells.json, coverage_diagnostics.json, transition_tables.json, and value_tables.json under research/sto_trl/artifacts/0009/.",
    "Write research/sto_trl/results/0009_result.json and research/sto_trl/results/0009_summary.md, then validate the result JSON with scripts/validate_artifacts.py and artifact checks."
  ]
}
```


## Latest result summary

```json
{
  "_source": "/home/eston/autoresearcher/research/sto_trl/results/0009_result.json",
  "artifacts": {
    "_type": "list",
    "first_items": [
      "research/sto_trl/artifacts/0009/transition_posterior_baselines.py",
      "research/sto_trl/artifacts/0009/raw_metrics.json",
      "research/sto_trl/artifacts/0009/metrics.csv"
    ],
    "length": 9
  },
  "baseline_metrics": {
    "empirical_model_dp": {
      "action_accuracy": 0.5,
      "mean_calibration_error": 0.26296875,
      "mean_policy_regret": 0.10901250000000001,
      "mean_q_overestimation": 0.11671875000000001,
      "mean_q_underestimation": 0.14625000000000002,
      "num_cells": 8,
      "risky_action_selection_rate": 0.375
    },
    "empirical_risky_value": {
      "action_accuracy": 0.5,
      "mean_calibration_error": 0.26296875,
      "mean_policy_regret": 0.10901250000000001,
      "mean_q_overestimation": 0.11671875000000001,
      "mean_q_underestimation": 0.14625000000000002,
      "num_cells": 8,
      "risky_action_selection_rate": 0.375
    },
    "posterior_lower_q10_dp_beta_1_1": {
      "action_accuracy": 0.75,
      "mean_calibration_error": 0.29698125000000003,
      "mean_policy_regret": 0.02024999999999999,
      "mean_q_overestimation": 0.04286250000000001,
      "mean_q_underestimation": 0.25411875,
      "num_cells": 8,
      "risky_action_selection_rate": 0.125
    },
    "posterior_mean_dp_beta_1_1": {
      "action_accuracy": 0.625,
      "mean_calibration_error": 0.23375,
      "mean_policy_regret": 0.08325,
      "mean_q_overestimation": 0.09,
      "mean_q_underestimation": 0.14375000000000004,
      "num_cells": 8,
      "risky_action_selection_rate": 0.25
    },
    "raw_trl": {
      "action_accuracy": 0.375,
      "mean_calibration_error": 0.405,
      "mean_policy_regret": 0.16863750000000002,
      "mean_q_overestimation": 0.275625,
      "mean_q_underestimation": 0.12937500000000002,
      "num_cells": 8,
      "risky_action_selection_rate": 0.75
    },
    "robust_lcb_dp_delta_0_2": {
      "action_accuracy": 0.625,
      "mean_calibration_error": 0.3772944862234698,
      "mean_policy_regret": 0.039487499999999995,
      "mean_q_overestimation": 0.024019705510612114,
      "mean_q_underestimation": 0.3532747807128576,
      "num_cells": 8,
      "risky_action_selection_rate": 0.0
    },
    "trl_log": {
      "action_accuracy": 0.5,
      "mean_calibration_error": 0.26296875,
      "mean_policy_regret": 0.10901250000000001,
      "mean_q_overestimation": 0.11671875000000001,
      "mean_q_underestimation": 0.14625000000000002,
      "num_cells": 8,
      "risky_action_selection_rate": 0.375
    }
  },
  "claim_tested": "Transition-level empirical, Bayesian, quantile, and robust model-DP baselines can explain which representative finite-coverage risky-shortcut regimes are recoverable before adding posterior TRL variants.",
  "experiment_id": "0009",
  "interpretation": "On the representative 0008 subset, transition-level uncertainty baselines explain the recoverable finite-coverage behavior: posterior_lower_q10_dp_beta_1_1 reduces mean target-regime regret versus TRL-log by -0.177525000000, while at least one posterior baseline preserves the matched risk-optimal action. No evaluated transition baseline solved risk_optimal_no_success; explicit priors or additional coverage remain necessary. Empirical model DP, empirical risky value, and TRL-log are identical on... [trimmed]",
  "known_failures": [
    "Risk-optimal no-success remains unsolved from counts alone."
  ],
  "metrics": {
    "best_transition_uncertainty_method": "posterior_lower_q10_dp_beta_1_1",
    "best_transition_uncertainty_target_regret_delta_vs_trl_log": -0.17752500000000004,
    "chain_guard": {
      "by_distance": {
        "_type": "object",
        "key_count": 8,
        "keys": [
          "1",
          "2",
          "3",
          "4",
          "5",
          "6",
          "7",
          "8"
        ]
      },
      "chain_length": 9,
      "passed": true,
      "raw_trl_max_abs_error": 0.0,
      "trl_log_max_abs_error": 0.0
    },
    "coverage_diagnostics": {
      "num_method_rows": 72,
      "num_selected_cells": 8,
      "regime_label_counts": {
        "_type": "object",
        "key_count": 8,
        "keys": [
          "ambiguous_risk_optimal",
          "ambiguous_safe_optimal",
          "lucky_only_safe_optimal",
          "matched_identifiable_safe_optimal",
          "matched_risk_optimal",
          "no_success_risk_optimal",
          "no_success_safe_optimal",
          "prior_dependent_safe_optimal"
        ]
      },
      "risky_sample_counts": {
        "_type": "object",
        "key_count": 8,
        "keys": [
          "ambiguous_risk_optimal_boundary",
          "ambiguous_safe_optimal_boundary",
          "matched_identifiable_safe_optimal",
          "matched_risk_optimal_high_coverage",
          "prior_dependent_safe_optimal",
          "risk_no_success_stress",
          "safe_lucky_only_stress",
          "safe_no_success_identifiable"
        ]
      },
      "tag_counts": {
        "_type": "object",
        "key_count": 8,
        "keys": [
          "ambiguous",
          "identifiable",
          "lucky_only",
          "matched",
          "no_success",
          "prior_dependent",
          "risky_optimal",
          "safe_optimal"
        ]
      },
      "target_regime_labels_for_posterior_delta": {
        "_type": "list",
        "length": 4
      }
    },
    "matched_risk_summary": {
      "empirical_model_dp": {
        "_type": "object",
        "key_count": 7,
        "keys": [
          "action_accuracy",
          "mean_calibration_error",
          "mean_policy_regret",
          "mean_q_overestimation",
          "mean_q_underestimation",
          "num_cells",
          "risky_action_selection_rate"
        ]
      },
      "empirical_risky_value": {
        "_type": "object",
        "key_count": 7,
        "keys": [
          "action_accuracy",
          "mean_calibration_error",
          "mean_policy_regret",
          "mean_q_overestimation",
          "mean_q_underestimation",
          "num_cells",
          "risky_action_selection_rate"
        ]
      },
      "posterior_lower_q10_dp_beta_1_1": {
        "_type": "object",
        "key_count": 7,
        "keys": [
          "action_accuracy",
          "mean_calibration_error",
          "mean_policy_regret",
          "mean_q_overestimation",
          "mean_q_underestimation",
          "num_cells",
          "risky_action_selection_rate"
        ]
      },
      "posterior_mean_dp_beta_1_1": {
        "_type": "object",
        "key_count": 7,
        "keys": [
          "action_accuracy",
          "mean_calibration_error",
          "mean_policy_regret",
          "mean_q_overestimation",
          "mean_q_underestimation",
          "num_cells",
          "risky_action_selection_rate"
        ]
      },
      "posterior_upper_q90_dp_beta_1_1": {
        "_type": "object",
        "key_count": 7,
        "keys": [
          "action_accuracy",
          "mean_calibration_error",
          "mean_policy_regret",
          "mean_q_overestimation",
          "mean_q_underestimation",
          "num_cells",
          "risky_action_selection_rate"
        ]
      },
      "raw_trl": {
        "_type": "object",
        "key_count": 7,
        "keys": [
          "action_accuracy",
          "mean_calibration_error",
          "mean_policy_regret",
          "mean_q_overestimation",
          "mean_q_underestimation",
          "num_cells",
          "risky_action_selection_rate"
        ]
      },
      "robust_lcb_dp_delta_0_2": {
        "_type": "object",
        "key_count": 7,
        "keys": [
          "action_accuracy",
          "mean_calibration_error",
          "mean_policy_regret",
          "mean_q_overestimation",
          "mean_q_underestimation",
          "num_cells",
          "risky_action_selection_rate"
        ]
      },
      "robust_ucb_dp_delta_0_2": {
        "_type": "object",
        "key_count": 7,
        "keys": [
          "action_accuracy",
          "mean_calibration_error",
          "mean_policy_regret",
          "mean_q_overestimation",
          "mean_q_underestimation",
          "num_cells",
          "risky_action_selection_rate"
        ]
      },
      "trl_log": {
        "_type": "object",
        "key_count": 7,
        "keys": [
          "action_accuracy",
          "mean_calibration_error",
          "mean_policy_regret",
          "mean_q_overestimation",
          "mean_q_underestimation",
          "num_cells",
          "risky_action_selection_rate"
        ]
      }
    },
    "method_summary": {
      "empirical_model_dp": {
        "_type": "object",
        "key_count": 7,
        "keys": [
          "action_accuracy",
          "mean_calibration_error",
          "mean_policy_regret",
          "mean_q_overestimation",
          "mean_q_underestimation",
          "num_cells",
          "risky_action_selection_rate"
        ]
      },
      "empirical_risky_value": {
        "_type": "object",
        "key_count": 7,
        "keys": [
          "action_accuracy",
          "mean_calibration_error",
          "mean_policy_regret",
          "mean_q_overestimation",
          "mean_q_underestimation",
          "num_cells",
          "risky_action_selection_rate"
        ]
      },
      "posterior_lower_q10_dp_beta_1_1": {
        "_type": "object",
        "key_count": 7,
        "keys": [
          "action_accuracy",
          "mean_calibration_error",
          "mean_policy_regret",
          "mean_q_overestimation",
          "mean_q_underestimation",
          "num_cells",
          "risky_action_selection_rate"
        ]
      },
      "posterior_mean_dp_beta_1_1": {
        "_type": "object",
        "key_count": 7,
        "keys": [
          "action_accuracy",
          "mean_calibration_error",
          "mean_policy_regret",
          "mean_q_overestimation",
          "mean_q_underestimation",
          "num_cells",
          "risky_action_selection_rate"
        ]
      },
      "posterior_upper_q90_dp_beta_1_1": {
        "_type": "object",
        "key_count": 7,
        "keys": [
          "action_accuracy",
          "mean_calibration_error",
          "mean_policy_regret",
          "mean_q_overestimation",
          "mean_q_underestimation",
          "num_cells",
          "risky_action_selection_rate"
        ]
      },
      "raw_trl": {
        "_type": "object",
        "key_count": 7,
        "keys": [
          "action_accuracy",
          "mean_calibration_error",
          "mean_policy_regret",
          "mean_q_overestimation",
          "mean_q_underestimation",
          "num_cells",
          "risky_action_selection_rate"
        ]
      },
      "robust_lcb_dp_delta_0_2": {
        "_type": "object",
        "key_count": 7,
        "keys": [
          "action_accuracy",
          "mean_calibration_error",
          "mean_policy_regret",
          "mean_q_overestimation",
          "mean_q_underestimation",
          "num_cells",
          "risky_action_selection_rate"
        ]
      },
      "robust_ucb_dp_delta_0_2": {
        "_type": "object",
        "key_count": 7,
        "keys": [
          "action_accuracy",
          "mean_calibration_error",
          "mean_policy_regret",
          "mean_q_overestimation",
          "mean_q_underestimation",
          "num_cells",
          "risky_action_selection_rate"
        ]
      },
      "trl_log": {
        "_type": "object",
        "key_count": 7,
        "keys": [
          "action_accuracy",
          "mean_calibration_error",
          "mean_policy_regret",
          "mean_q_overestimation",
          "mean_q_underestimation",
          "num_cells",
          "risky_action_selection_rate"
        ]
      }
    },
    "no_success_risk_optimal_solved_methods": [],
    "num_method_rows": 72,
    "num_selected_cells": 8,
    "posterior_candidate_target_regret_deltas_vs_trl_log": {
      "posterior_lower_q10_dp_beta_1_1": -0.17752500000000004,
      "posterior_mean_dp_beta_1_1": -0.051525000000000015,
      "posterior_upper_q90_dp_beta_1_1": -0.006749999999999978,
      "robust_lcb_dp_delta_0_2": -0.17752500000000004,
      "robust_ucb_dp_delta_0_2": -0.006749999999999978
    },
    "target_regime_summary": {
      "empirical_model_dp": {
        "_type": "object",
        "key_count": 7,
        "keys": [
          "action_accuracy",
          "mean_calibration_error",
          "mean_policy_regret",
          "mean_q_overestimation",
          "mean_q_underestimation",
          "num_cells",
          "risky_action_selection_rate"
        ]
      },
      "empirical_risky_value": {
        "_type": "object",
        "key_count": 7,
        "keys": [
          "action_accuracy",
          "mean_calibration_error",
          "mean_policy_regret",
          "mean_q_overestimation",
          "mean_q_underestimation",
          "num_cells",
          "risky_action_selection_rate"
        ]
      },
      "posterior_lower_q10_dp_beta_1_1": {
        "_type": "object",
        "key_count": 7,
        "keys": [
          "action_accuracy",
          "mean_calibration_error",
          "mean_policy_regret",
          "mean_q_overestimation",
          "mean_q_underestimation",
          "num_cells",
          "risky_action_selection_rate"
        ]
      },
      "posterior_mean_dp_beta_1_1": {
        "_type": "object",
        "key_count": 7,
        "keys": [
          "action_accuracy",
          "mean_calibration_error",
          "mean_policy_regret",
          "mean_q_overestimation",
          "mean_q_underestimation",
          "num_cells",
          "risky_action_selection_rate"
        ]
      },
      "posterior_upper_q90_dp_beta_1_1": {
        "_type": "object",
        "key_count": 7,
        "keys": [
          "action_accuracy",
          "mean_calibration_error",
          "mean_policy_regret",
          "mean_q_overestimation",
          "mean_q_underestimation",
          "num_cells",
          "risky_action_selection_rate"
        ]
      },
      "raw_trl": {
        "_type": "object",
        "key_count": 7,
        "keys": [
          "action_accuracy",
          "mean_calibration_error",
          "mean_policy_regret",
          "mean_q_overestimation",
          "mean_q_underestimation",
          "num_cells",
          "risky_action_selection_rate"
        ]
      },
      "robust_lcb_dp_delta_0_2": {
        "_type": "object",
        "key_count": 7,
        "keys": [
          "action_accuracy",
          "mean_calibration_error",
          "mean_policy_regret",
          "mean_q_overestimation",
          "mean_q_underestimation",
          "num_cells",
          "risky_action_selection_rate"
        ]
      },
      "robust_ucb_dp_delta_0_2": {
        "_type": "object",
        "key_count": 7,
        "keys": [
          "action_accuracy",
          "mean_calibration_error",
          "mean_policy_regret",
          "mean_q_overestimation",
          "mean_q_underestimation",
          "num_cells",
          "risky_action_selection_rate"
        ]
      },
      "trl_log": {
        "_type": "object",
        "key_count": 7,
        "keys": [
          "action_accuracy",
          "mean_calibration_error",
          "mean_policy_regret",
          "mean_q_overestimation",
          "mean_q_underestimation",
          "num_cells",
          "risky_action_selection_rate"
        ]
      }
    },
    "transition_baseline_positive": true
  },
  "next_questions": [
    "Should future posterior TRL variants report an identifiability or prior-dependence flag before selecting risky actions?",
    "What explicit prior is acceptable for risk-optimal no-success regimes where finite data lacks successful risky outcomes?",
    "Can transitive posterior propagation improve long-horizon estimates without outperforming these transition-model baselines only by prior choice?"
  ],
  "status": "completed"
}
```


## Latest summary

# Experiment 0009 Summary

## Objective

Audit compact transition-level posterior model-DP baselines on representative cells from the 0008 identifiability grid before adding posterior/transitive TRL variants.

## Commands Run

```bash
mkdir -p research/sto_trl/artifacts/0009 research/sto_trl/results
conda run -n autoresearcher_sto_trl python research/sto_trl/artifacts/0009/transition_posterior_baselines.py
conda run -n autoresearcher_sto_trl python scripts/validate_artifacts.py --repo-root . --json research/sto_trl/results/0009_result.json --schema schemas/result.schema.json --check-result-artifacts
```

## Representative Subset

- Selected cells: `8`
- Method rows: `72`
- Regime counts: `{'matched_identifiable_safe_optimal': 1, 'matched_risk_optimal': 1, 'lucky_only_safe_optimal': 1, 'no_success_safe_optimal': 1, 'no_success_risk_optimal': 1, 'ambiguous_safe_optimal': 1, 'ambiguous_risk_optimal': 1, 'prior_dependent_safe_optimal': 1}`
- Tag counts: `{'matched': 5, 'identifiable': 3, 'safe_optimal': 5, 'ambiguous': 5, 'risky_optimal': 3, 'lucky_only': 1, 'prior_dependent': 4, 'no_success': 2}`

## Method Summary

| Method | Action accuracy | Mean regret | Risky rate | Mean Q overestimate | Calibration error |
| --- | ---: | ---: | ---: | ---: | ---: |
| empirical_model_dp | 0.500000 | 0.109012500000 | 0.375000 | 0.116718750000 | 0.262968750000 |
| empirical_risky_value | 0.500000 | 0.109012500000 | 0.375000 | 0.116718750000 | 0.262968750000 |
| posterior_lower_q10_dp_beta_1_1 | 0.750000 | 0.020250000000 | 0.125000 | 0.042862500000 | 0.296981250000 |
| posterior_mean_dp_beta_1_1 | 0.625000 | 0.083250000000 | 0.250000 | 0.090000000000 | 0.233750000000 |
| posterior_upper_q90_dp_beta_1_1 | 0.500000 | 0.105637500000 | 0.625000 | 0.175856250000 | 0.255787500000 |
| raw_trl | 0.375000 | 0.168637500000 | 0.750000 | 0.275625000000 | 0.405000000000 |
| robust_lcb_dp_delta_0_2 | 0.625000 | 0.039487500000 | 0.000000 | 0.024019705511 | 0.377294486223 |
| robust_ucb_dp_delta_0_2 | 0.500000 | 0.105637500000 | 0.625000 | 0.248480276028 | 0.307052638014 |
| trl_log | 0.500000 | 0.109012500000 | 0.375000 | 0.116718750000 | 0.262968750000 |

## Decision Findings

- Best target-regime transition uncertainty baseline: `posterior_lower_q10_dp_beta_1_1`.
- Target-regime regret delta versus TRL-log: `-0.177525000000`.
- Positive transition-baseline evidence: `True`.
- Risk-optimal no-success solved methods: `[]`.
- Chain guard passed: `True`.

## Interpretation

On the representative 0008 subset, transition-level uncertainty baselines explain the recoverable finite-coverage behavior: posterior_lower_q10_dp_beta_1_1 reduces mean target-regime regret versus TRL-log by -0.177525000000, while at least one posterior baseline preserves the matched risk-optimal action. No evaluated transition baseline solved risk_optimal_no_success; explicit priors or additional coverage remain necessary. Empirical model DP, empirical risky value, and TRL-log are identical on this tabular family.

## Artifacts

- `research/sto_trl/artifacts/0009/transition_posterior_baselines.py`
- `research/sto_trl/artifacts/0009/raw_metrics.json`
- `research/sto_trl/artifacts/0009/metrics.csv`
- `research/sto_trl/artifacts/0009/regime_summary.csv`
- `research/sto_trl/artifacts/0009/posterior_diagnostics.json`
- `research/sto_trl/artifacts/0009/selected_grid_cells.json`
- `research/sto_trl/artifacts/0009/coverage_diagnostics.json`
- `research/sto_trl/artifacts/0009/transition_tables.json`
- `research/sto_trl/artifacts/0009/value_tables.json`


## Full evidence paths

- `research/sto_trl/results/0009_result.json`
- `research/sto_trl/results/0009_summary.md`

Inspect the full result JSON only when the compact summary and artifact list are insufficient.


## Artifact paths

- `/home/eston/autoresearcher/research/sto_trl/artifacts/0005`
- `/home/eston/autoresearcher/research/sto_trl/artifacts/0006`
- `/home/eston/autoresearcher/research/sto_trl/artifacts/0007`
- `/home/eston/autoresearcher/research/sto_trl/artifacts/0008`
- `/home/eston/autoresearcher/research/sto_trl/artifacts/0009`


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
    },
    "evidence_quality": {
      "type": "string",
      "enum": ["strong", "medium", "weak", "invalid"]
    },
    "success_criteria_satisfied": {
      "type": "boolean"
    },
    "failure_criteria_triggered": {
      "type": "boolean"
    },
    "should_escalate_to_pro": {
      "type": "boolean"
    },
    "escalation_reason": {
      "type": ["string", "null"]
    }
  },
  "required": [
    "experiment_id",
    "verdict",
    "allows_auto_continue",
    "reasons",
    "evidence_checked",
    "required_fixes",
    "risk_flags",
    "evidence_quality",
    "success_criteria_satisfied",
    "failure_criteria_triggered",
    "should_escalate_to_pro",
    "escalation_reason"
  ],
  "additionalProperties": false
}
```
