## Current Status

The project is **active at iteration `0009`** with `human_review_required: false`. The environment is ready, and reviewed evidence through `0009` stays within the tabular exact-DP scope.

The original successor-distance formulation remains weak/negative. The project has shifted, per the human pivot, to the reframed question: whether **transition-level stochastic uncertainty plus log-space transitive propagation** can improve calibrated long-horizon reachability under finite offline stochastic coverage.

Early charter positives are satisfied, but the broader research goal is **not solved**. The next bar is stricter: any future stochastic TRL variant must beat or add clear value beyond simple transition-posterior / robust model-DP baselines.

## Experiment Ledger

| Iteration | Review | Decision | Key Result |
|---|---:|---|---|
| `0001` | pass | continue | Built the tabular harness; raw TRL overestimated and preferred risky shortcut. |
| `0002` | pass | continue | Raw TRL optimism was support-driven; selected risky whenever lucky success was observed. |
| `0003` | weak_pass | continue | TRL-log / MC+TRL-log recovered long-horizon heldout values where MC-only failed. |
| `0004` | weak_pass | continue | Successor-distance + TRL-log improved over calibration-only, but looked near-identical to TRL-log. |
| `0005` | pass | continue | Equivalence audit was negative: no distinct successor-distance evidence. |
| `0006` | weak_pass | pivot | Hand-shaped conservative penalty helped lucky-only overestimation, but was narrow. |
| `0007` | weak_pass | needs_human | Generic count/Dirichlet uncertainty reduced Q overestimation but did not fix policy regret. |
| `0008` | weak_pass | continue | Identifiability grid mapped 465 exact-DP cells; TRL-log matched empirical transition DP on the grid. |
| `0009` | weak_pass | continue | Transition-posterior / robust DP baselines improved regret on selected regimes, setting a stronger baseline. |

## Main Findings

- **Confirmed:** raw deterministic-style TRL has a real stochastic overoptimism failure mode.
- **Confirmed:** log-TRL is useful for long-horizon propagation. In `0003`, MC-only chain heldout MSE was `0.3917`, while TRL-log and MC+TRL-log were near zero.
- **Confirmed negative:** the tested successor-distance variant is not meaningfully distinct from TRL-log; `0005` found `any_positive_successor_evidence=false`.
- **Confirmed:** finite stochastic coverage is a core issue. In `0008`, TRL-log and empirical transition DP had identical action accuracy `0.6903` and mean policy regret `0.0756`, indicating many failures are identifiability/coverage failures rather than uniquely TRL-log failures.
- **Confirmed:** posterior/conservative transition baselines can improve over TRL-log on the audited regimes. In `0009`, `posterior_lower_q10_dp_beta_1_1` was best with target-regret delta `-0.1775` versus TRL-log.
- **Confirmed negative:** risk-optimal no-success remains unsolved from counts alone.

## Limitations And Risks

- `0009` evidence rests on an 8-cell handpicked subset and four target cells; it should set a baseline, not support broad generalization.
- The best `0009` method is conservative: it helps lucky-only/prior-dependent safe cases but fails `ambiguous_risk_optimal` and `no_success_risk_optimal`.
- Robust LCB also fails the matched risk-optimal check in the reviewed summary.
- Posterior and confidence-set methods encode priors or risk preferences; their wins are not purely data-driven.
- The chain guard in `0008`/`0009` is still a formula check, not a full raw/log TRL execution check on a chain dataset.
- Larger neural, continuous-control, OGBench, PointMaze, or AntMaze work remains premature.

## Recommended Next Human Decision

Continue only if the next experiment tests a **specific transitive/log-TRL benefit beyond transition uncertainty alone**.

A reasonable next human decision is to approve a small tabular posterior-TRL comparison only if it:

- Uses transition-posterior / robust DP from `0009` as the baseline to beat.
- Preserves matched safe-optimal and matched risk-optimal choices.
- Reports regime-stratified regret, calibration, overestimation, and risky-action rate.
- Explicitly separates gains from priors versus gains from transitive propagation.

Do not proceed to larger environments until a transitive method beats or complements these transition-level baselines in tabular evidence.

## Files To Inspect

- `research/sto_trl/results/0009_result.json`
- `research/sto_trl/results/0009_summary.md`
- `research/sto_trl/reviews/0009_review.md`
- `research/sto_trl/artifacts/0009/metrics.csv`
- `research/sto_trl/artifacts/0009/regime_summary.csv`
- `research/sto_trl/results/0008_result.json`
- `research/sto_trl/reviews/0008_review.md`
- `research/sto_trl/progress/human_pivot_0008.md`
- `research/sto_trl/sto_trl_next_steps_review_plan.md`