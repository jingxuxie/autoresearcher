# Progress Summarizer Context: reward_to_gcrl

## Requested action

Write a concise human-readable Markdown progress summary for this project. Use the evidence below; do not overclaim beyond reviewed results.


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

## Current state

```json
{
  "best_primary_metric": null,
  "failure_streak": 0,
  "human_review_required": false,
  "iteration": 9,
  "last_decision": "continue",
  "last_failure": null,
  "last_pro_review_iteration": 8,
  "last_pro_review_path": "research/reward_to_gcrl/decisions/0009_pro_decision.json",
  "last_summary_iteration": 8,
  "last_summary_path": "research/reward_to_gcrl/progress/0008_pre_pro_this_is_the_first_shared_parameter_function_approximation_milestone__keep_the_run_small__but_require_review_before_expanding_to_larger_sweeps__neural_frameworks__or_publishable_auxiliary_goal_claims_summary.md",
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
    "2026-06-14T21:52:11+00:00: applied Pro decision continue from research/reward_to_gcrl/decisions/0007_pro_decision.json",
    "2026-06-14T22:55:15+00:00: Pro decision saved for checkpoint This is the first shared-parameter function-approximation milestone. Keep the run small, but require review before expanding to larger sweeps, neural frameworks, or publishable auxiliary-goal claims. (research/reward_to_gcrl/decisions/0009_pro_decision.json)",
    "2026-06-14T22:55:17+00:00: applied Pro decision continue from research/reward_to_gcrl/decisions/0009_pro_decision.json"
  ],
  "pending_checkpoint": null,
  "pending_local_decision_path": null,
  "primary_metric": null,
  "pro_review_count": 8,
  "protected_file_drift": false,
  "status": "active",
  "weak_pass_streak": 1
}
```


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


## Experiment ledger

```json
[
  {
    "allows_auto_continue": true,
    "baseline_metrics": {
      "_key_count": 6,
      "_keys": [
        "baseline_name",
        "baseline_target_definition",
        "max_sampled_g_plus_count_per_10000",
        "max_sampled_target_variance",
        "min_sampled_g_plus_count_per_10000",
        "per_setting_sampled_metrics"
      ],
      "scalars": {
        "baseline_name": "sampled_bernoulli_terminal_target",
        "baseline_target_definition": "Bernoulli((1 - gamma) * r_bar) indicator for g_plus.",
        "max_sampled_g_plus_count_per_10000": 1005.02,
        "max_sampled_target_variance": 0.090401347996,
        "min_sampled_g_plus_count_per_10000": 0.48000000000000004
      }
    },
    "claim_tested": "In a one-state normalized-reward augmented transition model, sampled Bernoulli g_plus terminal targets and deterministic soft expected-mass targets have the same mean, while sampled targets retain Bernoulli variance and increasingly rare g_...",
    "decision": "continue",
    "hypothesis": "For each gamma and normalized reward r_bar, the sampled Bernoulli terminal target has mean (1 - gamma) * r_bar and variance p * (1 - p), where p = (1 - gamma) * r_bar, while the soft target has the same mean and zero terminal-sampling varia...",
    "interpretation": "The deterministic soft target exactly equals the analytic expected terminal mass and has zero variance.",
    "iteration": "0001",
    "metrics": {
      "_key_count": 22,
      "_keys": [
        "all_sampled_means_within_tolerance",
        "all_soft_variances_negligible",
        "finite_mdp_equivalence",
        "finite_mdp_equivalence_pass",
        "finite_mdp_equivalence_tolerance",
        "finite_mdp_max_abs_error_scaled_f_vs_q",
        "gammas",
        "max_abs_sampled_minus_soft_mean",
        "max_analytic_target_coefficient_of_variation",
        "max_monte_carlo_abs_tolerance",
        "max_sampled_g_plus_count_per_10000",
        "max_sampled_target_variance",
        "max_soft_target_variance",
        "min_sampled_g_plus_count_per_10000",
        "model_definition",
        "monte_carlo_tolerance_rule",
        "num_sweep_points",
        "per_setting_metrics",
        "r_bars",
        "samples_per_setting",
        "seed",
        "soft_variance_tolerance"
      ],
      "scalars": {
        "all_sampled_means_within_tolerance": true,
        "all_soft_variances_negligible": true,
        "finite_mdp_equivalence_pass": true,
        "finite_mdp_equivalence_tolerance": 1e-06,
        "finite_mdp_max_abs_error_scaled_f_vs_q": 3.9475168023273e-08,
        "max_abs_sampled_minus_soft_mean": 0.0005020000000000163,
        "max_analytic_target_coefficient_of_variation": 141.41782065920822,
        "max_monte_carlo_abs_tolerance": 0.0018
      }
    },
    "objective": "Create a reproducible CPU-only diagnostic that verifies the sampled augmented terminal target and the deterministic soft terminal target have the same expectation, quantifies the sampled target variance and g_plus rarity, and confirms the s...",
    "review": "weak_pass",
    "review_reasons": [
      "Required result JSON, summary markdown, and artifact directory/files are present.",
      "Result JSON validates against schemas/result.schema.json, and declared artifact paths validate with scripts/validate_artifacts.py using local Python.",
      "The sweep covers all 16 planned gamma and r_bar combinations with raw means, variances, g_plus counts, soft zero variance, sample count, and seed.",
      "... 4 more; inspect full file"
    ],
    "risk_flags": [
      "Executor recorded and described a 6-SE Monte Carlo mean tolerance even though the plan specified 3 standard errors; raw metrics still pass the stricter 3-SE check.",
      "Variance agreement is reported through sampled and analytic raw variances but lacks an explicit variance-specific tolerance or pass flag in the result JSON.",
      "The script hard-codes commands_run rather than deriving them from argv; it matches this run's samples and seed but could misreport future reruns."
    ],
    "status": "completed"
  },
  {
    "allows_auto_continue": true,
    "baseline_metrics": {
      "_key_count": 6,
      "_keys": [
        "baseline_name",
        "evaluation_episodes_per_seed",
        "max_learned_bellman_residual",
        "mean_normalized_return",
        "mean_raw_return",
        "mean_success_rate"
      ],
      "scalars": {
        "baseline_name": "tabular_normalized_reward_q_learning",
        "evaluation_episodes_per_seed": 100,
        "max_learned_bellman_residual": 99.9999999999978,
        "mean_normalized_return": 200.0,
        "mean_raw_return": -200.0,
        "mean_success_rate": 0.0
      }
    },
    "claim_tested": "For a fully audited local deterministic 4x12 CliffWalking transition table, the terminal-only soft successor g_plus Bellman fixed point and paired tabular learner match normalized-reward Q-learning after division by (1 - gamma).",
    "decision": "continue",
    "hypothesis": "For a deterministic 4x12 CliffWalking MDP with declared rewards, reset, cliff, and terminal semantics, the exact soft successor fixed point satisfies F_gplus_star/(1-gamma) = Q_norm_star, and paired tabular soft successor learning induces t...",
    "interpretation": "The local deterministic CliffWalking table resolves the previous Gymnasium compatibility blocker.",
    "iteration": "0002",
    "metrics": {
      "_key_count": 5,
      "_keys": [
        "config",
        "environment_audit",
        "exact_dp",
        "paired_learning",
        "pass_flags"
      ],
      "nested_samples": {
        "config": {
          "exact_scaling_tolerance": 1e-06
        },
        "pass_flags": {
          "exact_dp_scaling_equivalence": true
        }
      }
    },
    "objective": "Rerun the blocked CliffWalking tabular equivalence test using a small local deterministic transition-table implementation with fully audited semantics, then compare exact-DP references, normalized Q-learning, and terminal-only soft successo...",
    "review": "weak_pass",
    "review_reasons": [
      "Required result JSON, summary markdown, and declared artifact directory/files are present.",
      "Result JSON validates against schemas/result.schema.json, and declared artifact paths validate successfully.",
      "The local environment audit is complete, records the requested CliffWalking semantics, uses no Gymnasium environment dependency, has 192 transition records, and the saved transitio...",
      "... 4 more; inspect full file"
    ],
    "risk_flags": [
      "The declared normalization maps ordinary step and goal rewards to 1 and cliff falls to 0, causing the learned/evaluated greedy policies to never reach the goal; this is acceptable...",
      "Policy-disagreement evidence is weak because exact DP has 37 tie states and 0 comparable non-tie states; paired learning also has many tie states and few comparable states in sever...",
      "The paired learned-value comparison is nearly algebraic because both learners use identical transitions, initialization, alpha, and targets that differ only by the (1-gamma) scale.",
      "... 2 more; inspect full file"
    ],
    "status": "completed"
  },
  {
    "allows_auto_continue": true,
    "baseline_metrics": {
      "_key_count": 7,
      "_keys": [
        "baseline_name",
        "mean_conditional_sampling_variance",
        "mean_final_bellman_residual_sufficient",
        "mean_final_value_error_sufficient",
        "mean_g_plus_events_per_10000",
        "mean_raw_return",
        "mean_success_rate"
      ],
      "scalars": {
        "baseline_name": "sampled_augmented_g_plus_learning",
        "mean_conditional_sampling_variance": 0.0004278098216495158,
        "mean_final_bellman_residual_sufficient": 0.04124613525377317,
        "mean_final_value_error_sufficient": 0.08156038291965984,
        "mean_g_plus_events_per_10000": 212.67000000000002,
        "mean_raw_return": -200.0,
        "mean_success_rate": 0.0
      }
    },
    "claim_tested": "On the audited local CliffWalking transition table, sampled augmented g_plus learning is an unbiased but higher-variance estimator of the terminal-only soft successor target and reduces error more slowly under the same original transition b...",
    "decision": "continue",
    "hypothesis": "For the same original transition stream, the sampled augmented g_plus learner is an unbiased but higher-variance estimator of the soft target, so it should observe sparse g_plus events and have higher TD target variance and worse or slower...",
    "interpretation": "The sampled augmented target is unbiased within the predeclared Monte Carlo tolerance in all gamma/seed runs, but its terminal sampling variance is strictly positive while the deterministic soft target has zero terminal sampling variance.",
    "iteration": "0003",
    "metrics": {
      "_key_count": 5,
      "_keys": [
        "config",
        "environment_audit",
        "exact_soft_dp",
        "pass_flags",
        "sampled_vs_soft"
      ]
    },
    "objective": "Compare sampled augmented g_plus learning against the terminal-only soft successor update on the audited local tabular CliffWalking MDP under the same data budget.",
    "review": "weak_pass",
    "review_reasons": [
      "Required 0003 result JSON, summary markdown, and declared artifact files are present.",
      "Result JSON validates against schemas/result.schema.json, and declared artifact paths validate successfully.",
      "The 0003 environment audit is complete, recomputes to the saved transition hash, and matches the audited 0002 transition table hash.",
      "... 5 more; inspect full file"
    ],
    "risk_flags": [
      "The target-mean pass compares sampled targets to the sampled learner's conditional expected target, not to the deterministic soft learner's recorded target; sampled-vs-soft-determi...",
      "The summary claims lower/faster value-error dominance, but mean final soft value error is slightly worse overall than sampled value error, and soft value-error dominance is only 17...",
      "At gamma 0.995, soft value-error dominance is only 4 of 10 seeds, so the value-error evidence does not strengthen as gamma approaches 1.",
      "... 4 more; inspect full file"
    ],
    "status": "completed"
  },
  {
    "allows_auto_continue": true,
    "baseline_metrics": {
      "_key_count": 8,
      "_keys": [
        "baseline_name",
        "mean_conditional_sampling_variance",
        "mean_final_bellman_residual",
        "mean_final_value_error",
        "mean_g_plus_events_per_10000",
        "mean_policy_disagreement",
        "mean_raw_return",
        "mean_success_rate"
      ],
      "scalars": {
        "baseline_name": "sampled_augmented_g_plus_learning",
        "mean_conditional_sampling_variance": 0.006258455730468815,
        "mean_final_bellman_residual": 0.005863347048562961,
        "mean_final_value_error": 0.028406430871095144,
        "mean_g_plus_events_per_10000": 63.79,
        "mean_policy_disagreement": 0.55,
        "mean_raw_return": 0.0,
        "mean_success_rate": 0.0
      }
    },
    "claim_tested": "In a nondegenerate tiny chain with identity reward normalization, sampled augmented g_plus updates are unbiased but higher variance, while deterministic soft terminal marginalization improves Bellman residual and preserves policy quality.",
    "decision": "needs_human",
    "hypothesis": "The 0004 scientific result is likely useful, but its evidential status depends on whether the protected-file drift is stale or harmless versus real or unresolved.",
    "interpretation": "The repaired chain preserves the raw policy under identity normalization.",
    "iteration": "0004",
    "metrics": {
      "_key_count": 14,
      "_keys": [
        "artifact_validation_status_after_drift_audit",
        "config",
        "drift_status",
        "environment_audit",
        "evidence_integrity_verdict",
        "exact_dp",
        "pass_flags",
        "protected_file_drift_affected_files",
        "protected_file_drift_audit",
        "protected_file_drift_currently_modified",
        "protected_file_drift_impact",
        "sampled_vs_soft",
        "schema_validation_status_after_drift_audit",
        "verdict"
      ],
      "nested_samples": {
        "pass_flags": {
          "exact_dp_non_tie_policy_informative": true
        }
      },
      "scalars": {
        "artifact_validation_status_after_drift_audit": "passed",
        "drift_status": "harmless",
        "evidence_integrity_verdict": "accepted_evidence",
        "protected_file_drift_audit": "research/reward_to_gcrl/artifacts/0004/protected_file_drift_audit.json",
        "protected_file_drift_currently_modified": false,
        "protected_file_drift_impact": "harmless for experiment logic/reporting; stale after committed configuration change",
        "schema_validation_status_after_drift_audit": "passed",
        "verdict": "learning-improvement"
      }
    },
    "objective": "Resolve the protected_file_drift blocker and determine whether the existing 0004 nondegenerate 5-state sampled-vs-soft result can be accepted as evidence, superseded by a clean rerun, rejected due to drift, or marked inconclusive.",
    "review": "weak_pass",
    "review_reasons": [
      "Required 0004 result JSON, summary markdown, and declared artifact files are present.",
      "Result JSON validates against schemas/result.schema.json, and declared artifact paths validate successfully.",
      "The drift audit identifies autoresearcher.yaml as the only protected file flagged by the guard, records it as clean at HEAD, includes a SHA-256 hash, and assesses the prior change...",
      "... 3 more; inspect full file"
    ],
    "risk_flags": [
      "The latest plan text inconsistently references 0005 audit/result paths, while required outputs and actual evidence use 0004 paths.",
      "drift_status and evidence_integrity_verdict are under metrics rather than top-level result fields.",
      "The accepted learning-improvement evidence is still from a tiny 5-state chain with controlled matched streams; broader environments remain untested.",
      "... 1 more; inspect full file"
    ],
    "status": "completed"
  },
  {
    "allows_auto_continue": true,
    "baseline_metrics": {
      "_key_count": 7,
      "_keys": [
        "baseline_name",
        "mean_final_bellman_residual",
        "mean_final_value_error",
        "mean_g_plus_events_per_10000",
        "mean_greedy_raw_return",
        "mean_policy_disagreement",
        "zero_g_plus_event_runs"
      ],
      "scalars": {
        "baseline_name": "sampled_augmented_g_plus_learning",
        "mean_final_bellman_residual": 0.012418827299201882,
        "mean_final_value_error": 0.11345317088891518,
        "mean_g_plus_events_per_10000": 66.60833333333332,
        "mean_greedy_raw_return": 48.28433333333334,
        "mean_policy_disagreement": 0.09444444444444446,
        "zero_g_plus_event_runs": 0
      }
    },
    "claim_tested": "On a small stochastic RiverSwim chain with normalized rewards in [0,1], sampled augmented g_plus updates are unbiased but higher variance than deterministic soft terminal updates, and soft learning improves Bellman/value error under matched...",
    "decision": "continue",
    "hypothesis": "On a small RiverSwim chain with rewards already normalized to [0,1], sampled augmented g_plus updates are unbiased but higher variance than deterministic soft terminal updates; under matched transition streams, the soft learner should show...",
    "interpretation": "The RiverSwim diagnostic supports the hypothesis: sampled targets match the deterministic soft marginal target within Monte Carlo tolerance while retaining higher terminal-sampling variance, and the deterministic soft learner has lower or f...",
    "iteration": "0005",
    "metrics": {
      "_key_count": 5,
      "_keys": [
        "config",
        "environment_audit",
        "exact_dp",
        "pass_flags",
        "sampled_vs_soft"
      ],
      "nested_samples": {
        "pass_flags": {
          "exact_scaled_soft_matches_q_norm": true
        }
      }
    },
    "objective": "Run a CPU-only tabular sampled-vs-soft diagnostic on a small stochastic RiverSwim chain to test long-horizon reward propagation under sparse right-end rewards.",
    "review": "pass",
    "review_reasons": [
      "Required 0005 result JSON, summary markdown, and artifact directory are present.",
      "Result JSON validates against schemas/result.schema.json, and declared artifact paths validate successfully.",
      "The artifact set includes the RiverSwim script, environment audit, exact DP references, per-seed metrics, learning curves, raw metrics, and progress log.",
      "... 5 more; inspect full file"
    ],
    "risk_flags": [
      "The behavior policy is epsilon-greedy with respect to the exact normalized-Q greedy action, so the result is a controlled matched-stream propagation test rather than an online expl...",
      "Right-end coverage is strong under the oracle-guided behavior stream; conclusions about sparse-reward exploration failures should be tested separately with a non-oracle exploratory...",
      "Greedy-policy return is not uniformly better for the soft learner per seed: soft has higher mean return overall, but is strictly higher than sampled in only 14 of 30 runs and has a...",
      "... 1 more; inspect full file"
    ],
    "status": "completed"
  },
  {
    "allows_auto_continue": true,
    "baseline_metrics": {
      "_key_count": 6,
      "_keys": [
        "baseline_name",
        "coverage_starved_count",
        "mean_final_bellman_residual",
        "mean_final_value_error",
        "mean_g_plus_events_per_10000",
        "mean_greedy_raw_return"
      ],
      "scalars": {
        "baseline_name": "sampled_augmented_g_plus_learning",
        "coverage_starved_count": 30,
        "mean_final_bellman_residual": 0.006132067160953,
        "mean_final_value_error": 0.16245872461872082,
        "mean_g_plus_events_per_10000": 6.636666666666667,
        "mean_greedy_raw_return": 23.626833333333334
      }
    },
    "claim_tested": "On 6-state RiverSwim with non-oracle behavior streams, sampled augmented g_plus updates remain unbiased but higher variance than deterministic soft updates, with coverage determining whether learning advantages are interpretable.",
    "decision": "continue",
    "hypothesis": "With matched original transition streams generated by non-oracle exploration, sampled augmented g_plus updates remain unbiased but higher variance than deterministic soft updates.",
    "interpretation": "With non-oracle behavior streams, sampled targets remain unbiased within tolerance and higher variance.",
    "iteration": "0006",
    "metrics": {
      "_key_count": 5,
      "_keys": [
        "config",
        "environment_audit",
        "exact_dp",
        "pass_flags",
        "sampled_vs_soft"
      ],
      "nested_samples": {
        "pass_flags": {
          "exact_scaled_soft_matches_q_norm": true
        }
      }
    },
    "objective": "Repeat the 6-state RiverSwim sampled-vs-soft diagnostic using non-oracle exploratory behavior streams.",
    "review": "pass",
    "review_reasons": [
      "Required 0006 result JSON, summary markdown, and artifact directory are present.",
      "Result JSON validates against schemas/result.schema.json, and declared artifact paths validate successfully.",
      "The artifact set includes the non-oracle RiverSwim script, environment audit, exact DP references, per-seed metrics, learning curves, raw metrics, and progress log.",
      "... 6 more; inspect full file"
    ],
    "risk_flags": [
      "Half of the runs are coverage-starved under the predeclared threshold, so learning-performance conclusions should be restricted to the adequate-coverage subset or explicitly labele...",
      "In coverage-starved uniform-random runs, soft has lower Bellman residual but worse mean value error than sampled in most runs, so value-error superiority is not uniform under poor...",
      "The behavior policies are simple state-independent random policies; additional non-oracle exploration policies may be needed before broader claims.",
      "... 1 more; inspect full file"
    ],
    "status": "completed"
  },
  {
    "allows_auto_continue": true,
    "baseline_metrics": {
      "_key_count": 6,
      "_keys": [
        "baseline_name",
        "coverage_starved_count",
        "mean_final_bellman_residual",
        "mean_final_value_error",
        "mean_g_plus_events_per_10000",
        "mean_greedy_raw_return"
      ],
      "scalars": {
        "baseline_name": "sampled_augmented_g_plus_learning",
        "coverage_starved_count": 30,
        "mean_final_bellman_residual": 0.006313229252871876,
        "mean_final_value_error": 0.1331149724439577,
        "mean_g_plus_events_per_10000": 5.397222222222222,
        "mean_greedy_raw_return": 30.848583333333334
      }
    },
    "claim_tested": "On 6-state RiverSwim with non-oracle behavior streams, sampled augmented g_plus updates remain unbiased but higher variance than deterministic soft updates, with coverage determining whether learning advantages are interpretable.",
    "hypothesis": "The deterministic soft update should consistently reduce terminal-sampling variance in all coverage regimes, but learning-performance advantages should appear mainly when right-reward and state-action coverage are adequate.",
    "interpretation": "Coverage dose response completed: sampled targets match deterministic soft marginal targets within tolerance and have higher terminal-sampling variance in every run.",
    "iteration": "0007",
    "metrics": {
      "_key_count": 6,
      "_keys": [
        "config",
        "environment_audit",
        "exact_dp",
        "pass_flags",
        "recommendation",
        "sampled_vs_soft"
      ],
      "nested_samples": {
        "pass_flags": {
          "exact_scaled_soft_matches_q_norm": true
        }
      },
      "scalars": {
        "recommendation": "move_next_to_tabular_auxiliary_real_state_goals"
      }
    },
    "objective": "Run a CPU-only tabular RiverSwim coverage dose-response experiment that uses several non-oracle behavior policies to create starved, borderline, and adequate coverage regimes, then quantify exactly when deterministic soft terminal marginali...",
    "review": "pass",
    "review_reasons": [
      "Required 0007 result JSON, summary markdown, and artifact directory are present.",
      "Result JSON validates against schemas/result.schema.json, and declared artifact paths validate successfully.",
      "The artifact set includes the coverage dose-response script, fresh environment audit, exact DP references, per-seed metrics, learning curves, raw metrics, and progress log.",
      "... 8 more; inspect full file"
    ],
    "risk_flags": [
      "The coverage-performance regression includes visited_state_action_pairs, but that feature is constant at 12 in the observed runs, so the regression is effectively driven by right-r...",
      "Soft value error is worse than sampled in 4 of 35 adequate-coverage individual runs, although the adequate-bin mean clearly favors soft and satisfies the stated criterion.",
      "Right-biased behavior policies are fixed and non-oracle, but they are hand-designed to favor the known RiverSwim rightward direction; broader non-oracle data-collection policies re...",
      "... 2 more; inspect full file"
    ],
    "status": "completed"
  },
  {
    "allows_auto_continue": true,
    "baseline_metrics": {
      "_key_count": 3,
      "_keys": [
        "baseline_name",
        "max_abs_terminal_only_scaled_minus_q_norm",
        "max_reward_policy_disagreement_vs_exact"
      ],
      "scalars": {
        "baseline_name": "terminal_only_soft_gplus",
        "max_abs_terminal_only_scaled_minus_q_norm": 1.1102230246251565e-16,
        "max_reward_policy_disagreement_vs_exact": 0.0
      }
    },
    "claim_tested": "Adding real-state goal slices to a tabular vector successor measure should leave the g_plus reward-success slice equivalent to the terminal-only soft learner while learning correct real-state goal reachability maps.",
    "decision": "continue",
    "hypothesis": "For a tabular vector SSM with independent goal slices, adding real-state goals should learn correct state-goal reachability maps while leaving the g_plus reward-success slice numerically equivalent to the terminal-only soft learner.",
    "interpretation": "The vector SSM slices are numerically independent in this tabular FourRooms check: the g_plus slice matches terminal-only soft learning, scaled g_plus matches normalized Q, and real-state goal slices match exact reachability references with...",
    "iteration": "0008",
    "metrics": {
      "_key_count": 5,
      "_keys": [
        "config",
        "environment_audit",
        "exact_dp",
        "pass_flags",
        "vector_ssm"
      ],
      "nested_samples": {
        "config": {
          "goal_success_threshold": 0.99
        },
        "pass_flags": {
          "exact_dp_references_computed": true,
          "real_goal_success_rate_high": true
        }
      }
    },
    "objective": "Run a CPU-only tabular vector successor-measure sanity check with real-state goals plus g_plus on a tiny deterministic FourRooms grid.",
    "review": "pass",
    "review_reasons": [
      "Required 0008 result JSON, summary markdown, and artifact directory are present.",
      "Result JSON validates against schemas/result.schema.json, and declared artifact paths validate successfully.",
      "Artifacts include the standalone FourRooms vector SSM script, environment audit, exact DP references, raw metrics, per-goal metrics, heatmap/arrow data, and progress log.",
      "... 6 more; inspect full file"
    ],
    "risk_flags": [
      "This is an exact/full-sweep deterministic sanity check; it validates indexing and independent tabular slices, not learning under sampled data or function approximation.",
      "The result is expected to be nearly tautological because exact references and learned vector backups use the same audited transition semantics; this is acceptable for the predeclar...",
      "Reward-policy comparison has many tie states, 17 of 40 with one skipped terminal state, although disagreement is zero on comparable non-tie states.",
      "... 2 more; inspect full file"
    ],
    "status": "completed"
  },
  {
    "allows_auto_continue": true,
    "baseline_metrics": {
      "_key_count": 4,
      "_keys": [
        "baseline_name",
        "mean_gplus_bellman_residual",
        "mean_gplus_scaled_value_error",
        "mean_reward_success_rate"
      ],
      "scalars": {
        "baseline_name": "terminal_only_gplus_lowrank",
        "mean_gplus_bellman_residual": 0.0009558486105185331,
        "mean_gplus_scaled_value_error": 0.0731219458562512,
        "mean_reward_success_rate": 0.5384615384615384
      }
    },
    "claim_tested": "A shared rank-4 NumPy low-rank FourRooms successor-measure model trained with real-state auxiliary goals should improve the g_plus reward-success slice versus terminal-only g_plus training under matched adequate offline replay, or the auxil...",
    "decision": "continue",
    "hypothesis": "If real-state auxiliary goals provide useful shared representation signal, then under a low-rank bottleneck and adequate replay coverage, combined auxiliary training should reduce g_plus value error and Bellman residual versus terminal-only...",
    "interpretation": "Combined auxiliary training worsened a g_plus metric or reward-policy disagreement under adequate replay coverage; auxiliary-goal benefit is not supported.",
    "iteration": "0009",
    "known_failures": [
      "reward_policy_not_worse",
      "auxiliary_helped_gplus_criterion"
    ],
    "metrics": {
      "_key_count": 5,
      "_keys": [
        "config",
        "environment_audit",
        "exact_dp",
        "lowrank_auxiliary",
        "pass_flags"
      ],
      "nested_samples": {
        "config": {
          "improvement_threshold": 0.1
        }
      }
    },
    "objective": "Run the first CPU-only NumPy shared-parameter test on tiny FourRooms using a low-rank factorized soft successor-measure model, comparing terminal-only g_plus training against combined g_plus plus real-state auxiliary-goal training under mat...",
    "review": "weak_pass",
    "review_reasons": [
      "Required 0009 result JSON, summary markdown, and declared artifact files are present.",
      "Result JSON validates against schemas/result.schema.json, and declared artifact paths validate successfully.",
      "The script is CPU-only NumPy and uses the audited tiny FourRooms transition hash from 0008; no neural framework, GPU, larger environment, or large dependency is present.",
      "... 5 more; inspect full file"
    ],
    "risk_flags": [
      "The primary auxiliary-helped success criterion is not satisfied; this is valid negative evidence, not a positive auxiliary-goal result.",
      "The result is a single predeclared rank-4, learning-rate 0.05, 4000-step checkpoint, so it should not be generalized across optimizer settings or ranks.",
      "Both models have imperfect reward policies, and the combined model collapses badly; this may reflect optimizer or loss-scaling issues as much as a general auxiliary-goal limitation...",
      "... 2 more; inspect full file"
    ],
    "status": "completed"
  }
]
```


## Latest supervisor decision

```json
{
  "confidence": 0.86,
  "decision": "continue",
  "evidence": [
    "The latest summary reports no current blocker and protected_file_drift false.",
    "Reviewed evidence reaches 0008, with strong small-tabular support for the estimator story: deterministic soft terminal marginalization preserves normalized-Q scaling while removing terminal-sampling variance.",
    "0004 repaired the degenerate CliffWalking issue with a nondegenerate 5-state chain and showed soft improved Bellman/value error and policy success over sampled.",
    "0005 and 0006 extended the estimator story to 6-state RiverSwim, including non-oracle behavior streams, while exposing coverage as a key condition.",
    "0007 ran a RiverSwim coverage dose-response and found adequate-coverage runs favored soft on mean Bellman residual and value error, while starved runs remained coverage-limited.",
    "0008 passed the tabular vector SSM implementation gate: max_abs_vector_gplus_minus_terminal_only was 0, scaled vector g_plus matched normalized Q within 1.1102230246251565e-16, and real-state goal slices had zero value error and min greedy goal success rate 1.0.",
    "The 0008 review explicitly warns that independent tabular slices do not test sampled learning, low-rank coupling, or auxiliary representation benefit.",
    "The latest local decision 0009 recommends a CPU-only low-rank factorized SSM on tiny FourRooms comparing terminal-only g_plus training against combined real-state-plus-g_plus auxiliary training under limited offline replay."
  ],
  "next_experiment": {
    "estimated_runtime_minutes": 25,
    "experiment_id": "0009",
    "failure_criteria": [
      "The model does not actually share parameters between real-state goals and g_plus.",
      "The experiment uses independent tabular slices again, which would duplicate 0008 rather than testing shared representation.",
      "Replay coverage is inadequate and the summary still makes auxiliary-benefit claims.",
      "Auxiliary training improves real-state goal metrics but worsens g_plus value error, Bellman residual, or reward-policy disagreement without being labeled negative transfer.",
      "The run sweeps many ranks, losses, auxiliary weights, or optimizers and then selects the best without predeclared criteria.",
      "The experiment installs neural frameworks, uses GPU, expands to larger environments, or makes publishable auxiliary-goal claims before review."
    ],
    "hypothesis": "If real-state auxiliary goals provide useful shared representation signal, then under a low-rank bottleneck and adequate replay coverage, combined auxiliary training should reduce g_plus value error and Bellman residual versus terminal-only g_plus training without increasing reward-policy disagreement. If it does not, then auxiliary-goal benefit is not yet supported and should not be claimed.",
    "objective": "Run the first CPU-only NumPy shared-parameter test on tiny FourRooms using a low-rank factorized soft successor-measure model, comparing terminal-only g_plus training against combined g_plus plus real-state auxiliary-goal training under matched limited offline replay.",
    "required_outputs": [
      "research/reward_to_gcrl/results/0009_result.json",
      "research/reward_to_gcrl/results/0009_summary.md",
      "research/reward_to_gcrl/artifacts/0009/"
    ],
    "success_criteria": [
      "Use only CPU NumPy code on the already-audited tiny FourRooms environment; no PyTorch, JAX, GPU, larger environments, or large dependencies.",
      "Reuse or verify the 0008 FourRooms transition semantics, reward normalization, terminal masks, goal indexing, and exact tabular references for g_plus and real-state goals.",
      "Train a genuinely shared low-rank model, such as M_hat(s,a,g) = sigmoid(u_{s,a} dot v_g + b_g) or a documented bounded equivalent, so real-state goals and g_plus share state-action factors.",
      "Compare at minimum terminal-only g_plus training versus combined g_plus plus real-state auxiliary training on identical replay datasets, seeds, rank, optimizer step budget, target construction, and evaluation protocol.",
      "Use a small predeclared configuration only, for example rank 4, 10 seeds, one replay budget, and at most one auxiliary weight plus a terminal-only baseline.",
      "Report replay coverage, visited state-action coverage, goal-label coverage, and whether each seed meets an adequate-coverage threshold before interpreting learning metrics.",
      "Combined auxiliary training must improve mean g_plus value error or Bellman residual by at least 10 percent on adequate-coverage seeds, or improve one while being statistically indistinguishable on the other, without increasing tie-aware reward-policy disagreement.",
      "Real-state auxiliary goal predictions must be evaluated against exact references, including mean state-goal value error and a greedy goal-reaching diagnostic, but these are auxiliary diagnostics rather than reward-task success criteria.",
      "The summary must explicitly label the result as one of: auxiliary_helped_gplus, auxiliary_neutral, negative_transfer, coverage_limited, or optimizer_failed."
    ],
    "tasks_for_codex": [
      "Create research/reward_to_gcrl/artifacts/0009/run_fourrooms_lowrank_auxiliary.py using CPU-only NumPy.",
      "Write an environment audit that verifies the FourRooms transition table, state indexing, wall/door layout, action mapping, reward normalization, terminal masks, and goal indexing against 0008 where possible.",
      "Generate a fixed offline replay dataset from a simple non-oracle behavior policy or small mixture of documented non-oracle policies, and save replay coverage diagnostics.",
      "Implement exact target computation from replay for g_plus and sampled real-state goals, using exact tabular references only for evaluation, not for behavior or training targets beyond normal bootstrapped target construction.",
      "Implement terminal-only and combined auxiliary low-rank SSM variants with matched initialization seeds, optimizer steps, batch schedule, learning rate, rank, and target-network or fitted-iteration protocol.",
      "Evaluate g_plus scaled value error, Bellman residual, tie-aware reward-policy disagreement, raw reward-task return/success, real-state goal value error, greedy goal-reaching success, and negative-transfer diagnostics.",
      "Save research/reward_to_gcrl/results/0009_result.json with raw per-seed metrics, pass/fail flags, exact commands, model configuration, replay coverage, and conservative verdict.",
      "Save research/reward_to_gcrl/results/0009_summary.md with a short review-oriented interpretation and a recommendation on whether to repeat the low-rank checkpoint, move to a slightly larger sweep, or stop auxiliary-goal claims for now."
    ]
  },
  "rationale": "Continue to the first shared-parameter milestone, but keep it explicitly as a small checkpointed pilot rather than a publishable auxiliary-goal claim. The repository evidence now supports the core tabular estimator story: soft terminal marginalization preserves normalized-Q scaling, removes terminal-sampling variance, works in small nondegenerate chains, and has RiverSwim evidence under controlled and non-oracle coverage regimes. The latest 0008 result also validated vector SSM indexing on tiny FourRooms, including real-state goal slices that do not perturb g_plus. The next unresolved question is whether auxiliary real-state goals help when parameters are actually shared. A CPU-only NumPy low-rank factorized FourRooms experiment is the right next step.",
  "risks": [
    "A positive low-rank FourRooms result would be early shared-parameter evidence only, not a general GCRL or neural-function-approximation claim.",
    "Auxiliary state-goal losses may hurt the g_plus reward head through negative transfer, especially if the auxiliary weight is too high.",
    "Low-rank NumPy optimization can be sensitive to initialization, rank, target scaling, replay coverage, and step size; raw per-seed metrics must be saved.",
    "If the replay dataset is coverage-starved, a failure may reflect data coverage rather than auxiliary-goal interference.",
    "If too many hyperparameters are swept, the result will look like tuning rather than a clean first shared-parameter checkpoint.",
    "Moving to PyTorch, JAX, GPU, larger FourRooms variants, or publishable auxiliary-goal claims before review would overrun the evidence."
  ]
}
```


## Recent decision summaries

## 0008_decision.json

```json
{
  "confidence": 0.86,
  "decision": "continue",
  "evidence": [
    "research/reward_to_gcrl/results/0007_result.json is present and reports status completed with exact commands and declared artifacts.",
    "research/reward_to_gcrl/reviews/0007_review.json reports verdict pass, evidence_quality strong, allows_auto_continue true, success_criteria_satisfied true, and no triggered failure criteria.",
    "0007 used fixed non-oracle behavior policies, not exact-Q-guided action selection, and separated starved, borderline, and adequate coverage regimes.",
    "0007 reports sampled target means matching deterministic soft marginal targets in all 120 runs and sampled terminal-sampling variance exceeding soft variance in all 120 runs.",
    "In adequate-coverage RiverSwim runs, soft had lower mean Bellman residual and lower mean value error than sampled; starved runs were explicitly caveated as coverage-limited.",
    "The 0007 result recommends moving next to tabular auxiliary real-state goals, and the prototype plan's Milestone 3 is exactly a tabular vector SSM with goals S union {g_plus}.",
    "The charter still prohibits neural function approximation and larger expensive work before the tabular diagnostics are correct."
  ],
  "next_experiment": {
    "estimated_runtime_minutes": 25,
    "experiment_id": "0008",
    "hypothesis": "For a tabular vector SSM with independent goal slices, adding real-state goals should learn correct state-goal reachability maps while leaving the g_plus reward-success slice numerically equivalent to the terminal-only soft learner. Any degradation of the g_plus policy or value slice would indicate an implementation, indexing, reward-normalization, or terminal-mask bug rather than a research effect.",
    "objective": "Run a CPU-only tabular vector successor-measure sanity check with real-state goals plus g_plus on a tiny deterministic FourRooms grid.",
    "required_outputs": [
      "research/reward_to_gcrl/results/0008_result.json",
      "research/reward_to_gcrl/results/0008_summary.md",
      "research/reward_to_gcrl/artifacts/0008/ with script, environment audit, exact DP references, raw per-goal metrics, aggregate metrics, and reachability diagnostics"
    ]
  },
  "progress_score": 7,
  "rationale": "Experiment 0007 is a strong reviewed pass that resolves the non-oracle RiverSwim coverage caveat well enough to move to the next planned milestone. The next small, high-information step is not neural function approximation yet, but a tabular vector successor-measure sanity check with real-state goals. This tests whether auxiliary goal slices learn sensible reachability while the g_plus reward slice remains equivalent to terminal-only soft learning, which is the planned gate before any shared-representation claim.",
  "risks": [
    "A tabular vector SSM cannot prove auxiliary representation learning benefits, because goal slices do not share parameters; it should be treated only as a correctness and diagnostics gate.",
    "Reward-task improvement should not be expected or claimed in tabular mode; the key check is that adding state-goal slices does not perturb the g_plus slice.",
    "A tiny FourRooms implementation can encode walls, doorways, terminal masks, or goal indexing incorrectly unless the transition table and state-goal IDs are audited.",
    "Reachability diagnostics can become subjective if they are only visual; include exact DP value errors, greedy goal-reaching success rates, and shortest-path distance checks."
  ]
}
```

## 0009_decision.json

```json
{
  "confidence": 0.83,
  "decision": "continue",
  "evidence": [
    "research/reward_to_gcrl/results/0008_result.json is present, schema-valid, and reports status completed with exact commands and declared artifacts.",
    "research/reward_to_gcrl/reviews/0008_review.json reports verdict pass, evidence_quality strong, allows_auto_continue true, and no triggered failure criteria.",
    "0008 showed max_abs_vector_gplus_minus_terminal_only = 0 and max_abs_vector_gplus_scaled_minus_q_norm = 1.1102230246251565e-16.",
    "0008 real-state goal slices had max value error 0, min greedy goal success rate 1.0, and zero goal-policy disagreement versus exact references.",
    "The 0008 review correctly flags that this was an exact deterministic independent-slice sanity check, not sampled learning or function approximation.",
    "The prototype plan identifies the next milestone as low-capacity shared/factorized SSM, where auxiliary real-state goals can first provide a meaningful representation-learning signal."
  ],
  "next_experiment": {
    "estimated_runtime_minutes": 25,
    "experiment_id": "0009",
    "hypothesis": "With shared low-rank state-action and goal embeddings, real-state auxiliary goals should improve or at least not destabilize the reward-success g_plus head in low-data FourRooms. A useful signal would be lower g_plus Bellman/value error, lower policy disagreement, or higher reward-task success for combined training compared with terminal-only training at the same replay budget.",
    "objective": "Run the first CPU-only low-rank factorized SSM test on tiny FourRooms, comparing terminal-only g_plus training against combined real-state-plus-g_plus auxiliary training under limited offline replay.",
    "required_outputs": [
      "research/reward_to_gcrl/results/0009_result.json",
      "research/reward_to_gcrl/results/0009_summary.md",
      "research/reward_to_gcrl/artifacts/0009/ with script, environment audit, dataset coverage, exact references, raw per-seed metrics, aggregate metrics, and learning curves"
    ]
  },
  "progress_score": 7,
  "rationale": "Experiment 0008 is a strong reviewed pass for the tabular vector SSM implementation gate: real-state goal slices work and do not perturb the g_plus slice. The next planned milestone is the first shared-parameter test. Keep it small and CPU-only: a low-rank numpy factorized SSM on tiny FourRooms, comparing terminal-only g_plus training against combined real-state-plus-g_plus training under limited replay.",
  "risks": [
    "Low-rank results can be sensitive to optimizer, initialization, target scaling, and dataset coverage; raw per-seed metrics and failure modes must be saved.",
    "A positive result on tiny FourRooms would be only early shared-representation evidence, not a general GCRL claim.",
    "Auxiliary state goals can hurt the g_plus head if lambda_state is too high; negative transfer should be reported, not tuned away silently.",
    "Do not install large dependencies or move to PyTorch/JAX/GPU for this first factorized check; numpy is sufficient."
  ]
}
```

## 0009_pro_decision.json

```json
{
  "confidence": 0.86,
  "decision": "continue",
  "evidence": [
    "The latest summary reports no current blocker and protected_file_drift false.",
    "Reviewed evidence reaches 0008, with strong small-tabular support for the estimator story: deterministic soft terminal marginalization preserves normalized-Q scaling while removing terminal-sampling variance.",
    "0004 repaired the degenerate CliffWalking issue with a nondegenerate 5-state chain and showed soft improved Bellman/value error and policy success over sampled.",
    "0005 and 0006 extended the estimator story to 6-state RiverSwim, including non-oracle behavior streams, while exposing coverage as a key condition.",
    "0007 ran a RiverSwim coverage dose-response and found adequate-coverage runs favored soft on mean Bellman residual and value error, while starved runs remained coverage-limited.",
    "0008 passed the tabular vector SSM implementation gate: max_abs_vector_gplus_minus_terminal_only was 0, scaled vector g_plus matched normalized Q within 1.1102230246251565e-16, and real-state goal slices had zero value error and min greedy goal success rate 1.0.",
    "The 0008 review explicitly warns that independent tabular slices do not test sampled learning, low-rank coupling, or auxiliary representation benefit.",
    "The latest local decision 0009 recommends a CPU-only low-rank factorized SSM on tiny FourRooms comparing terminal-only g_plus training against combined real-state-plus-g_plus auxiliary training under limited offline replay."
  ],
  "next_experiment": {
    "estimated_runtime_minutes": 25,
    "experiment_id": "0009",
    "hypothesis": "If real-state auxiliary goals provide useful shared representation signal, then under a low-rank bottleneck and adequate replay coverage, combined auxiliary training should reduce g_plus value error and Bellman residual versus terminal-only g_plus training without increasing reward-policy disagreement. If it does not, then auxiliary-goal benefit is not yet supported and should not be claimed.",
    "objective": "Run the first CPU-only NumPy shared-parameter test on tiny FourRooms using a low-rank factorized soft successor-measure model, comparing terminal-only g_plus training against combined g_plus plus real-state auxiliary-goal training under matched limited offline replay.",
    "required_outputs": [
      "research/reward_to_gcrl/results/0009_result.json",
      "research/reward_to_gcrl/results/0009_summary.md",
      "research/reward_to_gcrl/artifacts/0009/"
    ]
  },
  "progress_score": null,
  "rationale": "Continue to the first shared-parameter milestone, but keep it explicitly as a small checkpointed pilot rather than a publishable auxiliary-goal claim. The repository evidence now supports the core tabular estimator story: soft terminal marginalization preserves normalized-Q scaling, removes terminal-sampling variance, works in small nondegenerate chains, and has RiverSwim evidence under controlled and non-oracle coverage regimes. The latest 0008 result also validated vector SSM indexing on tiny FourRooms, including real-state goal slices that do not perturb g_plus. The next unresolved question is whether auxiliary real-state goals help when parameters are actually shared. A CPU-only NumPy low-rank factorized FourRooms experiment is the right next step.",
  "risks": [
    "A positive low-rank FourRooms result would be early shared-parameter evidence only, not a general GCRL or neural-function-approximation claim.",
    "Auxiliary state-goal losses may hurt the g_plus reward head through negative transfer, especially if the auxiliary weight is too high.",
    "Low-rank NumPy optimization can be sensitive to initialization, rank, target scaling, replay coverage, and step size; raw per-seed metrics must be saved.",
    "If the replay dataset is coverage-starved, a failure may reflect data coverage rather than auxiliary-goal interference.",
    "If too many hyperparameters are swept, the result will look like tuning rather than a clean first shared-parameter checkpoint.",
    "Moving to PyTorch, JAX, GPU, larger FourRooms variants, or publishable auxiliary-goal claims before review would overrun the evidence."
  ]
}
```


## Recent review summaries

## 0007_review.json

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

## 0008_review.json

```json
{
  "allows_auto_continue": true,
  "escalation_reason": null,
  "evidence_checked": {
    "_type": "list",
    "first_items": [
      "research/reward_to_gcrl/results/0008_result.json",
      "research/reward_to_gcrl/results/0008_summary.md",
      "research/reward_to_gcrl/artifacts/0008/run_fourrooms_vector_ssm.py"
    ],
    "length": 12
  },
  "evidence_quality": "strong",
  "experiment_id": "0008",
  "failure_criteria_triggered": false,
  "reasons": {
    "_type": "list",
    "first_items": [
      "Required 0008 result JSON, summary markdown, and artifact directory are present.",
      "Result JSON validates against schemas/result.schema.json, and declared artifact paths validate successfully.",
      "Artifacts include the standalone FourRooms vector SSM script, environment audit, exact DP references, raw metrics, per-goal metrics, heatmap/arrow data, and progress log."
    ],
    "length": 9
  },
  "required_fixes": [],
  "risk_flags": [
    "This is an exact/full-sweep deterministic sanity check; it validates indexing and independent tabular slices, not learning under sampled data or function approximation.",
    "The result is expected to be nearly tautological because exact references and learned vector backups use the same audited transition semantics; this is acceptable for the predeclared implementation gate but should not be overgeneralized.",
    "Reward-policy comparison has many tie states, 17 of 40 with one skipped terminal state, although disagreement is zero on comparable non-tie states.",
    "Heatmap/arrow artifacts are saved for a selected subset of goals, while numerical per-goal metrics cover all goals.",
    "Current git status shows an untracked reviewer packet, but no protected path is currently modified."
  ],
  "should_escalate_to_pro": false,
  "success_criteria_satisfied": true,
  "verdict": "pass"
}
```

## 0009_review.json

```json
{
  "allows_auto_continue": true,
  "escalation_reason": null,
  "evidence_checked": {
    "_type": "list",
    "first_items": [
      "research/reward_to_gcrl/results/0009_result.json",
      "research/reward_to_gcrl/results/0009_summary.md",
      "research/reward_to_gcrl/artifacts/0009/run_fourrooms_lowrank_auxiliary.py"
    ],
    "length": 13
  },
  "evidence_quality": "strong",
  "experiment_id": "0009",
  "failure_criteria_triggered": false,
  "reasons": [
    "Required 0009 result JSON, summary markdown, and declared artifact files are present.",
    "Result JSON validates against schemas/result.schema.json, and declared artifact paths validate successfully.",
    "The script is CPU-only NumPy and uses the audited tiny FourRooms transition hash from 0008; no neural framework, GPU, larger environment, or large dependency is present.",
    "The combined model is genuinely shared and low-rank: M_hat(s,a,g)=sigmoid(u_sa dot v_g + b_g), with u_sa shared across real-state goals and g_plus.",
    "Terminal-only and combined variants use matched replay datasets, initialization seeds, batch schedules, optimizer steps, rank, learning rate, and evaluation protocol.",
    "Replay coverage is reported and adequate for all 10 seeds: visited state-action fraction is 1.0 and reward-event counts exceed the threshold.",
    "The experiment correctly reports a negative result rather than claiming auxiliary benefit: combined auxiliary training substantially worsened g_plus value error, Bellman residual, reward-policy disagreement, reward success, and real-goal diagnostics.",
    "The summary explicitly labels the outcome as negative_transfer and recommends stopping auxiliary-goal claims for now."
  ],
  "required_fixes": [],
  "risk_flags": [
    "The primary auxiliary-helped success criterion is not satisfied; this is valid negative evidence, not a positive auxiliary-goal result.",
    "The result is a single predeclared rank-4, learning-rate 0.05, 4000-step checkpoint, so it should not be generalized across optimizer settings or ranks.",
    "Both models have imperfect reward policies, and the combined model collapses badly; this may reflect optimizer or loss-scaling issues as much as a general auxiliary-goal limitation.",
    "Replay uses uniform random state-action resets, which gives strong coverage but is less realistic than trajectory-only offline data.",
    "Current git status shows an untracked reviewer packet, but no protected path is currently modified."
  ],
  "should_escalate_to_pro": false,
  "success_criteria_satisfied": false,
  "verdict": "weak_pass"
}
```


## Existing progress summaries

- `research/reward_to_gcrl/progress/0006_pre_pro_cadence_summary.md`
- `research/reward_to_gcrl/progress/0008_pre_pro_this_is_the_first_shared_parameter_function_approximation_milestone__keep_the_run_small__but_require_review_before_expanding_to_larger_sweeps__neural_frameworks__or_publishable_auxiliary_goal_claims_summary.md`
- `research/reward_to_gcrl/progress/latest_summary.md`


## Full evidence paths

- `research/reward_to_gcrl/plans/0001_plan.md`
- `research/reward_to_gcrl/plans/0002_plan.md`
- `research/reward_to_gcrl/plans/0003_plan.md`
- `research/reward_to_gcrl/plans/0004_plan.md`
- `research/reward_to_gcrl/plans/0005_plan.md`
- `research/reward_to_gcrl/plans/0006_plan.md`
- `research/reward_to_gcrl/plans/0007_plan.md`
- `research/reward_to_gcrl/plans/0008_plan.md`
- `research/reward_to_gcrl/plans/0009_plan.md`
- `research/reward_to_gcrl/results/0001_summary.md`
- `research/reward_to_gcrl/results/0002_summary.md`
- `research/reward_to_gcrl/results/0003_summary.md`
- `research/reward_to_gcrl/results/0004_summary.md`
- `research/reward_to_gcrl/results/0005_summary.md`
- `research/reward_to_gcrl/results/0006_summary.md`
- `research/reward_to_gcrl/results/0007_summary.md`
- `research/reward_to_gcrl/results/0008_summary.md`
- `research/reward_to_gcrl/results/0009_summary.md`
- `research/reward_to_gcrl/results/0001_result.json`
- `research/reward_to_gcrl/results/0002_result.json`
- `research/reward_to_gcrl/results/0003_result.json`
- `research/reward_to_gcrl/results/0004_result.json`
- `research/reward_to_gcrl/results/0005_result.json`
- `research/reward_to_gcrl/results/0006_result.json`
- `research/reward_to_gcrl/results/0007_result.json`
- `research/reward_to_gcrl/results/0008_result.json`
- `research/reward_to_gcrl/results/0009_result.json`
- `research/reward_to_gcrl/reviews/0001_review.md`
- `research/reward_to_gcrl/reviews/0002_review.md`
- `research/reward_to_gcrl/reviews/0003_review.md`
- `research/reward_to_gcrl/reviews/0004_review.md`
- `research/reward_to_gcrl/reviews/0005_review.md`
- `research/reward_to_gcrl/reviews/0006_review.md`
- `research/reward_to_gcrl/reviews/0007_review.md`
- `research/reward_to_gcrl/reviews/0008_review.md`
- `research/reward_to_gcrl/reviews/0009_review.md`
- `research/reward_to_gcrl/decisions/0001_decision.md`
- `research/reward_to_gcrl/decisions/0001_pro_decision.md`
- `research/reward_to_gcrl/decisions/0002_decision.md`
- `research/reward_to_gcrl/decisions/0002_review3_pro_decision.md`
- `research/reward_to_gcrl/decisions/0003_decision.md`
- `research/reward_to_gcrl/decisions/0004_decision.md`
- `research/reward_to_gcrl/decisions/0004_review2_pro_decision.md`
- `research/reward_to_gcrl/decisions/0004_review3_pro_decision.md`
- `research/reward_to_gcrl/decisions/0004_review4_pro_decision.md`
- `research/reward_to_gcrl/decisions/0004_review5_pro_decision.md`
- `research/reward_to_gcrl/decisions/0005_decision.md`
- `research/reward_to_gcrl/decisions/0006_decision.md`
- `research/reward_to_gcrl/decisions/0007_pro_decision.md`
- `research/reward_to_gcrl/decisions/0008_decision.md`
- `research/reward_to_gcrl/decisions/0009_decision.md`
- `research/reward_to_gcrl/decisions/0009_pro_decision.md`
