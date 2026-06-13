# Experiment 0007 Summary

## Objective

Audit a generic count-based posterior uncertainty penalty against the 0006 one-sided conservative rule.

## Commands Run

```bash
mkdir -p research/sto_trl/artifacts/0007 research/sto_trl/results && cp research/sto_trl/artifacts/0006/run_uncertainty_conservative_log_trl.py research/sto_trl/artifacts/0007/run_generic_uncertainty_audit.py
conda run -n autoresearcher_sto_trl python research/sto_trl/artifacts/0007/run_generic_uncertainty_audit.py
conda run -n autoresearcher_sto_trl python scripts/validate_artifacts.py --repo-root . --json research/sto_trl/results/0007_result.json --schema schemas/result.schema.json --check-result-artifacts
```

## Setup

- Discount: `0.9`
- Label horizon cutoff: `2`
- Fixed backup iterations: `32`
- Prior grid: `[0.5, 1.0]`
- Alpha grid: `[0.0, 0.5, 1.0]`
- Generic penalty: interpolate empirical log backup with a Dirichlet unknown-zero posterior lower estimate for state-action counts at least 4.

## Metrics

| Scenario | Method | Prior | Alpha | Held-out MSE | Q calibration | Policy regret | Action | Risky selected |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- | ---: |
| chain_len9_holdout | mc_supervised | None | None | 0.391705823230 | 0.465607869047 | 0.000000000000 | right | 0.0 |
| chain_len9_holdout | trl_raw | None | None | 0.000000000000 | 0.000000000000 | 0.000000000000 | right | 0.0 |
| chain_len9_holdout | trl_log | None | None | 0.000000000000 | 0.000000000000 | 0.000000000000 | right | 0.0 |
| chain_len9_holdout | mc_plus_trl_log | None | None | 0.000000000000 | 0.131258278195 | 0.000000000000 | right | 0.0 |
| chain_len9_holdout | successor_distance_best_0005 | None | None | 0.000000000000 | 0.000000000000 | 0.000000000000 | right | 0.0 |
| chain_len9_holdout | one_sided_conservative_log_trl_alpha_0_40 | None | 0.4 | 0.000000000000 | 0.000000000000 | 0.000000000000 | right | 0.0 |
| chain_len9_holdout | generic_dirichlet_unknown_prior_0_50_alpha_0_00 | 0.5 | 0.0 | 0.000000000000 | 0.000000000000 | 0.000000000000 | right | 0.0 |
| chain_len9_holdout | generic_dirichlet_unknown_prior_0_50_alpha_0_50 | 0.5 | 0.5 | 0.000000000000 | 0.000000000000 | 0.000000000000 | right | 0.0 |
| chain_len9_holdout | generic_dirichlet_unknown_prior_0_50_alpha_1_00 | 0.5 | 1.0 | 0.000000000000 | 0.000000000000 | 0.000000000000 | right | 0.0 |
| chain_len9_holdout | generic_dirichlet_unknown_prior_1_00_alpha_0_00 | 1.0 | 0.0 | 0.000000000000 | 0.000000000000 | 0.000000000000 | right | 0.0 |
| chain_len9_holdout | generic_dirichlet_unknown_prior_1_00_alpha_0_50 | 1.0 | 0.5 | 0.000000000000 | 0.000000000000 | 0.000000000000 | right | 0.0 |
| chain_len9_holdout | generic_dirichlet_unknown_prior_1_00_alpha_1_00 | 1.0 | 1.0 | 0.000000000000 | 0.000000000000 | 0.000000000000 | right | 0.0 |
| safe_optimal_matched | mc_supervised | None | None | 0.254016000000 | 0.045562500000 | 0.504000000000 | risky | 1.0 |
| safe_optimal_matched | trl_raw | None | None | 0.029241000000 | 0.056250000000 | 0.504000000000 | risky | 1.0 |
| safe_optimal_matched | trl_log | None | None | 0.000000000000 | 0.000000000000 | 0.000000000000 | safe | 0.0 |
| safe_optimal_matched | mc_plus_trl_log | None | None | 0.000000000000 | 0.000000000000 | 0.000000000000 | safe | 0.0 |
| safe_optimal_matched | successor_distance_best_0005 | None | None | 0.000000000000 | 0.000000000000 | 0.000000000000 | safe | 0.0 |
| safe_optimal_matched | one_sided_conservative_log_trl_alpha_0_40 | None | 0.4 | 0.000000000000 | 0.011250000000 | 0.000000000000 | safe | 0.0 |
| safe_optimal_matched | generic_dirichlet_unknown_prior_0_50_alpha_0_00 | 0.5 | 0.0 | 0.000000000000 | 0.000000000000 | 0.000000000000 | safe | 0.0 |
| safe_optimal_matched | generic_dirichlet_unknown_prior_0_50_alpha_0_50 | 0.5 | 0.5 | 0.013196265625 | 0.029146599265 | 0.000000000000 | safe | 0.0 |
| safe_optimal_matched | generic_dirichlet_unknown_prior_0_50_alpha_1_00 | 0.5 | 1.0 | 0.047089000000 | 0.056871323529 | 0.000000000000 | safe | 0.0 |
| safe_optimal_matched | generic_dirichlet_unknown_prior_1_00_alpha_0_00 | 1.0 | 0.0 | 0.000000000000 | 0.000000000000 | 0.000000000000 | safe | 0.0 |
| safe_optimal_matched | generic_dirichlet_unknown_prior_1_00_alpha_0_50 | 1.0 | 0.5 | 0.039029558481 | 0.051584937500 | 0.000000000000 | safe | 0.0 |
| safe_optimal_matched | generic_dirichlet_unknown_prior_1_00_alpha_1_00 | 1.0 | 1.0 | 0.126559485504 | 0.098684500000 | 0.000000000000 | safe | 0.0 |
| risk_optimal_matched | mc_supervised | None | None | 0.000000000000 | 0.045562500000 | 0.000000000000 | risky | 1.0 |
| risk_optimal_matched | trl_raw | None | None | 0.000000000000 | 0.056250000000 | 0.000000000000 | risky | 1.0 |
| risk_optimal_matched | trl_log | None | None | 0.000000000000 | 0.000000000000 | 0.000000000000 | risky | 1.0 |
| risk_optimal_matched | mc_plus_trl_log | None | None | 0.000000000000 | 0.000000000000 | 0.000000000000 | risky | 1.0 |
| risk_optimal_matched | successor_distance_best_0005 | None | None | 0.000000000000 | 0.000000000000 | 0.000000000000 | risky | 1.0 |
| risk_optimal_matched | one_sided_conservative_log_trl_alpha_0_40 | None | 0.4 | 0.000000000000 | 0.011250000000 | 0.000000000000 | risky | 1.0 |
| risk_optimal_matched | generic_dirichlet_unknown_prior_0_50_alpha_0_00 | 0.5 | 0.0 | 0.000000000000 | 0.000000000000 | 0.000000000000 | risky | 1.0 |
| risk_optimal_matched | generic_dirichlet_unknown_prior_0_50_alpha_0_50 | 0.5 | 0.5 | 0.000000000000 | 0.028831473214 | 0.000000000000 | risky | 1.0 |
| risk_optimal_matched | generic_dirichlet_unknown_prior_0_50_alpha_1_00 | 0.5 | 1.0 | 0.000000000000 | 0.056241071429 | 0.000000000000 | risky | 1.0 |
| risk_optimal_matched | generic_dirichlet_unknown_prior_1_00_alpha_0_00 | 1.0 | 0.0 | 0.000000000000 | 0.000000000000 | 0.000000000000 | risky | 1.0 |
| risk_optimal_matched | generic_dirichlet_unknown_prior_1_00_alpha_0_50 | 1.0 | 0.5 | 0.000000000000 | 0.051016755682 | 0.000000000000 | risky | 1.0 |
| risk_optimal_matched | generic_dirichlet_unknown_prior_1_00_alpha_1_00 | 1.0 | 1.0 | 0.000000000000 | 0.097548136364 | 0.000000000000 | risky | 1.0 |
| safe_optimal_lucky_only_stress | mc_supervised | None | None | 0.029241000000 | 0.129937500000 | 0.504000000000 | risky | 1.0 |
| safe_optimal_lucky_only_stress | trl_raw | None | None | 0.029241000000 | 0.084375000000 | 0.504000000000 | risky | 1.0 |
| safe_optimal_lucky_only_stress | trl_log | None | None | 0.029241000000 | 0.084375000000 | 0.504000000000 | risky | 1.0 |
| safe_optimal_lucky_only_stress | mc_plus_trl_log | None | None | 0.029241000000 | 0.084375000000 | 0.504000000000 | risky | 1.0 |
| safe_optimal_lucky_only_stress | successor_distance_best_0005 | None | None | 0.029241000000 | 0.084375000000 | 0.504000000000 | risky | 1.0 |
| safe_optimal_lucky_only_stress | one_sided_conservative_log_trl_alpha_0_40 | None | 0.4 | 0.000000000000 | 0.084375000000 | 0.000000000000 | safe | 0.0 |
| safe_optimal_lucky_only_stress | generic_dirichlet_unknown_prior_0_50_alpha_0_00 | 0.5 | 0.0 | 0.029241000000 | 0.084375000000 | 0.504000000000 | risky | 1.0 |
| safe_optimal_lucky_only_stress | generic_dirichlet_unknown_prior_0_50_alpha_0_50 | 0.5 | 0.5 | 0.014641000000 | 0.108742187500 | 0.504000000000 | risky | 1.0 |
| safe_optimal_lucky_only_stress | generic_dirichlet_unknown_prior_0_50_alpha_1_00 | 0.5 | 1.0 | 0.005041000000 | 0.131687500000 | 0.504000000000 | risky | 1.0 |
| safe_optimal_lucky_only_stress | generic_dirichlet_unknown_prior_1_00_alpha_0_00 | 1.0 | 0.0 | 0.029241000000 | 0.084375000000 | 0.504000000000 | risky | 1.0 |
| safe_optimal_lucky_only_stress | generic_dirichlet_unknown_prior_1_00_alpha_0_50 | 1.0 | 0.5 | 0.006561000000 | 0.127209937500 | 0.504000000000 | risky | 1.0 |
| safe_optimal_lucky_only_stress | generic_dirichlet_unknown_prior_1_00_alpha_1_00 | 1.0 | 1.0 | 0.000081000000 | 0.165559500000 | 0.504000000000 | risky | 1.0 |
| risk_optimal_no_success_stress | mc_supervised | None | None | 0.000000000000 | 0.146812500000 | 0.000000000000 | risky | 1.0 |
| risk_optimal_no_success_stress | trl_raw | None | None | 0.000000000000 | 0.101250000000 | 0.081000000000 | safe | 0.0 |
| risk_optimal_no_success_stress | trl_log | None | None | 0.000000000000 | 0.101250000000 | 0.081000000000 | safe | 0.0 |
| risk_optimal_no_success_stress | mc_plus_trl_log | None | None | 0.000000000000 | 0.101250000000 | 0.081000000000 | safe | 0.0 |
| risk_optimal_no_success_stress | successor_distance_best_0005 | None | None | 0.000000000000 | 0.101250000000 | 0.081000000000 | safe | 0.0 |
| risk_optimal_no_success_stress | one_sided_conservative_log_trl_alpha_0_40 | None | 0.4 | 0.000000000000 | 0.104545048712 | 0.081000000000 | safe | 0.0 |
| risk_optimal_no_success_stress | generic_dirichlet_unknown_prior_0_50_alpha_0_00 | 0.5 | 0.0 | 0.000000000000 | 0.101250000000 | 0.081000000000 | safe | 0.0 |
| risk_optimal_no_success_stress | generic_dirichlet_unknown_prior_0_50_alpha_0_50 | 0.5 | 0.5 | 0.000000000000 | 0.127087775735 | 0.081000000000 | safe | 0.0 |
| risk_optimal_no_success_stress | generic_dirichlet_unknown_prior_0_50_alpha_1_00 | 0.5 | 1.0 | 0.000000000000 | 0.151503676471 | 0.081000000000 | safe | 0.0 |
| risk_optimal_no_success_stress | generic_dirichlet_unknown_prior_1_00_alpha_0_00 | 1.0 | 0.0 | 0.000000000000 | 0.101250000000 | 0.081000000000 | safe | 0.0 |
| risk_optimal_no_success_stress | generic_dirichlet_unknown_prior_1_00_alpha_0_50 | 1.0 | 0.5 | 0.000000000000 | 0.146584937500 | 0.081000000000 | safe | 0.0 |
| risk_optimal_no_success_stress | generic_dirichlet_unknown_prior_1_00_alpha_1_00 | 1.0 | 1.0 | 0.000000000000 | 0.187434500000 | 0.081000000000 | safe | 0.0 |

## Success Checks

- Chain raw exact: `True`
- Chain TRL-log exact: `True`
- Generic grid completed: `True`
- Positive generic uncertainty evidence: `True`
- Best positive method: `generic_dirichlet_unknown_prior_0_50_alpha_0_50`
- Risk-optimal no-success unsolved by best positive: `True`

## Interpretation

generic_dirichlet_unknown_prior_0_50_alpha_0_50 reduced safe-optimal lucky-only overestimation versus trl_log while preserving the chain and selecting risky with zero regret in the matched risk-optimal scenario. The risk-optimal no-success stress status is reported separately.

## Artifacts

- `research/sto_trl/artifacts/0007/run_generic_uncertainty_audit.py`
- `research/sto_trl/artifacts/0007/raw_metrics.json`
- `research/sto_trl/artifacts/0007/metrics.csv`
- `research/sto_trl/artifacts/0007/uncertainty_grid.json`
- `research/sto_trl/artifacts/0007/uncertainty_diagnostics.json`
- `research/sto_trl/artifacts/0007/offline_datasets.json`
- `research/sto_trl/artifacts/0007/transition_tables.json`
- `research/sto_trl/artifacts/0007/value_tables.json`

## Known Failures

- None.
