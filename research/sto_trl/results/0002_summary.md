# Experiment 0002 Summary

## Objective

Stress-test stochastic shortcut coverage with exact DP evaluation, including safe-optimal and risk-optimal risky-shortcut MDPs.

## Commands Run

```bash
mkdir -p research/sto_trl/artifacts/0002 research/sto_trl/results && cp research/sto_trl/artifacts/0001/run_tabular_sto_trl.py research/sto_trl/artifacts/0002/run_coverage_stress.py
conda run -n autoresearcher_sto_trl python research/sto_trl/artifacts/0002/run_coverage_stress.py
conda run -n autoresearcher_sto_trl python scripts/validate_artifacts.py --repo-root . --json research/sto_trl/results/0002_result.json --schema schemas/result.schema.json --check-result-artifacts
```

## Setup

- Discount: `0.9`
- Fixed backup iterations: `32`
- Safe episodes per risky regime: `4`
- Risky settings: safe-optimal true success `0.25`; risk-optimal true success `0.90`.
- Regimes per risky setting: `matched, lucky_biased, lucky_only, unlucky_biased, no_risky_success`.

## Aggregate Checks

- Chain raw TRL recovered exact reachability: `True`.
- Chain log TRL recovered exact reachability: `True`.
- All predeclared risky regimes present: `True`.
- Raw policy was support-driven: `True`.
- TRL-log chose the exact optimal action in matched regimes: `True`.

## Per-Regime Metrics

| Scenario | Method | Observed S/F | Exact optimal | Chosen | Regret | Risky Q learned/exact | Safe Q learned/exact |
| --- | --- | ---: | --- | --- | ---: | ---: | ---: |
| safe_optimal__matched | mc_supervised | 2/6 | safe | safe | 0.000000 | 0.225000/0.225000 | 0.729000/0.729000 |
| safe_optimal__matched | trl_raw | 2/6 | safe | risky | 0.504000 | 0.900000/0.225000 | 0.729000/0.729000 |
| safe_optimal__matched | trl_log | 2/6 | safe | safe | 0.000000 | 0.225000/0.225000 | 0.729000/0.729000 |
| safe_optimal__matched | mc_plus_trl_log | 2/6 | safe | safe | 0.000000 | 0.225000/0.225000 | 0.729000/0.729000 |
| safe_optimal__lucky_biased | mc_supervised | 6/2 | safe | safe | 0.000000 | 0.675000/0.225000 | 0.729000/0.729000 |
| safe_optimal__lucky_biased | trl_raw | 6/2 | safe | risky | 0.504000 | 0.900000/0.225000 | 0.729000/0.729000 |
| safe_optimal__lucky_biased | trl_log | 6/2 | safe | safe | 0.000000 | 0.675000/0.225000 | 0.729000/0.729000 |
| safe_optimal__lucky_biased | mc_plus_trl_log | 6/2 | safe | safe | 0.000000 | 0.675000/0.225000 | 0.729000/0.729000 |
| safe_optimal__lucky_only | mc_supervised | 4/0 | safe | risky | 0.504000 | 0.900000/0.225000 | 0.729000/0.729000 |
| safe_optimal__lucky_only | trl_raw | 4/0 | safe | risky | 0.504000 | 0.900000/0.225000 | 0.729000/0.729000 |
| safe_optimal__lucky_only | trl_log | 4/0 | safe | risky | 0.504000 | 0.900000/0.225000 | 0.729000/0.729000 |
| safe_optimal__lucky_only | mc_plus_trl_log | 4/0 | safe | risky | 0.504000 | 0.900000/0.225000 | 0.729000/0.729000 |
| safe_optimal__unlucky_biased | mc_supervised | 1/7 | safe | safe | 0.000000 | 0.112500/0.225000 | 0.729000/0.729000 |
| safe_optimal__unlucky_biased | trl_raw | 1/7 | safe | risky | 0.504000 | 0.900000/0.225000 | 0.729000/0.729000 |
| safe_optimal__unlucky_biased | trl_log | 1/7 | safe | safe | 0.000000 | 0.112500/0.225000 | 0.729000/0.729000 |
| safe_optimal__unlucky_biased | mc_plus_trl_log | 1/7 | safe | safe | 0.000000 | 0.112500/0.225000 | 0.729000/0.729000 |
| safe_optimal__no_risky_success | mc_supervised | 0/8 | safe | safe | 0.000000 | 0.000000/0.225000 | 0.729000/0.729000 |
| safe_optimal__no_risky_success | trl_raw | 0/8 | safe | safe | 0.000000 | 0.000000/0.225000 | 0.729000/0.729000 |
| safe_optimal__no_risky_success | trl_log | 0/8 | safe | safe | 0.000000 | 0.000000/0.225000 | 0.729000/0.729000 |
| safe_optimal__no_risky_success | mc_plus_trl_log | 0/8 | safe | safe | 0.000000 | 0.000000/0.225000 | 0.729000/0.729000 |
| risk_optimal__matched | mc_supervised | 9/1 | risky | risky | 0.000000 | 0.810000/0.810000 | 0.729000/0.729000 |
| risk_optimal__matched | trl_raw | 9/1 | risky | risky | 0.000000 | 0.900000/0.810000 | 0.729000/0.729000 |
| risk_optimal__matched | trl_log | 9/1 | risky | risky | 0.000000 | 0.810000/0.810000 | 0.729000/0.729000 |
| risk_optimal__matched | mc_plus_trl_log | 9/1 | risky | risky | 0.000000 | 0.810000/0.810000 | 0.729000/0.729000 |
| risk_optimal__lucky_biased | mc_supervised | 9/0 | risky | risky | 0.000000 | 0.900000/0.810000 | 0.729000/0.729000 |
| risk_optimal__lucky_biased | trl_raw | 9/0 | risky | risky | 0.000000 | 0.900000/0.810000 | 0.729000/0.729000 |
| risk_optimal__lucky_biased | trl_log | 9/0 | risky | risky | 0.000000 | 0.900000/0.810000 | 0.729000/0.729000 |
| risk_optimal__lucky_biased | mc_plus_trl_log | 9/0 | risky | risky | 0.000000 | 0.900000/0.810000 | 0.729000/0.729000 |
| risk_optimal__lucky_only | mc_supervised | 4/0 | risky | risky | 0.000000 | 0.900000/0.810000 | 0.729000/0.729000 |
| risk_optimal__lucky_only | trl_raw | 4/0 | risky | risky | 0.000000 | 0.900000/0.810000 | 0.729000/0.729000 |
| risk_optimal__lucky_only | trl_log | 4/0 | risky | risky | 0.000000 | 0.900000/0.810000 | 0.729000/0.729000 |
| risk_optimal__lucky_only | mc_plus_trl_log | 4/0 | risky | risky | 0.000000 | 0.900000/0.810000 | 0.729000/0.729000 |
| risk_optimal__unlucky_biased | mc_supervised | 4/4 | risky | safe | 0.081000 | 0.450000/0.810000 | 0.729000/0.729000 |
| risk_optimal__unlucky_biased | trl_raw | 4/4 | risky | risky | 0.000000 | 0.900000/0.810000 | 0.729000/0.729000 |
| risk_optimal__unlucky_biased | trl_log | 4/4 | risky | safe | 0.081000 | 0.450000/0.810000 | 0.729000/0.729000 |
| risk_optimal__unlucky_biased | mc_plus_trl_log | 4/4 | risky | safe | 0.081000 | 0.450000/0.810000 | 0.729000/0.729000 |
| risk_optimal__no_risky_success | mc_supervised | 0/8 | risky | safe | 0.081000 | 0.000000/0.810000 | 0.729000/0.729000 |
| risk_optimal__no_risky_success | trl_raw | 0/8 | risky | safe | 0.081000 | 0.000000/0.810000 | 0.729000/0.729000 |
| risk_optimal__no_risky_success | trl_log | 0/8 | risky | safe | 0.081000 | 0.000000/0.810000 | 0.729000/0.729000 |
| risk_optimal__no_risky_success | mc_plus_trl_log | 0/8 | risky | safe | 0.081000 | 0.000000/0.810000 | 0.729000/0.729000 |

## Outcome

The chain guard still recovered exact discounted reachability for raw and log TRL. Across risky regimes, raw TRL selected risky in every scenario with at least one observed lucky risky transition and did not select risky when no lucky risky transition was observed, confirming the support-driven failure mode. Empirical TRL-log and MC tracked observed frequencies: they were correct in matched regimes, became overoptimistic in safe-optimal lucky-biased/lucky-only regimes, and became too conservative in risk-optimal unlucky/no-success regimes. The risk-optimal setting therefore exposes that calibration gains are coverage-dependent, not simply safe-action conservatism.

## Artifacts

- `research/sto_trl/artifacts/0002/run_coverage_stress.py`
- `research/sto_trl/artifacts/0002/raw_metrics.json`
- `research/sto_trl/artifacts/0002/metrics.csv`
- `research/sto_trl/artifacts/0002/coverage_diagnostics.json`
- `research/sto_trl/artifacts/0002/dataset_specs.json`
- `research/sto_trl/artifacts/0002/offline_datasets.json`
- `research/sto_trl/artifacts/0002/transition_tables.json`
- `research/sto_trl/artifacts/0002/value_tables.json`

## Known Failures

- None.
