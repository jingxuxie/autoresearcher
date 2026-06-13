# Executor Context: sto_trl

## Current experiment plan

# Experiment 0005

## Objective

Run a small successor-distance lambda and equivalence audit to determine whether successor_distance_trl_log has a distinct effect beyond trl_log and calibration-only on the existing tabular chain and risky-shortcut diagnostics.

## Hypothesis

If the successor-distance formulation is meaningful rather than a relabeling of trl_log, then some predeclared lambda_tr value should change Q/value tables or policy behavior relative to trl_log while retaining lower held-out error than calibration-only and avoiding matched risky-branch overestimation. If all lambda_tr values collapse to trl_log or calibration-only, the successor-distance variant is not yet adding distinct evidence.

## Success criteria

- Creates a self-contained artifact under research/sto_trl/artifacts/0005/ without editing prior results, schemas, AGENTS.md, scripts/autoresearcher.py, or environment files.
- Reuses the exact DP tabular scenarios from 0004: chain_len9_holdout, safe_optimal_matched, risk_optimal_matched, and safe_optimal_lucky_only_stress.
- Sweeps a tiny predeclared set of successor transitive weights, such as lambda_tr in [0.0, 0.25, 0.5, 0.75, 1.0], with fixed trajectories and update count.
- Reports calibration-only, trl_log, mc_plus_trl_log, and successor_distance_trl_log for every lambda on the same datasets.
- Saves explicit equivalence diagnostics versus trl_log, including max_abs_q_diff, max_abs_value_diff, action_diff_rate, heldout_mse_delta, policy_regret_delta, and q_overestimation_delta by scenario and lambda.
- Counts positive successor-distance evidence only if at least one lambda improves versus calibration-only and is not numerically equivalent to trl_log on the main scenarios, without increasing matched risky policy regret or Q overestimation.
- Counts negative evidence explicitly if all successor-distance lambdas are equivalent to trl_log within tolerance or only improve by matching trl_log.
- Produces valid research/sto_trl/results/0005_result.json and research/sto_trl/results/0005_summary.md with exact commands run.

## Failure criteria

- The result compares successor_distance_trl_log only to calibration-only and omits equivalence diagnostics versus trl_log.
- The lambda sweep uses different trajectories, label censoring, or DP setup across methods.
- Exact DP ground truth is missing for any scenario.
- The experiment claims a successor-distance win when metrics are numerically identical to trl_log within the predeclared tolerance.
- The run expands to neural networks, OGBench, large sweeps, downloads, or exceeds 30 minutes.

## Estimated runtime

<= 20 minutes

## Tasks for Codex

- Create research/sto_trl/artifacts/0005/ and adapt the 0004 harness into a lambda/equivalence audit script.
- Parameterize successor_distance_trl_log by lambda_tr and run the predeclared small lambda set on the same constructed datasets.
- Compute and save per-scenario, per-lambda metrics plus direct table-difference diagnostics versus trl_log and calibration-only.
- Save raw_metrics.json, metrics.csv, lambda_sweep.json, equivalence_diagnostics.json, successor_distance_tables.json, distance_diagnostics.json, offline_datasets.json, transition_tables.json, and value_tables.json under research/sto_trl/artifacts/0005/.
- Write research/sto_trl/results/0005_result.json and research/sto_trl/results/0005_summary.md, then validate the result JSON against schemas/result.schema.json with artifact checks.

## Required outputs

- `research/sto_trl/results/0005_result.json`
- `research/sto_trl/results/0005_summary.md`
- `research/sto_trl/artifacts/0005/`


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

- `research/sto_trl/results/0005_result.json`
- `research/sto_trl/results/0005_summary.md`
- `research/sto_trl/artifacts/0005/`


## Timeout and environment warning

The orchestrator enforces the configured timeout externally. Run experiment commands inside the project conda environment, normally with `conda run -n <env> ...`. Keep the experiment small and write a failed result JSON if the plan is impossible.


## Existing code pointers

This starter repository has no project code yet. Create only the tiny files needed under the experiment artifact directory unless the plan explicitly asks for repo code changes.
