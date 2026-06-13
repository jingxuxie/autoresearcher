# Executor Context: project_001

## Current experiment plan

# Experiment 0001

## Objective

Run a deterministic positive-control counting experiment comparing a weak baseline against a corrected counting method on the same tiny synthetic dataset.

## Hypothesis

A corrected method that counts the target item exactly will achieve higher accuracy than a deliberately weak baseline on a fixed synthetic counting dataset.

## Success criteria

- Creates research/project_001/results/0001_result.json.
- Creates research/project_001/results/0001_summary.md.
- Records exact commands run in the result JSON.
- Saves raw per-example predictions and aggregate metrics under research/project_001/artifacts/0001/.
- Reports baseline_accuracy and corrected_accuracy on the same deterministic examples.
- corrected_accuracy is strictly greater than baseline_accuracy.
- Completes within 30 minutes without large dependencies, downloads, training, or expensive compute.

## Failure criteria

- Missing, invalid, or incomplete result JSON.
- No comparable weak baseline evaluated on the same examples.
- No exact commands recorded.
- No raw metrics or per-example outputs saved.
- Corrected method accuracy is not strictly higher than baseline accuracy.
- Experiment uses large dependencies, large data, expensive compute, or long runtime.

## Estimated runtime

<= 5 minutes

## Tasks for Codex

- Inspect the existing project_001 layout and result schema before writing outputs.
- Create a tiny deterministic dataset of counting examples with known labels.
- Evaluate a weak baseline, such as always predicting zero, on every example.
- Evaluate a corrected method that exactly counts the target item on every example.
- Save per-example records to research/project_001/artifacts/0001/raw_predictions.json.
- Save aggregate metrics to research/project_001/artifacts/0001/metrics.json.
- Write research/project_001/results/0001_result.json with exact commands, artifact paths, raw metrics, and success/failure status.
- Write research/project_001/results/0001_summary.md summarizing the setup, commands, metrics, and whether the success criteria were met.

## Required outputs

- `research/project_001/results/0001_result.json`
- `research/project_001/results/0001_summary.md`
- `research/project_001/artifacts/0001/`


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

- `research/project_001/results/0001_result.json`
- `research/project_001/results/0001_summary.md`
- `research/project_001/artifacts/0001/`


## Timeout warning

The orchestrator enforces the configured timeout externally. Keep the experiment small and write a failed result JSON if the plan is impossible.


## Existing code pointers

This starter repository has no project code yet. Create only the tiny files needed under the experiment artifact directory unless the plan explicitly asks for repo code changes.
