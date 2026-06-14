# Decision: continue

Confidence: 0.8
Progress score: 7

## Rationale

Experiment 0009 passed as a compact transition-posterior baseline audit and gives a clear next gate. It showed that posterior and robust transition-model DP baselines can reduce regret versus TRL-log on selected recoverable regimes, while TRL-log remains identical to empirical model DP on the one-step risky shortcut family. The next small experiment should test the approved next milestone: whether adding log-space transitive propagation to posterior transition uncertainty gives any benefit beyond prior-matched posterior model DP on a multi-step tabular diagnostic where transitive propagation can matter.

## Evidence

- 0009 result and review report required result, summary, and all listed artifacts, with result/artifact validation ok.
- 0009 review reports allows_auto_continue=true, success_criteria_satisfied=true, failure_criteria_triggered=false, and should_escalate_to_pro=false.
- Current state reports a Pro decision continue was applied from research/sto_trl/decisions/0010_pro_decision.json, so continuation under the approved plan is not blocked.
- 0009 selected 8 representative regimes covering matched safe, matched risk, lucky-only safe, no-success safe, no-success risk, ambiguous safe, ambiguous risk, and prior-dependent safe cases.
- 0009 reports empirical_model_dp, empirical_risky_value, and trl_log all have mean_policy_regret=0.10901250000000001, so TRL-log did not add distinct value on one-step risky shortcut decisions.
- 0009 reports posterior_lower_q10_dp_beta_1_1 as best_transition_uncertainty_method with target-regime regret delta versus TRL-log of -0.17752500000000004.
- 0009 known_failures states that risk-optimal no-success remains unsolved from counts alone, and no_success_risk_optimal_solved_methods is empty.
- 0009 review warns that the positive transition-baseline evidence rests on four target cells and an 8-cell handpicked subset, so it should set a baseline rather than support broad generalization.
- The human-approved next-step plan calls for transition-posterior TRL after transition-level posterior baselines, with a critical ablation against transition uncertainty alone.

## Risks

- Posterior transitive propagation may collapse to posterior model DP in tabular exact settings; equivalence should be reported as negative or boundary evidence.
- Any apparent improvement could come from the prior rather than transitive propagation, so all posterior TRL variants must be compared against prior-matched posterior model DP.
- Conservative posterior choices can look good by avoiding risk; matched risk-optimal and ambiguous risk-optimal regimes must be explicit checks.
- Keep the experiment tabular and small; do not move to neural networks, continuous control, OGBench, downloads, or broad sweeps.
- The deterministic chain guard should be a real raw/log TRL execution check if practical, not only a formula check.

## Next experiment

- Experiment id: `0010`
- Objective: Test whether posterior transition uncertainty plus log-space transitive propagation adds value beyond transition-model DP on a small multi-step tabular stochastic branch-chain diagnostic.
