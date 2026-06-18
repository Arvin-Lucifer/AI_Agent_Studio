from __future__ import annotations

import json
import time
from datetime import datetime, timezone
from secrets import token_hex
from typing import Any

from intelligent_customer.config import KNOWLEDGE_GAPS_PATH, ensure_runtime_dirs
from intelligent_customer.harness.file_lock import locked_path


def _read_gaps() -> list[dict[str, Any]]:
    with locked_path(KNOWLEDGE_GAPS_PATH):
        return _read_gaps_unlocked()


def _read_gaps_unlocked() -> list[dict[str, Any]]:
    ensure_runtime_dirs()
    gaps: list[dict[str, Any]] = []
    for line in KNOWLEDGE_GAPS_PATH.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            gaps.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return gaps


def _write_gaps_unlocked(gaps: list[dict[str, Any]]) -> None:
    ensure_runtime_dirs()
    with KNOWLEDGE_GAPS_PATH.open("w", encoding="utf-8") as f:
        for gap in gaps:
            f.write(json.dumps(gap, ensure_ascii=False) + "\n")


def _fingerprint(message: str, reason: str) -> str:
    normalized = "".join(message.lower().split())[:80]
    return f"{reason}:{normalized}"


def record_knowledge_gap(payload: dict[str, Any]) -> dict[str, Any]:
    ensure_runtime_dirs()
    with locked_path(KNOWLEDGE_GAPS_PATH):
        message = str(payload.get("message", ""))
        reason = str(payload.get("reason", "unknown"))
        fingerprint = _fingerprint(message, reason)
        gaps = _read_gaps_unlocked()
        now = datetime.now(timezone.utc).isoformat()
        for gap in gaps:
            if gap.get("fingerprint") != fingerprint or gap.get("status") == "closed":
                continue
            gap["count"] = int(gap.get("count", 1)) + 1
            gap["updated_at"] = now
            gap.setdefault("trace_ids", [])
            trace_id = payload.get("trace_id")
            if trace_id and trace_id not in gap["trace_ids"]:
                gap["trace_ids"].append(trace_id)
            gap["last_message"] = message
            gap["last_session_id"] = payload.get("session_id")
            _write_gaps_unlocked(gaps)
            return gap

        gap = {
            "gap_id": f"KG-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}-{token_hex(3)}",
            "created_at": now,
            "updated_at": now,
            "status": "open",
            "priority": payload.get("priority", "normal"),
            "reason": reason,
            "fingerprint": fingerprint,
            "count": 1,
            "message": message,
            "last_message": message,
            "session_id": payload.get("session_id"),
            "last_session_id": payload.get("session_id"),
            "trace_ids": [payload.get("trace_id")] if payload.get("trace_id") else [],
            "intent": payload.get("intent"),
            "route": payload.get("route"),
            "confidence": payload.get("confidence"),
            "suggested_action": payload.get("suggested_action", "补充知识库文档或新增评测用例"),
            "metadata": payload.get("metadata", {}),
        }
        with KNOWLEDGE_GAPS_PATH.open("a", encoding="utf-8") as f:
            f.write(json.dumps(gap, ensure_ascii=False) + "\n")
        return gap


def list_knowledge_gaps(limit: int = 100, status: str | None = None) -> list[dict[str, Any]]:
    gaps = _read_gaps()
    if status:
        gaps = [gap for gap in gaps if gap.get("status") == status]
    return sorted(gaps, key=lambda item: (item.get("status") != "open", -int(item.get("count", 1)), item.get("updated_at", "")))[:limit]


def get_knowledge_gap(gap_id: str) -> dict[str, Any] | None:
    for gap in _read_gaps():
        if gap.get("gap_id") == gap_id:
            return gap
    return None


def update_knowledge_gap(gap_id: str, status: str, note: str | None = None) -> dict[str, Any] | None:
    with locked_path(KNOWLEDGE_GAPS_PATH):
        gaps = _read_gaps_unlocked()
        now = datetime.now(timezone.utc).isoformat()
        updated: dict[str, Any] | None = None
        for gap in gaps:
            if gap.get("gap_id") != gap_id:
                continue
            gap["status"] = status
            gap["updated_at"] = now
            if note:
                gap.setdefault("notes", [])
                gap["notes"].append({"ts": now, "note": note})
            updated = gap
            break
        if updated is None:
            return None
        _write_gaps_unlocked(gaps)
    return updated


def knowledge_gap_stats() -> dict[str, Any]:
    gaps = _read_gaps()
    open_count = sum(1 for gap in gaps if gap.get("status") == "open")
    closed_count = sum(1 for gap in gaps if gap.get("status") == "closed")
    total_mentions = sum(int(gap.get("count", 1)) for gap in gaps)
    return {
        "total": len(gaps),
        "open": open_count,
        "closed": closed_count,
        "mentions": total_mentions,
        "ts": time.time(),
    }
