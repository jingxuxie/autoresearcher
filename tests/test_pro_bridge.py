import json
import os
import shutil
import sys
import tempfile
import unittest
from contextlib import contextmanager, redirect_stderr, redirect_stdout
from io import StringIO
from pathlib import Path
from unittest.mock import patch


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = REPO_ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import autoresearcher  # noqa: E402
from chatgpt_cdp_bridge import CdpResponse  # noqa: E402


def write_json(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n")


def make_repo(tmp: Path, project: str = "project_001") -> Path:
    shutil.copytree(REPO_ROOT / "prompts", tmp / "prompts")
    shutil.copytree(REPO_ROOT / "schemas", tmp / "schemas")
    (tmp / "autoresearcher.yaml").write_text(autoresearcher.DEFAULT_CONFIG_TEXT)
    root = tmp / "research" / project
    for subdir in (
        "plans",
        "results",
        "reviews",
        "decisions",
        "packets",
        "pro_packets",
        "artifacts",
        "setup_logs",
        "progress",
    ):
        (root / subdir).mkdir(parents=True, exist_ok=True)
    (root / "charter.md").write_text("# Charter\n\nTest charter.\n")
    write_json(root / "state.json", autoresearcher.DEFAULT_STATE)
    env_name = autoresearcher.conda_env_name_for_project(project)
    (root / "environment.yaml").write_text(autoresearcher.default_environment_yaml(env_name))
    env_state = autoresearcher.default_env_state(project, env_name)
    env_state["status"] = "ready"
    write_json(root / "env_state.json", env_state)
    return tmp


def fake_pre_pro_summary(orchestrator: autoresearcher.Orchestrator, project: str, state: dict, reason: str, force: bool = False) -> Path:
    iteration_id = f"{int(state.get('iteration', 0)):04d}"
    output_path, latest_path = autoresearcher.progress_summary_paths(orchestrator.repo_root, project, iteration_id, reason)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("# Progress Summary\n\nFake pre-Pro progress summary.\n")
    latest_path.write_text(output_path.read_text())
    state["last_summary_iteration"] = int(state.get("iteration", 0))
    state["last_summary_path"] = str(output_path.relative_to(orchestrator.repo_root))
    autoresearcher.save_project_state(orchestrator.repo_root, project, state)
    return output_path


@contextmanager
def fake_pro(mode: str):
    old = os.environ.get("FAKE_CHATGPT_PRO")
    os.environ["FAKE_CHATGPT_PRO"] = mode
    try:
        yield
    finally:
        if old is None:
            os.environ.pop("FAKE_CHATGPT_PRO", None)
        else:
            os.environ["FAKE_CHATGPT_PRO"] = old


class ProBridgeTests(unittest.TestCase):
    def test_fake_continue_pro_review_writes_decision_plan_and_pending_checkpoint(self) -> None:
        with tempfile.TemporaryDirectory() as td, fake_pro("continue"):
            repo = make_repo(Path(td))
            root = repo / "research" / "project_001"
            state = dict(autoresearcher.DEFAULT_STATE)
            state["iteration"] = 1
            state["status"] = "stopped"
            state["last_decision"] = "stop"
            write_json(root / "state.json", state)

            result = autoresearcher.run_pro_review(
                repo,
                "project_001",
                autoresearcher.load_config(repo),
                reason="local_stop",
            )

            self.assertEqual(result.status, "completed")
            self.assertTrue((root / "decisions" / "0002_pro_decision.json").exists())
            self.assertTrue((root / "decisions" / "0002_pro_raw_response.md").exists())
            self.assertTrue((root / "plans" / "0002_plan.md").exists())
            state = json.loads((root / "state.json").read_text())
            self.assertEqual(state["pending_checkpoint"]["status"], "pro_decision_ingested")
            self.assertEqual(state["status"], "stopped")

    def test_fake_stop_apply_keeps_state_stopped(self) -> None:
        with tempfile.TemporaryDirectory() as td, fake_pro("stop"):
            repo = make_repo(Path(td))
            root = repo / "research" / "project_001"
            state = dict(autoresearcher.DEFAULT_STATE)
            state["iteration"] = 1
            state["status"] = "stopped"
            state["last_decision"] = "stop"
            write_json(root / "state.json", state)

            autoresearcher.run_pro_review(repo, "project_001", autoresearcher.load_config(repo), reason="local_stop")
            autoresearcher.apply_pro_decision(repo, "project_001")

            state = json.loads((root / "state.json").read_text())
            self.assertEqual(state["status"], "stopped")
            self.assertFalse(state["human_review_required"])
            self.assertEqual(state["pro_review_count"], 1)
            self.assertFalse((root / "plans" / "0002_plan.md").exists())

    def test_fake_blocker_pauses_with_structured_blocker(self) -> None:
        with tempfile.TemporaryDirectory() as td, fake_pro("blocker:login_required"):
            repo = make_repo(Path(td))
            result = autoresearcher.run_pro_review(
                repo,
                "project_001",
                autoresearcher.load_config(repo),
                reason="local_stop",
            )

            root = repo / "research" / "project_001"
            self.assertEqual(result.status, "blocked")
            blocker = json.loads((root / "decisions" / "0001_pro_blocker.json").read_text())
            self.assertEqual(blocker["reason"], "login_required")
            state = json.loads((root / "state.json").read_text())
            self.assertEqual(state["status"], "paused")
            self.assertTrue(state["human_review_required"])

    def test_fake_malformed_response_writes_parse_blocker(self) -> None:
        with tempfile.TemporaryDirectory() as td, fake_pro("malformed"):
            repo = make_repo(Path(td))
            result = autoresearcher.run_pro_review(
                repo,
                "project_001",
                autoresearcher.load_config(repo),
                reason="local_stop",
            )

            root = repo / "research" / "project_001"
            self.assertEqual(result.status, "blocked")
            self.assertEqual(result.reason, "response_parse_failed")
            self.assertTrue((root / "decisions" / "0001_pro_raw_response.md").exists())
            blocker = json.loads((root / "decisions" / "0001_pro_blocker.json").read_text())
            self.assertEqual(blocker["reason"], "response_parse_failed")

    def test_run_stopped_project_fake_continue_resumes_without_executor(self) -> None:
        with tempfile.TemporaryDirectory() as td, fake_pro("continue"):
            repo = make_repo(Path(td))
            root = repo / "research" / "project_001"
            state = dict(autoresearcher.DEFAULT_STATE)
            state["iteration"] = 1
            state["status"] = "stopped"
            state["last_decision"] = "stop"
            write_json(root / "state.json", state)

            with patch.object(autoresearcher.Orchestrator, "_run_summary_agent", fake_pre_pro_summary):
                with redirect_stdout(StringIO()), redirect_stderr(StringIO()):
                    rc = autoresearcher.Orchestrator(repo, autoresearcher.load_config(repo)).run(
                        "project_001",
                        max_iters=1,
                        skip_model_check=True,
                    )

            self.assertEqual(rc, 0)
            self.assertTrue((root / "progress" / "latest_summary.md").exists())
            state = json.loads((root / "state.json").read_text())
            self.assertEqual(state["status"], "active")
            self.assertEqual(state["iteration"], 1)
            self.assertTrue((root / "plans" / "0002_plan.md").exists())
            self.assertFalse((root / "results" / "0002_result.json").exists())

    def test_run_stopped_project_blocks_pro_when_pre_summary_fails(self) -> None:
        with tempfile.TemporaryDirectory() as td, fake_pro("continue"):
            repo = make_repo(Path(td))
            root = repo / "research" / "project_001"
            state = dict(autoresearcher.DEFAULT_STATE)
            state["iteration"] = 1
            state["status"] = "stopped"
            state["last_decision"] = "stop"
            write_json(root / "state.json", state)

            with patch.object(autoresearcher.Orchestrator, "_run_summary_agent", return_value=None):
                with redirect_stdout(StringIO()), redirect_stderr(StringIO()):
                    rc = autoresearcher.Orchestrator(repo, autoresearcher.load_config(repo)).run(
                        "project_001",
                        max_iters=1,
                        skip_model_check=True,
                    )

            self.assertEqual(rc, 0)
            state = json.loads((root / "state.json").read_text())
            self.assertEqual(state["status"], "paused")
            self.assertTrue(state["human_review_required"])
            blocker = json.loads((root / "decisions" / "0002_pro_blocker.json").read_text())
            self.assertEqual(blocker["reason"], "summary_failed")
            self.assertFalse((root / "decisions" / "0002_pro_decision.json").exists())

    def test_run_stopped_project_fake_stop_stays_stopped(self) -> None:
        with tempfile.TemporaryDirectory() as td, fake_pro("stop"):
            repo = make_repo(Path(td))
            root = repo / "research" / "project_001"
            state = dict(autoresearcher.DEFAULT_STATE)
            state["iteration"] = 1
            state["status"] = "stopped"
            state["last_decision"] = "stop"
            write_json(root / "state.json", state)

            with patch.object(autoresearcher.Orchestrator, "_run_summary_agent", fake_pre_pro_summary):
                with redirect_stdout(StringIO()), redirect_stderr(StringIO()):
                    rc = autoresearcher.Orchestrator(repo, autoresearcher.load_config(repo)).run(
                        "project_001",
                        max_iters=1,
                        skip_model_check=True,
                    )

            self.assertEqual(rc, 0)
            self.assertTrue((root / "progress" / "latest_summary.md").exists())
            state = json.loads((root / "state.json").read_text())
            self.assertEqual(state["status"], "stopped")
            self.assertEqual(state["pro_review_count"], 1)
            self.assertFalse((root / "plans" / "0002_plan.md").exists())

    def test_cdp_backend_completed_response_writes_decision(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            repo = make_repo(Path(td))
            config = autoresearcher.load_config(repo)
            config["chatgpt_pro"]["thread_url"] = "https://chatgpt.com/c/test-thread"
            raw = "# Decision\n\n```json\n" + json.dumps(
                {
                    "decision": "stop",
                    "confidence": 0.82,
                    "rationale": "The compact prototype has enough evidence for this test.",
                    "evidence": ["CDP backend returned a valid decision."],
                    "risks": ["This is a mocked browser response."],
                    "next_experiment": None,
                },
                indent=2,
            ) + "\n```\n"

            with patch("chatgpt_cdp_bridge.run_cdp_review", return_value=CdpResponse(status="completed", raw_text=raw)) as mocked:
                result = autoresearcher.run_pro_review(
                    repo,
                    "project_001",
                    config,
                    reason="local_stop",
                    backend_override="cdp",
                )

            self.assertEqual(result.status, "completed")
            self.assertTrue((repo / "research" / "project_001" / "decisions" / "0001_pro_decision.json").exists())
            self.assertEqual(mocked.call_args.args[0], "http://127.0.0.1:9222")

    def test_cdp_backend_blocker_pauses_with_reason(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            repo = make_repo(Path(td))
            config = autoresearcher.load_config(repo)
            config["chatgpt_pro"]["thread_url"] = "https://chatgpt.com/c/test-thread"

            with patch(
                "chatgpt_cdp_bridge.run_cdp_review",
                return_value=CdpResponse(
                    status="blocked",
                    reason="login_required",
                    message="The visible ChatGPT tab is not logged in.",
                    details={"href": "https://chatgpt.com/"},
                ),
            ):
                result = autoresearcher.run_pro_review(
                    repo,
                    "project_001",
                    config,
                    reason="local_stop",
                    backend_override="cdp",
                )

            root = repo / "research" / "project_001"
            self.assertEqual(result.status, "blocked")
            blocker = json.loads((root / "decisions" / "0001_pro_blocker.json").read_text())
            self.assertEqual(blocker["reason"], "login_required")
            state = json.loads((root / "state.json").read_text())
            self.assertEqual(state["status"], "paused")


if __name__ == "__main__":
    unittest.main()
