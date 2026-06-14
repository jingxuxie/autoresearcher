# Reviewer Context: reward_to_gcrl

## Latest plan

# Experiment 0008

## Objective

Run a CPU-only tabular vector successor-measure sanity check with real-state goals plus g_plus on a tiny deterministic FourRooms grid.

## Hypothesis

For a tabular vector SSM with independent goal slices, adding real-state goals should learn correct state-goal reachability maps while leaving the g_plus reward-success slice numerically equivalent to the terminal-only soft learner. Any degradation of the g_plus policy or value slice would indicate an implementation, indexing, reward-normalization, or terminal-mask bug rather than a research effect.

## Success criteria

- Creates research/reward_to_gcrl/results/0008_result.json and research/reward_to_gcrl/results/0008_summary.md.
- Creates reproducible artifacts under research/reward_to_gcrl/artifacts/0008/.
- Uses only CPU tabular methods on a tiny deterministic FourRooms grid; no neural models, low-rank factorization, large environments, GPU-dependent work, large downloads, or expensive training.
- Predeclares and saves grid layout, wall cells, doorway cells, state indexing, action mapping, reward task, reward normalization, terminal masks, gamma values, update procedure, seeds if stochastic, and exact commands run.
- Solves exact DP references for the terminal-only g_plus slice and for real-state goal slices, and reports max_abs_error for learned vector slices versus exact references.
- Reports max_abs(M_vector[:,:,g_plus] - M_terminal_only), max_abs(M_vector[:,:,g_plus]/(1-gamma) - Q_norm), and reward-policy disagreement versus terminal-only soft or exact DP.
- For sampled real-state goals or all selected goals, reports greedy goal-reaching success rate, mean shortest-path distance reduction, policy disagreement versus exact goal policies, and reachability heatmap/arrow artifacts.
- Passes only if the g_plus slice matches terminal-only soft within a predeclared tolerance, reward-policy disagreement is zero or only due to ties, and real-state goal slices achieve high reachability accuracy on non-wall reachable goals.

## Failure criteria

- Missing, invalid, or schema-incompatible result JSON or summary markdown.
- Exact commands, raw metrics, artifact paths, environment audit, reward normalization, goal indexing, or terminal masks are omitted.
- The vector update couples goals or changes the g_plus slice relative to terminal-only soft beyond the predeclared tolerance.
- Real-state goal diagnostics are only visual/prose and omit exact value error or goal-reaching metrics.
- The experiment claims auxiliary-goal reward improvement in tabular mode without shared parameters.
- The executor adds neural approximation, low-rank factorization, sampled augmented baselines, larger environments, large downloads, GPU-dependent work, or long training before this tabular vector sanity gate is complete.

## Estimated runtime

<= 25 minutes

## Tasks for Codex

- Implement a standalone diagnostic script under research/reward_to_gcrl/artifacts/0008/ defining a tiny deterministic FourRooms transition table with audited state indexing, walls, doorways, actions, rewards, and terminals.
- Implement terminal-only soft M_plus and vector M[s,a,g] with real-state goals 0..n_states-1 and artificial g_plus = n_states using the prototype update immediate[s_next] += (1-gamma) and immediate[g_plus] += (1-gamma)*r_bar.
- Compute exact DP references for Q_norm, terminal-only soft g_plus, and real-state goal reachability slices for gamma values such as 0.95 and 0.99.
- Run small deterministic full-sweep tabular updates or a fixed logged transition stream to convergence within the 30-minute budget.
- Compute g_plus equivalence metrics, reward-policy disagreement, real-state goal value errors, greedy goal-reaching success rates, shortest-path distance diagnostics, and tie counts.
- Save raw per-goal metrics, aggregate metrics, environment audit, exact DP references, and reachability heatmap/arrow data under research/reward_to_gcrl/artifacts/0008/.
- Validate the result JSON with schemas/result.schema.json and validate declared artifacts with scripts/validate_artifacts.py.

## Required outputs

- `research/reward_to_gcrl/results/0008_result.json`
- `research/reward_to_gcrl/results/0008_summary.md`
- `research/reward_to_gcrl/artifacts/0008/`


## Latest plan JSON

```json
{
  "estimated_runtime_minutes": 25,
  "experiment_id": "0008",
  "failure_criteria": [
    "Missing, invalid, or schema-incompatible result JSON or summary markdown.",
    "Exact commands, raw metrics, artifact paths, environment audit, reward normalization, goal indexing, or terminal masks are omitted.",
    "The vector update couples goals or changes the g_plus slice relative to terminal-only soft beyond the predeclared tolerance.",
    "Real-state goal diagnostics are only visual/prose and omit exact value error or goal-reaching metrics.",
    "The experiment claims auxiliary-goal reward improvement in tabular mode without shared parameters.",
    "The executor adds neural approximation, low-rank factorization, sampled augmented baselines, larger environments, large downloads, GPU-dependent work, or long training before this tabular vector sanity gate is complete."
  ],
  "hypothesis": "For a tabular vector SSM with independent goal slices, adding real-state goals should learn correct state-goal reachability maps while leaving the g_plus reward-success slice numerically equivalent to the terminal-only soft learner. Any degradation of the g_plus policy or value slice would indicate an implementation, indexing, reward-normalization, or terminal-mask bug rather than a research effect.",
  "objective": "Run a CPU-only tabular vector successor-measure sanity check with real-state goals plus g_plus on a tiny deterministic FourRooms grid.",
  "required_outputs": [
    "research/reward_to_gcrl/results/0008_result.json",
    "research/reward_to_gcrl/results/0008_summary.md",
    "research/reward_to_gcrl/artifacts/0008/"
  ],
  "success_criteria": [
    "Creates research/reward_to_gcrl/results/0008_result.json and research/reward_to_gcrl/results/0008_summary.md.",
    "Creates reproducible artifacts under research/reward_to_gcrl/artifacts/0008/.",
    "Uses only CPU tabular methods on a tiny deterministic FourRooms grid; no neural models, low-rank factorization, large environments, GPU-dependent work, large downloads, or expensive training.",
    "Predeclares and saves grid layout, wall cells, doorway cells, state indexing, action mapping, reward task, reward normalization, terminal masks, gamma values, update procedure, seeds if stochastic, and exact commands run.",
    "Solves exact DP references for the terminal-only g_plus slice and for real-state goal slices, and reports max_abs_error for learned vector slices versus exact references.",
    "Reports max_abs(M_vector[:,:,g_plus] - M_terminal_only), max_abs(M_vector[:,:,g_plus]/(1-gamma) - Q_norm), and reward-policy disagreement versus terminal-only soft or exact DP.",
    "For sampled real-state goals or all selected goals, reports greedy goal-reaching success rate, mean shortest-path distance reduction, policy disagreement versus exact goal policies, and reachability heatmap/arrow artifacts.",
    "Passes only if the g_plus slice matches terminal-only soft within a predeclared tolerance, reward-policy disagreement is zero or only due to ties, and real-state goal slices achieve high reachability accuracy on non-wall reachable goals."
  ],
  "tasks_for_codex": [
    "Implement a standalone diagnostic script under research/reward_to_gcrl/artifacts/0008/ defining a tiny deterministic FourRooms transition table with audited state indexing, walls, doorways, actions, rewards, and terminals.",
    "Implement terminal-only soft M_plus and vector M[s,a,g] with real-state goals 0..n_states-1 and artificial g_plus = n_states using the prototype update immediate[s_next] += (1-gamma) and immediate[g_plus] += (1-gamma)*r_bar.",
    "Compute exact DP references for Q_norm, terminal-only soft g_plus, and real-state goal reachability slices for gamma values such as 0.95 and 0.99.",
    "Run small deterministic full-sweep tabular updates or a fixed logged transition stream to convergence within the 30-minute budget.",
    "Compute g_plus equivalence metrics, reward-policy disagreement, real-state goal value errors, greedy goal-reaching success rates, shortest-path distance diagnostics, and tie counts.",
    "Save raw per-goal metrics, aggregate metrics, environment audit, exact DP references, and reachability heatmap/arrow data under research/reward_to_gcrl/artifacts/0008/.",
    "Validate the result JSON with schemas/result.schema.json and validate declared artifacts with scripts/validate_artifacts.py."
  ]
}
```


## Latest result summary

```json
{
  "_source": "/home/eston/autoresearcher/research/reward_to_gcrl/results/0008_result.json",
  "artifacts": {
    "_type": "list",
    "first_items": [
      "research/reward_to_gcrl/artifacts/0008/run_fourrooms_vector_ssm.py",
      "research/reward_to_gcrl/artifacts/0008/local_compatibility_check.json",
      "research/reward_to_gcrl/artifacts/0008/environment_audit.json"
    ],
    "length": 11
  },
  "baseline_metrics": {
    "baseline_name": "terminal_only_soft_gplus",
    "max_abs_terminal_only_scaled_minus_q_norm": 1.1102230246251565e-16,
    "max_reward_policy_disagreement_vs_exact": 0.0
  },
  "claim_tested": "Adding real-state goal slices to a tabular vector successor measure should leave the g_plus reward-success slice equivalent to the terminal-only soft learner while learning correct real-state goal reachability maps.",
  "experiment_id": "0008",
  "interpretation": "The vector SSM slices are numerically independent in this tabular FourRooms check: the g_plus slice matches terminal-only soft learning, scaled g_plus matches normalized Q, and real-state goal slices match exact reachability references with successful greedy goal reaching.",
  "known_failures": [],
  "metrics": {
    "config": {
      "equivalence_tolerance": 1e-10,
      "gammas": {
        "_type": "list",
        "length": 2
      },
      "goal_success_threshold": 0.99,
      "grid_shape": {
        "_type": "list",
        "length": 2
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
      "update_procedure": {
        "_type": "object",
        "key_count": 6,
        "keys": [
          "g_plus_immediate",
          "goal_coupling",
          "max_iterations",
          "method",
          "real_goal_immediate",
          "tolerance"
        ]
      },
      "value_error_tolerance": 1e-10
    },
    "environment_audit": {
      "complete": true,
      "doorway_cells": {
        "_type": "list",
        "length": 4
      },
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
      "open_cell_count": 40,
      "reward_task": {
        "_type": "object",
        "key_count": 4,
        "keys": [
          "raw_reward",
          "reward_goal_cell",
          "reward_goal_state",
          "terminal_mask"
        ]
      },
      "transition_table_hash": "83e1f22232f65efd7c194f0e75ee92546b395520656f2336819472ef1b95d3de",
      "wall_cells": {
        "_type": "list",
        "length": 9
      }
    },
    "exact_dp": {
      "rows": {
        "_type": "list",
        "length": 2
      },
      "scaled_gplus_matches_q_norm": true
    },
    "pass_flags": {
      "cpu_tabular_tiny_fourrooms_only": true,
      "environment_audit_complete": true,
      "exact_dp_references_computed": true,
      "goal_policy_disagreement_zero_or_ties": true,
      "heatmap_arrow_artifacts_saved": true,
      "real_goal_success_rate_high": true,
      "real_goal_value_error_within_tolerance": true,
      "reward_policy_disagreement_zero_or_ties": true,
      "vector_gplus_matches_terminal_only": true,
      "vector_gplus_scaled_matches_q_norm": true
    },
    "vector_ssm": {
      "aggregate": {
        "_type": "object",
        "key_count": 12,
        "keys": [
          "gamma_count",
          "max_abs_real_goal_value_error",
          "max_abs_terminal_only_scaled_minus_q_norm",
          "max_abs_vector_gplus_minus_terminal_only",
          "max_abs_vector_gplus_scaled_minus_q_norm",
          "max_goal_policy_disagreement_rate_vs_exact",
          "max_reward_policy_disagreement_vs_exact",
          "max_reward_policy_disagreement_vs_terminal_only",
          "mean_abs_real_goal_value_error",
          "mean_first_step_shortest_path_distance_reduction",
          "mean_goal_success_rate",
          "min_goal_success_rate"
        ]
      },
      "rows": {
        "_type": "list",
        "length": 2
      }
    }
  },
  "next_questions": [
    "Should the next tabular check add shared parameters or low-rank coupling after this independent-slice gate?",
    "Which FourRooms goal subset should be used first when moving beyond full tabular exact backups?"
  ],
  "status": "completed"
}
```


## Latest summary

# Experiment 0008 Summary

## Verdict

FourRooms vector SSM sanity check status: **completed**.

## Key Metrics

- Gamma values: `[0.95, 0.99]`
- Open states: `40`
- Goal slices: `41`
- Max `M_vector[:,:,g_plus] - M_terminal_only`: `0`
- Max `M_vector[:,:,g_plus]/(1-gamma) - Q_norm`: `1.11022e-16`
- Max real-state goal value error: `0`
- Mean real-state goal value error: `0`
- Min greedy goal success rate: `1`
- Mean first-step shortest-path distance reduction: `1`
- Max reward-policy disagreement: `0`

## Interpretation

The vector SSM slices are numerically independent in this tabular FourRooms check: the g_plus slice matches terminal-only soft learning, scaled g_plus matches normalized Q, and real-state goal slices match exact reachability references with successful greedy goal reaching.

This is an independent-slice tabular sanity check only. It does not claim auxiliary-goal reward improvement without shared parameters.

## Commands Run

```bash
mkdir -p research/reward_to_gcrl/artifacts/0008 research/reward_to_gcrl/results
conda run -n autoresearcher_reward_to_gcrl python --version
conda run -n autoresearcher_reward_to_gcrl python -m py_compile research/reward_to_gcrl/artifacts/0008/run_fourrooms_vector_ssm.py
conda run -n autoresearcher_reward_to_gcrl python research/reward_to_gcrl/artifacts/0008/run_fourrooms_vector_ssm.py --check-only
conda run -n autoresearcher_reward_to_gcrl python research/reward_to_gcrl/artifacts/0008/run_fourrooms_vector_ssm.py
conda run -n autoresearcher_reward_to_gcrl python -m jsonschema -i research/reward_to_gcrl/results/0008_result.json schemas/result.schema.json
conda run -n autoresearcher_reward_to_gcrl python scripts/validate_artifacts.py --repo-root . --json research/reward_to_gcrl/results/0008_result.json --schema schemas/result.schema.json --check-result-artifacts
```

## Artifacts

- `research/reward_to_gcrl/artifacts/0008/run_fourrooms_vector_ssm.py`
- `research/reward_to_gcrl/artifacts/0008/local_compatibility_check.json`
- `research/reward_to_gcrl/artifacts/0008/environment_audit.json`
- `research/reward_to_gcrl/artifacts/0008/exact_dp_references.json`
- `research/reward_to_gcrl/artifacts/0008/raw_metrics.json`
- `research/reward_to_gcrl/artifacts/0008/all_raw_metrics.json`
- `research/reward_to_gcrl/artifacts/0008/per_goal_metrics.json`
- `research/reward_to_gcrl/artifacts/0008/per_goal_metrics.csv`
- `research/reward_to_gcrl/artifacts/0008/goal_heatmap_arrow_data.json`
- `research/reward_to_gcrl/artifacts/0008/goal_heatmap_arrow_data.csv`
- `research/reward_to_gcrl/artifacts/0008/progress.jsonl`


## Full evidence paths

- `research/reward_to_gcrl/results/0008_result.json`
- `research/reward_to_gcrl/results/0008_summary.md`

Inspect the full result JSON only when the compact summary and artifact list are insufficient.


## Artifact paths

- `/home/eston/autoresearcher/research/reward_to_gcrl/artifacts/0004`
- `/home/eston/autoresearcher/research/reward_to_gcrl/artifacts/0005`
- `/home/eston/autoresearcher/research/reward_to_gcrl/artifacts/0006`
- `/home/eston/autoresearcher/research/reward_to_gcrl/artifacts/0007`
- `/home/eston/autoresearcher/research/reward_to_gcrl/artifacts/0008`


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
