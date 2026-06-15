## Current Status

The project is active with no current blocker and `protected_file_drift: false`.

Iteration `0012` is a reviewed `pass` synthesis/packaging step. It ran **no new learning compute** and recommends moving to a short-paper draft using existing evidence only. The current evidence supports a scoped estimator claim, while the auxiliary-goal/shared-representation claim remains unsupported for the tested low-rank setup.

The research goal is **not fully solved**. The soft-terminal estimator mechanism is supported in small audited tabular settings, but neural, large-environment, online-exploration, and broad auxiliary-goal claims remain untested.

## Experiment Ledger

| Iterations | Focus | Review Status | Outcome |
|---|---|---:|---|
| `0001` | One-state variance diagnostic | `weak_pass` | Sampled/soft means matched; soft removed terminal variance. |
| `0002`-`0004` | CliffWalking and repaired chain checks | `weak_pass` | Scaling equivalence held; repaired chain showed soft improvement. |
| `0005`-`0007` | RiverSwim propagation and coverage | `pass` | Soft helped under adequate coverage; starved runs remain caveated. |
| `0008` | Tabular vector SSM FourRooms | `pass` | Real-state goal slices exact; `g_plus` unaffected. |
| `0009` | First shared low-rank FourRooms auxiliary test | `weak_pass` | Valid negative transfer. |
| `0010` | Low-rank auxiliary repair diagnostic | `weak_pass` | Negative transfer reproduced; repairs failed. |
| `0011` | Evidence synthesis report | `pass` | Separated estimator evidence from auxiliary evidence. |
| `0012` | Write-up outline / memo packaging | `pass` | Recommends `write_short_paper`; defines red-line claims and reopening gate. |

## Main Findings

Confirmed positive estimator evidence:

- Soft terminal marginalization removes terminal-sampling variance and preserves normalized-Q scaling in small audited tabular settings.
- RiverSwim results support Bellman/value improvements only when coverage is adequate.
- `0008` confirmed tabular vector SSM correctness: `g_plus` matched terminal-only exactly, scaled `g_plus` matched normalized Q to `1.1102230246251565e-16`, and real-state goal slices had zero value error.

Confirmed negative auxiliary evidence:

- `0009` tested a genuine shared low-rank model, `M_hat(s,a,g)=sigmoid(u_sa dot v_g + b_g)`.
- `0009` terminal-only had mean Bellman residual `0.0009558486` and mean scaled value error `0.0731219459`.
- `0009` combined auxiliary training worsened mean Bellman residual to `0.0364139480` and mean scaled value error to `16.8938684161`.
- `0010` reproduced the negative-transfer result and found neither loss-balanced nor staged auxiliary repair matched terminal-only on `g_plus` value error and Bellman residual.
- `0012` records the strongest defensible auxiliary claim as: the tested rank-4 NumPy low-rank FourRooms real-state auxiliary approach is unsupported and showed negative transfer.

## Limitations And Risks

- `0011` and `0012` are synthesis/packaging only, not new empirical evidence.
- Positive estimator claims are limited to small CPU tabular or CPU NumPy settings with audited reward normalization and terminal masks.
- RiverSwim learning advantages remain coverage-qualified; coverage-starved runs should not be cited as learning-superiority evidence.
- The auxiliary negative result is limited to the tested rank-4 FourRooms low-rank setup, replay construction, and predeclared repair diagnostics.
- No neural framework, GPU, larger environment, image observation, MuJoCo, AntMaze, OGBench, or publishable auxiliary-benefit claim is supported.
- A new auxiliary experiment requires a human-approved falsifiable hypothesis, not a broad hyperparameter sweep.

## Recommended Next Human Decision

Proceed to `0013`: write a scoped short-paper draft from existing `0001`-`0012` evidence only.

The draft should include a claim-to-evidence map and must preserve these boundaries:

- Supported: small-tabular soft terminal marginalization as a variance-reduction/equivalence mechanism under adequate coverage.
- Supported negative: tested rank-4 low-rank FourRooms auxiliary approach showed negative transfer.
- Not supported: neural/general benchmark claims, broad auxiliary-goal benefit or impossibility, online exploration robustness, and larger-environment generality.

Require review before external publication or broader claims.

## Files To Inspect

- `research/reward_to_gcrl/results/0012_result.json`
- `research/reward_to_gcrl/results/0012_summary.md`
- `research/reward_to_gcrl/reviews/0012_review.md`
- `research/reward_to_gcrl/reports/0012_writeup_outline.md`
- `research/reward_to_gcrl/reports/0011_evidence_synthesis.md`
- `research/reward_to_gcrl/results/0011_result.json`
- `research/reward_to_gcrl/results/0010_result.json`
- `research/reward_to_gcrl/reviews/0010_review.md`
- `research/reward_to_gcrl/results/0009_result.json`
- `research/reward_to_gcrl/reviews/0009_review.md`
- `research/reward_to_gcrl/decisions/0013_decision.md`