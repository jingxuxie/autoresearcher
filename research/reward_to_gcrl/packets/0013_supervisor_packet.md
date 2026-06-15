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
  "iteration": 12,
  "last_decision": "continue",
  "last_failure": null,
  "last_pro_review_iteration": 11,
  "last_pro_review_path": "research/reward_to_gcrl/decisions/0012_pro_decision.json",
  "last_summary_iteration": 11,
  "last_summary_path": "research/reward_to_gcrl/progress/0011_pre_pro_local_pivot_summary.md",
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
    "2026-06-14T22:55:17+00:00: applied Pro decision continue from research/reward_to_gcrl/decisions/0009_pro_decision.json",
    "2026-06-14T23:22:26+00:00: Pro decision saved for checkpoint This is the first shared-parameter function-approximation milestone. Keep the run small, but require review before expanding to larger sweeps, neural frameworks, or publishable auxiliary-goal claims. (research/reward_to_gcrl/decisions/0010_pro_decision.json)",
    "2026-06-14T23:22:27+00:00: applied Pro decision pivot from research/reward_to_gcrl/decisions/0010_pro_decision.json",
    "2026-06-14T23:41:56+00:00: Pro decision saved for checkpoint local_pivot (research/reward_to_gcrl/decisions/0011_pro_decision.json)",
    "2026-06-14T23:41:57+00:00: applied Pro decision pivot from research/reward_to_gcrl/decisions/0011_pro_decision.json",
    "2026-06-14T23:56:35+00:00: Pro decision saved for checkpoint local_pivot (research/reward_to_gcrl/decisions/0012_pro_decision.json)",
    "2026-06-14T23:56:37+00:00: applied Pro decision pivot from research/reward_to_gcrl/decisions/0012_pro_decision.json"
  ],
  "pending_checkpoint": null,
  "pending_local_decision_path": null,
  "primary_metric": null,
  "pro_review_count": 11,
  "protected_file_drift": false,
  "status": "active",
  "weak_pass_streak": 0
}
```


## Latest result summary

```json
{
  "_source": "/home/eston/autoresearcher/research/reward_to_gcrl/results/0012_result.json",
  "artifacts": [
    "research/reward_to_gcrl/reports/0012_writeup_outline.md",
    "research/reward_to_gcrl/artifacts/0012/build_writeup_outline.py",
    "research/reward_to_gcrl/artifacts/0012/local_compatibility_check.json",
    "research/reward_to_gcrl/artifacts/0012/numeric_evidence.json",
    "research/reward_to_gcrl/artifacts/0012/claim_status_table.json",
    "research/reward_to_gcrl/artifacts/0012/progress.jsonl"
  ],
  "baseline_metrics": {
    "new_baseline_run": false,
    "reason": "Memo-only iteration; baselines and comparisons are prior completed results 0001-0011."
  },
  "claim_tested": "Package existing 0001-0011 evidence into a concise memo and define a formal gate for future auxiliary-goal experiments without running new learning compute.",
  "experiment_id": "0012",
  "interpretation": "Current evidence is ready for a scoped write-up: positive small-tabular soft terminal marginalization, negative rank-4 low-rank FourRooms auxiliary result, and a formal gate before any more auxiliary compute.",
  "known_failures": [
    "rank4_lowrank_fourrooms_auxiliary_benefit_contradicted",
    "neural_larger_environment_online_claims_not_tested"
  ],
  "metrics": {
    "auxiliary_thread_gate": "new_hypothesis_required_before_more_compute",
    "claim_status_counts": {
      "contradicted": 1,
      "not_tested": 1,
      "partially_supported": 1,
      "supported": 2,
      "unsupported": 1
    },
    "final_recommendation": "write_short_paper",
    "inspected_experiment_ids": {
      "_type": "list",
      "first_items": [
        "0001",
        "0002",
        "0003"
      ],
      "length": 11
    },
    "new_learning_compute_run": false,
    "numeric_evidence": {
      "auxiliary_negative_evidence": {
        "_type": "object",
        "key_count": 14,
        "keys": [
          "0009_bellman_residual_delta_combined_minus_terminal",
          "0009_combined_gplus_bellman_residual",
          "0009_combined_gplus_value_error",
          "0009_combined_reward_success_rate",
          "0009_terminal_gplus_bellman_residual",
          "0009_terminal_gplus_value_error",
          "0009_terminal_reward_success_rate",
          "0009_value_error_delta_combined_minus_terminal",
          "0010_loss_balanced_gplus_residual",
          "0010_loss_balanced_gplus_value_error",
          "0010_staged_gplus_residual",
          "0010_staged_gplus_value_error",
          "0010_terminal_gplus_value_error",
          "0010_verdict"
        ]
      },
      "estimator_evidence": {
        "_type": "object",
        "key_count": 14,
        "keys": [
          "0001_finite_mdp_scaled_error",
          "0001_max_sampled_target_variance",
          "0001_max_soft_target_variance",
          "0002_cliffwalking_exact_scaled_error",
          "0003_sampled_residual",
          "0003_sampled_variance_exceeds_soft_rate",
          "0003_soft_residual",
          "0003_target_mean_match_rate",
          "0007_adequate_coverage_residual_delta",
          "0007_adequate_coverage_value_delta",
          "0007_starved_coverage_value_delta",
          "0008_min_goal_success_rate",
          "0008_vector_gplus_minus_terminal",
          "0008_vector_gplus_scaled_minus_q_norm"
        ]
      },
      "experiment_id": "0012",
      "new_learning_compute_run": false
    },
    "red_line_claims": [
      "auxiliary-goal benefit for g_plus",
      "general impossibility of real-state auxiliary goals",
      "neural auxiliary-goal benefit",
      "larger-environment generality",
      "online exploration robustness",
      "coverage-starved RiverSwim learning superiority",
      "reward-task improvement from independent tabular goal slices"
    ],
    "report_only": true,
    "strongest_defensible_auxiliary_claim": "The tested rank-4 NumPy low-rank FourRooms real-state auxiliary approach is unsupported and showed negative transfer.",
    "strongest_defensible_estimator_claim": "Soft terminal marginalization is a useful small-tabular estimator/equivalence mechanism under audited reward normalization and adequate coverage."
  },
  "next_questions": [
    "Should the short paper/blog draft be written from the 0012 outline?",
    "Is there a principled new auxiliary hypothesis worth reviewing before any further compute?"
  ],
  "status": "completed"
}
```


## Latest summary

# Experiment 0012 Summary

Status: **completed**.

This was a memo-only packaging step. No new learning compute, neural framework,
GPU run, larger environment, or broad sweep was used.

Recommendation: **write_short_paper**.

Auxiliary reopening gate: require a new human-approved falsifiable hypothesis
with a principled architecture or loss-normalization change and predeclared
terminal-only comparison criteria.

Outputs:

- `research/reward_to_gcrl/reports/0012_writeup_outline.md`
- `research/reward_to_gcrl/results/0012_result.json`
- `research/reward_to_gcrl/artifacts/0012/numeric_evidence.json`
- `research/reward_to_gcrl/artifacts/0012/claim_status_table.json`
- `research/reward_to_gcrl/artifacts/0012/progress.jsonl`


## Latest review summary

```json
{
  "allows_auto_continue": true,
  "escalation_reason": null,
  "evidence_checked": {
    "_type": "list",
    "first_items": [
      "research/reward_to_gcrl/results/0012_result.json",
      "research/reward_to_gcrl/results/0012_summary.md",
      "research/reward_to_gcrl/reports/0012_writeup_outline.md"
    ],
    "length": 10
  },
  "evidence_quality": "strong",
  "experiment_id": "0012",
  "failure_criteria_triggered": false,
  "reasons": [
    "Required 0012 result JSON, summary markdown, writeup outline, and artifact directory are present, and schema plus declared-artifact validation passed.",
    "The iteration is correctly report-only: result and artifacts record no new learning compute, no neural framework, no GPU run, no larger environment, and no broad sweep.",
    "The memo separates positive estimator evidence, negative auxiliary evidence, limitations, unsupported claims, and red-line claims without mixing the estimator result into an overbroad auxiliary-goal story.",
    "The claim table covers prior evidence through 0011 and includes supported, partially_supported, unsupported, contradicted, and not_tested labels with numeric evidence artifacts.",
    "The strongest estimator claim is scoped to small audited tabular settings with coverage caveats, while the auxiliary claim is scoped to the tested rank-4 NumPy low-rank FourRooms setup and not generalized to all auxiliary goals.",
    "The memo includes a figure/table plan based only on existing 0001-0011 evidence and defines a concrete new-hypothesis gate before reopening auxiliary experiments.",
    "The final recommendation, write_short_paper, is one of the predeclared allowed next directions."
  ],
  "required_fixes": [],
  "risk_flags": [
    "This iteration is packaging and synthesis only; it should not be treated as new empirical evidence.",
    "Auto-continuation should proceed only toward a short write-up using existing evidence, not toward new auxiliary compute without the stated gate.",
    "All positive estimator claims remain limited to small CPU tabular or CPU NumPy settings with audited reward normalization and terminal masks.",
    "RiverSwim learning advantages remain coverage-qualified; coverage-starved settings should not be cited as learning-superiority evidence.",
    "The auxiliary negative result is limited to the tested rank-4 FourRooms low-rank setup, replay construction, and predeclared repair diagnostics."
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
    },
    {
      "allows_auto_continue": true,
      "claim_tested": "Adding real-state goal slices to a tabular vector successor measure should leave the g_plus reward-success slice equivalent to the terminal-only soft learner while learning correct real-state goal reachability maps.",
      "decision": "continue",
      "important_metrics": {
        "metrics.config.goal_success_threshold": 0.99,
        "metrics.exact_dp.rows.0.gamma": 0.95,
        "metrics.exact_dp.rows.0.gplus_final_delta": 0.0,
        "metrics.exact_dp.rows.0.gplus_iterations": 14,
        "metrics.exact_dp.rows.0.max_abs_scaled_gplus_minus_q_norm": 1.1102230246251565e-16,
        "metrics.exact_dp.rows.0.q_final_delta": 0.0,
        "metrics.exact_dp.rows.0.q_iterations": 14,
        "metrics.exact_dp.rows.0.real_goal_final_delta": 0.0,
        "metrics.exact_dp.rows.0.real_goal_iterations": 14,
        "metrics.exact_dp.rows.1.gamma": 0.99,
        "metrics.exact_dp.rows.1.gplus_final_delta": 0.0,
        "metrics.exact_dp.rows.1.gplus_iterations": 14
      },
      "iteration": "0008",
      "negative_signals": [
        "Independent tabular real-state goal slices did not perturb the g_plus reward-success slice.",
        "This is an exact/full-sweep deterministic sanity check; it validates indexing and independent tabular slices, not learning under sampled data or function approximation.",
        "The result is expected to be nearly tautological because exact references and learned vector backups use the same audited transition semantics; this is acceptable for the predeclared implementation gate but should not be...",
        "Reward-policy comparison has many tie states, 17 of 40 with one skipped terminal state, although disagreement is zero on comparable non-tie states.",
        "Heatmap/arrow artifacts are saved for a selected subset of goals, while numerical per-goal metrics cover all goals."
      ],
      "positive_signals": [
        "The g_plus slice remains a direct scaled normalized-Q reference under the audited terminal mask.",
        "Real-state goals solve the deterministic reachability sanity check, so future reward changes require shared parameters or coupling to be meaningful.",
        "The vector SSM slices are numerically independent in this tabular FourRooms check: the g_plus slice matches terminal-only soft learning, scaled g_plus matches normalized Q, and real-state goal slices match exact reachability references with successful greedy g"
      ],
      "review_verdict": "pass",
      "status": "completed"
    },
    {
      "allows_auto_continue": true,
      "claim_tested": "A shared rank-4 NumPy low-rank FourRooms successor-measure model trained with real-state auxiliary goals should improve the g_plus reward-success slice versus terminal-only g_plus training under matched adequate offline replay, or the auxiliary benefit should not be claimed.",
      "decision": "continue",
      "important_metrics": {
        "metrics.config.improvement_threshold": 0.1,
        "metrics.config.replay_behavior.uses_exact_q_or_dp": false,
        "metrics.exact_dp.gamma": 0.95,
        "metrics.exact_dp.goal_iterations": 14,
        "metrics.exact_dp.gplus_iterations": 14,
        "metrics.exact_dp.max_abs_scaled_gplus_minus_q_norm": 1.1102230246251565e-16,
        "metrics.exact_dp.q_iterations": 14,
        "metrics.lowrank_auxiliary.aggregate.mean_combined_goal_success_rate": 0.003717948717948718,
        "metrics.lowrank_auxiliary.aggregate.mean_combined_reward_success_rate": 0.0,
        "metrics.lowrank_auxiliary.aggregate.mean_terminal_reward_success_rate": 0.5384615384615384,
        "metrics.lowrank_auxiliary.aggregate.relative_bellman_residual_improvement": -37.09593648978651,
        "metrics.lowrank_auxiliary.aggregate.relative_value_error_improvement": -230.03690989471423
      },
      "iteration": "0009",
      "negative_signals": [
        "Conservative verdict: negative_transfer.",
        "Exact tabular references are used only for evaluation, not behavior generation or target labels.",
        "Auxiliary reward-task benefit should not be claimed unless the verdict is auxiliary_helped_gplus.",
        "reward_policy_not_worse",
        "auxiliary_helped_gplus_criterion"
      ],
      "positive_signals": [
        "The low-rank model genuinely shares state-action factors across real-state goals and g_plus.",
        "Combined auxiliary training worsened a g_plus metric or reward-policy disagreement under adequate replay coverage; auxiliary-goal benefit is not supported."
      ],
      "review_verdict": "weak_pass",
      "status": "completed"
    },
    {
      "allows_auto_continue": true,
      "claim_tested": "The 0009 low-rank FourRooms negative transfer may be caused by loss-scaling or optimization imbalance; loss-balanced or staged auxiliary variants should reduce transfer harm if that diagnosis is correct.",
      "decision": null,
      "important_metrics": {
        "metrics.config.improvement_threshold": 0.1,
        "metrics.config.replay_behavior.uses_exact_q_or_dp": false,
        "metrics.environment_audit.verified_against_0009_where_available.aggregate.mean_combined_goal_success_rate": 0.003717948717948718,
        "metrics.environment_audit.verified_against_0009_where_available.aggregate.mean_combined_reward_success_rate": 0.0,
        "metrics.environment_audit.verified_against_0009_where_available.aggregate.mean_terminal_reward_success_rate": 0.5384615384615384,
        "metrics.environment_audit.verified_against_0009_where_available.aggregate.relative_bellman_residual_improvement": -37.09593648978651,
        "metrics.environment_audit.verified_against_0009_where_available.aggregate.relative_value_error_improvement": -230.03690989471423,
        "metrics.exact_dp.gamma": 0.95,
        "metrics.exact_dp.goal_iterations": 14,
        "metrics.exact_dp.gplus_iterations": 14,
        "metrics.exact_dp.max_abs_scaled_gplus_minus_q_norm": 1.1102230246251565e-16,
        "metrics.exact_dp.q_iterations": 14
      },
      "iteration": "0010",
      "negative_signals": [
        "Exact tabular references are used only for evaluation, not behavior generation or target labels.",
        "Auxiliary reward-task benefit should not be claimed unless the verdict is repaired_auxiliary_promising.",
        "repaired_variant_promising",
        "Primary positive auxiliary-repair success was not achieved; this is valid negative evidence, not support for auxiliary-goal benefit.",
        "Conclusion is limited to the single predeclared rank-4 low-rank architecture, optimizer, replay setup, and gamma used in this checkpoint."
      ],
      "positive_signals": [
        "Conservative verdict: auxiliary_unsupported_for_lowrank.",
        "The low-rank model genuinely shares state-action factors across real-state goals and g_plus.",
        "Original negative transfer reproduced, and neither repaired variant matched terminal-only on g_plus value error and Bellman residual. Auxiliary real-state goals should be paused for this low-rank architecture."
      ],
      "review_verdict": "weak_pass",
      "status": "completed"
    },
    {
      "allows_auto_continue": true,
      "claim_tested": "Synthesize 0001-0010 evidence to separate supported soft-terminal estimator claims from unsupported low-rank auxiliary-goal claims, without running new learning compute.",
      "decision": null,
      "important_metrics": {},
      "iteration": "0011",
      "negative_signals": [
        "RiverSwim learning advantages are coverage-qualified; starved runs are not learning-superiority evidence.",
        "Independent tabular real-state goals are a correctness sanity check, not an auxiliary reward-improvement result.",
        "lowrank_auxiliary_gplus_benefit_unsupported_for_tested_rank4_fourrooms_setup",
        "neural_larger_environment_online_auxiliary_claims_unsupported",
        "This iteration adds synthesis and decision framing only; it is not new empirical evidence."
      ],
      "positive_signals": [
        "Soft terminal marginalization has supported small-tabular estimator/equivalence evidence.",
        "Low-rank rank-4 FourRooms auxiliary training is unsupported after reproduction and repair diagnostics.",
        "The evidence supports soft terminal marginalization as a small-tabular estimator/equivalence mechanism with coverage-qualified RiverSwim learning advantages. It does not support low-rank shared real-state auxiliary goals for the tested FourRooms setup; pause t"
      ],
      "review_verdict": "pass",
      "status": "completed"
    },
    {
      "allows_auto_continue": true,
      "claim_tested": "Package existing 0001-0011 evidence into a concise memo and define a formal gate for future auxiliary-goal experiments without running new learning compute.",
      "decision": null,
      "important_metrics": {
        "metrics.numeric_evidence.auxiliary_negative_evidence.0009_combined_reward_success_rate": 0.0,
        "metrics.numeric_evidence.auxiliary_negative_evidence.0009_terminal_reward_success_rate": 0.5384615384615384,
        "metrics.numeric_evidence.estimator_evidence.0002_cliffwalking_exact_scaled_error": 9.711982329463353e-10,
        "metrics.numeric_evidence.estimator_evidence.0008_min_goal_success_rate": 1.0
      },
      "iteration": "0012",
      "negative_signals": [
        "rank4_lowrank_fourrooms_auxiliary_benefit_contradicted",
        "neural_larger_environment_online_claims_not_tested",
        "This iteration is packaging and synthesis only; it should not be treated as new empirical evidence.",
        "Auto-continuation should proceed only toward a short write-up using existing evidence, not toward new auxiliary compute without the stated gate.",
        "All positive estimator claims remain limited to small CPU tabular or CPU NumPy settings with audited reward normalization and terminal masks."
      ],
      "positive_signals": [
        "Existing evidence is mature enough for a scoped short write-up.",
        "Soft terminal marginalization claims must remain small-tabular and coverage-qualified.",
        "Rank-4 low-rank auxiliary FourRooms benefit is contradicted by 0009 and 0010.",
        "Future auxiliary work requires a new falsifiable hypothesis before compute.",
        "Current evidence is ready for a scoped write-up: positive small-tabular soft terminal marginalization, negative rank-4 low-rank FourRooms auxiliary result, and a formal gate before any more auxiliary compute."
      ],
      "review_verdict": "pass",
      "status": "completed"
    }
  ],
  "project": "reward_to_gcrl"
}
```


## Last decision summaries

## 0010_pro_decision.json

```json
{
  "confidence": 0.87,
  "decision": "pivot",
  "evidence": [
    "Reviewed evidence now reaches 0009, with no current blocker and protected_file_drift false.",
    "0001-0007 support the estimator story: deterministic soft terminal marginalization preserves normalized-Q scaling, removes terminal-sampling variance, and helps under adequate coverage in small tabular RiverSwim and repaired chain settings.",
    "0008 passed the vector SSM sanity gate: real-state goal slices were exact and did not perturb the g_plus slice, but the review correctly noted it was independent-slice tabular evidence, not shared representation evidence.",
    "0009 was the first genuinely shared low-rank FourRooms test: M_hat(s,a,g)=sigmoid(u_sa dot v_g + b_g), with u_sa shared across real-state goals and g_plus.",
    "0009 used CPU-only NumPy, audited FourRooms semantics from 0008, matched replay datasets, matched seeds, matched optimizer budgets, rank 4, learning rate 0.05, and adequate replay coverage for all 10 seeds.",
    "0009 produced a valid negative result: terminal-only g_plus had mean Bellman residual 0.0009558486, mean scaled value error 0.0731219459, and mean reward success rate 0.5384615385.",
    "0009 combined auxiliary training collapsed: mean g_plus Bellman residual worsened to 0.0364139480, mean scaled value error worsened to 16.8938684161, reward success fell to 0.0, and real-goal diagnostics were also poor.",
    "The 0009 review explicitly labels this as negative_transfer and warns that it may reflect optimizer or loss-scaling issues rather than a general impossibility of auxiliary goals."
  ],
  "next_experiment": {
    "estimated_runtime_minutes": 25,
    "experiment_id": "0010",
    "hypothesis": "If 0009 failed mainly because auxiliary real-state losses overwhelmed or destabilized the g_plus head, then a loss-balanced or staged auxiliary variant should reduce negative transfer and approach or improve terminal-only g_plus metrics. If these controlled variants still fail, auxiliary real-state goals are unsupported for this low-rank architecture and should be paused.",
    "objective": "Diagnose the 0009 negative transfer in the shared low-rank FourRooms SSM by testing whether auxiliary collapse is caused by loss-scaling or optimization imbalance, while keeping the run CPU-only, NumPy-only, tiny, and predeclared.",
    "required_outputs": [
      "research/reward_to_gcrl/results/0010_result.json",
      "research/reward_to_gcrl/results/0010_summary.md",
      "research/reward_to_gcrl/artifacts/0010/"
    ]
  },
  "progress_score": null,
  "rationale": "Pivot within the same research direction. The project has made real progress on the core estimator story, but the first shared-parameter auxiliary-goal milestone produced valid negative-transfer evidence, not auxiliary-benefit evidence. The next step should not expand to neural frameworks, larger sweeps, or publishable auxiliary-goal claims. It should run one small diagnostic to determine whether 0009 failed because auxiliary real-state goals are harmful in this setup, or because the low-rank model collapsed due to loss scaling, gradient imbalance, or optimization details.",
  "risks": [
    "A diagnostic ablation could become an unprincipled hyperparameter sweep if too many ranks, losses, and auxiliary weights are tried.",
    "If loss scaling fixes the collapse, the evidence will still be tiny NumPy low-rank evidence, not a neural or publishable auxiliary-goal claim.",
    "If loss scaling does not fix the collapse, the correct conclusion may be to stop the auxiliary-goal thread for this architecture and write up the negative result.",
    "Replay uses uniform state-action resets, so even a repaired result may not transfer to realistic trajectory-only offline data.",
    "Both terminal-only and combined models have imperfect reward policies, so improvements must be judged against terminal-only and exact references, not absolute success alone.",
    "Expanding to PyTorch, JAX, GPU, larger FourRooms, or broad auxiliary-goal claims before this diagnostic is reviewed would overinterpret the evidence."
  ]
}
```

## 0011_pro_decision.json

```json
{
  "confidence": 0.9,
  "decision": "pivot",
  "evidence": [
    "0001-0007 support the core estimator claim: deterministic soft terminal marginalization preserves normalized-Q scaling, removes terminal-sampling variance, and helps under adequate coverage in small tabular settings.",
    "0008 validated tabular vector SSM indexing: g_plus matched terminal-only exactly, scaled g_plus matched normalized Q to 1.1102230246251565e-16, and real-state goal slices had zero value error.",
    "0009 was the first genuinely shared low-rank test with M_hat(s,a,g)=sigmoid(u_sa dot v_g + b_g), CPU-only NumPy, matched replay, matched seeds, rank 4, learning rate 0.05, and adequate coverage.",
    "0009 produced negative transfer: terminal-only had mean Bellman residual 0.0009558486 and mean scaled value error 0.0731219459, while combined auxiliary training worsened mean Bellman residual to 0.0364139480 and mean scaled value error to 16.8938684161.",
    "0010 reproduced the original negative-transfer result under the same audited FourRooms setup.",
    "0010 tested only the four predeclared variants: terminal-only, original combined, loss-balanced combined, and staged auxiliary pretrain then g_plus fine-tuning.",
    "Neither repaired auxiliary variant matched terminal-only on g_plus value error and Bellman residual.",
    "The 0010 review labels the result auxiliary_unsupported_for_lowrank and warns that expanding to neural frameworks, GPU, larger environments, or broad sweeps would overreach."
  ],
  "next_experiment": {
    "estimated_runtime_minutes": 20,
    "experiment_id": "0011",
    "hypothesis": "The current evidence is strong enough for a scoped report with two claims: soft terminal marginalization is a reliable small-tabular variance-reduction/equivalence mechanism under adequate coverage, while real-state auxiliary goals are unsupported for the tested low-rank shared FourRooms architecture. No additional learning run is justified until this evidence is consolidated and reviewed.",
    "objective": "Produce a compact evidence-synthesis report that separates the positive soft-terminal estimator result from the negative low-rank auxiliary-goal result, and defines what evidence would be required before reopening auxiliary-goal experiments.",
    "required_outputs": [
      "research/reward_to_gcrl/results/0011_result.json",
      "research/reward_to_gcrl/results/0011_summary.md",
      "research/reward_to_gcrl/artifacts/0011/"
    ]
  },
  "progress_score": null,
  "rationale": "Pivot from further auxiliary-goal experimentation to consolidation and write-up. The project is making real progress on the soft-terminal estimator story, but the auxiliary/shared-representation hypothesis is currently unsupported. Experiments 0009 and 0010 are valid negative evidence: the first shared low-rank FourRooms auxiliary test collapsed, and the predeclared repair diagnostic reproduced negative transfer rather than fixing it. Continuing to larger sweeps, neural frameworks, or auxiliary-goal claims would reward activity over evidence. The next best move is to pause the low-rank auxiliary thread and produce a short evidence report separating the positive estimator claim from the negative auxiliary result.",
  "risks": [
    "The negative auxiliary conclusion is limited to one rank-4 NumPy low-rank architecture, optimizer, replay setup, and gamma.",
    "The loss-balanced variant still had large auxiliary-to-g_plus shared-factor gradient dominance, so scale imbalance may remain unresolved.",
    "Terminal-only is imperfect, so the result supports pausing this low-rank auxiliary thread, not claiming that auxiliary goals are generally harmful.",
    "Uniform state-action reset replay gives adequate coverage but is less realistic than trajectory-only offline data.",
    "A report could overstate the estimator story if it does not clearly separate matched-stream estimator evidence from online exploration evidence.",
    "A report could overstate the auxiliary result if it presents one low-rank failure as a general impossibility theorem."
  ]
}
```

## 0012_pro_decision.json

```json
{
  "confidence": 0.91,
  "decision": "pivot",
  "evidence": [
    "0011 is a reviewed report-only synthesis with verdict pass and strong evidence quality; no new learning compute was run.",
    "0001-0007 support the core estimator claim: deterministic soft terminal marginalization preserves normalized-Q scaling, removes terminal-sampling variance, and helps under adequate coverage in small tabular settings.",
    "0008 validated tabular vector SSM indexing: g_plus matched terminal-only exactly, scaled g_plus matched normalized Q to 1.1102230246251565e-16, and real-state goal slices had zero value error.",
    "0009 was the first shared low-rank FourRooms auxiliary test with M_hat(s,a,g)=sigmoid(u_sa dot v_g + b_g), and it produced valid negative transfer.",
    "0009 terminal-only had mean Bellman residual 0.0009558486 and mean scaled value error 0.0731219459, while combined auxiliary training worsened mean Bellman residual to 0.0364139480 and mean scaled value error to 16.8938684161.",
    "0010 reproduced the negative-transfer result and tested only the four predeclared variants: terminal-only, original combined, loss-balanced combined, and staged auxiliary pretrain followed by g_plus fine-tuning.",
    "Neither loss-balanced nor staged auxiliary repair matched terminal-only on g_plus value error and Bellman residual.",
    "0011 correctly frames the current state: positive estimator claims are supported only in scoped small-tabular settings, while low-rank shared real-state auxiliary training did not help g_plus in the tested rank-4 FourRooms setup."
  ],
  "next_experiment": {
    "estimated_runtime_minutes": 20,
    "experiment_id": "0012",
    "hypothesis": "The current evidence is mature enough for a scoped negative-and-positive write-up: soft terminal marginalization is a useful small-tabular estimator/equivalence mechanism under adequate coverage, while the tested low-rank real-state auxiliary approach is unsupported. Further progress requires either writing this up or proposing a genuinely new falsifiable auxiliary hypothesis.",
    "objective": "Package the current evidence into a concise research memo or draft note, and define a formal gate for any future auxiliary-goal experiments. No new learning compute should be run.",
    "required_outputs": [
      "research/reward_to_gcrl/results/0012_result.json",
      "research/reward_to_gcrl/results/0012_summary.md",
      "research/reward_to_gcrl/artifacts/0012/"
    ]
  },
  "progress_score": null,
  "rationale": "Pivot from running more experiments to packaging the current evidence and defining a new hypothesis gate. The project is making real progress on the soft-terminal estimator component, which is now well supported across small audited tabular settings. But the auxiliary/shared-representation direction is not supported: 0009 produced negative transfer, 0010 reproduced it after predeclared repair attempts, and 0011 passed as a report-only synthesis separating supported estimator claims from unsupported auxiliary claims. More compute, larger sweeps, neural frameworks, or auxiliary-goal claims would overreach unless a genuinely new falsifiable hypothesis is approved.",
  "risks": [
    "A write-up could overstate the estimator story if it ignores matched-stream and coverage caveats.",
    "A write-up could overstate the auxiliary negative result if it presents one rank-4 NumPy architecture as a general impossibility claim.",
    "The positive estimator evidence remains small-scale and mostly tabular; it does not establish neural, large-environment, online-exploration, or benchmark generality.",
    "The auxiliary conclusion is limited to one architecture family, optimizer, replay setup, gamma, and predeclared repair set.",
    "Starting PyTorch/JAX, GPU, larger FourRooms, or broad hyperparameter sweeps now would reward activity over evidence.",
    "A new auxiliary experiment is justified only if it changes architecture or loss normalization for a principled reason rather than tuning around a negative result."
  ]
}
```


## Full evidence paths

- `research/reward_to_gcrl/results/0012_result.json`
- `research/reward_to_gcrl/results/0012_summary.md`
- `research/reward_to_gcrl/reviews/0012_review.json`

Use these paths if compact summaries are insufficient.


## Stop, pivot, continue rules

- For iteration 0, a missing latest result is expected and is not by itself a reason to stop.
- After iteration 0, stop or choose needs_human on missing or invalid result files.
- Stop on repeated invalid, negative, or low-value results.
- Pivot only when evidence weakens the original idea but reveals a nearby testable idea.
- Continue or pivot only for one cheap, high-information experiment.
- Choose needs_human for ambiguity, expensive work, missing artifacts, or risky pivots.


## Next experiment id

Use `0013` as the exact `next_experiment.experiment_id` if you choose continue or pivot.
