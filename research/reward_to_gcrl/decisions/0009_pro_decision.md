# ChatGPT Pro Decision: continue

Confidence: 0.86

## Rationale

Continue to the first shared-parameter milestone, but keep it explicitly as a small checkpointed pilot rather than a publishable auxiliary-goal claim. The repository evidence now supports the core tabular estimator story: soft terminal marginalization preserves normalized-Q scaling, removes terminal-sampling variance, works in small nondegenerate chains, and has RiverSwim evidence under controlled and non-oracle coverage regimes. The latest 0008 result also validated vector SSM indexing on tiny FourRooms, including real-state goal slices that do not perturb g_plus. The next unresolved question is whether auxiliary real-state goals help when parameters are actually shared. A CPU-only NumPy low-rank factorized FourRooms experiment is the right next step.

## Evidence

- The latest summary reports no current blocker and protected_file_drift false.
- Reviewed evidence reaches 0008, with strong small-tabular support for the estimator story: deterministic soft terminal marginalization preserves normalized-Q scaling while removing terminal-sampling variance.
- 0004 repaired the degenerate CliffWalking issue with a nondegenerate 5-state chain and showed soft improved Bellman/value error and policy success over sampled.
- 0005 and 0006 extended the estimator story to 6-state RiverSwim, including non-oracle behavior streams, while exposing coverage as a key condition.
- 0007 ran a RiverSwim coverage dose-response and found adequate-coverage runs favored soft on mean Bellman residual and value error, while starved runs remained coverage-limited.
- 0008 passed the tabular vector SSM implementation gate: max_abs_vector_gplus_minus_terminal_only was 0, scaled vector g_plus matched normalized Q within 1.1102230246251565e-16, and real-state goal slices had zero value error and min greedy goal success rate 1.0.
- The 0008 review explicitly warns that independent tabular slices do not test sampled learning, low-rank coupling, or auxiliary representation benefit.
- The latest local decision 0009 recommends a CPU-only low-rank factorized SSM on tiny FourRooms comparing terminal-only g_plus training against combined real-state-plus-g_plus auxiliary training under limited offline replay.

## Risks

- A positive low-rank FourRooms result would be early shared-parameter evidence only, not a general GCRL or neural-function-approximation claim.
- Auxiliary state-goal losses may hurt the g_plus reward head through negative transfer, especially if the auxiliary weight is too high.
- Low-rank NumPy optimization can be sensitive to initialization, rank, target scaling, replay coverage, and step size; raw per-seed metrics must be saved.
- If the replay dataset is coverage-starved, a failure may reflect data coverage rather than auxiliary-goal interference.
- If too many hyperparameters are swept, the result will look like tuning rather than a clean first shared-parameter checkpoint.
- Moving to PyTorch, JAX, GPU, larger FourRooms variants, or publishable auxiliary-goal claims before review would overrun the evidence.

## Next experiment

- Experiment id: `0009`
- Objective: Run the first CPU-only NumPy shared-parameter test on tiny FourRooms using a low-rank factorized soft successor-measure model, comparing terminal-only g_plus training against combined g_plus plus real-state auxiliary-goal training under matched limited offline replay.
