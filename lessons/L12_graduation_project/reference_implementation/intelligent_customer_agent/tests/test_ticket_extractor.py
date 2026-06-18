from __future__ import annotations

from intelligent_customer.tools.ticket_extractor import extract_ticket_fields
from intelligent_customer.tools.ticket_tool import create_ticket, ticket_stats


def test_extract_ticket_fields_masks_contact_and_order() -> None:
    fields = extract_ticket_fields("订单号 ORD202606050001 重复扣费，请联系 13812345678，我要投诉。", is_complaint=True)
    assert fields["order_id"] == "ORD202606050001"
    assert fields["contact_masked"] == "138****5678"
    assert fields["contact_type"] == "phone"
    assert fields["issue_type"] == "payment"
    assert fields["priority"] == "high"
    assert fields["sla_hours"] == 4


def test_extract_critical_urgency() -> None:
    fields = extract_ticket_fields("系统业务中断，企业版完全无法使用，订单 ABCD202606050001", is_complaint=False)
    assert fields["urgency"] == "critical"
    assert fields["priority"] == "critical"
    assert fields["sla_hours"] == 2


def test_ticket_sla_state_is_calculated() -> None:
    ticket = create_ticket(
        {
            "category": "handoff",
            "priority": "critical",
            "urgency": "critical",
            "sla_hours": -1,
            "session_id": "test_ticket_sla",
            "trace_id": "trace_test_ticket_sla",
            "message": "SLA 测试工单",
        }
    )
    stats = ticket_stats()
    assert ticket["due_at"]
    assert ticket["overdue"] is True
    assert stats["overdue"] >= 1
