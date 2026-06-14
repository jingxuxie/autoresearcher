# Metric Ledger: reward_to_gcrl

| Iteration | Status | Review | Decision | Key metrics |
| --- | --- | --- | --- | --- |
| 0001 | completed | weak_pass | continue | _None extracted_ |
| 0002 | completed | weak_pass | continue | `metrics.config.exact_scaling_tolerance`=1e-06<br>`metrics.exact_dp.max_abs_error_scaled_f_vs_q`=9.711982329463353e-10<br>`metrics.exact_dp.max_policy_disagreement_rate`=0.0<br>`metrics.exact_dp.rows.0.f_final_delta`=9.581224702515101e-14<br>`metrics.exact_dp.rows.0.f_value_iteration_steps`=527 |
| 0003 | completed | weak_pass | continue | `metrics.exact_soft_dp.rows.0.bellman_residual_max_decision`=9.103828801926284e-14<br>`metrics.exact_soft_dp.rows.0.final_delta`=9.581224702515101e-14<br>`metrics.exact_soft_dp.rows.0.gamma`=0.95<br>`metrics.exact_soft_dp.rows.0.iterations`=527<br>`metrics.exact_soft_dp.rows.0.max_value`=0.999999999998179 |
| 0004 | completed | weak_pass | needs_human | `metrics.environment_audit.reward_audit.non_success_reward`=0.0<br>`metrics.environment_audit.reward_audit.success_reward`=1.0<br>`metrics.exact_dp.non_tie_policy_informative`=True<br>`metrics.exact_dp.raw_normalized_policy_preserved`=True<br>`metrics.exact_dp.rows.0.gamma`=0.95 |
| 0005 | completed | pass | continue | `metrics.exact_dp.rows.0.exact_greedy_policy.0`=1<br>`metrics.exact_dp.rows.0.exact_greedy_policy.1`=1<br>`metrics.exact_dp.rows.0.exact_greedy_policy.2`=1<br>`metrics.exact_dp.rows.0.exact_greedy_policy.3`=1<br>`metrics.exact_dp.rows.0.exact_greedy_policy.4`=1 |
| 0006 | completed | pass | continue | `metrics.config.behaviors.right_biased_random.uses_exact_q`=False<br>`metrics.config.behaviors.uniform_random.uses_exact_q`=False<br>`metrics.exact_dp.rows.0.exact_greedy_policy.0`=1<br>`metrics.exact_dp.rows.0.exact_greedy_policy.1`=1<br>`metrics.exact_dp.rows.0.exact_greedy_policy.2`=1 |
| 0007 | completed | pass | None | `metrics.config.behaviors.medium_right_bias.uses_exact_q`=False<br>`metrics.config.behaviors.mild_right_bias.uses_exact_q`=False<br>`metrics.config.behaviors.strong_right_bias.uses_exact_q`=False<br>`metrics.config.behaviors.uniform_random.uses_exact_q`=False<br>`metrics.exact_dp.rows.0.exact_greedy_policy.0`=1 |
| 0008 | completed | pass | continue | `metrics.config.goal_success_threshold`=0.99<br>`metrics.exact_dp.rows.0.gamma`=0.95<br>`metrics.exact_dp.rows.0.gplus_final_delta`=0.0<br>`metrics.exact_dp.rows.0.gplus_iterations`=14<br>`metrics.exact_dp.rows.0.max_abs_scaled_gplus_minus_q_norm`=1.1102230246251565e-16 |
| 0009 | completed | weak_pass | continue | `metrics.config.improvement_threshold`=0.1<br>`metrics.config.replay_behavior.uses_exact_q_or_dp`=False<br>`metrics.exact_dp.gamma`=0.95<br>`metrics.exact_dp.goal_iterations`=14<br>`metrics.exact_dp.gplus_iterations`=14 |
| 0010 | completed | weak_pass | None | `metrics.config.improvement_threshold`=0.1<br>`metrics.config.replay_behavior.uses_exact_q_or_dp`=False<br>`metrics.environment_audit.verified_against_0009_where_available.aggregate.mean_combined_goal_success_rate`=0.003717948717948718<br>`metrics.environment_audit.verified_against_0009_where_available.aggregate.mean_combined_reward_success_rate`=0.0<br>`metrics.environment_audit.verified_against_0009_where_available.aggregate.mean_terminal_reward_success_rate`=0.5384615384615384 |
| 0011 | completed | pass | None | _None extracted_ |

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
- `0005`: The RiverSwim transition table is stochastic, continuing, and has rewards already normalized to [0,1].
- `0005`: Sampled continued targets use max_a M(s_next,a) directly, without an extra gamma factor.
- `0005`: Right-end occupancy and reward-event counts are saved so sparse reward coverage is auditable.
- `0006`: Coverage thresholds are predeclared using right reward events per 10000 transitions and visited state-action pairs.
- `0006`: Estimator claims are separated from learning claims on coverage-starved runs.
- `0006`: The same 6-state RiverSwim transition semantics as 0005 were recreated and freshly audited.
- `0007`: Coverage bins are predeclared using right reward events per 10000 transitions and visited state-action pairs.
- `0007`: Estimator claims are separated from learning claims on coverage-starved runs.
- `0007`: The same 6-state RiverSwim transition hash as 0005 and 0006 was recreated and verified.
- `0008`: The g_plus slice remains a direct scaled normalized-Q reference under the audited terminal mask.
- `0008`: Real-state goals solve the deterministic reachability sanity check, so future reward changes require shared parameters or coupling to be meaningful.
- `0008`: The vector SSM slices are numerically independent in this tabular FourRooms check: the g_plus slice matches terminal-only soft learning, scaled g_plus matches normalized Q, and real-state goal slices match exact reachability references with successful greedy g
- `0009`: The low-rank model genuinely shares state-action factors across real-state goals and g_plus.
- `0009`: Combined auxiliary training worsened a g_plus metric or reward-policy disagreement under adequate replay coverage; auxiliary-goal benefit is not supported.
- `0010`: Conservative verdict: auxiliary_unsupported_for_lowrank.
- `0010`: The low-rank model genuinely shares state-action factors across real-state goals and g_plus.
- `0010`: Original negative transfer reproduced, and neither repaired variant matched terminal-only on g_plus value error and Bellman residual. Auxiliary real-state goals should be paused for this low-rank architecture.
- `0011`: Soft terminal marginalization has supported small-tabular estimator/equivalence evidence.
- `0011`: Low-rank rank-4 FourRooms auxiliary training is unsupported after reproduction and repair diagnostics.
- `0011`: The evidence supports soft terminal marginalization as a small-tabular estimator/equivalence mechanism with coverage-qualified RiverSwim learning advantages. It does not support low-rank shared real-state auxiliary goals for the tested FourRooms setup; pause t

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
- `0004`: The latest plan text inconsistently references 0005 audit/result paths, while required outputs and actual evidence use 0004 paths.
- `0004`: drift_status and evidence_integrity_verdict are under metrics rather than top-level result fields.
- `0004`: The accepted learning-improvement evidence is still from a tiny 5-state chain with controlled matched streams; broader environments remain untested.
- `0005`: The behavior policy is epsilon-greedy with respect to the exact normalized-Q greedy action, so the result is a controlled matched-stream propagation test rather than an online exploration test.
- `0005`: Right-end coverage is strong under the oracle-guided behavior stream; conclusions about sparse-reward exploration failures should be tested separately with a non-oracle exploratory behavior policy.
- `0005`: Greedy-policy return is not uniformly better for the soft learner per seed: soft has higher mean return overall, but is strictly higher than sampled in only 14 of 30 runs and has a few low-return learned policies.
- `0006`: Data generation used fixed action probabilities only; exact DP was not consulted by behavior policies.
- `0006`: Half of the runs are coverage-starved under the predeclared threshold, so learning-performance conclusions should be restricted to the adequate-coverage subset or explicitly labeled as coverage-limited.
- `0006`: In coverage-starved uniform-random runs, soft has lower Bellman residual but worse mean value error than sampled in most runs, so value-error superiority is not uniform under poor coverage.
- `0007`: Data generation used fixed action probabilities only; exact DP was not consulted by behavior policies.
- `0007`: The coverage-performance regression includes visited_state_action_pairs, but that feature is constant at 12 in the observed runs, so the regression is effectively driven by right-reward event variation.
- `0007`: Soft value error is worse than sampled in 4 of 35 adequate-coverage individual runs, although the adequate-bin mean clearly favors soft and satisfies the stated criterion.
- `0008`: Independent tabular real-state goal slices did not perturb the g_plus reward-success slice.
- `0008`: This is an exact/full-sweep deterministic sanity check; it validates indexing and independent tabular slices, not learning under sampled data or function approximation.
- `0008`: The result is expected to be nearly tautological because exact references and learned vector backups use the same audited transition semantics; this is acceptable for the predeclared implementation gate but should not be...
- `0009`: Conservative verdict: negative_transfer.
- `0009`: Exact tabular references are used only for evaluation, not behavior generation or target labels.
- `0009`: Auxiliary reward-task benefit should not be claimed unless the verdict is auxiliary_helped_gplus.
- `0010`: Exact tabular references are used only for evaluation, not behavior generation or target labels.
- `0010`: Auxiliary reward-task benefit should not be claimed unless the verdict is repaired_auxiliary_promising.
- `0010`: repaired_variant_promising
- `0011`: RiverSwim learning advantages are coverage-qualified; starved runs are not learning-superiority evidence.
- `0011`: Independent tabular real-state goals are a correctness sanity check, not an auxiliary reward-improvement result.
- `0011`: lowrank_auxiliary_gplus_benefit_unsupported_for_tested_rank4_fourrooms_setup
