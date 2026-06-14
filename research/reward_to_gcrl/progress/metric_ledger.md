# Metric Ledger: reward_to_gcrl

| Iteration | Status | Review | Decision | Key metrics |
| --- | --- | --- | --- | --- |
| 0001 | completed | weak_pass | continue | _None extracted_ |
| 0002 | completed | weak_pass | continue | `metrics.config.exact_scaling_tolerance`=1e-06<br>`metrics.exact_dp.max_abs_error_scaled_f_vs_q`=9.711982329463353e-10<br>`metrics.exact_dp.max_policy_disagreement_rate`=0.0<br>`metrics.exact_dp.rows.0.f_final_delta`=9.581224702515101e-14<br>`metrics.exact_dp.rows.0.f_value_iteration_steps`=527 |
| 0003 | completed | weak_pass | continue | `metrics.exact_soft_dp.rows.0.bellman_residual_max_decision`=9.103828801926284e-14<br>`metrics.exact_soft_dp.rows.0.final_delta`=9.581224702515101e-14<br>`metrics.exact_soft_dp.rows.0.gamma`=0.95<br>`metrics.exact_soft_dp.rows.0.iterations`=527<br>`metrics.exact_soft_dp.rows.0.max_value`=0.999999999998179 |
| 0004 | completed | fail | needs_human | `metrics.environment_audit.reward_audit.non_success_reward`=0.0<br>`metrics.environment_audit.reward_audit.success_reward`=1.0<br>`metrics.exact_dp.non_tie_policy_informative`=True<br>`metrics.exact_dp.raw_normalized_policy_preserved`=True<br>`metrics.exact_dp.rows.0.gamma`=0.95 |

## Positive Signals

- `0001`: The soft terminal-mass target removes the sampled terminal-event variance source in this isolated one-step diagnostic.
- `0001`: The tiny finite-MDP check confirms the soft g_plus Bellman fixed point matches normalized Q-learning after division by (1 - gamma).
- `0001`: For gamma=0.995 and r_bar=0.01, the analytic expected g_plus rate is only 0.5 per 10000 transitions, so sampled conversion can make dense reward supervision extremely sparse.
- `0002`: The previous Gymnasium CliffWalking-v0 blocker is avoided by a local deterministic transition table with a saved SHA-256 hash.
- `0002`: The exact soft g_plus fixed point is numerically identical to normalized Q_star after division by (1 - gamma) for both tested gamma values.
- `0002`: Paired online learning preserves the scaling relation under identical experience, so final greedy policies agree up to tie handling.
- `0003`: The local transition table hash matches the audited 0002 table.
- `0003`: The sampled update uses p(g_plus)=(1-gamma)r_bar, p(g_minus)=(1-gamma)(1-r_bar), and p(continue)=gamma.
- `0003`: Continued sampled targets use max_a M(s_next,a) directly, without an extra gamma factor.
- `0004`: Identity reward normalization avoids the CliffWalking objective mismatch.
- `0004`: The hand-built chain has three decision states, all with non-tie exact greedy actions.
- `0004`: The sampled target is compared to a deterministic soft target computed from the same sampled learner table before each update.

## Negative Signals

- `0001`: Executor recorded and described a 6-SE Monte Carlo mean tolerance even though the plan specified 3 standard errors; raw metrics still pass the stricter 3-SE check.
- `0001`: Variance agreement is reported through sampled and analytic raw variances but lacks an explicit variance-specific tolerance or pass flag in the result JSON.
- `0001`: The script hard-codes commands_run rather than deriving them from argv; it matches this run's samples and seed but could misreport future reruns.
- `0002`: The declared normalization maps ordinary step and goal rewards to 1 and cliff falls to 0, causing the learned/evaluated greedy policies to never reach the goal; this is acceptable for the equivalence gate but makes raw C...
- `0002`: Policy-disagreement evidence is weak because exact DP has 37 tie states and 0 comparable non-tie states; paired learning also has many tie states and few comparable states in several seeds.
- `0002`: The paired learned-value comparison is nearly algebraic because both learners use identical transitions, initialization, alpha, and targets that differ only by the (1-gamma) scale.
- `0003`: The target-mean pass compares sampled targets to the sampled learner's conditional expected target, not to the deterministic soft learner's recorded target; sampled-vs-soft-deterministic target means exceed the recorded...
- `0003`: The summary claims lower/faster value-error dominance, but mean final soft value error is slightly worse overall than sampled value error, and soft value-error dominance is only 17 of 30 runs.
- `0003`: At gamma 0.995, soft value-error dominance is only 4 of 10 seeds, so the value-error evidence does not strengthen as gamma approaches 1.
- `0004`: Protected file drift remains true in loop state without adjudication.
- `0004`: The prior 0004 result is being surfaced as completed learning-improvement evidence despite lacking the newly required drift_status field.
- `0004`: No audit identifies whether the previously flagged autoresearcher.yaml change can affect experiment logic or reporting.
