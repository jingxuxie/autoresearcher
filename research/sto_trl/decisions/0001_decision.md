# Decision: continue

Confidence: 0.89
Progress score: 1

## Rationale

This is project start: iteration is 0, no latest result is expected, the environment is ready, and the charter gives a specific, cheap first experiment. The next step should be one small tabular harness that tests deterministic sanity and a risky-shortcut stochastic diagnostic against exact DP ground truth.

## Evidence

- research/sto_trl/state.json reports iteration 0, status active, and no prior primary metric.
- research/sto_trl/env_state.json reports status ready for conda environment autoresearcher_sto_trl with JAX GPU probe completed.
- The charter explicitly scopes early work to tabular experiments and requires exact DP ground truth, deterministic chain sanity, risky shortcut MDP, offline data, and MC/TRL baselines.
- No result JSON exists yet, which is allowed by the first-iteration rule.

## Risks

- A first harness can appear to make progress while only testing training loss; require exact DP value and policy calibration metrics.
- TRL-raw, TRL-log, and MC+TRL-log may be implemented inconsistently unless the result saves raw per-method metrics and coverage diagnostics.
- The risky shortcut can be under-specified; include both lucky and unlucky stochastic outcomes in offline coverage and evaluate risky action selection under exact DP.
- Avoid expanding to neural networks, OGBench, or long sweeps before the tabular diagnostic is reproducible.

## Next experiment

- Experiment id: `0001`
- Objective: Build and run a minimal tabular diagnostic for stochastic TRL covering deterministic chain sanity and one risky-shortcut stochastic MDP, with exact discounted-reachability DP ground truth and raw metrics saved.
