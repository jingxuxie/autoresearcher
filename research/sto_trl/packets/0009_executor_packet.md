# Executor Context: sto_trl

## Current experiment plan

# Experiment 0009

## Objective

Run a compact transition-level posterior model-DP baseline audit on representative regimes from the 0008 identifiability grid, establishing what empirical, Bayesian, quantile, and robust transition models can solve before adding transitive/posterior TRL variants.

## Hypothesis

Transition-level uncertainty baselines will explain most recoverable performance in finite-coverage risky-shortcut regimes: posterior mean, posterior quantile, and robust confidence-set DP should improve regret versus raw TRL and empirical TRL-log in prior-dependent or lucky-only cells while preserving matched safe-optimal and matched risk-optimal choices. Any remaining failures should identify where explicit priors or future transitive propagation are necessary.

## Success criteria

- Creates a self-contained artifact under research/sto_trl/artifacts/0009/ without editing prior results, schemas, AGENTS.md, scripts/autoresearcher.py, or environment files.
- Selects a small representative subset from the 0008 grid covering matched-identifiable, lucky-only, no-success, ambiguous, prior-dependent, safe-optimal, and risk-optimal regimes.
- Implements and reports empirical model DP, Bayesian posterior mean DP, posterior lower and upper quantile DP, and robust confidence-set DP, alongside raw TRL, TRL-log, and empirical risky-value baselines.
- Uses exact DP ground truth only for evaluation, not as a training or decision input.
- Reports regime-stratified action accuracy, mean policy regret, risky-action selection rate, Q overestimation, calibration error, and prior-dependence diagnostics.
- Counts positive evidence only if transition-level posterior or robust baselines reduce regret versus TRL-log in prior-dependent or lucky-only regimes while not simply selecting safe everywhere and while preserving matched risk-optimal action choice.
- Explicitly states whether transition uncertainty alone matches or beats the current stochastic TRL variants, setting a baseline for any future transitive/posterior TRL experiment.
- Produces valid research/sto_trl/results/0009_result.json and research/sto_trl/results/0009_summary.md with exact commands run.

## Failure criteria

- The experiment uses exact DP values or true transition probabilities as decision inputs rather than evaluation ground truth.
- The selected subset omits anti-conservatism checks, especially matched risk-optimal and no-success risk-optimal regimes.
- The result reports only aggregate averages and omits regime-stratified metrics.
- The posterior or robust methods are not compared against both empirical transition DP and TRL-log.
- The experiment claims a stochastic TRL win without beating or matching simple transition-model DP baselines.
- The run expands to neural networks, continuous control, OGBench, large downloads, broad sweeps, or exceeds 30 minutes.

## Estimated runtime

<= 25 minutes

## Tasks for Codex

- Create research/sto_trl/artifacts/0009/ and implement a small transition_posterior_baselines.py script, reusing 0008 grid definitions where practical.
- Select and save a representative evaluation subset from 0008 with explicit regime labels and coverage diagnostics.
- Implement empirical model DP, beta-binomial posterior mean DP, posterior lower and upper quantile DP, and a simple robust confidence-set DP for the risky shortcut family.
- Evaluate raw TRL, TRL-log, empirical risky-value, and the transition-posterior baselines against exact DP ground truth on the same subset.
- Save raw_metrics.json, metrics.csv, regime_summary.csv, posterior_diagnostics.json, selected_grid_cells.json, coverage_diagnostics.json, transition_tables.json, and value_tables.json under research/sto_trl/artifacts/0009/.
- Write research/sto_trl/results/0009_result.json and research/sto_trl/results/0009_summary.md, then validate the result JSON with scripts/validate_artifacts.py and artifact checks.

## Required outputs

- `research/sto_trl/results/0009_result.json`
- `research/sto_trl/results/0009_summary.md`
- `research/sto_trl/artifacts/0009/`


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

- `research/sto_trl/results/0009_result.json`
- `research/sto_trl/results/0009_summary.md`
- `research/sto_trl/artifacts/0009/`


## Timeout and environment warning

The orchestrator enforces the configured timeout externally. Run experiment commands inside the project conda environment, normally with `conda run -n <env> ...`. Keep the experiment small and write a failed result JSON if the plan is impossible.


## Existing code pointers

This starter repository has no project code yet. Create only the tiny files needed under the experiment artifact directory unless the plan explicitly asks for repo code changes.
