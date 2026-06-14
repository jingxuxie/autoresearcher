# Executor Context: reward_to_gcrl

## Current experiment plan

# Experiment 0007

## Objective

Run a CPU-only tabular RiverSwim coverage dose-response experiment that uses several non-oracle behavior policies to create starved, borderline, and adequate coverage regimes, then quantify exactly when deterministic soft terminal marginalization improves Bellman residual, value error, and policy quality over sampled augmented updates.

## Hypothesis

The deterministic soft update should consistently reduce terminal-sampling variance in all coverage regimes, but learning-performance advantages should appear mainly when right-reward and state-action coverage are adequate. In coverage-starved regimes, soft may lower Bellman residual without reliably lowering value error, so coverage should be treated as a prerequisite for learning-superiority claims.

## Success criteria

- Use only CPU tabular code on the same audited 6-state RiverSwim semantics as 0005 and 0006.
- Generate matched logged streams from at least four fixed non-oracle behavior policies, such as uniform random, mild right bias, strong right bias, and alternating or epsilon-cyclic exploration, with no exact-Q action guidance.
- Predeclare coverage bins using right-reward events per 10000 transitions and visited state-action-pair counts, then report results separately for starved, borderline, and adequate coverage.
- For every gamma-behavior-seed run, sampled target means must match deterministic soft marginal targets within predeclared Monte Carlo tolerance, and sampled terminal-sampling variance must exceed soft terminal-sampling variance.
- On adequate-coverage runs, soft must have lower mean final Bellman residual and lower or statistically indistinguishable mean final value error than sampled.
- On starved runs, the summary must explicitly avoid learning-superiority claims and report whether Bellman residual and value error disagree.
- Include a simple coverage-performance regression or stratified table showing how soft-minus-sampled value error changes with right-reward event count and visited state-action coverage.
- The final recommendation must state whether to move next to tabular auxiliary real-state goals or whether more estimator-only RiverSwim work is still needed.

## Failure criteria

- Any behavior policy uses exact DP, exact Q, or reward-optimal action preferences to generate the logged stream.
- The run does not produce both adequate-coverage and coverage-starved regimes, making the coverage caveat unresolved.
- Target means are compared only to the sampled learner's own conditional expectation rather than the deterministic soft marginal target from the same transition and learner state.
- Soft has worse value error than sampled in adequate-coverage runs without a clear explanation.
- The summary makes an unconditional learning-superiority claim despite coverage-starved failures.
- The experiment adds auxiliary goals, neural approximation, larger environments, GPU dependence, or expensive hyperparameter sweeps before this coverage gate is resolved.

## Estimated runtime

<= 25 minutes

## Tasks for Codex

- Create research/reward_to_gcrl/artifacts/0007/run_riverswim_coverage_dose_response.py by extending the 0006 non-oracle RiverSwim script.
- Reuse and verify the same 6-state RiverSwim transition hash, reward normalization, action mapping, and exact DP references from 0005 and 0006.
- Implement at least four fixed non-oracle behavior policies that span expected coverage levels without consulting exact Q or exact DP for action selection.
- Run gamma in {0.95, 0.99, 0.995} over 10 seeds per behavior with a CPU-tabular budget no larger than 0006 unless a smaller pilot shows adequate coverage is impossible.
- Record direct sampled-vs-deterministic-soft target mean error, terminal-sampling variance, g_plus events, right-reward events, visited state-action pairs, Bellman residual, value error, policy disagreement, and greedy raw return.
- Stratify outputs by coverage bin and compute soft-minus-sampled deltas for Bellman residual, value error, and greedy return.
- Save research/reward_to_gcrl/results/0007_result.json with raw metrics, exact commands, behavior definitions, pass/fail flags, and coverage-bin summaries.
- Save research/reward_to_gcrl/results/0007_summary.md with a conservative verdict on whether coverage is sufficiently bounded to proceed to tabular auxiliary state-goal experiments.

## Required outputs

- `research/reward_to_gcrl/results/0007_result.json`
- `research/reward_to_gcrl/results/0007_summary.md`
- `research/reward_to_gcrl/artifacts/0007/`


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

- `research/reward_to_gcrl/results/0007_result.json`
- `research/reward_to_gcrl/results/0007_summary.md`
- `research/reward_to_gcrl/artifacts/0007/`


## Timeout and environment warning

The orchestrator enforces the configured timeout externally. Run experiment commands inside the project conda environment, normally with `conda run -n <env> ...`. Keep the experiment small and write a failed result JSON if the plan is impossible.


## Existing code pointers

This starter repository has no project code yet. Create only the tiny files needed under the experiment artifact directory unless the plan explicitly asks for repo code changes.
