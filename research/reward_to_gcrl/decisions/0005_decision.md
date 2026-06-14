# Decision: continue

Confidence: 0.79
Progress score: 5

## Rationale

The 0004 evidence-integrity blocker has been resolved and the repaired nondegenerate chain result is accepted as weak but useful evidence. It supports the estimator-variance and learning-improvement story in a tiny controlled task, but the result is still too narrow to justify auxiliary goals or function approximation. The next small, high-information step is to test the same sampled-vs-soft claim on a small stochastic RiverSwim chain, which is explicitly in the charter's initial scope and probes long-horizon reward propagation without expensive training.

## Evidence

- research/reward_to_gcrl/results/0004_result.json is present, schema-valid, and reports status completed with exact commands and declared artifacts.
- research/reward_to_gcrl/reviews/0004_review.json reports allows_auto_continue=true, success_criteria_satisfied=true, and no triggered failure criteria.
- 0004 records drift_status=harmless and evidence_integrity_verdict=accepted_evidence after a protected-file drift audit, with post-audit schema and artifact validation marked passed.
- 0004 uses identity reward normalization in a nondegenerate 5-state chain, avoiding the CliffWalking objective mismatch from 0002/0003.
- 0004 reports sampled target means matching deterministic soft marginal targets, sampled variance exceeding soft variance in all runs, and lower mean final soft Bellman/value error with soft success rate 1.0 versus sampled success rate 0.0.
- The reviewer still flags that 0004 is only a tiny controlled matched-stream chain, so broader environments remain untested.
- The charter's initial scope includes small RiverSwim chains for long-horizon reward propagation before larger grids or neural training.

## Risks

- RiverSwim learning can confound estimator variance with exploration difficulty; use matched transition streams plus exact DP references to keep the test interpretable.
- If the behavior stream rarely reaches the rewarding right end, both learners may fail for coverage reasons rather than estimator reasons; coverage and reward-event counts must be reported.
- A positive RiverSwim result would still be tabular evidence only, not evidence for auxiliary goals or neural representation learning.
- The sampled augmented update must again avoid an extra gamma factor on continued sampled transitions and must mask sampled absorbing events correctly.

## Next experiment

- Experiment id: `0005`
- Objective: Run a CPU-only tabular sampled-vs-soft diagnostic on a small stochastic RiverSwim chain to test long-horizon reward propagation under sparse right-end rewards.
