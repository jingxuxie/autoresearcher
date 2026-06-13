# Setup Environment Context: project_001

## Requested action

Create or verify the project-specific conda environment, then write `research/<project>/env_state.json`.


## Project charter

# Project 001 Charter

## Research goal

Positive-control smoke project for the autoresearcher loop.

Evaluate whether a tiny, deterministic experiment can detect and report an obvious improvement over a weak baseline. This project is intentionally simple so Phase 1 can validate orchestration, result schemas, reviewer behavior, and stopping rules without expensive compute.

## Main hypothesis

A simple corrected method should outperform a deliberately weak baseline on a small synthetic counting task.

## Primary metric

Accuracy on a deterministic toy dataset.

## Success criteria

- The executor creates a tiny reproducible experiment that runs in under 30 minutes.
- The result JSON reports exact commands run.
- The corrected method accuracy is higher than the baseline accuracy on the same data.
- Raw metrics are saved in `research/project_001/artifacts/NNNN/` when useful.

## Failure criteria

- Missing or invalid result JSON.
- No comparable baseline.
- No exact commands recorded.
- Claims of improvement without raw metrics.
- Any experiment that needs large dependencies, large data, or long training.

## Notes for adapting this project

Replace this charter with your actual research idea when you are ready. Keep the same structure so the supervisor, executor, and reviewer can reason against explicit criteria.



## Environment YAML

```yaml
name: autoresearcher_project_001
channels:
  - conda-forge
dependencies:
  - python=3.11
  - pip
  - pyyaml
  - jsonschema
  - pip:
      - "jax[cuda12]"
```


## Current environment state

```json
{
  "blocker": null,
  "commands_run": [],
  "conda_env_name": "autoresearcher_project_001",
  "conda_env_path": null,
  "environment_file": "research/project_001/environment.yaml",
  "gpu_available": null,
  "gpu_checks": [],
  "gpu_requested": true,
  "packages_verified": [],
  "project": "project_001",
  "status": "pending",
  "summary": "Environment has not been set up yet."
}
```


## Required env state schema

```json
{
  "type": "object",
  "properties": {
    "project": { "type": "string" },
    "status": {
      "type": "string",
      "enum": ["pending", "ready", "blocked", "failed"]
    },
    "conda_env_name": { "type": "string" },
    "conda_env_path": { "type": ["string", "null"] },
    "environment_file": { "type": "string" },
    "commands_run": {
      "type": "array",
      "items": { "type": "string" }
    },
    "packages_verified": {
      "type": "array",
      "items": { "type": "string" }
    },
    "gpu_requested": { "type": "boolean" },
    "gpu_available": { "type": ["boolean", "null"] },
    "gpu_checks": {
      "type": "array",
      "items": { "type": "string" }
    },
    "summary": { "type": "string" },
    "blocker": {
      "type": ["object", "null"],
      "properties": {
        "reason": { "type": "string" },
        "failed_command": { "type": "string" },
        "needs_escalation": { "type": "boolean" },
        "escalation_type": {
          "type": "string",
          "enum": ["network", "gpu", "filesystem", "approval", "unknown"]
        }
      },
      "required": ["reason", "failed_command", "needs_escalation", "escalation_type"],
      "additionalProperties": false
    }
  },
  "required": [
    "project",
    "status",
    "conda_env_name",
    "conda_env_path",
    "environment_file",
    "commands_run",
    "packages_verified",
    "gpu_requested",
    "gpu_available",
    "gpu_checks",
    "summary",
    "blocker"
  ],
  "additionalProperties": false
}
```


## Setup requirements

- Use only this project's conda environment.
- Verify `conda run -n <env> python --version`.
- GPU is preferred when available. Check `nvidia-smi` if possible.
- If conda, network, filesystem, or GPU access is blocked, write `status: "blocked"` with a blocker object and the exact failed command.
- Do not run the research experiment.


## Setup requirements

- Use only this project's conda environment.
- Verify `conda run -n <env> python --version`.
- GPU is preferred when available. Check `nvidia-smi` if possible.
- For JAX/GPU projects, run `conda run -n <env> python scripts/probe_jax_gpu.py --require-gpu --output research/<project>/setup_logs/jax_gpu_probe.json`.
- If conda, network, filesystem, or GPU access is blocked, write `status: "blocked"` with a blocker object and the exact failed command.
- Do not run the research experiment.
