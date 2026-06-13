from __future__ import annotations

import json
import os
import shutil
import stat
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
from build_context import build_context  # noqa: E402
from kill_process_tree import run_with_timeout  # noqa: E402
from validate_artifacts import validate_json_schema  # noqa: E402


def write_json(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n")


def make_repo(tmp: Path, project: str = "project_001") -> Path:
    shutil.copytree(REPO_ROOT / "prompts", tmp / "prompts")
    shutil.copytree(REPO_ROOT / "schemas", tmp / "schemas")
    (tmp / "autoresearcher.yaml").write_text(autoresearcher.DEFAULT_CONFIG_TEXT)
    root = tmp / "research" / project
    for subdir in ("plans", "results", "reviews", "decisions", "packets", "artifacts", "setup_logs"):
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
                output_path.write_text(json.dumps({
                    "decision": "continue",
                    "confidence": 0.8,
                    "progress_score": 6,
                    "rationale": "Run the tiny positive-control experiment.",
                    "evidence": ["Project charter asks for a toy positive control."],
                    "risks": ["Toy result may not generalize."],
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
                    "risk_flags": []
                }))
            else:
                output_path.write_text("ok\\n")
            """
        )
    )
    script.chmod(script.stat().st_mode | stat.S_IXUSR)
    return script


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
            self.assertIn('"iteration": 0', context)
            self.assertIn('"claim_tested": "claim"', context)
            self.assertIn('"verdict": "pass"', context)

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

    def test_missing_result_sets_human_review_required(self) -> None:
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
            self.assertTrue(state["human_review_required"])

    def test_git_commit_skips_when_not_a_repo(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            repo = make_repo(Path(td))
            config = autoresearcher.load_config(repo)
            manager = autoresearcher.GitManager(repo, config)
            self.assertFalse(manager.commit([repo / "autoresearcher.yaml"], "test"))

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


if __name__ == "__main__":
    unittest.main()
