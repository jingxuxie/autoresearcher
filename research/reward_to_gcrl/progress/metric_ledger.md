# Metric Ledger: reward_to_gcrl

| Iteration | Status | Review | Decision | Key metrics |
| --- | --- | --- | --- | --- |
| 0001 | completed | weak_pass | continue | _None extracted_ |
| 0002 | completed | weak_pass | continue | `metrics.config.exact_scaling_tolerance`=1e-06<br>`metrics.exact_dp.max_abs_error_scaled_f_vs_q`=9.711982329463353e-10<br>`metrics.exact_dp.max_policy_disagreement_rate`=0.0<br>`metrics.exact_dp.rows.0.f_final_delta`=9.581224702515101e-14<br>`metrics.exact_dp.rows.0.f_value_iteration_steps`=527 |

## Positive Signals

- `0001`: The soft terminal-mass target removes the sampled terminal-event variance source in this isolated one-step diagnostic.
- `0001`: The tiny finite-MDP check confirms the soft g_plus Bellman fixed point matches normalized Q-learning after division by (1 - gamma).
- `0001`: For gamma=0.995 and r_bar=0.01, the analytic expected g_plus rate is only 0.5 per 10000 transitions, so sampled conversion can make dense reward supervision extremely sparse.
- `0002`: The previous Gymnasium CliffWalking-v0 blocker is avoided by a local deterministic transition table with a saved SHA-256 hash.
- `0002`: The exact soft g_plus fixed point is numerically identical to normalized Q_star after division by (1 - gamma) for both tested gamma values.
- `0002`: Paired online learning preserves the scaling relation under identical experience, so final greedy policies agree up to tie handling.

## Negative Signals

- `0001`: Executor recorded and described a 6-SE Monte Carlo mean tolerance even though the plan specified 3 standard errors; raw metrics still pass the stricter 3-SE check.
- `0001`: Variance agreement is reported through sampled and analytic raw variances but lacks an explicit variance-specific tolerance or pass flag in the result JSON.
- `0001`: The script hard-codes commands_run rather than deriving them from argv; it matches this run's samples and seed but could misreport future reruns.
- `0002`: The declared normalization maps ordinary step and goal rewards to 1 and cliff falls to 0, causing the learned/evaluated greedy policies to never reach the goal; this is acceptable for the equivalence gate but makes raw C...
- `0002`: Policy-disagreement evidence is weak because exact DP has 37 tie states and 0 comparable non-tie states; paired learning also has many tie states and few comparable states in several seeds.
- `0002`: The paired learned-value comparison is nearly algebraic because both learners use identical transitions, initialization, alpha, and targets that differ only by the (1-gamma) scale.
