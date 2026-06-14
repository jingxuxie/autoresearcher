# Experiment 0006 Summary

## Verdict

Non-oracle RiverSwim diagnostic status: **completed**.

## Key Metrics

- Runs: `60` (`2` behaviors x `3` gammas x `10` seeds)
- Transition budget per run: `150000`
- Adequately covered runs: `30`
- Coverage-starved runs: `30`
- Target mean match rate: `1`
- Sampled variance exceeds soft terminal-sampling variance rate: `1`
- Mean `g_plus` events per 10000 transitions: `6.63667`
- Mean right reward events per 10000 transitions: `287.14`
- Mean final soft Bellman residual: `0.00192471`
- Mean final sampled Bellman residual: `0.00613207`
- Mean final soft value error: `0.152365`
- Mean final sampled value error: `0.162459`

## Interpretation

With non-oracle behavior streams, sampled targets remain unbiased within tolerance and higher variance. Coverage is explicitly split by the predeclared right-reward threshold; on adequately covered runs, soft retains the residual/value advantage.

Behavior policies are fixed action-probability policies (`uniform_random` and `right_biased_random`) and do not use exact Q or DP-derived action preferences.

## Commands Run

```bash
mkdir -p research/reward_to_gcrl/artifacts/0006 research/reward_to_gcrl/results
conda run -n autoresearcher_reward_to_gcrl python --version
conda run -n autoresearcher_reward_to_gcrl python -m py_compile research/reward_to_gcrl/artifacts/0006/run_riverswim_nonoracle.py
conda run -n autoresearcher_reward_to_gcrl python research/reward_to_gcrl/artifacts/0006/run_riverswim_nonoracle.py --check-only
conda run -n autoresearcher_reward_to_gcrl python research/reward_to_gcrl/artifacts/0006/run_riverswim_nonoracle.py
conda run -n autoresearcher_reward_to_gcrl python -m jsonschema -i research/reward_to_gcrl/results/0006_result.json schemas/result.schema.json
conda run -n autoresearcher_reward_to_gcrl python scripts/validate_artifacts.py --repo-root . --json research/reward_to_gcrl/results/0006_result.json --schema schemas/result.schema.json --check-result-artifacts
```

## Artifacts

- `research/reward_to_gcrl/artifacts/0006/run_riverswim_nonoracle.py`
- `research/reward_to_gcrl/artifacts/0006/local_compatibility_check.json`
- `research/reward_to_gcrl/artifacts/0006/environment_audit.json`
- `research/reward_to_gcrl/artifacts/0006/exact_dp_references.json`
- `research/reward_to_gcrl/artifacts/0006/per_seed_metrics.json`
- `research/reward_to_gcrl/artifacts/0006/per_seed_summary.csv`
- `research/reward_to_gcrl/artifacts/0006/learning_curves.json`
- `research/reward_to_gcrl/artifacts/0006/learning_curves.csv`
- `research/reward_to_gcrl/artifacts/0006/raw_metrics.json`
- `research/reward_to_gcrl/artifacts/0006/progress.jsonl`
