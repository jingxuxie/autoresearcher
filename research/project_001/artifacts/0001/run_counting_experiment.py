#!/usr/bin/env python3
"""Run experiment 0001: weak zero baseline vs exact counting."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List


EXPERIMENT_ID = "0001"
PROJECT = "project_001"

COMMANDS_RUN = [
    "find . -maxdepth 4 -type f | sort",
    "find research -maxdepth 4 -type d | sort",
    "sed -n '1,220p' schemas/result.schema.json",
    "sed -n '1,240p' scripts/validate_artifacts.py",
    "ls -la research/project_001/results research/project_001/artifacts",
    "mkdir -p research/project_001/artifacts/0001",
    "python3 research/project_001/artifacts/0001/run_counting_experiment.py",
    "python3 scripts/validate_artifacts.py --repo-root . --json research/project_001/results/0001_result.json --schema schemas/result.schema.json --check-result-artifacts",
]


DATASET = [
    {
        "example_id": "ex_001",
        "items": ["red", "blue", "red", "green"],
        "target": "red",
        "label": 2,
    },
    {
        "example_id": "ex_002",
        "items": ["triangle", "circle", "square", "circle"],
        "target": "circle",
        "label": 2,
    },
    {
        "example_id": "ex_003",
        "items": ["cat", "cat", "dog", "cat"],
        "target": "cat",
        "label": 3,
    },
    {
        "example_id": "ex_004",
        "items": ["north", "south", "east"],
        "target": "east",
        "label": 1,
    },
    {
        "example_id": "ex_005",
        "items": ["aa", "bb", "aa", "cc", "aa", "aa"],
        "target": "aa",
        "label": 4,
    },
    {
        "example_id": "ex_006",
        "items": ["m", "n", "m", "o", "n"],
        "target": "n",
        "label": 2,
    },
]


def always_zero(_: Dict[str, Any]) -> int:
    return 0


def exact_count(example: Dict[str, Any]) -> int:
    return sum(1 for item in example["items"] if item == example["target"])


def accuracy(records: List[Dict[str, Any]], key: str) -> float:
    correct = sum(1 for record in records if record[f"{key}_correct"])
    return correct / len(records)


def write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")


def main() -> int:
    repo_root = Path(__file__).resolve().parents[4]
    artifact_dir = repo_root / "research" / PROJECT / "artifacts" / EXPERIMENT_ID
    result_dir = repo_root / "research" / PROJECT / "results"
    artifact_dir.mkdir(parents=True, exist_ok=True)
    result_dir.mkdir(parents=True, exist_ok=True)

    records = []
    for example in DATASET:
        computed_label = exact_count(example)
        if computed_label != example["label"]:
            raise ValueError(f"{example['example_id']} has inconsistent label")
        baseline_prediction = always_zero(example)
        corrected_prediction = exact_count(example)
        records.append(
            {
                **example,
                "baseline_method": "always_predict_zero",
                "baseline_prediction": baseline_prediction,
                "baseline_correct": baseline_prediction == example["label"],
                "corrected_method": "exact_target_item_count",
                "corrected_prediction": corrected_prediction,
                "corrected_correct": corrected_prediction == example["label"],
            }
        )

    num_examples = len(records)
    baseline_correct = sum(1 for record in records if record["baseline_correct"])
    corrected_correct = sum(1 for record in records if record["corrected_correct"])
    baseline_accuracy = accuracy(records, "baseline")
    corrected_accuracy = accuracy(records, "corrected")
    accuracy_delta = corrected_accuracy - baseline_accuracy
    success = corrected_accuracy > baseline_accuracy

    raw_predictions = {
        "experiment_id": EXPERIMENT_ID,
        "dataset_name": "tiny_deterministic_counting_positive_control",
        "records": records,
    }
    metrics = {
        "experiment_id": EXPERIMENT_ID,
        "num_examples": num_examples,
        "baseline_method": "always_predict_zero",
        "baseline_correct": baseline_correct,
        "baseline_accuracy": baseline_accuracy,
        "corrected_method": "exact_target_item_count",
        "corrected_correct": corrected_correct,
        "corrected_accuracy": corrected_accuracy,
        "accuracy_delta": accuracy_delta,
        "success_criteria_met": success,
    }

    raw_predictions_path = artifact_dir / "raw_predictions.json"
    metrics_path = artifact_dir / "metrics.json"
    write_json(raw_predictions_path, raw_predictions)
    write_json(metrics_path, metrics)

    artifact_paths = [
        f"research/{PROJECT}/artifacts/{EXPERIMENT_ID}/raw_predictions.json",
        f"research/{PROJECT}/artifacts/{EXPERIMENT_ID}/metrics.json",
        f"research/{PROJECT}/artifacts/{EXPERIMENT_ID}/run_counting_experiment.py",
    ]
    result = {
        "experiment_id": EXPERIMENT_ID,
        "status": "completed" if success else "failed",
        "claim_tested": (
            "An exact target-item counting method achieves higher accuracy than "
            "a deliberately weak always-zero baseline on the same deterministic "
            "synthetic counting examples."
        ),
        "commands_run": COMMANDS_RUN,
        "metrics": {
            "num_examples": num_examples,
            "corrected_method": "exact_target_item_count",
            "corrected_correct": corrected_correct,
            "corrected_accuracy": corrected_accuracy,
            "baseline_accuracy": baseline_accuracy,
            "accuracy_delta": accuracy_delta,
            "success_criteria_met": success,
        },
        "baseline_metrics": {
            "baseline_method": "always_predict_zero",
            "baseline_correct": baseline_correct,
            "baseline_accuracy": baseline_accuracy,
        },
        "artifacts": artifact_paths,
        "interpretation": (
            "The corrected exact-counting method counted every target occurrence "
            f"correctly ({corrected_correct}/{num_examples}), while the weak "
            f"always-zero baseline was correct on {baseline_correct}/{num_examples}. "
            f"The corrected accuracy exceeded the baseline by {accuracy_delta:.3f}."
        ),
        "known_failures": [] if success else ["Corrected accuracy did not exceed baseline accuracy."],
        "next_questions": [
            "Does the same exact-counting implementation remain correct when examples include zero-count labels?",
            "How should this positive control be extended to a nontrivial counting method?",
        ],
    }
    write_json(result_dir / f"{EXPERIMENT_ID}_result.json", result)

    summary = f"""# Experiment {EXPERIMENT_ID} Summary

## Setup

This deterministic positive-control experiment used {num_examples} tiny synthetic counting examples. Each example specifies a list of items, one target item, and the known count label.

## Commands Run

```bash
{chr(10).join(COMMANDS_RUN)}
```

## Methods

- Baseline: always predict `0`.
- Corrected method: count exact matches to the target item in the example list.

## Raw Metrics

- Baseline accuracy: {baseline_accuracy:.6f} ({baseline_correct}/{num_examples})
- Corrected accuracy: {corrected_accuracy:.6f} ({corrected_correct}/{num_examples})
- Accuracy delta: {accuracy_delta:.6f}

## Artifacts

- `research/{PROJECT}/artifacts/{EXPERIMENT_ID}/raw_predictions.json`
- `research/{PROJECT}/artifacts/{EXPERIMENT_ID}/metrics.json`
- `research/{PROJECT}/artifacts/{EXPERIMENT_ID}/run_counting_experiment.py`

## Outcome

Success criteria were {'met' if success else 'not met'}: corrected accuracy is strictly greater than baseline accuracy on the same deterministic examples.
"""
    (result_dir / f"{EXPERIMENT_ID}_summary.md").write_text(summary)

    print(json.dumps(metrics, indent=2, sort_keys=True))
    return 0 if success else 1


if __name__ == "__main__":
    raise SystemExit(main())
