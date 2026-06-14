# Experiment 0011 Summary

## Objective

Run a randomized tabular equivalence and generalization audit for posterior TRL-log versus prior-matched posterior model DP.

## Commands Run

```bash
mkdir -p research/sto_trl/artifacts/0011 research/sto_trl/results
conda run -n autoresearcher_sto_trl python research/sto_trl/artifacts/0011/randomized_equivalence_audit.py
conda run -n autoresearcher_sto_trl python scripts/validate_artifacts.py --repo-root . --json research/sto_trl/results/0011_result.json --schema schemas/result.schema.json --check-result-artifacts
```

## Suite

- Families: `['branch_chain', 'stochastic_stitching', 'teleporter']`
- Seeds per family: `[0, 1, 2, 3, 4]`
- Total MDPs: `15`
- Label horizon cutoff: `2`

## Method Summary

| Method | Action accuracy | Heldout MSE | Policy regret | Risky rate | Q overestimation | Calibration error |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| empirical_model_dp | 0.400000 | 0.037651669545 | 0.068406683449 | 0.400000 | 0.072144533180 | 0.226524283748 |
| mc_supervised | 0.400000 | 0.432704401393 | 0.028055308380 | 0.000000 | 0.000000000000 | 0.569045217387 |
| posterior_lower_q10_model_dp | 0.466667 | 0.035925214745 | 0.022182232310 | 0.066667 | 0.016269178882 | 0.261509935151 |
| posterior_mc_plus_trl_log | 0.600000 | 0.032259348981 | 0.012917304567 | 0.200000 | 0.045769378882 | 0.214221377748 |
| posterior_mean_model_dp | 0.600000 | 0.032259348981 | 0.012917304567 | 0.200000 | 0.045769378882 | 0.214221377748 |
| posterior_trl_log | 0.600000 | 0.032259348981 | 0.012917304567 | 0.200000 | 0.045769378882 | 0.214221377748 |
| trl_log | 0.400000 | 0.037651669545 | 0.068406683449 | 0.400000 | 0.072144533180 | 0.226524283748 |
| trl_raw | 0.400000 | 0.041975170307 | 0.097601010862 | 0.800000 | 0.154109702482 | 0.294064622351 |

## Equivalence Audit

- Positive posterior TRL evidence: `False`
- Near-equivalent to prior-matched posterior model DP: `True`
- Max posterior_trl_log value difference vs model DP: `0`
- Posterior_trl_log action disagreement rate vs model DP: `0`
- Matched risk-optimal action preserved: `True`

## Interpretation

The randomized tiny-suite audit supports the 0010 boundary result: posterior TRL-log variants match the prior-matched posterior mean model-DP baseline within numerical tolerance across branch-chain, stochastic stitching, and teleporter families. Any aggregate improvement over plain TRL-log is explained by the shared posterior transition prior, not by a distinct transitive posterior TRL effect.

## Artifacts

- `research/sto_trl/artifacts/0011/randomized_equivalence_audit.py`
- `research/sto_trl/artifacts/0011/raw_metrics.json`
- `research/sto_trl/artifacts/0011/metrics.csv`
- `research/sto_trl/artifacts/0011/family_summary.csv`
- `research/sto_trl/artifacts/0011/regime_summary.csv`
- `research/sto_trl/artifacts/0011/equivalence_diagnostics.json`
- `research/sto_trl/artifacts/0011/coverage_diagnostics.json`
- `research/sto_trl/artifacts/0011/offline_datasets.json`
- `research/sto_trl/artifacts/0011/transition_tables.json`
- `research/sto_trl/artifacts/0011/value_tables.json`
