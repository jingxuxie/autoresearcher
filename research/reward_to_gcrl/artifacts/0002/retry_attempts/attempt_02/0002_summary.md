# Experiment 0002 Summary

## Compatibility Gate

Status: `failed`.

The supplied plan requires `gym.make("CliffWalking-v0")`. In the ready project environment, Gymnasium `1.3.0` rejected that environment id with `DeprecatedEnv`:

```text
Environment version v0 for `CliffWalking` is deprecated. Please use `CliffWalking-v1` instead.
```

Per the executor rule for compatibility failures, the DP and paired-learning phases were not run and no fallback to `CliffWalking-v1` or `CliffWalkingEnv(is_slippery=False)` was used.

## Commands Run

```bash
mkdir -p research/reward_to_gcrl/artifacts/0002 research/reward_to_gcrl/results
conda run -n autoresearcher_reward_to_gcrl python research/reward_to_gcrl/artifacts/0002/check_cliffwalking_v0_compatibility.py
conda run -n autoresearcher_reward_to_gcrl python -m jsonschema -i research/reward_to_gcrl/results/0002_result.json schemas/result.schema.json
conda run -n autoresearcher_reward_to_gcrl python scripts/validate_artifacts.py --repo-root . --json research/reward_to_gcrl/results/0002_result.json --schema schemas/result.schema.json --check-result-artifacts
```

## Planned But Not Run

- Reward normalization: `r_bar = (original_reward + 100) / 99`, mapping cliff `-100` to `0.0` and step/goal `-1` to `1.0`.
- Terminal mask: bootstrap would be zero when `terminated=True`.
- Gamma values: `[0.95, 0.99]`.
- Seeds: `[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]`.
- Episode budget: `5000`.

## Outcome

This is a failed compatibility result, not evidence against the soft successor equivalence hypothesis. The next plan should explicitly allow `CliffWalking-v1` or the direct non-slippery `CliffWalkingEnv` class if those semantics are acceptable.

## Artifacts

- `research/reward_to_gcrl/artifacts/0002/check_cliffwalking_v0_compatibility.py`
- `research/reward_to_gcrl/artifacts/0002/compatibility_check.json`
- `research/reward_to_gcrl/artifacts/0002/progress.jsonl`
