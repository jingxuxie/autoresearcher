# Reviewer Context: sto_trl

## Latest plan

# Experiment 0007

## Objective

Test whether a generic tabular posterior or bootstrap branch-uncertainty penalty can replace the hand-shaped one-sided shortcut rule from 0006 while reducing biased lucky-only risky overestimation and preserving deterministic and matched risk-optimal behavior.

## Hypothesis

A branch-uncertainty penalty computed only from offline outcome counts, such as a Dirichlet/Beta posterior lower-confidence estimate or small bootstrap variance penalty, will reduce safe-optimal lucky-only overestimation versus trl_log without relying on direct-goal shortcut eligibility, while preserving chain recovery and selecting risky in the matched risk-optimal scenario. If it fails risk_optimal_no_success, that should be classified as evidence that missing-success regimes need explicit priors rather than stronger TRL relaxation.

## Success criteria

- Creates a self-contained artifact under research/sto_trl/artifacts/0007/ without editing prior results, schemas, AGENTS.md, scripts/autoresearcher.py, or environment files.
- Uses the same exact-DP tabular scenarios as 0006: chain_len9_holdout, safe_optimal_matched, risk_optimal_matched, safe_optimal_lucky_only_stress, and risk_optimal_no_success_stress.
- Implements at least one generic uncertainty method that uses only offline transition/outcome counts and does not special-case direct-goal shortcut actions.
- Runs a tiny predeclared grid, such as two priors or bootstrap settings and two penalty strengths, plus the zero-penalty baseline, all on fixed trajectories and update count.
- Compares mc_supervised, trl_raw, trl_log, mc_plus_trl_log, the best 0006 one-sided conservative rows, and the new generic uncertainty variants on the same datasets.
- Reports exact DP metrics by scenario and method, including held-out long-horizon value MSE, Q/value overestimation and underestimation, calibration error, policy regret, risky action selection rate, and coverage/outcome diagnostics.
- Counts positive evidence only if a generic uncertainty variant reduces safe_optimal_lucky_only Q overestimation or policy regret versus trl_log, preserves deterministic chain held-out MSE near zero, and selects risky with zero regret in risk_optimal_matched.
- Explicitly reports whether risk_optimal_no_success_stress remains unsolved; do not treat fixing safe_optimal_lucky_only by blanket risk avoidance as success.
- Produces valid research/sto_trl/results/0007_result.json and research/sto_trl/results/0007_summary.md with exact commands run.

## Failure criteria

- The uncertainty penalty uses exact DP values, true transition probabilities, or oracle knowledge of unobserved outcomes.
- The new method is only the 0006 hand-shaped direct-goal shortcut rule with renamed parameters.
- The result omits the full predeclared grid or reports only the best setting.
- The method reduces safe-optimal lucky-only regret only by selecting safe in risk_optimal_matched or increasing matched policy regret.
- Exact DP ground truth, raw metrics, commands run, or coverage diagnostics are missing.
- The run expands to neural networks, OGBench, PointMaze, AntMaze, large downloads, broad sweeps, or exceeds 30 minutes.

## Estimated runtime

<= 25 minutes

## Tasks for Codex

- Create research/sto_trl/artifacts/0007/ and adapt the 0006 harness into a generic uncertainty audit script.
- Implement a count-based posterior or bootstrap branch-uncertainty estimator that operates on observed next-outcome counts for state-action pairs and saves its diagnostics.
- Run the fixed 0006 tabular scenarios with the predeclared small grid and the same update_steps and label_horizon_cutoff.
- Compute direct comparisons versus trl_log and versus the 0006 one-sided conservative variants, including policy/regret and Q overestimation deltas for the two biased stress cases.
- Save raw_metrics.json, metrics.csv, uncertainty_grid.json, uncertainty_diagnostics.json, offline_datasets.json, transition_tables.json, and value_tables.json under research/sto_trl/artifacts/0007/.
- Write research/sto_trl/results/0007_result.json and research/sto_trl/results/0007_summary.md, then validate the result JSON with scripts/validate_artifacts.py and artifact checks.

## Required outputs

- `research/sto_trl/results/0007_result.json`
- `research/sto_trl/results/0007_summary.md`
- `research/sto_trl/artifacts/0007/`


## Latest plan JSON

```json
{
  "estimated_runtime_minutes": 25,
  "experiment_id": "0007",
  "failure_criteria": [
    "The uncertainty penalty uses exact DP values, true transition probabilities, or oracle knowledge of unobserved outcomes.",
    "The new method is only the 0006 hand-shaped direct-goal shortcut rule with renamed parameters.",
    "The result omits the full predeclared grid or reports only the best setting.",
    "The method reduces safe-optimal lucky-only regret only by selecting safe in risk_optimal_matched or increasing matched policy regret.",
    "Exact DP ground truth, raw metrics, commands run, or coverage diagnostics are missing.",
    "The run expands to neural networks, OGBench, PointMaze, AntMaze, large downloads, broad sweeps, or exceeds 30 minutes."
  ],
  "hypothesis": "A branch-uncertainty penalty computed only from offline outcome counts, such as a Dirichlet/Beta posterior lower-confidence estimate or small bootstrap variance penalty, will reduce safe-optimal lucky-only overestimation versus trl_log without relying on direct-goal shortcut eligibility, while preserving chain recovery and selecting risky in the matched risk-optimal scenario. If it fails risk_optimal_no_success, that should be classified as evidence that missing-success regimes need explicit priors rather than stronger TRL relaxation.",
  "objective": "Test whether a generic tabular posterior or bootstrap branch-uncertainty penalty can replace the hand-shaped one-sided shortcut rule from 0006 while reducing biased lucky-only risky overestimation and preserving deterministic and matched risk-optimal behavior.",
  "required_outputs": [
    "research/sto_trl/results/0007_result.json",
    "research/sto_trl/results/0007_summary.md",
    "research/sto_trl/artifacts/0007/"
  ],
  "success_criteria": [
    "Creates a self-contained artifact under research/sto_trl/artifacts/0007/ without editing prior results, schemas, AGENTS.md, scripts/autoresearcher.py, or environment files.",
    "Uses the same exact-DP tabular scenarios as 0006: chain_len9_holdout, safe_optimal_matched, risk_optimal_matched, safe_optimal_lucky_only_stress, and risk_optimal_no_success_stress.",
    "Implements at least one generic uncertainty method that uses only offline transition/outcome counts and does not special-case direct-goal shortcut actions.",
    "Runs a tiny predeclared grid, such as two priors or bootstrap settings and two penalty strengths, plus the zero-penalty baseline, all on fixed trajectories and update count.",
    "Compares mc_supervised, trl_raw, trl_log, mc_plus_trl_log, the best 0006 one-sided conservative rows, and the new generic uncertainty variants on the same datasets.",
    "Reports exact DP metrics by scenario and method, including held-out long-horizon value MSE, Q/value overestimation and underestimation, calibration error, policy regret, risky action selection rate, and coverage/outcome diagnostics.",
    "Counts positive evidence only if a generic uncertainty variant reduces safe_optimal_lucky_only Q overestimation or policy regret versus trl_log, preserves deterministic chain held-out MSE near zero, and selects risky with zero regret in risk_optimal_matched.",
    "Explicitly reports whether risk_optimal_no_success_stress remains unsolved; do not treat fixing safe_optimal_lucky_only by blanket risk avoidance as success.",
    "Produces valid research/sto_trl/results/0007_result.json and research/sto_trl/results/0007_summary.md with exact commands run."
  ],
  "tasks_for_codex": [
    "Create research/sto_trl/artifacts/0007/ and adapt the 0006 harness into a generic uncertainty audit script.",
    "Implement a count-based posterior or bootstrap branch-uncertainty estimator that operates on observed next-outcome counts for state-action pairs and saves its diagnostics.",
    "Run the fixed 0006 tabular scenarios with the predeclared small grid and the same update_steps and label_horizon_cutoff.",
    "Compute direct comparisons versus trl_log and versus the 0006 one-sided conservative variants, including policy/regret and Q overestimation deltas for the two biased stress cases.",
    "Save raw_metrics.json, metrics.csv, uncertainty_grid.json, uncertainty_diagnostics.json, offline_datasets.json, transition_tables.json, and value_tables.json under research/sto_trl/artifacts/0007/.",
    "Write research/sto_trl/results/0007_result.json and research/sto_trl/results/0007_summary.md, then validate the result JSON with scripts/validate_artifacts.py and artifact checks."
  ]
}
```


## Latest result summary

```json
{
  "_source": "/home/eston/autoresearcher/research/sto_trl/results/0007_result.json",
  "artifacts": [
    "research/sto_trl/artifacts/0007/run_generic_uncertainty_audit.py",
    "research/sto_trl/artifacts/0007/raw_metrics.json",
    "research/sto_trl/artifacts/0007/metrics.csv",
    "research/sto_trl/artifacts/0007/uncertainty_grid.json",
    "research/sto_trl/artifacts/0007/uncertainty_diagnostics.json",
    "research/sto_trl/artifacts/0007/offline_datasets.json",
    "research/sto_trl/artifacts/0007/transition_tables.json",
    "research/sto_trl/artifacts/0007/value_tables.json"
  ],
  "baseline_metrics": {
    "chain_len9_holdout": {
      "calibration_error": 4.336808689942018e-18,
      "chose_exact_optimal_action": true,
      "eval_goal": "c8",
      "eval_greedy_action": "right",
      "eval_start": "c0",
      "eval_start_exact_q": {
        "_type": "object",
        "key_count": 1,
        "keys": [
          "right"
        ]
      },
      "eval_start_learned_q": {
        "_type": "object",
        "key_count": 1,
        "keys": [
          "right"
        ]
      },
      "exact_optimal_action": "right",
      "heldout_long_horizon_value_mse": 2.9347503914472164e-34,
      "horizon_metrics": {
        "_type": "object",
        "key_count": 3,
        "keys": [
          "h1_train_visible",
          "h2_train_visible",
          "heldout_gt2"
        ]
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
    "method": "trl_log",
    "risk_optimal_matched": {
      "calibration_error": 1.734723475976807e-18,
      "chose_exact_optimal_action": true,
      "eval_goal": "goal",
      "eval_greedy_action": "risky",
      "eval_start": "start",
      "eval_start_exact_q": {
        "_type": "object",
        "key_count": 2,
        "keys": [
          "risky",
          "safe"
        ]
      },
      "eval_start_learned_q": {
        "_type": "object",
        "key_count": 2,
        "keys": [
          "risky",
          "safe"
        ]
      },
      "exact_optimal_action": "risky",
      "heldout_long_horizon_value_mse": 0.0,
      "horizon_metrics": {
        "_type": "object",
        "key_count": 4,
        "keys": [
          "h1_train_visible",
          "h2_train_visible",
          "heldout_gt2",
          "unreachable"
        ]
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
    "safe_optimal_lucky_only_stress": {
      "calibration_error": 0.084375,
      "chose_exact_optimal_action": false,
      "eval_goal": "goal",
      "eval_greedy_action": "risky",
      "eval_start": "start",
      "eval_start_exact_q": {
        "_type": "object",
        "key_count": 2,
        "keys": [
          "risky",
          "safe"
        ]
      },
      "eval_start_learned_q": {
        "_type": "object",
        "key_count": 2,
        "keys": [
          "risky",
          "safe"
        ]
      },
      "exact_optimal_action": "safe",
      "heldout_long_horizon_value_mse": 0.029240999999999975,
      "horizon_metrics": {
        "_type": "object",
        "key_count": 4,
        "keys": [
          "h1_train_visible",
          "h2_train_visible",
          "heldout_gt2",
          "unreachable"
        ]
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
  "claim_tested": "A generic count-based posterior branch-uncertainty penalty can replace the hand-shaped 0006 shortcut rule while reducing lucky-only overestimation and preserving matched risk-optimal behavior.",
  "experiment_id": "0007",
  "interpretation": "generic_dirichlet_unknown_prior_0_50_alpha_0_50 reduced safe-optimal lucky-only overestimation versus trl_log while preserving the chain and selecting risky with zero regret in the matched risk-optimal scenario. The risk-optimal no-success stress status is reported separately.",
  "known_failures": [],
  "metrics": {
    "aggregate": {
      "best_positive_method": "generic_dirichlet_unknown_prior_0_50_alpha_0_50",
      "generic_summaries": {
        "_type": "object",
        "key_count": 6,
        "keys": [
          "generic_dirichlet_unknown_prior_0_50_alpha_0_00",
          "generic_dirichlet_unknown_prior_0_50_alpha_0_50",
          "generic_dirichlet_unknown_prior_0_50_alpha_1_00",
          "generic_dirichlet_unknown_prior_1_00_alpha_0_00",
          "generic_dirichlet_unknown_prior_1_00_alpha_0_50",
          "generic_dirichlet_unknown_prior_1_00_alpha_1_00"
        ]
      },
      "one_sided_0006_safe_lucky_policy_regret": 0.0,
      "one_sided_0006_safe_lucky_q_overestimation": 0.495,
      "positive_generic_uncertainty_evidence": true,
      "risk_optimal_no_success_unsolved_by_best_positive": true,
      "trl_log_safe_lucky_policy_regret": 0.5040000000000001,
      "trl_log_safe_lucky_q_overestimation": 0.675
    },
    "best_0006_alpha": 0.4,
    "experiment_id": "0007",
    "gamma": 0.9,
    "generic_alpha_grid": [
      0.0,
      0.5,
      1.0
    ],
    "generic_prior_grid": [
      0.5,
      1.0
    ],
    "label_horizon_cutoff": 2,
    "scenarios": {
      "chain_len9_holdout": {
        "_type": "object",
        "key_count": 6,
        "keys": [
          "coverage_diagnostics",
          "label_or_pair_coverage",
          "mdp",
          "methods",
          "scenario_role",
          "uncertainty_meta"
        ]
      },
      "risk_optimal_matched": {
        "_type": "object",
        "key_count": 6,
        "keys": [
          "coverage_diagnostics",
          "label_or_pair_coverage",
          "mdp",
          "methods",
          "scenario_role",
          "uncertainty_meta"
        ]
      },
      "risk_optimal_no_success_stress": {
        "_type": "object",
        "key_count": 6,
        "keys": [
          "coverage_diagnostics",
          "label_or_pair_coverage",
          "mdp",
          "methods",
          "scenario_role",
          "uncertainty_meta"
        ]
      },
      "safe_optimal_lucky_only_stress": {
        "_type": "object",
        "key_count": 6,
        "keys": [
          "coverage_diagnostics",
          "label_or_pair_coverage",
          "mdp",
          "methods",
          "scenario_role",
          "uncertainty_meta"
        ]
      },
      "safe_optimal_matched": {
        "_type": "object",
        "key_count": 6,
        "keys": [
          "coverage_diagnostics",
          "label_or_pair_coverage",
          "mdp",
          "methods",
          "scenario_role",
          "uncertainty_meta"
        ]
      }
    },
    "success_checks": {
      "chain_raw_exact": true,
      "chain_trl_log_exact": true,
      "experiment_completed": true,
      "generic_grid_completed": true,
      "positive_generic_uncertainty_evidence": true
    },
    "successor_baseline_lambda": 0.25,
    "update_steps": 32
  },
  "next_questions": [
    "Can a generic prior preserve multi-step safe routes without also discounting them below lucky shortcuts?",
    "Should no-success risk-optimal regimes be handled by explicit optimistic priors rather than stronger conservative penalties?",
    "Would bootstrap branch uncertainty distinguish deterministic safe routes from all-success risky shortcuts better than the unknown-outcome prior?"
  ],
  "status": "completed"
}
```


## Latest summary

# Experiment 0007 Summary

## Objective

Audit a generic count-based posterior uncertainty penalty against the 0006 one-sided conservative rule.

## Commands Run

```bash
mkdir -p research/sto_trl/artifacts/0007 research/sto_trl/results && cp research/sto_trl/artifacts/0006/run_uncertainty_conservative_log_trl.py research/sto_trl/artifacts/0007/run_generic_uncertainty_audit.py
conda run -n autoresearcher_sto_trl python research/sto_trl/artifacts/0007/run_generic_uncertainty_audit.py
conda run -n autoresearcher_sto_trl python scripts/validate_artifacts.py --repo-root . --json research/sto_trl/results/0007_result.json --schema schemas/result.schema.json --check-result-artifacts
```

## Setup

- Discount: `0.9`
- Label horizon cutoff: `2`
- Fixed backup iterations: `32`
- Prior grid: `[0.5, 1.0]`
- Alpha grid: `[0.0, 0.5, 1.0]`
- Generic penalty: interpolate empirical log backup with a Dirichlet unknown-zero posterior lower estimate for state-action counts at least 4.

## Metrics

| Scenario | Method | Prior | Alpha | Held-out MSE | Q calibration | Policy regret | Action | Risky selected |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- | ---: |
| chain_len9_holdout | mc_supervised | None | None | 0.391705823230 | 0.465607869047 | 0.000000000000 | right | 0.0 |
| chain_len9_holdout | trl_raw | None | None | 0.000000000000 | 0.000000000000 | 0.000000000000 | right | 0.0 |
| chain_len9_holdout | trl_log | None | None | 0.000000000000 | 0.000000000000 | 0.000000000000 | right | 0.0 |
| chain_len9_holdout | mc_plus_trl_log | None | None | 0.000000000000 | 0.131258278195 | 0.000000000000 | right | 0.0 |
| chain_len9_holdout | successor_distance_best_0005 | None | None | 0.000000000000 | 0.000000000000 | 0.000000000000 | right | 0.0 |
| chain_len9_holdout | one_sided_conservative_log_trl_alpha_0_40 | None | 0.4 | 0.000000000000 | 0.000000000000 | 0.000000000000 | right | 0.0 |
| chain_len9_holdout | generic_dirichlet_unknown_prior_0_50_alpha_0_00 | 0.5 | 0.0 | 0.000000000000 | 0.000000000000 | 0.000000000000 | right | 0.0 |
| chain_len9_holdout | generic_dirichlet_unknown_prior_0_50_alpha_0_50 | 0.5 | 0.5 | 0.000000000000 | 0.000000000000 | 0.000000000000 | right | 0.0 |
| chain_len9_holdout | generic_dirichlet_unknown_prior_0_50_alpha_1_00 | 0.5 | 1.0 | 0.000000000000 | 0.000000000000 | 0.000000000000 | right | 0.0 |
| chain_len9_holdout | generic_dirichlet_unknown_prior_1_00_alpha_0_00 | 1.0 | 0.0 | 0.000000000000 | 0.000000000000 | 0.000000000000 | right | 0.0 |
| chain_len9_holdout | generic_dirichlet_unknown_prior_1_00_alpha_0_50 | 1.0 | 0.5 | 0.000000000000 | 0.000000000000 | 0.000000000000 | right | 0.0 |
| chain_len9_holdout | generic_dirichlet_unknown_prior_1_00_alpha_1_00 | 1.0 | 1.0 | 0.000000000000 | 0.000000000000 | 0.000000000000 | right | 0.0 |
| safe_optimal_matched | mc_supervised | None | None | 0.254016000000 | 0.045562500000 | 0.504000000000 | risky | 1.0 |
| safe_optimal_matched | trl_raw | None | None | 0.029241000000 | 0.056250000000 | 0.504000000000 | risky | 1.0 |
| safe_optimal_matched | trl_log | None | None | 0.000000000000 | 0.000000000000 | 0.000000000000 | safe | 0.0 |
| safe_optimal_matched | mc_plus_trl_log | None | None | 0.000000000000 | 0.000000000000 | 0.000000000000 | safe | 0.0 |
| safe_optimal_matched | successor_distance_best_0005 | None | None | 0.000000000000 | 0.000000000000 | 0.000000000000 | safe | 0.0 |
| safe_optimal_matched | one_sided_conservative_log_trl_alpha_0_40 | None | 0.4 | 0.000000000000 | 0.011250000000 | 0.000000000000 | safe | 0.0 |
| safe_optimal_matched | generic_dirichlet_unknown_prior_0_50_alpha_0_00 | 0.5 | 0.0 | 0.000000000000 | 0.000000000000 | 0.000000000000 | safe | 0.0 |
| safe_optimal_matched | generic_dirichlet_unknown_prior_0_50_alpha_0_50 | 0.5 | 0.5 | 0.013196265625 | 0.029146599265 | 0.000000000000 | safe | 0.0 |
| safe_optimal_matched | generic_dirichlet_unknown_prior_0_50_alpha_1_00 | 0.5 | 1.0 | 0.047089000000 | 0.056871323529 | 0.000000000000 | safe | 0.0 |
| safe_optimal_matched | generic_dirichlet_unknown_prior_1_00_alpha_0_00 | 1.0 | 0.0 | 0.000000000000 | 0.000000000000 | 0.000000000000 | safe | 0.0 |
| safe_optimal_matched | generic_dirichlet_unknown_prior_1_00_alpha_0_50 | 1.0 | 0.5 | 0.039029558481 | 0.051584937500 | 0.000000000000 | safe | 0.0 |
| safe_optimal_matched | generic_dirichlet_unknown_prior_1_00_alpha_1_00 | 1.0 | 1.0 | 0.126559485504 | 0.098684500000 | 0.000000000000 | safe | 0.0 |
| risk_optimal_matched | mc_supervised | None | None | 0.000000000000 | 0.045562500000 | 0.000000000000 | risky | 1.0 |
| risk_optimal_matched | trl_raw | None | None | 0.000000000000 | 0.056250000000 | 0.000000000000 | risky | 1.0 |
| risk_optimal_matched | trl_log | None | None | 0.000000000000 | 0.000000000000 | 0.000000000000 | risky | 1.0 |
| risk_optimal_matched | mc_plus_trl_log | None | None | 0.000000000000 | 0.000000000000 | 0.000000000000 | risky | 1.0 |
| risk_optimal_matched | successor_distance_best_0005 | None | None | 0.000000000000 | 0.000000000000 | 0.000000000000 | risky | 1.0 |
| risk_optimal_matched | one_sided_conservative_log_trl_alpha_0_40 | None | 0.4 | 0.000000000000 | 0.011250000000 | 0.000000000000 | risky | 1.0 |
| risk_optimal_matched | generic_dirichlet_unknown_prior_0_50_alpha_0_00 | 0.5 | 0.0 | 0.000000000000 | 0.000000000000 | 0.000000000000 | risky | 1.0 |
| risk_optimal_matched | generic_dirichlet_unknown_prior_0_50_alpha_0_50 | 0.5 | 0.5 | 0.000000000000 | 0.028831473214 | 0.000000000000 | risky | 1.0 |
| risk_optimal_matched | generic_dirichlet_unknown_prior_0_50_alpha_1_00 | 0.5 | 1.0 | 0.000000000000 | 0.056241071429 | 0.000000000000 | risky | 1.0 |
| risk_optimal_matched | generic_dirichlet_unknown_prior_1_00_alpha_0_00 | 1.0 | 0.0 | 0.000000000000 | 0.000000000000 | 0.000000000000 | risky | 1.0 |
| risk_optimal_matched | generic_dirichlet_unknown_prior_1_00_alpha_0_50 | 1.0 | 0.5 | 0.000000000000 | 0.051016755682 | 0.000000000000 | risky | 1.0 |
| risk_optimal_matched | gen

_Trimmed to 6000 chars; inspect the source file for full text._


## Full evidence paths

- `research/sto_trl/results/0007_result.json`
- `research/sto_trl/results/0007_summary.md`

Inspect the full result JSON only when the compact summary and artifact list are insufficient.


## Artifact paths

- `/home/eston/autoresearcher/research/sto_trl/artifacts/0003`
- `/home/eston/autoresearcher/research/sto_trl/artifacts/0004`
- `/home/eston/autoresearcher/research/sto_trl/artifacts/0005`
- `/home/eston/autoresearcher/research/sto_trl/artifacts/0006`
- `/home/eston/autoresearcher/research/sto_trl/artifacts/0007`


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
