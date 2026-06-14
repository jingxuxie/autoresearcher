# Reviewer Context: reward_to_gcrl

## Latest plan

# Experiment 0010

## Objective

Diagnose the 0009 negative transfer in the shared low-rank FourRooms SSM by testing whether auxiliary collapse is caused by loss-scaling or optimization imbalance, while keeping the run CPU-only, NumPy-only, tiny, and predeclared.

## Hypothesis

If 0009 failed mainly because auxiliary real-state losses overwhelmed or destabilized the g_plus head, then a loss-balanced or staged auxiliary variant should reduce negative transfer and approach or improve terminal-only g_plus metrics. If these controlled variants still fail, auxiliary real-state goals are unsupported for this low-rank architecture and should be paused.

## Success criteria

- Use the same audited tiny FourRooms environment, transition hash, replay construction, exact references, rank 4 model form, and CPU-only NumPy implementation family as 0009.
- Run only a tightly predeclared diagnostic set: terminal-only reproduction, original combined auxiliary lambda=1 reproduction, loss-balanced combined auxiliary, and staged real-goal pretrain followed by g_plus fine-tuning.
- Report per-component g_plus and auxiliary losses, gradient norms on shared u_sa factors, target-value scales, and whether auxiliary gradients dominate terminal gradients.
- The terminal-only and original combined reproduction should qualitatively match 0009 within a reasonable tolerance; otherwise the diagnostic must be labeled reproduction_failed.
- A repaired auxiliary variant counts as promising only if it improves mean g_plus Bellman residual or mean scaled value error by at least 10 percent over terminal-only, or is statistically indistinguishable on both while improving real-state goal diagnostics, without increasing reward-policy disagreement.
- If no repaired auxiliary variant matches terminal-only g_plus value error and Bellman residual, the verdict must be auxiliary_unsupported_for_lowrank rather than tuned_failure.
- No PyTorch, JAX, GPU, larger environment, broad sweep, or publishable auxiliary-goal claim is allowed before review.

## Failure criteria

- The experiment tries more than the predeclared small set of diagnostic variants.
- The original 0009 negative-transfer result cannot be reproduced and the discrepancy is not explained.
- The result omits gradient-norm or loss-scale diagnostics, leaving the cause of collapse ambiguous.
- A variant improves real-state goal metrics while worsening g_plus value error, Bellman residual, or reward-policy disagreement and is not labeled negative transfer.
- The summary claims auxiliary-goal benefit without beating or matching terminal-only g_plus metrics under the predeclared criteria.
- The run uses neural frameworks, GPU, larger environments, or expensive hyperparameter sweeps.

## Estimated runtime

<= 25 minutes

## Tasks for Codex

- Create research/reward_to_gcrl/artifacts/0010/run_fourrooms_lowrank_aux_diagnostic.py by minimally extending the 0009 script.
- Reuse and verify the 0008/0009 FourRooms environment audit, transition hash, goal indexing, reward normalization, terminal masks, replay behavior, and exact references.
- Implement four predeclared variants: terminal_only, combined_lambda_1_reproduction, combined_loss_balanced, and staged_real_goal_pretrain_then_gplus_finetune.
- For each variant, run the same 10 seeds, replay budget, rank, optimizer family, and evaluation protocol unless a difference is explicitly part of the staged diagnostic.
- Log per-step or checkpointed g_plus loss, auxiliary loss, shared-factor gradient norms, head-specific gradient norms, value scales, Bellman residual, value error, policy disagreement, reward success, and real-goal diagnostics.
- Save raw per-seed metrics and aggregate deltas versus terminal-only and original combined auxiliary.
- Write research/reward_to_gcrl/results/0010_result.json with exact commands, artifacts, pass/fail flags, reproduction status, gradient-scale diagnostics, and conservative verdict.
- Write research/reward_to_gcrl/results/0010_summary.md recommending one of: proceed_to_tiny_reviewed_aux_followup, pause_auxiliary_thread, or write_negative_result.

## Required outputs

- `research/reward_to_gcrl/results/0010_result.json`
- `research/reward_to_gcrl/results/0010_summary.md`
- `research/reward_to_gcrl/artifacts/0010/`


## Latest plan JSON

```json
{
  "estimated_runtime_minutes": 25,
  "experiment_id": "0010",
  "failure_criteria": [
    "The experiment tries more than the predeclared small set of diagnostic variants.",
    "The original 0009 negative-transfer result cannot be reproduced and the discrepancy is not explained.",
    "The result omits gradient-norm or loss-scale diagnostics, leaving the cause of collapse ambiguous.",
    "A variant improves real-state goal metrics while worsening g_plus value error, Bellman residual, or reward-policy disagreement and is not labeled negative transfer.",
    "The summary claims auxiliary-goal benefit without beating or matching terminal-only g_plus metrics under the predeclared criteria.",
    "The run uses neural frameworks, GPU, larger environments, or expensive hyperparameter sweeps."
  ],
  "hypothesis": "If 0009 failed mainly because auxiliary real-state losses overwhelmed or destabilized the g_plus head, then a loss-balanced or staged auxiliary variant should reduce negative transfer and approach or improve terminal-only g_plus metrics. If these controlled variants still fail, auxiliary real-state goals are unsupported for this low-rank architecture and should be paused.",
  "objective": "Diagnose the 0009 negative transfer in the shared low-rank FourRooms SSM by testing whether auxiliary collapse is caused by loss-scaling or optimization imbalance, while keeping the run CPU-only, NumPy-only, tiny, and predeclared.",
  "required_outputs": [
    "research/reward_to_gcrl/results/0010_result.json",
    "research/reward_to_gcrl/results/0010_summary.md",
    "research/reward_to_gcrl/artifacts/0010/"
  ],
  "success_criteria": [
    "Use the same audited tiny FourRooms environment, transition hash, replay construction, exact references, rank 4 model form, and CPU-only NumPy implementation family as 0009.",
    "Run only a tightly predeclared diagnostic set: terminal-only reproduction, original combined auxiliary lambda=1 reproduction, loss-balanced combined auxiliary, and staged real-goal pretrain followed by g_plus fine-tuning.",
    "Report per-component g_plus and auxiliary losses, gradient norms on shared u_sa factors, target-value scales, and whether auxiliary gradients dominate terminal gradients.",
    "The terminal-only and original combined reproduction should qualitatively match 0009 within a reasonable tolerance; otherwise the diagnostic must be labeled reproduction_failed.",
    "A repaired auxiliary variant counts as promising only if it improves mean g_plus Bellman residual or mean scaled value error by at least 10 percent over terminal-only, or is statistically indistinguishable on both while improving real-state goal diagnostics, without increasing reward-policy disagreement.",
    "If no repaired auxiliary variant matches terminal-only g_plus value error and Bellman residual, the verdict must be auxiliary_unsupported_for_lowrank rather than tuned_failure.",
    "No PyTorch, JAX, GPU, larger environment, broad sweep, or publishable auxiliary-goal claim is allowed before review."
  ],
  "tasks_for_codex": [
    "Create research/reward_to_gcrl/artifacts/0010/run_fourrooms_lowrank_aux_diagnostic.py by minimally extending the 0009 script.",
    "Reuse and verify the 0008/0009 FourRooms environment audit, transition hash, goal indexing, reward normalization, terminal masks, replay behavior, and exact references.",
    "Implement four predeclared variants: terminal_only, combined_lambda_1_reproduction, combined_loss_balanced, and staged_real_goal_pretrain_then_gplus_finetune.",
    "For each variant, run the same 10 seeds, replay budget, rank, optimizer family, and evaluation protocol unless a difference is explicitly part of the staged diagnostic.",
    "Log per-step or checkpointed g_plus loss, auxiliary loss, shared-factor gradient norms, head-specific gradient norms, value scales, Bellman residual, value error, policy disagreement, reward success, and real-goal diagnostics.",
    "Save raw per-seed metrics and aggregate deltas versus terminal-only and original combined auxiliary.",
    "Write research/reward_to_gcrl/results/0010_result.json with exact commands, artifacts, pass/fail flags, reproduction status, gradient-scale diagnostics, and conservative verdict.",
    "Write research/reward_to_gcrl/results/0010_summary.md recommending one of: proceed_to_tiny_reviewed_aux_followup, pause_auxiliary_thread, or write_negative_result."
  ]
}
```


## Latest result summary

```json
{
  "_source": "/home/eston/autoresearcher/research/reward_to_gcrl/results/0010_result.json",
  "artifacts": {
    "_type": "list",
    "first_items": [
      "research/reward_to_gcrl/artifacts/0010/run_fourrooms_lowrank_aux_diagnostic.py",
      "research/reward_to_gcrl/artifacts/0010/local_compatibility_check.json",
      "research/reward_to_gcrl/artifacts/0010/environment_audit.json"
    ],
    "length": 9
  },
  "baseline_metrics": {
    "baseline_name": "terminal_only_gplus_lowrank",
    "mean_gplus_bellman_residual": 0.0009558486105185331,
    "mean_gplus_scaled_value_error": 0.0731219458562512,
    "mean_reward_success_rate": 0.5384615384615384
  },
  "claim_tested": "The 0009 low-rank FourRooms negative transfer may be caused by loss-scaling or optimization imbalance; loss-balanced or staged auxiliary variants should reduce transfer harm if that diagnosis is correct.",
  "experiment_id": "0010",
  "interpretation": "Original negative transfer reproduced, and neither repaired variant matched terminal-only on g_plus value error and Bellman residual. Auxiliary real-state goals should be paused for this low-rank architecture.",
  "known_failures": [
    "repaired_variant_promising"
  ],
  "metrics": {
    "config": {
      "coverage_thresholds": {
        "_type": "object",
        "key_count": 4,
        "keys": [
          "goal_label_fraction",
          "min_state_action_count",
          "reward_event_count",
          "visited_state_action_fraction"
        ]
      },
      "gamma": 0.95,
      "improvement_threshold": 0.1,
      "indistinguishable_z": 1.96,
      "model": {
        "_type": "object",
        "key_count": 5,
        "keys": [
          "form",
          "learning_rate",
          "optimizer",
          "rank",
          "shared_parameters"
        ]
      },
      "predeclared_variants": {
        "_type": "list",
        "length": 4
      },
      "rank": 4,
      "replay_behavior": {
        "_type": "object",
        "key_count": 4,
        "keys": [
          "description",
          "name",
          "uses_exact_q_or_dp",
          "uses_reward_optimal_preferences"
        ]
      },
      "seeds": {
        "_type": "list",
        "length": 10
      },
      "training_config": {
        "_type": "object",
        "key_count": 10,
        "keys": [
          "aux_goals_per_transition",
          "auxiliary_weight",
          "batch_size",
          "diagnostic_variants",
          "gamma",
          "loss_balance_clip",
          "optimizer_steps",
          "replay_transitions",
          "seeds",
          "staged_pretrain_steps"
        ]
      }
    },
    "environment_audit": {
      "complete": true,
      "goal_indexing": {
        "_type": "object",
        "key_count": 3,
        "keys": [
          "g_plus_index",
          "goal_count_total",
          "real_state_goal_indices"
        ]
      },
      "missing_fields": {
        "_type": "list",
        "length": 0
      },
      "reward_normalization": {
        "_type": "object",
        "key_count": 4,
        "keys": [
          "affine_offset",
          "affine_scale",
          "normalized_reward",
          "raw_rewards_in_[0,1]"
        ]
      },
      "terminal_masks": {
        "_type": "object",
        "key_count": 2,
        "keys": [
          "g_plus_slice",
          "real_state_goal_slice"
        ]
      },
      "transition_table_hash": "83e1f22232f65efd7c194f0e75ee92546b395520656f2336819472ef1b95d3de",
      "verified_against_0008_where_available": {
        "_type": "object",
        "key_count": 3,
        "keys": [
          "audit_path",
          "transition_hash_0008",
          "transition_hash_matches_0008"
        ]
      },
      "verified_against_0009_where_available": {
        "_type": "object",
        "key_count": 7,
        "keys": [
          "aggregate",
          "rank",
          "replay_transitions",
          "result_path",
          "status",
          "transition_hash_matches",
          "verdict"
        ]
      }
    },
    "exact_dp": {
      "gamma": 0.95,
      "goal_iterations": 14,
      "gplus_iterations": 14,
      "max_abs_scaled_gplus_minus_q_norm": 1.1102230246251565e-16,
      "q_iterations": 14
    },
    "lowrank_auxiliary": {
      "aggregate": {
        "_type": "object",
        "key_count": 11,
        "keys": [
          "adequate_coverage_count",
          "any_repaired_variant_matches_terminal",
          "any_repaired_variant_promising",
          "auxiliary_gradient_dominance",
          "coverage_limited_count",
          "deltas_vs_terminal",
          "repaired_variant_names",
          "reproduction_checks",
          "run_count",
          "variant_summaries",
          "verdict"
        ]
      },
      "rows": {
        "_type": "list",
        "length": 10
      },
      "verdict": "auxiliary_unsupported_for_lowrank"
    },
    "pass_flags": {
      "adequate_coverage_all_seeds": true,
      "cpu_numpy_only": true,
      "environment_audit_complete": true,
      "gradient_norm_and_loss_scale_diagnostics_reported": true,
      "matched_replay_and_optimizer_schedule": true,
      "no_unapproved_variant_sweep": true,
      "original_0009_reproduced": true,
      "real_goal_auxiliary_diagnostics_reported": true,
      "repaired_variant_promising": false,
      "shared_low_rank_model_used": true,
      "verified_fourrooms_config_against_0009": true,
      "verified_fourrooms_semantics_against_0008": true
    }
  },
  "next_questions": [
    "Should the auxiliary thread be paused for this low-rank architecture and written up as a negative result?",
    "Would a reviewed architecture with shared state-action generalization, not just shared goal factors, be a better next test?"
  ],
  "status": "completed"
}
```


## Latest summary

# Experiment 0010 Summary

## Verdict

Low-rank FourRooms loss-scale diagnostic status: **completed**.

Conservative label: **auxiliary_unsupported_for_lowrank**.

Recommendation: **write_negative_result**.

## Key Metrics

- Adequate-coverage seeds: `10` / `10`
- Original 0009 reproduction: `True`
- Any repaired variant promising: `False`
- Any repaired variant matches terminal g_plus metrics: `False`

| Variant | g_plus value error | Bellman residual | Policy disagreement | Real-goal value error | Mean aux/g_plus U-grad ratio |
| --- | ---: | ---: | ---: | ---: | --- |
| terminal_only | 0.0731219 | 0.000955849 | 0.140909 | 0.0183195 | 0.0 |
| combined_lambda_1_reproduction | 16.8939 | 0.0364139 | 0.667246 | 0.919111 | 4.3423814050417855 |
| combined_loss_balanced | 7.37704 | 0.0179085 | 0.650823 | 0.767482 | 451.2730071367794 |
| staged_real_goal_pretrain_then_gplus_finetune | 18.5798 | 0.0508149 | 0.652206 | 0.897855 | 0.0 |

## Interpretation

Original negative transfer reproduced, and neither repaired variant matched terminal-only on g_plus value error and Bellman residual. Auxiliary real-state goals should be paused for this low-rank architecture.

This is a tightly predeclared CPU NumPy diagnostic. It does not make publishable auxiliary-goal claims.

## Commands Run

```bash
mkdir -p research/reward_to_gcrl/artifacts/0010 research/reward_to_gcrl/results
conda run -n autoresearcher_reward_to_gcrl python --version
conda run -n autoresearcher_reward_to_gcrl python -m py_compile research/reward_to_gcrl/artifacts/0010/run_fourrooms_lowrank_aux_diagnostic.py
conda run -n autoresearcher_reward_to_gcrl python research/reward_to_gcrl/artifacts/0010/run_fourrooms_lowrank_aux_diagnostic.py --check-only
conda run -n autoresearcher_reward_to_gcrl python research/reward_to_gcrl/artifacts/0010/run_fourrooms_lowrank_aux_diagnostic.py
conda run -n autoresearcher_reward_to_gcrl python -m jsonschema -i research/reward_to_gcrl/results/0010_result.json schemas/result.schema.json
conda run -n autoresearcher_reward_to_gcrl python scripts/validate_artifacts.py --repo-root . --json research/reward_to_gcrl/results/0010_result.json --schema schemas/result.schema.json --check-result-artifacts
```

## Artifacts

- `research/reward_to_gcrl/artifacts/0010/run_fourrooms_lowrank_aux_diagnostic.py`
- `research/reward_to_gcrl/artifacts/0010/local_compatibility_check.json`
- `research/reward_to_gcrl/artifacts/0010/environment_audit.json`
- `research/reward_to_gcrl/artifacts/0010/exact_dp_references.json`
- `research/reward_to_gcrl/artifacts/0010/per_seed_metrics.json`
- `research/reward_to_gcrl/artifacts/0010/per_seed_summary.csv`
- `research/reward_to_gcrl/artifacts/0010/replay_datasets.npz`
- `research/reward_to_gcrl/artifacts/0010/raw_metrics.json`
- `research/reward_to_gcrl/artifacts/0010/progress.jsonl`


## Full evidence paths

- `research/reward_to_gcrl/results/0010_result.json`
- `research/reward_to_gcrl/results/0010_summary.md`

Inspect the full result JSON only when the compact summary and artifact list are insufficient.


## Artifact paths

- `/home/eston/autoresearcher/research/reward_to_gcrl/artifacts/0006`
- `/home/eston/autoresearcher/research/reward_to_gcrl/artifacts/0007`
- `/home/eston/autoresearcher/research/reward_to_gcrl/artifacts/0008`
- `/home/eston/autoresearcher/research/reward_to_gcrl/artifacts/0009`
- `/home/eston/autoresearcher/research/reward_to_gcrl/artifacts/0010`


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
