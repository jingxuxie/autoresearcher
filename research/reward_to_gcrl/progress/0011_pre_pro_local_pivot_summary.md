## Current Status

The project has reached `0011`, which is a reviewed **report-only synthesis** with verdict `pass` and strong evidence quality. No new learning compute was run in `0011`.

Current defensible state:

- Positive estimator claim is supported in scoped small-tabular settings.
- Low-rank auxiliary-goal benefit is unsupported for the tested FourRooms setup.
- The low-rank auxiliary thread should be paused unless a new human-approved hypothesis changes the architecture or loss normalization in a principled way.

The research goal is **not fully solved**. The soft-terminal estimator mechanism is well supported in small audited tabular settings, but broader GCRL, neural, online-exploration, and auxiliary-representation claims remain unsupported.

## Experiment Ledger

| Iterations | Focus | Review Status | Outcome |
|---|---|---:|---|
| `0001` | One-state variance diagnostic | `weak_pass` | Sampled/soft means matched; soft removed terminal-sampling variance. |
| `0002`-`0004` | CliffWalking and repaired chain equivalence/sampled-vs-soft | `weak_pass` | Scaling equivalence held; repaired nondegenerate chain showed soft learning improvement. |
| `0005`-`0007` | RiverSwim propagation and coverage dose-response | `pass` | Soft estimator helped under adequate coverage; starved regimes remain coverage-limited. |
| `0008` | Tabular vector SSM FourRooms | `pass` | Real-state goal slices were exact and did not perturb `g_plus`. |
| `0009` | First shared low-rank FourRooms auxiliary test | `weak_pass` | Valid negative transfer: auxiliary training collapsed the reward head. |
| `0010` | Low-rank auxiliary repair diagnostic | `weak_pass` | Negative transfer reproduced; repaired variants did not match terminal-only. |
| `0011` | Evidence synthesis report | `pass` | Separated supported estimator claims from unsupported auxiliary claims. |

## Main Findings

Confirmed positive evidence:

- Soft terminal marginalization removes terminal-sampling variance while preserving expected targets in the one-state diagnostic.
- Scaled `g_plus` values match normalized-reward Q in audited tabular settings.
- RiverSwim evidence supports learning advantages only when coverage is adequate.
- `0008` confirmed vector SSM indexing: `g_plus` matched terminal-only exactly, scaled `g_plus` matched normalized Q to `1.1102230246251565e-16`, and real-state goal slices had zero value error.

Confirmed negative evidence:

- `0009` was a genuine shared low-rank model: `M_hat(s,a,g)=sigmoid(u_sa dot v_g + b_g)`.
- `0009` terminal-only had mean Bellman residual `0.0009558486` and mean scaled value error `0.0731219459`.
- `0009` combined auxiliary training worsened mean Bellman residual to `0.0364139480` and mean scaled value error to `16.8938684161`.
- `0010` reproduced the negative-transfer result and tested four predeclared variants only.
- Neither loss-balanced nor staged auxiliary repair matched terminal-only on `g_plus` value error and Bellman residual.
- `0011` correctly frames this as: low-rank shared real-state auxiliary training did not help `g_plus` in the tested rank-4 FourRooms setup.

## Limitations And Risks

- `0011` adds synthesis and decision framing only; it is not new empirical evidence.
- Positive estimator claims remain limited to small CPU tabular or CPU NumPy settings with audited reward normalization and terminal masks.
- RiverSwim learning advantages remain coverage-qualified.
- The auxiliary conclusion is limited to one rank-4 NumPy low-rank architecture, optimizer, replay setup, and predeclared repair variants.
- Uniform state-action reset replay gives adequate coverage but is less realistic than trajectory-only offline data.
- The evidence does not support neural auxiliary benefit, larger-environment generality, online exploration robustness, or publishable auxiliary-goal improvement claims.

## Recommended Next Human Decision

Pause the low-rank auxiliary thread and write/package the negative result.

Reopen auxiliary-goal experiments only with a new human-approved falsifiable hypothesis that changes architecture or loss normalization in a principled way. Do not continue via broad hyperparameter sweeps, PyTorch/JAX, GPU, or larger environments.

## Files To Inspect

- `research/reward_to_gcrl/reports/0011_evidence_synthesis.md`
- `research/reward_to_gcrl/results/0011_result.json`
- `research/reward_to_gcrl/results/0011_summary.md`
- `research/reward_to_gcrl/reviews/0011_review.md`
- `research/reward_to_gcrl/results/0010_result.json`
- `research/reward_to_gcrl/reviews/0010_review.md`
- `research/reward_to_gcrl/results/0009_result.json`
- `research/reward_to_gcrl/reviews/0009_review.md`
- `research/reward_to_gcrl/decisions/0011_pro_decision.md`