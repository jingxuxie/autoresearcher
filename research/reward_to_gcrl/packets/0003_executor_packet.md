# Executor Context: reward_to_gcrl

## Current experiment plan

# Experiment 0003

## Objective

Compare sampled augmented g_plus learning against the terminal-only soft successor update on the audited local tabular CliffWalking MDP under the same data budget.

## Hypothesis

For the same original transition stream, the sampled augmented g_plus learner is an unbiased but higher-variance estimator of the soft target, so it should observe sparse g_plus events and have higher TD target variance and worse or slower Bellman-error reduction than the deterministic soft update as gamma approaches 1.

## Success criteria

- Creates research/reward_to_gcrl/results/0003_result.json and research/reward_to_gcrl/results/0003_summary.md.
- Creates reproducible artifacts under research/reward_to_gcrl/artifacts/0003/.
- Uses only CPU tabular methods on the already audited local CliffWalking transition semantics; no neural models, auxiliary state goals, RiverSwim, FourRooms, GPU-dependent work, or large dependencies.
- Runs gamma in {0.95, 0.99, 0.995} with at least 10 seeds and a predeclared transition budget small enough to finish within 30 minutes.
- Reports exact commands, reward normalization, terminal/absorbing-state handling, seeds, alpha/epsilon schedules, and transition budget.
- For each gamma and seed, saves sampled g_plus event counts, g_plus events per 10k original transitions, empirical sampled target variance, soft target variance or conditional terminal-sampling variance, Bellman error to the exact soft DP solution, and learning curves at fixed checkpoints.
- Primary hypothesis pass requires sampled and soft target means to agree within a predeclared Monte Carlo tolerance while sampled target variance exceeds soft terminal-sampling variance, and soft reaches lower final Bellman error or reaches a fixed Bellman-error threshold earlier for most gamma/seed settings.

## Failure criteria

- Missing, invalid, or schema-incompatible result JSON or summary markdown.
- Exact commands, raw metrics, artifact paths, reward normalization, or terminal masks are omitted.
- The sampled augmented baseline bootstraps after g_plus/g_minus absorbing terminal events or applies an extra gamma factor to continued sampled targets.
- The experiment reports only returns or training loss and omits target variance, g_plus event counts, and Bellman error to exact DP.
- The result claims soft dominance despite target means not matching within the predeclared tolerance or without raw per-seed metrics.
- The executor adds neural approximation, auxiliary goals, larger environments, large downloads, or expensive training before this sampled-vs-soft tabular gate is complete.

## Estimated runtime

<= 25 minutes

## Tasks for Codex

- Implement a standalone script under research/reward_to_gcrl/artifacts/0003/ that reuses or recreates the audited local CliffWalking transition table from 0002 with a fresh metadata audit.
- Solve the exact soft g_plus DP reference for each gamma under the declared normalized reward.
- Train terminal-only soft M_plus and sampled augmented g_plus learners on matched original transition streams for gamma values 0.95, 0.99, and 0.995 over 10 seeds.
- For the sampled learner, sample g_plus with probability (1 - gamma) * r_bar, g_minus with probability (1 - gamma) * (1 - r_bar), and otherwise continue to s_next with target max_a M(s_next,a), with no extra discount on that continued sampled target.
- Log checkpoint learning curves, TD target statistics, g_plus event counts, Bellman errors, policy diagnostics, raw return, normalized return, success rate, and cliff falls.
- Save raw per-seed metrics plus aggregate metrics under research/reward_to_gcrl/artifacts/0003/.
- Validate the result JSON with schemas/result.schema.json and validate declared artifacts with scripts/validate_artifacts.py.

## Required outputs

- `research/reward_to_gcrl/results/0003_result.json`
- `research/reward_to_gcrl/results/0003_summary.md`
- `research/reward_to_gcrl/artifacts/0003/`


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

- `research/reward_to_gcrl/results/0003_result.json`
- `research/reward_to_gcrl/results/0003_summary.md`
- `research/reward_to_gcrl/artifacts/0003/`


## Timeout and environment warning

The orchestrator enforces the configured timeout externally. Run experiment commands inside the project conda environment, normally with `conda run -n <env> ...`. Keep the experiment small and write a failed result JSON if the plan is impossible.


## Existing code pointers

This starter repository has no project code yet. Create only the tiny files needed under the experiment artifact directory unless the plan explicitly asks for repo code changes.
