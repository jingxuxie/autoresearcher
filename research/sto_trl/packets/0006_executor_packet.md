# Executor Context: sto_trl

## Current experiment plan

# Experiment 0006

## Objective

Test a minimal uncertainty-aware or one-sided conservative log-TRL backup on the tabular biased-coverage failure while preserving matched safe-optimal, matched risk-optimal, and deterministic long-horizon behavior.

## Hypothesis

A small uncertainty penalty based only on offline branch count or outcome variance can reduce lucky-only risky overestimation versus trl_log without breaking deterministic horizon recovery or incorrectly avoiding the risky action when it is truly optimal under matched coverage.

## Success criteria

- Create a self-contained artifact under research/sto_trl/artifacts/0006/ without editing prior results, schemas, AGENTS.md, scripts/autoresearcher.py, or environment files.
- Implement at least one predeclared uncertainty-aware log-TRL variant, such as empirical_log_backup_minus_count_penalty or one_sided_conservative_log_trl, with a tiny fixed penalty grid including zero.
- Evaluate exact DP on chain_len9_holdout, safe_optimal_matched, risk_optimal_matched, safe_optimal_lucky_only_stress, and one risk_optimal_unlucky_or_no_success stress case.
- Compare against mc_supervised, trl_raw, trl_log, mc_plus_trl_log, and the best 0005 trl_log-equivalent successor-distance baseline on identical constructed datasets.
- Report per-scenario and per-penalty raw metrics: held-out long-horizon value MSE, Q calibration error, overestimation, underestimation, policy regret, risky action selection rate, branch-count or variance diagnostics, and coverage diagnostics.
- Count positive evidence only if a nonzero uncertainty penalty reduces safe_optimal_lucky_only risky overestimation or policy regret versus trl_log while still selecting risky with zero policy regret on risk_optimal_matched and preserving chain held-out MSE near trl_log.
- Produce valid research/sto_trl/results/0006_result.json and research/sto_trl/results/0006_summary.md with exact commands run.

## Failure criteria

- The uncertainty penalty uses exact DP, true transition probabilities, or hidden knowledge of missing stochastic outcomes rather than offline coverage statistics.
- The experiment omits the matched risk-optimal anti-conservatism check.
- The result reports only the best penalty and hides the full predeclared penalty grid.
- The method is claimed successful despite failing deterministic chain recovery or selecting safe in the matched risk-optimal scenario.
- The run expands to neural networks, OGBench, large sweeps, downloads, or exceeds 30 minutes.

## Estimated runtime

<= 20 minutes

## Tasks for Codex

- Create research/sto_trl/artifacts/0006/ and adapt the 0005 audit harness into a conservative or uncertainty-aware log-TRL script.
- Define the uncertainty diagnostic and penalty formula explicitly in the artifact source, using only offline trajectory counts or observed outcome variance.
- Run a tiny predeclared penalty grid, for example alpha in [0.0, 0.05, 0.1, 0.2], on the fixed tabular scenarios.
- Save raw_metrics.json, metrics.csv, penalty_sweep.json, uncertainty_diagnostics.json, offline_datasets.json, transition_tables.json, and value_tables.json under research/sto_trl/artifacts/0006/.
- Write research/sto_trl/results/0006_result.json and research/sto_trl/results/0006_summary.md, then validate the result JSON against schemas/result.schema.json with artifact checks.

## Required outputs

- `research/sto_trl/results/0006_result.json`
- `research/sto_trl/results/0006_summary.md`
- `research/sto_trl/artifacts/0006/`


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

- `research/sto_trl/results/0006_result.json`
- `research/sto_trl/results/0006_summary.md`
- `research/sto_trl/artifacts/0006/`


## Timeout and environment warning

The orchestrator enforces the configured timeout externally. Run experiment commands inside the project conda environment, normally with `conda run -n <env> ...`. Keep the experiment small and write a failed result JSON if the plan is impossible.


## Existing code pointers

This starter repository has no project code yet. Create only the tiny files needed under the experiment artifact directory unless the plan explicitly asks for repo code changes.
