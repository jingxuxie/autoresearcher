# Experiment 0009 Summary

## Objective

Audit compact transition-level posterior model-DP baselines on representative cells from the 0008 identifiability grid before adding posterior/transitive TRL variants.

## Commands Run

```bash
mkdir -p research/sto_trl/artifacts/0009 research/sto_trl/results
conda run -n autoresearcher_sto_trl python research/sto_trl/artifacts/0009/transition_posterior_baselines.py
conda run -n autoresearcher_sto_trl python scripts/validate_artifacts.py --repo-root . --json research/sto_trl/results/0009_result.json --schema schemas/result.schema.json --check-result-artifacts
```

## Representative Subset

- Selected cells: `8`
- Method rows: `72`
- Regime counts: `{'matched_identifiable_safe_optimal': 1, 'matched_risk_optimal': 1, 'lucky_only_safe_optimal': 1, 'no_success_safe_optimal': 1, 'no_success_risk_optimal': 1, 'ambiguous_safe_optimal': 1, 'ambiguous_risk_optimal': 1, 'prior_dependent_safe_optimal': 1}`
- Tag counts: `{'matched': 5, 'identifiable': 3, 'safe_optimal': 5, 'ambiguous': 5, 'risky_optimal': 3, 'lucky_only': 1, 'prior_dependent': 4, 'no_success': 2}`

## Method Summary

| Method | Action accuracy | Mean regret | Risky rate | Mean Q overestimate | Calibration error |
| --- | ---: | ---: | ---: | ---: | ---: |
| empirical_model_dp | 0.500000 | 0.109012500000 | 0.375000 | 0.116718750000 | 0.262968750000 |
| empirical_risky_value | 0.500000 | 0.109012500000 | 0.375000 | 0.116718750000 | 0.262968750000 |
| posterior_lower_q10_dp_beta_1_1 | 0.750000 | 0.020250000000 | 0.125000 | 0.042862500000 | 0.296981250000 |
| posterior_mean_dp_beta_1_1 | 0.625000 | 0.083250000000 | 0.250000 | 0.090000000000 | 0.233750000000 |
| posterior_upper_q90_dp_beta_1_1 | 0.500000 | 0.105637500000 | 0.625000 | 0.175856250000 | 0.255787500000 |
| raw_trl | 0.375000 | 0.168637500000 | 0.750000 | 0.275625000000 | 0.405000000000 |
| robust_lcb_dp_delta_0_2 | 0.625000 | 0.039487500000 | 0.000000 | 0.024019705511 | 0.377294486223 |
| robust_ucb_dp_delta_0_2 | 0.500000 | 0.105637500000 | 0.625000 | 0.248480276028 | 0.307052638014 |
| trl_log | 0.500000 | 0.109012500000 | 0.375000 | 0.116718750000 | 0.262968750000 |

## Decision Findings

- Best target-regime transition uncertainty baseline: `posterior_lower_q10_dp_beta_1_1`.
- Target-regime regret delta versus TRL-log: `-0.177525000000`.
- Positive transition-baseline evidence: `True`.
- Risk-optimal no-success solved methods: `[]`.
- Chain guard passed: `True`.

## Interpretation

On the representative 0008 subset, transition-level uncertainty baselines explain the recoverable finite-coverage behavior: posterior_lower_q10_dp_beta_1_1 reduces mean target-regime regret versus TRL-log by -0.177525000000, while at least one posterior baseline preserves the matched risk-optimal action. No evaluated transition baseline solved risk_optimal_no_success; explicit priors or additional coverage remain necessary. Empirical model DP, empirical risky value, and TRL-log are identical on this tabular family.

## Artifacts

- `research/sto_trl/artifacts/0009/transition_posterior_baselines.py`
- `research/sto_trl/artifacts/0009/raw_metrics.json`
- `research/sto_trl/artifacts/0009/metrics.csv`
- `research/sto_trl/artifacts/0009/regime_summary.csv`
- `research/sto_trl/artifacts/0009/posterior_diagnostics.json`
- `research/sto_trl/artifacts/0009/selected_grid_cells.json`
- `research/sto_trl/artifacts/0009/coverage_diagnostics.json`
- `research/sto_trl/artifacts/0009/transition_tables.json`
- `research/sto_trl/artifacts/0009/value_tables.json`
