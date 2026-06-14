## Current Status

The project is **active after reviewed iteration `0009`**. The latest supervisor decision is **continue** with proposed experiment `0010`; no Pro checkpoint is recommended, and `human_review_required` is false.

The original successor-distance formulation remains weak/negative. The active direction is now the human-approved pivot: test whether **transition-level stochastic uncertainty plus log-space transitive propagation** adds value under finite offline stochastic coverage.

Early charter positives are satisfied, but the broader research goal is **not solved**. The key open gate is whether posterior/transitive TRL can beat or complement prior-matched transition-model DP baselines.

## Experiment Ledger

| Iteration | Review | Decision | Key Result |
|---|---:|---|---|
| `0001` | pass | continue | Built exact-DP tabular harness; raw TRL overestimated and preferred risky shortcut. |
| `0002` | pass | continue | Raw TRL optimism was support-driven; selected risky whenever lucky success was observed. |
| `0003` | weak_pass | continue | TRL-log / MC+TRL-log recovered long-horizon heldout values where MC-only failed. |
| `0004` | weak_pass | continue | Successor-distance + TRL-log improved over calibration-only, but appeared near-identical to TRL-log. |
| `0005` | pass | continue | Equivalence audit was negative: no distinct successor-distance evidence. |
| `0006` | weak_pass | pivot | Hand-shaped conservative penalty helped lucky-only overestimation but was not general. |
| `0007` | weak_pass | needs_human | Generic count/Dirichlet uncertainty reduced Q overestimation but did not fix lucky-only policy regret. |
| `0008` | weak_pass | continue | Identifiability grid mapped 465 exact-DP cells and separated empirical, prior-dependent, lucky-only, and no-success regimes. |
| `0009` | weak_pass | continue | Transition-posterior / robust DP baselines improved regret on selected regimes; no distinct TRL-log benefit on one-step risky shortcut. |

## Main Findings

- **Confirmed:** raw deterministic-style TRL has a real stochastic overoptimism failure mode.
- **Confirmed:** log-TRL helps long-horizon propagation. In `0003`, MC-only chain heldout MSE was `0.3917`, while TRL-log and MC+TRL-log were near zero.
- **Confirmed negative:** the tested successor-distance variant is not meaningfully distinct from TRL-log; `0005` found `any_positive_successor_evidence=false`.
- **Confirmed:** finite stochastic coverage is central. In `0008`, TRL-log matched empirical transition DP on the grid, indicating many failures are identifiability/coverage failures.
- **Confirmed:** in `0009`, `empirical_model_dp`, `empirical_risky_value`, and `trl_log` had identical mean policy regret `0.1090` on the representative subset.
- **Confirmed:** transition-posterior baselines can help. `posterior_lower_q10_dp_beta_1_1` was best in `0009`, with target-regime regret delta `-0.1775` versus TRL-log.
- **Confirmed negative:** risk-optimal no-success remains unsolved from counts alone.

## Limitations And Risks

- `0009` uses an 8-cell handpicked subset and only four target cells; it sets a baseline, not broad evidence.
- The best `0009` method is conservative: it fixes some safe cases but fails `ambiguous_risk_optimal` and `no_success_risk_optimal`.
- Robust LCB also fails the matched risk-optimal check in the review.
- Posterior and confidence methods encode priors or risk preferences, so wins must be separated from data-only evidence.
- The `0008`/`0009` chain guard is still a formula check, not a full raw/log TRL execution check.
- Larger neural, continuous-control, OGBench, PointMaze, or AntMaze experiments remain premature.

## Recommended Next Human Decision

Approve `0010` only as a **small tabular posterior-transitive ablation** with strict gates:

- Use a multi-step stochastic branch-chain or stitching graph where transitive propagation could matter.
- Compare against prior-matched empirical/posterior/robust model-DP baselines.
- Count success only if `posterior_trl_log` or `posterior_mc_plus_trl_log` improves over both TRL-log and prior-matched posterior model DP.
- Treat equivalence to posterior model DP, or improvement only from prior choice, as negative/boundary evidence.
- Preserve matched risk-optimal behavior and report regime-stratified metrics.

Do not move to larger environments until this ablation shows a distinct transitive benefit.

## Files To Inspect

- `research/sto_trl/decisions/0010_decision.md`
- `research/sto_trl/results/0009_result.json`
- `research/sto_trl/results/0009_summary.md`
- `research/sto_trl/reviews/0009_review.md`
- `research/sto_trl/artifacts/0009/metrics.csv`
- `research/sto_trl/artifacts/0009/regime_summary.csv`
- `research/sto_trl/results/0008_result.json`
- `research/sto_trl/reviews/0008_review.md`
- `research/sto_trl/progress/human_pivot_0008.md`
- `research/sto_trl/sto_trl_next_steps_review_plan.md`