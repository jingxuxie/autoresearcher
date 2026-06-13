# Decision: stop

Confidence: 0.74
Progress score: 6

## Rationale

The tabular loop has answered the core early question well enough to stop before adding another low-value variant. The strong results are for ordinary log TRL under matched coverage and for raw TRL's support-driven overoptimism. The distinct successor-distance variant failed an equivalence audit, the hand-shaped uncertainty penalty from 0006 only weakly supports a narrow fix, and 0007's generic uncertainty replacement does not fix the policy-level lucky-only failure and remains worse than the hand-shaped rule. Another tabular uncertainty tweak would likely be exploration around an assumption choice rather than a decisive test of the charter hypothesis.

## Evidence

- 0007 result and review report required result, summary, and artifacts, and the review says validation returned ok with artifact checks.
- 0007 uses the same five 0006 scenarios and the review reports 0007 offline_datasets.json and transition_tables.json match 0006 byte-for-byte, making comparisons controlled.
- 0007 review classifies the result as weak_pass and says the positive result is narrow: reduced safe_optimal_lucky_only Q overestimation versus trl_log, preserved chain recovery, and zero regret in risk_optimal_matched.
- 0007 metrics report best_positive_method=generic_dirichlet_unknown_prior_0_50_alpha_0_50 but safe_optimal_lucky_only policy_regret remains 0.504, unchanged from trl_log, and the method still selects risky.
- 0007 aggregate reports one_sided_0006_safe_lucky_policy_regret=0.0 and one_sided_0006_safe_lucky_q_overestimation=0.495, while generic variants keep lucky-only policy regret at 0.504, so the generic method does not replace the hand-shaped 0006 rule.
- 0007 reports risk_optimal_no_success_unsolved_by_best_positive=true, and the review says this stress case remains unsolved by the generic variants.
- Prior 0005 evidence remains negative for the explicit successor-distance direction: all improving successor-distance lambdas were equivalent to trl_log within tolerance and any_positive_successor_evidence=false.
- The charter's early positive evidence has already been established for raw TRL overoptimism and log-TRL long-horizon recovery, but the stochastic-calibrated extension has not produced robust general evidence beyond hand-shaped tabular penalties.

## Risks

- Stopping does not mean log TRL is useless; it means the proposed stochastic successor-distance or generic uncertainty extension is not yet justified by the tabular evidence.
- There may be a useful method with a stronger explicit prior or model-based uncertainty assumption, but choosing that assumption is now a design pivot that needs human judgment rather than another automatic small sweep.
- Moving next to neural networks, OGBench, PointMaze, or larger tasks would violate the charter's caution because the tabular stochastic-calibration story remains weak.
- The current worktree has unrelated uncommitted protected-file modifications according to the 0007 review, so future executor work should continue to avoid control-file edits.
