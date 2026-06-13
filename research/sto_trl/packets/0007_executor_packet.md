# Executor Context: sto_trl

## Current experiment plan

# Experiment 0007

## Objective

Test whether a generic tabular posterior or bootstrap branch-uncertainty penalty can replace the hand-shaped one-sided shortcut rule from 0006 while reducing biased lucky-only risky overestimation and preserving deterministic and matched risk-optimal behavior.

## Hypothesis

A branch-uncertainty penalty computed only from offline outcome counts, such as a Dirichlet/Beta posterior lower-confidence estimate or small bootstrap variance penalty, will reduce safe-optimal lucky-only overestimation versus trl_log without relying on direct-goal shortcut eligibility, while preserving chain recovery and selecting risky in the matched risk-optimal scenario. If it fails risk_optimal_no_success, that should be classified as evidence that missing-success regimes need explicit priors rather than stronger TRL relaxation.

## Success criteria

- Creates a self-contained artifact under research/sto_trl/artifacts/0007/ without editing prior results, schemas, AGENTS.md, scripts/autoresearcher.py, or environment files.
- Uses the same exact-DP tabular scenarios as 0006: chain_len9_holdout, safe_optimal_matched, risk_optimal_matched, safe_optimal_lucky_only_stress, and risk_optimal_no_success_stress.
- Implements at least one generic uncertainty method that uses only offline transition/outcome counts and does not special-case direct-goal shortcut actions.
- Runs a tiny predeclared grid, such as two priors or bootstrap settings and two penalty strengths, plus the zero-penalty baseline, all on fixed trajectories and update count.
- Compares mc_supervised, trl_raw, trl_log, mc_plus_trl_log, the best 0006 one-sided conservative rows, and the new generic uncertainty variants on the same datasets.
- Reports exact DP metrics by scenario and method, including held-out long-horizon value MSE, Q/value overestimation and underestimation, calibration error, policy regret, risky action selection rate, and coverage/outcome diagnostics.
- Counts positive evidence only if a generic uncertainty variant reduces safe_optimal_lucky_only Q overestimation or policy regret versus trl_log, preserves deterministic chain held-out MSE near zero, and selects risky with zero regret in risk_optimal_matched.
- Explicitly reports whether risk_optimal_no_success_stress remains unsolved; do not treat fixing safe_optimal_lucky_only by blanket risk avoidance as success.
- Produces valid research/sto_trl/results/0007_result.json and research/sto_trl/results/0007_summary.md with exact commands run.

## Failure criteria

- The uncertainty penalty uses exact DP values, true transition probabilities, or oracle knowledge of unobserved outcomes.
- The new method is only the 0006 hand-shaped direct-goal shortcut rule with renamed parameters.
- The result omits the full predeclared grid or reports only the best setting.
- The method reduces safe-optimal lucky-only regret only by selecting safe in risk_optimal_matched or increasing matched policy regret.
- Exact DP ground truth, raw metrics, commands run, or coverage diagnostics are missing.
- The run expands to neural networks, OGBench, PointMaze, AntMaze, large downloads, broad sweeps, or exceeds 30 minutes.

## Estimated runtime

<= 25 minutes

## Tasks for Codex

- Create research/sto_trl/artifacts/0007/ and adapt the 0006 harness into a generic uncertainty audit script.
- Implement a count-based posterior or bootstrap branch-uncertainty estimator that operates on observed next-outcome counts for state-action pairs and saves its diagnostics.
- Run the fixed 0006 tabular scenarios with the predeclared small grid and the same update_steps and label_horizon_cutoff.
- Compute direct comparisons versus trl_log and versus the 0006 one-sided conservative variants, including policy/regret and Q overestimation deltas for the two biased stress cases.
- Save raw_metrics.json, metrics.csv, uncertainty_grid.json, uncertainty_diagnostics.json, offline_datasets.json, transition_tables.json, and value_tables.json under research/sto_trl/artifacts/0007/.
- Write research/sto_trl/results/0007_result.json and research/sto_trl/results/0007_summary.md, then validate the result JSON with scripts/validate_artifacts.py and artifact checks.

## Required outputs

- `research/sto_trl/results/0007_result.json`
- `research/sto_trl/results/0007_summary.md`
- `research/sto_trl/artifacts/0007/`


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

- `research/sto_trl/results/0007_result.json`
- `research/sto_trl/results/0007_summary.md`
- `research/sto_trl/artifacts/0007/`


## Timeout and environment warning

The orchestrator enforces the configured timeout externally. Run experiment commands inside the project conda environment, normally with `conda run -n <env> ...`. Keep the experiment small and write a failed result JSON if the plan is impossible.


## Existing code pointers

This starter repository has no project code yet. Create only the tiny files needed under the experiment artifact directory unless the plan explicitly asks for repo code changes.
