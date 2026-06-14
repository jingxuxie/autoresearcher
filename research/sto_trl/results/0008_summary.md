# Experiment 0008 Summary

## Objective

Map finite-coverage identifiability for tabular risky shortcuts before adding new stochastic TRL algorithms.

## Commands Run

```bash
mkdir -p research/sto_trl/artifacts/0008 research/sto_trl/results
conda run -n autoresearcher_sto_trl python research/sto_trl/artifacts/0008/identifiability_grid.py
conda run -n autoresearcher_sto_trl python scripts/validate_artifacts.py --repo-root . --json research/sto_trl/results/0008_result.json --schema schemas/result.schema.json --check-result-artifacts
```

## Grid

- True risky success probabilities: `[0.1, 0.25, 0.5, 0.75, 0.9]`
- Safe route lengths: `[2, 3, 4]`
- Risky sample counts: `[4, 8, 16]`
- Observed successes: every integer from `0` to `risky_samples`
- Total cells: `465`

## Key Counts

- Classification counts: `{'no_success': 45, 'matched_identifiable': 44, 'ambiguous': 95, 'lucky_only': 45, 'identifiable': 136, 'prior_dependent': 100}`
- Tag counts: `{'no_success': 45, 'matched': 129, 'identifiable': 230, 'ambiguous': 235, 'lucky_only': 45, 'prior_dependent': 130}`
- Impossibility/prior-dependent cells: `285`
- Deterministic chain guard passed: `True`

## Method Summary

| Method | Action accuracy | Mean policy regret |
| --- | ---: | ---: |
| empirical_risky_value | 0.690323 | 0.075565161290 |
| empirical_transition_dp | 0.690323 | 0.075565161290 |
| hoeffding_lcb_delta_0_2 | 0.797849 | 0.019136129032 |
| hoeffding_ucb_delta_0_2 | 0.516129 | 0.157349032258 |
| posterior_lower_q10_beta_1_1 | 0.787097 | 0.026568387097 |
| posterior_mean_beta_1_1 | 0.741935 | 0.051303870968 |
| posterior_upper_q90_beta_1_1 | 0.640860 | 0.101171612903 |
| raw_trl | 0.258065 | 0.271358709677 |
| trl_log | 0.690323 | 0.075565161290 |

## Interpretation

The grid is useful as an identifiability map: it separates cells where empirical transition estimates match exact action choice from lucky-only, no-success, ambiguous, and prior-dependent cells where explicit priors are required.

## Artifacts

- `research/sto_trl/artifacts/0008/identifiability_grid.py`
- `research/sto_trl/artifacts/0008/raw_grid.json`
- `research/sto_trl/artifacts/0008/metrics.csv`
- `research/sto_trl/artifacts/0008/regret_heatmap.csv`
- `research/sto_trl/artifacts/0008/action_choice_grid.csv`
- `research/sto_trl/artifacts/0008/impossibility_cases.json`
- `research/sto_trl/artifacts/0008/coverage_diagnostics.json`
- `research/sto_trl/artifacts/0008/transition_tables.json`
- `research/sto_trl/artifacts/0008/value_tables.json`
