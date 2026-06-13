# Executor Context: sto_trl

## Current experiment plan

# Experiment 0003

## Objective

Run a small tabular horizon-holdout experiment that censors long-horizon goal labels during training and tests whether TRL-log or MC+TRL-log can recover long-horizon discounted reachability better than MC-only while retaining matched stochastic risky-branch calibration.

## Hypothesis

With only short-horizon MC labels, MC-supervised estimates will underpredict held-out long-horizon goals, while log-space transitive backups, especially MC+TRL-log, will propagate calibrated short-horizon information to longer horizons without raw TRL's stochastic risky-path optimism under matched branch coverage.

## Success criteria

- Creates a self-contained prototype under research/sto_trl/artifacts/0003/ without editing prior experiment artifacts, schemas, AGENTS.md, or scripts/autoresearcher.py.
- Includes a deterministic chain longer than 0001 plus at least one matched-coverage risky-shortcut MDP with exact DP ground truth.
- Explicitly censors MC/calibration training labels beyond a small horizon cutoff, such as 2 or 3 steps, and saves train/eval state-action-goal pair coverage by horizon bin.
- Compares mc_supervised, trl_raw, trl_log, and mc_plus_trl_log using the same trajectories and the same censored label budget.
- Reports raw metrics by method and horizon bin, including held-out long-horizon value MSE, overestimation, underestimation, calibration error, policy regret, risky action selection rate, and coverage diagnostics.
- Counts the experiment as positive only if trl_log or mc_plus_trl_log improves held-out long-horizon value MSE versus MC-only while raw/log deterministic chain sanity remains valid and matched risky calibration does not select the wrong risky action.
- Produces valid research/sto_trl/results/0003_result.json and research/sto_trl/results/0003_summary.md with exact commands run.

## Failure criteria

- Long-horizon labels are accidentally used in MC supervised targets or calibration anchors.
- The experiment lacks exact DP ground truth for every evaluated MDP.
- The result reports aggregate metrics without horizon-bin breakdown or train/eval coverage diagnostics.
- TRL-log or MC+TRL-log fails the deterministic chain sanity check under the censored-label setup.
- The stochastic risky evaluation uses biased coverage only, making calibration failures ambiguous rather than controlled.
- The run expands to neural networks, OGBench, large sweeps, downloads, or exceeds 30 minutes.

## Estimated runtime

<= 20 minutes

## Tasks for Codex

- Create research/sto_trl/artifacts/0003/ and adapt the 0002 harness into a horizon-holdout script.
- Implement a longer deterministic chain and a matched-coverage risky-shortcut scenario with exact discounted-reachability DP evaluation.
- Add a predeclared horizon cutoff for training labels, while still allowing transitive/log backups to use observed short transitions from trajectories.
- Run mc_supervised, trl_raw, trl_log, and mc_plus_trl_log on the censored-label datasets with fixed update counts and deterministic seeds or constructed trajectories.
- Save raw_metrics.json, metrics.csv, label_coverage_by_horizon.json, offline_datasets.json, transition_tables.json, and value_tables.json under research/sto_trl/artifacts/0003/.
- Write research/sto_trl/results/0003_result.json and research/sto_trl/results/0003_summary.md, then validate the result JSON against schemas/result.schema.json with artifact checks.

## Required outputs

- `research/sto_trl/results/0003_result.json`
- `research/sto_trl/results/0003_summary.md`
- `research/sto_trl/artifacts/0003/`


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

- `research/sto_trl/results/0003_result.json`
- `research/sto_trl/results/0003_summary.md`
- `research/sto_trl/artifacts/0003/`


## Timeout and environment warning

The orchestrator enforces the configured timeout externally. Run experiment commands inside the project conda environment, normally with `conda run -n <env> ...`. Keep the experiment small and write a failed result JSON if the plan is impossible.


## Existing code pointers

This starter repository has no project code yet. Create only the tiny files needed under the experiment artifact directory unless the plan explicitly asks for repo code changes.
