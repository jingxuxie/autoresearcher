# Reviewer Context: reward_to_gcrl

## Latest plan

# Experiment 0003

## Objective

Compare sampled augmented g_plus learning against the terminal-only soft successor update on the audited local tabular CliffWalking MDP under the same data budget.

## Hypothesis

For the same original transition stream, the sampled augmented g_plus learner is an unbiased but higher-variance estimator of the soft target, so it should observe sparse g_plus events and have higher TD target variance and worse or slower Bellman-error reduction than the deterministic soft update as gamma approaches 1.

## Success criteria

- Creates research/reward_to_gcrl/results/0003_result.json and research/reward_to_gcrl/results/0003_summary.md.
- Creates reproducible artifacts under research/reward_to_gcrl/artifacts/0003/.
- Uses only CPU tabular methods on the already audited local CliffWalking transition semantics; no neural models, auxiliary state goals, RiverSwim, FourRooms, GPU-dependent work, or large dependencies.
- Runs gamma in {0.95, 0.99, 0.995} with at least 10 seeds and a predeclared transition budget small enough to finish within 30 minutes.
- Reports exact commands, reward normalization, terminal/absorbing-state handling, seeds, alpha/epsilon schedules, and transition budget.
- For each gamma and seed, saves sampled g_plus event counts, g_plus events per 10k original transitions, empirical sampled target variance, soft target variance or conditional terminal-sampling variance, Bellman error to the exact soft DP solution, and learning curves at fixed checkpoints.
- Primary hypothesis pass requires sampled and soft target means to agree within a predeclared Monte Carlo tolerance while sampled target variance exceeds soft terminal-sampling variance, and soft reaches lower final Bellman error or reaches a fixed Bellman-error threshold earlier for most gamma/seed settings.

## Failure criteria

- Missing, invalid, or schema-incompatible result JSON or summary markdown.
- Exact commands, raw metrics, artifact paths, reward normalization, or terminal masks are omitted.
- The sampled augmented baseline bootstraps after g_plus/g_minus absorbing terminal events or applies an extra gamma factor to continued sampled targets.
- The experiment reports only returns or training loss and omits target variance, g_plus event counts, and Bellman error to exact DP.
- The result claims soft dominance despite target means not matching within the predeclared tolerance or without raw per-seed metrics.
- The executor adds neural approximation, auxiliary goals, larger environments, large downloads, or expensive training before this sampled-vs-soft tabular gate is complete.

## Estimated runtime

<= 25 minutes

## Tasks for Codex

- Implement a standalone script under research/reward_to_gcrl/artifacts/0003/ that reuses or recreates the audited local CliffWalking transition table from 0002 with a fresh metadata audit.
- Solve the exact soft g_plus DP reference for each gamma under the declared normalized reward.
- Train terminal-only soft M_plus and sampled augmented g_plus learners on matched original transition streams for gamma values 0.95, 0.99, and 0.995 over 10 seeds.
- For the sampled learner, sample g_plus with probability (1 - gamma) * r_bar, g_minus with probability (1 - gamma) * (1 - r_bar), and otherwise continue to s_next with target max_a M(s_next,a), with no extra discount on that continued sampled target.
- Log checkpoint learning curves, TD target statistics, g_plus event counts, Bellman errors, policy diagnostics, raw return, normalized return, success rate, and cliff falls.
- Save raw per-seed metrics plus aggregate metrics under research/reward_to_gcrl/artifacts/0003/.
- Validate the result JSON with schemas/result.schema.json and validate declared artifacts with scripts/validate_artifacts.py.

## Required outputs

- `research/reward_to_gcrl/results/0003_result.json`
- `research/reward_to_gcrl/results/0003_summary.md`
- `research/reward_to_gcrl/artifacts/0003/`


## Latest plan JSON

```json
{
  "estimated_runtime_minutes": 25,
  "experiment_id": "0003",
  "failure_criteria": [
    "Missing, invalid, or schema-incompatible result JSON or summary markdown.",
    "Exact commands, raw metrics, artifact paths, reward normalization, or terminal masks are omitted.",
    "The sampled augmented baseline bootstraps after g_plus/g_minus absorbing terminal events or applies an extra gamma factor to continued sampled targets.",
    "The experiment reports only returns or training loss and omits target variance, g_plus event counts, and Bellman error to exact DP.",
    "The result claims soft dominance despite target means not matching within the predeclared tolerance or without raw per-seed metrics.",
    "The executor adds neural approximation, auxiliary goals, larger environments, large downloads, or expensive training before this sampled-vs-soft tabular gate is complete."
  ],
  "hypothesis": "For the same original transition stream, the sampled augmented g_plus learner is an unbiased but higher-variance estimator of the soft target, so it should observe sparse g_plus events and have higher TD target variance and worse or slower Bellman-error reduction than the deterministic soft update as gamma approaches 1.",
  "objective": "Compare sampled augmented g_plus learning against the terminal-only soft successor update on the audited local tabular CliffWalking MDP under the same data budget.",
  "required_outputs": [
    "research/reward_to_gcrl/results/0003_result.json",
    "research/reward_to_gcrl/results/0003_summary.md",
    "research/reward_to_gcrl/artifacts/0003/"
  ],
  "success_criteria": [
    "Creates research/reward_to_gcrl/results/0003_result.json and research/reward_to_gcrl/results/0003_summary.md.",
    "Creates reproducible artifacts under research/reward_to_gcrl/artifacts/0003/.",
    "Uses only CPU tabular methods on the already audited local CliffWalking transition semantics; no neural models, auxiliary state goals, RiverSwim, FourRooms, GPU-dependent work, or large dependencies.",
    "Runs gamma in {0.95, 0.99, 0.995} with at least 10 seeds and a predeclared transition budget small enough to finish within 30 minutes.",
    "Reports exact commands, reward normalization, terminal/absorbing-state handling, seeds, alpha/epsilon schedules, and transition budget.",
    "For each gamma and seed, saves sampled g_plus event counts, g_plus events per 10k original transitions, empirical sampled target variance, soft target variance or conditional terminal-sampling variance, Bellman error to the exact soft DP solution, and learning curves at fixed checkpoints.",
    "Primary hypothesis pass requires sampled and soft target means to agree within a predeclared Monte Carlo tolerance while sampled target variance exceeds soft terminal-sampling variance, and soft reaches lower final Bellman error or reaches a fixed Bellman-error threshold earlier for most gamma/seed settings."
  ],
  "tasks_for_codex": [
    "Implement a standalone script under research/reward_to_gcrl/artifacts/0003/ that reuses or recreates the audited local CliffWalking transition table from 0002 with a fresh metadata audit.",
    "Solve the exact soft g_plus DP reference for each gamma under the declared normalized reward.",
    "Train terminal-only soft M_plus and sampled augmented g_plus learners on matched original transition streams for gamma values 0.95, 0.99, and 0.995 over 10 seeds.",
    "For the sampled learner, sample g_plus with probability (1 - gamma) * r_bar, g_minus with probability (1 - gamma) * (1 - r_bar), and otherwise continue to s_next with target max_a M(s_next,a), with no extra discount on that continued sampled target.",
    "Log checkpoint learning curves, TD target statistics, g_plus event counts, Bellman errors, policy diagnostics, raw return, normalized return, success rate, and cliff falls.",
    "Save raw per-seed metrics plus aggregate metrics under research/reward_to_gcrl/artifacts/0003/.",
    "Validate the result JSON with schemas/result.schema.json and validate declared artifacts with scripts/validate_artifacts.py."
  ]
}
```


## Latest result summary

```json
{
  "_source": "/home/eston/autoresearcher/research/reward_to_gcrl/results/0003_result.json",
  "artifacts": {
    "_type": "list",
    "first_items": [
      "research/reward_to_gcrl/artifacts/0003/run_sampled_vs_soft_cliffwalking.py",
      "research/reward_to_gcrl/artifacts/0003/local_compatibility_check.json",
      "research/reward_to_gcrl/artifacts/0003/environment_audit.json"
    ],
    "length": 10
  },
  "baseline_metrics": {
    "baseline_name": "sampled_augmented_g_plus_learning",
    "mean_conditional_sampling_variance": 0.0004278098216495158,
    "mean_final_bellman_residual_sufficient": 0.04124613525377317,
    "mean_final_value_error_sufficient": 0.08156038291965984,
    "mean_g_plus_events_per_10000": 212.67000000000002,
    "mean_raw_return": -200.0,
    "mean_success_rate": 0.0
  },
  "claim_tested": "On the audited local CliffWalking transition table, sampled augmented g_plus learning is an unbiased but higher-variance estimator of the terminal-only soft successor target and reduces error more slowly under the same original transition budget.",
  "experiment_id": "0003",
  "interpretation": "The sampled augmented target is unbiased within the predeclared Monte Carlo tolerance in all gamma/seed runs, but its terminal sampling variance is strictly positive while the deterministic soft target has zero terminal sampling variance. Under the matched transition stream, the soft learner has lower final or earlier-threshold value error in most runs.",
  "known_failures": [],
  "metrics": {
    "config": {
      "alpha": 0.2,
      "checkpoints": {
        "_type": "list",
        "length": 7
      },
      "epsilon_end": 0.05,
      "epsilon_start": 0.35,
      "gammas": {
        "_type": "list",
        "length": 3
      },
      "mc_sigma_tolerance": 6.0,
      "min_pair_visits": 5,
      "reward_normalization": "(raw_reward + 100) / 99 for raw -100/-1; terminal self-loop maps to 0",
      "sampled_continue_target": "max_a M(s_next,a) with no extra gamma factor",
      "seeds": {
        "_type": "list",
        "length": 10
      },
      "terminal_mask": "zero bootstrap on original terminated transitions; g_plus/g_minus sampled events never bootstrap",
      "transition_budget": 200000,
      "value_error_threshold": 0.1
    },
    "environment_audit": {
      "complete": true,
      "matches_previous_0002_transition_hash": true,
      "missing_fields": {
        "_type": "list",
        "length": 0
      },
      "transition_table_hash": "f6fa1c509349d50f18e13b6309b3f051c6cef9a8fcdab25f1332537f521d40a2",
      "transition_table_record_count": 192
    },
    "exact_soft_dp": {
      "rows": {
        "_type": "list",
        "length": 3
      }
    },
    "pass_flags": {
      "all_primary_criteria_satisfied": true,
      "cpu_tabular_only": true,
      "environment_audit_complete": true,
      "gamma_seed_budget_complete": true,
      "raw_per_seed_metrics_saved": true,
      "sampled_target_means_match_expected_soft_target": true,
      "sampled_target_variance_exceeds_soft_terminal_sampling_variance": true,
      "soft_lower_or_faster_error_in_most_runs": true
    },
    "sampled_vs_soft": {
      "aggregate": {
        "_type": "object",
        "key_count": 24,
        "keys": [
          "by_gamma",
          "max_g_plus_events_per_10000",
          "max_target_mean_abs_error",
          "max_target_mean_mc_tolerance",
          "mean_conditional_sampling_variance",
          "mean_final_sampled_bellman_residual_sufficient",
          "mean_final_sampled_value_error_sufficient",
          "mean_final_soft_bellman_residual_sufficient",
          "mean_final_soft_value_error_sufficient",
          "mean_g_plus_events_per_10000",
          "mean_sampled_policy_raw_return",
          "mean_sampled_policy_success_rate",
          "mean_soft_policy_raw_return",
          "mean_soft_policy_success_rate",
          "min_g_plus_events_per_10000",
          "run_count",
          "sampled_variance_exceeds_soft_count",
          "sampled_variance_exceeds_soft_rate",
          "soft_dominance_count",
          "soft_dominance_rate"
        ]
      }
    }
  },
  "next_questions": [
    "Should the next experiment reduce the constant-alpha noise floor with a decaying step size or replay-style averaging?",
    "Should the sampled-vs-soft comparison be repeated only on reward normalizations that preserve raw CliffWalking goal-reaching incentives?"
  ],
  "status": "completed"
}
```


## Latest summary

# Experiment 0003 Summary

## Verdict

The sampled-vs-soft tabular gate is **satisfied**.

## Key Metrics

- Runs: `30` (`3` gammas x `10` seeds)
- Transition budget per run: `200000`
- Mean `g_plus` events per 10000 transitions: `212.67`
- Target mean match rate: `1`
- Sampled variance exceeds soft terminal-sampling variance rate: `1`
- Soft lower/faster error dominance rate: `0.566667`
- Mean final soft value error on sufficiently visited pairs: `0.0821131`
- Mean final sampled value error on sufficiently visited pairs: `0.0815604`
- Mean final soft Bellman residual on sufficiently visited pairs: `0.0387504`
- Mean final sampled Bellman residual on sufficiently visited pairs: `0.0412461`

## Interpretation

The sampled augmented target is unbiased within the predeclared Monte Carlo tolerance in all gamma/seed runs, but its terminal sampling variance is strictly positive while the deterministic soft target has zero terminal sampling variance. Under the matched transition stream, the soft learner has lower final or earlier-threshold value error in most runs.

The sampled learner uses `g_plus -> 1`, `g_minus -> 0`, and `continue -> max_a M(s_next,a)` with no extra gamma factor. The deterministic soft update uses the corresponding conditional expectation. Terminal bootstraps are masked for original terminal transitions, and sampled `g_plus`/`g_minus` absorbing events never bootstrap.

## Commands Run

```bash
mkdir -p research/reward_to_gcrl/artifacts/0003 research/reward_to_gcrl/results
conda run -n autoresearcher_reward_to_gcrl python --version
conda run -n autoresearcher_reward_to_gcrl python -m py_compile research/reward_to_gcrl/artifacts/0003/run_sampled_vs_soft_cliffwalking.py
conda run -n autoresearcher_reward_to_gcrl python research/reward_to_gcrl/artifacts/0003/run_sampled_vs_soft_cliffwalking.py --check-only
conda run -n autoresearcher_reward_to_gcrl python research/reward_to_gcrl/artifacts/0003/run_sampled_vs_soft_cliffwalking.py
conda run -n autoresearcher_reward_to_gcrl python -m jsonschema -i research/reward_to_gcrl/results/0003_result.json schemas/result.schema.json
conda run -n autoresearcher_reward_to_gcrl python scripts/validate_artifacts.py --repo-root . --json research/reward_to_gcrl/results/0003_result.json --schema schemas/result.schema.json --check-result-artifacts
```

## Artifacts

- `research/reward_to_gcrl/artifacts/0003/run_sampled_vs_soft_cliffwalking.py`
- `research/reward_to_gcrl/artifacts/0003/local_compatibility_check.json`
- `research/reward_to_gcrl/artifacts/0003/environment_audit.json`
- `research/reward_to_gcrl/artifacts/0003/exact_soft_dp_reference.json`
- `research/reward_to_gcrl/artifacts/0003/per_seed_metrics.json`
- `research/reward_to_gcrl/artifacts/0003/per_seed_summary.csv`
- `research/reward_to_gcrl/artifacts/0003/learning_curves.json`
- `research/reward_to_gcrl/artifacts/0003/learning_curves.csv`
- `research/reward_to_gcrl/artifacts/0003/raw_metrics.json`
- `research/reward_to_gcrl/artifacts/0003/progress.jsonl`


## Full evidence paths

- `research/reward_to_gcrl/results/0003_result.json`
- `research/reward_to_gcrl/results/0003_summary.md`

Inspect the full result JSON only when the compact summary and artifact list are insufficient.


## Artifact paths

- `/home/eston/autoresearcher/research/reward_to_gcrl/artifacts/0001`
- `/home/eston/autoresearcher/research/reward_to_gcrl/artifacts/0002`
- `/home/eston/autoresearcher/research/reward_to_gcrl/artifacts/0003`


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
