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
  "iteration": 3,
  "last_decision": "continue",
  "last_failure": null,
  "last_pro_review_iteration": 1,
  "last_pro_review_path": "research/reward_to_gcrl/decisions/0002_review3_pro_decision.json",
  "last_summary_iteration": 3,
  "last_summary_path": "research/reward_to_gcrl/progress/0003_pre_pro_weak_pass_streak_summary.md",
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
    "2026-06-14T20:49:23+00:00: resumed: Retry Pro checkpoint after ChatGPT browser response finished"
  ],
  "pending_checkpoint": null,
  "pending_local_decision_path": null,
  "primary_metric": null,
  "pro_review_count": 2,
  "protected_file_drift": false,
  "status": "active",
  "weak_pass_streak": 2
}
```


## Latest result summary

```json
{
  "_source": "/home/eston/autoresearcher/research/reward_to_gcrl/results/0003_result.json",
  "artifacts": {
    "_type": "list",
    "first_items": [
      "research/reward_to_gcrl/artifacts/0003/run_sampled_vs_soft_cliffwalking.py",
      "research/reward_to_gcrl/artifacts/0003/local_compatibility_check.json",
      "research/reward_to_gcrl/artifacts/0003/environment_audit.json"
    ],
    "length": 10
  },
  "baseline_metrics": {
    "baseline_name": "sampled_augmented_g_plus_learning",
    "mean_conditional_sampling_variance": 0.0004278098216495158,
    "mean_final_bellman_residual_sufficient": 0.04124613525377317,
    "mean_final_value_error_sufficient": 0.08156038291965984,
    "mean_g_plus_events_per_10000": 212.67000000000002,
    "mean_raw_return": -200.0,
    "mean_success_rate": 0.0
  },
  "claim_tested": "On the audited local CliffWalking transition table, sampled augmented g_plus learning is an unbiased but higher-variance estimator of the terminal-only soft successor target and reduces error more slowly under the same original transition budget.",
  "experiment_id": "0003",
  "interpretation": "The sampled augmented target is unbiased within the predeclared Monte Carlo tolerance in all gamma/seed runs, but its terminal sampling variance is strictly positive while the deterministic soft target has zero terminal sampling variance. Under the matched transition stream, the soft learner has lower final or earlier-threshold value error in most runs.",
  "known_failures": [],
  "metrics": {
    "config": {
      "alpha": 0.2,
      "checkpoints": {
        "_type": "list",
        "length": 7
      },
      "epsilon_end": 0.05,
      "epsilon_start": 0.35,
      "gammas": {
        "_type": "list",
        "length": 3
      },
      "mc_sigma_tolerance": 6.0,
      "min_pair_visits": 5,
      "reward_normalization": "(raw_reward + 100) / 99 for raw -100/-1; terminal self-loop maps to 0",
      "sampled_continue_target": "max_a M(s_next,a) with no extra gamma factor",
      "seeds": {
        "_type": "list",
        "length": 10
      },
      "terminal_mask": "zero bootstrap on original terminated transitions; g_plus/g_minus sampled events never bootstrap",
      "transition_budget": 200000,
      "value_error_threshold": 0.1
    },
    "environment_audit": {
      "complete": true,
      "matches_previous_0002_transition_hash": true,
      "missing_fields": {
        "_type": "list",
        "length": 0
      },
      "transition_table_hash": "f6fa1c509349d50f18e13b6309b3f051c6cef9a8fcdab25f1332537f521d40a2",
      "transition_table_record_count": 192
    },
    "exact_soft_dp": {
      "rows": {
        "_type": "list",
        "length": 3
      }
    },
    "pass_flags": {
      "all_primary_criteria_satisfied": true,
      "cpu_tabular_only": true,
      "environment_audit_complete": true,
      "gamma_seed_budget_complete": true,
      "raw_per_seed_metrics_saved": true,
      "sampled_target_means_match_expected_soft_target": true,
      "sampled_target_variance_exceeds_soft_terminal_sampling_variance": true,
      "soft_lower_or_faster_error_in_most_runs": true
    },
    "sampled_vs_soft": {
      "aggregate": {
        "_type": "object",
        "key_count": 24,
        "keys": [
          "by_gamma",
          "max_g_plus_events_per_10000",
          "max_target_mean_abs_error",
          "max_target_mean_mc_tolerance",
          "mean_conditional_sampling_variance",
          "mean_final_sampled_bellman_residual_sufficient",
          "mean_final_sampled_value_error_sufficient",
          "mean_final_soft_bellman_residual_sufficient",
          "mean_final_soft_value_error_sufficient",
          "mean_g_plus_events_per_10000",
          "mean_sampled_policy_raw_return",
          "mean_sampled_policy_success_rate",
          "mean_soft_policy_raw_return",
          "mean_soft_policy_success_rate",
          "min_g_plus_events_per_10000",
          "run_count",
          "sampled_variance_exceeds_soft_count",
          "sampled_variance_exceeds_soft_rate",
          "soft_dominance_count",
          "soft_dominance_rate"
        ]
      }
    }
  },
  "next_questions": [
    "Should the next experiment reduce the constant-alpha noise floor with a decaying step size or replay-style averaging?",
    "Should the sampled-vs-soft comparison be repeated only on reward normalizations that preserve raw CliffWalking goal-reaching incentives?"
  ],
  "status": "completed"
}
```


## Latest summary

# Experiment 0003 Summary

## Verdict

The sampled-vs-soft tabular gate is **satisfied**.

## Key Metrics

- Runs: `30` (`3` gammas x `10` seeds)
- Transition budget per run: `200000`
- Mean `g_plus` events per 10000 transitions: `212.67`
- Target mean match rate: `1`
- Sampled variance exceeds soft terminal-sampling variance rate: `1`
- Soft lower/faster error dominance rate: `0.566667`
- Mean final soft value error on sufficiently visited pairs: `0.0821131`
- Mean final sampled value error on sufficiently visited pairs: `0.0815604`
- Mean final soft Bellman residual on sufficiently visited pairs: `0.0387504`
- Mean final sampled Bellman residual on sufficiently visited pairs: `0.0412461`

## Interpretation

The sampled augmented target is unbiased within the predeclared Monte Carlo tolerance in all gamma/seed runs, but its terminal sampling variance is strictly positive while the deterministic soft target has zero terminal sampling variance. Under the matched transition stream, the soft learner has lower final or earlier-threshold value error in most runs.

The sampled learner uses `g_plus -> 1`, `g_minus -> 0`, and `continue -> max_a M(s_next,a)` with no extra gamma factor. The deterministic soft update uses the corresponding conditional expectation. Terminal bootstraps are masked for original terminal transitions, and sampled `g_plus`/`g_minus` absorbing events never bootstrap.

## Commands Run

```bash
mkdir -p research/reward_to_gcrl/artifacts/0003 research/reward_to_gcrl/results
conda run -n autoresearcher_reward_to_gcrl python --version
conda run -n autoresearcher_reward_to_gcrl python -m py_compile research/reward_to_gcrl/artifacts/0003/run_sampled_vs_soft_cliffwalking.py
conda run -n autoresearcher_reward_to_gcrl python research/reward_to_gcrl/artifacts/0003/run_sampled_vs_soft_cliffwalking.py --check-only
conda run -n autoresearcher_reward_to_gcrl python research/reward_to_gcrl/artifacts/0003/run_sampled_vs_soft_cliffwalking.py
conda run -n autoresearcher_reward_to_gcrl python -m jsonschema -i research/reward_to_gcrl/results/0003_result.json schemas/result.schema.json
conda run -n autoresearcher_reward_to_gcrl python scripts/validate_artifacts.py --repo-root . --json research/reward_to_gcrl/results/0003_result.json --schema schemas/result.schema.json --check-result-artifacts
```

## Artifacts

- `research/reward_to_gcrl/artifacts/0003/run_sampled_vs_soft_cliffwalking.py`
- `research/reward_to_gcrl/artifacts/0003/local_compatibility_check.json`
- `research/reward_to_gcrl/artifacts/0003/environment_audit.json`
- `research/reward_to_gcrl/artifacts/0003/exact_soft_dp_reference.json`
- `research/reward_to_gcrl/artifacts/0003/per_seed_metrics.json`
- `research/reward_to_gcrl/artifacts/0003/per_seed_summary.csv`
- `research/reward_to_gcrl/artifacts/0003/learning_curves.json`
- `research/reward_to_gcrl/artifacts/0003/learning_curves.csv`
- `research/reward_to_gcrl/artifacts/0003/raw_metrics.json`
- `research/reward_to_gcrl/artifacts/0003/progress.jsonl`


## Latest review summary

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
    }
  ],
  "project": "reward_to_gcrl"
}
```


## Last decision summaries

## 0002_decision.json

```json
{
  "confidence": 0.86,
  "decision": "continue",
  "evidence": [
    "research/reward_to_gcrl/results/0001_result.json is present and records status completed, exact commands, raw per-setting metrics, and artifacts.",
    "The 0001 review allows auto-continue and reports no triggered failure criteria, while flagging only medium-quality evidence and minor reporting risks.",
    "0001 passed the one-state diagnostic: sampled and soft target means matched within tolerance across all 16 gamma/r_bar settings, soft variance was zero, and sampled g_plus events became rare at high gamma and low r_bar.",
    "0001 also included a tiny finite-MDP fixed-point check with max_abs_error_scaled_f_vs_q 3.9475e-08 below the 1e-6 tolerance, supporting the scaling relationship in a minimal setting.",
    "The charter explicitly requires tabular CliffWalking equivalence and low policy disagreement before moving to larger or neural experiments."
  ],
  "next_experiment": {
    "estimated_runtime_minutes": 20,
    "experiment_id": "0002",
    "hypothesis": "On Gymnasium CliffWalking-v0 dynamics with a predeclared normalized reward, the terminal-only soft successor learner with target (1 - gamma) * r_bar + gamma * max_a M(s_next,a,g_plus) will match ordinary normalized-reward Q-learning after scaling M_plus by 1/(1 - gamma), and their greedy policies will have near-zero disagreement.",
    "objective": "Run a CPU-only tabular CliffWalking equivalence diagnostic comparing ordinary normalized-reward Q-learning to the terminal-only soft successor g_plus learner.",
    "required_outputs": [
      "research/reward_to_gcrl/results/0002_result.json",
      "research/reward_to_gcrl/results/0002_summary.md",
      "research/reward_to_gcrl/artifacts/0002/ with diagnostic script, raw metrics, metadata, and DP/policy comparison artifacts"
    ]
  },
  "progress_score": 2,
  "rationale": "Experiment 0001 provides enough validated evidence to move to the next charter gate, but not enough to make a broader positive claim. The highest-value next test is the required small tabular CliffWalking equivalence check: terminal-only soft successor learning must match normalized Q-learning before sampled baselines, auxiliary goals, RiverSwim, or neural approximation are worth running.",
  "risks": [
    "Reward normalization in CliffWalking can change the task; the executor must predeclare the exact normalized reward and treat original-environment return as diagnostic, not as the equivalence pass/fail criterion.",
    "A paired-learning implementation could appear to pass because both learners share the same bug; include an exact dynamic-programming oracle for the declared normalized reward.",
    "Terminal handling is a known failure mode: bootstrapping after the goal terminal state would invalidate the result.",
    "The prior 0001 tolerance/reporting issues should not be copied forward; commands should reflect the actual invocation and pass/fail tolerances should be explicit."
  ]
}
```

## 0002_review3_pro_decision.json

```json
{
  "confidence": 0.84,
  "decision": "continue",
  "evidence": [
    "latest_summary.md says 0001 is the only accepted experimental evidence so far and that the broader research goal remains unsolved.",
    "0001 passed the planned one-state sampled-vs-soft diagnostic: all 16 gamma/r_bar settings were covered, sampled means passed the stricter 3-SE check, soft target variance was zero/negligible, and rare g_plus events were exposed at high gamma.",
    "0001 also passed the tiny finite-MDP scaling check with max_abs_error_scaled_f_vs_q = 3.9475168023273e-08, below the 1e-6 threshold.",
    "0002 is not accepted as equivalence evidence because the planned DP oracle and paired tabular-learning comparison did not run.",
    "The 0002 blocker is specific: gym.make('CliffWalking-v0') raises gymnasium.error.DeprecatedEnv under Gymnasium 1.3.0, while no exact-DP scaled value error, greedy policy disagreement, or 10-seed paired-learning metrics were produced.",
    "The local 0002 decision already identifies tabular CliffWalking equivalence as the required next charter gate before RiverSwim, FourRooms, sampled baselines, auxiliary goals, or neural approximation."
  ],
  "next_experiment": {
    "estimated_runtime_minutes": 20,
    "experiment_id": "0002",
    "hypothesis": "For a deterministic 4x12 CliffWalking MDP with declared rewards, reset, cliff, and terminal semantics, the exact soft successor fixed point satisfies F_gplus_star/(1-gamma) = Q_norm_star, and paired tabular soft successor learning induces the same greedy policy as normalized Q-learning up to tie handling.",
    "objective": "Rerun the blocked CliffWalking tabular equivalence test using a small local deterministic transition-table implementation with fully audited semantics, then compare exact-DP references, normalized Q-learning, and terminal-only soft successor g_plus learning.",
    "required_outputs": [
      "research/reward_to_gcrl/results/0002_result.json",
      "research/reward_to_gcrl/results/0002_summary.md",
      "research/reward_to_gcrl/artifacts/0002/"
    ]
  },
  "progress_score": null,
  "rationale": "Continue, but treat the current blocker as an experiment-infrastructure issue, not research evidence. The project has one accepted weak-pass result from 0001 showing the one-state variance/equivalence premise is plausible, while 0002 produced no DP oracle, no policy disagreement, and no paired tabular-learning evidence because CliffWalking-v0 was rejected by Gymnasium 1.3.0. The next step should unblock the same scientific gate with an explicit deterministic CliffWalking transition-table implementation, avoiding Gymnasium environment-id ambiguity entirely.",
  "risks": [
    "A hand-written CliffWalking transition table can accidentally encode the wrong cliff reset or terminal behavior unless every transition is audited.",
    "Reward normalization in CliffWalking can obscure original-task performance, so normalized value equivalence and raw-return diagnostics must both be reported.",
    "A paired learner comparison can falsely pass if both implementations share a bug; an independent exact-DP oracle is required.",
    "Policy disagreement can be misleading under action-value ties, so ties must be separated from true disagreements.",
    "Passing this experiment still only validates the base soft g_plus learner; it does not yet show auxiliary goals or GCRL structure improve learning."
  ]
}
```

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


## Full evidence paths

- `research/reward_to_gcrl/results/0003_result.json`
- `research/reward_to_gcrl/results/0003_summary.md`
- `research/reward_to_gcrl/reviews/0003_review.json`

Use these paths if compact summaries are insufficient.


## Stop, pivot, continue rules

- For iteration 0, a missing latest result is expected and is not by itself a reason to stop.
- After iteration 0, stop or choose needs_human on missing or invalid result files.
- Stop on repeated invalid, negative, or low-value results.
- Pivot only when evidence weakens the original idea but reveals a nearby testable idea.
- Continue or pivot only for one cheap, high-information experiment.
- Choose needs_human for ambiguity, expensive work, missing artifacts, or risky pivots.


## Next experiment id

Use `0004` as the exact `next_experiment.experiment_id` if you choose continue or pivot.
