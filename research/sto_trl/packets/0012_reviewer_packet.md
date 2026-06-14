# Reviewer Context: sto_trl

## Latest plan

# Experiment 0012

## Objective

Test whether short trajectory context plus log-space transitive propagation helps in a tiny stochastic POMDP with aliased observations, where observation-level model DP is not a fair Markov baseline.

## Hypothesis

In a latent tabular MDP with two or more hidden states sharing the same observation, observation-only empirical model DP and observation-only TRL-log will be miscalibrated, while history-keyed MC+TRL-log will improve held-out long-horizon value MSE and policy regret versus history-keyed MC-only without using latent states in training.

## Success criteria

- Observation-only empirical model DP and observation-only TRL-log show a measurable aliasing failure: higher heldout MSE or policy regret than a latent-oracle evaluation baseline.
- History-keyed MC+TRL-log improves heldout long-horizon value MSE over history-keyed MC-only by at least 25% on censored labels.
- History-keyed MC+TRL-log improves policy regret or risky/teleport action choice versus observation-only TRL-log on at least one aliased stochastic shortcut or teleporter family.
- The report includes a history-model-DP baseline; if history-model-DP fully explains the gain, the result is labeled as representation/context evidence rather than a distinct TRL algorithm win.
- No training method uses true latent state, exact DP labels, true transition probabilities, or future observations as inputs.

## Failure criteria

- History-keyed MC+TRL-log is equivalent to or worse than history-keyed MC-only on heldout long-horizon MSE.
- The apparent gain disappears when compared to a prior-matched history-model-DP baseline.
- The task requires oracle latent-state access or future-information leakage to show improvement.
- The experiment does not include observation-only, history-keyed, and latent-oracle evaluation baselines.
- Runtime exceeds 30 minutes or introduces neural networks, continuous control, OGBench, large downloads, or expensive training.

## Estimated runtime

<= 30 minutes

## Tasks for Codex

- Create a tiny latent tabular POMDP with aliased observations, including one risky shortcut or stochastic teleporter and one safe path.
- Generate offline trajectories where training inputs are observations, actions, rewards/goals, and bounded history keys only; store latent states only for audit and exact evaluation.
- Implement observation-only empirical model DP, observation-only TRL-log, history-keyed MC-only, history-keyed TRL-log, history-keyed MC+TRL-log, history-model DP, and latent-oracle DP evaluation.
- Use censored long-horizon labels so transitive propagation has a reason to help beyond MC supervision.
- Report metrics stratified by alias regime: heldout MSE, policy regret, risky/teleport action rate, calibration error, and action disagreement with latent-oracle policy.

## Required outputs

- `research/sto_trl/results/0012_result.json`
- `research/sto_trl/results/0012_summary.md`
- `research/sto_trl/artifacts/0012/`


## Latest plan JSON

```json
{
  "estimated_runtime_minutes": 30,
  "experiment_id": "0012",
  "failure_criteria": [
    "History-keyed MC+TRL-log is equivalent to or worse than history-keyed MC-only on heldout long-horizon MSE.",
    "The apparent gain disappears when compared to a prior-matched history-model-DP baseline.",
    "The task requires oracle latent-state access or future-information leakage to show improvement.",
    "The experiment does not include observation-only, history-keyed, and latent-oracle evaluation baselines.",
    "Runtime exceeds 30 minutes or introduces neural networks, continuous control, OGBench, large downloads, or expensive training."
  ],
  "hypothesis": "In a latent tabular MDP with two or more hidden states sharing the same observation, observation-only empirical model DP and observation-only TRL-log will be miscalibrated, while history-keyed MC+TRL-log will improve held-out long-horizon value MSE and policy regret versus history-keyed MC-only without using latent states in training.",
  "objective": "Test whether short trajectory context plus log-space transitive propagation helps in a tiny stochastic POMDP with aliased observations, where observation-level model DP is not a fair Markov baseline.",
  "required_outputs": [
    "research/sto_trl/results/0012_result.json",
    "research/sto_trl/results/0012_summary.md",
    "research/sto_trl/artifacts/0012/"
  ],
  "success_criteria": [
    "Observation-only empirical model DP and observation-only TRL-log show a measurable aliasing failure: higher heldout MSE or policy regret than a latent-oracle evaluation baseline.",
    "History-keyed MC+TRL-log improves heldout long-horizon value MSE over history-keyed MC-only by at least 25% on censored labels.",
    "History-keyed MC+TRL-log improves policy regret or risky/teleport action choice versus observation-only TRL-log on at least one aliased stochastic shortcut or teleporter family.",
    "The report includes a history-model-DP baseline; if history-model-DP fully explains the gain, the result is labeled as representation/context evidence rather than a distinct TRL algorithm win.",
    "No training method uses true latent state, exact DP labels, true transition probabilities, or future observations as inputs."
  ],
  "tasks_for_codex": [
    "Create a tiny latent tabular POMDP with aliased observations, including one risky shortcut or stochastic teleporter and one safe path.",
    "Generate offline trajectories where training inputs are observations, actions, rewards/goals, and bounded history keys only; store latent states only for audit and exact evaluation.",
    "Implement observation-only empirical model DP, observation-only TRL-log, history-keyed MC-only, history-keyed TRL-log, history-keyed MC+TRL-log, history-model DP, and latent-oracle DP evaluation.",
    "Use censored long-horizon labels so transitive propagation has a reason to help beyond MC supervision.",
    "Report metrics stratified by alias regime: heldout MSE, policy regret, risky/teleport action rate, calibration error, and action disagreement with latent-oracle policy."
  ]
}
```


## Latest result summary

```json
{
  "_source": "/home/eston/autoresearcher/research/sto_trl/results/0012_result.json",
  "artifacts": {
    "_type": "list",
    "first_items": [
      "research/sto_trl/artifacts/0012/aliased_pomdp_context_audit.py",
      "research/sto_trl/artifacts/0012/raw_metrics.json",
      "research/sto_trl/artifacts/0012/metrics.csv"
    ],
    "length": 9
  },
  "baseline_metrics": {
    "history_mc_only": {
      "action_disagreement_rate": 0.5,
      "mean_calibration_error": 0.5376375000000001,
      "mean_heldout_long_horizon_value_mse": 0.3404543906250001,
      "mean_policy_regret": 0.018224999999999936,
      "mean_teleport_q_overestimation": 0.0,
      "mean_teleport_q_underestimation": 0.419175,
      "num_rows": 2,
      "teleport_action_rate": 0.0
    },
    "history_model_dp": {
      "action_disagreement_rate": 0.0,
      "mean_calibration_error": 0.0,
      "mean_heldout_long_horizon_value_mse": 0.0,
      "mean_policy_regret": 0.0,
      "mean_teleport_q_overestimation": 0.0,
      "mean_teleport_q_underestimation": 0.0,
      "num_rows": 2,
      "teleport_action_rate": 0.5
    },
    "latent_oracle_dp": {
      "action_disagreement_rate": 0.0,
      "mean_calibration_error": 0.0,
      "mean_heldout_long_horizon_value_mse": 0.0,
      "mean_policy_regret": 0.0,
      "mean_teleport_q_overestimation": 0.0,
      "mean_teleport_q_underestimation": 0.0,
      "num_rows": 2,
      "teleport_action_rate": 0.5
    },
    "observation_empirical_model_dp": {
      "action_disagreement_rate": 0.5,
      "mean_calibration_error": 0.14613749999999995,
      "mean_heldout_long_horizon_value_mse": 0.037554514075413215,
      "mean_policy_regret": 0.018224999999999936,
      "mean_teleport_q_overestimation": 0.1388045454545454,
      "mean_teleport_q_underestimation": 0.13457045454545458,
      "num_rows": 2,
      "teleport_action_rate": 0.0
    },
    "observation_trl_log": {
      "action_disagreement_rate": 0.5,
      "mean_calibration_error": 0.14613749999999995,
      "mean_heldout_long_horizon_value_mse": 0.037554514075413215,
      "mean_policy_regret": 0.018224999999999936,
      "mean_teleport_q_overestimation": 0.1388045454545454,
      "mean_teleport_q_underestimation": 0.13457045454545458,
      "num_rows": 2,
      "teleport_action_rate": 0.0
    }
  },
  "claim_tested": "Short observation history plus log-space transitive propagation was tested in a tiny aliased-observation stochastic POMDP without latent-state training inputs.",
  "experiment_id": "0012",
  "interpretation": "Observation-only model DP and TRL-log fail on the aliased hub because good and bad hidden states share observation 'hub'. Bounded history keys using only the previous cue observation disambiguate the hubs, and history-keyed MC+TRL-log greatly improves censored long-horizon MSE over history-keyed MC-only. The gain is fully matched by history-model DP, so the result supports representation/context value rather than a distinct TRL algorithmic advantage.",
  "known_failures": [
    "history_model_dp fully explains the history-keyed MC+TRL-log gain, so this is representation/context evidence rather than a distinct TRL algorithm win."
  ],
  "metrics": {
    "alias_diagnostics": {
      "history_mc_plus_improves_policy_regret_vs_observation_trl_log": true,
      "history_mc_plus_mse_improvement_fraction_vs_history_mc_only": 1.0,
      "history_model_dp_fully_explains_history_mc_plus_gain": true,
      "obs_alias_failure": true,
      "training_inputs": "observation keys and bounded cue-plus-last-three-observation history keys only; latent states are stored only for audit/evaluation."
    },
    "label_horizon_cutoff": 2,
    "method_summary": {
      "history_mc_only": {
        "_type": "object",
        "key_count": 8,
        "keys": [
          "action_disagreement_rate",
          "mean_calibration_error",
          "mean_heldout_long_horizon_value_mse",
          "mean_policy_regret",
          "mean_teleport_q_overestimation",
          "mean_teleport_q_underestimation",
          "num_rows",
          "teleport_action_rate"
        ]
      },
      "history_mc_plus_trl_log": {
        "_type": "object",
        "key_count": 8,
        "keys": [
          "action_disagreement_rate",
          "mean_calibration_error",
          "mean_heldout_long_horizon_value_mse",
          "mean_policy_regret",
          "mean_teleport_q_overestimation",
          "mean_teleport_q_underestimation",
          "num_rows",
          "teleport_action_rate"
        ]
      },
      "history_model_dp": {
        "_type": "object",
        "key_count": 8,
        "keys": [
          "action_disagreement_rate",
          "mean_calibration_error",
          "mean_heldout_long_horizon_value_mse",
          "mean_policy_regret",
          "mean_teleport_q_overestimation",
          "mean_teleport_q_underestimation",
          "num_rows",
          "teleport_action_rate"
        ]
      },
      "history_trl_log": {
        "_type": "object",
        "key_count": 8,
        "keys": [
          "action_disagreement_rate",
          "mean_calibration_error",
          "mean_heldout_long_horizon_value_mse",
          "mean_policy_regret",
          "mean_teleport_q_overestimation",
          "mean_teleport_q_underestimation",
          "num_rows",
          "teleport_action_rate"
        ]
      },
      "latent_oracle_dp": {
        "_type": "object",
        "key_count": 8,
        "keys": [
          "action_disagreement_rate",
          "mean_calibration_error",
          "mean_heldout_long_horizon_value_mse",
          "mean_policy_regret",
          "mean_teleport_q_overestimation",
          "mean_teleport_q_underestimation",
          "num_rows",
          "teleport_action_rate"
        ]
      },
      "observation_empirical_model_dp": {
        "_type": "object",
        "key_count": 8,
        "keys": [
          "action_disagreement_rate",
          "mean_calibration_error",
          "mean_heldout_long_horizon_value_mse",
          "mean_policy_regret",
          "mean_teleport_q_overestimation",
          "mean_teleport_q_underestimation",
          "num_rows",
          "teleport_action_rate"
        ]
      },
      "observation_trl_log": {
        "_type": "object",
        "key_count": 8,
        "keys": [
          "action_disagreement_rate",
          "mean_calibration_error",
          "mean_heldout_long_horizon_value_mse",
          "mean_policy_regret",
          "mean_teleport_q_overestimation",
          "mean_teleport_q_underestimation",
          "num_rows",
          "teleport_action_rate"
        ]
      }
    },
    "num_trajectories": 56,
    "success_criteria_met": {
      "history_mc_plus_mse_improvement_at_least_25_percent": true,
      "history_mc_plus_policy_or_action_improvement_vs_observation_trl_log": true,
      "history_model_dp_included_and_explains_gain": true,
      "observation_aliasing_failure": true
    }
  },
  "next_questions": [
    "Can a non-model TRL objective exploit bounded history when model DP is unavailable or prohibitively large?",
    "How sensitive is the history key length to noisier cue observations?",
    "Should future stochastic TRL benchmarks include explicit aliasing/context diagnostics?"
  ],
  "status": "completed"
}
```


## Latest summary

# Experiment 0012 Summary

## Objective

Test whether short trajectory context plus log-space transitive propagation helps in a tiny stochastic POMDP with aliased observations.

## Commands Run

```bash
mkdir -p research/sto_trl/artifacts/0012 research/sto_trl/results
conda run -n autoresearcher_sto_trl python research/sto_trl/artifacts/0012/aliased_pomdp_context_audit.py
conda run -n autoresearcher_sto_trl python scripts/validate_artifacts.py --repo-root . --json research/sto_trl/results/0012_result.json --schema schemas/result.schema.json --check-result-artifacts
```

## Setup

- Hidden hubs: `hub_good` and `hub_bad`
- Aliased observation: `hub`
- History key: cue observation plus the last three observations, e.g. `cue_g|cue_g>hub`
- Label horizon cutoff: `2`
- Trajectories: `56`

## Method Summary

| Method | Heldout MSE | Policy regret | Teleport rate | Calibration error | Action disagreement |
| --- | ---: | ---: | ---: | ---: | ---: |
| history_mc_only | 0.340454390625 | 0.018225000000 | 0.000000 | 0.537637500000 | 0.500000 |
| history_mc_plus_trl_log | 0.000000000000 | 0.000000000000 | 0.500000 | 0.000000000000 | 0.000000 |
| history_model_dp | 0.000000000000 | 0.000000000000 | 0.500000 | 0.000000000000 | 0.000000 |
| history_trl_log | 0.000000000000 | 0.000000000000 | 0.500000 | 0.000000000000 | 0.000000 |
| latent_oracle_dp | 0.000000000000 | 0.000000000000 | 0.500000 | 0.000000000000 | 0.000000 |
| observation_empirical_model_dp | 0.037554514075 | 0.018225000000 | 0.000000 | 0.146137500000 | 0.500000 |
| observation_trl_log | 0.037554514075 | 0.018225000000 | 0.000000 | 0.146137500000 | 0.500000 |

## Decision Findings

- Observation-only aliasing failure: `True`
- History MC+TRL-log MSE improvement vs history MC-only: `1.000000`
- History MC+TRL-log improves policy regret vs observation TRL-log: `True`
- History-model DP fully explains the gain: `True`

## Interpretation

Observation-only model DP and TRL-log fail on the aliased hub because good and bad hidden states share observation 'hub'. Bounded history keys using only the previous cue observation disambiguate the hubs, and history-keyed MC+TRL-log greatly improves censored long-horizon MSE over history-keyed MC-only. The gain is fully matched by history-model DP, so the result supports representation/context value rather than a distinct TRL algorithmic advantage.

## Artifacts

- `research/sto_trl/artifacts/0012/aliased_pomdp_context_audit.py`
- `research/sto_trl/artifacts/0012/raw_metrics.json`
- `research/sto_trl/artifacts/0012/metrics.csv`
- `research/sto_trl/artifacts/0012/alias_summary.csv`
- `research/sto_trl/artifacts/0012/coverage_diagnostics.json`
- `research/sto_trl/artifacts/0012/offline_trajectories.json`
- `research/sto_trl/artifacts/0012/transition_tables.json`
- `research/sto_trl/artifacts/0012/value_tables.json`
- `research/sto_trl/artifacts/0012/alias_diagnostics.json`


## Full evidence paths

- `research/sto_trl/results/0012_result.json`
- `research/sto_trl/results/0012_summary.md`

Inspect the full result JSON only when the compact summary and artifact list are insufficient.


## Artifact paths

- `/home/eston/autoresearcher/research/sto_trl/artifacts/0008`
- `/home/eston/autoresearcher/research/sto_trl/artifacts/0009`
- `/home/eston/autoresearcher/research/sto_trl/artifacts/0010`
- `/home/eston/autoresearcher/research/sto_trl/artifacts/0011`
- `/home/eston/autoresearcher/research/sto_trl/artifacts/0012`


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
