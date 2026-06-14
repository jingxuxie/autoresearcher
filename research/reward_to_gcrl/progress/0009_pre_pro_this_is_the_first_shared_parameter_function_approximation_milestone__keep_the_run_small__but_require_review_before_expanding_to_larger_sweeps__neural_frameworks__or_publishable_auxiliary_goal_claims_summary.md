## Current Status

The project is active with no current blocker and `protected_file_drift: false`. Reviewed evidence now reaches `0009`.

The core tabular estimator story is well supported: soft terminal marginalization preserves normalized-Q scaling and removes terminal-sampling variance across one-state, CliffWalking, repaired chain, RiverSwim, and tabular FourRooms checks.

The broader research goal is **not solved**. The first shared-parameter auxiliary-goal test in `0009` produced valid **negative transfer** evidence: real-state auxiliary goals did not help the `g_plus` reward head under the tested low-rank setup.

## Experiment Ledger

| Iteration | Experiment | Review | Key Outcome |
|---|---|---:|---|
| `0001` | One-state variance diagnostic | `weak_pass` | Sampled/soft means matched; soft removed terminal variance. |
| `0002` | Audited CliffWalking equivalence | `weak_pass` | Exact soft scaling matched normalized Q. |
| `0003` | CliffWalking sampled-vs-soft | `weak_pass` | Variance held; Bellman residual favored soft, value-error evidence mixed. |
| `0004` | Nondegenerate 5-state chain plus drift audit | `weak_pass` | Drift cleared; soft improved Bellman/value error and policy success. |
| `0005` | RiverSwim with exact-Q-guided behavior | `pass` | Strong controlled propagation result. |
| `0006` | RiverSwim with non-oracle behavior | `pass` | Variance held; coverage limits exposed. |
| `0007` | RiverSwim coverage dose-response | `pass` | Adequate coverage favored soft; starved runs remained coverage-limited. |
| `0008` | Tabular vector SSM on FourRooms | `pass` | Real-state slices were correct and did not perturb `g_plus`. |
| `0009` | Low-rank shared FourRooms auxiliary test | `weak_pass` | Valid negative result: auxiliary training worsened reward-head metrics. |

## Main Findings

Confirmed positive findings:

- `0001` established the estimator premise: matching sampled/soft means and zero/negligible soft terminal variance.
- `0002` confirmed normalized-Q scaling equivalence in audited CliffWalking.
- `0004` accepted a nondegenerate chain result where soft improved Bellman/value error and policy success over sampled.
- `0005`-`0007` extended the sampled-vs-soft result to 6-state RiverSwim, including non-oracle and coverage-controlled regimes.
- `0007` found sampled target means matched deterministic soft marginal targets in all 120 runs, and sampled terminal-sampling variance exceeded soft variance in all 120 runs.
- `0008` showed `max_abs_vector_gplus_minus_terminal_only = 0` and `max_abs_vector_gplus_scaled_minus_q_norm = 1.1102230246251565e-16`.
- `0008` real-state goal slices had max value error `0`, min greedy goal success rate `1.0`, and zero goal-policy disagreement versus exact references.

Confirmed `0009` findings:

- The `0009` script is CPU-only NumPy, uses the audited tiny FourRooms transition hash from `0008`, and does not use neural frameworks, GPU, larger environments, or large dependencies.
- The low-rank model genuinely shares parameters: `M_hat(s,a,g)=sigmoid(u_sa dot v_g + b_g)`.
- Terminal-only and combined auxiliary variants used matched replay datasets, seeds, batch schedules, optimizer steps, rank, learning rate, and evaluation protocol.
- Replay coverage was adequate for all 10 seeds: visited state-action fraction `1.0`.
- The terminal-only baseline had mean `g_plus` Bellman residual `0.0009558486`, mean scaled value error `0.0731219459`, and mean reward success rate `0.5384615385`.
- Combined auxiliary training substantially worsened `g_plus` value error, Bellman residual, reward-policy disagreement, reward success, and real-goal diagnostics.
- The result is correctly labeled `negative_transfer`; auxiliary-goal benefit is **not supported**.

## Limitations And Risks

- `0009` is one predeclared low-rank setting: rank `4`, learning rate `0.05`, and `4000` steps. It should not be generalized across ranks, optimizers, losses, or auxiliary weights.
- The combined model collapse may reflect optimizer or loss-scaling issues, not a general impossibility of auxiliary goals.
- Replay used uniform random state-action resets, which gives strong coverage but is less realistic than trajectory-only offline data.
- Both terminal-only and combined models have imperfect reward policies.
- All evidence remains tiny-scale and mostly tabular or NumPy low-rank; no neural, larger FourRooms, MuJoCo, AntMaze, OGBench, or image setting has been tested.
- A publishable auxiliary-goal claim would be premature.

## Recommended Next Human Decision

Treat auxiliary real-state goals as **unsupported for now**.

Recommended decision: pause broad expansion and choose one of two narrow paths:

1. Stop the auxiliary-goal thread and write up the current result as: strong small-tabular estimator evidence plus negative low-rank auxiliary evidence.
2. Run one tightly predeclared diagnostic to determine whether `0009` failed because of optimizer/loss scaling, not because auxiliary goals are inherently harmful.

Do not move to PyTorch/JAX, GPU, larger sweeps, or publishable auxiliary-goal claims before that decision.

## Files To Inspect

- `research/reward_to_gcrl/results/0009_result.json`
- `research/reward_to_gcrl/results/0009_summary.md`
- `research/reward_to_gcrl/reviews/0009_review.md`
- `research/reward_to_gcrl/artifacts/0009/run_fourrooms_lowrank_auxiliary.py`
- `research/reward_to_gcrl/decisions/0009_pro_decision.md`
- `research/reward_to_gcrl/results/0008_result.json`
- `research/reward_to_gcrl/reviews/0008_review.md`
- `research/reward_to_gcrl/results/0007_result.json`
- `research/reward_to_gcrl/reviews/0007_review.md`
- `research/reward_to_gcrl/artifacts/0004/protected_file_drift_audit.json`