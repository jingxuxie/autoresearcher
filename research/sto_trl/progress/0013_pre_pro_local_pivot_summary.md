## Current Status

The project is **active at iteration `0013`**, but the latest reviewed evidence argues for **pausing or stopping the current representation/context branch unless a new human decision changes the question again**.

The original fully observed stochastic-TRL line already reached a negative boundary: successor-distance variants and posterior-transitive variants did not beat fair model-DP baselines. The later partial-observation pivot showed that history/context can help under aliasing, but `0012` and `0013` both found that **history-model DP fully explains the history-keyed MC+TRL-log gains**.

The research goal remains **unsolved**. The project has useful diagnostics, but no reviewed experiment shows a distinct stochastic TRL algorithmic advantage over the appropriate baseline.

## Experiment Ledger

| Iteration | Review | Decision | Key Result |
|---|---:|---|---|
| `0001` | pass | continue | Built exact-DP tabular harness; raw TRL overestimated and preferred risky shortcut. |
| `0002` | pass | continue | Raw TRL optimism was support-driven by observed lucky stochastic outcomes. |
| `0003` | weak_pass | continue | TRL-log / MC+TRL-log recovered censored long-horizon values better than MC-only. |
| `0004` | weak_pass | continue | Successor-distance + TRL-log improved over calibration-only but looked near-identical to TRL-log. |
| `0005` | pass | continue | Successor-distance equivalence audit was negative. |
| `0006` | weak_pass | pivot | Hand-shaped conservative penalty helped lucky-only overestimation but was not general. |
| `0007` | weak_pass | needs_human | Generic uncertainty reduced Q overestimation but did not fix policy-level lucky-only regret. |
| `0008` | weak_pass | continue | Identifiability grid mapped finite-coverage and prior-dependent regimes. |
| `0009` | weak_pass | continue | Transition-posterior baselines improved over TRL-log, setting a stronger baseline. |
| `0010` | pass | continue | Posterior TRL matched prior-matched posterior mean model DP; no distinct transitive benefit. |
| `0011` | pass | stop | Randomized tabular suite repeated posterior TRL/model-DP equivalence across 15 MDPs. |
| `0012` | weak_pass | pivot | Aliased POMDP showed history helps, but history-model DP fully explained the gain. |
| `0013` | weak_pass | pivot | Randomized aliased-POMDP suite confirmed history helps when cues are sufficient, but model DP explains all gains. |

## Main Findings

- **Confirmed positive:** raw deterministic TRL overestimates lucky stochastic paths.
- **Confirmed positive:** log-TRL helps long-horizon propagation versus MC-only under censored labels.
- **Confirmed negative:** successor-distance variants did not add distinct value beyond TRL-log.
- **Confirmed negative:** posterior TRL variants were equivalent or near-equivalent to prior-matched posterior mean model DP in `0010` and `0011`.
- **Confirmed representation finding:** observation-only methods fail under hidden-state aliasing.
- **Confirmed context finding:** bounded history improves strongly in cue-sufficient regimes. In `0013`, history MC+TRL-log improved heldout MSE over history MC-only by 100% in cue-sufficient cases.
- **Confirmed limitation:** `0013` reports `model_dp_explains_all_history_mc_plus_gains=true`; the gain is representation/context sufficiency, not a distinct TRL-style learning mechanism.
- **Leakage check:** `0013` reports `leakage_free_training_keys=true`.

## Limitations And Risks

- `0013` is still tiny and synthetic: 3 cue regimes, 5 seeds each, 15 cases, 280 metric rows.
- Positive cue-sufficient cases rely on observed cue tokens that disambiguate context; this is allowed by the plan but mainly demonstrates representation sufficiency.
- Generated true transition probabilities are tied to constructed offline success counts, simplifying stochastic estimation.
- History-model DP exactly explains the history MC+TRL-log gains, so claiming an algorithmic TRL win would be invalid.
- Fully observed stochastic TRL and posterior-transitive TRL have already failed against fair model-DP baselines.
- Do not move to neural networks, continuous control, PointMaze, AntMaze, OGBench, large downloads, or expensive training from this evidence.

## Recommended Next Human Decision

Stop the current automatic loop, or explicitly reframe it away from “TRL algorithmic advantage.”

A defensible next direction would need a new human-approved question, such as:

- representation learning under partial observability,
- history/key construction when model DP is unavailable,
- function approximation where exact history-model DP is not feasible,
- or environments where the fair model-DP baseline cannot be built.

Without that new framing, another automatic tabular experiment is likely to repeat the same boundary result: context helps, but model DP explains the gain.

## Files To Inspect

- `research/sto_trl/results/0013_result.json`
- `research/sto_trl/results/0013_summary.md`
- `research/sto_trl/reviews/0013_review.md`
- `research/sto_trl/artifacts/0013/randomized_pomdp_context_audit.py`
- `research/sto_trl/artifacts/0013/`
- `research/sto_trl/decisions/0013_pro_decision.json`
- `research/sto_trl/results/0012_result.json`
- `research/sto_trl/reviews/0012_review.md`
- `research/sto_trl/results/0011_result.json`
- `research/sto_trl/reviews/0011_review.md`