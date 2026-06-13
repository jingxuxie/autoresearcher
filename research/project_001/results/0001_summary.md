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
