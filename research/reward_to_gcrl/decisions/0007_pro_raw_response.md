JSON
{
  "decision": "continue",
  "confidence": 0.86,
  "rationale": "Continue with one more small CPU-tabular RiverSwim experiment before moving to auxiliary goals. The project is now making real progress toward the overall research goal: drift is cleared, 0004 supplied a nondegenerate small-chain result, 0005 gave a strong controlled RiverSwim propagation result, and 0006 removed exact-Q-guided behavior while preserving the estimator story. The remaining blocker is not whether the soft estimator reduces terminal-sampling variance; that is well supported. The open question is whether the learning advantage is robust once coverage is non-oracle but not starved. A coverage-controlled RiverSwim dose-response test is the cheapest decisive next step.",
  "evidence": [
    "The latest summary reports protected_file_drift is false and there is no current blocker.",
    "0001 validated the estimator premise: sampled and soft terminal targets matched means while soft terminal variance was zero or negligible.",
    "0002 confirmed tabular scaling equivalence in audited CliffWalking below the 1e-6 threshold.",
    "0004 accepted the repaired nondegenerate 5-state chain result: soft had lower Bellman residual and value error and achieved success where sampled failed.",
    "0005 passed on 6-state RiverSwim with exact-Q-guided behavior: sampled target means matched deterministic soft marginal targets in all 30 runs, sampled variance exceeded soft variance in all 30 runs, and soft residual dominance held in all runs.",
    "0006 passed with non-oracle behavior streams: sampled targets remained unbiased within tolerance and higher variance without exact-Q-guided behavior.",
    "The main 0006 caveat is coverage: half the runs were coverage-starved, and under poor coverage soft could have lower Bellman residual but worse value error than sampled.",
    "No auxiliary-goal, neural, FourRooms, larger RiverSwim, or offline fitted-learning evidence exists yet."
  ],
  "risks": [
    "A further RiverSwim run could become redundant if it only repeats the variance result without clarifying coverage dependence.",
    "Coverage-controlled behavior policies may still be too artificial to support online-control claims.",
    "If adequate coverage is achieved by hand-designed behavior, the result remains matched-stream estimator evidence, not full exploration evidence.",
    "Moving to auxiliary goals before bounding the coverage caveat could make later representation-learning results hard to interpret.",
    "All current evidence is still tiny tabular evidence, so even a positive 0007 should not be overclaimed as a general GCRL solution."
  ],
  "next_experiment": {
    "experiment_id": "0007_riverswim_coverage_dose_response",
    "objective": "Run a CPU-only tabular RiverSwim coverage dose-response experiment that uses several non-oracle behavior policies to create starved, borderline, and adequate coverage regimes, then quantify exactly when deterministic soft terminal marginalization improves Bellman residual, value error, and policy quality over sampled augmented updates.",
    "hypothesis": "The deterministic soft update should consistently reduce terminal-sampling variance in all coverage regimes, but learning-performance advantages should appear mainly when right-reward and state-action coverage are adequate. In coverage-starved regimes, soft may lower Bellman residual without reliably lowering value error, so coverage should be treated as a prerequisite for learning-superiority claims.",
    "success_criteria": [
      "Use only CPU tabular code on the same audited 6-state RiverSwim semantics as 0005 and 0006.",
      "Generate matched logged streams from at least four fixed non-oracle behavior policies, such as uniform random, mild right bias, strong right bias, and alternating or epsilon-cyclic exploration, with no exact-Q action guidance.",
      "Predeclare coverage bins using right-reward events per 10000 transitions and visited state-action-pair counts, then report results separately for starved, borderline, and adequate coverage.",
      "For every gamma-behavior-seed run, sampled target means must match deterministic soft marginal targets within predeclared Monte Carlo tolerance, and sampled terminal-sampling variance must exceed soft terminal-sampling variance.",
      "On adequate-coverage runs, soft must have lower mean final Bellman residual and lower or statistically indistinguishable mean final value error than sampled.",
      "On starved runs, the summary must explicitly avoid learning-superiority claims and report whether Bellman residual and value error disagree.",
      "Include a simple coverage-performance regression or stratified table showing how soft-minus-sampled value error changes with right-reward event count and visited state-action coverage.",
      "The final recommendation must state whether to move next to tabular auxiliary real-state goals or whether more estimator-only RiverSwim work is still needed."
    ],
    "failure_criteria": [
      "Any behavior policy uses exact DP, exact Q, or reward-optimal action preferences to generate the logged stream.",
      "The run does not produce both adequate-coverage and coverage-starved regimes, making the coverage caveat unresolved.",
      "Target means are compared only to the sampled learner's own conditional expectation rather than the deterministic soft marginal target from the same transition and learner state.",
      "Soft has worse value error than sampled in adequate-coverage runs without a clear explanation.",
      "The summary makes an unconditional learning-superiority claim despite coverage-starved failures.",
      "The experiment adds auxiliary goals, neural approximation, larger environments, GPU dependence, or expensive hyperparameter sweeps before this coverage gate is resolved."
    ],
    "tasks_for_codex": [
      "Create research/reward_to_gcrl/artifacts/0007/run_riverswim_coverage_dose_response.py by extending the 0006 non-oracle RiverSwim script.",
      "Reuse and verify the same 6-state RiverSwim transition hash, reward normalization, action mapping, and exact DP references from 0005 and 0006.",
      "Implement at least four fixed non-oracle behavior policies that span expected coverage levels without consulting exact Q or exact DP for action selection.",
      "Run gamma in {0.95, 0.99, 0.995} over 10 seeds per behavior with a CPU-tabular budget no larger than 0006 unless a smaller pilot shows adequate coverage is impossible.",
      "Record direct sampled-vs-deterministic-soft target mean error, terminal-sampling variance, g_plus events, right-reward events, visited state-action pairs, Bellman residual, value error, policy disagreement, and greedy raw return.",
      "Stratify outputs by coverage bin and compute soft-minus-sampled deltas for Bellman residual, value error, and greedy return.",
      "Save research/reward_to_gcrl/results/0007_result.json with raw metrics, exact commands, behavior definitions, pass/fail flags, and coverage-bin summaries.",
      "Save research/reward_to_gcrl/results/0007_summary.md with a conservative verdict on whether coverage is sufficiently bounded to proceed to tabular auxiliary state-goal experiments."
    ],
    "required_outputs": [
      "research/reward_to_gcrl/artifacts/0007/run_riverswim_coverage_dose_response.py",
      "research/reward_to_gcrl/artifacts/0007/environment_audit.json",
      "research/reward_to_gcrl/artifacts/0007/behavior_policy_audit.json",
      "research/reward_to_gcrl/artifacts/0007/exact_dp_references.json",
      "research/reward_to_gcrl/results/0007_result.json",
      "research/reward_to_gcrl/results/0007_summary.md",
      "Exact command used to run the experiment",
      "Coverage-bin table for starved, borderline, and adequate regimes",
      "Direct sampled-vs-deterministic-soft target comparison metrics",
      "Bellman residual, value error, policy disagreement, and greedy raw-return metrics",
      "Final recommendation: proceed_to_auxiliary_goals, repeat_coverage_test, or downgrade_to_variance_only_claim"
    ],
    "estimated_runtime_minutes": 25
  }
}

You are making credible progress, but the claim should remain “soft marginalization is a lower-variance estimator that helps under adequate coverage,” not yet “reward-to-GCRL works generally.”