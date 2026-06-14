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
  "iteration": 6,
  "last_decision": "continue",
  "last_failure": null,
  "last_pro_review_iteration": 3,
  "last_pro_review_path": "research/reward_to_gcrl/decisions/0004_review5_pro_decision.json",
  "last_summary_iteration": 3,
  "last_summary_path": "research/reward_to_gcrl/progress/0003_pre_pro_review_fail_summary.md",
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
    "2026-06-14T21:18:53+00:00: cleared protected_file_drift after audit research/reward_to_gcrl/artifacts/0004/protected_file_drift_audit.json; status=harmless accepted_evidence"
  ],
  "pending_checkpoint": null,
  "pending_local_decision_path": null,
  "primary_metric": null,
  "pro_review_count": 6,
  "protected_file_drift": false,
  "status": "active",
  "weak_pass_streak": 0
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
  }
]
```


## Latest supervisor decision

```json
{
  "checkpoint_reason": null,
  "checkpoint_recommended": false,
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
    "failure_criteria": [
      "Missing or schema-invalid result JSON or summary markdown.",
      "Exact commands, behavior definitions, transition hash, reward normalization, or raw per-seed metrics are omitted.",
      "Any behavior policy uses exact Q or DP-derived action preferences for data generation.",
      "Sampled baseline double-discounts continued targets or bootstraps after sampled absorbing events.",
      "Claims estimator superiority on coverage-starved runs without coverage diagnostics.",
      "Adds auxiliary goals, neural approximation, larger environments, large downloads, or expensive training."
    ],
    "hypothesis": "With matched original transition streams generated by non-oracle exploration, sampled augmented g_plus updates remain unbiased but higher variance than deterministic soft updates. When coverage is adequate, soft should retain lower Bellman residual or value error; when coverage is poor, coverage should be identified as the limiting factor.",
    "objective": "Repeat the 6-state RiverSwim sampled-vs-soft diagnostic using non-oracle exploratory behavior streams.",
    "required_outputs": [
      "research/reward_to_gcrl/results/0006_result.json",
      "research/reward_to_gcrl/results/0006_summary.md",
      "research/reward_to_gcrl/artifacts/0006/ with script, audit, DP references, raw metrics, aggregate metrics, and learning curves"
    ],
    "success_criteria": [
      "Creates research/reward_to_gcrl/results/0006_result.json and research/reward_to_gcrl/results/0006_summary.md.",
      "Creates reproducible artifacts under research/reward_to_gcrl/artifacts/0006/.",
      "Uses only CPU tabular methods on the same 6-state RiverSwim semantics.",
      "Predeclares at least two non-oracle behavior policies, with no exact-Q-guided data generation.",
      "Runs gamma in {0.95, 0.99, 0.995} with at least 10 seeds per behavior policy within 30 minutes.",
      "Reports exact commands, transition hash, behavior definitions, reward normalization, seeds, budget, and sampled absorbing handling.",
      "Saves per-run coverage, right reward events, g_plus counts, sampled target mean error, target variance, Bellman residual, value error, policy disagreement, and greedy return.",
      "Separates adequately covered runs from coverage-starved runs using a predeclared threshold."
    ],
    "tasks_for_codex": [
      "Reuse or recreate the audited 6-state RiverSwim table and save a fresh environment audit.",
      "Implement matched-stream generation for non-oracle behavior policies.",
      "Compute exact DP references only for evaluation, not behavior generation.",
      "Train soft M_plus and sampled augmented g_plus learners on the same logged transitions for each behavior, gamma, and seed.",
      "Log learning curves, target statistics, g_plus counts, Bellman residuals, value errors, coverage diagnostics, and policy metrics.",
      "Save raw and aggregate metrics under research/reward_to_gcrl/artifacts/0006/.",
      "Validate result JSON and declared artifacts."
    ]
  },
  "progress_score": 6,
  "rationale": "0005 is a strong reviewed pass for the sampled-vs-soft claim in small stochastic RiverSwim, but it used exact-Q-guided behavior. The next small decisive test should hold the RiverSwim setup fixed and remove that oracle coverage source before moving to auxiliary goals or function approximation.",
  "risks": [
    "Non-oracle RiverSwim may have poor right-end coverage; coverage-starved failures should not be overinterpreted as estimator failure.",
    "Independent learner behavior would confound exploration with estimator variance, so use matched logged streams generated without exact-Q guidance.",
    "Do not move to neural approximation or auxiliary goals until this oracle-behavior caveat is bounded."
  ],
  "terminal_decision_requires_pro": false
}
```


## Recent decision summaries

## 0004_review5_pro_decision.json

```json
{
  "confidence": 0.88,
  "decision": "continue",
  "evidence": [
    "Accepted 0001 evidence supports the basic estimator-variance premise: sampled and soft targets matched means, soft terminal variance was zero or negligible, and rare g_plus events were exposed.",
    "Accepted 0002 evidence supports tabular scaling equivalence: exact DP scaling equivalence passed and learned scaled soft M matched normalized Q on sufficiently visited state-action pairs.",
    "Accepted 0003 evidence is useful but ambiguous: sampled variance exceeded soft terminal-sampling variance in all 30 runs and soft had lower Bellman residual in most runs, but value-error evidence was mixed and CliffWalking normalization made raw task success uninformative.",
    "Reviewed 0004 scientific metrics look stronger because the task is a nondegenerate 5-state chain with identity normalization, preserved raw and normalized exact-DP policies, passing target and variance checks, lower soft Bellman residual and value error, and nondegenerate evaluation where soft succeeds while sampled fails.",
    "0004 is not accepted evidence because the review verdict is fail, allows_auto_continue is false, no protected_file_drift_audit.json exists, no top-level or metrics-level drift_status exists, and state.json still reports protected_file_drift true.",
    "The 0004 review states that current git status may suggest the protected-file modification is stale, but this was not recorded in an audit artifact or result field.",
    "The review explicitly warns that proceeding to RiverSwim, auxiliary goals, neural approximation, or larger environments would violate the current evidence-integrity gate."
  ],
  "next_experiment": {
    "estimated_runtime_minutes": 15,
    "experiment_id": "0004",
    "hypothesis": "The 0004 scientific result is likely useful, but its evidential status depends on whether the protected-file drift is stale or harmless versus real or unresolved. A cheap audit should either accept the existing 0004 artifacts with explicit drift_status or trigger a clean CPU-only rerun of the same 5-state diagnostic.",
    "objective": "Resolve the protected_file_drift blocker and determine whether the existing 0004 nondegenerate 5-state sampled-vs-soft result can be accepted as evidence, superseded by a clean rerun, rejected due to drift, or marked inconclusive.",
    "required_outputs": [
      "research/reward_to_gcrl/results/0004_result.json",
      "research/reward_to_gcrl/results/0004_summary.md",
      "research/reward_to_gcrl/artifacts/0004/"
    ]
  },
  "progress_score": null,
  "rationale": "Continue, but only through an evidence-integrity gate before any new scientific claim or larger experiment. The project is making real progress: 0001-0003 provide accepted weak evidence for the variance motivation, tabular scaling equivalence, and reduced Bellman residuals, and 0004 appears scientifically promising on a nondegenerate 5-state chain. However, 0004 currently failed review because protected_file_drift remains unresolved, no drift audit was written, and no drift_status was recorded. Therefore 0004 cannot yet count as evidence, and proceeding to RiverSwim, auxiliary goals, or neural approximation would violate the current gate.",
  "risks": [
    "Treating 0004 as accepted before drift adjudication would contaminate the evidence chain.",
    "If protected_file_drift reflects a real change to autoresearcher.yaml or another protected file, 0004 may need a clean rerun before any conclusion is valid.",
    "If the drift is stale but not documented, the loop may keep failing review for procedural rather than scientific reasons.",
    "Even if 0004 is accepted, it remains a tiny 5-state matched-stream result and does not establish generality to RiverSwim, larger grids, auxiliary goals, or function approximation.",
    "Starting a new RL experiment now would reward activity over evidence and could compound unresolved procedural uncertainty."
  ]
}
```

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


## Recent review summaries

## 0004_review.json

```json
{
  "allows_auto_continue": true,
  "escalation_reason": null,
  "evidence_checked": [
    "research/reward_to_gcrl/results/0004_result.json",
    "research/reward_to_gcrl/results/0004_summary.md",
    "research/reward_to_gcrl/artifacts/0004/protected_file_drift_audit.json",
    "research/reward_to_gcrl/state.json",
    "Schema validation of 0004_result.json",
    "Artifact validation via scripts/validate_artifacts.py",
    "Scoped git status for protected paths and reward_to_gcrl files"
  ],
  "evidence_quality": "medium",
  "experiment_id": "0004",
  "failure_criteria_triggered": false,
  "reasons": [
    "Required 0004 result JSON, summary markdown, and declared artifact files are present.",
    "Result JSON validates against schemas/result.schema.json, and declared artifact paths validate successfully.",
    "The drift audit identifies autoresearcher.yaml as the only protected file flagged by the guard, records it as clean at HEAD, includes a SHA-256 hash, and assesses the prior change as harmless for experiment logic, reporting, validation, seeds, metrics, and transition semantics.",
    "research/reward_to_gcrl/state.json now reports protected_file_drift as false with a note clearing the drift after the audit.",
    "0004 records drift_status=harmless and evidence_integrity_verdict=accepted_evidence under metrics, with post-audit schema and artifact validation marked passed.",
    "Scientific evidence remains relevant and complete: direct sampled-vs-deterministic-soft target comparison, sampled variance exceeding soft variance in all runs, lower soft Bellman/value error, and nondegenerate policy evaluation metrics."
  ],
  "required_fixes": [],
  "risk_flags": [
    "The latest plan text inconsistently references 0005 audit/result paths, while required outputs and actual evidence use 0004 paths.",
    "drift_status and evidence_integrity_verdict are under metrics rather than top-level result fields.",
    "The accepted learning-improvement evidence is still from a tiny 5-state chain with controlled matched streams; broader environments remain untested.",
    "Current git status shows a modified reviewer packet, but no protected path is currently modified."
  ],
  "should_escalate_to_pro": false,
  "success_criteria_satisfied": true,
  "verdict": "weak_pass"
}
```

## 0005_review.json

```json
{
  "allows_auto_continue": true,
  "escalation_reason": null,
  "evidence_checked": {
    "_type": "list",
    "first_items": [
      "research/reward_to_gcrl/results/0005_result.json",
      "research/reward_to_gcrl/results/0005_summary.md",
      "research/reward_to_gcrl/artifacts/0005/environment_audit.json"
    ],
    "length": 10
  },
  "evidence_quality": "strong",
  "experiment_id": "0005",
  "failure_criteria_triggered": false,
  "reasons": [
    "Required 0005 result JSON, summary markdown, and artifact directory are present.",
    "Result JSON validates against schemas/result.schema.json, and declared artifact paths validate successfully.",
    "The artifact set includes the RiverSwim script, environment audit, exact DP references, per-seed metrics, learning curves, raw metrics, and progress log.",
    "Environment audit records a 6-state stochastic continuing RiverSwim transition table, rewards already normalized to [0,1], terminal/absorbing handling, action mapping, and a transition-table hash.",
    "Exact DP references report scaled soft fixed-point agreement with normalized Q for all requested gammas, with max error below 1e-6.",
    "The run covers gamma values 0.95, 0.99, and 0.995 over 10 seeds with 200000 transitions per run and CPU tabular numpy code only.",
    "Per-seed metrics include g_plus counts, target mean errors and tolerances, sampled and soft target variance diagnostics, Bellman residuals, value errors, coverage/right-end reward diagnostics, greedy-policy returns, and policy disagreement.",
    "Sampled target means match the deterministic soft marginal target in all 30 runs, sampled terminal-sampling variance exceeds soft variance in all 30 runs, and soft residual dominance is reported in all 30 runs."
  ],
  "required_fixes": [],
  "risk_flags": [
    "The behavior policy is epsilon-greedy with respect to the exact normalized-Q greedy action, so the result is a controlled matched-stream propagation test rather than an online exploration test.",
    "Right-end coverage is strong under the oracle-guided behavior stream; conclusions about sparse-reward exploration failures should be tested separately with a non-oracle exploratory behavior policy.",
    "Greedy-policy return is not uniformly better for the soft learner per seed: soft has higher mean return overall, but is strictly higher than sampled in only 14 of 30 runs and has a few low-return learned policies.",
    "The experiment remains small-scale at 6 states; larger RiverSwim chains or auxiliary-goal settings remain untested."
  ],
  "should_escalate_to_pro": false,
  "success_criteria_satisfied": true,
  "verdict": "pass"
}
```

## 0006_review.json

```json
{
  "allows_auto_continue": true,
  "escalation_reason": null,
  "evidence_checked": {
    "_type": "list",
    "first_items": [
      "research/reward_to_gcrl/results/0006_result.json",
      "research/reward_to_gcrl/results/0006_summary.md",
      "research/reward_to_gcrl/artifacts/0006/run_riverswim_nonoracle.py"
    ],
    "length": 10
  },
  "evidence_quality": "strong",
  "experiment_id": "0006",
  "failure_criteria_triggered": false,
  "reasons": {
    "_type": "list",
    "first_items": [
      "Required 0006 result JSON, summary markdown, and artifact directory are present.",
      "Result JSON validates against schemas/result.schema.json, and declared artifact paths validate successfully.",
      "The artifact set includes the non-oracle RiverSwim script, environment audit, exact DP references, per-seed metrics, learning curves, raw metrics, and progress log."
    ],
    "length": 9
  },
  "required_fixes": [],
  "risk_flags": [
    "Half of the runs are coverage-starved under the predeclared threshold, so learning-performance conclusions should be restricted to the adequate-coverage subset or explicitly labeled as coverage-limited.",
    "In coverage-starved uniform-random runs, soft has lower Bellman residual but worse mean value error than sampled in most runs, so value-error superiority is not uniform under poor coverage.",
    "The behavior policies are simple state-independent random policies; additional non-oracle exploration policies may be needed before broader claims.",
    "Current git status shows an untracked reviewer packet, but no protected path is currently modified."
  ],
  "should_escalate_to_pro": false,
  "success_criteria_satisfied": true,
  "verdict": "pass"
}
```


## Existing progress summaries

- `research/reward_to_gcrl/progress/0003_pre_pro_review_needs_human_summary.md`
- `research/reward_to_gcrl/progress/0003_pre_pro_weak_pass_streak_summary.md`
- `research/reward_to_gcrl/progress/latest_summary.md`


## Full evidence paths

- `research/reward_to_gcrl/plans/0001_plan.md`
- `research/reward_to_gcrl/plans/0002_plan.md`
- `research/reward_to_gcrl/plans/0003_plan.md`
- `research/reward_to_gcrl/plans/0004_plan.md`
- `research/reward_to_gcrl/plans/0005_plan.md`
- `research/reward_to_gcrl/plans/0006_plan.md`
- `research/reward_to_gcrl/results/0001_summary.md`
- `research/reward_to_gcrl/results/0002_summary.md`
- `research/reward_to_gcrl/results/0003_summary.md`
- `research/reward_to_gcrl/results/0004_summary.md`
- `research/reward_to_gcrl/results/0005_summary.md`
- `research/reward_to_gcrl/results/0006_summary.md`
- `research/reward_to_gcrl/results/0001_result.json`
- `research/reward_to_gcrl/results/0002_result.json`
- `research/reward_to_gcrl/results/0003_result.json`
- `research/reward_to_gcrl/results/0004_result.json`
- `research/reward_to_gcrl/results/0005_result.json`
- `research/reward_to_gcrl/results/0006_result.json`
- `research/reward_to_gcrl/reviews/0001_review.md`
- `research/reward_to_gcrl/reviews/0002_review.md`
- `research/reward_to_gcrl/reviews/0003_review.md`
- `research/reward_to_gcrl/reviews/0004_review.md`
- `research/reward_to_gcrl/reviews/0005_review.md`
- `research/reward_to_gcrl/reviews/0006_review.md`
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
