from __future__ import annotations

from intelligent_customer.harness.observability import audit_trace, log_event
from intelligent_customer.harness.privacy import mask_sensitive_text
from intelligent_customer.tools.ticket_tool import create_ticket, update_ticket


def test_mask_sensitive_text_masks_phone_email_and_long_numbers() -> None:
    text = "请联系 13812345678，邮箱 customer@example.com，卡号 6222026060600012345。"
    masked = mask_sensitive_text(text)
    assert "13812345678" not in masked
    assert "customer@example.com" not in masked
    assert "6222026060600012345" not in masked
    assert "138****5678" in masked
    assert "cus***@example.com" in masked


def test_log_event_masks_sensitive_fields_recursively() -> None:
    trace_id = "trace_privacy_unit"
    log_event(
        trace_id,
        "privacy_session",
        "privacy.test",
        message="手机号 13912345678",
        nested={"email": "ops@example.com", "items": ["付款号 6222026060600012345"]},
    )
    events = audit_trace(trace_id)
    assert events
    serialized = str(events[-1])
    assert "13912345678" not in serialized
    assert "ops@example.com" not in serialized
    assert "6222026060600012345" not in serialized
    assert "139****5678" in serialized


def test_ticket_message_and_notes_are_masked_but_contact_field_is_kept() -> None:
    ticket = create_ticket(
        {
            "category": "complaint",
            "priority": "high",
            "urgency": "high",
            "sla_hours": 4,
            "trace_id": "trace_privacy_ticket",
            "session_id": "privacy_ticket_session",
            "message": "订单 ORD202606060001 重复扣费，请联系 13812345678。",
            "contact_masked": "138****5678",
            "contact_type": "phone",
        }
    )
    updated = update_ticket(ticket["ticket_id"], "in_progress", note="回拨 13812345678")
    assert updated is not None
    assert "13812345678" not in ticket["message"]
    assert ticket["contact_masked"] == "138****5678"
    assert "13812345678" not in str(updated.get("notes", []))
    assert "138****5678" in str(updated.get("notes", []))
