# Decision: continue

Confidence: 0.86
Progress score: 2

## Rationale

Experiment 0001 provides enough validated evidence to move to the next charter gate, but not enough to make a broader positive claim. The highest-value next test is the required small tabular CliffWalking equivalence check: terminal-only soft successor learning must match normalized Q-learning before sampled baselines, auxiliary goals, RiverSwim, or neural approximation are worth running.

## Evidence

- research/reward_to_gcrl/results/0001_result.json is present and records status completed, exact commands, raw per-setting metrics, and artifacts.
- The 0001 review allows auto-continue and reports no triggered failure criteria, while flagging only medium-quality evidence and minor reporting risks.
- 0001 passed the one-state diagnostic: sampled and soft target means matched within tolerance across all 16 gamma/r_bar settings, soft variance was zero, and sampled g_plus events became rare at high gamma and low r_bar.
- 0001 also included a tiny finite-MDP fixed-point check with max_abs_error_scaled_f_vs_q 3.9475e-08 below the 1e-6 tolerance, supporting the scaling relationship in a minimal setting.
- The charter explicitly requires tabular CliffWalking equivalence and low policy disagreement before moving to larger or neural experiments.

## Risks

- Reward normalization in CliffWalking can change the task; the executor must predeclare the exact normalized reward and treat original-environment return as diagnostic, not as the equivalence pass/fail criterion.
- A paired-learning implementation could appear to pass because both learners share the same bug; include an exact dynamic-programming oracle for the declared normalized reward.
- Terminal handling is a known failure mode: bootstrapping after the goal terminal state would invalidate the result.
- The prior 0001 tolerance/reporting issues should not be copied forward; commands should reflect the actual invocation and pass/fail tolerances should be explicit.

## Next experiment

- Experiment id: `0002`
- Objective: Run a CPU-only tabular CliffWalking equivalence diagnostic comparing ordinary normalized-reward Q-learning to the terminal-only soft successor g_plus learner.
