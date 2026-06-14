# Executor Context: reward_to_gcrl

## Current experiment plan

# Experiment 0009

## Objective

Run the first CPU-only NumPy shared-parameter test on tiny FourRooms using a low-rank factorized soft successor-measure model, comparing terminal-only g_plus training against combined g_plus plus real-state auxiliary-goal training under matched limited offline replay.

## Hypothesis

If real-state auxiliary goals provide useful shared representation signal, then under a low-rank bottleneck and adequate replay coverage, combined auxiliary training should reduce g_plus value error and Bellman residual versus terminal-only g_plus training without increasing reward-policy disagreement. If it does not, then auxiliary-goal benefit is not yet supported and should not be claimed.

## Success criteria

- Use only CPU NumPy code on the already-audited tiny FourRooms environment; no PyTorch, JAX, GPU, larger environments, or large dependencies.
- Reuse or verify the 0008 FourRooms transition semantics, reward normalization, terminal masks, goal indexing, and exact tabular references for g_plus and real-state goals.
- Train a genuinely shared low-rank model, such as M_hat(s,a,g) = sigmoid(u_{s,a} dot v_g + b_g) or a documented bounded equivalent, so real-state goals and g_plus share state-action factors.
- Compare at minimum terminal-only g_plus training versus combined g_plus plus real-state auxiliary training on identical replay datasets, seeds, rank, optimizer step budget, target construction, and evaluation protocol.
- Use a small predeclared configuration only, for example rank 4, 10 seeds, one replay budget, and at most one auxiliary weight plus a terminal-only baseline.
- Report replay coverage, visited state-action coverage, goal-label coverage, and whether each seed meets an adequate-coverage threshold before interpreting learning metrics.
- Combined auxiliary training must improve mean g_plus value error or Bellman residual by at least 10 percent on adequate-coverage seeds, or improve one while being statistically indistinguishable on the other, without increasing tie-aware reward-policy disagreement.
- Real-state auxiliary goal predictions must be evaluated against exact references, including mean state-goal value error and a greedy goal-reaching diagnostic, but these are auxiliary diagnostics rather than reward-task success criteria.
- The summary must explicitly label the result as one of: auxiliary_helped_gplus, auxiliary_neutral, negative_transfer, coverage_limited, or optimizer_failed.

## Failure criteria

- The model does not actually share parameters between real-state goals and g_plus.
- The experiment uses independent tabular slices again, which would duplicate 0008 rather than testing shared representation.
- Replay coverage is inadequate and the summary still makes auxiliary-benefit claims.
- Auxiliary training improves real-state goal metrics but worsens g_plus value error, Bellman residual, or reward-policy disagreement without being labeled negative transfer.
- The run sweeps many ranks, losses, auxiliary weights, or optimizers and then selects the best without predeclared criteria.
- The experiment installs neural frameworks, uses GPU, expands to larger environments, or makes publishable auxiliary-goal claims before review.

## Estimated runtime

<= 25 minutes

## Tasks for Codex

- Create research/reward_to_gcrl/artifacts/0009/run_fourrooms_lowrank_auxiliary.py using CPU-only NumPy.
- Write an environment audit that verifies the FourRooms transition table, state indexing, wall/door layout, action mapping, reward normalization, terminal masks, and goal indexing against 0008 where possible.
- Generate a fixed offline replay dataset from a simple non-oracle behavior policy or small mixture of documented non-oracle policies, and save replay coverage diagnostics.
- Implement exact target computation from replay for g_plus and sampled real-state goals, using exact tabular references only for evaluation, not for behavior or training targets beyond normal bootstrapped target construction.
- Implement terminal-only and combined auxiliary low-rank SSM variants with matched initialization seeds, optimizer steps, batch schedule, learning rate, rank, and target-network or fitted-iteration protocol.
- Evaluate g_plus scaled value error, Bellman residual, tie-aware reward-policy disagreement, raw reward-task return/success, real-state goal value error, greedy goal-reaching success, and negative-transfer diagnostics.
- Save research/reward_to_gcrl/results/0009_result.json with raw per-seed metrics, pass/fail flags, exact commands, model configuration, replay coverage, and conservative verdict.
- Save research/reward_to_gcrl/results/0009_summary.md with a short review-oriented interpretation and a recommendation on whether to repeat the low-rank checkpoint, move to a slightly larger sweep, or stop auxiliary-goal claims for now.

## Required outputs

- `research/reward_to_gcrl/results/0009_result.json`
- `research/reward_to_gcrl/results/0009_summary.md`
- `research/reward_to_gcrl/artifacts/0009/`


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

- `research/reward_to_gcrl/results/0009_result.json`
- `research/reward_to_gcrl/results/0009_summary.md`
- `research/reward_to_gcrl/artifacts/0009/`


## Timeout and environment warning

The orchestrator enforces the configured timeout externally. Run experiment commands inside the project conda environment, normally with `conda run -n <env> ...`. Keep the experiment small and write a failed result JSON if the plan is impossible.


## Existing code pointers

This starter repository has no project code yet. Create only the tiny files needed under the experiment artifact directory unless the plan explicitly asks for repo code changes.
