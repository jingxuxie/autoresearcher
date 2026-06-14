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
  "iteration": 9,
  "last_decision": "continue",
  "last_failure": null,
  "last_pro_review_iteration": 9,
  "last_pro_review_path": "research/sto_trl/decisions/0010_pro_decision.json",
  "last_summary_iteration": 9,
  "last_summary_path": "research/sto_trl/progress/0009_pre_pro_weak_pass_streak_summary.md",
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
    "2026-06-14T02:51:00+00:00: resumed after fixing strict structured-output schema requirements",
    "2026-06-14T03:26:20+00:00: Pro checkpoint blocked (response_parse_failed); packet research/sto_trl/pro_packets/0010_PRO_REVIEW_PACKET.md",
    "2026-06-14T03:29:27+00:00: applied Pro decision continue from research/sto_trl/decisions/0010_pro_decision.json"
  ],
  "pending_checkpoint": null,
  "pending_local_decision_path": null,
  "primary_metric": null,
  "pro_review_count": 1,
  "protected_file_drift": false,
  "status": "active",
  "weak_pass_streak": 0
}
```


## Latest result summary

```json
{
  "_source": "/home/eston/autoresearcher/research/sto_trl/results/0009_result.json",
  "artifacts": {
    "_type": "list",
    "first_items": [
      "research/sto_trl/artifacts/0009/transition_posterior_baselines.py",
      "research/sto_trl/artifacts/0009/raw_metrics.json",
      "research/sto_trl/artifacts/0009/metrics.csv"
    ],
    "length": 9
  },
  "baseline_metrics": {
    "empirical_model_dp": {
      "action_accuracy": 0.5,
      "mean_calibration_error": 0.26296875,
      "mean_policy_regret": 0.10901250000000001,
      "mean_q_overestimation": 0.11671875000000001,
      "mean_q_underestimation": 0.14625000000000002,
      "num_cells": 8,
      "risky_action_selection_rate": 0.375
    },
    "empirical_risky_value": {
      "action_accuracy": 0.5,
      "mean_calibration_error": 0.26296875,
      "mean_policy_regret": 0.10901250000000001,
      "mean_q_overestimation": 0.11671875000000001,
      "mean_q_underestimation": 0.14625000000000002,
      "num_cells": 8,
      "risky_action_selection_rate": 0.375
    },
    "posterior_lower_q10_dp_beta_1_1": {
      "action_accuracy": 0.75,
      "mean_calibration_error": 0.29698125000000003,
      "mean_policy_regret": 0.02024999999999999,
      "mean_q_overestimation": 0.04286250000000001,
      "mean_q_underestimation": 0.25411875,
      "num_cells": 8,
      "risky_action_selection_rate": 0.125
    },
    "posterior_mean_dp_beta_1_1": {
      "action_accuracy": 0.625,
      "mean_calibration_error": 0.23375,
      "mean_policy_regret": 0.08325,
      "mean_q_overestimation": 0.09,
      "mean_q_underestimation": 0.14375000000000004,
      "num_cells": 8,
      "risky_action_selection_rate": 0.25
    },
    "raw_trl": {
      "action_accuracy": 0.375,
      "mean_calibration_error": 0.405,
      "mean_policy_regret": 0.16863750000000002,
      "mean_q_overestimation": 0.275625,
      "mean_q_underestimation": 0.12937500000000002,
      "num_cells": 8,
      "risky_action_selection_rate": 0.75
    },
    "robust_lcb_dp_delta_0_2": {
      "action_accuracy": 0.625,
      "mean_calibration_error": 0.3772944862234698,
      "mean_policy_regret": 0.039487499999999995,
      "mean_q_overestimation": 0.024019705510612114,
      "mean_q_underestimation": 0.3532747807128576,
      "num_cells": 8,
      "risky_action_selection_rate": 0.0
    },
    "trl_log": {
      "action_accuracy": 0.5,
      "mean_calibration_error": 0.26296875,
      "mean_policy_regret": 0.10901250000000001,
      "mean_q_overestimation": 0.11671875000000001,
      "mean_q_underestimation": 0.14625000000000002,
      "num_cells": 8,
      "risky_action_selection_rate": 0.375
    }
  },
  "claim_tested": "Transition-level empirical, Bayesian, quantile, and robust model-DP baselines can explain which representative finite-coverage risky-shortcut regimes are recoverable before adding posterior TRL variants.",
  "experiment_id": "0009",
  "interpretation": "On the representative 0008 subset, transition-level uncertainty baselines explain the recoverable finite-coverage behavior: posterior_lower_q10_dp_beta_1_1 reduces mean target-regime regret versus TRL-log by -0.177525000000, while at least one posterior baseline preserves the matched risk-optimal action. No evaluated transition baseline solved risk_optimal_no_success; explicit priors or additional coverage remain necessary. Empirical model DP, empirical risky value, and TRL-log are identical on... [trimmed]",
  "known_failures": [
    "Risk-optimal no-success remains unsolved from counts alone."
  ],
  "metrics": {
    "best_transition_uncertainty_method": "posterior_lower_q10_dp_beta_1_1",
    "best_transition_uncertainty_target_regret_delta_vs_trl_log": -0.17752500000000004,
    "chain_guard": {
      "by_distance": {
        "_type": "object",
        "key_count": 8,
        "keys": [
          "1",
          "2",
          "3",
          "4",
          "5",
          "6",
          "7",
          "8"
        ]
      },
      "chain_length": 9,
      "passed": true,
      "raw_trl_max_abs_error": 0.0,
      "trl_log_max_abs_error": 0.0
    },
    "coverage_diagnostics": {
      "num_method_rows": 72,
      "num_selected_cells": 8,
      "regime_label_counts": {
        "_type": "object",
        "key_count": 8,
        "keys": [
          "ambiguous_risk_optimal",
          "ambiguous_safe_optimal",
          "lucky_only_safe_optimal",
          "matched_identifiable_safe_optimal",
          "matched_risk_optimal",
          "no_success_risk_optimal",
          "no_success_safe_optimal",
          "prior_dependent_safe_optimal"
        ]
      },
      "risky_sample_counts": {
        "_type": "object",
        "key_count": 8,
        "keys": [
          "ambiguous_risk_optimal_boundary",
          "ambiguous_safe_optimal_boundary",
          "matched_identifiable_safe_optimal",
          "matched_risk_optimal_high_coverage",
          "prior_dependent_safe_optimal",
          "risk_no_success_stress",
          "safe_lucky_only_stress",
          "safe_no_success_identifiable"
        ]
      },
      "tag_counts": {
        "_type": "object",
        "key_count": 8,
        "keys": [
          "ambiguous",
          "identifiable",
          "lucky_only",
          "matched",
          "no_success",
          "prior_dependent",
          "risky_optimal",
          "safe_optimal"
        ]
      },
      "target_regime_labels_for_posterior_delta": {
        "_type": "list",
        "length": 4
      }
    },
    "matched_risk_summary": {
      "empirical_model_dp": {
        "_type": "object",
        "key_count": 7,
        "keys": [
          "action_accuracy",
          "mean_calibration_error",
          "mean_policy_regret",
          "mean_q_overestimation",
          "mean_q_underestimation",
          "num_cells",
          "risky_action_selection_rate"
        ]
      },
      "empirical_risky_value": {
        "_type": "object",
        "key_count": 7,
        "keys": [
          "action_accuracy",
          "mean_calibration_error",
          "mean_policy_regret",
          "mean_q_overestimation",
          "mean_q_underestimation",
          "num_cells",
          "risky_action_selection_rate"
        ]
      },
      "posterior_lower_q10_dp_beta_1_1": {
        "_type": "object",
        "key_count": 7,
        "keys": [
          "action_accuracy",
          "mean_calibration_error",
          "mean_policy_regret",
          "mean_q_overestimation",
          "mean_q_underestimation",
          "num_cells",
          "risky_action_selection_rate"
        ]
      },
      "posterior_mean_dp_beta_1_1": {
        "_type": "object",
        "key_count": 7,
        "keys": [
          "action_accuracy",
          "mean_calibration_error",
          "mean_policy_regret",
          "mean_q_overestimation",
          "mean_q_underestimation",
          "num_cells",
          "risky_action_selection_rate"
        ]
      },
      "posterior_upper_q90_dp_beta_1_1": {
        "_type": "object",
        "key_count": 7,
        "keys": [
          "action_accuracy",
          "mean_calibration_error",
          "mean_policy_regret",
          "mean_q_overestimation",
          "mean_q_underestimation",
          "num_cells",
          "risky_action_selection_rate"
        ]
      },
      "raw_trl": {
        "_type": "object",
        "key_count": 7,
        "keys": [
          "action_accuracy",
          "mean_calibration_error",
          "mean_policy_regret",
          "mean_q_overestimation",
          "mean_q_underestimation",
          "num_cells",
          "risky_action_selection_rate"
        ]
      },
      "robust_lcb_dp_delta_0_2": {
        "_type": "object",
        "key_count": 7,
        "keys": [
          "action_accuracy",
          "mean_calibration_error",
          "mean_policy_regret",
          "mean_q_overestimation",
          "mean_q_underestimation",
          "num_cells",
          "risky_action_selection_rate"
        ]
      },
      "robust_ucb_dp_delta_0_2": {
        "_type": "object",
        "key_count": 7,
        "keys": [
          "action_accuracy",
          "mean_calibration_error",
          "mean_policy_regret",
          "mean_q_overestimation",
          "mean_q_underestimation",
          "num_cells",
          "risky_action_selection_rate"
        ]
      },
      "trl_log": {
        "_type": "object",
        "key_count": 7,
        "keys": [
          "action_accuracy",
          "mean_calibration_error",
          "mean_policy_regret",
          "mean_q_overestimation",
          "mean_q_underestimation",
          "num_cells",
          "risky_action_selection_rate"
        ]
      }
    },
    "method_summary": {
      "empirical_model_dp": {
        "_type": "object",
        "key_count": 7,
        "keys": [
          "action_accuracy",
          "mean_calibration_error",
          "mean_policy_regret",
          "mean_q_overestimation",
          "mean_q_underestimation",
          "num_cells",
          "risky_action_selection_rate"
        ]
      },
      "empirical_risky_value": {
        "_type": "object",
        "key_count": 7,
        "keys": [
          "action_accuracy",
          "mean_calibration_error",
          "mean_policy_regret",
          "mean_q_overestimation",
          "mean_q_underestimation",
          "num_cells",
          "risky_action_selection_rate"
        ]
      },
      "posterior_lower_q10_dp_beta_1_1": {
        "_type": "object",
        "key_count": 7,
        "keys": [
          "action_accuracy",
          "mean_calibration_error",
          "mean_policy_regret",
          "mean_q_overestimation",
          "mean_q_underestimation",
          "num_cells",
          "risky_action_selection_rate"
        ]
      },
      "posterior_mean_dp_beta_1_1": {
        "_type": "object",
        "key_count": 7,
        "keys": [
          "action_accuracy",
          "mean_calibration_error",
          "mean_policy_regret",
          "mean_q_overestimation",
          "mean_q_underestimation",
          "num_cells",
          "risky_action_selection_rate"
        ]
      },
      "posterior_upper_q90_dp_beta_1_1": {
        "_type": "object",
        "key_count": 7,
        "keys": [
          "action_accuracy",
          "mean_calibration_error",
          "mean_policy_regret",
          "mean_q_overestimation",
          "mean_q_underestimation",
          "num_cells",
          "risky_action_selection_rate"
        ]
      },
      "raw_trl": {
        "_type": "object",
        "key_count": 7,
        "keys": [
          "action_accuracy",
          "mean_calibration_error",
          "mean_policy_regret",
          "mean_q_overestimation",
          "mean_q_underestimation",
          "num_cells",
          "risky_action_selection_rate"
        ]
      },
      "robust_lcb_dp_delta_0_2": {
        "_type": "object",
        "key_count": 7,
        "keys": [
          "action_accuracy",
          "mean_calibration_error",
          "mean_policy_regret",
          "mean_q_overestimation",
          "mean_q_underestimation",
          "num_cells",
          "risky_action_selection_rate"
        ]
      },
      "robust_ucb_dp_delta_0_2": {
        "_type": "object",
        "key_count": 7,
        "keys": [
          "action_accuracy",
          "mean_calibration_error",
          "mean_policy_regret",
          "mean_q_overestimation",
          "mean_q_underestimation",
          "num_cells",
          "risky_action_selection_rate"
        ]
      },
      "trl_log": {
        "_type": "object",
        "key_count": 7,
        "keys": [
          "action_accuracy",
          "mean_calibration_error",
          "mean_policy_regret",
          "mean_q_overestimation",
          "mean_q_underestimation",
          "num_cells",
          "risky_action_selection_rate"
        ]
      }
    },
    "no_success_risk_optimal_solved_methods": [],
    "num_method_rows": 72,
    "num_selected_cells": 8,
    "posterior_candidate_target_regret_deltas_vs_trl_log": {
      "posterior_lower_q10_dp_beta_1_1": -0.17752500000000004,
      "posterior_mean_dp_beta_1_1": -0.051525000000000015,
      "posterior_upper_q90_dp_beta_1_1": -0.006749999999999978,
      "robust_lcb_dp_delta_0_2": -0.17752500000000004,
      "robust_ucb_dp_delta_0_2": -0.006749999999999978
    },
    "target_regime_summary": {
      "empirical_model_dp": {
        "_type": "object",
        "key_count": 7,
        "keys": [
          "action_accuracy",
          "mean_calibration_error",
          "mean_policy_regret",
          "mean_q_overestimation",
          "mean_q_underestimation",
          "num_cells",
          "risky_action_selection_rate"
        ]
      },
      "empirical_risky_value": {
        "_type": "object",
        "key_count": 7,
        "keys": [
          "action_accuracy",
          "mean_calibration_error",
          "mean_policy_regret",
          "mean_q_overestimation",
          "mean_q_underestimation",
          "num_cells",
          "risky_action_selection_rate"
        ]
      },
      "posterior_lower_q10_dp_beta_1_1": {
        "_type": "object",
        "key_count": 7,
        "keys": [
          "action_accuracy",
          "mean_calibration_error",
          "mean_policy_regret",
          "mean_q_overestimation",
          "mean_q_underestimation",
          "num_cells",
          "risky_action_selection_rate"
        ]
      },
      "posterior_mean_dp_beta_1_1": {
        "_type": "object",
        "key_count": 7,
        "keys": [
          "action_accuracy",
          "mean_calibration_error",
          "mean_policy_regret",
          "mean_q_overestimation",
          "mean_q_underestimation",
          "num_cells",
          "risky_action_selection_rate"
        ]
      },
      "posterior_upper_q90_dp_beta_1_1": {
        "_type": "object",
        "key_count": 7,
        "keys": [
          "action_accuracy",
          "mean_calibration_error",
          "mean_policy_regret",
          "mean_q_overestimation",
          "mean_q_underestimation",
          "num_cells",
          "risky_action_selection_rate"
        ]
      },
      "raw_trl": {
        "_type": "object",
        "key_count": 7,
        "keys": [
          "action_accuracy",
          "mean_calibration_error",
          "mean_policy_regret",
          "mean_q_overestimation",
          "mean_q_underestimation",
          "num_cells",
          "risky_action_selection_rate"
        ]
      },
      "robust_lcb_dp_delta_0_2": {
        "_type": "object",
        "key_count": 7,
        "keys": [
          "action_accuracy",
          "mean_calibration_error",
          "mean_policy_regret",
          "mean_q_overestimation",
          "mean_q_underestimation",
          "num_cells",
          "risky_action_selection_rate"
        ]
      },
      "robust_ucb_dp_delta_0_2": {
        "_type": "object",
        "key_count": 7,
        "keys": [
          "action_accuracy",
          "mean_calibration_error",
          "mean_policy_regret",
          "mean_q_overestimation",
          "mean_q_underestimation",
          "num_cells",
          "risky_action_selection_rate"
        ]
      },
      "trl_log": {
        "_type": "object",
        "key_count": 7,
        "keys": [
          "action_accuracy",
          "mean_calibration_error",
          "mean_policy_regret",
          "mean_q_overestimation",
          "mean_q_underestimation",
          "num_cells",
          "risky_action_selection_rate"
        ]
      }
    },
    "transition_baseline_positive": true
  },
  "next_questions": [
    "Should future posterior TRL variants report an identifiability or prior-dependence flag before selecting risky actions?",
    "What explicit prior is acceptable for risk-optimal no-success regimes where finite data lacks successful risky outcomes?",
    "Can transitive posterior propagation improve long-horizon estimates without outperforming these transition-model baselines only by prior choice?"
  ],
  "status": "completed"
}
```


## Latest summary

# Experiment 0009 Summary

## Objective

Audit compact transition-level posterior model-DP baselines on representative cells from the 0008 identifiability grid before adding posterior/transitive TRL variants.

## Commands Run

```bash
mkdir -p research/sto_trl/artifacts/0009 research/sto_trl/results
conda run -n autoresearcher_sto_trl python research/sto_trl/artifacts/0009/transition_posterior_baselines.py
conda run -n autoresearcher_sto_trl python scripts/validate_artifacts.py --repo-root . --json research/sto_trl/results/0009_result.json --schema schemas/result.schema.json --check-result-artifacts
```

## Representative Subset

- Selected cells: `8`
- Method rows: `72`
- Regime counts: `{'matched_identifiable_safe_optimal': 1, 'matched_risk_optimal': 1, 'lucky_only_safe_optimal': 1, 'no_success_safe_optimal': 1, 'no_success_risk_optimal': 1, 'ambiguous_safe_optimal': 1, 'ambiguous_risk_optimal': 1, 'prior_dependent_safe_optimal': 1}`
- Tag counts: `{'matched': 5, 'identifiable': 3, 'safe_optimal': 5, 'ambiguous': 5, 'risky_optimal': 3, 'lucky_only': 1, 'prior_dependent': 4, 'no_success': 2}`

## Method Summary

| Method | Action accuracy | Mean regret | Risky rate | Mean Q overestimate | Calibration error |
| --- | ---: | ---: | ---: | ---: | ---: |
| empirical_model_dp | 0.500000 | 0.109012500000 | 0.375000 | 0.116718750000 | 0.262968750000 |
| empirical_risky_value | 0.500000 | 0.109012500000 | 0.375000 | 0.116718750000 | 0.262968750000 |
| posterior_lower_q10_dp_beta_1_1 | 0.750000 | 0.020250000000 | 0.125000 | 0.042862500000 | 0.296981250000 |
| posterior_mean_dp_beta_1_1 | 0.625000 | 0.083250000000 | 0.250000 | 0.090000000000 | 0.233750000000 |
| posterior_upper_q90_dp_beta_1_1 | 0.500000 | 0.105637500000 | 0.625000 | 0.175856250000 | 0.255787500000 |
| raw_trl | 0.375000 | 0.168637500000 | 0.750000 | 0.275625000000 | 0.405000000000 |
| robust_lcb_dp_delta_0_2 | 0.625000 | 0.039487500000 | 0.000000 | 0.024019705511 | 0.377294486223 |
| robust_ucb_dp_delta_0_2 | 0.500000 | 0.105637500000 | 0.625000 | 0.248480276028 | 0.307052638014 |
| trl_log | 0.500000 | 0.109012500000 | 0.375000 | 0.116718750000 | 0.262968750000 |

## Decision Findings

- Best target-regime transition uncertainty baseline: `posterior_lower_q10_dp_beta_1_1`.
- Target-regime regret delta versus TRL-log: `-0.177525000000`.
- Positive transition-baseline evidence: `True`.
- Risk-optimal no-success solved methods: `[]`.
- Chain guard passed: `True`.

## Interpretation

On the representative 0008 subset, transition-level uncertainty baselines explain the recoverable finite-coverage behavior: posterior_lower_q10_dp_beta_1_1 reduces mean target-regime regret versus TRL-log by -0.177525000000, while at least one posterior baseline preserves the matched risk-optimal action. No evaluated transition baseline solved risk_optimal_no_success; explicit priors or additional coverage remain necessary. Empirical model DP, empirical risky value, and TRL-log are identical on this tabular family.

## Artifacts

- `research/sto_trl/artifacts/0009/transition_posterior_baselines.py`
- `research/sto_trl/artifacts/0009/raw_metrics.json`
- `research/sto_trl/artifacts/0009/metrics.csv`
- `research/sto_trl/artifacts/0009/regime_summary.csv`
- `research/sto_trl/artifacts/0009/posterior_diagnostics.json`
- `research/sto_trl/artifacts/0009/selected_grid_cells.json`
- `research/sto_trl/artifacts/0009/coverage_diagnostics.json`
- `research/sto_trl/artifacts/0009/transition_tables.json`
- `research/sto_trl/artifacts/0009/value_tables.json`


## Latest review summary

```json
{
  "allows_auto_continue": true,
  "escalation_reason": null,
  "evidence_checked": {
    "_type": "list",
    "first_items": [
      "research/sto_trl/results/0009_result.json",
      "research/sto_trl/results/0009_summary.md",
      "research/sto_trl/artifacts/0009/transition_posterior_baselines.py"
    ],
    "length": 15
  },
  "evidence_quality": "medium",
  "experiment_id": "0009",
  "failure_criteria_triggered": false,
  "reasons": {
    "_type": "list",
    "first_items": [
      "The required 0009 result, summary, and all nine listed artifacts are present, and result/artifact validation returned ok.",
      "The result commit only contains 0009 artifacts/results plus the executor packet; protected files such as schemas, AGENTS.md, scripts/autoresearcher.py, and environment files were not modified in the result commit.",
      "The selected subset has 8 representative cells covering matched safe, matched risk, lucky-only safe, no-success safe, no-success risk, ambiguous safe, ambiguous risk, and prior-dependent safe regimes."
    ],
    "length": 9
  },
  "required_fixes": [],
  "risk_flags": [
    "The positive transition-baseline evidence rests on four target cells and an 8-cell handpicked subset, so it should set a baseline rather than support a broad generalization.",
    "The best method, posterior_lower_q10_dp_beta_1_1, is conservative: it fixes lucky-only and prior-dependent safe cases but fails ambiguous_risk_optimal and no_success_risk_optimal; robust_lcb also fails matched risk-optimal in the matched_risk_summary.",
    "The chain guard remains a formula check, not a real raw/log TRL execution check on a chain dataset.",
    "The subset was chosen using known true regimes from the grid; that is acceptable for audit design but should not be confused with a deployable regime classifier."
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
    },
    {
      "allows_auto_continue": true,
      "claim_tested": "A compact exact-DP tabular grid can distinguish risky-shortcut failures caused by finite stochastic coverage from failures of the TRL-log update itself.",
      "decision": "continue",
      "important_metrics": {
        "metrics.classification_counts.no_success": 45,
        "metrics.method_summary.empirical_risky_value.action_accuracy": 0.6903225806451613,
        "metrics.method_summary.empirical_risky_value.mean_policy_regret": 0.07556516129032252,
        "metrics.method_summary.empirical_transition_dp.mean_policy_regret": 0.07556516129032252,
        "metrics.method_summary.hoeffding_lcb_delta_0_2.mean_policy_regret": 0.019136129032258063,
        "metrics.method_summary.hoeffding_ucb_delta_0_2.mean_policy_regret": 0.1573490322580649,
        "metrics.method_summary.posterior_lower_q10_beta_1_1.mean_policy_regret": 0.026568387096774195,
        "metrics.method_summary.posterior_mean_beta_1_1.mean_policy_regret": 0.05130387096774184,
        "metrics.method_summary.posterior_upper_q90_beta_1_1.mean_policy_regret": 0.10117161290322614,
        "metrics.method_summary.raw_trl.mean_policy_regret": 0.2713587096774201,
        "metrics.method_summary.trl_log.mean_policy_regret": 0.07556516129032252,
        "metrics.tag_counts.no_success": 45
      },
      "iteration": "0008",
      "negative_signals": [
        "Grid produced 285 ambiguous, lucky-only, no-success, or prior-dependent cells where action choice cannot be justified by empirical frequencies alone.",
        "TRL-log is identical to empirical transition DP on this tabular grid, so failures in those cells are data-identifiability failures rather than implementation-specific TRL-log failures.",
        "Do not use the method_summary rankings as probability-weighted performance claims; the sweep weights each possible observed success count equally.",
        "Do not treat all no-success or lucky-only primary cells as impossible without inspecting empirical_identifiable and prior_dependent tags.",
        "The chain guard should be strengthened in a future experiment if deterministic long-horizon recovery is an important acceptance gate."
      ],
      "positive_signals": [
        "Posterior lower and upper choices intentionally disagree in prior-dependent cells, exposing where explicit priors are unavoidable.",
        "The grid is useful as an identifiability map: it separates cells where empirical transition estimates match exact action choice from lucky-only, no-success, ambiguous, and prior-dependent cells where explicit priors are required."
      ],
      "review_verdict": "weak_pass",
      "status": "completed"
    },
    {
      "allows_auto_continue": true,
      "claim_tested": "Transition-level empirical, Bayesian, quantile, and robust model-DP baselines can explain which representative finite-coverage risky-shortcut regimes are recoverable before adding posterior TRL variants.",
      "decision": "continue",
      "important_metrics": {
        "metrics.best_transition_uncertainty_method": "posterior_lower_q10_dp_beta_1_1",
        "metrics.best_transition_uncertainty_target_regret_delta_vs_trl_log": -0.17752500000000004,
        "metrics.chain_guard.by_distance.1.exact": 0.9,
        "metrics.chain_guard.by_distance.2.exact": 0.81,
        "metrics.chain_guard.by_distance.3.exact": 0.7290000000000001,
        "metrics.chain_guard.by_distance.4.exact": 0.6561,
        "metrics.chain_guard.by_distance.5.exact": 0.5904900000000001,
        "metrics.chain_guard.by_distance.6.exact": 0.531441,
        "metrics.chain_guard.by_distance.7.exact": 0.4782969000000001,
        "metrics.chain_guard.by_distance.8.exact": 0.4304672100000001,
        "metrics.coverage_diagnostics.regime_label_counts.ambiguous_risk_optimal": 1,
        "metrics.coverage_diagnostics.regime_label_counts.matched_risk_optimal": 1
      },
      "iteration": "0009",
      "negative_signals": [
        "TRL-log, empirical risky value, and empirical model DP are numerically equivalent for these one-step risky shortcut decisions.",
        "No evaluated transition baseline solved risk_optimal_no_success; explicit priors or additional coverage remain necessary.",
        "Risk-optimal no-success remains unsolved from counts alone.",
        "The positive transition-baseline evidence rests on four target cells and an 8-cell handpicked subset, so it should set a baseline rather than support a broad generalization.",
        "The best method, posterior_lower_q10_dp_beta_1_1, is conservative: it fixes lucky-only and prior-dependent safe cases but fails ambiguous_risk_optimal and no_success_risk_optimal; robust_lcb also fails matched risk-optim..."
      ],
      "positive_signals": [
        "Best target-regime transition uncertainty baseline: posterior_lower_q10_dp_beta_1_1 with regret delta -0.177525000000 versus TRL-log.",
        "Posterior lower/mean baselines reduce safe lucky-only and safe prior-dependent regret without selecting safe everywhere.",
        "On the representative 0008 subset, transition-level uncertainty baselines explain the recoverable finite-coverage behavior: posterior_lower_q10_dp_beta_1_1 reduces mean target-regime regret versus TRL-log by -0.177525000000, while at least one posterior baseli"
      ],
      "review_verdict": "weak_pass",
      "status": "completed"
    }
  ],
  "project": "sto_trl"
}
```


## Last decision summaries

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

## 0008_decision.json

```json
{
  "confidence": 0.84,
  "decision": "continue",
  "evidence": [
    "The human pivot note research/sto_trl/progress/human_pivot_0008.md says to continue only under the reframed question: transition-level stochastic uncertainty plus log-space transitive propagation under finite offline stochastic coverage.",
    "The same human pivot note recommends the next experiment: sweep true risky success probability, safe path length, risky sample count, and observed risky successes; compare empirical risky value, posterior means/quantiles, lower/upper confidence choices, TRL-log, and raw TRL.",
    "0007 result and review are present and accepted as weak_pass, with validation reported ok and allows_auto_continue=true.",
    "0007 review says the generic method only gives modest Q-overestimation reduction, does not fix safe_optimal_lucky_only policy regret, and remains worse than the 0006 one-sided alpha 0.40 comparison on that stress case.",
    "0007 aggregate reports trl_log_safe_lucky_policy_regret=0.504, one_sided_0006_safe_lucky_policy_regret=0.0, and risk_optimal_no_success_unsolved_by_best_positive=true.",
    "Prior 0005 evidence remains negative for the original successor-distance formulation: improving successor-distance lambdas were equivalent to trl_log and any_positive_successor_evidence=false.",
    "The environment state is ready and the proposed grid is tabular with exact DP ground truth, so it stays within the charter's initial scope and compute budget."
  ],
  "next_experiment": {
    "estimated_runtime_minutes": 25,
    "experiment_id": "0008",
    "hypothesis": "Across risky-shortcut MDPs, some regimes are identifiable from observed risky successes/failures and simple empirical or posterior transition estimates should match exact DP action choice, while lucky-only and no-success regimes will expose impossibility or prior-dependence. This grid should clarify when log-TRL failures are data-identifiability failures versus algorithmic failures.",
    "objective": "Run a small tabular identifiability and coverage grid that maps when risky-shortcut action choice is identifiable from finite offline stochastic coverage, before adding new stochastic TRL algorithms.",
    "required_outputs": {
      "_type": "list",
      "first_items": [
        "research/sto_trl/artifacts/0008/run_identifiability_coverage_grid.py",
        "research/sto_trl/artifacts/0008/raw_grid.json",
        "research/sto_trl/artifacts/0008/metrics.csv"
      ],
      "length": 11
    }
  },
  "progress_score": 6,
  "rationale": "The latest accepted evidence does not justify more algorithm tweaking, but the human pivot note explicitly approves a reframed direction and recommends a small identifiability and coverage grid. That is the right next experiment: it tests what finite offline stochastic coverage can and cannot identify before adding posterior transition models or more TRL variants. This remains tabular, exact-DP evaluable, and should be cheaper and more decisive than another method sweep.",
  "risks": [
    "The grid must not be interpreted as an algorithm win; its value is identifying solvable, ambiguous, and impossible coverage regimes.",
    "If the grid is too broad it could become low-value exploration; keep it small enough to finish within 30 minutes and save all raw cells.",
    "Posterior or confidence-choice baselines encode assumptions; the result must label which conclusions depend on priors versus observed data.",
    "Do not move to neural networks, OGBench, PointMaze, AntMaze, downloads, or larger training from this step.",
    "The executor should avoid protected files and preserve previous artifacts, especially given prior review flags about unrelated control-file modifications."
  ]
}
```

## 0009_decision.json

```json
{
  "confidence": 0.82,
  "decision": "continue",
  "evidence": [
    "0008 result is completed with required artifacts, summary, and validation reported ok in the review.",
    "0008 review reports success_criteria_satisfied=true, failure_criteria_triggered=false, allows_auto_continue=true, and should_escalate_to_pro=false.",
    "0008 grid covered 465 exact-DP cells over true risky probability, safe path length, risky sample count, and observed successes, with 4185 method rows.",
    "0008 chain guard passed with raw_trl_max_abs_error=0.0 and trl_log_max_abs_error=0.0.",
    "0008 method summary shows trl_log and empirical_transition_dp have identical action_accuracy=0.6903225806451613 and mean_policy_regret=0.07556516129032252, indicating the tested TRL-log failures are empirical transition-identifiability failures on this grid.",
    "0008 posterior/conservative baselines improved mean regret on the uniformly weighted grid: posterior_mean_beta_1_1 mean_policy_regret=0.05130387096774184, posterior_lower_q10_beta_1_1=0.026568387096774195, and hoeffding_lcb_delta_0_2=0.019136129032258063, while raw_trl was much worse at 0.2713587096774201.",
    "0008 classified many cells as ambiguous, lucky-only, no-success, or prior-dependent, so the next test should establish transition-posterior baselines before any further stochastic TRL algorithm claims.",
    "The human pivot and next-step plan explicitly recommend continuing under the reframed transition-level stochastic uncertainty question, with Milestone 2 focused on empirical model DP, Bayesian posterior mean/quantile DP, and robust confidence-set DP."
  ],
  "next_experiment": {
    "estimated_runtime_minutes": 25,
    "experiment_id": "0009",
    "hypothesis": "Transition-level uncertainty baselines will explain most recoverable performance in finite-coverage risky-shortcut regimes: posterior mean, posterior quantile, and robust confidence-set DP should improve regret versus raw TRL and empirical TRL-log in prior-dependent or lucky-only cells while preserving matched safe-optimal and matched risk-optimal choices. Any remaining failures should identify where explicit priors or future transitive propagation are necessary.",
    "objective": "Run a compact transition-level posterior model-DP baseline audit on representative regimes from the 0008 identifiability grid, establishing what empirical, Bayesian, quantile, and robust transition models can solve before adding transitive/posterior TRL variants.",
    "required_outputs": {
      "_type": "list",
      "first_items": [
        "research/sto_trl/artifacts/0009/transition_posterior_baselines.py",
        "research/sto_trl/artifacts/0009/raw_metrics.json",
        "research/sto_trl/artifacts/0009/metrics.csv"
      ],
      "length": 11
    }
  },
  "progress_score": 7,
  "rationale": "Experiment 0008 successfully did the human-approved identifiability step and produced a useful map, but it also showed that TRL-log is effectively identical to empirical transition DP on this tabular risky-shortcut grid. The next small, high-information test should follow the approved next-step plan: compare transition-level posterior and robust model-DP baselines directly against TRL-log/raw on representative grid regimes before adding any new transitive algorithm. This tests whether stochastic uncertainty alone explains the remaining gains and sets a baseline that any future transitive/posterior TRL variant must beat.",
  "risks": [
    "Do not treat the 0008 method rankings as probability-weighted performance claims because the grid weights observed success counts uniformly.",
    "Posterior and confidence-set methods encode priors or risk preferences; the result must separate empirical evidence from prior assumptions.",
    "If the posterior DP baseline already dominates, future TRL-style extensions need a specific transitive benefit beyond transition uncertainty alone.",
    "Keep this tabular and exact-DP based; do not move to neural networks, continuous control, OGBench, downloads, or broad sweeps.",
    "Avoid overfitting to the full 0008 grid by using a compact representative subset and reporting regime-stratified results."
  ]
}
```


## Full evidence paths

- `research/sto_trl/results/0009_result.json`
- `research/sto_trl/results/0009_summary.md`
- `research/sto_trl/reviews/0009_review.json`

Use these paths if compact summaries are insufficient.


## Stop, pivot, continue rules

- For iteration 0, a missing latest result is expected and is not by itself a reason to stop.
- After iteration 0, stop or choose needs_human on missing or invalid result files.
- Stop on repeated invalid, negative, or low-value results.
- Pivot only when evidence weakens the original idea but reveals a nearby testable idea.
- Continue or pivot only for one cheap, high-information experiment.
- Choose needs_human for ambiguity, expensive work, missing artifacts, or risky pivots.


## Next experiment id

Use `0010` as the exact `next_experiment.experiment_id` if you choose continue or pivot.
