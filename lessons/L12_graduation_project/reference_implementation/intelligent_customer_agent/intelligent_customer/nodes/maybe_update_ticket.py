from __future__ import annotations

from intelligent_customer.harness.observability import log_event
from intelligent_customer.harness.state import AgentState
from intelligent_customer.tools.context_tool import suggest_next_actions
from intelligent_customer.tools.ticket_extractor import extract_ticket_fields
from intelligent_customer.tools.ticket_tool import find_latest_active_ticket, update_ticket_details


def maybe_update_ticket_node(state: AgentState) -> AgentState:
    ticket = find_latest_active_ticket(state["session_id"])
    if not ticket:
        return {"ticket_updated": False}

    extracted = extract_ticket_fields(state["message"], is_complaint=ticket.get("category") == "complaint")
    if not extracted.get("order_id") and not extracted.get("contact_masked"):
        return {"ticket_updated": False}

    updates = {}
    if extracted.get("order_id") and not ticket.get("order_id"):
        updates["order_id"] = extracted["order_id"]
    if extracted.get("contact_masked") and not ticket.get("contact_masked"):
        updates["contact_masked"] = extracted["contact_masked"]
        updates["contact_type"] = extracted["contact_type"]
    if extracted.get("issue_type") and ticket.get("issue_type") in {None, "general", "complaint"}:
        updates["issue_type"] = extracted["issue_type"]
    if extracted.get("priority") in {"high", "critical"} and ticket.get("priority") != extracted["priority"]:
        updates["priority"] = extracted["priority"]
        updates["urgency"] = extracted["urgency"]
        updates["sla_hours"] = extracted["sla_hours"]

    if not updates:
        return {"ticket_updated": False}

    updated = update_ticket_details(
        ticket["ticket_id"],
        fields=updates,
        note=f"用户补充信息：{state['message']}",
    )
    if not updated:
        return {"ticket_updated": False}

    parts = []
    if updated.get("order_id"):
        parts.append(f"订单号 {updated['order_id']}")
    if updated.get("contact_masked"):
        parts.append(f"联系方式 {updated['contact_masked']}")
    if updated.get("issue_type"):
        parts.append(f"问题类型 {updated['issue_type']}")
    detail = "、".join(parts) or "补充信息"
    answer = f"已将{detail}补充到工单 {updated['ticket_id']}，客服会基于最新信息继续处理。"
    log_event(
        state["trace_id"],
        state["session_id"],
        "ticket.enriched",
        ticket_id=updated["ticket_id"],
        updated_fields=sorted(updates),
    )
    return {
        "ticket_updated": True,
        "intent": "consult",
        "route": "final",
        "answer": answer,
        "ticket_id": updated["ticket_id"],
        "ticket_payload": updated,
        "need_human": True,
        "confidence": 0.9,
        "citations": [],
        "metadata": {
            **state.get("metadata", {}),
            "ticket_enriched": True,
            "updated_fields": sorted(updates),
            "suggested_actions": suggest_next_actions(state["message"], "ticket", need_human=True, ticket_id=updated["ticket_id"]),
        },
    }


def ticket_update_route_key(state: AgentState) -> str:
    return "updated" if state.get("ticket_updated") else "continue"
