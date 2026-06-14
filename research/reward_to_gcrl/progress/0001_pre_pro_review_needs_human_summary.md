## Current Status

The project is **paused** with `human_review_required: true` after the retry limit was reached: 3 failures, latest due to reviewer verdict `needs_human`.

Iteration `0001` produced a reviewed `weak_pass` for the one-state variance diagnostic. The broader research goal is **not solved** because the required CliffWalking tabular equivalence and policy-disagreement evidence has not been produced.

The attempted `0002` CliffWalking diagnostic is **not valid evidence** for or against the hypothesis. It stopped at an environment compatibility failure before running the planned DP oracle or paired tabular-learning comparison.

## Experiment Ledger

| Iteration | Status | Review | Accepted Evidence? | Summary |
|---|---|---:|---:|---|
| `0001` | Completed | `weak_pass` | Yes, limited | One-state sampled-vs-soft terminal target diagnostic passed reviewed checks. |
| `0002` | Failed/blocker | `needs_human` | No | Planned CliffWalking equivalence test did not run because `gym.make('CliffWalking-v0')` is rejected under Gymnasium 1.3.0. |

## Main Findings

Confirmed from reviewed `0001` evidence:

- The one-state sweep covered all 16 planned `gamma` and `r_bar` combinations.
- Sampled Bernoulli terminal targets and deterministic soft targets matched expected means within the reviewed stricter 3-SE check; max z-score was `2.211`.
- Soft terminal target variance was zero/negligible by construction.
- Sampled `g_plus` events became rare at high `gamma`; event counts ranged from `0.48` to `1005.02` per 10k samples.
- Maximum sampled target variance was `0.090401347996`.
- Tiny finite-MDP scaling equivalence passed: `max_abs_error_scaled_f_vs_q = 3.9475168023273e-08`, below the `1e-6` tolerance.

Confirmed from reviewed `0002` evidence:

- Required `0002` result files and artifacts exist and validate structurally.
- The planned learning/equivalence experiment did **not** run.
- `gym.make('CliffWalking-v0')` raises `gymnasium.error.DeprecatedEnv` under Gymnasium `1.3.0`.
- No exact-DP value error, policy disagreement, or 10-seed paired-learning metrics were produced.

## Limitations And Risks

- The charter’s early positive evidence criteria are not yet satisfied because CliffWalking equivalence and low policy disagreement remain untested.
- `0002` cannot be interpreted as a negative result about soft successor learning; it is only an environment-id compatibility failure.
- The next experiment needs an explicit human-approved CliffWalking semantic choice: `CliffWalking-v1`, direct `CliffWalkingEnv(is_slippery=False)`, or `tabular/CliffWalking-v0` with approved dependency handling.
- Prior reporting risks remain: `0001` used a 6-SE tolerance in executor text despite passing the stricter 3-SE review; variance lacked an explicit pass flag; some scripts hard-code `commands_run`.
- The loop is paused after repeated failures, including one executor timeout and repeated `needs_human` review outcomes.

## Recommended Next Human Decision

Approve one exact CliffWalking environment semantic for the rerun of `0002`. The cleanest next step is to explicitly permit a Gymnasium-supported CliffWalking equivalent, then rerun the full CPU-only tabular diagnostic with:

- exact-DP oracle,
- `M_plus / (1 - gamma)` versus normalized Q-learning value error,
- greedy policy disagreement,
- 10-seed paired-learning metrics,
- explicit terminal-mask diagnostics,
- exact commands and non-hard-coded reporting.

Do not move to RiverSwim, FourRooms, auxiliary goals, sampled baselines, or neural approximation until this gate passes.

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