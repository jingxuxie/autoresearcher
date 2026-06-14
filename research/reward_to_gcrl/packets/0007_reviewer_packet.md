# Reviewer Context: reward_to_gcrl

## Latest plan

# Experiment 0007

## Objective

Run a CPU-only tabular RiverSwim coverage dose-response experiment that uses several non-oracle behavior policies to create starved, borderline, and adequate coverage regimes, then quantify exactly when deterministic soft terminal marginalization improves Bellman residual, value error, and policy quality over sampled augmented updates.

## Hypothesis

The deterministic soft update should consistently reduce terminal-sampling variance in all coverage regimes, but learning-performance advantages should appear mainly when right-reward and state-action coverage are adequate. In coverage-starved regimes, soft may lower Bellman residual without reliably lowering value error, so coverage should be treated as a prerequisite for learning-superiority claims.

## Success criteria

- Use only CPU tabular code on the same audited 6-state RiverSwim semantics as 0005 and 0006.
- Generate matched logged streams from at least four fixed non-oracle behavior policies, such as uniform random, mild right bias, strong right bias, and alternating or epsilon-cyclic exploration, with no exact-Q action guidance.
- Predeclare coverage bins using right-reward events per 10000 transitions and visited state-action-pair counts, then report results separately for starved, borderline, and adequate coverage.
- For every gamma-behavior-seed run, sampled target means must match deterministic soft marginal targets within predeclared Monte Carlo tolerance, and sampled terminal-sampling variance must exceed soft terminal-sampling variance.
- On adequate-coverage runs, soft must have lower mean final Bellman residual and lower or statistically indistinguishable mean final value error than sampled.
- On starved runs, the summary must explicitly avoid learning-superiority claims and report whether Bellman residual and value error disagree.
- Include a simple coverage-performance regression or stratified table showing how soft-minus-sampled value error changes with right-reward event count and visited state-action coverage.
- The final recommendation must state whether to move next to tabular auxiliary real-state goals or whether more estimator-only RiverSwim work is still needed.

## Failure criteria

- Any behavior policy uses exact DP, exact Q, or reward-optimal action preferences to generate the logged stream.
- The run does not produce both adequate-coverage and coverage-starved regimes, making the coverage caveat unresolved.
- Target means are compared only to the sampled learner's own conditional expectation rather than the deterministic soft marginal target from the same transition and learner state.
- Soft has worse value error than sampled in adequate-coverage runs without a clear explanation.
- The summary makes an unconditional learning-superiority claim despite coverage-starved failures.
- The experiment adds auxiliary goals, neural approximation, larger environments, GPU dependence, or expensive hyperparameter sweeps before this coverage gate is resolved.

## Estimated runtime

<= 25 minutes

## Tasks for Codex

- Create research/reward_to_gcrl/artifacts/0007/run_riverswim_coverage_dose_response.py by extending the 0006 non-oracle RiverSwim script.
- Reuse and verify the same 6-state RiverSwim transition hash, reward normalization, action mapping, and exact DP references from 0005 and 0006.
- Implement at least four fixed non-oracle behavior policies that span expected coverage levels without consulting exact Q or exact DP for action selection.
- Run gamma in {0.95, 0.99, 0.995} over 10 seeds per behavior with a CPU-tabular budget no larger than 0006 unless a smaller pilot shows adequate coverage is impossible.
- Record direct sampled-vs-deterministic-soft target mean error, terminal-sampling variance, g_plus events, right-reward events, visited state-action pairs, Bellman residual, value error, policy disagreement, and greedy raw return.
- Stratify outputs by coverage bin and compute soft-minus-sampled deltas for Bellman residual, value error, and greedy return.
- Save research/reward_to_gcrl/results/0007_result.json with raw metrics, exact commands, behavior definitions, pass/fail flags, and coverage-bin summaries.
- Save research/reward_to_gcrl/results/0007_summary.md with a conservative verdict on whether coverage is sufficiently bounded to proceed to tabular auxiliary state-goal experiments.

## Required outputs

- `research/reward_to_gcrl/results/0007_result.json`
- `research/reward_to_gcrl/results/0007_summary.md`
- `research/reward_to_gcrl/artifacts/0007/`


## Latest plan JSON

```json
{
  "estimated_runtime_minutes": 25,
  "experiment_id": "0007",
  "failure_criteria": [
    "Any behavior policy uses exact DP, exact Q, or reward-optimal action preferences to generate the logged stream.",
    "The run does not produce both adequate-coverage and coverage-starved regimes, making the coverage caveat unresolved.",
    "Target means are compared only to the sampled learner's own conditional expectation rather than the deterministic soft marginal target from the same transition and learner state.",
    "Soft has worse value error than sampled in adequate-coverage runs without a clear explanation.",
    "The summary makes an unconditional learning-superiority claim despite coverage-starved failures.",
    "The experiment adds auxiliary goals, neural approximation, larger environments, GPU dependence, or expensive hyperparameter sweeps before this coverage gate is resolved."
  ],
  "hypothesis": "The deterministic soft update should consistently reduce terminal-sampling variance in all coverage regimes, but learning-performance advantages should appear mainly when right-reward and state-action coverage are adequate. In coverage-starved regimes, soft may lower Bellman residual without reliably lowering value error, so coverage should be treated as a prerequisite for learning-superiority claims.",
  "objective": "Run a CPU-only tabular RiverSwim coverage dose-response experiment that uses several non-oracle behavior policies to create starved, borderline, and adequate coverage regimes, then quantify exactly when deterministic soft terminal marginalization improves Bellman residual, value error, and policy quality over sampled augmented updates.",
  "required_outputs": [
    "research/reward_to_gcrl/results/0007_result.json",
    "research/reward_to_gcrl/results/0007_summary.md",
    "research/reward_to_gcrl/artifacts/0007/"
  ],
  "success_criteria": [
    "Use only CPU tabular code on the same audited 6-state RiverSwim semantics as 0005 and 0006.",
    "Generate matched logged streams from at least four fixed non-oracle behavior policies, such as uniform random, mild right bias, strong right bias, and alternating or epsilon-cyclic exploration, with no exact-Q action guidance.",
    "Predeclare coverage bins using right-reward events per 10000 transitions and visited state-action-pair counts, then report results separately for starved, borderline, and adequate coverage.",
    "For every gamma-behavior-seed run, sampled target means must match deterministic soft marginal targets within predeclared Monte Carlo tolerance, and sampled terminal-sampling variance must exceed soft terminal-sampling variance.",
    "On adequate-coverage runs, soft must have lower mean final Bellman residual and lower or statistically indistinguishable mean final value error than sampled.",
    "On starved runs, the summary must explicitly avoid learning-superiority claims and report whether Bellman residual and value error disagree.",
    "Include a simple coverage-performance regression or stratified table showing how soft-minus-sampled value error changes with right-reward event count and visited state-action coverage.",
    "The final recommendation must state whether to move next to tabular auxiliary real-state goals or whether more estimator-only RiverSwim work is still needed."
  ],
  "tasks_for_codex": [
    "Create research/reward_to_gcrl/artifacts/0007/run_riverswim_coverage_dose_response.py by extending the 0006 non-oracle RiverSwim script.",
    "Reuse and verify the same 6-state RiverSwim transition hash, reward normalization, action mapping, and exact DP references from 0005 and 0006.",
    "Implement at least four fixed non-oracle behavior policies that span expected coverage levels without consulting exact Q or exact DP for action selection.",
    "Run gamma in {0.95, 0.99, 0.995} over 10 seeds per behavior with a CPU-tabular budget no larger than 0006 unless a smaller pilot shows adequate coverage is impossible.",
    "Record direct sampled-vs-deterministic-soft target mean error, terminal-sampling variance, g_plus events, right-reward events, visited state-action pairs, Bellman residual, value error, policy disagreement, and greedy raw return.",
    "Stratify outputs by coverage bin and compute soft-minus-sampled deltas for Bellman residual, value error, and greedy return.",
    "Save research/reward_to_gcrl/results/0007_result.json with raw metrics, exact commands, behavior definitions, pass/fail flags, and coverage-bin summaries.",
    "Save research/reward_to_gcrl/results/0007_summary.md with a conservative verdict on whether coverage is sufficiently bounded to proceed to tabular auxiliary state-goal experiments."
  ]
}
```


## Latest result summary

```json
{
  "_source": "/home/eston/autoresearcher/research/reward_to_gcrl/results/0007_result.json",
  "artifacts": {
    "_type": "list",
    "first_items": [
      "research/reward_to_gcrl/artifacts/0007/run_riverswim_coverage_dose_response.py",
      "research/reward_to_gcrl/artifacts/0007/local_compatibility_check.json",
      "research/reward_to_gcrl/artifacts/0007/environment_audit.json"
    ],
    "length": 10
  },
  "baseline_metrics": {
    "baseline_name": "sampled_augmented_g_plus_learning",
    "coverage_starved_count": 30,
    "mean_final_bellman_residual": 0.006313229252871876,
    "mean_final_value_error": 0.1331149724439577,
    "mean_g_plus_events_per_10000": 5.397222222222222,
    "mean_greedy_raw_return": 30.848583333333334
  },
  "claim_tested": "On 6-state RiverSwim with non-oracle behavior streams, sampled augmented g_plus updates remain unbiased but higher variance than deterministic soft updates, with coverage determining whether learning advantages are interpretable.",
  "experiment_id": "0007",
  "interpretation": "Coverage dose response completed: sampled targets match deterministic soft marginal targets within tolerance and have higher terminal-sampling variance in every run. Soft learning advantages are supported on adequate-coverage runs only; starved runs are reported as coverage-limited diagnostics rather than learning-superiority evidence.",
  "known_failures": [],
  "metrics": {
    "config": {
      "alpha": 0.05,
      "behaviors": {
        "_type": "object",
        "key_count": 4,
        "keys": [
          "medium_right_bias",
          "mild_right_bias",
          "strong_right_bias",
          "uniform_random"
        ]
      },
      "bellman_residual_threshold": 0.01,
      "checkpoints": {
        "_type": "list",
        "length": 7
      },
      "coverage_thresholds": {
        "_type": "object",
        "key_count": 4,
        "keys": [
          "adequate_right_reward_events_per_10000_gte",
          "borderline_right_reward_events_per_10000_lt",
          "min_visited_state_action_pairs",
          "starved_right_reward_events_per_10000_lt"
        ]
      },
      "gammas": {
        "_type": "list",
        "length": 3
      },
      "mc_sigma_tolerance": 6.0,
      "reward_normalization": "identity(raw_reward), rewards already in [0,1]",
      "sampled_continue_target": "max_a M(s_next,a), no extra gamma factor",
      "seeds": {
        "_type": "list",
        "length": 10
      },
      "transition_budget": 150000,
      "value_error_indistinguishable_z": 1.96
    },
    "environment_audit": {
      "complete": true,
      "missing_fields": {
        "_type": "list",
        "length": 0
      },
      "reward_normalization": {
        "_type": "object",
        "key_count": 7,
        "keys": [
          "affine_offset",
          "affine_scale",
          "all_other_rewards",
          "left_end_small_reward",
          "normalized_reward",
          "raw_rewards_in_[0,1]",
          "right_end_sparse_reward"
        ]
      },
      "transition_table_hash": "2e481565b49954b048469471863e55d38268fb628e07d8839b77f881ae07a2ed",
      "transition_table_shape": {
        "_type": "list",
        "length": 3
      }
    },
    "exact_dp": {
      "rows": {
        "_type": "list",
        "length": 3
      },
      "scaled_soft_matches_q_norm": true
    },
    "pass_flags": {
      "adequate_coverage_soft_advantage": true,
      "at_least_four_non_oracle_behaviors": true,
      "coverage_bin_summaries_and_regression_reported": true,
      "cpu_tabular_only": true,
      "environment_audit_complete": true,
      "exact_scaled_soft_matches_q_norm": true,
      "gamma_seed_behavior_grid_complete": true,
      "same_transition_hash_as_0005_0006": true,
      "sampled_variance_exceeds_soft_all_runs": true,
      "starved_borderline_adequate_bins_present": true,
      "starved_runs_caveated": true,
      "target_mean_match_all_runs": true
    },
    "recommendation": "move_next_to_tabular_auxiliary_real_state_goals",
    "sampled_vs_soft": {
      "aggregate": {
        "_type": "object",
        "key_count": 39,
        "keys": [
          "adequate_coverage_count",
          "adequately_covered",
          "bellman_value_direction_disagreement",
          "borderline_coverage",
          "borderline_coverage_count",
          "by_behavior",
          "by_coverage_bin",
          "coverage_bin_counts",
          "coverage_bin_thresholds",
          "coverage_bins_present",
          "coverage_performance_regression",
          "coverage_starved",
          "coverage_starved_count",
          "mean_final_sampled_bellman_residual",
          "mean_final_sampled_value_error",
          "mean_final_soft_bellman_residual",
          "mean_final_soft_value_error",
          "mean_g_plus_events_per_10000",
          "mean_right_end_occupancy_rate",
          "mean_right_reward_events_per_10000"
        ]
      }
    }
  },
  "next_questions": [
    "Do tabular auxiliary real-state goals preserve the estimator advantages under adequate RiverSwim coverage?",
    "Do coverage-starved settings need explicit data-collection fixes before making learning-superiority claims?"
  ],
  "status": "completed"
}
```


## Latest summary

# Experiment 0007 Summary

## Verdict

RiverSwim coverage dose-response status: **completed**.

Recommendation: **move_next_to_tabular_auxiliary_real_state_goals**.

## Key Metrics

- Runs: `120` (`4` behaviors x `3` gammas x `10` seeds)
- Transition budget per run: `150000`
- Starved runs: `30`
- Borderline runs: `55`
- Adequately covered runs: `35`
- Target mean match rate: `1`
- Sampled variance exceeds soft terminal-sampling variance rate: `1`
- Mean `g_plus` events per 10000 transitions: `5.39722`
- Mean right reward events per 10000 transitions: `232.197`
- Mean final soft Bellman residual: `0.0018651`
- Mean final sampled Bellman residual: `0.00631323`
- Mean final soft value error: `0.123756`
- Mean final sampled value error: `0.133115`

## Coverage Dose Response

| Bin | Runs | Right rewards / 10k | Soft-sampled residual delta | Soft-sampled value-error delta | Soft-sampled raw-return delta | Residual/value disagreement |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| starved | 30 | 11.4222 | -0.00277697 | 0.0401128 | 49.9263 | True |
| borderline | 55 | 164.088 | -0.00478021 | -0.00317412 | 45.7185 | False |
| adequate | 35 | 528.461 | -0.00535871 | -0.0614823 | 54.0566 | False |

Regression target: `soft_minus_sampled_final_value_error`; right-reward coefficient: `-0.000193094`; R^2: `0.39568`.

## Interpretation

Coverage dose response completed: sampled targets match deterministic soft marginal targets within tolerance and have higher terminal-sampling variance in every run. Soft learning advantages are supported on adequate-coverage runs only; starved runs are reported as coverage-limited diagnostics rather than learning-superiority evidence.

Starved runs are coverage-limited and are not used for learning-superiority claims. Bellman/value disagreement in starved runs: `True`.

Behavior policies are fixed action-probability policies (`uniform_random, mild_right_bias, medium_right_bias, strong_right_bias`) and do not use exact Q or DP-derived action preferences.

## Commands Run

```bash
mkdir -p research/reward_to_gcrl/artifacts/0007 research/reward_to_gcrl/results
conda run -n autoresearcher_reward_to_gcrl python --version
conda run -n autoresearcher_reward_to_gcrl python -m py_compile research/reward_to_gcrl/artifacts/0007/run_riverswim_coverage_dose_response.py
conda run -n autoresearcher_reward_to_gcrl python research/reward_to_gcrl/artifacts/0007/run_riverswim_coverage_dose_response.py --check-only
conda run -n autoresearcher_reward_to_gcrl python research/reward_to_gcrl/artifacts/0007/run_riverswim_coverage_dose_response.py
conda run -n autoresearcher_reward_to_gcrl python -m jsonschema -i research/reward_to_gcrl/results/0007_result.json schemas/result.schema.json
conda run -n autoresearcher_reward_to_gcrl python scripts/validate_artifacts.py --repo-root . --json research/reward_to_gcrl/results/0007_result.json --schema schemas/result.schema.json --check-result-artifacts
```

## Artifacts

- `research/reward_to_gcrl/artifacts/0007/run_riverswim_coverage_dose_response.py`
- `research/reward_to_gcrl/artifacts/0007/local_compatibility_check.json`
- `research/reward_to_gcrl/artifacts/0007/environment_audit.json`
- `research/reward_to_gcrl/artifacts/0007/exact_dp_references.json`
- `research/reward_to_gcrl/artifacts/0007/per_seed_metrics.json`
- `research/reward_to_gcrl/artifacts/0007/per_seed_summary.csv`
- `research/reward_to_gcrl/artifacts/0007/learning_curves.json`
- `research/reward_to_gcrl/artifacts/0007/learning_curves.csv`
- `research/reward_to_gcrl/artifacts/0007/raw_metrics.json`
- `research/reward_to_gcrl/artifacts/0007/progress.jsonl`


## Full evidence paths

- `research/reward_to_gcrl/results/0007_result.json`
- `research/reward_to_gcrl/results/0007_summary.md`

Inspect the full result JSON only when the compact summary and artifact list are insufficient.


## Artifact paths

- `/home/eston/autoresearcher/research/reward_to_gcrl/artifacts/0003`
- `/home/eston/autoresearcher/research/reward_to_gcrl/artifacts/0004`
- `/home/eston/autoresearcher/research/reward_to_gcrl/artifacts/0005`
- `/home/eston/autoresearcher/research/reward_to_gcrl/artifacts/0006`
- `/home/eston/autoresearcher/research/reward_to_gcrl/artifacts/0007`


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
