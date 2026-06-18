from __future__ import annotations

from types import SimpleNamespace
from uuid import uuid4

import pytest

from intelligent_customer import api
from intelligent_customer.config import KB_DIR
from intelligent_customer.rag.kb_builder import build_kb_index
from intelligent_customer.rag.retriever import clear_index_cache, search_kb
from intelligent_customer.schemas import (
    ChatRequest,
    FeedbackRequest,
    KBDocumentCreateRequest,
    KnowledgeGapUpdateRequest,
    TicketUpdateRequest,
)
from intelligent_customer.tools.memory_tool import reset_memory


class _Headers(dict):
    def get(self, key: str, default: str | None = None) -> str | None:
        return super().get(key, default)


def _request() -> SimpleNamespace:
    return SimpleNamespace(headers=_Headers(), client=SimpleNamespace(host="testclient"))


def _chat(message: str, session_id: str, user_id: str | None = None):
    return api.chat(ChatRequest(message=message, session_id=session_id, user_id=user_id), _request())


def setup_module() -> None:
    build_kb_index()
    clear_index_cache()


def test_health_returns_ok() -> None:
    assert api.health().model_dump() == {"status": "ok"}


def test_chat_returns_uniform_schema() -> None:
    reset_memory("test_api_schema")
    response = _chat("忘记密码怎么找回？", "test_api_schema", user_id="u1")
    payload = response.model_dump()
    for key in ["trace_id", "session_id", "intent", "route", "reply", "confidence", "ticket_id", "need_human"]:
        assert key in payload
    assert payload["intent"] == "qa"
    assert payload["route"] == "retrieve"
    assert payload["citations"]
    assert payload["citations"][0]["snippet"]
    assert payload["metadata"]["latency_ms"] >= 0
    history = api.session_history("test_api_schema")
    latest_assistant = [item for item in history["messages"] if item["role"] == "assistant"][-1]
    assert latest_assistant["metadata"]["latency_ms"] >= 0


def test_sessions_include_persistent_status_snapshot() -> None:
    session_id = f"test_api_session_snapshot_{uuid4().hex[:8]}"
    reset_memory(session_id)
    _chat("我要投诉，订单号 ORD202606050001 重复扣费，请联系 13812345678。", session_id)
    sessions = api.sessions()["sessions"]
    snapshot = next(item for item in sessions if item["session_id"] == session_id)
    assert snapshot["title"].startswith("我要投诉")
    assert "13812345678" not in str(snapshot)
    assert snapshot["message_count"] >= 2
    assert snapshot["last_intent"] == "complaint"
    assert snapshot["last_route"] == "ticket"
    assert snapshot["ticket_id"]
    assert snapshot["need_human"] is True
    assert snapshot["last_updated"] > 0


def test_complaint_creates_ticket() -> None:
    reset_memory("test_api_complaint")
    payload = _chat("我要投诉，你们客服态度差。", "test_api_complaint").model_dump()
    assert payload["intent"] == "complaint"
    assert payload["route"] == "ticket"
    assert payload["ticket_id"]
    assert payload["need_human"] is True


def test_complaint_ticket_has_extracted_fields() -> None:
    response = _chat(
        "我要投诉，订单号 ORD202606050001 重复扣费，请联系 13812345678。",
        "test_api_ticket_extract",
    )
    ticket_id = response.ticket_id
    tickets = api.tickets(limit=20)["tickets"]
    ticket = next(item for item in tickets if item["ticket_id"] == ticket_id)
    assert ticket["order_id"] == "ORD202606050001"
    assert ticket["contact_masked"] == "138****5678"
    assert "13812345678" not in ticket["message"]
    assert ticket["issue_type"] == "payment"
    assert ticket["priority"] == "high"
    assert ticket["sla_hours"] == 4
    assert ticket["due_at"]
    assert "minutes_to_due" in ticket
    assert ticket["metadata"]["handoff"]["summary"]
    assert "13812345678" not in str(ticket["metadata"]["handoff"])
    assert "按优先级联系用户并更新工单状态" in ticket["metadata"]["handoff"]["next_steps"]


def test_followup_message_enriches_existing_ticket() -> None:
    session_id = "test_api_ticket_enrich"
    first = _chat("我要投诉，重复扣费一直没人处理。", session_id)
    second = _chat("补充一下，订单号 ORD202606050099，手机号 13912345678。", session_id)
    tickets = api.tickets(limit=50)["tickets"]
    ticket = next(item for item in tickets if item["ticket_id"] == first.ticket_id)
    assert second.ticket_id == first.ticket_id
    assert second.route == "final"
    assert second.metadata["ticket_enriched"] is True
    assert ticket["order_id"] == "ORD202606050099"
    assert ticket["contact_masked"] == "139****5678"


def test_metrics_and_audit() -> None:
    payload = _chat("企业版 SLA 是多少？", "test_api_audit")
    metrics = api.metrics()
    audit = api.audit(payload.trace_id)
    assert metrics["total_requests"] >= 1
    assert any(event["stage"] == "chat.request" for event in audit)


def test_eval_report_endpoint_runs_quality_gate(monkeypatch: pytest.MonkeyPatch) -> None:
    def fake_report() -> dict:
        return {
            "status": "ok",
            "generated_at": "2026-06-06T00:00:00+00:00",
            "dataset_cases": 24,
            "report_path": "evals/eval_report.json",
            "dataset_path": "evals/eval_dataset.jsonl",
            "metrics": {"total": 24, "overall_score": 1.0},
            "failure_count": 0,
            "results": [],
        }

    monkeypatch.setattr(api, "run_quality_eval", fake_report)
    monkeypatch.setattr(api, "load_eval_report", fake_report)
    run = api.eval_run()
    report = api.eval_report()
    assert run["status"] == "ok"
    assert run["metrics"]["total"] == 24
    assert "overall_score" in run["metrics"]
    assert report["failure_count"] == 0


def test_feedback_and_recent_events() -> None:
    payload = _chat("忘记密码怎么找回？", "test_api_feedback")
    feedback = api.feedback(FeedbackRequest(trace_id=payload.trace_id, session_id=payload.session_id, rating="up"))
    events = api.events_recent(limit=20)
    metrics = api.metrics()
    assert feedback["status"] == "ok"
    assert any(event["stage"] == "feedback.received" for event in events["events"])
    assert metrics["feedback_count"] >= 1


def test_negative_feedback_records_knowledge_gap() -> None:
    payload = _chat("专业版和企业版有什么区别？", "test_api_gap_feedback")
    feedback = api.feedback(
        FeedbackRequest(
            trace_id=payload.trace_id,
            session_id=payload.session_id,
            rating="down",
            comment="价格说明还不够清楚",
        )
    )
    gaps = api.knowledge_gaps(limit=20)
    assert feedback["status"] == "ok"
    assert any(gap["reason"] == "negative_feedback" for gap in gaps["gaps"])


def test_knowledge_gap_can_generate_eval_case() -> None:
    token = uuid4().hex[:8]
    payload = _chat("专业版和企业版有什么区别？", f"test_api_gap_eval_{token}")
    comment = f"这个价格解释还是不清楚，请联系 13812345678，case {token}"
    api.feedback(
        FeedbackRequest(
            trace_id=payload.trace_id,
            session_id=payload.session_id,
            rating="down",
            comment=comment,
        )
    )
    gaps = api.knowledge_gaps(limit=100)["gaps"]
    gap = next(item for item in gaps if token in str(item.get("last_message") or item.get("message")))
    case = api.create_gap_eval_case(gap["gap_id"])
    generated = api.generated_eval_cases(limit=100)
    assert case["source_gap_id"] == gap["gap_id"]
    assert case["status"] == "draft"
    assert case["review_required"] is True
    assert "13812345678" not in str(case)
    assert any(item["source_gap_id"] == gap["gap_id"] for item in generated["cases"])


def test_handoff_records_and_updates_knowledge_gap() -> None:
    payload = _chat("帮我预测明天股票走势。", "test_api_gap_handoff")
    gaps = api.knowledge_gaps(limit=50)
    matching = [gap for gap in gaps["gaps"] if payload.trace_id in gap.get("trace_ids", [])]
    assert payload.route == "human_handoff"
    assert matching
    update = api.patch_knowledge_gap(
        matching[0]["gap_id"],
        KnowledgeGapUpdateRequest(status="reviewing", note="需要确认是否扩展服务范围"),
    )
    stats = api.knowledge_gaps_stats()
    assert update["status"] == "reviewing"
    assert stats["total"] >= 1


def test_ticket_status_can_be_updated() -> None:
    response = _chat("我要投诉，重复扣费没人处理。", "test_api_ticket_update")
    update = api.patch_ticket(
        response.ticket_id,
        TicketUpdateRequest(status="in_progress", assignee="qa-agent", note="开始跟进"),
    )
    stats = api.tickets_stats()
    assert update["status"] == "in_progress"
    assert update["assignee"] == "qa-agent"
    assert stats["in_progress"] >= 1
    assert "overdue" in stats


def test_kb_admin_can_create_and_rebuild_document() -> None:
    created_source_id = ""
    try:
        create = api.create_kb_doc(
            KBDocumentCreateRequest(
                title="专项测试知识",
                collection="faq",
                source_id="test_runtime_kb_admin",
                content="专项测试知识用于验证知识库运营 API。用户询问专项测试时，应回答来自新增知识库文档。",
            )
        )
        created_source_id = create["source_id"]
        docs = api.kb_docs()
        rebuild = api.kb_rebuild()
        clear_index_cache()
        results = search_kb("专项测试知识")
        assert created_source_id.startswith("test_runtime_kb_admin")
        assert any(doc["title"] == "专项测试知识" for doc in docs["documents"])
        assert rebuild["doc_count"] >= 10
        assert any(item["title"] == "专项测试知识" for item in results)
    finally:
        for path in KB_DIR.glob("test_runtime_kb_admin*.md"):
            path.unlink(missing_ok=True)
        build_kb_index()
        clear_index_cache()


def test_kb_search_endpoint_returns_debug_results() -> None:
    payload = api.kb_search_debug(q="退款多久到账？", collection="policy", k=3)
    assert payload["query"] == "退款多久到账？"
    assert payload["collection"] == "policy"
    assert payload["k"] == 3
    assert payload["results"]
    assert all(item["collection"] == "policy" for item in payload["results"])
    assert payload["results"][0]["score"] >= 0
    assert payload["results"][0]["content"]


def test_kb_search_endpoint_rejects_invalid_input() -> None:
    with pytest.raises(Exception):
        api.kb_search_debug(q="   ")
    with pytest.raises(Exception):
        api.kb_search_debug(q="退款", collection="unknown")
