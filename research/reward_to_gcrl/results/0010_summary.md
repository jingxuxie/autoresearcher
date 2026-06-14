# Experiment 0010 Summary

## Verdict

Low-rank FourRooms loss-scale diagnostic status: **completed**.

Conservative label: **auxiliary_unsupported_for_lowrank**.

Recommendation: **write_negative_result**.

## Key Metrics

- Adequate-coverage seeds: `10` / `10`
- Original 0009 reproduction: `True`
- Any repaired variant promising: `False`
- Any repaired variant matches terminal g_plus metrics: `False`

| Variant | g_plus value error | Bellman residual | Policy disagreement | Real-goal value error | Mean aux/g_plus U-grad ratio |
| --- | ---: | ---: | ---: | ---: | --- |
| terminal_only | 0.0731219 | 0.000955849 | 0.140909 | 0.0183195 | 0.0 |
| combined_lambda_1_reproduction | 16.8939 | 0.0364139 | 0.667246 | 0.919111 | 4.3423814050417855 |
| combined_loss_balanced | 7.37704 | 0.0179085 | 0.650823 | 0.767482 | 451.2730071367794 |
| staged_real_goal_pretrain_then_gplus_finetune | 18.5798 | 0.0508149 | 0.652206 | 0.897855 | 0.0 |

## Interpretation

Original negative transfer reproduced, and neither repaired variant matched terminal-only on g_plus value error and Bellman residual. Auxiliary real-state goals should be paused for this low-rank architecture.

This is a tightly predeclared CPU NumPy diagnostic. It does not make publishable auxiliary-goal claims.

## Commands Run

```bash
mkdir -p research/reward_to_gcrl/artifacts/0010 research/reward_to_gcrl/results
conda run -n autoresearcher_reward_to_gcrl python --version
conda run -n autoresearcher_reward_to_gcrl python -m py_compile research/reward_to_gcrl/artifacts/0010/run_fourrooms_lowrank_aux_diagnostic.py
conda run -n autoresearcher_reward_to_gcrl python research/reward_to_gcrl/artifacts/0010/run_fourrooms_lowrank_aux_diagnostic.py --check-only
conda run -n autoresearcher_reward_to_gcrl python research/reward_to_gcrl/artifacts/0010/run_fourrooms_lowrank_aux_diagnostic.py
conda run -n autoresearcher_reward_to_gcrl python -m jsonschema -i research/reward_to_gcrl/results/0010_result.json schemas/result.schema.json
conda run -n autoresearcher_reward_to_gcrl python scripts/validate_artifacts.py --repo-root . --json research/reward_to_gcrl/results/0010_result.json --schema schemas/result.schema.json --check-result-artifacts
```

## Artifacts

- `research/reward_to_gcrl/artifacts/0010/run_fourrooms_lowrank_aux_diagnostic.py`
- `research/reward_to_gcrl/artifacts/0010/local_compatibility_check.json`
- `research/reward_to_gcrl/artifacts/0010/environment_audit.json`
- `research/reward_to_gcrl/artifacts/0010/exact_dp_references.json`
- `research/reward_to_gcrl/artifacts/0010/per_seed_metrics.json`
- `research/reward_to_gcrl/artifacts/0010/per_seed_summary.csv`
- `research/reward_to_gcrl/artifacts/0010/replay_datasets.npz`
- `research/reward_to_gcrl/artifacts/0010/raw_metrics.json`
- `research/reward_to_gcrl/artifacts/0010/progress.jsonl`
