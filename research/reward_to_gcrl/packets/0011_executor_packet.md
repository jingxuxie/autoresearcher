# Executor Context: reward_to_gcrl

## Current experiment plan

# Experiment 0011

## Objective

Produce a compact evidence-synthesis report that separates the positive soft-terminal estimator result from the negative low-rank auxiliary-goal result, and defines what evidence would be required before reopening auxiliary-goal experiments.

## Hypothesis

The current evidence is strong enough for a scoped report with two claims: soft terminal marginalization is a reliable small-tabular variance-reduction/equivalence mechanism under adequate coverage, while real-state auxiliary goals are unsupported for the tested low-rank shared FourRooms architecture. No additional learning run is justified until this evidence is consolidated and reviewed.

## Success criteria

- Summarize 0001-0010 in a claim-by-claim evidence table separating accepted positive evidence, accepted negative evidence, limitations, and unsupported claims.
- State the strongest defensible positive claim: soft terminal marginalization removes terminal-sampling variance and preserves normalized-Q scaling in small tabular settings, with RiverSwim learning advantages only under adequate coverage.
- State the strongest defensible negative claim: low-rank shared real-state auxiliary training did not help g_plus in FourRooms and remained harmful after the predeclared repair diagnostic.
- Include a red-line section listing claims that must not be made yet, including neural auxiliary benefit, larger-environment generality, online exploration robustness, and publishable auxiliary-goal improvement.
- Include a minimal reopening criterion for the auxiliary thread, such as a new human-approved hypothesis that changes architecture or loss normalization in a principled way rather than sweeping hyperparameters.
- Require no new learning runs, no neural frameworks, no GPU, no large environments, and no broad hyperparameter sweeps.
- Output a clear recommendation: pause_lowrank_auxiliary_thread and either write_negative_result or design_new_hypothesis_before_more_compute.

## Failure criteria

- The report mixes estimator evidence and auxiliary-goal evidence into one overbroad positive story.
- The report treats 0009 or 0010 as evidence that auxiliary goals are generally impossible rather than unsupported for the tested low-rank setup.
- The report proposes larger sweeps, PyTorch/JAX, GPU, or neural experiments without a new falsifiable hypothesis.
- The report omits coverage caveats from RiverSwim or matched-stream caveats from earlier estimator tests.
- The report omits the fact that 0009 and 0010 used uniform state-action reset replay and a single rank-4 configuration.
- The report fails to produce a concrete next-decision recommendation.

## Estimated runtime

<= 20 minutes

## Tasks for Codex

- Create research/reward_to_gcrl/reports/0011_evidence_synthesis.md.
- Extract key metrics from results 0001 through 0010 and organize them into positive estimator evidence, negative auxiliary evidence, and limitations.
- Create a claim-status table with labels supported, partially_supported, unsupported, or contradicted.
- Write a conservative abstract-style summary of the project so far.
- Write a red-line section listing claims not supported by the evidence.
- Write a future-work gate specifying what new hypothesis would justify reopening auxiliary-goal experiments.
- Create research/reward_to_gcrl/results/0011_result.json recording that no new learning compute was run, listing inspected files, and giving the final recommendation.
- Create research/reward_to_gcrl/results/0011_summary.md with the decision recommendation and links to the synthesis report.

## Required outputs

- `research/reward_to_gcrl/results/0011_result.json`
- `research/reward_to_gcrl/results/0011_summary.md`
- `research/reward_to_gcrl/artifacts/0011/`


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

- `research/reward_to_gcrl/results/0011_result.json`
- `research/reward_to_gcrl/results/0011_summary.md`
- `research/reward_to_gcrl/artifacts/0011/`


## Timeout and environment warning

The orchestrator enforces the configured timeout externally. Run experiment commands inside the project conda environment, normally with `conda run -n <env> ...`. Keep the experiment small and write a failed result JSON if the plan is impossible.


## Existing code pointers

This starter repository has no project code yet. Create only the tiny files needed under the experiment artifact directory unless the plan explicitly asks for repo code changes.
