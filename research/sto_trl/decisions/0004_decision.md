# Decision: continue

Confidence: 0.82
Progress score: 6

## Rationale

Experiment 0003 is a valid weak-pass result with useful evidence: log transitive backups recovered censored long-horizon tabular reachability and avoided raw TRL's matched risky-shortcut optimism. The remaining charter-critical question is whether a first stochastic-calibrated successor-distance style variant adds anything beyond empirical log backups and calibration-only baselines, without becoming conservative on risk-optimal cases. That is a small tabular Milestone 3 experiment, still within the initial scope.

## Evidence

- research/sto_trl/results/0003_result.json validates against schemas/result.schema.json with artifact checks.
- 0003 status is completed with no known_failures and success_criteria_met=true.
- 0003 aggregate metrics show chain held-out value MSE improved from MC 0.3917058232298766 to TRL-log and MC+TRL-log 2.9347503914472164e-34.
- 0003 risky matched metrics show MC selected risky with policy_regret=0.504, raw TRL selected risky with policy_regret=0.504, while TRL-log and MC+TRL-log selected safe with zero policy regret.
- The 0003 review allows auto-continue but flags that TRL-log/raw are tabular transitive backups over observed transitions rather than the same supervised label budget as MC-only, so a calibration-only versus calibrated+transitive ablation is the right next test.
- The prototype plan's Milestone 3 calls for a first stochastic-calibrated variant: contrastive successor-distance or self-normalized successor score, Successor-distance + TRL-log, and comparison against calibration-only.

## Risks

- A self-normalized successor variant may collapse to the same empirical log backup already tested; require saved value tables and method definitions that distinguish calibration-only from calibrated+transitive.
- No tabular method can infer missing stochastic outcomes without assumptions, so lucky-only or no-success regimes should be reported as boundary cases rather than hidden or overclaimed.
- A conservative variant can look good on safe-optimal shortcuts while failing risk-optimal shortcuts; include an anti-conservatism check.
- Keep this tabular and small; do not move to OGBench, neural networks, downloads, or broad sweeps yet.

## Next experiment

- Experiment id: `0004`
- Objective: Implement and test the first tabular stochastic-calibrated successor-distance variant, comparing calibration-only against successor-distance + TRL-log on the existing horizon-holdout and risky-shortcut diagnostics.
