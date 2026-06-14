## Current Status

The project is active with `protected_file_drift: false` after the `0004` drift audit. There is no current blocker, and the environment remains ready.

Reviewed evidence now includes six completed iterations. The strongest current evidence is that deterministic soft terminal marginalization removes terminal-sampling variance and matches normalized-Q scaling in small tabular settings. Recent RiverSwim results extend this beyond CliffWalking, but the research goal is **not fully solved**: evidence is still tabular, small-scale, and coverage-sensitive, with no auxiliary-goal or function-approximation validation.

## Experiment Ledger

| Iteration | Experiment | Review | Key Outcome |
|---|---|---:|---|
| `0001` | One-state variance diagnostic | `weak_pass` | Sampled and soft means matched; soft removed terminal-sampling variance. |
| `0002` | Audited CliffWalking equivalence | `weak_pass` | Exact scaling equivalence passed; paired scaled `M` matched normalized Q on visited pairs. |
| `0003` | CliffWalking sampled-vs-soft | `weak_pass` | Variance result held; Bellman residual favored soft, but value-error evidence was mixed. |
| `0004` | Repaired 5-state nondegenerate chain plus drift audit | `weak_pass` | Drift cleared as harmless; accepted evidence; soft beat sampled on Bellman/value and policy success. |
| `0005` | RiverSwim with exact-Q-guided behavior | `pass` | Strong controlled propagation result; soft residual dominance in all runs. |
| `0006` | RiverSwim with non-oracle behavior streams | `pass` | Variance result held without oracle behavior, but many runs were coverage-starved. |

## Main Findings

Confirmed findings:

- `0001` validated the basic estimator premise: sampled and soft terminal targets had matching means, while soft terminal variance was zero/negligible.
- `0002` confirmed tabular scaling equivalence in audited CliffWalking: exact soft scaling matched normalized Q below `1e-6`.
- `0003` showed sampled conditional variance exceeded zero soft variance in all 30 CliffWalking runs; soft had lower final Bellman residual in 26 of 30 runs.
- `0004` resolved the prior protected-file drift as harmless and accepted the repaired nondegenerate 5-state chain result.
- `0004` directly compared sampled targets to deterministic soft targets from the same learner state, with sampled variance higher and soft lower on mean Bellman residual and value error.
- `0004` produced nondegenerate evaluation: soft policies had mean raw return `1` and success rate `1`, while sampled policies had mean raw return `0` and success rate `0`.
- `0005` gave a strong RiverSwim controlled-propagation result: sampled target means matched deterministic soft marginal targets in all 30 runs, sampled variance exceeded soft variance in all 30 runs, and soft residual dominance held in all runs.
- `0006` removed exact-Q-guided behavior. The sampled targets remained unbiased within tolerance and higher variance, confirming the estimator story under non-oracle streams.

Important negative results:

- `0002`/`0003` CliffWalking raw success was degenerate: mean raw return `-200`, success rate `0`.
- `0003` value-error dominance was weak and did not improve at `gamma = 0.995`.
- `0005` used exact-Q-guided behavior, so it was not an online exploration test.
- `0006` had 30 coverage-starved runs, about half the runs under the predeclared threshold.
- Under poor coverage in `0006`, soft could have lower Bellman residual but worse value error than sampled.

## Limitations And Risks

- All accepted evidence remains CPU-only tabular evidence on tiny environments.
- RiverSwim results depend strongly on coverage; non-oracle exploration exposed coverage-starved regimes.
- `0006` behavior policies were simple state-independent random policies; broader non-oracle exploration behavior is untested.
- `0005` and `0006` use matched logged streams, so they isolate estimator quality more than full online control robustness.
- No auxiliary real-state goals, neural function approximation, FourRooms, larger RiverSwim chains, or offline fitted learning have been tested.
- A positive tabular estimator result should not yet be treated as evidence that representation sharing will help.

## Recommended Next Human Decision

Decide whether the `0006` coverage caveat is sufficiently bounded.

Recommended next step: run one more small tabular RiverSwim follow-up with non-oracle but coverage-controlled behavior policies, separating adequate-coverage and starved regimes more cleanly. If that confirms the same pattern, move next to the tabular auxiliary state-goal milestone.

Do not move to neural approximation or larger environments yet.

## Files To Inspect

- `research/reward_to_gcrl/results/0006_result.json`
- `research/reward_to_gcrl/results/0006_summary.md`
- `research/reward_to_gcrl/reviews/0006_review.md`
- `research/reward_to_gcrl/artifacts/0006/run_riverswim_nonoracle.py`
- `research/reward_to_gcrl/results/0005_result.json`
- `research/reward_to_gcrl/reviews/0005_review.md`
- `research/reward_to_gcrl/results/0004_result.json`
- `research/reward_to_gcrl/reviews/0004_review.md`
- `research/reward_to_gcrl/artifacts/0004/protected_file_drift_audit.json`
- `research/reward_to_gcrl/decisions/0006_decision.md`