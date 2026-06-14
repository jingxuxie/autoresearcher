# Decision: continue

Confidence: 0.83
Progress score: 7

## Rationale

Experiment 0008 is a strong reviewed pass for the tabular vector SSM implementation gate: real-state goal slices work and do not perturb the g_plus slice. The next planned milestone is the first shared-parameter test. Keep it small and CPU-only: a low-rank numpy factorized SSM on tiny FourRooms, comparing terminal-only g_plus training against combined real-state-plus-g_plus training under limited replay.

## Evidence

- research/reward_to_gcrl/results/0008_result.json is present, schema-valid, and reports status completed with exact commands and declared artifacts.
- research/reward_to_gcrl/reviews/0008_review.json reports verdict pass, evidence_quality strong, allows_auto_continue true, and no triggered failure criteria.
- 0008 showed max_abs_vector_gplus_minus_terminal_only = 0 and max_abs_vector_gplus_scaled_minus_q_norm = 1.1102230246251565e-16.
- 0008 real-state goal slices had max value error 0, min greedy goal success rate 1.0, and zero goal-policy disagreement versus exact references.
- The 0008 review correctly flags that this was an exact deterministic independent-slice sanity check, not sampled learning or function approximation.
- The prototype plan identifies the next milestone as low-capacity shared/factorized SSM, where auxiliary real-state goals can first provide a meaningful representation-learning signal.

## Risks

- Low-rank results can be sensitive to optimizer, initialization, target scaling, and dataset coverage; raw per-seed metrics and failure modes must be saved.
- A positive result on tiny FourRooms would be only early shared-representation evidence, not a general GCRL claim.
- Auxiliary state goals can hurt the g_plus head if lambda_state is too high; negative transfer should be reported, not tuned away silently.
- Do not install large dependencies or move to PyTorch/JAX/GPU for this first factorized check; numpy is sufficient.

## Next experiment

- Experiment id: `0009`
- Objective: Run the first CPU-only low-rank factorized SSM test on tiny FourRooms, comparing terminal-only g_plus training against combined real-state-plus-g_plus auxiliary training under limited offline replay.
