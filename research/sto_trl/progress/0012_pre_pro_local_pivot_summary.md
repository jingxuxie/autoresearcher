## Current Status

The project is **active at iteration `0012` after a human/Pro-approved pivot** from fully observed stochastic TRL to a tiny partial-observation / hidden-alias diagnostic.

The reviewed `0012` result is a **weak pass**: required files and artifacts were produced and validated, and the experiment stayed small and tabular. It confirmed that observation-only methods fail under aliasing and that history keys can help. However, a predeclared limitation was triggered: **history-model DP fully explains the gain**, so `0012` is representation/context evidence, not a distinct TRL algorithm win.

The broader research goal is still **not solved**. The current evidence supports useful diagnostics, but not a confirmed stochastic TRL method that beats fair model-DP baselines.

## Experiment Ledger

| Iteration | Review | Decision | Key Result |
|---|---:|---|---|
| `0001` | pass | continue | Built exact-DP tabular harness; raw TRL overestimated and preferred risky shortcut. |
| `0002` | pass | continue | Raw TRL optimism was support-driven by observed lucky stochastic outcomes. |
| `0003` | weak_pass | continue | TRL-log / MC+TRL-log recovered censored long-horizon values better than MC-only. |
| `0004` | weak_pass | continue | Successor-distance + TRL-log improved over calibration-only but looked near-identical to TRL-log. |
| `0005` | pass | continue | Successor-distance equivalence audit was negative: no distinct successor-distance evidence. |
| `0006` | weak_pass | pivot | Hand-shaped conservative penalty helped lucky-only overestimation but was not general. |
| `0007` | weak_pass | needs_human | Generic uncertainty reduced Q overestimation but did not fix policy-level lucky-only regret. |
| `0008` | weak_pass | continue | Identifiability grid mapped finite-coverage and prior-dependent regimes. |
| `0009` | weak_pass | continue | Transition-posterior baselines improved over TRL-log, setting a stronger baseline. |
| `0010` | pass | continue | Posterior TRL matched prior-matched posterior mean model DP; no distinct transitive benefit. |
| `0011` | pass | stop | Randomized tiny suite repeated posterior TRL/model-DP equivalence across 15 MDPs. |
| `0012` | weak_pass | pivot | Aliased POMDP showed history context helps, but history-model DP explains the gain. |

## Main Findings

- **Confirmed positive:** raw deterministic TRL overestimates lucky stochastic paths.
- **Confirmed positive:** log-TRL helps long-horizon propagation versus MC-only under censored labels.
- **Confirmed negative:** successor-distance variants did not add distinct value beyond TRL-log.
- **Confirmed negative:** posterior TRL variants were equivalent or near-equivalent to prior-matched posterior mean model DP in `0010` and `0011`.
- **Confirmed positive for representation:** in `0012`, observation-only model DP and observation-only TRL-log failed on the aliased hub, while history-keyed methods improved long-horizon metrics.
- **Confirmed limitation:** in `0012`, `history_model_dp` achieved zero mean calibration error, zero heldout MSE, and zero policy regret, fully explaining the history-keyed MC+TRL-log gain.
- **Important negative:** no reviewed experiment has shown a distinct stochastic TRL algorithmic advantage over the appropriate model-DP baseline.

## Limitations And Risks

- `0012` uses one tiny hand-constructed POMDP with two evaluated alias regimes.
- The bounded history key includes the cue observation, nearly disambiguating the latent hub by construction.
- Latent states are present in trajectories for audit/evaluation; future work must keep explicit checks that training code does not consume them.
- The `0012` result should not be framed as posterior stochastic TRL success.
- Fully observed tabular stochastic TRL has already hit a negative boundary against model-DP baselines.
- Moving to neural networks, continuous control, PointMaze, AntMaze, OGBench, large downloads, or expensive training remains unjustified without a new human-approved question.

## Recommended Next Human Decision

Pause automatic experimentation and decide whether the project should pivot again.

Reasonable choices:

- **Stop the stochastic TRL algorithm line**: preserve the positives on raw TRL overoptimism and log-TRL horizon propagation, but conclude that the tested stochastic extensions did not beat fair tabular baselines.
- **Reframe as representation/context research**: continue only with new success criteria focused on partial observability, history construction, or unavailable model-DP baselines. This should not be described as solving the original stochastic TRL algorithm question.

Do not run another automatic method tweak without a new human-approved target and baseline.

## Files To Inspect

- `research/sto_trl/results/0012_result.json`
- `research/sto_trl/results/0012_summary.md`
- `research/sto_trl/reviews/0012_review.md`
- `research/sto_trl/artifacts/0012/aliased_pomdp_context_audit.py`
- `research/sto_trl/artifacts/0012/`
- `research/sto_trl/decisions/0012_review4_pro_decision.json`
- `research/sto_trl/decisions/0012_pro_decision.md`
- `research/sto_trl/results/0011_result.json`
- `research/sto_trl/reviews/0011_review.md`
- `research/sto_trl/results/0010_result.json`
- `research/sto_trl/reviews/0010_review.md`