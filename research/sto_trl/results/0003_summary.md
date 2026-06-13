# Experiment 0003 Summary

## Objective

Test whether transitive log backups recover held-out long-horizon discounted reachability when MC labels are censored beyond horizon `2`.

## Commands Run

```bash
mkdir -p research/sto_trl/artifacts/0003 research/sto_trl/results && cp research/sto_trl/artifacts/0002/run_coverage_stress.py research/sto_trl/artifacts/0003/run_horizon_holdout.py
conda run -n autoresearcher_sto_trl python research/sto_trl/artifacts/0003/run_horizon_holdout.py
conda run -n autoresearcher_sto_trl python scripts/validate_artifacts.py --repo-root . --json research/sto_trl/results/0003_result.json --schema schemas/result.schema.json --check-result-artifacts
```

## Setup

- Discount: `0.9`
- Fixed backup iterations: `32`
- Label cutoff: positive MC labels with horizon `>2` are censored.
- MDPs: deterministic chain length 9 and matched-coverage risky shortcut with risky success/failure counts `2/6`.

## Key Metrics

| Scenario | Method | Held-out value MSE | Policy regret | Chosen action | Risky selected |
| --- | --- | ---: | ---: | --- | ---: |
| chain_len9 | mc_supervised | 0.391705823230 | 0.000000000000 | right | 0.0 |
| chain_len9 | trl_raw | 0.000000000000 | 0.000000000000 | right | 0.0 |
| chain_len9 | trl_log | 0.000000000000 | 0.000000000000 | right | 0.0 |
| chain_len9 | mc_plus_trl_log | 0.000000000000 | 0.000000000000 | right | 0.0 |
| risky_matched | mc_supervised | 0.254016000000 | 0.504000000000 | risky | 1.0 |
| risky_matched | trl_raw | 0.029241000000 | 0.504000000000 | risky | 1.0 |
| risky_matched | trl_log | 0.000000000000 | 0.000000000000 | safe | 0.0 |
| risky_matched | mc_plus_trl_log | 0.000000000000 | 0.000000000000 | safe | 0.0 |

## Success Checks

- Chain raw exact under censoring: `True`
- Chain TRL-log exact under censoring: `True`
- MC+TRL-log improves chain held-out MSE vs MC: `True`
- Held-out MSE improves vs MC on chain and risky: `True`
- Matched risky TRL-log selects safe: `True`
- Matched risky MC+TRL-log selects safe: `True`
- Matched risky raw TRL selects wrong risky: `True`

## Interpretation

With positive labels beyond horizon 2 censored, MC-supervised underpredicted held-out long-horizon reachability. TRL-log and MC+TRL-log propagated through observed transitions and reduced held-out value MSE on the longer chain and the matched risky MDP. In the matched risky MDP, TRL-log and MC+TRL-log selected the safe action, while raw TRL selected the risky shortcut from support alone.

## Artifacts

- `research/sto_trl/artifacts/0003/run_horizon_holdout.py`
- `research/sto_trl/artifacts/0003/raw_metrics.json`
- `research/sto_trl/artifacts/0003/metrics.csv`
- `research/sto_trl/artifacts/0003/label_coverage_by_horizon.json`
- `research/sto_trl/artifacts/0003/offline_datasets.json`
- `research/sto_trl/artifacts/0003/transition_tables.json`
- `research/sto_trl/artifacts/0003/value_tables.json`

## Known Failures

- None.
