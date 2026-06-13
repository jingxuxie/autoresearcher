# AGENTS.md

This repository is controlled by an autoresearcher loop.

Hard rules for all Codex sessions:

1. Do not change the research goal unless the task explicitly asks for a pivot proposal.
2. Do not delete previous experiment plans, results, reviews, decisions, or artifacts.
3. Every experiment must be small-scale and suitable for fast validation.
4. The executor must finish within the configured timeout, normally 30 minutes.
5. Every experiment must produce:
   - `research/<project>/results/NNNN_result.json`
   - `research/<project>/results/NNNN_summary.md`
   - artifacts under `research/<project>/artifacts/NNNN/` when applicable
6. Every result must include exact commands run.
7. Negative results are valuable. Do not hide failures.
8. Do not claim success unless the predeclared success criteria are satisfied.
9. Do not install large dependencies, download large datasets, or run expensive training without explicit human approval.
10. Prefer small, decisive experiments over broad exploration.
11. For numerical claims, save raw metrics, not just prose.
12. Do not edit `scripts/autoresearcher.py`, schemas, or this file unless explicitly instructed.
13. Every project must use its own conda environment described by `research/<project>/environment.yaml`.
14. The main research loop must not start until `research/<project>/env_state.json` reports `status: "ready"`.
15. GPU setup and GPU experiment runs require the configured escalation policy; if GPU, network, or conda access is blocked, write a blocker with the exact failed command.
