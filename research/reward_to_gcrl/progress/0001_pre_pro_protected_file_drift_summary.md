## Current Status

The project has completed iteration `0001` with a reviewed `weak_pass`. The first one-state variance diagnostic satisfied its reviewed success criteria, and auto-continue is allowed.

The overall research goal is **not solved yet**. Only the first diagnostic gate has passed; tabular CliffWalking equivalence, policy disagreement, RiverSwim, and any function-approximation claims remain untested.

## Experiment Ledger

| Iteration | Experiment | Review | Decision | Key Outcome |
|---|---|---:|---:|---|
| `0001` | One-state sampled-vs-soft terminal target diagnostic plus tiny finite-MDP equivalence check | `weak_pass` | `continue` | Sampled and soft targets matched expected means; soft target had zero terminal-sampling variance; finite-MDP scaling equivalence passed. |

## Main Findings

- Sampled Bernoulli and deterministic soft terminal targets matched expected means across all 16 planned `gamma` and `r_bar` settings.
- Independent review confirmed sampled means passed the stricter planned 3-standard-error check; max z-score was `2.211`.
- Soft terminal target variance was negligible/zero by construction.
- Sampled terminal events became very rare at high `gamma`: observed `g_plus` counts ranged from `0.48` to `1005.02` per 10k transitions.
- Maximum sampled target variance was `0.090401347996`.
- Maximum sampled-vs-soft mean difference was `0.0005020000000000163`.
- The tiny finite-MDP equivalence check passed: `max_abs_error(F_gplus_star / (1 - gamma) - Q_norm_star) = 3.9475e-08`, below the `1e-6` threshold.

## Limitations And Risks

- This is only a variance/equivalence sanity check, not evidence that the full reward-to-GCRL method improves learning.
- CliffWalking tabular equivalence and learned policy disagreement are still untested, so the charter’s early positive evidence criteria are not fully satisfied.
- No RiverSwim, FourRooms, auxiliary state-goal, neural, or offline fitted-learning claims are supported yet.
- The executor described a 6-SE Monte Carlo tolerance even though the plan specified 3 SE; reviewed raw metrics still pass the stricter 3-SE check.
- Variance agreement is reported through raw sampled and analytic variance fields, but the result JSON lacks an explicit variance-specific tolerance/pass flag.
- The diagnostic script hard-codes `commands_run`, which matched this run but could misreport future reruns.

## Recommended Next Human Decision

Continue to a small iteration `0002` focused on **tabular CliffWalking equivalence**, without neural models or larger environments. Require explicit reward normalization, terminal-mask handling, value error versus normalized Q-learning, and policy disagreement metrics.

## Files To Inspect

- `research/reward_to_gcrl/results/0001_result.json`
- `research/reward_to_gcrl/results/0001_summary.md`
- `research/reward_to_gcrl/reviews/0001_review.md`
- `research/reward_to_gcrl/artifacts/0001/run_terminal_variance_diagnostic.py`
- `research/reward_to_gcrl/decisions/0001_decision.md`
- `research/reward_to_gcrl/decisions/0001_pro_decision.md`