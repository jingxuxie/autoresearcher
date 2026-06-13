# Executor Context: sto_trl

## Current experiment plan

# Experiment 0004

## Objective

Implement and test the first tabular stochastic-calibrated successor-distance variant, comparing calibration-only against successor-distance + TRL-log on the existing horizon-holdout and risky-shortcut diagnostics.

## Hypothesis

A self-normalized successor-distance calibration with a log-space transitive relaxation will improve held-out long-horizon value estimates over calibration-only while preserving matched stochastic branch calibration, reducing raw TRL overestimation, and not simply avoiding risky actions when risk is truly optimal.

## Success criteria

- Creates a self-contained prototype under research/sto_trl/artifacts/0004/ without editing prior results, schemas, AGENTS.md, scripts/autoresearcher.py, or environment files.
- Implements at least two new ablations: successor_calibration_only with lambda_tr=0 and successor_distance_trl_log with a small predeclared transitive weight or equivalent tabular update.
- Evaluates exact DP ground truth on a deterministic chain horizon-holdout scenario, a matched safe-optimal risky shortcut, and a matched risk-optimal risky shortcut.
- Includes one small biased-coverage boundary case, such as safe-optimal lucky-only, but labels it as a stress case rather than the sole success criterion.
- Compares against existing mc_supervised, trl_raw, trl_log, and mc_plus_trl_log on the same constructed datasets.
- Reports raw metrics by scenario and method, including held-out long-horizon value MSE, calibration error, overestimation, underestimation, policy regret, risky action selection rate, triangle violation rate or distance consistency diagnostics, and coverage diagnostics.
- Counts the result as positive only if successor_distance_trl_log improves held-out long-horizon MSE versus successor_calibration_only and does not increase matched risky-branch overestimation or policy regret versus calibration-only.
- Produces valid research/sto_trl/results/0004_result.json and research/sto_trl/results/0004_summary.md with exact commands run.

## Failure criteria

- The successor-distance variant is not separately reported from existing trl_log or mc_plus_trl_log.
- Exact DP ground truth is missing for any evaluated scenario.
- The transitive term improves deterministic long-horizon MSE only by increasing risky-branch overestimation or by choosing safe in the matched risk-optimal scenario.
- The result omits calibration-only versus calibrated+transitive ablation metrics.
- The experiment relies on true transition probabilities, DP labels, neural networks, OGBench, large sweeps, downloads, or runtime over 30 minutes.

## Estimated runtime

<= 25 minutes

## Tasks for Codex

- Create research/sto_trl/artifacts/0004/ and adapt the 0003 harness into a successor-distance ablation script.
- Define the self-normalized successor score and distance tables explicitly in the artifact source and save learned score, distance, value, and Q tables.
- Run the chain horizon-holdout, matched safe-optimal risky shortcut, matched risk-optimal risky shortcut, and one biased safe-optimal boundary case.
- Evaluate mc_supervised, trl_raw, trl_log, mc_plus_trl_log, successor_calibration_only, and successor_distance_trl_log with fixed seeds or constructed trajectories.
- Save raw_metrics.json, metrics.csv, successor_distance_tables.json, distance_diagnostics.json, label_or_pair_coverage.json, offline_datasets.json, transition_tables.json, and value_tables.json under research/sto_trl/artifacts/0004/.
- Write research/sto_trl/results/0004_result.json and research/sto_trl/results/0004_summary.md, then validate the result JSON against schemas/result.schema.json with artifact checks.

## Required outputs

- `research/sto_trl/results/0004_result.json`
- `research/sto_trl/results/0004_summary.md`
- `research/sto_trl/artifacts/0004/`


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

- `research/sto_trl/results/0004_result.json`
- `research/sto_trl/results/0004_summary.md`
- `research/sto_trl/artifacts/0004/`


## Timeout and environment warning

The orchestrator enforces the configured timeout externally. Run experiment commands inside the project conda environment, normally with `conda run -n <env> ...`. Keep the experiment small and write a failed result JSON if the plan is impossible.


## Existing code pointers

This starter repository has no project code yet. Create only the tiny files needed under the experiment artifact directory unless the plan explicitly asks for repo code changes.
