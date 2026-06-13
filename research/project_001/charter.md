# Project 001 Charter

## Research goal

Positive-control smoke project for the autoresearcher loop.

Evaluate whether a tiny, deterministic experiment can detect and report an obvious improvement over a weak baseline. This project is intentionally simple so Phase 1 can validate orchestration, result schemas, reviewer behavior, and stopping rules without expensive compute.

## Main hypothesis

A simple corrected method should outperform a deliberately weak baseline on a small synthetic counting task.

## Primary metric

Accuracy on a deterministic toy dataset.

## Success criteria

- The executor creates a tiny reproducible experiment that runs in under 30 minutes.
- The result JSON reports exact commands run.
- The corrected method accuracy is higher than the baseline accuracy on the same data.
- Raw metrics are saved in `research/project_001/artifacts/NNNN/` when useful.

## Failure criteria

- Missing or invalid result JSON.
- No comparable baseline.
- No exact commands recorded.
- Claims of improvement without raw metrics.
- Any experiment that needs large dependencies, large data, or long training.

## Notes for adapting this project

Replace this charter with your actual research idea when you are ready. Keep the same structure so the supervisor, executor, and reviewer can reason against explicit criteria.

