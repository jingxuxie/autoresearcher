# Executor Context: reward_to_gcrl

## Current experiment plan

# Experiment 0012

## Objective

Package the current evidence into a concise research memo or draft note, and define a formal gate for any future auxiliary-goal experiments. No new learning compute should be run.

## Hypothesis

The current evidence is mature enough for a scoped negative-and-positive write-up: soft terminal marginalization is a useful small-tabular estimator/equivalence mechanism under adequate coverage, while the tested low-rank real-state auxiliary approach is unsupported. Further progress requires either writing this up or proposing a genuinely new falsifiable auxiliary hypothesis.

## Success criteria

- Produce a concise memo that separates positive estimator evidence, negative auxiliary evidence, limitations, and unsupported claims.
- Include a claim table with labels such as supported, partially_supported, unsupported, contradicted, and not_tested.
- State the strongest defensible estimator claim without implying neural, large-environment, or online-exploration generality.
- State the strongest defensible auxiliary claim as negative evidence limited to the tested rank-4 NumPy low-rank FourRooms setup.
- Include a figure/table plan for a future paper or blog post, using only existing 0001-0011 evidence.
- Define a new-hypothesis gate for reopening auxiliary experiments, requiring a principled architecture or loss-normalization change and predeclared success criteria.
- Recommend one of three next directions after the memo: write_short_paper, design_new_auxiliary_hypothesis, or stop_auxiliary_thread.

## Failure criteria

- The memo proposes new compute before summarizing and reviewing existing evidence.
- The memo claims auxiliary-goal benefit despite 0009 and 0010 negative-transfer evidence.
- The memo presents the low-rank auxiliary failure as a general impossibility result.
- The memo omits RiverSwim coverage caveats or the small-tabular limitation.
- The memo recommends broad sweeps, neural frameworks, GPU use, or larger environments without a new falsifiable hypothesis.
- The memo lacks a concrete go/no-go gate for reopening auxiliary experiments.

## Estimated runtime

<= 20 minutes

## Tasks for Codex

- Create research/reward_to_gcrl/reports/0012_writeup_outline.md.
- Create a claim-status table covering 0001 through 0011.
- Extract the key numeric evidence for the estimator claim, including variance removal, scaling equivalence, RiverSwim adequate-coverage behavior, and FourRooms vector SSM sanity checks.
- Extract the key numeric evidence for the auxiliary negative result, including 0009 terminal-only versus combined metrics and 0010 repair failure.
- Write a red-line section listing claims not supported by current evidence.
- Write a new-hypothesis gate describing what would justify reopening auxiliary experiments.
- Create research/reward_to_gcrl/results/0012_result.json recording that no new learning compute was run and giving the final recommendation.
- Create research/reward_to_gcrl/results/0012_summary.md with a short decision summary and next-step recommendation.

## Required outputs

- `research/reward_to_gcrl/results/0012_result.json`
- `research/reward_to_gcrl/results/0012_summary.md`
- `research/reward_to_gcrl/artifacts/0012/`


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

- `research/reward_to_gcrl/results/0012_result.json`
- `research/reward_to_gcrl/results/0012_summary.md`
- `research/reward_to_gcrl/artifacts/0012/`


## Timeout and environment warning

The orchestrator enforces the configured timeout externally. Run experiment commands inside the project conda environment, normally with `conda run -n <env> ...`. Keep the experiment small and write a failed result JSON if the plan is impossible.


## Existing code pointers

This starter repository has no project code yet. Create only the tiny files needed under the experiment artifact directory unless the plan explicitly asks for repo code changes.
