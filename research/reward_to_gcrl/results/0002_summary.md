# Experiment 0002 Summary

## Verdict

The blocked 0002 gate is **satisfied** for the stated equivalence test.

## Key Metrics

- Transition table hash: `f6fa1c509349d50f18e13b6309b3f051c6cef9a8fcdab25f1332537f521d40a2`
- Exact DP max `abs(F_gplus_star / (1 - gamma) - Q_norm_star)`: `9.71198232946e-10`
- Paired learning runs: `20` across `2` gamma values and `10` seeds
- Learned max scaled value error on sufficiently visited pairs: `5.11590769747e-13`
- Max tie-aware greedy policy disagreement rate: `0`
- Mean raw return, Q policy: `-200`
- Mean raw return, scaled `g_plus` policy: `-200`
- Mean success rate, Q policy: `0`
- Mean success rate, scaled `g_plus` policy: `0`

## Interpretation

The local deterministic CliffWalking table resolves the previous Gymnasium compatibility blocker. Exact DP passes the scaled soft-successor equivalence with max error 9.71198e-10. Paired tabular learners preserve the same values after scaling and have zero tie-aware greedy-policy disagreement on comparable learned states. The raw CliffWalking evaluation is diagnostic: with the declared normalization, the paired policies agree exactly even though the normalized objective can prefer continuing reward over reaching the raw task goal.

The local audit records the grid, start, goal, cliff cells, action mapping, off-grid behavior, cliff reset behavior, terminal behavior, raw rewards, normalized rewards, terminal mask, and full transition table hash. No Gymnasium environment was used for the transition semantics.

## Commands Run

```bash
mkdir -p research/reward_to_gcrl/artifacts/0002 research/reward_to_gcrl/results
conda run -n autoresearcher_reward_to_gcrl python research/reward_to_gcrl/artifacts/0002/run_local_cliffwalking_equivalence.py --check-only
conda run -n autoresearcher_reward_to_gcrl python research/reward_to_gcrl/artifacts/0002/run_local_cliffwalking_equivalence.py
conda run -n autoresearcher_reward_to_gcrl python -m jsonschema -i research/reward_to_gcrl/results/0002_result.json schemas/result.schema.json
conda run -n autoresearcher_reward_to_gcrl python scripts/validate_artifacts.py --repo-root . --json research/reward_to_gcrl/results/0002_result.json --schema schemas/result.schema.json --check-result-artifacts
```

## Artifacts

- `research/reward_to_gcrl/artifacts/0002/run_local_cliffwalking_equivalence.py`
- `research/reward_to_gcrl/artifacts/0002/local_compatibility_check.json`
- `research/reward_to_gcrl/artifacts/0002/environment_audit.json`
- `research/reward_to_gcrl/artifacts/0002/exact_dp_metrics.json`
- `research/reward_to_gcrl/artifacts/0002/exact_value_tables.json`
- `research/reward_to_gcrl/artifacts/0002/paired_learning_metrics.json`
- `research/reward_to_gcrl/artifacts/0002/paired_seed_metrics.csv`
- `research/reward_to_gcrl/artifacts/0002/raw_metrics.json`
- `research/reward_to_gcrl/artifacts/0002/progress.jsonl`
