# ChatGPT Pro Decision: continue

Confidence: 0.9

## Rationale

Proceed with the proposed 0013 short-paper draft using existing reward_to_gcrl evidence only, with no new learning compute. The project has enough reviewed evidence for a scoped internal draft: the soft-terminal estimator mechanism is supported in small audited tabular settings, while the tested low-rank auxiliary-goal approach has negative evidence. The draft must preserve strict claim boundaries and require review before external publication or broader claims.

## Evidence

- The latest project state reports no current blocker and protected_file_drift=false.
- 0012 passed as a synthesis and packaging step, ran no new learning compute, and recommended write_short_paper.
- 0001-0007 support the scoped estimator claim: deterministic soft terminal marginalization preserves normalized-Q scaling, removes terminal-sampling variance, and helps under adequate coverage in small audited tabular settings.
- RiverSwim evidence is coverage-qualified: adequate-coverage runs support Bellman/value improvements, while coverage-starved runs should not be used for learning-superiority claims.
- 0008 validated tabular vector SSM correctness on FourRooms: g_plus matched terminal-only exactly, scaled g_plus matched normalized Q to numerical precision, and real-state goal slices were correct.
- 0009 produced valid negative transfer for the first shared low-rank FourRooms auxiliary test.
- 0010 reproduced the low-rank auxiliary negative-transfer result, and the predeclared loss-balanced and staged repair variants did not match terminal-only on g_plus value error and Bellman residual.
- The current evidence does not support neural auxiliary benefit, larger-environment generality, online exploration robustness, or broad auxiliary-goal improvement claims.

## Risks

- The short-paper draft could overstate small CPU tabular evidence as a general reward-to-GCRL or neural-function-approximation result.
- The draft could overgeneralize the low-rank auxiliary negative result into a claim that auxiliary goals are generally harmful or impossible.
- The draft could blur estimator evidence with auxiliary-representation evidence, making the story stronger than the experiments support.
- Coverage caveats from RiverSwim and matched-stream limitations could be underemphasized.
- Because 0013 is synthesis only, it must not be described as new empirical validation.
- External release before review could propagate unsupported broader claims.

## Next experiment

- Experiment id: `0013`
- Objective: Write an internal short-paper draft from existing 0001-0012 reward_to_gcrl evidence only, with a claim-to-evidence map, explicit limitations, unsupported-claims red lines, and a pre-publication review checklist.
