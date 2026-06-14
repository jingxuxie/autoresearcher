## Current Status

The project is **active after reviewed iteration `0009`**. A Pro decision has been applied and agrees with continuing to a strict small tabular `0010` ablation. The environment is ready, `human_review_required` is false, and the project remains within the charter’s tabular/exact-DP scope.

The original successor-distance formulation is still weak or negative. The active reframed question is whether **transition-level stochastic uncertainty plus log-space transitive propagation** can add value under finite offline stochastic coverage.

Early charter evidence is positive, but the research goal is **not solved**. No distinct stochastic-TRL benefit beyond transition uncertainty has been confirmed yet.

## Experiment Ledger

| Iteration | Review | Decision | Key Result |
|---|---:|---|---|
| `0001` | pass | continue | Built exact-DP tabular harness; raw TRL overestimated and preferred risky shortcut. |
| `0002` | pass | continue | Raw TRL optimism was support-driven; it selected risky whenever lucky success was observed. |
| `0003` | weak_pass | continue | TRL-log / MC+TRL-log recovered long-horizon heldout values where MC-only failed. |
| `0004` | weak_pass | continue | Successor-distance + TRL-log improved over calibration-only, but appeared near-identical to TRL-log. |
| `0005` | pass | continue | Equivalence audit was negative: `any_positive_successor_evidence=false`. |
| `0006` | weak_pass | pivot | Hand-shaped conservative penalty helped lucky-only overestimation but was not general. |
| `0007` | weak_pass | needs_human | Generic count/Dirichlet uncertainty reduced Q overestimation but did not fix lucky-only policy regret. |
| `0008` | weak_pass | continue | Identifiability grid mapped 465 exact-DP cells and clarified finite-coverage/prior-dependent regimes. |
| `0009` | weak_pass | continue | Transition-posterior baselines improved over TRL-log on selected regimes, setting a stronger baseline. |

## Main Findings

- **Confirmed:** raw deterministic-style TRL has a real stochastic overoptimism failure mode.
- **Confirmed:** log-TRL helps long-horizon propagation. In `0003`, MC-only chain heldout MSE was `0.3917`; TRL-log and MC+TRL-log were near zero.
- **Confirmed negative:** the successor-distance variant tested in `0005` was not distinct from TRL-log.
- **Confirmed negative:** the generic uncertainty method in `0007` did not fix safe-optimal lucky-only policy regret; it stayed at `0.504`.
- **Confirmed:** `0008` showed many failures are finite-coverage or identifiability failures. TRL-log and empirical transition DP had identical mean policy regret `0.075565`.
- **Confirmed:** `0009` found `empirical_model_dp`, `empirical_risky_value`, and `trl_log` all had mean policy regret `0.1090125` on the representative subset, so one-step risky shortcuts show no distinct transitive benefit.
- **Confirmed:** `posterior_lower_q10_dp_beta_1_1` improved target-regime regret versus TRL-log by `-0.177525`, but it is a conservative transition-uncertainty baseline.
- **Confirmed negative:** risk-optimal no-success remains unsolved from counts alone.

## Limitations And Risks

- `0009` evidence rests on an 8-cell handpicked subset and four target cells; it is a baseline gate, not broad generalization.
- The best posterior method is conservative and fails `ambiguous_risk_optimal` and `no_success_risk_optimal`.
- Robust LCB also fails matched risk-optimal behavior in the review.
- Apparent gains may come from prior choice or conservatism rather than TRL-style propagation.
- The recent chain guard is still only a formula check; `0010` should include a real raw/log TRL chain execution check if practical.
- Large neural, continuous-control, OGBench, PointMaze, or AntMaze experiments remain premature.

## Recommended Next Human Decision

No new pivot is needed. Continue only with the planned `0010` small tabular ablation:

- Test a multi-step branch-chain or stitching graph where transitive propagation could matter.
- Compare `posterior_trl_log` and `posterior_mc_plus_trl_log` against prior-matched posterior model DP.
- Treat equivalence to posterior model DP as negative or boundary evidence.
- Require matched safe-optimal and matched risk-optimal behavior.
- Keep runtime under 30 minutes and avoid all larger-environment work.

If `0010` shows no distinct benefit beyond prior-matched transition-model DP, the reframed stochastic-TRL direction should likely pause.

## Files To Inspect

- `research/sto_trl/decisions/0010_pro_decision.json`
- `research/sto_trl/decisions/0010_decision.md`
- `research/sto_trl/plans/0010_plan.md`
- `research/sto_trl/results/0009_result.json`
- `research/sto_trl/results/0009_summary.md`
- `research/sto_trl/reviews/0009_review.md`
- `research/sto_trl/artifacts/0009/metrics.csv`
- `research/sto_trl/artifacts/0009/regime_summary.csv`
- `research/sto_trl/progress/human_pivot_0008.md`
- `research/sto_trl/sto_trl_next_steps_review_plan.md`