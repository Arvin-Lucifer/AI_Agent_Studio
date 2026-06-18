from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from uuid import uuid4

from intelligent_customer.harness.observability import metrics_snapshot, record_chat_metrics
from intelligent_customer.tools.knowledge_gap_tool import list_knowledge_gaps, record_knowledge_gap
from intelligent_customer.tools.memory_tool import list_sessions, reset_memory, save_memory
from intelligent_customer.tools.ticket_tool import create_ticket, list_tickets


def test_memory_writes_are_serialized_across_sessions() -> None:
    prefix = f"persist-memory-{uuid4().hex}"
    session_ids = [f"{prefix}-{index}" for index in range(8)]

    with ThreadPoolExecutor(max_workers=4) as pool:
        list(
            pool.map(
                lambda session_id: save_memory(session_id, "用户消息", "客服回复", {"source": "unit"}),
                session_ids,
            )
        )

    sessions = {item["session_id"]: item for item in list_sessions()}
    for session_id in session_ids:
        assert sessions[session_id]["message_count"] == 2
        reset_memory(session_id)


def test_ticket_append_is_serialized_under_concurrency() -> None:
    session_id = f"persist-ticket-{uuid4().hex}"

    def create(index: int) -> str:
        ticket = create_ticket(
            {
                "category": "handoff",
                "priority": "normal",
                "trace_id": f"trace-{index}",
                "session_id": session_id,
                "user_id": "unit",
                "message": f"并发工单 {index}",
                "reason": "unit_concurrency",
            }
        )
        return ticket["ticket_id"]

    with ThreadPoolExecutor(max_workers=6) as pool:
        ticket_ids = set(pool.map(create, range(12)))

    stored = {ticket["ticket_id"] for ticket in list_tickets(limit=100000) if ticket.get("session_id") == session_id}
    assert ticket_ids <= stored


def test_knowledge_gap_updates_are_serialized_under_concurrency() -> None:
    token = uuid4().hex
    message = f"并发知识缺口 {token}"

    def record(index: int) -> str:
        gap = record_knowledge_gap(
            {
                "trace_id": f"trace-gap-{index}",
                "session_id": f"session-gap-{index}",
                "message": message,
                "reason": "unit_concurrency",
                "priority": "normal",
            }
        )
        return gap["gap_id"]

    with ThreadPoolExecutor(max_workers=6) as pool:
        gap_ids = set(pool.map(record, range(8)))

    matching = [gap for gap in list_knowledge_gaps(limit=100000) if gap.get("message") == message]
    assert len(gap_ids) == 1
    assert len(matching) == 1
    assert matching[0]["count"] == 8
    assert len(matching[0]["trace_ids"]) == 8


def test_metrics_updates_are_serialized_under_concurrency() -> None:
    before = metrics_snapshot()["total_requests"]

    with ThreadPoolExecutor(max_workers=6) as pool:
        list(pool.map(lambda _: record_chat_metrics("qa", "retrieve", 10.0, None), range(12)))

    after = metrics_snapshot()["total_requests"]
    assert after >= before + 12
