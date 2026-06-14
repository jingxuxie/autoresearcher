# Decision: continue

Confidence: 0.86
Progress score: 7

## Rationale

Experiment 0007 is a strong reviewed pass that resolves the non-oracle RiverSwim coverage caveat well enough to move to the next planned milestone. The next small, high-information step is not neural function approximation yet, but a tabular vector successor-measure sanity check with real-state goals. This tests whether auxiliary goal slices learn sensible reachability while the g_plus reward slice remains equivalent to terminal-only soft learning, which is the planned gate before any shared-representation claim.

## Evidence

- research/reward_to_gcrl/results/0007_result.json is present and reports status completed with exact commands and declared artifacts.
- research/reward_to_gcrl/reviews/0007_review.json reports verdict pass, evidence_quality strong, allows_auto_continue true, success_criteria_satisfied true, and no triggered failure criteria.
- 0007 used fixed non-oracle behavior policies, not exact-Q-guided action selection, and separated starved, borderline, and adequate coverage regimes.
- 0007 reports sampled target means matching deterministic soft marginal targets in all 120 runs and sampled terminal-sampling variance exceeding soft variance in all 120 runs.
- In adequate-coverage RiverSwim runs, soft had lower mean Bellman residual and lower mean value error than sampled; starved runs were explicitly caveated as coverage-limited.
- The 0007 result recommends moving next to tabular auxiliary real-state goals, and the prototype plan's Milestone 3 is exactly a tabular vector SSM with goals S union {g_plus}.
- The charter still prohibits neural function approximation and larger expensive work before the tabular diagnostics are correct.

## Risks

- A tabular vector SSM cannot prove auxiliary representation learning benefits, because goal slices do not share parameters; it should be treated only as a correctness and diagnostics gate.
- Reward-task improvement should not be expected or claimed in tabular mode; the key check is that adding state-goal slices does not perturb the g_plus slice.
- A tiny FourRooms implementation can encode walls, doorways, terminal masks, or goal indexing incorrectly unless the transition table and state-goal IDs are audited.
- Reachability diagnostics can become subjective if they are only visual; include exact DP value errors, greedy goal-reaching success rates, and shortest-path distance checks.

## Next experiment

- Experiment id: `0008`
- Objective: Run a CPU-only tabular vector successor-measure sanity check with real-state goals plus g_plus on a tiny deterministic FourRooms grid.
