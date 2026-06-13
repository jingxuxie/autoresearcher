# Experiment 0006 Summary

## Objective

Test a one-sided conservative log-TRL backup on biased stochastic coverage while preserving matched and deterministic behavior.

## Commands Run

```bash
mkdir -p research/sto_trl/artifacts/0006 research/sto_trl/results && cp research/sto_trl/artifacts/0005/run_lambda_equivalence_audit.py research/sto_trl/artifacts/0006/run_uncertainty_conservative_log_trl.py
conda run -n autoresearcher_sto_trl python research/sto_trl/artifacts/0006/run_uncertainty_conservative_log_trl.py
conda run -n autoresearcher_sto_trl python scripts/validate_artifacts.py --repo-root . --json research/sto_trl/results/0006_result.json --schema schemas/result.schema.json --check-result-artifacts
```

## Setup

- Discount: `0.9`
- Label horizon cutoff: `2`
- Fixed backup iterations: `32`
- Alpha grid: `[0.0, 0.2, 0.4, 0.6]`
- Conservative penalty: `alpha * gamma / sqrt(count)` for direct-goal single-branch shortcut actions at multi-action states with count at least 4.

## Metrics

| Scenario | Method | Alpha | Held-out MSE | Q calibration | Policy regret | Action | Risky selected |
| --- | --- | ---: | ---: | ---: | ---: | --- | ---: |
| chain_len9_holdout | mc_supervised | None | 0.391705823230 | 0.465607869047 | 0.000000000000 | right | 0.0 |
| chain_len9_holdout | trl_raw | None | 0.000000000000 | 0.000000000000 | 0.000000000000 | right | 0.0 |
| chain_len9_holdout | trl_log | None | 0.000000000000 | 0.000000000000 | 0.000000000000 | right | 0.0 |
| chain_len9_holdout | mc_plus_trl_log | None | 0.000000000000 | 0.131258278195 | 0.000000000000 | right | 0.0 |
| chain_len9_holdout | successor_distance_best_0005 | None | 0.000000000000 | 0.000000000000 | 0.000000000000 | right | 0.0 |
| chain_len9_holdout | one_sided_conservative_log_trl_alpha_0_00 | 0.0 | 0.000000000000 | 0.000000000000 | 0.000000000000 | right | 0.0 |
| chain_len9_holdout | one_sided_conservative_log_trl_alpha_0_20 | 0.2 | 0.000000000000 | 0.000000000000 | 0.000000000000 | right | 0.0 |
| chain_len9_holdout | one_sided_conservative_log_trl_alpha_0_40 | 0.4 | 0.000000000000 | 0.000000000000 | 0.000000000000 | right | 0.0 |
| chain_len9_holdout | one_sided_conservative_log_trl_alpha_0_60 | 0.6 | 0.000000000000 | 0.000000000000 | 0.000000000000 | right | 0.0 |
| safe_optimal_matched | mc_supervised | None | 0.254016000000 | 0.045562500000 | 0.504000000000 | risky | 1.0 |
| safe_optimal_matched | trl_raw | None | 0.029241000000 | 0.056250000000 | 0.504000000000 | risky | 1.0 |
| safe_optimal_matched | trl_log | None | 0.000000000000 | 0.000000000000 | 0.000000000000 | safe | 0.0 |
| safe_optimal_matched | mc_plus_trl_log | None | 0.000000000000 | 0.000000000000 | 0.000000000000 | safe | 0.0 |
| safe_optimal_matched | successor_distance_best_0005 | None | 0.000000000000 | 0.000000000000 | 0.000000000000 | safe | 0.0 |
| safe_optimal_matched | one_sided_conservative_log_trl_alpha_0_00 | 0.0 | 0.000000000000 | 0.000000000000 | 0.000000000000 | safe | 0.0 |
| safe_optimal_matched | one_sided_conservative_log_trl_alpha_0_20 | 0.2 | 0.000000000000 | 0.005625000000 | 0.000000000000 | safe | 0.0 |
| safe_optimal_matched | one_sided_conservative_log_trl_alpha_0_40 | 0.4 | 0.000000000000 | 0.011250000000 | 0.000000000000 | safe | 0.0 |
| safe_optimal_matched | one_sided_conservative_log_trl_alpha_0_60 | 0.6 | 0.000000000000 | 0.016875000000 | 0.000000000000 | safe | 0.0 |
| risk_optimal_matched | mc_supervised | None | 0.000000000000 | 0.045562500000 | 0.000000000000 | risky | 1.0 |
| risk_optimal_matched | trl_raw | None | 0.000000000000 | 0.056250000000 | 0.000000000000 | risky | 1.0 |
| risk_optimal_matched | trl_log | None | 0.000000000000 | 0.000000000000 | 0.000000000000 | risky | 1.0 |
| risk_optimal_matched | mc_plus_trl_log | None | 0.000000000000 | 0.000000000000 | 0.000000000000 | risky | 1.0 |
| risk_optimal_matched | successor_distance_best_0005 | None | 0.000000000000 | 0.000000000000 | 0.000000000000 | risky | 1.0 |
| risk_optimal_matched | one_sided_conservative_log_trl_alpha_0_00 | 0.0 | 0.000000000000 | 0.000000000000 | 0.000000000000 | risky | 1.0 |
| risk_optimal_matched | one_sided_conservative_log_trl_alpha_0_20 | 0.2 | 0.000000000000 | 0.005625000000 | 0.000000000000 | risky | 1.0 |
| risk_optimal_matched | one_sided_conservative_log_trl_alpha_0_40 | 0.4 | 0.000000000000 | 0.011250000000 | 0.000000000000 | risky | 1.0 |
| risk_optimal_matched | one_sided_conservative_log_trl_alpha_0_60 | 0.6 | 0.000000000000 | 0.016875000000 | 0.000000000000 | risky | 1.0 |
| safe_optimal_lucky_only_stress | mc_supervised | None | 0.029241000000 | 0.129937500000 | 0.504000000000 | risky | 1.0 |
| safe_optimal_lucky_only_stress | trl_raw | None | 0.029241000000 | 0.084375000000 | 0.504000000000 | risky | 1.0 |
| safe_optimal_lucky_only_stress | trl_log | None | 0.029241000000 | 0.084375000000 | 0.504000000000 | risky | 1.0 |
| safe_optimal_lucky_only_stress | mc_plus_trl_log | None | 0.029241000000 | 0.084375000000 | 0.504000000000 | risky | 1.0 |
| safe_optimal_lucky_only_stress | successor_distance_best_0005 | None | 0.029241000000 | 0.084375000000 | 0.504000000000 | risky | 1.0 |
| safe_optimal_lucky_only_stress | one_sided_conservative_log_trl_alpha_0_00 | 0.0 | 0.029241000000 | 0.084375000000 | 0.504000000000 | risky | 1.0 |
| safe_optimal_lucky_only_stress | one_sided_conservative_log_trl_alpha_0_20 | 0.2 | 0.006561000000 | 0.084375000000 | 0.504000000000 | risky | 1.0 |
| safe_optimal_lucky_only_stress | one_sided_conservative_log_trl_alpha_0_40 | 0.4 | 0.000000000000 | 0.084375000000 | 0.000000000000 | safe | 0.0 |
| safe_optimal_lucky_only_stress | one_sided_conservative_log_trl_alpha_0_60 | 0.6 | 0.000000000000 | 0.084375000000 | 0.000000000000 | safe | 0.0 |
| risk_optimal_no_success_stress | mc_supervised | None | 0.000000000000 | 0.146812500000 | 0.000000000000 | risky | 1.0 |
| risk_optimal_no_success_stress | trl_raw | None | 0.000000000000 | 0.101250000000 | 0.081000000000 | safe | 0.0 |
| risk_optimal_no_success_stress | trl_log | None | 0.000000000000 | 0.101250000000 | 0.081000000000 | safe | 0.0 |
| risk_optimal_no_success_stress | mc_plus_trl_log | None | 0.000000000000 | 0.101250000000 | 0.081000000000 | safe | 0.0 |
| risk_optimal_no_success_stress | successor_distance_best_0005 | None | 0.000000000000 | 0.101250000000 | 0.081000000000 | safe | 0.0 |
| risk_optimal_no_success_stress | one_sided_conservative_log_trl_alpha_0_00 | 0.0 | 0.000000000000 | 0.101250000000 | 0.081000000000 | safe | 0.0 |
| risk_optimal_no_success_stress | one_sided_conservative_log_trl_alpha_0_20 | 0.2 | 0.000000000000 | 0.102897524356 | 0.081000000000 | safe | 0.0 |
| risk_optimal_no_success_stress | one_sided_conservative_log_trl_alpha_0_40 | 0.4 | 0.000000000000 | 0.104545048712 | 0.081000000000 | safe | 0.0 |
| risk_optimal_no_success_stress | one_sided_conservative_log_trl_alpha_0_60 | 0.6 | 0.000000000000 | 0.106192573067 | 0.081000000000 | safe | 0.0 |

## Success Checks

- Chain raw exact: `True`
- Chain TRL-log exact: `True`
- Alpha grid completed: `True`
- Positive uncertainty evidence: `True`
- Best positive method: `one_sided_conservative_log_trl_alpha_0_20`

## Interpretation

one_sided_conservative_log_trl_alpha_0_20 reduced the lucky-only safe-optimal failure versus trl_log while preserving the chain and selecting risky with zero regret in the matched risk-optimal scenario.

## Artifacts

- `research/sto_trl/artifacts/0006/run_uncertainty_conservative_log_trl.py`
- `research/sto_trl/artifacts/0006/raw_metrics.json`
- `research/sto_trl/artifacts/0006/metrics.csv`
- `research/sto_trl/artifacts/0006/penalty_sweep.json`
- `research/sto_trl/artifacts/0006/uncertainty_diagnostics.json`
- `research/sto_trl/artifacts/0006/offline_datasets.json`
- `research/sto_trl/artifacts/0006/transition_tables.json`
- `research/sto_trl/artifacts/0006/value_tables.json`

## Known Failures

- None.
