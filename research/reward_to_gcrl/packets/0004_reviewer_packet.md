# Reviewer Context: reward_to_gcrl

## Latest plan

# Experiment 0004

## Objective

Resolve the protected_file_drift blocker and determine whether the existing 0004 nondegenerate 5-state sampled-vs-soft result can be accepted as evidence, superseded by a clean rerun, rejected due to drift, or marked inconclusive.

## Hypothesis

The 0004 scientific result is likely useful, but its evidential status depends on whether the protected-file drift is stale or harmless versus real or unresolved. A cheap audit should either accept the existing 0004 artifacts with explicit drift_status or trigger a clean CPU-only rerun of the same 5-state diagnostic.

## Success criteria

- A protected-file drift audit is written to research/reward_to_gcrl/artifacts/0005/protected_file_drift_audit.json.
- The audit identifies every affected protected file, including autoresearcher.yaml if still relevant, and records current status, available hashes or timestamps, whether the file is still modified, and whether the change can affect experiment logic, reporting, or validation.
- research/reward_to_gcrl/results/0005_result.json includes a top-level drift_status with one of stale, harmless, real, or unresolved.
- research/reward_to_gcrl/results/0005_result.json includes a final verdict on 0004 with one of accepted_evidence, superseded_by_clean_rerun, rejected_due_to_drift, or inconclusive.
- If drift is stale or harmless, existing 0004 result JSON, summary markdown, and declared artifact paths are revalidated and this validation is recorded.
- If drift is real or unresolved, the same 5-state CPU-only diagnostic is rerun from a clean or explicitly adjudicated state, with the prior 0004 result marked superseded or inconclusive.
- No RiverSwim, auxiliary goals, neural approximation, GPU use, large dependencies, or larger environments are started before this evidence-integrity gate passes.

## Failure criteria

- protected_file_drift remains true without an audit artifact.
- The audit does not identify which protected file changed or whether the change could affect experiment logic or reporting.
- 0004 is treated as accepted evidence without drift_status and final verdict fields.
- A rerun, if needed, changes the 5-state scientific setup without documenting differences from the prior 0004 run.
- The clean rerun fails to reproduce the main 0004 qualitative claims and the summary does not downgrade the evidence.
- The workflow proceeds to RiverSwim, auxiliary goals, neural approximation, or larger experiments before resolving this gate.

## Estimated runtime

<= 15 minutes

## Tasks for Codex

- Inspect research/reward_to_gcrl/state.json and research/reward_to_gcrl/decisions/0004_worktree_guard.json to determine why protected_file_drift is true.
- Create research/reward_to_gcrl/artifacts/0004/protected_file_drift_audit.json with affected files, current worktree status, hashes if available, impact assessment, and drift_status.
- Validate existing research/reward_to_gcrl/results/0004_result.json, research/reward_to_gcrl/results/0004_summary.md, and declared 0004 artifacts if drift is stale or harmless.
- If drift is real or unresolved, rerun the existing 0004 repaired nondegenerate 5-state sampled-vs-soft diagnostic with the same seeds, gammas, transition budget, and CPU-only tabular scope.
- Write research/reward_to_gcrl/results/0004_result.json with drift_status, 0004 verdict, validation status, exact commands, pass/fail flags, and key scientific metrics if a rerun occurs.
- Write research/reward_to_gcrl/results/0004_summary.md with a conservative recommendation: move to RiverSwim only if 0004 is accepted or cleanly reproduced; otherwise repair the drift or rerun again.

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
    "protected_file_drift remains true without an audit artifact.",
    "The audit does not identify which protected file changed or whether the change could affect experiment logic or reporting.",
    "0004 is treated as accepted evidence without drift_status and final verdict fields.",
    "A rerun, if needed, changes the 5-state scientific setup without documenting differences from the prior 0004 run.",
    "The clean rerun fails to reproduce the main 0004 qualitative claims and the summary does not downgrade the evidence.",
    "The workflow proceeds to RiverSwim, auxiliary goals, neural approximation, or larger experiments before resolving this gate."
  ],
  "hypothesis": "The 0004 scientific result is likely useful, but its evidential status depends on whether the protected-file drift is stale or harmless versus real or unresolved. A cheap audit should either accept the existing 0004 artifacts with explicit drift_status or trigger a clean CPU-only rerun of the same 5-state diagnostic.",
  "objective": "Resolve the protected_file_drift blocker and determine whether the existing 0004 nondegenerate 5-state sampled-vs-soft result can be accepted as evidence, superseded by a clean rerun, rejected due to drift, or marked inconclusive.",
  "required_outputs": [
    "research/reward_to_gcrl/results/0004_result.json",
    "research/reward_to_gcrl/results/0004_summary.md",
    "research/reward_to_gcrl/artifacts/0004/"
  ],
  "success_criteria": [
    "A protected-file drift audit is written to research/reward_to_gcrl/artifacts/0005/protected_file_drift_audit.json.",
    "The audit identifies every affected protected file, including autoresearcher.yaml if still relevant, and records current status, available hashes or timestamps, whether the file is still modified, and whether the change can affect experiment logic, reporting, or validation.",
    "research/reward_to_gcrl/results/0005_result.json includes a top-level drift_status with one of stale, harmless, real, or unresolved.",
    "research/reward_to_gcrl/results/0005_result.json includes a final verdict on 0004 with one of accepted_evidence, superseded_by_clean_rerun, rejected_due_to_drift, or inconclusive.",
    "If drift is stale or harmless, existing 0004 result JSON, summary markdown, and declared artifact paths are revalidated and this validation is recorded.",
    "If drift is real or unresolved, the same 5-state CPU-only diagnostic is rerun from a clean or explicitly adjudicated state, with the prior 0004 result marked superseded or inconclusive.",
    "No RiverSwim, auxiliary goals, neural approximation, GPU use, large dependencies, or larger environments are started before this evidence-integrity gate passes."
  ],
  "tasks_for_codex": [
    "Inspect research/reward_to_gcrl/state.json and research/reward_to_gcrl/decisions/0004_worktree_guard.json to determine why protected_file_drift is true.",
    "Create research/reward_to_gcrl/artifacts/0004/protected_file_drift_audit.json with affected files, current worktree status, hashes if available, impact assessment, and drift_status.",
    "Validate existing research/reward_to_gcrl/results/0004_result.json, research/reward_to_gcrl/results/0004_summary.md, and declared 0004 artifacts if drift is stale or harmless.",
    "If drift is real or unresolved, rerun the existing 0004 repaired nondegenerate 5-state sampled-vs-soft diagnostic with the same seeds, gammas, transition budget, and CPU-only tabular scope.",
    "Write research/reward_to_gcrl/results/0004_result.json with drift_status, 0004 verdict, validation status, exact commands, pass/fail flags, and key scientific metrics if a rerun occurs.",
    "Write research/reward_to_gcrl/results/0004_summary.md with a conservative recommendation: move to RiverSwim only if 0004 is accepted or cleanly reproduced; otherwise repair the drift or rerun again."
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
    "length": 11
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
  "interpretation": "The repaired chain preserves the raw policy under identity normalization. Sampled targets match the deterministic soft marginal target within the predeclared Monte Carlo tolerance, have positive sampling variance, and the deterministic soft learner achieves lower mean final Bellman residual with statistically non-worse value error and policy quality. Protected-file drift was subsequently audited as harmless/stale: the only flagged protected change was autoresearcher.yaml speed configuration, now... [trimmed]",
  "known_failures": [],
  "metrics": {
    "artifact_validation_status_after_drift_audit": "passed",
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
    "drift_status": "harmless",
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
    "evidence_integrity_verdict": "accepted_evidence",
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
    "protected_file_drift_affected_files": [
      "autoresearcher.yaml"
    ],
    "protected_file_drift_audit": "research/reward_to_gcrl/artifacts/0004/protected_file_drift_audit.json",
    "protected_file_drift_currently_modified": false,
    "protected_file_drift_impact": "harmless for experiment logic/reporting; stale after committed configuration change",
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
    "schema_validation_status_after_drift_audit": "passed",
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


## Evidence Integrity Gate

Protected-file drift was audited after the original 0004 run. The prior guard flagged `autoresearcher.yaml`; the only protected change was the user-requested commenting out of `codex.speed: Fast`, which was committed and pushed before this audit. The audit status is `harmless`: this configuration change affects Codex role invocation preference only and does not affect the 0004 experiment script, environment, transition table, seeds, metrics, schemas, or artifact validation.

Audit artifact: `research/reward_to_gcrl/artifacts/0004/protected_file_drift_audit.json`.

Evidence-integrity verdict: `accepted_evidence` for the repaired nondegenerate tabular gate, subject to the post-audit validation commands listed below.

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
