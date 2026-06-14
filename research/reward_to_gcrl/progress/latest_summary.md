## Current Status

The project is **paused** with `human_review_required: true`. The loop hit the retry limit after 3 failures, with the latest failure recorded as reviewer verdict `needs_human`.

Iteration `0001` is the only accepted experimental evidence so far. It received a reviewed `weak_pass` for the one-state terminal-target variance diagnostic. The broader research goal is **not solved**: the required CliffWalking tabular equivalence and policy-disagreement criteria remain unmet.

A pending ChatGPT Pro checkpoint for `0002_review2` is blocked with `response_parse_failed` and `manual_fallback: true`.

## Experiment Ledger

| Iteration | Status | Review | Evidence Use | Outcome |
|---|---|---:|---|---|
| `0001` | Completed | `weak_pass` | Accepted, limited | One-state sampled-vs-soft diagnostic passed reviewed checks. |
| `0002` | Blocked/failed | `needs_human` | Not accepted as equivalence evidence | Planned CliffWalking test did not run because `CliffWalking-v0` is rejected by Gymnasium 1.3.0. |

## Main Findings

Confirmed from reviewed `0001` evidence:

- The sweep covered all 16 planned `gamma` and `r_bar` combinations.
- Sampled Bernoulli terminal targets matched expected means within the stricter reviewed 3-SE check; max z-score was `2.211`.
- Soft terminal target variance was zero/negligible by construction.
- Sampled `g_plus` events became rare at high `gamma`; counts ranged from `0.48` to `1005.02` per 10k transitions.
- Maximum sampled target variance was `0.090401347996`.
- Tiny finite-MDP scaling equivalence passed: `max_abs_error_scaled_f_vs_q = 3.9475168023273e-08`, below the `1e-6` threshold.

Confirmed from reviewed `0002` evidence:

- Required result, summary, and artifact files exist and validate structurally.
- The planned DP oracle and paired tabular-learning comparison did **not** run.
- `gym.make('CliffWalking-v0')` raises `gymnasium.error.DeprecatedEnv` under Gymnasium `1.3.0`.
- No exact-DP scaled value error, greedy policy disagreement, or 10-seed paired-learning metrics were produced.

## Limitations And Risks

- `0002` is a compatibility/blocker result, not evidence for or against the soft successor equivalence hypothesis.
- The charter’s early positive evidence criteria are incomplete because CliffWalking equivalence and low policy disagreement are still untested.
- Human approval is needed to choose the intended CliffWalking semantics: `CliffWalking-v1`, direct `CliffWalkingEnv(is_slippery=False)`, or `tabular/CliffWalking-v0` with approved dependency handling.
- Prior reporting issues should not be copied forward: the `0001` executor text used 6-SE tolerance despite the 3-SE plan, variance lacked an explicit pass flag, and some scripts hard-code `commands_run`.
- The `0002` artifact directory contains timeout/retry files not listed in final result artifacts.

## Recommended Next Human Decision

Resolve the `0002` blocker by explicitly approving the CliffWalking environment semantics, then rerun the full CPU-only tabular equivalence diagnostic.

The rerun should require exact-DP oracle metrics, `M_plus / (1 - gamma)` versus normalized Q-learning value error, greedy policy disagreement, 10-seed paired-learning metrics, explicit terminal-mask diagnostics, and accurate command recording.

Do not proceed to RiverSwim, FourRooms, sampled baselines, auxiliary goals, neural approximation, or larger experiments until this CliffWalking gate passes.

## Files To Inspect

- `research/reward_to_gcrl/results/0001_result.json`
- `research/reward_to_gcrl/results/0001_summary.md`
- `research/reward_to_gcrl/reviews/0001_review.md`
- `research/reward_to_gcrl/results/0002_result.json`
- `research/reward_to_gcrl/results/0002_summary.md`
- `research/reward_to_gcrl/reviews/0002_review.md`
- `research/reward_to_gcrl/artifacts/0002/compatibility_check.json`
- `research/reward_to_gcrl/artifacts/0002/check_cliffwalking_v0_compatibility.py`
- `research/reward_to_gcrl/decisions/0002_decision.md`
- `research/reward_to_gcrl/decisions/0002_review2_pro_blocker.json`