# Experiment 0004 Summary

## Objective

Test successor-distance calibration-only versus successor-distance + TRL-log on horizon holdout and stochastic risky shortcuts.

## Commands Run

```bash
mkdir -p research/sto_trl/artifacts/0004 research/sto_trl/results && cp research/sto_trl/artifacts/0003/run_horizon_holdout.py research/sto_trl/artifacts/0004/run_successor_distance.py
conda run -n autoresearcher_sto_trl python research/sto_trl/artifacts/0004/run_successor_distance.py
conda run -n autoresearcher_sto_trl python scripts/validate_artifacts.py --repo-root . --json research/sto_trl/results/0004_result.json --schema schemas/result.schema.json --check-result-artifacts
```

## Setup

- Discount: `0.9`
- Label horizon cutoff: `2`
- Fixed backup iterations: `32`
- Successor transitive weight: `0.75`
- Main scenarios: chain holdout, matched safe-optimal risky shortcut, matched risk-optimal risky shortcut.
- Stress scenario: safe-optimal lucky-only risky shortcut.

## Main Metrics

| Scenario | Method | Held-out MSE | Q calibration | Policy regret | Action | Triangle violation |
| --- | --- | ---: | ---: | ---: | --- | ---: |
| chain_len9_holdout | mc_supervised | 0.391705823230 | 0.465607869047 | 0.000000000000 | right | 0.166667 |
| chain_len9_holdout | trl_raw | 0.000000000000 | 0.000000000000 | 0.000000000000 | right | 0.000000 |
| chain_len9_holdout | trl_log | 0.000000000000 | 0.000000000000 | 0.000000000000 | right | 0.000000 |
| chain_len9_holdout | mc_plus_trl_log | 0.000000000000 | 0.131258278195 | 0.000000000000 | right | 0.000000 |
| chain_len9_holdout | successor_calibration_only | 0.391705823230 | 0.465607869047 | 0.000000000000 | right | 0.166667 |
| chain_len9_holdout | successor_distance_trl_log | 0.000000000000 | 0.000000000000 | 0.000000000000 | right | 0.000000 |
| safe_optimal_matched | mc_supervised | 0.254016000000 | 0.045562500000 | 0.504000000000 | risky | 0.375000 |
| safe_optimal_matched | trl_raw | 0.029241000000 | 0.056250000000 | 0.504000000000 | risky | 0.000000 |
| safe_optimal_matched | trl_log | 0.000000000000 | 0.000000000000 | 0.000000000000 | safe | 0.250000 |
| safe_optimal_matched | mc_plus_trl_log | 0.000000000000 | 0.000000000000 | 0.000000000000 | safe | 0.250000 |
| safe_optimal_matched | successor_calibration_only | 0.254016000000 | 0.045562500000 | 0.504000000000 | risky | 0.375000 |
| safe_optimal_matched | successor_distance_trl_log | 0.000000000000 | 0.000000000000 | 0.000000000000 | safe | 0.250000 |
| risk_optimal_matched | mc_supervised | 0.000000000000 | 0.045562500000 | 0.000000000000 | risky | 0.250000 |
| risk_optimal_matched | trl_raw | 0.000000000000 | 0.056250000000 | 0.000000000000 | risky | 0.000000 |
| risk_optimal_matched | trl_log | 0.000000000000 | 0.000000000000 | 0.000000000000 | risky | 0.250000 |
| risk_optimal_matched | mc_plus_trl_log | 0.000000000000 | 0.000000000000 | 0.000000000000 | risky | 0.250000 |
| risk_optimal_matched | successor_calibration_only | 0.000000000000 | 0.045562500000 | 0.000000000000 | risky | 0.250000 |
| risk_optimal_matched | successor_distance_trl_log | 0.000000000000 | 0.000000000000 | 0.000000000000 | risky | 0.250000 |
| safe_optimal_lucky_only_stress | mc_supervised | 0.029241000000 | 0.129937500000 | 0.504000000000 | risky | 0.000000 |
| safe_optimal_lucky_only_stress | trl_raw | 0.029241000000 | 0.084375000000 | 0.504000000000 | risky | 0.000000 |
| safe_optimal_lucky_only_stress | trl_log | 0.029241000000 | 0.084375000000 | 0.504000000000 | risky | 0.000000 |
| safe_optimal_lucky_only_stress | mc_plus_trl_log | 0.029241000000 | 0.084375000000 | 0.504000000000 | risky | 0.000000 |
| safe_optimal_lucky_only_stress | successor_calibration_only | 0.029241000000 | 0.129937500000 | 0.504000000000 | risky | 0.000000 |
| safe_optimal_lucky_only_stress | successor_distance_trl_log | 0.029241000000 | 0.084375000000 | 0.504000000000 | risky | 0.000000 |

## Success Checks

- Chain raw exact: `True`
- Chain TRL-log exact: `True`
- Successor-distance improves main held-out MSE vs calibration-only: `True`
- No matched policy-regret increase vs calibration-only: `True`
- No matched Q-overestimation increase vs calibration-only: `True`
- Risk-optimal matched scenario selects risky: `True`
- Safe-optimal matched scenario selects safe: `True`

## Interpretation

The successor-distance transitive relaxation improved main held-out long-horizon value MSE over calibration-only. On matched safe-optimal risky coverage it selected safe with no policy-regret increase versus calibration-only, and on matched risk-optimal coverage it selected risky, so the effect was not simple conservative avoidance. The lucky-only stress case remains a biased-coverage failure case rather than a success criterion.

## Artifacts

- `research/sto_trl/artifacts/0004/run_successor_distance.py`
- `research/sto_trl/artifacts/0004/raw_metrics.json`
- `research/sto_trl/artifacts/0004/metrics.csv`
- `research/sto_trl/artifacts/0004/successor_distance_tables.json`
- `research/sto_trl/artifacts/0004/distance_diagnostics.json`
- `research/sto_trl/artifacts/0004/label_or_pair_coverage.json`
- `research/sto_trl/artifacts/0004/offline_datasets.json`
- `research/sto_trl/artifacts/0004/transition_tables.json`
- `research/sto_trl/artifacts/0004/value_tables.json`

## Known Failures

- None.
