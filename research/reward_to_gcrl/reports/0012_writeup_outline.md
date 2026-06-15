# 0012 Writeup Outline: reward_to_gcrl

## Decision

Recommended next direction: `write_short_paper`.

Auxiliary-goal compute should remain gated. The low-rank auxiliary thread should
not be reopened without a new falsifiable mechanism and human approval.

## Draft Memo Summary

The evidence supports a scoped positive result and a scoped negative result.
Soft terminal marginalization is a useful small-tabular estimator/equivalence
mechanism: it removes terminal-sampling variance, preserves normalized-Q scaling
under audited reward normalization and terminal masks, and improves or matches
learning metrics in adequately covered tabular regimes. This does not imply
neural, large-environment, or online-exploration generality.

The auxiliary result is negative and narrow. In tiny FourRooms with a CPU NumPy
rank-4 shared low-rank SSM, real-state auxiliary goals did not improve g_plus.
The first shared-parameter run showed negative transfer, and the predeclared
loss-balanced and staged repair diagnostics did not recover terminal-only g_plus
value error or Bellman residual.

## Claim Status Table

| Experiments | Claim | Status | Numeric Evidence |
| --- | --- | --- | --- |
| 0001, 0002, 0003, 0004, 0005, 0006, 0007, 0008, 0011 | Soft terminal marginalization is a useful small-tabular estimator/equivalence mechanism under audited reward normalization and adequate coverage. | supported | 0001 soft variance 0 vs sampled variance up to 0.0904013<br>0002 scaled CliffWalking error 9.71198e-10<br>0008 vector g_plus scaled-Q error 1.11022e-16 |
| 0005, 0006, 0007, 0011 | RiverSwim learning advantages are coverage-qualified rather than unconditional. | partially_supported | 0007 adequate bin value delta -0.0614823<br>0007 starved bin value delta 0.0401128 |
| 0008 | Independent tabular real-state goal slices are correct and do not perturb g_plus. | supported | g_plus perturbation 0<br>min goal success rate 1 |
| 0009, 0010, 0011 | The tested rank-4 NumPy low-rank real-state auxiliary approach improves g_plus. | contradicted | 0009 combined value error 16.8939 vs terminal-only 0.0731219<br>0010 loss-balanced value error 7.37704 vs terminal-only 0.0731219 |
| 0009, 0010, 0011 | Real-state auxiliary goals are generally impossible or useless. | unsupported | Only one tiny rank-4 architecture family and replay construction were tested. |
| 0001, 0002, 0003, 0004, 0005, 0006, 0007, 0008, 0009, 0010, 0011 | Neural, large-environment, GPU, or online-exploration generality follows from this evidence. | not_tested | No neural framework, GPU training, larger environment, or broad online robustness run exists in 0001-0011. |

## Positive Estimator Evidence

- Variance removal: 0001 reports soft target variance
  `0` while sampled target variance
  reaches `0.0904013`. Later sampled-vs-soft
  runs keep `sampled_variance_exceeds_soft_rate = 1`.
- Scaling equivalence: finite-MDP scaled error is
  `3.94752e-08` in 0001, CliffWalking exact-DP
  scaled error is `9.71198e-10` in 0002,
  and FourRooms vector g_plus scaled-vs-Q error is
  `1.11022e-16` in 0008.
- RiverSwim coverage behavior: in 0007, adequate-coverage soft-minus-sampled
  value error is `-0.0614823` and Bellman
  residual delta is `-0.00535871`.
  Starved-coverage value error delta is `0.0401128`,
  so coverage caveats must stay attached to any learning claim.
- FourRooms vector sanity: 0008 reports g_plus perturbation
  `0`, scaled-Q error
  `1.11022e-16`, and minimum real-goal
  success rate `1`.

## Negative Auxiliary Evidence

- 0009 terminal-only g_plus value error was
  `0.0731219` with Bellman residual
  `0.000955849`. Combined auxiliary
  value error rose to `16.8939` with
  Bellman residual `0.0364139`.
- 0009 reward success fell from terminal-only
  `0.538462` to combined
  `0`.
- 0010 reproduced the 0009 failure. The loss-balanced repair had g_plus value
  error `7.37704` and residual
  `0.0179085`; the staged repair had value
  error `18.5798` and residual
  `0.0508149`. The recorded 0010 verdict is
  `auxiliary_unsupported_for_lowrank`.

## Figure And Table Plan

| Item | Title | Source | Plan |
| --- | --- | --- | --- |
| Figure 1 | Terminal target variance sweep | 0001 | Plot sampled target variance against gamma/r_bar and overlay zero soft variance. |
| Table 1 | Claim-status table | 0001-0011 | Use the claim table in this memo; keep supported, partially_supported, unsupported, contradicted, and not_tested labels. |
| Table 2 | Scaling-equivalence checks | 0001, 0002, 0008 | List finite-MDP, CliffWalking, and FourRooms scaled g_plus-vs-Q errors. |
| Figure 2 | RiverSwim coverage dose response | 0007 | Bar/table of adequate, borderline, and starved soft-minus-sampled value/residual/return deltas. |
| Table 3 | FourRooms vector sanity | 0008 | Report g_plus perturbation, scaled-Q error, real-goal value error, and goal success. |
| Table 4 | Low-rank auxiliary negative result | 0009, 0010 | Compare terminal-only, combined lambda=1, loss-balanced, and staged metrics. |
| Appendix Table | Exact commands and artifact paths | 0001-0012 | Summarize command provenance and raw metric artifact locations. |

## Red Lines

Do not claim:

- Auxiliary-goal benefit for g_plus.
- General impossibility of real-state auxiliary goals.
- Neural auxiliary-goal benefit.
- Larger-environment generality.
- Online exploration robustness.
- Coverage-starved RiverSwim learning superiority.
- Reward-task improvement from independent tabular goal slices.
- Any result requiring PyTorch, JAX, GPU, or broad sweeps.

## New-Hypothesis Gate

Reopen auxiliary-goal experiments only if a new packet supplies all of the
following:

1. A single falsifiable mechanism explaining why 0009/0010 failed.
2. A principled architecture or loss-normalization change, not a broad sweep over
   rank, optimizer, learning rate, or auxiliary weight.
3. A predeclared tiny CPU diagnostic with fixed seeds, replay construction,
   coverage thresholds, and exact terminal-only baseline.
4. Success criteria requiring g_plus scaled value error or Bellman residual to
   beat terminal-only by at least 10 percent, or statistically match both while
   improving real-goal diagnostics, without increasing tie-aware reward-policy
   disagreement.
5. A review step before any neural framework, GPU run, larger environment, or
   expensive sweep.

No-go condition: if the proposal only asks for more tuning of the tested rank-4
formulation, do not run it.
