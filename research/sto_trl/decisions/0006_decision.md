# Decision: pivot

Confidence: 0.82
Progress score: 6

## Rationale

The latest valid result weakens the specific successor-distance variant: 0005 found that all improving successor-distance lambdas were numerically equivalent to trl_log, so it does not add distinct evidence. However, the results reveal a nearby cheap test: uncertainty-aware or one-sided conservative log-TRL aimed at the biased lucky-only coverage failure that raw/log/successor variants still share.

## Evidence

- 0005 result and review report valid result, summary, and artifacts with schema validation passing.
- 0005 metrics report any_positive_successor_evidence=false and negative_equivalence_evidence=true.
- 0005 aggregate reports all_improving_lambdas_equivalent_to_trl_log=true under equivalence_tolerance=1e-10.
- 0005 summary says improving successor-distance lambdas reduced held-out error only by matching trl_log within tolerance.
- The safe_optimal_lucky_only_stress scenario remains unresolved: trl_log, mc_plus_trl_log, and successor-distance variants select risky with policy_regret=0.504.
- Earlier tabular results still show a real target: raw TRL is support-optimistic under stochastic lucky paths, and log TRL improves long-horizon holdout under matched coverage.

## Risks

- A conservative penalty could appear to fix safe-optimal lucky-only by avoiding all risky actions, so risk_optimal_matched must be a hard anti-conservatism check.
- Unobserved stochastic failures cannot be inferred without an explicit assumption; the uncertainty penalty must use only offline coverage statistics and state that assumption clearly.
- A penalty grid can be overfit if only best results are reported; require the full predeclared grid and negative outcomes.
- Do not move to function approximation, OGBench, downloads, or broad sweeps while the tabular biased-coverage failure remains unresolved.

## Next experiment

- Experiment id: `0006`
- Objective: Test a minimal uncertainty-aware or one-sided conservative log-TRL backup on the tabular biased-coverage failure while preserving matched safe-optimal, matched risk-optimal, and deterministic long-horizon behavior.
