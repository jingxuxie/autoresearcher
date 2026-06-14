# Metric Ledger: reward_to_gcrl

| Iteration | Status | Review | Decision | Key metrics |
| --- | --- | --- | --- | --- |
| 0001 | completed | weak_pass | continue | _None extracted_ |
| 0002 | failed | needs_human | continue | `metrics.predeclared_tolerances.exact_dp_policy_disagreement_rate`=0.0<br>`metrics.predeclared_tolerances.exact_dp_scaled_value_error`=1e-06 |

## Positive Signals

- `0001`: The soft terminal-mass target removes the sampled terminal-event variance source in this isolated one-step diagnostic.
- `0001`: The tiny finite-MDP check confirms the soft g_plus Bellman fixed point matches normalized Q-learning after division by (1 - gamma).
- `0001`: For gamma=0.995 and r_bar=0.01, the analytic expected g_plus rate is only 0.5 per 10000 transitions, so sampled conversion can make dense reward supervision extremely sparse.
- `0002`: The installed Gymnasium version exposes CliffWalking-v1 and tabular/CliffWalking-v0, but gym.make('CliffWalking-v0') raises a DeprecatedEnv exception.
- `0002`: Experiment 0002 did not run the DP or paired-learning phases. The compatibility check failed because Gymnasium rejected CliffWalking-v0 in this environment (Environment version v0 for `CliffWalking` is deprecated. Please use `CliffWalking-v1` instead.). Since 

## Negative Signals

- `0001`: Executor recorded and described a 6-SE Monte Carlo mean tolerance even though the plan specified 3 standard errors; raw metrics still pass the stricter 3-SE check.
- `0001`: Variance agreement is reported through sampled and analytic raw variances but lacks an explicit variance-specific tolerance or pass flag in the result JSON.
- `0001`: The script hard-codes commands_run rather than deriving them from argv; it matches this run's samples and seed but could misreport future reruns.
- `0002`: Because the plan names CliffWalking-v0 exactly, this iteration should be treated as a compatibility failure rather than evidence for or against soft successor equivalence.
- `0002`: gym.make('CliffWalking-v0') failed in the ready project environment.
- `0002`: No exact-DP oracle metrics or paired-learning metrics were produced because the compatibility gate failed before the experiment could run as written.
