# Executor Context: sto_trl

## Current experiment plan

# Experiment 0013

## Objective

Test whether the partial-observation/context pivot generalizes beyond the single hand-constructed 0012 POMDP and whether any TRL-style transitive component adds value beyond history-model DP.

## Hypothesis

Across a small randomized suite of aliased tabular POMDPs with varying cue reliability and history sufficiency, observation-only methods will fail when observations alias latent states, bounded-history methods will improve when history is sufficient, and a viable TRL/context direction requires MC+TRL-log to improve over history MC-only without being fully explained by history-model DP on every regime.

## Success criteria

- Run at least 3 tiny POMDP families with 5 fixed seeds each, including cue-sufficient, cue-noisy, and cue-insufficient regimes.
- Observation-only TRL-log and observation-only model DP have higher heldout MSE or policy regret than latent-oracle evaluation in aliased regimes.
- History-keyed MC+TRL-log improves heldout MSE over history-keyed MC-only by at least 25% averaged over cue-sufficient regimes.
- The report explicitly compares history-keyed MC+TRL-log against history-model DP; if model DP fully explains all gains, the result is labeled boundary/negative for TRL algorithmic value.
- No training method consumes latent states, exact DP labels, true transition probabilities, or future observations as inputs.

## Failure criteria

- History-keyed MC+TRL-log is not better than history-keyed MC-only in cue-sufficient regimes.
- All gains are fully matched by history-model DP with zero action disagreement and no heldout-MSE gap.
- The only positive cases use history keys that directly encode the latent state or otherwise leak oracle information.
- Cue-noisy or cue-insufficient regimes are omitted, preventing separation of context sufficiency from oracle disambiguation.
- Runtime exceeds 30 minutes or introduces neural networks, continuous control, OGBench, large downloads, or expensive training.

## Estimated runtime

<= 30 minutes

## Tasks for Codex

- Generate a randomized suite of tiny latent tabular POMDPs with aliased observations, stochastic shortcuts or teleporters, and controlled cue reliability.
- Evaluate observation-only empirical model DP, observation-only TRL-log, history MC-only, history TRL-log, history MC+TRL-log, history-model DP, and latent-oracle DP.
- Keep latent states only for audit and exact evaluation; add explicit leakage checks confirming training keys are observation/history-only.
- Stratify metrics by cue-sufficient, cue-noisy, and cue-insufficient regimes.
- Write a summary that decides whether this is real representation/context evidence or another model-DP-equivalence boundary.

## Required outputs

- `research/sto_trl/results/0013_result.json`
- `research/sto_trl/results/0013_summary.md`
- `research/sto_trl/artifacts/0013/`


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

- `research/sto_trl/results/0013_result.json`
- `research/sto_trl/results/0013_summary.md`
- `research/sto_trl/artifacts/0013/`


## Timeout and environment warning

The orchestrator enforces the configured timeout externally. Run experiment commands inside the project conda environment, normally with `conda run -n <env> ...`. Keep the experiment small and write a failed result JSON if the plan is impossible.


## Existing code pointers

This starter repository has no project code yet. Create only the tiny files needed under the experiment artifact directory unless the plan explicitly asks for repo code changes.
