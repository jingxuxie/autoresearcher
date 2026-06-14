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
  "iteration": 11,
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
  "_source": "/home/eston/autoresearcher/research/sto_trl/results/0011_result.json",
  "artifacts": {
    "_type": "list",
    "first_items": [
      "research/sto_trl/artifacts/0011/randomized_equivalence_audit.py",
      "research/sto_trl/artifacts/0011/raw_metrics.json",
      "research/sto_trl/artifacts/0011/metrics.csv"
    ],
    "length": 10
  },
  "baseline_metrics": {
    "empirical_model_dp": {
      "action_accuracy": 0.4,
      "mean_all_pair_value_mse": 0.04481289688774978,
      "mean_heldout_long_horizon_value_mse": 0.03765166954543893,
      "mean_policy_regret": 0.06840668344867584,
      "mean_risky_q_calibration_error": 0.22652428374775355,
      "mean_risky_q_overestimation": 0.07214453318022322,
      "mean_risky_q_underestimation": 0.15437975056753034,
      "num_rows": 15,
      "risky_action_selection_rate": 0.4
    },
    "mc_supervised": {
      "action_accuracy": 0.4,
      "mean_all_pair_value_mse": 0.23531227403396845,
      "mean_heldout_long_horizon_value_mse": 0.432704401392902,
      "mean_policy_regret": 0.028055308380006028,
      "mean_risky_q_calibration_error": 0.5690452173873072,
      "mean_risky_q_overestimation": 0.0,
      "mean_risky_q_underestimation": 0.5690452173873072,
      "num_rows": 15,
      "risky_action_selection_rate": 0.0
    },
    "posterior_lower_q10_model_dp": {
      "action_accuracy": 0.4666666666666667,
      "mean_all_pair_value_mse": 0.04437558018198091,
      "mean_heldout_long_horizon_value_mse": 0.03592521474547472,
      "mean_policy_regret": 0.02218223230951611,
      "mean_risky_q_calibration_error": 0.2615099351506468,
      "mean_risky_q_overestimation": 0.01626917888166985,
      "mean_risky_q_underestimation": 0.245240756268977,
      "num_rows": 15,
      "risky_action_selection_rate": 0.06666666666666667
    },
    "posterior_mean_model_dp": {
      "action_accuracy": 0.6,
      "mean_all_pair_value_mse": 0.0423569966153239,
      "mean_heldout_long_horizon_value_mse": 0.032259348981387076,
      "mean_policy_regret": 0.012917304567005971,
      "mean_risky_q_calibration_error": 0.21422137774804942,
      "mean_risky_q_overestimation": 0.045769378881669855,
      "mean_risky_q_underestimation": 0.16845199886637957,
      "num_rows": 15,
      "risky_action_selection_rate": 0.2
    },
    "trl_log": {
      "action_accuracy": 0.4,
      "mean_all_pair_value_mse": 0.04481289688774978,
      "mean_heldout_long_horizon_value_mse": 0.03765166954543893,
      "mean_policy_regret": 0.06840668344867584,
      "mean_risky_q_calibration_error": 0.22652428374775355,
      "mean_risky_q_overestimation": 0.07214453318022322,
      "mean_risky_q_underestimation": 0.15437975056753034,
      "num_rows": 15,
      "risky_action_selection_rate": 0.4
    }
  },
  "claim_tested": "A fixed tiny randomized suite tested whether posterior TRL-log has distinct value over prior-matched posterior model DP beyond handcrafted branch-chain regimes.",
  "experiment_id": "0011",
  "interpretation": "The randomized tiny-suite audit supports the 0010 boundary result: posterior TRL-log variants match the prior-matched posterior mean model-DP baseline within numerical tolerance across branch-chain, stochastic stitching, and teleporter families. Any aggregate improvement over plain TRL-log is explained by the shared posterior transition prior, not by a distinct transitive posterior TRL effect.",
  "known_failures": [
    "posterior_trl_log and posterior_mc_plus_trl_log were near-equivalent to prior-matched posterior mean model DP across the randomized suite.",
    "No credible posterior TRL benefit over both TRL-log and prior-matched posterior model DP was detected."
  ],
  "metrics": {
    "coverage_diagnostics": {
      "label_horizon_cutoff": 2,
      "tag_counts": {
        "_type": "object",
        "key_count": 9,
        "keys": [
          "ambiguous",
          "biased_coverage",
          "lucky_only",
          "matched",
          "no_success",
          "prior_dependent",
          "risk_optimal",
          "safe_optimal",
          "sparse_coverage"
        ]
      }
    },
    "equivalence_aggregate": {
      "action_disagreement_rate_posterior_mc_plus_vs_model": 0.0,
      "action_disagreement_rate_posterior_trl_log_vs_model": 0.0,
      "best_candidate": "posterior_mc_plus_trl_log",
      "candidate_improves_vs_prior_matched_model_dp": false,
      "candidate_improves_vs_trl_log": true,
      "matched_risk_optimal_preserved": true,
      "max_abs_value_diff_posterior_mc_plus_vs_model": 3.3306690738754696e-16,
      "max_abs_value_diff_posterior_trl_log_vs_model": 0.0,
      "not_safe_everywhere": true,
      "positive_evidence": false,
      "posterior_trl_near_equivalent_to_prior_matched_model_dp": true
    },
    "families": [
      "branch_chain",
      "stochastic_stitching",
      "teleporter"
    ],
    "matched_risk_optimal_preserved": true,
    "method_summary": {
      "empirical_model_dp": {
        "_type": "object",
        "key_count": 9,
        "keys": [
          "action_accuracy",
          "mean_all_pair_value_mse",
          "mean_heldout_long_horizon_value_mse",
          "mean_policy_regret",
          "mean_risky_q_calibration_error",
          "mean_risky_q_overestimation",
          "mean_risky_q_underestimation",
          "num_rows",
          "risky_action_selection_rate"
        ]
      },
      "mc_supervised": {
        "_type": "object",
        "key_count": 9,
        "keys": [
          "action_accuracy",
          "mean_all_pair_value_mse",
          "mean_heldout_long_horizon_value_mse",
          "mean_policy_regret",
          "mean_risky_q_calibration_error",
          "mean_risky_q_overestimation",
          "mean_risky_q_underestimation",
          "num_rows",
          "risky_action_selection_rate"
        ]
      },
      "posterior_lower_q10_model_dp": {
        "_type": "object",
        "key_count": 9,
        "keys": [
          "action_accuracy",
          "mean_all_pair_value_mse",
          "mean_heldout_long_horizon_value_mse",
          "mean_policy_regret",
          "mean_risky_q_calibration_error",
          "mean_risky_q_overestimation",
          "mean_risky_q_underestimation",
          "num_rows",
          "risky_action_selection_rate"
        ]
      },
      "posterior_mc_plus_trl_log": {
        "_type": "object",
        "key_count": 9,
        "keys": [
          "action_accuracy",
          "mean_all_pair_value_mse",
          "mean_heldout_long_horizon_value_mse",
          "mean_policy_regret",
          "mean_risky_q_calibration_error",
          "mean_risky_q_overestimation",
          "mean_risky_q_underestimation",
          "num_rows",
          "risky_action_selection_rate"
        ]
      },
      "posterior_mean_model_dp": {
        "_type": "object",
        "key_count": 9,
        "keys": [
          "action_accuracy",
          "mean_all_pair_value_mse",
          "mean_heldout_long_horizon_value_mse",
          "mean_policy_regret",
          "mean_risky_q_calibration_error",
          "mean_risky_q_overestimation",
          "mean_risky_q_underestimation",
          "num_rows",
          "risky_action_selection_rate"
        ]
      },
      "posterior_trl_log": {
        "_type": "object",
        "key_count": 9,
        "keys": [
          "action_accuracy",
          "mean_all_pair_value_mse",
          "mean_heldout_long_horizon_value_mse",
          "mean_policy_regret",
          "mean_risky_q_calibration_error",
          "mean_risky_q_overestimation",
          "mean_risky_q_underestimation",
          "num_rows",
          "risky_action_selection_rate"
        ]
      },
      "trl_log": {
        "_type": "object",
        "key_count": 9,
        "keys": [
          "action_accuracy",
          "mean_all_pair_value_mse",
          "mean_heldout_long_horizon_value_mse",
          "mean_policy_regret",
          "mean_risky_q_calibration_error",
          "mean_risky_q_overestimation",
          "mean_risky_q_underestimation",
          "num_rows",
          "risky_action_selection_rate"
        ]
      },
      "trl_raw": {
        "_type": "object",
        "key_count": 9,
        "keys": [
          "action_accuracy",
          "mean_all_pair_value_mse",
          "mean_heldout_long_horizon_value_mse",
          "mean_policy_regret",
          "mean_risky_q_calibration_error",
          "mean_risky_q_overestimation",
          "mean_risky_q_underestimation",
          "num_rows",
          "risky_action_selection_rate"
        ]
      }
    },
    "num_mdps": 15,
    "num_method_rows": 120,
    "positive_evidence": false,
    "posterior_trl_near_equivalent_to_prior_matched_model_dp": true,
    "seeds": [
      0,
      1,
      2,
      3,
      4
    ]
  },
  "next_questions": [
    "Can a future posterior TRL method beat posterior model DP only when state aliases or partial observability make model DP insufficient?",
    "Should posterior TRL audits require model-DP equivalence checks by default?",
    "Which explicit priors should be predeclared for no-success risk-optimal regimes?"
  ],
  "status": "completed"
}
```


## Latest summary

# Experiment 0011 Summary

## Objective

Run a randomized tabular equivalence and generalization audit for posterior TRL-log versus prior-matched posterior model DP.

## Commands Run

```bash
mkdir -p research/sto_trl/artifacts/0011 research/sto_trl/results
conda run -n autoresearcher_sto_trl python research/sto_trl/artifacts/0011/randomized_equivalence_audit.py
conda run -n autoresearcher_sto_trl python scripts/validate_artifacts.py --repo-root . --json research/sto_trl/results/0011_result.json --schema schemas/result.schema.json --check-result-artifacts
```

## Suite

- Families: `['branch_chain', 'stochastic_stitching', 'teleporter']`
- Seeds per family: `[0, 1, 2, 3, 4]`
- Total MDPs: `15`
- Label horizon cutoff: `2`

## Method Summary

| Method | Action accuracy | Heldout MSE | Policy regret | Risky rate | Q overestimation | Calibration error |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| empirical_model_dp | 0.400000 | 0.037651669545 | 0.068406683449 | 0.400000 | 0.072144533180 | 0.226524283748 |
| mc_supervised | 0.400000 | 0.432704401393 | 0.028055308380 | 0.000000 | 0.000000000000 | 0.569045217387 |
| posterior_lower_q10_model_dp | 0.466667 | 0.035925214745 | 0.022182232310 | 0.066667 | 0.016269178882 | 0.261509935151 |
| posterior_mc_plus_trl_log | 0.600000 | 0.032259348981 | 0.012917304567 | 0.200000 | 0.045769378882 | 0.214221377748 |
| posterior_mean_model_dp | 0.600000 | 0.032259348981 | 0.012917304567 | 0.200000 | 0.045769378882 | 0.214221377748 |
| posterior_trl_log | 0.600000 | 0.032259348981 | 0.012917304567 | 0.200000 | 0.045769378882 | 0.214221377748 |
| trl_log | 0.400000 | 0.037651669545 | 0.068406683449 | 0.400000 | 0.072144533180 | 0.226524283748 |
| trl_raw | 0.400000 | 0.041975170307 | 0.097601010862 | 0.800000 | 0.154109702482 | 0.294064622351 |

## Equivalence Audit

- Positive posterior TRL evidence: `False`
- Near-equivalent to prior-matched posterior model DP: `True`
- Max posterior_trl_log value difference vs model DP: `0`
- Posterior_trl_log action disagreement rate vs model DP: `0`
- Matched risk-optimal action preserved: `True`

## Interpretation

The randomized tiny-suite audit supports the 0010 boundary result: posterior TRL-log variants match the prior-matched posterior mean model-DP baseline within numerical tolerance across branch-chain, stochastic stitching, and teleporter families. Any aggregate improvement over plain TRL-log is explained by the shared posterior transition prior, not by a distinct transitive posterior TRL effect.

## Artifacts

- `research/sto_trl/artifacts/0011/randomized_equivalence_audit.py`
- `research/sto_trl/artifacts/0011/raw_metrics.json`
- `research/sto_trl/artifacts/0011/metrics.csv`
- `research/sto_trl/artifacts/0011/family_summary.csv`
- `research/sto_trl/artifacts/0011/regime_summary.csv`
- `research/sto_trl/artifacts/0011/equivalence_diagnostics.json`
- `research/sto_trl/artifacts/0011/coverage_diagnostics.json`
- `research/sto_trl/artifacts/0011/offline_datasets.json`
- `research/sto_trl/artifacts/0011/transition_tables.json`
- `research/sto_trl/artifacts/0011/value_tables.json`


## Latest review summary

```json
{
  "allows_auto_continue": true,
  "escalation_reason": null,
  "evidence_checked": {
    "_type": "list",
    "first_items": [
      "research/sto_trl/results/0011_result.json",
      "research/sto_trl/results/0011_summary.md",
      "research/sto_trl/artifacts/0011/randomized_equivalence_audit.py"
    ],
    "length": 15
  },
  "evidence_quality": "medium",
  "experiment_id": "0011",
  "failure_criteria_triggered": false,
  "reasons": [
    "The required 0011 result, summary, and all ten listed artifacts are present, and result/artifact validation returned ok.",
    "The result commit only contains 0011 artifacts/results plus the executor packet; protected files such as schemas, AGENTS.md, scripts/autoresearcher.py, and environment files were not modified in the result commit.",
    "The suite matches the plan: 3 families, 5 fixed seeds each, 15 generated tabular MDPs, CPU runtime about 5.5 seconds, and no large dependencies or expensive training.",
    "metrics.csv contains 120 rows: 15 MDPs by 8 methods, with all planned baselines and posterior TRL variants present for every MDP.",
    "Per-family, per-regime, coverage, transition, value, and equivalence artifacts are present, including family_summary.csv, regime_summary.csv, coverage_diagnostics.json, transition_tables.json, value_tables.json, and equivalence_diagnostics.json.",
    "The code uses exact DP and true transition probabilities for evaluation/audit artifacts, while method decisions use observed transition counts and the declared Beta prior; I did not find evidence of exact-DP training leakage.",
    "The direct equivalence audit supports the interpretation: posterior_trl_log and posterior_mc_plus_trl_log have zero action disagreement with posterior_mean_model_dp and max value differences at numerical precision.",
    "The result correctly treats equivalence and prior-driven improvement as negative or boundary evidence rather than a stochastic TRL win."
  ],
  "required_fixes": [],
  "risk_flags": [
    "The suite is intentionally tiny and tabular; it is suitable for this loop but should not be generalized beyond these toy MDP families.",
    "posterior_trl_log is implemented with the same run_model posterior_mean backup as posterior_mean_model_dp, so the equivalence finding is partly structural; useful as a baseline audit, not as proof about future distinct posterior TRL implementations.",
    "Positive evidence is false; future work should not claim a posterior TRL win from this result.",
    "True transition probabilities are stored in transition_tables.json for audit/evaluation, so future experiments should keep the same clear separation from training inputs."
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
    },
    {
      "allows_auto_continue": true,
      "claim_tested": "Posterior transition uncertainty plus log-space transitive propagation was tested against prior-matched transition-model DP on censored multi-step stochastic branch-chain diagnostics.",
      "decision": "continue",
      "important_metrics": {
        "metrics.best_posterior_trl_candidate": "posterior_trl_log",
        "metrics.chain_guard.start_exact_value": 0.38742048900000015,
        "metrics.coverage_diagnostics.regimes.lucky_only_safe_optimal.label_coverage.risk_1|advance.censored_positive_labels": 0,
        "metrics.coverage_diagnostics.regimes.lucky_only_safe_optimal.label_coverage.risk_1|advance.label_count_used": 4,
        "metrics.coverage_diagnostics.regimes.lucky_only_safe_optimal.label_coverage.risk_1|advance.mean_used_label": 0.81,
        "metrics.coverage_diagnostics.regimes.lucky_only_safe_optimal.label_coverage.risk_1|advance.positive_labels": 4,
        "metrics.coverage_diagnostics.regimes.lucky_only_safe_optimal.label_coverage.risk_1|advance.total_occurrences": 4,
        "metrics.coverage_diagnostics.regimes.lucky_only_safe_optimal.label_coverage.risk_1|advance.zero_labels": 0,
        "metrics.coverage_diagnostics.regimes.lucky_only_safe_optimal.label_coverage.risk_2|advance.censored_positive_labels": 0,
        "metrics.coverage_diagnostics.regimes.lucky_only_safe_optimal.label_coverage.risk_2|advance.label_count_used": 4,
        "metrics.coverage_diagnostics.regimes.lucky_only_safe_optimal.label_coverage.risk_2|advance.mean_used_label": 0.9,
        "metrics.coverage_diagnostics.regimes.lucky_only_safe_optimal.label_coverage.risk_2|advance.positive_labels": 4
      },
      "iteration": "0010",
      "negative_signals": [
        "Matched risk-optimal action preserved by posterior TRL candidates: True.",
        "posterior_trl_log and posterior_mc_plus_trl_log were numerically equivalent to the prior-matched posterior mean model-DP baseline.",
        "No distinct posterior transitive benefit over both TRL-log and prior-matched posterior model DP was detected.",
        "Evidence is still a compact handcrafted tabular diagnostic with five regimes; it establishes a baseline, not a broad claim about stochastic TRL.",
        "posterior_lower_q10_model_dp is conservative and does not preserve matched risk-optimal action, while posterior mean variants preserve matched risk but do not beat prior-matched model DP."
      ],
      "positive_signals": [
        "Positive transitive evidence: False.",
        "Posterior TRL candidates equivalent to posterior model DP: True.",
        "MC-only heldout MSE minus TRL-log heldout MSE: 0.380607415380.",
        "The multi-step branch-chain confirms that transitive backups recover censored long-horizon values better than MC-only, and posterior transition uncertainty changes the risky branch through the declared Beta prior. However, posterior_trl_log and posterior_mc_pl"
      ],
      "review_verdict": "pass",
      "status": "completed"
    },
    {
      "allows_auto_continue": true,
      "claim_tested": "A fixed tiny randomized suite tested whether posterior TRL-log has distinct value over prior-matched posterior model DP beyond handcrafted branch-chain regimes.",
      "decision": "continue",
      "important_metrics": {
        "metrics.coverage_diagnostics.tag_counts.no_success": 3,
        "metrics.coverage_diagnostics.tag_counts.risk_optimal": 9,
        "metrics.equivalence_aggregate.best_candidate": "posterior_mc_plus_trl_log",
        "metrics.equivalence_aggregate.matched_risk_optimal_preserved": true,
        "metrics.equivalence_aggregate.positive_evidence": false,
        "metrics.matched_risk_optimal_preserved": true,
        "metrics.method_summary.empirical_model_dp.mean_all_pair_value_mse": 0.04481289688774978,
        "metrics.method_summary.empirical_model_dp.mean_heldout_long_horizon_value_mse": 0.03765166954543893,
        "metrics.method_summary.empirical_model_dp.mean_policy_regret": 0.06840668344867584,
        "metrics.method_summary.empirical_model_dp.mean_risky_q_calibration_error": 0.22652428374775355,
        "metrics.method_summary.empirical_model_dp.mean_risky_q_overestimation": 0.07214453318022322,
        "metrics.method_summary.empirical_model_dp.mean_risky_q_underestimation": 0.15437975056753034
      },
      "iteration": "0011",
      "negative_signals": [
        "posterior_trl_log and posterior_mc_plus_trl_log were near-equivalent to prior-matched posterior mean model DP across the randomized suite.",
        "No credible posterior TRL benefit over both TRL-log and prior-matched posterior model DP was detected.",
        "The suite is intentionally tiny and tabular; it is suitable for this loop but should not be generalized beyond these toy MDP families.",
        "posterior_trl_log is implemented with the same run_model posterior_mean backup as posterior_mean_model_dp, so the equivalence finding is partly structural; useful as a baseline audit, not as proof about future distinct p...",
        "Positive evidence is false; future work should not claim a posterior TRL win from this result."
      ],
      "positive_signals": [
        "Positive evidence: False.",
        "Near-equivalence to posterior model DP: True.",
        "Max posterior_trl_log value difference vs posterior model DP: 0.",
        "Action disagreement rate vs posterior model DP: 0.",
        "The randomized tiny-suite audit supports the 0010 boundary result: posterior TRL-log variants match the prior-matched posterior mean model-DP baseline within numerical tolerance across branch-chain, stochastic stitching, and teleporter families. Any aggregate "
      ],
      "review_verdict": "pass",
      "status": "completed"
    }
  ],
  "project": "sto_trl"
}
```


## Last decision summaries

## 0010_decision.json

```json
{
  "confidence": 0.8,
  "decision": "continue",
  "evidence": {
    "_type": "list",
    "first_items": [
      "0009 result and review report required result, summary, and all listed artifacts, with result/artifact validation ok.",
      "0009 review reports allows_auto_continue=true, success_criteria_satisfied=true, failure_criteria_triggered=false, and should_escalate_to_pro=false.",
      "Current state reports a Pro decision continue was applied from research/sto_trl/decisions/0010_pro_decision.json, so continuation under the approved plan is not blocked."
    ],
    "length": 9
  },
  "next_experiment": {
    "estimated_runtime_minutes": 25,
    "experiment_id": "0010",
    "hypothesis": "On a multi-step stochastic branch-chain with censored long-horizon labels, posterior transition uncertainty can reduce risky-path overestimation while log-space transitive propagation preserves long-horizon reachability. If posterior TRL-log is equivalent to posterior model DP, or only improves through the same prior, then there is no distinct posterior transitive benefit yet.",
    "objective": "Test whether posterior transition uncertainty plus log-space transitive propagation adds value beyond transition-model DP on a small multi-step tabular stochastic branch-chain diagnostic.",
    "required_outputs": {
      "_type": "list",
      "first_items": [
        "research/sto_trl/artifacts/0010/posterior_transitive_ablation.py",
        "research/sto_trl/artifacts/0010/raw_metrics.json",
        "research/sto_trl/artifacts/0010/metrics.csv"
      ],
      "length": 11
    }
  },
  "progress_score": 7,
  "rationale": "Experiment 0009 passed as a compact transition-posterior baseline audit and gives a clear next gate. It showed that posterior and robust transition-model DP baselines can reduce regret versus TRL-log on selected recoverable regimes, while TRL-log remains identical to empirical model DP on the one-step risky shortcut family. The next small experiment should test the approved next milestone: whether adding log-space transitive propagation to posterior transition uncertainty gives any benefit beyond prior-matched posterior model DP on a multi-step tabular diagnostic where transitive propagation can matter.",
  "risks": [
    "Posterior transitive propagation may collapse to posterior model DP in tabular exact settings; equivalence should be reported as negative or boundary evidence.",
    "Any apparent improvement could come from the prior rather than transitive propagation, so all posterior TRL variants must be compared against prior-matched posterior model DP.",
    "Conservative posterior choices can look good by avoiding risk; matched risk-optimal and ambiguous risk-optimal regimes must be explicit checks.",
    "Keep the experiment tabular and small; do not move to neural networks, continuous control, OGBench, downloads, or broad sweeps.",
    "The deterministic chain guard should be a real raw/log TRL execution check if practical, not only a formula check."
  ]
}
```

## 0010_pro_decision.json

```json
{
  "confidence": 0.78,
  "decision": "continue",
  "evidence": [
    "The latest summary says the project is active after reviewed iteration 0009, with the original successor-distance formulation still weak/negative and the active direction shifted to transition-level stochastic uncertainty plus log-space transitive propagation.",
    "The charter requires small tabular diagnostics first and forbids OGBench, PointMaze, AntMaze, or large neural training before tabular evidence is clean.",
    "0009 found empirical_model_dp, empirical_risky_value, and trl_log had identical mean policy regret 0.1090125 on the representative subset, so one-step risky shortcuts do not show a distinct transitive benefit.",
    "0009 found posterior_lower_q10_dp_beta_1_1 improved target-regime regret versus TRL-log by -0.177525, establishing a stronger transition-uncertainty baseline to beat.",
    "0009 review judged the result weak_pass, validated artifacts and 72 method rows, but warned evidence rests on a handpicked 8-cell subset, the best method is conservative, and the chain guard is only a formula check."
  ],
  "next_experiment": {
    "estimated_runtime_minutes": 30,
    "experiment_id": "0010_posterior_transitive_branch_chain",
    "hypothesis": "If the pivot is promising, posterior_trl_log or posterior_mc_plus_trl_log will improve multi-step stitch/regret metrics over both TRL-log and prior-matched posterior model DP while preserving matched safe-optimal and matched risk-optimal actions.",
    "objective": "Test whether posterior transition uncertainty plus log-space transitive propagation adds value beyond prior-matched transition-model DP on a small multi-step tabular stochastic branch-chain or stitching graph.",
    "required_outputs": [
      "research/sto_trl/results/0010_result.json",
      "research/sto_trl/results/0010_summary.md",
      "research/sto_trl/reviews/0010_review.md",
      "research/sto_trl/artifacts/0010/metrics.csv",
      "research/sto_trl/artifacts/0010/regime_summary.csv",
      "research/sto_trl/artifacts/0010/transition_tables.json",
      "research/sto_trl/artifacts/0010/value_tables.json"
    ]
  },
  "progress_score": null,
  "rationale": "I do not see a local stop recommendation in the latest packet; the local decision is continue with experiment 0010. I agree, but only for one strict small tabular ablation. The project is making real but weak progress after the human pivot: raw TRL overoptimism, log-TRL horizon propagation, and transition-posterior baselines are now characterized, but no distinct stochastic-TRL benefit has been shown yet. The next experiment must directly test whether posterior/log-space transitive propagation adds value beyond prior-matched transition-model DP; equivalence must be counted as negative or boundary evidence.",
  "risks": [
    "Posterior transitive propagation may collapse to posterior model DP in tabular settings, which should not be counted as success.",
    "Any apparent improvement may come from prior choice or conservatism rather than TRL-style transitive propagation.",
    "The current evidence is based on selected tabular regimes, so broader claims remain unsupported.",
    "Risk-optimal no-success remains unsolved from counts alone, so impossible or prior-dependent regimes must be labeled rather than treated as ordinary failures.",
    "Large neural, continuous-control, OGBench, PointMaze, or AntMaze experiments remain premature."
  ]
}
```

## 0011_decision.json

```json
{
  "confidence": 0.78,
  "decision": "continue",
  "evidence": {
    "_type": "list",
    "first_items": [
      "0010 result and review report the required result, summary, and all listed artifacts, with artifact validation ok.",
      "0010 review reports allows_auto_continue=true, success_criteria_satisfied=true, failure_criteria_triggered=false, should_escalate_to_pro=false, and verdict=pass.",
      "0010 implemented a real deterministic chain guard with raw TRL and TRL-log backup execution, and it passed with raw_trl_max_abs_error=0.0 and trl_log_max_abs_error=0.0."
    ],
    "length": 10
  },
  "next_experiment": {
    "estimated_runtime_minutes": 25,
    "experiment_id": "0011",
    "hypothesis": "Across tiny randomized branch-chain, stochastic stitching, and stochastic teleporter-style tabular MDPs with exact DP ground truth and finite offline coverage, posterior_trl_log will usually remain equivalent or near-equivalent to prior-matched posterior model DP. A credible positive result requires a predeclared regime where posterior_trl_log improves value or policy metrics over both TRL-log and prior-matched posterior model DP without relying on model-DP misspecification or conservative risk avoidance.",
    "objective": "Run a small randomized tabular equivalence and generalization audit to test whether posterior TRL-log has any distinct benefit over prior-matched posterior model DP beyond the handcrafted 0010 branch-chain regimes.",
    "required_outputs": {
      "_type": "list",
      "first_items": [
        "research/sto_trl/artifacts/0011/randomized_equivalence_audit.py",
        "research/sto_trl/artifacts/0011/raw_metrics.json",
        "research/sto_trl/artifacts/0011/metrics.csv"
      ],
      "length": 11
    }
  },
  "progress_score": 7,
  "rationale": "Experiment 0010 is a valid negative result for a distinct posterior transitive effect: posterior TRL-log matched the prior-matched posterior model-DP baseline exactly. That weakens the reframed algorithmic idea, but there is one cheap decisive next test before stopping or asking for a risky pivot: audit whether this equivalence holds across a small randomized tabular suite including branch-chain, stitching, and teleporter-style graphs. The next experiment should be framed as an equivalence and generalization audit, not as another algorithm tweak or a broad benchmark step.",
  "risks": [
    "A new algorithm variant would be low-value now; the next test should audit equivalence/generalization rather than tune another method.",
    "Do not create an artificial TRL win by deliberately misspecifying or withholding a fair transition-model DP baseline.",
    "A randomized suite can become broad exploration; keep it tiny, predeclared, and under 30 minutes.",
    "Posterior methods may appear better only by prior choice or conservatism, so matched risk-optimal and risk-avoidance diagnostics must remain hard checks.",
    "If posterior TRL remains equivalent to posterior model DP across the randomized suite, the supervisor should be prepared to stop or require human direction before any further stochastic TRL algorithm work.",
    "Do not move to neural networks, continuous control, PointMaze, AntMaze, OGBench, downloads, or expensive training."
  ]
}
```


## Full evidence paths

- `research/sto_trl/results/0011_result.json`
- `research/sto_trl/results/0011_summary.md`
- `research/sto_trl/reviews/0011_review.json`

Use these paths if compact summaries are insufficient.


## Stop, pivot, continue rules

- For iteration 0, a missing latest result is expected and is not by itself a reason to stop.
- After iteration 0, stop or choose needs_human on missing or invalid result files.
- Stop on repeated invalid, negative, or low-value results.
- Pivot only when evidence weakens the original idea but reveals a nearby testable idea.
- Continue or pivot only for one cheap, high-information experiment.
- Choose needs_human for ambiguity, expensive work, missing artifacts, or risky pivots.


## Next experiment id

Use `0012` as the exact `next_experiment.experiment_id` if you choose continue or pivot.
