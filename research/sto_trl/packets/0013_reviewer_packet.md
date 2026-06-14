# Reviewer Context: sto_trl

## Latest plan

# Experiment 0013

## Objective

Test whether the partial-observation/context pivot generalizes beyond the single hand-constructed 0012 POMDP and whether any TRL-style transitive component adds value beyond history-model DP.

## Hypothesis

Across a small randomized suite of aliased tabular POMDPs with varying cue reliability and history sufficiency, observation-only methods will fail when observations alias latent states, bounded-history methods will improve when history is sufficient, and a viable TRL/context direction requires MC+TRL-log to improve over history MC-only without being fully explained by history-model DP on every regime.

## Success criteria

- Run at least 3 tiny POMDP families with 5 fixed seeds each, including cue-sufficient, cue-noisy, and cue-insufficient regimes.
- Observation-only TRL-log and observation-only model DP have higher heldout MSE or policy regret than latent-oracle evaluation in aliased regimes.
- History-keyed MC+TRL-log improves heldout MSE over history-keyed MC-only by at least 25% averaged over cue-sufficient regimes.
- The report explicitly compares history-keyed MC+TRL-log against history-model DP; if model DP fully explains all gains, the result is labeled boundary/negative for TRL algorithmic value.
- No training method consumes latent states, exact DP labels, true transition probabilities, or future observations as inputs.

## Failure criteria

- History-keyed MC+TRL-log is not better than history-keyed MC-only in cue-sufficient regimes.
- All gains are fully matched by history-model DP with zero action disagreement and no heldout-MSE gap.
- The only positive cases use history keys that directly encode the latent state or otherwise leak oracle information.
- Cue-noisy or cue-insufficient regimes are omitted, preventing separation of context sufficiency from oracle disambiguation.
- Runtime exceeds 30 minutes or introduces neural networks, continuous control, OGBench, large downloads, or expensive training.

## Estimated runtime

<= 30 minutes

## Tasks for Codex

- Generate a randomized suite of tiny latent tabular POMDPs with aliased observations, stochastic shortcuts or teleporters, and controlled cue reliability.
- Evaluate observation-only empirical model DP, observation-only TRL-log, history MC-only, history TRL-log, history MC+TRL-log, history-model DP, and latent-oracle DP.
- Keep latent states only for audit and exact evaluation; add explicit leakage checks confirming training keys are observation/history-only.
- Stratify metrics by cue-sufficient, cue-noisy, and cue-insufficient regimes.
- Write a summary that decides whether this is real representation/context evidence or another model-DP-equivalence boundary.

## Required outputs

- `research/sto_trl/results/0013_result.json`
- `research/sto_trl/results/0013_summary.md`
- `research/sto_trl/artifacts/0013/`


## Latest plan JSON

```json
{
  "estimated_runtime_minutes": 30,
  "experiment_id": "0013",
  "failure_criteria": [
    "History-keyed MC+TRL-log is not better than history-keyed MC-only in cue-sufficient regimes.",
    "All gains are fully matched by history-model DP with zero action disagreement and no heldout-MSE gap.",
    "The only positive cases use history keys that directly encode the latent state or otherwise leak oracle information.",
    "Cue-noisy or cue-insufficient regimes are omitted, preventing separation of context sufficiency from oracle disambiguation.",
    "Runtime exceeds 30 minutes or introduces neural networks, continuous control, OGBench, large downloads, or expensive training."
  ],
  "hypothesis": "Across a small randomized suite of aliased tabular POMDPs with varying cue reliability and history sufficiency, observation-only methods will fail when observations alias latent states, bounded-history methods will improve when history is sufficient, and a viable TRL/context direction requires MC+TRL-log to improve over history MC-only without being fully explained by history-model DP on every regime.",
  "objective": "Test whether the partial-observation/context pivot generalizes beyond the single hand-constructed 0012 POMDP and whether any TRL-style transitive component adds value beyond history-model DP.",
  "required_outputs": [
    "research/sto_trl/results/0013_result.json",
    "research/sto_trl/results/0013_summary.md",
    "research/sto_trl/artifacts/0013/"
  ],
  "success_criteria": [
    "Run at least 3 tiny POMDP families with 5 fixed seeds each, including cue-sufficient, cue-noisy, and cue-insufficient regimes.",
    "Observation-only TRL-log and observation-only model DP have higher heldout MSE or policy regret than latent-oracle evaluation in aliased regimes.",
    "History-keyed MC+TRL-log improves heldout MSE over history-keyed MC-only by at least 25% averaged over cue-sufficient regimes.",
    "The report explicitly compares history-keyed MC+TRL-log against history-model DP; if model DP fully explains all gains, the result is labeled boundary/negative for TRL algorithmic value.",
    "No training method consumes latent states, exact DP labels, true transition probabilities, or future observations as inputs."
  ],
  "tasks_for_codex": [
    "Generate a randomized suite of tiny latent tabular POMDPs with aliased observations, stochastic shortcuts or teleporters, and controlled cue reliability.",
    "Evaluate observation-only empirical model DP, observation-only TRL-log, history MC-only, history TRL-log, history MC+TRL-log, history-model DP, and latent-oracle DP.",
    "Keep latent states only for audit and exact evaluation; add explicit leakage checks confirming training keys are observation/history-only.",
    "Stratify metrics by cue-sufficient, cue-noisy, and cue-insufficient regimes.",
    "Write a summary that decides whether this is real representation/context evidence or another model-DP-equivalence boundary."
  ]
}
```


## Latest result summary

```json
{
  "_source": "/home/eston/autoresearcher/research/sto_trl/results/0013_result.json",
  "artifacts": {
    "_type": "list",
    "first_items": [
      "research/sto_trl/artifacts/0013/randomized_pomdp_context_audit.py",
      "research/sto_trl/artifacts/0013/raw_metrics.json",
      "research/sto_trl/artifacts/0013/metrics.csv"
    ],
    "length": 10
  },
  "baseline_metrics": {
    "history_mc_only": {
      "action_disagreement_rate": 0.5,
      "mean_calibration_error": 0.5364225000000001,
      "mean_heldout_long_horizon_value_mse": 0.340365817125,
      "mean_policy_regret": 0.018224999999999936,
      "mean_teleport_q_overestimation": 0.0,
      "mean_teleport_q_underestimation": 0.4167449999999999,
      "num_rows": 40,
      "teleport_action_rate": 0.0,
      "weight_sum": 30.0
    },
    "history_model_dp": {
      "action_disagreement_rate": 0.3333333333333333,
      "mean_calibration_error": 0.0906910714285714,
      "mean_heldout_long_horizon_value_mse": 0.025861880330357138,
      "mean_policy_regret": 0.012149999999999958,
      "mean_teleport_q_overestimation": 0.09069107142857144,
      "mean_teleport_q_underestimation": 0.09069107142857141,
      "num_rows": 40,
      "teleport_action_rate": 0.16666666666666666,
      "weight_sum": 30.0
    },
    "latent_oracle_dp": {
      "action_disagreement_rate": 0.0,
      "mean_calibration_error": 0.0,
      "mean_heldout_long_horizon_value_mse": 0.0,
      "mean_policy_regret": 0.0,
      "mean_teleport_q_overestimation": 0.0,
      "mean_teleport_q_underestimation": 0.0,
      "num_rows": 40,
      "teleport_action_rate": 0.5,
      "weight_sum": 30.0
    },
    "observation_empirical_model_dp": {
      "action_disagreement_rate": 0.5,
      "mean_calibration_error": 0.14735249999999994,
      "mean_heldout_long_horizon_value_mse": 0.03835158520351239,
      "mean_policy_regret": 0.018224999999999936,
      "mean_teleport_q_overestimation": 0.1400072727272727,
      "mean_teleport_q_underestimation": 0.1357977272727273,
      "num_rows": 40,
      "teleport_action_rate": 0.0,
      "weight_sum": 30.0
    },
    "observation_trl_log": {
      "action_disagreement_rate": 0.5,
      "mean_calibration_error": 0.14735249999999994,
      "mean_heldout_long_horizon_value_mse": 0.03835158520351239,
      "mean_policy_regret": 0.018224999999999936,
      "mean_teleport_q_overestimation": 0.1400072727272727,
      "mean_teleport_q_underestimation": 0.1357977272727273,
      "num_rows": 40,
      "teleport_action_rate": 0.0,
      "weight_sum": 30.0
    }
  },
  "claim_tested": "A randomized aliased-POMDP suite tested whether bounded observation history generalizes the 0012 context pivot and whether MC+TRL-log adds value beyond history-model DP.",
  "experiment_id": "0013",
  "interpretation": "Observation-only methods fail under aliasing, and bounded history improves strongly when cues are sufficient. Cue-noisy and cue-insufficient families separate representation sufficiency from oracle disambiguation. History MC+TRL-log improves over MC-only, but the gains are fully explained by history-model DP, so this is representation/context evidence and a boundary result for TRL algorithmic value.",
  "known_failures": [
    "history-model DP fully matches history MC+TRL-log gains, so this is boundary/negative for distinct TRL algorithmic value."
  ],
  "metrics": {
    "cue_regimes_present": true,
    "cue_sufficient_history_mc_plus_improvement_fraction_vs_mc_only": 1.0,
    "cue_sufficient_summary": {
      "history_mc_only": {
        "_type": "object",
        "key_count": 9,
        "keys": [
          "action_disagreement_rate",
          "mean_calibration_error",
          "mean_heldout_long_horizon_value_mse",
          "mean_policy_regret",
          "mean_teleport_q_overestimation",
          "mean_teleport_q_underestimation",
          "num_rows",
          "teleport_action_rate",
          "weight_sum"
        ]
      },
      "history_mc_plus_trl_log": {
        "_type": "object",
        "key_count": 9,
        "keys": [
          "action_disagreement_rate",
          "mean_calibration_error",
          "mean_heldout_long_horizon_value_mse",
          "mean_policy_regret",
          "mean_teleport_q_overestimation",
          "mean_teleport_q_underestimation",
          "num_rows",
          "teleport_action_rate",
          "weight_sum"
        ]
      },
      "history_model_dp": {
        "_type": "object",
        "key_count": 9,
        "keys": [
          "action_disagreement_rate",
          "mean_calibration_error",
          "mean_heldout_long_horizon_value_mse",
          "mean_policy_regret",
          "mean_teleport_q_overestimation",
          "mean_teleport_q_underestimation",
          "num_rows",
          "teleport_action_rate",
          "weight_sum"
        ]
      },
      "history_trl_log": {
        "_type": "object",
        "key_count": 9,
        "keys": [
          "action_disagreement_rate",
          "mean_calibration_error",
          "mean_heldout_long_horizon_value_mse",
          "mean_policy_regret",
          "mean_teleport_q_overestimation",
          "mean_teleport_q_underestimation",
          "num_rows",
          "teleport_action_rate",
          "weight_sum"
        ]
      },
      "latent_oracle_dp": {
        "_type": "object",
        "key_count": 9,
        "keys": [
          "action_disagreement_rate",
          "mean_calibration_error",
          "mean_heldout_long_horizon_value_mse",
          "mean_policy_regret",
          "mean_teleport_q_overestimation",
          "mean_teleport_q_underestimation",
          "num_rows",
          "teleport_action_rate",
          "weight_sum"
        ]
      },
      "observation_empirical_model_dp": {
        "_type": "object",
        "key_count": 9,
        "keys": [
          "action_disagreement_rate",
          "mean_calibration_error",
          "mean_heldout_long_horizon_value_mse",
          "mean_policy_regret",
          "mean_teleport_q_overestimation",
          "mean_teleport_q_underestimation",
          "num_rows",
          "teleport_action_rate",
          "weight_sum"
        ]
      },
      "observation_trl_log": {
        "_type": "object",
        "key_count": 9,
        "keys": [
          "action_disagreement_rate",
          "mean_calibration_error",
          "mean_heldout_long_horizon_value_mse",
          "mean_policy_regret",
          "mean_teleport_q_overestimation",
          "mean_teleport_q_underestimation",
          "num_rows",
          "teleport_action_rate",
          "weight_sum"
        ]
      }
    },
    "leakage_free_training_keys": true,
    "method_summary": {
      "history_mc_only": {
        "_type": "object",
        "key_count": 9,
        "keys": [
          "action_disagreement_rate",
          "mean_calibration_error",
          "mean_heldout_long_horizon_value_mse",
          "mean_policy_regret",
          "mean_teleport_q_overestimation",
          "mean_teleport_q_underestimation",
          "num_rows",
          "teleport_action_rate",
          "weight_sum"
        ]
      },
      "history_mc_plus_trl_log": {
        "_type": "object",
        "key_count": 9,
        "keys": [
          "action_disagreement_rate",
          "mean_calibration_error",
          "mean_heldout_long_horizon_value_mse",
          "mean_policy_regret",
          "mean_teleport_q_overestimation",
          "mean_teleport_q_underestimation",
          "num_rows",
          "teleport_action_rate",
          "weight_sum"
        ]
      },
      "history_model_dp": {
        "_type": "object",
        "key_count": 9,
        "keys": [
          "action_disagreement_rate",
          "mean_calibration_error",
          "mean_heldout_long_horizon_value_mse",
          "mean_policy_regret",
          "mean_teleport_q_overestimation",
          "mean_teleport_q_underestimation",
          "num_rows",
          "teleport_action_rate",
          "weight_sum"
        ]
      },
      "history_trl_log": {
        "_type": "object",
        "key_count": 9,
        "keys": [
          "action_disagreement_rate",
          "mean_calibration_error",
          "mean_heldout_long_horizon_value_mse",
          "mean_policy_regret",
          "mean_teleport_q_overestimation",
          "mean_teleport_q_underestimation",
          "num_rows",
          "teleport_action_rate",
          "weight_sum"
        ]
      },
      "latent_oracle_dp": {
        "_type": "object",
        "key_count": 9,
        "keys": [
          "action_disagreement_rate",
          "mean_calibration_error",
          "mean_heldout_long_horizon_value_mse",
          "mean_policy_regret",
          "mean_teleport_q_overestimation",
          "mean_teleport_q_underestimation",
          "num_rows",
          "teleport_action_rate",
          "weight_sum"
        ]
      },
      "observation_empirical_model_dp": {
        "_type": "object",
        "key_count": 9,
        "keys": [
          "action_disagreement_rate",
          "mean_calibration_error",
          "mean_heldout_long_horizon_value_mse",
          "mean_policy_regret",
          "mean_teleport_q_overestimation",
          "mean_teleport_q_underestimation",
          "num_rows",
          "teleport_action_rate",
          "weight_sum"
        ]
      },
      "observation_trl_log": {
        "_type": "object",
        "key_count": 9,
        "keys": [
          "action_disagreement_rate",
          "mean_calibration_error",
          "mean_heldout_long_horizon_value_mse",
          "mean_policy_regret",
          "mean_teleport_q_overestimation",
          "mean_teleport_q_underestimation",
          "num_rows",
          "teleport_action_rate",
          "weight_sum"
        ]
      }
    },
    "model_dp_explains_all_history_mc_plus_gains": true,
    "num_cases": 15,
    "num_metric_rows": 280,
    "observation_aliasing_failure": true
  },
  "next_questions": [
    "Can non-model TRL exploit history when the history-model state space is too large for exact DP?",
    "How should cue reliability be estimated before deciding whether history context is sufficient?",
    "Can a future benchmark include noisy cues without latent leakage while still requiring policy improvement?"
  ],
  "status": "completed"
}
```


## Latest summary

# Experiment 0013 Summary

## Objective

Test whether the partial-observation/context pivot generalizes beyond the single hand-constructed 0012 POMDP and whether any TRL-style transitive component adds value beyond history-model DP.

## Commands Run

```bash
mkdir -p research/sto_trl/artifacts/0013 research/sto_trl/results
conda run -n autoresearcher_sto_trl python research/sto_trl/artifacts/0013/randomized_pomdp_context_audit.py
conda run -n autoresearcher_sto_trl python scripts/validate_artifacts.py --repo-root . --json research/sto_trl/results/0013_result.json --schema schemas/result.schema.json --check-result-artifacts
```

## Suite

- Families: `['cue_sufficient', 'cue_noisy', 'cue_insufficient']`
- Seeds: `[0, 1, 2, 3, 4]`
- Cases: `15`
- Label horizon cutoff: `2`

## Method Summary

| Method | Heldout MSE | Policy regret | Teleport rate | Calibration error | Action disagreement |
| --- | ---: | ---: | ---: | ---: | ---: |
| history_mc_only | 0.340365817125 | 0.018225000000 | 0.000000 | 0.536422500000 | 0.500000 |
| history_mc_plus_trl_log | 0.025861880330 | 0.012150000000 | 0.166667 | 0.090691071429 | 0.333333 |
| history_model_dp | 0.025861880330 | 0.012150000000 | 0.166667 | 0.090691071429 | 0.333333 |
| history_trl_log | 0.025861880330 | 0.012150000000 | 0.166667 | 0.090691071429 | 0.333333 |
| latent_oracle_dp | 0.000000000000 | 0.000000000000 | 0.500000 | 0.000000000000 | 0.000000 |
| observation_empirical_model_dp | 0.038351585204 | 0.018225000000 | 0.000000 | 0.147352500000 | 0.500000 |
| observation_trl_log | 0.038351585204 | 0.018225000000 | 0.000000 | 0.147352500000 | 0.500000 |

## Decision Findings

- Observation-only aliasing failure: `True`
- Cue-sufficient MC+TRL-log improvement vs MC-only: `1.000000`
- History-model DP explains all gains: `True`
- Leakage-free training keys: `True`

## Interpretation

Observation-only methods fail under aliasing, and bounded history improves strongly when cues are sufficient. Cue-noisy and cue-insufficient families separate representation sufficiency from oracle disambiguation. History MC+TRL-log improves over MC-only, but the gains are fully explained by history-model DP, so this is representation/context evidence and a boundary result for TRL algorithmic value.

## Artifacts

- `research/sto_trl/artifacts/0013/randomized_pomdp_context_audit.py`
- `research/sto_trl/artifacts/0013/raw_metrics.json`
- `research/sto_trl/artifacts/0013/metrics.csv`
- `research/sto_trl/artifacts/0013/family_summary.csv`
- `research/sto_trl/artifacts/0013/context_summary.csv`
- `research/sto_trl/artifacts/0013/coverage_diagnostics.json`
- `research/sto_trl/artifacts/0013/offline_datasets.json`
- `research/sto_trl/artifacts/0013/transition_tables.json`
- `research/sto_trl/artifacts/0013/value_tables.json`
- `research/sto_trl/artifacts/0013/leakage_checks.json`


## Full evidence paths

- `research/sto_trl/results/0013_result.json`
- `research/sto_trl/results/0013_summary.md`

Inspect the full result JSON only when the compact summary and artifact list are insufficient.


## Artifact paths

- `/home/eston/autoresearcher/research/sto_trl/artifacts/0009`
- `/home/eston/autoresearcher/research/sto_trl/artifacts/0010`
- `/home/eston/autoresearcher/research/sto_trl/artifacts/0011`
- `/home/eston/autoresearcher/research/sto_trl/artifacts/0012`
- `/home/eston/autoresearcher/research/sto_trl/artifacts/0013`


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
