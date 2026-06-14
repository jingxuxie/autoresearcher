## Current Status

The project has three reviewed `weak_pass` experiments (`0001`-`0003`). The latest Pro decision is to **pivot within the same research direction**: repair the sampled-vs-soft comparison using a nondegenerate tabular setting instead of continuing with the current degenerate CliffWalking normalization.

The research goal is **not solved**. The evidence supports the variance motivation and tabular scaling equivalence in limited settings, but it does not yet show a clear learning-performance advantage for the soft update.

Current state also flags `protected_file_drift: true`. The packet lists `0004` result/summary paths, but no reviewed `0004` evidence is supplied here, so `0004` should not be used for claims yet.

## Experiment Ledger

| Iteration | Experiment | Review | Key Outcome |
|---|---|---:|---|
| `0001` | One-state sampled-vs-soft terminal target diagnostic | `weak_pass` | Sampled and soft means matched; soft removed terminal-sampling variance; rare `g_plus` events were exposed. |
| `0002` | Audited local CliffWalking tabular equivalence | `weak_pass` | Exact DP scaling equivalence passed; paired scaled soft values matched normalized Q on sufficiently visited pairs. |
| `0003` | Sampled augmented vs deterministic soft update on audited CliffWalking | `weak_pass` | Sampled variance was higher and soft Bellman residual was lower in most runs, but value-error evidence was mixed. |
| `0004` | Repaired sampled-vs-soft pivot | Not reviewed in packet | Planned/pivoted; any existing outputs need review before being treated as evidence. |

## Main Findings

Confirmed from reviewed evidence:

- `0001` covered all 16 planned `gamma`/`r_bar` settings.
- `0001` sampled means passed the stricter 3-SE review check with max z-score `2.211`.
- `0001` soft terminal variance was zero/negligible; sampled `g_plus` counts ranged from `0.48` to `1005.02` per 10k transitions.
- `0001` finite-MDP scaling equivalence passed with `max_abs_error_scaled_f_vs_q = 3.9475168023273e-08`.
- `0002` used an audited local deterministic 4x12 CliffWalking table with 192 transition records.
- `0002` exact DP scaling equivalence passed with `max_abs_error_scaled_f_vs_q = 9.711982329463353e-10`.
- `0002` paired learning produced 20 runs; learned scaled `M` and normalized `Q` agreed within `5.115907697472721e-13` on sufficiently visited state-action pairs.
- `0003` ran 30 CPU-tabular runs across `gamma = 0.95, 0.99, 0.995`, 10 seeds each, with 200k transitions per run.
- `0003` sampled conditional variance exceeded zero soft terminal-sampling variance in all 30 runs.
- `0003` soft had lower final Bellman residual in 26 of 30 runs.

Important negative results:

- `0002` and `0003` policies had raw return `-200` and success rate `0.0` under the declared CliffWalking normalization.
- `0003` mean final soft value error was slightly worse than sampled value error.
- Soft value-error dominance was only 17 of 30 runs, and only 4 of 10 seeds at `gamma = 0.995`.
- `0003` target-mean validation did not directly compare sampled targets to the deterministic soft learner’s recorded target.

## Limitations And Risks

- The current CliffWalking normalization makes raw task success uninformative and creates nearly degenerate policy comparisons.
- Policy disagreement evidence is weak because many action-value ties remain.
- The strongest `0003` evidence is variance reduction and Bellman residual, not value-error or policy-quality dominance.
- The sampled-vs-soft deterministic target comparison failed tolerance in 19 of 30 runs, according to the Pro decision evidence.
- Continuing to auxiliary goals, neural models, RiverSwim, or larger experiments before repairing this ambiguity could compound an overclaim.
- `protected_file_drift` should be resolved before further loop progress is trusted.

## Recommended Next Human Decision

Clear or adjudicate the protected file drift, then proceed with the Pro-approved pivot only if the human accepts the scope:

- Use a small nondegenerate tabular task where raw success is meaningful.
- Audit raw rewards, normalized rewards, affine constants, terminal handling, and policy preservation under exact DP.
- Compare sampled targets directly against the deterministic soft target from the same learner state and transition.
- Require soft to show lower Bellman residual and lower or statistically indistinguishable value error; otherwise label the result as variance-only.

Do not treat any `0004` files as evidence until a review validates them.

## Files To Inspect

- `research/reward_to_gcrl/results/0001_result.json`
- `research/reward_to_gcrl/results/0002_result.json`
- `research/reward_to_gcrl/results/0003_result.json`
- `research/reward_to_gcrl/reviews/0001_review.md`
- `research/reward_to_gcrl/reviews/0002_review.md`
- `research/reward_to_gcrl/reviews/0003_review.md`
- `research/reward_to_gcrl/results/0003_summary.md`
- `research/reward_to_gcrl/decisions/0004_decision.md`
- `research/reward_to_gcrl/decisions/0004_review2_pro_decision.md`
- `research/reward_to_gcrl/plans/0004_plan.md`
- `research/reward_to_gcrl/results/0004_result.json`
- `research/reward_to_gcrl/results/0004_summary.md`