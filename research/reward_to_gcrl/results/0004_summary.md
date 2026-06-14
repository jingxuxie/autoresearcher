# Experiment 0004 Summary

## Verdict

Conservative verdict: **learning-improvement**.

## Key Metrics

- Runs: `30` (`3` gammas x `10` seeds)
- Transition budget per run: `100000`
- Mean `g_plus` events per 10000 transitions: `63.79`
- Target mean match rate: `1`
- Sampled variance exceeds soft terminal-sampling variance rate: `1`
- Mean final soft Bellman residual: `1.09866e-17`
- Mean final sampled Bellman residual: `0.00586335`
- Mean final soft value error: `3.05022e-17`
- Mean final sampled value error: `0.0284064`
- Mean soft success rate: `1`
- Mean sampled success rate: `0`

## Interpretation

The repaired chain preserves the raw policy under identity normalization. Sampled targets match the deterministic soft marginal target within the predeclared Monte Carlo tolerance, have positive sampling variance, and the deterministic soft learner achieves lower mean final Bellman residual with statistically non-worse value error and policy quality.

The chain uses identity reward normalization: normalized reward equals raw reward, with success reward `1` and all other rewards `0`. Exact DP verifies raw and normalized policies agree on non-terminal non-tie decision states.

## Commands Run

```bash
mkdir -p research/reward_to_gcrl/artifacts/0004 research/reward_to_gcrl/results
conda run -n autoresearcher_reward_to_gcrl python --version
conda run -n autoresearcher_reward_to_gcrl python -m py_compile research/reward_to_gcrl/artifacts/0004/run_repaired_sampled_vs_soft.py
conda run -n autoresearcher_reward_to_gcrl python research/reward_to_gcrl/artifacts/0004/run_repaired_sampled_vs_soft.py --check-only
conda run -n autoresearcher_reward_to_gcrl python research/reward_to_gcrl/artifacts/0004/run_repaired_sampled_vs_soft.py
conda run -n autoresearcher_reward_to_gcrl python -m jsonschema -i research/reward_to_gcrl/results/0004_result.json schemas/result.schema.json
conda run -n autoresearcher_reward_to_gcrl python scripts/validate_artifacts.py --repo-root . --json research/reward_to_gcrl/results/0004_result.json --schema schemas/result.schema.json --check-result-artifacts
```

## Artifacts

- `research/reward_to_gcrl/artifacts/0004/run_repaired_sampled_vs_soft.py`
- `research/reward_to_gcrl/artifacts/0004/local_compatibility_check.json`
- `research/reward_to_gcrl/artifacts/0004/environment_audit.json`
- `research/reward_to_gcrl/artifacts/0004/exact_dp_references.json`
- `research/reward_to_gcrl/artifacts/0004/per_seed_metrics.json`
- `research/reward_to_gcrl/artifacts/0004/per_seed_summary.csv`
- `research/reward_to_gcrl/artifacts/0004/learning_curves.json`
- `research/reward_to_gcrl/artifacts/0004/learning_curves.csv`
- `research/reward_to_gcrl/artifacts/0004/raw_metrics.json`
- `research/reward_to_gcrl/artifacts/0004/progress.jsonl`
