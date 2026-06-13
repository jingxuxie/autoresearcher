# Decision: pivot

Confidence: 0.82
Progress score: 6

## Rationale

Experiment 0005 is valid and is negative for the distinct successor-distance variant: every improving successor-distance lambda collapsed to trl_log within the predeclared tolerance. That weakens the original successor-distance formulation but reveals a nearby, charter-aligned testable idea: an uncertainty-aware or conservative log-TRL backup aimed specifically at the biased lucky-only coverage failure that trl_log and successor_distance_trl_log both share.

## Evidence

- 0005 result JSON is reported as schema-valid with artifact checks and review verdict pass.
- 0005 aggregate metrics report any_positive_successor_evidence=false, negative_equivalence_evidence=true, and all_improving_lambdas_equivalent_to_trl_log=true.
- For lambda_tr in {0.25, 0.5, 0.75, 1.0}, successor_distance_trl_log improved over calibration-only but was equivalent to trl_log on all main scenarios within tolerance 1e-10.
- The safe_optimal_lucky_only_stress scenario still failed: trl_log, mc_plus_trl_log, and all improving successor-distance lambdas selected risky with policy_regret=0.504.
- Earlier results still support a real target: raw TRL is support-optimistic on stochastic lucky paths, and log TRL improves long-horizon tabular holdout under matched branch coverage.
- The project plan lists uncertainty-aware TRL and conservative or one-sided backups as pivot options when current stochastic-calibrated variants are mixed or collapse to simpler baselines.

## Risks

- A conservative backup may only avoid all risky actions; the experiment must include a matched risk-optimal scenario and count that as a hard anti-conservatism check.
- No method can infer unobserved failures from lucky-only data without an explicit uncertainty assumption, so the assumption must be stated and stress-tested rather than hidden.
- If uncertainty penalties are tuned on the same lucky-only case used for evaluation, the result will be weak; use a tiny predeclared penalty grid and report all outcomes.
- Do not move to function approximation, OGBench, downloads, or broad sweeps until this tabular biased-coverage failure has a clear outcome.

## Next experiment

- Experiment id: `0006`
- Objective: Test a minimal uncertainty-aware or one-sided conservative log-TRL backup on the tabular biased-coverage failure, while preserving matched safe-optimal and matched risk-optimal behavior.
