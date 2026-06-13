# Experiment 0001 Summary

## Objective

Build a minimal tabular diagnostic for stochastic TRL with exact discounted-reachability DP ground truth.

## Commands Run

```bash
mkdir -p research/sto_trl/artifacts/0001 research/sto_trl/results
conda run -n autoresearcher_sto_trl python research/sto_trl/artifacts/0001/run_tabular_sto_trl.py
conda run -n autoresearcher_sto_trl python scripts/validate_artifacts.py --repo-root . --json research/sto_trl/results/0001_result.json --schema schemas/result.schema.json --check-result-artifacts
```

## Setup

- Discount: `0.9`
- Fixed backup iterations: `32`
- MDPs: deterministic 6-state chain and 5-state risky-shortcut MDP.
- Offline risky coverage: `2` lucky risky successes and `6` unlucky risky failures.

## Key Raw Metrics

| MDP | Method | Long-horizon value MSE | Q calibration error | Policy regret | Risky selection |
| --- | --- | ---: | ---: | ---: | ---: |
| deterministic_chain | mc_supervised | 0.000000000000 | 0.263868840000 | 0.000000000000 | 0.0 |
| deterministic_chain | trl_raw | 0.000000000000 | 0.000000000000 | 0.000000000000 | 0.0 |
| deterministic_chain | trl_log | 0.000000000000 | 0.000000000000 | 0.000000000000 | 0.0 |
| deterministic_chain | mc_plus_trl_log | 0.000000000000 | 0.131934420000 | 0.000000000000 | 0.0 |
| risky_shortcut | mc_supervised | 0.000000000000 | 0.000000000000 | 0.000000000000 | 0.0 |
| risky_shortcut | trl_raw | 0.019966500000 | 0.056250000000 | 0.504000000000 | 1.0 |
| risky_shortcut | trl_log | 0.000000000000 | 0.000000000000 | 0.000000000000 | 0.0 |
| risky_shortcut | mc_plus_trl_log | 0.000000000000 | 0.000000000000 | 0.000000000000 | 0.0 |

## Diagnostic Outcome

- Chain raw TRL recovered exact discounted reachability: `True`.
- Chain log TRL recovered exact discounted reachability: `True`.
- Risky dataset covered lucky and unlucky outcomes: `True`.
- Raw TRL chose the risky shortcut: `True`.
- Log TRL chose the safe route: `True`.

The most decisive risky-start numbers are:

- Exact risky Q: `0.225000`
- Raw TRL risky Q: `0.900000`
- Log TRL risky Q: `0.225000`
- Exact safe Q: `0.729000`
- Raw TRL safe Q: `0.729000`
- Log TRL safe Q: `0.729000`

## Artifacts

- `research/sto_trl/artifacts/0001/run_tabular_sto_trl.py`
- `research/sto_trl/artifacts/0001/raw_metrics.json`
- `research/sto_trl/artifacts/0001/metrics.csv`
- `research/sto_trl/artifacts/0001/offline_dataset.json`
- `research/sto_trl/artifacts/0001/transition_tables.json`
- `research/sto_trl/artifacts/0001/value_tables.json`

## Interpretation

The deterministic chain sanity check was recovered by both raw and log TRL. On the risky-shortcut MDP, raw deterministic-style TRL treated the observed lucky risky edge as reliable and selected risky with Q=0.900000 versus exact Q=0.225000. The empirical log backup and MC+TRL-log selected the safe route and had zero start-goal policy regret in this tiny dataset. MC supervised was also calibrated here because the offline set deliberately included both lucky and unlucky risky outcomes.

## Known Failures

- None.
