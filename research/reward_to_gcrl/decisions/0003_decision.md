# Decision: continue

Confidence: 0.82
Progress score: 4

## Rationale

The latest accepted result is a weak but valid pass for the tabular equivalence gate: exact soft g_plus values matched normalized Q-learning after scaling, and the reviewer allowed auto-continue. The next small, decisive gate is Milestone 2: compare the sampled augmented g_plus learner against the deterministic soft terminal update under the same tabular data budget, focusing on target variance, g_plus event counts, and Bellman error rather than raw CliffWalking success.

## Evidence

- research/reward_to_gcrl/results/0002_result.json exists, validates, and reports status completed with exact commands and declared artifacts.
- The 0002 review reports allows_auto_continue=true, success_criteria_satisfied=true, and no triggered failure criteria.
- Exact DP in 0002 passed the scaling check with max_abs_error_scaled_f_vs_q = 9.711982329463353e-10, below the 1e-6 tolerance.
- Paired learning in 0002 produced 20 runs across 2 gammas and 10 seeds, with learned scaled M and normalized Q agreeing within 5.115907697472721e-13 on sufficiently visited state-action pairs.
- The major 0002 caveat is scientific rather than structural: the declared reward normalization makes raw CliffWalking success 0 and creates many policy ties, so raw success is not positive evidence.
- The prototype plan's next gate after tabular equivalence is sampled augmented versus soft terminal update, with metrics for TD target variance, g_plus event count, and Bellman error.

## Risks

- The 0002 normalization makes raw goal-reaching performance uninformative; 0003 must treat raw return and success rate as diagnostics, not as the primary pass criterion.
- A sampled augmented baseline can be implemented incorrectly by double-discounting continued transitions; the expected sampled target must match (1 - gamma) * r_bar + gamma * max M_next.
- Policy metrics may remain tie-heavy in CliffWalking, so Bellman error and target-variance metrics should carry more weight than greedy disagreement alone.
- The artifact directory should be clean for 0003 and should not inherit stale timeout or compatibility files from earlier 0002 attempts.

## Next experiment

- Experiment id: `0003`
- Objective: Compare sampled augmented g_plus learning against the terminal-only soft successor update on the audited local tabular CliffWalking MDP under the same data budget.
