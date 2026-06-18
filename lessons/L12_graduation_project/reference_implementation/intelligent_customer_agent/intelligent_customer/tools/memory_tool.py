from __future__ import annotations

import json
import time
from typing import Any

from intelligent_customer.config import MAX_HISTORY_MESSAGES, MEMORY_PATH, ensure_runtime_dirs
from intelligent_customer.harness.file_lock import locked_path
from intelligent_customer.harness.privacy import mask_sensitive_text


def _read_memory_unlocked() -> dict[str, Any]:
    ensure_runtime_dirs()
    try:
        return json.loads(MEMORY_PATH.read_text(encoding="utf-8") or "{}")
    except json.JSONDecodeError:
        return {}


def _write_memory_unlocked(payload: dict[str, Any]) -> None:
    ensure_runtime_dirs()
    MEMORY_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def _read_memory() -> dict[str, Any]:
    with locked_path(MEMORY_PATH):
        return _read_memory_unlocked()


def load_memory(session_id: str) -> dict[str, Any]:
    memory = _read_memory()
    return memory.get(session_id, {"session_id": session_id, "messages": [], "summary": ""})


def save_memory(session_id: str, user_message: str, assistant_message: str, metadata: dict[str, Any]) -> None:
    with locked_path(MEMORY_PATH):
        memory = _read_memory_unlocked()
        session = memory.setdefault(session_id, {"session_id": session_id, "messages": [], "summary": ""})
        now = time.time()
        session["messages"].append({"role": "user", "content": user_message, "ts": now})
        session["messages"].append({"role": "assistant", "content": assistant_message, "ts": now, "metadata": metadata})
        session["messages"] = session["messages"][-MAX_HISTORY_MESSAGES:]
        session["summary"] = summarize_messages(session["messages"])
        memory[session_id] = session
        _write_memory_unlocked(memory)


def summarize_messages(messages: list[dict[str, Any]]) -> str:
    recent = messages[-6:]
    parts = []
    for item in recent:
        content = str(item.get("content", "")).replace("\n", " ")[:80]
        parts.append(f"{item.get('role', 'unknown')}: {content}")
    return " | ".join(parts)


def _session_title(messages: list[dict[str, Any]]) -> str:
    for item in messages:
        if item.get("role") != "user":
            continue
        content = mask_sensitive_text(str(item.get("content", "")).replace("\n", " ").strip())
        if content:
            return content[:42]
    return "空会话"


def _latest_assistant_metadata(messages: list[dict[str, Any]]) -> dict[str, Any]:
    for item in reversed(messages):
        if item.get("role") == "assistant":
            metadata = item.get("metadata") or {}
            if isinstance(metadata, dict):
                return metadata
    return {}


def _last_updated(messages: list[dict[str, Any]]) -> float:
    timestamps = [float(item.get("ts", 0) or 0) for item in messages]
    return max(timestamps) if timestamps else 0.0


def reset_memory(session_id: str | None = None) -> None:
    with locked_path(MEMORY_PATH):
        memory = _read_memory_unlocked()
        if session_id is None:
            _write_memory_unlocked({})
            return
        memory.pop(session_id, None)
        _write_memory_unlocked(memory)


def list_sessions() -> list[dict[str, Any]]:
    memory = _read_memory()
    sessions: list[dict[str, Any]] = []
    for session_id, payload in memory.items():
        messages = payload.get("messages", [])
        metadata = _latest_assistant_metadata(messages)
        sessions.append(
            {
                "session_id": session_id,
                "message_count": len(messages),
                "title": _session_title(messages),
                "summary": mask_sensitive_text(str(payload.get("summary", ""))),
                "last_updated": _last_updated(messages),
                "last_intent": metadata.get("intent"),
                "last_route": metadata.get("route"),
                "ticket_id": metadata.get("ticket_id"),
                "need_human": bool(metadata.get("need_human", False)),
            }
        )
    return sorted(sessions, key=lambda item: (item["last_updated"], item["session_id"]), reverse=True)
