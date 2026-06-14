# Reviewer Context: sto_trl

## Latest plan

# Experiment 0011

## Objective

Run a small randomized tabular equivalence and generalization audit to test whether posterior TRL-log has any distinct benefit over prior-matched posterior model DP beyond the handcrafted 0010 branch-chain regimes.

## Hypothesis

Across tiny randomized branch-chain, stochastic stitching, and stochastic teleporter-style tabular MDPs with exact DP ground truth and finite offline coverage, posterior_trl_log will usually remain equivalent or near-equivalent to prior-matched posterior model DP. A credible positive result requires a predeclared regime where posterior_trl_log improves value or policy metrics over both TRL-log and prior-matched posterior model DP without relying on model-DP misspecification or conservative risk avoidance.

## Success criteria

- Creates a self-contained artifact under research/sto_trl/artifacts/0011/ without editing prior results, schemas, AGENTS.md, scripts/autoresearcher.py, or environment files.
- Uses exact DP ground truth for every generated tabular MDP and keeps total runtime under 30 minutes.
- Predeclares a tiny randomized suite, such as 3 MDP families with 5 seeds each: branch-chain, stochastic stitching graph, and stochastic teleporter graph.
- Includes finite offline coverage regimes with matched coverage, lucky-only coverage, no-success coverage, and sparse long-horizon label censoring where applicable.
- Compares mc_supervised, trl_raw, trl_log, empirical_model_dp, posterior_mean_model_dp, posterior_lower or robust model DP, posterior_trl_log, and posterior_mc_plus_trl_log using prior-matched assumptions.
- Reports per-family and per-regime heldout long-horizon value MSE, all-pair value MSE, Q overestimation and underestimation, calibration error, policy regret, risky action selection rate, and coverage diagnostics.
- Reports an explicit equivalence audit: max absolute value difference, action disagreement rate, and metric deltas between posterior_trl_log and prior-matched posterior model DP.
- Counts positive evidence only if posterior_trl_log or posterior_mc_plus_trl_log beats both TRL-log and prior-matched posterior model DP on predeclared metrics while preserving matched risk-optimal action choice and avoiding safe-everywhere behavior.
- Counts equivalence, near-equivalence, or improvement only from prior choice as negative or boundary evidence.
- Produces valid research/sto_trl/results/0011_result.json and research/sto_trl/results/0011_summary.md with exact commands run.

## Failure criteria

- The experiment omits prior-matched posterior model-DP baselines or does not report direct equivalence diagnostics.
- The experiment creates a TRL advantage by making transition-model DP unavailable, deliberately misspecified, or evaluated with less information than posterior TRL uses.
- Exact DP values or true transition probabilities are used for training or action selection rather than only evaluation and audit artifacts.
- The suite expands beyond a tiny tabular CPU-scale audit or exceeds 30 minutes.
- The result reports only aggregate averages without per-family, per-regime, and coverage-stratified metrics.
- A method is treated as successful because it is conservative everywhere or fails matched risk-optimal action selection.
- The run moves to neural networks, continuous control, PointMaze, AntMaze, OGBench, large downloads, or expensive training.

## Estimated runtime

<= 25 minutes

## Tasks for Codex

- Create research/sto_trl/artifacts/0011/ and implement a small randomized_equivalence_audit.py script, reusing prior tabular helpers where practical.
- Define a tiny predeclared randomized suite with fixed seeds for branch-chain, stochastic stitching, and stochastic teleporter-style MDPs.
- Generate finite offline datasets and censored long-horizon labels for each seed while saving coverage diagnostics and offline dataset summaries.
- Implement prior-matched empirical and posterior model-DP baselines plus posterior_trl_log and posterior_mc_plus_trl_log variants.
- Compute exact DP ground truth for all generated MDPs and evaluate value, calibration, overestimation, policy, action-selection, and equivalence metrics.
- Save raw_metrics.json, metrics.csv, family_summary.csv, regime_summary.csv, equivalence_diagnostics.json, coverage_diagnostics.json, transition_tables.json, and value_tables.json under research/sto_trl/artifacts/0011/.
- Write research/sto_trl/results/0011_result.json and research/sto_trl/results/0011_summary.md, then validate the result JSON with scripts/validate_artifacts.py and artifact checks.

## Required outputs

- `research/sto_trl/results/0011_result.json`
- `research/sto_trl/results/0011_summary.md`
- `research/sto_trl/artifacts/0011/`


## Latest plan JSON

```json
{
  "estimated_runtime_minutes": 25,
  "experiment_id": "0011",
  "failure_criteria": [
    "The experiment omits prior-matched posterior model-DP baselines or does not report direct equivalence diagnostics.",
    "The experiment creates a TRL advantage by making transition-model DP unavailable, deliberately misspecified, or evaluated with less information than posterior TRL uses.",
    "Exact DP values or true transition probabilities are used for training or action selection rather than only evaluation and audit artifacts.",
    "The suite expands beyond a tiny tabular CPU-scale audit or exceeds 30 minutes.",
    "The result reports only aggregate averages without per-family, per-regime, and coverage-stratified metrics.",
    "A method is treated as successful because it is conservative everywhere or fails matched risk-optimal action selection.",
    "The run moves to neural networks, continuous control, PointMaze, AntMaze, OGBench, large downloads, or expensive training."
  ],
  "hypothesis": "Across tiny randomized branch-chain, stochastic stitching, and stochastic teleporter-style tabular MDPs with exact DP ground truth and finite offline coverage, posterior_trl_log will usually remain equivalent or near-equivalent to prior-matched posterior model DP. A credible positive result requires a predeclared regime where posterior_trl_log improves value or policy metrics over both TRL-log and prior-matched posterior model DP without relying on model-DP misspecification or conservative risk avoidance.",
  "objective": "Run a small randomized tabular equivalence and generalization audit to test whether posterior TRL-log has any distinct benefit over prior-matched posterior model DP beyond the handcrafted 0010 branch-chain regimes.",
  "required_outputs": [
    "research/sto_trl/results/0011_result.json",
    "research/sto_trl/results/0011_summary.md",
    "research/sto_trl/artifacts/0011/"
  ],
  "success_criteria": [
    "Creates a self-contained artifact under research/sto_trl/artifacts/0011/ without editing prior results, schemas, AGENTS.md, scripts/autoresearcher.py, or environment files.",
    "Uses exact DP ground truth for every generated tabular MDP and keeps total runtime under 30 minutes.",
    "Predeclares a tiny randomized suite, such as 3 MDP families with 5 seeds each: branch-chain, stochastic stitching graph, and stochastic teleporter graph.",
    "Includes finite offline coverage regimes with matched coverage, lucky-only coverage, no-success coverage, and sparse long-horizon label censoring where applicable.",
    "Compares mc_supervised, trl_raw, trl_log, empirical_model_dp, posterior_mean_model_dp, posterior_lower or robust model DP, posterior_trl_log, and posterior_mc_plus_trl_log using prior-matched assumptions.",
    "Reports per-family and per-regime heldout long-horizon value MSE, all-pair value MSE, Q overestimation and underestimation, calibration error, policy regret, risky action selection rate, and coverage diagnostics.",
    "Reports an explicit equivalence audit: max absolute value difference, action disagreement rate, and metric deltas between posterior_trl_log and prior-matched posterior model DP.",
    "Counts positive evidence only if posterior_trl_log or posterior_mc_plus_trl_log beats both TRL-log and prior-matched posterior model DP on predeclared metrics while preserving matched risk-optimal action choice and avoiding safe-everywhere behavior.",
    "Counts equivalence, near-equivalence, or improvement only from prior choice as negative or boundary evidence.",
    "Produces valid research/sto_trl/results/0011_result.json and research/sto_trl/results/0011_summary.md with exact commands run."
  ],
  "tasks_for_codex": [
    "Create research/sto_trl/artifacts/0011/ and implement a small randomized_equivalence_audit.py script, reusing prior tabular helpers where practical.",
    "Define a tiny predeclared randomized suite with fixed seeds for branch-chain, stochastic stitching, and stochastic teleporter-style MDPs.",
    "Generate finite offline datasets and censored long-horizon labels for each seed while saving coverage diagnostics and offline dataset summaries.",
    "Implement prior-matched empirical and posterior model-DP baselines plus posterior_trl_log and posterior_mc_plus_trl_log variants.",
    "Compute exact DP ground truth for all generated MDPs and evaluate value, calibration, overestimation, policy, action-selection, and equivalence metrics.",
    "Save raw_metrics.json, metrics.csv, family_summary.csv, regime_summary.csv, equivalence_diagnostics.json, coverage_diagnostics.json, transition_tables.json, and value_tables.json under research/sto_trl/artifacts/0011/.",
    "Write research/sto_trl/results/0011_result.json and research/sto_trl/results/0011_summary.md, then validate the result JSON with scripts/validate_artifacts.py and artifact checks."
  ]
}
```


## Latest result summary

```json
{
  "_source": "/home/eston/autoresearcher/research/sto_trl/results/0011_result.json",
  "artifacts": {
    "_type": "list",
    "first_items": [
      "research/sto_trl/artifacts/0011/randomized_equivalence_audit.py",
      "research/sto_trl/artifacts/0011/raw_metrics.json",
      "research/sto_trl/artifacts/0011/metrics.csv"
    ],
    "length": 10
  },
  "baseline_metrics": {
    "empirical_model_dp": {
      "action_accuracy": 0.4,
      "mean_all_pair_value_mse": 0.04481289688774978,
      "mean_heldout_long_horizon_value_mse": 0.03765166954543893,
      "mean_policy_regret": 0.06840668344867584,
      "mean_risky_q_calibration_error": 0.22652428374775355,
      "mean_risky_q_overestimation": 0.07214453318022322,
      "mean_risky_q_underestimation": 0.15437975056753034,
      "num_rows": 15,
      "risky_action_selection_rate": 0.4
    },
    "mc_supervised": {
      "action_accuracy": 0.4,
      "mean_all_pair_value_mse": 0.23531227403396845,
      "mean_heldout_long_horizon_value_mse": 0.432704401392902,
      "mean_policy_regret": 0.028055308380006028,
      "mean_risky_q_calibration_error": 0.5690452173873072,
      "mean_risky_q_overestimation": 0.0,
      "mean_risky_q_underestimation": 0.5690452173873072,
      "num_rows": 15,
      "risky_action_selection_rate": 0.0
    },
    "posterior_lower_q10_model_dp": {
      "action_accuracy": 0.4666666666666667,
      "mean_all_pair_value_mse": 0.04437558018198091,
      "mean_heldout_long_horizon_value_mse": 0.03592521474547472,
      "mean_policy_regret": 0.02218223230951611,
      "mean_risky_q_calibration_error": 0.2615099351506468,
      "mean_risky_q_overestimation": 0.01626917888166985,
      "mean_risky_q_underestimation": 0.245240756268977,
      "num_rows": 15,
      "risky_action_selection_rate": 0.06666666666666667
    },
    "posterior_mean_model_dp": {
      "action_accuracy": 0.6,
      "mean_all_pair_value_mse": 0.0423569966153239,
      "mean_heldout_long_horizon_value_mse": 0.032259348981387076,
      "mean_policy_regret": 0.012917304567005971,
      "mean_risky_q_calibration_error": 0.21422137774804942,
      "mean_risky_q_overestimation": 0.045769378881669855,
      "mean_risky_q_underestimation": 0.16845199886637957,
      "num_rows": 15,
      "risky_action_selection_rate": 0.2
    },
    "trl_log": {
      "action_accuracy": 0.4,
      "mean_all_pair_value_mse": 0.04481289688774978,
      "mean_heldout_long_horizon_value_mse": 0.03765166954543893,
      "mean_policy_regret": 0.06840668344867584,
      "mean_risky_q_calibration_error": 0.22652428374775355,
      "mean_risky_q_overestimation": 0.07214453318022322,
      "mean_risky_q_underestimation": 0.15437975056753034,
      "num_rows": 15,
      "risky_action_selection_rate": 0.4
    }
  },
  "claim_tested": "A fixed tiny randomized suite tested whether posterior TRL-log has distinct value over prior-matched posterior model DP beyond handcrafted branch-chain regimes.",
  "experiment_id": "0011",
  "interpretation": "The randomized tiny-suite audit supports the 0010 boundary result: posterior TRL-log variants match the prior-matched posterior mean model-DP baseline within numerical tolerance across branch-chain, stochastic stitching, and teleporter families. Any aggregate improvement over plain TRL-log is explained by the shared posterior transition prior, not by a distinct transitive posterior TRL effect.",
  "known_failures": [
    "posterior_trl_log and posterior_mc_plus_trl_log were near-equivalent to prior-matched posterior mean model DP across the randomized suite.",
    "No credible posterior TRL benefit over both TRL-log and prior-matched posterior model DP was detected."
  ],
  "metrics": {
    "coverage_diagnostics": {
      "label_horizon_cutoff": 2,
      "tag_counts": {
        "_type": "object",
        "key_count": 9,
        "keys": [
          "ambiguous",
          "biased_coverage",
          "lucky_only",
          "matched",
          "no_success",
          "prior_dependent",
          "risk_optimal",
          "safe_optimal",
          "sparse_coverage"
        ]
      }
    },
    "equivalence_aggregate": {
      "action_disagreement_rate_posterior_mc_plus_vs_model": 0.0,
      "action_disagreement_rate_posterior_trl_log_vs_model": 0.0,
      "best_candidate": "posterior_mc_plus_trl_log",
      "candidate_improves_vs_prior_matched_model_dp": false,
      "candidate_improves_vs_trl_log": true,
      "matched_risk_optimal_preserved": true,
      "max_abs_value_diff_posterior_mc_plus_vs_model": 3.3306690738754696e-16,
      "max_abs_value_diff_posterior_trl_log_vs_model": 0.0,
      "not_safe_everywhere": true,
      "positive_evidence": false,
      "posterior_trl_near_equivalent_to_prior_matched_model_dp": true
    },
    "families": [
      "branch_chain",
      "stochastic_stitching",
      "teleporter"
    ],
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
    "num_mdps": 15,
    "num_method_rows": 120,
    "positive_evidence": false,
    "posterior_trl_near_equivalent_to_prior_matched_model_dp": true,
    "seeds": [
      0,
      1,
      2,
      3,
      4
    ]
  },
  "next_questions": [
    "Can a future posterior TRL method beat posterior model DP only when state aliases or partial observability make model DP insufficient?",
    "Should posterior TRL audits require model-DP equivalence checks by default?",
    "Which explicit priors should be predeclared for no-success risk-optimal regimes?"
  ],
  "status": "completed"
}
```


## Latest summary

# Experiment 0011 Summary

## Objective

Run a randomized tabular equivalence and generalization audit for posterior TRL-log versus prior-matched posterior model DP.

## Commands Run

```bash
mkdir -p research/sto_trl/artifacts/0011 research/sto_trl/results
conda run -n autoresearcher_sto_trl python research/sto_trl/artifacts/0011/randomized_equivalence_audit.py
conda run -n autoresearcher_sto_trl python scripts/validate_artifacts.py --repo-root . --json research/sto_trl/results/0011_result.json --schema schemas/result.schema.json --check-result-artifacts
```

## Suite

- Families: `['branch_chain', 'stochastic_stitching', 'teleporter']`
- Seeds per family: `[0, 1, 2, 3, 4]`
- Total MDPs: `15`
- Label horizon cutoff: `2`

## Method Summary

| Method | Action accuracy | Heldout MSE | Policy regret | Risky rate | Q overestimation | Calibration error |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| empirical_model_dp | 0.400000 | 0.037651669545 | 0.068406683449 | 0.400000 | 0.072144533180 | 0.226524283748 |
| mc_supervised | 0.400000 | 0.432704401393 | 0.028055308380 | 0.000000 | 0.000000000000 | 0.569045217387 |
| posterior_lower_q10_model_dp | 0.466667 | 0.035925214745 | 0.022182232310 | 0.066667 | 0.016269178882 | 0.261509935151 |
| posterior_mc_plus_trl_log | 0.600000 | 0.032259348981 | 0.012917304567 | 0.200000 | 0.045769378882 | 0.214221377748 |
| posterior_mean_model_dp | 0.600000 | 0.032259348981 | 0.012917304567 | 0.200000 | 0.045769378882 | 0.214221377748 |
| posterior_trl_log | 0.600000 | 0.032259348981 | 0.012917304567 | 0.200000 | 0.045769378882 | 0.214221377748 |
| trl_log | 0.400000 | 0.037651669545 | 0.068406683449 | 0.400000 | 0.072144533180 | 0.226524283748 |
| trl_raw | 0.400000 | 0.041975170307 | 0.097601010862 | 0.800000 | 0.154109702482 | 0.294064622351 |

## Equivalence Audit

- Positive posterior TRL evidence: `False`
- Near-equivalent to prior-matched posterior model DP: `True`
- Max posterior_trl_log value difference vs model DP: `0`
- Posterior_trl_log action disagreement rate vs model DP: `0`
- Matched risk-optimal action preserved: `True`

## Interpretation

The randomized tiny-suite audit supports the 0010 boundary result: posterior TRL-log variants match the prior-matched posterior mean model-DP baseline within numerical tolerance across branch-chain, stochastic stitching, and teleporter families. Any aggregate improvement over plain TRL-log is explained by the shared posterior transition prior, not by a distinct transitive posterior TRL effect.

## Artifacts

- `research/sto_trl/artifacts/0011/randomized_equivalence_audit.py`
- `research/sto_trl/artifacts/0011/raw_metrics.json`
- `research/sto_trl/artifacts/0011/metrics.csv`
- `research/sto_trl/artifacts/0011/family_summary.csv`
- `research/sto_trl/artifacts/0011/regime_summary.csv`
- `research/sto_trl/artifacts/0011/equivalence_diagnostics.json`
- `research/sto_trl/artifacts/0011/coverage_diagnostics.json`
- `research/sto_trl/artifacts/0011/offline_datasets.json`
- `research/sto_trl/artifacts/0011/transition_tables.json`
- `research/sto_trl/artifacts/0011/value_tables.json`


## Full evidence paths

- `research/sto_trl/results/0011_result.json`
- `research/sto_trl/results/0011_summary.md`

Inspect the full result JSON only when the compact summary and artifact list are insufficient.


## Artifact paths

- `/home/eston/autoresearcher/research/sto_trl/artifacts/0007`
- `/home/eston/autoresearcher/research/sto_trl/artifacts/0008`
- `/home/eston/autoresearcher/research/sto_trl/artifacts/0009`
- `/home/eston/autoresearcher/research/sto_trl/artifacts/0010`
- `/home/eston/autoresearcher/research/sto_trl/artifacts/0011`


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
