## Current Status

The project is active with no current blocker and `protected_file_drift: false`.

The core soft-terminal estimator story is now well supported in small tabular settings: soft marginalization preserves normalized-Q scaling and removes terminal-sampling variance. However, the auxiliary-goal/shared-representation hypothesis is **not supported** by the first low-rank FourRooms tests.

The research goal is **not solved**. The estimator component looks promising in tiny tabular settings, but the auxiliary representation direction has produced negative evidence so far.

## Experiment Ledger

| Iteration | Experiment | Review | Key Outcome |
|---|---|---:|---|
| `0001` | One-state variance diagnostic | `weak_pass` | Sampled/soft means matched; soft removed terminal variance. |
| `0002` | Audited CliffWalking equivalence | `weak_pass` | Exact soft scaling matched normalized Q. |
| `0003` | CliffWalking sampled-vs-soft | `weak_pass` | Variance held; value-error evidence mixed. |
| `0004` | Nondegenerate 5-state chain plus drift audit | `weak_pass` | Drift cleared; soft improved Bellman/value and success. |
| `0005` | RiverSwim with exact-Q-guided behavior | `pass` | Strong controlled propagation result. |
| `0006` | RiverSwim non-oracle behavior | `pass` | Variance held; coverage limits exposed. |
| `0007` | RiverSwim coverage dose-response | `pass` | Adequate coverage favored soft; starved runs remained coverage-limited. |
| `0008` | Tabular vector SSM FourRooms | `pass` | Real-state slices correct; `g_plus` unaffected. |
| `0009` | Low-rank shared FourRooms auxiliary test | `weak_pass` | Valid negative transfer result. |
| `0010` | Low-rank auxiliary repair diagnostic | `weak_pass` | Negative transfer reproduced; repair variants did not match terminal-only. |

## Main Findings

Confirmed positive findings:

- `0001`-`0007` support the estimator claim: deterministic soft terminal marginalization preserves scaling, removes terminal-sampling variance, and helps under adequate coverage in small tabular settings.
- `0007` showed coverage is the main condition for learning-performance claims in non-oracle RiverSwim.
- `0008` validated tabular vector SSM indexing: `g_plus` matched terminal-only exactly, scaled `g_plus` matched normalized Q to `1.1102230246251565e-16`, and real-state goal slices had zero value error.

Confirmed negative auxiliary findings:

- `0009` was the first genuinely shared low-rank test: `M_hat(s,a,g)=sigmoid(u_sa dot v_g + b_g)`.
- `0009` used CPU-only NumPy, matched replay, matched seeds, rank `4`, learning rate `0.05`, and adequate coverage for all 10 seeds.
- `0009` terminal-only baseline had mean Bellman residual `0.0009558486`, mean scaled value error `0.0731219459`, and mean reward success rate `0.5384615385`.
- `0009` combined auxiliary training collapsed: mean `g_plus` Bellman residual worsened to `0.0364139480`, mean scaled value error worsened to `16.8938684161`, reward success fell to `0.0`, and real-goal diagnostics were poor.
- `0010` reproduced the original negative-transfer result under the same audited FourRooms setup.
- `0010` tested only the four predeclared variants: terminal-only, original combined, loss-balanced combined, and staged auxiliary pretrain then `g_plus` fine-tuning.
- Neither repaired variant matched terminal-only on `g_plus` value error and Bellman residual.
- `0010` correctly labels the result as `auxiliary_unsupported_for_lowrank`.

## Limitations And Risks

- The auxiliary conclusion is limited to one predeclared rank-4 NumPy low-rank architecture, optimizer, replay setup, and gamma.
- The loss-balanced variant still had very large auxiliary-to-`g_plus` shared-factor gradient dominance, so scale imbalance may remain unresolved.
- Terminal-only baseline is imperfect, so the result supports pausing this low-rank auxiliary thread, not making a broad architectural impossibility claim.
- Replay uses uniform state-action resets, which gives good coverage but is less realistic than trajectory-only offline data.
- No PyTorch/JAX, neural, larger FourRooms, or broad hyperparameter result exists.
- A publishable auxiliary-goal claim would be overreach.

## Recommended Next Human Decision

Pause the low-rank auxiliary-goal thread for this architecture and write up the negative result.

Recommended next step: consolidate the evidence into a short report with two separate claims:

- Positive: soft terminal marginalization is a reliable tabular variance-reduction/equivalence mechanism under adequate coverage.
- Negative: real-state auxiliary goals did not help the first shared low-rank FourRooms model and remained harmful after two small repair attempts.

Do not expand to neural frameworks, GPU, larger sweeps, or publishable auxiliary-goal claims without an explicit new human-approved hypothesis.

## Files To Inspect

- `research/reward_to_gcrl/results/0010_result.json`
- `research/reward_to_gcrl/results/0010_summary.md`
- `research/reward_to_gcrl/reviews/0010_review.md`
- `research/reward_to_gcrl/artifacts/0010/run_fourrooms_lowrank_aux_diagnostic.py`
- `research/reward_to_gcrl/results/0009_result.json`
- `research/reward_to_gcrl/reviews/0009_review.md`
- `research/reward_to_gcrl/artifacts/0009/run_fourrooms_lowrank_auxiliary.py`
- `research/reward_to_gcrl/results/0008_result.json`
- `research/reward_to_gcrl/reviews/0008_review.md`
- `research/reward_to_gcrl/decisions/0010_pro_decision.md`