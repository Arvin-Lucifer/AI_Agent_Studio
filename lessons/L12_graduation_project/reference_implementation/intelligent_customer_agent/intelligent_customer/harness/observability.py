from __future__ import annotations

import json
import statistics
import time
from collections import Counter
from pathlib import Path
from typing import Any

from intelligent_customer.config import EVENTS_PATH, METRICS_PATH, ensure_runtime_dirs
from intelligent_customer.harness.file_lock import locked_path
from intelligent_customer.harness.privacy import sanitize_fields


def log_event(trace_id: str, session_id: str, stage: str, **fields: Any) -> None:
    ensure_runtime_dirs()
    safe_fields = sanitize_fields(fields)
    event = {
        "ts": time.time(),
        "trace_id": trace_id,
        "session_id": session_id,
        "stage": stage,
        **safe_fields,
    }
    with locked_path(EVENTS_PATH):
        with EVENTS_PATH.open("a", encoding="utf-8") as f:
            f.write(json.dumps(event, ensure_ascii=False) + "\n")


def read_events(path: Path = EVENTS_PATH) -> list[dict[str, Any]]:
    ensure_runtime_dirs()
    with locked_path(path):
        events: list[dict[str, Any]] = []
        for line in path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            try:
                events.append(json.loads(line))
            except json.JSONDecodeError:
                continue
        return events


def audit_trace(trace_id: str) -> list[dict[str, Any]]:
    return [event for event in read_events() if event.get("trace_id") == trace_id]


def record_chat_metrics(intent: str, route: str, latency_ms: float, ticket_id: str | None) -> None:
    ensure_runtime_dirs()
    with locked_path(METRICS_PATH):
        metrics = _load_metrics_unlocked()
        metrics["total_requests"] = metrics.get("total_requests", 0) + 1
        metrics.setdefault("intent_distribution", {})
        metrics["intent_distribution"][intent] = metrics["intent_distribution"].get(intent, 0) + 1
        metrics.setdefault("route_distribution", {})
        metrics["route_distribution"][route] = metrics["route_distribution"].get(route, 0) + 1
        metrics.setdefault("latencies_ms", [])
        metrics["latencies_ms"] = (metrics["latencies_ms"] + [latency_ms])[-1000:]
        if ticket_id:
            metrics["ticket_count"] = metrics.get("ticket_count", 0) + 1
        if route == "human_handoff":
            metrics["fallback_count"] = metrics.get("fallback_count", 0) + 1
        if route == "clarify":
            metrics["clarification_count"] = metrics.get("clarification_count", 0) + 1
        _write_metrics_unlocked(metrics)


def record_feedback_metrics(rating: str) -> None:
    ensure_runtime_dirs()
    with locked_path(METRICS_PATH):
        metrics = _load_metrics_unlocked()
        metrics.setdefault("feedback_distribution", {})
        metrics["feedback_distribution"][rating] = metrics["feedback_distribution"].get(rating, 0) + 1
        metrics["feedback_count"] = metrics.get("feedback_count", 0) + 1
        _write_metrics_unlocked(metrics)


def _load_metrics_unlocked() -> dict[str, Any]:
    ensure_runtime_dirs()
    if not METRICS_PATH.exists():
        return {}
    try:
        return json.loads(METRICS_PATH.read_text(encoding="utf-8") or "{}")
    except json.JSONDecodeError:
        return {}


def _write_metrics_unlocked(metrics: dict[str, Any]) -> None:
    METRICS_PATH.write_text(json.dumps(metrics, ensure_ascii=False, indent=2), encoding="utf-8")


def load_metrics() -> dict[str, Any]:
    with locked_path(METRICS_PATH):
        return _load_metrics_unlocked()


def metrics_snapshot() -> dict[str, Any]:
    metrics = load_metrics()
    latencies = [float(v) for v in metrics.get("latencies_ms", [])]
    total = int(metrics.get("total_requests", 0))
    p95 = 0.0
    if latencies:
        ordered = sorted(latencies)
        p95 = ordered[min(len(ordered) - 1, int(len(ordered) * 0.95))]
    return {
        "total_requests": total,
        "intent_distribution": metrics.get("intent_distribution", {}),
        "route_distribution": metrics.get("route_distribution", {}),
        "avg_latency_ms": round(statistics.mean(latencies), 2) if latencies else 0.0,
        "p95_latency_ms": round(p95, 2),
        "ticket_count": int(metrics.get("ticket_count", 0)),
        "fallback_rate": round(metrics.get("fallback_count", 0) / total, 4) if total else 0.0,
        "clarification_rate": round(metrics.get("clarification_count", 0) / total, 4) if total else 0.0,
        "feedback_count": int(metrics.get("feedback_count", 0)),
        "feedback_distribution": metrics.get("feedback_distribution", {}),
        "react_trigger_rate": 0.0,
        "multihop_rate": 0.0,
        "recent_event_count": len(read_events()[-500:]),
        "top_intents": Counter(metrics.get("intent_distribution", {})).most_common(),
    }


def recent_events(limit: int = 100) -> list[dict[str, Any]]:
    return read_events()[-limit:][::-1]
