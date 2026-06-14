# Evidence Synthesis 0011: reward_to_gcrl

## Abstract

This report consolidates experiments 0001-0010 without running new learning compute.
The strongest defensible positive claim is that soft terminal marginalization
removes terminal-sampling variance and preserves normalized-Q scaling in the
small audited tabular settings tested here. RiverSwim learning advantages are
supported only when right-reward and state-action coverage are adequate.

The strongest defensible negative claim is narrower: real-state auxiliary goals
are unsupported for the tested rank-4 shared low-rank FourRooms architecture.
Experiment 0009 showed negative transfer under adequate replay coverage, and
experiment 0010 reproduced that failure while showing that the predeclared
loss-balanced and staged repair diagnostics did not recover terminal-only g_plus
performance.

## Claim Status Table

| Claim | Status | Evidence | Limitations |
| --- | --- | --- | --- |
| Soft terminal marginalization removes terminal-sampling variance in small tabular diagnostics. | supported | 0001: soft target variance is negligible while sampled variance is positive; max sampled variance 0.0904013.<br>0003/0005/0006/0007: sampled_variance_exceeds_soft_rate = 1.0. | Tabular CPU settings only; matched-stream or controlled behavior settings. |
| The soft g_plus fixed point scales to normalized Q in audited small tabular MDPs. | supported | 0001 finite-MDP max scaled error 3.94752e-08.<br>0002 CliffWalking exact-DP max scaled error 9.71198e-10.<br>0008 FourRooms vector g_plus scaled-minus-Q error 1.11022e-16. | Depends on declared reward normalization and terminal masks being audited. |
| Deterministic soft updates improve learning metrics under adequate tabular coverage. | partially_supported | 0004: nondegenerate chain verdict learning-improvement; soft-minus-sampled Bellman residual -0.00586335.<br>0007 adequate coverage bin: soft-minus-sampled value error -0.0614823 and Bellman residual -0.00535871. | 0007 starved bin has lower residual but worse value error, so coverage is a prerequisite. |
| Soft updates reliably improve learning in coverage-starved settings. | unsupported | 0007 starved bin: soft-minus-sampled value error 0.0401128 despite lower Bellman residual -0.00277697. | Coverage-starved results are diagnostic only and not learning-superiority evidence. |
| Independent tabular real-state goal slices can be added without perturbing g_plus. | supported | 0008: max_abs_vector_gplus_minus_terminal_only = 0.<br>0008: min real-goal greedy success rate = 1. | This is a sanity check with independent tabular slices, not evidence of reward-task improvement. |
| Rank-4 shared low-rank real-state auxiliary training improves g_plus in tiny FourRooms. | contradicted | 0009: verdict negative_transfer; combined-minus-terminal value error 16.8207 and residual 0.0354581.<br>0010: reproduction passed, repaired variants were not promising; verdict auxiliary_unsupported_for_lowrank. | Contradicts only this rank-4 low-rank setup with the tested replay and loss variants. |
| Real-state auxiliary goals are generally impossible or useless. | unsupported | 0009/0010 are scoped to one tiny FourRooms rank-4 architecture and replay construction. | A different architecture or principled loss design would require a new human-approved hypothesis. |
| Neural auxiliary benefit, larger-environment generality, or online exploration robustness. | unsupported | No PyTorch/JAX neural runs, larger environments, GPU runs, or broad online robustness tests were performed. | Must not be claimed from the current evidence. |

## Experiment Evidence Table

| Experiment | Status | Role | Key Metric |
| --- | --- | --- | --- |
| 0001 | completed | One-step terminal marginalization and finite-MDP scaling equivalence. | max sampled variance 0.0904; finite scaling error 3.948e-08 |
| 0002 | completed | Audited local CliffWalking exact-DP and paired-learning equivalence. | exact scaling error 9.712e-10; learned policy disagreement 0 |
| 0003 | completed | CliffWalking sampled-vs-soft under matched streams, with reward-normalization caveat. | target match 1; variance rate 1; residual soft 0.03875 vs sampled 0.04125 |
| 0004 | completed | Nondegenerate chain repair with direct sampled target comparison. | learning-improvement; soft residual delta -0.005863; value delta -0.02841 |
| 0005 | completed | 6-state RiverSwim sampled-vs-soft with sparse right-end rewards. | target match 1; variance rate 1; soft residual delta -0.009929 |
| 0006 | completed | RiverSwim non-oracle behavior streams with adequate/starved coverage split. | target match 1; variance rate 1; soft residual delta -0.004207 |
| 0007 | completed | RiverSwim coverage dose-response over four non-oracle behavior policies. | target match 1; variance rate 1; soft residual delta -0.004448 |
| 0008 | completed | Independent tabular FourRooms vector SSM sanity check. | g_plus perturbation 0; goal success 1 |
| 0009 | completed | Rank-4 shared low-rank FourRooms auxiliary-goal first test. | negative_transfer; value delta 16.82; residual delta 0.03546 |
| 0010 | completed | Rank-4 low-rank auxiliary repair diagnostic. | auxiliary_unsupported_for_lowrank; repaired promising=false |

## Accepted Positive Evidence

- Soft terminal marginalization is a reliable estimator transformation in the
  current tabular tests: sampled targets match deterministic soft marginal
  targets within tolerance while sampled terminal-sampling variance remains
  positive.
- The g_plus fixed point scales to normalized Q under the audited reward
  normalizations and terminal masks used in 0001, 0002, 0005, and 0008.
- Learning improvements are defensible only with coverage qualifiers. In the
  nondegenerate chain and adequately covered RiverSwim bins, soft updates lower
  Bellman residual and have non-worse or lower value error. In coverage-starved
  RiverSwim, residual and value error can disagree.

## Accepted Negative Evidence

- The first shared low-rank FourRooms auxiliary test is negative: 0009 reports
  `negative_transfer`, with combined-minus-terminal g_plus value error
  16.8207
  and Bellman residual 0.0354581.
- The repair diagnostic did not rescue the low-rank setup. In 0010, the original
  0009 behavior reproduced, `combined_loss_balanced` still worsened mean g_plus
  value error by 7.30392,
  and the staged variant worsened it by
  18.5066.
- This is not evidence that auxiliary goals are generally impossible. It is
  evidence against the tested rank-4 shared low-rank formulation, replay setup,
  and predeclared repair variants.

## Limitations

- All evidence is tiny, CPU tabular, or CPU NumPy. No neural framework, GPU
  training, larger environment, or broad hyperparameter sweep is represented.
- 0003 CliffWalking raw returns are diagnostic only because the declared reward
  normalization creates an objective mismatch with raw goal reaching.
- RiverSwim learning claims require coverage caveats. 0007 includes starved,
  borderline, and adequate bins, and starved runs must not be used for an
  unconditional soft-learning-superiority claim.
- 0009 and 0010 use uniform state-action reset replay, a single rank-4 model
  family, one main replay budget, and tightly predeclared variants. They do not
  establish online exploration robustness or larger-environment behavior.
- 0008 shows independent tabular goal slices are correct and non-interfering,
  but independent slices cannot support a shared-representation reward-task
  improvement claim.

## Red Lines

Do not claim:

- Neural auxiliary-goal benefit.
- Larger-environment generality.
- Online exploration robustness.
- Publishable auxiliary-goal improvement.
- That real-state auxiliary goals are generally impossible.
- That soft updates improve learning in coverage-starved regimes without the
  RiverSwim coverage caveat.
- That independent tabular real-state goals improve reward-task learning through
  shared representation.

## Auxiliary Reopening Gate

The low-rank auxiliary thread should stay paused unless a new human-approved,
falsifiable hypothesis changes the architecture or loss normalization in a
principled way. A valid reopening packet should specify exactly one proposed
mechanism, why 0009/0010 failed under that mechanism, a predeclared tiny
diagnostic, and a success criterion that beats or statistically matches
terminal-only g_plus value error and Bellman residual without increasing
tie-aware reward-policy disagreement. More rank, learning-rate, auxiliary-weight,
or optimizer sweeps without this hypothesis should not be run.

## Recommendation

Recommendation: `pause_lowrank_auxiliary_thread`.

Next decision: `write_negative_result`. If auxiliary work is reopened later, do
so only through `design_new_hypothesis_before_more_compute`.
