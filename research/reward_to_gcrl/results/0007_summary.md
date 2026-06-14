# Experiment 0007 Summary

## Verdict

RiverSwim coverage dose-response status: **completed**.

Recommendation: **move_next_to_tabular_auxiliary_real_state_goals**.

## Key Metrics

- Runs: `120` (`4` behaviors x `3` gammas x `10` seeds)
- Transition budget per run: `150000`
- Starved runs: `30`
- Borderline runs: `55`
- Adequately covered runs: `35`
- Target mean match rate: `1`
- Sampled variance exceeds soft terminal-sampling variance rate: `1`
- Mean `g_plus` events per 10000 transitions: `5.39722`
- Mean right reward events per 10000 transitions: `232.197`
- Mean final soft Bellman residual: `0.0018651`
- Mean final sampled Bellman residual: `0.00631323`
- Mean final soft value error: `0.123756`
- Mean final sampled value error: `0.133115`

## Coverage Dose Response

| Bin | Runs | Right rewards / 10k | Soft-sampled residual delta | Soft-sampled value-error delta | Soft-sampled raw-return delta | Residual/value disagreement |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| starved | 30 | 11.4222 | -0.00277697 | 0.0401128 | 49.9263 | True |
| borderline | 55 | 164.088 | -0.00478021 | -0.00317412 | 45.7185 | False |
| adequate | 35 | 528.461 | -0.00535871 | -0.0614823 | 54.0566 | False |

Regression target: `soft_minus_sampled_final_value_error`; right-reward coefficient: `-0.000193094`; R^2: `0.39568`.

## Interpretation

Coverage dose response completed: sampled targets match deterministic soft marginal targets within tolerance and have higher terminal-sampling variance in every run. Soft learning advantages are supported on adequate-coverage runs only; starved runs are reported as coverage-limited diagnostics rather than learning-superiority evidence.

Starved runs are coverage-limited and are not used for learning-superiority claims. Bellman/value disagreement in starved runs: `True`.

Behavior policies are fixed action-probability policies (`uniform_random, mild_right_bias, medium_right_bias, strong_right_bias`) and do not use exact Q or DP-derived action preferences.

## Commands Run

```bash
mkdir -p research/reward_to_gcrl/artifacts/0007 research/reward_to_gcrl/results
conda run -n autoresearcher_reward_to_gcrl python --version
conda run -n autoresearcher_reward_to_gcrl python -m py_compile research/reward_to_gcrl/artifacts/0007/run_riverswim_coverage_dose_response.py
conda run -n autoresearcher_reward_to_gcrl python research/reward_to_gcrl/artifacts/0007/run_riverswim_coverage_dose_response.py --check-only
conda run -n autoresearcher_reward_to_gcrl python research/reward_to_gcrl/artifacts/0007/run_riverswim_coverage_dose_response.py
conda run -n autoresearcher_reward_to_gcrl python -m jsonschema -i research/reward_to_gcrl/results/0007_result.json schemas/result.schema.json
conda run -n autoresearcher_reward_to_gcrl python scripts/validate_artifacts.py --repo-root . --json research/reward_to_gcrl/results/0007_result.json --schema schemas/result.schema.json --check-result-artifacts
```

## Artifacts

- `research/reward_to_gcrl/artifacts/0007/run_riverswim_coverage_dose_response.py`
- `research/reward_to_gcrl/artifacts/0007/local_compatibility_check.json`
- `research/reward_to_gcrl/artifacts/0007/environment_audit.json`
- `research/reward_to_gcrl/artifacts/0007/exact_dp_references.json`
- `research/reward_to_gcrl/artifacts/0007/per_seed_metrics.json`
- `research/reward_to_gcrl/artifacts/0007/per_seed_summary.csv`
- `research/reward_to_gcrl/artifacts/0007/learning_curves.json`
- `research/reward_to_gcrl/artifacts/0007/learning_curves.csv`
- `research/reward_to_gcrl/artifacts/0007/raw_metrics.json`
- `research/reward_to_gcrl/artifacts/0007/progress.jsonl`
