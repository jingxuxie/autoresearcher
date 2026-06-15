# Reviewer Context: reward_to_gcrl

## Latest plan

# Experiment 0012

## Objective

Package the current evidence into a concise research memo or draft note, and define a formal gate for any future auxiliary-goal experiments. No new learning compute should be run.

## Hypothesis

The current evidence is mature enough for a scoped negative-and-positive write-up: soft terminal marginalization is a useful small-tabular estimator/equivalence mechanism under adequate coverage, while the tested low-rank real-state auxiliary approach is unsupported. Further progress requires either writing this up or proposing a genuinely new falsifiable auxiliary hypothesis.

## Success criteria

- Produce a concise memo that separates positive estimator evidence, negative auxiliary evidence, limitations, and unsupported claims.
- Include a claim table with labels such as supported, partially_supported, unsupported, contradicted, and not_tested.
- State the strongest defensible estimator claim without implying neural, large-environment, or online-exploration generality.
- State the strongest defensible auxiliary claim as negative evidence limited to the tested rank-4 NumPy low-rank FourRooms setup.
- Include a figure/table plan for a future paper or blog post, using only existing 0001-0011 evidence.
- Define a new-hypothesis gate for reopening auxiliary experiments, requiring a principled architecture or loss-normalization change and predeclared success criteria.
- Recommend one of three next directions after the memo: write_short_paper, design_new_auxiliary_hypothesis, or stop_auxiliary_thread.

## Failure criteria

- The memo proposes new compute before summarizing and reviewing existing evidence.
- The memo claims auxiliary-goal benefit despite 0009 and 0010 negative-transfer evidence.
- The memo presents the low-rank auxiliary failure as a general impossibility result.
- The memo omits RiverSwim coverage caveats or the small-tabular limitation.
- The memo recommends broad sweeps, neural frameworks, GPU use, or larger environments without a new falsifiable hypothesis.
- The memo lacks a concrete go/no-go gate for reopening auxiliary experiments.

## Estimated runtime

<= 20 minutes

## Tasks for Codex

- Create research/reward_to_gcrl/reports/0012_writeup_outline.md.
- Create a claim-status table covering 0001 through 0011.
- Extract the key numeric evidence for the estimator claim, including variance removal, scaling equivalence, RiverSwim adequate-coverage behavior, and FourRooms vector SSM sanity checks.
- Extract the key numeric evidence for the auxiliary negative result, including 0009 terminal-only versus combined metrics and 0010 repair failure.
- Write a red-line section listing claims not supported by current evidence.
- Write a new-hypothesis gate describing what would justify reopening auxiliary experiments.
- Create research/reward_to_gcrl/results/0012_result.json recording that no new learning compute was run and giving the final recommendation.
- Create research/reward_to_gcrl/results/0012_summary.md with a short decision summary and next-step recommendation.

## Required outputs

- `research/reward_to_gcrl/results/0012_result.json`
- `research/reward_to_gcrl/results/0012_summary.md`
- `research/reward_to_gcrl/artifacts/0012/`


## Latest plan JSON

```json
{
  "estimated_runtime_minutes": 20,
  "experiment_id": "0012",
  "failure_criteria": [
    "The memo proposes new compute before summarizing and reviewing existing evidence.",
    "The memo claims auxiliary-goal benefit despite 0009 and 0010 negative-transfer evidence.",
    "The memo presents the low-rank auxiliary failure as a general impossibility result.",
    "The memo omits RiverSwim coverage caveats or the small-tabular limitation.",
    "The memo recommends broad sweeps, neural frameworks, GPU use, or larger environments without a new falsifiable hypothesis.",
    "The memo lacks a concrete go/no-go gate for reopening auxiliary experiments."
  ],
  "hypothesis": "The current evidence is mature enough for a scoped negative-and-positive write-up: soft terminal marginalization is a useful small-tabular estimator/equivalence mechanism under adequate coverage, while the tested low-rank real-state auxiliary approach is unsupported. Further progress requires either writing this up or proposing a genuinely new falsifiable auxiliary hypothesis.",
  "objective": "Package the current evidence into a concise research memo or draft note, and define a formal gate for any future auxiliary-goal experiments. No new learning compute should be run.",
  "required_outputs": [
    "research/reward_to_gcrl/results/0012_result.json",
    "research/reward_to_gcrl/results/0012_summary.md",
    "research/reward_to_gcrl/artifacts/0012/"
  ],
  "success_criteria": [
    "Produce a concise memo that separates positive estimator evidence, negative auxiliary evidence, limitations, and unsupported claims.",
    "Include a claim table with labels such as supported, partially_supported, unsupported, contradicted, and not_tested.",
    "State the strongest defensible estimator claim without implying neural, large-environment, or online-exploration generality.",
    "State the strongest defensible auxiliary claim as negative evidence limited to the tested rank-4 NumPy low-rank FourRooms setup.",
    "Include a figure/table plan for a future paper or blog post, using only existing 0001-0011 evidence.",
    "Define a new-hypothesis gate for reopening auxiliary experiments, requiring a principled architecture or loss-normalization change and predeclared success criteria.",
    "Recommend one of three next directions after the memo: write_short_paper, design_new_auxiliary_hypothesis, or stop_auxiliary_thread."
  ],
  "tasks_for_codex": [
    "Create research/reward_to_gcrl/reports/0012_writeup_outline.md.",
    "Create a claim-status table covering 0001 through 0011.",
    "Extract the key numeric evidence for the estimator claim, including variance removal, scaling equivalence, RiverSwim adequate-coverage behavior, and FourRooms vector SSM sanity checks.",
    "Extract the key numeric evidence for the auxiliary negative result, including 0009 terminal-only versus combined metrics and 0010 repair failure.",
    "Write a red-line section listing claims not supported by current evidence.",
    "Write a new-hypothesis gate describing what would justify reopening auxiliary experiments.",
    "Create research/reward_to_gcrl/results/0012_result.json recording that no new learning compute was run and giving the final recommendation.",
    "Create research/reward_to_gcrl/results/0012_summary.md with a short decision summary and next-step recommendation."
  ]
}
```


## Latest result summary

```json
{
  "_source": "/home/eston/autoresearcher/research/reward_to_gcrl/results/0012_result.json",
  "artifacts": [
    "research/reward_to_gcrl/reports/0012_writeup_outline.md",
    "research/reward_to_gcrl/artifacts/0012/build_writeup_outline.py",
    "research/reward_to_gcrl/artifacts/0012/local_compatibility_check.json",
    "research/reward_to_gcrl/artifacts/0012/numeric_evidence.json",
    "research/reward_to_gcrl/artifacts/0012/claim_status_table.json",
    "research/reward_to_gcrl/artifacts/0012/progress.jsonl"
  ],
  "baseline_metrics": {
    "new_baseline_run": false,
    "reason": "Memo-only iteration; baselines and comparisons are prior completed results 0001-0011."
  },
  "claim_tested": "Package existing 0001-0011 evidence into a concise memo and define a formal gate for future auxiliary-goal experiments without running new learning compute.",
  "experiment_id": "0012",
  "interpretation": "Current evidence is ready for a scoped write-up: positive small-tabular soft terminal marginalization, negative rank-4 low-rank FourRooms auxiliary result, and a formal gate before any more auxiliary compute.",
  "known_failures": [
    "rank4_lowrank_fourrooms_auxiliary_benefit_contradicted",
    "neural_larger_environment_online_claims_not_tested"
  ],
  "metrics": {
    "auxiliary_thread_gate": "new_hypothesis_required_before_more_compute",
    "claim_status_counts": {
      "contradicted": 1,
      "not_tested": 1,
      "partially_supported": 1,
      "supported": 2,
      "unsupported": 1
    },
    "final_recommendation": "write_short_paper",
    "inspected_experiment_ids": {
      "_type": "list",
      "first_items": [
        "0001",
        "0002",
        "0003"
      ],
      "length": 11
    },
    "new_learning_compute_run": false,
    "numeric_evidence": {
      "auxiliary_negative_evidence": {
        "_type": "object",
        "key_count": 14,
        "keys": [
          "0009_bellman_residual_delta_combined_minus_terminal",
          "0009_combined_gplus_bellman_residual",
          "0009_combined_gplus_value_error",
          "0009_combined_reward_success_rate",
          "0009_terminal_gplus_bellman_residual",
          "0009_terminal_gplus_value_error",
          "0009_terminal_reward_success_rate",
          "0009_value_error_delta_combined_minus_terminal",
          "0010_loss_balanced_gplus_residual",
          "0010_loss_balanced_gplus_value_error",
          "0010_staged_gplus_residual",
          "0010_staged_gplus_value_error",
          "0010_terminal_gplus_value_error",
          "0010_verdict"
        ]
      },
      "estimator_evidence": {
        "_type": "object",
        "key_count": 14,
        "keys": [
          "0001_finite_mdp_scaled_error",
          "0001_max_sampled_target_variance",
          "0001_max_soft_target_variance",
          "0002_cliffwalking_exact_scaled_error",
          "0003_sampled_residual",
          "0003_sampled_variance_exceeds_soft_rate",
          "0003_soft_residual",
          "0003_target_mean_match_rate",
          "0007_adequate_coverage_residual_delta",
          "0007_adequate_coverage_value_delta",
          "0007_starved_coverage_value_delta",
          "0008_min_goal_success_rate",
          "0008_vector_gplus_minus_terminal",
          "0008_vector_gplus_scaled_minus_q_norm"
        ]
      },
      "experiment_id": "0012",
      "new_learning_compute_run": false
    },
    "red_line_claims": [
      "auxiliary-goal benefit for g_plus",
      "general impossibility of real-state auxiliary goals",
      "neural auxiliary-goal benefit",
      "larger-environment generality",
      "online exploration robustness",
      "coverage-starved RiverSwim learning superiority",
      "reward-task improvement from independent tabular goal slices"
    ],
    "report_only": true,
    "strongest_defensible_auxiliary_claim": "The tested rank-4 NumPy low-rank FourRooms real-state auxiliary approach is unsupported and showed negative transfer.",
    "strongest_defensible_estimator_claim": "Soft terminal marginalization is a useful small-tabular estimator/equivalence mechanism under audited reward normalization and adequate coverage."
  },
  "next_questions": [
    "Should the short paper/blog draft be written from the 0012 outline?",
    "Is there a principled new auxiliary hypothesis worth reviewing before any further compute?"
  ],
  "status": "completed"
}
```


## Latest summary

# Experiment 0012 Summary

Status: **completed**.

This was a memo-only packaging step. No new learning compute, neural framework,
GPU run, larger environment, or broad sweep was used.

Recommendation: **write_short_paper**.

Auxiliary reopening gate: require a new human-approved falsifiable hypothesis
with a principled architecture or loss-normalization change and predeclared
terminal-only comparison criteria.

Outputs:

- `research/reward_to_gcrl/reports/0012_writeup_outline.md`
- `research/reward_to_gcrl/results/0012_result.json`
- `research/reward_to_gcrl/artifacts/0012/numeric_evidence.json`
- `research/reward_to_gcrl/artifacts/0012/claim_status_table.json`
- `research/reward_to_gcrl/artifacts/0012/progress.jsonl`


## Full evidence paths

- `research/reward_to_gcrl/results/0012_result.json`
- `research/reward_to_gcrl/results/0012_summary.md`

Inspect the full result JSON only when the compact summary and artifact list are insufficient.


## Artifact paths

- `/home/eston/autoresearcher/research/reward_to_gcrl/artifacts/0008`
- `/home/eston/autoresearcher/research/reward_to_gcrl/artifacts/0009`
- `/home/eston/autoresearcher/research/reward_to_gcrl/artifacts/0010`
- `/home/eston/autoresearcher/research/reward_to_gcrl/artifacts/0011`
- `/home/eston/autoresearcher/research/reward_to_gcrl/artifacts/0012`


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
