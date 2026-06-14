# Experiment 0013 Summary

## Objective

Test whether the partial-observation/context pivot generalizes beyond the single hand-constructed 0012 POMDP and whether any TRL-style transitive component adds value beyond history-model DP.

## Commands Run

```bash
mkdir -p research/sto_trl/artifacts/0013 research/sto_trl/results
conda run -n autoresearcher_sto_trl python research/sto_trl/artifacts/0013/randomized_pomdp_context_audit.py
conda run -n autoresearcher_sto_trl python scripts/validate_artifacts.py --repo-root . --json research/sto_trl/results/0013_result.json --schema schemas/result.schema.json --check-result-artifacts
```

## Suite

- Families: `['cue_sufficient', 'cue_noisy', 'cue_insufficient']`
- Seeds: `[0, 1, 2, 3, 4]`
- Cases: `15`
- Label horizon cutoff: `2`

## Method Summary

| Method | Heldout MSE | Policy regret | Teleport rate | Calibration error | Action disagreement |
| --- | ---: | ---: | ---: | ---: | ---: |
| history_mc_only | 0.340365817125 | 0.018225000000 | 0.000000 | 0.536422500000 | 0.500000 |
| history_mc_plus_trl_log | 0.025861880330 | 0.012150000000 | 0.166667 | 0.090691071429 | 0.333333 |
| history_model_dp | 0.025861880330 | 0.012150000000 | 0.166667 | 0.090691071429 | 0.333333 |
| history_trl_log | 0.025861880330 | 0.012150000000 | 0.166667 | 0.090691071429 | 0.333333 |
| latent_oracle_dp | 0.000000000000 | 0.000000000000 | 0.500000 | 0.000000000000 | 0.000000 |
| observation_empirical_model_dp | 0.038351585204 | 0.018225000000 | 0.000000 | 0.147352500000 | 0.500000 |
| observation_trl_log | 0.038351585204 | 0.018225000000 | 0.000000 | 0.147352500000 | 0.500000 |

## Decision Findings

- Observation-only aliasing failure: `True`
- Cue-sufficient MC+TRL-log improvement vs MC-only: `1.000000`
- History-model DP explains all gains: `True`
- Leakage-free training keys: `True`

## Interpretation

Observation-only methods fail under aliasing, and bounded history improves strongly when cues are sufficient. Cue-noisy and cue-insufficient families separate representation sufficiency from oracle disambiguation. History MC+TRL-log improves over MC-only, but the gains are fully explained by history-model DP, so this is representation/context evidence and a boundary result for TRL algorithmic value.

## Artifacts

- `research/sto_trl/artifacts/0013/randomized_pomdp_context_audit.py`
- `research/sto_trl/artifacts/0013/raw_metrics.json`
- `research/sto_trl/artifacts/0013/metrics.csv`
- `research/sto_trl/artifacts/0013/family_summary.csv`
- `research/sto_trl/artifacts/0013/context_summary.csv`
- `research/sto_trl/artifacts/0013/coverage_diagnostics.json`
- `research/sto_trl/artifacts/0013/offline_datasets.json`
- `research/sto_trl/artifacts/0013/transition_tables.json`
- `research/sto_trl/artifacts/0013/value_tables.json`
- `research/sto_trl/artifacts/0013/leakage_checks.json`
