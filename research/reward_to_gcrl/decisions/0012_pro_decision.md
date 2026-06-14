# ChatGPT Pro Decision: pivot

Confidence: 0.91

## Rationale

Pivot from running more experiments to packaging the current evidence and defining a new hypothesis gate. The project is making real progress on the soft-terminal estimator component, which is now well supported across small audited tabular settings. But the auxiliary/shared-representation direction is not supported: 0009 produced negative transfer, 0010 reproduced it after predeclared repair attempts, and 0011 passed as a report-only synthesis separating supported estimator claims from unsupported auxiliary claims. More compute, larger sweeps, neural frameworks, or auxiliary-goal claims would overreach unless a genuinely new falsifiable hypothesis is approved.

## Evidence

- 0011 is a reviewed report-only synthesis with verdict pass and strong evidence quality; no new learning compute was run.
- 0001-0007 support the core estimator claim: deterministic soft terminal marginalization preserves normalized-Q scaling, removes terminal-sampling variance, and helps under adequate coverage in small tabular settings.
- 0008 validated tabular vector SSM indexing: g_plus matched terminal-only exactly, scaled g_plus matched normalized Q to 1.1102230246251565e-16, and real-state goal slices had zero value error.
- 0009 was the first shared low-rank FourRooms auxiliary test with M_hat(s,a,g)=sigmoid(u_sa dot v_g + b_g), and it produced valid negative transfer.
- 0009 terminal-only had mean Bellman residual 0.0009558486 and mean scaled value error 0.0731219459, while combined auxiliary training worsened mean Bellman residual to 0.0364139480 and mean scaled value error to 16.8938684161.
- 0010 reproduced the negative-transfer result and tested only the four predeclared variants: terminal-only, original combined, loss-balanced combined, and staged auxiliary pretrain followed by g_plus fine-tuning.
- Neither loss-balanced nor staged auxiliary repair matched terminal-only on g_plus value error and Bellman residual.
- 0011 correctly frames the current state: positive estimator claims are supported only in scoped small-tabular settings, while low-rank shared real-state auxiliary training did not help g_plus in the tested rank-4 FourRooms setup.

## Risks

- A write-up could overstate the estimator story if it ignores matched-stream and coverage caveats.
- A write-up could overstate the auxiliary negative result if it presents one rank-4 NumPy architecture as a general impossibility claim.
- The positive estimator evidence remains small-scale and mostly tabular; it does not establish neural, large-environment, online-exploration, or benchmark generality.
- The auxiliary conclusion is limited to one architecture family, optimizer, replay setup, gamma, and predeclared repair set.
- Starting PyTorch/JAX, GPU, larger FourRooms, or broad hyperparameter sweeps now would reward activity over evidence.
- A new auxiliary experiment is justified only if it changes architecture or loss normalization for a principled reason rather than tuning around a negative result.

## Next experiment

- Experiment id: `0012`
- Objective: Package the current evidence into a concise research memo or draft note, and define a formal gate for any future auxiliary-goal experiments. No new learning compute should be run.
