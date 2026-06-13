# Experiment 0005 Summary

## Objective

Audit whether successor-distance + TRL-log has a distinct tabular effect beyond calibration-only and trl_log.

## Commands Run

```bash
mkdir -p research/sto_trl/artifacts/0005 research/sto_trl/results && cp research/sto_trl/artifacts/0004/run_successor_distance.py research/sto_trl/artifacts/0005/run_lambda_equivalence_audit.py
conda run -n autoresearcher_sto_trl python research/sto_trl/artifacts/0005/run_lambda_equivalence_audit.py
conda run -n autoresearcher_sto_trl python scripts/validate_artifacts.py --repo-root . --json research/sto_trl/results/0005_result.json --schema schemas/result.schema.json --check-result-artifacts
```

## Setup

- Discount: `0.9`
- Label horizon cutoff: `2`
- Fixed backup iterations: `32`
- Lambda sweep: `[0.0, 0.25, 0.5, 0.75, 1.0]`
- Equivalence tolerance: `1e-10`
- Main scenarios: chain holdout, matched safe-optimal risky shortcut, matched risk-optimal risky shortcut.
- Stress scenario: safe-optimal lucky-only risky shortcut.

## Main Metrics

| Scenario | Method | Lambda | Held-out MSE | Q calibration | Policy regret | Action | Triangle violation |
| --- | --- | ---: | ---: | ---: | ---: | --- | ---: |
| chain_len9_holdout | mc_supervised | None | 0.391705823230 | 0.465607869047 | 0.000000000000 | right | 0.166667 |
| chain_len9_holdout | trl_raw | None | 0.000000000000 | 0.000000000000 | 0.000000000000 | right | 0.000000 |
| chain_len9_holdout | trl_log | None | 0.000000000000 | 0.000000000000 | 0.000000000000 | right | 0.000000 |
| chain_len9_holdout | mc_plus_trl_log | None | 0.000000000000 | 0.131258278195 | 0.000000000000 | right | 0.000000 |
| chain_len9_holdout | successor_calibration_only | 0.0 | 0.391705823230 | 0.465607869047 | 0.000000000000 | right | 0.166667 |
| chain_len9_holdout | successor_distance_trl_log_lambda_0_00 | 0.0 | 0.391705823230 | 0.465607869047 | 0.000000000000 | right | 0.166667 |
| chain_len9_holdout | successor_distance_trl_log_lambda_0_25 | 0.25 | 0.000000000000 | 0.000000000000 | 0.000000000000 | right | 0.000000 |
| chain_len9_holdout | successor_distance_trl_log_lambda_0_50 | 0.5 | 0.000000000000 | 0.000000000000 | 0.000000000000 | right | 0.000000 |
| chain_len9_holdout | successor_distance_trl_log_lambda_0_75 | 0.75 | 0.000000000000 | 0.000000000000 | 0.000000000000 | right | 0.000000 |
| chain_len9_holdout | successor_distance_trl_log_lambda_1_00 | 1.0 | 0.000000000000 | 0.000000000000 | 0.000000000000 | right | 0.000000 |
| safe_optimal_matched | mc_supervised | None | 0.254016000000 | 0.045562500000 | 0.504000000000 | risky | 0.375000 |
| safe_optimal_matched | trl_raw | None | 0.029241000000 | 0.056250000000 | 0.504000000000 | risky | 0.000000 |
| safe_optimal_matched | trl_log | None | 0.000000000000 | 0.000000000000 | 0.000000000000 | safe | 0.250000 |
| safe_optimal_matched | mc_plus_trl_log | None | 0.000000000000 | 0.000000000000 | 0.000000000000 | safe | 0.250000 |
| safe_optimal_matched | successor_calibration_only | 0.0 | 0.254016000000 | 0.045562500000 | 0.504000000000 | risky | 0.375000 |
| safe_optimal_matched | successor_distance_trl_log_lambda_0_00 | 0.0 | 0.254016000000 | 0.045562500000 | 0.504000000000 | risky | 0.375000 |
| safe_optimal_matched | successor_distance_trl_log_lambda_0_25 | 0.25 | 0.000000000000 | 0.000000000000 | 0.000000000000 | safe | 0.250000 |
| safe_optimal_matched | successor_distance_trl_log_lambda_0_50 | 0.5 | 0.000000000000 | 0.000000000000 | 0.000000000000 | safe | 0.250000 |
| safe_optimal_matched | successor_distance_trl_log_lambda_0_75 | 0.75 | 0.000000000000 | 0.000000000000 | 0.000000000000 | safe | 0.250000 |
| safe_optimal_matched | successor_distance_trl_log_lambda_1_00 | 1.0 | 0.000000000000 | 0.000000000000 | 0.000000000000 | safe | 0.250000 |
| risk_optimal_matched | mc_supervised | None | 0.000000000000 | 0.045562500000 | 0.000000000000 | risky | 0.250000 |
| risk_optimal_matched | trl_raw | None | 0.000000000000 | 0.056250000000 | 0.000000000000 | risky | 0.000000 |
| risk_optimal_matched | trl_log | None | 0.000000000000 | 0.000000000000 | 0.000000000000 | risky | 0.250000 |
| risk_optimal_matched | mc_plus_trl_log | None | 0.000000000000 | 0.000000000000 | 0.000000000000 | risky | 0.250000 |
| risk_optimal_matched | successor_calibration_only | 0.0 | 0.000000000000 | 0.045562500000 | 0.000000000000 | risky | 0.250000 |
| risk_optimal_matched | successor_distance_trl_log_lambda_0_00 | 0.0 | 0.000000000000 | 0.045562500000 | 0.000000000000 | risky | 0.250000 |
| risk_optimal_matched | successor_distance_trl_log_lambda_0_25 | 0.25 | 0.000000000000 | 0.000000000000 | 0.000000000000 | risky | 0.250000 |
| risk_optimal_matched | successor_distance_trl_log_lambda_0_50 | 0.5 | 0.000000000000 | 0.000000000000 | 0.000000000000 | risky | 0.250000 |
| risk_optimal_matched | successor_distance_trl_log_lambda_0_75 | 0.75 | 0.000000000000 | 0.000000000000 | 0.000000000000 | risky | 0.250000 |
| risk_optimal_matched | successor_distance_trl_log_lambda_1_00 | 1.0 | 0.000000000000 | 0.000000000000 | 0.000000000000 | risky | 0.250000 |
| safe_optimal_lucky_only_stress | mc_supervised | None | 0.029241000000 | 0.129937500000 | 0.504000000000 | risky | 0.000000 |
| safe_optimal_lucky_only_stress | trl_raw | None | 0.029241000000 | 0.084375000000 | 0.504000000000 | risky | 0.000000 |
| safe_optimal_lucky_only_stress | trl_log | None | 0.029241000000 | 0.084375000000 | 0.504000000000 | risky | 0.000000 |
| safe_optimal_lucky_only_stress | mc_plus_trl_log | None | 0.029241000000 | 0.084375000000 | 0.504000000000 | risky | 0.000000 |
| safe_optimal_lucky_only_stress | successor_calibration_only | 0.0 | 0.029241000000 | 0.129937500000 | 0.504000000000 | risky | 0.000000 |
| safe_optimal_lucky_only_stress | successor_distance_trl_log_lambda_0_00 | 0.0 | 0.029241000000 | 0.129937500000 | 0.504000000000 | risky | 0.000000 |
| safe_optimal_lucky_only_stress | successor_distance_trl_log_lambda_0_25 | 0.25 | 0.029241000000 | 0.084375000000 | 0.504000000000 | risky | 0.000000 |
| safe_optimal_lucky_only_stress | successor_distance_trl_log_lambda_0_50 | 0.5 | 0.029241000000 | 0.084375000000 | 0.504000000000 | risky | 0.000000 |
| safe_optimal_lucky_only_stress | successor_distance_trl_log_lambda_0_75 | 0.75 | 0.029241000000 | 0.084375000000 | 0.504000000000 | risky | 0.000000 |
| safe_optimal_lucky_only_stress | successor_distance_trl_log_lambda_1_00 | 1.0 | 0.029241000000 | 0.084375000000 | 0.504000000000 | risky | 0.000000 |

## Audit Classification

- Chain raw exact: `True`
- Chain TRL-log exact: `True`
- Positive successor-distance evidence: `False`
- Negative equivalence evidence: `True`
- All improving lambdas equivalent to trl_log: `True`

## Interpretation

The audit found negative successor-distance evidence: improving lambdas reduced held-out error by matching trl_log within the predeclared tolerance, so this variant is not yet distinct from trl_log on these tabular diagnostics.

## Artifacts

- `research/sto_trl/artifacts/0005/run_lambda_equivalence_audit.py`
- `research/sto_trl/artifacts/0005/raw_metrics.json`
- `research/sto_trl/artifacts/0005/metrics.csv`
- `research/sto_trl/artifacts/0005/lambda_sweep.json`
- `research/sto_trl/artifacts/0005/equivalence_diagnostics.json`
- `research/sto_trl/artifacts/0005/successor_distance_tables.json`
- `research/sto_trl/artifacts/0005/distance_diagnostics.json`
- `research/sto_trl/artifacts/0005/label_or_pair_coverage.json`
- `research/sto_trl/artifacts/0005/offline_datasets.json`
- `research/sto_trl/artifacts/0005/transition_tables.json`
- `research/sto_trl/artifacts/0005/value_tables.json`

## Known Failures

- None.
