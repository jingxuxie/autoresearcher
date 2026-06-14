# Review 0004: needs_human

Allows auto-continue: False

## Reasons

- Required 0004 result JSON, summary markdown, and declared artifacts are present.
- Result JSON validates against schemas/result.schema.json, and declared artifact paths validate successfully.
- The repaired experiment itself is scientifically stronger than 0003: it uses a nondegenerate 5-state chain, identity reward normalization, non-tie exact DP policies, direct sampled-vs-deterministic-soft target comparison from the same sampled learner state, and matched transition streams over 3 gammas x 10 seeds.
- Raw and normalized exact-DP policies are preserved, exact soft scaling matches normalized Q, and evaluation is nondegenerate: soft policies have mean raw return 1 and success rate 1 while sampled policies have mean raw return 0 and success rate 0.
- Target mean matching and sampled variance criteria pass in all 30 runs; soft also has lower mean final Bellman residual and lower mean value error.
- However, the plan's first gate was protected file drift resolution/adjudication. The 0004 result does not contain any drift_status/protected_file_drift audit, and research/reward_to_gcrl/state.json still reports protected_file_drift: true.
- A prior guard file research/reward_to_gcrl/decisions/0004_worktree_guard.json records protected drift on autoresearcher.yaml. Although a current scoped git status did not show tracked protected modifications, the loop state and result artifact do not explicitly clear or adjudicate this drift, so the prerequisite evidence gate is not satisfied.

## Required fixes

- Clear or explicitly adjudicate protected_file_drift before treating 0004 as accepted evidence.
- Add a drift_status or protected_file_drift audit field to the 0004 result, including whether protected paths changed and why the output is safe to use.
- If the supervisor confirms the drift flag is stale and no protected files are currently modified, the 0004 scientific result can likely be accepted without rerunning learning.

## Risk flags

- Protected file drift remains unresolved in loop metadata despite current git status not showing tracked protected-path modifications.
- The 0004 result omits the required drift status even though the plan explicitly required it.
- The behavior stream is oracle-guided by exact normalized Q with epsilon, so the result tests matched-stream estimator quality rather than fully online learner-induced exploration.
- The environment is a very small 5-state chain; it is decisive for the repaired tabular gate but not sufficient evidence for larger grid or long-horizon tasks.
- Sampled baseline failure is stark under a fixed 100000-transition budget, but no decaying step-size or larger-budget sensitivity check was run.
