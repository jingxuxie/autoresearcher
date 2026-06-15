# Reviewer Context: reward_to_gcrl

## Latest plan

# Experiment 0013

## Objective

Write an internal short-paper draft from existing 0001-0012 reward_to_gcrl evidence only, with a claim-to-evidence map, explicit limitations, unsupported-claims red lines, and a pre-publication review checklist.

## Hypothesis

Existing evidence is sufficient for a scoped internal short-paper draft with two defensible conclusions: soft terminal marginalization is a useful small-tabular variance-reduction and equivalence mechanism under adequate coverage, while the tested rank-4 low-rank FourRooms real-state auxiliary approach is unsupported and showed negative transfer.

## Success criteria

- No new learning compute is run.
- The draft clearly separates estimator claims, vector-SSM correctness claims, and auxiliary-goal negative evidence.
- Every main claim is linked to specific existing iterations from 0001 through 0012.
- The strongest supported positive claim is limited to small audited tabular or CPU NumPy settings, normalized-Q scaling, terminal-sampling variance reduction, and adequate-coverage learning improvements.
- The auxiliary result is stated only as limited negative evidence for the tested rank-4 low-rank FourRooms architecture, optimizer, replay setup, gamma, and repair variants.
- The draft includes limitations covering coverage dependence, matched-stream tests, tiny environments, tabular scope, uniform reset replay, and lack of neural or large-environment evidence.
- The draft includes a red-line section listing unsupported claims: neural auxiliary benefit, broad GCRL success, online exploration robustness, benchmark generality, and general impossibility of auxiliary goals.
- The output includes a review checklist that must pass before external publication or broader claims.

## Failure criteria

- The draft proposes or runs new experiments.
- The draft claims general reward-to-GCRL success beyond audited small-tabular evidence.
- The draft claims auxiliary-goal benefit despite 0009 and 0010 negative-transfer evidence.
- The draft claims auxiliary goals are generally impossible or harmful rather than unsupported for the tested low-rank setup.
- The draft omits RiverSwim coverage caveats or matched-stream limitations.
- The draft omits or minimizes the negative auxiliary evidence.
- The draft is framed as externally publishable without requiring review.

## Estimated runtime

<= 25 minutes

## Tasks for Codex

- Create research/reward_to_gcrl/reports/0013_short_paper_draft.md.
- Use research/reward_to_gcrl/reports/0012_writeup_outline.md and research/reward_to_gcrl/reports/0011_evidence_synthesis.md as the primary scaffolding.
- Create a claim-to-evidence map covering iterations 0001 through 0012.
- Write a concise abstract, introduction, method summary, experimental evidence summary, negative auxiliary result section, limitations, and conclusion.
- Add an unsupported-claims red-line section and a pre-publication review checklist.
- Create research/reward_to_gcrl/results/0013_result.json recording that no new learning compute was run, listing inspected evidence files, and giving the draft status.
- Create research/reward_to_gcrl/results/0013_summary.md with a short decision summary and explicit instruction that the draft requires review before external use.

## Required outputs

- `research/reward_to_gcrl/results/0013_result.json`
- `research/reward_to_gcrl/results/0013_summary.md`
- `research/reward_to_gcrl/artifacts/0013/`


## Latest plan JSON

```json
{
  "estimated_runtime_minutes": 25,
  "experiment_id": "0013",
  "failure_criteria": [
    "The draft proposes or runs new experiments.",
    "The draft claims general reward-to-GCRL success beyond audited small-tabular evidence.",
    "The draft claims auxiliary-goal benefit despite 0009 and 0010 negative-transfer evidence.",
    "The draft claims auxiliary goals are generally impossible or harmful rather than unsupported for the tested low-rank setup.",
    "The draft omits RiverSwim coverage caveats or matched-stream limitations.",
    "The draft omits or minimizes the negative auxiliary evidence.",
    "The draft is framed as externally publishable without requiring review."
  ],
  "hypothesis": "Existing evidence is sufficient for a scoped internal short-paper draft with two defensible conclusions: soft terminal marginalization is a useful small-tabular variance-reduction and equivalence mechanism under adequate coverage, while the tested rank-4 low-rank FourRooms real-state auxiliary approach is unsupported and showed negative transfer.",
  "objective": "Write an internal short-paper draft from existing 0001-0012 reward_to_gcrl evidence only, with a claim-to-evidence map, explicit limitations, unsupported-claims red lines, and a pre-publication review checklist.",
  "required_outputs": [
    "research/reward_to_gcrl/results/0013_result.json",
    "research/reward_to_gcrl/results/0013_summary.md",
    "research/reward_to_gcrl/artifacts/0013/"
  ],
  "success_criteria": [
    "No new learning compute is run.",
    "The draft clearly separates estimator claims, vector-SSM correctness claims, and auxiliary-goal negative evidence.",
    "Every main claim is linked to specific existing iterations from 0001 through 0012.",
    "The strongest supported positive claim is limited to small audited tabular or CPU NumPy settings, normalized-Q scaling, terminal-sampling variance reduction, and adequate-coverage learning improvements.",
    "The auxiliary result is stated only as limited negative evidence for the tested rank-4 low-rank FourRooms architecture, optimizer, replay setup, gamma, and repair variants.",
    "The draft includes limitations covering coverage dependence, matched-stream tests, tiny environments, tabular scope, uniform reset replay, and lack of neural or large-environment evidence.",
    "The draft includes a red-line section listing unsupported claims: neural auxiliary benefit, broad GCRL success, online exploration robustness, benchmark generality, and general impossibility of auxiliary goals.",
    "The output includes a review checklist that must pass before external publication or broader claims."
  ],
  "tasks_for_codex": [
    "Create research/reward_to_gcrl/reports/0013_short_paper_draft.md.",
    "Use research/reward_to_gcrl/reports/0012_writeup_outline.md and research/reward_to_gcrl/reports/0011_evidence_synthesis.md as the primary scaffolding.",
    "Create a claim-to-evidence map covering iterations 0001 through 0012.",
    "Write a concise abstract, introduction, method summary, experimental evidence summary, negative auxiliary result section, limitations, and conclusion.",
    "Add an unsupported-claims red-line section and a pre-publication review checklist.",
    "Create research/reward_to_gcrl/results/0013_result.json recording that no new learning compute was run, listing inspected evidence files, and giving the draft status.",
    "Create research/reward_to_gcrl/results/0013_summary.md with a short decision summary and explicit instruction that the draft requires review before external use."
  ]
}
```


## Latest result summary

```json
{
  "_source": "/home/eston/autoresearcher/research/reward_to_gcrl/results/0013_result.json",
  "artifacts": [
    "research/reward_to_gcrl/reports/0013_short_paper_draft.md",
    "research/reward_to_gcrl/artifacts/0013/build_short_paper_draft.py",
    "research/reward_to_gcrl/artifacts/0013/local_compatibility_check.json",
    "research/reward_to_gcrl/artifacts/0013/claim_to_evidence_map.json",
    "research/reward_to_gcrl/artifacts/0013/draft_metadata.json",
    "research/reward_to_gcrl/artifacts/0013/progress.jsonl"
  ],
  "baseline_metrics": {
    "new_baseline_run": false,
    "reason": "Draft-only iteration; all evidence and comparisons come from completed iterations 0001-0012."
  },
  "claim_tested": "Existing 0001-0012 evidence is sufficient for an internal short-paper draft with scoped positive estimator claims and scoped negative low-rank auxiliary evidence.",
  "experiment_id": "0013",
  "interpretation": "An internal short-paper draft now exists, but it is not externally publishable without review. The draft preserves the scoped positive estimator claim and the scoped negative low-rank auxiliary result.",
  "known_failures": [
    "rank4_lowrank_fourrooms_auxiliary_benefit_contradicted",
    "neural_large_environment_online_generality_not_tested",
    "external_publication_not_yet_reviewed"
  ],
  "metrics": {
    "claim_status_counts": {
      "contradicted": 1,
      "not_tested": 1,
      "partially_supported": 1,
      "supported": 3,
      "unsupported": 1
    },
    "contains_prepublication_checklist": true,
    "contains_red_lines": true,
    "draft_status": "internal_review_required",
    "external_use_requires_review": true,
    "inspected_evidence_files": {
      "_type": "list",
      "first_items": [
        "research/reward_to_gcrl/results/0001_result.json",
        "research/reward_to_gcrl/results/0002_result.json",
        "research/reward_to_gcrl/results/0003_result.json"
      ],
      "length": 14
    },
    "main_claim_count": 7,
    "new_learning_compute_run": false,
    "report_only": true,
    "separates_estimator_vector_and_auxiliary_sections": true,
    "strongest_auxiliary_claim": "The tested rank-4 low-rank FourRooms real-state auxiliary approach is unsupported and showed negative transfer.",
    "strongest_positive_claim": "Soft terminal marginalization is useful for small audited tabular variance reduction and normalized-Q equivalence, with adequate-coverage learning improvements."
  },
  "next_questions": [
    "Who will perform the pre-publication review against the checklist?",
    "Should a separate negative-result note be prepared for 0009 and 0010 details?"
  ],
  "status": "completed"
}
```


## Latest summary

# Experiment 0013 Summary

Status: **completed**.

Created an internal short-paper draft from existing 0001-0012 evidence only. No
new learning compute, neural framework, GPU run, larger environment, or broad
sweep was used.

Draft status: **internal_review_required**.

External use instruction: the draft requires pre-publication review before any
external publication or broader claims.

Outputs:

- `research/reward_to_gcrl/reports/0013_short_paper_draft.md`
- `research/reward_to_gcrl/results/0013_result.json`
- `research/reward_to_gcrl/artifacts/0013/claim_to_evidence_map.json`
- `research/reward_to_gcrl/artifacts/0013/draft_metadata.json`
- `research/reward_to_gcrl/artifacts/0013/progress.jsonl`


## Full evidence paths

- `research/reward_to_gcrl/results/0013_result.json`
- `research/reward_to_gcrl/results/0013_summary.md`

Inspect the full result JSON only when the compact summary and artifact list are insufficient.


## Artifact paths

- `/home/eston/autoresearcher/research/reward_to_gcrl/artifacts/0009`
- `/home/eston/autoresearcher/research/reward_to_gcrl/artifacts/0010`
- `/home/eston/autoresearcher/research/reward_to_gcrl/artifacts/0011`
- `/home/eston/autoresearcher/research/reward_to_gcrl/artifacts/0012`
- `/home/eston/autoresearcher/research/reward_to_gcrl/artifacts/0013`


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
