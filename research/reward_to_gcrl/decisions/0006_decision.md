# Decision: continue

Confidence: 0.84
Progress score: 6

## Rationale

0005 is a strong reviewed pass for the sampled-vs-soft claim in small stochastic RiverSwim, but it used exact-Q-guided behavior. The next small decisive test should hold the RiverSwim setup fixed and remove that oracle coverage source before moving to auxiliary goals or function approximation.

## Evidence

- 0005_result.json reports status completed with exact commands and declared artifacts.
- 0005_review.json reports verdict pass, evidence_quality strong, allows_auto_continue true, and no triggered failure criteria.
- 0005 used CPU-only tabular code on a 6-state stochastic continuing RiverSwim chain with rewards normalized to [0,1].
- Across 30 runs, sampled target means matched deterministic soft marginal targets, sampled variance exceeded soft variance, and soft residual dominance was reported in all runs.
- The key reviewer caveat is that behavior was epsilon-greedy with respect to exact normalized-Q greedy actions, so 0005 is a controlled propagation test rather than a non-oracle exploration test.

## Risks

- Non-oracle RiverSwim may have poor right-end coverage; coverage-starved failures should not be overinterpreted as estimator failure.
- Independent learner behavior would confound exploration with estimator variance, so use matched logged streams generated without exact-Q guidance.
- Do not move to neural approximation or auxiliary goals until this oracle-behavior caveat is bounded.

## Next experiment

- Experiment id: `0006`
- Objective: Repeat the 6-state RiverSwim sampled-vs-soft diagnostic using non-oracle exploratory behavior streams.
