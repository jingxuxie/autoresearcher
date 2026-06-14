## Current Status

The project is active, but the current gate is **evidence integrity**, not a new scientific experiment. The latest `0004` review verdict is `fail` with `allows_auto_continue: false` because `protected_file_drift` remains unresolved.

The research goal is **not solved**. Accepted reviewed evidence from `0001`-`0003` supports the variance motivation and tabular scaling equivalence, but `0004` cannot be accepted until the drift audit requirement is satisfied.

## Experiment Ledger

| Iteration | Experiment | Review | Evidence Status | Key Outcome |
|---|---|---:|---|---|
| `0001` | One-state sampled-vs-soft terminal target diagnostic | `weak_pass` | Accepted, limited | Sampled and soft means matched; soft removed terminal-sampling variance. |
| `0002` | Audited local CliffWalking tabular equivalence | `weak_pass` | Accepted, limited | Exact DP scaling equivalence passed; paired scaled soft values matched normalized Q on sufficiently visited pairs. |
| `0003` | Sampled augmented vs soft update on audited CliffWalking | `weak_pass` | Accepted, ambiguous | Sampled variance was higher; soft Bellman residual was better in most runs, but value-error evidence was mixed. |
| `0004` | Repaired nondegenerate sampled-vs-soft diagnostic / drift gate | `fail` | Not accepted | Files validate structurally, but no drift audit or `drift_status` was recorded. |

## Main Findings

Confirmed from accepted reviewed evidence:

- `0001` showed sampled and soft target means matched while soft terminal variance was zero/negligible.
- `0001` exposed rare `g_plus` events, with sampled counts from `0.48` to `1005.02` per 10k transitions.
- `0001` finite-MDP scaling equivalence passed with `max_abs_error_scaled_f_vs_q = 3.9475168023273e-08`.
- `0002` exact DP scaling equivalence passed with `max_abs_error_scaled_f_vs_q = 9.711982329463353e-10`.
- `0002` paired learning matched scaled soft `M` to normalized `Q` within `5.115907697472721e-13` on sufficiently visited state-action pairs.
- `0003` sampled conditional variance exceeded zero soft terminal-sampling variance in all 30 runs.
- `0003` soft had lower final Bellman residual in 26 of 30 runs.

Reviewed but **not accepted** for `0004`:

- Required `0004` result, summary, and artifact directory are present.
- Existing `0004_result.json` validates against schema, and declared artifact paths validate.
- The scientific metrics from the prior `0004` run look promising, but the run does not satisfy the current drift-resolution plan.
- No `protected_file_drift_audit.json` exists under `research/reward_to_gcrl/artifacts/0004/`.
- `0004_result.json` has no top-level or metrics-level `drift_status`.
- `state.json` still reports `protected_file_drift: true`.
- `0004_worktree_guard.json` records protected drift on `autoresearcher.yaml`.

## Limitations And Risks

- `0004` cannot be treated as accepted evidence until protected file drift is explicitly adjudicated.
- Current scoped git status may no longer show `autoresearcher.yaml` modified, but that fact is not recorded in an audit artifact or result field.
- `0002` and `0003` remain limited by degenerate CliffWalking normalization: raw return `-200` and success rate `0.0`.
- `0003` value-error evidence was mixed despite stronger Bellman-residual evidence.
- No accepted RiverSwim, auxiliary-goal, neural, or larger-environment result exists.
- Proceeding beyond `0004` now would violate the current evidence-integrity gate.

## Recommended Next Human Decision

Do not start RiverSwim, auxiliary goals, neural approximation, or larger experiments yet.

The next step should be to resolve `0004` evidence integrity:

- Write a protected-file drift audit identifying affected files, current status, hashes if available, impact assessment, and final `drift_status`.
- Add `drift_status` and a verdict to `0004_result.json`: `accepted_evidence`, `superseded_by_clean_rerun`, `rejected_due_to_drift`, or `inconclusive`.
- If drift is stale or harmless, revalidate the existing `0004` result and artifact paths and record that validation.
- If drift is real or unresolved, rerun the same 5-state CPU-only diagnostic from a clean/adjudicated state.

Only after `0004` is accepted or superseded should the loop decide whether to move to RiverSwim.

## Files To Inspect

- `research/reward_to_gcrl/reviews/0004_review.md`
- `research/reward_to_gcrl/results/0004_result.json`
- `research/reward_to_gcrl/results/0004_summary.md`
- `research/reward_to_gcrl/artifacts/0004/`
- `research/reward_to_gcrl/decisions/0004_worktree_guard.json`
- `research/reward_to_gcrl/state.json`
- `research/reward_to_gcrl/decisions/0004_review4_pro_decision.md`
- `research/reward_to_gcrl/reviews/0003_review.md`
- `research/reward_to_gcrl/results/0003_result.json`