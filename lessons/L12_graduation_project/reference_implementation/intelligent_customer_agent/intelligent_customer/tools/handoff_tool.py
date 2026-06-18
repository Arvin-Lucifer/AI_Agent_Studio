from __future__ import annotations

from typing import Any

from intelligent_customer.harness.privacy import mask_sensitive_text


def _clip(text: str, limit: int = 180) -> str:
    normalized = " ".join(text.split())
    if len(normalized) <= limit:
        return normalized
    return f"{normalized[: limit - 1]}…"


def build_handoff_summary(
    *,
    message: str,
    history: list[dict[str, Any]],
    intent: str | None,
    route: str | None,
    confidence: float,
    retrieved_docs: list[dict[str, Any]],
    missing_fields: list[str],
    extracted_fields: list[str],
    reason: str,
) -> dict[str, Any]:
    recent_turns = [
        {
            "role": item.get("role", "unknown"),
            "content": _clip(mask_sensitive_text(str(item.get("content", ""))), 120),
        }
        for item in history[-6:]
    ]
    evidence = [
        {
            "source_id": doc.get("source_id"),
            "title": doc.get("title"),
            "score": doc.get("score"),
        }
        for doc in retrieved_docs[:3]
    ]
    next_steps: list[str] = []
    if "order_id" in missing_fields:
        next_steps.append("向用户确认订单号")
    if "contact" in missing_fields:
        next_steps.append("向用户确认联系方式")
    if not evidence and reason != "customer_complaint":
        next_steps.append("由人工确认服务范围或补充知识库")
    if not next_steps:
        next_steps.append("按优先级联系用户并更新工单状态")

    summary_text = "；".join(
        [
            f"用户当前问题：{_clip(mask_sensitive_text(message), 160)}",
            f"意图/路由：{intent or 'unknown'} / {route or 'unknown'}",
            f"置信度：{round(float(confidence), 4)}",
            f"缺失字段：{', '.join(missing_fields) if missing_fields else '无'}",
        ]
    )
    return {
        "summary": summary_text,
        "recent_turns": recent_turns,
        "evidence": evidence,
        "missing_fields": missing_fields,
        "extracted_fields": extracted_fields,
        "next_steps": next_steps,
        "reason": reason,
    }
