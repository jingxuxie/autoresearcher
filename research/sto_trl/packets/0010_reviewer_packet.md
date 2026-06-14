# Reviewer Context: sto_trl

## Latest plan

# Experiment 0010

## Objective

Test whether posterior transition uncertainty plus log-space transitive propagation adds value beyond transition-model DP on a small multi-step tabular stochastic branch-chain diagnostic.

## Hypothesis

On a multi-step stochastic branch-chain with censored long-horizon labels, posterior transition uncertainty can reduce risky-path overestimation while log-space transitive propagation preserves long-horizon reachability. If posterior TRL-log is equivalent to posterior model DP, or only improves through the same prior, then there is no distinct posterior transitive benefit yet.

## Success criteria

- Creates a self-contained artifact under research/sto_trl/artifacts/0010/ without editing prior results, schemas, AGENTS.md, scripts/autoresearcher.py, or environment files.
- Uses exact DP ground truth for every evaluated tabular MDP and keeps runtime under 30 minutes.
- Includes a deterministic chain guard with real raw TRL and TRL-log execution if practical.
- Includes at least one multi-step stochastic branch-chain or stochastic stitching graph where long-horizon labels are censored and transitive propagation could differ from one-step empirical transition scoring.
- Compares mc_supervised, trl_raw, trl_log, empirical model DP, posterior mean model DP, posterior quantile or robust model DP, posterior_trl_log, and posterior_mc_plus_trl_log under matched priors.
- Reports held-out long-horizon value MSE, calibration error, Q overestimation and underestimation, policy regret, risky action selection rate, and coverage diagnostics by regime.
- Counts positive evidence only if posterior_trl_log or posterior_mc_plus_trl_log improves long-horizon or policy metrics versus both trl_log and the prior-matched posterior model DP without losing matched risk-optimal action choice.
- Counts equivalence to posterior model DP, or improvement only from prior choice, as negative or boundary evidence rather than a stochastic TRL win.
- Produces valid research/sto_trl/results/0010_result.json and research/sto_trl/results/0010_summary.md with exact commands run.

## Failure criteria

- The experiment omits prior-matched posterior model DP baselines, making transitive propagation effects impossible to isolate.
- Exact DP values or true transition probabilities are used as training or decision inputs rather than evaluation ground truth.
- The scenario is only a one-step risky shortcut where 0008 and 0009 already showed TRL-log is equivalent to empirical model DP.
- The result reports aggregate averages without per-regime or coverage-stratified diagnostics.
- The method appears successful only by choosing safe in matched risk-optimal regimes or by being conservative everywhere.
- The run expands to neural networks, continuous control, OGBench, large downloads, broad sweeps, or exceeds 30 minutes.

## Estimated runtime

<= 25 minutes

## Tasks for Codex

- Create research/sto_trl/artifacts/0010/ and implement a small posterior_transitive_ablation.py script reusing prior tabular helpers where practical.
- Define a compact deterministic chain guard and a multi-step stochastic branch-chain or stitching MDP with exact DP ground truth, finite offline coverage, and long-horizon label censoring.
- Implement prior-matched empirical and posterior model-DP baselines plus posterior_trl_log and posterior_mc_plus_trl_log variants.
- Evaluate methods on matched safe-optimal, matched risk-optimal, lucky-only safe-optimal, no-success risk-optimal, and at least one ambiguous or prior-dependent multi-step regime.
- Save raw_metrics.json, metrics.csv, regime_summary.csv, posterior_transitive_diagnostics.json, coverage_diagnostics.json, offline_datasets.json, transition_tables.json, and value_tables.json under research/sto_trl/artifacts/0010/.
- Write research/sto_trl/results/0010_result.json and research/sto_trl/results/0010_summary.md, then validate the result JSON with scripts/validate_artifacts.py and artifact checks.

## Required outputs

- `research/sto_trl/results/0010_result.json`
- `research/sto_trl/results/0010_summary.md`
- `research/sto_trl/artifacts/0010/`


## Latest plan JSON

```json
{
  "estimated_runtime_minutes": 25,
  "experiment_id": "0010",
  "failure_criteria": [
    "The experiment omits prior-matched posterior model DP baselines, making transitive propagation effects impossible to isolate.",
    "Exact DP values or true transition probabilities are used as training or decision inputs rather than evaluation ground truth.",
    "The scenario is only a one-step risky shortcut where 0008 and 0009 already showed TRL-log is equivalent to empirical model DP.",
    "The result reports aggregate averages without per-regime or coverage-stratified diagnostics.",
    "The method appears successful only by choosing safe in matched risk-optimal regimes or by being conservative everywhere.",
    "The run expands to neural networks, continuous control, OGBench, large downloads, broad sweeps, or exceeds 30 minutes."
  ],
  "hypothesis": "On a multi-step stochastic branch-chain with censored long-horizon labels, posterior transition uncertainty can reduce risky-path overestimation while log-space transitive propagation preserves long-horizon reachability. If posterior TRL-log is equivalent to posterior model DP, or only improves through the same prior, then there is no distinct posterior transitive benefit yet.",
  "objective": "Test whether posterior transition uncertainty plus log-space transitive propagation adds value beyond transition-model DP on a small multi-step tabular stochastic branch-chain diagnostic.",
  "required_outputs": [
    "research/sto_trl/results/0010_result.json",
    "research/sto_trl/results/0010_summary.md",
    "research/sto_trl/artifacts/0010/"
  ],
  "success_criteria": [
    "Creates a self-contained artifact under research/sto_trl/artifacts/0010/ without editing prior results, schemas, AGENTS.md, scripts/autoresearcher.py, or environment files.",
    "Uses exact DP ground truth for every evaluated tabular MDP and keeps runtime under 30 minutes.",
    "Includes a deterministic chain guard with real raw TRL and TRL-log execution if practical.",
    "Includes at least one multi-step stochastic branch-chain or stochastic stitching graph where long-horizon labels are censored and transitive propagation could differ from one-step empirical transition scoring.",
    "Compares mc_supervised, trl_raw, trl_log, empirical model DP, posterior mean model DP, posterior quantile or robust model DP, posterior_trl_log, and posterior_mc_plus_trl_log under matched priors.",
    "Reports held-out long-horizon value MSE, calibration error, Q overestimation and underestimation, policy regret, risky action selection rate, and coverage diagnostics by regime.",
    "Counts positive evidence only if posterior_trl_log or posterior_mc_plus_trl_log improves long-horizon or policy metrics versus both trl_log and the prior-matched posterior model DP without losing matched risk-optimal action choice.",
    "Counts equivalence to posterior model DP, or improvement only from prior choice, as negative or boundary evidence rather than a stochastic TRL win.",
    "Produces valid research/sto_trl/results/0010_result.json and research/sto_trl/results/0010_summary.md with exact commands run."
  ],
  "tasks_for_codex": [
    "Create research/sto_trl/artifacts/0010/ and implement a small posterior_transitive_ablation.py script reusing prior tabular helpers where practical.",
    "Define a compact deterministic chain guard and a multi-step stochastic branch-chain or stitching MDP with exact DP ground truth, finite offline coverage, and long-horizon label censoring.",
    "Implement prior-matched empirical and posterior model-DP baselines plus posterior_trl_log and posterior_mc_plus_trl_log variants.",
    "Evaluate methods on matched safe-optimal, matched risk-optimal, lucky-only safe-optimal, no-success risk-optimal, and at least one ambiguous or prior-dependent multi-step regime.",
    "Save raw_metrics.json, metrics.csv, regime_summary.csv, posterior_transitive_diagnostics.json, coverage_diagnostics.json, offline_datasets.json, transition_tables.json, and value_tables.json under research/sto_trl/artifacts/0010/.",
    "Write research/sto_trl/results/0010_result.json and research/sto_trl/results/0010_summary.md, then validate the result JSON with scripts/validate_artifacts.py and artifact checks."
  ]
}
```


## Latest result summary

```json
{
  "_source": "/home/eston/autoresearcher/research/sto_trl/results/0010_result.json",
  "artifacts": {
    "_type": "list",
    "first_items": [
      "research/sto_trl/artifacts/0010/posterior_transitive_ablation.py",
      "research/sto_trl/artifacts/0010/raw_metrics.json",
      "research/sto_trl/artifacts/0010/metrics.csv"
    ],
    "length": 9
  },
  "baseline_metrics": {
    "empirical_model_dp": {
      "action_accuracy": 0.4,
      "mean_all_pair_value_mse": 0.05945326587964287,
      "mean_heldout_long_horizon_value_mse": 0.040962586545,
      "mean_policy_regret": 0.06706799999999995,
      "mean_risky_q_calibration_error": 0.22161599999999998,
      "mean_risky_q_overestimation": 0.0729,
      "mean_risky_q_underestimation": 0.148716,
      "num_rows": 5,
      "risky_action_selection_rate": 0.4
    },
    "mc_supervised": {
      "action_accuracy": 0.4,
      "mean_all_pair_value_mse": 0.22851831360535724,
      "mean_heldout_long_horizon_value_mse": 0.42157000192500016,
      "mean_policy_regret": 0.016037999999999906,
      "mean_risky_q_calibration_error": 0.542376,
      "mean_risky_q_overestimation": 0.0,
      "mean_risky_q_underestimation": 0.542376,
      "num_rows": 5,
      "risky_action_selection_rate": 0.0
    },
    "posterior_lower_q10_model_dp": {
      "action_accuracy": 0.4,
      "mean_all_pair_value_mse": 0.058753952315927685,
      "mean_heldout_long_horizon_value_mse": 0.0386303210569125,
      "mean_policy_regret": 0.016037999999999906,
      "mean_risky_q_calibration_error": 0.26100629999999997,
      "mean_risky_q_overestimation": 0.0190998,
      "mean_risky_q_underestimation": 0.24190650000000002,
      "num_rows": 5,
      "risky_action_selection_rate": 0.0
    },
    "posterior_mean_model_dp": {
      "action_accuracy": 0.6,
      "mean_all_pair_value_mse": 0.05761705199748525,
      "mean_heldout_long_horizon_value_mse": 0.03659566492413223,
      "mean_policy_regret": 0.008747999999999933,
      "mean_risky_q_calibration_error": 0.2154305454545454,
      "mean_risky_q_overestimation": 0.0486,
      "mean_risky_q_underestimation": 0.16683054545454543,
      "num_rows": 5,
      "risky_action_selection_rate": 0.2
    },
    "trl_log": {
      "action_accuracy": 0.4,
      "mean_all_pair_value_mse": 0.05945326587964287,
      "mean_heldout_long_horizon_value_mse": 0.040962586545,
      "mean_policy_regret": 0.06706799999999995,
      "mean_risky_q_calibration_error": 0.22161599999999998,
      "mean_risky_q_overestimation": 0.0729,
      "mean_risky_q_underestimation": 0.148716,
      "num_rows": 5,
      "risky_action_selection_rate": 0.4
    }
  },
  "claim_tested": "Posterior transition uncertainty plus log-space transitive propagation was tested against prior-matched transition-model DP on censored multi-step stochastic branch-chain diagnostics.",
  "experiment_id": "0010",
  "interpretation": "The multi-step branch-chain confirms that transitive backups recover censored long-horizon values better than MC-only, and posterior transition uncertainty changes the risky branch through the declared Beta prior. However, posterior_trl_log and posterior_mc_plus_trl_log are numerically equivalent to the prior-matched posterior mean model-DP baseline on every regime, so the improvement is attributable to the transition prior/model rather than a distinct posterior TRL transitive effect.",
  "known_failures": [
    "posterior_trl_log and posterior_mc_plus_trl_log were numerically equivalent to the prior-matched posterior mean model-DP baseline.",
    "No distinct posterior transitive benefit over both TRL-log and prior-matched posterior model DP was detected."
  ],
  "metrics": {
    "best_posterior_trl_candidate": "posterior_trl_log",
    "chain_guard": {
      "chain_length": 9,
      "passed": true,
      "raw_trl_max_abs_error": 0.0,
      "start_exact_value": 0.38742048900000015,
      "start_raw_trl_value": 0.38742048900000015,
      "start_trl_log_value": 0.38742048900000015,
      "trl_log_max_abs_error": 0.0
    },
    "coverage_diagnostics": {
      "label_horizon_cutoff": 2,
      "regimes": {
        "_type": "object",
        "key_count": 5,
        "keys": [
          "lucky_only_safe_optimal",
          "matched_risk_optimal",
          "matched_safe_optimal",
          "no_success_risk_optimal",
          "prior_dependent_risk_optimal"
        ]
      },
      "tag_counts": {
        "_type": "object",
        "key_count": 8,
        "keys": [
          "ambiguous",
          "biased_coverage",
          "lucky_only",
          "matched",
          "no_success",
          "prior_dependent",
          "risk_optimal",
          "safe_optimal"
        ]
      }
    },
    "matched_risk_optimal_preserved": true,
    "method_summary": {
      "empirical_model_dp": {
        "_type": "object",
        "key_count": 9,
        "keys": [
          "action_accuracy",
          "mean_all_pair_value_mse",
          "mean_heldout_long_horizon_value_mse",
          "mean_policy_regret",
          "mean_risky_q_calibration_error",
          "mean_risky_q_overestimation",
          "mean_risky_q_underestimation",
          "num_rows",
          "risky_action_selection_rate"
        ]
      },
      "mc_supervised": {
        "_type": "object",
        "key_count": 9,
        "keys": [
          "action_accuracy",
          "mean_all_pair_value_mse",
          "mean_heldout_long_horizon_value_mse",
          "mean_policy_regret",
          "mean_risky_q_calibration_error",
          "mean_risky_q_overestimation",
          "mean_risky_q_underestimation",
          "num_rows",
          "risky_action_selection_rate"
        ]
      },
      "posterior_lower_q10_model_dp": {
        "_type": "object",
        "key_count": 9,
        "keys": [
          "action_accuracy",
          "mean_all_pair_value_mse",
          "mean_heldout_long_horizon_value_mse",
          "mean_policy_regret",
          "mean_risky_q_calibration_error",
          "mean_risky_q_overestimation",
          "mean_risky_q_underestimation",
          "num_rows",
          "risky_action_selection_rate"
        ]
      },
      "posterior_mc_plus_trl_log": {
        "_type": "object",
        "key_count": 9,
        "keys": [
          "action_accuracy",
          "mean_all_pair_value_mse",
          "mean_heldout_long_horizon_value_mse",
          "mean_policy_regret",
          "mean_risky_q_calibration_error",
          "mean_risky_q_overestimation",
          "mean_risky_q_underestimation",
          "num_rows",
          "risky_action_selection_rate"
        ]
      },
      "posterior_mean_model_dp": {
        "_type": "object",
        "key_count": 9,
        "keys": [
          "action_accuracy",
          "mean_all_pair_value_mse",
          "mean_heldout_long_horizon_value_mse",
          "mean_policy_regret",
          "mean_risky_q_calibration_error",
          "mean_risky_q_overestimation",
          "mean_risky_q_underestimation",
          "num_rows",
          "risky_action_selection_rate"
        ]
      },
      "posterior_trl_log": {
        "_type": "object",
        "key_count": 9,
        "keys": [
          "action_accuracy",
          "mean_all_pair_value_mse",
          "mean_heldout_long_horizon_value_mse",
          "mean_policy_regret",
          "mean_risky_q_calibration_error",
          "mean_risky_q_overestimation",
          "mean_risky_q_underestimation",
          "num_rows",
          "risky_action_selection_rate"
        ]
      },
      "trl_log": {
        "_type": "object",
        "key_count": 9,
        "keys": [
          "action_accuracy",
          "mean_all_pair_value_mse",
          "mean_heldout_long_horizon_value_mse",
          "mean_policy_regret",
          "mean_risky_q_calibration_error",
          "mean_risky_q_overestimation",
          "mean_risky_q_underestimation",
          "num_rows",
          "risky_action_selection_rate"
        ]
      },
      "trl_raw": {
        "_type": "object",
        "key_count": 9,
        "keys": [
          "action_accuracy",
          "mean_all_pair_value_mse",
          "mean_heldout_long_horizon_value_mse",
          "mean_policy_regret",
          "mean_risky_q_calibration_error",
          "mean_risky_q_overestimation",
          "mean_risky_q_underestimation",
          "num_rows",
          "risky_action_selection_rate"
        ]
      }
    },
    "num_method_rows": 40,
    "num_regimes": 5,
    "positive_transitive_evidence": false,
    "posterior_trl_equivalent_to_prior_matched_model_dp": true,
    "regime_summary": {
      "lucky_only_safe_optimal": {
        "_type": "object",
        "key_count": 9,
        "keys": [
          "action_accuracy",
          "mean_all_pair_value_mse",
          "mean_heldout_long_horizon_value_mse",
          "mean_policy_regret",
          "mean_risky_q_calibration_error",
          "mean_risky_q_overestimation",
          "mean_risky_q_underestimation",
          "num_rows",
          "risky_action_selection_rate"
        ]
      },
      "matched_risk_optimal": {
        "_type": "object",
        "key_count": 9,
        "keys": [
          "action_accuracy",
          "mean_all_pair_value_mse",
          "mean_heldout_long_horizon_value_mse",
          "mean_policy_regret",
          "mean_risky_q_calibration_error",
          "mean_risky_q_overestimation",
          "mean_risky_q_underestimation",
          "num_rows",
          "risky_action_selection_rate"
        ]
      },
      "matched_safe_optimal": {
        "_type": "object",
        "key_count": 9,
        "keys": [
          "action_accuracy",
          "mean_all_pair_value_mse",
          "mean_heldout_long_horizon_value_mse",
          "mean_policy_regret",
          "mean_risky_q_calibration_error",
          "mean_risky_q_overestimation",
          "mean_risky_q_underestimation",
          "num_rows",
          "risky_action_selection_rate"
        ]
      },
      "no_success_risk_optimal": {
        "_type": "object",
        "key_count": 9,
        "keys": [
          "action_accuracy",
          "mean_all_pair_value_mse",
          "mean_heldout_long_horizon_value_mse",
          "mean_policy_regret",
          "mean_risky_q_calibration_error",
          "mean_risky_q_overestimation",
          "mean_risky_q_underestimation",
          "num_rows",
          "risky_action_selection_rate"
        ]
      },
      "prior_dependent_risk_optimal": {
        "_type": "object",
        "key_count": 9,
        "keys": [
          "action_accuracy",
          "mean_all_pair_value_mse",
          "mean_heldout_long_horizon_value_mse",
          "mean_policy_regret",
          "mean_risky_q_calibration_error",
          "mean_risky_q_overestimation",
          "mean_risky_q_underestimation",
          "num_rows",
          "risky_action_selection_rate"
        ]
      }
    }
  },
  "next_questions": [
    "Can a posterior TRL variant exploit partial graph stitching where transition-model DP is deliberately misspecified or unavailable?",
    "What prior should be declared for no-success risk-optimal regimes before treating risk avoidance as a success?",
    "Can posterior transitive methods beat posterior model DP on graphs with hidden intermediate aliases or sparse stitching coverage?"
  ],
  "status": "completed"
}
```


## Latest summary

# Experiment 0010 Summary

## Objective

Test whether posterior transition uncertainty plus log-space transitive propagation adds value beyond transition-model DP on a small multi-step stochastic branch-chain diagnostic.

## Commands Run

```bash
mkdir -p research/sto_trl/artifacts/0010 research/sto_trl/results
conda run -n autoresearcher_sto_trl python research/sto_trl/artifacts/0010/posterior_transitive_ablation.py
conda run -n autoresearcher_sto_trl python scripts/validate_artifacts.py --repo-root . --json research/sto_trl/results/0010_result.json --schema schemas/result.schema.json --check-result-artifacts
```

## Setup

- Regimes: `5`
- Label horizon cutoff: `2`
- Methods: `['mc_supervised', 'trl_raw', 'trl_log', 'empirical_model_dp', 'posterior_mean_model_dp', 'posterior_lower_q10_model_dp', 'posterior_trl_log', 'posterior_mc_plus_trl_log']`
- Chain guard passed: `True`

## Method Summary

| Method | Action accuracy | Heldout MSE | Policy regret | Risky rate | Q overestimation | Calibration error |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| empirical_model_dp | 0.400000 | 0.040962586545 | 0.067068000000 | 0.400000 | 0.072900000000 | 0.221616000000 |
| mc_supervised | 0.400000 | 0.421570001925 | 0.016038000000 | 0.000000 | 0.000000000000 | 0.542376000000 |
| posterior_lower_q10_model_dp | 0.400000 | 0.038630321057 | 0.016038000000 | 0.000000 | 0.019099800000 | 0.261006300000 |
| posterior_mc_plus_trl_log | 0.600000 | 0.036595664924 | 0.008748000000 | 0.200000 | 0.048600000000 | 0.215430545455 |
| posterior_mean_model_dp | 0.600000 | 0.036595664924 | 0.008748000000 | 0.200000 | 0.048600000000 | 0.215430545455 |
| posterior_trl_log | 0.600000 | 0.036595664924 | 0.008748000000 | 0.200000 | 0.048600000000 | 0.215430545455 |
| trl_log | 0.400000 | 0.040962586545 | 0.067068000000 | 0.400000 | 0.072900000000 | 0.221616000000 |
| trl_raw | 0.400000 | 0.050639241420 | 0.123930000000 | 0.800000 | 0.179334000000 | 0.317844000000 |

## Decision Findings

- Positive posterior transitive evidence: `False`
- Posterior TRL equivalent to prior-matched posterior model DP: `True`
- Matched risk-optimal action preserved: `True`
- Posterior TRL minus posterior model heldout MSE: `0.000000000000`
- MC-only minus TRL-log heldout MSE: `0.380607415380`

## Interpretation

The multi-step branch-chain confirms that transitive backups recover censored long-horizon values better than MC-only, and posterior transition uncertainty changes the risky branch through the declared Beta prior. However, posterior_trl_log and posterior_mc_plus_trl_log are numerically equivalent to the prior-matched posterior mean model-DP baseline on every regime, so the improvement is attributable to the transition prior/model rather than a distinct posterior TRL transitive effect.

## Artifacts

- `research/sto_trl/artifacts/0010/posterior_transitive_ablation.py`
- `research/sto_trl/artifacts/0010/raw_metrics.json`
- `research/sto_trl/artifacts/0010/metrics.csv`
- `research/sto_trl/artifacts/0010/regime_summary.csv`
- `research/sto_trl/artifacts/0010/posterior_transitive_diagnostics.json`
- `research/sto_trl/artifacts/0010/coverage_diagnostics.json`
- `research/sto_trl/artifacts/0010/offline_datasets.json`
- `research/sto_trl/artifacts/0010/transition_tables.json`
- `research/sto_trl/artifacts/0010/value_tables.json`


## Full evidence paths

- `research/sto_trl/results/0010_result.json`
- `research/sto_trl/results/0010_summary.md`

Inspect the full result JSON only when the compact summary and artifact list are insufficient.


## Artifact paths

- `/home/eston/autoresearcher/research/sto_trl/artifacts/0006`
- `/home/eston/autoresearcher/research/sto_trl/artifacts/0007`
- `/home/eston/autoresearcher/research/sto_trl/artifacts/0008`
- `/home/eston/autoresearcher/research/sto_trl/artifacts/0009`
- `/home/eston/autoresearcher/research/sto_trl/artifacts/0010`


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
