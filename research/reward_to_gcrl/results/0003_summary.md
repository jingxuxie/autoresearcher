# Experiment 0003 Summary

## Verdict

The sampled-vs-soft tabular gate is **satisfied**.

## Key Metrics

- Runs: `30` (`3` gammas x `10` seeds)
- Transition budget per run: `200000`
- Mean `g_plus` events per 10000 transitions: `212.67`
- Target mean match rate: `1`
- Sampled variance exceeds soft terminal-sampling variance rate: `1`
- Soft lower/faster error dominance rate: `0.566667`
- Mean final soft value error on sufficiently visited pairs: `0.0821131`
- Mean final sampled value error on sufficiently visited pairs: `0.0815604`
- Mean final soft Bellman residual on sufficiently visited pairs: `0.0387504`
- Mean final sampled Bellman residual on sufficiently visited pairs: `0.0412461`

## Interpretation

The sampled augmented target is unbiased within the predeclared Monte Carlo tolerance in all gamma/seed runs, but its terminal sampling variance is strictly positive while the deterministic soft target has zero terminal sampling variance. Under the matched transition stream, the soft learner has lower final or earlier-threshold value error in most runs.

The sampled learner uses `g_plus -> 1`, `g_minus -> 0`, and `continue -> max_a M(s_next,a)` with no extra gamma factor. The deterministic soft update uses the corresponding conditional expectation. Terminal bootstraps are masked for original terminal transitions, and sampled `g_plus`/`g_minus` absorbing events never bootstrap.

## Commands Run

```bash
mkdir -p research/reward_to_gcrl/artifacts/0003 research/reward_to_gcrl/results
conda run -n autoresearcher_reward_to_gcrl python --version
conda run -n autoresearcher_reward_to_gcrl python -m py_compile research/reward_to_gcrl/artifacts/0003/run_sampled_vs_soft_cliffwalking.py
conda run -n autoresearcher_reward_to_gcrl python research/reward_to_gcrl/artifacts/0003/run_sampled_vs_soft_cliffwalking.py --check-only
conda run -n autoresearcher_reward_to_gcrl python research/reward_to_gcrl/artifacts/0003/run_sampled_vs_soft_cliffwalking.py
conda run -n autoresearcher_reward_to_gcrl python -m jsonschema -i research/reward_to_gcrl/results/0003_result.json schemas/result.schema.json
conda run -n autoresearcher_reward_to_gcrl python scripts/validate_artifacts.py --repo-root . --json research/reward_to_gcrl/results/0003_result.json --schema schemas/result.schema.json --check-result-artifacts
```

## Artifacts

- `research/reward_to_gcrl/artifacts/0003/run_sampled_vs_soft_cliffwalking.py`
- `research/reward_to_gcrl/artifacts/0003/local_compatibility_check.json`
- `research/reward_to_gcrl/artifacts/0003/environment_audit.json`
- `research/reward_to_gcrl/artifacts/0003/exact_soft_dp_reference.json`
- `research/reward_to_gcrl/artifacts/0003/per_seed_metrics.json`
- `research/reward_to_gcrl/artifacts/0003/per_seed_summary.csv`
- `research/reward_to_gcrl/artifacts/0003/learning_curves.json`
- `research/reward_to_gcrl/artifacts/0003/learning_curves.csv`
- `research/reward_to_gcrl/artifacts/0003/raw_metrics.json`
- `research/reward_to_gcrl/artifacts/0003/progress.jsonl`
