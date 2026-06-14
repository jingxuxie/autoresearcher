# Experiment 0010 Summary

## Objective

Test whether posterior transition uncertainty plus log-space transitive propagation adds value beyond transition-model DP on a small multi-step stochastic branch-chain diagnostic.

## Commands Run

```bash
mkdir -p research/sto_trl/artifacts/0010 research/sto_trl/results
conda run -n autoresearcher_sto_trl python research/sto_trl/artifacts/0010/posterior_transitive_ablation.py
conda run -n autoresearcher_sto_trl python scripts/validate_artifacts.py --repo-root . --json research/sto_trl/results/0010_result.json --schema schemas/result.schema.json --check-result-artifacts
```

## Setup

- Regimes: `5`
- Label horizon cutoff: `2`
- Methods: `['mc_supervised', 'trl_raw', 'trl_log', 'empirical_model_dp', 'posterior_mean_model_dp', 'posterior_lower_q10_model_dp', 'posterior_trl_log', 'posterior_mc_plus_trl_log']`
- Chain guard passed: `True`

## Method Summary

| Method | Action accuracy | Heldout MSE | Policy regret | Risky rate | Q overestimation | Calibration error |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| empirical_model_dp | 0.400000 | 0.040962586545 | 0.067068000000 | 0.400000 | 0.072900000000 | 0.221616000000 |
| mc_supervised | 0.400000 | 0.421570001925 | 0.016038000000 | 0.000000 | 0.000000000000 | 0.542376000000 |
| posterior_lower_q10_model_dp | 0.400000 | 0.038630321057 | 0.016038000000 | 0.000000 | 0.019099800000 | 0.261006300000 |
| posterior_mc_plus_trl_log | 0.600000 | 0.036595664924 | 0.008748000000 | 0.200000 | 0.048600000000 | 0.215430545455 |
| posterior_mean_model_dp | 0.600000 | 0.036595664924 | 0.008748000000 | 0.200000 | 0.048600000000 | 0.215430545455 |
| posterior_trl_log | 0.600000 | 0.036595664924 | 0.008748000000 | 0.200000 | 0.048600000000 | 0.215430545455 |
| trl_log | 0.400000 | 0.040962586545 | 0.067068000000 | 0.400000 | 0.072900000000 | 0.221616000000 |
| trl_raw | 0.400000 | 0.050639241420 | 0.123930000000 | 0.800000 | 0.179334000000 | 0.317844000000 |

## Decision Findings

- Positive posterior transitive evidence: `False`
- Posterior TRL equivalent to prior-matched posterior model DP: `True`
- Matched risk-optimal action preserved: `True`
- Posterior TRL minus posterior model heldout MSE: `0.000000000000`
- MC-only minus TRL-log heldout MSE: `0.380607415380`

## Interpretation

The multi-step branch-chain confirms that transitive backups recover censored long-horizon values better than MC-only, and posterior transition uncertainty changes the risky branch through the declared Beta prior. However, posterior_trl_log and posterior_mc_plus_trl_log are numerically equivalent to the prior-matched posterior mean model-DP baseline on every regime, so the improvement is attributable to the transition prior/model rather than a distinct posterior TRL transitive effect.

## Artifacts

- `research/sto_trl/artifacts/0010/posterior_transitive_ablation.py`
- `research/sto_trl/artifacts/0010/raw_metrics.json`
- `research/sto_trl/artifacts/0010/metrics.csv`
- `research/sto_trl/artifacts/0010/regime_summary.csv`
- `research/sto_trl/artifacts/0010/posterior_transitive_diagnostics.json`
- `research/sto_trl/artifacts/0010/coverage_diagnostics.json`
- `research/sto_trl/artifacts/0010/offline_datasets.json`
- `research/sto_trl/artifacts/0010/transition_tables.json`
- `research/sto_trl/artifacts/0010/value_tables.json`
