# ChatGPT Pro Decision: pivot

Confidence: 0.85

## Rationale

Pivot within the same research direction and do not treat any 0004 outputs as evidence yet. The reviewed evidence from 0001-0003 supports the variance motivation and tabular scaling equivalence, but the learning-performance story is still weak: the CliffWalking normalization made raw success meaningless, 0003 value-error dominance was mixed, and target comparisons were not directly against the deterministic soft learner target. The latest summary also reports protected_file_drift and unreviewed 0004 result paths, so the next step should be a cheap evidence-gating experiment: clear/adjudicate file drift, validate or rerun the repaired nondegenerate sampled-vs-soft diagnostic, and only then decide whether to move to RiverSwim or auxiliary goals.

## Evidence

- 0001 weak-passed the one-state sampled-vs-soft diagnostic: sampled means matched expected means, soft terminal variance was zero/negligible, rare g_plus events were exposed, and finite-MDP scaling equivalence passed.
- 0002 weak-passed audited local CliffWalking tabular equivalence: exact DP scaling equivalence passed and learned scaled M matched normalized Q on sufficiently visited state-action pairs.
- 0003 weak-passed structurally: sampled conditional variance exceeded zero soft terminal-sampling variance in all 30 runs and soft had lower final Bellman residual in 26 of 30 runs.
- The learning-performance evidence remains ambiguous: 0003 mean final soft value error was slightly worse than sampled value error, and soft value-error dominance was only 17 of 30 runs.
- The CliffWalking normalization used in 0002 and 0003 made policies have raw return -200 and success rate 0.0, so raw task success is not positive evidence.
- The latest summary says protected_file_drift is true and that 0004 result/summary paths exist but no reviewed 0004 evidence is supplied.
- The latest local decision says needs_human because continuing automatically could compound overclaims from ambiguous 0003 evidence.

## Risks

- Using unreviewed 0004 files as evidence could contaminate the research loop if protected file drift affected results or summaries.
- Repeating CliffWalking without fixing reward normalization will likely reproduce degenerate policy and tie-heavy diagnostics.
- A repaired nondegenerate task may show only variance reduction and no learning advantage, which would weaken the algorithmic contribution.
- Moving to RiverSwim, auxiliary goals, or neural approximation before resolving the 0003 ambiguity would make later failures hard to interpret.
- If the repaired experiment changes both environment and estimator checks at once, it may be unclear whether results are due to nondegenerate rewards or implementation changes.

## Next experiment

- Experiment id: `0004`
- Objective: Resolve protected file drift and validate the repaired nondegenerate sampled-vs-soft experiment. If existing 0004 artifacts are complete and trustworthy, review them without new learning runs; otherwise rerun a CPU-only tabular repaired diagnostic that directly compares sampled augmented targets to deterministic soft targets in a nondegenerate task.
