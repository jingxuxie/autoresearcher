# Reviewer Context: sto_trl

## Latest plan

# Experiment 0008

## Objective

Run a small tabular identifiability and coverage grid that maps when risky-shortcut action choice is identifiable from finite offline stochastic coverage, before adding new stochastic TRL algorithms.

## Hypothesis

Across risky-shortcut MDPs, some regimes are identifiable from observed risky successes/failures and simple empirical or posterior transition estimates should match exact DP action choice, while lucky-only and no-success regimes will expose impossibility or prior-dependence. This grid should clarify when log-TRL failures are data-identifiability failures versus algorithmic failures.

## Success criteria

- Creates a self-contained artifact under research/sto_trl/artifacts/0008/ without editing prior results, schemas, AGENTS.md, scripts/autoresearcher.py, or environment files.
- Sweeps a small predeclared grid over true risky success probability, safe route length, risky sample count, and observed risky success count, with exact DP ground truth for every cell.
- Includes at least one deterministic chain guard or equivalent sanity row showing raw/log TRL still recover deterministic long-horizon behavior.
- Compares raw TRL, TRL-log, empirical risky-value or empirical-transition DP, Bayesian posterior mean, posterior lower and upper quantile choices, and simple confidence-bound choices on the same grid cells.
- Reports per-cell action choice, policy regret, risky value overestimation, calibration error, and whether the cell is empirically identifiable, ambiguous, lucky-only, no-success, or prior-dependent.
- Saves coverage diagnostics and raw grid metrics, plus compact heatmap-friendly CSV or JSON tables for regret and action choice.
- Counts the experiment as useful if it identifies regimes where no method can be justified without explicit priors, and regimes where transition-level uncertainty baselines are sufficient or insufficient versus TRL-log.
- Produces valid research/sto_trl/results/0008_result.json and research/sto_trl/results/0008_summary.md with exact commands run.

## Failure criteria

- The grid omits exact DP ground truth or policy regret for any evaluated cell.
- The result reports only aggregate averages and does not save per-cell raw metrics.
- The experiment claims an algorithmic win instead of separating identifiable, ambiguous, and prior-dependent regimes.
- The posterior or confidence baselines use true transition probabilities or exact DP labels as training inputs rather than evaluation ground truth.
- The sweep is too broad, exceeds 30 minutes, or expands to neural networks, continuous control, OGBench, downloads, or large training.
- The result omits commands run, artifacts, coverage diagnostics, or validation against schemas/result.schema.json.

## Estimated runtime

<= 25 minutes

## Tasks for Codex

- Create research/sto_trl/artifacts/0008/ and implement a small standalone identifiability_grid.py or equivalent script, reusing helper code from prior tabular artifacts when useful.
- Define the predeclared grid with a compact set such as true risky success probabilities, safe path lengths, risky sample counts, and observed success counts that can run in minutes.
- For each cell, compute exact DP risky and safe values, empirical estimates from observed counts, posterior mean and quantile estimates under explicit priors, confidence-bound choices, raw TRL, and TRL-log where applicable.
- Classify each cell by coverage regime, including matched, lucky-only, no-success, ambiguous, and prior-dependent cases.
- Save raw_grid.json, metrics.csv, regret_heatmap.csv, action_choice_grid.csv, impossibility_cases.json, coverage_diagnostics.json, transition_tables.json, and value_tables.json under research/sto_trl/artifacts/0008/.
- Write research/sto_trl/results/0008_result.json and research/sto_trl/results/0008_summary.md, then validate the result JSON with scripts/validate_artifacts.py and artifact checks.

## Required outputs

- `research/sto_trl/results/0008_result.json`
- `research/sto_trl/results/0008_summary.md`
- `research/sto_trl/artifacts/0008/`


## Latest plan JSON

```json
{
  "estimated_runtime_minutes": 25,
  "experiment_id": "0008",
  "failure_criteria": [
    "The grid omits exact DP ground truth or policy regret for any evaluated cell.",
    "The result reports only aggregate averages and does not save per-cell raw metrics.",
    "The experiment claims an algorithmic win instead of separating identifiable, ambiguous, and prior-dependent regimes.",
    "The posterior or confidence baselines use true transition probabilities or exact DP labels as training inputs rather than evaluation ground truth.",
    "The sweep is too broad, exceeds 30 minutes, or expands to neural networks, continuous control, OGBench, downloads, or large training.",
    "The result omits commands run, artifacts, coverage diagnostics, or validation against schemas/result.schema.json."
  ],
  "hypothesis": "Across risky-shortcut MDPs, some regimes are identifiable from observed risky successes/failures and simple empirical or posterior transition estimates should match exact DP action choice, while lucky-only and no-success regimes will expose impossibility or prior-dependence. This grid should clarify when log-TRL failures are data-identifiability failures versus algorithmic failures.",
  "objective": "Run a small tabular identifiability and coverage grid that maps when risky-shortcut action choice is identifiable from finite offline stochastic coverage, before adding new stochastic TRL algorithms.",
  "required_outputs": [
    "research/sto_trl/results/0008_result.json",
    "research/sto_trl/results/0008_summary.md",
    "research/sto_trl/artifacts/0008/"
  ],
  "success_criteria": [
    "Creates a self-contained artifact under research/sto_trl/artifacts/0008/ without editing prior results, schemas, AGENTS.md, scripts/autoresearcher.py, or environment files.",
    "Sweeps a small predeclared grid over true risky success probability, safe route length, risky sample count, and observed risky success count, with exact DP ground truth for every cell.",
    "Includes at least one deterministic chain guard or equivalent sanity row showing raw/log TRL still recover deterministic long-horizon behavior.",
    "Compares raw TRL, TRL-log, empirical risky-value or empirical-transition DP, Bayesian posterior mean, posterior lower and upper quantile choices, and simple confidence-bound choices on the same grid cells.",
    "Reports per-cell action choice, policy regret, risky value overestimation, calibration error, and whether the cell is empirically identifiable, ambiguous, lucky-only, no-success, or prior-dependent.",
    "Saves coverage diagnostics and raw grid metrics, plus compact heatmap-friendly CSV or JSON tables for regret and action choice.",
    "Counts the experiment as useful if it identifies regimes where no method can be justified without explicit priors, and regimes where transition-level uncertainty baselines are sufficient or insufficient versus TRL-log.",
    "Produces valid research/sto_trl/results/0008_result.json and research/sto_trl/results/0008_summary.md with exact commands run."
  ],
  "tasks_for_codex": [
    "Create research/sto_trl/artifacts/0008/ and implement a small standalone identifiability_grid.py or equivalent script, reusing helper code from prior tabular artifacts when useful.",
    "Define the predeclared grid with a compact set such as true risky success probabilities, safe path lengths, risky sample counts, and observed success counts that can run in minutes.",
    "For each cell, compute exact DP risky and safe values, empirical estimates from observed counts, posterior mean and quantile estimates under explicit priors, confidence-bound choices, raw TRL, and TRL-log where applicable.",
    "Classify each cell by coverage regime, including matched, lucky-only, no-success, ambiguous, and prior-dependent cases.",
    "Save raw_grid.json, metrics.csv, regret_heatmap.csv, action_choice_grid.csv, impossibility_cases.json, coverage_diagnostics.json, transition_tables.json, and value_tables.json under research/sto_trl/artifacts/0008/.",
    "Write research/sto_trl/results/0008_result.json and research/sto_trl/results/0008_summary.md, then validate the result JSON with scripts/validate_artifacts.py and artifact checks."
  ]
}
```


## Latest result summary

```json
{
  "_source": "/home/eston/autoresearcher/research/sto_trl/results/0008_result.json",
  "artifacts": {
    "_type": "list",
    "first_items": [
      "research/sto_trl/artifacts/0008/identifiability_grid.py",
      "research/sto_trl/artifacts/0008/raw_grid.json",
      "research/sto_trl/artifacts/0008/metrics.csv"
    ],
    "length": 9
  },
  "baseline_metrics": {
    "empirical_transition_dp": {
      "action_accuracy": 0.6903225806451613,
      "mean_policy_regret": 0.07556516129032252
    },
    "posterior_mean_beta_1_1": {
      "action_accuracy": 0.7419354838709677,
      "mean_policy_regret": 0.05130387096774184
    },
    "trl_log": {
      "action_accuracy": 0.6903225806451613,
      "mean_policy_regret": 0.07556516129032252
    }
  },
  "claim_tested": "A compact exact-DP tabular grid can distinguish risky-shortcut failures caused by finite stochastic coverage from failures of the TRL-log update itself.",
  "experiment_id": "0008",
  "interpretation": "The grid is useful as an identifiability map: it separates cells where empirical transition estimates match exact action choice from lucky-only, no-success, ambiguous, and prior-dependent cells where explicit priors are required.",
  "known_failures": [],
  "metrics": {
    "chain_guard": {
      "chain_length": 9,
      "passed": true,
      "raw_trl_max_abs_error": 0.0,
      "trl_log_max_abs_error": 0.0
    },
    "classification_counts": {
      "ambiguous": 95,
      "identifiable": 136,
      "lucky_only": 45,
      "matched_identifiable": 44,
      "no_success": 45,
      "prior_dependent": 100
    },
    "method_summary": {
      "empirical_risky_value": {
        "_type": "object",
        "key_count": 2,
        "keys": [
          "action_accuracy",
          "mean_policy_regret"
        ]
      },
      "empirical_transition_dp": {
        "_type": "object",
        "key_count": 2,
        "keys": [
          "action_accuracy",
          "mean_policy_regret"
        ]
      },
      "hoeffding_lcb_delta_0_2": {
        "_type": "object",
        "key_count": 2,
        "keys": [
          "action_accuracy",
          "mean_policy_regret"
        ]
      },
      "hoeffding_ucb_delta_0_2": {
        "_type": "object",
        "key_count": 2,
        "keys": [
          "action_accuracy",
          "mean_policy_regret"
        ]
      },
      "posterior_lower_q10_beta_1_1": {
        "_type": "object",
        "key_count": 2,
        "keys": [
          "action_accuracy",
          "mean_policy_regret"
        ]
      },
      "posterior_mean_beta_1_1": {
        "_type": "object",
        "key_count": 2,
        "keys": [
          "action_accuracy",
          "mean_policy_regret"
        ]
      },
      "posterior_upper_q90_beta_1_1": {
        "_type": "object",
        "key_count": 2,
        "keys": [
          "action_accuracy",
          "mean_policy_regret"
        ]
      },
      "raw_trl": {
        "_type": "object",
        "key_count": 2,
        "keys": [
          "action_accuracy",
          "mean_policy_regret"
        ]
      },
      "trl_log": {
        "_type": "object",
        "key_count": 2,
        "keys": [
          "action_accuracy",
          "mean_policy_regret"
        ]
      }
    },
    "num_cells": 465,
    "num_method_rows": 4185,
    "tag_counts": {
      "ambiguous": 235,
      "identifiable": 230,
      "lucky_only": 45,
      "matched": 129,
      "no_success": 45,
      "prior_dependent": 130
    },
    "useful_identifiability_map": true
  },
  "next_questions": [
    "Which prior should be declared for lucky-only and no-success regimes before algorithm development continues?",
    "Can future algorithms report identifiability status before choosing risky or safe?",
    "Should finite-coverage diagnostics gate TRL-style transitive updates in stochastic offline data?"
  ],
  "status": "completed"
}
```


## Latest summary

# Experiment 0008 Summary

## Objective

Map finite-coverage identifiability for tabular risky shortcuts before adding new stochastic TRL algorithms.

## Commands Run

```bash
mkdir -p research/sto_trl/artifacts/0008 research/sto_trl/results
conda run -n autoresearcher_sto_trl python research/sto_trl/artifacts/0008/identifiability_grid.py
conda run -n autoresearcher_sto_trl python scripts/validate_artifacts.py --repo-root . --json research/sto_trl/results/0008_result.json --schema schemas/result.schema.json --check-result-artifacts
```

## Grid

- True risky success probabilities: `[0.1, 0.25, 0.5, 0.75, 0.9]`
- Safe route lengths: `[2, 3, 4]`
- Risky sample counts: `[4, 8, 16]`
- Observed successes: every integer from `0` to `risky_samples`
- Total cells: `465`

## Key Counts

- Classification counts: `{'no_success': 45, 'matched_identifiable': 44, 'ambiguous': 95, 'lucky_only': 45, 'identifiable': 136, 'prior_dependent': 100}`
- Tag counts: `{'no_success': 45, 'matched': 129, 'identifiable': 230, 'ambiguous': 235, 'lucky_only': 45, 'prior_dependent': 130}`
- Impossibility/prior-dependent cells: `285`
- Deterministic chain guard passed: `True`

## Method Summary

| Method | Action accuracy | Mean policy regret |
| --- | ---: | ---: |
| empirical_risky_value | 0.690323 | 0.075565161290 |
| empirical_transition_dp | 0.690323 | 0.075565161290 |
| hoeffding_lcb_delta_0_2 | 0.797849 | 0.019136129032 |
| hoeffding_ucb_delta_0_2 | 0.516129 | 0.157349032258 |
| posterior_lower_q10_beta_1_1 | 0.787097 | 0.026568387097 |
| posterior_mean_beta_1_1 | 0.741935 | 0.051303870968 |
| posterior_upper_q90_beta_1_1 | 0.640860 | 0.101171612903 |
| raw_trl | 0.258065 | 0.271358709677 |
| trl_log | 0.690323 | 0.075565161290 |

## Interpretation

The grid is useful as an identifiability map: it separates cells where empirical transition estimates match exact action choice from lucky-only, no-success, ambiguous, and prior-dependent cells where explicit priors are required.

## Artifacts

- `research/sto_trl/artifacts/0008/identifiability_grid.py`
- `research/sto_trl/artifacts/0008/raw_grid.json`
- `research/sto_trl/artifacts/0008/metrics.csv`
- `research/sto_trl/artifacts/0008/regret_heatmap.csv`
- `research/sto_trl/artifacts/0008/action_choice_grid.csv`
- `research/sto_trl/artifacts/0008/impossibility_cases.json`
- `research/sto_trl/artifacts/0008/coverage_diagnostics.json`
- `research/sto_trl/artifacts/0008/transition_tables.json`
- `research/sto_trl/artifacts/0008/value_tables.json`


## Full evidence paths

- `research/sto_trl/results/0008_result.json`
- `research/sto_trl/results/0008_summary.md`

Inspect the full result JSON only when the compact summary and artifact list are insufficient.


## Artifact paths

- `/home/eston/autoresearcher/research/sto_trl/artifacts/0004`
- `/home/eston/autoresearcher/research/sto_trl/artifacts/0005`
- `/home/eston/autoresearcher/research/sto_trl/artifacts/0006`
- `/home/eston/autoresearcher/research/sto_trl/artifacts/0007`
- `/home/eston/autoresearcher/research/sto_trl/artifacts/0008`


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
