# Executor Context: sto_trl

## Current experiment plan

# Experiment 0001

## Objective

Build and run a minimal tabular diagnostic for stochastic TRL covering deterministic chain sanity and one risky-shortcut stochastic MDP, with exact discounted-reachability DP ground truth and raw metrics saved.

## Hypothesis

A small tabular risky-shortcut MDP with offline lucky/unlucky outcomes will reveal whether raw deterministic-style TRL overestimates risky stochastic paths, while log-space or MC+TRL-log variants preserve deterministic behavior and improve calibration relative to MC-only or raw TRL.

## Success criteria

- Creates a reproducible prototype under research/sto_trl/artifacts/0001/ without modifying repository control scripts or schemas.
- Produces exact DP ground truth for the deterministic chain and risky-shortcut MDP.
- Compares MC supervised, TRL-raw, TRL-log, and MC+TRL-log on the same tiny offline datasets.
- Saves raw numeric metrics including overestimation error, underestimation error, long-horizon value MSE, policy regret, risky action selection rate, calibration error, and coverage diagnostics.
- Writes valid research/sto_trl/results/0001_result.json and research/sto_trl/results/0001_summary.md with exact commands run.

## Failure criteria

- No exact DP ground truth is implemented for the stochastic diagnostic.
- The deterministic chain does not recover shortest-path or discounted-reachability structure for raw/log variants.
- The result only reports training loss or prose without raw value and policy metrics.
- The risky-shortcut dataset lacks coverage of lucky and unlucky stochastic outcomes.
- The run requires large downloads, OGBench, AntMaze, neural-network training, or exceeds the 30 minute executor budget.

## Estimated runtime

<= 20 minutes

## Tasks for Codex

- Create a small self-contained tabular prototype in research/sto_trl/artifacts/0001/.
- Implement deterministic chain and one risky-shortcut versus safe-route stochastic MDP with exact transition tables.
- Implement exact discounted reachability DP and greedy policy evaluation from the DP values.
- Generate tiny offline trajectories with explicit coverage diagnostics for states, actions, goals, and risky success/failure outcomes.
- Implement MC supervised, TRL-raw product backup, TRL-log additive backup, and MC+TRL-log using simple tabular tables and fixed small update counts.
- Run the experiment in conda environment autoresearcher_sto_trl with deterministic seeds and save raw metrics as JSON or CSV under research/sto_trl/artifacts/0001/.
- Write research/sto_trl/results/0001_result.json matching schemas/result.schema.json and research/sto_trl/results/0001_summary.md, including exact commands run.

## Required outputs

- `research/sto_trl/results/0001_result.json`
- `research/sto_trl/results/0001_summary.md`
- `research/sto_trl/artifacts/0001/`


## Environment YAML

```yaml
name: autoresearcher_sto_trl
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


## Environment state

```json
{
  "blocker": null,
  "commands_run": [
    "conda env create -f research/sto_trl/environment.yaml",
    "nvidia-smi -L",
    "conda run -n autoresearcher_sto_trl python scripts/probe_jax_gpu.py --require-gpu --output research/sto_trl/setup_logs/jax_gpu_probe.json",
    "conda run -n autoresearcher_sto_trl python -c \"import sys, yaml, jsonschema, jax; print(sys.version.split()[0]); print(yaml.__version__); print(jsonschema.__version__); print(jax.__version__)\""
  ],
  "conda_env_name": "autoresearcher_sto_trl",
  "conda_env_path": "/home/eston/anaconda3/envs/autoresearcher_sto_trl",
  "environment_file": "research/sto_trl/environment.yaml",
  "gpu_available": true,
  "gpu_checks": [
    "nvidia-smi -L reported GPU 0: NVIDIA GeForce RTX 4090",
    "JAX default_backend reported gpu",
    "JAX devices reported cuda:0",
    "Tiny JAX compute returned 140.0"
  ],
  "gpu_requested": true,
  "packages_verified": [
    "python 3.11.15",
    "pyyaml 6.0.3",
    "jsonschema 4.26.0",
    "jax 0.10.1",
    "jaxlib 0.10.1",
    "jax[cuda12]"
  ],
  "project": "sto_trl",
  "status": "ready",
  "summary": "Conda environment autoresearcher_sto_trl was created from environment.yaml. JAX imports successfully, sees cuda:0, uses gpu as the default backend, and completed a tiny GPU computation."
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

- `research/sto_trl/results/0001_result.json`
- `research/sto_trl/results/0001_summary.md`
- `research/sto_trl/artifacts/0001/`


## Timeout and environment warning

The orchestrator enforces the configured timeout externally. Run experiment commands inside the project conda environment, normally with `conda run -n <env> ...`. Keep the experiment small and write a failed result JSON if the plan is impossible.


## Existing code pointers

This starter repository has no project code yet. Create only the tiny files needed under the experiment artifact directory unless the plan explicitly asks for repo code changes.
