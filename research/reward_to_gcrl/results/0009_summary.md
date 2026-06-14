# Experiment 0009 Summary

## Verdict

Low-rank FourRooms auxiliary diagnostic status: **completed**.

Conservative label: **negative_transfer**.

Recommendation: **stop_auxiliary_goal_claims_for_now**.

## Key Metrics

- Adequate-coverage seeds: `10` / `10`
- Terminal-only mean g_plus scaled value error: `0.0731219`
- Combined mean g_plus scaled value error: `16.8939`
- Relative value-error improvement: `-230.037`
- Terminal-only mean Bellman residual: `0.000955849`
- Combined mean Bellman residual: `0.0364139`
- Relative Bellman-residual improvement: `-37.0959`
- Mean reward-policy disagreement delta: `0.526337`
- Combined mean real-state goal value error: `0.919111`
- Combined mean goal-reaching success rate: `0.00371795`

## Interpretation

Combined auxiliary training worsened a g_plus metric or reward-policy disagreement under adequate replay coverage; auxiliary-goal benefit is not supported.

This is a single predeclared rank-4 NumPy checkpoint. It does not make publishable auxiliary-goal claims.

## Commands Run

```bash
mkdir -p research/reward_to_gcrl/artifacts/0009 research/reward_to_gcrl/results
conda run -n autoresearcher_reward_to_gcrl python --version
conda run -n autoresearcher_reward_to_gcrl python -m py_compile research/reward_to_gcrl/artifacts/0009/run_fourrooms_lowrank_auxiliary.py
conda run -n autoresearcher_reward_to_gcrl python research/reward_to_gcrl/artifacts/0009/run_fourrooms_lowrank_auxiliary.py --check-only
conda run -n autoresearcher_reward_to_gcrl python research/reward_to_gcrl/artifacts/0009/run_fourrooms_lowrank_auxiliary.py
conda run -n autoresearcher_reward_to_gcrl python -m jsonschema -i research/reward_to_gcrl/results/0009_result.json schemas/result.schema.json
conda run -n autoresearcher_reward_to_gcrl python scripts/validate_artifacts.py --repo-root . --json research/reward_to_gcrl/results/0009_result.json --schema schemas/result.schema.json --check-result-artifacts
```

## Artifacts

- `research/reward_to_gcrl/artifacts/0009/run_fourrooms_lowrank_auxiliary.py`
- `research/reward_to_gcrl/artifacts/0009/local_compatibility_check.json`
- `research/reward_to_gcrl/artifacts/0009/environment_audit.json`
- `research/reward_to_gcrl/artifacts/0009/exact_dp_references.json`
- `research/reward_to_gcrl/artifacts/0009/per_seed_metrics.json`
- `research/reward_to_gcrl/artifacts/0009/per_seed_summary.csv`
- `research/reward_to_gcrl/artifacts/0009/replay_datasets.npz`
- `research/reward_to_gcrl/artifacts/0009/raw_metrics.json`
- `research/reward_to_gcrl/artifacts/0009/progress.jsonl`
