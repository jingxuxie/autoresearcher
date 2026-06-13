# Supervisor Context: sto_trl

## Requested action

Choose continue, pivot, stop, or needs_human. If this is iteration 0 with no prior result, propose the first small experiment when the charter is specific enough. If continuing, propose exactly one small experiment.


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
  "failure_streak": 1,
  "human_review_required": false,
  "iteration": 6,
  "last_decision": "retryable_failure",
  "last_failure": {
    "at": "2026-06-13T09:21:15+00:00",
    "attempt": 1,
    "max_attempts": 3,
    "note": "reviewer failed or timed out; see /home/eston/autoresearcher/research/sto_trl/reviews/0007_review_stderr.log"
  },
  "last_pro_review_iteration": 0,
  "no_progress_rounds": 0,
  "notes": [
    "2026-06-13T08:58:38+00:00: supervisor decision pivot",
    "2026-06-13T09:21:15+00:00: retryable failure 1/3: reviewer failed or timed out; see /home/eston/autoresearcher/research/sto_trl/reviews/0007_review_stderr.log"
  ],
  "primary_metric": null,
  "status": "active"
}
```


## Latest result summary

```json
{
  "_source": "/home/eston/autoresearcher/research/sto_trl/results/0006_result.json",
  "artifacts": [
    "research/sto_trl/artifacts/0006/run_uncertainty_conservative_log_trl.py",
    "research/sto_trl/artifacts/0006/raw_metrics.json",
    "research/sto_trl/artifacts/0006/metrics.csv",
    "research/sto_trl/artifacts/0006/penalty_sweep.json",
    "research/sto_trl/artifacts/0006/uncertainty_diagnostics.json",
    "research/sto_trl/artifacts/0006/offline_datasets.json",
    "research/sto_trl/artifacts/0006/transition_tables.json",
    "research/sto_trl/artifacts/0006/value_tables.json"
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
  "claim_tested": "A one-sided count-based conservative log-TRL backup can reduce lucky-only risky overestimation without breaking deterministic recovery or matched risk-optimal action selection.",
  "experiment_id": "0006",
  "interpretation": "one_sided_conservative_log_trl_alpha_0_20 reduced the lucky-only safe-optimal failure versus trl_log while preserving the chain and selecting risky with zero regret in the matched risk-optimal scenario.",
  "known_failures": [],
  "metrics": {
    "aggregate": {
      "alpha_summaries": {
        "_type": "object",
        "key_count": 4,
        "keys": [
          "one_sided_conservative_log_trl_alpha_0_00",
          "one_sided_conservative_log_trl_alpha_0_20",
          "one_sided_conservative_log_trl_alpha_0_40",
          "one_sided_conservative_log_trl_alpha_0_60"
        ]
      },
      "best_positive_method": "one_sided_conservative_log_trl_alpha_0_20",
      "positive_uncertainty_evidence": true,
      "trl_log_safe_lucky_policy_regret": 0.5040000000000001,
      "trl_log_safe_lucky_q_overestimation": 0.675
    },
    "alpha_grid": [
      0.0,
      0.2,
      0.4,
      0.6
    ],
    "experiment_id": "0006",
    "gamma": 0.9,
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
      "alpha_grid_completed": true,
      "chain_raw_exact": true,
      "chain_trl_log_exact": true,
      "experiment_completed": true,
      "positive_uncertainty_evidence": true
    },
    "successor_baseline_lambda": 0.25,
    "update_steps": 32
  },
  "next_questions": [
    "Can the direct-goal shortcut penalty be generalized without hand-tuning the decision-state eligibility rule?",
    "How should uncertainty penalties trade off lucky-only safety against no-success risk-optimal conservatism?",
    "Would bootstrap or Bayesian branch uncertainty provide smoother behavior than the fixed count penalty grid?"
  ],
  "status": "completed"
}
```


## Latest summary

# Experiment 0006 Summary

## Objective

Test a one-sided conservative log-TRL backup on biased stochastic coverage while preserving matched and deterministic behavior.

## Commands Run

```bash
mkdir -p research/sto_trl/artifacts/0006 research/sto_trl/results && cp research/sto_trl/artifacts/0005/run_lambda_equivalence_audit.py research/sto_trl/artifacts/0006/run_uncertainty_conservative_log_trl.py
conda run -n autoresearcher_sto_trl python research/sto_trl/artifacts/0006/run_uncertainty_conservative_log_trl.py
conda run -n autoresearcher_sto_trl python scripts/validate_artifacts.py --repo-root . --json research/sto_trl/results/0006_result.json --schema schemas/result.schema.json --check-result-artifacts
```

## Setup

- Discount: `0.9`
- Label horizon cutoff: `2`
- Fixed backup iterations: `32`
- Alpha grid: `[0.0, 0.2, 0.4, 0.6]`
- Conservative penalty: `alpha * gamma / sqrt(count)` for direct-goal single-branch shortcut actions at multi-action states with count at least 4.

## Metrics

| Scenario | Method | Alpha | Held-out MSE | Q calibration | Policy regret | Action | Risky selected |
| --- | --- | ---: | ---: | ---: | ---: | --- | ---: |
| chain_len9_holdout | mc_supervised | None | 0.391705823230 | 0.465607869047 | 0.000000000000 | right | 0.0 |
| chain_len9_holdout | trl_raw | None | 0.000000000000 | 0.000000000000 | 0.000000000000 | right | 0.0 |
| chain_len9_holdout | trl_log | None | 0.000000000000 | 0.000000000000 | 0.000000000000 | right | 0.0 |
| chain_len9_holdout | mc_plus_trl_log | None | 0.000000000000 | 0.131258278195 | 0.000000000000 | right | 0.0 |
| chain_len9_holdout | successor_distance_best_0005 | None | 0.000000000000 | 0.000000000000 | 0.000000000000 | right | 0.0 |
| chain_len9_holdout | one_sided_conservative_log_trl_alpha_0_00 | 0.0 | 0.000000000000 | 0.000000000000 | 0.000000000000 | right | 0.0 |
| chain_len9_holdout | one_sided_conservative_log_trl_alpha_0_20 | 0.2 | 0.000000000000 | 0.000000000000 | 0.000000000000 | right | 0.0 |
| chain_len9_holdout | one_sided_conservative_log_trl_alpha_0_40 | 0.4 | 0.000000000000 | 0.000000000000 | 0.000000000000 | right | 0.0 |
| chain_len9_holdout | one_sided_conservative_log_trl_alpha_0_60 | 0.6 | 0.000000000000 | 0.000000000000 | 0.000000000000 | right | 0.0 |
| safe_optimal_matched | mc_supervised | None | 0.254016000000 | 0.045562500000 | 0.504000000000 | risky | 1.0 |
| safe_optimal_matched | trl_raw | None | 0.029241000000 | 0.056250000000 | 0.504000000000 | risky | 1.0 |
| safe_optimal_matched | trl_log | None | 0.000000000000 | 0.000000000000 | 0.000000000000 | safe | 0.0 |
| safe_optimal_matched | mc_plus_trl_log | None | 0.000000000000 | 0.000000000000 | 0.000000000000 | safe | 0.0 |
| safe_optimal_matched | successor_distance_best_0005 | None | 0.000000000000 | 0.000000000000 | 0.000000000000 | safe | 0.0 |
| safe_optimal_matched | one_sided_conservative_log_trl_alpha_0_00 | 0.0 | 0.000000000000 | 0.000000000000 | 0.000000000000 | safe | 0.0 |
| safe_optimal_matched | one_sided_conservative_log_trl_alpha_0_20 | 0.2 | 0.000000000000 | 0.005625000000 | 0.000000000000 | safe | 0.0 |
| safe_optimal_matched | one_sided_conservative_log_trl_alpha_0_40 | 0.4 | 0.000000000000 | 0.011250000000 | 0.000000000000 | safe | 0.0 |
| safe_optimal_matched | one_sided_conservative_log_trl_alpha_0_60 | 0.6 | 0.000000000000 | 0.016875000000 | 0.000000000000 | safe | 0.0 |
| risk_optimal_matched | mc_supervised | None | 0.000000000000 | 0.045562500000 | 0.000000000000 | risky | 1.0 |
| risk_optimal_matched | trl_raw | None | 0.000000000000 | 0.056250000000 | 0.000000000000 | risky | 1.0 |
| risk_optimal_matched | trl_log | None | 0.000000000000 | 0.000000000000 | 0.000000000000 | risky | 1.0 |
| risk_optimal_matched | mc_plus_trl_log | None | 0.000000000000 | 0.000000000000 | 0.000000000000 | risky | 1.0 |
| risk_optimal_matched | successor_distance_best_0005 | None | 0.000000000000 | 0.000000000000 | 0.000000000000 | risky | 1.0 |
| risk_optimal_matched | one_sided_conservative_log_trl_alpha_0_00 | 0.0 | 0.000000000000 | 0.000000000000 | 0.000000000000 | risky | 1.0 |
| risk_optimal_matched | one_sided_conservative_log_trl_alpha_0_20 | 0.2 | 0.000000000000 | 0.005625000000 | 0.000000000000 | risky | 1.0 |
| risk_optimal_matched | one_sided_conservative_log_trl_alpha_0_40 | 0.4 | 0.000000000000 | 0.011250000000 | 0.000000000000 | risky | 1.0 |
| risk_optimal_matched | one_sided_conservative_log_trl_alpha_0_60 | 0.6 | 0.000000000000 | 0.016875000000 | 0.000000000000 | risky | 1.0 |
| safe_optimal_lucky_only_stress | mc_supervised | None | 0.029241000000 | 0.129937500000 | 0.504000000000 | risky | 1.0 |
| safe_optimal_lucky_only_stress | trl_raw | None | 0.029241000000 | 0.084375000000 | 0.504000000000 | risky | 1.0 |
| safe_optimal_lucky_only_stress | trl_log | None | 0.029241000000 | 0.084375000000 | 0.504000000000 | risky | 1.0 |
| safe_optimal_lucky_only_stress | mc_plus_trl_log | None | 0.029241000000 | 0.084375000000 | 0.504000000000 | risky | 1.0 |
| safe_optimal_lucky_only_stress | successor_distance_best_0005 | None | 0.029241000000 | 0.084375000000 | 0.504000000000 | risky | 1.0 |
| safe_optimal_lucky_only_stress | one_sided_conservative_log_trl_alpha_0_00 | 0.0 | 0.029241000000 | 0.084375000000 | 0.504000000000 | risky | 1.0 |
| safe_optimal_lucky_only_stress | one_sided_conservative_log_trl_alpha_0_20 | 0.2 | 0.006561000000 | 0.084375000000 | 0.504000000000 | risky | 1.0 |
| safe_optimal_lucky_only_stress | one_sided_conservative_log_trl_alpha_0_40 | 0.4 | 0.000000000000 | 0.084375000000 | 0.000000000000 | safe | 0.0 |
| safe_optimal_lucky_only_stress | one_sided_conservative_log_trl_alpha_0_60 | 0.6 | 0.000000000000 | 0.084375000000 | 0.000000000000 | safe | 0.0 |
| risk_optimal_no_success_stress | mc_supervised | None | 0.000000000000 | 0.146812500000 | 0.000000000000 | risky | 1.0 |
| risk_optimal_no_success_stress | trl_raw | None | 0.000000000000 | 0.101250000000 | 0.081000000000 | safe | 0.0 |
| risk_optimal_

_Trimmed to 6000 chars; inspect the source file for full text._


## Latest review summary

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


## Last decision summaries

## 0004_decision.json

```json
{
  "confidence": 0.82,
  "decision": "continue",
  "evidence": [
    "research/sto_trl/results/0003_result.json validates against schemas/result.schema.json with artifact checks.",
    "0003 status is completed with no known_failures and success_criteria_met=true.",
    "0003 aggregate metrics show chain held-out value MSE improved from MC 0.3917058232298766 to TRL-log and MC+TRL-log 2.9347503914472164e-34.",
    "0003 risky matched metrics show MC selected risky with policy_regret=0.504, raw TRL selected risky with policy_regret=0.504, while TRL-log and MC+TRL-log selected safe with zero policy regret.",
    "The 0003 review allows auto-continue but flags that TRL-log/raw are tabular transitive backups over observed transitions rather than the same supervised label budget as MC-only, so a calibration-only versus calibrated+transitive ablation is the right next test.",
    "The prototype plan's Milestone 3 calls for a first stochastic-calibrated variant: contrastive successor-distance or self-normalized successor score, Successor-distance + TRL-log, and comparison against calibration-only."
  ],
  "next_experiment": {
    "estimated_runtime_minutes": 25,
    "experiment_id": "0004",
    "hypothesis": "A self-normalized successor-distance calibration with a log-space transitive relaxation will improve held-out long-horizon value estimates over calibration-only while preserving matched stochastic branch calibration, reducing raw TRL overestimation, and not simply avoiding risky actions when risk is truly optimal.",
    "objective": "Implement and test the first tabular stochastic-calibrated successor-distance variant, comparing calibration-only against successor-distance + TRL-log on the existing horizon-holdout and risky-shortcut diagnostics.",
    "required_outputs": [
      "research/sto_trl/artifacts/0004/run_successor_distance_ablation.py",
      "research/sto_trl/artifacts/0004/raw_metrics.json",
      "research/sto_trl/artifacts/0004/metrics.csv",
      "research/sto_trl/artifacts/0004/successor_distance_tables.json",
      "research/sto_trl/artifacts/0004/distance_diagnostics.json",
      "research/sto_trl/artifacts/0004/label_or_pair_coverage.json",
      "research/sto_trl/results/0004_result.json",
      "research/sto_trl/results/0004_summary.md"
    ]
  },
  "progress_score": 6,
  "rationale": "Experiment 0003 is a valid weak-pass result with useful evidence: log transitive backups recovered censored long-horizon tabular reachability and avoided raw TRL's matched risky-shortcut optimism. The remaining charter-critical question is whether a first stochastic-calibrated successor-distance style variant adds anything beyond empirical log backups and calibration-only baselines, without becoming conservative on risk-optimal cases. That is a small tabular Milestone 3 experiment, still within the initial scope.",
  "risks": [
    "A self-normalized successor variant may collapse to the same empirical log backup already tested; require saved value tables and method definitions that distinguish calibration-only from calibrated+transitive.",
    "No tabular method can infer missing stochastic outcomes without assumptions, so lucky-only or no-success regimes should be reported as boundary cases rather than hidden or overclaimed.",
    "A conservative variant can look good on safe-optimal shortcuts while failing risk-optimal shortcuts; include an anti-conservatism check.",
    "Keep this tabular and small; do not move to OGBench, neural networks, downloads, or broad sweeps yet."
  ]
}
```

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


## Full evidence paths

- `research/sto_trl/results/0006_result.json`
- `research/sto_trl/results/0006_summary.md`
- `research/sto_trl/reviews/0006_review.json`

Use these paths if compact summaries are insufficient.


## Stop, pivot, continue rules

- For iteration 0, a missing latest result is expected and is not by itself a reason to stop.
- After iteration 0, stop or choose needs_human on missing or invalid result files.
- Stop on repeated invalid, negative, or low-value results.
- Pivot only when evidence weakens the original idea but reveals a nearby testable idea.
- Continue or pivot only for one cheap, high-information experiment.
- Choose needs_human for ambiguity, expensive work, missing artifacts, or risky pivots.


## Next experiment id

Use `0007` as the exact `next_experiment.experiment_id` if you choose continue or pivot.
