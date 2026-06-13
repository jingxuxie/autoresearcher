# Decision: continue

Confidence: 0.84
Progress score: 5

## Rationale

Experiment 0002 is valid and informative: it confirms raw TRL's support-driven stochastic overestimation, and it also weakens the simpler empirical MC/log story by showing those methods depend heavily on branch coverage and can be overoptimistic or too conservative. The next cheap decisive test should isolate the other core claim: whether TRL-style log transitive backups actually improve long-horizon generalization over MC calibration when long-horizon labels are withheld, while preserving the stochastic branch behavior under matched coverage.

## Evidence

- research/sto_trl/results/0002_result.json validates against schemas/result.schema.json with artifact checks.
- 0002 success checks report deterministic chain raw/log recovery, all predeclared risky regimes present, raw_policy_is_support_driven=true, and trl_log_is_optimal_on_matched_regimes=true.
- 0002 aggregate metrics show raw TRL selected risky in 8/8 scenarios with observed risky success and 0/2 scenarios with no observed success, confirming the support-driven failure mode.
- 0002 shows empirical MC/log methods are only calibrated in matched regimes: they choose risky incorrectly in safe_optimal__lucky_only and choose safe incorrectly in risk_optimal__unlucky_biased and risk_optimal__no_risky_success.
- The charter still requires evidence that log or MC+TRL-log improves long-horizon estimates over MC-only without breaking deterministic sanity checks before moving beyond tabular diagnostics.

## Risks

- Do not treat 0002 as proving stochastic calibration; it shows empirical log/MC calibration is coverage-dependent.
- A horizon-holdout test can leak labels if the script computes MC targets from all future states; it must explicitly censor long-horizon training labels and save train/eval pair coverage.
- If the next experiment only repeats matched risky coverage without long-horizon label withholding, it will not test the remaining TRL horizon-generalization claim.
- Exact DP must remain evaluation-only ground truth, not a training target.

## Next experiment

- Experiment id: `0003`
- Objective: Run a small tabular horizon-holdout experiment that censors long-horizon goal labels during training and tests whether TRL-log or MC+TRL-log can recover long-horizon discounted reachability better than MC-only while retaining matched stochastic risky-branch calibration.
