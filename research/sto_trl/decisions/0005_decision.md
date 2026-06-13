# Decision: continue

Confidence: 0.8
Progress score: 6

## Rationale

Experiment 0004 is valid but only a weak positive for the successor-distance direction. It shows calibrated+transitive beats calibration-only on the tabular main scenarios, but the review and code indicate successor_calibration_only is effectively MC-supervised and successor_distance_trl_log is behaviorally near-identical to trl_log. The next cheap decisive experiment should audit whether the successor-distance formulation has any distinct effect across transitive weights before moving to function approximation or larger tasks.

## Evidence

- research/sto_trl/results/0004_result.json validates against schemas/result.schema.json with artifact checks.
- 0004 success checks report successor_distance_improves_main_heldout_mse_vs_calibration_only=true and no matched policy-regret or Q-overestimation increase versus calibration-only.
- 0004 aggregate metrics show successor_calibration_only main mean held-out MSE 0.21524060774329223 versus successor_distance_trl_log 9.782501304824055e-35.
- 0004 matched safe-optimal metrics show successor_distance_trl_log selected safe with zero policy regret, while calibration-only selected risky with policy_regret=0.504.
- 0004 matched risk-optimal metrics show successor_distance_trl_log selected risky with zero policy regret, so it did not simply avoid risk under matched coverage.
- The 0004 review flags two key weaknesses: successor_distance_trl_log is near-identical to trl_log in the main metrics, and self_normalize_successor_scores is an identity transform for scores already in [0,1].
- The 0004 lucky-only stress scenario remains a failure case: successor_distance_trl_log selected risky with policy_regret=0.504 under biased safe-optimal coverage.

## Risks

- Continuing without an equivalence audit could mistake ordinary trl_log behavior for evidence supporting a distinct successor-distance method.
- A lambda sweep can become low-value if it only repeats calibration-only comparisons; require explicit distance-to-trl_log diagnostics.
- No tabular method should be expected to solve missing-outcome lucky-only coverage without an uncertainty assumption, so that stress case should be used as a boundary diagnostic, not a sole success criterion.
- Do not move to OGBench, neural networks, or broad sweeps while the tabular method distinction is unresolved.

## Next experiment

- Experiment id: `0005`
- Objective: Run a small successor-distance lambda and equivalence audit to determine whether successor_distance_trl_log has a distinct effect beyond trl_log and calibration-only on the existing tabular chain and risky-shortcut diagnostics.
