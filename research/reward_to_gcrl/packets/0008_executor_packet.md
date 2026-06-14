# Executor Context: reward_to_gcrl

## Current experiment plan

# Experiment 0008

## Objective

Run a CPU-only tabular vector successor-measure sanity check with real-state goals plus g_plus on a tiny deterministic FourRooms grid.

## Hypothesis

For a tabular vector SSM with independent goal slices, adding real-state goals should learn correct state-goal reachability maps while leaving the g_plus reward-success slice numerically equivalent to the terminal-only soft learner. Any degradation of the g_plus policy or value slice would indicate an implementation, indexing, reward-normalization, or terminal-mask bug rather than a research effect.

## Success criteria

- Creates research/reward_to_gcrl/results/0008_result.json and research/reward_to_gcrl/results/0008_summary.md.
- Creates reproducible artifacts under research/reward_to_gcrl/artifacts/0008/.
- Uses only CPU tabular methods on a tiny deterministic FourRooms grid; no neural models, low-rank factorization, large environments, GPU-dependent work, large downloads, or expensive training.
- Predeclares and saves grid layout, wall cells, doorway cells, state indexing, action mapping, reward task, reward normalization, terminal masks, gamma values, update procedure, seeds if stochastic, and exact commands run.
- Solves exact DP references for the terminal-only g_plus slice and for real-state goal slices, and reports max_abs_error for learned vector slices versus exact references.
- Reports max_abs(M_vector[:,:,g_plus] - M_terminal_only), max_abs(M_vector[:,:,g_plus]/(1-gamma) - Q_norm), and reward-policy disagreement versus terminal-only soft or exact DP.
- For sampled real-state goals or all selected goals, reports greedy goal-reaching success rate, mean shortest-path distance reduction, policy disagreement versus exact goal policies, and reachability heatmap/arrow artifacts.
- Passes only if the g_plus slice matches terminal-only soft within a predeclared tolerance, reward-policy disagreement is zero or only due to ties, and real-state goal slices achieve high reachability accuracy on non-wall reachable goals.

## Failure criteria

- Missing, invalid, or schema-incompatible result JSON or summary markdown.
- Exact commands, raw metrics, artifact paths, environment audit, reward normalization, goal indexing, or terminal masks are omitted.
- The vector update couples goals or changes the g_plus slice relative to terminal-only soft beyond the predeclared tolerance.
- Real-state goal diagnostics are only visual/prose and omit exact value error or goal-reaching metrics.
- The experiment claims auxiliary-goal reward improvement in tabular mode without shared parameters.
- The executor adds neural approximation, low-rank factorization, sampled augmented baselines, larger environments, large downloads, GPU-dependent work, or long training before this tabular vector sanity gate is complete.

## Estimated runtime

<= 25 minutes

## Tasks for Codex

- Implement a standalone diagnostic script under research/reward_to_gcrl/artifacts/0008/ defining a tiny deterministic FourRooms transition table with audited state indexing, walls, doorways, actions, rewards, and terminals.
- Implement terminal-only soft M_plus and vector M[s,a,g] with real-state goals 0..n_states-1 and artificial g_plus = n_states using the prototype update immediate[s_next] += (1-gamma) and immediate[g_plus] += (1-gamma)*r_bar.
- Compute exact DP references for Q_norm, terminal-only soft g_plus, and real-state goal reachability slices for gamma values such as 0.95 and 0.99.
- Run small deterministic full-sweep tabular updates or a fixed logged transition stream to convergence within the 30-minute budget.
- Compute g_plus equivalence metrics, reward-policy disagreement, real-state goal value errors, greedy goal-reaching success rates, shortest-path distance diagnostics, and tie counts.
- Save raw per-goal metrics, aggregate metrics, environment audit, exact DP references, and reachability heatmap/arrow data under research/reward_to_gcrl/artifacts/0008/.
- Validate the result JSON with schemas/result.schema.json and validate declared artifacts with scripts/validate_artifacts.py.

## Required outputs

- `research/reward_to_gcrl/results/0008_result.json`
- `research/reward_to_gcrl/results/0008_summary.md`
- `research/reward_to_gcrl/artifacts/0008/`


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

- `research/reward_to_gcrl/results/0008_result.json`
- `research/reward_to_gcrl/results/0008_summary.md`
- `research/reward_to_gcrl/artifacts/0008/`


## Timeout and environment warning

The orchestrator enforces the configured timeout externally. Run experiment commands inside the project conda environment, normally with `conda run -n <env> ...`. Keep the experiment small and write a failed result JSON if the plan is impossible.


## Existing code pointers

This starter repository has no project code yet. Create only the tiny files needed under the experiment artifact directory unless the plan explicitly asks for repo code changes.
