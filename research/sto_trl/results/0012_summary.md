# Experiment 0012 Summary

## Objective

Test whether short trajectory context plus log-space transitive propagation helps in a tiny stochastic POMDP with aliased observations.

## Commands Run

```bash
mkdir -p research/sto_trl/artifacts/0012 research/sto_trl/results
conda run -n autoresearcher_sto_trl python research/sto_trl/artifacts/0012/aliased_pomdp_context_audit.py
conda run -n autoresearcher_sto_trl python scripts/validate_artifacts.py --repo-root . --json research/sto_trl/results/0012_result.json --schema schemas/result.schema.json --check-result-artifacts
```

## Setup

- Hidden hubs: `hub_good` and `hub_bad`
- Aliased observation: `hub`
- History key: cue observation plus the last three observations, e.g. `cue_g|cue_g>hub`
- Label horizon cutoff: `2`
- Trajectories: `56`

## Method Summary

| Method | Heldout MSE | Policy regret | Teleport rate | Calibration error | Action disagreement |
| --- | ---: | ---: | ---: | ---: | ---: |
| history_mc_only | 0.340454390625 | 0.018225000000 | 0.000000 | 0.537637500000 | 0.500000 |
| history_mc_plus_trl_log | 0.000000000000 | 0.000000000000 | 0.500000 | 0.000000000000 | 0.000000 |
| history_model_dp | 0.000000000000 | 0.000000000000 | 0.500000 | 0.000000000000 | 0.000000 |
| history_trl_log | 0.000000000000 | 0.000000000000 | 0.500000 | 0.000000000000 | 0.000000 |
| latent_oracle_dp | 0.000000000000 | 0.000000000000 | 0.500000 | 0.000000000000 | 0.000000 |
| observation_empirical_model_dp | 0.037554514075 | 0.018225000000 | 0.000000 | 0.146137500000 | 0.500000 |
| observation_trl_log | 0.037554514075 | 0.018225000000 | 0.000000 | 0.146137500000 | 0.500000 |

## Decision Findings

- Observation-only aliasing failure: `True`
- History MC+TRL-log MSE improvement vs history MC-only: `1.000000`
- History MC+TRL-log improves policy regret vs observation TRL-log: `True`
- History-model DP fully explains the gain: `True`

## Interpretation

Observation-only model DP and TRL-log fail on the aliased hub because good and bad hidden states share observation 'hub'. Bounded history keys using only the previous cue observation disambiguate the hubs, and history-keyed MC+TRL-log greatly improves censored long-horizon MSE over history-keyed MC-only. The gain is fully matched by history-model DP, so the result supports representation/context value rather than a distinct TRL algorithmic advantage.

## Artifacts

- `research/sto_trl/artifacts/0012/aliased_pomdp_context_audit.py`
- `research/sto_trl/artifacts/0012/raw_metrics.json`
- `research/sto_trl/artifacts/0012/metrics.csv`
- `research/sto_trl/artifacts/0012/alias_summary.csv`
- `research/sto_trl/artifacts/0012/coverage_diagnostics.json`
- `research/sto_trl/artifacts/0012/offline_trajectories.json`
- `research/sto_trl/artifacts/0012/transition_tables.json`
- `research/sto_trl/artifacts/0012/value_tables.json`
- `research/sto_trl/artifacts/0012/alias_diagnostics.json`
