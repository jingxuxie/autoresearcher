# Reviewer Context: reward_to_gcrl

## Latest plan

# Experiment 0009

## Objective

Run the first CPU-only NumPy shared-parameter test on tiny FourRooms using a low-rank factorized soft successor-measure model, comparing terminal-only g_plus training against combined g_plus plus real-state auxiliary-goal training under matched limited offline replay.

## Hypothesis

If real-state auxiliary goals provide useful shared representation signal, then under a low-rank bottleneck and adequate replay coverage, combined auxiliary training should reduce g_plus value error and Bellman residual versus terminal-only g_plus training without increasing reward-policy disagreement. If it does not, then auxiliary-goal benefit is not yet supported and should not be claimed.

## Success criteria

- Use only CPU NumPy code on the already-audited tiny FourRooms environment; no PyTorch, JAX, GPU, larger environments, or large dependencies.
- Reuse or verify the 0008 FourRooms transition semantics, reward normalization, terminal masks, goal indexing, and exact tabular references for g_plus and real-state goals.
- Train a genuinely shared low-rank model, such as M_hat(s,a,g) = sigmoid(u_{s,a} dot v_g + b_g) or a documented bounded equivalent, so real-state goals and g_plus share state-action factors.
- Compare at minimum terminal-only g_plus training versus combined g_plus plus real-state auxiliary training on identical replay datasets, seeds, rank, optimizer step budget, target construction, and evaluation protocol.
- Use a small predeclared configuration only, for example rank 4, 10 seeds, one replay budget, and at most one auxiliary weight plus a terminal-only baseline.
- Report replay coverage, visited state-action coverage, goal-label coverage, and whether each seed meets an adequate-coverage threshold before interpreting learning metrics.
- Combined auxiliary training must improve mean g_plus value error or Bellman residual by at least 10 percent on adequate-coverage seeds, or improve one while being statistically indistinguishable on the other, without increasing tie-aware reward-policy disagreement.
- Real-state auxiliary goal predictions must be evaluated against exact references, including mean state-goal value error and a greedy goal-reaching diagnostic, but these are auxiliary diagnostics rather than reward-task success criteria.
- The summary must explicitly label the result as one of: auxiliary_helped_gplus, auxiliary_neutral, negative_transfer, coverage_limited, or optimizer_failed.

## Failure criteria

- The model does not actually share parameters between real-state goals and g_plus.
- The experiment uses independent tabular slices again, which would duplicate 0008 rather than testing shared representation.
- Replay coverage is inadequate and the summary still makes auxiliary-benefit claims.
- Auxiliary training improves real-state goal metrics but worsens g_plus value error, Bellman residual, or reward-policy disagreement without being labeled negative transfer.
- The run sweeps many ranks, losses, auxiliary weights, or optimizers and then selects the best without predeclared criteria.
- The experiment installs neural frameworks, uses GPU, expands to larger environments, or makes publishable auxiliary-goal claims before review.

## Estimated runtime

<= 25 minutes

## Tasks for Codex

- Create research/reward_to_gcrl/artifacts/0009/run_fourrooms_lowrank_auxiliary.py using CPU-only NumPy.
- Write an environment audit that verifies the FourRooms transition table, state indexing, wall/door layout, action mapping, reward normalization, terminal masks, and goal indexing against 0008 where possible.
- Generate a fixed offline replay dataset from a simple non-oracle behavior policy or small mixture of documented non-oracle policies, and save replay coverage diagnostics.
- Implement exact target computation from replay for g_plus and sampled real-state goals, using exact tabular references only for evaluation, not for behavior or training targets beyond normal bootstrapped target construction.
- Implement terminal-only and combined auxiliary low-rank SSM variants with matched initialization seeds, optimizer steps, batch schedule, learning rate, rank, and target-network or fitted-iteration protocol.
- Evaluate g_plus scaled value error, Bellman residual, tie-aware reward-policy disagreement, raw reward-task return/success, real-state goal value error, greedy goal-reaching success, and negative-transfer diagnostics.
- Save research/reward_to_gcrl/results/0009_result.json with raw per-seed metrics, pass/fail flags, exact commands, model configuration, replay coverage, and conservative verdict.
- Save research/reward_to_gcrl/results/0009_summary.md with a short review-oriented interpretation and a recommendation on whether to repeat the low-rank checkpoint, move to a slightly larger sweep, or stop auxiliary-goal claims for now.

## Required outputs

- `research/reward_to_gcrl/results/0009_result.json`
- `research/reward_to_gcrl/results/0009_summary.md`
- `research/reward_to_gcrl/artifacts/0009/`


## Latest plan JSON

```json
{
  "estimated_runtime_minutes": 25,
  "experiment_id": "0009",
  "failure_criteria": [
    "The model does not actually share parameters between real-state goals and g_plus.",
    "The experiment uses independent tabular slices again, which would duplicate 0008 rather than testing shared representation.",
    "Replay coverage is inadequate and the summary still makes auxiliary-benefit claims.",
    "Auxiliary training improves real-state goal metrics but worsens g_plus value error, Bellman residual, or reward-policy disagreement without being labeled negative transfer.",
    "The run sweeps many ranks, losses, auxiliary weights, or optimizers and then selects the best without predeclared criteria.",
    "The experiment installs neural frameworks, uses GPU, expands to larger environments, or makes publishable auxiliary-goal claims before review."
  ],
  "hypothesis": "If real-state auxiliary goals provide useful shared representation signal, then under a low-rank bottleneck and adequate replay coverage, combined auxiliary training should reduce g_plus value error and Bellman residual versus terminal-only g_plus training without increasing reward-policy disagreement. If it does not, then auxiliary-goal benefit is not yet supported and should not be claimed.",
  "objective": "Run the first CPU-only NumPy shared-parameter test on tiny FourRooms using a low-rank factorized soft successor-measure model, comparing terminal-only g_plus training against combined g_plus plus real-state auxiliary-goal training under matched limited offline replay.",
  "required_outputs": [
    "research/reward_to_gcrl/results/0009_result.json",
    "research/reward_to_gcrl/results/0009_summary.md",
    "research/reward_to_gcrl/artifacts/0009/"
  ],
  "success_criteria": [
    "Use only CPU NumPy code on the already-audited tiny FourRooms environment; no PyTorch, JAX, GPU, larger environments, or large dependencies.",
    "Reuse or verify the 0008 FourRooms transition semantics, reward normalization, terminal masks, goal indexing, and exact tabular references for g_plus and real-state goals.",
    "Train a genuinely shared low-rank model, such as M_hat(s,a,g) = sigmoid(u_{s,a} dot v_g + b_g) or a documented bounded equivalent, so real-state goals and g_plus share state-action factors.",
    "Compare at minimum terminal-only g_plus training versus combined g_plus plus real-state auxiliary training on identical replay datasets, seeds, rank, optimizer step budget, target construction, and evaluation protocol.",
    "Use a small predeclared configuration only, for example rank 4, 10 seeds, one replay budget, and at most one auxiliary weight plus a terminal-only baseline.",
    "Report replay coverage, visited state-action coverage, goal-label coverage, and whether each seed meets an adequate-coverage threshold before interpreting learning metrics.",
    "Combined auxiliary training must improve mean g_plus value error or Bellman residual by at least 10 percent on adequate-coverage seeds, or improve one while being statistically indistinguishable on the other, without increasing tie-aware reward-policy disagreement.",
    "Real-state auxiliary goal predictions must be evaluated against exact references, including mean state-goal value error and a greedy goal-reaching diagnostic, but these are auxiliary diagnostics rather than reward-task success criteria.",
    "The summary must explicitly label the result as one of: auxiliary_helped_gplus, auxiliary_neutral, negative_transfer, coverage_limited, or optimizer_failed."
  ],
  "tasks_for_codex": [
    "Create research/reward_to_gcrl/artifacts/0009/run_fourrooms_lowrank_auxiliary.py using CPU-only NumPy.",
    "Write an environment audit that verifies the FourRooms transition table, state indexing, wall/door layout, action mapping, reward normalization, terminal masks, and goal indexing against 0008 where possible.",
    "Generate a fixed offline replay dataset from a simple non-oracle behavior policy or small mixture of documented non-oracle policies, and save replay coverage diagnostics.",
    "Implement exact target computation from replay for g_plus and sampled real-state goals, using exact tabular references only for evaluation, not for behavior or training targets beyond normal bootstrapped target construction.",
    "Implement terminal-only and combined auxiliary low-rank SSM variants with matched initialization seeds, optimizer steps, batch schedule, learning rate, rank, and target-network or fitted-iteration protocol.",
    "Evaluate g_plus scaled value error, Bellman residual, tie-aware reward-policy disagreement, raw reward-task return/success, real-state goal value error, greedy goal-reaching success, and negative-transfer diagnostics.",
    "Save research/reward_to_gcrl/results/0009_result.json with raw per-seed metrics, pass/fail flags, exact commands, model configuration, replay coverage, and conservative verdict.",
    "Save research/reward_to_gcrl/results/0009_summary.md with a short review-oriented interpretation and a recommendation on whether to repeat the low-rank checkpoint, move to a slightly larger sweep, or stop auxiliary-goal claims for now."
  ]
}
```


## Latest result summary

```json
{
  "_source": "/home/eston/autoresearcher/research/reward_to_gcrl/results/0009_result.json",
  "artifacts": {
    "_type": "list",
    "first_items": [
      "research/reward_to_gcrl/artifacts/0009/run_fourrooms_lowrank_auxiliary.py",
      "research/reward_to_gcrl/artifacts/0009/local_compatibility_check.json",
      "research/reward_to_gcrl/artifacts/0009/environment_audit.json"
    ],
    "length": 9
  },
  "baseline_metrics": {
    "baseline_name": "terminal_only_gplus_lowrank",
    "mean_gplus_bellman_residual": 0.0009558486105185331,
    "mean_gplus_scaled_value_error": 0.0731219458562512,
    "mean_reward_success_rate": 0.5384615384615384
  },
  "claim_tested": "A shared rank-4 NumPy low-rank FourRooms successor-measure model trained with real-state auxiliary goals should improve the g_plus reward-success slice versus terminal-only g_plus training under matched adequate offline replay, or the auxiliary benefit should not be claimed.",
  "experiment_id": "0009",
  "interpretation": "Combined auxiliary training worsened a g_plus metric or reward-policy disagreement under adequate replay coverage; auxiliary-goal benefit is not supported.",
  "known_failures": [
    "reward_policy_not_worse",
    "auxiliary_helped_gplus_criterion"
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
        "key_count": 7,
        "keys": [
          "aux_goals_per_transition",
          "auxiliary_weight",
          "batch_size",
          "gamma",
          "optimizer_steps",
          "replay_transitions",
          "seeds"
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
        "key_count": 22,
        "keys": [
          "adequate_coverage_count",
          "coverage_limited_count",
          "mean_bellman_residual_delta_combined_minus_terminal",
          "mean_combined_goal_success_rate",
          "mean_combined_gplus_bellman_residual",
          "mean_combined_gplus_scaled_value_error",
          "mean_combined_real_goal_value_error",
          "mean_combined_reward_success_rate",
          "mean_reward_policy_disagreement_delta",
          "mean_terminal_gplus_bellman_residual",
          "mean_terminal_gplus_scaled_value_error",
          "mean_terminal_reward_success_rate",
          "mean_value_error_delta_combined_minus_terminal",
          "policy_not_worse",
          "relative_bellman_residual_improvement",
          "relative_value_error_improvement",
          "residual_non_worse_or_indistinguishable",
          "run_count",
          "sem_bellman_residual_delta",
          "sem_value_error_delta"
        ]
      },
      "rows": {
        "_type": "list",
        "length": 10
      },
      "verdict": "negative_transfer"
    },
    "pass_flags": {
      "adequate_coverage_all_seeds": true,
      "auxiliary_helped_gplus_criterion": false,
      "cpu_numpy_only": true,
      "environment_audit_complete": true,
      "matched_replay_and_optimizer_schedule": true,
      "real_goal_auxiliary_diagnostics_reported": true,
      "reward_policy_not_worse": false,
      "shared_low_rank_model_used": true,
      "verified_fourrooms_semantics_against_0008": true
    }
  },
  "next_questions": [
    "Should the low-rank checkpoint be repeated with a slightly different optimizer seed or lower learning rate?",
    "If auxiliary remains neutral or negative, should auxiliary-goal claims stop until a reviewed shared-parameter design is available?"
  ],
  "status": "completed"
}
```


## Latest summary

# Experiment 0009 Summary

## Verdict

Low-rank FourRooms auxiliary diagnostic status: **completed**.

Conservative label: **negative_transfer**.

Recommendation: **stop_auxiliary_goal_claims_for_now**.

## Key Metrics

- Adequate-coverage seeds: `10` / `10`
- Terminal-only mean g_plus scaled value error: `0.0731219`
- Combined mean g_plus scaled value error: `16.8939`
- Relative value-error improvement: `-230.037`
- Terminal-only mean Bellman residual: `0.000955849`
- Combined mean Bellman residual: `0.0364139`
- Relative Bellman-residual improvement: `-37.0959`
- Mean reward-policy disagreement delta: `0.526337`
- Combined mean real-state goal value error: `0.919111`
- Combined mean goal-reaching success rate: `0.00371795`

## Interpretation

Combined auxiliary training worsened a g_plus metric or reward-policy disagreement under adequate replay coverage; auxiliary-goal benefit is not supported.

This is a single predeclared rank-4 NumPy checkpoint. It does not make publishable auxiliary-goal claims.

## Commands Run

```bash
mkdir -p research/reward_to_gcrl/artifacts/0009 research/reward_to_gcrl/results
conda run -n autoresearcher_reward_to_gcrl python --version
conda run -n autoresearcher_reward_to_gcrl python -m py_compile research/reward_to_gcrl/artifacts/0009/run_fourrooms_lowrank_auxiliary.py
conda run -n autoresearcher_reward_to_gcrl python research/reward_to_gcrl/artifacts/0009/run_fourrooms_lowrank_auxiliary.py --check-only
conda run -n autoresearcher_reward_to_gcrl python research/reward_to_gcrl/artifacts/0009/run_fourrooms_lowrank_auxiliary.py
conda run -n autoresearcher_reward_to_gcrl python -m jsonschema -i research/reward_to_gcrl/results/0009_result.json schemas/result.schema.json
conda run -n autoresearcher_reward_to_gcrl python scripts/validate_artifacts.py --repo-root . --json research/reward_to_gcrl/results/0009_result.json --schema schemas/result.schema.json --check-result-artifacts
```

## Artifacts

- `research/reward_to_gcrl/artifacts/0009/run_fourrooms_lowrank_auxiliary.py`
- `research/reward_to_gcrl/artifacts/0009/local_compatibility_check.json`
- `research/reward_to_gcrl/artifacts/0009/environment_audit.json`
- `research/reward_to_gcrl/artifacts/0009/exact_dp_references.json`
- `research/reward_to_gcrl/artifacts/0009/per_seed_metrics.json`
- `research/reward_to_gcrl/artifacts/0009/per_seed_summary.csv`
- `research/reward_to_gcrl/artifacts/0009/replay_datasets.npz`
- `research/reward_to_gcrl/artifacts/0009/raw_metrics.json`
- `research/reward_to_gcrl/artifacts/0009/progress.jsonl`


## Full evidence paths

- `research/reward_to_gcrl/results/0009_result.json`
- `research/reward_to_gcrl/results/0009_summary.md`

Inspect the full result JSON only when the compact summary and artifact list are insufficient.


## Artifact paths

- `/home/eston/autoresearcher/research/reward_to_gcrl/artifacts/0005`
- `/home/eston/autoresearcher/research/reward_to_gcrl/artifacts/0006`
- `/home/eston/autoresearcher/research/reward_to_gcrl/artifacts/0007`
- `/home/eston/autoresearcher/research/reward_to_gcrl/artifacts/0008`
- `/home/eston/autoresearcher/research/reward_to_gcrl/artifacts/0009`


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
