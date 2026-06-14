# Experiment 0008 Summary

## Verdict

FourRooms vector SSM sanity check status: **completed**.

## Key Metrics

- Gamma values: `[0.95, 0.99]`
- Open states: `40`
- Goal slices: `41`
- Max `M_vector[:,:,g_plus] - M_terminal_only`: `0`
- Max `M_vector[:,:,g_plus]/(1-gamma) - Q_norm`: `1.11022e-16`
- Max real-state goal value error: `0`
- Mean real-state goal value error: `0`
- Min greedy goal success rate: `1`
- Mean first-step shortest-path distance reduction: `1`
- Max reward-policy disagreement: `0`

## Interpretation

The vector SSM slices are numerically independent in this tabular FourRooms check: the g_plus slice matches terminal-only soft learning, scaled g_plus matches normalized Q, and real-state goal slices match exact reachability references with successful greedy goal reaching.

This is an independent-slice tabular sanity check only. It does not claim auxiliary-goal reward improvement without shared parameters.

## Commands Run

```bash
mkdir -p research/reward_to_gcrl/artifacts/0008 research/reward_to_gcrl/results
conda run -n autoresearcher_reward_to_gcrl python --version
conda run -n autoresearcher_reward_to_gcrl python -m py_compile research/reward_to_gcrl/artifacts/0008/run_fourrooms_vector_ssm.py
conda run -n autoresearcher_reward_to_gcrl python research/reward_to_gcrl/artifacts/0008/run_fourrooms_vector_ssm.py --check-only
conda run -n autoresearcher_reward_to_gcrl python research/reward_to_gcrl/artifacts/0008/run_fourrooms_vector_ssm.py
conda run -n autoresearcher_reward_to_gcrl python -m jsonschema -i research/reward_to_gcrl/results/0008_result.json schemas/result.schema.json
conda run -n autoresearcher_reward_to_gcrl python scripts/validate_artifacts.py --repo-root . --json research/reward_to_gcrl/results/0008_result.json --schema schemas/result.schema.json --check-result-artifacts
```

## Artifacts

- `research/reward_to_gcrl/artifacts/0008/run_fourrooms_vector_ssm.py`
- `research/reward_to_gcrl/artifacts/0008/local_compatibility_check.json`
- `research/reward_to_gcrl/artifacts/0008/environment_audit.json`
- `research/reward_to_gcrl/artifacts/0008/exact_dp_references.json`
- `research/reward_to_gcrl/artifacts/0008/raw_metrics.json`
- `research/reward_to_gcrl/artifacts/0008/all_raw_metrics.json`
- `research/reward_to_gcrl/artifacts/0008/per_goal_metrics.json`
- `research/reward_to_gcrl/artifacts/0008/per_goal_metrics.csv`
- `research/reward_to_gcrl/artifacts/0008/goal_heatmap_arrow_data.json`
- `research/reward_to_gcrl/artifacts/0008/goal_heatmap_arrow_data.csv`
- `research/reward_to_gcrl/artifacts/0008/progress.jsonl`
