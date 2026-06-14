## Current Status

The project has reviewed evidence through `0004`, but `0004` is **not accepted yet**. The current blocker is procedural, not primarily scientific: `protected_file_drift` remains unresolved in loop state, and the `0004` result did not include the required drift audit.

The research goal is **not solved**. The evidence supports the variance motivation and tabular scaling equivalence, and `0004` appears scientifically stronger than `0003`, but it cannot be treated as accepted evidence until the drift issue is cleared or adjudicated.

## Experiment Ledger

| Iteration | Experiment | Review | Evidence Status | Key Outcome |
|---|---|---:|---|---|
| `0001` | One-state sampled-vs-soft terminal target diagnostic | `weak_pass` | Accepted, limited | Sampled and soft means matched; soft removed terminal-sampling variance. |
| `0002` | Audited local CliffWalking tabular equivalence | `weak_pass` | Accepted, limited | Exact DP scaling equivalence passed; paired scaled soft values matched normalized Q on sufficiently visited pairs. |
| `0003` | Sampled augmented vs soft update on audited CliffWalking | `weak_pass` | Accepted, ambiguous | Sampled variance was higher; soft Bellman residual was better in most runs, but value-error evidence was mixed. |
| `0004` | Repaired sampled-vs-soft test on nondegenerate 5-state chain | `needs_human` | Not accepted yet | Scientific checks look stronger, but protected file drift was not resolved or audited. |

## Main Findings

Confirmed from accepted reviewed evidence:

- `0001` covered all 16 planned `gamma`/`r_bar` settings; sampled means passed the stricter 3-SE review check with max z-score `2.211`.
- `0001` soft terminal variance was zero/negligible; sampled `g_plus` counts ranged from `0.48` to `1005.02` per 10k transitions.
- `0001` finite-MDP scaling equivalence passed with `max_abs_error_scaled_f_vs_q = 3.9475168023273e-08`.
- `0002` exact DP scaling equivalence passed with `max_abs_error_scaled_f_vs_q = 9.711982329463353e-10`.
- `0002` paired learning produced 20 runs; learned scaled `M` and normalized `Q` agreed within `5.115907697472721e-13` on sufficiently visited state-action pairs.
- `0003` sampled conditional variance exceeded zero soft terminal-sampling variance in all 30 runs.
- `0003` soft had lower final Bellman residual in 26 of 30 runs.

Reviewed but not yet accepted for `0004`:

- `0004` uses a nondegenerate 5-state chain with identity reward normalization and non-tie exact DP policies.
- Raw and normalized exact-DP policies are preserved.
- Exact soft scaling matches normalized Q.
- Target mean matching and sampled variance criteria pass in all 30 runs.
- Soft has lower mean final Bellman residual and lower mean value error.
- Evaluation is nondegenerate: soft policies have mean raw return `1` and success rate `1`, while sampled policies have mean raw return `0` and success rate `0`.

Important negative results:

- `0002` and `0003` had raw return `-200` and success rate `0.0` under the chosen CliffWalking normalization.
- `0003` mean final soft value error was slightly worse than sampled value error; soft value-error dominance was only 17 of 30 runs.
- `0004` triggered failure criteria because protected file drift remains unresolved and the result omits `drift_status`.

## Limitations And Risks

- `0004` cannot be accepted until protected file drift is cleared or explicitly adjudicated.
- `research/reward_to_gcrl/state.json` still reports `protected_file_drift: true`.
- A prior guard file reports protected drift on `autoresearcher.yaml`.
- `0004` tests a very small 5-state chain; even if accepted, it is not evidence for larger grids, RiverSwim, auxiliary goals, or function approximation.
- `0004` behavior streams are oracle-guided by exact normalized Q with epsilon, so it tests matched-stream estimator quality rather than fully online exploration.
- No larger-budget or decaying-step-size sensitivity check was run for the stark sampled-baseline failure.

## Recommended Next Human Decision

First decide whether the protected file drift is stale/safe or real.

- If drift is stale and protected files are clean, accept `0004` after adding or recording an explicit drift adjudication.
- If drift is real or unclear, rerun or revalidate `0004` after clearing drift.
- Do not use `0004` as evidence, and do not proceed to RiverSwim, auxiliary goals, or neural approximation, until this gate is resolved.

If `0004` is accepted after drift adjudication, the next scientific decision is whether to move to a small RiverSwim long-horizon propagation test or stop the sampled-vs-soft learning-advantage thread as tabular-only evidence.

## Files To Inspect

- `research/reward_to_gcrl/reviews/0004_review.md`
- `research/reward_to_gcrl/results/0004_result.json`
- `research/reward_to_gcrl/results/0004_summary.md`
- `research/reward_to_gcrl/artifacts/0004/run_repaired_sampled_vs_soft.py`
- `research/reward_to_gcrl/decisions/0004_review3_pro_decision.md`
- `research/reward_to_gcrl/decisions/0004_worktree_guard.json`
- `research/reward_to_gcrl/state.json`
- `research/reward_to_gcrl/reviews/0003_review.md`
- `research/reward_to_gcrl/results/0003_result.json`
- `research/reward_to_gcrl/reviews/0002_review.md`