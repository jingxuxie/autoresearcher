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
  "iteration": 2,
  "last_decision": "continue",
  "last_failure": null,
  "last_pro_review_iteration": 0,
  "no_progress_rounds": 0,
  "notes": [],
  "primary_metric": null,
  "status": "active"
}
```


## Latest result JSON

```json
{
  "artifacts": [
    "research/sto_trl/artifacts/0002/run_coverage_stress.py",
    "research/sto_trl/artifacts/0002/raw_metrics.json",
    "research/sto_trl/artifacts/0002/metrics.csv",
    "research/sto_trl/artifacts/0002/coverage_diagnostics.json",
    "research/sto_trl/artifacts/0002/dataset_specs.json",
    "research/sto_trl/artifacts/0002/offline_datasets.json",
    "research/sto_trl/artifacts/0002/transition_tables.json",
    "research/sto_trl/artifacts/0002/value_tables.json"
  ],
  "baseline_metrics": {
    "mean_policy_regret_on_risky_scenarios": 0.0666,
    "method": "mc_supervised",
    "num_rows": 11,
    "optimal_action_rate_on_risky_scenarios": 0.7,
    "rows": [
      {
        "chose_exact_optimal_action": true,
        "eval_greedy_action": "right",
        "eval_start_exact_value": 0.5904900000000002,
        "eval_start_learned_value": 0.5904900000000001,
        "exact_optimal_action": "right",
        "exact_risky_q": null,
        "exact_safe_q": null,
        "learned_risky_q": null,
        "learned_safe_q": null,
        "long_horizon_value_mse": 3.697785493223493e-33,
        "max_policy_regret": 0.0,
        "mdp": "deterministic_chain",
        "mean_policy_regret": 0.0,
        "method": "mc_supervised",
        "observed_risky_failures": 0,
        "observed_risky_success_rate": null,
        "observed_risky_successes": 0,
        "policy_regret": 0.0,
        "q_calibration_error": 0.2638688400000001,
        "q_overestimation_error": 0.0,
        "q_underestimation_error": 0.7290000000000001,
        "regime": "chain_regression",
        "risky_action_selection_rate": 0.0,
        "scenario_id": "deterministic_chain__chain_regression",
        "true_risky_success_prob": null,
        "value_mse": 2.0543252740130515e-33,
        "value_overestimation_error": 0.0,
        "value_underestimation_error": 1.1102230246251565e-16
      },
      {
        "chose_exact_optimal_action": true,
        "eval_greedy_action": "safe",
        "eval_start_exact_value": 0.7290000000000001,
        "eval_start_learned_value": 0.7290000000000001,
        "exact_optimal_action": "safe",
        "exact_risky_q": 0.225,
        "exact_safe_q": 0.7290000000000001,
        "learned_risky_q": 0.225,
        "learned_safe_q": 0.7290000000000001,
        "long_horizon_value_mse": 0.0,
        "max_policy_regret": 0.0,
        "mdp": "risky_safe_optimal",
        "mean_policy_regret": 0.0,
        "method": "mc_supervised",
        "observed_risky_failures": 6,
        "observed_risky_success_rate": 0.25,
        "observed_risky_successes": 2,
        "policy_regret": 0.0,
        "q_calibration_error": 0.0,
        "q_overestimation_error": 0.0,
        "q_underestimation_error": 0.0,
        "regime": "matched",
        "risky_action_selection_rate": 0.0,
        "scenario_id": "safe_optimal__matched",
        "true_risky_success_prob": 0.25,
        "value_mse": 0.0,
        "value_overestimation_error": 0.0,
        "value_underestimation_error": 0.0
      },
      {
        "chose_exact_optimal_action": true,
        "eval_greedy_action": "safe",
        "eval_start_exact_value": 0.7290000000000001,
        "eval_start_learned_value": 0.7290000000000001,
        "exact_optimal_action": "safe",
        "exact_risky_q": 0.225,
        "exact_safe_q": 0.7290000000000001,
        "learned_risky_q": 0.675,
        "learned_safe_q": 0.7290000000000001,
        "long_horizon_value_mse": 0.05062500000000002,
        "max_policy_regret": 0.0,
        "mdp": "risky_safe_optimal",
        "mean_policy_regret": 0.0,
        "method": "mc_supervised",
        "observed_risky_failures": 2,
        "observed_risky_success_rate": 0.75,
        "observed_risky_successes": 6,
        "policy_regret": 0.0,
        "q_calibration_error": 0.05625000000000001,
        "q_overestimation_error": 0.45000000000000007,
        "q_underestimation_error": 0.45000000000000007,
        "regime": "lucky_biased",
        "risky_action_selection_rate": 0.0,
        "scenario_id": "safe_optimal__lucky_biased",
        "true_risky_success_prob": 0.25,
        "value_mse": 0.008100000000000003,
        "value_overestimation_error": 0.0,
        "value_underestimation_error": 0.45000000000000007
      },
      {
        "chose_exact_optimal_action": false,
        "eval_greedy_action": "risky",
        "eval_start_exact_value": 0.7290000000000001,
        "eval_start_learned_value": 0.9,
        "exact_optimal_action": "safe",
        "exact_risky_q": 0.225,
        "exact_safe_q": 0.7290000000000001,
        "learned_risky_q": 0.9,
        "learned_safe_q": 0.7290000000000001,
        "long_horizon_value_mse": 0.1212165,
        "max_policy_regret": 0.5040000000000001,
        "mdp": "risky_safe_optimal",
        "mean_policy_regret": 0.07200000000000002,
        "method": "mc_supervised",
        "observed_risky_failures": 0,
        "observed_risky_success_rate": 1.0,
        "observed_risky_successes": 4,
        "policy_regret": 0.5040000000000001,
        "q_calibration_error": 0.084375,
        "q_overestimation_error": 0.675,
        "q_underestimation_error": 0.675,
        "regime": "lucky_only",
        "risky_action_selection_rate": 1.0,
        "scenario_id": "safe_optimal__lucky_only",
        "true_risky_success_prob": 0.25,
        "value_mse": 0.01939464,
        "value_overestimation_error": 0.17099999999999993,
        "value_underestimation_error": 0.675
      },
      {
        "chose_exact_optimal_action": true,
        "eval_greedy_action": "safe",
        "eval_start_exact_value": 0.7290000000000001,
        "eval_start_learned_value": 0.7290000000000001,
        "exact_optimal_action": "safe",
        "exact_risky_q": 0.225,
        "exact_safe_q": 0.7290000000000001,
        "learned_risky_q": 0.1125,
        "learned_safe_q": 0.7290000000000001,
        "long_horizon_value_mse": 0.0031640625000000024,
        "max_policy_regret": 0.0,
        "mdp": "risky_safe_optimal",
        "mean_policy_regret": 0.0,
        "method": "mc_supervised",
        "observed_risky_failures": 7,
        "observed_risky_success_rate": 0.125,
        "observed_risky_successes": 1,
        "policy_regret": 0.0,
        "q_calibration_error": 0.014062500000000002,
        "q_overestimation_error": 0.11250000000000004,
        "q_underestimation_error": 0.1125,
        "regime": "unlucky_biased",
        "risky_action_selection_rate": 0.0,
        "scenario_id": "safe_optimal__unlucky_biased",
        "true_risky_success_prob": 0.25,
        "value_mse": 0.0005062500000000004,
        "value_overestimation_error": 0.11250000000000004,
        "value_underestimation_error": 0.0
      },
      {
        "chose_exact_optimal_action": true,
        "eval_greedy_action": "safe",
        "eval_start_exact_value": 0.7290000000000001,
        "eval_start_learned_value": 0.7290000000000001,
        "exact_optimal_action": "safe",
        "exact_risky_q": 0.225,
        "exact_safe_q": 0.7290000000000001,
        "learned_risky_q": 0.0,
        "learned_safe_q": 0.7290000000000001,
        "long_horizon_value_mse": 0.01265625000000001,
        "max_policy_regret": 0.0,
        "mdp": "risky_safe_optimal",
        "mean_policy_regret": 0.0,
        "method": "mc_supervised",
        "observed_risky_failures": 8,
        "observed_risky_success_rate": 0.0,
        "observed_risky_successes": 0,
        "policy_regret": 0.0,
        "q_calibration_error": 0.028125000000000004,
        "q_overestimation_error": 0.2250000000000001,
        "q_underestimation_error": 0.225,
        "regime": "no_risky_success",
        "risky_action_selection_rate": 0.0,
        "scenario_id": "safe_optimal__no_risky_success",
        "true_risky_success_prob": 0.25,
        "value_mse": 0.0020250000000000016,
        "value_overestimation_error": 0.2250000000000001,
        "value_underestimation_error": 0.0
      },
      {
        "chose_exact_optimal_action": true,
        "eval_greedy_action": "risky",
        "eval_start_exact_value": 0.81,
        "eval_start_learned_value": 0.8100000000000002,
        "exact_optimal_action": "risky",
        "exact_risky_q": 0.81,
        "exact_safe_q": 0.7290000000000001,
        "learned_risky_q": 0.8100000000000002,
        "learned_safe_q": 0.7290000000000001,
        "long_horizon_value_mse": 3.129636159629258e-33,
        "max_policy_regret": 0.0,
        "mdp": "risky_risk_optimal",
        "mean_policy_regret": 0.0,
        "method": "mc_supervised",
        "observed_risky_failures": 1,
        "observed_risky_success_rate": 0.9,
        "observed_risky_successes": 9,
        "policy_regret": 0.0,
        "q_calibration_error": 7.806255641895632e-18,
        "q_overestimation_error": 1.1102230246251565e-16,
        "q_underestimation_error": 0.0,
        "regime": "matched",
        "risky_action_selection_rate": 1.0,
        "scenario_id": "risk_optimal__matched",
        "true_risky_success_prob": 0.9,
        "value_mse": 5.007417855406813e-34,
        "value_overestimation_error": 1.1102230246251565e-16,
        "value_underestimation_error": 0.0
      },
      {
        "chose_exact_optimal_action": true,
        "eval_greedy_action": "risky",
        "eval_start_exact_value": 0.81,
        "eval_start_learned_value": 0.9000000000000001,
        "exact_optimal_action": "risky",
        "exact_risky_q": 0.81,
        "exact_safe_q": 0.7290000000000001,
        "learned_risky_q": 0.9000000000000001,
        "learned_safe_q": 0.7290000000000001,
        "long_horizon_value_mse": 0.004050000000000003,
        "max_policy_regret": 0.0,
        "mdp": "risky_risk_optimal",
        "mean_policy_regret": 0.0,
        "method": "mc_supervised",
        "observed_risky_failures": 0,
        "observed_risky_success_rate": 1.0,
        "observed_risky_successes": 9,
        "policy_regret": 0.0,
        "q_calibration_error": 0.011250000000000003,
        "q_overestimation_error": 0.09000000000000008,
        "q_underestimation_error": 0.08999999999999998,
        "regime": "lucky_biased",
        "risky_action_selection_rate": 1.0,
        "scenario_id": "risk_optimal__lucky_biased",
        "true_risky_success_prob": 0.9,
        "value_mse": 0.0006480000000000006,
        "value_overestimation_error": 0.09000000000000008,
        "value_underestimation_error": 0.08999999999999998
      },
      {
        "chose_exact_optimal_action": true,
        "eval_greedy_action": "risky",
        "eval_start_exact_value": 0.81,
        "eval_start_learned_value": 0.9,
        "exact_optimal_action": "risky",
        "exact_risky_q": 0.81,
        "exact_safe_q": 0.7290000000000001,
        "learned_risky_q": 0.9,
        "learned_safe_q": 0.7290000000000001,
        "long_horizon_value_mse": 0.004049999999999998,
        "max_policy_regret": 0.0,
        "mdp": "risky_risk_optimal",
        "mean_policy_regret": 0.0,
        "method": "mc_supervised",
        "observed_risky_failures": 0,
        "observed_risky_success_rate": 1.0,
        "observed_risky_successes": 4,
        "policy_regret": 0.0,
        "q_calibration_error": 0.011249999999999996,
        "q_overestimation_error": 0.08999999999999997,
        "q_underestimation_error": 0.08999999999999998,
        "regime": "lucky_only",
        "risky_action_selection_rate": 1.0,
        "scenario_id": "risk_optimal__lucky_only",
        "true_risky_success_prob": 0.9,
        "value_mse": 0.0006479999999999997,
        "value_overestimation_error": 0.08999999999999997,
        "value_underestimation_error": 0.08999999999999998
      },
      {
        "chose_exact_optimal_action": false,
        "eval_greedy_action": "safe",
        "eval_start_exact_value": 0.81,
        "eval_start_learned_value": 0.7290000000000001,
        "exact_optimal_action": "risky",
        "exact_risky_q": 0.81,
        "exact_safe_q": 0.7290000000000001,
        "learned_risky_q": 0.45,
        "learned_safe_q": 0.7290000000000001,
        "long_horizon_value_mse": 0.03404025,
        "max_policy_regret": 0.08099999999999996,
        "mdp": "risky_risk_optimal",
        "mean_policy_regret": 0.011571428571428566,
        "method": "mc_supervised",
        "observed_risky_failures": 4,
        "observed_risky_success_rate": 0.5,
        "observed_risky_successes": 4,
        "policy_regret": 0.08099999999999996,
        "q_calibration_error": 0.045000000000000005,
        "q_overestimation_error": 0.36000000000000004,
        "q_underestimation_error": 0.36000000000000004,
        "regime": "unlucky_biased",
        "risky_action_selection_rate": 0.0,
        "scenario_id": "risk_optimal__unlucky_biased",
        "true_risky_success_prob": 0.9,
        "value_mse": 0.00544644,
        "value_overestimation_error": 0.36000000000000004,
        "value_underestimation_error": 0.08099999999999996
      },
      {
        "chose_exact_optimal_action": false,
        "eval_greedy_action": "safe",
        "eval_start_exact_value": 0.81,
        "eval_start_learned_value": 0.7290000000000001,
        "exact_optimal_action": "risky",
        "exact_risky_q": 0.81,
        "exact_safe_q": 0.7290000000000001,
        "learned_risky_q": 0.0,
        "learned_safe_q": 0.7290000000000001,
        "long_horizon_value_mse": 0.16566525000000007,
        "max_policy_regret": 0.08099999999999996,
        "mdp": "risky_risk_optimal",
        "mean_policy_regret": 0.011571428571428566,
        "method": "mc_supervised",
        "observed_risky_failures": 8,
        "observed_risky_success_rate": 0.0,
        "observed_risky_successes": 0,
        "policy_regret": 0.08099999999999996,
        "q_calibration_error": 0.10125,
        "q_overestimation_error": 0.8100000000000002,
        "q_underestimation_error": 0.81,
        "regime": "no_risky_success",
        "risky_action_selection_rate": 0.0,
        "scenario_id": "risk_optimal__no_risky_success",
        "true_risky_success_prob": 0.9,
        "value_mse": 0.02650644000000001,
        "value_overestimation_error": 0.8100000000000002,
        "value_underestimation_error": 0.08099999999999996
      }
    ]
  },
  "claim_tested": "Raw TRL overestimation is support-driven under stochastic coverage, while empirical MC/log methods are calibrated only when observed risky branch frequencies match the true MDP; a risk-optimal setting tests for conservative avoidance.",
  "commands_run": [
    "mkdir -p research/sto_trl/artifacts/0002 research/sto_trl/results && cp research/sto_trl/artifacts/0001/run_tabular_sto_trl.py research/sto_trl/artifacts/0002/run_coverage_stress.py",
    "conda run -n autoresearcher_sto_trl python research/sto_trl/artifacts/0002/run_coverage_stress.py",
    "conda run -n autoresearcher_sto_trl python scripts/validate_artifacts.py --repo-root . --json research/sto_trl/results/0002_result.json --schema schemas/result.schema.json --check-result-artifacts"
  ],
  "experiment_id": "0002",
  "interpretation": "The chain guard still recovered exact discounted reachability for raw and log TRL. Across risky regimes, raw TRL selected risky in every scenario with at least one observed lucky risky transition and did not select risky when no lucky risky transition was observed, confirming the support-driven failure mode. Empirical TRL-log and MC tracked observed frequencies: they were correct in matched regimes, became overoptimistic in safe-optimal lucky-biased/lucky-only regimes, and became too conservative in risk-optimal unlucky/no-success regimes. The risk-optimal setting therefore exposes that calibration gains are coverage-dependent, not simply safe-action conservatism.",
  "known_failures": [],
  "metrics": {
    "aggregate": {
      "mc_supervised_mean_policy_regret": 0.0666,
      "mc_supervised_optimal_action_rate": 0.7,
      "num_risky_scenarios": 10,
      "num_scenarios": 11,
      "raw_no_success_scenarios": 2,
      "raw_selected_risky_when_no_success_observed": 0,
      "raw_selected_risky_when_success_observed": 8,
      "raw_success_observed_scenarios": 8,
      "trl_log_mean_policy_regret": 0.0666,
      "trl_log_optimal_action_rate": 0.7,
      "trl_raw_mean_policy_regret": 0.20970000000000005
    },
    "experiment_id": "0002",
    "gamma": 0.9,
    "regime_specs": {
      "risk_optimal": {
        "lucky_biased": {
          "risky_failures": 0,
          "risky_successes": 9
        },
        "lucky_only": {
          "risky_failures": 0,
          "risky_successes": 4
        },
        "matched": {
          "risky_failures": 1,
          "risky_successes": 9
        },
        "no_risky_success": {
          "risky_failures": 8,
          "risky_successes": 0
        },
        "unlucky_biased": {
          "risky_failures": 4,
          "risky_successes": 4
        }
      },
      "safe_optimal": {
        "lucky_biased": {
          "risky_failures": 2,
          "risky_successes": 6
        },
        "lucky_only": {
          "risky_failures": 0,
          "risky_successes": 4
        },
        "matched": {
          "risky_failures": 6,
          "risky_successes": 2
        },
        "no_risky_success": {
          "risky_failures": 8,
          "risky_successes": 0
        },
        "unlucky_biased": {
          "risky_failures": 7,
          "risky_successes": 1
        }
      }
    },
    "safe_episodes_per_regime": 4,
    "scenarios": {
      "deterministic_chain__chain_regression": {
        "coverage_diagnostics": {
          "action_counts": {
            "left": 5,
            "right": 5
          },
          "future_goal_coverage_fraction": 1.0,
          "future_goals_seen": [
            "c0",
            "c1",
            "c2",
            "c3",
            "c4",
            "c5"
          ],
          "mdp": "deterministic_chain",
          "num_episodes": 2,
          "num_transitions": 10,
          "outcome_counts": {
            "deterministic": 10
          },
          "regime": "chain_regression",
          "risky_failure_count": 0,
          "risky_success_count": 0,
          "risky_success_rate_observed": null,
          "state_action_coverage_fraction": 1.0,
          "state_action_pairs_seen": [
            [
              "c0",
              "right"
            ],
            [
              "c1",
              "left"
            ],
            [
              "c1",
              "right"
            ],
            [
              "c2",
              "left"
            ],
            [
              "c2",
              "right"
            ],
            [
              "c3",
              "left"
            ],
            [
              "c3",
              "right"
            ],
            [
              "c4",
              "left"
            ],
            [
              "c4",
              "right"
            ],
            [
              "c5",
              "left"
            ]
          ],
          "state_coverage_fraction": 1.0,
          "states_seen": [
            "c0",
            "c1",
            "c2",
            "c3",
            "c4",
            "c5"
          ],
          "transition_counts": {
            "c0|right|c1": 1,
            "c1|left|c0": 1,
            "c1|right|c2": 1,
            "c2|left|c1": 1,
            "c2|right|c3": 1,
            "c3|left|c2": 1,
            "c3|right|c4": 1,
            "c4|left|c3": 1,
            "c4|right|c5": 1,
            "c5|left|c4": 1
          },
          "true_risky_success_prob": null
        },
        "mdp": "deterministic_chain",
        "methods": {
          "mc_plus_trl_log": {
            "calibration_error": 0.13193442000000005,
            "chose_exact_optimal_action": true,
            "eval_goal": "c5",
            "eval_greedy_action": "right",
            "eval_start": "c0",
            "eval_start_exact_q": {
              "right": 0.5904900000000002
            },
            "eval_start_exact_value": 0.5904900000000002,
            "eval_start_learned_q": {
              "right": 0.5904900000000002
            },
            "eval_start_learned_value": 0.5904900000000002,
            "exact_optimal_action": "right",
            "long_horizon_value_mse": 0.0,
            "max_policy_regret": 0.0,
            "mean_policy_regret": 0.0,
            "policy_regret": 0.0,
            "q_calibration_error": 0.13193442000000005,
            "q_overestimation_error": 0.0,
            "q_underestimation_error": 0.36450000000000005,
            "risky_action_selection_rate": 0.0,
            "value_mse": 0.0,
            "value_overestimation_error": 0.0,
            "value_underestimation_error": 0.0
          },
          "mc_supervised": {
            "calibration_error": 0.2638688400000001,
            "chose_exact_optimal_action": true,
            "eval_goal": "c5",
            "eval_greedy_action": "right",
            "eval_start": "c0",
            "eval_start_exact_q": {
              "right": 0.5904900000000002
            },
            "eval_start_exact_value": 0.5904900000000002,
            "eval_start_learned_q": {
              "right": 0.5904900000000001
            },
            "eval_start_learned_value": 0.5904900000000001,
            "exact_optimal_action": "right",
            "long_horizon_value_mse": 3.697785493223493e-33,
            "max_policy_regret": 0.0,
            "mean_policy_regret": 0.0,
            "policy_regret": 0.0,
            "q_calibration_error": 0.2638688400000001,
            "q_overestimation_error": 0.0,
            "q_underestimation_error": 0.7290000000000001,
            "risky_action_selection_rate": 0.0,
            "value_mse": 2.0543252740130515e-33,
            "value_overestimation_error": 0.0,
            "value_underestimation_error": 1.1102230246251565e-16
          },
          "trl_log": {
            "calibration_error": 0.0,
            "chose_exact_optimal_action": true,
            "eval_goal": "c5",
            "eval_greedy_action": "right",
            "eval_start": "c0",
            "eval_start_exact_q": {
              "right": 0.5904900000000002
            },
            "eval_start_exact_value": 0.5904900000000002,
            "eval_start_learned_q": {
              "right": 0.5904900000000002
            },
            "eval_start_learned_value": 0.5904900000000002,
            "exact_optimal_action": "right",
            "long_horizon_value_mse": 0.0,
            "max_policy_regret": 0.0,
            "mean_policy_regret": 0.0,
            "policy_regret": 0.0,
            "q_calibration_error": 0.0,
            "q_overestimation_error": 0.0,
            "q_underestimation_error": 0.0,
            "risky_action_selection_rate": 0.0,
            "value_mse": 0.0,
            "value_overestimation_error": 0.0,
            "value_underestimation_error": 0.0
          },
          "trl_raw": {
            "calibration_error": 0.0,
            "chose_exact_optimal_action": true,
            "eval_goal": "c5",
            "eval_greedy_action": "right",
            "eval_start": "c0",
            "eval_start_exact_q": {
              "right": 0.5904900000000002
            },
            "eval_start_exact_value": 0.5904900000000002,
            "eval_start_learned_q": {
              "right": 0.5904900000000002
            },
            "eval_start_learned_value": 0.5904900000000002,
            "exact_optimal_action": "right",
            "long_horizon_value_mse": 0.0,
            "max_policy_regret": 0.0,
            "mean_policy_regret": 0.0,
            "policy_regret": 0.0,
            "q_calibration_error": 0.0,
            "q_overestimation_error": 0.0,
            "q_underestimation_error": 0.0,
            "risky_action_selection_rate": 0.0,
            "value_mse": 0.0,
            "value_overestimation_error": 0.0,
            "value_underestimation_error": 0.0
          }
        },
        "regime": "chain_regression"
      },
      "risk_optimal__lucky_biased": {
        "coverage_diagnostics": {
          "action_counts": {
            "forward": 8,
            "risky": 9,
            "safe": 4
          },
          "future_goal_coverage_fraction": 0.6,
          "future_goals_seen": [
            "goal",
            "safe1",
            "safe2"
          ],
          "mdp": "risky_risk_optimal",
          "num_episodes": 13,
          "num_transitions": 21,
          "outcome_counts": {
            "risky_success": 9,
            "safe_goal": 4,
            "safe_step": 8
          },
          "regime": "lucky_biased",
          "risky_failure_count": 0,
          "risky_success_count": 9,
          "risky_success_rate_observed": 1.0,
          "state_action_coverage_fraction": 1.0,
          "state_action_pairs_seen": [
            [
              "safe1",
              "forward"
            ],
            [
              "safe2",
              "forward"
            ],
            [
              "start",
              "risky"
            ],
            [
              "start",
              "safe"
            ]
          ],
          "state_coverage_fraction": 0.8,
          "states_seen": [
            "goal",
            "safe1",
            "safe2",
            "start"
          ],
          "transition_counts": {
            "safe1|forward|safe2": 4,
            "safe2|forward|goal": 4,
            "start|risky|goal": 9,
            "start|safe|safe1": 4
          },
          "true_risky_success_prob": 0.9
        },
        "mdp": "risky_risk_optimal",
        "methods": {
          "mc_plus_trl_log": {
            "calibration_error": 0.011250000000000003,
            "chose_exact_optimal_action": true,
            "eval_goal": "goal",
            "eval_greedy_action": "risky",
            "eval_start": "start",
            "eval_start_exact_q": {
              "risky": 0.81,
              "safe": 0.7290000000000001
            },
            "eval_start_exact_value": 0.81,
            "eval_start_learned_q": {
              "risky": 0.9000000000000001,
              "safe": 0.7290000000000001
            },
            "eval_start_learned_value": 0.9000000000000001,
            "exact_optimal_action": "risky",
            "long_horizon_value_mse": 0.004050000000000003,
            "max_policy_regret": 0.0,
            "mean_policy_regret": 0.0,
            "policy_regret": 0.0,
            "q_calibration_error": 0.011250000000000003,
            "q_overestimation_error": 0.09000000000000008,
            "q_underestimation_error": 0.08999999999999998,
            "risky_action_selection_rate": 1.0,
            "value_mse": 0.0006480000000000006,
            "value_overestimation_error": 0.09000000000000008,
            "value_underestimation_error": 0.08999999999999998
          },
          "mc_supervised": {
            "calibration_error": 0.011250000000000003,
            "chose_exact_optimal_action": true,
            "eval_goal": "goal",
            "eval_greedy_action": "risky",
            "eval_start": "start",
            "eval_start_exact_q": {
              "risky": 0.81,
              "safe": 0.7290000000000001
            },
            "eval_start_exact_value": 0.81,
            "eval_start_learned_q": {
              "risky": 0.9000000000000001,
              "safe": 0.7290000000000001
            },
            "eval_start_learned_value": 0.9000000000000001,
            "exact_optimal_action": "risky",
            "long_horizon_value_mse": 0.004050000000000003,
            "max_policy_regret": 0.0,
            "mean_policy_regret": 0.0,
            "policy_regret": 0.0,
            "q_calibration_error": 0.011250000000000003,
            "q_overestimation_error": 0.09000000000000008,
            "q_underestimation_error": 0.08999999999999998,
            "risky_action_selection_rate": 1.0,
            "value_mse": 0.0006480000000000006,
            "value_overestimation_error": 0.09000000000000008,
            "value_underestimation_error": 0.08999999999999998
          },
          "trl_log": {
            "calibration_error": 0.011249999999999996,
            "chose_exact_optimal_action": true,
            "eval_goal": "goal",
            "eval_greedy_action": "risky",
            "eval_start": "start",
            "eval_start_exact_q": {
              "risky": 0.81,
              "safe": 0.7290000000000001
            },
            "eval_start_exact_value": 0.81,
            "eval_start_learned_q": {
              "risky": 0.9,
              "safe": 0.7290000000000001
            },
            "eval_start_learned_value": 0.9,
            "exact_optimal_action": "risky",
            "long_horizon_value_mse": 0.004049999999999998,
            "max_policy_regret": 0.0,
            "mean_policy_regret": 0.0,
            "policy_regret": 0.0,
            "q_calibration_error": 0.011249999999999996,
            "q_overestimation_error": 0.08999999999999997,
            "q_underestimation_error": 0.08999999999999998,
            "risky_action_selection_rate": 1.0,
            "value_mse": 0.0006479999999999997,
            "value_overestimation_error": 0.08999999999999997,
            "value_underestimation_error": 0.08999999999999998
          },
          "trl_raw": {
            "calibration_error": 0.011249999999999996,
            "chose_exact_optimal_action": true,
            "eval_goal": "goal",
            "eval_greedy_action": "risky",
            "eval_start": "start",
            "eval_start_exact_q": {
              "risky": 0.81,
              "safe": 0.7290000000000001
            },
            "eval_start_exact_value": 0.81,
            "eval_start_learned_q": {
              "risky": 0.9,
              "safe": 0.7290000000000001
            },
            "eval_start_learned_value": 0.9,
            "exact_optimal_action": "risky",
            "long_horizon_value_mse": 0.004049999999999998,
            "max_policy_regret": 0.0,
            "mean_policy_regret": 0.0,
            "policy_regret": 0.0,
            "q_calibration_error": 0.011249999999999996,
            "q_overestimation_error": 0.08999999999999997,
            "q_underestimation_error": 0.08999999999999998,
            "risky_action_selection_rate": 1.0,
            "value_mse": 0.0006479999999999997,
            "value_overestimation_error": 0.08999999999999997,
            "value_underestimation_error": 0.08999999999999998
          }
        },
        "regime": "lucky_biased",
        "setting": "risk_optimal"
      },
      "risk_optimal__lucky_only": {
        "coverage_diagnostics": {
          "action_counts": {
            "forward": 8,
            "risky": 4,
            "safe": 4
          },
          "future_goal_coverage_fraction": 0.6,
          "future_goals_seen": [
            "goal",
            "safe1",
            "safe2"
          ],
          "mdp": "risky_risk_optimal",
          "num_episodes": 8,
          "num_transitions": 16,
          "outcome_counts": {
            "risky_success": 4,
            "safe_goal": 4,
            "safe_step": 8
          },
          "regime": "lucky_only",
          "risky_failure_count": 0,
          "risky_success_count": 4,
          "risky_success_rate_observed": 1.0,
          "state_action_coverage_fraction": 1.0,
          "state_action_pairs_seen": [
            [
              "safe1",
              "forward"
            ],
            [
              "safe2",
              "forward"
            ],
            [
              "start",
              "risky"
            ],
            [
              "start",
              "safe"
            ]
          ],
          "state_coverage_fraction": 0.8,
          "states_seen": [
            "goal",
            "safe1",
            "safe2",
            "start"
          ],
          "transition_counts": {
            "safe1|forward|safe2": 4,
            "safe2|forward|goal": 4,
            "start|risky|goal": 4,
            "start|safe|safe1": 4
          },
          "true_risky_success_prob": 0.9
        },
        "mdp": "risky_risk_optimal",
        "methods": {
          "mc_plus_trl_log": {
            "calibration_error": 0.011249999999999996,
            "chose_exact_optimal_action": true,
            "eval_goal": "goal",
            "eval_greedy_action": "risky",
            "eval_start": "start",
            "eval_start_exact_q": {
              "risky": 0.81,
              "safe": 0.7290000000000001
            },
            "eval_start_exact_value": 0.81,
            "eval_start_learned_q": {
              "risky": 0.9,
              "safe": 0.7290000000000001
            },
            "eval_start_learned_value": 0.9,
            "exact_optimal_action": "risky",
            "long_horizon_value_mse": 0.004049999999999998,
            "max_policy_regret": 0.0,
            "mean_policy_regret": 0.0,
            "policy_regret": 0.0,
            "q_calibration_error": 0.011249999999999996,
            "q_overestimation_error": 0.08999999999999997,
            "q_underestimation_error": 0.08999999999999998,
            "risky_action_selection_rate": 1.0,
            "value_mse": 0.0006479999999999997,
            "value_overestimation_error": 0.08999999999999997,
            "value_underestimation_error": 0.08999999999999998
          },
          "mc_supervised": {
            "calibration_error": 0.011249999999999996,
            "chose_exact_optimal_action": true,
            "eval_goal": "goal",
            "eval_greedy_action": "risky",
            "eval_start": "start",
            "eval_start_exact_q": {
              "risky": 0.81,
              "safe": 0.7290000000000001
            },
            "eval_start_exact_value": 0.81,
            "eval_start_learned_q": {
              "risky": 0.9,
              "safe": 0.7290000000000001
            },
            "eval_start_learned_value": 0.9,
            "exact_optimal_action": "risky",
            "long_horizon_value_mse": 0.004049999999999998,
            "max_policy_regret": 0.0,
            "mean_policy_regret": 0.0,
            "policy_regret": 0.0,
            "q_calibration_error": 0.011249999999999996,
            "q_overestimation_error": 0.08999999999999997,
            "q_underestimation_error": 0.08999999999999998,
            "risky_action_selection_rate": 1.0,
            "value_mse": 0.0006479999999999997,
            "value_overestimation_error": 0.08999999999999997,
            "value_underestimation_error": 0.08999999999999998
          },
          "trl_log": {
            "calibration_error": 0.011249999999999996,
            "chose_exact_optimal_action": true,
            "eval_goal": "goal",
            "eval_greedy_action": "risky",
            "eval_start": "start",
            "eval_start_exact_q": {
              "risky": 0.81,
              "safe": 0.7290000000000001
            },
            "eval_start_exact_value": 0.81,
            "eval_start_learned_q": {
              "risky": 0.9,
              "safe": 0.7290000000000001
            },
            "eval_start_learned_value": 0.9,
            "exact_optimal_action": "risky",
            "long_horizon_value_mse": 0.004049999999999998,
            "max_policy_regret": 0.0,
            "mean_policy_regret": 0.0,
            "policy_regret": 0.0,
            "q_calibration_error": 0.011249999999999996,
            "q_overestimation_error": 0.08999999999999997,
            "q_underestimation_error": 0.08999999999999998,
            "risky_action_selection_rate": 1.0,
            "value_mse": 0.0006479999999999997,
            "value_overestimation_error": 0.08999999999999997,
            "value_underestimation_error": 0.08999999999999998
          },
          "trl_raw": {
            "calibration_error": 0.011249999999999996,
            "chose_exact_optimal_action": true,
            "eval_goal": "goal",
            "eval_greedy_action": "risky",
            "eval_start": "start",
            "eval_start_exact_q": {
              "risky": 0.81,
              "safe": 0.7290000000000001
            },
            "eval_start_exact_value": 0.81,
            "eval_start_learned_q": {
              "risky": 0.9,
              "safe": 0.7290000000000001
            },
            "eval_start_learned_value": 0.9,
            "exact_optimal_action": "risky",
            "long_horizon_value_mse": 0.004049999999999998,
            "max_policy_regret": 0.0,
            "mean_policy_regret": 0.0,
            "policy_regret": 0.0,
            "q_calibration_error": 0.011249999999999996,
            "q_overestimation_error": 0.08999999999999997,
            "q_underestimation_error": 0.08999999999999998,
            "risky_action_selection_rate": 1.0,
            "value_mse": 0.0006479999999999997,
            "value_overestimation_error": 0.08999999999999997,
            "value_underestimation_error": 0.08999999999999998
          }
        },
        "regime": "lucky_only",
        "setting": "risk_optimal"
      },
      "risk_optimal__matched": {
        "coverage_diagnostics": {
          "action_counts": {
            "forward": 8,
            "risky": 10,
            "safe": 4
          },
          "future_goal_coverage_fraction": 0.8,
          "future_goals_seen": [
            "goal",
            "safe1",
            "safe2",
            "trap"
          ],
          "mdp": "risky_risk_optimal",
          "num_episodes": 14,
          "num_transitions": 22,
          "outcome_counts": {
            "risky_failure": 1,
            "risky_success": 9,
            "safe_goal": 4,
            "safe_step": 8
          },
          "regime": "matched",
          "risky_failure_count": 1,
          "risky_success_count": 9,
          "risky_success_rate_observed": 0.9,
          "state_action_coverage_fraction": 1.0,
          "state_action_pairs_seen": [
            [
              "safe1",
              "forward"
            ],
            [
              "safe2",
              "forward"
            ],
            [
              "start",
              "risky"
            ],
            [
              "start",
              "safe"
            ]
          ],
          "state_coverage_fraction": 1.0,
          "states_seen": [
            "goal",
            "safe1",
            "safe2",
            "start",
            "trap"
          ],
          "transition_counts": {
            "safe1|forward|safe2": 4,
            "safe2|forward|goal": 4,
            "start|risky|goal": 9,
            "start|risky|trap": 1,
            "start|safe|safe1": 4
          },
          "true_risky_success_prob": 0.9
        },
        "mdp": "risky_risk_optimal",
        "methods": {
          "mc_plus_trl_log": {
            "calibration_error": 8.673617379884035e-19,
            "chose_exact_optimal_action": true,
            "eval_goal": "goal",
            "eval_greedy_action": "risky",
            "eval_start": "start",
            "eval_start_exact_q": {
              "risky": 0.81,
              "safe": 0.7290000000000001
            },
            "eval_start_exact_value": 0.81,
            "eval_start_learned_q": {
              "risky": 0.81,
              "safe": 0.7290000000000001
            },
            "eval_start_learned_value": 0.81,
            "exact_optimal_action": "risky",
            "long_horizon_value_mse": 4.81482486096809e-35,
            "max_policy_regret": 0.0,
            "mean_policy_regret": 0.0,
            "policy_regret": 0.0,
            "q_calibration_error": 8.673617379884035e-19,
            "q_overestimation_error": 1.3877787807814457e-17,
            "q_underestimation_error": 0.0,
            "risky_action_selection_rate": 1.0,
            "value_mse": 7.703719777548944e-36,
            "value_overestimation_error": 1.3877787807814457e-17,
            "value_underestimation_error": 0.0
          },
          "mc_supervised": {
            "calibration_error": 7.806255641895632e-18,
            "chose_exact_optimal_action": true,
            "eval_goal": "goal",
            "eval_greedy_action": "risky",
            "eval_start": "start",
            "eval_start_exact_q": {
              "risky": 0.81,
              "safe": 0.7290000000000001
            },
            "eval_start_exact_value": 0.81,
            "eval_start_learned_q": {
              "risky": 0.8100000000000002,
              "safe": 0.7290000000000001
            },
            "eval_start_learned_value": 0.8100000000000002,
            "exact_optimal_action": "risky",
            "long_horizon_value_mse": 3.129636159629258e-33,
            "max_policy_regret": 0.0,
            "mean_policy_regret": 0.0,
            "policy_regret": 0.0,
            "q_calibration_error": 7.806255641895632e-18,
            "q_overestimation_error": 1.1102230246251565e-16,
            "q_underestimation_error": 0.0,
            "risky_action_selection_rate": 1.0,
            "value_mse": 5.007417855406813e-34,
            "value_overestimation_error": 1.1102230246251565e-16,
            "value_underestimation_error": 0.0
          },
          "trl_log": {
            "calibration_error": 1.734723475976807e-18,
            "chose_exact_optimal_action": true,
            "eval_goal": "goal",
            "eval_greedy_action": "risky",
            "eval_start": "start",
            "eval_start_exact_q": {
              "risky": 0.81,
              "safe": 0.7290000000000001
            },
            "eval_start_exact_value": 0.81,
            "eval_start_learned_q": {
              "risky": 0.81,
              "safe": 0.7290000000000001
            },
            "eval_start_learned_value": 0.81,
            "exact_optimal_action": "risky",
            "long_horizon_value_mse": 1.925929944387236e-34,
            "max_policy_regret": 0.0,
            "mean_policy_regret": 0.0,
            "policy_regret": 0.0,
            "q_calibration_error": 1.734723475976807e-18,
            "q_overestimation_error": 2.7755575615628914e-17,
            "q_underestimation_error": 0.0,
            "risky_action_selection_rate": 1.0,
            "value_mse": 3.0814879110195774e-35,
            "value_overestimation_error": 2.7755575615628914e-17,
            "value_underestimation_error": 0.0
          },
          "trl_raw": {
            "calibration_error": 0.05625,
            "chose_exact_optimal_action": true,
            "eval_goal": "goal",
            "eval_greedy_action": "risky",
            "eval_start": "start",
            "eval_start_exact_q": {
              "risky": 0.81,
              "safe": 0.7290000000000001
            },
            "eval_start_exact_value": 0.81,
            "eval_start_learned_q": {
              "risky": 0.9,
              "safe": 0.7290000000000001
            },
            "eval_start_learned_value": 0.9,
            "exact_optimal_action": "risky",
            "long_horizon_value_mse": 0.16605000000000003,
            "max_policy_regret": 0.0,
            "mean_policy_regret": 0.0,
            "policy_regret": 0.0,
            "q_calibration_error": 0.05625,
            "q_overestimation_error": 0.81,
            "q_underestimation_error": 0.0,
            "risky_action_selection_rate": 1.0,
            "value_mse": 0.026568000000000005,
            "value_overestimation_error": 0.81,
            "value_underestimation_error": 0.0
          }
        },
        "regime": "matched",
        "setting": "risk_optimal"
      },
      "risk_optimal__no_risky_success": {
        "coverage_diagnostics": {
          "action_counts": {
            "forward": 8,
            "risky": 8,
            "safe": 4
          },
          "future_goal_coverage_fraction": 0.8,
          "future_goals_seen": [
            "goal",
            "safe1",
            "safe2",
            "trap"
          ],
          "mdp": "risky_risk_optimal",
          "num_episodes": 12,
          "num_transitions": 20,
          "outcome_counts": {
            "risky_failure": 8,
            "safe_goal": 4,
            "safe_step": 8
          },
          "regime": "no_risky_success",
          "risky_failure_count": 8,
          "risky_success_count": 0,
          "risky_success_rate_observed": 0.0,
          "state_action_coverage_fraction": 1.0,
          "state_action_pairs_seen": [
            [
              "safe1",
              "forward"
            ],
            [
              "safe2",
              "forward"
            ],
            [
              "start",
              "risky"
            ],
            [
              "start",
              "safe"
            ]
          ],
          "state_coverage_fraction": 1.0,
          "states_seen": [
            "goal",
            "safe1",
            "safe2",
            "start",
            "trap"
          ],
          "transition_counts": {
            "safe1|forward|safe2": 4,
            "safe2|forward|goal": 4,
            "start|risky|trap": 8,
            "start|safe|safe1": 4
          },
          "true_risky_success_prob": 0.9
        },
        "mdp": "risky_risk_optimal",
        "methods": {
          "mc_plus_trl_log": {
            "calibration_error": 0.10125,
            "chose_exact_optimal_action": false,
            "eval_goal": "goal",
            "eval_greedy_action": "safe",
            "eval_start": "start",
            "eval_start_exact_q": {
              "risky": 0.81,
              "safe": 0.7290000000000001
            },
            "eval_start_exact_value": 0.81,
            "eval_start_learned_q": {
              "risky": 0.0,
              "safe": 0.7290000000000001
            },
            "eval_start_learned_value": 0.7290000000000001,
            "exact_optimal_action": "risky",
            "long_horizon_value_mse": 0.16566525000000007,
            "max_policy_regret": 0.08099999999999996,
            "mean_policy_regret": 0.011571428571428566,
            "policy_regret": 0.08099999999999996,
            "q_calibration_error": 0.10125,
            "q_overestimation_error": 0.8100000000000002,
            "q_underestimation_error": 0.81,
            "risky_action_selection_rate": 0.0,
            "value_mse": 0.02650644000000001,
            "value_overestimation_error": 0.8100000000000002,
            "value_underestimation_error": 0.08099999999999996
          },
          "mc_supervised": {
            "calibration_error": 0.10125,
            "chose_exact_optimal_action": false,
            "eval_goal": "goal",
            "eval_greedy_action": "safe",
            "eval_start": "start",
            "eval_start_exact_q": {
              "risky": 0.81,
              "safe": 0.7290000000000001
            },
            "eval_start_exact_value": 0.81,
            "eval_start_learned_q": {
              "risky": 0.0,
              "safe": 0.7290000000000001
            },
            "eval_start_learned_value": 0.7290000000000001,
            "exact_optimal_action": "risky",
            "long_horizon_value_mse": 0.16566525000000007,
            "max_policy_regret": 0.08099999999999996,
            "mean_policy_regret": 0.011571428571428566,
            "policy_regret": 0.08099999999999996,
            "q_calibration_error": 0.10125,
            "q_overestimation_error": 0.8100000000000002,
            "q_underestimation_error": 0.81,
            "risky_action_selection_rate": 0.0,
            "value_mse": 0.02650644000000001,
            "value_overestimation_error": 0.8100000000000002,
            "value_underestimation_error": 0.08099999999999996
          },
          "trl_log": {
            "calibration_error": 0.10125,
            "chose_exact_optimal_action": false,
            "eval_goal": "goal",
            "eval_greedy_action": "safe",
            "eval_start": "start",
            "eval_start_exact_q": {
              "risky": 0.81,
              "safe": 0.7290000000000001
            },
            "eval_start_exact_value": 0.81,
            "eval_start_learned_q": {
              "risky": 0.0,
              "safe": 0.7290000000000001
            },
            "eval_start_learned_value": 0.7290000000000001,
            "exact_optimal_action": "risky",
            "long_horizon_value_mse": 0.16566525000000004,
            "max_policy_regret": 0.08099999999999996,
            "mean_policy_regret": 0.011571428571428566,
            "policy_regret": 0.08099999999999996,
            "q_calibration_error": 0.10125,
            "q_overestimation_error": 0.81,
            "q_underestimation_error": 0.81,
            "risky_action_selection_rate": 0.0,
            "value_mse": 0.026506440000000006,
            "value_overestimation_error": 0.81,
            "value_underestimation_error": 0.08099999999999996
          },
          "trl_raw": {
            "calibration_error": 0.10125,
            "chose_exact_optimal_action": false,
            "eval_goal": "goal",
            "eval_greedy_action": "safe",
            "eval_start": "start",
            "eval_start_exact_q": {
              "risky": 0.81,
              "safe": 0.7290000000000001
            },
            "eval_start_exact_value": 0.81,
            "eval_start_learned_q": {
              "risky": 0.0,
              "safe": 0.7290000000000001
            },
            "eval_start_learned_value": 0.7290000000000001,
            "exact_optimal_action": "risky",
            "long_horizon_value_mse": 0.16566525000000004,
            "max_policy_regret": 0.08099999999999996,
            "mean_policy_regret": 0.011571428571428566,
            "policy_regret": 0.08099999999999996,
            "q_calibration_error": 0.10125,
            "q_overestimation_error": 0.81,
            "q_underestimation_error": 0.81,
            "risky_action_selection_rate": 0.0,
            "value_mse": 0.026506440000000006,
            "value_overestimation_error": 0.81,
            "value_underestimation_error": 0.08099999999999996
          }
        },
        "regime": "no_risky_success",
        "setting": "risk_optimal"
      },
      "risk_optimal__unlucky_biased": {
        "coverage_diagnostics": {
          "action_counts": {
            "forward": 8,
            "risky": 8,
            "safe": 4
          },
          "future_goal_coverage_fraction": 0.8,
          "future_goals_seen": [
            "goal",
            "safe1",
            "safe2",
            "trap"
          ],
          "mdp": "risky_risk_optimal",
          "num_episodes": 12,
          "num_transitions": 20,
          "outcome_counts": {
            "risky_failure": 4,
            "risky_success": 4,
            "safe_goal": 4,
            "safe_step": 8
          },
          "regime": "unlucky_biased",
          "risky_failure_count": 4,
          "risky_success_count": 4,
          "risky_success_rate_observed": 0.5,
          "state_action_coverage_fraction": 1.0,
          "state_action_pairs_seen": [
            [
              "safe1",
              "forward"
            ],
            [
              "safe2",
              "forward"
            ],
            [
              "start",
              "risky"
            ],
            [
              "start",
              "safe"
            ]
          ],
          "state_coverage_fraction": 1.0,
          "states_seen": [
            "goal",
            "safe1",
            "safe2",
            "start",
            "trap"
          ],
          "transition_counts": {
            "safe1|forward|safe2": 4,
            "safe2|forward|goal": 4,
            "start|risky|goal": 4,
            "start|risky|trap": 4,
            "start|safe|safe1": 4
          },
          "true_risky_success_prob": 0.9
        },
        "mdp": "risky_risk_optimal",
        "methods": {
          "mc_plus_trl_log": {
            "calibration_error": 0.045000000000000005,
            "chose_exact_optimal_action": false,
            "eval_goal": "goal",
            "eval_greedy_action": "safe",
            "eval_start": "start",
            "eval_start_exact_q": {
              "risky": 0.81,
              "safe": 0.7290000000000001
            },
            "eval_start_exact_value": 0.81,
            "eval_start_learned_q": {
              "risky": 0.45000000000000007,
              "safe": 0.7290000000000001
            },
            "eval_start_learned_value": 0.7290000000000001,
            "exact_optimal_action": "risky",
            "long_horizon_value_mse": 0.034040250000000015,
            "max_policy_regret": 0.08099999999999996,
            "mean_policy_regret": 0.011571428571428566,
            "policy_regret": 0.08099999999999996,
            "q_calibration_error": 0.045000000000000005,
            "q_overestimation_error": 0.3600000000000001,
            "q_underestimation_error": 0.36,
            "risky_action_selection_rate": 0.0,
            "value_mse": 0.005446440000000002,
            "value_overestimation_error": 0.3600000000000001,
            "value_underestimation_error": 0.08099999999999996
          },
          "mc_supervised": {
            "calibration_error": 0.045000000000000005,
            "chose_exact_optimal_action": false,
            "eval_goal": "goal",
            "eval_greedy_action": "safe",
            "eval_start": "start",
            "eval_start_exact_q": {
              "risky": 0.81,
              "safe": 0.7290000000000001
            },
            "eval_start_exact_value": 0.81,
            "eval_start_learned_q": {
              "risky": 0.45,
              "safe": 0.7290000000000001
            },
            "eval_start_learned_value": 0.7290000000000001,
            "exact_optimal_action": "risky",
            "long_horizon_value_mse": 0.03404025,
            "max_policy_regret": 0.08099999999999996,
            "mean_policy_regret": 0.011571428571428566,
            "policy_regret": 0.08099999999999996,
            "q_calibration_error": 0.045000000000000005,
            "q_overestimation_error": 0.36000000000000004,
            "q_underestimation_error": 0.36000000000000004,
            "risky_action_selection_rate": 0.0,
            "value_mse": 0.00544644,
            "value_overestimation_error": 0.36000000000000004,
            "value_underestimation_error": 0.08099999999999996
          },
          "trl_log": {
            "calibration_error": 0.045000000000000005,
            "chose_exact_optimal_action": false,
            "eval_goal": "goal",
            "eval_greedy_action": "safe",
            "eval_start": "start",
            "eval_start_exact_q": {
              "risky": 0.81,
              "safe": 0.7290000000000001
            },
            "eval_start_exact_value": 0.81,
            "eval_start_learned_q": {
              "risky": 0.45000000000000007,
              "safe": 0.7290000000000001
            },
            "eval_start_learned_value": 0.7290000000000001,
            "exact_optimal_action": "risky",
            "long_horizon_value_mse": 0.034040250000000015,
            "max_policy_regret": 0.08099999999999996,
            "mean_policy_regret": 0.011571428571428566,
            "policy_regret": 0.08099999999999996,
            "q_calibration_error": 0.045000000000000005,
            "q_overestimation_error": 0.3600000000000001,
            "q_underestimation_error": 0.36,
            "risky_action_selection_rate": 0.0,
            "value_mse": 0.005446440000000002,
            "value_overestimation_error": 0.3600000000000001,
            "value_underestimation_error": 0.08099999999999996
          },
          "trl_raw": {
            "calibration_error": 0.05625,
            "chose_exact_optimal_action": true,
            "eval_goal": "goal",
            "eval_greedy_action": "risky",
            "eval_start": "start",
            "eval_start_exact_q": {
              "risky": 0.81,
              "safe": 0.7290000000000001
            },
            "eval_start_exact_value": 0.81,
            "eval_start_learned_q": {
              "risky": 0.9,
              "safe": 0.7290000000000001
            },
            "eval_start_learned_value": 0.9,
            "exact_optimal_action": "risky",
            "long_horizon_value_mse": 0.16605000000000003,
            "max_policy_regret": 0.0,
            "mean_policy_regret": 0.0,
            "policy_regret": 0.0,
            "q_calibration_error": 0.05625,
            "q_overestimation_error": 0.81,
            "q_underestimation_error": 0.0,
            "risky_action_selection_rate": 1.0,
            "value_mse": 0.026568000000000005,
            "value_overestimation_error": 0.81,
            "value_underestimation_error": 0.0
          }
        },
        "regime": "unlucky_biased",
        "setting": "risk_optimal"
      },
      "safe_optimal__lucky_biased": {
        "coverage_diagnostics": {
          "action_counts": {
            "forward": 8,
            "risky": 8,
            "safe": 4
          },
          "future_goal_coverage_fraction": 0.8,
          "future_goals_seen": [
            "goal",
            "safe1",
            "safe2",
            "trap"
          ],
          "mdp": "risky_safe_optimal",
          "num_episodes": 12,
          "num_transitions": 20,
          "outcome_counts": {
            "risky_failure": 2,
            "risky_success": 6,
            "safe_goal": 4,
            "safe_step": 8
          },
          "regime": "lucky_biased",
          "risky_failure_count": 2,
          "risky_success_count": 6,
          "risky_success_rate_observed": 0.75,
          "state_action_coverage_fraction": 1.0,
          "state_action_pairs_seen": [
            [
              "safe1",
              "forward"
            ],
            [
              "safe2",
              "forward"
            ],
            [
              "start",
              "risky"
            ],
            [
              "start",
              "safe"
            ]
          ],
          "state_coverage_fraction": 1.0,
          "states_seen": [
            "goal",
            "safe1",
            "safe2",
            "start",
            "trap"
          ],
          "transition_counts": {
            "safe1|forward|safe2": 4,
            "safe2|forward|goal": 4,
            "start|risky|goal": 6,
            "start|risky|trap": 2,
            "start|safe|safe1": 4
          },
          "true_risky_success_prob": 0.25
        },
        "mdp": "risky_safe_optimal",
        "methods": {
          "mc_plus_trl_log": {
            "calibration_error": 0.05625000000000001,
            "chose_exact_optimal_action": true,
            "eval_goal": "goal",
            "eval_greedy_action": "safe",
            "eval_start": "start",
            "eval_start_exact_q": {
              "risky": 0.225,
              "safe": 0.7290000000000001
            },
            "eval_start_exact_value": 0.7290000000000001,
            "eval_start_learned_q": {
              "risky": 0.675,
              "safe": 0.7290000000000001
            },
            "eval_start_learned_value": 0.7290000000000001,
            "exact_optimal_action": "safe",
            "long_horizon_value_mse": 0.05062500000000002,
            "max_policy_regret": 0.0,
            "mean_policy_regret": 0.0,
            "policy_regret": 0.0,
            "q_calibration_error": 0.05625000000000001,
            "q_overestimation_error": 0.45000000000000007,
            "q_underestimation_error": 0.45000000000000007,
            "risky_action_selection_rate": 0.0,
            "value_mse": 0.008100000000000003,
            "value_overestimation_error": 0.0,
            "value_underestimation_error": 0.45000000000000007
          },
          "mc_supervised": {
            "calibration_error": 0.05625000000000001,
            "chose_exact_optimal_action": true,
            "eval_goal": "goal",
            "eval_greedy_action": "safe",
            "eval_start": "start",
            "eval_start_exact_q": {
              "risky": 0.225,
              "safe": 0.7290000000000001
            },
            "eval_start_exact_value": 0.7290000000000001,
            "eval_start_learned_q": {
              "risky": 0.675,
              "safe": 0.7290000000000001
            },
            "eval_start_learned_value": 0.7290000000000001,
            "exact_optimal_action": "safe",
            "long_horizon_value_mse": 0.05062500000000002,
            "max_policy_regret": 0.0,
            "mean_policy_regret": 0.0,
            "policy_regret": 0.0,
            "q_calibration_error": 0.05625000000000001,
            "q_overestimation_error": 0.45000000000000007,
            "q_underestimation_error": 0.45000000000000007,
            "risky_action_selection_rate": 0.0,
            "value_mse": 0.008100000000000003,
            "value_overestimation_error": 0.0,
            "value_underestimation_error": 0.45000000000000007
          },
          "trl_log": {
            "calibration_error": 0.05625000000000001,
            "chose_exact_optimal_action": true,
            "eval_goal": "goal",
            "eval_greedy_action": "safe",
            "eval_start": "start",
            "eval_start_exact_q": {
              "risky": 0.225,
              "safe": 0.7290000000000001
            },
            "eval_start_exact_value": 0.7290000000000001,
            "eval_start_learned_q": {
              "risky": 0.675,
              "safe": 0.7290000000000001
            },
            "eval_start_learned_value": 0.7290000000000001,
            "exact_optimal_action": "safe",
            "long_horizon_value_mse": 0.05062500000000002,
            "max_policy_regret": 0.0,
            "mean_policy_regret": 0.0,
            "policy_regret": 0.0,
            "q_calibration_error": 0.05625000000000001,
            "q_overestimation_error": 0.45000000000000007,
            "q_underestimation_error": 0.45000000000000007,
            "risky_action_selection_rate": 0.0,
            "value_mse": 0.008100000000000003,
            "value_overestimation_error": 0.0,
            "value_underestimation_error": 0.45000000000000007
          },
          "trl_raw": {
            "calibration_error": 0.05625,
            "chose_exact_optimal_action": false,
            "eval_goal": "goal",
            "eval_greedy_action": "risky",
            "eval_start": "start",
            "eval_start_exact_q": {
              "risky": 0.225,
              "safe": 0.7290000000000001
            },
            "eval_start_exact_value": 0.7290000000000001,
            "eval_start_learned_q": {
              "risky": 0.9,
              "safe": 0.7290000000000001
            },
            "eval_start_learned_value": 0.9,
            "exact_optimal_action": "safe",
            "long_horizon_value_mse": 0.01996649999999999,
            "max_policy_regret": 0.5040000000000001,
            "mean_policy_regret": 0.07200000000000002,
            "policy_regret": 0.5040000000000001,
            "q_calibration_error": 0.05625,
            "q_overestimation_error": 0.675,
            "q_underestimation_error": 0.0,
            "risky_action_selection_rate": 1.0,
            "value_mse": 0.0031946399999999986,
            "value_overestimation_error": 0.22499999999999998,
            "value_underestimation_error": 0.0
          }
        },
        "regime": "lucky_biased",
        "setting": "safe_optimal"
      },
      "safe_optimal__lucky_only": {
        "coverage_diagnostics": {
          "action_counts": {
            "forward": 8,
            "risky": 4,
            "safe": 4
          },
          "future_goal_coverage_fraction": 0.6,
          "future_goals_seen": [
            "goal",
            "safe1",
            "safe2"
          ],
          "mdp": "risky_safe_optimal",
          "num_episodes": 8,
          "num_transitions": 16,
          "outcome_counts": {
            "risky_success": 4,
            "safe_goal": 4,
            "safe_step": 8
          },
          "regime": "lucky_only",
          "risky_failure_count": 0,
          "risky_success_count": 4,
          "risky_success_rate_observed": 1.0,
          "state_action_coverage_fraction": 1.0,
          "state_action_pairs_seen": [
            [
              "safe1",
              "forward"
            ],
            [
              "safe2",
              "forward"
            ],
            [
              "start",
              "risky"
            ],
            [
              "start",
              "safe"
            ]
          ],
          "state_coverage_fraction": 0.8,
          "states_seen": [
            "goal",
            "safe1",
            "safe2",
            "start"
          ],
          "transition_counts": {
            "safe1|forward|safe2": 4,
            "safe2|forward|goal": 4,
            "start|risky|goal": 4,
            "start|safe|safe1": 4
          },
          "true_risky_success_prob": 0.25
        },
        "mdp": "risky_safe_optimal",
        "methods": {
          "mc_plus_trl_log": {
            "calibration_error": 0.084375,
            "chose_exact_optimal_action": false,
            "eval_goal": "goal",
            "eval_greedy_action": "risky",
            "eval_start": "start",
            "eval_start_exact_q": {
              "risky": 0.225,
              "safe": 0.7290000000000001
            },
            "eval_start_exact_value": 0.7290000000000001,
            "eval_start_learned_q": {
              "risky": 0.9,
              "safe": 0.7290000000000001
            },
            "eval_start_learned_value": 0.9,
            "exact_optimal_action": "safe",
            "long_horizon_value_mse": 0.1212165,
            "max_policy_regret": 0.5040000000000001,
            "mean_policy_regret": 0.07200000000000002,
            "policy_regret": 0.5040000000000001,
            "q_calibration_error": 0.084375,
            "q_overestimation_error": 0.675,
            "q_underestimation_error": 0.675,
            "risky_action_selection_rate": 1.0,
            "value_mse": 0.01939464,
            "value_overestimation_error": 0.17099999999999993,
            "value_underestimation_error": 0.675
          },
          "mc_supervised": {
            "calibration_error": 0.084375,
            "chose_exact_optimal_action": false,
            "eval_goal": "goal",
            "eval_greedy_action": "risky",
            "eval_start": "start",
            "eval_start_exact_q": {
              "risky": 0.225,
              "safe": 0.7290000000000001
            },
            "eval_start_exact_value": 0.7290000000000001,
            "eval_start_learned_q": {
              "risky": 0.9,
              "safe": 0.7290000000000001
            },
            "eval_start_learned_value": 0.9,
            "exact_optimal_action": "safe",
            "long_horizon_value_mse": 0.1212165,
            "max_policy_regret": 0.5040000000000001,
            "mean_policy_regret": 0.07200000000000002,
            "policy_regret": 0.5040000000000001,
            "q_calibration_error": 0.084375,
            "q_overestimation_error": 0.675,
            "q_underestimation_error": 0.675,
            "risky_action_selection_rate": 1.0,
            "value_mse": 0.01939464,
            "value_overestimation_error": 0.17099999999999993,
            "value_underestimation_error": 0.675
          },
          "trl_log": {
            "calibration_error": 0.084375,
            "chose_exact_optimal_action": false,
            "eval_goal": "goal",
            "eval_greedy_action": "risky",
            "eval_start": "start",
            "eval_start_exact_q": {
              "risky": 0.225,
              "safe": 0.7290000000000001
            },
            "eval_start_exact_value": 0.7290000000000001,
            "eval_start_learned_q": {
              "risky": 0.9,
              "safe": 0.7290000000000001
            },
            "eval_start_learned_value": 0.9,
            "exact_optimal_action": "safe",
            "long_horizon_value_mse": 0.1212165,
            "max_policy_regret": 0.5040000000000001,
            "mean_policy_regret": 0.07200000000000002,
            "policy_regret": 0.5040000000000001,
            "q_calibration_error": 0.084375,
            "q_overestimation_error": 0.675,
            "q_underestimation_error": 0.675,
            "risky_action_selection_rate": 1.0,
            "value_mse": 0.01939464,
            "value_overestimation_error": 0.17099999999999993,
            "value_underestimation_error": 0.675
          },
          "trl_raw": {
            "calibration_error": 0.084375,
            "chose_exact_optimal_action": false,
            "eval_goal": "goal",
            "eval_greedy_action": "risky",
            "eval_start": "start",
            "eval_start_exact_q": {
              "risky": 0.225,
              "safe": 0.7290000000000001
            },
            "eval_start_exact_value": 0.7290000000000001,
            "eval_start_learned_q": {
              "risky": 0.9,
              "safe": 0.7290000000000001
            },
            "eval_start_learned_value": 0.9,
            "exact_optimal_action": "safe",
            "long_horizon_value_mse": 0.1212165,
            "max_policy_regret": 0.5040000000000001,
            "mean_policy_regret": 0.07200000000000002,
            "policy_regret": 0.5040000000000001,
            "q_calibration_error": 0.084375,
            "q_overestimation_error": 0.675,
            "q_underestimation_error": 0.675,
            "risky_action_selection_rate": 1.0,
            "value_mse": 0.01939464,
            "value_overestimation_error": 0.17099999999999993,
            "value_underestimation_error": 0.675
          }
        },
        "regime": "lucky_only",
        "setting": "safe_optimal"
      },
      "safe_optimal__matched": {
        "coverage_diagnostics": {
          "action_counts": {
            "forward": 8,
            "risky": 8,
            "safe": 4
          },
          "future_goal_coverage_fraction": 0.8,
          "future_goals_seen": [
            "goal",
            "safe1",
            "safe2",
            "trap"
          ],
          "mdp": "risky_safe_optimal",
          "num_episodes": 12,
          "num_transitions": 20,
          "outcome_counts": {
            "risky_failure": 6,
            "risky_success": 2,
            "safe_goal": 4,
            "safe_step": 8
          },
          "regime": "matched",
          "risky_failure_count": 6,
          "risky_success_count": 2,
          "risky_success_rate_observed": 0.25,
          "state_action_coverage_fraction": 1.0,
          "state_action_pairs_seen": [
            [
              "safe1",
              "forward"
            ],
            [
              "safe2",
              "forward"
            ],
            [
              "start",
              "risky"
            ],
            [
              "start",
              "safe"
            ]
          ],
          "state_coverage_fraction": 1.0,
          "states_seen": [
            "goal",
            "safe1",
            "safe2",
            "start",
            "trap"
          ],
          "transition_counts": {
            "safe1|forward|safe2": 4,
            "safe2|forward|goal": 4,
            "start|risky|goal": 2,
            "start|risky|trap": 6,
            "start|safe|safe1": 4
          },
          "true_risky_success_prob": 0.25
        },
        "mdp": "risky_safe_optimal",
        "methods": {
          "mc_plus_trl_log": {
            "calibration_error": 0.0,
            "chose_exact_optimal_action": true,
            "eval_goal": "goal",
            "eval_greedy_action": "safe",
            "eval_start": "start",
            "eval_start_exact_q": {
              "risky": 0.225,
              "safe": 0.7290000000000001
            },
            "eval_start_exact_value": 0.7290000000000001,
            "eval_start_learned_q": {
              "risky": 0.225,
              "safe": 0.7290000000000001
            },
            "eval_start_learned_value": 0.7290000000000001,
            "exact_optimal_action": "safe",
            "long_horizon_value_mse": 0.0,
            "max_policy_regret": 0.0,
            "mean_policy_regret": 0.0,
            "policy_regret": 0.0,
            "q_calibration_error": 0.0,
            "q_overestimation_error": 0.0,
            "q_underestimation_error": 0.0,
            "risky_action_selection_rate": 0.0,
            "value_mse": 0.0,
            "value_overestimation_error": 0.0,
            "value_underestimation_error": 0.0
          },
          "mc_supervised": {
            "calibration_error": 0.0,
            "chose_exact_optimal_action": true,
            "eval_goal": "goal",
            "eval_greedy_action": "safe",
            "eval_start": "start",
            "eval_start_exact_q": {
              "risky": 0.225,
              "safe": 0.7290000000000001
            },
            "eval_start_exact_value": 0.7290000000000001,
            "eval_start_learned_q": {
              "risky": 0.225,
              "safe": 0.7290000000000001
            },
            "eval_start_learned_value": 0.7290000000000001,
            "exact_optimal_action": "safe",
            "long_horizon_value_mse": 0.0,
            "max_policy_regret": 0.0,
            "mean_policy_regret": 0.0,
            "policy_regret": 0.0,
            "q_calibration_error": 0.0,
            "q_overestimation_error": 0.0,
            "q_underestimation_error": 0.0,
            "risky_action_selection_rate": 0.0,
            "value_mse": 0.0,
            "value_overestimation_error": 0.0,
            "value_underestimation_error": 0.0
          },
          "trl_log": {
            "calibration_error": 0.0,
            "chose_exact_optimal_action": true,
            "eval_goal": "goal",
            "eval_greedy_action": "safe",
            "eval_start": "start",
            "eval_start_exact_q": {
              "risky": 0.225,
              "safe": 0.7290000000000001
            },
            "eval_start_exact_value": 0.7290000000000001,
            "eval_start_learned_q": {
              "risky": 0.225,
              "safe": 0.7290000000000001
            },
            "eval_start_learned_value": 0.7290000000000001,
            "exact_optimal_action": "safe",
            "long_horizon_value_mse": 0.0,
            "max_policy_regret": 0.0,
            "mean_policy_regret": 0.0,
            "policy_regret": 0.0,
            "q_calibration_error": 0.0,
            "q_overestimation_error": 0.0,
            "q_underestimation_error": 0.0,
            "risky_action_selection_rate": 0.0,
            "value_mse": 0.0,
            "value_overestimation_error": 0.0,
            "value_underestimation_error": 0.0
          },
          "trl_raw": {
            "calibration_error": 0.05625,
            "chose_exact_optimal_action": false,
            "eval_goal": "goal",
            "eval_greedy_action": "risky",
            "eval_start": "start",
            "eval_start_exact_q": {
              "risky": 0.225,
              "safe": 0.7290000000000001
            },
            "eval_start_exact_value": 0.7290000000000001,
            "eval_start_learned_q": {
              "risky": 0.9,
              "safe": 0.7290000000000001
            },
            "eval_start_learned_value": 0.9,
            "exact_optimal_action": "safe",
            "long_horizon_value_mse": 0.01996649999999999,
            "max_policy_regret": 0.5040000000000001,
            "mean_policy_regret": 0.07200000000000002,
            "policy_regret": 0.5040000000000001,
            "q_calibration_error": 0.05625,
            "q_overestimation_error": 0.675,
            "q_underestimation_error": 0.0,
            "risky_action_selection_rate": 1.0,
            "value_mse": 0.0031946399999999986,
            "value_overestimation_error": 0.22499999999999998,
            "value_underestimation_error": 0.0
          }
        },
        "regime": "matched",
        "setting": "safe_optimal"
      },
      "safe_optimal__no_risky_success": {
        "coverage_diagnostics": {
          "action_counts": {
            "forward": 8,
            "risky": 8,
            "safe": 4
          },
          "future_goal_coverage_fraction": 0.8,
          "future_goals_seen": [
            "goal",
            "safe1",
            "safe2",
            "trap"
          ],
          "mdp": "risky_safe_optimal",
          "num_episodes": 12,
          "num_transitions": 20,
          "outcome_counts": {
            "risky_failure": 8,
            "safe_goal": 4,
            "safe_step": 8
          },
          "regime": "no_risky_success",
          "risky_failure_count": 8,
          "risky_success_count": 0,
          "risky_success_rate_observed": 0.0,
          "state_action_coverage_fraction": 1.0,
          "state_action_pairs_seen": [
            [
              "safe1",
              "forward"
            ],
            [
              "safe2",
              "forward"
            ],
            [
              "start",
              "risky"
            ],
            [
              "start",
              "safe"
            ]
          ],
          "state_coverage_fraction": 1.0,
          "states_seen": [
            "goal",
            "safe1",
            "safe2",
            "start",
            "trap"
          ],
          "transition_counts": {
            "safe1|forward|safe2": 4,
            "safe2|forward|goal": 4,
            "start|risky|trap": 8,
            "start|safe|safe1": 4
          },
          "true_risky_success_prob": 0.25
        },
        "mdp": "risky_safe_optimal",
        "methods": {
          "mc_plus_trl_log": {
            "calibration_error": 0.028125000000000004,
            "chose_exact_optimal_action": true,
            "eval_goal": "goal",
            "eval_greedy_action": "safe",
            "eval_start": "start",
            "eval_start_exact_q": {
              "risky": 0.225,
              "safe": 0.7290000000000001
            },
            "eval_start_exact_value": 0.7290000000000001,
            "eval_start_learned_q": {
              "risky": 0.0,
              "safe": 0.7290000000000001
            },
            "eval_start_learned_value": 0.7290000000000001,
            "exact_optimal_action": "safe",
            "long_horizon_value_mse": 0.01265625000000001,
            "max_policy_regret": 0.0,
            "mean_policy_regret": 0.0,
            "policy_regret": 0.0,
            "q_calibration_error": 0.028125000000000004,
            "q_overestimation_error": 0.2250000000000001,
            "q_underestimation_error": 0.225,
            "risky_action_selection_rate": 0.0,
            "value_mse": 0.0020250000000000016,
            "value_overestimation_error": 0.2250000000000001,
            "value_underestimation_error": 0.0
          },
          "mc_supervised": {
            "calibration_error": 0.028125000000000004,
            "chose_exact_optimal_action": true,
            "eval_goal": "goal",
            "eval_greedy_action": "safe",
            "eval_start": "start",
            "eval_start_exact_q": {
              "risky": 0.225,
              "safe": 0.7290000000000001
            },
            "eval_start_exact_value": 0.7290000000000001,
            "eval_start_learned_q": {
              "risky": 0.0,
              "safe": 0.7290000000000001
            },
            "eval_start_learned_value": 0.7290000000000001,
            "exact_optimal_action": "safe",
            "long_horizon_value_mse": 0.01265625000000001,
            "max_policy_regret": 0.0,
            "mean_policy_regret": 0.0,
            "policy_regret": 0.0,
            "q_calibration_error": 0.028125000000000004,
            "q_overestimation_error": 0.2250000000000001,
            "q_underestimation_error": 0.225,
            "risky_action_selection_rate": 0.0,
            "value_mse": 0.0020250000000000016,
            "value_overestimation_error": 0.2250000000000001,
            "value_underestimation_error": 0.0
          },
          "trl_log": {
            "calibration_error": 0.028124999999999997,
            "chose_exact_optimal_action": true,
            "eval_goal": "goal",
            "eval_greedy_action": "safe",
            "eval_start": "start",
            "eval_start_exact_q": {
              "risky": 0.225,
              "safe": 0.7290000000000001
            },
            "eval_start_exact_value": 0.7290000000000001,
            "eval_start_learned_q": {
              "risky": 0.0,
              "safe": 0.7290000000000001
            },
            "eval_start_learned_value": 0.7290000000000001,
            "exact_optimal_action": "safe",
            "long_horizon_value_mse": 0.012656249999999997,
            "max_policy_regret": 0.0,
            "mean_policy_regret": 0.0,
            "policy_regret": 0.0,
            "q_calibration_error": 0.028124999999999997,
            "q_overestimation_error": 0.22499999999999998,
            "q_underestimation_error": 0.225,
            "risky_action_selection_rate": 0.0,
            "value_mse": 0.0020249999999999995,
            "value_overestimation_error": 0.22499999999999998,
            "value_underestimation_error": 0.0
          },
          "trl_raw": {
            "calibration_error": 0.028124999999999997,
            "chose_exact_optimal_action": true,
            "eval_goal": "goal",
            "eval_greedy_action": "safe",
            "eval_start": "start",
            "eval_start_exact_q": {
              "risky": 0.225,
              "safe": 0.7290000000000001
            },
            "eval_start_exact_value": 0.7290000000000001,
            "eval_start_learned_q": {
              "risky": 0.0,
              "safe": 0.7290000000000001
            },
            "eval_start_learned_value": 0.7290000000000001,
            "exact_optimal_action": "safe",
            "long_horizon_value_mse": 0.012656249999999997,
            "max_policy_regret": 0.0,
            "mean_policy_regret": 0.0,
            "policy_regret": 0.0,
            "q_calibration_error": 0.028124999999999997,
            "q_overestimation_error": 0.22499999999999998,
            "q_underestimation_error": 0.225,
            "risky_action_selection_rate": 0.0,
            "value_mse": 0.0020249999999999995,
            "value_overestimation_error": 0.22499999999999998,
            "value_underestimation_error": 0.0
          }
        },
        "regime": "no_risky_success",
        "setting": "safe_optimal"
      },
      "safe_optimal__unlucky_biased": {
        "coverage_diagnostics": {
          "action_counts": {
            "forward": 8,
            "risky": 8,
            "safe": 4
          },
          "future_goal_coverage_fraction": 0.8,
          "future_goals_seen": [
            "goal",
            "safe1",
            "safe2",
            "trap"
          ],
          "mdp": "risky_safe_optimal",
          "num_episodes": 12,
          "num_transitions": 20,
          "outcome_counts": {
            "risky_failure": 7,
            "risky_success": 1,
            "safe_goal": 4,
            "safe_step": 8
          },
          "regime": "unlucky_biased",
          "risky_failure_count": 7,
          "risky_success_count": 1,
          "risky_success_rate_observed": 0.125,
          "state_action_coverage_fraction": 1.0,
          "state_action_pairs_seen": [
            [
              "safe1",
              "forward"
            ],
            [
              "safe2",
              "forward"
            ],
            [
              "start",
              "risky"
            ],
            [
              "start",
              "safe"
            ]
          ],
          "state_coverage_fraction": 1.0,
          "states_seen": [
            "goal",
            "safe1",
            "safe2",
            "start",
            "trap"
          ],
          "transition_counts": {
            "safe1|forward|safe2": 4,
            "safe2|forward|goal": 4,
            "start|risky|goal": 1,
            "start|risky|trap": 7,
            "start|safe|safe1": 4
          },
          "true_risky_success_prob": 0.25
        },
        "mdp": "risky_safe_optimal",
        "methods": {
          "mc_plus_trl_log": {
            "calibration_error": 0.014062500000000002,
            "chose_exact_optimal_action": true,
            "eval_goal": "goal",
            "eval_greedy_action": "safe",
            "eval_start": "start",
            "eval_start_exact_q": {
              "risky": 0.225,
              "safe": 0.7290000000000001
            },
            "eval_start_exact_value": 0.7290000000000001,
            "eval_start_learned_q": {
              "risky": 0.11250000000000002,
              "safe": 0.7290000000000001
            },
            "eval_start_learned_value": 0.7290000000000001,
            "exact_optimal_action": "safe",
            "long_horizon_value_mse": 0.0031640625000000024,
            "max_policy_regret": 0.0,
            "mean_policy_regret": 0.0,
            "policy_regret": 0.0,
            "q_calibration_error": 0.014062500000000002,
            "q_overestimation_error": 0.11250000000000004,
            "q_underestimation_error": 0.11249999999999999,
            "risky_action_selection_rate": 0.0,
            "value_mse": 0.0005062500000000004,
            "value_overestimation_error": 0.11250000000000004,
            "value_underestimation_error": 0.0
          },
          "mc_supervised": {
            "calibration_error": 0.014062500000000002,
            "chose_exact_optimal_action": true,
            "eval_goal": "goal",
            "eval_greedy_action": "safe",
            "eval_start": "start",
            "eval_start_exact_q": {
              "risky": 0.225,
              "safe": 0.7290000000000001
            },
            "eval_start_exact_value": 0.7290000000000001,
            "eval_start_learned_q": {
              "risky": 0.1125,
              "safe": 0.7290000000000001
            },
            "eval_start_learned_value": 0.7290000000000001,
            "exact_optimal_action": "safe",
            "long_horizon_value_mse": 0.0031640625000000024,
            "max_policy_regret": 0.0,
            "mean_policy_regret": 0.0,
            "policy_regret": 0.0,
            "q_calibration_error": 0.014062500000000002,
            "q_overestimation_error": 0.11250000000000004,
            "q_underestimation_error": 0.1125,
            "risky_action_selection_rate": 0.0,
            "value_mse": 0.0005062500000000004,
            "value_overestimation_error": 0.11250000000000004,
            "value_underestimation_error": 0.0
          },
          "trl_log": {
            "calibration_error": 0.014062499999999995,
            "chose_exact_optimal_action": true,
            "eval_goal": "goal",
            "eval_greedy_action": "safe",
            "eval_start": "start",
            "eval_start_exact_q": {
              "risky": 0.225,
              "safe": 0.7290000000000001
            },
            "eval_start_exact_value": 0.7290000000000001,
            "eval_start_learned_q": {
              "risky": 0.11250000000000002,
              "safe": 0.7290000000000001
            },
            "eval_start_learned_value": 0.7290000000000001,
            "exact_optimal_action": "safe",
            "long_horizon_value_mse": 0.0031640624999999963,
            "max_policy_regret": 0.0,
            "mean_policy_regret": 0.0,
            "policy_regret": 0.0,
            "q_calibration_error": 0.014062499999999995,
            "q_overestimation_error": 0.11249999999999993,
            "q_underestimation_error": 0.11249999999999999,
            "risky_action_selection_rate": 0.0,
            "value_mse": 0.0005062499999999994,
            "value_overestimation_error": 0.11249999999999993,
            "value_underestimation_error": 0.0
          },
          "trl_raw": {
            "calibration_error": 0.05625,
            "chose_exact_optimal_action": false,
            "eval_goal": "goal",
            "eval_greedy_action": "risky",
            "eval_start": "start",
            "eval_start_exact_q": {
              "risky": 0.225,
              "safe": 0.7290000000000001
            },
            "eval_start_exact_value": 0.7290000000000001,
            "eval_start_learned_q": {
              "risky": 0.9,
              "safe": 0.7290000000000001
            },
            "eval_start_learned_value": 0.9,
            "exact_optimal_action": "safe",
            "long_horizon_value_mse": 0.01996649999999999,
            "max_policy_regret": 0.5040000000000001,
            "mean_policy_regret": 0.07200000000000002,
            "policy_regret": 0.5040000000000001,
            "q_calibration_error": 0.05625,
            "q_overestimation_error": 0.675,
            "q_underestimation_error": 0.0,
            "risky_action_selection_rate": 1.0,
            "value_mse": 0.0031946399999999986,
            "value_overestimation_error": 0.22499999999999998,
            "value_underestimation_error": 0.0
          }
        },
        "regime": "unlucky_biased",
        "setting": "safe_optimal"
      }
    },
    "success_checks": {
      "all_predeclared_risky_regimes_present": true,
      "chain_log_recovers_discounted_reachability": true,
      "chain_raw_recovers_discounted_reachability": true,
      "raw_policy_is_support_driven": true,
      "success_criteria_met": true,
      "trl_log_is_optimal_on_matched_regimes": true
    },
    "update_steps": 32
  },
  "next_questions": [
    "How much stochastic branch coverage is needed before empirical log backups choose the right action with high probability?",
    "Can uncertainty-aware backups avoid both lucky-only overestimation and no-success conservative underestimation?",
    "Does the same support-driven raw TRL failure appear with sampled goals and function approximation?"
  ],
  "status": "completed"
}
```


## Latest summary

# Experiment 0002 Summary

## Objective

Stress-test stochastic shortcut coverage with exact DP evaluation, including safe-optimal and risk-optimal risky-shortcut MDPs.

## Commands Run

```bash
mkdir -p research/sto_trl/artifacts/0002 research/sto_trl/results && cp research/sto_trl/artifacts/0001/run_tabular_sto_trl.py research/sto_trl/artifacts/0002/run_coverage_stress.py
conda run -n autoresearcher_sto_trl python research/sto_trl/artifacts/0002/run_coverage_stress.py
conda run -n autoresearcher_sto_trl python scripts/validate_artifacts.py --repo-root . --json research/sto_trl/results/0002_result.json --schema schemas/result.schema.json --check-result-artifacts
```

## Setup

- Discount: `0.9`
- Fixed backup iterations: `32`
- Safe episodes per risky regime: `4`
- Risky settings: safe-optimal true success `0.25`; risk-optimal true success `0.90`.
- Regimes per risky setting: `matched, lucky_biased, lucky_only, unlucky_biased, no_risky_success`.

## Aggregate Checks

- Chain raw TRL recovered exact reachability: `True`.
- Chain log TRL recovered exact reachability: `True`.
- All predeclared risky regimes present: `True`.
- Raw policy was support-driven: `True`.
- TRL-log chose the exact optimal action in matched regimes: `True`.

## Per-Regime Metrics

| Scenario | Method | Observed S/F | Exact optimal | Chosen | Regret | Risky Q learned/exact | Safe Q learned/exact |
| --- | --- | ---: | --- | --- | ---: | ---: | ---: |
| safe_optimal__matched | mc_supervised | 2/6 | safe | safe | 0.000000 | 0.225000/0.225000 | 0.729000/0.729000 |
| safe_optimal__matched | trl_raw | 2/6 | safe | risky | 0.504000 | 0.900000/0.225000 | 0.729000/0.729000 |
| safe_optimal__matched | trl_log | 2/6 | safe | safe | 0.000000 | 0.225000/0.225000 | 0.729000/0.729000 |
| safe_optimal__matched | mc_plus_trl_log | 2/6 | safe | safe | 0.000000 | 0.225000/0.225000 | 0.729000/0.729000 |
| safe_optimal__lucky_biased | mc_supervised | 6/2 | safe | safe | 0.000000 | 0.675000/0.225000 | 0.729000/0.729000 |
| safe_optimal__lucky_biased | trl_raw | 6/2 | safe | risky | 0.504000 | 0.900000/0.225000 | 0.729000/0.729000 |
| safe_optimal__lucky_biased | trl_log | 6/2 | safe | safe | 0.000000 | 0.675000/0.225000 | 0.729000/0.729000 |
| safe_optimal__lucky_biased | mc_plus_trl_log | 6/2 | safe | safe | 0.000000 | 0.675000/0.225000 | 0.729000/0.729000 |
| safe_optimal__lucky_only | mc_supervised | 4/0 | safe | risky | 0.504000 | 0.900000/0.225000 | 0.729000/0.729000 |
| safe_optimal__lucky_only | trl_raw | 4/0 | safe | risky | 0.504000 | 0.900000/0.225000 | 0.729000/0.729000 |
| safe_optimal__lucky_only | trl_log | 4/0 | safe | risky | 0.504000 | 0.900000/0.225000 | 0.729000/0.729000 |
| safe_optimal__lucky_only | mc_plus_trl_log | 4/0 | safe | risky | 0.504000 | 0.900000/0.225000 | 0.729000/0.729000 |
| safe_optimal__unlucky_biased | mc_supervised | 1/7 | safe | safe | 0.000000 | 0.112500/0.225000 | 0.729000/0.729000 |
| safe_optimal__unlucky_biased | trl_raw | 1/7 | safe | risky | 0.504000 | 0.900000/0.225000 | 0.729000/0.729000 |
| safe_optimal__unlucky_biased | trl_log | 1/7 | safe | safe | 0.000000 | 0.112500/0.225000 | 0.729000/0.729000 |
| safe_optimal__unlucky_biased | mc_plus_trl_log | 1/7 | safe | safe | 0.000000 | 0.112500/0.225000 | 0.729000/0.729000 |
| safe_optimal__no_risky_success | mc_supervised | 0/8 | safe | safe | 0.000000 | 0.000000/0.225000 | 0.729000/0.729000 |
| safe_optimal__no_risky_success | trl_raw | 0/8 | safe | safe | 0.000000 | 0.000000/0.225000 | 0.729000/0.729000 |
| safe_optimal__no_risky_success | trl_log | 0/8 | safe | safe | 0.000000 | 0.000000/0.225000 | 0.729000/0.729000 |
| safe_optimal__no_risky_success | mc_plus_trl_log | 0/8 | safe | safe | 0.000000 | 0.000000/0.225000 | 0.729000/0.729000 |
| risk_optimal__matched | mc_supervised | 9/1 | risky | risky | 0.000000 | 0.810000/0.810000 | 0.729000/0.729000 |
| risk_optimal__matched | trl_raw | 9/1 | risky | risky | 0.000000 | 0.900000/0.810000 | 0.729000/0.729000 |
| risk_optimal__matched | trl_log | 9/1 | risky | risky | 0.000000 | 0.810000/0.810000 | 0.729000/0.729000 |
| risk_optimal__matched | mc_plus_trl_log | 9/1 | risky | risky | 0.000000 | 0.810000/0.810000 | 0.729000/0.729000 |
| risk_optimal__lucky_biased | mc_supervised | 9/0 | risky | risky | 0.000000 | 0.900000/0.810000 | 0.729000/0.729000 |
| risk_optimal__lucky_biased | trl_raw | 9/0 | risky | risky | 0.000000 | 0.900000/0.810000 | 0.729000/0.729000 |
| risk_optimal__lucky_biased | trl_log | 9/0 | risky | risky | 0.000000 | 0.900000/0.810000 | 0.729000/0.729000 |
| risk_optimal__lucky_biased | mc_plus_trl_log | 9/0 | risky | risky | 0.000000 | 0.900000/0.810000 | 0.729000/0.729000 |
| risk_optimal__lucky_only | mc_supervised | 4/0 | risky | risky | 0.000000 | 0.900000/0.810000 | 0.729000/0.729000 |
| risk_optimal__lucky_only | trl_raw | 4/0 | risky | risky | 0.000000 | 0.900000/0.810000 | 0.729000/0.729000 |
| risk_optimal__lucky_only | trl_log | 4/0 | risky | risky | 0.000000 | 0.900000/0.810000 | 0.729000/0.729000 |
| risk_optimal__lucky_only | mc_plus_trl_log | 4/0 | risky | risky | 0.000000 | 0.900000/0.810000 | 0.729000/0.729000 |
| risk_optimal__unlucky_biased | mc_supervised | 4/4 | risky | safe | 0.081000 | 0.450000/0.810000 | 0.729000/0.729000 |
| risk_optimal__unlucky_biased | trl_raw | 4/4 | risky | risky | 0.000000 | 0.900000/0.810000 | 0.729000/0.729000 |
| risk_optimal__unlucky_biased | trl_log | 4/4 | risky | safe | 0.081000 | 0.450000/0.810000 | 0.729000/0.729000 |
| risk_optimal__unlucky_biased | mc_plus_trl_log | 4/4 | risky | safe | 0.081000 | 0.450000/0.810000 | 0.729000/0.729000 |
| risk_optimal__no_risky_success | mc_supervised | 0/8 | risky | safe | 0.081000 | 0.000000/0.810000 | 0.729000/0.729000 |
| risk_optimal__no_risky_success | trl_raw | 0/8 | risky | safe | 0.081000 | 0.000000/0.810000 | 0.729000/0.729000 |
| risk_optimal__no_risky_success | trl_log | 0/8 | risky | safe | 0.081000 | 0.000000/0.810000 | 0.729000/0.729000 |
| risk_optimal__no_risky_success | mc_plus_trl_log | 0/8 | risky | safe | 0.081000 | 0.000000/0.810000 | 0.729000/0.729000 |

## Outcome

The chain guard still recovered exact discounted reachability for raw and log TRL. Across risky regimes, raw TRL selected risky in every scenario with at least one observed lucky risky transition and did not select risky when no lucky risky transition was observed, confirming the support-driven failure mode. Empirical TRL-log and MC tracked observed frequencies: they were correct in matched regimes, became overoptimistic in safe-optimal lucky-biased/lucky-only regimes, and became too conservative in risk-optimal unlucky/no-success regimes. The risk-optimal setting therefore exposes that calibration gains are coverage-dependent, not simply safe-action conservatism.

## Artifacts

- `research/sto_trl/artifacts/0002/run_coverage_stress.py`
- `research/sto_trl/artifacts/0002/raw_metrics.json`
- `research/sto_trl/artifacts/0002/metrics.csv`
- `research/sto_trl/artifacts/0002/coverage_diagnostics.json`
- `research/sto_trl/artifacts/0002/dataset_specs.json`
- `research/sto_trl/artifacts/0002/offline_datasets.json`
- `research/sto_trl/artifacts/0002/transition_tables.json`
- `research/sto_trl/artifacts/0002/value_tables.json`

## Known Failures

- None.


## Latest review JSON

```json
{
  "allows_auto_continue": true,
  "evidence_checked": [
    "research/sto_trl/results/0002_result.json",
    "research/sto_trl/results/0002_summary.md",
    "research/sto_trl/artifacts/0002/run_coverage_stress.py",
    "research/sto_trl/artifacts/0002/raw_metrics.json",
    "research/sto_trl/artifacts/0002/metrics.csv",
    "research/sto_trl/artifacts/0002/coverage_diagnostics.json",
    "research/sto_trl/artifacts/0002/dataset_specs.json",
    "research/sto_trl/artifacts/0002/offline_datasets.json",
    "research/sto_trl/artifacts/0002/transition_tables.json",
    "research/sto_trl/artifacts/0002/value_tables.json",
    "research/sto_trl/env_state.json",
    "schemas/review.schema.json",
    "python scripts/validate_artifacts.py --repo-root . --json research/sto_trl/results/0002_result.json --schema schemas/result.schema.json --check-result-artifacts",
    "git status --short"
  ],
  "experiment_id": "0002",
  "reasons": [
    "Required outputs are present: research/sto_trl/results/0002_result.json, research/sto_trl/results/0002_summary.md, and populated artifacts under research/sto_trl/artifacts/0002.",
    "Result JSON validates against schemas/result.schema.json with artifact existence checks.",
    "The script implements exact discounted-reachability DP for evaluation and uses constructed offline trajectories for training; the training methods inspected use empirical trajectory counts or returns, not true transition probabilities or DP labels.",
    "The comparison is fair for this diagnostic: mc_supervised, trl_raw, trl_log, and mc_plus_trl_log are run on the same per-scenario offline datasets with the same gamma and fixed update count.",
    "The experiment includes the deterministic chain guard plus both safe-optimal and risk-optimal risky-shortcut settings across matched, lucky_biased, lucky_only, unlucky_biased, and no_risky_success regimes.",
    "Raw metrics are not limited to prose or aggregates: metrics.csv and raw_metrics.json include per-scenario, per-method value errors, Q calibration, policy regret, risky action selection, learned/exact Q values, and coverage diagnostics.",
    "The interpretation is appropriately bounded: it reports raw TRL support-driven overestimation and explicitly notes that MC/log calibration is coverage-dependent and can become overoptimistic or conservative."
  ],
  "required_fixes": [],
  "risk_flags": [
    "The Q overestimation and underestimation maxima are computed across all goals, not only the eval goal, so those headline error fields can reflect non-eval goals such as trap; eval-goal learned/exact Q columns mitigate this.",
    "commands_run records setup, execution, and validation commands but not the manual edits that transformed the copied 0001 script into the 0002 harness.",
    "git status only showed an untracked reviewer packet, but without committed baselines this review cannot fully prove no prior artifacts were modified."
  ],
  "verdict": "pass"
}
```


## Last decisions

## 0001_decision.json

```json
{
  "confidence": 0.89,
  "decision": "continue",
  "evidence": [
    "research/sto_trl/state.json reports iteration 0, status active, and no prior primary metric.",
    "research/sto_trl/env_state.json reports status ready for conda environment autoresearcher_sto_trl with JAX GPU probe completed.",
    "The charter explicitly scopes early work to tabular experiments and requires exact DP ground truth, deterministic chain sanity, risky shortcut MDP, offline data, and MC/TRL baselines.",
    "No result JSON exists yet, which is allowed by the first-iteration rule."
  ],
  "next_experiment": {
    "estimated_runtime_minutes": 20,
    "experiment_id": "0001",
    "failure_criteria": [
      "No exact DP ground truth is implemented for the stochastic diagnostic.",
      "The deterministic chain does not recover shortest-path or discounted-reachability structure for raw/log variants.",
      "The result only reports training loss or prose without raw value and policy metrics.",
      "The risky-shortcut dataset lacks coverage of lucky and unlucky stochastic outcomes.",
      "The run requires large downloads, OGBench, AntMaze, neural-network training, or exceeds the 30 minute executor budget."
    ],
    "hypothesis": "A small tabular risky-shortcut MDP with offline lucky/unlucky outcomes will reveal whether raw deterministic-style TRL overestimates risky stochastic paths, while log-space or MC+TRL-log variants preserve deterministic behavior and improve calibration relative to MC-only or raw TRL.",
    "objective": "Build and run a minimal tabular diagnostic for stochastic TRL covering deterministic chain sanity and one risky-shortcut stochastic MDP, with exact discounted-reachability DP ground truth and raw metrics saved.",
    "required_outputs": [
      "research/sto_trl/artifacts/0001/tabular_sto_trl_prototype.py or equivalent self-contained source",
      "research/sto_trl/artifacts/0001/raw_metrics.json or raw_metrics.csv",
      "research/sto_trl/artifacts/0001/coverage_diagnostics.json",
      "research/sto_trl/results/0001_result.json",
      "research/sto_trl/results/0001_summary.md"
    ],
    "success_criteria": [
      "Creates a reproducible prototype under research/sto_trl/artifacts/0001/ without modifying repository control scripts or schemas.",
      "Produces exact DP ground truth for the deterministic chain and risky-shortcut MDP.",
      "Compares MC supervised, TRL-raw, TRL-log, and MC+TRL-log on the same tiny offline datasets.",
      "Saves raw numeric metrics including overestimation error, underestimation error, long-horizon value MSE, policy regret, risky action selection rate, calibration error, and coverage diagnostics.",
      "Writes valid research/sto_trl/results/0001_result.json and research/sto_trl/results/0001_summary.md with exact commands run."
    ],
    "tasks_for_codex": [
      "Create a small self-contained tabular prototype in research/sto_trl/artifacts/0001/.",
      "Implement deterministic chain and one risky-shortcut versus safe-route stochastic MDP with exact transition tables.",
      "Implement exact discounted reachability DP and greedy policy evaluation from the DP values.",
      "Generate tiny offline trajectories with explicit coverage diagnostics for states, actions, goals, and risky success/failure outcomes.",
      "Implement MC supervised, TRL-raw product backup, TRL-log additive backup, and MC+TRL-log using simple tabular tables and fixed small update counts.",
      "Run the experiment in conda environment autoresearcher_sto_trl with deterministic seeds and save raw metrics as JSON or CSV under research/sto_trl/artifacts/0001/.",
      "Write research/sto_trl/results/0001_result.json matching schemas/result.schema.json and research/sto_trl/results/0001_summary.md, including exact commands run."
    ]
  },
  "progress_score": 1,
  "rationale": "This is project start: iteration is 0, no latest result is expected, the environment is ready, and the charter gives a specific, cheap first experiment. The next step should be one small tabular harness that tests deterministic sanity and a risky-shortcut stochastic diagnostic against exact DP ground truth.",
  "risks": [
    "A first harness can appear to make progress while only testing training loss; require exact DP value and policy calibration metrics.",
    "TRL-raw, TRL-log, and MC+TRL-log may be implemented inconsistently unless the result saves raw per-method metrics and coverage diagnostics.",
    "The risky shortcut can be under-specified; include both lucky and unlucky stochastic outcomes in offline coverage and evaluate risky action selection under exact DP.",
    "Avoid expanding to neural networks, OGBench, or long sweeps before the tabular diagnostic is reproducible."
  ]
}
```

## 0002_decision.json

```json
{
  "confidence": 0.86,
  "decision": "continue",
  "evidence": [
    "Artifact validation for research/sto_trl/results/0001_result.json completed successfully against schemas/result.schema.json with artifact checks.",
    "The 0001 result reports deterministic-chain sanity passed for trl_raw and trl_log with zero value error and zero policy regret.",
    "On risky_shortcut, trl_raw learned risky Q=0.9 versus exact risky Q=0.225, selected risky, and incurred policy_regret=0.504.",
    "On the same risky_shortcut dataset, trl_log, mc_supervised, and mc_plus_trl_log were perfect because the offline risky outcomes exactly matched the true 2/8 success rate.",
    "The 0001 code shows train_trl_raw maximizes over observed next states while train_trl_log uses empirical transition counts, making coverage imbalance the obvious next confound to test."
  ],
  "next_experiment": {
    "estimated_runtime_minutes": 20,
    "experiment_id": "0002",
    "failure_criteria": [
      "Training methods use true transition probabilities or exact DP labels beyond evaluation.",
      "The experiment only repeats the matched 2/6 risky outcome setting from 0001.",
      "No risk-optimal configuration is included, making conservatism impossible to diagnose.",
      "The result reports only aggregate prose or training loss instead of raw numeric metrics by method, MDP setting, and coverage regime.",
      "The run expands to neural networks, OGBench, large sweeps, downloads, or runtime over 30 minutes."
    ],
    "hypothesis": "Raw TRL overestimation is support-driven and will select risky whenever a lucky risky transition is observed, while empirical TRL-log and MC variants will be calibrated only when observed risky success/failure frequencies approximate the true stochastic branch; adding a risk-optimal setting will detect whether apparent improvements are merely conservative avoidance.",
    "objective": "Run a small tabular coverage-sensitivity stress test for the risky shortcut diagnostic, including both risk-suboptimal and risk-optimal settings, to check whether raw TRL overestimation and log/MC calibration claims survive biased or sparse stochastic outcome coverage.",
    "required_outputs": [
      "research/sto_trl/artifacts/0002/run_tabular_coverage_stress.py",
      "research/sto_trl/artifacts/0002/raw_metrics.json",
      "research/sto_trl/artifacts/0002/metrics.csv",
      "research/sto_trl/artifacts/0002/dataset_specs.json",
      "research/sto_trl/results/0002_result.json",
      "research/sto_trl/results/0002_summary.md"
    ],
    "success_criteria": [
      "Reuses or copies the 0001 tabular harness into research/sto_trl/artifacts/0002/ without editing prior results or control scripts.",
      "Evaluates exact DP ground truth for deterministic chain plus two risky-shortcut configurations: one where safe is optimal and one where risky is optimal.",
      "Runs a tiny predeclared set of offline risky coverage regimes, such as matched, lucky-biased, lucky-only, unlucky-biased, and no-risky-success, with fixed deterministic seeds or explicit constructed counts.",
      "Compares the same methods as 0001: mc_supervised, trl_raw, trl_log, and mc_plus_trl_log, using exact DP only for evaluation.",
      "Saves raw per-regime metrics including overestimation error, underestimation error, long-horizon value MSE, policy regret, risky action selection rate, calibration error, and coverage diagnostics.",
      "Produces valid research/sto_trl/results/0002_result.json and research/sto_trl/results/0002_summary.md with exact commands run."
    ],
    "tasks_for_codex": [
      "Create research/sto_trl/artifacts/0002/ and a self-contained coverage stress script, preferably by adapting the 0001 prototype.",
      "Keep the deterministic chain sanity check as a regression guard.",
      "Define two risky-shortcut MDP configurations with exact DP: safe-optimal and risky-optimal.",
      "Construct a tiny set of offline datasets with explicit risky success/failure counts for each coverage regime and save their specifications.",
      "Run mc_supervised, trl_raw, trl_log, and mc_plus_trl_log on each MDP/configuration/regime combination.",
      "Write raw_metrics.json, metrics.csv, coverage_diagnostics.json or equivalent structured artifacts under research/sto_trl/artifacts/0002/.",
      "Validate research/sto_trl/results/0002_result.json against schemas/result.schema.json with artifact checks."
    ]
  },
  "progress_score": 3,
  "rationale": "Experiment 0001 is valid and tests the main early hypothesis, but it is still a matched-coverage toy case: the risky dataset used 2 successes and 6 failures, exactly matching the true 0.25 risky success probability. The next high-information step is a small tabular coverage-sensitivity stress test to determine whether the raw-TRL failure is robust and whether empirical log/MC methods only look good when observed stochastic outcomes match ground truth.",
  "risks": [
    "A larger sweep could become activity without insight; keep the grid tiny and predeclared.",
    "Empirical log-space backups may fail under lucky-only or biased coverage, which would be a useful boundary rather than a reason to hide the result.",
    "Do not introduce oracle access to true transition probabilities in training methods; exact DP should remain evaluation-only ground truth.",
    "A method that avoids all risky actions is not enough; the next test must include a configuration where the risky action is truly optimal."
  ]
}
```


## Stop, pivot, continue rules

- For iteration 0, a missing latest result is expected and is not by itself a reason to stop.
- After iteration 0, stop or choose needs_human on missing or invalid result files.
- Stop on repeated invalid, negative, or low-value results.
- Pivot only when evidence weakens the original idea but reveals a nearby testable idea.
- Continue only for one cheap, high-information experiment.
- Choose needs_human for ambiguity, expensive work, missing artifacts, or risky pivots.


## Next experiment id

Use `0003` as the exact `next_experiment.experiment_id` if you choose continue.
