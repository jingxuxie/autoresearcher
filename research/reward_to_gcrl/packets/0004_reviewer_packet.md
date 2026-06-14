# Reviewer Context: reward_to_gcrl

## Latest plan

# Experiment 0004

## Objective

Resolve protected file drift and validate the repaired nondegenerate sampled-vs-soft experiment. If existing 0004 artifacts are complete and trustworthy, review them without new learning runs; otherwise rerun a CPU-only tabular repaired diagnostic that directly compares sampled augmented targets to deterministic soft targets in a nondegenerate task.

## Hypothesis

The earlier positive variance result should survive in a nondegenerate tabular task, but a credible learning-improvement claim requires direct sampled-vs-deterministic-soft target comparison, preserved or explicitly audited raw-objective policy behavior, and soft Bellman/value performance that is lower or statistically indistinguishable from sampled under matched data.

## Success criteria

- Protected file drift is cleared or explicitly adjudicated before any 0004 or 0005 output is treated as evidence.
- The result includes an environment and reward audit with raw rewards, normalized rewards, affine constants, terminal handling, exact transition table hash, and exact-DP policy-preservation check.
- Exact DP has meaningful non-tie states and nondegenerate raw task success metrics.
- Sampled targets are compared directly to the deterministic soft target computed from the same learner state, transition, and bootstrap values, not only to the sampled learner's own conditional expectation.
- Across gamma in {0.95, 0.99, 0.995} and 10 seeds, sampled target variance exceeds deterministic soft terminal-sampling variance, while sampled target means match deterministic soft targets within predeclared Monte Carlo tolerance.
- Soft has lower mean final Bellman residual and lower or statistically indistinguishable mean final value error versus sampled; otherwise the verdict must be labeled variance-only rather than learning-improvement.
- Evaluation reports raw return, normalized return, success rate, steps to goal, and tie-aware policy disagreement against exact DP.

## Failure criteria

- Protected file drift remains unresolved.
- Existing 0004 outputs are used as evidence without review validation.
- The normalized objective again destroys raw task success or produces mostly tie states without being labeled as an objective-mismatch result.
- The target comparison again validates sampled targets only against the sampled learner's conditional expectation.
- Soft has worse value error and no compensating Bellman-residual or policy-quality advantage.
- The run adds neural networks, auxiliary goals, large environments, GPU dependence, or expensive hyperparameter sweeps before this repaired tabular gate passes.

## Estimated runtime

<= 25 minutes

## Tasks for Codex

- Inspect protected_file_drift and record whether protected files changed; do not proceed until drift is cleared or documented.
- Review existing research/reward_to_gcrl/results/0004_result.json and research/reward_to_gcrl/results/0004_summary.md if present, but mark them unaccepted unless schema, artifact, and scientific criteria pass.
- If 0004 is insufficient, create or rerun a CPU-only tabular diagnostic under research/reward_to_gcrl/artifacts/0004/ using a small nondegenerate chain or gridworld.
- Compute exact DP references for raw Q, normalized Q, and soft g_plus, including tie-aware policy preservation and value-scaling checks.
- Run matched-stream sampled augmented and deterministic soft learners with synchronized initialization, transition stream, alpha, epsilon schedule, gamma values, seeds, and transition budget.
- Record deterministic soft targets from the same learner state and transition for every sampled update so target means and variances are directly comparable.
- Save result JSON with raw metrics, pass/fail flags, exact commands, environment audit, drift status, and conservative verdict: evidence-accepted, variance-only, objective-mismatch, or failed diagnostic.
- Write a short summary that decides whether the next step should be RiverSwim long-horizon propagation, auxiliary state goals, or stopping the sampled-vs-soft learning-advantage thread.

## Required outputs

- `research/reward_to_gcrl/results/0004_result.json`
- `research/reward_to_gcrl/results/0004_summary.md`
- `research/reward_to_gcrl/artifacts/0004/`


## Latest plan JSON

```json
{
  "estimated_runtime_minutes": 25,
  "experiment_id": "0004",
  "failure_criteria": [
    "Protected file drift remains unresolved.",
    "Existing 0004 outputs are used as evidence without review validation.",
    "The normalized objective again destroys raw task success or produces mostly tie states without being labeled as an objective-mismatch result.",
    "The target comparison again validates sampled targets only against the sampled learner's conditional expectation.",
    "Soft has worse value error and no compensating Bellman-residual or policy-quality advantage.",
    "The run adds neural networks, auxiliary goals, large environments, GPU dependence, or expensive hyperparameter sweeps before this repaired tabular gate passes."
  ],
  "hypothesis": "The earlier positive variance result should survive in a nondegenerate tabular task, but a credible learning-improvement claim requires direct sampled-vs-deterministic-soft target comparison, preserved or explicitly audited raw-objective policy behavior, and soft Bellman/value performance that is lower or statistically indistinguishable from sampled under matched data.",
  "objective": "Resolve protected file drift and validate the repaired nondegenerate sampled-vs-soft experiment. If existing 0004 artifacts are complete and trustworthy, review them without new learning runs; otherwise rerun a CPU-only tabular repaired diagnostic that directly compares sampled augmented targets to deterministic soft targets in a nondegenerate task.",
  "required_outputs": [
    "research/reward_to_gcrl/results/0004_result.json",
    "research/reward_to_gcrl/results/0004_summary.md",
    "research/reward_to_gcrl/artifacts/0004/"
  ],
  "success_criteria": [
    "Protected file drift is cleared or explicitly adjudicated before any 0004 or 0005 output is treated as evidence.",
    "The result includes an environment and reward audit with raw rewards, normalized rewards, affine constants, terminal handling, exact transition table hash, and exact-DP policy-preservation check.",
    "Exact DP has meaningful non-tie states and nondegenerate raw task success metrics.",
    "Sampled targets are compared directly to the deterministic soft target computed from the same learner state, transition, and bootstrap values, not only to the sampled learner's own conditional expectation.",
    "Across gamma in {0.95, 0.99, 0.995} and 10 seeds, sampled target variance exceeds deterministic soft terminal-sampling variance, while sampled target means match deterministic soft targets within predeclared Monte Carlo tolerance.",
    "Soft has lower mean final Bellman residual and lower or statistically indistinguishable mean final value error versus sampled; otherwise the verdict must be labeled variance-only rather than learning-improvement.",
    "Evaluation reports raw return, normalized return, success rate, steps to goal, and tie-aware policy disagreement against exact DP."
  ],
  "tasks_for_codex": [
    "Inspect protected_file_drift and record whether protected files changed; do not proceed until drift is cleared or documented.",
    "Review existing research/reward_to_gcrl/results/0004_result.json and research/reward_to_gcrl/results/0004_summary.md if present, but mark them unaccepted unless schema, artifact, and scientific criteria pass.",
    "If 0004 is insufficient, create or rerun a CPU-only tabular diagnostic under research/reward_to_gcrl/artifacts/0004/ using a small nondegenerate chain or gridworld.",
    "Compute exact DP references for raw Q, normalized Q, and soft g_plus, including tie-aware policy preservation and value-scaling checks.",
    "Run matched-stream sampled augmented and deterministic soft learners with synchronized initialization, transition stream, alpha, epsilon schedule, gamma values, seeds, and transition budget.",
    "Record deterministic soft targets from the same learner state and transition for every sampled update so target means and variances are directly comparable.",
    "Save result JSON with raw metrics, pass/fail flags, exact commands, environment audit, drift status, and conservative verdict: evidence-accepted, variance-only, objective-mismatch, or failed diagnostic.",
    "Write a short summary that decides whether the next step should be RiverSwim long-horizon propagation, auxiliary state goals, or stopping the sampled-vs-soft learning-advantage thread."
  ]
}
```


## Latest result summary

```json
{
  "_source": "/home/eston/autoresearcher/research/reward_to_gcrl/results/0004_result.json",
  "artifacts": {
    "_type": "list",
    "first_items": [
      "research/reward_to_gcrl/artifacts/0004/run_repaired_sampled_vs_soft.py",
      "research/reward_to_gcrl/artifacts/0004/local_compatibility_check.json",
      "research/reward_to_gcrl/artifacts/0004/environment_audit.json"
    ],
    "length": 10
  },
  "baseline_metrics": {
    "baseline_name": "sampled_augmented_g_plus_learning",
    "mean_conditional_sampling_variance": 0.006258455730468815,
    "mean_final_bellman_residual": 0.005863347048562961,
    "mean_final_value_error": 0.028406430871095144,
    "mean_g_plus_events_per_10000": 63.79,
    "mean_policy_disagreement": 0.55,
    "mean_raw_return": 0.0,
    "mean_success_rate": 0.0
  },
  "claim_tested": "In a nondegenerate tiny chain with identity reward normalization, sampled augmented g_plus updates are unbiased but higher variance, while deterministic soft terminal marginalization improves Bellman residual and preserves policy quality.",
  "experiment_id": "0004",
  "interpretation": "The repaired chain preserves the raw policy under identity normalization. Sampled targets match the deterministic soft marginal target within the predeclared Monte Carlo tolerance, have positive sampling variance, and the deterministic soft learner achieves lower mean final Bellman residual with statistically non-worse value error and policy quality.",
  "known_failures": [],
  "metrics": {
    "config": {
      "alpha": 0.1,
      "checkpoints": {
        "_type": "list",
        "length": 8
      },
      "epsilon_end": 0.02,
      "epsilon_start": 0.2,
      "gammas": {
        "_type": "list",
        "length": 3
      },
      "mc_sigma_tolerance": 6.0,
      "reward_normalization": "identity affine map, normalized_reward = raw_reward",
      "sampled_continue_target": "max_a M(s_next,a), no extra gamma factor",
      "seeds": {
        "_type": "list",
        "length": 10
      },
      "statistical_z_for_value_error_indistinguishable": 2.0,
      "transition_budget": 100000
    },
    "environment_audit": {
      "complete": true,
      "missing_fields": {
        "_type": "list",
        "length": 0
      },
      "reward_audit": {
        "_type": "object",
        "key_count": 8,
        "keys": [
          "affine_offset",
          "affine_scale",
          "non_success_reward",
          "normalization",
          "normalized_rewards",
          "raw_rewards",
          "success_reward",
          "terminal_self_loop_reward"
        ]
      },
      "transition_table_hash": "7495dbe7c45ab92e3360f7de0dfd64d16a3f6299147d6ea847d8cd418f49ffbb",
      "transition_table_record_count": 10
    },
    "exact_dp": {
      "non_tie_policy_informative": true,
      "raw_normalized_policy_preserved": true,
      "rows": {
        "_type": "list",
        "length": 3
      }
    },
    "pass_flags": {
      "cpu_tabular_only": true,
      "environment_audit_complete": true,
      "exact_dp_non_tie_policy_informative": true,
      "gamma_seed_budget_complete": true,
      "raw_normalized_policy_preserved": true,
      "sampled_variance_exceeds_soft_all_runs": true,
      "soft_lower_mean_final_bellman_residual": true,
      "soft_policy_quality_non_worse": true,
      "soft_value_error_lower_or_statistically_indistinguishable": true,
      "target_mean_match_all_runs": true
    },
    "sampled_vs_soft": {
      "aggregate": {
        "_type": "object",
        "key_count": 23,
        "keys": [
          "by_gamma",
          "mean_conditional_sampling_variance",
          "mean_final_sampled_bellman_residual",
          "mean_final_sampled_value_error",
          "mean_final_soft_bellman_residual",
          "mean_final_soft_value_error",
          "mean_g_plus_events_per_10000",
          "mean_sampled_policy_disagreement",
          "mean_sampled_raw_return",
          "mean_sampled_success_rate",
          "mean_soft_policy_disagreement",
          "mean_soft_raw_return",
          "mean_soft_success_rate",
          "run_count",
          "sampled_variance_exceeds_soft_count",
          "sampled_variance_exceeds_soft_rate",
          "soft_bellman_residual_lower",
          "soft_minus_sampled_bellman_residual",
          "soft_minus_sampled_value_error",
          "soft_policy_quality_non_worse"
        ]
      }
    },
    "verdict": "learning-improvement"
  },
  "next_questions": [
    "Would a decaying step-size schedule preserve the soft Bellman-residual advantage while reducing both learners' value error?",
    "Does the repaired chain result transfer to a small grid with identity or policy-preserving reward normalization?"
  ],
  "status": "completed"
}
```


## Latest summary

# Experiment 0004 Summary

## Verdict

Conservative verdict: **learning-improvement**.

## Key Metrics

- Runs: `30` (`3` gammas x `10` seeds)
- Transition budget per run: `100000`
- Mean `g_plus` events per 10000 transitions: `63.79`
- Target mean match rate: `1`
- Sampled variance exceeds soft terminal-sampling variance rate: `1`
- Mean final soft Bellman residual: `1.09866e-17`
- Mean final sampled Bellman residual: `0.00586335`
- Mean final soft value error: `3.05022e-17`
- Mean final sampled value error: `0.0284064`
- Mean soft success rate: `1`
- Mean sampled success rate: `0`

## Interpretation

The repaired chain preserves the raw policy under identity normalization. Sampled targets match the deterministic soft marginal target within the predeclared Monte Carlo tolerance, have positive sampling variance, and the deterministic soft learner achieves lower mean final Bellman residual with statistically non-worse value error and policy quality.

The chain uses identity reward normalization: normalized reward equals raw reward, with success reward `1` and all other rewards `0`. Exact DP verifies raw and normalized policies agree on non-terminal non-tie decision states.

## Commands Run

```bash
mkdir -p research/reward_to_gcrl/artifacts/0004 research/reward_to_gcrl/results
conda run -n autoresearcher_reward_to_gcrl python --version
conda run -n autoresearcher_reward_to_gcrl python -m py_compile research/reward_to_gcrl/artifacts/0004/run_repaired_sampled_vs_soft.py
conda run -n autoresearcher_reward_to_gcrl python research/reward_to_gcrl/artifacts/0004/run_repaired_sampled_vs_soft.py --check-only
conda run -n autoresearcher_reward_to_gcrl python research/reward_to_gcrl/artifacts/0004/run_repaired_sampled_vs_soft.py
conda run -n autoresearcher_reward_to_gcrl python -m jsonschema -i research/reward_to_gcrl/results/0004_result.json schemas/result.schema.json
conda run -n autoresearcher_reward_to_gcrl python scripts/validate_artifacts.py --repo-root . --json research/reward_to_gcrl/results/0004_result.json --schema schemas/result.schema.json --check-result-artifacts
```

## Artifacts

- `research/reward_to_gcrl/artifacts/0004/run_repaired_sampled_vs_soft.py`
- `research/reward_to_gcrl/artifacts/0004/local_compatibility_check.json`
- `research/reward_to_gcrl/artifacts/0004/environment_audit.json`
- `research/reward_to_gcrl/artifacts/0004/exact_dp_references.json`
- `research/reward_to_gcrl/artifacts/0004/per_seed_metrics.json`
- `research/reward_to_gcrl/artifacts/0004/per_seed_summary.csv`
- `research/reward_to_gcrl/artifacts/0004/learning_curves.json`
- `research/reward_to_gcrl/artifacts/0004/learning_curves.csv`
- `research/reward_to_gcrl/artifacts/0004/raw_metrics.json`
- `research/reward_to_gcrl/artifacts/0004/progress.jsonl`


## Full evidence paths

- `research/reward_to_gcrl/results/0004_result.json`
- `research/reward_to_gcrl/results/0004_summary.md`

Inspect the full result JSON only when the compact summary and artifact list are insufficient.


## Artifact paths

- `/home/eston/autoresearcher/research/reward_to_gcrl/artifacts/0001`
- `/home/eston/autoresearcher/research/reward_to_gcrl/artifacts/0002`
- `/home/eston/autoresearcher/research/reward_to_gcrl/artifacts/0003`
- `/home/eston/autoresearcher/research/reward_to_gcrl/artifacts/0004`


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
