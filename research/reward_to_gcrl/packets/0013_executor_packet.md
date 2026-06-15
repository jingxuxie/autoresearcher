# Executor Context: reward_to_gcrl

## Current experiment plan

# Experiment 0013

## Objective

Write an internal short-paper draft from existing 0001-0012 reward_to_gcrl evidence only, with a claim-to-evidence map, explicit limitations, unsupported-claims red lines, and a pre-publication review checklist.

## Hypothesis

Existing evidence is sufficient for a scoped internal short-paper draft with two defensible conclusions: soft terminal marginalization is a useful small-tabular variance-reduction and equivalence mechanism under adequate coverage, while the tested rank-4 low-rank FourRooms real-state auxiliary approach is unsupported and showed negative transfer.

## Success criteria

- No new learning compute is run.
- The draft clearly separates estimator claims, vector-SSM correctness claims, and auxiliary-goal negative evidence.
- Every main claim is linked to specific existing iterations from 0001 through 0012.
- The strongest supported positive claim is limited to small audited tabular or CPU NumPy settings, normalized-Q scaling, terminal-sampling variance reduction, and adequate-coverage learning improvements.
- The auxiliary result is stated only as limited negative evidence for the tested rank-4 low-rank FourRooms architecture, optimizer, replay setup, gamma, and repair variants.
- The draft includes limitations covering coverage dependence, matched-stream tests, tiny environments, tabular scope, uniform reset replay, and lack of neural or large-environment evidence.
- The draft includes a red-line section listing unsupported claims: neural auxiliary benefit, broad GCRL success, online exploration robustness, benchmark generality, and general impossibility of auxiliary goals.
- The output includes a review checklist that must pass before external publication or broader claims.

## Failure criteria

- The draft proposes or runs new experiments.
- The draft claims general reward-to-GCRL success beyond audited small-tabular evidence.
- The draft claims auxiliary-goal benefit despite 0009 and 0010 negative-transfer evidence.
- The draft claims auxiliary goals are generally impossible or harmful rather than unsupported for the tested low-rank setup.
- The draft omits RiverSwim coverage caveats or matched-stream limitations.
- The draft omits or minimizes the negative auxiliary evidence.
- The draft is framed as externally publishable without requiring review.

## Estimated runtime

<= 25 minutes

## Tasks for Codex

- Create research/reward_to_gcrl/reports/0013_short_paper_draft.md.
- Use research/reward_to_gcrl/reports/0012_writeup_outline.md and research/reward_to_gcrl/reports/0011_evidence_synthesis.md as the primary scaffolding.
- Create a claim-to-evidence map covering iterations 0001 through 0012.
- Write a concise abstract, introduction, method summary, experimental evidence summary, negative auxiliary result section, limitations, and conclusion.
- Add an unsupported-claims red-line section and a pre-publication review checklist.
- Create research/reward_to_gcrl/results/0013_result.json recording that no new learning compute was run, listing inspected evidence files, and giving the draft status.
- Create research/reward_to_gcrl/results/0013_summary.md with a short decision summary and explicit instruction that the draft requires review before external use.

## Required outputs

- `research/reward_to_gcrl/results/0013_result.json`
- `research/reward_to_gcrl/results/0013_summary.md`
- `research/reward_to_gcrl/artifacts/0013/`


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

- `research/reward_to_gcrl/results/0013_result.json`
- `research/reward_to_gcrl/results/0013_summary.md`
- `research/reward_to_gcrl/artifacts/0013/`


## Timeout and environment warning

The orchestrator enforces the configured timeout externally. Run experiment commands inside the project conda environment, normally with `conda run -n <env> ...`. Keep the experiment small and write a failed result JSON if the plan is impossible.


## Existing code pointers

This starter repository has no project code yet. Create only the tiny files needed under the experiment artifact directory unless the plan explicitly asks for repo code changes.
