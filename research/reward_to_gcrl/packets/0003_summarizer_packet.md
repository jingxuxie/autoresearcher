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
  "iteration": 3,
  "last_decision": "protected_file_drift",
  "last_failure": null,
  "last_pro_review_iteration": 3,
  "last_pro_review_path": "research/reward_to_gcrl/decisions/0004_review2_pro_decision.json",
  "last_summary_iteration": 3,
  "last_summary_path": "research/reward_to_gcrl/progress/0003_pre_pro_local_needs_human_summary.md",
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
    "2026-06-14T20:52:46+00:00: applied Pro decision pivot from research/reward_to_gcrl/decisions/0004_review2_pro_decision.json"
  ],
  "pending_checkpoint": null,
  "pending_local_decision_path": null,
  "primary_metric": null,
  "pro_review_count": 3,
  "protected_file_drift": true,
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
  }
]
```


## Latest supervisor decision

```json
{
  "confidence": 0.83,
  "decision": "pivot",
  "evidence": [
    "0001 weak-passed: sampled and soft terminal targets matched expected means, soft removed terminal-sampling variance, and rare g_plus events were exposed.",
    "0002 weak-passed: an audited local deterministic CliffWalking table was used, exact DP scaling equivalence passed, and learned scaled M matched normalized Q on sufficiently visited pairs.",
    "0003 weak-passed structurally: sampled conditional variance exceeded zero soft terminal-sampling variance in all 30 CPU-tabular runs, and soft had lower final Bellman residual in 26 of 30 runs.",
    "The strongest 0003 learning-performance claim is mixed: mean final soft value error was slightly worse than sampled value error, soft value-error dominance was only 17 of 30 runs, and only 4 of 10 seeds at gamma 0.995.",
    "The current CliffWalking normalization made raw task success uninformative: policies in 0002 and 0003 had raw return -200 and success rate 0.0.",
    "0003 target-mean validation compared sampled targets to the sampled learner's conditional expectation rather than directly to the deterministic soft learner's recorded target, and sampled-vs-soft deterministic target means exceeded tolerance in 19 of 30 runs.",
    "The latest local decision is needs_human because continuing automatically risks compounding overclaims from ambiguous 0003 evidence."
  ],
  "next_experiment": {
    "estimated_runtime_minutes": 25,
    "experiment_id": "0004",
    "failure_criteria": [
      "The normalized objective does not preserve the raw optimal policy and the experiment does not explicitly label this as an objective-mismatch result.",
      "The target comparison again validates sampled targets only against the sampled learner's own conditional expectation rather than the deterministic soft target from the same state.",
      "Exact DP has mostly tie states, making policy disagreement uninformative.",
      "Raw task success remains zero or uninformative for all learned policies.",
      "Soft has worse mean final value error and no compensating Bellman-residual or policy-quality advantage.",
      "The run adds neural networks, auxiliary goals, large environments, GPU dependence, or expensive hyperparameter sweeps."
    ],
    "hypothesis": "When reward normalization is audited so that the induced normalized objective does not create degenerate all-step rewards, the sampled augmented update remains unbiased but higher variance, while the deterministic soft update should achieve lower Bellman residual and at least non-worse value error and greedy policy quality under the same transition budget.",
    "objective": "Repair the sampled-vs-soft comparison using a small nondegenerate tabular setting where the raw task objective remains meaningful, and directly test whether deterministic soft terminal marginalization improves Bellman residual, value error, and policy quality over sampled augmented updates under matched data.",
    "required_outputs": [
      "research/reward_to_gcrl/results/0004_result.json",
      "research/reward_to_gcrl/results/0004_summary.md",
      "research/reward_to_gcrl/artifacts/0004/"
    ],
    "success_criteria": [
      "Include an explicit reward audit reporting raw rewards, normalized rewards, affine constants, terminal handling, and whether the normalized objective preserves the raw optimal policy under exact DP.",
      "Use at least one tiny analytic counterexample or hand-built chain where raw task success is nondegenerate and exact DP has non-tie greedy actions.",
      "Compute exact DP for raw Q, normalized Q, and soft g_plus, and report whether normalized Q and raw Q have the same greedy policy on non-terminal non-tie states.",
      "Run matched-stream sampled augmented and deterministic soft updates for gamma in {0.95, 0.99, 0.995} over 10 seeds with CPU-tabular code only.",
      "Compare sampled targets directly against the deterministic soft target computed from the same learner state and transition, with pass/fail tolerance stated before the run.",
      "Soft must have lower mean final Bellman residual and lower or statistically indistinguishable mean final value error versus sampled across seeds; otherwise the result should be labeled variance-only, not learning-improvement evidence.",
      "Evaluation must report raw return, normalized return, success rate, steps to goal, and policy disagreement against exact DP, with tie states separated."
    ],
    "tasks_for_codex": [
      "Create research/reward_to_gcrl/artifacts/0004/run_repaired_sampled_vs_soft.py using CPU-only tabular code.",
      "Implement a small nondegenerate chain or gridworld with audited raw rewards, normalized rewards, terminal states, and exact transition table.",
      "Optionally include a repaired CliffWalking variant only if exact DP confirms the normalized objective has meaningful non-tie policies and nonzero success incentives.",
      "Compute exact DP references for raw Q, normalized Q, and soft g_plus, including policy preservation checks.",
      "Run matched-stream sampled augmented and deterministic soft learners with synchronized initialization, alpha, epsilon schedule, transition budget, gamma values, and seeds.",
      "For every sampled update, record the deterministic soft target from the same learner state and transition so sampled-vs-soft target mean and variance are directly comparable.",
      "Save raw metrics, target diagnostics, Bellman residuals, value errors, policy disagreement, evaluation returns, and pass/fail flags to research/reward_to_gcrl/results/0004_result.json.",
      "Write research/reward_to_gcrl/results/0004_summary.md with a conservative verdict: variance-only, learning-improvement, objective-mismatch, or failed diagnostic."
    ]
  },
  "rationale": "Pivot within the same research direction rather than stop. The project has made real but limited progress: 0001-0003 support the variance motivation and tabular scaling equivalence, but the current CliffWalking setup is scientifically too degenerate to justify moving to auxiliary goals or neural models. The main new evidence is not that soft successor learning is clearly better, but that naive normalized reward-to-goal conversion can preserve a scaled normalized objective while destroying useful raw-task incentives. The next experiment should repair this ambiguity by using a nondegenerate reward/task setting and directly comparing sampled targets to the deterministic soft target, not by continuing to collect weak CliffWalking evidence under the same normalization.",
  "risks": [
    "A repaired experiment may show that soft terminal marginalization mainly reduces estimator variance but does not improve learned value error under tabular control.",
    "Changing the reward normalization could accidentally change the task again unless raw reward, normalized reward, and affine constants are explicitly audited.",
    "Direct sampled-vs-soft target comparisons require matched state-action-next-state streams and synchronized learner states; otherwise differences may reflect policy/data drift rather than estimator variance.",
    "If the experiment uses only CliffWalking again, policy ties and episodic-duration effects may remain confusing.",
    "Moving to RiverSwim, auxiliary goals, or neural function approximation before resolving this ambiguity would make later failures hard to interpret."
  ]
}
```


## Recent decision summaries

## 0003_decision.json

```json
{
  "confidence": 0.82,
  "decision": "continue",
  "evidence": [
    "research/reward_to_gcrl/results/0002_result.json exists, validates, and reports status completed with exact commands and declared artifacts.",
    "The 0002 review reports allows_auto_continue=true, success_criteria_satisfied=true, and no triggered failure criteria.",
    "Exact DP in 0002 passed the scaling check with max_abs_error_scaled_f_vs_q = 9.711982329463353e-10, below the 1e-6 tolerance.",
    "Paired learning in 0002 produced 20 runs across 2 gammas and 10 seeds, with learned scaled M and normalized Q agreeing within 5.115907697472721e-13 on sufficiently visited state-action pairs.",
    "The major 0002 caveat is scientific rather than structural: the declared reward normalization makes raw CliffWalking success 0 and creates many policy ties, so raw success is not positive evidence.",
    "The prototype plan's next gate after tabular equivalence is sampled augmented versus soft terminal update, with metrics for TD target variance, g_plus event count, and Bellman error."
  ],
  "next_experiment": {
    "estimated_runtime_minutes": 25,
    "experiment_id": "0003",
    "hypothesis": "For the same original transition stream, the sampled augmented g_plus learner is an unbiased but higher-variance estimator of the soft target, so it should observe sparse g_plus events and have higher TD target variance and worse or slower Bellman-error reduction than the deterministic soft update as gamma approaches 1.",
    "objective": "Compare sampled augmented g_plus learning against the terminal-only soft successor update on the audited local tabular CliffWalking MDP under the same data budget.",
    "required_outputs": [
      "research/reward_to_gcrl/results/0003_result.json",
      "research/reward_to_gcrl/results/0003_summary.md",
      "research/reward_to_gcrl/artifacts/0003/ with diagnostic script, raw per-seed metrics, aggregate metrics, metadata, and DP references"
    ]
  },
  "progress_score": 4,
  "rationale": "The latest accepted result is a weak but valid pass for the tabular equivalence gate: exact soft g_plus values matched normalized Q-learning after scaling, and the reviewer allowed auto-continue. The next small, decisive gate is Milestone 2: compare the sampled augmented g_plus learner against the deterministic soft terminal update under the same tabular data budget, focusing on target variance, g_plus event counts, and Bellman error rather than raw CliffWalking success.",
  "risks": [
    "The 0002 normalization makes raw goal-reaching performance uninformative; 0003 must treat raw return and success rate as diagnostics, not as the primary pass criterion.",
    "A sampled augmented baseline can be implemented incorrectly by double-discounting continued transitions; the expected sampled target must match (1 - gamma) * r_bar + gamma * max M_next.",
    "Policy metrics may remain tie-heavy in CliffWalking, so Bellman error and target-variance metrics should carry more weight than greedy disagreement alone.",
    "The artifact directory should be clean for 0003 and should not inherit stale timeout or compatibility files from earlier 0002 attempts."
  ]
}
```

## 0004_decision.json

```json
{
  "confidence": 0.91,
  "decision": "needs_human",
  "evidence": {
    "_type": "list",
    "first_items": [
      "0003_result.json reports status completed with commands, artifacts, raw per-seed metrics, and CPU-only tabular scope.",
      "0003_review.json allows auto-continue and reports no triggered failure criteria, but grades evidence quality as medium with verdict weak_pass.",
      "The strongest positive result is estimator variance: sampled conditional variance exceeds zero soft terminal-sampling variance in all 30 runs."
    ],
    "length": 9
  },
  "next_experiment": null,
  "progress_score": 4,
  "rationale": "Do not auto-continue to a new experiment yet. Iteration 0003 is structurally valid but only a weak pass, and its main scientific interpretation is ambiguous: the sampled-vs-soft advantage is not consistently supported by value error, the target-mean check is not against the recorded deterministic soft learner target, and the CliffWalking normalization makes policy success uninformative.",
  "risks": [
    "Continuing automatically could compound an overclaim from 0003 into later experiments.",
    "Moving to auxiliary goals or function approximation now would be premature.",
    "Repeating CliffWalking without fixing reward normalization may keep producing degenerate policies and tie-heavy comparisons.",
    "A RiverSwim experiment may be the right next step, but choosing it now is a scope decision after ambiguous evidence."
  ]
}
```

## 0004_review2_pro_decision.json

```json
{
  "confidence": 0.83,
  "decision": "pivot",
  "evidence": [
    "0001 weak-passed: sampled and soft terminal targets matched expected means, soft removed terminal-sampling variance, and rare g_plus events were exposed.",
    "0002 weak-passed: an audited local deterministic CliffWalking table was used, exact DP scaling equivalence passed, and learned scaled M matched normalized Q on sufficiently visited pairs.",
    "0003 weak-passed structurally: sampled conditional variance exceeded zero soft terminal-sampling variance in all 30 CPU-tabular runs, and soft had lower final Bellman residual in 26 of 30 runs.",
    "The strongest 0003 learning-performance claim is mixed: mean final soft value error was slightly worse than sampled value error, soft value-error dominance was only 17 of 30 runs, and only 4 of 10 seeds at gamma 0.995.",
    "The current CliffWalking normalization made raw task success uninformative: policies in 0002 and 0003 had raw return -200 and success rate 0.0.",
    "0003 target-mean validation compared sampled targets to the sampled learner's conditional expectation rather than directly to the deterministic soft learner's recorded target, and sampled-vs-soft deterministic target means exceeded tolerance in 19 of 30 runs.",
    "The latest local decision is needs_human because continuing automatically risks compounding overclaims from ambiguous 0003 evidence."
  ],
  "next_experiment": {
    "estimated_runtime_minutes": 25,
    "experiment_id": "0004",
    "hypothesis": "When reward normalization is audited so that the induced normalized objective does not create degenerate all-step rewards, the sampled augmented update remains unbiased but higher variance, while the deterministic soft update should achieve lower Bellman residual and at least non-worse value error and greedy policy quality under the same transition budget.",
    "objective": "Repair the sampled-vs-soft comparison using a small nondegenerate tabular setting where the raw task objective remains meaningful, and directly test whether deterministic soft terminal marginalization improves Bellman residual, value error, and policy quality over sampled augmented updates under matched data.",
    "required_outputs": [
      "research/reward_to_gcrl/results/0004_result.json",
      "research/reward_to_gcrl/results/0004_summary.md",
      "research/reward_to_gcrl/artifacts/0004/"
    ]
  },
  "progress_score": null,
  "rationale": "Pivot within the same research direction rather than stop. The project has made real but limited progress: 0001-0003 support the variance motivation and tabular scaling equivalence, but the current CliffWalking setup is scientifically too degenerate to justify moving to auxiliary goals or neural models. The main new evidence is not that soft successor learning is clearly better, but that naive normalized reward-to-goal conversion can preserve a scaled normalized objective while destroying useful raw-task incentives. The next experiment should repair this ambiguity by using a nondegenerate reward/task setting and directly comparing sampled targets to the deterministic soft target, not by continuing to collect weak CliffWalking evidence under the same normalization.",
  "risks": [
    "A repaired experiment may show that soft terminal marginalization mainly reduces estimator variance but does not improve learned value error under tabular control.",
    "Changing the reward normalization could accidentally change the task again unless raw reward, normalized reward, and affine constants are explicitly audited.",
    "Direct sampled-vs-soft target comparisons require matched state-action-next-state streams and synchronized learner states; otherwise differences may reflect policy/data drift rather than estimator variance.",
    "If the experiment uses only CliffWalking again, policy ties and episodic-duration effects may remain confusing.",
    "Moving to RiverSwim, auxiliary goals, or neural function approximation before resolving this ambiguity would make later failures hard to interpret."
  ]
}
```


## Recent review summaries

## 0001_review.json

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

## 0002_review.json

```json
{
  "allows_auto_continue": true,
  "escalation_reason": null,
  "evidence_checked": {
    "_type": "list",
    "first_items": [
      "research/reward_to_gcrl/results/0002_result.json",
      "research/reward_to_gcrl/results/0002_summary.md",
      "research/reward_to_gcrl/artifacts/0002/run_local_cliffwalking_equivalence.py"
    ],
    "length": 13
  },
  "evidence_quality": "medium",
  "experiment_id": "0002",
  "failure_criteria_triggered": false,
  "reasons": [
    "Required result JSON, summary markdown, and declared artifact directory/files are present.",
    "Result JSON validates against schemas/result.schema.json, and declared artifact paths validate successfully.",
    "The local environment audit is complete, records the requested CliffWalking semantics, uses no Gymnasium environment dependency, has 192 transition records, and the saved transition hash recomputes correctly.",
    "Exact DP covers gamma values 0.95 and 0.99 and passes the scaling check with max_abs_error_scaled_f_vs_q 9.711982329463353e-10, below 1e-6.",
    "Paired learning produced 20 runs across 2 gammas and 10 seeds; learned scaled M and normalized Q agree within 5.115907697472721e-13 on sufficiently visited state-action pairs.",
    "Evaluation metrics over 100 episodes per seed are present for both policies and include raw return, normalized return, steps, cliff falls, and success rate.",
    "The report does not hide poor raw CliffWalking performance: both policies have mean raw return -200 and success rate 0 under the declared normalization."
  ],
  "required_fixes": [],
  "risk_flags": [
    "The declared normalization maps ordinary step and goal rewards to 1 and cliff falls to 0, causing the learned/evaluated greedy policies to never reach the goal; this is acceptable for the equivalence gate but makes raw CliffWalking task success invalid as positive evidence.",
    "Policy-disagreement evidence is weak because exact DP has 37 tie states and 0 comparable non-tie states; paired learning also has many tie states and few comparable states in several seeds.",
    "The paired learned-value comparison is nearly algebraic because both learners use identical transitions, initialization, alpha, and targets that differ only by the (1-gamma) scale.",
    "Learned Bellman residuals are large in some paired runs, up to about 100, so this does not demonstrate convergence to the exact DP solution.",
    "The artifact directory still contains stale timeout and compatibility files from earlier 0002 attempts, although the final result correctly declares the nine relevant artifacts."
  ],
  "should_escalate_to_pro": false,
  "success_criteria_satisfied": true,
  "verdict": "weak_pass"
}
```

## 0003_review.json

```json
{
  "allows_auto_continue": true,
  "escalation_reason": null,
  "evidence_checked": {
    "_type": "list",
    "first_items": [
      "research/reward_to_gcrl/results/0003_result.json",
      "research/reward_to_gcrl/results/0003_summary.md",
      "research/reward_to_gcrl/artifacts/0003/run_sampled_vs_soft_cliffwalking.py"
    ],
    "length": 14
  },
  "evidence_quality": "medium",
  "experiment_id": "0003",
  "failure_criteria_triggered": false,
  "reasons": [
    "Required 0003 result JSON, summary markdown, and declared artifact files are present.",
    "Result JSON validates against schemas/result.schema.json, and declared artifact paths validate successfully.",
    "The 0003 environment audit is complete, recomputes to the saved transition hash, and matches the audited 0002 transition table hash.",
    "The run is CPU-only tabular work on the local CliffWalking table with gammas 0.95, 0.99, and 0.995, 10 seeds each, and a 200000-transition budget per run.",
    "Per-seed raw metrics and checkpoint learning curves are present and include g_plus counts, events per 10000 transitions, target variance statistics, Bellman/value error to exact soft DP, policy diagnostics, returns, success rate, and cliff falls.",
    "The sampled augmented update implementation uses g_plus -> 1, g_minus -> 0, and continue -> max_a M(s_next,a) with no extra gamma factor; sampled absorbing events do not bootstrap.",
    "The sampled target mean matches its conditional expected sampled target within the declared Monte Carlo tolerance in all 30 runs, and sampled conditional variance exceeds zero soft terminal-sampling variance in all 30 runs.",
    "Soft has lower final Bellman residual in 26 of 30 runs, although the reported value-error dominance evidence is much weaker."
  ],
  "required_fixes": [],
  "risk_flags": [
    "The target-mean pass compares sampled targets to the sampled learner's conditional expected target, not to the deterministic soft learner's recorded target; sampled-vs-soft-deterministic target means exceed the recorded Monte Carlo tolerance in 19 of 30 runs.",
    "The summary claims lower/faster value-error dominance, but mean final soft value error is slightly worse overall than sampled value error, and soft value-error dominance is only 17 of 30 runs.",
    "At gamma 0.995, soft value-error dominance is only 4 of 10 seeds, so the value-error evidence does not strengthen as gamma approaches 1.",
    "The stronger dominance evidence is Bellman residual, where soft is lower in 26 of 30 runs; this should be preferred over the weaker value-error wording.",
    "All evaluated policies have raw return -200 and success rate 0 because the chosen normalization rewards continuing steps, so raw CliffWalking performance is diagnostic only and not positive task-performance evidence.",
    "The matched transition stream is generated by the soft learner's behavior policy, so the comparison is fair for fixed-stream estimator variance but not a deployment comparison between independently acting learners.",
    "The exact soft DP values are nearly degenerate under this normalization, so policy diagnostics and raw-return conclusions remain weak."
  ],
  "should_escalate_to_pro": false,
  "success_criteria_satisfied": true,
  "verdict": "weak_pass"
}
```


## Existing progress summaries

- `research/reward_to_gcrl/progress/0003_pre_pro_local_needs_human_summary.md`
- `research/reward_to_gcrl/progress/0003_pre_pro_weak_pass_streak_summary.md`
- `research/reward_to_gcrl/progress/latest_summary.md`


## Full evidence paths

- `research/reward_to_gcrl/plans/0001_plan.md`
- `research/reward_to_gcrl/plans/0002_plan.md`
- `research/reward_to_gcrl/plans/0003_plan.md`
- `research/reward_to_gcrl/plans/0004_plan.md`
- `research/reward_to_gcrl/results/0001_summary.md`
- `research/reward_to_gcrl/results/0002_summary.md`
- `research/reward_to_gcrl/results/0003_summary.md`
- `research/reward_to_gcrl/results/0004_summary.md`
- `research/reward_to_gcrl/results/0001_result.json`
- `research/reward_to_gcrl/results/0002_result.json`
- `research/reward_to_gcrl/results/0003_result.json`
- `research/reward_to_gcrl/results/0004_result.json`
- `research/reward_to_gcrl/reviews/0001_review.md`
- `research/reward_to_gcrl/reviews/0002_review.md`
- `research/reward_to_gcrl/reviews/0003_review.md`
- `research/reward_to_gcrl/decisions/0001_decision.md`
- `research/reward_to_gcrl/decisions/0001_pro_decision.md`
- `research/reward_to_gcrl/decisions/0002_decision.md`
- `research/reward_to_gcrl/decisions/0002_review3_pro_decision.md`
- `research/reward_to_gcrl/decisions/0003_decision.md`
- `research/reward_to_gcrl/decisions/0004_decision.md`
- `research/reward_to_gcrl/decisions/0004_review2_pro_decision.md`
