# Progress Summarizer Context: sto_trl

## Requested action

Write a concise human-readable Markdown progress summary for this project. Use the evidence below; do not overclaim beyond reviewed results.


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


## Current state

```json
{
  "best_primary_metric": null,
  "failure_streak": 0,
  "human_review_required": true,
  "iteration": 7,
  "last_decision": "stop",
  "last_failure": null,
  "last_pro_review_iteration": 0,
  "last_pro_review_path": null,
  "last_summary_iteration": 7,
  "last_summary_path": "research/sto_trl/progress/0007_manual_summary.md",
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
    "2026-06-14T01:25:11+00:00: Pro checkpoint blocked (login_required); packet research/sto_trl/pro_packets/0008_PRO_REVIEW_PACKET.md"
  ],
  "pending_checkpoint": {
    "backend": "codex-chatgpt-control",
    "blocker_path": "research/sto_trl/decisions/0008_pro_blocker.json",
    "iteration_id": "0008",
    "manual_fallback": true,
    "packet_path": "research/sto_trl/pro_packets/0008_PRO_REVIEW_PACKET.md",
    "reason": "local_stop",
    "status": "blocked",
    "type": "chatgpt_pro"
  },
  "pending_local_decision_path": null,
  "primary_metric": null,
  "pro_review_count": 0,
  "protected_file_drift": false,
  "status": "paused",
  "weak_pass_streak": 0
}
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


## Experiment ledger

```json
[
  {
    "allows_auto_continue": true,
    "baseline_metrics": {
      "_key_count": 3,
      "_keys": [
        "deterministic_chain",
        "method",
        "risky_shortcut"
      ],
      "nested_samples": {
        "deterministic_chain": {
          "calibration_error": 0.2638688400000001,
          "eval_start_exact_value": 0.5904900000000002,
          "long_horizon_value_mse": 3.697785493223493e-33,
          "max_policy_regret": 0.0,
          "mean_policy_regret": 0.0,
          "policy_regret": 0.0,
          "q_calibration_error": 0.2638688400000001,
          "q_overestimation_error": 0.0
        },
        "risky_shortcut": {
          "calibration_error": 0.0,
          "eval_start_exact_value": 0.7290000000000001,
          "long_horizon_value_mse": 0.0,
          "max_policy_regret": 0.0,
          "mean_policy_regret": 0.0,
          "policy_regret": 0.0,
          "q_calibration_error": 0.0,
          "q_overestimation_error": 0.0
        }
      },
      "scalars": {
        "method": "mc_supervised"
      }
    },
    "claim_tested": "A tiny stochastic risky-shortcut MDP exposes overestimation by deterministic raw TRL backups, while log-space stochastic backups preserve deterministic-chain behavior and improve risky-action calibration relative to raw TRL.",
    "decision": "continue",
    "hypothesis": "A small tabular risky-shortcut MDP with offline lucky/unlucky outcomes will reveal whether raw deterministic-style TRL overestimates risky stochastic paths, while log-space or MC+TRL-log variants preserve deterministic behavior and improve...",
    "interpretation": "The deterministic chain sanity check was recovered by both raw and log TRL.",
    "iteration": "0001",
    "metrics": {
      "_key_count": 5,
      "_keys": [
        "experiment_id",
        "gamma",
        "mdps",
        "success_checks",
        "update_steps"
      ],
      "nested_samples": {
        "success_checks": {
          "risky_dataset_has_lucky_and_unlucky_outcomes": true,
          "success_criteria_met": true,
          "trl_raw_overestimates_risky_action": true,
          "trl_raw_prefers_risky_shortcut": true
        }
      },
      "scalars": {
        "experiment_id": "0001",
        "gamma": 0.9,
        "update_steps": 32
      }
    },
    "objective": "Build and run a minimal tabular diagnostic for stochastic TRL covering deterministic chain sanity and one risky-shortcut stochastic MDP, with exact discounted-reachability DP ground truth and raw metrics saved.",
    "review": "pass",
    "review_reasons": [
      "Required result, summary, and artifact files are present under research/sto_trl/results and research/sto_trl/artifacts/0001.",
      "Result JSON validates against schemas/result.schema.json, and artifact existence validation returned validation ok.",
      "The prototype implements exact discounted-reachability DP over explicit transition tables for both deterministic_chain and risky_shortcut.",
      "... 3 more; inspect full file"
    ],
    "risk_flags": [
      "Evidence is intentionally small-scale and balanced: risky outcome coverage exactly matches the true 0.25 success probability, so MC supervised is perfect here and the experiment ma...",
      "/home/eston/autoresearcher is not a git repository, so unrelated modifications could not be audited with git status."
    ],
    "status": "completed"
  },
  {
    "allows_auto_continue": true,
    "baseline_metrics": {
      "_key_count": 5,
      "_keys": [
        "mean_policy_regret_on_risky_scenarios",
        "method",
        "num_rows",
        "optimal_action_rate_on_risky_scenarios",
        "rows"
      ],
      "scalars": {
        "mean_policy_regret_on_risky_scenarios": 0.0666,
        "method": "mc_supervised",
        "num_rows": 11,
        "optimal_action_rate_on_risky_scenarios": 0.7
      }
    },
    "claim_tested": "Raw TRL overestimation is support-driven under stochastic coverage, while empirical MC/log methods are calibrated only when observed risky branch frequencies match the true MDP; a risk-optimal setting tests for conservative avoidance.",
    "decision": "continue",
    "hypothesis": "Raw TRL overestimation is support-driven and will select risky whenever a lucky risky transition is observed, while empirical TRL-log and MC variants will be calibrated only when observed risky success/failure frequencies approximate the tr...",
    "interpretation": "The chain guard still recovered exact discounted reachability for raw and log TRL.",
    "iteration": "0002",
    "metrics": {
      "_key_count": 8,
      "_keys": [
        "aggregate",
        "experiment_id",
        "gamma",
        "regime_specs",
        "safe_episodes_per_regime",
        "scenarios",
        "success_checks",
        "update_steps"
      ],
      "nested_samples": {
        "aggregate": {
          "mc_supervised_mean_policy_regret": 0.0666,
          "num_risky_scenarios": 10,
          "raw_no_success_scenarios": 2,
          "raw_selected_risky_when_no_success_observed": 0,
          "raw_selected_risky_when_success_observed": 8,
          "raw_success_observed_scenarios": 8,
          "trl_log_mean_policy_regret": 0.0666,
          "trl_raw_mean_policy_regret": 0.20970000000000005
        },
        "success_checks": {
          "all_predeclared_risky_regimes_present": true,
          "success_criteria_met": true
        }
      },
      "scalars": {
        "experiment_id": "0002",
        "gamma": 0.9,
        "safe_episodes_per_regime": 4,
        "update_steps": 32
      }
    },
    "objective": "Run a small tabular coverage-sensitivity stress test for the risky shortcut diagnostic, including both risk-suboptimal and risk-optimal settings, to check whether raw TRL overestimation and log/MC calibration claims survive biased or sparse...",
    "review": "pass",
    "review_reasons": [
      "Required outputs are present: research/sto_trl/results/0002_result.json, research/sto_trl/results/0002_summary.md, and populated artifacts under research/sto_trl/artifacts/0002.",
      "Result JSON validates against schemas/result.schema.json with artifact existence checks.",
      "The script implements exact discounted-reachability DP for evaluation and uses constructed offline trajectories for training; the training methods inspected use empirical trajector...",
      "... 4 more; inspect full file"
    ],
    "risk_flags": [
      "The Q overestimation and underestimation maxima are computed across all goals, not only the eval goal, so those headline error fields can reflect non-eval goals such as trap; eval-...",
      "commands_run records setup, execution, and validation commands but not the manual edits that transformed the copied 0001 script into the 0002 harness.",
      "git status only showed an untracked reviewer packet, but without committed baselines this review cannot fully prove no prior artifacts were modified."
    ],
    "status": "completed"
  },
  {
    "allows_auto_continue": true,
    "baseline_metrics": {
      "_key_count": 3,
      "_keys": [
        "chain_len9",
        "method",
        "risky_matched"
      ],
      "nested_samples": {
        "chain_len9": {
          "calibration_error": 0.4656078690468753,
          "chose_exact_optimal_action": true,
          "exact_optimal_action": "right",
          "heldout_long_horizon_value_mse": 0.3917058232298766,
          "policy_regret": 0.0,
          "q_calibration_error": 0.4656078690468753,
          "q_overestimation_error": 0.0,
          "risky_action_selection_rate": 0.0
        },
        "risky_matched": {
          "calibration_error": 0.045562500000000006,
          "chose_exact_optimal_action": false,
          "exact_optimal_action": "safe",
          "heldout_long_horizon_value_mse": 0.25401600000000013,
          "policy_regret": 0.5040000000000001,
          "q_calibration_error": 0.045562500000000006,
          "q_overestimation_error": 0.0,
          "risky_action_selection_rate": 1.0
        }
      },
      "scalars": {
        "method": "mc_supervised"
      }
    },
    "claim_tested": "Censoring long-horizon MC labels makes MC-only underpredict held-out discounted reachability, while log transitive backups recover longer horizons and keep matched risky-branch calibration.",
    "decision": "continue",
    "hypothesis": "With only short-horizon MC labels, MC-supervised estimates will underpredict held-out long-horizon goals, while log-space transitive backups, especially MC+TRL-log, will propagate calibrated short-horizon information to longer horizons with...",
    "interpretation": "With positive labels beyond horizon 2 censored, MC-supervised underpredicted held-out long-horizon reachability.",
    "iteration": "0003",
    "metrics": {
      "_key_count": 7,
      "_keys": [
        "aggregate",
        "experiment_id",
        "gamma",
        "label_horizon_cutoff",
        "scenarios",
        "success_checks",
        "update_steps"
      ],
      "nested_samples": {
        "aggregate": {
          "chain_mc_heldout_value_mse": 0.3917058232298766,
          "chain_mc_plus_trl_log_heldout_value_mse": 2.9347503914472164e-34,
          "chain_trl_log_heldout_value_mse": 2.9347503914472164e-34,
          "risky_mc_heldout_value_mse": 0.25401600000000013,
          "risky_mc_plus_trl_log_heldout_value_mse": 0.0,
          "risky_mc_plus_trl_log_policy_regret": 0.0,
          "risky_trl_log_heldout_value_mse": 0.0,
          "risky_trl_log_policy_regret": 0.0
        },
        "success_checks": {
          "chain_raw_exact_under_censoring": true,
          "chain_trl_log_exact_under_censoring": true,
          "heldout_mse_improved_vs_mc_on_chain_and_risky": true,
          "matched_risky_mc_plus_trl_log_selects_safe": true,
          "matched_risky_trl_log_selects_safe": true,
          "matched_risky_trl_raw_selects_wrong_risky": true,
          "mc_plus_improves_chain_heldout_mse_vs_mc": true,
          "success_criteria_met": true
        }
      },
      "scalars": {
        "experiment_id": "0003",
        "gamma": 0.9,
        "label_horizon_cutoff": 2,
        "update_steps": 32
      }
    },
    "objective": "Run a small tabular horizon-holdout experiment that censors long-horizon goal labels during training and tests whether TRL-log or MC+TRL-log can recover long-horizon discounted reachability better than MC-only while retaining matched stocha...",
    "review": "weak_pass",
    "review_reasons": [
      "Required outputs are present: research/sto_trl/results/0003_result.json, research/sto_trl/results/0003_summary.md, and populated artifacts under research/sto_trl/artifacts/0003.",
      "Result JSON validates against schemas/result.schema.json with artifact checks.",
      "The harness includes exact DP ground truth for both evaluated MDPs: deterministic_chain_len9 and risky_shortcut_matched.",
      "... 4 more; inspect full file"
    ],
    "risk_flags": [
      "git status shows modified control files including scripts/autoresearcher.py, autoresearcher.yaml, tests/test_phase1.py, and research/sto_trl/state.json. Their mtimes precede the 00...",
      "commands_run records setup, execution, and validation commands, but not the manual edit operation that adapted the copied 0002 script into the 0003 harness.",
      "TRL-log and raw TRL are transitive model-based tabular backups over observed transitions, so they do not consume the same supervised label budget as MC-only; this is intended by th..."
    ],
    "status": "completed"
  },
  {
    "allows_auto_continue": true,
    "baseline_metrics": {
      "_key_count": 3,
      "_keys": [
        "main_mean_heldout_long_horizon_value_mse",
        "main_rows",
        "method"
      ],
      "scalars": {
        "main_mean_heldout_long_horizon_value_mse": 0.21524060774329223,
        "method": "successor_calibration_only"
      }
    },
    "claim_tested": "A self-normalized successor-distance calibration with log-space transitive relaxation improves held-out reachability versus calibration-only without increasing matched risky overestimation or avoiding truly optimal risky actions.",
    "decision": "continue",
    "hypothesis": "A self-normalized successor-distance calibration with a log-space transitive relaxation will improve held-out long-horizon value estimates over calibration-only while preserving matched stochastic branch calibration, reducing raw TRL overes...",
    "interpretation": "The successor-distance transitive relaxation improved main held-out long-horizon value MSE over calibration-only.",
    "iteration": "0004",
    "metrics": {
      "_key_count": 8,
      "_keys": [
        "aggregate",
        "experiment_id",
        "gamma",
        "label_horizon_cutoff",
        "scenarios",
        "success_checks",
        "successor_lambda_tr",
        "update_steps"
      ],
      "nested_samples": {
        "aggregate": {
          "risk_matched_successor_calibration_only_policy_regret": 0.0,
          "risk_matched_successor_distance_trl_log_policy_regret": 0.0,
          "safe_lucky_stress_successor_distance_action": "risky",
          "safe_matched_successor_calibration_only_policy_regret": 0.5040000000000001,
          "safe_matched_successor_distance_trl_log_policy_regret": 0.0,
          "successor_calibration_only_main_mean_heldout_mse": 0.21524060774329223,
          "successor_distance_trl_log_main_mean_heldout_mse": 9.782501304824055e-35
        },
        "success_checks": {
          "chain_raw_exact": true,
          "chain_trl_log_exact": true,
          "success_criteria_met": true,
          "successor_distance_improves_main_heldout_mse_vs_calibration_only": true,
          "successor_distance_no_matched_policy_regret_increase_vs_calibration_only": true,
          "successor_distance_no_matched_q_overestimation_increase_vs_calibration_only": true,
          "successor_distance_selects_risky_when_risk_optimal": true,
          "successor_distance_selects_safe_when_safe_optimal_matched": true
        }
      },
      "scalars": {
        "experiment_id": "0004",
        "gamma": 0.9,
        "label_horizon_cutoff": 2,
        "successor_lambda_tr": 0.75,
        "update_steps": 32
      }
    },
    "objective": "Implement and test the first tabular stochastic-calibrated successor-distance variant, comparing calibration-only against successor-distance + TRL-log on the existing horizon-holdout and risky-shortcut diagnostics.",
    "review": "weak_pass",
    "review_reasons": [
      "Required outputs are present: research/sto_trl/results/0004_result.json, research/sto_trl/results/0004_summary.md, and populated artifacts under research/sto_trl/artifacts/0004.",
      "Result JSON validates against schemas/result.schema.json with artifact checks.",
      "The artifact script separately reports successor_calibration_only and successor_distance_trl_log, with successor lambda_tr=0.75 and saved successor score/distance tables.",
      "... 5 more; inspect full file"
    ],
    "risk_flags": [
      "successor_distance_trl_log is behaviorally identical or near-identical to trl_log in the saved main metrics, so the result supports the calibration-only versus transitive-relaxatio...",
      "self_normalize_successor_scores divides by max([scores] + [1.0]), which is an identity transform for scores already in [0,1]; successor_calibration_only therefore matches mc_superv...",
      "git status still shows modified control/config/test files, including scripts/autoresearcher.py and autoresearcher.yaml. Their mtimes predate the 0004 artifact generation, but the d...",
      "... 1 more; inspect full file"
    ],
    "status": "completed"
  },
  {
    "allows_auto_continue": true,
    "baseline_metrics": {
      "_key_count": 3,
      "_keys": [
        "main_mean_heldout_long_horizon_value_mse",
        "main_rows",
        "method"
      ],
      "scalars": {
        "main_mean_heldout_long_horizon_value_mse": 0.21524060774329223,
        "method": "successor_calibration_only"
      }
    },
    "claim_tested": "A successor-distance lambda sweep can reveal whether successor_distance_trl_log has a distinct effect beyond trl_log while retaining calibration and lower held-out error than calibration-only.",
    "decision": "continue",
    "hypothesis": "If the successor-distance formulation is meaningful rather than a relabeling of trl_log, then some predeclared lambda_tr value should change Q/value tables or policy behavior relative to trl_log while retaining lower held-out error than cal...",
    "interpretation": "The audit found negative successor-distance evidence: improving lambdas reduced held-out error by matching trl_log within the predeclared tolerance, so this variant is not yet distinct from trl_log on these tabular diagnostics.",
    "iteration": "0005",
    "metrics": {
      "_key_count": 9,
      "_keys": [
        "aggregate",
        "equivalence_tolerance",
        "experiment_id",
        "gamma",
        "label_horizon_cutoff",
        "lambda_sweep",
        "scenarios",
        "success_checks",
        "update_steps"
      ],
      "nested_samples": {
        "aggregate": {
          "any_positive_successor_evidence": false,
          "successor_calibration_only_main_mean_heldout_mse": 0.21524060774329223
        },
        "success_checks": {
          "chain_raw_exact": true,
          "chain_trl_log_exact": true,
          "positive_successor_evidence": false
        }
      },
      "scalars": {
        "equivalence_tolerance": 1e-10,
        "experiment_id": "0005",
        "gamma": 0.9,
        "label_horizon_cutoff": 2,
        "update_steps": 32
      }
    },
    "objective": "Run a small successor-distance lambda and equivalence audit to determine whether successor_distance_trl_log has a distinct effect beyond trl_log and calibration-only on the existing tabular chain and risky-shortcut diagnostics.",
    "review": "pass",
    "review_reasons": [
      "Required result, summary, and 0005 artifact files were produced, including raw metrics, CSV metrics, lambda sweep, equivalence diagnostics, distance diagnostics, datasets, transiti...",
      "The result JSON validates against schemas/result.schema.json with artifact checks.",
      "The lambda sweep uses the predeclared weights [0.0, 0.25, 0.5, 0.75, 1.0] and reports calibration-only, trl_log, mc_plus_trl_log, and successor-distance variants on the same four s...",
      "... 2 more; inspect full file"
    ],
    "risk_flags": [
      "Working tree contains pre-existing modified control/config/test files, including scripts/autoresearcher.py, so the no-control-file-edit criterion cannot be proven from git status a...",
      "commands_run records copy, run, and validation commands, but not any manual edit steps used to adapt the copied 0004 script into the 0005 audit.",
      "A generated __pycache__/ directory exists under artifacts/0005; harmless but extra artifact noise.",
      "... 1 more; inspect full file"
    ],
    "status": "completed"
  },
  {
    "allows_auto_continue": true,
    "baseline_metrics": {
      "_key_count": 4,
      "_keys": [
        "chain_len9_holdout",
        "method",
        "risk_optimal_matched",
        "safe_optimal_lucky_only_stress"
      ],
      "nested_samples": {
        "chain_len9_holdout": {
          "calibration_error": 4.336808689942018e-18,
          "chose_exact_optimal_action": true,
          "exact_optimal_action": "right",
          "heldout_long_horizon_value_mse": 2.9347503914472164e-34,
          "policy_regret": 0.0,
          "q_calibration_error": 4.336808689942018e-18,
          "q_overestimation_error": 5.551115123125783e-17,
          "risky_action_selection_rate": 0.0
        },
        "risk_optimal_matched": {
          "calibration_error": 1.734723475976807e-18,
          "chose_exact_optimal_action": true,
          "exact_optimal_action": "risky",
          "heldout_long_horizon_value_mse": 0.0,
          "policy_regret": 0.0,
          "q_calibration_error": 1.734723475976807e-18,
          "q_overestimation_error": 2.7755575615628914e-17,
          "risky_action_selection_rate": 1.0
        },
        "safe_optimal_lucky_only_stress": {
          "calibration_error": 0.084375,
          "chose_exact_optimal_action": false,
          "exact_optimal_action": "safe",
          "heldout_long_horizon_value_mse": 0.029240999999999975,
          "policy_regret": 0.5040000000000001,
          "q_calibration_error": 0.084375,
          "q_overestimation_error": 0.675,
          "risky_action_selection_rate": 1.0
        }
      },
      "scalars": {
        "method": "trl_log"
      }
    },
    "claim_tested": "A one-sided count-based conservative log-TRL backup can reduce lucky-only risky overestimation without breaking deterministic recovery or matched risk-optimal action selection.",
    "decision": "pivot",
    "hypothesis": "A small uncertainty penalty based only on offline branch count or outcome variance can reduce lucky-only risky overestimation versus trl_log without breaking deterministic horizon recovery or incorrectly avoiding the risky action when it is...",
    "interpretation": "one_sided_conservative_log_trl_alpha_0_20 reduced the lucky-only safe-optimal failure versus trl_log while preserving the chain and selecting risky with zero regret in the matched risk-optimal scenario.",
    "iteration": "0006",
    "metrics": {
      "_key_count": 9,
      "_keys": [
        "aggregate",
        "alpha_grid",
        "experiment_id",
        "gamma",
        "label_horizon_cutoff",
        "scenarios",
        "success_checks",
        "successor_baseline_lambda",
        "update_steps"
      ],
      "nested_samples": {
        "aggregate": {
          "best_positive_method": "one_sided_conservative_log_trl_alpha_0_20",
          "positive_uncertainty_evidence": true,
          "trl_log_safe_lucky_policy_regret": 0.5040000000000001,
          "trl_log_safe_lucky_q_overestimation": 0.675
        },
        "success_checks": {
          "chain_raw_exact": true,
          "chain_trl_log_exact": true,
          "positive_uncertainty_evidence": true
        }
      },
      "scalars": {
        "experiment_id": "0006",
        "gamma": 0.9,
        "label_horizon_cutoff": 2,
        "successor_baseline_lambda": 0.25,
        "update_steps": 32
      }
    },
    "objective": "Test a minimal uncertainty-aware or one-sided conservative log-TRL backup on the tabular biased-coverage failure while preserving matched safe-optimal, matched risk-optimal, and deterministic long-horizon behavior.",
    "review": "weak_pass",
    "review_reasons": [
      "Required result, summary, and artifact files for 0006 are present, and the result JSON validates against schemas/result.schema.json with artifact checks.",
      "The experiment reports the full alpha grid [0.0, 0.2, 0.4, 0.6], includes the zero baseline, and compares against mc_supervised, trl_raw, trl_log, mc_plus_trl_log, and successor_di...",
      "Exact DP evaluation is present for chain_len9_holdout, safe_optimal_matched, risk_optimal_matched, safe_optimal_lucky_only_stress, and risk_optimal_no_success_stress; the matched r...",
      "... 2 more; inspect full file"
    ],
    "risk_flags": [
      "The aggregate labels one_sided_conservative_log_trl_alpha_0_20 as best_positive_method even though alpha 0.40 and 0.60 also eliminate lucky-only policy regret; this is a first-posi...",
      "The interpretation says alpha 0.20 reduced the lucky-only safe-optimal failure, but alpha 0.20 still selects risky with policy regret 0.504; the stronger claim should be limited to...",
      "The risk_optimal_no_success_stress case remains a biased-coverage failure for trl_log and all conservative alpha values: they select safe with regret 0.081 despite the true risky o...",
      "... 4 more; inspect full file"
    ],
    "status": "completed"
  },
  {
    "allows_auto_continue": true,
    "baseline_metrics": {
      "_key_count": 4,
      "_keys": [
        "chain_len9_holdout",
        "method",
        "risk_optimal_matched",
        "safe_optimal_lucky_only_stress"
      ],
      "nested_samples": {
        "chain_len9_holdout": {
          "calibration_error": 4.336808689942018e-18,
          "chose_exact_optimal_action": true,
          "exact_optimal_action": "right",
          "heldout_long_horizon_value_mse": 2.9347503914472164e-34,
          "policy_regret": 0.0,
          "q_calibration_error": 4.336808689942018e-18,
          "q_overestimation_error": 5.551115123125783e-17,
          "risky_action_selection_rate": 0.0
        },
        "risk_optimal_matched": {
          "calibration_error": 1.734723475976807e-18,
          "chose_exact_optimal_action": true,
          "exact_optimal_action": "risky",
          "heldout_long_horizon_value_mse": 0.0,
          "policy_regret": 0.0,
          "q_calibration_error": 1.734723475976807e-18,
          "q_overestimation_error": 2.7755575615628914e-17,
          "risky_action_selection_rate": 1.0
        },
        "safe_optimal_lucky_only_stress": {
          "calibration_error": 0.084375,
          "chose_exact_optimal_action": false,
          "exact_optimal_action": "safe",
          "heldout_long_horizon_value_mse": 0.029240999999999975,
          "policy_regret": 0.5040000000000001,
          "q_calibration_error": 0.084375,
          "q_overestimation_error": 0.675,
          "risky_action_selection_rate": 1.0
        }
      },
      "scalars": {
        "method": "trl_log"
      }
    },
    "claim_tested": "A generic count-based posterior branch-uncertainty penalty can replace the hand-shaped 0006 shortcut rule while reducing lucky-only overestimation and preserving matched risk-optimal behavior.",
    "decision": "needs_human",
    "hypothesis": "A branch-uncertainty penalty computed only from offline outcome counts, such as a Dirichlet/Beta posterior lower-confidence estimate or small bootstrap variance penalty, will reduce safe-optimal lucky-only overestimation versus trl_log with...",
    "interpretation": "generic_dirichlet_unknown_prior_0_50_alpha_0_50 reduced safe-optimal lucky-only overestimation versus trl_log while preserving the chain and selecting risky with zero regret in the matched risk-optimal scenario.",
    "iteration": "0007",
    "metrics": {
      "_key_count": 11,
      "_keys": [
        "aggregate",
        "best_0006_alpha",
        "experiment_id",
        "gamma",
        "generic_alpha_grid",
        "generic_prior_grid",
        "label_horizon_cutoff",
        "scenarios",
        "success_checks",
        "successor_baseline_lambda",
        "update_steps"
      ],
      "nested_samples": {
        "aggregate": {
          "best_positive_method": "generic_dirichlet_unknown_prior_0_50_alpha_0_50",
          "one_sided_0006_safe_lucky_policy_regret": 0.0,
          "one_sided_0006_safe_lucky_q_overestimation": 0.495,
          "positive_generic_uncertainty_evidence": true,
          "risk_optimal_no_success_unsolved_by_best_positive": true,
          "trl_log_safe_lucky_policy_regret": 0.5040000000000001,
          "trl_log_safe_lucky_q_overestimation": 0.675
        },
        "success_checks": {
          "chain_raw_exact": true,
          "chain_trl_log_exact": true,
          "positive_generic_uncertainty_evidence": true
        }
      },
      "scalars": {
        "best_0006_alpha": 0.4,
        "experiment_id": "0007",
        "gamma": 0.9,
        "label_horizon_cutoff": 2,
        "successor_baseline_lambda": 0.25,
        "update_steps": 32
      }
    },
    "objective": "Test whether a generic tabular posterior or bootstrap branch-uncertainty penalty can replace the hand-shaped one-sided shortcut rule from 0006 while reducing biased lucky-only risky overestimation and preserving deterministic and matched ri...",
    "review": "weak_pass",
    "review_reasons": [
      "Required result, summary, and listed 0007 artifacts are present, and result validation returned ok.",
      "The executor used the same five 0006 scenarios; 0007 offline_datasets.json and transition_tables.json match 0006 byte-for-byte, so the comparisons are on the same datasets.",
      "metrics.csv includes all required baselines, the 0006 one-sided comparison row, and the full generic grid: two priors by three alphas, including zero-penalty baselines.",
      "... 4 more; inspect full file"
    ],
    "risk_flags": [
      "Do not treat 0007 as showing that the generic method fully replaces the 0006 one-sided rule; it only gives modest Q-overestimation reduction without fixing lucky-only policy regret...",
      "known_failures is empty despite risk_optimal_no_success_stress remaining unsolved; this is acceptable for continuation only because the limitation is explicit in metrics and summar...",
      "The current worktree has unrelated uncommitted modifications to scripts/autoresearcher.py, but the 0007 result commit did not include that protected file."
    ],
    "status": "completed"
  }
]
```


## Latest supervisor decision

```json
{
  "confidence": 0.74,
  "decision": "stop",
  "evidence": [
    "0007 result and review report required result, summary, and artifacts, and the review says validation returned ok with artifact checks.",
    "0007 uses the same five 0006 scenarios and the review reports 0007 offline_datasets.json and transition_tables.json match 0006 byte-for-byte, making comparisons controlled.",
    "0007 review classifies the result as weak_pass and says the positive result is narrow: reduced safe_optimal_lucky_only Q overestimation versus trl_log, preserved chain recovery, and zero regret in risk_optimal_matched.",
    "0007 metrics report best_positive_method=generic_dirichlet_unknown_prior_0_50_alpha_0_50 but safe_optimal_lucky_only policy_regret remains 0.504, unchanged from trl_log, and the method still selects risky.",
    "0007 aggregate reports one_sided_0006_safe_lucky_policy_regret=0.0 and one_sided_0006_safe_lucky_q_overestimation=0.495, while generic variants keep lucky-only policy regret at 0.504, so the generic method does not replace the hand-shaped 0006 rule.",
    "0007 reports risk_optimal_no_success_unsolved_by_best_positive=true, and the review says this stress case remains unsolved by the generic variants.",
    "Prior 0005 evidence remains negative for the explicit successor-distance direction: all improving successor-distance lambdas were equivalent to trl_log within tolerance and any_positive_successor_evidence=false.",
    "The charter's early positive evidence has already been established for raw TRL overoptimism and log-TRL long-horizon recovery, but the stochastic-calibrated extension has not produced robust general evidence beyond hand-shaped tabular penalties."
  ],
  "next_experiment": null,
  "progress_score": 6,
  "rationale": "The tabular loop has answered the core early question well enough to stop before adding another low-value variant. The strong results are for ordinary log TRL under matched coverage and for raw TRL's support-driven overoptimism. The distinct successor-distance variant failed an equivalence audit, the hand-shaped uncertainty penalty from 0006 only weakly supports a narrow fix, and 0007's generic uncertainty replacement does not fix the policy-level lucky-only failure and remains worse than the hand-shaped rule. Another tabular uncertainty tweak would likely be exploration around an assumption choice rather than a decisive test of the charter hypothesis.",
  "risks": [
    "Stopping does not mean log TRL is useless; it means the proposed stochastic successor-distance or generic uncertainty extension is not yet justified by the tabular evidence.",
    "There may be a useful method with a stronger explicit prior or model-based uncertainty assumption, but choosing that assumption is now a design pivot that needs human judgment rather than another automatic small sweep.",
    "Moving next to neural networks, OGBench, PointMaze, or larger tasks would violate the charter's caution because the tabular stochastic-calibration story remains weak.",
    "The current worktree has unrelated uncommitted protected-file modifications according to the 0007 review, so future executor work should continue to avoid control-file edits."
  ]
}
```


## Recent decision summaries

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

## 0008_decision.json

```json
{
  "confidence": 0.74,
  "decision": "stop",
  "evidence": [
    "0007 result and review report required result, summary, and artifacts, and the review says validation returned ok with artifact checks.",
    "0007 uses the same five 0006 scenarios and the review reports 0007 offline_datasets.json and transition_tables.json match 0006 byte-for-byte, making comparisons controlled.",
    "0007 review classifies the result as weak_pass and says the positive result is narrow: reduced safe_optimal_lucky_only Q overestimation versus trl_log, preserved chain recovery, and zero regret in risk_optimal_matched.",
    "0007 metrics report best_positive_method=generic_dirichlet_unknown_prior_0_50_alpha_0_50 but safe_optimal_lucky_only policy_regret remains 0.504, unchanged from trl_log, and the method still selects risky.",
    "0007 aggregate reports one_sided_0006_safe_lucky_policy_regret=0.0 and one_sided_0006_safe_lucky_q_overestimation=0.495, while generic variants keep lucky-only policy regret at 0.504, so the generic method does not replace the hand-shaped 0006 rule.",
    "0007 reports risk_optimal_no_success_unsolved_by_best_positive=true, and the review says this stress case remains unsolved by the generic variants.",
    "Prior 0005 evidence remains negative for the explicit successor-distance direction: all improving successor-distance lambdas were equivalent to trl_log within tolerance and any_positive_successor_evidence=false.",
    "The charter's early positive evidence has already been established for raw TRL overoptimism and log-TRL long-horizon recovery, but the stochastic-calibrated extension has not produced robust general evidence beyond hand-shaped tabular penalties."
  ],
  "next_experiment": null,
  "progress_score": 6,
  "rationale": "The tabular loop has answered the core early question well enough to stop before adding another low-value variant. The strong results are for ordinary log TRL under matched coverage and for raw TRL's support-driven overoptimism. The distinct successor-distance variant failed an equivalence audit, the hand-shaped uncertainty penalty from 0006 only weakly supports a narrow fix, and 0007's generic uncertainty replacement does not fix the policy-level lucky-only failure and remains worse than the hand-shaped rule. Another tabular uncertainty tweak would likely be exploration around an assumption choice rather than a decisive test of the charter hypothesis.",
  "risks": [
    "Stopping does not mean log TRL is useless; it means the proposed stochastic successor-distance or generic uncertainty extension is not yet justified by the tabular evidence.",
    "There may be a useful method with a stronger explicit prior or model-based uncertainty assumption, but choosing that assumption is now a design pivot that needs human judgment rather than another automatic small sweep.",
    "Moving next to neural networks, OGBench, PointMaze, or larger tasks would violate the charter's caution because the tabular stochastic-calibration story remains weak.",
    "The current worktree has unrelated uncommitted protected-file modifications according to the 0007 review, so future executor work should continue to avoid control-file edits."
  ]
}
```


## Recent review summaries

## 0005_review.json

```json
{
  "allows_auto_continue": true,
  "evidence_checked": [
    "research/sto_trl/results/0005_result.json",
    "research/sto_trl/results/0005_summary.md",
    "research/sto_trl/artifacts/0005/ file listing",
    "research/sto_trl/artifacts/0005/run_lambda_equivalence_audit.py constants and setup",
    "python scripts/validate_artifacts.py --repo-root . --json research/sto_trl/results/0005_result.json --schema schemas/result.schema.json --check-result-artifacts",
    "git status --short"
  ],
  "experiment_id": "0005",
  "reasons": [
    "Required result, summary, and 0005 artifact files were produced, including raw metrics, CSV metrics, lambda sweep, equivalence diagnostics, distance diagnostics, datasets, transitions, and value tables.",
    "The result JSON validates against schemas/result.schema.json with artifact checks.",
    "The lambda sweep uses the predeclared weights [0.0, 0.25, 0.5, 0.75, 1.0] and reports calibration-only, trl_log, mc_plus_trl_log, and successor-distance variants on the same four scenarios.",
    "Equivalence diagnostics versus trl_log include the requested Q/value/action/MSE/regret/overestimation deltas by scenario and lambda.",
    "The interpretation is appropriately negative: improving successor-distance lambdas are reported as equivalent to trl_log within tolerance, so no distinct successor-distance win is claimed."
  ],
  "required_fixes": [],
  "risk_flags": [
    "Working tree contains pre-existing modified control/config/test files, including scripts/autoresearcher.py, so the no-control-file-edit criterion cannot be proven from git status alone.",
    "commands_run records copy, run, and validation commands, but not any manual edit steps used to adapt the copied 0004 script into the 0005 audit.",
    "A generated __pycache__/ directory exists under artifacts/0005; harmless but extra artifact noise.",
    "Supervisor should continue only treating 0005 as negative evidence for distinct successor-distance value, not as support for the prior positive 0004 interpretation."
  ],
  "verdict": "pass"
}
```

## 0006_review.json

```json
{
  "allows_auto_continue": true,
  "evidence_checked": {
    "_type": "list",
    "first_items": [
      "research/sto_trl/results/0006_result.json",
      "research/sto_trl/results/0006_summary.md",
      "research/sto_trl/artifacts/0006/ file listing"
    ],
    "length": 9
  },
  "experiment_id": "0006",
  "reasons": [
    "Required result, summary, and artifact files for 0006 are present, and the result JSON validates against schemas/result.schema.json with artifact checks.",
    "The experiment reports the full alpha grid [0.0, 0.2, 0.4, 0.6], includes the zero baseline, and compares against mc_supervised, trl_raw, trl_log, mc_plus_trl_log, and successor_distance_best_0005 on the same constructed scenarios.",
    "Exact DP evaluation is present for chain_len9_holdout, safe_optimal_matched, risk_optimal_matched, safe_optimal_lucky_only_stress, and risk_optimal_no_success_stress; the matched risk-optimal anti-conservatism check is included.",
    "The penalty implementation inspected in the artifact source uses empirical transition counts, observed branch count, and a count penalty; I did not find use of exact DP values or true transition probabilities in the penalty computation itself.",
    "The positive-evidence criterion is technically met because nonzero alphas reduce lucky-only Q overestimation while preserving chain recovery and matched risk-optimal action selection, but the interpretation is somewhat optimistic because the reported best positive alpha 0.20 still selects risky and keeps full lucky-only policy regret."
  ],
  "required_fixes": [],
  "risk_flags": [
    "The aggregate labels one_sided_conservative_log_trl_alpha_0_20 as best_positive_method even though alpha 0.40 and 0.60 also eliminate lucky-only policy regret; this is a first-positive selection, not a best-by-regret selection.",
    "The interpretation says alpha 0.20 reduced the lucky-only safe-optimal failure, but alpha 0.20 still selects risky with policy regret 0.504; the stronger claim should be limited to reduced overestimation/held-out MSE unless using alpha 0.40 or 0.60.",
    "The risk_optimal_no_success_stress case remains a biased-coverage failure for trl_log and all conservative alpha values: they select safe with regret 0.081 despite the true risky optimum.",
    "The penalty eligibility rule is hand-shaped around direct-goal single-branch shortcut actions at multi-action states, so evidence may not generalize beyond these toy diagnostics.",
    "Working tree contains modified control/config/test files including scripts/autoresearcher.py and additional state files; these appear outside the 0006 artifact set but prevent proving the no-control-file-edit criterion from git status alone.",
    "commands_run records copy, run, and validation commands, but not any manual edit steps used to adapt the copied 0005 script into the 0006 experiment.",
    "A generated __pycache__/ directory exists under artifacts/0006; harmless but extra artifact noise."
  ],
  "verdict": "weak_pass"
}
```

## 0007_review.json

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


## Existing progress summaries

- `research/sto_trl/progress/0007_manual_summary.md`
- `research/sto_trl/progress/latest_summary.md`


## Full evidence paths

- `research/sto_trl/plans/0001_plan.md`
- `research/sto_trl/plans/0002_plan.md`
- `research/sto_trl/plans/0003_plan.md`
- `research/sto_trl/plans/0004_plan.md`
- `research/sto_trl/plans/0005_plan.md`
- `research/sto_trl/plans/0006_plan.md`
- `research/sto_trl/plans/0007_plan.md`
- `research/sto_trl/results/0001_summary.md`
- `research/sto_trl/results/0002_summary.md`
- `research/sto_trl/results/0003_summary.md`
- `research/sto_trl/results/0004_summary.md`
- `research/sto_trl/results/0005_summary.md`
- `research/sto_trl/results/0006_summary.md`
- `research/sto_trl/results/0007_summary.md`
- `research/sto_trl/results/0001_result.json`
- `research/sto_trl/results/0002_result.json`
- `research/sto_trl/results/0003_result.json`
- `research/sto_trl/results/0004_result.json`
- `research/sto_trl/results/0005_result.json`
- `research/sto_trl/results/0006_result.json`
- `research/sto_trl/results/0007_result.json`
- `research/sto_trl/reviews/0001_review.md`
- `research/sto_trl/reviews/0002_review.md`
- `research/sto_trl/reviews/0003_review.md`
- `research/sto_trl/reviews/0004_review.md`
- `research/sto_trl/reviews/0005_review.md`
- `research/sto_trl/reviews/0006_review.md`
- `research/sto_trl/reviews/0007_review.md`
- `research/sto_trl/decisions/0001_decision.md`
- `research/sto_trl/decisions/0002_decision.md`
- `research/sto_trl/decisions/0003_decision.md`
- `research/sto_trl/decisions/0004_decision.md`
- `research/sto_trl/decisions/0005_decision.md`
- `research/sto_trl/decisions/0006_decision.md`
- `research/sto_trl/decisions/0007_decision.md`
- `research/sto_trl/decisions/0008_decision.md`
