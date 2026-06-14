from __future__ import annotations

import json
import os
import shutil
import stat
import subprocess
import sys
import tempfile
import textwrap
import unittest
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = REPO_ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import autoresearcher  # noqa: E402
from checkpoint_policy import pro_checkpoint_due  # noqa: E402
from build_context import build_context  # noqa: E402
from kill_process_tree import run_with_timeout  # noqa: E402
from metrics_ledger import build_metric_ledger, write_metric_ledger  # noqa: E402
from validate_artifacts import validate_json_schema  # noqa: E402
from worktree_guard import protected_file_drift, write_guard_report  # noqa: E402


def write_json(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n")


def make_repo(tmp: Path, project: str = "project_001") -> Path:
    shutil.copytree(REPO_ROOT / "prompts", tmp / "prompts")
    shutil.copytree(REPO_ROOT / "schemas", tmp / "schemas")
    (tmp / "autoresearcher.yaml").write_text(autoresearcher.DEFAULT_CONFIG_TEXT)
    root = tmp / "research" / project
    for subdir in ("plans", "results", "reviews", "decisions", "packets", "pro_packets", "artifacts", "setup_logs", "progress"):
        (root / subdir).mkdir(parents=True, exist_ok=True)
    (root / "charter.md").write_text("# Charter\n\nTest charter includes synthetic accuracy.\n")
    write_json(root / "state.json", autoresearcher.DEFAULT_STATE)
    env_name = autoresearcher.conda_env_name_for_project(project)
    (root / "environment.yaml").write_text(autoresearcher.default_environment_yaml(env_name))
    write_json(root / "env_state.json", autoresearcher.default_env_state(project, env_name))
    return tmp


def make_fake_codex(tmp: Path) -> Path:
    script = tmp / "fake_codex.py"
    script.write_text(
        textwrap.dedent(
            """\
            #!/usr/bin/env python3
            import json
            import os
            import sys
            from pathlib import Path

            args = sys.argv[1:]
            log = os.environ.get("FAKE_CODEX_ARG_LOG")
            if log:
                Path(log).write_text(json.dumps(args))

            if args[:2] == ["debug", "models"]:
                print(json.dumps({"models": [{"id": "gpt-5.5"}]}))
                raise SystemExit(0)

            output_path = Path(args[args.index("--output-last-message") + 1])
            repo_root = Path(args[args.index("--cd") + 1])
            output_path.parent.mkdir(parents=True, exist_ok=True)

            print(json.dumps({"type": "thread.started", "thread_id": "thread-fake"}))
            name = output_path.name

            if name.endswith("_decision.json"):
                decision = os.environ.get("FAKE_DECISION", "continue")
                output_path.write_text(json.dumps({
                    "decision": decision,
                    "confidence": 0.8,
                    "progress_score": 6,
                    "rationale": "Run the tiny positive-control experiment.",
                    "evidence": ["Project charter asks for a toy positive control."],
                    "risks": ["Toy result may not generalize."],
                    "checkpoint_recommended": False,
                    "checkpoint_reason": None,
                    "terminal_decision_requires_pro": False,
                    "next_experiment": {
                        "experiment_id": "0001",
                        "objective": "Compare a weak baseline to a corrected method.",
                        "hypothesis": "Corrected counting is more accurate than the weak baseline.",
                        "success_criteria": ["corrected_accuracy > baseline_accuracy"],
                        "failure_criteria": ["missing result JSON"],
                        "tasks_for_codex": ["Write a tiny deterministic metric artifact."],
                        "required_outputs": [
                            "research/project_001/results/0001_result.json",
                            "research/project_001/results/0001_summary.md",
                            "research/project_001/artifacts/0001/"
                        ],
                        "estimated_runtime_minutes": 1
                    }
                }))
            elif name == "env_state.json":
                project = output_path.parent.name
                env_name = f"autoresearcher_{project}"
                output_path.write_text(json.dumps({
                    "project": project,
                    "status": "ready",
                    "conda_env_name": env_name,
                    "conda_env_path": None,
                    "environment_file": f"research/{project}/environment.yaml",
                    "commands_run": [
                        f"conda env create -f research/{project}/environment.yaml",
                        f"conda run -n {env_name} python --version",
                        "nvidia-smi"
                    ],
                    "packages_verified": ["python"],
                    "gpu_requested": True,
                    "gpu_available": False,
                    "gpu_checks": ["nvidia-smi unavailable in fake test"],
                    "summary": "Fake setup completed.",
                    "blocker": None
                }))
                (repo_root / "research" / project / "setup_logs").mkdir(parents=True, exist_ok=True)
                (repo_root / "research" / project / "setup_logs" / "setup_summary.md").write_text("# Setup\\n\\nFake setup completed.\\n")
            elif "executor_last_message" in name:
                output_path.write_text("executor done\\n")
                if not os.environ.get("FAKE_MISSING_RESULT"):
                    project = output_path.parent.name
                    iteration = name.split("_", 1)[0]
                    result_dir = repo_root / "research" / project / "results"
                    artifact_dir = repo_root / "research" / project / "artifacts" / iteration
                    result_dir.mkdir(parents=True, exist_ok=True)
                    artifact_dir.mkdir(parents=True, exist_ok=True)
                    metrics = artifact_dir / "metrics.json"
                    metrics.write_text(json.dumps({"baseline_accuracy": 0.5, "corrected_accuracy": 1.0}))
                    (result_dir / f"{iteration}_result.json").write_text(json.dumps({
                        "experiment_id": iteration,
                        "status": "completed",
                        "claim_tested": "Corrected method beats weak baseline.",
                        "commands_run": ["python toy_eval.py"],
                        "metrics": {"corrected_accuracy": 1.0},
                        "baseline_metrics": {"baseline_accuracy": 0.5},
                        "artifacts": [f"research/{project}/artifacts/{iteration}/metrics.json"],
                        "interpretation": "Corrected method wins on the toy task.",
                        "known_failures": [],
                        "next_questions": ["Validate on a less trivial toy task."]
                    }))
                    (result_dir / f"{iteration}_summary.md").write_text("# Summary\\n\\nCorrected method wins.\\n")
            elif name.endswith("_review.json"):
                iteration = name.split("_", 1)[0]
                output_path.write_text(json.dumps({
                    "experiment_id": iteration,
                    "verdict": os.environ.get("FAKE_REVIEW_VERDICT", "pass"),
                    "allows_auto_continue": os.environ.get("FAKE_REVIEW_VERDICT", "pass") in ("pass", "weak_pass"),
                    "reasons": ["Required files and metrics are present."],
                    "evidence_checked": ["result JSON", "metrics artifact"],
                    "required_fixes": [],
                    "risk_flags": [],
                    "evidence_quality": "medium",
                    "success_criteria_satisfied": True,
                    "failure_criteria_triggered": False,
                    "should_escalate_to_pro": False,
                    "escalation_reason": None
                }))
            elif name.endswith("_summary.md") and output_path.parent.name == "progress":
                output_path.write_text("# Progress Summary\\n\\nFake project progress summary.\\n")
            else:
                output_path.write_text("ok\\n")
            """
        )
    )
    script.chmod(script.stat().st_mode | stat.S_IXUSR)
    return script


def fake_pro_response(path: Path, decision: str = "continue") -> None:
    next_experiment = None
    if decision in ("continue", "pivot"):
        next_experiment = {
            "experiment_id": "0001",
            "objective": "Run one more tiny controlled experiment.",
            "hypothesis": "The controlled experiment resolves the open question.",
            "success_criteria": ["metric improves"],
            "failure_criteria": ["required result missing"],
            "tasks_for_codex": ["Write a tiny artifact and result JSON."],
            "required_outputs": [
                "research/project_001/results/0001_result.json",
                "research/project_001/results/0001_summary.md",
                "research/project_001/artifacts/0001/",
            ],
            "estimated_runtime_minutes": 1,
        }
    response = {
        "decision": decision,
        "confidence": 0.82,
        "rationale": "Fake Pro decision for tests.",
        "evidence": ["Reviewed packet evidence."],
        "risks": ["Toy fake response."],
        "next_experiment": next_experiment,
    }
    path.write_text("# ChatGPT Pro Decision\n\n```json\n" + json.dumps(response, indent=2) + "\n```\n")


class ContextBuilderTests(unittest.TestCase):
    def test_init_scaffold_includes_environment_files(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            repo = Path(td)
            shutil.copytree(REPO_ROOT / "prompts", repo / "prompts")
            shutil.copytree(REPO_ROOT / "schemas", repo / "schemas")
            (repo / "autoresearcher.yaml").write_text(autoresearcher.DEFAULT_CONFIG_TEXT)
            autoresearcher.ensure_project_scaffold(repo, "new_project")
            root = repo / "research" / "new_project"
            self.assertTrue((root / "environment.yaml").exists())
            env_state = json.loads((root / "env_state.json").read_text())
            self.assertEqual(env_state["conda_env_name"], "autoresearcher_new_project")
            self.assertEqual(env_state["status"], "pending")

    def test_context_builder_includes_charter_state_latest_result_and_review(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            repo = make_repo(Path(td))
            root = repo / "research" / "project_001"
            state = dict(autoresearcher.DEFAULT_STATE)
            state["iteration"] = 1
            write_json(root / "state.json", state)
            write_json(root / "results" / "0001_result.json", {
                "experiment_id": "0001",
                "status": "completed",
                "claim_tested": "claim",
                "commands_run": [],
                "metrics": {},
                "baseline_metrics": {},
                "artifacts": [],
                "interpretation": "interp",
                "known_failures": [],
                "next_questions": [],
            })
            (root / "results" / "0001_summary.md").write_text("summary body")
            write_json(root / "reviews" / "0001_review.json", {
                "experiment_id": "0001",
                "verdict": "pass",
                "allows_auto_continue": True,
                "reasons": ["ok"],
                "evidence_checked": ["result"],
                "required_fixes": [],
                "risk_flags": [],
            })
            context = build_context(repo, "project_001", "supervisor")
            self.assertIn("Test charter", context)
            self.assertIn('"iteration": 1', context)
            self.assertIn('"claim_tested": "claim"', context)
            self.assertIn('"verdict": "pass"', context)

    def test_supervisor_context_compacts_large_latest_result(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            repo = make_repo(Path(td))
            root = repo / "research" / "project_001"
            state = dict(autoresearcher.DEFAULT_STATE)
            state["iteration"] = 1
            write_json(root / "state.json", state)
            write_json(root / "results" / "0001_result.json", {
                "experiment_id": "0001",
                "status": "completed",
                "claim_tested": "large rows should not be embedded in full",
                "commands_run": [],
                "metrics": {"score": 1.0},
                "baseline_metrics": {
                    "main_rows": [
                        {"row_marker": f"row_{idx}", "value": idx}
                        for idx in range(100)
                    ],
                    "scalar": 0.5,
                },
                "artifacts": ["research/project_001/artifacts/0001/metrics.json"],
                "interpretation": "interp",
                "known_failures": [],
                "next_questions": [],
            })
            (root / "results" / "0001_summary.md").write_text("summary body")
            write_json(root / "reviews" / "0001_review.json", {
                "experiment_id": "0001",
                "verdict": "pass",
                "allows_auto_continue": True,
                "reasons": ["ok"],
                "evidence_checked": ["result"],
                "required_fixes": [],
                "risk_flags": [],
            })
            context = build_context(repo, "project_001", "supervisor")
            self.assertIn("Latest result summary", context)
            self.assertIn("research/project_001/results/0001_result.json", context)
            self.assertIn("large rows should not be embedded in full", context)
            self.assertNotIn("row_99", context)
            self.assertLess(len(context), 50000)

    def test_reviewer_context_compacts_large_latest_result(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            repo = make_repo(Path(td))
            root = repo / "research" / "project_001"
            write_json(root / "plans" / "0001_plan.json", {
                "experiment_id": "0001",
                "objective": "o",
                "hypothesis": "h",
                "success_criteria": ["s"],
                "failure_criteria": ["f"],
                "tasks_for_codex": ["t"],
                "required_outputs": ["x"],
                "estimated_runtime_minutes": 1,
            })
            (root / "plans" / "0001_plan.md").write_text("# Plan\n")
            write_json(root / "results" / "0001_result.json", {
                "experiment_id": "0001",
                "status": "completed",
                "claim_tested": "large reviewer rows should not be embedded in full",
                "commands_run": [],
                "metrics": {"score": 1.0},
                "baseline_metrics": {
                    "main_rows": [
                        {"row_marker": f"review_row_{idx}", "value": idx}
                        for idx in range(100)
                    ],
                },
                "artifacts": ["research/project_001/artifacts/0001/metrics.json"],
                "interpretation": "interp",
                "known_failures": [],
                "next_questions": [],
            })
            (root / "results" / "0001_summary.md").write_text("summary body")
            context = build_context(repo, "project_001", "reviewer")
            self.assertIn("Latest result summary", context)
            self.assertIn("research/project_001/results/0001_result.json", context)
            self.assertIn("large reviewer rows should not be embedded in full", context)
            self.assertNotIn("review_row_99", context)
            self.assertLess(len(context), 50000)

    def test_summarizer_context_includes_experiment_ledger(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            repo = make_repo(Path(td))
            root = repo / "research" / "project_001"
            state = dict(autoresearcher.DEFAULT_STATE)
            state["iteration"] = 1
            write_json(root / "state.json", state)
            write_json(root / "plans" / "0001_plan.json", {
                "experiment_id": "0001",
                "objective": "Measure whether the corrected toy method improves accuracy.",
                "hypothesis": "Corrected counting is better.",
                "success_criteria": ["s"],
                "failure_criteria": ["f"],
                "tasks_for_codex": ["t"],
                "required_outputs": ["x"],
                "estimated_runtime_minutes": 1,
            })
            write_json(root / "results" / "0001_result.json", {
                "experiment_id": "0001",
                "status": "completed",
                "claim_tested": "Corrected method beats weak baseline.",
                "commands_run": [],
                "metrics": {"corrected_accuracy": 1.0},
                "baseline_metrics": {"baseline_accuracy": 0.5},
                "artifacts": [],
                "interpretation": "Corrected method wins on the toy task.",
                "known_failures": [],
                "next_questions": [],
            })
            write_json(root / "reviews" / "0001_review.json", {
                "experiment_id": "0001",
                "verdict": "pass",
                "allows_auto_continue": True,
                "reasons": ["Required files and metrics are present."],
                "evidence_checked": ["result"],
                "required_fixes": [],
                "risk_flags": [],
            })
            context = build_context(repo, "project_001", "summarizer")
            self.assertIn("Experiment ledger", context)
            self.assertIn('"iteration": "0001"', context)
            self.assertIn("corrected_accuracy", context)
            self.assertIn('"review": "pass"', context)

    def test_setup_context_includes_environment_contract(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            repo = make_repo(Path(td))
            context = build_context(repo, "project_001", "setup_env")
            self.assertIn("Environment YAML", context)
            self.assertIn('"gpu_requested"', context)
            self.assertIn("conda", context)


class CodexRunnerTests(unittest.TestCase):
    def test_fresh_run_parses_thread_started_session_id(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            repo = make_repo(Path(td))
            fake = make_fake_codex(Path(td))
            config = autoresearcher.load_config(repo)
            runner = autoresearcher.CodexRunner(repo, config, codex_bin=str(fake))
            result = runner.run_role(
                project="project_001",
                role="supervisor",
                prompt="prompt",
                output_path=repo / "out.json",
                schema_path=None,
                sandbox="read-only",
                timeout_minutes=1,
                resume=True,
            )
            self.assertEqual(result.session_id, "thread-fake")
            local = autoresearcher.load_local_state(repo, "project_001")
            self.assertEqual(local["projects"]["project_001"]["codex_sessions"]["supervisor"]["session_id"], "thread-fake")

    def test_role_resume_uses_stored_session_id(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            repo = make_repo(Path(td))
            fake = make_fake_codex(Path(td))
            arg_log = Path(td) / "args.json"
            state = autoresearcher.load_local_state(repo, "project_001")
            state["projects"]["project_001"]["codex_sessions"]["supervisor"]["session_id"] = "existing-session"
            autoresearcher.save_local_state(repo, state)
            config = autoresearcher.load_config(repo)
            runner = autoresearcher.CodexRunner(repo, config, codex_bin=str(fake))
            old = os.environ.get("FAKE_CODEX_ARG_LOG")
            os.environ["FAKE_CODEX_ARG_LOG"] = str(arg_log)
            try:
                runner.run_role(
                    project="project_001",
                    role="supervisor",
                    prompt="prompt",
                    output_path=repo / "out.json",
                    schema_path=None,
                    sandbox="read-only",
                    timeout_minutes=1,
                    resume=True,
                )
            finally:
                if old is None:
                    os.environ.pop("FAKE_CODEX_ARG_LOG", None)
                else:
                    os.environ["FAKE_CODEX_ARG_LOG"] = old
            args = json.loads(arg_log.read_text())
            self.assertIn("resume", args)
            self.assertIn("existing-session", args)

    def test_gpu_roles_use_configured_gpu_sandbox(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            repo = make_repo(Path(td))
            fake = make_fake_codex(Path(td))
            arg_log = Path(td) / "args.json"
            config = autoresearcher.load_config(repo)
            old = os.environ.get("FAKE_CODEX_ARG_LOG")
            os.environ["FAKE_CODEX_ARG_LOG"] = str(arg_log)
            try:
                with redirect_stdout(StringIO()), redirect_stderr(StringIO()):
                    autoresearcher.Orchestrator(repo, config, codex_bin=str(fake)).setup_environment("project_001")
            finally:
                if old is None:
                    os.environ.pop("FAKE_CODEX_ARG_LOG", None)
                else:
                    os.environ["FAKE_CODEX_ARG_LOG"] = old
            args = json.loads(arg_log.read_text())
            sandbox_index = args.index("--sandbox") + 1
            self.assertEqual(args[sandbox_index], "danger-full-access")


class ValidationAndPlanTests(unittest.TestCase):
    def test_supervisor_decision_json_validates(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            repo = make_repo(Path(td))
            decision = repo / "decision.json"
            write_json(decision, {
                "decision": "continue",
                "confidence": 0.7,
                "progress_score": 5,
                "rationale": "r",
                "evidence": [],
                "risks": [],
                "checkpoint_recommended": False,
                "checkpoint_reason": None,
                "terminal_decision_requires_pro": False,
                "next_experiment": {
                    "experiment_id": "0001",
                    "objective": "o",
                    "hypothesis": "h",
                    "success_criteria": ["s"],
                    "failure_criteria": ["f"],
                    "tasks_for_codex": ["t"],
                    "required_outputs": ["x"],
                    "estimated_runtime_minutes": 1,
                },
            })
            validate_json_schema(decision, repo / "schemas" / "decision.schema.json")

    def test_plan_markdown_is_generated(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            repo = make_repo(Path(td))
            experiment = autoresearcher.normalize_experiment_paths("project_001", "0001", {
                "experiment_id": "other",
                "objective": "Objective text",
                "hypothesis": "Hypothesis text",
                "success_criteria": ["success"],
                "failure_criteria": ["failure"],
                "tasks_for_codex": ["task"],
                "required_outputs": [],
                "estimated_runtime_minutes": 2,
            })
            _, plan_md = autoresearcher.write_plan(repo, "project_001", "0001", experiment)
            text = plan_md.read_text()
            self.assertIn("# Experiment 0001", text)
            self.assertIn("Objective text", text)
            self.assertIn("research/project_001/results/0001_result.json", text)

    def test_timeout_result_json_validates(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            repo = make_repo(Path(td))
            written = autoresearcher.write_timeout_result(repo, "project_001", "0001")
            self.assertTrue(all(path.exists() for path in written))
            validate_json_schema(
                repo / "research" / "project_001" / "results" / "0001_result.json",
                repo / "schemas" / "result.schema.json",
            )

    def test_timeout_command_terminates_process_group(self) -> None:
        result = run_with_timeout(
            [
                sys.executable,
                "-c",
                "import subprocess, time; subprocess.Popen(['sleep','60']); time.sleep(60)",
            ],
            timeout_seconds=0.2,
            grace_seconds=0.1,
        )
        self.assertTrue(result.timed_out)
        self.assertNotEqual(result.return_code, 0)


class StateAndLoopTests(unittest.TestCase):
    def test_pass_review_resets_no_progress_even_with_low_planning_score(self) -> None:
        state = dict(autoresearcher.DEFAULT_STATE)
        state["no_progress_rounds"] = 2
        state["failure_streak"] = 2
        state["last_failure"] = {"note": "prior retryable failure"}
        decision = {"decision": "continue", "progress_score": 1}
        review = {
            "verdict": "pass",
            "allows_auto_continue": True,
            "reasons": [],
            "evidence_checked": [],
            "required_fixes": [],
            "risk_flags": [],
        }
        autoresearcher.update_state_after_review(state, 3, decision, review, max_no_progress_rounds=3)
        self.assertEqual(state["no_progress_rounds"], 0)
        self.assertEqual(state["failure_streak"], 0)
        self.assertIsNone(state["last_failure"])
        self.assertFalse(state["human_review_required"])
        self.assertEqual(state["status"], "active")

    def test_weak_pass_review_resets_no_progress_when_auto_continue_allowed(self) -> None:
        state = dict(autoresearcher.DEFAULT_STATE)
        state["no_progress_rounds"] = 2
        decision = {"decision": "continue", "progress_score": 0}
        review = {
            "verdict": "weak_pass",
            "allows_auto_continue": True,
            "reasons": [],
            "evidence_checked": [],
            "required_fixes": [],
            "risk_flags": [],
        }
        autoresearcher.update_state_after_review(state, 3, decision, review, max_no_progress_rounds=3)
        self.assertEqual(state["no_progress_rounds"], 0)
        self.assertFalse(state["human_review_required"])
        self.assertEqual(state["status"], "active")

    def test_reviewer_fail_sets_human_review_required(self) -> None:
        state = dict(autoresearcher.DEFAULT_STATE)
        decision = {"decision": "continue", "progress_score": 6}
        review = {
            "verdict": "fail",
            "allows_auto_continue": False,
            "reasons": [],
            "evidence_checked": [],
            "required_fixes": [],
            "risk_flags": [],
        }
        autoresearcher.update_state_after_review(state, 1, decision, review, max_no_progress_rounds=3)
        self.assertTrue(state["human_review_required"])
        self.assertEqual(state["status"], "paused")

    def test_retryable_failure_gives_two_chances_before_pause(self) -> None:
        state = dict(autoresearcher.DEFAULT_STATE)
        self.assertFalse(autoresearcher.record_retryable_failure(state, "missing result", 3))
        self.assertEqual(state["failure_streak"], 1)
        self.assertFalse(state["human_review_required"])
        self.assertFalse(autoresearcher.record_retryable_failure(state, "missing result", 3))
        self.assertEqual(state["failure_streak"], 2)
        self.assertFalse(state["human_review_required"])
        self.assertTrue(autoresearcher.record_retryable_failure(state, "missing result", 3))
        self.assertEqual(state["failure_streak"], 3)
        self.assertTrue(state["human_review_required"])
        self.assertEqual(state["status"], "paused")

    def test_persistent_missing_result_pauses_after_retry_limit(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            repo = make_repo(Path(td))
            fake = make_fake_codex(Path(td))
            config = autoresearcher.load_config(repo)
            old = os.environ.get("FAKE_MISSING_RESULT")
            os.environ["FAKE_MISSING_RESULT"] = "1"
            try:
                with redirect_stdout(StringIO()), redirect_stderr(StringIO()):
                    rc = autoresearcher.Orchestrator(repo, config, codex_bin=str(fake)).run(
                        "project_001",
                        max_iters=1,
                        skip_model_check=True,
                    )
            finally:
                if old is None:
                    os.environ.pop("FAKE_MISSING_RESULT", None)
                else:
                    os.environ["FAKE_MISSING_RESULT"] = old
            self.assertEqual(rc, 1)
            state = json.loads((repo / "research" / "project_001" / "state.json").read_text())
            self.assertEqual(state["iteration"], 0)
            self.assertEqual(state["failure_streak"], 3)
            self.assertTrue(state["human_review_required"])
            self.assertEqual(state["status"], "paused")

    def test_persistent_reviewer_fail_pauses_after_retry_limit(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            repo = make_repo(Path(td))
            fake = make_fake_codex(Path(td))
            config = autoresearcher.load_config(repo)
            old = os.environ.get("FAKE_REVIEW_VERDICT")
            os.environ["FAKE_REVIEW_VERDICT"] = "fail"
            try:
                with redirect_stdout(StringIO()), redirect_stderr(StringIO()):
                    rc = autoresearcher.Orchestrator(repo, config, codex_bin=str(fake)).run(
                        "project_001",
                        max_iters=1,
                        skip_model_check=True,
                    )
            finally:
                if old is None:
                    os.environ.pop("FAKE_REVIEW_VERDICT", None)
                else:
                    os.environ["FAKE_REVIEW_VERDICT"] = old
            self.assertEqual(rc, 1)
            state = json.loads((repo / "research" / "project_001" / "state.json").read_text())
            self.assertEqual(state["iteration"], 0)
            self.assertEqual(state["failure_streak"], 3)
            self.assertTrue(state["human_review_required"])
            self.assertEqual(state["status"], "paused")

    def test_valid_unreviewed_result_is_reviewed_before_supervisor(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            repo = make_repo(Path(td))
            root = repo / "research" / "project_001"
            env_state = autoresearcher.default_env_state("project_001", "autoresearcher_project_001")
            env_state["status"] = "ready"
            write_json(root / "env_state.json", env_state)
            artifact_dir = root / "artifacts" / "0001"
            artifact_dir.mkdir(parents=True)
            metrics = artifact_dir / "metrics.json"
            metrics.write_text(json.dumps({"score": 1.0}))
            write_json(root / "results" / "0001_result.json", {
                "experiment_id": "0001",
                "status": "completed",
                "claim_tested": "Existing result should be reviewed before a new supervisor turn.",
                "commands_run": ["python existing.py"],
                "metrics": {"score": 1.0},
                "baseline_metrics": {},
                "artifacts": ["research/project_001/artifacts/0001/metrics.json"],
                "interpretation": "Existing result is ready for review.",
                "known_failures": [],
                "next_questions": [],
            })
            (root / "results" / "0001_summary.md").write_text("# Summary\n")
            fake = make_fake_codex(Path(td))
            config = autoresearcher.load_config(repo)
            with redirect_stdout(StringIO()), redirect_stderr(StringIO()):
                rc = autoresearcher.Orchestrator(repo, config, codex_bin=str(fake)).run(
                    "project_001",
                    max_iters=1,
                    skip_model_check=True,
                )
            self.assertEqual(rc, 0)
            self.assertFalse((root / "decisions" / "0001_decision.json").exists())
            self.assertTrue((root / "reviews" / "0001_review.json").exists())
            state = json.loads((root / "state.json").read_text())
            self.assertEqual(state["iteration"], 1)
            self.assertEqual(state["failure_streak"], 0)

    def test_local_pivot_triggers_pro_checkpoint(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            repo = make_repo(Path(td))
            fake = make_fake_codex(Path(td))
            config = autoresearcher.load_config(repo)
            config["loop"]["require_human_for_pivot"] = False
            old = os.environ.get("FAKE_DECISION")
            os.environ["FAKE_DECISION"] = "pivot"
            try:
                with redirect_stdout(StringIO()), redirect_stderr(StringIO()):
                    rc = autoresearcher.Orchestrator(repo, config, codex_bin=str(fake)).run(
                        "project_001",
                        max_iters=1,
                        skip_model_check=True,
                    )
            finally:
                if old is None:
                    os.environ.pop("FAKE_DECISION", None)
                else:
                    os.environ["FAKE_DECISION"] = old
            self.assertEqual(rc, 0)
            state = json.loads((repo / "research" / "project_001" / "state.json").read_text())
            self.assertEqual(state["iteration"], 0)
            self.assertTrue(state["human_review_required"])
            self.assertEqual(state["status"], "paused")
            self.assertEqual(state["pending_checkpoint"]["reason"], "local_pivot")
            self.assertTrue((repo / "research" / "project_001" / "pro_packets" / "0001_PRO_REVIEW_PACKET.md").exists())

    def test_git_commit_skips_when_not_a_repo(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            repo = make_repo(Path(td))
            config = autoresearcher.load_config(repo)
            manager = autoresearcher.GitManager(repo, config)
            self.assertFalse(manager.commit([repo / "autoresearcher.yaml"], "test"))

    def test_git_commit_skips_ignored_paths(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            repo = make_repo(Path(td))
            subprocess.run(["git", "init"], cwd=repo, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=repo, check=True)
            subprocess.run(["git", "config", "user.name", "Test User"], cwd=repo, check=True)
            (repo / ".gitignore").write_text("*.log\n")
            ignored = repo / "ignored.log"
            tracked = repo / "tracked.txt"
            ignored.write_text("ignore me\n")
            tracked.write_text("track me\n")
            manager = autoresearcher.GitManager(
                repo,
                {"git": {"enabled": True, "commit": True, "push": False}},
            )
            self.assertTrue(manager.commit([ignored, tracked], "test ignored paths"))
            files = subprocess.run(
                ["git", "ls-files"],
                cwd=repo,
                check=True,
                text=True,
                stdout=subprocess.PIPE,
            ).stdout.splitlines()
            self.assertIn("tracked.txt", files)
            self.assertNotIn("ignored.log", files)

    def test_context_window_failure_resets_role_session(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            repo = make_repo(Path(td))
            config = autoresearcher.load_config(repo)
            local = autoresearcher.load_local_state(repo, "project_001")
            local["projects"]["project_001"]["codex_sessions"]["reviewer"] = {
                "session_id": "old-reviewer-session",
                "last_used_at": "2026-01-01T00:00:00+00:00",
            }
            autoresearcher.save_local_state(repo, local)
            orchestrator = autoresearcher.Orchestrator(repo, config, codex_bin="fake")
            result = autoresearcher.CodexRunResult(
                role="reviewer",
                session_id="old-reviewer-session",
                output_path=repo / "review.json",
                jsonl_log_path=repo / "review_events.jsonl",
                stderr_log_path=repo / "review_stderr.log",
                return_code=1,
                timed_out=False,
                stdout_tail="Codex ran out of room in the model's context window.",
                stderr_tail="",
            )
            orchestrator._reset_role_session_on_context_overflow("project_001", result)
            local = autoresearcher.load_local_state(repo, "project_001")
            self.assertIsNone(local["projects"]["project_001"]["codex_sessions"]["reviewer"]["session_id"])

    def test_summary_due_uses_cadence_and_stop(self) -> None:
        config = {"summary": {"enabled": True, "cadence_iterations": 3, "on_stop": True}}
        self.assertFalse(autoresearcher.summary_due({"iteration": 2, "last_summary_iteration": 0}, config, "progress"))
        self.assertTrue(autoresearcher.summary_due({"iteration": 3, "last_summary_iteration": 0}, config, "progress"))
        self.assertTrue(autoresearcher.summary_due({"iteration": 4, "last_summary_iteration": 3}, config, "final"))
        self.assertFalse(autoresearcher.summary_due({"iteration": 4, "last_summary_iteration": 4}, config, "final"))

    def test_manual_summary_writes_progress_files(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            repo = make_repo(Path(td))
            root = repo / "research" / "project_001"
            state = dict(autoresearcher.DEFAULT_STATE)
            state["iteration"] = 1
            write_json(root / "state.json", state)
            fake = make_fake_codex(Path(td))
            config = autoresearcher.load_config(repo)
            with redirect_stdout(StringIO()), redirect_stderr(StringIO()):
                rc = autoresearcher.run_manual_summary(
                    repo,
                    "project_001",
                    config,
                    codex_bin=str(fake),
                    skip_model_check=True,
                )
            self.assertEqual(rc, 0)
            summary_path = root / "progress" / "0001_manual_summary.md"
            latest_path = root / "progress" / "latest_summary.md"
            self.assertTrue(summary_path.exists())
            self.assertTrue(latest_path.exists())
            self.assertIn("Fake project progress summary", latest_path.read_text())
            state = json.loads((root / "state.json").read_text())
            self.assertEqual(state["last_summary_iteration"], 1)
            self.assertEqual(state["last_summary_path"], "research/project_001/progress/0001_manual_summary.md")

    def test_checkpoint_policy_terminal_and_cadence(self) -> None:
        state = dict(autoresearcher.DEFAULT_STATE)
        self.assertEqual(pro_checkpoint_due(state, {}, local_decision={"decision": "stop"}), (True, "local_stop"))
        self.assertEqual(pro_checkpoint_due(state, {}, local_decision={"decision": "pivot"}), (True, "local_pivot"))
        self.assertEqual(pro_checkpoint_due(state, {}, latest_review={"verdict": "fail"}), (True, "review_fail"))
        state["iteration"] = 3
        config = {"chatgpt_pro": {"enabled": True, "cadence_iterations": 3, "allow_cadence_2_or_3": True}}
        self.assertEqual(pro_checkpoint_due(state, config), (True, "cadence"))

    def test_metric_ledger_extracts_scalar_metrics(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            repo = make_repo(Path(td))
            root = repo / "research" / "project_001"
            write_json(root / "results" / "0001_result.json", {
                "experiment_id": "0001",
                "status": "completed",
                "claim_tested": "Risk regret audit.",
                "commands_run": [],
                "metrics": {
                    "safe_optimal_lucky_only": {
                        "policy_regret": 0.504,
                        "q_overestimation": 0.675,
                    },
                    "best_positive_method": "generic",
                },
                "baseline_metrics": {"baseline_mse": 0.4},
                "artifacts": [],
                "interpretation": "Generic method helped Q calibration but not regret.",
                "known_failures": ["policy regret unchanged"],
                "next_questions": [],
            })
            write_json(root / "reviews" / "0001_review.json", {
                "experiment_id": "0001",
                "verdict": "weak_pass",
                "allows_auto_continue": True,
                "reasons": [],
                "evidence_checked": [],
                "required_fixes": [],
                "risk_flags": ["Do not overclaim."],
            })
            ledger = build_metric_ledger(repo, "project_001")
            row = ledger["iterations"][0]
            self.assertIn("metrics.safe_optimal_lucky_only.policy_regret", row["important_metrics"])
            self.assertIn("baseline_metrics.baseline_mse", row["important_metrics"])
            json_path, md_path = write_metric_ledger(repo, "project_001")
            self.assertTrue(json_path.exists())
            self.assertTrue(md_path.exists())

    def test_build_pro_packet_is_brief_github_summary_handoff(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            repo = make_repo(Path(td))
            (repo / "autoresearcher.yaml").write_text(
                autoresearcher.DEFAULT_CONFIG_TEXT
                + "\ngithub:\n  repo_url: https://github.com/example/autoresearcher\n  branch: main\n"
            )
            root = repo / "research" / "project_001"
            (root / "toy_prototype_plan.md").write_text("# Prototype Plan\n\nImportant source plan.\n")
            (root / "toy_next_steps_review_plan.md").write_text("# Next Steps\n\nImportant next-step plan.\n")
            (root / "progress" / "latest_summary.md").write_text("# Latest Summary\n\nStopped for research reasons.\n")
            state = dict(autoresearcher.DEFAULT_STATE)
            state["iteration"] = 1
            state["status"] = "stopped"
            write_json(root / "state.json", state)
            write_json(root / "decisions" / "0002_decision.json", {
                "decision": "stop",
                "confidence": 0.7,
                "progress_score": 6,
                "rationale": "Local Codex recommends stop.",
                "evidence": ["negative evidence"],
                "risks": [],
                "next_experiment": None,
            })
            (root / "decisions" / "0003_pro_decision.md").write_text("# Pro Decision\n\nShould not be the local decision link.\n")
            path = autoresearcher.build_pro_packet(repo, "project_001", reason="local_stop")
            text = path.read_text()
            self.assertEqual(path.name, "0002_PRO_REVIEW_PACKET.md")
            self.assertIn("`local_stop`", text)
            self.assertIn("# Check-In: project_001", text)
            self.assertIn("existing advisor thread", text)
            self.assertIn("https://github.com/example/autoresearcher", text)
            self.assertIn(
                "https://github.com/example/autoresearcher/blob/main/research/project_001/progress/latest_summary.md",
                text,
            )
            self.assertIn(
                "https://github.com/example/autoresearcher/blob/main/research/project_001/decisions/0002_decision.json",
                text,
            )
            self.assertNotIn("0003_pro_decision.md", text)
            self.assertIn("## Broader Project Context", text)
            self.assertIn(
                "https://github.com/example/autoresearcher/blob/main/research/project_001/toy_prototype_plan.md",
                text,
            )
            self.assertIn(
                "https://github.com/example/autoresearcher/blob/main/research/project_001/toy_next_steps_review_plan.md",
                text,
            )
            self.assertIn("Choose exactly one: `continue`, `pivot`, or `stop`.", text)
            self.assertNotIn("needs_human", text)
            self.assertNotIn("Important source plan", text)
            self.assertNotIn("Important next-step plan", text)
            self.assertNotIn("Stopped for research reasons", text)
            self.assertNotIn("Local Codex recommends stop", text)
            self.assertNotIn("Metric ledger", text)

    def test_ingest_apply_pro_continue_and_resume(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            repo = make_repo(Path(td))
            root = repo / "research" / "project_001"
            state = dict(autoresearcher.DEFAULT_STATE)
            state["iteration"] = 1
            state["status"] = "paused"
            state["human_review_required"] = True
            write_json(root / "state.json", state)
            response = Path(td) / "pro_response.md"
            fake_pro_response(response, decision="continue")
            decision_path, _ = autoresearcher.ingest_pro_response(repo, "project_001", response)
            self.assertTrue(decision_path.exists())
            self.assertTrue((root / "plans" / "0002_plan.md").exists())
            autoresearcher.apply_pro_decision(repo, "project_001")
            state = json.loads((root / "state.json").read_text())
            self.assertEqual(state["status"], "active")
            self.assertFalse(state["human_review_required"])
            self.assertEqual(state["last_pro_review_iteration"], 1)
            self.assertEqual(state["pro_review_count"], 1)

            state["status"] = "paused"
            state["human_review_required"] = True
            write_json(root / "state.json", state)
            autoresearcher.resume_project(repo, "project_001", "manual test resume")
            state = json.loads((root / "state.json").read_text())
            self.assertEqual(state["status"], "active")
            self.assertFalse(state["human_review_required"])

    def test_pro_decision_schema_rejects_bad_next_experiment(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            repo = make_repo(Path(td))
            bad = Path(td) / "bad_pro.json"
            write_json(bad, {
                "decision": "continue",
                "confidence": 0.5,
                "rationale": "bad",
                "evidence": [],
                "risks": [],
                "next_experiment": {"objective": "missing fields"},
            })
            with self.assertRaises(Exception):
                validate_json_schema(bad, repo / "schemas" / "pro_decision.schema.json")

    def test_worktree_guard_detects_protected_file_drift(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            repo = make_repo(Path(td))
            subprocess.run(["git", "init"], cwd=repo, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=repo, check=True)
            subprocess.run(["git", "config", "user.name", "Test User"], cwd=repo, check=True)
            (repo / "scripts").mkdir(exist_ok=True)
            (repo / "scripts" / "autoresearcher.py").write_text("clean\n")
            subprocess.run(["git", "add", "."], cwd=repo, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            subprocess.run(["git", "commit", "-m", "baseline"], cwd=repo, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            (repo / "scripts" / "autoresearcher.py").write_text("dirty\n")
            result = protected_file_drift(repo, "project_001")
            self.assertTrue(result.drift_detected)
            self.assertIn("scripts/autoresearcher.py", result.protected_paths)
            json_path, md_path = write_guard_report(repo, "project_001", "0001", result)
            self.assertTrue(json_path.exists())
            self.assertTrue(md_path.exists())

    def test_pro_cadence_defaults_to_three(self) -> None:
        config = {"chatgpt_pro": {"enabled": True, "cadence_iterations": 3}}
        self.assertFalse(autoresearcher.pro_review_due({"iteration": 2, "last_pro_review_iteration": 0}, config))
        self.assertTrue(autoresearcher.pro_review_due({"iteration": 3, "last_pro_review_iteration": 0}, config))

    def test_pro_cadence_can_be_two(self) -> None:
        config = {"chatgpt_pro": {"enabled": True, "cadence_iterations": 2}}
        self.assertTrue(autoresearcher.pro_review_due({"iteration": 2, "last_pro_review_iteration": 0}, config))

    def test_pro_bridge_blocker_pauses_when_enabled(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            repo = make_repo(Path(td))
            config = autoresearcher.load_config(repo)
            config["chatgpt_pro"]["enabled"] = True
            with redirect_stdout(StringIO()):
                rc = autoresearcher.pro_smoke(repo, "project_001", config)
            self.assertEqual(rc, 2)
            state = json.loads((repo / "research" / "project_001" / "state.json").read_text())
            self.assertTrue(state["human_review_required"])

    def test_phase1_loop_runs_with_chatgpt_disabled_and_fake_codex(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            repo = make_repo(Path(td))
            fake = make_fake_codex(Path(td))
            config = autoresearcher.load_config(repo)
            self.assertFalse(config["chatgpt_pro"]["enabled"])
            with redirect_stdout(StringIO()), redirect_stderr(StringIO()):
                rc = autoresearcher.Orchestrator(repo, config, codex_bin=str(fake)).run(
                    "project_001",
                    max_iters=1,
                    skip_model_check=True,
                )
            self.assertEqual(rc, 0)
            state = json.loads((repo / "research" / "project_001" / "state.json").read_text())
            env_state = json.loads((repo / "research" / "project_001" / "env_state.json").read_text())
            self.assertEqual(state["iteration"], 1)
            self.assertEqual(env_state["status"], "ready")
            self.assertFalse(state["human_review_required"])

    def test_run_executes_existing_plan_without_overwriting_prior_decision(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            repo = make_repo(Path(td))
            fake = make_fake_codex(Path(td))
            root = repo / "research" / "project_001"
            env_state = autoresearcher.default_env_state("project_001", "autoresearcher_project_001")
            env_state["status"] = "ready"
            write_json(root / "env_state.json", env_state)
            state = dict(autoresearcher.DEFAULT_STATE)
            state["iteration"] = 1
            state["status"] = "active"
            state["last_decision"] = "pivot"
            write_json(root / "state.json", state)
            old_decision = {
                "decision": "stop",
                "confidence": 0.7,
                "progress_score": 2,
                "rationale": "Prior terminal local decision.",
                "evidence": ["old"],
                "risks": [],
                "checkpoint_recommended": False,
                "checkpoint_reason": None,
                "terminal_decision_requires_pro": True,
                "next_experiment": None,
            }
            write_json(root / "decisions" / "0002_decision.json", old_decision)
            experiment = autoresearcher.normalize_experiment_paths(
                "project_001",
                "0002",
                {
                    "experiment_id": "0002",
                    "objective": "Execute existing approved plan.",
                    "hypothesis": "The plan can be executed without a new supervisor decision.",
                    "success_criteria": ["corrected_accuracy > baseline_accuracy"],
                    "failure_criteria": ["missing result JSON"],
                    "tasks_for_codex": ["Write fake result files."],
                    "required_outputs": [],
                    "estimated_runtime_minutes": 1,
                },
            )
            autoresearcher.write_plan(repo, "project_001", "0002", experiment)

            config = autoresearcher.load_config(repo)
            with redirect_stdout(StringIO()), redirect_stderr(StringIO()):
                rc = autoresearcher.Orchestrator(repo, config, codex_bin=str(fake)).run(
                    "project_001",
                    max_iters=1,
                    skip_model_check=True,
                )

            self.assertEqual(rc, 0)
            self.assertFalse((root / "packets" / "0002_supervisor_packet.md").exists())
            self.assertEqual(json.loads((root / "decisions" / "0002_decision.json").read_text()), old_decision)
            self.assertTrue((root / "results" / "0002_result.json").exists())
            state = json.loads((root / "state.json").read_text())
            self.assertEqual(state["iteration"], 2)


if __name__ == "__main__":
    unittest.main()
