# ChatGPT Pro Decision: pivot

Confidence: 0.83

## Rationale

Pivot within the same research direction rather than stop. The project has made real but limited progress: 0001-0003 support the variance motivation and tabular scaling equivalence, but the current CliffWalking setup is scientifically too degenerate to justify moving to auxiliary goals or neural models. The main new evidence is not that soft successor learning is clearly better, but that naive normalized reward-to-goal conversion can preserve a scaled normalized objective while destroying useful raw-task incentives. The next experiment should repair this ambiguity by using a nondegenerate reward/task setting and directly comparing sampled targets to the deterministic soft target, not by continuing to collect weak CliffWalking evidence under the same normalization.

## Evidence

- 0001 weak-passed: sampled and soft terminal targets matched expected means, soft removed terminal-sampling variance, and rare g_plus events were exposed.
- 0002 weak-passed: an audited local deterministic CliffWalking table was used, exact DP scaling equivalence passed, and learned scaled M matched normalized Q on sufficiently visited pairs.
- 0003 weak-passed structurally: sampled conditional variance exceeded zero soft terminal-sampling variance in all 30 CPU-tabular runs, and soft had lower final Bellman residual in 26 of 30 runs.
- The strongest 0003 learning-performance claim is mixed: mean final soft value error was slightly worse than sampled value error, soft value-error dominance was only 17 of 30 runs, and only 4 of 10 seeds at gamma 0.995.
- The current CliffWalking normalization made raw task success uninformative: policies in 0002 and 0003 had raw return -200 and success rate 0.0.
- 0003 target-mean validation compared sampled targets to the sampled learner's conditional expectation rather than directly to the deterministic soft learner's recorded target, and sampled-vs-soft deterministic target means exceeded tolerance in 19 of 30 runs.
- The latest local decision is needs_human because continuing automatically risks compounding overclaims from ambiguous 0003 evidence.

## Risks

- A repaired experiment may show that soft terminal marginalization mainly reduces estimator variance but does not improve learned value error under tabular control.
- Changing the reward normalization could accidentally change the task again unless raw reward, normalized reward, and affine constants are explicitly audited.
- Direct sampled-vs-soft target comparisons require matched state-action-next-state streams and synchronized learner states; otherwise differences may reflect policy/data drift rather than estimator variance.
- If the experiment uses only CliffWalking again, policy ties and episodic-duration effects may remain confusing.
- Moving to RiverSwim, auxiliary goals, or neural function approximation before resolving this ambiguity would make later failures hard to interpret.

## Next experiment

- Experiment id: `0004`
- Objective: Repair the sampled-vs-soft comparison using a small nondegenerate tabular setting where the raw task objective remains meaningful, and directly test whether deterministic soft terminal marginalization improves Bellman residual, value error, and policy quality over sampled augmented updates under matched data.
