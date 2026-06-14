# Reviewer Context: reward_to_gcrl

## Latest plan

# Experiment 0002

## Objective

Run a CPU-only tabular CliffWalking equivalence diagnostic comparing ordinary normalized-reward Q-learning to the terminal-only soft successor g_plus learner.

## Hypothesis

On Gymnasium CliffWalking-v0 dynamics with a predeclared normalized reward, the terminal-only soft successor learner with target (1 - gamma) * r_bar + gamma * max_a M(s_next,a,g_plus) will match ordinary normalized-reward Q-learning after scaling M_plus by 1/(1 - gamma), and their greedy policies will have near-zero disagreement.

## Success criteria

- Creates research/reward_to_gcrl/results/0002_result.json and research/reward_to_gcrl/results/0002_summary.md.
- Creates reproducible artifacts under research/reward_to_gcrl/artifacts/0002/.
- Uses only tabular CPU methods on CliffWalking-v0; no neural models, vector state-goal learner, RiverSwim, FourRooms, large datasets, or GPU-dependent work.
- Predeclares and saves the reward normalization, gamma values, alpha schedule, epsilon schedule, seeds, episode budget, terminal-mask behavior, and exact commands run.
- Reports exact-DP oracle metrics for the declared normalized reward, including max_abs(M_plus/(1-gamma) - Q_norm) and greedy policy disagreement rate.
- Reports paired-learning metrics over 10 seeds for gamma in {0.95, 0.99}, including final scaled value error, policy disagreement, average normalized return, original CliffWalking return, success rate, and any terminal-mask diagnostics.
- Passes if exact-DP scaled value error is <= 1e-6, exact-DP policy disagreement is 0 or explained only by value ties, and paired-learning final scaled value error/policy disagreement are within predeclared tolerances.

## Failure criteria

- Missing, invalid, or schema-incompatible result JSON or summary markdown.
- Reward normalization, terminal masks, or CliffWalking transition semantics are ambiguous or omitted.
- The result reports only training loss or returns and omits scaled value error and policy disagreement.
- The soft learner fails to match normalized Q-learning in exact DP or paired tabular learning beyond predeclared tolerance.
- The experiment includes sampled augmented baselines, auxiliary state goals, neural approximation, large environments, or expensive training before this equivalence gate passes.
- Commands are hard-coded inaccurately or raw metrics/artifact paths are missing.

## Estimated runtime

<= 20 minutes

## Tasks for Codex

- Implement a standalone diagnostic script under research/reward_to_gcrl/artifacts/0002/ for Gymnasium CliffWalking-v0 using numpy/gymnasium only.
- Build an exact transition model from the environment and solve both Q_norm_star and F_gplus_star by value iteration with terminal bootstraps masked.
- Implement paired online tabular updates for ordinary Q-learning and terminal-only soft M_plus using identical sampled transitions for 10 seeds and gamma values 0.95 and 0.99.
- Save raw per-seed and per-gamma metrics, DP oracle tables or summary arrays, and metadata under research/reward_to_gcrl/artifacts/0002/.
- Validate research/reward_to_gcrl/results/0002_result.json against schemas/result.schema.json and validate declared artifact paths.
- Write a concise summary that separates equivalence evidence from any original-CliffWalking return or success-rate observations.

## Required outputs

- `research/reward_to_gcrl/results/0002_result.json`
- `research/reward_to_gcrl/results/0002_summary.md`
- `research/reward_to_gcrl/artifacts/0002/`


## Latest plan JSON

```json
{
  "estimated_runtime_minutes": 20,
  "experiment_id": "0002",
  "failure_criteria": [
    "Missing, invalid, or schema-incompatible result JSON or summary markdown.",
    "Reward normalization, terminal masks, or CliffWalking transition semantics are ambiguous or omitted.",
    "The result reports only training loss or returns and omits scaled value error and policy disagreement.",
    "The soft learner fails to match normalized Q-learning in exact DP or paired tabular learning beyond predeclared tolerance.",
    "The experiment includes sampled augmented baselines, auxiliary state goals, neural approximation, large environments, or expensive training before this equivalence gate passes.",
    "Commands are hard-coded inaccurately or raw metrics/artifact paths are missing."
  ],
  "hypothesis": "On Gymnasium CliffWalking-v0 dynamics with a predeclared normalized reward, the terminal-only soft successor learner with target (1 - gamma) * r_bar + gamma * max_a M(s_next,a,g_plus) will match ordinary normalized-reward Q-learning after scaling M_plus by 1/(1 - gamma), and their greedy policies will have near-zero disagreement.",
  "objective": "Run a CPU-only tabular CliffWalking equivalence diagnostic comparing ordinary normalized-reward Q-learning to the terminal-only soft successor g_plus learner.",
  "required_outputs": [
    "research/reward_to_gcrl/results/0002_result.json",
    "research/reward_to_gcrl/results/0002_summary.md",
    "research/reward_to_gcrl/artifacts/0002/"
  ],
  "success_criteria": [
    "Creates research/reward_to_gcrl/results/0002_result.json and research/reward_to_gcrl/results/0002_summary.md.",
    "Creates reproducible artifacts under research/reward_to_gcrl/artifacts/0002/.",
    "Uses only tabular CPU methods on CliffWalking-v0; no neural models, vector state-goal learner, RiverSwim, FourRooms, large datasets, or GPU-dependent work.",
    "Predeclares and saves the reward normalization, gamma values, alpha schedule, epsilon schedule, seeds, episode budget, terminal-mask behavior, and exact commands run.",
    "Reports exact-DP oracle metrics for the declared normalized reward, including max_abs(M_plus/(1-gamma) - Q_norm) and greedy policy disagreement rate.",
    "Reports paired-learning metrics over 10 seeds for gamma in {0.95, 0.99}, including final scaled value error, policy disagreement, average normalized return, original CliffWalking return, success rate, and any terminal-mask diagnostics.",
    "Passes if exact-DP scaled value error is <= 1e-6, exact-DP policy disagreement is 0 or explained only by value ties, and paired-learning final scaled value error/policy disagreement are within predeclared tolerances."
  ],
  "tasks_for_codex": [
    "Implement a standalone diagnostic script under research/reward_to_gcrl/artifacts/0002/ for Gymnasium CliffWalking-v0 using numpy/gymnasium only.",
    "Build an exact transition model from the environment and solve both Q_norm_star and F_gplus_star by value iteration with terminal bootstraps masked.",
    "Implement paired online tabular updates for ordinary Q-learning and terminal-only soft M_plus using identical sampled transitions for 10 seeds and gamma values 0.95 and 0.99.",
    "Save raw per-seed and per-gamma metrics, DP oracle tables or summary arrays, and metadata under research/reward_to_gcrl/artifacts/0002/.",
    "Validate research/reward_to_gcrl/results/0002_result.json against schemas/result.schema.json and validate declared artifact paths.",
    "Write a concise summary that separates equivalence evidence from any original-CliffWalking return or success-rate observations."
  ]
}
```


## Latest result summary

```json
{
  "_source": "/home/eston/autoresearcher/research/reward_to_gcrl/results/0002_result.json",
  "artifacts": [
    "research/reward_to_gcrl/artifacts/0002/check_cliffwalking_v0_compatibility.py",
    "research/reward_to_gcrl/artifacts/0002/compatibility_check.json",
    "research/reward_to_gcrl/artifacts/0002/progress.jsonl"
  ],
  "baseline_metrics": {},
  "claim_tested": "CPU-only tabular CliffWalking-v0 equivalence between ordinary normalized-reward Q-learning and terminal-only soft successor g_plus learning.",
  "experiment_id": "0002",
  "interpretation": "Experiment 0002 did not run the DP or paired-learning phases. The compatibility check failed because Gymnasium rejected CliffWalking-v0 in this environment (Environment version v0 for `CliffWalking` is deprecated. Please use `CliffWalking-v1` instead.). Since the plan specifically requires CliffWalking-v0, using CliffWalking-v1 or a direct class fallback would change the supplied plan.",
  "known_failures": [
    "gym.make('CliffWalking-v0') failed in the ready project environment.",
    "No exact-DP oracle metrics or paired-learning metrics were produced because the compatibility gate failed before the experiment could run as written."
  ],
  "metrics": {
    "compatibility_status": "failed",
    "dp_oracle_metrics_available": false,
    "gym_make_cliffwalking_v0": {
      "exception_module": "gymnasium.error",
      "exception_type": "DeprecatedEnv",
      "message": "Environment version v0 for `CliffWalking` is deprecated. Please use `CliffWalking-v1` instead.",
      "status": "failed",
      "traceback": "Traceback (most recent call last):\n  File \"/home/eston/autoresearcher/research/reward_to_gcrl/artifacts/0002/check_cliffwalking_v0_compatibility.py\", line 69, in check_cliffwalking_v0\n    env = gym.make(\"CliffWalking-v0\")\n          ^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/eston/anaconda3/envs/autoresearcher_reward_to_gcrl/lib/python3.11/site-packages/gymnasium/envs/registration.py\", line 682, in make\n    env_spec = _find_spec(id)\n               ^^^^^^^^^^^^^^\n  File \"/home/eston/anaconda3/envs/... [trimmed]"
    },
    "gymnasium_version": "1.3.0",
    "paired_learning_metrics_available": false,
    "plan_can_run_as_written": false,
    "planned_alpha_schedule": "constant alpha=0.5 for both paired learners",
    "planned_episode_budget": 5000,
    "planned_epsilon_schedule": "epsilon starts at 0.2 and linearly decays to 0.02 over the episode budget",
    "planned_gamma_values": [
      0.95,
      0.99
    ],
    "planned_seeds": {
      "_type": "list",
      "first_items": [
        0,
        1,
        2
      ],
      "length": 10
    },
    "predeclared_tolerances": {
      "exact_dp_policy_disagreement_rate": 0.0,
      "exact_dp_scaled_value_error": 1e-06,
      "paired_policy_disagreement_rate": 0.0,
      "paired_scaled_value_error_between_learners": 1e-10
    },
    "reason_experiment_not_run": "The installed Gymnasium raises an exception for gym.make('CliffWalking-v0'). The plan explicitly requires CliffWalking-v0, and the executor rule says to write a failed or blocked result immediately when compatibility checks show the plan cannot run as written.",
    "registry_cliffwalking_ids": [
      "CliffWalking-v1",
      "CliffWalkingSlippery-v1",
      "tabular/CliffWalking-v0"
    ],
    "requested_env_id": "CliffWalking-v0",
    "reward_normalization_predeclared_for_unrun_plan": {
      "mapped_values": {
        "_type": "object",
        "key_count": 2,
        "keys": [
          "cliff_-100",
          "step_or_goal_-1"
        ]
      },
      "normalization_formula": "r_bar = (original_reward + 100) / 99",
      "note": "Saved for audit only; no experiment was run because v0 could not be instantiated.",
      "original_reward_range": "CliffWalking rewards are -100 for cliff and -1 otherwise."
    },
    "terminal_mask_behavior_predeclared_for_unrun_plan": "Bootstrap would be set to 0.0 whenever Gymnasium returns terminated=True; truncated would not occur in the transition-table DP."
  },
  "next_questions": [
    "Should the next plan explicitly permit Gymnasium CliffWalking-v1 or direct CliffWalkingEnv(is_slippery=False) as equivalent semantics?",
    "Should JAX be added only if the tabular/CliffWalking-v0 registry alias is required by a future plan?"
  ],
  "status": "failed"
}
```


## Latest summary

# Experiment 0002 Summary

## Compatibility Gate

Status: `failed`.

The supplied plan requires `gym.make("CliffWalking-v0")`. In the ready project environment, Gymnasium `1.3.0` rejected that environment id with `DeprecatedEnv`:

```text
Environment version v0 for `CliffWalking` is deprecated. Please use `CliffWalking-v1` instead.
```

Per the executor rule for compatibility failures, the DP and paired-learning phases were not run and no fallback to `CliffWalking-v1` or `CliffWalkingEnv(is_slippery=False)` was used.

## Commands Run

```bash
mkdir -p research/reward_to_gcrl/artifacts/0002 research/reward_to_gcrl/results
conda run -n autoresearcher_reward_to_gcrl python research/reward_to_gcrl/artifacts/0002/check_cliffwalking_v0_compatibility.py
conda run -n autoresearcher_reward_to_gcrl python -m jsonschema -i research/reward_to_gcrl/results/0002_result.json schemas/result.schema.json
conda run -n autoresearcher_reward_to_gcrl python scripts/validate_artifacts.py --repo-root . --json research/reward_to_gcrl/results/0002_result.json --schema schemas/result.schema.json --check-result-artifacts
```

## Planned But Not Run

- Reward normalization: `r_bar = (original_reward + 100) / 99`, mapping cliff `-100` to `0.0` and step/goal `-1` to `1.0`.
- Terminal mask: bootstrap would be zero when `terminated=True`.
- Gamma values: `[0.95, 0.99]`.
- Seeds: `[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]`.
- Episode budget: `5000`.

## Outcome

This is a failed compatibility result, not evidence against the soft successor equivalence hypothesis. The next plan should explicitly allow `CliffWalking-v1` or the direct non-slippery `CliffWalkingEnv` class if those semantics are acceptable.

## Artifacts

- `research/reward_to_gcrl/artifacts/0002/check_cliffwalking_v0_compatibility.py`
- `research/reward_to_gcrl/artifacts/0002/compatibility_check.json`
- `research/reward_to_gcrl/artifacts/0002/progress.jsonl`


## Full evidence paths

- `research/reward_to_gcrl/results/0002_result.json`
- `research/reward_to_gcrl/results/0002_summary.md`

Inspect the full result JSON only when the compact summary and artifact list are insufficient.


## Artifact paths

- `/home/eston/autoresearcher/research/reward_to_gcrl/artifacts/0001`
- `/home/eston/autoresearcher/research/reward_to_gcrl/artifacts/0002`


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
    },
    "evidence_quality": {
      "type": "string",
      "enum": ["strong", "medium", "weak", "invalid"]
    },
    "success_criteria_satisfied": {
      "type": "boolean"
    },
    "failure_criteria_triggered": {
      "type": "boolean"
    },
    "should_escalate_to_pro": {
      "type": "boolean"
    },
    "escalation_reason": {
      "type": ["string", "null"]
    }
  },
  "required": [
    "experiment_id",
    "verdict",
    "allows_auto_continue",
    "reasons",
    "evidence_checked",
    "required_fixes",
    "risk_flags",
    "evidence_quality",
    "success_criteria_satisfied",
    "failure_criteria_triggered",
    "should_escalate_to_pro",
    "escalation_reason"
  ],
  "additionalProperties": false
}
```
