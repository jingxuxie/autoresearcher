# ChatGPT Pro Decision: pivot

Confidence: 0.87

## Rationale

Pivot within the same research direction. The project has made real progress on the core estimator story, but the first shared-parameter auxiliary-goal milestone produced valid negative-transfer evidence, not auxiliary-benefit evidence. The next step should not expand to neural frameworks, larger sweeps, or publishable auxiliary-goal claims. It should run one small diagnostic to determine whether 0009 failed because auxiliary real-state goals are harmful in this setup, or because the low-rank model collapsed due to loss scaling, gradient imbalance, or optimization details.

## Evidence

- Reviewed evidence now reaches 0009, with no current blocker and protected_file_drift false.
- 0001-0007 support the estimator story: deterministic soft terminal marginalization preserves normalized-Q scaling, removes terminal-sampling variance, and helps under adequate coverage in small tabular RiverSwim and repaired chain settings.
- 0008 passed the vector SSM sanity gate: real-state goal slices were exact and did not perturb the g_plus slice, but the review correctly noted it was independent-slice tabular evidence, not shared representation evidence.
- 0009 was the first genuinely shared low-rank FourRooms test: M_hat(s,a,g)=sigmoid(u_sa dot v_g + b_g), with u_sa shared across real-state goals and g_plus.
- 0009 used CPU-only NumPy, audited FourRooms semantics from 0008, matched replay datasets, matched seeds, matched optimizer budgets, rank 4, learning rate 0.05, and adequate replay coverage for all 10 seeds.
- 0009 produced a valid negative result: terminal-only g_plus had mean Bellman residual 0.0009558486, mean scaled value error 0.0731219459, and mean reward success rate 0.5384615385.
- 0009 combined auxiliary training collapsed: mean g_plus Bellman residual worsened to 0.0364139480, mean scaled value error worsened to 16.8938684161, reward success fell to 0.0, and real-goal diagnostics were also poor.
- The 0009 review explicitly labels this as negative_transfer and warns that it may reflect optimizer or loss-scaling issues rather than a general impossibility of auxiliary goals.

## Risks

- A diagnostic ablation could become an unprincipled hyperparameter sweep if too many ranks, losses, and auxiliary weights are tried.
- If loss scaling fixes the collapse, the evidence will still be tiny NumPy low-rank evidence, not a neural or publishable auxiliary-goal claim.
- If loss scaling does not fix the collapse, the correct conclusion may be to stop the auxiliary-goal thread for this architecture and write up the negative result.
- Replay uses uniform state-action resets, so even a repaired result may not transfer to realistic trajectory-only offline data.
- Both terminal-only and combined models have imperfect reward policies, so improvements must be judged against terminal-only and exact references, not absolute success alone.
- Expanding to PyTorch, JAX, GPU, larger FourRooms, or broad auxiliary-goal claims before this diagnostic is reviewed would overinterpret the evidence.

## Next experiment

- Experiment id: `0010`
- Objective: Diagnose the 0009 negative transfer in the shared low-rank FourRooms SSM by testing whether auxiliary collapse is caused by loss-scaling or optimization imbalance, while keeping the run CPU-only, NumPy-only, tiny, and predeclared.
