# Reviewer Context: reward_to_gcrl

## Latest plan

# Experiment 0004

## Objective

Resolve protected_file_drift and determine whether 0004 can be accepted as valid evidence. If drift is stale or harmless, add an explicit drift audit and review 0004 without new learning compute. If drift is real or unclear, rerun the 0004 nondegenerate 5-state chain diagnostic after clearing drift.

## Hypothesis

The 0004 scientific result is likely useful but cannot be trusted until evidence integrity is restored. After drift adjudication, either the existing 0004 artifacts will be accepted as a stronger tabular matched-stream result, or a clean rerun will reproduce the same qualitative outcome: deterministic soft targets have zero terminal-sampling variance, lower Bellman/value error, and better nondegenerate policy evaluation than sampled augmented updates.

## Success criteria

- A protected-file drift audit is written and explicitly states whether drift is stale, harmless, real, or unresolved.
- The audit identifies the exact protected file or files involved, including autoresearcher.yaml if still flagged, and records whether they affect the reward_to_gcrl experiment logic or reporting.
- If drift is stale or harmless, existing 0004 result and summary are revalidated against schemas and artifact paths, and a reviewed acceptance note records drift_status.
- If drift is real or unresolved, 0004 is rerun from a clean state with the same CPU-only tabular scope and a new result JSON containing drift_status.
- Accepted or rerun evidence must include direct sampled-vs-deterministic-soft target comparison, sampled variance versus soft variance, Bellman residual, value error, raw return, success rate, and policy diagnostics.
- The final verdict labels 0004 as one of: accepted_evidence, superseded_by_clean_rerun, rejected_due_to_drift, or inconclusive.
- No RiverSwim, auxiliary goals, neural approximation, GPU use, or larger environments are started before this gate passes.

## Failure criteria

- protected_file_drift remains true without adjudication.
- 0004 is treated as accepted evidence without a drift_status field or equivalent audit artifact.
- The drift audit does not identify which protected file changed or whether the change can affect the experiment.
- A rerun changes the scientific setup without documenting differences from 0004.
- The rerun fails to reproduce the main 0004 qualitative claims and the summary does not downgrade the evidence accordingly.
- The next step proceeds to RiverSwim, auxiliary goals, or neural approximation before resolving evidence integrity.

## Estimated runtime

<= 15 minutes

## Tasks for Codex

- Inspect research/reward_to_gcrl/state.json and the worktree guard artifact to determine why protected_file_drift is true.
- Write research/reward_to_gcrl/artifacts/0004/protected_file_drift_audit.json with affected files, hashes if available, impact assessment, and final drift_status.
- Validate existing research/reward_to_gcrl/results/0004_result.json, research/reward_to_gcrl/results/0004_summary.md, and declared artifacts if drift is judged stale or harmless.
- If drift is real or unclear, rerun the 0004 repaired sampled-vs-soft diagnostic in a clean state using the same nondegenerate 5-state chain, seeds, gammas, and CPU-only tabular budget.
- Write research/reward_to_gcrl/results/0004_result.json containing drift_status, whether 0004 was accepted or superseded, schema validation status, key scientific metrics, and pass/fail flags.
- Write research/reward_to_gcrl/results/0004_summary.md with a conservative recommendation: move to RiverSwim if 0004 is accepted or reproduced; otherwise repair the nondegenerate diagnostic again.

## Required outputs

- `research/reward_to_gcrl/results/0004_result.json`
- `research/reward_to_gcrl/results/0004_summary.md`
- `research/reward_to_gcrl/artifacts/0004/`


## Latest plan JSON

```json
{
  "estimated_runtime_minutes": 15,
  "experiment_id": "0004",
  "failure_criteria": [
    "protected_file_drift remains true without adjudication.",
    "0004 is treated as accepted evidence without a drift_status field or equivalent audit artifact.",
    "The drift audit does not identify which protected file changed or whether the change can affect the experiment.",
    "A rerun changes the scientific setup without documenting differences from 0004.",
    "The rerun fails to reproduce the main 0004 qualitative claims and the summary does not downgrade the evidence accordingly.",
    "The next step proceeds to RiverSwim, auxiliary goals, or neural approximation before resolving evidence integrity."
  ],
  "hypothesis": "The 0004 scientific result is likely useful but cannot be trusted until evidence integrity is restored. After drift adjudication, either the existing 0004 artifacts will be accepted as a stronger tabular matched-stream result, or a clean rerun will reproduce the same qualitative outcome: deterministic soft targets have zero terminal-sampling variance, lower Bellman/value error, and better nondegenerate policy evaluation than sampled augmented updates.",
  "objective": "Resolve protected_file_drift and determine whether 0004 can be accepted as valid evidence. If drift is stale or harmless, add an explicit drift audit and review 0004 without new learning compute. If drift is real or unclear, rerun the 0004 nondegenerate 5-state chain diagnostic after clearing drift.",
  "required_outputs": [
    "research/reward_to_gcrl/results/0004_result.json",
    "research/reward_to_gcrl/results/0004_summary.md",
    "research/reward_to_gcrl/artifacts/0004/"
  ],
  "success_criteria": [
    "A protected-file drift audit is written and explicitly states whether drift is stale, harmless, real, or unresolved.",
    "The audit identifies the exact protected file or files involved, including autoresearcher.yaml if still flagged, and records whether they affect the reward_to_gcrl experiment logic or reporting.",
    "If drift is stale or harmless, existing 0004 result and summary are revalidated against schemas and artifact paths, and a reviewed acceptance note records drift_status.",
    "If drift is real or unresolved, 0004 is rerun from a clean state with the same CPU-only tabular scope and a new result JSON containing drift_status.",
    "Accepted or rerun evidence must include direct sampled-vs-deterministic-soft target comparison, sampled variance versus soft variance, Bellman residual, value error, raw return, success rate, and policy diagnostics.",
    "The final verdict labels 0004 as one of: accepted_evidence, superseded_by_clean_rerun, rejected_due_to_drift, or inconclusive.",
    "No RiverSwim, auxiliary goals, neural approximation, GPU use, or larger environments are started before this gate passes."
  ],
  "tasks_for_codex": [
    "Inspect research/reward_to_gcrl/state.json and the worktree guard artifact to determine why protected_file_drift is true.",
    "Write research/reward_to_gcrl/artifacts/0004/protected_file_drift_audit.json with affected files, hashes if available, impact assessment, and final drift_status.",
    "Validate existing research/reward_to_gcrl/results/0004_result.json, research/reward_to_gcrl/results/0004_summary.md, and declared artifacts if drift is judged stale or harmless.",
    "If drift is real or unclear, rerun the 0004 repaired sampled-vs-soft diagnostic in a clean state using the same nondegenerate 5-state chain, seeds, gammas, and CPU-only tabular budget.",
    "Write research/reward_to_gcrl/results/0004_result.json containing drift_status, whether 0004 was accepted or superseded, schema validation status, key scientific metrics, and pass/fail flags.",
    "Write research/reward_to_gcrl/results/0004_summary.md with a conservative recommendation: move to RiverSwim if 0004 is accepted or reproduced; otherwise repair the nondegenerate diagnostic again."
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
