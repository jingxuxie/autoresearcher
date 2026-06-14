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
  "iteration": 1,
  "last_decision": "continue",
  "last_failure": null,
  "last_pro_review_iteration": 0,
  "last_pro_review_path": "research/reward_to_gcrl/decisions/0001_pro_decision.json",
  "last_summary_iteration": 1,
  "last_summary_path": "research/reward_to_gcrl/progress/0001_pre_pro_protected_file_drift_summary.md",
  "no_progress_rounds": 0,
  "notes": [
    "2026-06-14T09:16:58+00:00: setup_env failed or timed out; see /home/eston/autoresearcher/research/reward_to_gcrl/env_state_stderr.log",
    "2026-06-14T09:27:51+00:00: resumed: Environment setup is ready after rerun; start requested by user.",
    "2026-06-14T09:40:04+00:00: Pro decision saved for checkpoint protected_file_drift (research/reward_to_gcrl/decisions/0001_pro_decision.json)",
    "2026-06-14T09:40:05+00:00: applied Pro decision continue from research/reward_to_gcrl/decisions/0001_pro_decision.json",
    "2026-06-14T09:47:02+00:00: Pro checkpoint blocked (response_parse_failed); packet research/reward_to_gcrl/pro_packets/0002_PRO_REVIEW_PACKET.md",
    "2026-06-14T09:48:30+00:00: cleared stale protected_file_drift after committing/pushing a clean worktree"
  ],
  "pending_checkpoint": null,
  "pending_local_decision_path": null,
  "primary_metric": null,
  "pro_review_count": 1,
  "protected_file_drift": false,
  "status": "active",
  "weak_pass_streak": 1
}
```


## Latest result summary

```json
{
  "_source": "/home/eston/autoresearcher/research/reward_to_gcrl/results/0001_result.json",
  "artifacts": [
    "research/reward_to_gcrl/artifacts/0001/run_terminal_variance_diagnostic.py",
    "research/reward_to_gcrl/artifacts/0001/raw_metrics.json",
    "research/reward_to_gcrl/artifacts/0001/metrics.csv",
    "research/reward_to_gcrl/artifacts/0001/metadata.json",
    "research/reward_to_gcrl/artifacts/0001/finite_mdp_equivalence.json"
  ],
  "baseline_metrics": {
    "baseline_name": "sampled_bernoulli_terminal_target",
    "baseline_target_definition": "Bernoulli((1 - gamma) * r_bar) indicator for g_plus.",
    "max_sampled_g_plus_count_per_10000": 1005.02,
    "max_sampled_target_variance": 0.090401347996,
    "min_sampled_g_plus_count_per_10000": 0.48000000000000004,
    "per_setting_sampled_metrics": {
      "_type": "list",
      "first_items": [
        {
          "_type": "object",
          "key_count": 8,
          "keys": [
            "analytic_expected_mean",
            "analytic_expected_variance",
            "gamma",
            "r_bar",
            "sampled_g_plus_count",
            "sampled_g_plus_count_per_10000",
            "sampled_target_mean",
            "sampled_target_variance"
          ]
        },
        {
          "_type": "object",
          "key_count": 8,
          "keys": [
            "analytic_expected_mean",
            "analytic_expected_variance",
            "gamma",
            "r_bar",
            "sampled_g_plus_count",
            "sampled_g_plus_count_per_10000",
            "sampled_target_mean",
            "sampled_target_variance"
          ]
        },
        {
          "_type": "object",
          "key_count": 8,
          "keys": [
            "analytic_expected_mean",
            "analytic_expected_variance",
            "gamma",
            "r_bar",
            "sampled_g_plus_count",
            "sampled_g_plus_count_per_10000",
            "sampled_target_mean",
            "sampled_target_variance"
          ]
        }
      ],
      "length": 16
    }
  },
  "claim_tested": "In a one-state normalized-reward augmented transition model, sampled Bernoulli g_plus terminal targets and deterministic soft expected-mass targets have the same mean, while sampled targets retain Bernoulli variance and increasingly rare g_plus events as gamma approaches 1; in a tiny finite MDP, F_gplus_star / (1 - gamma) matches normalized Q_star.",
  "experiment_id": "0001",
  "interpretation": "The deterministic soft target exactly equals the analytic expected terminal mass and has zero variance. The sampled Bernoulli estimator matched that mean within the predeclared Monte Carlo tolerance at all 16 sweep points, but retained nonzero target variance up to 0.0904013. The rarest observed g_plus rate was 0.48 per 10000 transitions, exposing the sparse-event issue for high gamma and low r_bar. The finite-MDP scaled soft successor check passed with max_abs_error 3.94752e-08.",
  "known_failures": [],
  "metrics": {
    "all_sampled_means_within_tolerance": true,
    "all_soft_variances_negligible": true,
    "finite_mdp_equivalence": {
      "_type": "list",
      "first_items": [
        {
          "_type": "object",
          "key_count": 10,
          "keys": [
            "f_final_delta",
            "f_gplus_star",
            "f_value_iteration_steps",
            "gamma",
            "max_abs_error_scaled_f_vs_q",
            "passes_tolerance",
            "q_final_delta",
            "q_star",
            "q_value_iteration_steps",
            "scaled_f_gplus_star"
          ]
        },
        {
          "_type": "object",
          "key_count": 10,
          "keys": [
            "f_final_delta",
            "f_gplus_star",
            "f_value_iteration_steps",
            "gamma",
            "max_abs_error_scaled_f_vs_q",
            "passes_tolerance",
            "q_final_delta",
            "q_star",
            "q_value_iteration_steps",
            "scaled_f_gplus_star"
          ]
        },
        {
          "_type": "object",
          "key_count": 10,
          "keys": [
            "f_final_delta",
            "f_gplus_star",
            "f_value_iteration_steps",
            "gamma",
            "max_abs_error_scaled_f_vs_q",
            "passes_tolerance",
            "q_final_delta",
            "q_star",
            "q_value_iteration_steps",
            "scaled_f_gplus_star"
          ]
        }
      ],
      "length": 4
    },
    "finite_mdp_equivalence_pass": true,
    "finite_mdp_equivalence_tolerance": 1e-06,
    "finite_mdp_max_abs_error_scaled_f_vs_q": 3.9475168023273e-08,
    "gammas": [
      0.9,
      0.95,
      0.99,
      0.995
    ],
    "max_abs_sampled_minus_soft_mean": 0.0005020000000000163,
    "max_analytic_target_coefficient_of_variation": 141.41782065920822,
    "max_monte_carlo_abs_tolerance": 0.0018,
    "max_sampled_g_plus_count_per_10000": 1005.02,
    "max_sampled_target_variance": 0.090401347996,
    "max_soft_target_variance": 0.0,
    "min_sampled_g_plus_count_per_10000": 0.48000000000000004,
    "model_definition": {
      "bootstrap_term": "Set to zero to isolate the immediate terminal-mass estimator; this is the variance source being tested in experiment 0001.",
      "deterministic_soft_target": {
        "_type": "object",
        "key_count": 2,
        "keys": [
          "sampling_variance",
          "soft_g_plus_target"
        ]
      },
      "one_state_setup": "Every row represents repeated draws from one normalized-reward state-action transition with fixed r_bar in [0, 1].",
      "reward_normalization": "r_bar is pre-normalized reward in [0, 1].",
      "sampled_augmented_terminal_model": {
        "_type": "object",
        "key_count": 4,
        "keys": [
          "P(continue_to_original_next_state | s,a)",
          "P(g_minus | s,a)",
          "P(g_plus | s,a)",
          "sampled_g_plus_target"
        ]
      }
    },
    "monte_carlo_tolerance_rule": "abs(sampled_target_mean - soft_target_mean) <= 6.0 * sqrt(p_g_plus * (1 - p_g_plus) / samples)",
    "num_sweep_points": 16,
    "per_setting_metrics": {
      "_type": "list",
      "first_items": [
        {
          "_type": "object",
          "key_count": 24,
          "keys": [
            "analytic_expected_g_plus_count",
            "analytic_expected_g_plus_count_per_10000",
            "analytic_expected_mean",
            "analytic_expected_variance",
            "analytic_sample_mean_stderr",
            "analytic_target_coefficient_of_variation",
            "gamma",
            "monte_carlo_abs_tolerance",
            "p_continue",
            "p_g_minus",
            "p_g_plus",
            "r_bar",
            "sampled_g_plus_count",
            "sampled_g_plus_count_per_10000",
            "sampled_mean_abs_error_vs_soft",
            "sampled_mean_within_tolerance",
            "sampled_minus_soft_mean",
            "sampled_minus_soft_variance",
            "sampled_target_mean",
            "sampled_target_variance"
          ]
        },
        {
          "_type": "object",
          "key_count": 24,
          "keys": [
            "analytic_expected_g_plus_count",
            "analytic_expected_g_plus_count_per_10000",
            "analytic_expected_mean",
            "analytic_expected_variance",
            "analytic_sample_mean_stderr",
            "analytic_target_coefficient_of_variation",
            "gamma",
            "monte_carlo_abs_tolerance",
            "p_continue",
            "p_g_minus",
            "p_g_plus",
            "r_bar",
            "sampled_g_plus_count",
            "sampled_g_plus_count_per_10000",
            "sampled_mean_abs_error_vs_soft",
            "sampled_mean_within_tolerance",
            "sampled_minus_soft_mean",
            "sampled_minus_soft_variance",
            "sampled_target_mean",
            "sampled_target_variance"
          ]
        },
        {
          "_type": "object",
          "key_count": 24,
          "keys": [
            "analytic_expected_g_plus_count",
            "analytic_expected_g_plus_count_per_10000",
            "analytic_expected_mean",
            "analytic_expected_variance",
            "analytic_sample_mean_stderr",
            "analytic_target_coefficient_of_variation",
            "gamma",
            "monte_carlo_abs_tolerance",
            "p_continue",
            "p_g_minus",
            "p_g_plus",
            "r_bar",
            "sampled_g_plus_count",
            "sampled_g_plus_count_per_10000",
            "sampled_mean_abs_error_vs_soft",
            "sampled_mean_within_tolerance",
            "sampled_minus_soft_mean",
            "sampled_minus_soft_variance",
            "sampled_target_mean",
            "sampled_target_variance"
          ]
        }
      ],
      "length": 16
    },
    "r_bars": [
      0.01,
      0.1,
      0.5,
      1.0
    ],
    "samples_per_setting": 1000000,
    "seed": 20260614,
    "soft_variance_tolerance": 1e-15
  },
  "next_questions": [
    "Does the same expected-mass target match normalized Q-learning in a tabular CliffWalking sanity check?",
    "How much TD target variance remains once the bootstrap term is included in a tiny tabular learner?",
    "Does the finite-MDP equivalence stay stable in off-policy fitted tabular updates with partial coverage?"
  ],
  "status": "completed"
}
```


## Latest summary

# Experiment 0001 Summary

## Setup

This diagnostic isolates the immediate terminal-mass estimator in the one-state augmented model. Rewards are pre-normalized as `r_bar in [0, 1]`; the sampled model uses `P(g_plus | s,a) = (1 - gamma) * r_bar`, and the deterministic soft target uses the same expected mass directly.

Samples per sweep point: `1000000`. Seed: `20260614`. Bootstrap is set to zero so the only variance source is the sampled terminal event.

## Commands Run

```bash
mkdir -p research/reward_to_gcrl/artifacts/0001 research/reward_to_gcrl/results
conda run -n autoresearcher_reward_to_gcrl python research/reward_to_gcrl/artifacts/0001/run_terminal_variance_diagnostic.py --samples 1000000 --seed 20260614
conda run -n autoresearcher_reward_to_gcrl python -m jsonschema -i research/reward_to_gcrl/results/0001_result.json schemas/result.schema.json
conda run -n autoresearcher_reward_to_gcrl python scripts/validate_artifacts.py --repo-root . --json research/reward_to_gcrl/results/0001_result.json --schema schemas/result.schema.json --check-result-artifacts
```

## Raw Metrics

| gamma | r_bar | sampled mean | soft mean | sampled var | soft var | g_plus / 10000 | expected / 10000 |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 0.900 | 0.01 | 0.00096100 | 0.00100000 | 0.00096008 | 0.0 | 9.6100 | 10.0000 |
| 0.900 | 0.10 | 0.01019400 | 0.01000000 | 0.01009008 | 0.0 | 101.9400 | 100.0000 |
| 0.900 | 0.50 | 0.04987600 | 0.05000000 | 0.04738838 | 0.0 | 498.7600 | 500.0000 |
| 0.900 | 1.00 | 0.10050200 | 0.10000000 | 0.09040135 | 0.0 | 1005.0200 | 1000.0000 |
| 0.950 | 0.01 | 0.00047900 | 0.00050000 | 0.00047877 | 0.0 | 4.7900 | 5.0000 |
| 0.950 | 0.10 | 0.00508600 | 0.00500000 | 0.00506013 | 0.0 | 50.8600 | 50.0000 |
| 0.950 | 0.50 | 0.02521700 | 0.02500000 | 0.02458110 | 0.0 | 252.1700 | 250.0000 |
| 0.950 | 1.00 | 0.05002500 | 0.05000000 | 0.04752250 | 0.0 | 500.2500 | 500.0000 |
| 0.990 | 0.01 | 0.00010900 | 0.00010000 | 0.00010899 | 0.0 | 1.0900 | 1.0000 |
| 0.990 | 0.10 | 0.00099700 | 0.00100000 | 0.00099601 | 0.0 | 9.9700 | 10.0000 |
| 0.990 | 0.50 | 0.00502600 | 0.00500000 | 0.00500074 | 0.0 | 50.2600 | 50.0000 |
| 0.990 | 1.00 | 0.00978000 | 0.01000000 | 0.00968435 | 0.0 | 97.8000 | 100.0000 |
| 0.995 | 0.01 | 0.00004800 | 0.00005000 | 0.00004800 | 0.0 | 0.4800 | 0.5000 |
| 0.995 | 0.10 | 0.00047900 | 0.00050000 | 0.00047877 | 0.0 | 4.7900 | 5.0000 |
| 0.995 | 0.50 | 0.00254900 | 0.00250000 | 0.00254250 | 0.0 | 25.4900 | 25.0000 |
| 0.995 | 1.00 | 0.00501000 | 0.00500000 | 0.00498490 | 0.0 | 50.1000 | 50.0000 |

The rarest analytic event rate occurs at `gamma=0.995` and `r_bar=0.01`: `0.5000` expected `g_plus` events per 10000 transitions.

## Finite-MDP Equivalence

The same script solves a tiny 3-state, 2-action finite MDP twice: once with normalized rewards as `Q_norm_star`, and once with soft terminal mass rewards `(1 - gamma) * r_bar` as `F_gplus_star`. The check reports `max_abs(F_gplus_star / (1 - gamma) - Q_norm_star)`.

| gamma | max abs error | tolerance | q iterations | f iterations |
|---:|---:|---:|---:|---:|
| 0.900 | 7.615e-11 | 1.0e-06 | 264 | 242 |
| 0.950 | 3.476e-10 | 1.0e-06 | 540 | 482 |
| 0.990 | 9.708e-09 | 1.0e-06 | 2751 | 2293 |
| 0.995 | 3.948e-08 | 1.0e-06 | 5514 | 4457 |

## Outcome

Status: `completed`.

All sampled means were within the predeclared Monte Carlo tolerance rule `6 * sqrt(p * (1 - p) / samples)`, where `p=(1-gamma)*r_bar`. The soft target variance was exactly zero in every setting. The finite-MDP scaled soft successor check passed at tolerance `1.0e-06`. The sampled estimator therefore matches the soft target mean in this sanity check, but keeps Bernoulli target variance and exposes rare `g_plus` events as `gamma` approaches 1.

## Artifacts

- `research/reward_to_gcrl/artifacts/0001/run_terminal_variance_diagnostic.py`
- `research/reward_to_gcrl/artifacts/0001/raw_metrics.json`
- `research/reward_to_gcrl/artifacts/0001/metrics.csv`
- `research/reward_to_gcrl/artifacts/0001/metadata.json`
- `research/reward_to_gcrl/artifacts/0001/finite_mdp_equivalence.json`

## Negative Findings

No success criterion failed in this isolated diagnostic. This does not yet test bootstrapped fitted updates, partial-coverage data, or larger tabular environments; those remain separate follow-up checks.


## Latest review summary

```json
{
  "allows_auto_continue": true,
  "escalation_reason": null,
  "evidence_checked": {
    "_type": "list",
    "first_items": [
      "research/reward_to_gcrl/results/0001_result.json",
      "research/reward_to_gcrl/results/0001_summary.md",
      "research/reward_to_gcrl/artifacts/0001/run_terminal_variance_diagnostic.py"
    ],
    "length": 11
  },
  "evidence_quality": "medium",
  "experiment_id": "0001",
  "failure_criteria_triggered": false,
  "reasons": [
    "Required result JSON, summary markdown, and artifact directory/files are present.",
    "Result JSON validates against schemas/result.schema.json, and declared artifact paths validate with scripts/validate_artifacts.py using local Python.",
    "The sweep covers all 16 planned gamma and r_bar combinations with raw means, variances, g_plus counts, soft zero variance, sample count, and seed.",
    "Independent recomputation confirms all sampled means are within the planned 3 standard errors; max z score was 2.211.",
    "Finite-MDP equivalence passes with max_abs_error_scaled_f_vs_q 3.9475e-08, below the 1e-6 criterion.",
    "No neural approximation, large environment, expensive training, or GPU dependence was introduced.",
    "Interpretation is mostly scoped correctly and notes that bootstrap, partial coverage, and larger tabular environments remain untested."
  ],
  "required_fixes": [],
  "risk_flags": [
    "Executor recorded and described a 6-SE Monte Carlo mean tolerance even though the plan specified 3 standard errors; raw metrics still pass the stricter 3-SE check.",
    "Variance agreement is reported through sampled and analytic raw variances but lacks an explicit variance-specific tolerance or pass flag in the result JSON.",
    "The script hard-codes commands_run rather than deriving them from argv; it matches this run's samples and seed but could misreport future reruns."
  ],
  "should_escalate_to_pro": false,
  "success_criteria_satisfied": true,
  "verdict": "weak_pass"
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
    }
  ],
  "project": "reward_to_gcrl"
}
```


## Last decision summaries

## 0001_decision.json

```json
{
  "confidence": 0.93,
  "decision": "continue",
  "evidence": [
    "Current state iteration is 0, so missing latest result/summary/review is expected under the provided first-iteration rule.",
    "env_state reports status: ready for conda environment autoresearcher_reward_to_gcrl.",
    "The charter explicitly names the first experiment: one-state variance sanity check sweeping gamma in {0.90, 0.95, 0.99, 0.995} and r_bar in {0.01, 0.1, 0.5, 1.0}.",
    "The experiment is CPU-scale, synthetic, and directly measures sampled versus soft target means, variances, and g_plus event rarity."
  ],
  "next_experiment": {
    "estimated_runtime_minutes": 10,
    "experiment_id": "0001",
    "hypothesis": "Sampled Bernoulli terminal targets and deterministic soft expected targets have matching means, while the sampled estimator has variance and increasingly rare g_plus events as gamma approaches 1; the soft target has zero sampling variance for the terminal mass term.",
    "objective": "Implement and run the one-state terminal-target variance sanity check for the soft successor reward-success goal.",
    "required_outputs": [
      "research/reward_to_gcrl/results/0001_result.json",
      "research/reward_to_gcrl/results/0001_summary.md",
      "research/reward_to_gcrl/artifacts/0001/ with diagnostic script and raw metrics"
    ]
  },
  "progress_score": 0,
  "rationale": "Iteration 0 has no prior result, which is expected. The charter is specific, the project environment is ready, and the first experiment guidance is concrete, cheap, and directly tests the estimator-variance premise before larger learners.",
  "risks": [
    "The executor could accidentally implement larger tabular or neural learners before the variance diagnostic is validated.",
    "Reward normalization and Bernoulli event probability must be stated explicitly so mean comparisons are interpretable.",
    "Rare events at high gamma may make empirical mean matching noisy unless analytic expectations and Monte Carlo tolerances are reported."
  ]
}
```

## 0001_pro_decision.json

```json
{
  "confidence": 0.74,
  "decision": "continue",
  "evidence": [
    "The project charter defines the goal as testing whether soft successor-measure reward-to-goal conversion preserves equivalence while avoiding sparse high-variance terminal sampling.",
    "The charter states the main hypothesis: the g_plus head trained with expected terminal mass should match normalized Q-learning in tabular sanity checks while avoiding sampled terminal event variance.",
    "The current repository state has iteration 0, no last summary path, no primary metric, and no best primary metric, so there is not yet recorded experimental evidence of progress.",
    "The local Codex decision chose continue and identified experiment 0001 as the one-state terminal-target variance sanity check.",
    "The charter explicitly prohibits MuJoCo, AntMaze, OGBench, large downloads, or long neural training before tabular diagnostics pass."
  ],
  "next_experiment": {
    "estimated_runtime_minutes": 10,
    "experiment_id": "0001",
    "hypothesis": "For each gamma and normalized reward r_bar, the sampled Bernoulli terminal target has mean (1 - gamma) * r_bar and variance p * (1 - p), where p = (1 - gamma) * r_bar, while the soft target has the same mean and zero terminal-sampling variance; in a tiny finite MDP, F_gplus_star / (1 - gamma) should match Q_norm_star within numerical tolerance.",
    "objective": "Create a reproducible CPU-only diagnostic that verifies the sampled augmented terminal target and the deterministic soft terminal target have the same expectation, quantifies the sampled target variance and g_plus rarity, and confirms the soft g_plus Bellman fixed point equals normalized Q-learning up to the (1 - gamma) scaling in a tiny finite MDP.",
    "required_outputs": [
      "research/reward_to_gcrl/results/0001_result.json",
      "research/reward_to_gcrl/results/0001_summary.md",
      "research/reward_to_gcrl/artifacts/0001/"
    ]
  },
  "progress_score": null,
  "rationale": "Continue, but treat the project as still pre-evidence rather than making any positive research claim. The available repository state shows iteration 0 with no recorded latest summary or primary metric, while the charter and local decision specify a cheap first diagnostic that directly tests the estimator-variance premise. The missing latest_summary.md means I cannot credit unverified progress, so the next step should be the smallest reproducible variance-and-equivalence diagnostic, not neural learners or larger environments.",
  "risks": [
    "The latest progress summary path supplied by the user was not found, so reported results cannot be evaluated from the repository evidence.",
    "The soft g_plus head alone may reduce to normalized Q-learning up to scaling, so it is not a research contribution unless later experiments show auxiliary goals, transfer, variance reduction, or diagnostics add value.",
    "A variance sanity check can prove the sampled estimator is noisy but cannot prove the full method improves GCRL or reward learning.",
    "Moving to neural function approximation before exact/tabular equivalence is verified would create ambiguous failures."
  ]
}
```


## Full evidence paths

- `research/reward_to_gcrl/results/0001_result.json`
- `research/reward_to_gcrl/results/0001_summary.md`
- `research/reward_to_gcrl/reviews/0001_review.json`

Use these paths if compact summaries are insufficient.


## Stop, pivot, continue rules

- For iteration 0, a missing latest result is expected and is not by itself a reason to stop.
- After iteration 0, stop or choose needs_human on missing or invalid result files.
- Stop on repeated invalid, negative, or low-value results.
- Pivot only when evidence weakens the original idea but reveals a nearby testable idea.
- Continue or pivot only for one cheap, high-information experiment.
- Choose needs_human for ambiguity, expensive work, missing artifacts, or risky pivots.


## Next experiment id

Use `0002` as the exact `next_experiment.experiment_id` if you choose continue or pivot.
