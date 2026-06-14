# Executor Context: reward_to_gcrl

## Current experiment plan

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


## Environment YAML

```yaml
name: autoresearcher_reward_to_gcrl
channels:
  - conda-forge
dependencies:
  - python=3.11
  - pip
  - numpy
  - pandas
  - matplotlib
  - pyyaml
  - jsonschema
  - pytest
  - gymnasium
```


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


## Result schema

```json
{
  "type": "object",
  "properties": {
    "experiment_id": { "type": "string" },
    "status": {
      "type": "string",
      "enum": ["completed", "failed", "blocked", "timeout"]
    },
    "claim_tested": { "type": "string" },
    "commands_run": {
      "type": "array",
      "items": { "type": "string" }
    },
    "metrics": {
      "type": "object",
      "additionalProperties": true
    },
    "baseline_metrics": {
      "type": "object",
      "additionalProperties": true
    },
    "artifacts": {
      "type": "array",
      "items": { "type": "string" }
    },
    "interpretation": { "type": "string" },
    "known_failures": {
      "type": "array",
      "items": { "type": "string" }
    },
    "next_questions": {
      "type": "array",
      "items": { "type": "string" }
    },
    "runtime_seconds": {
      "type": ["number", "null"]
    },
    "resource_usage": {
      "type": "object",
      "additionalProperties": true
    },
    "success_criteria_results": {
      "type": "array",
      "items": { "type": "string" }
    },
    "failure_criteria_results": {
      "type": "array",
      "items": { "type": "string" }
    },
    "metric_deltas": {
      "type": "object",
      "additionalProperties": true
    },
    "decision_relevant_findings": {
      "type": "array",
      "items": { "type": "string" }
    }
  },
  "required": [
    "experiment_id",
    "status",
    "claim_tested",
    "commands_run",
    "metrics",
    "baseline_metrics",
    "artifacts",
    "interpretation",
    "known_failures",
    "next_questions"
  ],
  "additionalProperties": false
}
```


## Required output paths

- `research/reward_to_gcrl/results/0002_result.json`
- `research/reward_to_gcrl/results/0002_summary.md`
- `research/reward_to_gcrl/artifacts/0002/`


## Timeout and environment warning

The orchestrator enforces the configured timeout externally. Run experiment commands inside the project conda environment, normally with `conda run -n <env> ...`. Keep the experiment small and write a failed result JSON if the plan is impossible.


## Existing code pointers

This starter repository has no project code yet. Create only the tiny files needed under the experiment artifact directory unless the plan explicitly asks for repo code changes.
