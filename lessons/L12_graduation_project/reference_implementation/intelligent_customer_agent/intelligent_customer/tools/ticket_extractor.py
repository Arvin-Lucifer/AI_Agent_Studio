from __future__ import annotations

import re
from typing import Any


ISSUE_KEYWORDS: list[tuple[str, list[str]]] = [
    ("refund", ["退款", "退费", "退货", "换货"]),
    ("payment", ["支付", "扣款", "重复扣费", "已扣款", "未支付", "对公转账"]),
    ("invoice", ["发票", "抬头", "税号"]),
    ("login", ["登录", "密码", "验证码", "账号锁定"]),
    ("account", ["账号", "注册", "删除账号", "隐私", "数据"]),
    ("product", ["套餐", "价格", "企业版", "专业版", "免费版", "sla"]),
    ("technical", ["失败", "异常", "故障", "打不开", "无法使用", "同步"]),
    ("complaint", ["投诉", "态度差", "没人处理", "不满意", "维权"]),
]

CRITICAL_WORDS = ["监管", "维权", "起诉", "投诉平台", "业务中断", "无法使用", "紧急", "严重"]
HIGH_WORDS = ["投诉", "赔偿", "重复扣费", "已扣款", "没人处理", "态度差", "生气"]


def _mask_phone(phone: str) -> str:
    return f"{phone[:3]}****{phone[-4:]}"


def _mask_email(email: str) -> str:
    name, domain = email.split("@", 1)
    if len(name) <= 2:
        masked = f"{name[0]}***"
    else:
        masked = f"{name[:2]}***{name[-1]}"
    return f"{masked}@{domain}"


def extract_ticket_fields(message: str, is_complaint: bool = False) -> dict[str, Any]:
    text = message.strip()
    lowered = text.lower()
    order_match = re.search(r"(?:订单号?|order[_\-\s]?id[:：]?)\s*([A-Za-z0-9][A-Za-z0-9_\-]{5,32})", text, re.I)
    loose_order_match = re.search(r"\b([A-Z]{1,4}\d{6,20})\b", text)
    phone_match = re.search(r"(?<!\d)(1[3-9]\d{9})(?!\d)", text)
    email_match = re.search(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}", text)

    issue_type = "complaint" if is_complaint else "general"
    for candidate, keywords in ISSUE_KEYWORDS:
        if any(keyword.lower() in lowered for keyword in keywords):
            issue_type = candidate
            break

    urgency = "normal"
    if any(word.lower() in lowered for word in CRITICAL_WORDS):
        urgency = "critical"
    elif is_complaint or any(word.lower() in lowered for word in HIGH_WORDS):
        urgency = "high"

    priority = {"critical": "critical", "high": "high", "normal": "normal"}[urgency]
    sla_hours = {"critical": 2, "high": 4, "normal": 24}[urgency]

    contact_masked = None
    contact_type = None
    if phone_match:
        contact_masked = _mask_phone(phone_match.group(1))
        contact_type = "phone"
    elif email_match:
        contact_masked = _mask_email(email_match.group(0))
        contact_type = "email"

    return {
        "issue_type": issue_type,
        "urgency": urgency,
        "priority": priority,
        "sla_hours": sla_hours,
        "order_id": (order_match.group(1) if order_match else (loose_order_match.group(1) if loose_order_match else None)),
        "contact_masked": contact_masked,
        "contact_type": contact_type,
        "extracted_fields": {
            "has_order_id": bool(order_match or loose_order_match),
            "has_contact": bool(contact_masked),
        },
    }
