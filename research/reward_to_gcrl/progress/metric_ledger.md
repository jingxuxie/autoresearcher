# Metric Ledger: reward_to_gcrl

| Iteration | Status | Review | Decision | Key metrics |
| --- | --- | --- | --- | --- |
| 0001 | completed | weak_pass | continue | _None extracted_ |

## Positive Signals

- `0001`: The soft terminal-mass target removes the sampled terminal-event variance source in this isolated one-step diagnostic.
- `0001`: The tiny finite-MDP check confirms the soft g_plus Bellman fixed point matches normalized Q-learning after division by (1 - gamma).
- `0001`: For gamma=0.995 and r_bar=0.01, the analytic expected g_plus rate is only 0.5 per 10000 transitions, so sampled conversion can make dense reward supervision extremely sparse.

## Negative Signals

- `0001`: Executor recorded and described a 6-SE Monte Carlo mean tolerance even though the plan specified 3 standard errors; raw metrics still pass the stricter 3-SE check.
- `0001`: Variance agreement is reported through sampled and analytic raw variances but lacks an explicit variance-specific tolerance or pass flag in the result JSON.
- `0001`: The script hard-codes commands_run rather than deriving them from argv; it matches this run's samples and seed but could misreport future reruns.
