# Executor Context: reward_to_gcrl

## Current experiment plan

# Experiment 0010

## Objective

Diagnose the 0009 negative transfer in the shared low-rank FourRooms SSM by testing whether auxiliary collapse is caused by loss-scaling or optimization imbalance, while keeping the run CPU-only, NumPy-only, tiny, and predeclared.

## Hypothesis

If 0009 failed mainly because auxiliary real-state losses overwhelmed or destabilized the g_plus head, then a loss-balanced or staged auxiliary variant should reduce negative transfer and approach or improve terminal-only g_plus metrics. If these controlled variants still fail, auxiliary real-state goals are unsupported for this low-rank architecture and should be paused.

## Success criteria

- Use the same audited tiny FourRooms environment, transition hash, replay construction, exact references, rank 4 model form, and CPU-only NumPy implementation family as 0009.
- Run only a tightly predeclared diagnostic set: terminal-only reproduction, original combined auxiliary lambda=1 reproduction, loss-balanced combined auxiliary, and staged real-goal pretrain followed by g_plus fine-tuning.
- Report per-component g_plus and auxiliary losses, gradient norms on shared u_sa factors, target-value scales, and whether auxiliary gradients dominate terminal gradients.
- The terminal-only and original combined reproduction should qualitatively match 0009 within a reasonable tolerance; otherwise the diagnostic must be labeled reproduction_failed.
- A repaired auxiliary variant counts as promising only if it improves mean g_plus Bellman residual or mean scaled value error by at least 10 percent over terminal-only, or is statistically indistinguishable on both while improving real-state goal diagnostics, without increasing reward-policy disagreement.
- If no repaired auxiliary variant matches terminal-only g_plus value error and Bellman residual, the verdict must be auxiliary_unsupported_for_lowrank rather than tuned_failure.
- No PyTorch, JAX, GPU, larger environment, broad sweep, or publishable auxiliary-goal claim is allowed before review.

## Failure criteria

- The experiment tries more than the predeclared small set of diagnostic variants.
- The original 0009 negative-transfer result cannot be reproduced and the discrepancy is not explained.
- The result omits gradient-norm or loss-scale diagnostics, leaving the cause of collapse ambiguous.
- A variant improves real-state goal metrics while worsening g_plus value error, Bellman residual, or reward-policy disagreement and is not labeled negative transfer.
- The summary claims auxiliary-goal benefit without beating or matching terminal-only g_plus metrics under the predeclared criteria.
- The run uses neural frameworks, GPU, larger environments, or expensive hyperparameter sweeps.

## Estimated runtime

<= 25 minutes

## Tasks for Codex

- Create research/reward_to_gcrl/artifacts/0010/run_fourrooms_lowrank_aux_diagnostic.py by minimally extending the 0009 script.
- Reuse and verify the 0008/0009 FourRooms environment audit, transition hash, goal indexing, reward normalization, terminal masks, replay behavior, and exact references.
- Implement four predeclared variants: terminal_only, combined_lambda_1_reproduction, combined_loss_balanced, and staged_real_goal_pretrain_then_gplus_finetune.
- For each variant, run the same 10 seeds, replay budget, rank, optimizer family, and evaluation protocol unless a difference is explicitly part of the staged diagnostic.
- Log per-step or checkpointed g_plus loss, auxiliary loss, shared-factor gradient norms, head-specific gradient norms, value scales, Bellman residual, value error, policy disagreement, reward success, and real-goal diagnostics.
- Save raw per-seed metrics and aggregate deltas versus terminal-only and original combined auxiliary.
- Write research/reward_to_gcrl/results/0010_result.json with exact commands, artifacts, pass/fail flags, reproduction status, gradient-scale diagnostics, and conservative verdict.
- Write research/reward_to_gcrl/results/0010_summary.md recommending one of: proceed_to_tiny_reviewed_aux_followup, pause_auxiliary_thread, or write_negative_result.

## Required outputs

- `research/reward_to_gcrl/results/0010_result.json`
- `research/reward_to_gcrl/results/0010_summary.md`
- `research/reward_to_gcrl/artifacts/0010/`


## Environment YAML

```yaml
name: autoresearcher_reward_to_gcrl
channels:
  - conda-forge
dependencies:
  - python=3.11
  - pip
  - numpy
  - pandas
  - matplotlib
  - pyyaml
  - jsonschema
  - pytest
  - gymnasium
```


## Environment state

```json
{
  "blocker": null,
  "commands_run": [
    "conda env list",
    "nvidia-smi",
    "conda env create -f research/reward_to_gcrl/environment.yaml",
    "kill 1528368",
    "conda create -y -n autoresearcher_reward_to_gcrl -c conda-forge --override-channels python=3.11 pip",
    "conda install -y -n autoresearcher_reward_to_gcrl -c conda-forge --override-channels numpy pandas matplotlib pyyaml jsonschema pytest gymnasium",
    "conda run -n autoresearcher_reward_to_gcrl python --version",
    "conda run -n autoresearcher_reward_to_gcrl python -c \"import sys, numpy, pandas, matplotlib, yaml, jsonschema, pytest, gymnasium; print(sys.executable); print('numpy', numpy.__version__); print('pandas', pandas.__version__); print('matplotlib', matplotlib.__version__); print('pyyaml', yaml.__version__); print('jsonschema', jsonschema.__version__); print('pytest', pytest.__version__); print('gymnasium', gymnasium.__version__)\"",
    "conda env list | rg 'autoresearcher_reward_to_gcrl'",
    "nvidia-smi --query-gpu=name,driver_version,memory.total --format=csv,noheader",
    "mkdir -p research/reward_to_gcrl/setup_logs",
    "conda run -n autoresearcher_reward_to_gcrl python -m jsonschema -i research/reward_to_gcrl/env_state.json schemas/env_setup.schema.json"
  ],
  "conda_env_name": "autoresearcher_reward_to_gcrl",
  "conda_env_path": "/home/eston/anaconda3/envs/autoresearcher_reward_to_gcrl",
  "environment_file": "research/reward_to_gcrl/environment.yaml",
  "gpu_available": true,
  "gpu_checks": [
    "nvidia-smi: NVIDIA GeForce RTX 4090 visible, driver 560.94, CUDA 12.6, 24564 MiB total memory",
    "nvidia-smi --query-gpu=name,driver_version,memory.total --format=csv,noheader: NVIDIA GeForce RTX 4090, 560.94, 24564 MiB"
  ],
  "gpu_requested": true,
  "packages_verified": [
    "python 3.11.15",
    "numpy 2.4.6",
    "pandas 3.0.3",
    "matplotlib 3.10.9",
    "pyyaml 6.0.3",
    "jsonschema 4.26.0",
    "pytest 9.0.3",
    "gymnasium 1.3.0"
  ],
  "project": "reward_to_gcrl",
  "status": "ready",
  "summary": "Project-specific conda environment is ready at /home/eston/anaconda3/envs/autoresearcher_reward_to_gcrl. Python and declared imports were verified, and env_state.json validates against schemas/env_setup.schema.json. GPU is visible via nvidia-smi. No research experiment or training was run."
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

- `research/reward_to_gcrl/results/0010_result.json`
- `research/reward_to_gcrl/results/0010_summary.md`
- `research/reward_to_gcrl/artifacts/0010/`


## Timeout and environment warning

The orchestrator enforces the configured timeout externally. Run experiment commands inside the project conda environment, normally with `conda run -n <env> ...`. Keep the experiment small and write a failed result JSON if the plan is impossible.


## Existing code pointers

This starter repository has no project code yet. Create only the tiny files needed under the experiment artifact directory unless the plan explicitly asks for repo code changes.
