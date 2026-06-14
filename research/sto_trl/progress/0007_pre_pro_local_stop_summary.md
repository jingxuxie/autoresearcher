## Current Status

The project is **paused after iteration `0007`** with `human_review_required: true`. The latest supervisor decision is **stop** for the original automatic loop, and the pending Pro checkpoint for `0008` is blocked.

Reviewed evidence supports early tabular positives: raw TRL shows stochastic overoptimism, and log-TRL helps long-horizon propagation under matched coverage. It does **not** support the original stochastic successor-distance extension as a robust next method. A future continuation would need a human-approved pivot, not another automatic variant sweep.

## Experiment Ledger

| Iteration | Review | Decision | Takeaway |
|---|---:|---|---|
| `0001` | pass | continue | Built the tabular harness with exact DP. Raw TRL overestimated and preferred the risky shortcut. |
| `0002` | pass | continue | Coverage stress test confirmed raw TRL optimism is support-driven; raw chose risky in all 8 scenarios where lucky risky success was observed. |
| `0003` | weak_pass | continue | Horizon holdout showed TRL-log / MC+TRL-log recovered long-horizon values where MC-only failed. |
| `0004` | weak_pass | continue | Successor-distance + TRL-log improved over calibration-only, but reviewer flagged near-identity with TRL-log. |
| `0005` | pass | continue | Equivalence audit was negative: improving successor-distance lambdas matched TRL-log within `1e-10`; no distinct successor-distance evidence. |
| `0006` | weak_pass | pivot | Hand-shaped one-sided uncertainty penalty reduced lucky-only overestimation; stronger alphas fixed policy regret but the rule was narrow. |
| `0007` | weak_pass | needs_human / stop | Generic count-based uncertainty reduced Q overestimation modestly but did not fix lucky-only policy regret or replace the `0006` hand-shaped rule. |

## Main Findings

- **Confirmed positive:** raw deterministic-style TRL has a measurable overoptimism failure on stochastic risky paths.
- **Confirmed positive:** log-space transitive backups are useful for long-horizon propagation. In `0003`, chain MC-only heldout MSE was `0.3917`, while TRL-log and MC+TRL-log were near zero.
- **Confirmed positive but narrow:** one-sided conservative penalties can reduce lucky-only overestimation in the toy setting.
- **Confirmed negative:** the tested successor-distance formulation is not distinct from TRL-log on these diagnostics.
- **Confirmed negative:** the generic Dirichlet/count uncertainty variant in `0007` did not fix the key safe-optimal lucky-only policy failure; policy regret stayed `0.504`.
- **Confirmed negative:** `risk_optimal_no_success_stress` remains unsolved by the generic variants.

## Limitations And Risks

- The original stochastic successor-distance idea is weakly supported at best; the cleanest audit result is negative.
- The `0006` penalty is diagnostic, not general: it uses a hand-shaped shortcut eligibility rule.
- The `0007` generic method is more principled than `0006` but weaker on the central policy metric.
- Offline data without observed failures cannot identify stochastic risk without an explicit prior or model assumption.
- Larger neural, OGBench, PointMaze, or AntMaze experiments would be premature under the charter.
- Pro checkpointing for `0008` is currently blocked, and the loop state is paused pending human action.

## Recommended Next Human Decision

Choose one of two paths:

1. **Stop the original project line**: preserve the result as evidence that raw TRL overoptimism is real and log-TRL is a useful baseline, but the tested stochastic successor-distance extension is not justified.

2. **Approve the human pivot for `0008`**: reframe the question as transition-level stochastic uncertainty plus log-space transitive propagation. The recommended next experiment is an identifiability and coverage grid, not another algorithm win attempt.

Do not continue the old automatic loop unchanged.

## Files To Inspect

- `research/sto_trl/progress/human_pivot_0008.md`
- `research/sto_trl/decisions/0008_decision.md`
- `research/sto_trl/reviews/0007_review.md`
- `research/sto_trl/results/0007_result.json`
- `research/sto_trl/results/0007_summary.md`
- `research/sto_trl/reviews/0005_review.md`
- `research/sto_trl/results/0005_result.json`
- `research/sto_trl/sto_trl_next_steps_review_plan.md`