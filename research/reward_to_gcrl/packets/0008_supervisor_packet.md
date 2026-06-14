# Supervisor Context: reward_to_gcrl

## Requested action

Choose continue, pivot, stop, or needs_human. If this is iteration 0 with no prior result, propose the first small experiment when the charter is specific enough. If continuing, propose exactly one small experiment. If a human pivot note or next-step review plan exists, treat it as approved human direction and normally choose continue with the next small experiment from that plan, unless it is unsafe or impossible.


## Project charter

# Reward-To-GCRL Soft Successor Charter

## Research Goal

Rapidly test whether a soft successor-measure reward-to-goal conversion can preserve the reward-to-goal equivalence while avoiding the sparse, high-variance terminal sampling used in the sampled MDP-to-GCMDP conversion.

The full prototype plan is in `research/reward_to_gcrl/reward_to_gcrl_soft_successor_prototype_plan.md`. This charter is the compact source of truth for the autoresearcher loop.

## Main Hypothesis

Training the artificial success-goal head with expected terminal mass,

```text
y(s,a,g_plus) = (1 - gamma) * r_bar(s,a) + gamma * max_a' M_target(s',a',g_plus)
```

will match normalized Q-learning in tabular sanity checks while avoiding the high target variance of sampled terminal success events.

A later, separate hypothesis is that auxiliary real-state successor goals can improve low-capacity function approximation for the reward-success goal through shared representations.

## Initial Scope

Start with tiny discrete environments only:

1. One-state synthetic MDP for terminal-event variance diagnostics.
2. CliffWalking for tabular equivalence to normalized Q-learning.
3. Small RiverSwim chains for long-horizon reward propagation.
4. Tiny FourRooms only after the first diagnostics are correct.

Do not start with MuJoCo, AntMaze, image observations, OGBench, large downloads, or expensive neural training.

## Primary Metrics

Use exact or analytically known ground truth whenever possible.

Primary metrics:

- Empirical target mean and variance for sampled versus soft terminal targets.
- Number of sampled `g_plus` events per 10k transitions.
- Max absolute value error between `M_plus / (1 - gamma)` and normalized-reward Q-learning.
- Policy disagreement rate versus normalized Q-learning or exact DP.
- Bellman error to exact DP where available.
- Average return and success rate for the reward-task policy.

Secondary metrics:

- TD target variance during learning.
- Sample efficiency to a fixed return or Bellman-error threshold.
- Real-state goal reachability diagnostics for vector successor-measure variants.
- Interference between auxiliary state-goal loss and the `g_plus` reward head.

## Success Criteria

Early evidence is positive only if small-scale experiments show all of:

- Soft terminal targets and sampled terminal targets have matching means in the one-state diagnostic.
- Soft terminal targets remove the terminal-sampling variance and expose the rarity of `g_plus` events as `gamma` approaches 1.
- In tabular CliffWalking, terminal-only soft successor learning matches normalized Q-learning up to the expected `(1 - gamma)` scaling.
- The learned reward-task policy from `argmax_a M(s,a,g_plus)` has low disagreement with the Q-learning or exact-DP policy.

The first iteration should be considered successful if it creates a reproducible variance diagnostic with raw metrics and clearly verifies the expected mean/variance relationship before implementing larger learners.

## Failure Criteria

Pause or stop before larger experiments if:

- Terminal-only soft successor learning fails to match normalized Q-learning in tabular CliffWalking.
- Reward normalization is ambiguous or not reported.
- Terminal masks are wrong, causing bootstrap after true terminal states.
- The experiment reports only training loss and omits target variance, value error, or policy disagreement.
- Auxiliary state goals improve reward-task performance only by changing the task definition or leaking privileged state.
- The loop attempts MuJoCo, AntMaze, OGBench, large downloads, or long neural training before tabular diagnostics pass.
- Results omit exact commands, raw metrics, or reproducible artifacts.

## Runtime And Compute Budget

Initial experiments should complete in minutes on CPU. GPU may be checked and used if available, but it is not required for milestones 0 through 3.

Use the project conda environment `autoresearcher_reward_to_gcrl`. Add JAX or PyTorch only when a reviewed plan reaches the low-capacity function-approximation milestone.

## First Experiment Guidance

The supervisor should propose exactly one small experiment for iteration 1:

- Implement the one-state variance sanity check under `research/reward_to_gcrl/artifacts/0001/`.
- Sweep `gamma in {0.90, 0.95, 0.99, 0.995}` and `r_bar in {0.01, 0.1, 0.5, 1.0}`.
- Compare sampled Bernoulli terminal targets against the deterministic soft expected target.
- Save empirical means, variances, and `g_plus` event counts per 10k transitions.
- Produce `research/reward_to_gcrl/results/0001_result.json` and `research/reward_to_gcrl/results/0001_summary.md`.

Do not implement neural function approximation in the first run. Optimize for a correct diagnostic that can reveal whether the sampled conversion failure is plausibly an estimator-variance problem.


## Project planning docs

## research/reward_to_gcrl/charter.md

```markdown
# Reward-To-GCRL Soft Successor Charter

## Research Goal

Rapidly test whether a soft successor-measure reward-to-goal conversion can preserve the reward-to-goal equivalence while avoiding the sparse, high-variance terminal sampling used in the sampled MDP-to-GCMDP conversion.

The full prototype plan is in `research/reward_to_gcrl/reward_to_gcrl_soft_successor_prototype_plan.md`. This charter is the compact source of truth for the autoresearcher loop.

## Main Hypothesis

Training the artificial success-goal head with expected terminal mass,

```text
y(s,a,g_plus) = (1 - gamma) * r_bar(s,a) + gamma * max_a' M_target(s',a',g_plus)
```

will match normalized Q-learning in tabular sanity checks while avoiding the high target variance of sampled terminal success events.

A later, separate hypothesis is that auxiliary real-state successor goals can improve low-capacity function approximation for the reward-success goal through shared representations.

## Initial Scope

Start with tiny discrete environments only:

1. One-state synthetic MDP for terminal-event variance diagnostics.
2. CliffWalking for tabular equivalence to normalized Q-learning.
3. Small RiverSwim chains for long-horizon reward propagation.
4. Tiny FourRooms only after the first diagnostics are correct.

Do not start with MuJoCo, AntMaze, image observations, OGBench, large downloads, or expensive neural training.

## Primary Metrics

Use exact or analytically known ground truth whenever possible.

Primary metrics:

- Empirical target mean and variance for sampled versus soft terminal targets.
- Number of sampled `g_plus` events per 10k transitions.
- Max absolute value error between `M_plus / (1 - gamma)` and normalized-reward Q-learning.
- Policy disagreement rate versus normalized Q-learning or exact DP.
- Bellman error to exact DP where available.
- Average return and success rate for the reward-task policy.

Secondary metrics:

- TD target variance during learning.
- Sample efficiency to a fixed return or Bellman-error threshold.
- Real-state goal reachability diagnostics for vector successor-measure variants.
- Interference between auxiliary state-goal loss and the `g_plus` reward head.

## Success Criteria

Early evidence is positive only if small-scale experiments show all of:

- Soft terminal targets and sampled terminal targets have matching means in the one-state diagnostic.
- Soft terminal targets remove the terminal-sampling variance and expose the rarity of `g_plus` events as `gamma` approaches 1.
- In tabular CliffWalking, terminal-only soft successor learning matches normalized Q-learning up to the expected `(1 - gamma)` scaling.
- The learned reward-task policy from `argmax_a M(s,a,g_plus)` has low disagreement with the Q-learning or exact-DP policy.

The first iteration should be considered successful if it creates a reproducible variance diagnostic with raw metrics and clearly verifies the expected mean/variance relationship before implementing larger learners.

## Failure Criteria

Pause or stop before larger experiments if:

- Terminal-only soft successor learning fails to match normalized Q-learning in tabular CliffWalking.
- Reward normalization is ambiguous or not reported.
- Terminal masks are wrong, causing bootstrap after true terminal states.
- The experiment reports only training loss and omits target variance, value error, or policy disagreement.
- Auxiliary state goals improve reward-task performance only by changing the task definition or leaking privileged state.
- The loop attempts MuJoCo, AntMaze, OGBench, large downloads, or long neural training before tabular diagnostics pass.
- Results omit exact commands, raw metrics, or reproducible artifacts.

## Runtime And Compute Budget

Initial experiments should complete in minutes on CPU. GPU may be checked and used if available, but it is not required for milestones 0 through 3.

Use the project conda environment `autoresearcher_reward_to_gcrl`. Add JAX or PyTorch only when a reviewed plan reaches the low-capacity function-approximation milestone.

## First Experiment Guidance

The supervisor should propose exactly one small experiment for iteration 1:

- Implement the one-state variance sanity check under `research/reward_to_gcrl/artifacts/0001/`.
- Sweep `gamma in {0.90, 0.95, 0.99, 0.995}` and `r_bar in {0.01, 0.1, 0.5, 1.0}`.
- Compare sampled Bernoulli terminal targets against the deterministic soft expected target.
- Save empirical means, variances, and `g_plus` event counts per 10k transitions.
- Produce `research/reward_to_gcrl/results/0001_result.json` and `research/reward_to_gcrl/results/0001_summary.md`.

Do not implement neural function approximation in the first run. Optimize for a correct diagnostic that can reveal whether the sampled conversion failure is plausibly an estimator-variance problem.
```

## research/reward_to_gcrl/reward_to_gcrl_soft_successor_prototype_plan.md

```markdown
Source document is 24729 chars, exceeding max_source_doc_chars=12000.

Headings:

# Prototype Plan: Soft Successor-Measure for Reward-to-GCRL
## 1. Core idea
### 1.1 The blog conversion, in one line
## 2. Soft successor-measure version
## 3. Why this is worth testing
## 4. Minimal implementation path
### 4.1 Start with discrete environments
## 5. Code organization
## 6. Prototype v0: tabular terminal-only soft learner
### 6.1 Data structures
### 6.2 Update
### 6.3 First validation
## 7. Prototype v1: tabular vector successor-measure learner
### 7.1 Data structures
### 7.2 Vector update over all goals
# Real-state successor-measure mass.
# Reward-success soft terminal mass.
### 7.3 What this version tests
## 8. Prototype v2: low-capacity factorized successor-measure learner
### 8.1 Simple factorized model
### 8.2 Loss
### 8.3 Goal sampling
### 8.4 Loss weighting
## 9. Small-scale experiments and milestones
### Milestone 0: variance sanity check
### Milestone 1: tabular CliffWalking equivalence
### Milestone 2: sampled augmented vs soft terminal update
### Milestone 3: real-state auxiliary goals in tabular mode
### Milestone 4: low-capacity function approximation
### Milestone 5: offline fitted learning
## 10. Diagnostics to implement from day one
### 10.1 Reward-success target variance
### 10.2 Bellman residual by goal type
### 10.3 Policy/value equivalence check
### 10.4 Auxiliary transfer vs interference
## 11. Concrete experiment grid
### Experiment A: CliffWalking sanity
### Experiment B: sampled vs soft estimator
### Experiment C: auxiliary representation test
### Experiment D: offline mixed dataset
## 12. Minimal pseudocode for neural SSM
        # Max over actions for each sampled goal.
## 13. Reward normalization
## 14. What would count as evidence that the idea is promising?
## 15. Likely failure modes and fixes
## 16. Suggested first implementation order
## 17. One-sentence research framing
## 18. Best first result to aim for

Inspect `research/reward_to_gcrl/reward_to_gcrl_soft_successor_prototype_plan.md` for full text.
```


## Human pivot notes

_None._

## Environment state

```json
{
  "blocker": null,
  "commands_run": [
    "conda env list",
    "nvidia-smi",
    "conda env create -f research/reward_to_gcrl/environment.yaml",
    "kill 1528368",
    "conda create -y -n autoresearcher_reward_to_gcrl -c conda-forge --override-channels python=3.11 pip",
    "conda install -y -n autoresearcher_reward_to_gcrl -c conda-forge --override-channels numpy pandas matplotlib pyyaml jsonschema pytest gymnasium",
    "conda run -n autoresearcher_reward_to_gcrl python --version",
    "conda run -n autoresearcher_reward_to_gcrl python -c \"import sys, numpy, pandas, matplotlib, yaml, jsonschema, pytest, gymnasium; print(sys.executable); print('numpy', numpy.__version__); print('pandas', pandas.__version__); print('matplotlib', matplotlib.__version__); print('pyyaml', yaml.__version__); print('jsonschema', jsonschema.__version__); print('pytest', pytest.__version__); print('gymnasium', gymnasium.__version__)\"",
    "conda env list | rg 'autoresearcher_reward_to_gcrl'",
    "nvidia-smi --query-gpu=name,driver_version,memory.total --format=csv,noheader",
    "mkdir -p research/reward_to_gcrl/setup_logs",
    "conda run -n autoresearcher_reward_to_gcrl python -m jsonschema -i research/reward_to_gcrl/env_state.json schemas/env_setup.schema.json"
  ],
  "conda_env_name": "autoresearcher_reward_to_gcrl",
  "conda_env_path": "/home/eston/anaconda3/envs/autoresearcher_reward_to_gcrl",
  "environment_file": "research/reward_to_gcrl/environment.yaml",
  "gpu_available": true,
  "gpu_checks": [
    "nvidia-smi: NVIDIA GeForce RTX 4090 visible, driver 560.94, CUDA 12.6, 24564 MiB total memory",
    "nvidia-smi --query-gpu=name,driver_version,memory.total --format=csv,noheader: NVIDIA GeForce RTX 4090, 560.94, 24564 MiB"
  ],
  "gpu_requested": true,
  "packages_verified": [
    "python 3.11.15",
    "numpy 2.4.6",
    "pandas 3.0.3",
    "matplotlib 3.10.9",
    "pyyaml 6.0.3",
    "jsonschema 4.26.0",
    "pytest 9.0.3",
    "gymnasium 1.3.0"
  ],
  "project": "reward_to_gcrl",
  "status": "ready",
  "summary": "Project-specific conda environment is ready at /home/eston/anaconda3/envs/autoresearcher_reward_to_gcrl. Python and declared imports were verified, and env_state.json validates against schemas/env_setup.schema.json. GPU is visible via nvidia-smi. No research experiment or training was run."
}
```


## Current state

```json
{
  "best_primary_metric": null,
  "failure_streak": 0,
  "human_review_required": false,
  "iteration": 7,
  "last_decision": "continue",
  "last_failure": null,
  "last_pro_review_iteration": 6,
  "last_pro_review_path": "research/reward_to_gcrl/decisions/0007_pro_decision.json",
  "last_summary_iteration": 6,
  "last_summary_path": "research/reward_to_gcrl/progress/0006_pre_pro_cadence_summary.md",
  "no_progress_rounds": 0,
  "notes": [
    "2026-06-14T09:16:58+00:00: setup_env failed or timed out; see /home/eston/autoresearcher/research/reward_to_gcrl/env_state_stderr.log",
    "2026-06-14T09:27:51+00:00: resumed: Environment setup is ready after rerun; start requested by user.",
    "2026-06-14T09:40:04+00:00: Pro decision saved for checkpoint protected_file_drift (research/reward_to_gcrl/decisions/0001_pro_decision.json)",
    "2026-06-14T09:40:05+00:00: applied Pro decision continue from research/reward_to_gcrl/decisions/0001_pro_decision.json",
    "2026-06-14T09:47:02+00:00: Pro checkpoint blocked (response_parse_failed); packet research/reward_to_gcrl/pro_packets/0002_PRO_REVIEW_PACKET.md",
    "2026-06-14T09:48:30+00:00: cleared stale protected_file_drift after committing/pushing a clean worktree",
    "2026-06-14T10:19:58+00:00: retryable failure 1/3: executor timeout",
    "2026-06-14T10:51:56+00:00: retryable failure 2/3: reviewer verdict needs_human",
    "2026-06-14T10:55:39+00:00: retry limit reached after 3/3 failures: reviewer verdict needs_human",
    "2026-06-14T11:05:19+00:00: Pro checkpoint blocked (response_parse_failed); packet research/reward_to_gcrl/pro_packets/0002_review2_PRO_REVIEW_PACKET.md",
    "2026-06-14T11:11:01+00:00: Pro decision saved for checkpoint review_needs_human (research/reward_to_gcrl/decisions/0002_review3_pro_decision.json)",
    "2026-06-14T11:11:03+00:00: applied Pro decision continue from research/reward_to_gcrl/decisions/0002_review3_pro_decision.json",
    "2026-06-14T11:12:06+00:00: cleared retry failure state after applied Pro continuation",
    "2026-06-14T11:50:30+00:00: Pro checkpoint blocked (pro_backend_failed); packet research/reward_to_gcrl/pro_packets/0004_PRO_REVIEW_PACKET.md",
    "2026-06-14T20:49:23+00:00: resumed: Retry Pro checkpoint after ChatGPT browser response finished",
    "2026-06-14T20:52:44+00:00: Pro decision saved for checkpoint local_needs_human (research/reward_to_gcrl/decisions/0004_review2_pro_decision.json)",
    "2026-06-14T20:52:46+00:00: applied Pro decision pivot from research/reward_to_gcrl/decisions/0004_review2_pro_decision.json",
    "2026-06-14T21:06:17+00:00: Pro decision saved for checkpoint protected_file_drift (research/reward_to_gcrl/decisions/0004_review3_pro_decision.json)",
    "2026-06-14T21:06:18+00:00: applied Pro decision pivot from research/reward_to_gcrl/decisions/0004_review3_pro_decision.json",
    "2026-06-14T21:12:57+00:00: Pro decision saved for checkpoint review_needs_human (research/reward_to_gcrl/decisions/0004_review4_pro_decision.json)",
    "2026-06-14T21:12:58+00:00: applied Pro decision continue from research/reward_to_gcrl/decisions/0004_review4_pro_decision.json",
    "2026-06-14T21:17:18+00:00: Pro decision saved for checkpoint review_fail (research/reward_to_gcrl/decisions/0004_review5_pro_decision.json)",
    "2026-06-14T21:17:20+00:00: applied Pro decision continue from research/reward_to_gcrl/decisions/0004_review5_pro_decision.json",
    "2026-06-14T21:18:53+00:00: cleared protected_file_drift after audit research/reward_to_gcrl/artifacts/0004/protected_file_drift_audit.json; status=harmless accepted_evidence",
    "2026-06-14T21:52:09+00:00: Pro decision saved for checkpoint cadence (research/reward_to_gcrl/decisions/0007_pro_decision.json)",
    "2026-06-14T21:52:11+00:00: applied Pro decision continue from research/reward_to_gcrl/decisions/0007_pro_decision.json"
  ],
  "pending_checkpoint": null,
  "pending_local_decision_path": null,
  "primary_metric": null,
  "pro_review_count": 7,
  "protected_file_drift": false,
  "status": "active",
  "weak_pass_streak": 0
}
```


## Latest result summary

```json
{
  "_source": "/home/eston/autoresearcher/research/reward_to_gcrl/results/0007_result.json",
  "artifacts": {
    "_type": "list",
    "first_items": [
      "research/reward_to_gcrl/artifacts/0007/run_riverswim_coverage_dose_response.py",
      "research/reward_to_gcrl/artifacts/0007/local_compatibility_check.json",
      "research/reward_to_gcrl/artifacts/0007/environment_audit.json"
    ],
    "length": 10
  },
  "baseline_metrics": {
    "baseline_name": "sampled_augmented_g_plus_learning",
    "coverage_starved_count": 30,
    "mean_final_bellman_residual": 0.006313229252871876,
    "mean_final_value_error": 0.1331149724439577,
    "mean_g_plus_events_per_10000": 5.397222222222222,
    "mean_greedy_raw_return": 30.848583333333334
  },
  "claim_tested": "On 6-state RiverSwim with non-oracle behavior streams, sampled augmented g_plus updates remain unbiased but higher variance than deterministic soft updates, with coverage determining whether learning advantages are interpretable.",
  "experiment_id": "0007",
  "interpretation": "Coverage dose response completed: sampled targets match deterministic soft marginal targets within tolerance and have higher terminal-sampling variance in every run. Soft learning advantages are supported on adequate-coverage runs only; starved runs are reported as coverage-limited diagnostics rather than learning-superiority evidence.",
  "known_failures": [],
  "metrics": {
    "config": {
      "alpha": 0.05,
      "behaviors": {
        "_type": "object",
        "key_count": 4,
        "keys": [
          "medium_right_bias",
          "mild_right_bias",
          "strong_right_bias",
          "uniform_random"
        ]
      },
      "bellman_residual_threshold": 0.01,
      "checkpoints": {
        "_type": "list",
        "length": 7
      },
      "coverage_thresholds": {
        "_type": "object",
        "key_count": 4,
        "keys": [
          "adequate_right_reward_events_per_10000_gte",
          "borderline_right_reward_events_per_10000_lt",
          "min_visited_state_action_pairs",
          "starved_right_reward_events_per_10000_lt"
        ]
      },
      "gammas": {
        "_type": "list",
        "length": 3
      },
      "mc_sigma_tolerance": 6.0,
      "reward_normalization": "identity(raw_reward), rewards already in [0,1]",
      "sampled_continue_target": "max_a M(s_next,a), no extra gamma factor",
      "seeds": {
        "_type": "list",
        "length": 10
      },
      "transition_budget": 150000,
      "value_error_indistinguishable_z": 1.96
    },
    "environment_audit": {
      "complete": true,
      "missing_fields": {
        "_type": "list",
        "length": 0
      },
      "reward_normalization": {
        "_type": "object",
        "key_count": 7,
        "keys": [
          "affine_offset",
          "affine_scale",
          "all_other_rewards",
          "left_end_small_reward",
          "normalized_reward",
          "raw_rewards_in_[0,1]",
          "right_end_sparse_reward"
        ]
      },
      "transition_table_hash": "2e481565b49954b048469471863e55d38268fb628e07d8839b77f881ae07a2ed",
      "transition_table_shape": {
        "_type": "list",
        "length": 3
      }
    },
    "exact_dp": {
      "rows": {
        "_type": "list",
        "length": 3
      },
      "scaled_soft_matches_q_norm": true
    },
    "pass_flags": {
      "adequate_coverage_soft_advantage": true,
      "at_least_four_non_oracle_behaviors": true,
      "coverage_bin_summaries_and_regression_reported": true,
      "cpu_tabular_only": true,
      "environment_audit_complete": true,
      "exact_scaled_soft_matches_q_norm": true,
      "gamma_seed_behavior_grid_complete": true,
      "same_transition_hash_as_0005_0006": true,
      "sampled_variance_exceeds_soft_all_runs": true,
      "starved_borderline_adequate_bins_present": true,
      "starved_runs_caveated": true,
      "target_mean_match_all_runs": true
    },
    "recommendation": "move_next_to_tabular_auxiliary_real_state_goals",
    "sampled_vs_soft": {
      "aggregate": {
        "_type": "object",
        "key_count": 39,
        "keys": [
          "adequate_coverage_count",
          "adequately_covered",
          "bellman_value_direction_disagreement",
          "borderline_coverage",
          "borderline_coverage_count",
          "by_behavior",
          "by_coverage_bin",
          "coverage_bin_counts",
          "coverage_bin_thresholds",
          "coverage_bins_present",
          "coverage_performance_regression",
          "coverage_starved",
          "coverage_starved_count",
          "mean_final_sampled_bellman_residual",
          "mean_final_sampled_value_error",
          "mean_final_soft_bellman_residual",
          "mean_final_soft_value_error",
          "mean_g_plus_events_per_10000",
          "mean_right_end_occupancy_rate",
          "mean_right_reward_events_per_10000"
        ]
      }
    }
  },
  "next_questions": [
    "Do tabular auxiliary real-state goals preserve the estimator advantages under adequate RiverSwim coverage?",
    "Do coverage-starved settings need explicit data-collection fixes before making learning-superiority claims?"
  ],
  "status": "completed"
}
```


## Latest summary

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


## Latest review summary

```json
{
  "allows_auto_continue": true,
  "escalation_reason": null,
  "evidence_checked": {
    "_type": "list",
    "first_items": [
      "research/reward_to_gcrl/results/0007_result.json",
      "research/reward_to_gcrl/results/0007_summary.md",
      "research/reward_to_gcrl/artifacts/0007/run_riverswim_coverage_dose_response.py"
    ],
    "length": 11
  },
  "evidence_quality": "strong",
  "experiment_id": "0007",
  "failure_criteria_triggered": false,
  "reasons": {
    "_type": "list",
    "first_items": [
      "Required 0007 result JSON, summary markdown, and artifact directory are present.",
      "Result JSON validates against schemas/result.schema.json, and declared artifact paths validate successfully.",
      "The artifact set includes the coverage dose-response script, fresh environment audit, exact DP references, per-seed metrics, learning curves, raw metrics, and progress log."
    ],
    "length": 11
  },
  "required_fixes": [],
  "risk_flags": [
    "The coverage-performance regression includes visited_state_action_pairs, but that feature is constant at 12 in the observed runs, so the regression is effectively driven by right-reward event variation.",
    "Soft value error is worse than sampled in 4 of 35 adequate-coverage individual runs, although the adequate-bin mean clearly favors soft and satisfies the stated criterion.",
    "Right-biased behavior policies are fixed and non-oracle, but they are hand-designed to favor the known RiverSwim rightward direction; broader non-oracle data-collection policies remain untested.",
    "Starved runs show lower soft Bellman residual but worse soft value error, so future claims should preserve the coverage caveat.",
    "Current git status shows an untracked reviewer packet, but no protected path is currently modified."
  ],
  "should_escalate_to_pro": false,
  "success_criteria_satisfied": true,
  "verdict": "pass"
}
```


## Metric ledger

```json
{
  "iterations": [
    {
      "allows_auto_continue": true,
      "claim_tested": "In a one-state normalized-reward augmented transition model, sampled Bernoulli g_plus terminal targets and deterministic soft expected-mass targets have the same mean, while sampled targets retain Bernoulli variance and increasingly rare g_plus events as gamma approaches 1; in a tiny finite MDP, F_gplus_star / (1 - gamma) matches normalized Q_star.",
      "decision": "continue",
      "important_metrics": {},
      "iteration": "0001",
      "negative_signals": [
        "Executor recorded and described a 6-SE Monte Carlo mean tolerance even though the plan specified 3 standard errors; raw metrics still pass the stricter 3-SE check.",
        "Variance agreement is reported through sampled and analytic raw variances but lacks an explicit variance-specific tolerance or pass flag in the result JSON.",
        "The script hard-codes commands_run rather than deriving them from argv; it matches this run's samples and seed but could misreport future reruns."
      ],
      "positive_signals": [
        "The soft terminal-mass target removes the sampled terminal-event variance source in this isolated one-step diagnostic.",
        "The tiny finite-MDP check confirms the soft g_plus Bellman fixed point matches normalized Q-learning after division by (1 - gamma).",
        "For gamma=0.995 and r_bar=0.01, the analytic expected g_plus rate is only 0.5 per 10000 transitions, so sampled conversion can make dense reward supervision extremely sparse.",
        "The largest analytic single-target coefficient of variation is 141.418, showing relative noise grows sharply for rare terminal mass.",
        "The deterministic soft target exactly equals the analytic expected terminal mass and has zero variance. The sampled Bernoulli estimator matched that mean within the predeclared Monte Carlo tolerance at all 16 sweep points, but retained nonzero target variance "
      ],
      "review_verdict": "weak_pass",
      "status": "completed"
    },
    {
      "allows_auto_continue": true,
      "claim_tested": "For a fully audited local deterministic 4x12 CliffWalking transition table, the terminal-only soft successor g_plus Bellman fixed point and paired tabular learner match normalized-reward Q-learning after division by (1 - gamma).",
      "decision": "continue",
      "important_metrics": {
        "metrics.config.exact_scaling_tolerance": 1e-06,
        "metrics.exact_dp.max_abs_error_scaled_f_vs_q": 9.711982329463353e-10,
        "metrics.exact_dp.max_policy_disagreement_rate": 0.0,
        "metrics.exact_dp.rows.0.f_final_delta": 9.581224702515101e-14,
        "metrics.exact_dp.rows.0.f_value_iteration_steps": 527,
        "metrics.exact_dp.rows.0.gamma": 0.95,
        "metrics.exact_dp.rows.0.max_abs_error_scaled_f_vs_q": 3.4564351381050074e-11,
        "metrics.exact_dp.rows.0.passes_exact_scaling_tolerance": true,
        "metrics.exact_dp.rows.0.policy_comparison.comparable_non_tie_state_count": 0,
        "metrics.exact_dp.rows.0.policy_comparison.disagreement_count": 0,
        "metrics.exact_dp.rows.0.policy_comparison.disagreement_rate": 0.0,
        "metrics.exact_dp.rows.0.policy_comparison.insufficient_state_count": 0
      },
      "iteration": "0002",
      "negative_signals": [
        "The declared normalization maps ordinary step and goal rewards to 1 and cliff falls to 0, causing the learned/evaluated greedy policies to never reach the goal; this is acceptable for the equivalence gate but makes raw C...",
        "Policy-disagreement evidence is weak because exact DP has 37 tie states and 0 comparable non-tie states; paired learning also has many tie states and few comparable states in several seeds.",
        "The paired learned-value comparison is nearly algebraic because both learners use identical transitions, initialization, alpha, and targets that differ only by the (1-gamma) scale.",
        "Learned Bellman residuals are large in some paired runs, up to about 100, so this does not demonstrate convergence to the exact DP solution."
      ],
      "positive_signals": [
        "The previous Gymnasium CliffWalking-v0 blocker is avoided by a local deterministic transition table with a saved SHA-256 hash.",
        "The exact soft g_plus fixed point is numerically identical to normalized Q_star after division by (1 - gamma) for both tested gamma values.",
        "Paired online learning preserves the scaling relation under identical experience, so final greedy policies agree up to tie handling.",
        "The declared normalization maps ordinary step and goal rewards to 1 and cliff falls to 0, so raw goal-reaching performance is only a diagnostic and can be poor even when equivalence passes.",
        "The local deterministic CliffWalking table resolves the previous Gymnasium compatibility blocker. Exact DP passes the scaled soft-successor equivalence with max error 9.71198e-10. Paired tabular learners preserve the same values after scaling and have zero tie"
      ],
      "review_verdict": "weak_pass",
      "status": "completed"
    },
    {
      "allows_auto_continue": true,
      "claim_tested": "On the audited local CliffWalking transition table, sampled augmented g_plus learning is an unbiased but higher-variance estimator of the terminal-only soft successor target and reduces error more slowly under the same original transition budget.",
      "decision": "continue",
      "important_metrics": {
        "metrics.exact_soft_dp.rows.0.bellman_residual_max_decision": 9.103828801926284e-14,
        "metrics.exact_soft_dp.rows.0.final_delta": 9.581224702515101e-14,
        "metrics.exact_soft_dp.rows.0.gamma": 0.95,
        "metrics.exact_soft_dp.rows.0.iterations": 527,
        "metrics.exact_soft_dp.rows.0.max_value": 0.999999999998179,
        "metrics.exact_soft_dp.rows.0.min_value": 0.0,
        "metrics.exact_soft_dp.rows.1.bellman_residual_max_decision": 9.814371537686384e-14,
        "metrics.exact_soft_dp.rows.1.final_delta": 9.914291609902648e-14,
        "metrics.exact_soft_dp.rows.1.gamma": 0.99,
        "metrics.exact_soft_dp.rows.1.iterations": 2522,
        "metrics.exact_soft_dp.rows.1.max_value": 0.9999999999901835,
        "metrics.exact_soft_dp.rows.1.min_value": 0.0
      },
      "iteration": "0003",
      "negative_signals": [
        "The target-mean pass compares sampled targets to the sampled learner's conditional expected target, not to the deterministic soft learner's recorded target; sampled-vs-soft-deterministic target means exceed the recorded...",
        "The summary claims lower/faster value-error dominance, but mean final soft value error is slightly worse overall than sampled value error, and soft value-error dominance is only 17 of 30 runs.",
        "At gamma 0.995, soft value-error dominance is only 4 of 10 seeds, so the value-error evidence does not strengthen as gamma approaches 1.",
        "The stronger dominance evidence is Bellman residual, where soft is lower in 26 of 30 runs; this should be preferred over the weaker value-error wording."
      ],
      "positive_signals": [
        "The local transition table hash matches the audited 0002 table.",
        "The sampled update uses p(g_plus)=(1-gamma)r_bar, p(g_minus)=(1-gamma)(1-r_bar), and p(continue)=gamma.",
        "Continued sampled targets use max_a M(s_next,a) directly, without an extra gamma factor.",
        "The raw CliffWalking policy returns remain diagnostic because the normalized reward maps ordinary steps and goal transitions to the same reward.",
        "The sampled augmented target is unbiased within the predeclared Monte Carlo tolerance in all gamma/seed runs, but its terminal sampling variance is strictly positive while the deterministic soft target has zero terminal sampling variance. Under the matched tra"
      ],
      "review_verdict": "weak_pass",
      "status": "completed"
    },
    {
      "allows_auto_continue": true,
      "claim_tested": "In a nondegenerate tiny chain with identity reward normalization, sampled augmented g_plus updates are unbiased but higher variance, while deterministic soft terminal marginalization improves Bellman residual and preserves policy quality.",
      "decision": "needs_human",
      "important_metrics": {
        "metrics.environment_audit.reward_audit.non_success_reward": 0.0,
        "metrics.environment_audit.reward_audit.success_reward": 1.0,
        "metrics.exact_dp.non_tie_policy_informative": true,
        "metrics.exact_dp.raw_normalized_policy_preserved": true,
        "metrics.exact_dp.rows.0.gamma": 0.95,
        "metrics.exact_dp.rows.0.max_abs_scaled_soft_minus_normalized_q": 1.1102230246251565e-16,
        "metrics.exact_dp.rows.0.non_tie_decision_state_fraction": 1.0,
        "metrics.exact_dp.rows.0.normalized_final_delta": 0.0,
        "metrics.exact_dp.rows.0.normalized_q.0.0": 0.8573749999999999,
        "metrics.exact_dp.rows.0.normalized_q.0.1": 0.9025,
        "metrics.exact_dp.rows.0.normalized_q.1.0": 0.8573749999999999,
        "metrics.exact_dp.rows.0.normalized_q.1.1": 0.95
      },
      "iteration": "0004",
      "negative_signals": [
        "The latest plan text inconsistently references 0005 audit/result paths, while required outputs and actual evidence use 0004 paths.",
        "drift_status and evidence_integrity_verdict are under metrics rather than top-level result fields.",
        "The accepted learning-improvement evidence is still from a tiny 5-state chain with controlled matched streams; broader environments remain untested.",
        "Current git status shows a modified reviewer packet, but no protected path is currently modified."
      ],
      "positive_signals": [
        "Identity reward normalization avoids the CliffWalking objective mismatch.",
        "The hand-built chain has three decision states, all with non-tie exact greedy actions.",
        "The sampled target is compared to a deterministic soft target computed from the same sampled learner table before each update.",
        "The conservative verdict is learning-improvement.",
        "The repaired chain preserves the raw policy under identity normalization. Sampled targets match the deterministic soft marginal target within the predeclared Monte Carlo tolerance, have positive sampling variance, and the deterministic soft learner achieves lo"
      ],
      "review_verdict": "weak_pass",
      "status": "completed"
    },
    {
      "allows_auto_continue": true,
      "claim_tested": "On a small stochastic RiverSwim chain with normalized rewards in [0,1], sampled augmented g_plus updates are unbiased but higher variance than deterministic soft terminal updates, and soft learning improves Bellman/value error under matched transition streams.",
      "decision": "continue",
      "important_metrics": {
        "metrics.exact_dp.rows.0.exact_greedy_policy.0": 1,
        "metrics.exact_dp.rows.0.exact_greedy_policy.1": 1,
        "metrics.exact_dp.rows.0.exact_greedy_policy.2": 1,
        "metrics.exact_dp.rows.0.exact_greedy_policy.3": 1,
        "metrics.exact_dp.rows.0.exact_greedy_policy.4": 1,
        "metrics.exact_dp.rows.0.exact_greedy_policy.5": 1,
        "metrics.exact_dp.rows.0.f_gplus_star.0.0": 0.2126535293972451,
        "metrics.exact_dp.rows.0.f_gplus_star.0.1": 0.2233195046287773,
        "metrics.exact_dp.rows.0.f_gplus_star.1.0": 0.2121535293972451,
        "metrics.exact_dp.rows.0.f_gplus_star.1.1": 0.25270364997491473,
        "metrics.exact_dp.rows.0.f_gplus_star.2.0": 0.24006846747607563,
        "metrics.exact_dp.rows.0.f_gplus_star.2.1": 0.29490193389305197
      },
      "iteration": "0005",
      "negative_signals": [
        "The behavior policy is epsilon-greedy with respect to the exact normalized-Q greedy action, so the result is a controlled matched-stream propagation test rather than an online exploration test.",
        "Right-end coverage is strong under the oracle-guided behavior stream; conclusions about sparse-reward exploration failures should be tested separately with a non-oracle exploratory behavior policy.",
        "Greedy-policy return is not uniformly better for the soft learner per seed: soft has higher mean return overall, but is strictly higher than sampled in only 14 of 30 runs and has a few low-return learned policies.",
        "The experiment remains small-scale at 6 states; larger RiverSwim chains or auxiliary-goal settings remain untested."
      ],
      "positive_signals": [
        "The RiverSwim transition table is stochastic, continuing, and has rewards already normalized to [0,1].",
        "Sampled continued targets use max_a M(s_next,a) directly, without an extra gamma factor.",
        "Right-end occupancy and reward-event counts are saved so sparse reward coverage is auditable.",
        "The primary pass flag combines target unbiasedness, positive sampled variance, interpretable coverage, and soft residual dominance in most runs.",
        "The RiverSwim diagnostic supports the hypothesis: sampled targets match the deterministic soft marginal target within Monte Carlo tolerance while retaining higher terminal-sampling variance, and the deterministic soft learner has lower or faster Bellman residu"
      ],
      "review_verdict": "pass",
      "status": "completed"
    },
    {
      "allows_auto_continue": true,
      "claim_tested": "On 6-state RiverSwim with non-oracle behavior streams, sampled augmented g_plus updates remain unbiased but higher variance than deterministic soft updates, with coverage determining whether learning advantages are interpretable.",
      "decision": "continue",
      "important_metrics": {
        "metrics.config.behaviors.right_biased_random.uses_exact_q": false,
        "metrics.config.behaviors.uniform_random.uses_exact_q": false,
        "metrics.exact_dp.rows.0.exact_greedy_policy.0": 1,
        "metrics.exact_dp.rows.0.exact_greedy_policy.1": 1,
        "metrics.exact_dp.rows.0.exact_greedy_policy.2": 1,
        "metrics.exact_dp.rows.0.exact_greedy_policy.3": 1,
        "metrics.exact_dp.rows.0.exact_greedy_policy.4": 1,
        "metrics.exact_dp.rows.0.exact_greedy_policy.5": 1,
        "metrics.exact_dp.rows.0.f_gplus_star.0.0": 0.2126535293972451,
        "metrics.exact_dp.rows.0.f_gplus_star.0.1": 0.2233195046287773,
        "metrics.exact_dp.rows.0.f_gplus_star.1.0": 0.2121535293972451,
        "metrics.exact_dp.rows.0.f_gplus_star.1.1": 0.25270364997491473
      },
      "iteration": "0006",
      "negative_signals": [
        "Data generation used fixed action probabilities only; exact DP was not consulted by behavior policies.",
        "Half of the runs are coverage-starved under the predeclared threshold, so learning-performance conclusions should be restricted to the adequate-coverage subset or explicitly labeled as coverage-limited.",
        "In coverage-starved uniform-random runs, soft has lower Bellman residual but worse mean value error than sampled in most runs, so value-error superiority is not uniform under poor coverage.",
        "The behavior policies are simple state-independent random policies; additional non-oracle exploration policies may be needed before broader claims.",
        "Current git status shows an untracked reviewer packet, but no protected path is currently modified."
      ],
      "positive_signals": [
        "Coverage thresholds are predeclared using right reward events per 10000 transitions and visited state-action pairs.",
        "Estimator claims are separated from learning claims on coverage-starved runs.",
        "The same 6-state RiverSwim transition semantics as 0005 were recreated and freshly audited.",
        "With non-oracle behavior streams, sampled targets remain unbiased within tolerance and higher variance. Coverage is explicitly split by the predeclared right-reward threshold; on adequately covered runs, soft retains the residual/value advantage."
      ],
      "review_verdict": "pass",
      "status": "completed"
    },
    {
      "allows_auto_continue": true,
      "claim_tested": "On 6-state RiverSwim with non-oracle behavior streams, sampled augmented g_plus updates remain unbiased but higher variance than deterministic soft updates, with coverage determining whether learning advantages are interpretable.",
      "decision": null,
      "important_metrics": {
        "metrics.config.behaviors.medium_right_bias.uses_exact_q": false,
        "metrics.config.behaviors.mild_right_bias.uses_exact_q": false,
        "metrics.config.behaviors.strong_right_bias.uses_exact_q": false,
        "metrics.config.behaviors.uniform_random.uses_exact_q": false,
        "metrics.exact_dp.rows.0.exact_greedy_policy.0": 1,
        "metrics.exact_dp.rows.0.exact_greedy_policy.1": 1,
        "metrics.exact_dp.rows.0.exact_greedy_policy.2": 1,
        "metrics.exact_dp.rows.0.exact_greedy_policy.3": 1,
        "metrics.exact_dp.rows.0.exact_greedy_policy.4": 1,
        "metrics.exact_dp.rows.0.exact_greedy_policy.5": 1,
        "metrics.exact_dp.rows.0.f_gplus_star.0.0": 0.2126535293972451,
        "metrics.exact_dp.rows.0.f_gplus_star.0.1": 0.2233195046287773
      },
      "iteration": "0007",
      "negative_signals": [
        "Data generation used fixed action probabilities only; exact DP was not consulted by behavior policies.",
        "The coverage-performance regression includes visited_state_action_pairs, but that feature is constant at 12 in the observed runs, so the regression is effectively driven by right-reward event variation.",
        "Soft value error is worse than sampled in 4 of 35 adequate-coverage individual runs, although the adequate-bin mean clearly favors soft and satisfies the stated criterion.",
        "Right-biased behavior policies are fixed and non-oracle, but they are hand-designed to favor the known RiverSwim rightward direction; broader non-oracle data-collection policies remain untested.",
        "Starved runs show lower soft Bellman residual but worse soft value error, so future claims should preserve the coverage caveat."
      ],
      "positive_signals": [
        "Coverage bins are predeclared using right reward events per 10000 transitions and visited state-action pairs.",
        "Estimator claims are separated from learning claims on coverage-starved runs.",
        "The same 6-state RiverSwim transition hash as 0005 and 0006 was recreated and verified.",
        "Coverage dose response completed: sampled targets match deterministic soft marginal targets within tolerance and have higher terminal-sampling variance in every run. Soft learning advantages are supported on adequate-coverage runs only; starved runs are report"
      ],
      "review_verdict": "pass",
      "status": "completed"
    }
  ],
  "project": "reward_to_gcrl"
}
```


## Last decision summaries

## 0005_decision.json

```json
{
  "confidence": 0.79,
  "decision": "continue",
  "evidence": [
    "research/reward_to_gcrl/results/0004_result.json is present, schema-valid, and reports status completed with exact commands and declared artifacts.",
    "research/reward_to_gcrl/reviews/0004_review.json reports allows_auto_continue=true, success_criteria_satisfied=true, and no triggered failure criteria.",
    "0004 records drift_status=harmless and evidence_integrity_verdict=accepted_evidence after a protected-file drift audit, with post-audit schema and artifact validation marked passed.",
    "0004 uses identity reward normalization in a nondegenerate 5-state chain, avoiding the CliffWalking objective mismatch from 0002/0003.",
    "0004 reports sampled target means matching deterministic soft marginal targets, sampled variance exceeding soft variance in all runs, and lower mean final soft Bellman/value error with soft success rate 1.0 versus sampled success rate 0.0.",
    "The reviewer still flags that 0004 is only a tiny controlled matched-stream chain, so broader environments remain untested.",
    "The charter's initial scope includes small RiverSwim chains for long-horizon reward propagation before larger grids or neural training."
  ],
  "next_experiment": {
    "estimated_runtime_minutes": 25,
    "experiment_id": "0005",
    "hypothesis": "On a small RiverSwim chain with rewards already normalized to [0,1], sampled augmented g_plus updates are unbiased but higher variance than deterministic soft terminal updates; under matched transition streams, the soft learner should show lower TD target variance, fewer failures from rare g_plus events, and lower Bellman/value error to exact DP at the same data budget, especially as gamma approaches 1.",
    "objective": "Run a CPU-only tabular sampled-vs-soft diagnostic on a small stochastic RiverSwim chain to test long-horizon reward propagation under sparse right-end rewards.",
    "required_outputs": [
      "research/reward_to_gcrl/results/0005_result.json",
      "research/reward_to_gcrl/results/0005_summary.md",
      "research/reward_to_gcrl/artifacts/0005/ with script, raw per-seed metrics, aggregate metrics, environment audit, learning curves, and DP references"
    ]
  },
  "progress_score": 5,
  "rationale": "The 0004 evidence-integrity blocker has been resolved and the repaired nondegenerate chain result is accepted as weak but useful evidence. It supports the estimator-variance and learning-improvement story in a tiny controlled task, but the result is still too narrow to justify auxiliary goals or function approximation. The next small, high-information step is to test the same sampled-vs-soft claim on a small stochastic RiverSwim chain, which is explicitly in the charter's initial scope and probes long-horizon reward propagation without expensive training.",
  "risks": [
    "RiverSwim learning can confound estimator variance with exploration difficulty; use matched transition streams plus exact DP references to keep the test interpretable.",
    "If the behavior stream rarely reaches the rewarding right end, both learners may fail for coverage reasons rather than estimator reasons; coverage and reward-event counts must be reported.",
    "A positive RiverSwim result would still be tabular evidence only, not evidence for auxiliary goals or neural representation learning.",
    "The sampled augmented update must again avoid an extra gamma factor on continued sampled transitions and must mask sampled absorbing events correctly."
  ]
}
```

## 0006_decision.json

```json
{
  "confidence": 0.84,
  "decision": "continue",
  "evidence": [
    "0005_result.json reports status completed with exact commands and declared artifacts.",
    "0005_review.json reports verdict pass, evidence_quality strong, allows_auto_continue true, and no triggered failure criteria.",
    "0005 used CPU-only tabular code on a 6-state stochastic continuing RiverSwim chain with rewards normalized to [0,1].",
    "Across 30 runs, sampled target means matched deterministic soft marginal targets, sampled variance exceeded soft variance, and soft residual dominance was reported in all runs.",
    "The key reviewer caveat is that behavior was epsilon-greedy with respect to exact normalized-Q greedy actions, so 0005 is a controlled propagation test rather than a non-oracle exploration test."
  ],
  "next_experiment": {
    "estimated_runtime_minutes": 25,
    "experiment_id": "0006",
    "hypothesis": "With matched original transition streams generated by non-oracle exploration, sampled augmented g_plus updates remain unbiased but higher variance than deterministic soft updates. When coverage is adequate, soft should retain lower Bellman residual or value error; when coverage is poor, coverage should be identified as the limiting factor.",
    "objective": "Repeat the 6-state RiverSwim sampled-vs-soft diagnostic using non-oracle exploratory behavior streams.",
    "required_outputs": [
      "research/reward_to_gcrl/results/0006_result.json",
      "research/reward_to_gcrl/results/0006_summary.md",
      "research/reward_to_gcrl/artifacts/0006/ with script, audit, DP references, raw metrics, aggregate metrics, and learning curves"
    ]
  },
  "progress_score": 6,
  "rationale": "0005 is a strong reviewed pass for the sampled-vs-soft claim in small stochastic RiverSwim, but it used exact-Q-guided behavior. The next small decisive test should hold the RiverSwim setup fixed and remove that oracle coverage source before moving to auxiliary goals or function approximation.",
  "risks": [
    "Non-oracle RiverSwim may have poor right-end coverage; coverage-starved failures should not be overinterpreted as estimator failure.",
    "Independent learner behavior would confound exploration with estimator variance, so use matched logged streams generated without exact-Q guidance.",
    "Do not move to neural approximation or auxiliary goals until this oracle-behavior caveat is bounded."
  ]
}
```

## 0007_pro_decision.json

```json
{
  "confidence": 0.86,
  "decision": "continue",
  "evidence": [
    "The latest summary reports protected_file_drift is false and there is no current blocker.",
    "0001 validated the estimator premise: sampled and soft terminal targets matched means while soft terminal variance was zero or negligible.",
    "0002 confirmed tabular scaling equivalence in audited CliffWalking below the 1e-6 threshold.",
    "0004 accepted the repaired nondegenerate 5-state chain result: soft had lower Bellman residual and value error and achieved success where sampled failed.",
    "0005 passed on 6-state RiverSwim with exact-Q-guided behavior: sampled target means matched deterministic soft marginal targets in all 30 runs, sampled variance exceeded soft variance in all 30 runs, and soft residual dominance held in all runs.",
    "0006 passed with non-oracle behavior streams: sampled targets remained unbiased within tolerance and higher variance without exact-Q-guided behavior.",
    "The main 0006 caveat is coverage: half the runs were coverage-starved, and under poor coverage soft could have lower Bellman residual but worse value error than sampled.",
    "No auxiliary-goal, neural, FourRooms, larger RiverSwim, or offline fitted-learning evidence exists yet."
  ],
  "next_experiment": {
    "estimated_runtime_minutes": 25,
    "experiment_id": "0007",
    "hypothesis": "The deterministic soft update should consistently reduce terminal-sampling variance in all coverage regimes, but learning-performance advantages should appear mainly when right-reward and state-action coverage are adequate. In coverage-starved regimes, soft may lower Bellman residual without reliably lowering value error, so coverage should be treated as a prerequisite for learning-superiority claims.",
    "objective": "Run a CPU-only tabular RiverSwim coverage dose-response experiment that uses several non-oracle behavior policies to create starved, borderline, and adequate coverage regimes, then quantify exactly when deterministic soft terminal marginalization improves Bellman residual, value error, and policy quality over sampled augmented updates.",
    "required_outputs": [
      "research/reward_to_gcrl/results/0007_result.json",
      "research/reward_to_gcrl/results/0007_summary.md",
      "research/reward_to_gcrl/artifacts/0007/"
    ]
  },
  "progress_score": null,
  "rationale": "Continue with one more small CPU-tabular RiverSwim experiment before moving to auxiliary goals. The project is now making real progress toward the overall research goal: drift is cleared, 0004 supplied a nondegenerate small-chain result, 0005 gave a strong controlled RiverSwim propagation result, and 0006 removed exact-Q-guided behavior while preserving the estimator story. The remaining blocker is not whether the soft estimator reduces terminal-sampling variance; that is well supported. The open question is whether the learning advantage is robust once coverage is non-oracle but not starved. A coverage-controlled RiverSwim dose-response test is the cheapest decisive next step.",
  "risks": [
    "A further RiverSwim run could become redundant if it only repeats the variance result without clarifying coverage dependence.",
    "Coverage-controlled behavior policies may still be too artificial to support online-control claims.",
    "If adequate coverage is achieved by hand-designed behavior, the result remains matched-stream estimator evidence, not full exploration evidence.",
    "Moving to auxiliary goals before bounding the coverage caveat could make later representation-learning results hard to interpret.",
    "All current evidence is still tiny tabular evidence, so even a positive 0007 should not be overclaimed as a general GCRL solution."
  ]
}
```


## Full evidence paths

- `research/reward_to_gcrl/results/0007_result.json`
- `research/reward_to_gcrl/results/0007_summary.md`
- `research/reward_to_gcrl/reviews/0007_review.json`

Use these paths if compact summaries are insufficient.


## Stop, pivot, continue rules

- For iteration 0, a missing latest result is expected and is not by itself a reason to stop.
- After iteration 0, stop or choose needs_human on missing or invalid result files.
- Stop on repeated invalid, negative, or low-value results.
- Pivot only when evidence weakens the original idea but reveals a nearby testable idea.
- Continue or pivot only for one cheap, high-information experiment.
- Choose needs_human for ambiguity, expensive work, missing artifacts, or risky pivots.


## Next experiment id

Use `0008` as the exact `next_experiment.experiment_id` if you choose continue or pivot.
