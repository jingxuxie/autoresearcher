# Supervisor Context: sto_trl

## Requested action

Choose continue, pivot, stop, or needs_human. If this is iteration 0 with no prior result, propose the first small experiment when the charter is specific enough. If continuing, propose exactly one small experiment. If a human pivot note or next-step review plan exists, treat it as approved human direction and normally choose continue with the next small experiment from that plan, unless it is unsafe or impossible.


## Project charter

# Stochastic TRL Charter

## Research Goal

Rapidly test whether a stochastic extension of Transitive RL is worth pursuing.

The core question is whether calibrated stochastic successor distances plus TRL-style divide-and-conquer path relaxation can improve long-horizon offline goal-conditioned RL under stochastic dynamics, especially in environments with risky shortcuts or stochastic teleporters.

The full prototype plan is in `research/sto_trl/stochastic_trl_fast_prototype_plan.md`. This charter is the compact source of truth for the autoresearcher loop.

## Main Hypothesis

A stochastic-calibrated log or successor-distance TRL variant can reduce optimistic bias on risky stochastic paths while preserving TRL-style horizon generalization.

More concretely:

- Raw deterministic-style TRL may overestimate lucky stochastic paths.
- Log-space TRL should be numerically safer for long horizons than raw probability products.
- Adding a calibrated stochastic distance or successor-distance term should improve value calibration at stochastic branch points.
- A useful method should reduce overestimation without simply becoming conservative everywhere.

## Initial Scope

Start with tabular experiments only. Do not start with OGBench, PointMaze, AntMaze, or large neural-network training.

The first autoresearcher iterations should implement and test:

1. A deterministic chain sanity check.
2. A risky shortcut versus safe route stochastic MDP.
3. Exact DP ground truth for discounted reachability.
4. Small offline trajectory generation with lucky and unlucky stochastic outcomes.
5. Baselines: MC supervised, TRL-raw, TRL-log, and MC + TRL-log.

Only after deterministic and stochastic tabular diagnostics are clean should later iterations consider learned tabular models, tiny MLPs, continuous point mazes, or OGBench teleport tasks.

## Primary Metrics

Use exact DP ground truth wherever possible.

Primary metrics:

- Overestimation error: mean `max(0, U_hat - U_star)`.
- Policy regret versus exact DP policy.
- Long-horizon value MSE.
- Risky action selection rate.
- Calibration error for discounted reachability.

Secondary metrics:

- Underestimation error.
- Triangle violation rate for learned distance-like quantities.
- Greedy policy success rate.
- Median steps to goal.
- Coverage diagnostics for states, actions, goals, and risky success/failure outcomes.

## Success Criteria

Early evidence is positive only if a small tabular experiment shows at least one of:

- Raw TRL has a measurable overoptimism region on stochastic risky paths.
- TRL-log or MC + TRL-log improves long-horizon estimates over MC-only without breaking deterministic sanity checks.
- A stochastic-calibrated variant reduces risky-path overestimation while preserving safe-route value estimates.
- The greedy policy improves regret or risky-action choice versus raw TRL under exact DP evaluation.

The first iteration should be considered successful if it creates a reproducible tabular harness and produces a valid result table for at least the deterministic chain and one risky-shortcut configuration.

## Failure Criteria

Pause or stop before larger experiments if:

- Raw/log TRL cannot recover deterministic shortest-path behavior in a simple chain.
- There is no exact DP ground truth for the stochastic diagnostic.
- The experiment only reports training loss and no value/policy calibration metrics.
- The stochastic variant wins only by being conservative and avoiding all risky paths, including cases where risk is optimal.
- The loop attempts OGBench, AntMaze, large downloads, or long training before tabular diagnostics pass.
- The result omits exact commands, raw metrics, or coverage diagnostics.

## Runtime And Compute Budget

Initial experiments should complete in minutes on CPU or GPU.

Use the project conda environment `autoresearcher_sto_trl`. JAX/GPU is allowed and preferred when available, but the first tabular experiments must remain small enough to run without expensive training.

Treat step counts in offline diagnostics as optimizer/update steps unless the experiment explicitly reports environment rollouts. For this project, early runtime should mostly come from JAX/XLA compilation, repeated updates, pair sampling, and scoring rather than environment interaction.

## First Experiment Guidance

The supervisor should propose exactly one small experiment for iteration 1:

- Build a minimal tabular prototype under `research/sto_trl/artifacts/0001/`.
- Implement deterministic chain and risky shortcut MDPs.
- Implement exact discounted reachability DP.
- Compare MC supervised, TRL-raw, TRL-log, and MC + TRL-log on a tiny configuration.
- Save raw metrics to JSON or CSV.
- Produce `research/sto_trl/results/0001_result.json` and `research/sto_trl/results/0001_summary.md`.

Do not optimize for benchmark performance in the first run. Optimize for a correct diagnostic that can reveal whether the idea has a real failure mode to target.


## Project planning docs

## research/sto_trl/charter.md

```markdown
# Stochastic TRL Charter

## Research Goal

Rapidly test whether a stochastic extension of Transitive RL is worth pursuing.

The core question is whether calibrated stochastic successor distances plus TRL-style divide-and-conquer path relaxation can improve long-horizon offline goal-conditioned RL under stochastic dynamics, especially in environments with risky shortcuts or stochastic teleporters.

The full prototype plan is in `research/sto_trl/stochastic_trl_fast_prototype_plan.md`. This charter is the compact source of truth for the autoresearcher loop.

## Main Hypothesis

A stochastic-calibrated log or successor-distance TRL variant can reduce optimistic bias on risky stochastic paths while preserving TRL-style horizon generalization.

More concretely:

- Raw deterministic-style TRL may overestimate lucky stochastic paths.
- Log-space TRL should be numerically safer for long horizons than raw probability products.
- Adding a calibrated stochastic distance or successor-distance term should improve value calibration at stochastic branch points.
- A useful method should reduce overestimation without simply becoming conservative everywhere.

## Initial Scope

Start with tabular experiments only. Do not start with OGBench, PointMaze, AntMaze, or large neural-network training.

The first autoresearcher iterations should implement and test:

1. A deterministic chain sanity check.
2. A risky shortcut versus safe route stochastic MDP.
3. Exact DP ground truth for discounted reachability.
4. Small offline trajectory generation with lucky and unlucky stochastic outcomes.
5. Baselines: MC supervised, TRL-raw, TRL-log, and MC + TRL-log.

Only after deterministic and stochastic tabular diagnostics are clean should later iterations consider learned tabular models, tiny MLPs, continuous point mazes, or OGBench teleport tasks.

## Primary Metrics

Use exact DP ground truth wherever possible.

Primary metrics:

- Overestimation error: mean `max(0, U_hat - U_star)`.
- Policy regret versus exact DP policy.
- Long-horizon value MSE.
- Risky action selection rate.
- Calibration error for discounted reachability.

Secondary metrics:

- Underestimation error.
- Triangle violation rate for learned distance-like quantities.
- Greedy policy success rate.
- Median steps to goal.
- Coverage diagnostics for states, actions, goals, and risky success/failure outcomes.

## Success Criteria

Early evidence is positive only if a small tabular experiment shows at least one of:

- Raw TRL has a measurable overoptimism region on stochastic risky paths.
- TRL-log or MC + TRL-log improves long-horizon estimates over MC-only without breaking deterministic sanity checks.
- A stochastic-calibrated variant reduces risky-path overestimation while preserving safe-route value estimates.
- The greedy policy improves regret or risky-action choice versus raw TRL under exact DP evaluation.

The first iteration should be considered successful if it creates a reproducible tabular harness and produces a valid result table for at least the deterministic chain and one risky-shortcut configuration.

## Failure Criteria

Pause or stop before larger experiments if:

- Raw/log TRL cannot recover deterministic shortest-path behavior in a simple chain.
- There is no exact DP ground truth for the stochastic diagnostic.
- The experiment only reports training loss and no value/policy calibration metrics.
- The stochastic variant wins only by being conservative and avoiding all risky paths, including cases where risk is optimal.
- The loop attempts OGBench, AntMaze, large downloads, or long training before tabular diagnostics pass.
- The result omits exact commands, raw metrics, or coverage diagnostics.

## Runtime And Compute Budget

Initial experiments should complete in minutes on CPU or GPU.

Use the project conda environment `autoresearcher_sto_trl`. JAX/GPU is allowed and preferred when available, but the first tabular experiments must remain small enough to run without expensive training.

Treat step counts in offline diagnostics as optimizer/update steps unless the experiment explicitly reports environment rollouts. For this project, early runtime should mostly come from JAX/XLA compilation, repeated updates, pair sampling, and scoring rather than environment interaction.

## First Experiment Guidance

The supervisor should propose exactly one small experiment for iteration 1:

- Build a minimal tabular prototype under `research/sto_trl/artifacts/0001/`.
- Implement deterministic chain and risky shortcut MDPs.
- Implement exact discounted reachability DP.
- Compare MC supervised, TRL-raw, TRL-log, and MC + TRL-log on a tiny configuration.
- Save raw metrics to JSON or CSV.
- Produce `research/sto_trl/results/0001_result.json` and `research/sto_trl/results/0001_summary.md`.

Do not optimize for benchmark performance in the first run. Optimize for a correct diagnostic that can reveal whether the idea has a real failure mode to target.
```

## research/sto_trl/stochastic_trl_fast_prototype_plan.md

```markdown
Source document is 34324 chars, exceeding max_source_doc_chars=12000.

Headings:

# Fast Prototyping Plan: Stochastic Transitive RL
## 0. One-sentence project framing
## 1. What should count as early evidence?
## 2. Grounding in the current code and benchmarks
## 3. Algorithm variants to prototype
### Variant 0: `TRL-raw`
### Variant 1: `TRL-log`
### Variant 2: `MC-cal + TRL-log`
### Variant 3: `Successor-distance + TRL-log`
### Variant 4: `TMD + TRL-relax`
## 4. Experiment ladder
## 5. Stage A: deterministic tabular sanity check
### Purpose
### Environment A1: deterministic chain
### Environment A2: deterministic two-room maze
### Data
### Baselines
### Metrics
### Pass criteria
### Failure interpretation
## 6. Stage B: stochastic tabular tests with exact ground truth
### Shared ground truth
### Environment B1: slip chain
### Environment B2: risky shortcut vs safe route
### Environment B3: stochastic teleporter maze
### Environment B4: stochastic stitching graph
## 7. Stage C: learned tabular offline experiments
### Model classes
### Offline dataset sizes
### Losses to compare
#### C0: MC supervised
#### C1: raw TRL
#### C2: log TRL
#### C3: MC + log TRL
#### C4: contrastive successor distance
#### C5: contrastive successor distance + log TRL
### Hyperparameter sweep
### Core metrics
### Minimum result table
## 8. Stage D: tiny continuous control before OGBench
### Environment D1: continuous point navigation with stochastic wind
### Environment D2: continuous risky teleporter
### Data
### Metrics
### Pass criteria
## 9. Stage E: OGBench PointMaze teleport experiments
### Why PointMaze first?
### Recommended datasets
### Fast-run settings
### Baselines
### Implementation fork
#### `trl_log.py` changes
#### `trl_stoch.py` additions
### Screening metrics
### Pass criteria
## 10. Stage F: OGBench AntMaze teleport
### Datasets
### Baselines
### Run protocol
### Pass criteria
## 11. Ablation checklist
## 12. Diagnostics that prevent flawed conclusions
### Coverage diagnostics
### Calibration diagnostics
### Optimism diagnostics
### Policy diagnostics
### Robustness diagnostics
## 13. Milestone plan
### Milestone 1: tabular harness and deterministic reproduction
### Milestone 2: risky stochastic MDP failure test
### Milestone 3: first stochastic-calibrated variant
### Milestone 4: stochastic teleporter gridworld
### Milestone 5: continuous tiny point maze
### Milestone 6: OGBench PointMaze teleport screening
### Milestone 7: TMD comparison/integration
## 14. Practical commands and scaffolding
### TRL setup
### OGBench direct API smoke test
### Suggested tabular run commands
### Suggested result aggregation

Inspect `research/sto_trl/stochastic_trl_fast_prototype_plan.md` for full text.
```

## research/sto_trl/sto_trl_next_steps_review_plan.md

```markdown
Source document is 25255 chars, exceeding max_source_doc_chars=12000.

Headings:

# Stochastic TRL: Results Review and Next-Step Plan
## 1. Bottom line
## 2. Evidence review
### 2.1 Experiment setup quality
### 2.2 What is genuinely positive
### 2.3 What is negative or weak
## 3. My answer: should you continue?
### Continue if the project is reframed
### Do not continue the original formulation unchanged
## 4. Key conceptual pivot
### A. Long-horizon propagation
### B. Aleatoric stochasticity
### C. Epistemic uncertainty / finite offline coverage
## 5. Immediate next-step plan
# Milestone 0 — Freeze current evidence and tighten success criteria
# Milestone 1 — Identifiability and coverage grid
## Question
## Why this matters
## MDP family
## Required outputs
## Metrics
## Pass/fail interpretation
# Milestone 2 — Transition-level posterior baseline
## Question
## Why this differs from 0007
## Methods to implement
### 1. Empirical model DP
### 2. Bayesian posterior mean DP
### 3. Posterior quantile DP
### 4. Robust confidence-set DP
## Baselines
## Pass criteria
## Expected decision after this milestone
# Milestone 3 — Add transitive propagation to posterior transition models
## Question
## Design
## Critical ablation
## Pass criteria
# Milestone 4 — Randomized MDP generalization suite
## Question
## Why this matters
## MDP families
### Family A: Branch-chain MDPs
### Family B: Stochastic safe route
### Family C: Multi-branch stochastic maze
### Family D: Stochastic teleporter
## Dataset regimes
## Metrics
## Pass criteria
# Milestone 5 — One-hot neural tabular approximation
## Question
## Setup
## Metrics
## Pass criteria
# Milestone 6 — Tiny stochastic gridworld / point maze
## Question
## Start with a hand-coded gridworld
## Baselines
## Pass criteria
# Milestone 7 — OGBench/PointMaze teleport only after gates pass
## 6. Specific algorithmic directions to test
### Direction A — Keep log-TRL as a baseline, not the full method
### Direction B — Transition-posterior TRL
# Estimate transition uncertainty
# Sample transition models
# Use posterior mean or quantile for learning/action selection
### Direction C — Robust TRL lower bound
### Direction D — Bayesian risk-sensitive family
## 7. What not to do next
## 8. Recommended experiment order
## 9. Proposed decision gates
### Gate A — After Milestone 1
### Gate B — After Milestone 2
### Gate C — After Milestone 3
### Gate D — After Milestone 4
### Gate E — After Milestone 5
## 10. Concrete result table template for future summaries
## 11. Code hygiene recommendations
## 12. Suggested next experiment prompt
## 13. Final recommendation

Inspect `research/sto_trl/sto_trl_next_steps_review_plan.md` for full text.
```


## Human pivot notes

## research/sto_trl/progress/human_pivot_0008.md

```markdown
# Human Pivot 0008

The automatic loop should continue only under a reframed stochastic TRL question:

> Can transition-level stochastic uncertainty plus log-space transitive propagation produce calibrated long-horizon goal reachability under finite offline stochastic coverage?

Current evidence to preserve:

- Raw deterministic-style TRL has a real stochastic overoptimism failure mode.
- Log-TRL is a useful long-horizon propagation baseline.
- The current successor-distance plus TRL-log formulation is negative or not distinct from TRL-log.
- The hand-shaped one-sided penalty is diagnostic, not a general method.
- The generic count/Dirichlet-style uncertainty penalty reduced some Q overestimation but did not fix policy-level lucky-only regret.

Future positive criteria:

1. Preserve deterministic chain held-out MSE near zero.
2. Preserve matched safe-optimal and matched risk-optimal action choices.
3. Improve safe-optimal lucky-only policy regret versus TRL-log.
4. Avoid simply choosing safe everywhere.
5. Beat or match a simple empirical-transition-model DP baseline.
6. Show a specific benefit from transitive/log-TRL beyond transition uncertainty alone.

Recommended next experiment:

Run an identifiability and coverage grid before adding more algorithms. Sweep true risky success probability, safe path length, risky sample count, and observed risky successes. Compare empirical risky value, posterior means/quantiles, lower/upper confidence choices, TRL-log, and raw TRL. Save the grid, regret heatmaps, impossibility cases, result JSON, and summary under iteration `0008`.

The expected value of this experiment is not an algorithm win. It should identify which regimes are solvable from offline data and which require explicit priors or assumptions.
```


## Environment state

```json
{
  "blocker": null,
  "commands_run": [
    "conda env create -f research/sto_trl/environment.yaml",
    "nvidia-smi -L",
    "conda run -n autoresearcher_sto_trl python scripts/probe_jax_gpu.py --require-gpu --output research/sto_trl/setup_logs/jax_gpu_probe.json",
    "conda run -n autoresearcher_sto_trl python -c \"import sys, yaml, jsonschema, jax; print(sys.version.split()[0]); print(yaml.__version__); print(jsonschema.__version__); print(jax.__version__)\""
  ],
  "conda_env_name": "autoresearcher_sto_trl",
  "conda_env_path": "/home/eston/anaconda3/envs/autoresearcher_sto_trl",
  "environment_file": "research/sto_trl/environment.yaml",
  "gpu_available": true,
  "gpu_checks": [
    "nvidia-smi -L reported GPU 0: NVIDIA GeForce RTX 4090",
    "JAX default_backend reported gpu",
    "JAX devices reported cuda:0",
    "Tiny JAX compute returned 140.0"
  ],
  "gpu_requested": true,
  "packages_verified": [
    "python 3.11.15",
    "pyyaml 6.0.3",
    "jsonschema 4.26.0",
    "jax 0.10.1",
    "jaxlib 0.10.1",
    "jax[cuda12]"
  ],
  "project": "sto_trl",
  "status": "ready",
  "summary": "Conda environment autoresearcher_sto_trl was created from environment.yaml. JAX imports successfully, sees cuda:0, uses gpu as the default backend, and completed a tiny GPU computation."
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
  "last_pro_review_iteration": 7,
  "last_pro_review_path": null,
  "last_summary_iteration": 7,
  "last_summary_path": "research/sto_trl/progress/0007_pre_pro_local_stop_summary.md",
  "no_progress_rounds": 0,
  "notes": [
    "2026-06-13T08:58:38+00:00: supervisor decision pivot",
    "2026-06-13T09:21:15+00:00: retryable failure 1/3: reviewer failed or timed out; see /home/eston/autoresearcher/research/sto_trl/reviews/0007_review_stderr.log",
    "2026-06-13T09:29:31+00:00: supervisor decision needs_human",
    "2026-06-14T00:48:41+00:00: Pro checkpoint blocked (browser_bridge_unavailable); packet research/sto_trl/pro_packets/0008_PRO_REVIEW_PACKET.md",
    "2026-06-14T00:49:04+00:00: Pro checkpoint blocked (pro_backend_failed); packet research/sto_trl/pro_packets/0008_PRO_REVIEW_PACKET.md",
    "2026-06-14T00:49:55+00:00: Pro checkpoint blocked (browser_bridge_unavailable); packet research/sto_trl/pro_packets/0008_PRO_REVIEW_PACKET.md",
    "2026-06-14T00:56:09+00:00: Pro checkpoint blocked (browser_bridge_unavailable); packet research/sto_trl/pro_packets/0008_PRO_REVIEW_PACKET.md",
    "2026-06-14T00:56:57+00:00: Pro checkpoint blocked (browser_bridge_unavailable); packet research/sto_trl/pro_packets/0008_PRO_REVIEW_PACKET.md",
    "2026-06-14T01:08:34+00:00: Pro checkpoint blocked (browser_bridge_unavailable); packet research/sto_trl/pro_packets/0008_PRO_REVIEW_PACKET.md",
    "2026-06-14T01:25:11+00:00: Pro checkpoint blocked (login_required); packet research/sto_trl/pro_packets/0008_PRO_REVIEW_PACKET.md",
    "2026-06-14T02:45:00+00:00: resumed from human-approved stochastic TRL next-step plan; GPT-Pro cadence reset to after iteration 7",
    "2026-06-14T02:48:15+00:00: retryable failure 1/3: supervisor failed or timed out; see /home/eston/autoresearcher/research/sto_trl/decisions/0008_decision_stderr.log",
    "2026-06-14T02:48:22+00:00: retryable failure 2/3: supervisor failed or timed out; see /home/eston/autoresearcher/research/sto_trl/decisions/0008_decision_stderr.log",
    "2026-06-14T02:48:28+00:00: retry limit reached after 3/3 failures: supervisor failed or timed out; see /home/eston/autoresearcher/research/sto_trl/decisions/0008_decision_stderr.log",
    "2026-06-14T02:51:00+00:00: resumed after fixing strict structured-output schema requirements"
  ],
  "pending_checkpoint": null,
  "pending_local_decision_path": null,
  "primary_metric": null,
  "pro_review_count": 0,
  "protected_file_drift": false,
  "status": "active",
  "weak_pass_streak": 0
}
```


## Latest result summary

```json
{
  "_source": "/home/eston/autoresearcher/research/sto_trl/results/0007_result.json",
  "artifacts": [
    "research/sto_trl/artifacts/0007/run_generic_uncertainty_audit.py",
    "research/sto_trl/artifacts/0007/raw_metrics.json",
    "research/sto_trl/artifacts/0007/metrics.csv",
    "research/sto_trl/artifacts/0007/uncertainty_grid.json",
    "research/sto_trl/artifacts/0007/uncertainty_diagnostics.json",
    "research/sto_trl/artifacts/0007/offline_datasets.json",
    "research/sto_trl/artifacts/0007/transition_tables.json",
    "research/sto_trl/artifacts/0007/value_tables.json"
  ],
  "baseline_metrics": {
    "chain_len9_holdout": {
      "calibration_error": 4.336808689942018e-18,
      "chose_exact_optimal_action": true,
      "eval_goal": "c8",
      "eval_greedy_action": "right",
      "eval_start": "c0",
      "eval_start_exact_q": {
        "_type": "object",
        "key_count": 1,
        "keys": [
          "right"
        ]
      },
      "eval_start_learned_q": {
        "_type": "object",
        "key_count": 1,
        "keys": [
          "right"
        ]
      },
      "exact_optimal_action": "right",
      "heldout_long_horizon_value_mse": 2.9347503914472164e-34,
      "horizon_metrics": {
        "_type": "object",
        "key_count": 3,
        "keys": [
          "h1_train_visible",
          "h2_train_visible",
          "heldout_gt2"
        ]
      },
      "policy_regret": 0.0,
      "q_calibration_error": 4.336808689942018e-18,
      "q_overestimation_error": 5.551115123125783e-17,
      "q_underestimation_error": 0.0,
      "risky_action_selection_rate": 0.0,
      "value_mse": 1.7119377283442096e-34,
      "value_overestimation_error": 5.551115123125783e-17,
      "value_underestimation_error": 0.0
    },
    "method": "trl_log",
    "risk_optimal_matched": {
      "calibration_error": 1.734723475976807e-18,
      "chose_exact_optimal_action": true,
      "eval_goal": "goal",
      "eval_greedy_action": "risky",
      "eval_start": "start",
      "eval_start_exact_q": {
        "_type": "object",
        "key_count": 2,
        "keys": [
          "risky",
          "safe"
        ]
      },
      "eval_start_learned_q": {
        "_type": "object",
        "key_count": 2,
        "keys": [
          "risky",
          "safe"
        ]
      },
      "exact_optimal_action": "risky",
      "heldout_long_horizon_value_mse": 0.0,
      "horizon_metrics": {
        "_type": "object",
        "key_count": 4,
        "keys": [
          "h1_train_visible",
          "h2_train_visible",
          "heldout_gt2",
          "unreachable"
        ]
      },
      "policy_regret": 0.0,
      "q_calibration_error": 1.734723475976807e-18,
      "q_overestimation_error": 2.7755575615628914e-17,
      "q_underestimation_error": 0.0,
      "risky_action_selection_rate": 1.0,
      "value_mse": 3.851859888774472e-35,
      "value_overestimation_error": 2.7755575615628914e-17,
      "value_underestimation_error": 0.0
    },
    "safe_optimal_lucky_only_stress": {
      "calibration_error": 0.084375,
      "chose_exact_optimal_action": false,
      "eval_goal": "goal",
      "eval_greedy_action": "risky",
      "eval_start": "start",
      "eval_start_exact_q": {
        "_type": "object",
        "key_count": 2,
        "keys": [
          "risky",
          "safe"
        ]
      },
      "eval_start_learned_q": {
        "_type": "object",
        "key_count": 2,
        "keys": [
          "risky",
          "safe"
        ]
      },
      "exact_optimal_action": "safe",
      "heldout_long_horizon_value_mse": 0.029240999999999975,
      "horizon_metrics": {
        "_type": "object",
        "key_count": 4,
        "keys": [
          "h1_train_visible",
          "h2_train_visible",
          "heldout_gt2",
          "unreachable"
        ]
      },
      "policy_regret": 0.5040000000000001,
      "q_calibration_error": 0.084375,
      "q_overestimation_error": 0.675,
      "q_underestimation_error": 0.675,
      "risky_action_selection_rate": 1.0,
      "value_mse": 0.024243300000000002,
      "value_overestimation_error": 0.17099999999999993,
      "value_underestimation_error": 0.675
    }
  },
  "claim_tested": "A generic count-based posterior branch-uncertainty penalty can replace the hand-shaped 0006 shortcut rule while reducing lucky-only overestimation and preserving matched risk-optimal behavior.",
  "experiment_id": "0007",
  "interpretation": "generic_dirichlet_unknown_prior_0_50_alpha_0_50 reduced safe-optimal lucky-only overestimation versus trl_log while preserving the chain and selecting risky with zero regret in the matched risk-optimal scenario. The risk-optimal no-success stress status is reported separately.",
  "known_failures": [],
  "metrics": {
    "aggregate": {
      "best_positive_method": "generic_dirichlet_unknown_prior_0_50_alpha_0_50",
      "generic_summaries": {
        "_type": "object",
        "key_count": 6,
        "keys": [
          "generic_dirichlet_unknown_prior_0_50_alpha_0_00",
          "generic_dirichlet_unknown_prior_0_50_alpha_0_50",
          "generic_dirichlet_unknown_prior_0_50_alpha_1_00",
          "generic_dirichlet_unknown_prior_1_00_alpha_0_00",
          "generic_dirichlet_unknown_prior_1_00_alpha_0_50",
          "generic_dirichlet_unknown_prior_1_00_alpha_1_00"
        ]
      },
      "one_sided_0006_safe_lucky_policy_regret": 0.0,
      "one_sided_0006_safe_lucky_q_overestimation": 0.495,
      "positive_generic_uncertainty_evidence": true,
      "risk_optimal_no_success_unsolved_by_best_positive": true,
      "trl_log_safe_lucky_policy_regret": 0.5040000000000001,
      "trl_log_safe_lucky_q_overestimation": 0.675
    },
    "best_0006_alpha": 0.4,
    "experiment_id": "0007",
    "gamma": 0.9,
    "generic_alpha_grid": [
      0.0,
      0.5,
      1.0
    ],
    "generic_prior_grid": [
      0.5,
      1.0
    ],
    "label_horizon_cutoff": 2,
    "scenarios": {
      "chain_len9_holdout": {
        "_type": "object",
        "key_count": 6,
        "keys": [
          "coverage_diagnostics",
          "label_or_pair_coverage",
          "mdp",
          "methods",
          "scenario_role",
          "uncertainty_meta"
        ]
      },
      "risk_optimal_matched": {
        "_type": "object",
        "key_count": 6,
        "keys": [
          "coverage_diagnostics",
          "label_or_pair_coverage",
          "mdp",
          "methods",
          "scenario_role",
          "uncertainty_meta"
        ]
      },
      "risk_optimal_no_success_stress": {
        "_type": "object",
        "key_count": 6,
        "keys": [
          "coverage_diagnostics",
          "label_or_pair_coverage",
          "mdp",
          "methods",
          "scenario_role",
          "uncertainty_meta"
        ]
      },
      "safe_optimal_lucky_only_stress": {
        "_type": "object",
        "key_count": 6,
        "keys": [
          "coverage_diagnostics",
          "label_or_pair_coverage",
          "mdp",
          "methods",
          "scenario_role",
          "uncertainty_meta"
        ]
      },
      "safe_optimal_matched": {
        "_type": "object",
        "key_count": 6,
        "keys": [
          "coverage_diagnostics",
          "label_or_pair_coverage",
          "mdp",
          "methods",
          "scenario_role",
          "uncertainty_meta"
        ]
      }
    },
    "success_checks": {
      "chain_raw_exact": true,
      "chain_trl_log_exact": true,
      "experiment_completed": true,
      "generic_grid_completed": true,
      "positive_generic_uncertainty_evidence": true
    },
    "successor_baseline_lambda": 0.25,
    "update_steps": 32
  },
  "next_questions": [
    "Can a generic prior preserve multi-step safe routes without also discounting them below lucky shortcuts?",
    "Should no-success risk-optimal regimes be handled by explicit optimistic priors rather than stronger conservative penalties?",
    "Would bootstrap branch uncertainty distinguish deterministic safe routes from all-success risky shortcuts better than the unknown-outcome prior?"
  ],
  "status": "completed"
}
```


## Latest summary

# Experiment 0007 Summary

## Objective

Audit a generic count-based posterior uncertainty penalty against the 0006 one-sided conservative rule.

## Commands Run

```bash
mkdir -p research/sto_trl/artifacts/0007 research/sto_trl/results && cp research/sto_trl/artifacts/0006/run_uncertainty_conservative_log_trl.py research/sto_trl/artifacts/0007/run_generic_uncertainty_audit.py
conda run -n autoresearcher_sto_trl python research/sto_trl/artifacts/0007/run_generic_uncertainty_audit.py
conda run -n autoresearcher_sto_trl python scripts/validate_artifacts.py --repo-root . --json research/sto_trl/results/0007_result.json --schema schemas/result.schema.json --check-result-artifacts
```

## Setup

- Discount: `0.9`
- Label horizon cutoff: `2`
- Fixed backup iterations: `32`
- Prior grid: `[0.5, 1.0]`
- Alpha grid: `[0.0, 0.5, 1.0]`
- Generic penalty: interpolate empirical log backup with a Dirichlet unknown-zero posterior lower estimate for state-action counts at least 4.

## Metrics

| Scenario | Method | Prior | Alpha | Held-out MSE | Q calibration | Policy regret | Action | Risky selected |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- | ---: |
| chain_len9_holdout | mc_supervised | None | None | 0.391705823230 | 0.465607869047 | 0.000000000000 | right | 0.0 |
| chain_len9_holdout | trl_raw | None | None | 0.000000000000 | 0.000000000000 | 0.000000000000 | right | 0.0 |
| chain_len9_holdout | trl_log | None | None | 0.000000000000 | 0.000000000000 | 0.000000000000 | right | 0.0 |
| chain_len9_holdout | mc_plus_trl_log | None | None | 0.000000000000 | 0.131258278195 | 0.000000000000 | right | 0.0 |
| chain_len9_holdout | successor_distance_best_0005 | None | None | 0.000000000000 | 0.000000000000 | 0.000000000000 | right | 0.0 |
| chain_len9_holdout | one_sided_conservative_log_trl_alpha_0_40 | None | 0.4 | 0.000000000000 | 0.000000000000 | 0.000000000000 | right | 0.0 |
| chain_len9_holdout | generic_dirichlet_unknown_prior_0_50_alpha_0_00 | 0.5 | 0.0 | 0.000000000000 | 0.000000000000 | 0.000000000000 | right | 0.0 |
| chain_len9_holdout | generic_dirichlet_unknown_prior_0_50_alpha_0_50 | 0.5 | 0.5 | 0.000000000000 | 0.000000000000 | 0.000000000000 | right | 0.0 |
| chain_len9_holdout | generic_dirichlet_unknown_prior_0_50_alpha_1_00 | 0.5 | 1.0 | 0.000000000000 | 0.000000000000 | 0.000000000000 | right | 0.0 |
| chain_len9_holdout | generic_dirichlet_unknown_prior_1_00_alpha_0_00 | 1.0 | 0.0 | 0.000000000000 | 0.000000000000 | 0.000000000000 | right | 0.0 |
| chain_len9_holdout | generic_dirichlet_unknown_prior_1_00_alpha_0_50 | 1.0 | 0.5 | 0.000000000000 | 0.000000000000 | 0.000000000000 | right | 0.0 |
| chain_len9_holdout | generic_dirichlet_unknown_prior_1_00_alpha_1_00 | 1.0 | 1.0 | 0.000000000000 | 0.000000000000 | 0.000000000000 | right | 0.0 |
| safe_optimal_matched | mc_supervised | None | None | 0.254016000000 | 0.045562500000 | 0.504000000000 | risky | 1.0 |
| safe_optimal_matched | trl_raw | None | None | 0.029241000000 | 0.056250000000 | 0.504000000000 | risky | 1.0 |
| safe_optimal_matched | trl_log | None | None | 0.000000000000 | 0.000000000000 | 0.000000000000 | safe | 0.0 |
| safe_optimal_matched | mc_plus_trl_log | None | None | 0.000000000000 | 0.000000000000 | 0.000000000000 | safe | 0.0 |
| safe_optimal_matched | successor_distance_best_0005 | None | None | 0.000000000000 | 0.000000000000 | 0.000000000000 | safe | 0.0 |
| safe_optimal_matched | one_sided_conservative_log_trl_alpha_0_40 | None | 0.4 | 0.000000000000 | 0.011250000000 | 0.000000000000 | safe | 0.0 |
| safe_optimal_matched | generic_dirichlet_unknown_prior_0_50_alpha_0_00 | 0.5 | 0.0 | 0.000000000000 | 0.000000000000 | 0.000000000000 | safe | 0.0 |
| safe_optimal_matched | generic_dirichlet_unknown_prior_0_50_alpha_0_50 | 0.5 | 0.5 | 0.013196265625 | 0.029146599265 | 0.000000000000 | safe | 0.0 |
| safe_optimal_matched | generic_dirichlet_unknown_prior_0_50_alpha_1_00 | 0.5 | 1.0 | 0.047089000000 | 0.056871323529 | 0.000000000000 | safe | 0.0 |
| safe_optimal_matched | generic_dirichlet_unknown_prior_1_00_alpha_0_00 | 1.0 | 0.0 | 0.000000000000 | 0.000000000000 | 0.000000000000 | safe | 0.0 |
| safe_optimal_matched | generic_dirichlet_unknown_prior_1_00_alpha_0_50 | 1.0 | 0.5 | 0.039029558481 | 0.051584937500 | 0.000000000000 | safe | 0.0 |
| safe_optimal_matched | generic_dirichlet_unknown_prior_1_00_alpha_1_00 | 1.0 | 1.0 | 0.126559485504 | 0.098684500000 | 0.000000000000 | safe | 0.0 |
| risk_optimal_matched | mc_supervised | None | None | 0.000000000000 | 0.045562500000 | 0.000000000000 | risky | 1.0 |
| risk_optimal_matched | trl_raw | None | None | 0.000000000000 | 0.056250000000 | 0.000000000000 | risky | 1.0 |
| risk_optimal_matched | trl_log | None | None | 0.000000000000 | 0.000000000000 | 0.000000000000 | risky | 1.0 |
| risk_optimal_matched | mc_plus_trl_log | None | None | 0.000000000000 | 0.000000000000 | 0.000000000000 | risky | 1.0 |
| risk_optimal_matched | successor_distance_best_0005 | None | None | 0.000000000000 | 0.000000000000 | 0.000000000000 | risky | 1.0 |
| risk_optimal_matched | one_sided_conservative_log_trl_alpha_0_40 | None | 0.4 | 0.000000000000 | 0.011250000000 | 0.000000000000 | risky | 1.0 |
| risk_optimal_matched | generic_dirichlet_unknown_prior_0_50_alpha_0_00 | 0.5 | 0.0 | 0.000000000000 | 0.000000000000 | 0.000000000000 | risky | 1.0 |
| risk_optimal_matched | generic_dirichlet_unknown_prior_0_50_alpha_0_50 | 0.5 | 0.5 | 0.000000000000 | 0.028831473214 | 0.000000000000 | risky | 1.0 |
| risk_optimal_matched | generic_dirichlet_unknown_prior_0_50_alpha_1_00 | 0.5 | 1.0 | 0.000000000000 | 0.056241071429 | 0.000000000000 | risky | 1.0 |
| risk_optimal_matched | generic_dirichlet_unknown_prior_1_00_alpha_0_00 | 1.0 | 0.0 | 0.000000000000 | 0.000000000000 | 0.000000000000 | risky | 1.0 |
| risk_optimal_matched | generic_dirichlet_unknown_prior_1_00_alpha_0_50 | 1.0 | 0.5 | 0.000000000000 | 0.051016755682 | 0.000000000000 | risky | 1.0 |
| risk_optimal_matched | gen

_Trimmed to 6000 chars; inspect the source file for full text._


## Latest review summary

```json
{
  "allows_auto_continue": true,
  "evidence_checked": {
    "_type": "list",
    "first_items": [
      "research/sto_trl/results/0007_result.json",
      "research/sto_trl/results/0007_summary.md",
      "research/sto_trl/artifacts/0007/run_generic_uncertainty_audit.py"
    ],
    "length": 13
  },
  "experiment_id": "0007",
  "reasons": [
    "Required result, summary, and listed 0007 artifacts are present, and result validation returned ok.",
    "The executor used the same five 0006 scenarios; 0007 offline_datasets.json and transition_tables.json match 0006 byte-for-byte, so the comparisons are on the same datasets.",
    "metrics.csv includes all required baselines, the 0006 one-sided comparison row, and the full generic grid: two priors by three alphas, including zero-penalty baselines.",
    "The generic method is count-based and does not use the 0006 direct-goal shortcut eligibility rule for its new variants; exact DP appears confined to evaluation ground truth.",
    "The positive result is narrow: the selected generic variant reduces safe_optimal_lucky_only Q overestimation versus trl_log, preserves chain recovery, and keeps zero regret in risk_optimal_matched.",
    "Interpretation is somewhat optimistic because safe_optimal_lucky_only policy regret is unchanged from trl_log at 0.504 and the method still selects risky there; it is also worse than the 0006 one-sided alpha 0.40 comparison on that stress case.",
    "risk_optimal_no_success_stress remains unsolved by the generic variants and should be treated as a continuing limitation, even though the summary reports it separately."
  ],
  "required_fixes": [],
  "risk_flags": [
    "Do not treat 0007 as showing that the generic method fully replaces the 0006 one-sided rule; it only gives modest Q-overestimation reduction without fixing lucky-only policy regret.",
    "known_failures is empty despite risk_optimal_no_success_stress remaining unsolved; this is acceptable for continuation only because the limitation is explicit in metrics and summary.",
    "The current worktree has unrelated uncommitted modifications to scripts/autoresearcher.py, but the 0007 result commit did not include that protected file."
  ],
  "verdict": "weak_pass"
}
```


## Metric ledger

```json
{
  "iterations": [
    {
      "allows_auto_continue": true,
      "claim_tested": "A tiny stochastic risky-shortcut MDP exposes overestimation by deterministic raw TRL backups, while log-space stochastic backups preserve deterministic-chain behavior and improve risky-action calibration relative to raw TRL.",
      "decision": "continue",
      "important_metrics": {
        "metrics.mdps.deterministic_chain.coverage_diagnostics.risky_failure_count": 0,
        "metrics.mdps.deterministic_chain.coverage_diagnostics.risky_success_count": 0,
        "metrics.mdps.deterministic_chain.coverage_diagnostics.risky_success_rate_observed": null,
        "metrics.mdps.deterministic_chain.methods.mc_plus_trl_log.calibration_error": 0.13193442000000005,
        "metrics.mdps.deterministic_chain.methods.mc_plus_trl_log.eval_start_exact_q.right": 0.5904900000000002,
        "metrics.mdps.deterministic_chain.methods.mc_plus_trl_log.eval_start_exact_value": 0.5904900000000002,
        "metrics.mdps.deterministic_chain.methods.mc_plus_trl_log.long_horizon_value_mse": 0.0,
        "metrics.mdps.deterministic_chain.methods.mc_plus_trl_log.max_policy_regret": 0.0,
        "metrics.mdps.deterministic_chain.methods.mc_plus_trl_log.mean_policy_regret": 0.0,
        "metrics.mdps.deterministic_chain.methods.mc_plus_trl_log.policy_regret": 0.0,
        "metrics.mdps.deterministic_chain.methods.mc_plus_trl_log.q_calibration_error": 0.13193442000000005,
        "metrics.mdps.deterministic_chain.methods.mc_plus_trl_log.q_overestimation_error": 0.0
      },
      "iteration": "0001",
      "negative_signals": [
        "Evidence is intentionally small-scale and balanced: risky outcome coverage exactly matches the true 0.25 success probability, so MC supervised is perfect here and the experiment mainly supports the raw-TRL overestimation...",
        "/home/eston/autoresearcher is not a git repository, so unrelated modifications could not be audited with git status."
      ],
      "positive_signals": [
        "The deterministic chain sanity check was recovered by both raw and log TRL. On the risky-shortcut MDP, raw deterministic-style TRL treated the observed lucky risky edge as reliable and selected risky with Q=0.900000 versus exact Q=0.225000. The empirical log b"
      ],
      "review_verdict": "pass",
      "status": "completed"
    },
    {
      "allows_auto_continue": true,
      "claim_tested": "Raw TRL overestimation is support-driven under stochastic coverage, while empirical MC/log methods are calibrated only when observed risky branch frequencies match the true MDP; a risk-optimal setting tests for conservative avoidance.",
      "decision": "continue",
      "important_metrics": {
        "metrics.aggregate.mc_supervised_mean_policy_regret": 0.0666,
        "metrics.aggregate.num_risky_scenarios": 10,
        "metrics.aggregate.raw_no_success_scenarios": 2,
        "metrics.aggregate.raw_selected_risky_when_no_success_observed": 0,
        "metrics.aggregate.raw_selected_risky_when_success_observed": 8,
        "metrics.aggregate.raw_success_observed_scenarios": 8,
        "metrics.aggregate.trl_log_mean_policy_regret": 0.0666,
        "metrics.aggregate.trl_raw_mean_policy_regret": 0.20970000000000005,
        "metrics.regime_specs.risk_optimal.lucky_biased.risky_failures": 0,
        "metrics.regime_specs.risk_optimal.lucky_biased.risky_successes": 9,
        "metrics.regime_specs.risk_optimal.lucky_only.risky_failures": 0,
        "metrics.regime_specs.risk_optimal.lucky_only.risky_successes": 4
      },
      "iteration": "0002",
      "negative_signals": [
        "The Q overestimation and underestimation maxima are computed across all goals, not only the eval goal, so those headline error fields can reflect non-eval goals such as trap; eval-goal learned/exact Q columns mitigate th...",
        "commands_run records setup, execution, and validation commands but not the manual edits that transformed the copied 0001 script into the 0002 harness.",
        "git status only showed an untracked reviewer packet, but without committed baselines this review cannot fully prove no prior artifacts were modified."
      ],
      "positive_signals": [
        "The chain guard still recovered exact discounted reachability for raw and log TRL. Across risky regimes, raw TRL selected risky in every scenario with at least one observed lucky risky transition and did not select risky when no lucky risky transition was obse"
      ],
      "review_verdict": "pass",
      "status": "completed"
    },
    {
      "allows_auto_continue": true,
      "claim_tested": "Censoring long-horizon MC labels makes MC-only underpredict held-out discounted reachability, while log transitive backups recover longer horizons and keep matched risky-branch calibration.",
      "decision": "continue",
      "important_metrics": {
        "metrics.aggregate.chain_mc_heldout_value_mse": 0.3917058232298766,
        "metrics.aggregate.chain_mc_plus_trl_log_heldout_value_mse": 2.9347503914472164e-34,
        "metrics.aggregate.chain_trl_log_heldout_value_mse": 2.9347503914472164e-34,
        "metrics.aggregate.risky_mc_heldout_value_mse": 0.25401600000000013,
        "metrics.aggregate.risky_mc_plus_trl_log_heldout_value_mse": 0.0,
        "metrics.aggregate.risky_mc_plus_trl_log_policy_regret": 0.0,
        "metrics.aggregate.risky_trl_log_heldout_value_mse": 0.0,
        "metrics.aggregate.risky_trl_log_policy_regret": 0.0,
        "metrics.aggregate.risky_trl_raw_policy_regret": 0.5040000000000001,
        "metrics.scenarios.chain_len9.coverage_diagnostics.risky_failure_count": 0,
        "metrics.scenarios.chain_len9.coverage_diagnostics.risky_success_count": 0,
        "metrics.scenarios.chain_len9.coverage_diagnostics.risky_success_rate_observed": null
      },
      "iteration": "0003",
      "negative_signals": [
        "git status shows modified control files including scripts/autoresearcher.py, autoresearcher.yaml, tests/test_phase1.py, and research/sto_trl/state.json. Their mtimes precede the 0003 plan, so they appear pre-existing to...",
        "commands_run records setup, execution, and validation commands, but not the manual edit operation that adapted the copied 0002 script into the 0003 harness.",
        "TRL-log and raw TRL are transitive model-based tabular backups over observed transitions, so they do not consume the same supervised label budget as MC-only; this is intended by the plan but should be kept in mind when i..."
      ],
      "positive_signals": [
        "With positive labels beyond horizon 2 censored, MC-supervised underpredicted held-out long-horizon reachability. TRL-log and MC+TRL-log propagated through observed transitions and reduced held-out value MSE on the longer chain and the matched risky MDP. In the"
      ],
      "review_verdict": "weak_pass",
      "status": "completed"
    },
    {
      "allows_auto_continue": true,
      "claim_tested": "A self-normalized successor-distance calibration with log-space transitive relaxation improves held-out reachability versus calibration-only without increasing matched risky overestimation or avoiding truly optimal risky actions.",
      "decision": "continue",
      "important_metrics": {
        "metrics.aggregate.risk_matched_successor_calibration_only_policy_regret": 0.0,
        "metrics.aggregate.risk_matched_successor_distance_trl_log_policy_regret": 0.0,
        "metrics.aggregate.safe_lucky_stress_successor_distance_action": "risky",
        "metrics.aggregate.safe_matched_successor_calibration_only_policy_regret": 0.5040000000000001,
        "metrics.aggregate.safe_matched_successor_distance_trl_log_policy_regret": 0.0,
        "metrics.aggregate.successor_calibration_only_main_mean_heldout_mse": 0.21524060774329223,
        "metrics.aggregate.successor_distance_trl_log_main_mean_heldout_mse": 9.782501304824055e-35,
        "metrics.scenarios.chain_len9_holdout.coverage_diagnostics.risky_failure_count": 0,
        "metrics.scenarios.chain_len9_holdout.coverage_diagnostics.risky_success_count": 0,
        "metrics.scenarios.chain_len9_holdout.coverage_diagnostics.risky_success_rate_observed": null,
        "metrics.scenarios.chain_len9_holdout.label_or_pair_coverage.censored_examples.0.positive_horizon": 3,
        "metrics.scenarios.chain_len9_holdout.label_or_pair_coverage.censored_examples.1.positive_horizon": 4
      },
      "iteration": "0004",
      "negative_signals": [
        "successor_distance_trl_log is behaviorally identical or near-identical to trl_log in the saved main metrics, so the result supports the calibration-only versus transitive-relaxation ablation but not a clear advantage ove...",
        "self_normalize_successor_scores divides by max([scores] + [1.0]), which is an identity transform for scores already in [0,1]; successor_calibration_only therefore matches mc_supervised in these runs.",
        "git status still shows modified control/config/test files, including scripts/autoresearcher.py and autoresearcher.yaml. Their mtimes predate the 0004 artifact generation, but the dirty tree means the no-control-file-edit...",
        "commands_run records the copy, execution, and validation commands but not the manual edits that adapted the copied 0003 script into the 0004 successor-distance harness."
      ],
      "positive_signals": [
        "The successor-distance transitive relaxation improved main held-out long-horizon value MSE over calibration-only. On matched safe-optimal risky coverage it selected safe with no policy-regret increase versus calibration-only, and on matched risk-optimal covera"
      ],
      "review_verdict": "weak_pass",
      "status": "completed"
    },
    {
      "allows_auto_continue": true,
      "claim_tested": "A successor-distance lambda sweep can reveal whether successor_distance_trl_log has a distinct effect beyond trl_log while retaining calibration and lower held-out error than calibration-only.",
      "decision": "continue",
      "important_metrics": {
        "metrics.aggregate.any_positive_successor_evidence": false,
        "metrics.aggregate.lambda_summaries.successor_distance_trl_log_lambda_0_00.equivalent_to_trl_log_all_main": false,
        "metrics.aggregate.lambda_summaries.successor_distance_trl_log_lambda_0_00.improves_vs_calibration_only": false,
        "metrics.aggregate.lambda_summaries.successor_distance_trl_log_lambda_0_00.lambda_tr": 0.0,
        "metrics.aggregate.lambda_summaries.successor_distance_trl_log_lambda_0_00.main_mean_heldout_mse": 0.21524060774329223,
        "metrics.aggregate.lambda_summaries.successor_distance_trl_log_lambda_0_00.matched_no_policy_regret_increase_vs_calibration_only": true,
        "metrics.aggregate.lambda_summaries.successor_distance_trl_log_lambda_0_00.matched_no_q_overestimation_increase_vs_calibration_only": true,
        "metrics.aggregate.lambda_summaries.successor_distance_trl_log_lambda_0_00.non_equivalent_to_trl_log_any_main": true,
        "metrics.aggregate.lambda_summaries.successor_distance_trl_log_lambda_0_00.positive_successor_evidence": false,
        "metrics.aggregate.lambda_summaries.successor_distance_trl_log_lambda_0_00.risk_optimal_selects_risky": true,
        "metrics.aggregate.lambda_summaries.successor_distance_trl_log_lambda_0_25.equivalent_to_trl_log_all_main": true,
        "metrics.aggregate.lambda_summaries.successor_distance_trl_log_lambda_0_25.improves_vs_calibration_only": true
      },
      "iteration": "0005",
      "negative_signals": [
        "Working tree contains pre-existing modified control/config/test files, including scripts/autoresearcher.py, so the no-control-file-edit criterion cannot be proven from git status alone.",
        "commands_run records copy, run, and validation commands, but not any manual edit steps used to adapt the copied 0004 script into the 0005 audit.",
        "A generated __pycache__/ directory exists under artifacts/0005; harmless but extra artifact noise.",
        "Supervisor should continue only treating 0005 as negative evidence for distinct successor-distance value, not as support for the prior positive 0004 interpretation."
      ],
      "positive_signals": [
        "The audit found negative successor-distance evidence: improving lambdas reduced held-out error by matching trl_log within the predeclared tolerance, so this variant is not yet distinct from trl_log on these tabular diagnostics."
      ],
      "review_verdict": "pass",
      "status": "completed"
    },
    {
      "allows_auto_continue": true,
      "claim_tested": "A one-sided count-based conservative log-TRL backup can reduce lucky-only risky overestimation without breaking deterministic recovery or matched risk-optimal action selection.",
      "decision": "pivot",
      "important_metrics": {
        "metrics.aggregate.alpha_summaries.one_sided_conservative_log_trl_alpha_0_00.chain_heldout_mse": 2.9347503914472164e-34,
        "metrics.aggregate.alpha_summaries.one_sided_conservative_log_trl_alpha_0_00.lucky_q_overestimation_reduced_vs_trl_log": false,
        "metrics.aggregate.alpha_summaries.one_sided_conservative_log_trl_alpha_0_00.lucky_regret_reduced_vs_trl_log": false,
        "metrics.aggregate.alpha_summaries.one_sided_conservative_log_trl_alpha_0_00.positive_uncertainty_evidence": false,
        "metrics.aggregate.alpha_summaries.one_sided_conservative_log_trl_alpha_0_00.risk_optimal_matched_action": "risky",
        "metrics.aggregate.alpha_summaries.one_sided_conservative_log_trl_alpha_0_00.risk_optimal_matched_ok": true,
        "metrics.aggregate.alpha_summaries.one_sided_conservative_log_trl_alpha_0_00.risk_optimal_matched_policy_regret": 0.0,
        "metrics.aggregate.alpha_summaries.one_sided_conservative_log_trl_alpha_0_00.safe_optimal_lucky_policy_regret": 0.5040000000000001,
        "metrics.aggregate.alpha_summaries.one_sided_conservative_log_trl_alpha_0_00.safe_optimal_lucky_q_overestimation": 0.675,
        "metrics.aggregate.alpha_summaries.one_sided_conservative_log_trl_alpha_0_20.chain_heldout_mse": 2.9347503914472164e-34,
        "metrics.aggregate.alpha_summaries.one_sided_conservative_log_trl_alpha_0_20.lucky_q_overestimation_reduced_vs_trl_log": true,
        "metrics.aggregate.alpha_summaries.one_sided_conservative_log_trl_alpha_0_20.lucky_regret_reduced_vs_trl_log": false
      },
      "iteration": "0006",
      "negative_signals": [
        "The aggregate labels one_sided_conservative_log_trl_alpha_0_20 as best_positive_method even though alpha 0.40 and 0.60 also eliminate lucky-only policy regret; this is a first-positive selection, not a best-by-regret sel...",
        "The interpretation says alpha 0.20 reduced the lucky-only safe-optimal failure, but alpha 0.20 still selects risky with policy regret 0.504; the stronger claim should be limited to reduced overestimation/held-out MSE unl...",
        "The risk_optimal_no_success_stress case remains a biased-coverage failure for trl_log and all conservative alpha values: they select safe with regret 0.081 despite the true risky optimum.",
        "The penalty eligibility rule is hand-shaped around direct-goal single-branch shortcut actions at multi-action states, so evidence may not generalize beyond these toy diagnostics."
      ],
      "positive_signals": [
        "one_sided_conservative_log_trl_alpha_0_20 reduced the lucky-only safe-optimal failure versus trl_log while preserving the chain and selecting risky with zero regret in the matched risk-optimal scenario."
      ],
      "review_verdict": "weak_pass",
      "status": "completed"
    },
    {
      "allows_auto_continue": true,
      "claim_tested": "A generic count-based posterior branch-uncertainty penalty can replace the hand-shaped 0006 shortcut rule while reducing lucky-only overestimation and preserving matched risk-optimal behavior.",
      "decision": "needs_human",
      "important_metrics": {
        "metrics.aggregate.best_positive_method": "generic_dirichlet_unknown_prior_0_50_alpha_0_50",
        "metrics.aggregate.generic_summaries.generic_dirichlet_unknown_prior_0_50_alpha_0_00.chain_heldout_mse": 2.9347503914472164e-34,
        "metrics.aggregate.generic_summaries.generic_dirichlet_unknown_prior_0_50_alpha_0_00.lucky_policy_regret_delta_vs_one_sided_0006": 0.5040000000000001,
        "metrics.aggregate.generic_summaries.generic_dirichlet_unknown_prior_0_50_alpha_0_00.lucky_policy_regret_delta_vs_trl_log": 0.0,
        "metrics.aggregate.generic_summaries.generic_dirichlet_unknown_prior_0_50_alpha_0_00.lucky_q_overestimation_delta_vs_one_sided_0006": 0.18000000000000005,
        "metrics.aggregate.generic_summaries.generic_dirichlet_unknown_prior_0_50_alpha_0_00.lucky_q_overestimation_delta_vs_trl_log": 0.0,
        "metrics.aggregate.generic_summaries.generic_dirichlet_unknown_prior_0_50_alpha_0_00.positive_generic_uncertainty_evidence": false,
        "metrics.aggregate.generic_summaries.generic_dirichlet_unknown_prior_0_50_alpha_0_00.risk_no_success_policy_regret_delta_vs_one_sided_0006": 0.0,
        "metrics.aggregate.generic_summaries.generic_dirichlet_unknown_prior_0_50_alpha_0_00.risk_no_success_policy_regret_delta_vs_trl_log": 0.0,
        "metrics.aggregate.generic_summaries.generic_dirichlet_unknown_prior_0_50_alpha_0_00.risk_optimal_matched_action": "risky",
        "metrics.aggregate.generic_summaries.generic_dirichlet_unknown_prior_0_50_alpha_0_00.risk_optimal_matched_ok": true,
        "metrics.aggregate.generic_summaries.generic_dirichlet_unknown_prior_0_50_alpha_0_00.risk_optimal_matched_policy_regret": 0.0
      },
      "iteration": "0007",
      "negative_signals": [
        "Do not treat 0007 as showing that the generic method fully replaces the 0006 one-sided rule; it only gives modest Q-overestimation reduction without fixing lucky-only policy regret.",
        "known_failures is empty despite risk_optimal_no_success_stress remaining unsolved; this is acceptable for continuation only because the limitation is explicit in metrics and summary.",
        "The current worktree has unrelated uncommitted modifications to scripts/autoresearcher.py, but the 0007 result commit did not include that protected file."
      ],
      "positive_signals": [
        "generic_dirichlet_unknown_prior_0_50_alpha_0_50 reduced safe-optimal lucky-only overestimation versus trl_log while preserving the chain and selecting risky with zero regret in the matched risk-optimal scenario. The risk-optimal no-success stress status is rep"
      ],
      "review_verdict": "weak_pass",
      "status": "completed"
    }
  ],
  "project": "sto_trl"
}
```


## Last decision summaries

## 0005_decision.json

```json
{
  "confidence": 0.8,
  "decision": "continue",
  "evidence": [
    "research/sto_trl/results/0004_result.json validates against schemas/result.schema.json with artifact checks.",
    "0004 success checks report successor_distance_improves_main_heldout_mse_vs_calibration_only=true and no matched policy-regret or Q-overestimation increase versus calibration-only.",
    "0004 aggregate metrics show successor_calibration_only main mean held-out MSE 0.21524060774329223 versus successor_distance_trl_log 9.782501304824055e-35.",
    "0004 matched safe-optimal metrics show successor_distance_trl_log selected safe with zero policy regret, while calibration-only selected risky with policy_regret=0.504.",
    "0004 matched risk-optimal metrics show successor_distance_trl_log selected risky with zero policy regret, so it did not simply avoid risk under matched coverage.",
    "The 0004 review flags two key weaknesses: successor_distance_trl_log is near-identical to trl_log in the main metrics, and self_normalize_successor_scores is an identity transform for scores already in [0,1].",
    "The 0004 lucky-only stress scenario remains a failure case: successor_distance_trl_log selected risky with policy_regret=0.504 under biased safe-optimal coverage."
  ],
  "next_experiment": {
    "estimated_runtime_minutes": 20,
    "experiment_id": "0005",
    "hypothesis": "If the successor-distance formulation is meaningful rather than a relabeling of trl_log, then some predeclared lambda_tr value should change Q/value tables or policy behavior relative to trl_log while retaining lower held-out error than calibration-only and avoiding matched risky-branch overestimation. If all lambda_tr values collapse to trl_log or calibration-only, the successor-distance variant is not yet adding distinct evidence.",
    "objective": "Run a small successor-distance lambda and equivalence audit to determine whether successor_distance_trl_log has a distinct effect beyond trl_log and calibration-only on the existing tabular chain and risky-shortcut diagnostics.",
    "required_outputs": [
      "research/sto_trl/artifacts/0005/run_successor_lambda_equivalence.py",
      "research/sto_trl/artifacts/0005/raw_metrics.json",
      "research/sto_trl/artifacts/0005/metrics.csv",
      "research/sto_trl/artifacts/0005/lambda_sweep.json",
      "research/sto_trl/artifacts/0005/equivalence_diagnostics.json",
      "research/sto_trl/artifacts/0005/successor_distance_tables.json",
      "research/sto_trl/results/0005_result.json",
      "research/sto_trl/results/0005_summary.md"
    ]
  },
  "progress_score": 6,
  "rationale": "Experiment 0004 is valid but only a weak positive for the successor-distance direction. It shows calibrated+transitive beats calibration-only on the tabular main scenarios, but the review and code indicate successor_calibration_only is effectively MC-supervised and successor_distance_trl_log is behaviorally near-identical to trl_log. The next cheap decisive experiment should audit whether the successor-distance formulation has any distinct effect across transitive weights before moving to function approximation or larger tasks.",
  "risks": [
    "Continuing without an equivalence audit could mistake ordinary trl_log behavior for evidence supporting a distinct successor-distance method.",
    "A lambda sweep can become low-value if it only repeats calibration-only comparisons; require explicit distance-to-trl_log diagnostics.",
    "No tabular method should be expected to solve missing-outcome lucky-only coverage without an uncertainty assumption, so that stress case should be used as a boundary diagnostic, not a sole success criterion.",
    "Do not move to OGBench, neural networks, or broad sweeps while the tabular method distinction is unresolved."
  ]
}
```

## 0006_decision.json

```json
{
  "confidence": 0.82,
  "decision": "pivot",
  "evidence": [
    "0005 result and review report valid result, summary, and artifacts with schema validation passing.",
    "0005 metrics report any_positive_successor_evidence=false and negative_equivalence_evidence=true.",
    "0005 aggregate reports all_improving_lambdas_equivalent_to_trl_log=true under equivalence_tolerance=1e-10.",
    "0005 summary says improving successor-distance lambdas reduced held-out error only by matching trl_log within tolerance.",
    "The safe_optimal_lucky_only_stress scenario remains unresolved: trl_log, mc_plus_trl_log, and successor-distance variants select risky with policy_regret=0.504.",
    "Earlier tabular results still show a real target: raw TRL is support-optimistic under stochastic lucky paths, and log TRL improves long-horizon holdout under matched coverage."
  ],
  "next_experiment": {
    "estimated_runtime_minutes": 20,
    "experiment_id": "0006",
    "hypothesis": "A small uncertainty penalty based only on offline branch count or outcome variance can reduce lucky-only risky overestimation versus trl_log without breaking deterministic horizon recovery or incorrectly avoiding the risky action when it is truly optimal under matched coverage.",
    "objective": "Test a minimal uncertainty-aware or one-sided conservative log-TRL backup on the tabular biased-coverage failure while preserving matched safe-optimal, matched risk-optimal, and deterministic long-horizon behavior.",
    "required_outputs": [
      "research/sto_trl/artifacts/0006/run_uncertainty_aware_log_trl.py",
      "research/sto_trl/artifacts/0006/raw_metrics.json",
      "research/sto_trl/artifacts/0006/metrics.csv",
      "research/sto_trl/artifacts/0006/penalty_sweep.json",
      "research/sto_trl/artifacts/0006/uncertainty_diagnostics.json",
      "research/sto_trl/results/0006_result.json",
      "research/sto_trl/results/0006_summary.md"
    ]
  },
  "progress_score": 6,
  "rationale": "The latest valid result weakens the specific successor-distance variant: 0005 found that all improving successor-distance lambdas were numerically equivalent to trl_log, so it does not add distinct evidence. However, the results reveal a nearby cheap test: uncertainty-aware or one-sided conservative log-TRL aimed at the biased lucky-only coverage failure that raw/log/successor variants still share.",
  "risks": [
    "A conservative penalty could appear to fix safe-optimal lucky-only by avoiding all risky actions, so risk_optimal_matched must be a hard anti-conservatism check.",
    "Unobserved stochastic failures cannot be inferred without an explicit assumption; the uncertainty penalty must use only offline coverage statistics and state that assumption clearly.",
    "A penalty grid can be overfit if only best results are reported; require the full predeclared grid and negative outcomes.",
    "Do not move to function approximation, OGBench, downloads, or broad sweeps while the tabular biased-coverage failure remains unresolved."
  ]
}
```

## 0007_decision.json

```json
{
  "confidence": 0.76,
  "decision": "needs_human",
  "evidence": [
    "Current state reports last_decision=retryable_failure with failure_streak=1 and note: reviewer failed or timed out for 0007.",
    "research/sto_trl/results/0007_result.json and research/sto_trl/results/0007_summary.md exist, along with artifacts under research/sto_trl/artifacts/0007/.",
    "Validation of research/sto_trl/results/0007_result.json against schemas/result.schema.json with artifact checks returned validation ok.",
    "research/sto_trl/reviews/0007_review_events.jsonl reports: Codex ran out of room in the model's context window; turn.failed.",
    "research/sto_trl/reviews/0007_review_stderr.log is empty and no research/sto_trl/reviews/0007_review.json is present in the review listing.",
    "The prompt's latest accepted result summary is still 0006, while the filesystem contains an unreviewed 0007 result, so the source-of-truth state is inconsistent."
  ],
  "next_experiment": null,
  "progress_score": 6,
  "rationale": "Do not launch another experiment yet. The loop state is ambiguous: the current state reports a retryable reviewer failure for iteration 0007 and still presents 0006 as the latest accepted result, but the workspace already contains a completed 0007 result and artifacts. The 0007 result validates, yet the 0007 reviewer failed from context exhaustion and no accepted 0007 review JSON is present. Proposing another 0007 experiment risks duplicating or overwriting unreviewed outputs; advancing scientifically without resolving the review failure would treat an unsupported result as accepted.",
  "risks": [
    "Repeating experiment id 0007 could overwrite or duplicate an existing unreviewed result, conflicting with the repository rule to preserve prior results and artifacts.",
    "Treating 0007 as accepted without a completed review would weaken the evidence gate and bypass the loop's validation process.",
    "The reviewer failure appears to be an infrastructure/context-window issue, not a scientific result; the right next action is to resolve or rerun the review in a compact mode before selecting a further experiment.",
    "If the system cannot reconcile whether 0007 is accepted, any proposed next experiment id would be unsafe because the prompt still requires 0007 rather than a new 0008 id."
  ]
}
```


## Full evidence paths

- `research/sto_trl/results/0007_result.json`
- `research/sto_trl/results/0007_summary.md`
- `research/sto_trl/reviews/0007_review.json`

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
