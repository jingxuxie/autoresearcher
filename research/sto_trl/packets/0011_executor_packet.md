# Executor Context: sto_trl

## Current experiment plan

# Experiment 0011

## Objective

Run a small randomized tabular equivalence and generalization audit to test whether posterior TRL-log has any distinct benefit over prior-matched posterior model DP beyond the handcrafted 0010 branch-chain regimes.

## Hypothesis

Across tiny randomized branch-chain, stochastic stitching, and stochastic teleporter-style tabular MDPs with exact DP ground truth and finite offline coverage, posterior_trl_log will usually remain equivalent or near-equivalent to prior-matched posterior model DP. A credible positive result requires a predeclared regime where posterior_trl_log improves value or policy metrics over both TRL-log and prior-matched posterior model DP without relying on model-DP misspecification or conservative risk avoidance.

## Success criteria

- Creates a self-contained artifact under research/sto_trl/artifacts/0011/ without editing prior results, schemas, AGENTS.md, scripts/autoresearcher.py, or environment files.
- Uses exact DP ground truth for every generated tabular MDP and keeps total runtime under 30 minutes.
- Predeclares a tiny randomized suite, such as 3 MDP families with 5 seeds each: branch-chain, stochastic stitching graph, and stochastic teleporter graph.
- Includes finite offline coverage regimes with matched coverage, lucky-only coverage, no-success coverage, and sparse long-horizon label censoring where applicable.
- Compares mc_supervised, trl_raw, trl_log, empirical_model_dp, posterior_mean_model_dp, posterior_lower or robust model DP, posterior_trl_log, and posterior_mc_plus_trl_log using prior-matched assumptions.
- Reports per-family and per-regime heldout long-horizon value MSE, all-pair value MSE, Q overestimation and underestimation, calibration error, policy regret, risky action selection rate, and coverage diagnostics.
- Reports an explicit equivalence audit: max absolute value difference, action disagreement rate, and metric deltas between posterior_trl_log and prior-matched posterior model DP.
- Counts positive evidence only if posterior_trl_log or posterior_mc_plus_trl_log beats both TRL-log and prior-matched posterior model DP on predeclared metrics while preserving matched risk-optimal action choice and avoiding safe-everywhere behavior.
- Counts equivalence, near-equivalence, or improvement only from prior choice as negative or boundary evidence.
- Produces valid research/sto_trl/results/0011_result.json and research/sto_trl/results/0011_summary.md with exact commands run.

## Failure criteria

- The experiment omits prior-matched posterior model-DP baselines or does not report direct equivalence diagnostics.
- The experiment creates a TRL advantage by making transition-model DP unavailable, deliberately misspecified, or evaluated with less information than posterior TRL uses.
- Exact DP values or true transition probabilities are used for training or action selection rather than only evaluation and audit artifacts.
- The suite expands beyond a tiny tabular CPU-scale audit or exceeds 30 minutes.
- The result reports only aggregate averages without per-family, per-regime, and coverage-stratified metrics.
- A method is treated as successful because it is conservative everywhere or fails matched risk-optimal action selection.
- The run moves to neural networks, continuous control, PointMaze, AntMaze, OGBench, large downloads, or expensive training.

## Estimated runtime

<= 25 minutes

## Tasks for Codex

- Create research/sto_trl/artifacts/0011/ and implement a small randomized_equivalence_audit.py script, reusing prior tabular helpers where practical.
- Define a tiny predeclared randomized suite with fixed seeds for branch-chain, stochastic stitching, and stochastic teleporter-style MDPs.
- Generate finite offline datasets and censored long-horizon labels for each seed while saving coverage diagnostics and offline dataset summaries.
- Implement prior-matched empirical and posterior model-DP baselines plus posterior_trl_log and posterior_mc_plus_trl_log variants.
- Compute exact DP ground truth for all generated MDPs and evaluate value, calibration, overestimation, policy, action-selection, and equivalence metrics.
- Save raw_metrics.json, metrics.csv, family_summary.csv, regime_summary.csv, equivalence_diagnostics.json, coverage_diagnostics.json, transition_tables.json, and value_tables.json under research/sto_trl/artifacts/0011/.
- Write research/sto_trl/results/0011_result.json and research/sto_trl/results/0011_summary.md, then validate the result JSON with scripts/validate_artifacts.py and artifact checks.

## Required outputs

- `research/sto_trl/results/0011_result.json`
- `research/sto_trl/results/0011_summary.md`
- `research/sto_trl/artifacts/0011/`


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

- `research/sto_trl/results/0011_result.json`
- `research/sto_trl/results/0011_summary.md`
- `research/sto_trl/artifacts/0011/`


## Timeout and environment warning

The orchestrator enforces the configured timeout externally. Run experiment commands inside the project conda environment, normally with `conda run -n <env> ...`. Keep the experiment small and write a failed result JSON if the plan is impossible.


## Existing code pointers

This starter repository has no project code yet. Create only the tiny files needed under the experiment artifact directory unless the plan explicitly asks for repo code changes.
