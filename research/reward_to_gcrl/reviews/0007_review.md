# Review 0007: pass

Allows auto-continue: True

## Reasons

- Required 0007 result JSON, summary markdown, and artifact directory are present.
- Result JSON validates against schemas/result.schema.json, and declared artifact paths validate successfully.
- The artifact set includes the coverage dose-response script, fresh environment audit, exact DP references, per-seed metrics, learning curves, raw metrics, and progress log.
- The environment audit records the same 6-state RiverSwim transition hash used in 0005 and 0006, reward normalization, terminal handling, action mapping, and four fixed non-oracle behavior policies.
- Behavior generation uses fixed action probabilities only; exact DP/Q references are computed for evaluation and error metrics, not for logged-stream action selection.
- The run covers 4 behaviors, 3 gammas, and 10 seeds for 120 total runs within the predeclared CPU tabular budget.
- Coverage bins are predeclared and all present: 30 starved, 55 borderline, and 35 adequate runs.
- Per-run metrics include direct sampled-vs-deterministic-soft target mean error, terminal-sampling variance, g_plus counts, right-reward coverage, visited state-action pairs, Bellman residual, value error, policy disagreement, and greedy return.
- Sampled target means match deterministic soft marginal targets in all 120 runs, and sampled terminal-sampling variance exceeds soft variance in all 120 runs.
- Adequate-coverage runs satisfy the learning criterion: soft has lower mean Bellman residual and lower mean value error than sampled; starved runs are explicitly caveated and show the expected Bellman/value disagreement.
- The summary includes a stratified coverage table and a coverage-performance regression, and the final recommendation is to move next to tabular auxiliary real-state goals.

## Required fixes


## Risk flags

- The coverage-performance regression includes visited_state_action_pairs, but that feature is constant at 12 in the observed runs, so the regression is effectively driven by right-reward event variation.
- Soft value error is worse than sampled in 4 of 35 adequate-coverage individual runs, although the adequate-bin mean clearly favors soft and satisfies the stated criterion.
- Right-biased behavior policies are fixed and non-oracle, but they are hand-designed to favor the known RiverSwim rightward direction; broader non-oracle data-collection policies remain untested.
- Starved runs show lower soft Bellman residual but worse soft value error, so future claims should preserve the coverage caveat.
- Current git status shows an untracked reviewer packet, but no protected path is currently modified.
