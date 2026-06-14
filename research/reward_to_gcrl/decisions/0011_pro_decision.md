# ChatGPT Pro Decision: pivot

Confidence: 0.9

## Rationale

Pivot from further auxiliary-goal experimentation to consolidation and write-up. The project is making real progress on the soft-terminal estimator story, but the auxiliary/shared-representation hypothesis is currently unsupported. Experiments 0009 and 0010 are valid negative evidence: the first shared low-rank FourRooms auxiliary test collapsed, and the predeclared repair diagnostic reproduced negative transfer rather than fixing it. Continuing to larger sweeps, neural frameworks, or auxiliary-goal claims would reward activity over evidence. The next best move is to pause the low-rank auxiliary thread and produce a short evidence report separating the positive estimator claim from the negative auxiliary result.

## Evidence

- 0001-0007 support the core estimator claim: deterministic soft terminal marginalization preserves normalized-Q scaling, removes terminal-sampling variance, and helps under adequate coverage in small tabular settings.
- 0008 validated tabular vector SSM indexing: g_plus matched terminal-only exactly, scaled g_plus matched normalized Q to 1.1102230246251565e-16, and real-state goal slices had zero value error.
- 0009 was the first genuinely shared low-rank test with M_hat(s,a,g)=sigmoid(u_sa dot v_g + b_g), CPU-only NumPy, matched replay, matched seeds, rank 4, learning rate 0.05, and adequate coverage.
- 0009 produced negative transfer: terminal-only had mean Bellman residual 0.0009558486 and mean scaled value error 0.0731219459, while combined auxiliary training worsened mean Bellman residual to 0.0364139480 and mean scaled value error to 16.8938684161.
- 0010 reproduced the original negative-transfer result under the same audited FourRooms setup.
- 0010 tested only the four predeclared variants: terminal-only, original combined, loss-balanced combined, and staged auxiliary pretrain then g_plus fine-tuning.
- Neither repaired auxiliary variant matched terminal-only on g_plus value error and Bellman residual.
- The 0010 review labels the result auxiliary_unsupported_for_lowrank and warns that expanding to neural frameworks, GPU, larger environments, or broad sweeps would overreach.

## Risks

- The negative auxiliary conclusion is limited to one rank-4 NumPy low-rank architecture, optimizer, replay setup, and gamma.
- The loss-balanced variant still had large auxiliary-to-g_plus shared-factor gradient dominance, so scale imbalance may remain unresolved.
- Terminal-only is imperfect, so the result supports pausing this low-rank auxiliary thread, not claiming that auxiliary goals are generally harmful.
- Uniform state-action reset replay gives adequate coverage but is less realistic than trajectory-only offline data.
- A report could overstate the estimator story if it does not clearly separate matched-stream estimator evidence from online exploration evidence.
- A report could overstate the auxiliary result if it presents one low-rank failure as a general impossibility theorem.

## Next experiment

- Experiment id: `0011`
- Objective: Produce a compact evidence-synthesis report that separates the positive soft-terminal estimator result from the negative low-rank auxiliary-goal result, and defines what evidence would be required before reopening auxiliary-goal experiments.
