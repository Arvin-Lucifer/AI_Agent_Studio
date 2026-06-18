from __future__ import annotations

import re
from typing import Any

from intelligent_customer.harness.observability import log_event
from intelligent_customer.harness.state import AgentState
from intelligent_customer.tools.context_tool import suggest_next_actions
from intelligent_customer.tools.ticket_tool import find_latest_ticket, find_ticket


TICKET_ID_RE = re.compile(r"\b[TH]-\d{14}-[0-9a-fA-F]{6}\b")
STATUS_TERMS = ["工单", "处理单", "查看工单", "查询工单", "工单状态", "工单进度", "处理单状态", "处理单进度"]
FOLLOWUP_STATUS_TERMS = ["处理到哪", "处理了吗", "有进展吗"]

STATUS_LABELS = {
    "open": "待处理",
    "in_progress": "处理中",
    "resolved": "已解决",
    "closed": "已关闭",
}


def _is_status_question(message: str) -> bool:
    compact = message.lower()
    if TICKET_ID_RE.search(message):
        return True
    if any(term in compact for term in STATUS_TERMS):
        return True
    return any(term in compact for term in FOLLOWUP_STATUS_TERMS) and "订单状态" not in compact


def _ticket_sla_line(ticket: dict[str, Any]) -> str:
    status = ticket.get("status")
    if status not in {"open", "in_progress"}:
        return "当前工单已经结束，不再计算 SLA 倒计时。"
    if ticket.get("overdue"):
        return "该工单已经超过 SLA，请在 Dashboard 中优先处理。"
    minutes = ticket.get("minutes_to_due")
    if minutes is None:
        return "当前没有可用的 SLA 倒计时。"
    if minutes >= 60:
        return f"SLA 预计还剩约 {round(float(minutes) / 60, 1)} 小时。"
    return f"SLA 预计还剩约 {minutes} 分钟。"


def _compose_ticket_status(ticket: dict[str, Any]) -> str:
    status = str(ticket.get("status", "open"))
    label = STATUS_LABELS.get(status, status)
    parts = [
        f"我查到当前工单 {ticket['ticket_id']} 的状态是：{label}。",
        f"优先级：{ticket.get('priority', 'normal')}；问题类型：{ticket.get('issue_type', 'general')}。",
        _ticket_sla_line(ticket),
    ]
    if ticket.get("order_id"):
        parts.append(f"已记录订单号：{ticket['order_id']}。")
    if ticket.get("contact_masked"):
        parts.append(f"已记录联系方式：{ticket['contact_masked']}。")
    if ticket.get("assignee"):
        parts.append(f"当前负责人：{ticket['assignee']}。")
    missing = (ticket.get("metadata") or {}).get("missing_fields") or []
    if missing:
        human_fields = "、".join(["订单号" if item == "order_id" else "联系方式" for item in missing])
        parts.append(f"还可以继续补充{human_fields}，有助于客服更快处理。")
    return "\n".join(parts)


def maybe_ticket_status_node(state: AgentState) -> AgentState:
    if not _is_status_question(state["message"]):
        return {"ticket_status_checked": False}

    match = TICKET_ID_RE.search(state["message"])
    ticket = find_ticket(match.group(0)) if match else find_latest_ticket(state["session_id"])
    if not ticket:
        answer = "我还没有在当前会话中找到工单。请提供工单号，或先描述问题，我可以帮您创建工单。"
        log_event(state["trace_id"], state["session_id"], "ticket.status_lookup", found=False)
        return {
            "ticket_status_checked": True,
            "intent": "consult",
            "route": "clarify",
            "answer": answer,
            "need_human": False,
            "need_clarification": True,
            "confidence": 0.6,
            "citations": [],
            "metadata": {
                **state.get("metadata", {}),
                "ticket_status_lookup": True,
                "suggested_actions": ["提供工单号", "描述投诉问题", "转人工处理"],
            },
        }

    log_event(
        state["trace_id"],
        state["session_id"],
        "ticket.status_lookup",
        found=True,
        ticket_id=ticket["ticket_id"],
        status=ticket.get("status"),
    )
    return {
        "ticket_status_checked": True,
        "intent": "consult",
        "route": "final",
        "answer": _compose_ticket_status(ticket),
        "ticket_id": ticket["ticket_id"],
        "ticket_payload": ticket,
        "need_human": ticket.get("status") in {"open", "in_progress"},
        "confidence": 0.95,
        "citations": [],
        "metadata": {
            **state.get("metadata", {}),
            "ticket_status_lookup": True,
            "ticket_status": ticket.get("status"),
            "suggested_actions": suggest_next_actions(
                state["message"],
                "ticket",
                need_human=ticket.get("status") in {"open", "in_progress"},
                ticket_id=ticket["ticket_id"],
            ),
        },
    }


def ticket_status_route_key(state: AgentState) -> str:
    return "answered" if state.get("ticket_status_checked") else "continue"
