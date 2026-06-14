# Reviewer Context: reward_to_gcrl

## Latest plan

# Experiment 0011

## Objective

Produce a compact evidence-synthesis report that separates the positive soft-terminal estimator result from the negative low-rank auxiliary-goal result, and defines what evidence would be required before reopening auxiliary-goal experiments.

## Hypothesis

The current evidence is strong enough for a scoped report with two claims: soft terminal marginalization is a reliable small-tabular variance-reduction/equivalence mechanism under adequate coverage, while real-state auxiliary goals are unsupported for the tested low-rank shared FourRooms architecture. No additional learning run is justified until this evidence is consolidated and reviewed.

## Success criteria

- Summarize 0001-0010 in a claim-by-claim evidence table separating accepted positive evidence, accepted negative evidence, limitations, and unsupported claims.
- State the strongest defensible positive claim: soft terminal marginalization removes terminal-sampling variance and preserves normalized-Q scaling in small tabular settings, with RiverSwim learning advantages only under adequate coverage.
- State the strongest defensible negative claim: low-rank shared real-state auxiliary training did not help g_plus in FourRooms and remained harmful after the predeclared repair diagnostic.
- Include a red-line section listing claims that must not be made yet, including neural auxiliary benefit, larger-environment generality, online exploration robustness, and publishable auxiliary-goal improvement.
- Include a minimal reopening criterion for the auxiliary thread, such as a new human-approved hypothesis that changes architecture or loss normalization in a principled way rather than sweeping hyperparameters.
- Require no new learning runs, no neural frameworks, no GPU, no large environments, and no broad hyperparameter sweeps.
- Output a clear recommendation: pause_lowrank_auxiliary_thread and either write_negative_result or design_new_hypothesis_before_more_compute.

## Failure criteria

- The report mixes estimator evidence and auxiliary-goal evidence into one overbroad positive story.
- The report treats 0009 or 0010 as evidence that auxiliary goals are generally impossible rather than unsupported for the tested low-rank setup.
- The report proposes larger sweeps, PyTorch/JAX, GPU, or neural experiments without a new falsifiable hypothesis.
- The report omits coverage caveats from RiverSwim or matched-stream caveats from earlier estimator tests.
- The report omits the fact that 0009 and 0010 used uniform state-action reset replay and a single rank-4 configuration.
- The report fails to produce a concrete next-decision recommendation.

## Estimated runtime

<= 20 minutes

## Tasks for Codex

- Create research/reward_to_gcrl/reports/0011_evidence_synthesis.md.
- Extract key metrics from results 0001 through 0010 and organize them into positive estimator evidence, negative auxiliary evidence, and limitations.
- Create a claim-status table with labels supported, partially_supported, unsupported, or contradicted.
- Write a conservative abstract-style summary of the project so far.
- Write a red-line section listing claims not supported by the evidence.
- Write a future-work gate specifying what new hypothesis would justify reopening auxiliary-goal experiments.
- Create research/reward_to_gcrl/results/0011_result.json recording that no new learning compute was run, listing inspected files, and giving the final recommendation.
- Create research/reward_to_gcrl/results/0011_summary.md with the decision recommendation and links to the synthesis report.

## Required outputs

- `research/reward_to_gcrl/results/0011_result.json`
- `research/reward_to_gcrl/results/0011_summary.md`
- `research/reward_to_gcrl/artifacts/0011/`


## Latest plan JSON

```json
{
  "estimated_runtime_minutes": 20,
  "experiment_id": "0011",
  "failure_criteria": [
    "The report mixes estimator evidence and auxiliary-goal evidence into one overbroad positive story.",
    "The report treats 0009 or 0010 as evidence that auxiliary goals are generally impossible rather than unsupported for the tested low-rank setup.",
    "The report proposes larger sweeps, PyTorch/JAX, GPU, or neural experiments without a new falsifiable hypothesis.",
    "The report omits coverage caveats from RiverSwim or matched-stream caveats from earlier estimator tests.",
    "The report omits the fact that 0009 and 0010 used uniform state-action reset replay and a single rank-4 configuration.",
    "The report fails to produce a concrete next-decision recommendation."
  ],
  "hypothesis": "The current evidence is strong enough for a scoped report with two claims: soft terminal marginalization is a reliable small-tabular variance-reduction/equivalence mechanism under adequate coverage, while real-state auxiliary goals are unsupported for the tested low-rank shared FourRooms architecture. No additional learning run is justified until this evidence is consolidated and reviewed.",
  "objective": "Produce a compact evidence-synthesis report that separates the positive soft-terminal estimator result from the negative low-rank auxiliary-goal result, and defines what evidence would be required before reopening auxiliary-goal experiments.",
  "required_outputs": [
    "research/reward_to_gcrl/results/0011_result.json",
    "research/reward_to_gcrl/results/0011_summary.md",
    "research/reward_to_gcrl/artifacts/0011/"
  ],
  "success_criteria": [
    "Summarize 0001-0010 in a claim-by-claim evidence table separating accepted positive evidence, accepted negative evidence, limitations, and unsupported claims.",
    "State the strongest defensible positive claim: soft terminal marginalization removes terminal-sampling variance and preserves normalized-Q scaling in small tabular settings, with RiverSwim learning advantages only under adequate coverage.",
    "State the strongest defensible negative claim: low-rank shared real-state auxiliary training did not help g_plus in FourRooms and remained harmful after the predeclared repair diagnostic.",
    "Include a red-line section listing claims that must not be made yet, including neural auxiliary benefit, larger-environment generality, online exploration robustness, and publishable auxiliary-goal improvement.",
    "Include a minimal reopening criterion for the auxiliary thread, such as a new human-approved hypothesis that changes architecture or loss normalization in a principled way rather than sweeping hyperparameters.",
    "Require no new learning runs, no neural frameworks, no GPU, no large environments, and no broad hyperparameter sweeps.",
    "Output a clear recommendation: pause_lowrank_auxiliary_thread and either write_negative_result or design_new_hypothesis_before_more_compute."
  ],
  "tasks_for_codex": [
    "Create research/reward_to_gcrl/reports/0011_evidence_synthesis.md.",
    "Extract key metrics from results 0001 through 0010 and organize them into positive estimator evidence, negative auxiliary evidence, and limitations.",
    "Create a claim-status table with labels supported, partially_supported, unsupported, or contradicted.",
    "Write a conservative abstract-style summary of the project so far.",
    "Write a red-line section listing claims not supported by the evidence.",
    "Write a future-work gate specifying what new hypothesis would justify reopening auxiliary-goal experiments.",
    "Create research/reward_to_gcrl/results/0011_result.json recording that no new learning compute was run, listing inspected files, and giving the final recommendation.",
    "Create research/reward_to_gcrl/results/0011_summary.md with the decision recommendation and links to the synthesis report."
  ]
}
```


## Latest result summary

```json
{
  "_source": "/home/eston/autoresearcher/research/reward_to_gcrl/results/0011_result.json",
  "artifacts": [
    "research/reward_to_gcrl/reports/0011_evidence_synthesis.md",
    "research/reward_to_gcrl/artifacts/0011/build_evidence_synthesis.py",
    "research/reward_to_gcrl/artifacts/0011/local_compatibility_check.json",
    "research/reward_to_gcrl/artifacts/0011/extracted_prior_results.json",
    "research/reward_to_gcrl/artifacts/0011/claim_status_table.json",
    "research/reward_to_gcrl/artifacts/0011/progress.jsonl"
  ],
  "baseline_metrics": {
    "new_baseline_run": false,
    "prior_baselines_inspected": {
      "_type": "list",
      "first_items": [
        "research/reward_to_gcrl/results/0001_result.json",
        "research/reward_to_gcrl/results/0002_result.json",
        "research/reward_to_gcrl/results/0003_result.json"
      ],
      "length": 10
    },
    "reason": "This is a report-only synthesis; all baselines are prior completed experiments 0001-0010."
  },
  "claim_tested": "Synthesize 0001-0010 evidence to separate supported soft-terminal estimator claims from unsupported low-rank auxiliary-goal claims, without running new learning compute.",
  "experiment_id": "0011",
  "interpretation": "The evidence supports soft terminal marginalization as a small-tabular estimator/equivalence mechanism with coverage-qualified RiverSwim learning advantages. It does not support low-rank shared real-state auxiliary goals for the tested FourRooms setup; pause that thread and write the negative result.",
  "known_failures": [
    "lowrank_auxiliary_gplus_benefit_unsupported_for_tested_rank4_fourrooms_setup",
    "neural_larger_environment_online_auxiliary_claims_unsupported"
  ],
  "metrics": {
    "all_prior_results_completed": true,
    "auxiliary_next_decision": "write_negative_result",
    "claim_status_counts": {
      "contradicted": 1,
      "partially_supported": 1,
      "supported": 3,
      "unsupported": 3
    },
    "claims": {
      "_type": "list",
      "first_items": [
        {
          "_type": "object",
          "key_count": 4,
          "keys": [
            "claim",
            "evidence",
            "limitations",
            "status"
          ]
        },
        {
          "_type": "object",
          "key_count": 4,
          "keys": [
            "claim",
            "evidence",
            "limitations",
            "status"
          ]
        },
        {
          "_type": "object",
          "key_count": 4,
          "keys": [
            "claim",
            "evidence",
            "limitations",
            "status"
          ]
        }
      ],
      "length": 8
    },
    "final_recommendation": "pause_lowrank_auxiliary_thread",
    "inspected_experiment_count": 10,
    "inspected_result_files": {
      "_type": "list",
      "first_items": [
        "research/reward_to_gcrl/results/0001_result.json",
        "research/reward_to_gcrl/results/0002_result.json",
        "research/reward_to_gcrl/results/0003_result.json"
      ],
      "length": 10
    },
    "limitations": [
      "tiny CPU tabular or CPU NumPy settings only",
      "RiverSwim learning claims require adequate coverage",
      "CliffWalking raw-task returns are limited by reward-normalization mismatch",
      "0009/0010 use uniform state-action reset replay",
      "0009/0010 test a single rank-4 low-rank configuration family"
    ],
    "new_learning_compute_run": false,
    "red_line_claims": [
      "neural auxiliary-goal benefit",
      "larger-environment generality",
      "online exploration robustness",
      "publishable auxiliary-goal improvement",
      "general impossibility of auxiliary goals",
      "coverage-starved soft learning superiority"
    ],
    "reopening_gate": "Reopen only with a human-approved falsifiable hypothesis that changes architecture or loss normalization in a principled way, not with broad hyperparameter sweeps.",
    "report_only": true,
    "strongest_defensible_negative_claim": "Low-rank shared real-state auxiliary training did not help g_plus in FourRooms and remained harmful after the predeclared repair diagnostic.",
    "strongest_defensible_positive_claim": "Soft terminal marginalization removes terminal-sampling variance and preserves normalized-Q scaling in small audited tabular settings, with RiverSwim learning advantages only under adequate coverage."
  },
  "next_questions": [
    "What concise negative-result writeup should be produced from 0009 and 0010?",
    "Is there a new principled architecture or loss-normalization hypothesis that justifies reopening auxiliary-goal experiments later?"
  ],
  "status": "completed"
}
```


## Latest summary

# Experiment 0011 Summary

Status: **completed**.

This was a report-only synthesis. No new learning compute, neural framework,
GPU run, larger environment, or hyperparameter sweep was used.

Recommendation: **pause_lowrank_auxiliary_thread**.

Next decision: **write_negative_result**. Reopen auxiliary-goal experiments only
with a new human-approved falsifiable hypothesis that changes architecture or
loss normalization in a principled way.

Outputs:

- `research/reward_to_gcrl/reports/0011_evidence_synthesis.md`
- `research/reward_to_gcrl/results/0011_result.json`
- `research/reward_to_gcrl/artifacts/0011/extracted_prior_results.json`
- `research/reward_to_gcrl/artifacts/0011/claim_status_table.json`
- `research/reward_to_gcrl/artifacts/0011/progress.jsonl`


## Full evidence paths

- `research/reward_to_gcrl/results/0011_result.json`
- `research/reward_to_gcrl/results/0011_summary.md`

Inspect the full result JSON only when the compact summary and artifact list are insufficient.


## Artifact paths

- `/home/eston/autoresearcher/research/reward_to_gcrl/artifacts/0007`
- `/home/eston/autoresearcher/research/reward_to_gcrl/artifacts/0008`
- `/home/eston/autoresearcher/research/reward_to_gcrl/artifacts/0009`
- `/home/eston/autoresearcher/research/reward_to_gcrl/artifacts/0010`
- `/home/eston/autoresearcher/research/reward_to_gcrl/artifacts/0011`


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
