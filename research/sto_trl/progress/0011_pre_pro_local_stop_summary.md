## Current Status

Reviewed evidence now supports a **terminal stop for the current automatic research line**. The latest supervisor decision is `stop`, with a checkpoint recommended because any new direction would be a substantive human/Pro-approved pivot.

The project has produced useful early positives, but the core stochastic-TRL extension has **not** shown a distinct benefit. The successor-distance line was negative or equivalent to TRL-log, and the posterior-transitive line was equivalent to prior-matched posterior model DP in both handcrafted and randomized tabular audits.

This is not a broad impossibility result. It is a stop for the current tabular stochastic-TRL/posterior-transitive formulation.

## Experiment Ledger

| Iteration | Review | Decision | Key Result |
|---|---:|---|---|
| `0001` | pass | continue | Built exact-DP tabular harness; raw TRL overestimated and preferred risky shortcut. |
| `0002` | pass | continue | Raw TRL optimism was support-driven under lucky stochastic coverage. |
| `0003` | weak_pass | continue | TRL-log / MC+TRL-log recovered long-horizon heldout values where MC-only failed. |
| `0004` | weak_pass | continue | Successor-distance + TRL-log improved over calibration-only but appeared near-identical to TRL-log. |
| `0005` | pass | continue | Equivalence audit was negative: no distinct successor-distance evidence. |
| `0006` | weak_pass | pivot | Hand-shaped conservative penalty helped lucky-only overestimation but was not general. |
| `0007` | weak_pass | needs_human | Generic uncertainty reduced Q overestimation but did not fix lucky-only policy regret. |
| `0008` | weak_pass | continue | Identifiability grid mapped finite-coverage and prior-dependent regimes. |
| `0009` | weak_pass | continue | Transition-posterior baselines improved over TRL-log, setting a stronger baseline. |
| `0010` | pass | continue | Posterior TRL matched prior-matched posterior mean model DP; no distinct transitive benefit. |
| `0011` | pass | stop | Randomized tiny suite repeated the equivalence result across 15 tabular MDPs. |

## Main Findings

- **Confirmed positive:** raw deterministic TRL overestimates lucky stochastic paths.
- **Confirmed positive:** log-TRL helps long-horizon propagation versus MC-only under censored labels.
- **Confirmed negative:** successor-distance variants did not add distinct value beyond TRL-log.
- **Confirmed negative:** generic count/Dirichlet uncertainty did not fix policy-level lucky-only regret.
- **Confirmed:** transition uncertainty matters. Posterior transition baselines improved over plain TRL-log in selected finite-coverage regimes.
- **Confirmed negative:** posterior TRL-log did not beat prior-matched posterior model DP.
- **0010:** `positive_transitive_evidence=false`; posterior TRL variants were numerically equivalent to posterior mean model DP.
- **0011:** `positive_evidence=false`; posterior TRL variants were near-equivalent to prior-matched posterior mean model DP across 3 families, 5 seeds each, 15 MDPs, and 120 method rows.
- **Important unresolved case:** risk-optimal no-success remains unsolved from counts alone.

## Limitations And Risks

- The evidence is intentionally small, tabular, and diagnostic; it should not be generalized beyond these toy MDP families.
- The `0011` reviewer notes posterior TRL-log shares the same posterior mean backup as posterior mean model DP, so the equivalence is partly structural.
- This stop does not invalidate log-TRL as a long-horizon propagation baseline.
- This stop does not rule out future work under partial observability, hidden aliases, neural approximation, or settings where model DP is unavailable.
- Any such future direction changes the research question and needs explicit human approval and new success criteria.
- Do not move to OGBench, PointMaze, AntMaze, continuous control, large downloads, or expensive training from the current evidence.

## Recommended Next Human Decision

Approve the stop for the current automatic line.

If continuing, require a new human-approved pivot such as partial observability, hidden-state aliasing, function approximation, or unavailable transition-model DP. The next plan should define fresh success criteria and explain why posterior model DP is no longer the fair baseline or why TRL-style propagation should help beyond it.

Do not launch another automatic tabular method tweak.

## Files To Inspect

- `research/sto_trl/decisions/0012_decision.md`
- `research/sto_trl/results/0011_result.json`
- `research/sto_trl/results/0011_summary.md`
- `research/sto_trl/reviews/0011_review.md`
- `research/sto_trl/artifacts/0011/metrics.csv`
- `research/sto_trl/artifacts/0011/equivalence_diagnostics.json`
- `research/sto_trl/results/0010_result.json`
- `research/sto_trl/reviews/0010_review.md`
- `research/sto_trl/reviews/0005_review.md`
- `research/sto_trl/progress/human_pivot_0008.md`