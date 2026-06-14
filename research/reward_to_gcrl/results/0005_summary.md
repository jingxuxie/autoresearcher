# Experiment 0005 Summary

## Verdict

RiverSwim sampled-vs-soft diagnostic status: **completed**.

## Key Metrics

- Runs: `30` (`3` gammas x `10` seeds)
- Transition budget per run: `200000`
- Mean `g_plus` events per 10000 transitions: `66.6083`
- Mean right-end occupancy rate: `0.326288`
- Mean right reward events per 10000 transitions: `3060.1`
- Target mean match rate: `1`
- Sampled variance exceeds soft terminal-sampling variance rate: `1`
- Soft residual dominance rate: `1`
- Mean final soft Bellman residual: `0.00248977`
- Mean final sampled Bellman residual: `0.0124188`
- Mean final soft value error: `0.00455664`
- Mean final sampled value error: `0.113453`

## Interpretation

The RiverSwim diagnostic supports the hypothesis: sampled targets match the deterministic soft marginal target within Monte Carlo tolerance while retaining higher terminal-sampling variance, and the deterministic soft learner has lower or faster Bellman residual reduction in most matched-stream runs.

The environment is a continuing 6-state RiverSwim chain. Original transitions never terminate; sampled `g_plus` and `g_minus` absorbing events never bootstrap, and continued sampled targets use `max_a M(s_next,a)` with no extra gamma.

## Commands Run

```bash
mkdir -p research/reward_to_gcrl/artifacts/0005 research/reward_to_gcrl/results
conda run -n autoresearcher_reward_to_gcrl python --version
conda run -n autoresearcher_reward_to_gcrl python -m py_compile research/reward_to_gcrl/artifacts/0005/run_riverswim_sampled_vs_soft.py
conda run -n autoresearcher_reward_to_gcrl python research/reward_to_gcrl/artifacts/0005/run_riverswim_sampled_vs_soft.py --check-only
conda run -n autoresearcher_reward_to_gcrl python research/reward_to_gcrl/artifacts/0005/run_riverswim_sampled_vs_soft.py
conda run -n autoresearcher_reward_to_gcrl python -m jsonschema -i research/reward_to_gcrl/results/0005_result.json schemas/result.schema.json
conda run -n autoresearcher_reward_to_gcrl python scripts/validate_artifacts.py --repo-root . --json research/reward_to_gcrl/results/0005_result.json --schema schemas/result.schema.json --check-result-artifacts
```

## Artifacts

- `research/reward_to_gcrl/artifacts/0005/run_riverswim_sampled_vs_soft.py`
- `research/reward_to_gcrl/artifacts/0005/local_compatibility_check.json`
- `research/reward_to_gcrl/artifacts/0005/environment_audit.json`
- `research/reward_to_gcrl/artifacts/0005/exact_dp_references.json`
- `research/reward_to_gcrl/artifacts/0005/per_seed_metrics.json`
- `research/reward_to_gcrl/artifacts/0005/per_seed_summary.csv`
- `research/reward_to_gcrl/artifacts/0005/learning_curves.json`
- `research/reward_to_gcrl/artifacts/0005/learning_curves.csv`
- `research/reward_to_gcrl/artifacts/0005/raw_metrics.json`
- `research/reward_to_gcrl/artifacts/0005/progress.jsonl`
