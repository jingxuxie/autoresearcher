# Executor Context: sto_trl

## Current experiment plan

# Experiment 0012

## Objective

Test whether short trajectory context plus log-space transitive propagation helps in a tiny stochastic POMDP with aliased observations, where observation-level model DP is not a fair Markov baseline.

## Hypothesis

In a latent tabular MDP with two or more hidden states sharing the same observation, observation-only empirical model DP and observation-only TRL-log will be miscalibrated, while history-keyed MC+TRL-log will improve held-out long-horizon value MSE and policy regret versus history-keyed MC-only without using latent states in training.

## Success criteria

- Observation-only empirical model DP and observation-only TRL-log show a measurable aliasing failure: higher heldout MSE or policy regret than a latent-oracle evaluation baseline.
- History-keyed MC+TRL-log improves heldout long-horizon value MSE over history-keyed MC-only by at least 25% on censored labels.
- History-keyed MC+TRL-log improves policy regret or risky/teleport action choice versus observation-only TRL-log on at least one aliased stochastic shortcut or teleporter family.
- The report includes a history-model-DP baseline; if history-model-DP fully explains the gain, the result is labeled as representation/context evidence rather than a distinct TRL algorithm win.
- No training method uses true latent state, exact DP labels, true transition probabilities, or future observations as inputs.

## Failure criteria

- History-keyed MC+TRL-log is equivalent to or worse than history-keyed MC-only on heldout long-horizon MSE.
- The apparent gain disappears when compared to a prior-matched history-model-DP baseline.
- The task requires oracle latent-state access or future-information leakage to show improvement.
- The experiment does not include observation-only, history-keyed, and latent-oracle evaluation baselines.
- Runtime exceeds 30 minutes or introduces neural networks, continuous control, OGBench, large downloads, or expensive training.

## Estimated runtime

<= 30 minutes

## Tasks for Codex

- Create a tiny latent tabular POMDP with aliased observations, including one risky shortcut or stochastic teleporter and one safe path.
- Generate offline trajectories where training inputs are observations, actions, rewards/goals, and bounded history keys only; store latent states only for audit and exact evaluation.
- Implement observation-only empirical model DP, observation-only TRL-log, history-keyed MC-only, history-keyed TRL-log, history-keyed MC+TRL-log, history-model DP, and latent-oracle DP evaluation.
- Use censored long-horizon labels so transitive propagation has a reason to help beyond MC supervision.
- Report metrics stratified by alias regime: heldout MSE, policy regret, risky/teleport action rate, calibration error, and action disagreement with latent-oracle policy.

## Required outputs

- `research/sto_trl/results/0012_result.json`
- `research/sto_trl/results/0012_summary.md`
- `research/sto_trl/artifacts/0012/`


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

- `research/sto_trl/results/0012_result.json`
- `research/sto_trl/results/0012_summary.md`
- `research/sto_trl/artifacts/0012/`


## Timeout and environment warning

The orchestrator enforces the configured timeout externally. Run experiment commands inside the project conda environment, normally with `conda run -n <env> ...`. Keep the experiment small and write a failed result JSON if the plan is impossible.


## Existing code pointers

This starter repository has no project code yet. Create only the tiny files needed under the experiment artifact directory unless the plan explicitly asks for repo code changes.
