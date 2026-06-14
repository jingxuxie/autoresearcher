# Executor Context: sto_trl

## Current experiment plan

# Experiment 0008

## Objective

Run a small tabular identifiability and coverage grid that maps when risky-shortcut action choice is identifiable from finite offline stochastic coverage, before adding new stochastic TRL algorithms.

## Hypothesis

Across risky-shortcut MDPs, some regimes are identifiable from observed risky successes/failures and simple empirical or posterior transition estimates should match exact DP action choice, while lucky-only and no-success regimes will expose impossibility or prior-dependence. This grid should clarify when log-TRL failures are data-identifiability failures versus algorithmic failures.

## Success criteria

- Creates a self-contained artifact under research/sto_trl/artifacts/0008/ without editing prior results, schemas, AGENTS.md, scripts/autoresearcher.py, or environment files.
- Sweeps a small predeclared grid over true risky success probability, safe route length, risky sample count, and observed risky success count, with exact DP ground truth for every cell.
- Includes at least one deterministic chain guard or equivalent sanity row showing raw/log TRL still recover deterministic long-horizon behavior.
- Compares raw TRL, TRL-log, empirical risky-value or empirical-transition DP, Bayesian posterior mean, posterior lower and upper quantile choices, and simple confidence-bound choices on the same grid cells.
- Reports per-cell action choice, policy regret, risky value overestimation, calibration error, and whether the cell is empirically identifiable, ambiguous, lucky-only, no-success, or prior-dependent.
- Saves coverage diagnostics and raw grid metrics, plus compact heatmap-friendly CSV or JSON tables for regret and action choice.
- Counts the experiment as useful if it identifies regimes where no method can be justified without explicit priors, and regimes where transition-level uncertainty baselines are sufficient or insufficient versus TRL-log.
- Produces valid research/sto_trl/results/0008_result.json and research/sto_trl/results/0008_summary.md with exact commands run.

## Failure criteria

- The grid omits exact DP ground truth or policy regret for any evaluated cell.
- The result reports only aggregate averages and does not save per-cell raw metrics.
- The experiment claims an algorithmic win instead of separating identifiable, ambiguous, and prior-dependent regimes.
- The posterior or confidence baselines use true transition probabilities or exact DP labels as training inputs rather than evaluation ground truth.
- The sweep is too broad, exceeds 30 minutes, or expands to neural networks, continuous control, OGBench, downloads, or large training.
- The result omits commands run, artifacts, coverage diagnostics, or validation against schemas/result.schema.json.

## Estimated runtime

<= 25 minutes

## Tasks for Codex

- Create research/sto_trl/artifacts/0008/ and implement a small standalone identifiability_grid.py or equivalent script, reusing helper code from prior tabular artifacts when useful.
- Define the predeclared grid with a compact set such as true risky success probabilities, safe path lengths, risky sample counts, and observed success counts that can run in minutes.
- For each cell, compute exact DP risky and safe values, empirical estimates from observed counts, posterior mean and quantile estimates under explicit priors, confidence-bound choices, raw TRL, and TRL-log where applicable.
- Classify each cell by coverage regime, including matched, lucky-only, no-success, ambiguous, and prior-dependent cases.
- Save raw_grid.json, metrics.csv, regret_heatmap.csv, action_choice_grid.csv, impossibility_cases.json, coverage_diagnostics.json, transition_tables.json, and value_tables.json under research/sto_trl/artifacts/0008/.
- Write research/sto_trl/results/0008_result.json and research/sto_trl/results/0008_summary.md, then validate the result JSON with scripts/validate_artifacts.py and artifact checks.

## Required outputs

- `research/sto_trl/results/0008_result.json`
- `research/sto_trl/results/0008_summary.md`
- `research/sto_trl/artifacts/0008/`


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

- `research/sto_trl/results/0008_result.json`
- `research/sto_trl/results/0008_summary.md`
- `research/sto_trl/artifacts/0008/`


## Timeout and environment warning

The orchestrator enforces the configured timeout externally. Run experiment commands inside the project conda environment, normally with `conda run -n <env> ...`. Keep the experiment small and write a failed result JSON if the plan is impossible.


## Existing code pointers

This starter repository has no project code yet. Create only the tiny files needed under the experiment artifact directory unless the plan explicitly asks for repo code changes.
