from __future__ import annotations

from intelligent_customer.harness.observability import log_event
from intelligent_customer.harness.state import AgentState
from intelligent_customer.tools.context_tool import suggest_next_actions
from intelligent_customer.tools.handoff_tool import build_handoff_summary
from intelligent_customer.tools.knowledge_gap_tool import record_knowledge_gap
from intelligent_customer.tools.ticket_extractor import extract_ticket_fields
from intelligent_customer.tools.ticket_tool import create_ticket


def create_ticket_node(state: AgentState) -> AgentState:
    is_complaint = state.get("intent") == "complaint"
    extracted = extract_ticket_fields(state["message"], is_complaint=is_complaint)
    reason = "customer_complaint" if is_complaint else state.get("metadata", {}).get("evaluation_reason", "needs_human")
    payload = {
        "category": "complaint" if is_complaint else "handoff",
        "priority": extracted["priority"],
        "urgency": extracted["urgency"],
        "sla_hours": extracted["sla_hours"],
        "issue_type": extracted["issue_type"],
        "order_id": extracted["order_id"],
        "contact_masked": extracted["contact_masked"],
        "contact_type": extracted["contact_type"],
        "trace_id": state["trace_id"],
        "session_id": state["session_id"],
        "user_id": state.get("user_id"),
        "message": state["message"],
        "reason": reason,
        "metadata": {
            "intent": state.get("intent"),
            "route": state.get("route"),
            "confidence": state.get("confidence", 0.0),
            "evidence_count": state.get("evidence_count", 0),
            "extracted_fields": extracted["extracted_fields"],
        },
    }
    missing_fields = []
    if not extracted["order_id"]:
        missing_fields.append("order_id")
    if not extracted["contact_masked"]:
        missing_fields.append("contact")
    payload["metadata"]["missing_fields"] = missing_fields
    payload["metadata"]["handoff"] = build_handoff_summary(
        message=state["message"],
        history=state.get("history", []),
        intent=str(state.get("intent")),
        route=str(state.get("route")),
        confidence=float(state.get("confidence", 0.0)),
        retrieved_docs=state.get("retrieved_docs", []),
        missing_fields=missing_fields,
        extracted_fields=extracted["extracted_fields"],
        reason=reason,
    )
    ticket = create_ticket(payload)
    gap_id = None
    if not is_complaint:
        gap = record_knowledge_gap(
            {
                "trace_id": state["trace_id"],
                "session_id": state["session_id"],
                "message": state["message"],
                "reason": payload["reason"],
                "intent": state.get("intent"),
                "route": "human_handoff",
                "confidence": state.get("confidence", 0.0),
                "priority": "normal",
                "metadata": {"ticket_id": ticket["ticket_id"]},
            }
        )
        gap_id = gap.get("gap_id")
    reply = (
        f"已为您创建投诉工单 {ticket['ticket_id']}，客服会优先跟进。"
        if is_complaint
        else f"这个问题目前没有足够的知识库证据直接回答，已为您创建人工处理单 {ticket['ticket_id']}。"
    )
    if missing_fields:
        human_fields = "、".join(["订单号" if item == "order_id" else "联系方式" for item in missing_fields])
        reply += f" 为了更快处理，您可以继续补充{human_fields}。"
    log_event(
        state["trace_id"],
        state["session_id"],
        "ticket.created",
        ticket_id=ticket["ticket_id"],
        category=ticket["category"],
        priority=ticket["priority"],
        urgency=ticket["urgency"],
        issue_type=ticket["issue_type"],
        has_order_id=bool(ticket.get("order_id")),
        has_contact=bool(ticket.get("contact_masked")),
        knowledge_gap_id=gap_id,
    )
    return {
        "route": "ticket" if is_complaint else "human_handoff",
        "answer": reply,
        "ticket_id": ticket["ticket_id"],
        "ticket_payload": ticket,
        "need_human": True,
        "citations": [],
        "confidence": max(float(state.get("confidence", 0.0)), 0.1),
        "metadata": {
            **state.get("metadata", {}),
            "suggested_actions": suggest_next_actions(
                state["message"],
                "ticket" if is_complaint else "human_handoff",
                need_human=True,
                ticket_id=ticket["ticket_id"],
            ),
        },
    }
