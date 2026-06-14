# Decision: continue

Confidence: 0.84
Progress score: 6

## Rationale

The latest accepted evidence does not justify more algorithm tweaking, but the human pivot note explicitly approves a reframed direction and recommends a small identifiability and coverage grid. That is the right next experiment: it tests what finite offline stochastic coverage can and cannot identify before adding posterior transition models or more TRL variants. This remains tabular, exact-DP evaluable, and should be cheaper and more decisive than another method sweep.

## Evidence

- The human pivot note research/sto_trl/progress/human_pivot_0008.md says to continue only under the reframed question: transition-level stochastic uncertainty plus log-space transitive propagation under finite offline stochastic coverage.
- The same human pivot note recommends the next experiment: sweep true risky success probability, safe path length, risky sample count, and observed risky successes; compare empirical risky value, posterior means/quantiles, lower/upper confidence choices, TRL-log, and raw TRL.
- 0007 result and review are present and accepted as weak_pass, with validation reported ok and allows_auto_continue=true.
- 0007 review says the generic method only gives modest Q-overestimation reduction, does not fix safe_optimal_lucky_only policy regret, and remains worse than the 0006 one-sided alpha 0.40 comparison on that stress case.
- 0007 aggregate reports trl_log_safe_lucky_policy_regret=0.504, one_sided_0006_safe_lucky_policy_regret=0.0, and risk_optimal_no_success_unsolved_by_best_positive=true.
- Prior 0005 evidence remains negative for the original successor-distance formulation: improving successor-distance lambdas were equivalent to trl_log and any_positive_successor_evidence=false.
- The environment state is ready and the proposed grid is tabular with exact DP ground truth, so it stays within the charter's initial scope and compute budget.

## Risks

- The grid must not be interpreted as an algorithm win; its value is identifying solvable, ambiguous, and impossible coverage regimes.
- If the grid is too broad it could become low-value exploration; keep it small enough to finish within 30 minutes and save all raw cells.
- Posterior or confidence-choice baselines encode assumptions; the result must label which conclusions depend on priors versus observed data.
- Do not move to neural networks, OGBench, PointMaze, AntMaze, downloads, or larger training from this step.
- The executor should avoid protected files and preserve previous artifacts, especially given prior review flags about unrelated control-file modifications.

## Next experiment

- Experiment id: `0008`
- Objective: Run a small tabular identifiability and coverage grid that maps when risky-shortcut action choice is identifiable from finite offline stochastic coverage, before adding new stochastic TRL algorithms.
