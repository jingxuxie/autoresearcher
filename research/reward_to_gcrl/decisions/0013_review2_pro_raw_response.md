JSON
{
  "decision": "continue",
  "confidence": 0.9,
  "rationale": "Proceed with the proposed 0013 short-paper draft using existing reward_to_gcrl evidence only, with no new learning compute. The project has enough reviewed evidence for a scoped internal draft: the soft-terminal estimator mechanism is supported in small audited tabular settings, while the tested low-rank auxiliary-goal approach has negative evidence. The draft must preserve strict claim boundaries and require review before external publication or broader claims.",
  "evidence": [
    "The latest project state reports no current blocker and protected_file_drift=false.",
    "0012 passed as a synthesis and packaging step, ran no new learning compute, and recommended write_short_paper.",
    "0001-0007 support the scoped estimator claim: deterministic soft terminal marginalization preserves normalized-Q scaling, removes terminal-sampling variance, and helps under adequate coverage in small audited tabular settings.",
    "RiverSwim evidence is coverage-qualified: adequate-coverage runs support Bellman/value improvements, while coverage-starved runs should not be used for learning-superiority claims.",
    "0008 validated tabular vector SSM correctness on FourRooms: g_plus matched terminal-only exactly, scaled g_plus matched normalized Q to numerical precision, and real-state goal slices were correct.",
    "0009 produced valid negative transfer for the first shared low-rank FourRooms auxiliary test.",
    "0010 reproduced the low-rank auxiliary negative-transfer result, and the predeclared loss-balanced and staged repair variants did not match terminal-only on g_plus value error and Bellman residual.",
    "The current evidence does not support neural auxiliary benefit, larger-environment generality, online exploration robustness, or broad auxiliary-goal improvement claims."
  ],
  "risks": [
    "The short-paper draft could overstate small CPU tabular evidence as a general reward-to-GCRL or neural-function-approximation result.",
    "The draft could overgeneralize the low-rank auxiliary negative result into a claim that auxiliary goals are generally harmful or impossible.",
    "The draft could blur estimator evidence with auxiliary-representation evidence, making the story stronger than the experiments support.",
    "Coverage caveats from RiverSwim and matched-stream limitations could be underemphasized.",
    "Because 0013 is synthesis only, it must not be described as new empirical validation.",
    "External release before review could propagate unsupported broader claims."
  ],
  "next_experiment": {
    "experiment_id": "0013_scoped_short_paper_draft",
    "objective": "Write an internal short-paper draft from existing 0001-0012 reward_to_gcrl evidence only, with a claim-to-evidence map, explicit limitations, unsupported-claims red lines, and a pre-publication review checklist.",
    "hypothesis": "Existing evidence is sufficient for a scoped internal short-paper draft with two defensible conclusions: soft terminal marginalization is a useful small-tabular variance-reduction and equivalence mechanism under adequate coverage, while the tested rank-4 low-rank FourRooms real-state auxiliary approach is unsupported and showed negative transfer.",
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
    "failure_criteria": [
      "The draft proposes or runs new experiments.",
      "The draft claims general reward-to-GCRL success beyond audited small-tabular evidence.",
      "The draft claims auxiliary-goal benefit despite 0009 and 0010 negative-transfer evidence.",
      "The draft claims auxiliary goals are generally impossible or harmful rather than unsupported for the tested low-rank setup.",
      "The draft omits RiverSwim coverage caveats or matched-stream limitations.",
      "The draft omits or minimizes the negative auxiliary evidence.",
      "The draft is framed as externally publishable without requiring review."
    ],
    "tasks_for_codex": [
      "Create research/reward_to_gcrl/reports/0013_short_paper_draft.md.",
      "Use research/reward_to_gcrl/reports/0012_writeup_outline.md and research/reward_to_gcrl/reports/0011_evidence_synthesis.md as the primary scaffolding.",
      "Create a claim-to-evidence map covering iterations 0001 through 0012.",
      "Write a concise abstract, introduction, method summary, experimental evidence summary, negative auxiliary result section, limitations, and conclusion.",
      "Add an unsupported-claims red-line section and a pre-publication review checklist.",
      "Create research/reward_to_gcrl/results/0013_result.json recording that no new learning compute was run, listing inspected evidence files, and giving the draft status.",
      "Create research/reward_to_gcrl/results/0013_summary.md with a short decision summary and explicit instruction that the draft requires review before external use."
    ],
    "required_outputs": [
      "research/reward_to_gcrl/reports/0013_short_paper_draft.md",
      "research/reward_to_gcrl/results/0013_result.json",
      "research/reward_to_gcrl/results/0013_summary.md",
      "Claim-to-evidence map for 0001-0012",
      "Unsupported-claims red-line section",
      "Limitations and threats-to-validity section",
      "Pre-publication review checklist",
      "Statement that no new learning compute was run"
    ],
    "estimated_runtime_minutes": 25
  }
}

Proceed with the internal 0013 draft, but keep it scoped and review-gated before any external use.