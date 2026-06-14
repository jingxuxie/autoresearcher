# Reviewer Context: reward_to_gcrl

## Latest plan

# Experiment 0001

## Objective

Create a reproducible CPU-only diagnostic that verifies the sampled augmented terminal target and the deterministic soft terminal target have the same expectation, quantifies the sampled target variance and g_plus rarity, and confirms the soft g_plus Bellman fixed point equals normalized Q-learning up to the (1 - gamma) scaling in a tiny finite MDP.

## Hypothesis

For each gamma and normalized reward r_bar, the sampled Bernoulli terminal target has mean (1 - gamma) * r_bar and variance p * (1 - p), where p = (1 - gamma) * r_bar, while the soft target has the same mean and zero terminal-sampling variance; in a tiny finite MDP, F_gplus_star / (1 - gamma) should match Q_norm_star within numerical tolerance.

## Success criteria

- For all gamma in {0.90, 0.95, 0.99, 0.995} and r_bar in {0.01, 0.1, 0.5, 1.0}, empirical sampled means are within 3 standard errors of analytic p = (1 - gamma) * r_bar.
- Reported sampled variances match p * (1 - p) within a clear Monte Carlo tolerance, and soft-target terminal variance is exactly zero by construction.
- The report includes g_plus event counts per 10000 samples and shows rarity worsening as gamma approaches 1.
- On a tiny finite MDP, max_abs_error(F_gplus_star / (1 - gamma) - Q_norm_star) is less than 1e-6.
- Artifacts include exact command, config, raw JSON metrics, and a short markdown summary with pass/fail interpretation.

## Failure criteria

- Reward normalization, gamma placement, or terminal target definitions are ambiguous.
- Empirical means/variances do not match analytic values and the discrepancy is not explained by sample size.
- The finite-MDP equivalence check fails above 1e-6.
- The output reports only plots or training loss without raw mean, variance, event-count, and equivalence metrics.
- The experiment introduces neural function approximation, large environments, or GPU dependence before this gate passes.

## Estimated runtime

<= 10 minutes

## Tasks for Codex

- Add a script under research/reward_to_gcrl/artifacts/0001/ that computes analytic and Monte Carlo sampled-vs-soft terminal target statistics for the specified gamma and r_bar sweep.
- Add a tiny finite-MDP value-iteration check comparing Q_norm_star to F_gplus_star / (1 - gamma).
- Save research/reward_to_gcrl/results/0001_result.json with raw metrics, tolerances, pass/fail flags, and exact command.
- Save research/reward_to_gcrl/results/0001_summary.md with a compact table and interpretation.
- Do not implement neural models, CliffWalking, RiverSwim, or auxiliary state goals in this iteration.

## Required outputs

- `research/reward_to_gcrl/results/0001_result.json`
- `research/reward_to_gcrl/results/0001_summary.md`
- `research/reward_to_gcrl/artifacts/0001/`


## Latest plan JSON

```json
{
  "estimated_runtime_minutes": 10,
  "experiment_id": "0001",
  "failure_criteria": [
    "Reward normalization, gamma placement, or terminal target definitions are ambiguous.",
    "Empirical means/variances do not match analytic values and the discrepancy is not explained by sample size.",
    "The finite-MDP equivalence check fails above 1e-6.",
    "The output reports only plots or training loss without raw mean, variance, event-count, and equivalence metrics.",
    "The experiment introduces neural function approximation, large environments, or GPU dependence before this gate passes."
  ],
  "hypothesis": "For each gamma and normalized reward r_bar, the sampled Bernoulli terminal target has mean (1 - gamma) * r_bar and variance p * (1 - p), where p = (1 - gamma) * r_bar, while the soft target has the same mean and zero terminal-sampling variance; in a tiny finite MDP, F_gplus_star / (1 - gamma) should match Q_norm_star within numerical tolerance.",
  "objective": "Create a reproducible CPU-only diagnostic that verifies the sampled augmented terminal target and the deterministic soft terminal target have the same expectation, quantifies the sampled target variance and g_plus rarity, and confirms the soft g_plus Bellman fixed point equals normalized Q-learning up to the (1 - gamma) scaling in a tiny finite MDP.",
  "required_outputs": [
    "research/reward_to_gcrl/results/0001_result.json",
    "research/reward_to_gcrl/results/0001_summary.md",
    "research/reward_to_gcrl/artifacts/0001/"
  ],
  "success_criteria": [
    "For all gamma in {0.90, 0.95, 0.99, 0.995} and r_bar in {0.01, 0.1, 0.5, 1.0}, empirical sampled means are within 3 standard errors of analytic p = (1 - gamma) * r_bar.",
    "Reported sampled variances match p * (1 - p) within a clear Monte Carlo tolerance, and soft-target terminal variance is exactly zero by construction.",
    "The report includes g_plus event counts per 10000 samples and shows rarity worsening as gamma approaches 1.",
    "On a tiny finite MDP, max_abs_error(F_gplus_star / (1 - gamma) - Q_norm_star) is less than 1e-6.",
    "Artifacts include exact command, config, raw JSON metrics, and a short markdown summary with pass/fail interpretation."
  ],
  "tasks_for_codex": [
    "Add a script under research/reward_to_gcrl/artifacts/0001/ that computes analytic and Monte Carlo sampled-vs-soft terminal target statistics for the specified gamma and r_bar sweep.",
    "Add a tiny finite-MDP value-iteration check comparing Q_norm_star to F_gplus_star / (1 - gamma).",
    "Save research/reward_to_gcrl/results/0001_result.json with raw metrics, tolerances, pass/fail flags, and exact command.",
    "Save research/reward_to_gcrl/results/0001_summary.md with a compact table and interpretation.",
    "Do not implement neural models, CliffWalking, RiverSwim, or auxiliary state goals in this iteration."
  ]
}
```


## Latest result summary

```json
{
  "_source": "/home/eston/autoresearcher/research/reward_to_gcrl/results/0001_result.json",
  "artifacts": [
    "research/reward_to_gcrl/artifacts/0001/run_terminal_variance_diagnostic.py",
    "research/reward_to_gcrl/artifacts/0001/raw_metrics.json",
    "research/reward_to_gcrl/artifacts/0001/metrics.csv",
    "research/reward_to_gcrl/artifacts/0001/metadata.json",
    "research/reward_to_gcrl/artifacts/0001/finite_mdp_equivalence.json"
  ],
  "baseline_metrics": {
    "baseline_name": "sampled_bernoulli_terminal_target",
    "baseline_target_definition": "Bernoulli((1 - gamma) * r_bar) indicator for g_plus.",
    "max_sampled_g_plus_count_per_10000": 1005.02,
    "max_sampled_target_variance": 0.090401347996,
    "min_sampled_g_plus_count_per_10000": 0.48000000000000004,
    "per_setting_sampled_metrics": {
      "_type": "list",
      "first_items": [
        {
          "_type": "object",
          "key_count": 8,
          "keys": [
            "analytic_expected_mean",
            "analytic_expected_variance",
            "gamma",
            "r_bar",
            "sampled_g_plus_count",
            "sampled_g_plus_count_per_10000",
            "sampled_target_mean",
            "sampled_target_variance"
          ]
        },
        {
          "_type": "object",
          "key_count": 8,
          "keys": [
            "analytic_expected_mean",
            "analytic_expected_variance",
            "gamma",
            "r_bar",
            "sampled_g_plus_count",
            "sampled_g_plus_count_per_10000",
            "sampled_target_mean",
            "sampled_target_variance"
          ]
        },
        {
          "_type": "object",
          "key_count": 8,
          "keys": [
            "analytic_expected_mean",
            "analytic_expected_variance",
            "gamma",
            "r_bar",
            "sampled_g_plus_count",
            "sampled_g_plus_count_per_10000",
            "sampled_target_mean",
            "sampled_target_variance"
          ]
        }
      ],
      "length": 16
    }
  },
  "claim_tested": "In a one-state normalized-reward augmented transition model, sampled Bernoulli g_plus terminal targets and deterministic soft expected-mass targets have the same mean, while sampled targets retain Bernoulli variance and increasingly rare g_plus events as gamma approaches 1; in a tiny finite MDP, F_gplus_star / (1 - gamma) matches normalized Q_star.",
  "experiment_id": "0001",
  "interpretation": "The deterministic soft target exactly equals the analytic expected terminal mass and has zero variance. The sampled Bernoulli estimator matched that mean within the predeclared Monte Carlo tolerance at all 16 sweep points, but retained nonzero target variance up to 0.0904013. The rarest observed g_plus rate was 0.48 per 10000 transitions, exposing the sparse-event issue for high gamma and low r_bar. The finite-MDP scaled soft successor check passed with max_abs_error 3.94752e-08.",
  "known_failures": [],
  "metrics": {
    "all_sampled_means_within_tolerance": true,
    "all_soft_variances_negligible": true,
    "finite_mdp_equivalence": {
      "_type": "list",
      "first_items": [
        {
          "_type": "object",
          "key_count": 10,
          "keys": [
            "f_final_delta",
            "f_gplus_star",
            "f_value_iteration_steps",
            "gamma",
            "max_abs_error_scaled_f_vs_q",
            "passes_tolerance",
            "q_final_delta",
            "q_star",
            "q_value_iteration_steps",
            "scaled_f_gplus_star"
          ]
        },
        {
          "_type": "object",
          "key_count": 10,
          "keys": [
            "f_final_delta",
            "f_gplus_star",
            "f_value_iteration_steps",
            "gamma",
            "max_abs_error_scaled_f_vs_q",
            "passes_tolerance",
            "q_final_delta",
            "q_star",
            "q_value_iteration_steps",
            "scaled_f_gplus_star"
          ]
        },
        {
          "_type": "object",
          "key_count": 10,
          "keys": [
            "f_final_delta",
            "f_gplus_star",
            "f_value_iteration_steps",
            "gamma",
            "max_abs_error_scaled_f_vs_q",
            "passes_tolerance",
            "q_final_delta",
            "q_star",
            "q_value_iteration_steps",
            "scaled_f_gplus_star"
          ]
        }
      ],
      "length": 4
    },
    "finite_mdp_equivalence_pass": true,
    "finite_mdp_equivalence_tolerance": 1e-06,
    "finite_mdp_max_abs_error_scaled_f_vs_q": 3.9475168023273e-08,
    "gammas": [
      0.9,
      0.95,
      0.99,
      0.995
    ],
    "max_abs_sampled_minus_soft_mean": 0.0005020000000000163,
    "max_analytic_target_coefficient_of_variation": 141.41782065920822,
    "max_monte_carlo_abs_tolerance": 0.0018,
    "max_sampled_g_plus_count_per_10000": 1005.02,
    "max_sampled_target_variance": 0.090401347996,
    "max_soft_target_variance": 0.0,
    "min_sampled_g_plus_count_per_10000": 0.48000000000000004,
    "model_definition": {
      "bootstrap_term": "Set to zero to isolate the immediate terminal-mass estimator; this is the variance source being tested in experiment 0001.",
      "deterministic_soft_target": {
        "_type": "object",
        "key_count": 2,
        "keys": [
          "sampling_variance",
          "soft_g_plus_target"
        ]
      },
      "one_state_setup": "Every row represents repeated draws from one normalized-reward state-action transition with fixed r_bar in [0, 1].",
      "reward_normalization": "r_bar is pre-normalized reward in [0, 1].",
      "sampled_augmented_terminal_model": {
        "_type": "object",
        "key_count": 4,
        "keys": [
          "P(continue_to_original_next_state | s,a)",
          "P(g_minus | s,a)",
          "P(g_plus | s,a)",
          "sampled_g_plus_target"
        ]
      }
    },
    "monte_carlo_tolerance_rule": "abs(sampled_target_mean - soft_target_mean) <= 6.0 * sqrt(p_g_plus * (1 - p_g_plus) / samples)",
    "num_sweep_points": 16,
    "per_setting_metrics": {
      "_type": "list",
      "first_items": [
        {
          "_type": "object",
          "key_count": 24,
          "keys": [
            "analytic_expected_g_plus_count",
            "analytic_expected_g_plus_count_per_10000",
            "analytic_expected_mean",
            "analytic_expected_variance",
            "analytic_sample_mean_stderr",
            "analytic_target_coefficient_of_variation",
            "gamma",
            "monte_carlo_abs_tolerance",
            "p_continue",
            "p_g_minus",
            "p_g_plus",
            "r_bar",
            "sampled_g_plus_count",
            "sampled_g_plus_count_per_10000",
            "sampled_mean_abs_error_vs_soft",
            "sampled_mean_within_tolerance",
            "sampled_minus_soft_mean",
            "sampled_minus_soft_variance",
            "sampled_target_mean",
            "sampled_target_variance"
          ]
        },
        {
          "_type": "object",
          "key_count": 24,
          "keys": [
            "analytic_expected_g_plus_count",
            "analytic_expected_g_plus_count_per_10000",
            "analytic_expected_mean",
            "analytic_expected_variance",
            "analytic_sample_mean_stderr",
            "analytic_target_coefficient_of_variation",
            "gamma",
            "monte_carlo_abs_tolerance",
            "p_continue",
            "p_g_minus",
            "p_g_plus",
            "r_bar",
            "sampled_g_plus_count",
            "sampled_g_plus_count_per_10000",
            "sampled_mean_abs_error_vs_soft",
            "sampled_mean_within_tolerance",
            "sampled_minus_soft_mean",
            "sampled_minus_soft_variance",
            "sampled_target_mean",
            "sampled_target_variance"
          ]
        },
        {
          "_type": "object",
          "key_count": 24,
          "keys": [
            "analytic_expected_g_plus_count",
            "analytic_expected_g_plus_count_per_10000",
            "analytic_expected_mean",
            "analytic_expected_variance",
            "analytic_sample_mean_stderr",
            "analytic_target_coefficient_of_variation",
            "gamma",
            "monte_carlo_abs_tolerance",
            "p_continue",
            "p_g_minus",
            "p_g_plus",
            "r_bar",
            "sampled_g_plus_count",
            "sampled_g_plus_count_per_10000",
            "sampled_mean_abs_error_vs_soft",
            "sampled_mean_within_tolerance",
            "sampled_minus_soft_mean",
            "sampled_minus_soft_variance",
            "sampled_target_mean",
            "sampled_target_variance"
          ]
        }
      ],
      "length": 16
    },
    "r_bars": [
      0.01,
      0.1,
      0.5,
      1.0
    ],
    "samples_per_setting": 1000000,
    "seed": 20260614,
    "soft_variance_tolerance": 1e-15
  },
  "next_questions": [
    "Does the same expected-mass target match normalized Q-learning in a tabular CliffWalking sanity check?",
    "How much TD target variance remains once the bootstrap term is included in a tiny tabular learner?",
    "Does the finite-MDP equivalence stay stable in off-policy fitted tabular updates with partial coverage?"
  ],
  "status": "completed"
}
```


## Latest summary

# Experiment 0001 Summary

## Setup

This diagnostic isolates the immediate terminal-mass estimator in the one-state augmented model. Rewards are pre-normalized as `r_bar in [0, 1]`; the sampled model uses `P(g_plus | s,a) = (1 - gamma) * r_bar`, and the deterministic soft target uses the same expected mass directly.

Samples per sweep point: `1000000`. Seed: `20260614`. Bootstrap is set to zero so the only variance source is the sampled terminal event.

## Commands Run

```bash
mkdir -p research/reward_to_gcrl/artifacts/0001 research/reward_to_gcrl/results
conda run -n autoresearcher_reward_to_gcrl python research/reward_to_gcrl/artifacts/0001/run_terminal_variance_diagnostic.py --samples 1000000 --seed 20260614
conda run -n autoresearcher_reward_to_gcrl python -m jsonschema -i research/reward_to_gcrl/results/0001_result.json schemas/result.schema.json
conda run -n autoresearcher_reward_to_gcrl python scripts/validate_artifacts.py --repo-root . --json research/reward_to_gcrl/results/0001_result.json --schema schemas/result.schema.json --check-result-artifacts
```

## Raw Metrics

| gamma | r_bar | sampled mean | soft mean | sampled var | soft var | g_plus / 10000 | expected / 10000 |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 0.900 | 0.01 | 0.00096100 | 0.00100000 | 0.00096008 | 0.0 | 9.6100 | 10.0000 |
| 0.900 | 0.10 | 0.01019400 | 0.01000000 | 0.01009008 | 0.0 | 101.9400 | 100.0000 |
| 0.900 | 0.50 | 0.04987600 | 0.05000000 | 0.04738838 | 0.0 | 498.7600 | 500.0000 |
| 0.900 | 1.00 | 0.10050200 | 0.10000000 | 0.09040135 | 0.0 | 1005.0200 | 1000.0000 |
| 0.950 | 0.01 | 0.00047900 | 0.00050000 | 0.00047877 | 0.0 | 4.7900 | 5.0000 |
| 0.950 | 0.10 | 0.00508600 | 0.00500000 | 0.00506013 | 0.0 | 50.8600 | 50.0000 |
| 0.950 | 0.50 | 0.02521700 | 0.02500000 | 0.02458110 | 0.0 | 252.1700 | 250.0000 |
| 0.950 | 1.00 | 0.05002500 | 0.05000000 | 0.04752250 | 0.0 | 500.2500 | 500.0000 |
| 0.990 | 0.01 | 0.00010900 | 0.00010000 | 0.00010899 | 0.0 | 1.0900 | 1.0000 |
| 0.990 | 0.10 | 0.00099700 | 0.00100000 | 0.00099601 | 0.0 | 9.9700 | 10.0000 |
| 0.990 | 0.50 | 0.00502600 | 0.00500000 | 0.00500074 | 0.0 | 50.2600 | 50.0000 |
| 0.990 | 1.00 | 0.00978000 | 0.01000000 | 0.00968435 | 0.0 | 97.8000 | 100.0000 |
| 0.995 | 0.01 | 0.00004800 | 0.00005000 | 0.00004800 | 0.0 | 0.4800 | 0.5000 |
| 0.995 | 0.10 | 0.00047900 | 0.00050000 | 0.00047877 | 0.0 | 4.7900 | 5.0000 |
| 0.995 | 0.50 | 0.00254900 | 0.00250000 | 0.00254250 | 0.0 | 25.4900 | 25.0000 |
| 0.995 | 1.00 | 0.00501000 | 0.00500000 | 0.00498490 | 0.0 | 50.1000 | 50.0000 |

The rarest analytic event rate occurs at `gamma=0.995` and `r_bar=0.01`: `0.5000` expected `g_plus` events per 10000 transitions.

## Finite-MDP Equivalence

The same script solves a tiny 3-state, 2-action finite MDP twice: once with normalized rewards as `Q_norm_star`, and once with soft terminal mass rewards `(1 - gamma) * r_bar` as `F_gplus_star`. The check reports `max_abs(F_gplus_star / (1 - gamma) - Q_norm_star)`.

| gamma | max abs error | tolerance | q iterations | f iterations |
|---:|---:|---:|---:|---:|
| 0.900 | 7.615e-11 | 1.0e-06 | 264 | 242 |
| 0.950 | 3.476e-10 | 1.0e-06 | 540 | 482 |
| 0.990 | 9.708e-09 | 1.0e-06 | 2751 | 2293 |
| 0.995 | 3.948e-08 | 1.0e-06 | 5514 | 4457 |

## Outcome

Status: `completed`.

All sampled means were within the predeclared Monte Carlo tolerance rule `6 * sqrt(p * (1 - p) / samples)`, where `p=(1-gamma)*r_bar`. The soft target variance was exactly zero in every setting. The finite-MDP scaled soft successor check passed at tolerance `1.0e-06`. The sampled estimator therefore matches the soft target mean in this sanity check, but keeps Bernoulli target variance and exposes rare `g_plus` events as `gamma` approaches 1.

## Artifacts

- `research/reward_to_gcrl/artifacts/0001/run_terminal_variance_diagnostic.py`
- `research/reward_to_gcrl/artifacts/0001/raw_metrics.json`
- `research/reward_to_gcrl/artifacts/0001/metrics.csv`
- `research/reward_to_gcrl/artifacts/0001/metadata.json`
- `research/reward_to_gcrl/artifacts/0001/finite_mdp_equivalence.json`

## Negative Findings

No success criterion failed in this isolated diagnostic. This does not yet test bootstrapped fitted updates, partial-coverage data, or larger tabular environments; those remain separate follow-up checks.


## Full evidence paths

- `research/reward_to_gcrl/results/0001_result.json`
- `research/reward_to_gcrl/results/0001_summary.md`

Inspect the full result JSON only when the compact summary and artifact list are insufficient.


## Artifact paths

- `/home/eston/autoresearcher/research/reward_to_gcrl/artifacts/0001`


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
