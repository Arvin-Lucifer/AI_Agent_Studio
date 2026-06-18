from __future__ import annotations

import re
import shutil
import subprocess
from pathlib import Path

import pytest
from fastapi import HTTPException

from intelligent_customer.harness.security import check_rate_limit, require_admin_key


ROOT = Path(__file__).resolve().parents[1]


def test_admin_key_protects_write_endpoints(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("ADMIN_API_KEY", "test-admin-key")
    with pytest.raises(HTTPException) as denied:
        require_admin_key(None)
    require_admin_key("test-admin-key")
    assert denied.value.status_code == 401


def test_rate_limit_guard_blocks_after_limit() -> None:
    identity = "unit-test-rate-limit"
    check_rate_limit(identity, limit=2)
    check_rate_limit(identity, limit=2)
    with pytest.raises(Exception):
        check_rate_limit(identity, limit=2)


def test_frontend_script_syntax_if_node_is_available(tmp_path: Path) -> None:
    node = shutil.which("node")
    if node is None:
        pytest.skip("node is not installed")
    for name in ["dashboard", "index"]:
        html = (ROOT / "web" / f"{name}.html").read_text(encoding="utf-8")
        match = re.search(r"<script>(.*?)</script>", html, re.S)
        assert match
        script_path = tmp_path / f"{name}.js"
        script_path.write_text(match.group(1), encoding="utf-8")
        result = subprocess.run([node, "--check", str(script_path)], check=False, capture_output=True, text=True)
        assert result.returncode == 0, result.stderr


def test_chat_frontend_keeps_operational_controls() -> None:
    html = (ROOT / "web" / "index.html").read_text(encoding="utf-8")
    assert "data-retry" in html
    assert "data-copy" in html
    assert "navigator.clipboard" in html
    assert "哪里需要改进" in html
    assert "retry_text" in html


def test_chat_frontend_has_polished_status_visuals() -> None:
    html = (ROOT / "web" / "index.html").read_text(encoding="utf-8")
    assert ".avatar" in html
    assert "composer-inner:focus-within" in html
    assert "ticket-active" in html
    assert "route.human_handoff" in html
    assert "avatarLabel" in html
    assert "处理中" in html


def test_chat_frontend_renders_session_snapshots() -> None:
    html = (ROOT / "web" / "index.html").read_text(encoding="utf-8")
    assert "session-meta" in html
    assert "session-chip" in html
    assert "last_route" in html
    assert "last_intent" in html
    assert "formatRelativeTime" in html


def test_chat_frontend_filters_session_queue() -> None:
    html = (ROOT / "web" / "index.html").read_text(encoding="utf-8")
    assert "sessionSearch" in html
    assert "sessionFilter" in html
    assert "sessionMatchesFilter" in html
    assert "sessionMatchesSearch" in html
    assert "renderSessions" in html
    assert "待人工" in html
