# Metric Ledger: sto_trl

| Iteration | Status | Review | Decision | Key metrics |
| --- | --- | --- | --- | --- |
| 0001 | completed | pass | continue | `metrics.mdps.deterministic_chain.coverage_diagnostics.risky_failure_count`=0<br>`metrics.mdps.deterministic_chain.coverage_diagnostics.risky_success_count`=0<br>`metrics.mdps.deterministic_chain.coverage_diagnostics.risky_success_rate_observed`=None<br>`metrics.mdps.deterministic_chain.methods.mc_plus_trl_log.calibration_error`=0.13193442000000005<br>`metrics.mdps.deterministic_chain.methods.mc_plus_trl_log.eval_start_exact_q.right`=0.5904900000000002 |
| 0002 | completed | pass | continue | `metrics.aggregate.mc_supervised_mean_policy_regret`=0.0666<br>`metrics.aggregate.num_risky_scenarios`=10<br>`metrics.aggregate.raw_no_success_scenarios`=2<br>`metrics.aggregate.raw_selected_risky_when_no_success_observed`=0<br>`metrics.aggregate.raw_selected_risky_when_success_observed`=8 |
| 0003 | completed | weak_pass | continue | `metrics.aggregate.chain_mc_heldout_value_mse`=0.3917058232298766<br>`metrics.aggregate.chain_mc_plus_trl_log_heldout_value_mse`=2.9347503914472164e-34<br>`metrics.aggregate.chain_trl_log_heldout_value_mse`=2.9347503914472164e-34<br>`metrics.aggregate.risky_mc_heldout_value_mse`=0.25401600000000013<br>`metrics.aggregate.risky_mc_plus_trl_log_heldout_value_mse`=0.0 |
| 0004 | completed | weak_pass | continue | `metrics.aggregate.risk_matched_successor_calibration_only_policy_regret`=0.0<br>`metrics.aggregate.risk_matched_successor_distance_trl_log_policy_regret`=0.0<br>`metrics.aggregate.safe_lucky_stress_successor_distance_action`=risky<br>`metrics.aggregate.safe_matched_successor_calibration_only_policy_regret`=0.5040000000000001<br>`metrics.aggregate.safe_matched_successor_distance_trl_log_policy_regret`=0.0 |
| 0005 | completed | pass | continue | `metrics.aggregate.any_positive_successor_evidence`=False<br>`metrics.aggregate.lambda_summaries.successor_distance_trl_log_lambda_0_00.equivalent_to_trl_log_all_main`=False<br>`metrics.aggregate.lambda_summaries.successor_distance_trl_log_lambda_0_00.improves_vs_calibration_only`=False<br>`metrics.aggregate.lambda_summaries.successor_distance_trl_log_lambda_0_00.lambda_tr`=0.0<br>`metrics.aggregate.lambda_summaries.successor_distance_trl_log_lambda_0_00.main_mean_heldout_mse`=0.21524060774329223 |
| 0006 | completed | weak_pass | pivot | `metrics.aggregate.alpha_summaries.one_sided_conservative_log_trl_alpha_0_00.chain_heldout_mse`=2.9347503914472164e-34<br>`metrics.aggregate.alpha_summaries.one_sided_conservative_log_trl_alpha_0_00.lucky_q_overestimation_reduced_vs_trl_log`=False<br>`metrics.aggregate.alpha_summaries.one_sided_conservative_log_trl_alpha_0_00.lucky_regret_reduced_vs_trl_log`=False<br>`metrics.aggregate.alpha_summaries.one_sided_conservative_log_trl_alpha_0_00.positive_uncertainty_evidence`=False<br>`metrics.aggregate.alpha_summaries.one_sided_conservative_log_trl_alpha_0_00.risk_optimal_matched_action`=risky |
| 0007 | completed | weak_pass | needs_human | `metrics.aggregate.best_positive_method`=generic_dirichlet_unknown_prior_0_50_alpha_0_50<br>`metrics.aggregate.generic_summaries.generic_dirichlet_unknown_prior_0_50_alpha_0_00.chain_heldout_mse`=2.9347503914472164e-34<br>`metrics.aggregate.generic_summaries.generic_dirichlet_unknown_prior_0_50_alpha_0_00.lucky_policy_regret_delta_vs_one_sided_0006`=0.5040000000000001<br>`metrics.aggregate.generic_summaries.generic_dirichlet_unknown_prior_0_50_alpha_0_00.lucky_policy_regret_delta_vs_trl_log`=0.0<br>`metrics.aggregate.generic_summaries.generic_dirichlet_unknown_prior_0_50_alpha_0_00.lucky_q_overestimation_delta_vs_one_sided_0006`=0.18000000000000005 |
| 0008 | completed | weak_pass | continue | `metrics.classification_counts.no_success`=45<br>`metrics.method_summary.empirical_risky_value.action_accuracy`=0.6903225806451613<br>`metrics.method_summary.empirical_risky_value.mean_policy_regret`=0.07556516129032252<br>`metrics.method_summary.empirical_transition_dp.mean_policy_regret`=0.07556516129032252<br>`metrics.method_summary.hoeffding_lcb_delta_0_2.mean_policy_regret`=0.019136129032258063 |
| 0009 | completed | weak_pass | continue | `metrics.best_transition_uncertainty_method`=posterior_lower_q10_dp_beta_1_1<br>`metrics.best_transition_uncertainty_target_regret_delta_vs_trl_log`=-0.17752500000000004<br>`metrics.chain_guard.by_distance.1.exact`=0.9<br>`metrics.chain_guard.by_distance.2.exact`=0.81<br>`metrics.chain_guard.by_distance.3.exact`=0.7290000000000001 |
| 0010 | completed | pass | continue | `metrics.best_posterior_trl_candidate`=posterior_trl_log<br>`metrics.chain_guard.start_exact_value`=0.38742048900000015<br>`metrics.coverage_diagnostics.regimes.lucky_only_safe_optimal.label_coverage.risk_1|advance.censored_positive_labels`=0<br>`metrics.coverage_diagnostics.regimes.lucky_only_safe_optimal.label_coverage.risk_1|advance.label_count_used`=4<br>`metrics.coverage_diagnostics.regimes.lucky_only_safe_optimal.label_coverage.risk_1|advance.mean_used_label`=0.81 |
| 0011 | completed | pass | continue | `metrics.coverage_diagnostics.tag_counts.no_success`=3<br>`metrics.coverage_diagnostics.tag_counts.risk_optimal`=9<br>`metrics.equivalence_aggregate.best_candidate`=posterior_mc_plus_trl_log<br>`metrics.equivalence_aggregate.matched_risk_optimal_preserved`=True<br>`metrics.equivalence_aggregate.positive_evidence`=False |
| 0012 | completed | weak_pass | stop | `metrics.alias_diagnostics.history_mc_plus_improves_policy_regret_vs_observation_trl_log`=True<br>`metrics.alias_diagnostics.history_mc_plus_mse_improvement_fraction_vs_history_mc_only`=1.0<br>`metrics.method_summary.history_mc_only.mean_calibration_error`=0.5376375000000001<br>`metrics.method_summary.history_mc_only.mean_heldout_long_horizon_value_mse`=0.3404543906250001<br>`metrics.method_summary.history_mc_only.mean_policy_regret`=0.018224999999999936 |
| 0013 | completed | weak_pass | None | `metrics.cue_sufficient_history_mc_plus_improvement_fraction_vs_mc_only`=1.0<br>`metrics.cue_sufficient_summary.history_mc_only.mean_calibration_error`=0.5358150000000002<br>`metrics.cue_sufficient_summary.history_mc_only.mean_heldout_long_horizon_value_mse`=0.34012224<br>`metrics.cue_sufficient_summary.history_mc_only.mean_policy_regret`=0.018224999999999936<br>`metrics.cue_sufficient_summary.history_mc_only.mean_teleport_q_overestimation`=0.0 |

## Positive Signals

- `0001`: The deterministic chain sanity check was recovered by both raw and log TRL. On the risky-shortcut MDP, raw deterministic-style TRL treated the observed lucky risky edge as reliable and selected risky with Q=0.900000 versus exact Q=0.225000. The empirical log b
- `0002`: The chain guard still recovered exact discounted reachability for raw and log TRL. Across risky regimes, raw TRL selected risky in every scenario with at least one observed lucky risky transition and did not select risky when no lucky risky transition was obse
- `0003`: With positive labels beyond horizon 2 censored, MC-supervised underpredicted held-out long-horizon reachability. TRL-log and MC+TRL-log propagated through observed transitions and reduced held-out value MSE on the longer chain and the matched risky MDP. In the
- `0004`: The successor-distance transitive relaxation improved main held-out long-horizon value MSE over calibration-only. On matched safe-optimal risky coverage it selected safe with no policy-regret increase versus calibration-only, and on matched risk-optimal covera
- `0005`: The audit found negative successor-distance evidence: improving lambdas reduced held-out error by matching trl_log within the predeclared tolerance, so this variant is not yet distinct from trl_log on these tabular diagnostics.
- `0006`: one_sided_conservative_log_trl_alpha_0_20 reduced the lucky-only safe-optimal failure versus trl_log while preserving the chain and selecting risky with zero regret in the matched risk-optimal scenario.
- `0007`: generic_dirichlet_unknown_prior_0_50_alpha_0_50 reduced safe-optimal lucky-only overestimation versus trl_log while preserving the chain and selecting risky with zero regret in the matched risk-optimal scenario. The risk-optimal no-success stress status is rep
- `0008`: Posterior lower and upper choices intentionally disagree in prior-dependent cells, exposing where explicit priors are unavoidable.
- `0008`: The grid is useful as an identifiability map: it separates cells where empirical transition estimates match exact action choice from lucky-only, no-success, ambiguous, and prior-dependent cells where explicit priors are required.
- `0009`: Best target-regime transition uncertainty baseline: posterior_lower_q10_dp_beta_1_1 with regret delta -0.177525000000 versus TRL-log.
- `0009`: Posterior lower/mean baselines reduce safe lucky-only and safe prior-dependent regret without selecting safe everywhere.
- `0009`: On the representative 0008 subset, transition-level uncertainty baselines explain the recoverable finite-coverage behavior: posterior_lower_q10_dp_beta_1_1 reduces mean target-regime regret versus TRL-log by -0.177525000000, while at least one posterior baseli
- `0010`: Positive transitive evidence: False.
- `0010`: Posterior TRL candidates equivalent to posterior model DP: True.
- `0010`: MC-only heldout MSE minus TRL-log heldout MSE: 0.380607415380.
- `0011`: Positive evidence: False.
- `0011`: Near-equivalence to posterior model DP: True.
- `0011`: Max posterior_trl_log value difference vs posterior model DP: 0.
- `0012`: History MC+TRL-log improves heldout MSE over history MC-only by 1.000000.
- `0012`: Observation TRL-log policy regret minus history MC+TRL-log policy regret: 0.018225000000.
- `0012`: The measured gain is explained by bounded history representation plus model-style propagation.
- `0013`: Cue-sufficient MC+TRL improvement fraction: 1.000000.
- `0013`: Model DP explains all gains: True.
- `0013`: Overall history MC+TRL minus history-model-DP heldout MSE: 0.000000000000.

## Negative Signals

- `0001`: Evidence is intentionally small-scale and balanced: risky outcome coverage exactly matches the true 0.25 success probability, so MC supervised is perfect here and the experiment mainly supports the raw-TRL overestimation...
- `0001`: /home/eston/autoresearcher is not a git repository, so unrelated modifications could not be audited with git status.
- `0002`: The Q overestimation and underestimation maxima are computed across all goals, not only the eval goal, so those headline error fields can reflect non-eval goals such as trap; eval-goal learned/exact Q columns mitigate th...
- `0002`: commands_run records setup, execution, and validation commands but not the manual edits that transformed the copied 0001 script into the 0002 harness.
- `0002`: git status only showed an untracked reviewer packet, but without committed baselines this review cannot fully prove no prior artifacts were modified.
- `0003`: git status shows modified control files including scripts/autoresearcher.py, autoresearcher.yaml, tests/test_phase1.py, and research/sto_trl/state.json. Their mtimes precede the 0003 plan, so they appear pre-existing to...
- `0003`: commands_run records setup, execution, and validation commands, but not the manual edit operation that adapted the copied 0002 script into the 0003 harness.
- `0003`: TRL-log and raw TRL are transitive model-based tabular backups over observed transitions, so they do not consume the same supervised label budget as MC-only; this is intended by the plan but should be kept in mind when i...
- `0004`: successor_distance_trl_log is behaviorally identical or near-identical to trl_log in the saved main metrics, so the result supports the calibration-only versus transitive-relaxation ablation but not a clear advantage ove...
- `0004`: self_normalize_successor_scores divides by max([scores] + [1.0]), which is an identity transform for scores already in [0,1]; successor_calibration_only therefore matches mc_supervised in these runs.
- `0004`: git status still shows modified control/config/test files, including scripts/autoresearcher.py and autoresearcher.yaml. Their mtimes predate the 0004 artifact generation, but the dirty tree means the no-control-file-edit...
- `0005`: Working tree contains pre-existing modified control/config/test files, including scripts/autoresearcher.py, so the no-control-file-edit criterion cannot be proven from git status alone.
- `0005`: commands_run records copy, run, and validation commands, but not any manual edit steps used to adapt the copied 0004 script into the 0005 audit.
- `0005`: A generated __pycache__/ directory exists under artifacts/0005; harmless but extra artifact noise.
- `0006`: The aggregate labels one_sided_conservative_log_trl_alpha_0_20 as best_positive_method even though alpha 0.40 and 0.60 also eliminate lucky-only policy regret; this is a first-positive selection, not a best-by-regret sel...
- `0006`: The interpretation says alpha 0.20 reduced the lucky-only safe-optimal failure, but alpha 0.20 still selects risky with policy regret 0.504; the stronger claim should be limited to reduced overestimation/held-out MSE unl...
- `0006`: The risk_optimal_no_success_stress case remains a biased-coverage failure for trl_log and all conservative alpha values: they select safe with regret 0.081 despite the true risky optimum.
- `0007`: Do not treat 0007 as showing that the generic method fully replaces the 0006 one-sided rule; it only gives modest Q-overestimation reduction without fixing lucky-only policy regret.
- `0007`: known_failures is empty despite risk_optimal_no_success_stress remaining unsolved; this is acceptable for continuation only because the limitation is explicit in metrics and summary.
- `0007`: The current worktree has unrelated uncommitted modifications to scripts/autoresearcher.py, but the 0007 result commit did not include that protected file.
- `0008`: Grid produced 285 ambiguous, lucky-only, no-success, or prior-dependent cells where action choice cannot be justified by empirical frequencies alone.
- `0008`: TRL-log is identical to empirical transition DP on this tabular grid, so failures in those cells are data-identifiability failures rather than implementation-specific TRL-log failures.
- `0008`: Do not use the method_summary rankings as probability-weighted performance claims; the sweep weights each possible observed success count equally.
- `0009`: TRL-log, empirical risky value, and empirical model DP are numerically equivalent for these one-step risky shortcut decisions.
- `0009`: No evaluated transition baseline solved risk_optimal_no_success; explicit priors or additional coverage remain necessary.
- `0009`: Risk-optimal no-success remains unsolved from counts alone.
- `0010`: Matched risk-optimal action preserved by posterior TRL candidates: True.
- `0010`: posterior_trl_log and posterior_mc_plus_trl_log were numerically equivalent to the prior-matched posterior mean model-DP baseline.
- `0010`: No distinct posterior transitive benefit over both TRL-log and prior-matched posterior model DP was detected.
- `0011`: posterior_trl_log and posterior_mc_plus_trl_log were near-equivalent to prior-matched posterior mean model DP across the randomized suite.
- `0011`: No credible posterior TRL benefit over both TRL-log and prior-matched posterior model DP was detected.
- `0011`: The suite is intentionally tiny and tabular; it is suitable for this loop but should not be generalized beyond these toy MDP families.
- `0012`: history_model_dp fully explains the history-keyed MC+TRL-log gain, so this is representation/context evidence rather than a distinct TRL algorithm win.
- `0012`: Only one tiny hand-constructed POMDP with two evaluated alias regimes; generalization evidence is limited.
- `0012`: The bounded history key includes the cue observation, which nearly disambiguates the latent hub by construction, so the result is mainly a representation/context sanity check.
- `0013`: history-model DP fully matches history MC+TRL-log gains, so this is boundary/negative for distinct TRL algorithmic value.
- `0013`: History-model DP exactly explains the history MC+TRL-log gains, so continuing this line as an algorithmic TRL win would be invalid.
- `0013`: The positive cue-sufficient cases rely on observed cue tokens that disambiguate context; this is allowed by the plan but mainly demonstrates representation sufficiency rather than a new learning mechanism.
