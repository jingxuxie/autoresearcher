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
  "failure_streak": 0,
  "human_review_required": false,
  "iteration": 5,
  "last_decision": "pivot",
  "last_failure": null,
  "last_pro_review_iteration": 0,
  "no_progress_rounds": 0,
  "notes": [
    "2026-06-13T08:58:38+00:00: supervisor decision pivot"
  ],
  "primary_metric": null,
  "status": "active"
}
```


## Latest result summary

```json
{
  "_source": "/home/eston/autoresearcher/research/sto_trl/results/0005_result.json",
  "artifacts": {
    "_type": "list",
    "first_items": [
      "research/sto_trl/artifacts/0005/run_lambda_equivalence_audit.py",
      "research/sto_trl/artifacts/0005/raw_metrics.json",
      "research/sto_trl/artifacts/0005/metrics.csv"
    ],
    "length": 11
  },
  "baseline_metrics": {
    "main_mean_heldout_long_horizon_value_mse": 0.21524060774329223,
    "main_rows": {
      "_type": "list",
      "first_items": [
        {
          "_type": "object",
          "key_count": 26,
          "keys": [
            "chose_exact_optimal_action",
            "eval_greedy_action",
            "exact_optimal_action",
            "exact_risky_q",
            "exact_safe_q",
            "heldout_long_horizon_value_mse",
            "lambda_tr",
            "learned_risky_q",
            "learned_safe_q",
            "mdp",
            "method",
            "policy_regret",
            "q_calibration_error",
            "q_overestimation_error",
            "q_underestimation_error",
            "risky_action_selection_rate",
            "risky_failure_count",
            "risky_success_count",
            "risky_success_rate_observed",
            "scenario_id"
          ]
        },
        {
          "_type": "object",
          "key_count": 26,
          "keys": [
            "chose_exact_optimal_action",
            "eval_greedy_action",
            "exact_optimal_action",
            "exact_risky_q",
            "exact_safe_q",
            "heldout_long_horizon_value_mse",
            "lambda_tr",
            "learned_risky_q",
            "learned_safe_q",
            "mdp",
            "method",
            "policy_regret",
            "q_calibration_error",
            "q_overestimation_error",
            "q_underestimation_error",
            "risky_action_selection_rate",
            "risky_failure_count",
            "risky_success_count",
            "risky_success_rate_observed",
            "scenario_id"
          ]
        },
        {
          "_type": "object",
          "key_count": 26,
          "keys": [
            "chose_exact_optimal_action",
            "eval_greedy_action",
            "exact_optimal_action",
            "exact_risky_q",
            "exact_safe_q",
            "heldout_long_horizon_value_mse",
            "lambda_tr",
            "learned_risky_q",
            "learned_safe_q",
            "mdp",
            "method",
            "policy_regret",
            "q_calibration_error",
            "q_overestimation_error",
            "q_underestimation_error",
            "risky_action_selection_rate",
            "risky_failure_count",
            "risky_success_count",
            "risky_success_rate_observed",
            "scenario_id"
          ]
        }
      ],
      "length": 3
    },
    "method": "successor_calibration_only"
  },
  "claim_tested": "A successor-distance lambda sweep can reveal whether successor_distance_trl_log has a distinct effect beyond trl_log while retaining calibration and lower held-out error than calibration-only.",
  "experiment_id": "0005",
  "interpretation": "The audit found negative successor-distance evidence: improving lambdas reduced held-out error by matching trl_log within the predeclared tolerance, so this variant is not yet distinct from trl_log on these tabular diagnostics.",
  "known_failures": [],
  "metrics": {
    "aggregate": {
      "all_improving_lambdas_equivalent_to_trl_log": true,
      "any_positive_successor_evidence": false,
      "lambda_summaries": {
        "_type": "object",
        "key_count": 5,
        "keys": [
          "successor_distance_trl_log_lambda_0_00",
          "successor_distance_trl_log_lambda_0_25",
          "successor_distance_trl_log_lambda_0_50",
          "successor_distance_trl_log_lambda_0_75",
          "successor_distance_trl_log_lambda_1_00"
        ]
      },
      "negative_equivalence_evidence": true,
      "successor_calibration_only_main_mean_heldout_mse": 0.21524060774329223
    },
    "equivalence_tolerance": 1e-10,
    "experiment_id": "0005",
    "gamma": 0.9,
    "label_horizon_cutoff": 2,
    "lambda_sweep": [
      0.0,
      0.25,
      0.5,
      0.75,
      1.0
    ],
    "scenarios": {
      "chain_len9_holdout": {
        "_type": "object",
        "key_count": 7,
        "keys": [
          "coverage_diagnostics",
          "equivalence_diagnostics",
          "label_or_pair_coverage",
          "mdp",
          "methods",
          "scenario_role",
          "successor_meta"
        ]
      },
      "risk_optimal_matched": {
        "_type": "object",
        "key_count": 7,
        "keys": [
          "coverage_diagnostics",
          "equivalence_diagnostics",
          "label_or_pair_coverage",
          "mdp",
          "methods",
          "scenario_role",
          "successor_meta"
        ]
      },
      "safe_optimal_lucky_only_stress": {
        "_type": "object",
        "key_count": 7,
        "keys": [
          "coverage_diagnostics",
          "equivalence_diagnostics",
          "label_or_pair_coverage",
          "mdp",
          "methods",
          "scenario_role",
          "successor_meta"
        ]
      },
      "safe_optimal_matched": {
        "_type": "object",
        "key_count": 7,
        "keys": [
          "coverage_diagnostics",
          "equivalence_diagnostics",
          "label_or_pair_coverage",
          "mdp",
          "methods",
          "scenario_role",
          "successor_meta"
        ]
      }
    },
    "success_checks": {
      "audit_completed": true,
      "chain_raw_exact": true,
      "chain_trl_log_exact": true,
      "lambda_sweep_completed": true,
      "negative_equivalence_evidence": true,
      "positive_successor_evidence": false
    },
    "update_steps": 32
  },
  "next_questions": [
    "What update or regularizer would make successor-distance relaxation differ from pure empirical trl_log in deterministic tabular cases?",
    "Should future variants add uncertainty penalties so biased lucky-only support does not collapse to raw support optimism?",
    "Can a non-tabular setting expose distance-space interpolation differences that are absent in this exact tabular audit?"
  ],
  "status": "completed"
}
```


## Latest summary

# Experiment 0005 Summary

## Objective

Audit whether successor-distance + TRL-log has a distinct tabular effect beyond calibration-only and trl_log.

## Commands Run

```bash
mkdir -p research/sto_trl/artifacts/0005 research/sto_trl/results && cp research/sto_trl/artifacts/0004/run_successor_distance.py research/sto_trl/artifacts/0005/run_lambda_equivalence_audit.py
conda run -n autoresearcher_sto_trl python research/sto_trl/artifacts/0005/run_lambda_equivalence_audit.py
conda run -n autoresearcher_sto_trl python scripts/validate_artifacts.py --repo-root . --json research/sto_trl/results/0005_result.json --schema schemas/result.schema.json --check-result-artifacts
```

## Setup

- Discount: `0.9`
- Label horizon cutoff: `2`
- Fixed backup iterations: `32`
- Lambda sweep: `[0.0, 0.25, 0.5, 0.75, 1.0]`
- Equivalence tolerance: `1e-10`
- Main scenarios: chain holdout, matched safe-optimal risky shortcut, matched risk-optimal risky shortcut.
- Stress scenario: safe-optimal lucky-only risky shortcut.

## Main Metrics

| Scenario | Method | Lambda | Held-out MSE | Q calibration | Policy regret | Action | Triangle violation |
| --- | --- | ---: | ---: | ---: | ---: | --- | ---: |
| chain_len9_holdout | mc_supervised | None | 0.391705823230 | 0.465607869047 | 0.000000000000 | right | 0.166667 |
| chain_len9_holdout | trl_raw | None | 0.000000000000 | 0.000000000000 | 0.000000000000 | right | 0.000000 |
| chain_len9_holdout | trl_log | None | 0.000000000000 | 0.000000000000 | 0.000000000000 | right | 0.000000 |
| chain_len9_holdout | mc_plus_trl_log | None | 0.000000000000 | 0.131258278195 | 0.000000000000 | right | 0.000000 |
| chain_len9_holdout | successor_calibration_only | 0.0 | 0.391705823230 | 0.465607869047 | 0.000000000000 | right | 0.166667 |
| chain_len9_holdout | successor_distance_trl_log_lambda_0_00 | 0.0 | 0.391705823230 | 0.465607869047 | 0.000000000000 | right | 0.166667 |
| chain_len9_holdout | successor_distance_trl_log_lambda_0_25 | 0.25 | 0.000000000000 | 0.000000000000 | 0.000000000000 | right | 0.000000 |
| chain_len9_holdout | successor_distance_trl_log_lambda_0_50 | 0.5 | 0.000000000000 | 0.000000000000 | 0.000000000000 | right | 0.000000 |
| chain_len9_holdout | successor_distance_trl_log_lambda_0_75 | 0.75 | 0.000000000000 | 0.000000000000 | 0.000000000000 | right | 0.000000 |
| chain_len9_holdout | successor_distance_trl_log_lambda_1_00 | 1.0 | 0.000000000000 | 0.000000000000 | 0.000000000000 | right | 0.000000 |
| safe_optimal_matched | mc_supervised | None | 0.254016000000 | 0.045562500000 | 0.504000000000 | risky | 0.375000 |
| safe_optimal_matched | trl_raw | None | 0.029241000000 | 0.056250000000 | 0.504000000000 | risky | 0.000000 |
| safe_optimal_matched | trl_log | None | 0.000000000000 | 0.000000000000 | 0.000000000000 | safe | 0.250000 |
| safe_optimal_matched | mc_plus_trl_log | None | 0.000000000000 | 0.000000000000 | 0.000000000000 | safe | 0.250000 |
| safe_optimal_matched | successor_calibration_only | 0.0 | 0.254016000000 | 0.045562500000 | 0.504000000000 | risky | 0.375000 |
| safe_optimal_matched | successor_distance_trl_log_lambda_0_00 | 0.0 | 0.254016000000 | 0.045562500000 | 0.504000000000 | risky | 0.375000 |
| safe_optimal_matched | successor_distance_trl_log_lambda_0_25 | 0.25 | 0.000000000000 | 0.000000000000 | 0.000000000000 | safe | 0.250000 |
| safe_optimal_matched | successor_distance_trl_log_lambda_0_50 | 0.5 | 0.000000000000 | 0.000000000000 | 0.000000000000 | safe | 0.250000 |
| safe_optimal_matched | successor_distance_trl_log_lambda_0_75 | 0.75 | 0.000000000000 | 0.000000000000 | 0.000000000000 | safe | 0.250000 |
| safe_optimal_matched | successor_distance_trl_log_lambda_1_00 | 1.0 | 0.000000000000 | 0.000000000000 | 0.000000000000 | safe | 0.250000 |
| risk_optimal_matched | mc_supervised | None | 0.000000000000 | 0.045562500000 | 0.000000000000 | risky | 0.250000 |
| risk_optimal_matched | trl_raw | None | 0.000000000000 | 0.056250000000 | 0.000000000000 | risky | 0.000000 |
| risk_optimal_matched | trl_log | None | 0.000000000000 | 0.000000000000 | 0.000000000000 | risky | 0.250000 |
| risk_optimal_matched | mc_plus_trl_log | None | 0.000000000000 | 0.000000000000 | 0.000000000000 | risky | 0.250000 |
| risk_optimal_matched | successor_calibration_only | 0.0 | 0.000000000000 | 0.045562500000 | 0.000000000000 | risky | 0.250000 |
| risk_optimal_matched | successor_distance_trl_log_lambda_0_00 | 0.0 | 0.000000000000 | 0.045562500000 | 0.000000000000 | risky | 0.250000 |
| risk_optimal_matched | successor_distance_trl_log_lambda_0_25 | 0.25 | 0.000000000000 | 0.000000000000 | 0.000000000000 | risky | 0.250000 |
| risk_optimal_matched | successor_distance_trl_log_lambda_0_50 | 0.5 | 0.000000000000 | 0.000000000000 | 0.000000000000 | risky | 0.250000 |
| risk_optimal_matched | successor_distance_trl_log_lambda_0_75 | 0.75 | 0.000000000000 | 0.000000000000 | 0.000000000000 | risky | 0.250000 |
| risk_optimal_matched | successor_distance_trl_log_lambda_1_00 | 1.0 | 0.000000000000 | 0.000000000000 | 0.000000000000 | risky | 0.250000 |
| safe_optimal_lucky_only_stress | mc_supervised | None | 0.029241000000 | 0.129937500000 | 0.504000000000 | risky | 0.000000 |
| safe_optimal_lucky_only_stress | trl_raw | None | 0.029241000000 | 0.084375000000 | 0.504000000000 | risky | 0.000000 |
| safe_optimal_lucky_only_stress | trl_log | None | 0.029241000000 | 0.084375000000 | 0.504000000000 | risky | 0.000000 |
| safe_optimal_lucky_only_stress | mc_plus_trl_log | None | 0.029241000000 | 0.084375000000 | 0.504000000000 | risky | 0.000000 |
| safe_optimal_lucky_only_stress | successor_calibration_only | 0.0 | 0.029241000000 | 0.129937500000 | 0.504000000000 | risky | 0.000000 |
| safe_optimal_lucky_only_stress | successor_distance_trl_log_lambda_0_00 | 0.0 | 0.029241000000 | 0.129937500000 | 0.504000000000 | risky | 0.000000 |
| safe_optimal_lucky_only_stress | successor_distance_trl_log_lambda_0_25 | 0.25 | 0.029241000000 | 0.084375000000 | 0.5040000

_Trimmed to 6000 chars; inspect the source file for full text._


## Latest review summary

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


## Last decision summaries

## 0003_decision.json

```json
{
  "confidence": 0.84,
  "decision": "continue",
  "evidence": [
    "research/sto_trl/results/0002_result.json validates against schemas/result.schema.json with artifact checks.",
    "0002 success checks report deterministic chain raw/log recovery, all predeclared risky regimes present, raw_policy_is_support_driven=true, and trl_log_is_optimal_on_matched_regimes=true.",
    "0002 aggregate metrics show raw TRL selected risky in 8/8 scenarios with observed risky success and 0/2 scenarios with no observed success, confirming the support-driven failure mode.",
    "0002 shows empirical MC/log methods are only calibrated in matched regimes: they choose risky incorrectly in safe_optimal__lucky_only and choose safe incorrectly in risk_optimal__unlucky_biased and risk_optimal__no_risky_success.",
    "The charter still requires evidence that log or MC+TRL-log improves long-horizon estimates over MC-only without breaking deterministic sanity checks before moving beyond tabular diagnostics."
  ],
  "next_experiment": {
    "estimated_runtime_minutes": 20,
    "experiment_id": "0003",
    "hypothesis": "With only short-horizon MC labels, MC-supervised estimates will underpredict held-out long-horizon goals, while log-space transitive backups, especially MC+TRL-log, will propagate calibrated short-horizon information to longer horizons without raw TRL's stochastic risky-path optimism under matched branch coverage.",
    "objective": "Run a small tabular horizon-holdout experiment that censors long-horizon goal labels during training and tests whether TRL-log or MC+TRL-log can recover long-horizon discounted reachability better than MC-only while retaining matched stochastic risky-branch calibration.",
    "required_outputs": [
      "research/sto_trl/artifacts/0003/run_horizon_holdout.py",
      "research/sto_trl/artifacts/0003/raw_metrics.json",
      "research/sto_trl/artifacts/0003/metrics.csv",
      "research/sto_trl/artifacts/0003/label_coverage_by_horizon.json",
      "research/sto_trl/artifacts/0003/offline_datasets.json",
      "research/sto_trl/results/0003_result.json",
      "research/sto_trl/results/0003_summary.md"
    ]
  },
  "progress_score": 5,
  "rationale": "Experiment 0002 is valid and informative: it confirms raw TRL's support-driven stochastic overestimation, and it also weakens the simpler empirical MC/log story by showing those methods depend heavily on branch coverage and can be overoptimistic or too conservative. The next cheap decisive test should isolate the other core claim: whether TRL-style log transitive backups actually improve long-horizon generalization over MC calibration when long-horizon labels are withheld, while preserving the stochastic branch behavior under matched coverage.",
  "risks": [
    "Do not treat 0002 as proving stochastic calibration; it shows empirical log/MC calibration is coverage-dependent.",
    "A horizon-holdout test can leak labels if the script computes MC targets from all future states; it must explicitly censor long-horizon training labels and save train/eval pair coverage.",
    "If the next experiment only repeats matched risky coverage without long-horizon label withholding, it will not test the remaining TRL horizon-generalization claim.",
    "Exact DP must remain evaluation-only ground truth, not a training target."
  ]
}
```

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


## Full evidence paths

- `research/sto_trl/results/0005_result.json`
- `research/sto_trl/results/0005_summary.md`
- `research/sto_trl/reviews/0005_review.json`

Use these paths if compact summaries are insufficient.


## Stop, pivot, continue rules

- For iteration 0, a missing latest result is expected and is not by itself a reason to stop.
- After iteration 0, stop or choose needs_human on missing or invalid result files.
- Stop on repeated invalid, negative, or low-value results.
- Pivot only when evidence weakens the original idea but reveals a nearby testable idea.
- Continue or pivot only for one cheap, high-information experiment.
- Choose needs_human for ambiguity, expensive work, missing artifacts, or risky pivots.


## Next experiment id

Use `0006` as the exact `next_experiment.experiment_id` if you choose continue or pivot.
