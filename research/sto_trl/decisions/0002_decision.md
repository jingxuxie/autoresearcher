# Decision: continue

Confidence: 0.86
Progress score: 3

## Rationale

Experiment 0001 is valid and tests the main early hypothesis, but it is still a matched-coverage toy case: the risky dataset used 2 successes and 6 failures, exactly matching the true 0.25 risky success probability. The next high-information step is a small tabular coverage-sensitivity stress test to determine whether the raw-TRL failure is robust and whether empirical log/MC methods only look good when observed stochastic outcomes match ground truth.

## Evidence

- Artifact validation for research/sto_trl/results/0001_result.json completed successfully against schemas/result.schema.json with artifact checks.
- The 0001 result reports deterministic-chain sanity passed for trl_raw and trl_log with zero value error and zero policy regret.
- On risky_shortcut, trl_raw learned risky Q=0.9 versus exact risky Q=0.225, selected risky, and incurred policy_regret=0.504.
- On the same risky_shortcut dataset, trl_log, mc_supervised, and mc_plus_trl_log were perfect because the offline risky outcomes exactly matched the true 2/8 success rate.
- The 0001 code shows train_trl_raw maximizes over observed next states while train_trl_log uses empirical transition counts, making coverage imbalance the obvious next confound to test.

## Risks

- A larger sweep could become activity without insight; keep the grid tiny and predeclared.
- Empirical log-space backups may fail under lucky-only or biased coverage, which would be a useful boundary rather than a reason to hide the result.
- Do not introduce oracle access to true transition probabilities in training methods; exact DP should remain evaluation-only ground truth.
- A method that avoids all risky actions is not enough; the next test must include a configuration where the risky action is truly optimal.

## Next experiment

- Experiment id: `0002`
- Objective: Run a small tabular coverage-sensitivity stress test for the risky shortcut diagnostic, including both risk-suboptimal and risk-optimal settings, to check whether raw TRL overestimation and log/MC calibration claims survive biased or sparse stochastic outcome coverage.
