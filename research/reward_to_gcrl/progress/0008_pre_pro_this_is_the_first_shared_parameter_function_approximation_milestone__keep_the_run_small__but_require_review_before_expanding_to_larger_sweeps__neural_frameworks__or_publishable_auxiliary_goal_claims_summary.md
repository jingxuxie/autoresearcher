## Current Status

The project is active with no current blocker and `protected_file_drift: false`. Reviewed evidence now reaches `0008`.

The small-tabular evidence is strong for the core estimator story: deterministic soft terminal marginalization preserves the normalized-Q scaling relationship while removing terminal-sampling variance. RiverSwim results also support the claim under controlled and non-oracle coverage regimes.

The broader research goal is **not solved**. The next milestone is the first shared-parameter/function-approximation-style test: a CPU-only low-rank factorized SSM on tiny FourRooms. No neural framework, large environment, or auxiliary-representation claim has been validated yet.

## Experiment Ledger

| Iteration | Experiment | Review | Key Outcome |
|---|---|---:|---|
| `0001` | One-state variance diagnostic | `weak_pass` | Sampled and soft means matched; soft removed terminal variance. |
| `0002` | Audited CliffWalking equivalence | `weak_pass` | Exact soft scaling matched normalized Q. |
| `0003` | CliffWalking sampled-vs-soft | `weak_pass` | Variance result held; Bellman residual favored soft, but value-error evidence was mixed. |
| `0004` | Nondegenerate 5-state chain plus drift audit | `weak_pass` | Drift cleared; soft improved Bellman/value error and policy success over sampled. |
| `0005` | RiverSwim with exact-Q-guided behavior | `pass` | Strong controlled propagation result; soft residual dominance in all runs. |
| `0006` | RiverSwim with non-oracle behavior | `pass` | Variance result held; coverage limitations were exposed. |
| `0007` | RiverSwim coverage dose-response | `pass` | Adequate coverage favored soft on Bellman/value error; starved runs remained coverage-limited. |
| `0008` | Tabular vector SSM on tiny FourRooms | `pass` | Real-state goal slices were correct and did not perturb the `g_plus` slice. |

## Main Findings

Confirmed findings:

- `0001` validated the estimator premise: matching sampled/soft means and zero/negligible soft terminal variance.
- `0002` confirmed normalized-Q scaling equivalence in audited CliffWalking.
- `0004` repaired the degenerate task issue with a nondegenerate 5-state chain and accepted drift audit.
- `0005` showed in 6-state RiverSwim that sampled target means matched deterministic soft marginal targets in all 30 runs, sampled variance exceeded soft variance in all 30, and soft residual dominance held in all runs.
- `0006` removed exact-Q-guided behavior; sampled targets remained unbiased and higher variance, but coverage determined whether learning metrics were interpretable.
- `0007` ran 120 RiverSwim coverage-regime runs; sampled means matched soft marginal targets in all runs, and sampled terminal variance exceeded soft variance in all runs.
- In `0007`, adequate-coverage RiverSwim runs favored soft on mean Bellman residual and mean value error.
- `0008` showed `max_abs_vector_gplus_minus_terminal_only = 0`.
- `0008` showed `max_abs_vector_gplus_scaled_minus_q_norm = 1.1102230246251565e-16`.
- `0008` real-state goal slices had max value error `0`, min greedy goal success rate `1.0`, and zero goal-policy disagreement versus exact references.

Important negative results:

- `0002` and `0003` CliffWalking raw success was degenerate under the chosen normalization.
- `0003` value-error evidence was mixed and weaker than Bellman-residual evidence.
- `0006` had half of runs coverage-starved.
- In coverage-starved `0006` runs, soft could have lower Bellman residual but worse value error.
- `0007` still used hand-designed non-oracle behavior policies; broader data-collection policies remain untested.
- `0008` is an exact/full-sweep deterministic sanity check, not sampled learning or function approximation.

## Limitations And Risks

- All accepted evidence is still tiny, CPU-only, tabular evidence.
- Matched-stream RiverSwim tests isolate estimator quality but do not prove full online exploration robustness.
- Coverage remains a key precondition for learning-performance claims.
- The `0008` vector SSM has independent tabular slices, so it cannot show auxiliary representation benefit.
- Reward-policy comparison in `0008` has many tie states, although disagreement is zero on comparable non-tie states.
- No low-rank/shared-parameter, neural, offline fitted-learning, or larger-environment result has passed review.

## Recommended Next Human Decision

Approve `0009` as a **small checkpointed shared-parameter test**, not a broad neural experiment.

Recommended scope:

- CPU-only NumPy low-rank factorized SSM on tiny FourRooms.
- Compare terminal-only `g_plus` training against combined real-state-plus-`g_plus` auxiliary training.
- Use matched replay datasets and identical optimizer budgets.
- Report oracle value error, Bellman residual, policy disagreement, reward-task return/success, state-goal reachability accuracy, and coverage diagnostics.
- Require review before expanding to larger sweeps, PyTorch/JAX, GPU, or publishable auxiliary-goal claims.

## Files To Inspect

- `research/reward_to_gcrl/results/0008_result.json`
- `research/reward_to_gcrl/results/0008_summary.md`
- `research/reward_to_gcrl/reviews/0008_review.md`
- `research/reward_to_gcrl/artifacts/0008/run_fourrooms_vector_ssm.py`
- `research/reward_to_gcrl/decisions/0009_decision.md`
- `research/reward_to_gcrl/results/0007_result.json`
- `research/reward_to_gcrl/reviews/0007_review.md`
- `research/reward_to_gcrl/results/0006_result.json`
- `research/reward_to_gcrl/reviews/0006_review.md`
- `research/reward_to_gcrl/artifacts/0004/protected_file_drift_audit.json`