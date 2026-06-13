## Current Status

Project is **stopped after iteration 0007**. The reviewed tabular evidence is enough to answer the early screening question: raw TRL has a real stochastic overoptimism failure mode, and log-TRL helps with long-horizon recovery under matched coverage, but the proposed stochastic successor-distance or generic uncertainty extension is **not yet justified as a robust method**.

The research goal should **not** be treated as solved. The strongest positive evidence supports diagnostics and baseline behavior, not a general stochastic TRL variant.

## Experiment Ledger

| Iteration | Review | Decision | Main Result |
|---|---:|---|---|
| 0001 | pass | continue | Built valid tabular harness. Deterministic chain passed; raw TRL overestimated and preferred risky shortcut. |
| 0002 | pass | continue | Coverage stress test showed raw TRL is support-driven: selected risky in 8/8 scenarios where risky success was observed. |
| 0003 | weak_pass | continue | Horizon holdout: MC-only failed long-horizon estimates; TRL-log and MC+TRL-log recovered near-exact heldout MSE. |
| 0004 | weak_pass | continue | Successor-distance + TRL-log beat calibration-only, but reviewer flagged it as likely behaviorally identical to TRL-log. |
| 0005 | pass | continue | Lambda/equivalence audit was negative: no distinct successor-distance evidence; improving lambdas matched TRL-log within `1e-10`. |
| 0006 | weak_pass | pivot | Hand-shaped one-sided conservative penalty reduced lucky-only overestimation; stronger alphas fixed policy regret, but rule was narrow and hand-shaped. |
| 0007 | weak_pass | stop | Generic count-based uncertainty reduced Q overestimation modestly but did **not** fix lucky-only policy regret and did not replace the 0006 hand-shaped rule. |

## Main Findings

- Confirmed: the tabular setup is reproducible and uses exact DP ground truth with required result, summary, and artifact files.

- Confirmed: raw deterministic-style TRL can be overoptimistic under stochastic risky shortcuts. This satisfies one early positive charter criterion.

- Confirmed: TRL-log and MC+TRL-log recover long-horizon discounted reachability in the censored-label holdout setting. In 0003, chain heldout MSE dropped from MC-only `0.3917` to near zero for TRL-log / MC+TRL-log.

- Confirmed negative: the explicit successor-distance variant did not show distinct value beyond TRL-log. In 0005, `any_positive_successor_evidence=false`.

- Confirmed weak/narrow positive: a hand-shaped one-sided penalty in 0006 can reduce lucky-only risky overestimation and, at stronger alphas, eliminate safe-optimal lucky-only policy regret.

- Confirmed negative for generalization: 0007’s generic Dirichlet-style uncertainty method did not fix the policy-level lucky-only failure. `safe_optimal_lucky_only` policy regret stayed `0.504`, unchanged from TRL-log, and the method still selected risky.

## Limitations And Risks

- The promising 0006 penalty is hand-shaped around direct-goal shortcut actions, so it is not strong evidence for a general stochastic-calibrated TRL method.

- The 0007 generic method gives only modest Q-overestimation reduction and remains worse than the 0006 hand-shaped rule on the key lucky-only stress case.

- `risk_optimal_no_success_stress` remains unsolved by the generic variants; missing lucky outcomes cannot be inferred without an explicit prior or model assumption.

- Several reviews note unrelated uncommitted protected-file modifications, including `scripts/autoresearcher.py`; future executor work should continue avoiding control-file edits.

- Moving to neural networks, OGBench, PointMaze, AntMaze, or larger tasks would be premature under the charter because the tabular stochastic-calibration story remains weak.

## Recommended Next Human Decision

Stop the automatic experiment loop for now. A human should decide whether to:

1. End this line as a negative result for stochastic successor-distance TRL.
2. Reframe the idea around explicit model-based uncertainty or priors.
3. Keep only log-TRL as the useful baseline and abandon the stochastic-calibrated extension.
4. Design a new, principled uncertainty assumption before any further experiments.

Do **not** launch another small automatic sweep without a human design pivot.

## Files To Inspect

- `research/sto_trl/results/0007_result.json`
- `research/sto_trl/results/0007_summary.md`
- `research/sto_trl/reviews/0007_review.md`
- `research/sto_trl/decisions/0008_decision.md`
- `research/sto_trl/results/0005_result.json`
- `research/sto_trl/reviews/0005_review.md`
- `research/sto_trl/results/0006_result.json`
- `research/sto_trl/reviews/0006_review.md`