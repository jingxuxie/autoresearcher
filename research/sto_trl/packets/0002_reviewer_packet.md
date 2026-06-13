# Reviewer Context: sto_trl

## Latest plan

# Experiment 0002

## Objective

Run a small tabular coverage-sensitivity stress test for the risky shortcut diagnostic, including both risk-suboptimal and risk-optimal settings, to check whether raw TRL overestimation and log/MC calibration claims survive biased or sparse stochastic outcome coverage.

## Hypothesis

Raw TRL overestimation is support-driven and will select risky whenever a lucky risky transition is observed, while empirical TRL-log and MC variants will be calibrated only when observed risky success/failure frequencies approximate the true stochastic branch; adding a risk-optimal setting will detect whether apparent improvements are merely conservative avoidance.

## Success criteria

- Reuses or copies the 0001 tabular harness into research/sto_trl/artifacts/0002/ without editing prior results or control scripts.
- Evaluates exact DP ground truth for deterministic chain plus two risky-shortcut configurations: one where safe is optimal and one where risky is optimal.
- Runs a tiny predeclared set of offline risky coverage regimes, such as matched, lucky-biased, lucky-only, unlucky-biased, and no-risky-success, with fixed deterministic seeds or explicit constructed counts.
- Compares the same methods as 0001: mc_supervised, trl_raw, trl_log, and mc_plus_trl_log, using exact DP only for evaluation.
- Saves raw per-regime metrics including overestimation error, underestimation error, long-horizon value MSE, policy regret, risky action selection rate, calibration error, and coverage diagnostics.
- Produces valid research/sto_trl/results/0002_result.json and research/sto_trl/results/0002_summary.md with exact commands run.

## Failure criteria

- Training methods use true transition probabilities or exact DP labels beyond evaluation.
- The experiment only repeats the matched 2/6 risky outcome setting from 0001.
- No risk-optimal configuration is included, making conservatism impossible to diagnose.
- The result reports only aggregate prose or training loss instead of raw numeric metrics by method, MDP setting, and coverage regime.
- The run expands to neural networks, OGBench, large sweeps, downloads, or runtime over 30 minutes.

## Estimated runtime

<= 20 minutes

## Tasks for Codex

- Create research/sto_trl/artifacts/0002/ and a self-contained coverage stress script, preferably by adapting the 0001 prototype.
- Keep the deterministic chain sanity check as a regression guard.
- Define two risky-shortcut MDP configurations with exact DP: safe-optimal and risky-optimal.
- Construct a tiny set of offline datasets with explicit risky success/failure counts for each coverage regime and save their specifications.
- Run mc_supervised, trl_raw, trl_log, and mc_plus_trl_log on each MDP/configuration/regime combination.
- Write raw_metrics.json, metrics.csv, coverage_diagnostics.json or equivalent structured artifacts under research/sto_trl/artifacts/0002/.
- Validate research/sto_trl/results/0002_result.json against schemas/result.schema.json with artifact checks.

## Required outputs

- `research/sto_trl/results/0002_result.json`
- `research/sto_trl/results/0002_summary.md`
- `research/sto_trl/artifacts/0002/`


## Latest plan JSON

```json
{
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
    "research/sto_trl/results/0002_result.json",
    "research/sto_trl/results/0002_summary.md",
    "research/sto_trl/artifacts/0002/"
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


## Artifact paths

- `/home/eston/autoresearcher/research/sto_trl/artifacts/0001`
- `/home/eston/autoresearcher/research/sto_trl/artifacts/0002`


## Review schema

```json
{
  "type": "object",
  "properties": {
    "experiment_id": { "type": "string" },
    "verdict": {
      "type": "string",
      "enum": ["pass", "weak_pass", "fail", "needs_human"]
    },
    "allows_auto_continue": {
      "type": "boolean"
    },
    "reasons": {
      "type": "array",
      "items": { "type": "string" }
    },
    "evidence_checked": {
      "type": "array",
      "items": { "type": "string" }
    },
    "required_fixes": {
      "type": "array",
      "items": { "type": "string" }
    },
    "risk_flags": {
      "type": "array",
      "items": { "type": "string" }
    }
  },
  "required": [
    "experiment_id",
    "verdict",
    "allows_auto_continue",
    "reasons",
    "evidence_checked",
    "required_fixes",
    "risk_flags"
  ],
  "additionalProperties": false
}
```
