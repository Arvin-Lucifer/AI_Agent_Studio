from __future__ import annotations

from intelligent_customer.graph import run_agent
from intelligent_customer.rag.kb_builder import build_kb_index
from intelligent_customer.rag.retriever import clear_index_cache
from intelligent_customer.tools.memory_tool import reset_memory
from intelligent_customer.tools.ticket_tool import update_ticket


def setup_module() -> None:
    build_kb_index()
    clear_index_cache()


def test_qa_routes_to_retrieve() -> None:
    reset_memory("test_graph_qa")
    response = run_agent("退款需要几天到账？", session_id="test_graph_qa")
    assert response.intent == "qa"
    assert response.route == "retrieve"
    assert response.need_human is False


def test_consult_routes_to_retrieve() -> None:
    reset_memory("test_graph_consult")
    response = run_agent("专业版多少钱，适合什么团队？", session_id="test_graph_consult")
    assert response.intent == "consult"
    assert response.route == "retrieve"


def test_complaint_routes_to_ticket() -> None:
    reset_memory("test_graph_complaint")
    response = run_agent("我要投诉，你们一直没人处理。", session_id="test_graph_complaint")
    assert response.intent == "complaint"
    assert response.route == "ticket"
    assert response.ticket_id


def test_unclear_routes_to_clarify() -> None:
    reset_memory("test_graph_unclear")
    response = run_agent("这个怎么办？", session_id="test_graph_unclear")
    assert response.intent == "unclear"
    assert response.route == "clarify"
    assert "补充" in response.reply


def test_out_of_scope_routes_to_human_handoff() -> None:
    reset_memory("test_graph_oos")
    response = run_agent("帮我预测明天股票走势。", session_id="test_graph_oos")
    assert response.intent == "out_of_scope"
    assert response.route == "human_handoff"
    assert response.need_human is True
    assert response.ticket_id


def test_contextual_followup_reuses_previous_topic() -> None:
    session_id = "test_graph_contextual_followup"
    reset_memory(session_id)
    first = run_agent("专业版和企业版有什么区别？", session_id=session_id)
    second = run_agent("那 SLA 呢？", session_id=session_id)
    assert first.route == "retrieve"
    assert second.intent == "consult"
    assert second.route == "retrieve"
    assert second.metadata["query_rewritten"] is True
    assert "SLA" in second.reply or "99.9%" in second.reply
    assert "了解企业版 SLA" in second.metadata["suggested_actions"]


def test_colloquial_refund_question_uses_policy_rag() -> None:
    reset_memory("test_graph_colloquial_refund")
    response = run_agent("钱什么时候能退回来？", session_id="test_graph_colloquial_refund")
    assert response.intent == "qa"
    assert response.route == "retrieve"
    assert response.need_human is False
    assert any(citation.source_id == "policy_01" for citation in response.citations)
    assert "3 到 7 个工作日" in response.reply


def test_colloquial_sms_code_question_uses_troubleshooting_rag() -> None:
    reset_memory("test_graph_colloquial_sms_code")
    response = run_agent("短信码一直收不到", session_id="test_graph_colloquial_sms_code")
    assert response.intent == "qa"
    assert response.route == "retrieve"
    assert response.need_human is False
    assert any(citation.source_id == "troubleshoot_01" for citation in response.citations)
    assert "10 分钟" in response.reply


def test_colloquial_invoice_title_question_uses_faq_rag() -> None:
    reset_memory("test_graph_colloquial_invoice")
    response = run_agent("开票抬头填错了怎么改？", session_id="test_graph_colloquial_invoice")
    assert response.intent == "qa"
    assert response.route == "retrieve"
    assert response.need_human is False
    assert any(citation.source_id == "faq_02" for citation in response.citations)
    assert "30 天" in response.reply


def test_answer_prioritizes_relevant_sentences_within_retrieved_docs() -> None:
    reset_memory("test_graph_relevant_sentence_order")
    response = run_agent("团队成员看不到报表怎么办？", session_id="test_graph_relevant_sentence_order")
    assert response.intent == "qa"
    assert response.route == "retrieve"
    assert "报表导出和细粒度权限管理" in response.reply
    assert "重新登录" in response.reply
    assert response.reply.find("报表导出和细粒度权限管理") < response.reply.find("完成支付后")


def test_ticket_status_lookup_uses_current_session_ticket() -> None:
    session_id = "test_graph_ticket_status"
    reset_memory(session_id)
    first = run_agent("我要投诉，重复扣费一直没人处理。", session_id=session_id)
    assert first.ticket_id
    update_ticket(first.ticket_id, "in_progress", assignee="ops-unit", note="已联系用户")
    second = run_agent("查看工单状态", session_id=session_id)
    assert second.route == "final"
    assert second.ticket_id == first.ticket_id
    assert second.metadata["ticket_status_lookup"] is True
    assert "处理中" in second.reply
    assert "ops-unit" in second.reply


def test_ticket_status_lookup_accepts_explicit_ticket_id() -> None:
    session_id = "test_graph_ticket_status_by_id"
    reset_memory(session_id)
    first = run_agent("我要投诉，客服态度差。", session_id=session_id)
    assert first.ticket_id
    second = run_agent(f"帮我查一下 {first.ticket_id} 的进度", session_id="another_session_for_ticket_status")
    assert second.route == "final"
    assert second.ticket_id == first.ticket_id
    assert "状态" in second.reply
