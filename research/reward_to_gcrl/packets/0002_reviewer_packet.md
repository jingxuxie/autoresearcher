# Reviewer Context: reward_to_gcrl

## Latest plan

# Experiment 0002

## Objective

Rerun the blocked CliffWalking tabular equivalence test using a small local deterministic transition-table implementation with fully audited semantics, then compare exact-DP references, normalized Q-learning, and terminal-only soft successor g_plus learning.

## Hypothesis

For a deterministic 4x12 CliffWalking MDP with declared rewards, reset, cliff, and terminal semantics, the exact soft successor fixed point satisfies F_gplus_star/(1-gamma) = Q_norm_star, and paired tabular soft successor learning induces the same greedy policy as normalized Q-learning up to tie handling.

## Success criteria

- The local CliffWalking environment audit explicitly records grid size, start state, goal state, cliff states, action mapping, off-grid behavior, cliff transition behavior, terminal behavior, raw rewards, normalized rewards, and transition table hash.
- Exact value iteration produces max_abs_error(F_gplus_star/(1-gamma) - Q_norm_star) < 1e-6 for gamma in {0.95, 0.99}.
- Across 10 paired seeds, learned M_plus/(1-gamma) and learned normalized Q values agree within a predeclared tolerance on sufficiently visited non-terminal state-action pairs.
- Greedy policy disagreement between paired learners is below 1 percent on non-terminal non-tie states, with tie states and insufficiently visited states reported separately.
- Evaluation over at least 100 episodes per seed reports raw return, normalized return, steps to goal, cliff-fall count, and success rate for both policies.
- Result JSON contains explicit pass/fail flags for environment audit, exact-DP scaling equivalence, learned value agreement, policy disagreement, and evaluation agreement.

## Failure criteria

- The local transition-table audit is missing or incomplete.
- Exact-DP scaling equivalence fails above 1e-6.
- No paired 10-seed learning metrics are produced.
- Reward normalization or terminal-mask handling is ambiguous.
- True greedy policy disagreement exceeds 5 percent on non-terminal non-tie states after sufficient visitation.
- The experiment adds RiverSwim, FourRooms, auxiliary goals, neural models, sampled baselines, GPU use, or large dependencies before this gate passes.

## Estimated runtime

<= 20 minutes

## Tasks for Codex

- Create research/reward_to_gcrl/artifacts/0002/run_local_cliffwalking_equivalence.py with a local deterministic tabular CliffWalking transition table and no Gymnasium dependency for the environment.
- Write research/reward_to_gcrl/artifacts/0002/environment_audit.json containing the full transition semantics and a transition table hash.
- Implement exact value iteration for normalized Q_star and exact soft F_gplus_star from the same transition table.
- Implement paired tabular normalized Q-learning and terminal-only soft successor learning with matched alpha, epsilon schedule, gamma values, episode budget, and seeds.
- Compute exact-DP scaling error, learned value-scaling error, Bellman residuals, visitation coverage, tie-aware greedy policy disagreement, raw evaluation return, steps to goal, cliff-fall count, and success rate.
- Save research/reward_to_gcrl/results/0002_result.json with raw metrics, exact command, config, artifact paths, and pass/fail flags.
- Save research/reward_to_gcrl/results/0002_summary.md with a compact verdict explaining whether the blocked 0002 gate is now satisfied.

## Required outputs

- `research/reward_to_gcrl/results/0002_result.json`
- `research/reward_to_gcrl/results/0002_summary.md`
- `research/reward_to_gcrl/artifacts/0002/`


## Latest plan JSON

```json
{
  "estimated_runtime_minutes": 20,
  "experiment_id": "0002",
  "failure_criteria": [
    "The local transition-table audit is missing or incomplete.",
    "Exact-DP scaling equivalence fails above 1e-6.",
    "No paired 10-seed learning metrics are produced.",
    "Reward normalization or terminal-mask handling is ambiguous.",
    "True greedy policy disagreement exceeds 5 percent on non-terminal non-tie states after sufficient visitation.",
    "The experiment adds RiverSwim, FourRooms, auxiliary goals, neural models, sampled baselines, GPU use, or large dependencies before this gate passes."
  ],
  "hypothesis": "For a deterministic 4x12 CliffWalking MDP with declared rewards, reset, cliff, and terminal semantics, the exact soft successor fixed point satisfies F_gplus_star/(1-gamma) = Q_norm_star, and paired tabular soft successor learning induces the same greedy policy as normalized Q-learning up to tie handling.",
  "objective": "Rerun the blocked CliffWalking tabular equivalence test using a small local deterministic transition-table implementation with fully audited semantics, then compare exact-DP references, normalized Q-learning, and terminal-only soft successor g_plus learning.",
  "required_outputs": [
    "research/reward_to_gcrl/results/0002_result.json",
    "research/reward_to_gcrl/results/0002_summary.md",
    "research/reward_to_gcrl/artifacts/0002/"
  ],
  "success_criteria": [
    "The local CliffWalking environment audit explicitly records grid size, start state, goal state, cliff states, action mapping, off-grid behavior, cliff transition behavior, terminal behavior, raw rewards, normalized rewards, and transition table hash.",
    "Exact value iteration produces max_abs_error(F_gplus_star/(1-gamma) - Q_norm_star) < 1e-6 for gamma in {0.95, 0.99}.",
    "Across 10 paired seeds, learned M_plus/(1-gamma) and learned normalized Q values agree within a predeclared tolerance on sufficiently visited non-terminal state-action pairs.",
    "Greedy policy disagreement between paired learners is below 1 percent on non-terminal non-tie states, with tie states and insufficiently visited states reported separately.",
    "Evaluation over at least 100 episodes per seed reports raw return, normalized return, steps to goal, cliff-fall count, and success rate for both policies.",
    "Result JSON contains explicit pass/fail flags for environment audit, exact-DP scaling equivalence, learned value agreement, policy disagreement, and evaluation agreement."
  ],
  "tasks_for_codex": [
    "Create research/reward_to_gcrl/artifacts/0002/run_local_cliffwalking_equivalence.py with a local deterministic tabular CliffWalking transition table and no Gymnasium dependency for the environment.",
    "Write research/reward_to_gcrl/artifacts/0002/environment_audit.json containing the full transition semantics and a transition table hash.",
    "Implement exact value iteration for normalized Q_star and exact soft F_gplus_star from the same transition table.",
    "Implement paired tabular normalized Q-learning and terminal-only soft successor learning with matched alpha, epsilon schedule, gamma values, episode budget, and seeds.",
    "Compute exact-DP scaling error, learned value-scaling error, Bellman residuals, visitation coverage, tie-aware greedy policy disagreement, raw evaluation return, steps to goal, cliff-fall count, and success rate.",
    "Save research/reward_to_gcrl/results/0002_result.json with raw metrics, exact command, config, artifact paths, and pass/fail flags.",
    "Save research/reward_to_gcrl/results/0002_summary.md with a compact verdict explaining whether the blocked 0002 gate is now satisfied."
  ]
}
```


## Latest result summary

```json
{
  "_source": "/home/eston/autoresearcher/research/reward_to_gcrl/results/0002_result.json",
  "artifacts": {
    "_type": "list",
    "first_items": [
      "research/reward_to_gcrl/artifacts/0002/run_local_cliffwalking_equivalence.py",
      "research/reward_to_gcrl/artifacts/0002/local_compatibility_check.json",
      "research/reward_to_gcrl/artifacts/0002/environment_audit.json"
    ],
    "length": 9
  },
  "baseline_metrics": {
    "baseline_name": "tabular_normalized_reward_q_learning",
    "evaluation_episodes_per_seed": 100,
    "max_learned_bellman_residual": 99.9999999999978,
    "mean_normalized_return": 200.0,
    "mean_raw_return": -200.0,
    "mean_success_rate": 0.0
  },
  "claim_tested": "For a fully audited local deterministic 4x12 CliffWalking transition table, the terminal-only soft successor g_plus Bellman fixed point and paired tabular learner match normalized-reward Q-learning after division by (1 - gamma).",
  "experiment_id": "0002",
  "interpretation": "The local deterministic CliffWalking table resolves the previous Gymnasium compatibility blocker. Exact DP passes the scaled soft-successor equivalence with max error 9.71198e-10. Paired tabular learners preserve the same values after scaling and have zero tie-aware greedy-policy disagreement on comparable learned states. The raw CliffWalking evaluation is diagnostic: with the declared normalization, the paired policies agree exactly even though the normalized objective can prefer continuing rew... [trimmed]",
  "known_failures": [],
  "metrics": {
    "config": {
      "alpha": 0.5,
      "episodes": 5000,
      "epsilon_end": 0.02,
      "epsilon_start": 0.2,
      "eval_episodes": 100,
      "exact_scaling_tolerance": 1e-06,
      "gammas": {
        "_type": "list",
        "length": 2
      },
      "learned_scaling_tolerance": 1e-08,
      "max_eval_steps": 200,
      "max_train_steps": 200,
      "min_pair_visits": 5,
      "seeds": {
        "_type": "list",
        "length": 10
      },
      "tie_tolerance": 1e-10
    },
    "environment_audit": {
      "cliff_state_count": 10,
      "complete": true,
      "goal_state": {
        "_type": "object",
        "key_count": 3,
        "keys": [
          "col",
          "row",
          "state"
        ]
      },
      "grid_size": {
        "_type": "object",
        "key_count": 2,
        "keys": [
          "cols",
          "rows"
        ]
      },
      "missing_fields": {
        "_type": "list",
        "length": 0
      },
      "start_state": {
        "_type": "object",
        "key_count": 3,
        "keys": [
          "col",
          "row",
          "state"
        ]
      },
      "transition_table_hash": "f6fa1c509349d50f18e13b6309b3f051c6cef9a8fcdab25f1332537f521d40a2",
      "transition_table_record_count": 192
    },
    "exact_dp": {
      "max_abs_error_scaled_f_vs_q": 9.711982329463353e-10,
      "max_policy_disagreement_rate": 0.0,
      "rows": {
        "_type": "list",
        "length": 2
      }
    },
    "paired_learning": {
      "aggregate": {
        "_type": "object",
        "key_count": 21,
        "keys": [
          "gamma_count",
          "max_abs_eval_normalized_return_delta_m_minus_q",
          "max_abs_eval_raw_return_delta_m_minus_q",
          "max_abs_eval_success_rate_delta_m_minus_q",
          "max_abs_scaled_m_minus_q_all_decision",
          "max_abs_scaled_m_minus_q_sufficient",
          "max_learned_q_bellman_residual",
          "max_learned_scaled_m_bellman_residual",
          "max_policy_disagreement_count",
          "max_policy_disagreement_rate",
          "max_policy_insufficient_state_count",
          "max_policy_tie_state_count",
          "mean_m_policy_normalized_return",
          "mean_m_policy_raw_return",
          "mean_m_policy_success_rate",
          "mean_q_policy_normalized_return",
          "mean_q_policy_raw_return",
          "mean_q_policy_success_rate",
          "min_sufficiently_visited_decision_state_action_pairs",
          "run_count"
        ]
      },
      "per_seed_metric_path": "research/reward_to_gcrl/artifacts/0002/paired_learning_metrics.json"
    },
    "pass_flags": {
      "all_gate_criteria_satisfied": true,
      "environment_audit_complete": true,
      "evaluation_agreement_between_paired_policies": true,
      "exact_dp_scaling_equivalence": true,
      "learned_value_agreement": true,
      "no_forbidden_expansions_added": true,
      "paired_10_seed_learning_metrics_produced": true,
      "tie_aware_policy_disagreement_below_1_percent": true
    }
  },
  "next_questions": [
    "Should the next gate test whether an affine or sign-preserving reward transform keeps the raw CliffWalking objective aligned with goal reaching?",
    "After this tabular equivalence gate, should auxiliary real-state successor goals be tested separately as the next source of possible research value?"
  ],
  "status": "completed"
}
```


## Latest summary

# Experiment 0002 Summary

## Verdict

The blocked 0002 gate is **satisfied** for the stated equivalence test.

## Key Metrics

- Transition table hash: `f6fa1c509349d50f18e13b6309b3f051c6cef9a8fcdab25f1332537f521d40a2`
- Exact DP max `abs(F_gplus_star / (1 - gamma) - Q_norm_star)`: `9.71198232946e-10`
- Paired learning runs: `20` across `2` gamma values and `10` seeds
- Learned max scaled value error on sufficiently visited pairs: `5.11590769747e-13`
- Max tie-aware greedy policy disagreement rate: `0`
- Mean raw return, Q policy: `-200`
- Mean raw return, scaled `g_plus` policy: `-200`
- Mean success rate, Q policy: `0`
- Mean success rate, scaled `g_plus` policy: `0`

## Interpretation

The local deterministic CliffWalking table resolves the previous Gymnasium compatibility blocker. Exact DP passes the scaled soft-successor equivalence with max error 9.71198e-10. Paired tabular learners preserve the same values after scaling and have zero tie-aware greedy-policy disagreement on comparable learned states. The raw CliffWalking evaluation is diagnostic: with the declared normalization, the paired policies agree exactly even though the normalized objective can prefer continuing reward over reaching the raw task goal.

The local audit records the grid, start, goal, cliff cells, action mapping, off-grid behavior, cliff reset behavior, terminal behavior, raw rewards, normalized rewards, terminal mask, and full transition table hash. No Gymnasium environment was used for the transition semantics.

## Commands Run

```bash
mkdir -p research/reward_to_gcrl/artifacts/0002 research/reward_to_gcrl/results
conda run -n autoresearcher_reward_to_gcrl python research/reward_to_gcrl/artifacts/0002/run_local_cliffwalking_equivalence.py --check-only
conda run -n autoresearcher_reward_to_gcrl python research/reward_to_gcrl/artifacts/0002/run_local_cliffwalking_equivalence.py
conda run -n autoresearcher_reward_to_gcrl python -m jsonschema -i research/reward_to_gcrl/results/0002_result.json schemas/result.schema.json
conda run -n autoresearcher_reward_to_gcrl python scripts/validate_artifacts.py --repo-root . --json research/reward_to_gcrl/results/0002_result.json --schema schemas/result.schema.json --check-result-artifacts
```

## Artifacts

- `research/reward_to_gcrl/artifacts/0002/run_local_cliffwalking_equivalence.py`
- `research/reward_to_gcrl/artifacts/0002/local_compatibility_check.json`
- `research/reward_to_gcrl/artifacts/0002/environment_audit.json`
- `research/reward_to_gcrl/artifacts/0002/exact_dp_metrics.json`
- `research/reward_to_gcrl/artifacts/0002/exact_value_tables.json`
- `research/reward_to_gcrl/artifacts/0002/paired_learning_metrics.json`
- `research/reward_to_gcrl/artifacts/0002/paired_seed_metrics.csv`
- `research/reward_to_gcrl/artifacts/0002/raw_metrics.json`
- `research/reward_to_gcrl/artifacts/0002/progress.jsonl`


## Full evidence paths

- `research/reward_to_gcrl/results/0002_result.json`
- `research/reward_to_gcrl/results/0002_summary.md`

Inspect the full result JSON only when the compact summary and artifact list are insufficient.


## Artifact paths

- `/home/eston/autoresearcher/research/reward_to_gcrl/artifacts/0001`
- `/home/eston/autoresearcher/research/reward_to_gcrl/artifacts/0002`


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
