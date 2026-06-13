# Executor Context: sto_trl

## Current experiment plan

# Experiment 0002

## Objective

Run a small tabular coverage-sensitivity stress test for the risky shortcut diagnostic, including both risk-suboptimal and risk-optimal settings, to check whether raw TRL overestimation and log/MC calibration claims survive biased or sparse stochastic outcome coverage.

## Hypothesis

Raw TRL overestimation is support-driven and will select risky whenever a lucky risky transition is observed, while empirical TRL-log and MC variants will be calibrated only when observed risky success/failure frequencies approximate the true stochastic branch; adding a risk-optimal setting will detect whether apparent improvements are merely conservative avoidance.

## Success criteria

- Reuses or copies the 0001 tabular harness into research/sto_trl/artifacts/0002/ without editing prior results or control scripts.
- Evaluates exact DP ground truth for deterministic chain plus two risky-shortcut configurations: one where safe is optimal and one where risky is optimal.
- Runs a tiny predeclared set of offline risky coverage regimes, such as matched, lucky-biased, lucky-only, unlucky-biased, and no-risky-success, with fixed deterministic seeds or explicit constructed counts.
- Compares the same methods as 0001: mc_supervised, trl_raw, trl_log, and mc_plus_trl_log, using exact DP only for evaluation.
- Saves raw per-regime metrics including overestimation error, underestimation error, long-horizon value MSE, policy regret, risky action selection rate, calibration error, and coverage diagnostics.
- Produces valid research/sto_trl/results/0002_result.json and research/sto_trl/results/0002_summary.md with exact commands run.

## Failure criteria

- Training methods use true transition probabilities or exact DP labels beyond evaluation.
- The experiment only repeats the matched 2/6 risky outcome setting from 0001.
- No risk-optimal configuration is included, making conservatism impossible to diagnose.
- The result reports only aggregate prose or training loss instead of raw numeric metrics by method, MDP setting, and coverage regime.
- The run expands to neural networks, OGBench, large sweeps, downloads, or runtime over 30 minutes.

## Estimated runtime

<= 20 minutes

## Tasks for Codex

- Create research/sto_trl/artifacts/0002/ and a self-contained coverage stress script, preferably by adapting the 0001 prototype.
- Keep the deterministic chain sanity check as a regression guard.
- Define two risky-shortcut MDP configurations with exact DP: safe-optimal and risky-optimal.
- Construct a tiny set of offline datasets with explicit risky success/failure counts for each coverage regime and save their specifications.
- Run mc_supervised, trl_raw, trl_log, and mc_plus_trl_log on each MDP/configuration/regime combination.
- Write raw_metrics.json, metrics.csv, coverage_diagnostics.json or equivalent structured artifacts under research/sto_trl/artifacts/0002/.
- Validate research/sto_trl/results/0002_result.json against schemas/result.schema.json with artifact checks.

## Required outputs

- `research/sto_trl/results/0002_result.json`
- `research/sto_trl/results/0002_summary.md`
- `research/sto_trl/artifacts/0002/`


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

- `research/sto_trl/results/0002_result.json`
- `research/sto_trl/results/0002_summary.md`
- `research/sto_trl/artifacts/0002/`


## Timeout and environment warning

The orchestrator enforces the configured timeout externally. Run experiment commands inside the project conda environment, normally with `conda run -n <env> ...`. Keep the experiment small and write a failed result JSON if the plan is impossible.


## Existing code pointers

This starter repository has no project code yet. Create only the tiny files needed under the experiment artifact directory unless the plan explicitly asks for repo code changes.
