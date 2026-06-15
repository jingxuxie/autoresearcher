# Internal Draft: Soft Terminal Marginalization and a Negative Low-Rank Auxiliary Result

**Status:** internal draft only. Requires pre-publication review before external
use or broader claims.

## Abstract

We study a small, audited sequence of tabular and CPU NumPy diagnostics for
reward-to-GCRL style soft successor measures. The positive evidence supports a
scoped estimator claim: soft terminal marginalization removes terminal-sampling
variance and preserves normalized-Q scaling in small audited tabular settings,
with learning advantages only when transition and reward coverage are adequate.
The negative evidence is also scoped: in tiny FourRooms, a rank-4 shared
low-rank real-state auxiliary-goal model did not improve the g_plus reward slice
and showed negative transfer. Loss-balanced and staged repair diagnostics did
not recover terminal-only g_plus value error or Bellman residual. These results
support an internal write-up, not external generality claims.

## Introduction

The project began with a narrow question: can a terminal-only soft
successor-measure target represent normalized reward value while avoiding sparse
sampled terminal events? Experiments 0001-0008 answer this in controlled small
settings. The estimator transformation behaves as expected, and independent
tabular vector goal slices are correct and non-interfering.

The later question was whether real-state auxiliary goals help g_plus through
shared parameters. Experiments 0009 and 0010 do not support that claim for the
tested rank-4 low-rank FourRooms model. The draft therefore separates estimator
evidence from auxiliary-goal evidence.

## Method Summary

The estimator experiments compare sampled augmented g_plus updates with
deterministic soft terminal marginalization. The sampled update keeps the same
expected target but retains terminal-sampling variance; the soft update replaces
sampled terminal events with their deterministic marginal mass. Exact DP checks
compare scaled soft g_plus values to normalized Q references under audited reward
normalization and terminal masks.

The auxiliary experiments use a CPU NumPy low-rank shared model in tiny
FourRooms. Terminal-only g_plus training is compared with combined real-state
auxiliary training under matched replay and fixed rank. The 0010 repair
diagnostic tests only the predeclared variants: terminal-only reproduction,
combined lambda=1 reproduction, loss-balanced combined training, and staged
real-goal pretraining followed by g_plus fine-tuning.

## Claim-To-Evidence Map

| ID | Claim | Status | Iterations | Evidence |
| --- | --- | --- | --- | --- |
| C1 | Soft terminal marginalization removes terminal-sampling variance in audited small tabular settings. | supported | 0001, 0003, 0005, 0006, 0007, 0011, 0012 | 0001 max soft target variance 0<br>0001 max sampled target variance 0.0904013<br>sampled_variance_exceeds_soft_rate is 1 in 0003/0005/0006/0007 |
| C2 | Soft g_plus fixed points preserve normalized-Q scaling under audited reward normalization and terminal masks. | supported | 0001, 0002, 0008, 0011, 0012 | 0001 finite-MDP scaled error 3.94752e-08<br>0002 CliffWalking scaled error 9.71198e-10<br>0008 FourRooms scaled error 1.11022e-16 |
| C3 | Soft updates can improve learning metrics when coverage is adequate. | partially_supported | 0004, 0005, 0006, 0007, 0011, 0012 | 0007 adequate value-error delta -0.0614823<br>0007 adequate Bellman-residual delta -0.00535871<br>0007 starved value-error delta 0.0401128 |
| C4 | Independent tabular vector SSM real-state goals are correct and non-interfering. | supported | 0008, 0011, 0012 | 0008 vector g_plus minus terminal-only 0<br>0008 min goal success rate 1 |
| C5 | The tested rank-4 low-rank FourRooms real-state auxiliary approach improves g_plus. | contradicted | 0009, 0010, 0011, 0012 | 0009 terminal-only value error 0.0731219<br>0009 combined value error 16.8939<br>0010 loss-balanced value error 7.37704<br>0010 staged value error 18.5798 |
| C6 | Auxiliary goals are generally impossible or harmful. | unsupported | 0009, 0010, 0011, 0012 | Only one tiny rank-4 shared low-rank setup was tested. |
| C7 | Neural, large-environment, benchmark, or online-exploration generality follows. | not_tested | 0001, 0002, 0003, 0004, 0005, 0006, 0007, 0008, 0009, 0010, 0011, 0012 | No neural, GPU, large-environment, benchmark, or broad online robustness experiment exists. |

## Experimental Evidence Summary

Soft terminal marginalization removes terminal-sampling variance in the tested
settings. In 0001, the maximum soft target variance is
`0` while sampled target variance
reaches `0.0904013`. Later sampled-vs-soft
experiments keep sampled variance above soft variance in all reported settings.

Scaling checks support the normalized-Q relation. The finite-MDP scaled error in
0001 is `3.94752e-08`, the audited local
CliffWalking scaled error in 0002 is
`9.71198e-10`, and the FourRooms vector
g_plus scaled-vs-Q error in 0008 is
`1.11022e-16`.

Learning improvements are coverage-qualified. In the 0007 RiverSwim dose
response, adequate-coverage runs have soft-minus-sampled value-error delta
`-0.0614823` and Bellman-residual delta
`-0.00535871`. Starved-coverage runs have
value-error delta `0.0401128`, so they must
not be used for an unconditional learning-superiority claim.

Vector SSM correctness is supported only in the independent tabular sense. In
0008, vector g_plus minus terminal-only is
`0`, scaled-Q error is
`1.11022e-16`, and minimum real-goal
success rate is `1`.

## Negative Auxiliary Result

The shared low-rank auxiliary result is negative. In 0009, terminal-only g_plus
value error is `0.0731219` with Bellman
residual `0.000955849`. Combined auxiliary
training increases value error to `16.8939`
and Bellman residual to `0.0364139`.
Reward success falls from `0.538462` to
`0`.

Experiment 0010 reproduces the negative-transfer pattern and tests two repair
variants. Loss-balanced training still has value error
`7.37704` and residual
`0.0179085`. The staged variant has value
error `18.5798` and residual
`0.0508149`. The recorded verdict is
`auxiliary_unsupported_for_lowrank`.

This is evidence against the tested architecture and training recipe, not
against auxiliary goals in general.

## Limitations

- The evidence is tiny-environment, tabular, or CPU NumPy only.
- Several estimator tests use matched streams or controlled behavior policies.
- RiverSwim learning claims depend on adequate right-reward and state-action
  coverage.
- CliffWalking raw-task returns are limited by reward-normalization mismatch.
- FourRooms auxiliary tests use uniform state-action reset replay, one rank-4
  low-rank model family, fixed optimizer settings, fixed gamma, and predeclared
  repair variants.
- No neural framework, GPU run, larger environment, benchmark suite, or online
  exploration robustness test was run.

## Unsupported-Claims Red Lines

Do not claim:

- Neural auxiliary benefit.
- Broad reward-to-GCRL success.
- Online exploration robustness.
- Benchmark or larger-environment generality.
- General impossibility or general harmfulness of auxiliary goals.
- Coverage-starved RiverSwim learning superiority.
- Reward-task improvement from independent tabular goal slices.

## Pre-Publication Review Checklist

| Check | Requirement | Status Before External Use |
| --- | --- | --- |
| Claim scope | Every estimator claim says small tabular or CPU NumPy and adequate coverage where relevant. | required |
| Auxiliary wording | Auxiliary result is limited to the tested rank-4 FourRooms architecture, optimizer, replay setup, gamma, and repair variants. | required |
| No overclaim | No neural, benchmark, large-environment, broad GCRL, or online exploration claim is present. | required |
| Negative evidence | 0009 and 0010 negative-transfer metrics are shown without minimization. | required |
| Coverage caveat | RiverSwim starved and adequate bins are both reported. | required |
| Artifact trace | Each claim links to iteration IDs and raw result artifacts. | required |
| Human review | A human reviewer signs off before external publication or broader claims. | required |

## Conclusion

The internal evidence supports a narrow positive estimator conclusion and a
narrow negative auxiliary conclusion. The next safe step is review of this draft
against the checklist. External publication or broader claims require explicit
human review. Future auxiliary experiments require a new falsifiable hypothesis
that changes the architecture or loss normalization in a principled way, not a
broad sweep over the failed rank-4 setup.
