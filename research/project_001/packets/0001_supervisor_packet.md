# Supervisor Context: project_001

## Requested action

Choose continue, pivot, stop, or needs_human. If this is iteration 0 with no prior result, propose the first small experiment when the charter is specific enough. If continuing, propose exactly one small experiment.


## Project charter

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



## Current state

```json
{
  "best_primary_metric": null,
  "human_review_required": false,
  "iteration": 0,
  "last_decision": "start",
  "last_pro_review_iteration": 0,
  "no_progress_rounds": 0,
  "notes": [],
  "primary_metric": null,
  "status": "active"
}
```


## Latest result JSON

```json
_Missing._
```


## Latest summary

_Missing._

## Latest review JSON

```json
_Missing._
```


## Last decisions



## Stop, pivot, continue rules

- For iteration 0, a missing latest result is expected and is not by itself a reason to stop.
- After iteration 0, stop or choose needs_human on missing or invalid result files.
- Stop on repeated invalid, negative, or low-value results.
- Pivot only when evidence weakens the original idea but reveals a nearby testable idea.
- Continue only for one cheap, high-information experiment.
- Choose needs_human for ambiguity, expensive work, missing artifacts, or risky pivots.


## Next experiment id

Use `0001` as the exact `next_experiment.experiment_id` if you choose continue.


## First-iteration rule

No prior result is expected for iteration 0. Do not choose needs_human solely because latest result, summary, and review are missing.
