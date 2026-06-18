from __future__ import annotations

from intelligent_customer.tools.handoff_tool import build_handoff_summary


def test_build_handoff_summary_includes_context_and_masks_pii() -> None:
    summary = build_handoff_summary(
        message="我要投诉，手机号 13812345678。",
        history=[{"role": "user", "content": "之前订单重复扣费"}, {"role": "assistant", "content": "请补充订单号"}],
        intent="complaint",
        route="ticket",
        confidence=0.8,
        retrieved_docs=[{"source_id": "faq_01", "title": "订单说明", "score": 0.7}],
        missing_fields=["order_id"],
        extracted_fields=["contact"],
        reason="customer_complaint",
    )
    assert "13812345678" not in str(summary)
    assert "138****5678" in summary["summary"]
    assert summary["recent_turns"]
    assert summary["evidence"][0]["source_id"] == "faq_01"
    assert "向用户确认订单号" in summary["next_steps"]
