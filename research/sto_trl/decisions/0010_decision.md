# Decision: continue

Confidence: 0.78
Progress score: 7

## Rationale

Experiment 0009 established the transition-posterior baseline gate on a representative tabular subset. It showed that posterior and robust transition-model DP can reduce regret versus TRL-log in recoverable finite-coverage regimes, while TRL-log is equivalent to empirical model DP on the one-step risky shortcut family. The next small decisive step is the planned Milestone 3 ablation: add posterior transition uncertainty to log-space transitive propagation in a setting where multi-step propagation could matter, and require comparison against transition-model DP so any gain is not just a prior choice.

## Evidence

- 0009 result and review report required result, summary, and artifacts, with result/artifact validation ok and allows_auto_continue=true.
- 0009 selected 8 representative cells covering matched safe, matched risk, lucky-only safe, no-success safe, no-success risk, ambiguous safe, ambiguous risk, and prior-dependent safe regimes.
- 0009 reports empirical_model_dp, empirical_risky_value, and trl_log have identical mean_policy_regret=0.10901250000000001 on the representative subset, showing no distinct transitive benefit on the one-step risky shortcut family.
- 0009 reports posterior_lower_q10_dp_beta_1_1 as best_transition_uncertainty_method with target-regime regret delta versus TRL-log of -0.17752500000000004.
- 0009 reports transition_baseline_positive=true, but no_success_risk_optimal_solved_methods is empty and known_failures includes risk-optimal no-success remains unsolved from counts alone.
- 0009 review warns that the positive evidence rests on four target cells and an 8-cell handpicked subset, so it should set a baseline rather than support broad generalization.
- The human-approved next-step plan explicitly moves from transition-level posterior baselines to adding transitive propagation to posterior transition models, with a critical ablation against transition uncertainty alone.

## Risks

- Posterior transitive propagation may collapse to posterior model DP in fully tabular settings; the experiment must treat equivalence as negative or boundary evidence, not success.
- Any apparent win can come from prior choice rather than TRL-style propagation; require prior-matched comparisons against posterior model DP.
- A conservative posterior method can reduce risky overestimation by avoiding risk everywhere; matched risk-optimal and ambiguous risk-optimal regimes must be hard checks.
- Keep the experiment small and tabular; do not move to neural networks, continuous control, OGBench, downloads, or broad sweeps.
- The chain guard should be a real raw/log TRL execution check rather than only a formula check if feasible within the small harness.

## Next experiment

- Experiment id: `0010`
- Objective: Test whether posterior transition uncertainty plus log-space transitive propagation adds value beyond transition-model DP on a small multi-step tabular stochastic branch-chain diagnostic.
