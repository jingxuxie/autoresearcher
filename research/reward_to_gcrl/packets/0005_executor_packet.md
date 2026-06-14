# Executor Context: reward_to_gcrl

## Current experiment plan

# Experiment 0005

## Objective

Run a CPU-only tabular sampled-vs-soft diagnostic on a small stochastic RiverSwim chain to test long-horizon reward propagation under sparse right-end rewards.

## Hypothesis

On a small RiverSwim chain with rewards already normalized to [0,1], sampled augmented g_plus updates are unbiased but higher variance than deterministic soft terminal updates; under matched transition streams, the soft learner should show lower TD target variance, fewer failures from rare g_plus events, and lower Bellman/value error to exact DP at the same data budget, especially as gamma approaches 1.

## Success criteria

- Creates research/reward_to_gcrl/results/0005_result.json and research/reward_to_gcrl/results/0005_summary.md.
- Creates reproducible artifacts under research/reward_to_gcrl/artifacts/0005/.
- Uses only CPU tabular methods on a small RiverSwim chain, with no neural models, auxiliary goals, large datasets, GPU-dependent work, or expensive sweeps.
- Predeclares and saves the RiverSwim transition table, reward normalization, gamma values, seeds, alpha/epsilon or behavior policy, transition budget, terminal/absorbing handling, and exact commands run.
- Solves exact normalized Q and exact soft g_plus DP references for each gamma and reports max_abs(M_plus/(1-gamma) - Q_norm) for the soft fixed point.
- Runs gamma in {0.95, 0.99, 0.995} with at least 10 seeds and a transition budget that completes within 30 minutes.
- For each gamma and seed, saves sampled g_plus event counts per 10000 transitions, target mean error against deterministic soft marginal target, sampled target variance, soft terminal-sampling variance, Bellman residual, value error to exact DP, right-end reward/occupancy diagnostics, and greedy-policy return.
- Primary pass requires sampled target means to match deterministic soft marginal targets within a predeclared Monte Carlo tolerance, sampled target variance to exceed soft terminal-sampling variance, and soft to have lower final Bellman residual or reach a fixed Bellman-error threshold earlier in most runs.

## Failure criteria

- Missing, invalid, or schema-incompatible result JSON or summary markdown.
- Exact commands, raw metrics, artifact paths, transition table, reward normalization, or terminal/absorbing handling are omitted.
- The sampled augmented baseline applies an extra gamma factor to continued sampled targets or bootstraps after sampled g_plus/g_minus absorbing events.
- The result reports only returns or training loss and omits target variance, g_plus event counts, Bellman residual, or value error to exact DP.
- Coverage is too poor to interpret and is not reported with right-end visits/reward-event counts.
- The executor adds auxiliary goals, neural approximation, larger environments, large downloads, or expensive training before this RiverSwim tabular gate is complete.

## Estimated runtime

<= 25 minutes

## Tasks for Codex

- Implement a standalone script under research/reward_to_gcrl/artifacts/0005/ defining a small stochastic RiverSwim transition table, preferably 6 or 10 states, with rewards in [0,1].
- Write an environment audit artifact containing transition probabilities, rewards, action mapping, reward normalization, and a transition-table hash.
- Compute exact DP references for normalized Q and soft g_plus fixed points for each gamma.
- Train terminal-only soft M_plus and sampled augmented g_plus learners on matched original transition streams for gamma values 0.95, 0.99, and 0.995 over at least 10 seeds.
- Use sampled probabilities p_g_plus=(1-gamma)*r_bar, p_g_minus=(1-gamma)*(1-r_bar), p_continue=gamma, with continued sampled target max_a M(s_next,a) and no extra gamma factor.
- Log checkpoint learning curves, TD target statistics, g_plus event counts, Bellman residuals, value errors, visitation coverage, right-end occupancy/reward, greedy-policy return, and policy disagreement versus exact DP.
- Save raw per-seed metrics plus aggregate metrics under research/reward_to_gcrl/artifacts/0005/.
- Validate the result JSON with schemas/result.schema.json and validate declared artifacts with scripts/validate_artifacts.py.

## Required outputs

- `research/reward_to_gcrl/results/0005_result.json`
- `research/reward_to_gcrl/results/0005_summary.md`
- `research/reward_to_gcrl/artifacts/0005/`


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

- `research/reward_to_gcrl/results/0005_result.json`
- `research/reward_to_gcrl/results/0005_summary.md`
- `research/reward_to_gcrl/artifacts/0005/`


## Timeout and environment warning

The orchestrator enforces the configured timeout externally. Run experiment commands inside the project conda environment, normally with `conda run -n <env> ...`. Keep the experiment small and write a failed result JSON if the plan is impossible.


## Existing code pointers

This starter repository has no project code yet. Create only the tiny files needed under the experiment artifact directory unless the plan explicitly asks for repo code changes.
