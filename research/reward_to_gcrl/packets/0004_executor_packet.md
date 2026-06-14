# Executor Context: reward_to_gcrl

## Current experiment plan

# Experiment 0004

## Objective

Repair the sampled-vs-soft comparison using a small nondegenerate tabular setting where the raw task objective remains meaningful, and directly test whether deterministic soft terminal marginalization improves Bellman residual, value error, and policy quality over sampled augmented updates under matched data.

## Hypothesis

When reward normalization is audited so that the induced normalized objective does not create degenerate all-step rewards, the sampled augmented update remains unbiased but higher variance, while the deterministic soft update should achieve lower Bellman residual and at least non-worse value error and greedy policy quality under the same transition budget.

## Success criteria

- Include an explicit reward audit reporting raw rewards, normalized rewards, affine constants, terminal handling, and whether the normalized objective preserves the raw optimal policy under exact DP.
- Use at least one tiny analytic counterexample or hand-built chain where raw task success is nondegenerate and exact DP has non-tie greedy actions.
- Compute exact DP for raw Q, normalized Q, and soft g_plus, and report whether normalized Q and raw Q have the same greedy policy on non-terminal non-tie states.
- Run matched-stream sampled augmented and deterministic soft updates for gamma in {0.95, 0.99, 0.995} over 10 seeds with CPU-tabular code only.
- Compare sampled targets directly against the deterministic soft target computed from the same learner state and transition, with pass/fail tolerance stated before the run.
- Soft must have lower mean final Bellman residual and lower or statistically indistinguishable mean final value error versus sampled across seeds; otherwise the result should be labeled variance-only, not learning-improvement evidence.
- Evaluation must report raw return, normalized return, success rate, steps to goal, and policy disagreement against exact DP, with tie states separated.

## Failure criteria

- The normalized objective does not preserve the raw optimal policy and the experiment does not explicitly label this as an objective-mismatch result.
- The target comparison again validates sampled targets only against the sampled learner's own conditional expectation rather than the deterministic soft target from the same state.
- Exact DP has mostly tie states, making policy disagreement uninformative.
- Raw task success remains zero or uninformative for all learned policies.
- Soft has worse mean final value error and no compensating Bellman-residual or policy-quality advantage.
- The run adds neural networks, auxiliary goals, large environments, GPU dependence, or expensive hyperparameter sweeps.

## Estimated runtime

<= 25 minutes

## Tasks for Codex

- Create research/reward_to_gcrl/artifacts/0004/run_repaired_sampled_vs_soft.py using CPU-only tabular code.
- Implement a small nondegenerate chain or gridworld with audited raw rewards, normalized rewards, terminal states, and exact transition table.
- Optionally include a repaired CliffWalking variant only if exact DP confirms the normalized objective has meaningful non-tie policies and nonzero success incentives.
- Compute exact DP references for raw Q, normalized Q, and soft g_plus, including policy preservation checks.
- Run matched-stream sampled augmented and deterministic soft learners with synchronized initialization, alpha, epsilon schedule, transition budget, gamma values, and seeds.
- For every sampled update, record the deterministic soft target from the same learner state and transition so sampled-vs-soft target mean and variance are directly comparable.
- Save raw metrics, target diagnostics, Bellman residuals, value errors, policy disagreement, evaluation returns, and pass/fail flags to research/reward_to_gcrl/results/0004_result.json.
- Write research/reward_to_gcrl/results/0004_summary.md with a conservative verdict: variance-only, learning-improvement, objective-mismatch, or failed diagnostic.

## Required outputs

- `research/reward_to_gcrl/results/0004_result.json`
- `research/reward_to_gcrl/results/0004_summary.md`
- `research/reward_to_gcrl/artifacts/0004/`


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

- `research/reward_to_gcrl/results/0004_result.json`
- `research/reward_to_gcrl/results/0004_summary.md`
- `research/reward_to_gcrl/artifacts/0004/`


## Timeout and environment warning

The orchestrator enforces the configured timeout externally. Run experiment commands inside the project conda environment, normally with `conda run -n <env> ...`. Keep the experiment small and write a failed result JSON if the plan is impossible.


## Existing code pointers

This starter repository has no project code yet. Create only the tiny files needed under the experiment artifact directory unless the plan explicitly asks for repo code changes.
