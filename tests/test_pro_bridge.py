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
from chatgpt_cdp_bridge import CdpClient, CdpError, CdpResponse, build_visible_prompt, connect_page, select_chatgpt_page, wait_for_response  # noqa: E402
from chatgpt_pro_bridge import effective_thread_url, extract_fenced_json  # noqa: E402


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
    def test_project_local_thread_url_overrides_global_config(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            repo = make_repo(Path(td), project="reward_to_gcrl")
            write_json(
                repo / ".autoresearcher" / "local_state.json",
                {
                    "projects": {
                        "reward_to_gcrl": {
                            "chatgpt_pro": {
                                "thread_url": "https://chatgpt.com/c/project-local",
                            }
                        }
                    }
                },
            )

            url = effective_thread_url(
                repo,
                "reward_to_gcrl",
                {"thread_url": "https://chatgpt.com/c/global-default"},
            )

            self.assertEqual(url, "https://chatgpt.com/c/project-local")

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
            state["weak_pass_streak"] = 2
            write_json(root / "state.json", state)

            autoresearcher.run_pro_review(repo, "project_001", autoresearcher.load_config(repo), reason="local_stop")
            autoresearcher.apply_pro_decision(repo, "project_001")

            state = json.loads((root / "state.json").read_text())
            self.assertEqual(state["status"], "stopped")
            self.assertFalse(state["human_review_required"])
            self.assertEqual(state["pro_review_count"], 1)
            self.assertEqual(state["weak_pass_streak"], 0)
            self.assertFalse((root / "plans" / "0002_plan.md").exists())

            autoresearcher.apply_pro_decision(repo, "project_001")
            state = json.loads((root / "state.json").read_text())
            self.assertEqual(state["pro_review_count"], 1)

    def test_followup_pro_review_does_not_overwrite_prior_stop_decision(self) -> None:
        with tempfile.TemporaryDirectory() as td, fake_pro("continue"):
            repo = make_repo(Path(td))
            root = repo / "research" / "project_001"
            state = dict(autoresearcher.DEFAULT_STATE)
            state["iteration"] = 1
            state["status"] = "stopped"
            state["last_decision"] = "stop"
            state["last_pro_review_path"] = "research/project_001/decisions/0002_pro_decision.json"
            write_json(root / "state.json", state)
            old_stop = {
                "decision": "stop",
                "confidence": 0.8,
                "rationale": "Prior stop decision.",
                "evidence": ["Prior evidence."],
                "risks": [],
                "next_experiment": None,
            }
            write_json(root / "decisions" / "0002_pro_decision.json", old_stop)

            result = autoresearcher.run_pro_review(
                repo,
                "project_001",
                autoresearcher.load_config(repo),
                reason="human_requested_pivot",
            )

            self.assertEqual(result.status, "completed")
            self.assertTrue((root / "decisions" / "0002_review2_pro_decision.json").exists())
            self.assertEqual(json.loads((root / "decisions" / "0002_pro_decision.json").read_text())["decision"], "stop")
            followup = json.loads((root / "decisions" / "0002_review2_pro_decision.json").read_text())
            self.assertEqual(followup["next_experiment"]["experiment_id"], "0002")
            self.assertTrue((root / "plans" / "0002_plan.md").exists())
            state = json.loads((root / "state.json").read_text())
            self.assertEqual(
                state["pending_checkpoint"]["pro_decision_path"],
                "research/project_001/decisions/0002_review2_pro_decision.json",
            )

            autoresearcher.apply_pro_decision(repo, "project_001")
            state = json.loads((root / "state.json").read_text())
            self.assertEqual(state["status"], "active")
            self.assertEqual(state["last_pro_review_path"], "research/project_001/decisions/0002_review2_pro_decision.json")

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

    def test_extract_pro_json_accepts_chatgpt_json_label_and_trailing_text(self) -> None:
        raw = """JSON
{
  "decision": "continue",
  "confidence": 0.78,
  "rationale": "Continue with one strict small experiment.",
  "evidence": ["The latest summary supports one more tabular check."],
  "risks": ["The result may still be equivalent to a baseline."],
  "next_experiment": null
}

Short supporting paragraph.
"""

        parsed = extract_fenced_json(raw)

        self.assertEqual(parsed["decision"], "continue")
        self.assertIsNone(parsed["next_experiment"])
        self.assertEqual(autoresearcher.extract_fenced_json(raw)["decision"], "continue")

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

    def test_cdp_client_wraps_websocket_disconnects(self) -> None:
        class ClosedWebSocket:
            def send(self, _payload: str) -> None:
                return None

            def recv(self) -> str:
                raise RuntimeError("Connection is already closed.")

            def close(self) -> None:
                return None

        client = object.__new__(CdpClient)
        client._ws = ClosedWebSocket()
        client._next_id = 0

        with self.assertRaises(CdpError) as ctx:
            client.call("Runtime.enable")

        self.assertEqual(ctx.exception.reason, "browser_bridge_unavailable")
        self.assertEqual(ctx.exception.details["method"], "Runtime.enable")

    def test_cdp_connect_skips_stale_matching_target(self) -> None:
        pages = [
            {
                "type": "page",
                "title": "Stale",
                "url": "https://chatgpt.com/c/abc123",
                "webSocketDebuggerUrl": "ws://stale",
            },
            {
                "type": "page",
                "title": "Fresh",
                "url": "https://chatgpt.com/g/project/c/abc123",
                "webSocketDebuggerUrl": "ws://fresh",
            },
        ]

        class FakeClient:
            instances = []

            def __init__(self, websocket_url: str):
                self.websocket_url = websocket_url
                self.closed = False
                FakeClient.instances.append(self)

            def call(self, method: str, _params=None) -> dict:
                if self.websocket_url == "ws://stale" and method == "Runtime.evaluate":
                    raise CdpError("browser_bridge_unavailable", "closed", {"method": method})
                return {}

            def close(self) -> None:
                self.closed = True

        with patch("chatgpt_cdp_bridge._list_pages", return_value=pages):
            with patch("chatgpt_cdp_bridge.CdpClient", FakeClient):
                client = connect_page("http://127.0.0.1:9222", "https://chatgpt.com/c/abc123", allow_new_tab=False)

        self.assertEqual(client.websocket_url, "ws://fresh")
        self.assertTrue(FakeClient.instances[0].closed)

    def test_cdp_visible_prompt_uses_existing_thread_framing(self) -> None:
        prompt = build_visible_prompt("Advisor instructions.", "Pointer packet.", "local_stop")

        self.assertIn("Continuing this existing research-advisor thread", prompt)
        self.assertIn("thread memory", prompt)
        self.assertIn("## Standing Advisor Instructions", prompt)
        self.assertIn("## Current Pointer Packet", prompt)
        self.assertIn("Checkpoint reason: local_stop", prompt)

    def test_cdp_wait_for_response_ignores_short_partial_text(self) -> None:
        class FakeClient:
            def __init__(self) -> None:
                self.calls = 0

            def evaluate(self, _script: str) -> dict:
                self.calls += 1
                if self.calls <= 2:
                    return {
                        "composerFound": True,
                        "generating": False,
                        "assistantCount": 2,
                        "latestAssistant": "I",
                    }
                return {
                    "composerFound": True,
                    "generating": False,
                    "assistantCount": 2,
                    "latestAssistant": "```json\n{\"decision\":\"continue\"}\n```",
                }

        ticks = iter(range(100))
        with patch("chatgpt_cdp_bridge.time.monotonic", side_effect=lambda: next(ticks)):
            with patch("chatgpt_cdp_bridge.time.sleep", return_value=None):
                text = wait_for_response(FakeClient(), "", timeout_seconds=20, previous_assistant_count=1)

        self.assertIn('"decision":"continue"', text)

    def test_cdp_page_selection_requires_configured_thread(self) -> None:
        pages = [
            {
                "type": "page",
                "title": "Project Decision: Stop",
                "url": "https://chatgpt.com/c/wrong-thread",
                "webSocketDebuggerUrl": "ws://wrong",
            }
        ]
        with patch("chatgpt_cdp_bridge._list_pages", return_value=pages):
            with self.assertRaises(CdpError) as ctx:
                select_chatgpt_page("http://127.0.0.1:9222", "https://chatgpt.com/c/right-thread", allow_new_tab=False)

        self.assertEqual(ctx.exception.reason, "thread_unavailable")

    def test_cdp_page_selection_matches_project_thread_conversation_id(self) -> None:
        pages = [
            {
                "type": "page",
                "title": "Transitive RL Research",
                "url": "https://chatgpt.com/g/g-p-project/c/abc123?model=gpt-5",
                "webSocketDebuggerUrl": "ws://right",
            }
        ]
        with patch("chatgpt_cdp_bridge._list_pages", return_value=pages):
            page = select_chatgpt_page("http://127.0.0.1:9222", "https://chatgpt.com/c/abc123", allow_new_tab=False)

        self.assertEqual(page["webSocketDebuggerUrl"], "ws://right")


if __name__ == "__main__":
    unittest.main()
