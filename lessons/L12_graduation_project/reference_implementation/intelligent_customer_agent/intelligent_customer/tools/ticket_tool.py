from __future__ import annotations

import json
import time
from datetime import datetime, timedelta, timezone
from secrets import token_hex
from typing import Any

from intelligent_customer.config import TICKETS_PATH, ensure_runtime_dirs
from intelligent_customer.harness.file_lock import locked_path
from intelligent_customer.harness.privacy import mask_sensitive_text, sanitize_value


def create_ticket(payload: dict[str, Any]) -> dict[str, Any]:
    ensure_runtime_dirs()
    prefix = "T" if payload.get("category") == "complaint" else "H"
    created_at = datetime.now(timezone.utc)
    sla_hours = payload.get("sla_hours") or (2 if payload.get("priority") == "critical" else 4 if payload.get("priority") == "high" else 24)
    ticket_id = f"{prefix}-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}-{token_hex(3)}"
    ticket = {
        "ticket_id": ticket_id,
        "created_at": created_at.isoformat(),
        "due_at": (created_at + timedelta(hours=float(sla_hours))).isoformat(),
        "status": "open",
        "priority": payload.get("priority", "normal"),
        "urgency": payload.get("urgency", "normal"),
        "category": payload.get("category", "handoff"),
        "issue_type": payload.get("issue_type", "general"),
        "order_id": payload.get("order_id"),
        "contact_masked": payload.get("contact_masked"),
        "contact_type": payload.get("contact_type"),
        "trace_id": payload.get("trace_id"),
        "session_id": payload.get("session_id"),
        "user_id": payload.get("user_id"),
        "message": mask_sensitive_text(str(payload.get("message") or "")),
        "reason": payload.get("reason", ""),
        "metadata": sanitize_value(payload.get("metadata", {})),
        "sla_hours": sla_hours,
    }
    with locked_path(TICKETS_PATH):
        with TICKETS_PATH.open("a", encoding="utf-8") as f:
            f.write(json.dumps(ticket, ensure_ascii=False) + "\n")
    return _with_sla_state(ticket)


def list_tickets(limit: int = 100) -> list[dict[str, Any]]:
    tickets = _read_tickets()
    enriched = [_with_sla_state(ticket) for ticket in tickets]
    return sorted(enriched, key=lambda item: item.get("updated_at") or item.get("created_at", ""), reverse=True)[:limit]


def _read_tickets() -> list[dict[str, Any]]:
    with locked_path(TICKETS_PATH):
        return _read_tickets_unlocked()


def _read_tickets_unlocked() -> list[dict[str, Any]]:
    ensure_runtime_dirs()
    tickets: list[dict[str, Any]] = []
    for line in TICKETS_PATH.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            tickets.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return tickets


def _write_tickets_unlocked(tickets: list[dict[str, Any]]) -> None:
    ensure_runtime_dirs()
    with TICKETS_PATH.open("w", encoding="utf-8") as f:
        for ticket in tickets:
            f.write(json.dumps(ticket, ensure_ascii=False) + "\n")


def _parse_dt(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def _with_sla_state(ticket: dict[str, Any]) -> dict[str, Any]:
    enriched = dict(ticket)
    created = _parse_dt(str(enriched.get("created_at") or ""))
    due = _parse_dt(str(enriched.get("due_at") or ""))
    if due is None and created is not None:
        due = created + timedelta(hours=float(enriched.get("sla_hours") or 24))
        enriched["due_at"] = due.isoformat()
    now = datetime.now(timezone.utc)
    status = enriched.get("status")
    is_active = status in {"open", "in_progress"}
    overdue = bool(is_active and due is not None and now > due)
    minutes_left = None
    if is_active and due is not None:
        minutes_left = round((due - now).total_seconds() / 60, 1)
    enriched["overdue"] = overdue
    enriched["minutes_to_due"] = minutes_left
    return enriched


def update_ticket(ticket_id: str, status: str, assignee: str | None = None, note: str | None = None) -> dict[str, Any] | None:
    with locked_path(TICKETS_PATH):
        tickets = _read_tickets_unlocked()
        now = datetime.now(timezone.utc).isoformat()
        updated: dict[str, Any] | None = None
        for ticket in tickets:
            if ticket.get("ticket_id") != ticket_id:
                continue
            ticket["status"] = status
            ticket["updated_at"] = now
            if assignee is not None:
                ticket["assignee"] = assignee
            if note:
                ticket.setdefault("notes", [])
                ticket["notes"].append({"ts": now, "note": mask_sensitive_text(note), "assignee": assignee})
            updated = ticket
            break
        if updated is None:
            return None
        _write_tickets_unlocked(tickets)
    return _with_sla_state(updated)


def update_ticket_details(ticket_id: str, fields: dict[str, Any], note: str | None = None) -> dict[str, Any] | None:
    with locked_path(TICKETS_PATH):
        tickets = _read_tickets_unlocked()
        now = datetime.now(timezone.utc).isoformat()
        updated: dict[str, Any] | None = None
        allowed = {"issue_type", "urgency", "priority", "sla_hours", "order_id", "contact_masked", "contact_type"}
        for ticket in tickets:
            if ticket.get("ticket_id") != ticket_id:
                continue
            for key, value in fields.items():
                if key in allowed and value:
                    ticket[key] = value
            if "sla_hours" in fields and fields.get("sla_hours") and ticket.get("created_at"):
                created = _parse_dt(str(ticket.get("created_at")))
                if created is not None:
                    ticket["due_at"] = (created + timedelta(hours=float(fields["sla_hours"]))).isoformat()
            ticket["updated_at"] = now
            if note:
                ticket.setdefault("notes", [])
                ticket["notes"].append({"ts": now, "note": mask_sensitive_text(note), "assignee": "agent"})
            updated = ticket
            break
        if updated is None:
            return None
        _write_tickets_unlocked(tickets)
    return _with_sla_state(updated)


def find_latest_active_ticket(session_id: str) -> dict[str, Any] | None:
    tickets = [
        ticket
        for ticket in _read_tickets()
        if ticket.get("session_id") == session_id and ticket.get("status") in {"open", "in_progress"}
    ]
    if not tickets:
        return None
    return sorted(tickets, key=lambda item: item.get("updated_at") or item.get("created_at", ""), reverse=True)[0]


def find_ticket(ticket_id: str) -> dict[str, Any] | None:
    for ticket in _read_tickets():
        if str(ticket.get("ticket_id", "")).lower() == ticket_id.lower():
            return _with_sla_state(ticket)
    return None


def find_latest_ticket(session_id: str) -> dict[str, Any] | None:
    tickets = [ticket for ticket in _read_tickets() if ticket.get("session_id") == session_id]
    if not tickets:
        return None
    latest = sorted(tickets, key=lambda item: item.get("updated_at") or item.get("created_at", ""), reverse=True)[0]
    return _with_sla_state(latest)


def ticket_stats() -> dict[str, Any]:
    tickets = list_tickets(limit=100000)
    open_count = sum(1 for ticket in tickets if ticket.get("status") == "open")
    in_progress_count = sum(1 for ticket in tickets if ticket.get("status") == "in_progress")
    resolved_count = sum(1 for ticket in tickets if ticket.get("status") in {"resolved", "closed"})
    overdue_count = sum(1 for ticket in tickets if ticket.get("overdue"))
    return {
        "total": len(tickets),
        "open": open_count,
        "in_progress": in_progress_count,
        "resolved": resolved_count,
        "overdue": overdue_count,
        "ts": time.time(),
    }
