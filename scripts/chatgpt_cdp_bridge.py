"""Visible ChatGPT browser bridge using Chrome DevTools Protocol.

This is a pragmatic fallback for environments where the codex-chatgpt-control
host bridge is unavailable in an ordinary shell. It automates a user-visible
Chrome tab through CDP only; it does not call private ChatGPT endpoints.
"""

from __future__ import annotations

import argparse
import json
import socket
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional


DEFAULT_CDP_URL = "http://127.0.0.1:9222"
CHATGPT_ORIGIN = "https://chatgpt.com"
PROMPT_MARKER = "Autoresearcher ChatGPT Pro checkpoint."


@dataclass
class CdpResponse:
    status: str
    raw_text: Optional[str] = None
    reason: Optional[str] = None
    message: Optional[str] = None
    details: Optional[Dict[str, Any]] = None


class CdpError(RuntimeError):
    def __init__(self, reason: str, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.reason = reason
        self.details = details or {}


class CdpClient:
    def __init__(self, websocket_url: str, timeout: float = 30.0):
        try:
            from websocket import create_connection  # type: ignore
        except ImportError as exc:  # pragma: no cover - optional dependency
            raise CdpError(
                "backend_dependency_missing",
                "Python package websocket-client is required for the CDP backend.",
                {"import_error": str(exc)},
            ) from exc
        try:
            self._ws = create_connection(websocket_url, timeout=timeout, suppress_origin=True)
        except Exception as exc:  # websocket-client raises its own exception hierarchy.
            raise CdpError(
                "browser_bridge_unavailable",
                f"Could not connect to the Chrome DevTools page WebSocket: {exc}",
                {"websocket_url": websocket_url, "error": str(exc)},
            ) from exc
        self._next_id = 0

    def close(self) -> None:
        try:
            self._ws.close()
        except Exception:
            pass

    def call(self, method: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        self._next_id += 1
        message_id = self._next_id
        try:
            self._ws.send(json.dumps({"id": message_id, "method": method, "params": params or {}}))
            while True:
                raw = self._ws.recv()
                payload = json.loads(raw)
                if payload.get("id") != message_id:
                    continue
                if "error" in payload:
                    raise CdpError(
                        "pro_backend_failed",
                        f"CDP call {method} failed: {payload['error']}",
                        {"method": method, "error": payload["error"]},
                    )
                result = payload.get("result")
                return result if isinstance(result, dict) else {}
        except CdpError:
            raise
        except Exception as exc:  # websocket-client disconnects are not OSError subclasses.
            raise CdpError(
                "browser_bridge_unavailable",
                f"Chrome DevTools WebSocket connection failed during {method}: {exc}",
                {"method": method, "error": str(exc)},
            ) from exc

    def evaluate(self, expression: str, timeout_ms: int = 30000) -> Any:
        result = self.call(
            "Runtime.evaluate",
            {
                "expression": expression,
                "awaitPromise": True,
                "returnByValue": True,
                "timeout": timeout_ms,
            },
        )
        if "exceptionDetails" in result:
            raise CdpError(
                "pro_backend_failed",
                "JavaScript evaluation failed in the ChatGPT tab.",
                {"exception": result.get("exceptionDetails")},
            )
        value = result.get("result", {}).get("value")
        return value


def _read_json(url: str, timeout: float = 5.0) -> Any:
    try:
        with urllib.request.urlopen(url, timeout=timeout) as response:
            return json.loads(response.read().decode("utf-8"))
    except (OSError, urllib.error.URLError, json.JSONDecodeError) as exc:
        raise CdpError(
            "browser_bridge_unavailable",
            f"Chrome DevTools endpoint is not reachable at {url}: {exc}",
            {"url": url},
        ) from exc


def _safe_cdp_url(url: str) -> str:
    return url.rstrip("/")


def _normalize_thread_url(url: str) -> str:
    parsed = urllib.parse.urlparse(url.strip())
    if not parsed.scheme or not parsed.netloc:
        return url.strip().rstrip("/")
    return urllib.parse.urlunparse((parsed.scheme, parsed.netloc, parsed.path.rstrip("/"), "", "", ""))


def _conversation_id(url: str) -> Optional[str]:
    parsed = urllib.parse.urlparse(url.strip())
    parts = [urllib.parse.unquote(part) for part in parsed.path.split("/") if part]
    for index, part in enumerate(parts):
        if part == "c" and index + 1 < len(parts):
            return parts[index + 1]
    return None


def _page_matches_thread(page_url: str, thread_url: str) -> bool:
    if not thread_url:
        return False
    normalized_page = _normalize_thread_url(page_url)
    normalized_thread = _normalize_thread_url(thread_url)
    if normalized_page == normalized_thread:
        return True
    page_conversation = _conversation_id(normalized_page)
    thread_conversation = _conversation_id(normalized_thread)
    return bool(page_conversation and thread_conversation and page_conversation == thread_conversation)


def _page_score(page: Dict[str, Any], thread_url: str) -> int:
    url = str(page.get("url") or "")
    if thread_url:
        if _normalize_thread_url(url) == _normalize_thread_url(thread_url):
            return 100
        if _page_matches_thread(url, thread_url):
            return 95
        return 0
    if "chatgpt.com/c/" in url:
        return 100
    if url.startswith(CHATGPT_ORIGIN):
        return 70
    return 0


def _list_pages(cdp_url: str) -> List[Dict[str, Any]]:
    payload = _read_json(f"{_safe_cdp_url(cdp_url)}/json/list")
    if not isinstance(payload, list):
        raise CdpError("browser_bridge_unavailable", "Chrome DevTools /json/list did not return a list.")
    return [item for item in payload if isinstance(item, dict) and item.get("type") == "page"]


def _open_tab(cdp_url: str, url: str) -> Optional[Dict[str, Any]]:
    encoded = urllib.parse.quote(url, safe="")
    for method in ("PUT", "GET"):
        request = urllib.request.Request(f"{_safe_cdp_url(cdp_url)}/json/new?{encoded}", method=method)
        try:
            with urllib.request.urlopen(request, timeout=5) as response:
                payload = json.loads(response.read().decode("utf-8"))
            return payload if isinstance(payload, dict) else None
        except (OSError, urllib.error.URLError, json.JSONDecodeError):
            continue
    return None


def select_chatgpt_page(cdp_url: str, thread_url: str, allow_new_tab: bool = True) -> Dict[str, Any]:
    pages = _list_pages(cdp_url)
    scored = sorted(((page, _page_score(page, thread_url)) for page in pages), key=lambda item: item[1], reverse=True)
    if scored and scored[0][1] > 0:
        return scored[0][0]
    if allow_new_tab and thread_url:
        opened = _open_tab(cdp_url, thread_url)
        if opened is not None:
            return opened
    raise CdpError(
        "thread_unavailable",
        "The configured ChatGPT thread is not available through Chrome DevTools.",
        {"cdp_url": cdp_url, "page_urls": [page.get("url") for page in pages]},
    )


STATE_SCRIPT = r"""
(() => {
  const text = document.body ? document.body.innerText : "";
  const composerSelectors = [
    '#prompt-textarea',
    '[contenteditable="true"][id="prompt-textarea"]',
    '[data-testid="composer-text-input"]',
    'textarea',
    '[contenteditable="true"]'
  ];
  const sendSelectors = [
    'button[data-testid="send-button"]',
    'button[aria-label*="Send"]',
    'button[aria-label*="send"]',
    'button[type="submit"]'
  ];
  const composer = composerSelectors.map((s) => document.querySelector(s)).find(Boolean);
  const sendButton = sendSelectors.map((s) => document.querySelector(s)).find(Boolean);
  const assistantNodes = Array.from(document.querySelectorAll([
    '[data-message-author-role="assistant"]',
    '[data-testid="assistant-turn"]',
    'article'
  ].join(','))).filter((node) => {
    const value = (node.getAttribute('data-message-author-role') || '').toLowerCase();
    return value === 'assistant' || node.matches('[data-testid="assistant-turn"]') || node.innerText.length > 50;
  });
  const latestAssistant = assistantNodes.length ? assistantNodes[assistantNodes.length - 1].innerText : "";
  const generating = Boolean(document.querySelector('button[data-testid="stop-button"]')) ||
    Array.from(document.querySelectorAll('button')).some((button) => {
      const label = (button.getAttribute('aria-label') || button.innerText || '').trim().toLowerCase();
      return [
        'stop generating',
        'stop streaming',
        'stop response',
        'stop responding'
      ].includes(label);
    });
  const loginRequired = /log in|sign up|continue with google|continue with microsoft/i.test(text) && !composer;
  const captcha = /captcha|verify you are human|checking your browser/i.test(text);
  const rateLimited = /too many requests|rate limit|try again later/i.test(text);
  return {
    href: location.href,
    title: document.title,
    loginRequired,
    captcha,
    rateLimited,
    composerFound: Boolean(composer),
    sendFound: Boolean(sendButton),
    sendDisabled: sendButton ? Boolean(sendButton.disabled || sendButton.getAttribute('aria-disabled') === 'true') : null,
    generating,
    assistantCount: assistantNodes.length,
    latestAssistant,
    bodySample: text.slice(0, 1200)
  };
})()
"""


FOCUS_COMPOSER_SCRIPT = r"""
(() => {
  const selectors = [
    '#prompt-textarea',
    '[contenteditable="true"][id="prompt-textarea"]',
    '[data-testid="composer-text-input"]',
    'textarea',
    '[contenteditable="true"]'
  ];
  const composer = selectors.map((s) => document.querySelector(s)).find(Boolean);
  if (!composer) {
    return { ok: false, reason: "composer_not_found" };
  }
  composer.focus();
  return { ok: true, tagName: composer.tagName, contentEditable: composer.isContentEditable };
})()
"""


CLICK_SEND_SCRIPT = r"""
(() => {
  const selectors = [
    'button[data-testid="send-button"]',
    'button[aria-label*="Send"]',
    'button[aria-label*="send"]',
    'button[type="submit"]'
  ];
  const button = selectors.map((s) => document.querySelector(s)).find(Boolean);
  if (!button) {
    return { ok: false, reason: "send_button_not_found" };
  }
  if (button.disabled || button.getAttribute('aria-disabled') === 'true') {
    return { ok: false, reason: "send_button_disabled" };
  }
  button.click();
  return { ok: true };
})()
"""


def _require_ready(state: Dict[str, Any]) -> None:
    if state.get("captcha"):
        raise CdpError("captcha", "ChatGPT is showing a human verification challenge.", state)
    if state.get("rateLimited"):
        raise CdpError("rate_limit", "ChatGPT is rate-limited or asking to try later.", state)
    if state.get("loginRequired"):
        raise CdpError("login_required", "The visible ChatGPT tab is not logged in.", state)
    if not state.get("composerFound"):
        raise CdpError("selector_drift", "Could not find the ChatGPT message composer.", state)


def connect_page(cdp_url: str, thread_url: str, allow_new_tab: bool = True) -> CdpClient:
    page = select_chatgpt_page(cdp_url, thread_url, allow_new_tab=allow_new_tab)
    websocket_url = page.get("webSocketDebuggerUrl")
    if not isinstance(websocket_url, str) or not websocket_url:
        raise CdpError("browser_bridge_unavailable", "Selected Chrome page has no webSocketDebuggerUrl.", page)
    client = CdpClient(websocket_url)
    client.call("Runtime.enable")
    client.call("Page.enable")
    if thread_url and not _page_matches_thread(str(page.get("url") or ""), thread_url):
        client.call("Page.navigate", {"url": thread_url})
    return client


def wait_for_ready(client: CdpClient, timeout_seconds: int = 120) -> Dict[str, Any]:
    deadline = time.monotonic() + timeout_seconds
    latest_state: Dict[str, Any] = {}
    while time.monotonic() < deadline:
        value = client.evaluate(STATE_SCRIPT)
        latest_state = value if isinstance(value, dict) else {}
        if latest_state.get("captcha") or latest_state.get("rateLimited") or latest_state.get("loginRequired"):
            _require_ready(latest_state)
        if latest_state.get("composerFound") and not latest_state.get("generating"):
            return latest_state
        time.sleep(1)
    _require_ready(latest_state)
    if latest_state.get("generating"):
        raise CdpError("pro_backend_failed", "Timed out waiting for ChatGPT to finish the current response.", latest_state)
    raise CdpError("selector_drift", "Timed out waiting for ChatGPT composer.", latest_state)


def submit_prompt(client: CdpClient, prompt: str) -> Dict[str, Any]:
    focus = client.evaluate(FOCUS_COMPOSER_SCRIPT)
    if not isinstance(focus, dict) or not focus.get("ok"):
        raise CdpError("selector_drift", "Could not focus the ChatGPT composer.", {"focus": focus})

    ctrl = 2
    client.call("Input.dispatchKeyEvent", {"type": "keyDown", "modifiers": ctrl, "windowsVirtualKeyCode": 65, "code": "KeyA", "key": "a"})
    client.call("Input.dispatchKeyEvent", {"type": "keyUp", "modifiers": ctrl, "windowsVirtualKeyCode": 65, "code": "KeyA", "key": "a"})
    client.call("Input.dispatchKeyEvent", {"type": "keyDown", "windowsVirtualKeyCode": 8, "code": "Backspace", "key": "Backspace"})
    client.call("Input.dispatchKeyEvent", {"type": "keyUp", "windowsVirtualKeyCode": 8, "code": "Backspace", "key": "Backspace"})
    client.call("Input.insertText", {"text": prompt})

    deadline = time.monotonic() + 20
    click_result: Any = None
    while time.monotonic() < deadline:
        click_result = client.evaluate(CLICK_SEND_SCRIPT)
        if isinstance(click_result, dict) and click_result.get("ok"):
            return click_result
        time.sleep(0.5)
    raise CdpError("selector_drift", "Could not click the ChatGPT send button.", {"click": click_result})


def wait_for_response(client: CdpClient, previous_assistant: str, timeout_seconds: int = 600) -> str:
    deadline = time.monotonic() + timeout_seconds
    stable_since: Optional[float] = None
    latest_text = ""
    latest_state: Dict[str, Any] = {}
    while time.monotonic() < deadline:
        value = client.evaluate(STATE_SCRIPT)
        latest_state = value if isinstance(value, dict) else {}
        _require_ready(latest_state)
        candidate = str(latest_state.get("latestAssistant") or "")
        if PROMPT_MARKER in candidate:
            candidate = ""
        changed = candidate.strip() and candidate != previous_assistant and candidate != latest_text
        if changed:
            latest_text = candidate
            stable_since = time.monotonic()
        elif latest_text and not latest_state.get("generating") and stable_since is not None:
            if time.monotonic() - stable_since >= 4:
                return latest_text
        time.sleep(1)
    raise CdpError("pro_backend_failed", "Timed out waiting for a ChatGPT assistant response.", latest_state)


def build_visible_prompt(instructions: str, packet: str, reason: str) -> str:
    return (
        f"{PROMPT_MARKER}\n\n"
        f"Checkpoint reason: {reason}\n\n"
        "Continuing this existing research-advisor thread: use your thread memory plus the linked GitHub evidence in the packet. "
        "Please decide the next research direction and return the requested fenced JSON plus at most one short paragraph.\n\n"
        "## Standing Advisor Instructions\n\n"
        f"{instructions.strip()}\n\n"
        "## Current Pointer Packet\n\n"
        f"{packet.strip()}\n"
    )


def run_cdp_review(
    cdp_url: str,
    thread_url: str,
    instructions: str,
    packet: str,
    reason: str,
    allow_new_tab: bool = True,
    ready_timeout_seconds: int = 120,
    response_timeout_seconds: int = 600,
) -> CdpResponse:
    client: Optional[CdpClient] = None
    try:
        client = connect_page(cdp_url, thread_url, allow_new_tab=allow_new_tab)
        state = wait_for_ready(client, timeout_seconds=ready_timeout_seconds)
        previous = str(state.get("latestAssistant") or "")
        submit_prompt(client, build_visible_prompt(instructions, packet, reason))
        raw_text = wait_for_response(client, previous, timeout_seconds=response_timeout_seconds)
        return CdpResponse(status="completed", raw_text=raw_text)
    except CdpError as exc:
        return CdpResponse(status="blocked", reason=exc.reason, message=str(exc), details=exc.details)
    except (socket.timeout, TimeoutError, OSError) as exc:
        return CdpResponse(
            status="blocked",
            reason="browser_bridge_unavailable",
            message=f"Chrome DevTools connection failed: {exc}",
            details={"error": str(exc)},
        )
    finally:
        if client is not None:
            client.close()


def probe_cdp(cdp_url: str, thread_url: str) -> Dict[str, Any]:
    client: Optional[CdpClient] = None
    try:
        page = select_chatgpt_page(cdp_url, thread_url, allow_new_tab=False)
        websocket_url = page.get("webSocketDebuggerUrl")
        if not isinstance(websocket_url, str):
            raise CdpError("browser_bridge_unavailable", "Selected page has no websocket URL.", page)
        client = CdpClient(websocket_url)
        client.call("Runtime.enable")
        state = client.evaluate(STATE_SCRIPT)
        return {"ok": True, "page": {"title": page.get("title"), "url": page.get("url")}, "state": state}
    except CdpError as exc:
        return {"ok": False, "reason": exc.reason, "message": str(exc), "details": exc.details}
    finally:
        if client is not None:
            client.close()


def main(argv: Optional[Iterable[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Probe or use a visible ChatGPT tab through Chrome DevTools.")
    subparsers = parser.add_subparsers(dest="command", required=True)
    probe_p = subparsers.add_parser("probe")
    probe_p.add_argument("--cdp-url", default=DEFAULT_CDP_URL)
    probe_p.add_argument("--thread-url", required=True)
    args = parser.parse_args(list(argv) if argv is not None else None)

    if args.command == "probe":
        print(json.dumps(probe_cdp(args.cdp_url, args.thread_url), indent=2, sort_keys=True))
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
