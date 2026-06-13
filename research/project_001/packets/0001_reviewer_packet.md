# Reviewer Context: project_001

## Latest plan

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


## Latest plan JSON

```json
{
  "estimated_runtime_minutes": 5,
  "experiment_id": "0001",
  "failure_criteria": [
    "Missing, invalid, or incomplete result JSON.",
    "No comparable weak baseline evaluated on the same examples.",
    "No exact commands recorded.",
    "No raw metrics or per-example outputs saved.",
    "Corrected method accuracy is not strictly higher than baseline accuracy.",
    "Experiment uses large dependencies, large data, expensive compute, or long runtime."
  ],
  "hypothesis": "A corrected method that counts the target item exactly will achieve higher accuracy than a deliberately weak baseline on a fixed synthetic counting dataset.",
  "objective": "Run a deterministic positive-control counting experiment comparing a weak baseline against a corrected counting method on the same tiny synthetic dataset.",
  "required_outputs": [
    "research/project_001/results/0001_result.json",
    "research/project_001/results/0001_summary.md",
    "research/project_001/artifacts/0001/"
  ],
  "success_criteria": [
    "Creates research/project_001/results/0001_result.json.",
    "Creates research/project_001/results/0001_summary.md.",
    "Records exact commands run in the result JSON.",
    "Saves raw per-example predictions and aggregate metrics under research/project_001/artifacts/0001/.",
    "Reports baseline_accuracy and corrected_accuracy on the same deterministic examples.",
    "corrected_accuracy is strictly greater than baseline_accuracy.",
    "Completes within 30 minutes without large dependencies, downloads, training, or expensive compute."
  ],
  "tasks_for_codex": [
    "Inspect the existing project_001 layout and result schema before writing outputs.",
    "Create a tiny deterministic dataset of counting examples with known labels.",
    "Evaluate a weak baseline, such as always predicting zero, on every example.",
    "Evaluate a corrected method that exactly counts the target item on every example.",
    "Save per-example records to research/project_001/artifacts/0001/raw_predictions.json.",
    "Save aggregate metrics to research/project_001/artifacts/0001/metrics.json.",
    "Write research/project_001/results/0001_result.json with exact commands, artifact paths, raw metrics, and success/failure status.",
    "Write research/project_001/results/0001_summary.md summarizing the setup, commands, metrics, and whether the success criteria were met."
  ]
}
```


## Latest result JSON

```json
{
  "artifacts": [
    "research/project_001/artifacts/0001/raw_predictions.json",
    "research/project_001/artifacts/0001/metrics.json",
    "research/project_001/artifacts/0001/run_counting_experiment.py"
  ],
  "baseline_metrics": {
    "baseline_accuracy": 0.0,
    "baseline_correct": 0,
    "baseline_method": "always_predict_zero"
  },
  "claim_tested": "An exact target-item counting method achieves higher accuracy than a deliberately weak always-zero baseline on the same deterministic synthetic counting examples.",
  "commands_run": [
    "find . -maxdepth 4 -type f | sort",
    "find research -maxdepth 4 -type d | sort",
    "sed -n '1,220p' schemas/result.schema.json",
    "sed -n '1,240p' scripts/validate_artifacts.py",
    "ls -la research/project_001/results research/project_001/artifacts",
    "mkdir -p research/project_001/artifacts/0001",
    "python3 research/project_001/artifacts/0001/run_counting_experiment.py",
    "python3 scripts/validate_artifacts.py --repo-root . --json research/project_001/results/0001_result.json --schema schemas/result.schema.json --check-result-artifacts"
  ],
  "experiment_id": "0001",
  "interpretation": "The corrected exact-counting method counted every target occurrence correctly (6/6), while the weak always-zero baseline was correct on 0/6. The corrected accuracy exceeded the baseline by 1.000.",
  "known_failures": [],
  "metrics": {
    "accuracy_delta": 1.0,
    "baseline_accuracy": 0.0,
    "corrected_accuracy": 1.0,
    "corrected_correct": 6,
    "corrected_method": "exact_target_item_count",
    "num_examples": 6,
    "success_criteria_met": true
  },
  "next_questions": [
    "Does the same exact-counting implementation remain correct when examples include zero-count labels?",
    "How should this positive control be extended to a nontrivial counting method?"
  ],
  "status": "completed"
}
```


## Latest summary

# Experiment 0001 Summary

## Setup

This deterministic positive-control experiment used 6 tiny synthetic counting examples. Each example specifies a list of items, one target item, and the known count label.

## Commands Run

```bash
find . -maxdepth 4 -type f | sort
find research -maxdepth 4 -type d | sort
sed -n '1,220p' schemas/result.schema.json
sed -n '1,240p' scripts/validate_artifacts.py
ls -la research/project_001/results research/project_001/artifacts
mkdir -p research/project_001/artifacts/0001
python3 research/project_001/artifacts/0001/run_counting_experiment.py
python3 scripts/validate_artifacts.py --repo-root . --json research/project_001/results/0001_result.json --schema schemas/result.schema.json --check-result-artifacts
```

## Methods

- Baseline: always predict `0`.
- Corrected method: count exact matches to the target item in the example list.

## Raw Metrics

- Baseline accuracy: 0.000000 (0/6)
- Corrected accuracy: 1.000000 (6/6)
- Accuracy delta: 1.000000

## Artifacts

- `research/project_001/artifacts/0001/raw_predictions.json`
- `research/project_001/artifacts/0001/metrics.json`
- `research/project_001/artifacts/0001/run_counting_experiment.py`

## Outcome

Success criteria were met: corrected accuracy is strictly greater than baseline accuracy on the same deterministic examples.


## Artifact paths

- `/home/eston/autoresearcher/research/project_001/artifacts/0001`


## Review schema

```json
{
  "type": "object",
  "properties": {
    "experiment_id": { "type": "string" },
    "verdict": {
      "type": "string",
      "enum": ["pass", "weak_pass", "fail", "needs_human"]
    },
    "allows_auto_continue": {
      "type": "boolean"
    },
    "reasons": {
      "type": "array",
      "items": { "type": "string" }
    },
    "evidence_checked": {
      "type": "array",
      "items": { "type": "string" }
    },
    "required_fixes": {
      "type": "array",
      "items": { "type": "string" }
    },
    "risk_flags": {
      "type": "array",
      "items": { "type": "string" }
    }
  },
  "required": [
    "experiment_id",
    "verdict",
    "allows_auto_continue",
    "reasons",
    "evidence_checked",
    "required_fixes",
    "risk_flags"
  ],
  "additionalProperties": false
}
```
