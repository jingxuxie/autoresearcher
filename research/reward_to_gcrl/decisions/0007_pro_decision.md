# ChatGPT Pro Decision: continue

Confidence: 0.86

## Rationale

Continue with one more small CPU-tabular RiverSwim experiment before moving to auxiliary goals. The project is now making real progress toward the overall research goal: drift is cleared, 0004 supplied a nondegenerate small-chain result, 0005 gave a strong controlled RiverSwim propagation result, and 0006 removed exact-Q-guided behavior while preserving the estimator story. The remaining blocker is not whether the soft estimator reduces terminal-sampling variance; that is well supported. The open question is whether the learning advantage is robust once coverage is non-oracle but not starved. A coverage-controlled RiverSwim dose-response test is the cheapest decisive next step.

## Evidence

- The latest summary reports protected_file_drift is false and there is no current blocker.
- 0001 validated the estimator premise: sampled and soft terminal targets matched means while soft terminal variance was zero or negligible.
- 0002 confirmed tabular scaling equivalence in audited CliffWalking below the 1e-6 threshold.
- 0004 accepted the repaired nondegenerate 5-state chain result: soft had lower Bellman residual and value error and achieved success where sampled failed.
- 0005 passed on 6-state RiverSwim with exact-Q-guided behavior: sampled target means matched deterministic soft marginal targets in all 30 runs, sampled variance exceeded soft variance in all 30 runs, and soft residual dominance held in all runs.
- 0006 passed with non-oracle behavior streams: sampled targets remained unbiased within tolerance and higher variance without exact-Q-guided behavior.
- The main 0006 caveat is coverage: half the runs were coverage-starved, and under poor coverage soft could have lower Bellman residual but worse value error than sampled.
- No auxiliary-goal, neural, FourRooms, larger RiverSwim, or offline fitted-learning evidence exists yet.

## Risks

- A further RiverSwim run could become redundant if it only repeats the variance result without clarifying coverage dependence.
- Coverage-controlled behavior policies may still be too artificial to support online-control claims.
- If adequate coverage is achieved by hand-designed behavior, the result remains matched-stream estimator evidence, not full exploration evidence.
- Moving to auxiliary goals before bounding the coverage caveat could make later representation-learning results hard to interpret.
- All current evidence is still tiny tabular evidence, so even a positive 0007 should not be overclaimed as a general GCRL solution.

## Next experiment

- Experiment id: `0007`
- Objective: Run a CPU-only tabular RiverSwim coverage dose-response experiment that uses several non-oracle behavior policies to create starved, borderline, and adequate coverage regimes, then quantify exactly when deterministic soft terminal marginalization improves Bellman residual, value error, and policy quality over sampled augmented updates.
