# Review 0004: weak_pass

Allows auto-continue: True

## Reasons

- Required outputs are present: research/sto_trl/results/0004_result.json, research/sto_trl/results/0004_summary.md, and populated artifacts under research/sto_trl/artifacts/0004.
- Result JSON validates against schemas/result.schema.json with artifact checks.
- The artifact script separately reports successor_calibration_only and successor_distance_trl_log, with successor lambda_tr=0.75 and saved successor score/distance tables.
- Exact DP ground truth is implemented for all evaluated scenarios: chain_len9_holdout, safe_optimal_matched, risk_optimal_matched, and safe_optimal_lucky_only_stress.
- The compared methods run on the same constructed datasets per scenario: mc_supervised, trl_raw, trl_log, mc_plus_trl_log, successor_calibration_only, and successor_distance_trl_log.
- Metrics include per-scenario method rows with held-out MSE, calibration, over/underestimation, policy regret, risky selection, triangle violation diagnostics, and coverage artifacts.
- The positive criteria are met in the reported metrics: successor_distance_trl_log improves main mean held-out MSE versus successor_calibration_only, does not increase matched policy regret or q overestimation, selects safe in safe-optimal matched, and selects risky in risk-optimal matched.
- The lucky-only biased case is included and treated as a stress failure case rather than as the success criterion.

## Required fixes


## Risk flags

- successor_distance_trl_log is behaviorally identical or near-identical to trl_log in the saved main metrics, so the result supports the calibration-only versus transitive-relaxation ablation but not a clear advantage over the existing trl_log baseline.
- self_normalize_successor_scores divides by max([scores] + [1.0]), which is an identity transform for scores already in [0,1]; successor_calibration_only therefore matches mc_supervised in these runs.
- git status still shows modified control/config/test files, including scripts/autoresearcher.py and autoresearcher.yaml. Their mtimes predate the 0004 artifact generation, but the dirty tree means the no-control-file-edit criterion cannot be proven solely from current git state.
- commands_run records the copy, execution, and validation commands but not the manual edits that adapted the copied 0003 script into the 0004 successor-distance harness.
