# Review 0005: pass

Allows auto-continue: True

## Reasons

- Required 0005 result JSON, summary markdown, and artifact directory are present.
- Result JSON validates against schemas/result.schema.json, and declared artifact paths validate successfully.
- The artifact set includes the RiverSwim script, environment audit, exact DP references, per-seed metrics, learning curves, raw metrics, and progress log.
- Environment audit records a 6-state stochastic continuing RiverSwim transition table, rewards already normalized to [0,1], terminal/absorbing handling, action mapping, and a transition-table hash.
- Exact DP references report scaled soft fixed-point agreement with normalized Q for all requested gammas, with max error below 1e-6.
- The run covers gamma values 0.95, 0.99, and 0.995 over 10 seeds with 200000 transitions per run and CPU tabular numpy code only.
- Per-seed metrics include g_plus counts, target mean errors and tolerances, sampled and soft target variance diagnostics, Bellman residuals, value errors, coverage/right-end reward diagnostics, greedy-policy returns, and policy disagreement.
- Sampled target means match the deterministic soft marginal target in all 30 runs, sampled terminal-sampling variance exceeds soft variance in all 30 runs, and soft residual dominance is reported in all 30 runs.

## Required fixes


## Risk flags

- The behavior policy is epsilon-greedy with respect to the exact normalized-Q greedy action, so the result is a controlled matched-stream propagation test rather than an online exploration test.
- Right-end coverage is strong under the oracle-guided behavior stream; conclusions about sparse-reward exploration failures should be tested separately with a non-oracle exploratory behavior policy.
- Greedy-policy return is not uniformly better for the soft learner per seed: soft has higher mean return overall, but is strictly higher than sampled in only 14 of 30 runs and has a few low-return learned policies.
- The experiment remains small-scale at 6 states; larger RiverSwim chains or auxiliary-goal settings remain untested.
