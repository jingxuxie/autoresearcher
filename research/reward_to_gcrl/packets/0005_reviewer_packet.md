# Reviewer Context: reward_to_gcrl

## Latest plan

# Experiment 0005

## Objective

Run a CPU-only tabular sampled-vs-soft diagnostic on a small stochastic RiverSwim chain to test long-horizon reward propagation under sparse right-end rewards.

## Hypothesis

On a small RiverSwim chain with rewards already normalized to [0,1], sampled augmented g_plus updates are unbiased but higher variance than deterministic soft terminal updates; under matched transition streams, the soft learner should show lower TD target variance, fewer failures from rare g_plus events, and lower Bellman/value error to exact DP at the same data budget, especially as gamma approaches 1.

## Success criteria

- Creates research/reward_to_gcrl/results/0005_result.json and research/reward_to_gcrl/results/0005_summary.md.
- Creates reproducible artifacts under research/reward_to_gcrl/artifacts/0005/.
- Uses only CPU tabular methods on a small RiverSwim chain, with no neural models, auxiliary goals, large datasets, GPU-dependent work, or expensive sweeps.
- Predeclares and saves the RiverSwim transition table, reward normalization, gamma values, seeds, alpha/epsilon or behavior policy, transition budget, terminal/absorbing handling, and exact commands run.
- Solves exact normalized Q and exact soft g_plus DP references for each gamma and reports max_abs(M_plus/(1-gamma) - Q_norm) for the soft fixed point.
- Runs gamma in {0.95, 0.99, 0.995} with at least 10 seeds and a transition budget that completes within 30 minutes.
- For each gamma and seed, saves sampled g_plus event counts per 10000 transitions, target mean error against deterministic soft marginal target, sampled target variance, soft terminal-sampling variance, Bellman residual, value error to exact DP, right-end reward/occupancy diagnostics, and greedy-policy return.
- Primary pass requires sampled target means to match deterministic soft marginal targets within a predeclared Monte Carlo tolerance, sampled target variance to exceed soft terminal-sampling variance, and soft to have lower final Bellman residual or reach a fixed Bellman-error threshold earlier in most runs.

## Failure criteria

- Missing, invalid, or schema-incompatible result JSON or summary markdown.
- Exact commands, raw metrics, artifact paths, transition table, reward normalization, or terminal/absorbing handling are omitted.
- The sampled augmented baseline applies an extra gamma factor to continued sampled targets or bootstraps after sampled g_plus/g_minus absorbing events.
- The result reports only returns or training loss and omits target variance, g_plus event counts, Bellman residual, or value error to exact DP.
- Coverage is too poor to interpret and is not reported with right-end visits/reward-event counts.
- The executor adds auxiliary goals, neural approximation, larger environments, large downloads, or expensive training before this RiverSwim tabular gate is complete.

## Estimated runtime

<= 25 minutes

## Tasks for Codex

- Implement a standalone script under research/reward_to_gcrl/artifacts/0005/ defining a small stochastic RiverSwim transition table, preferably 6 or 10 states, with rewards in [0,1].
- Write an environment audit artifact containing transition probabilities, rewards, action mapping, reward normalization, and a transition-table hash.
- Compute exact DP references for normalized Q and soft g_plus fixed points for each gamma.
- Train terminal-only soft M_plus and sampled augmented g_plus learners on matched original transition streams for gamma values 0.95, 0.99, and 0.995 over at least 10 seeds.
- Use sampled probabilities p_g_plus=(1-gamma)*r_bar, p_g_minus=(1-gamma)*(1-r_bar), p_continue=gamma, with continued sampled target max_a M(s_next,a) and no extra gamma factor.
- Log checkpoint learning curves, TD target statistics, g_plus event counts, Bellman residuals, value errors, visitation coverage, right-end occupancy/reward, greedy-policy return, and policy disagreement versus exact DP.
- Save raw per-seed metrics plus aggregate metrics under research/reward_to_gcrl/artifacts/0005/.
- Validate the result JSON with schemas/result.schema.json and validate declared artifacts with scripts/validate_artifacts.py.

## Required outputs

- `research/reward_to_gcrl/results/0005_result.json`
- `research/reward_to_gcrl/results/0005_summary.md`
- `research/reward_to_gcrl/artifacts/0005/`


## Latest plan JSON

```json
{
  "estimated_runtime_minutes": 25,
  "experiment_id": "0005",
  "failure_criteria": [
    "Missing, invalid, or schema-incompatible result JSON or summary markdown.",
    "Exact commands, raw metrics, artifact paths, transition table, reward normalization, or terminal/absorbing handling are omitted.",
    "The sampled augmented baseline applies an extra gamma factor to continued sampled targets or bootstraps after sampled g_plus/g_minus absorbing events.",
    "The result reports only returns or training loss and omits target variance, g_plus event counts, Bellman residual, or value error to exact DP.",
    "Coverage is too poor to interpret and is not reported with right-end visits/reward-event counts.",
    "The executor adds auxiliary goals, neural approximation, larger environments, large downloads, or expensive training before this RiverSwim tabular gate is complete."
  ],
  "hypothesis": "On a small RiverSwim chain with rewards already normalized to [0,1], sampled augmented g_plus updates are unbiased but higher variance than deterministic soft terminal updates; under matched transition streams, the soft learner should show lower TD target variance, fewer failures from rare g_plus events, and lower Bellman/value error to exact DP at the same data budget, especially as gamma approaches 1.",
  "objective": "Run a CPU-only tabular sampled-vs-soft diagnostic on a small stochastic RiverSwim chain to test long-horizon reward propagation under sparse right-end rewards.",
  "required_outputs": [
    "research/reward_to_gcrl/results/0005_result.json",
    "research/reward_to_gcrl/results/0005_summary.md",
    "research/reward_to_gcrl/artifacts/0005/"
  ],
  "success_criteria": [
    "Creates research/reward_to_gcrl/results/0005_result.json and research/reward_to_gcrl/results/0005_summary.md.",
    "Creates reproducible artifacts under research/reward_to_gcrl/artifacts/0005/.",
    "Uses only CPU tabular methods on a small RiverSwim chain, with no neural models, auxiliary goals, large datasets, GPU-dependent work, or expensive sweeps.",
    "Predeclares and saves the RiverSwim transition table, reward normalization, gamma values, seeds, alpha/epsilon or behavior policy, transition budget, terminal/absorbing handling, and exact commands run.",
    "Solves exact normalized Q and exact soft g_plus DP references for each gamma and reports max_abs(M_plus/(1-gamma) - Q_norm) for the soft fixed point.",
    "Runs gamma in {0.95, 0.99, 0.995} with at least 10 seeds and a transition budget that completes within 30 minutes.",
    "For each gamma and seed, saves sampled g_plus event counts per 10000 transitions, target mean error against deterministic soft marginal target, sampled target variance, soft terminal-sampling variance, Bellman residual, value error to exact DP, right-end reward/occupancy diagnostics, and greedy-policy return.",
    "Primary pass requires sampled target means to match deterministic soft marginal targets within a predeclared Monte Carlo tolerance, sampled target variance to exceed soft terminal-sampling variance, and soft to have lower final Bellman residual or reach a fixed Bellman-error threshold earlier in most runs."
  ],
  "tasks_for_codex": [
    "Implement a standalone script under research/reward_to_gcrl/artifacts/0005/ defining a small stochastic RiverSwim transition table, preferably 6 or 10 states, with rewards in [0,1].",
    "Write an environment audit artifact containing transition probabilities, rewards, action mapping, reward normalization, and a transition-table hash.",
    "Compute exact DP references for normalized Q and soft g_plus fixed points for each gamma.",
    "Train terminal-only soft M_plus and sampled augmented g_plus learners on matched original transition streams for gamma values 0.95, 0.99, and 0.995 over at least 10 seeds.",
    "Use sampled probabilities p_g_plus=(1-gamma)*r_bar, p_g_minus=(1-gamma)*(1-r_bar), p_continue=gamma, with continued sampled target max_a M(s_next,a) and no extra gamma factor.",
    "Log checkpoint learning curves, TD target statistics, g_plus event counts, Bellman residuals, value errors, visitation coverage, right-end occupancy/reward, greedy-policy return, and policy disagreement versus exact DP.",
    "Save raw per-seed metrics plus aggregate metrics under research/reward_to_gcrl/artifacts/0005/.",
    "Validate the result JSON with schemas/result.schema.json and validate declared artifacts with scripts/validate_artifacts.py."
  ]
}
```


## Latest result summary

```json
{
  "_source": "/home/eston/autoresearcher/research/reward_to_gcrl/results/0005_result.json",
  "artifacts": {
    "_type": "list",
    "first_items": [
      "research/reward_to_gcrl/artifacts/0005/run_riverswim_sampled_vs_soft.py",
      "research/reward_to_gcrl/artifacts/0005/local_compatibility_check.json",
      "research/reward_to_gcrl/artifacts/0005/environment_audit.json"
    ],
    "length": 10
  },
  "baseline_metrics": {
    "baseline_name": "sampled_augmented_g_plus_learning",
    "mean_final_bellman_residual": 0.012418827299201882,
    "mean_final_value_error": 0.11345317088891518,
    "mean_g_plus_events_per_10000": 66.60833333333332,
    "mean_greedy_raw_return": 48.28433333333334,
    "mean_policy_disagreement": 0.09444444444444446,
    "zero_g_plus_event_runs": 0
  },
  "claim_tested": "On a small stochastic RiverSwim chain with normalized rewards in [0,1], sampled augmented g_plus updates are unbiased but higher variance than deterministic soft terminal updates, and soft learning improves Bellman/value error under matched transition streams.",
  "experiment_id": "0005",
  "interpretation": "The RiverSwim diagnostic supports the hypothesis: sampled targets match the deterministic soft marginal target within Monte Carlo tolerance while retaining higher terminal-sampling variance, and the deterministic soft learner has lower or faster Bellman residual reduction in most matched-stream runs.",
  "known_failures": [],
  "metrics": {
    "config": {
      "alpha": 0.05,
      "behavior_policy": "epsilon-greedy with respect to exact normalized-Q greedy action",
      "bellman_residual_threshold": 0.01,
      "checkpoints": {
        "_type": "list",
        "length": 7
      },
      "epsilon_end": 0.02,
      "epsilon_start": 0.25,
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
      "terminal_absorbing_handling": "No original RiverSwim states are terminal. Original-transition bootstraps are always active. Sampled g_plus/g_minus absorbing events do not bootstrap.",
      "transition_budget": 200000
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
      "coverage_interpretable": true,
      "cpu_tabular_only": true,
      "environment_audit_complete": true,
      "exact_scaled_soft_matches_q_norm": true,
      "gamma_seed_budget_complete": true,
      "primary_pass": true,
      "sampled_variance_exceeds_soft_all_runs": true,
      "soft_dominates_most_runs": true,
      "target_mean_match_all_runs": true
    },
    "sampled_vs_soft": {
      "aggregate": {
        "_type": "object",
        "key_count": 23,
        "keys": [
          "by_gamma",
          "mean_conditional_sampling_variance",
          "mean_exact_greedy_raw_return",
          "mean_final_sampled_bellman_residual",
          "mean_final_sampled_value_error",
          "mean_final_soft_bellman_residual",
          "mean_final_soft_value_error",
          "mean_g_plus_events_per_10000",
          "mean_right_end_occupancy_rate",
          "mean_right_reward_events_per_10000",
          "mean_sampled_greedy_raw_return",
          "mean_sampled_policy_disagreement",
          "mean_soft_greedy_raw_return",
          "mean_soft_policy_disagreement",
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
    "Would a purely exploratory behavior stream change the soft-vs-sampled gap on rarely visited right-end actions?",
    "Does a larger 10-state RiverSwim preserve the same target-variance and Bellman-residual pattern under the same CPU tabular budget?"
  ],
  "status": "completed"
}
```


## Latest summary

# Experiment 0005 Summary

## Verdict

RiverSwim sampled-vs-soft diagnostic status: **completed**.

## Key Metrics

- Runs: `30` (`3` gammas x `10` seeds)
- Transition budget per run: `200000`
- Mean `g_plus` events per 10000 transitions: `66.6083`
- Mean right-end occupancy rate: `0.326288`
- Mean right reward events per 10000 transitions: `3060.1`
- Target mean match rate: `1`
- Sampled variance exceeds soft terminal-sampling variance rate: `1`
- Soft residual dominance rate: `1`
- Mean final soft Bellman residual: `0.00248977`
- Mean final sampled Bellman residual: `0.0124188`
- Mean final soft value error: `0.00455664`
- Mean final sampled value error: `0.113453`

## Interpretation

The RiverSwim diagnostic supports the hypothesis: sampled targets match the deterministic soft marginal target within Monte Carlo tolerance while retaining higher terminal-sampling variance, and the deterministic soft learner has lower or faster Bellman residual reduction in most matched-stream runs.

The environment is a continuing 6-state RiverSwim chain. Original transitions never terminate; sampled `g_plus` and `g_minus` absorbing events never bootstrap, and continued sampled targets use `max_a M(s_next,a)` with no extra gamma.

## Commands Run

```bash
mkdir -p research/reward_to_gcrl/artifacts/0005 research/reward_to_gcrl/results
conda run -n autoresearcher_reward_to_gcrl python --version
conda run -n autoresearcher_reward_to_gcrl python -m py_compile research/reward_to_gcrl/artifacts/0005/run_riverswim_sampled_vs_soft.py
conda run -n autoresearcher_reward_to_gcrl python research/reward_to_gcrl/artifacts/0005/run_riverswim_sampled_vs_soft.py --check-only
conda run -n autoresearcher_reward_to_gcrl python research/reward_to_gcrl/artifacts/0005/run_riverswim_sampled_vs_soft.py
conda run -n autoresearcher_reward_to_gcrl python -m jsonschema -i research/reward_to_gcrl/results/0005_result.json schemas/result.schema.json
conda run -n autoresearcher_reward_to_gcrl python scripts/validate_artifacts.py --repo-root . --json research/reward_to_gcrl/results/0005_result.json --schema schemas/result.schema.json --check-result-artifacts
```

## Artifacts

- `research/reward_to_gcrl/artifacts/0005/run_riverswim_sampled_vs_soft.py`
- `research/reward_to_gcrl/artifacts/0005/local_compatibility_check.json`
- `research/reward_to_gcrl/artifacts/0005/environment_audit.json`
- `research/reward_to_gcrl/artifacts/0005/exact_dp_references.json`
- `research/reward_to_gcrl/artifacts/0005/per_seed_metrics.json`
- `research/reward_to_gcrl/artifacts/0005/per_seed_summary.csv`
- `research/reward_to_gcrl/artifacts/0005/learning_curves.json`
- `research/reward_to_gcrl/artifacts/0005/learning_curves.csv`
- `research/reward_to_gcrl/artifacts/0005/raw_metrics.json`
- `research/reward_to_gcrl/artifacts/0005/progress.jsonl`


## Full evidence paths

- `research/reward_to_gcrl/results/0005_result.json`
- `research/reward_to_gcrl/results/0005_summary.md`

Inspect the full result JSON only when the compact summary and artifact list are insufficient.


## Artifact paths

- `/home/eston/autoresearcher/research/reward_to_gcrl/artifacts/0001`
- `/home/eston/autoresearcher/research/reward_to_gcrl/artifacts/0002`
- `/home/eston/autoresearcher/research/reward_to_gcrl/artifacts/0003`
- `/home/eston/autoresearcher/research/reward_to_gcrl/artifacts/0004`
- `/home/eston/autoresearcher/research/reward_to_gcrl/artifacts/0005`


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
