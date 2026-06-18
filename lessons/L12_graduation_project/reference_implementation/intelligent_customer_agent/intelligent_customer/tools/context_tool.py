from __future__ import annotations

from typing import Any

from intelligent_customer.rag.query_normalizer import expand_query


TOPIC_TERMS = [
    "账号",
    "注册",
    "登录",
    "密码",
    "验证码",
    "订单",
    "发票",
    "支付",
    "扣款",
    "退款",
    "对公转账",
    "套餐",
    "价格",
    "企业版",
    "专业版",
    "免费版",
    "sla",
    "售后",
    "隐私",
    "删除账号",
    "权限",
    "报表",
    "自动化",
    "故障",
    "失败",
]

FOLLOWUP_MARKERS = ["那", "那么", "还有", "另外", "继续", "刚才", "上面", "之前", "呢", "这个", "那个", "对比"]


def _dedupe(items: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        key = item.lower()
        if key in seen:
            continue
        seen.add(key)
        result.append(item)
    return result


def extract_topic_terms(text: str) -> list[str]:
    lowered = expand_query(text).lower()
    return [term for term in TOPIC_TERMS if term.lower() in lowered]


def _history_terms(history: list[dict[str, Any]]) -> list[str]:
    terms: list[str] = []
    for item in reversed(history[-8:]):
        if item.get("role") == "user":
            terms.extend(extract_topic_terms(str(item.get("content", ""))))
        metadata = item.get("metadata") or {}
        for citation in metadata.get("citations", [])[:2]:
            terms.extend(extract_topic_terms(str(citation.get("title", ""))))
    return _dedupe(terms)


def rewrite_contextual_query(message: str, history: list[dict[str, Any]], memory_summary: str = "") -> dict[str, Any]:
    current = message.strip()
    current_terms = extract_topic_terms(current)
    prior_terms = _history_terms(history) or extract_topic_terms(memory_summary)
    is_followup = bool(history) and (
        len(current) <= 16
        or any(marker in current for marker in FOLLOWUP_MARKERS)
        or (len(current_terms) <= 1 and len(current) <= 24)
    )
    if not is_followup or not prior_terms:
        return {
            "query": message,
            "rewritten": False,
            "context_terms": [],
        }

    context_terms = [term for term in prior_terms if term.lower() not in {item.lower() for item in current_terms}][:5]
    if not context_terms:
        return {
            "query": message,
            "rewritten": False,
            "context_terms": [],
        }
    return {
        "query": f"{' '.join(context_terms)} {message}",
        "rewritten": True,
        "context_terms": context_terms,
    }


def suggest_next_actions(message: str, route: str, need_human: bool = False, ticket_id: str | None = None) -> list[str]:
    text = expand_query(message).lower()
    if ticket_id or need_human or route in {"ticket", "human_handoff"}:
        return ["补充订单号", "补充联系方式", "查看工单状态"]
    if any(term in text for term in ["退款", "订单", "发票", "支付", "扣款", "对公转账"]):
        return ["查询订单状态", "申请发票", "补充订单号"]
    if any(term in text for term in ["登录", "密码", "验证码", "账号"]):
        return ["收不到验证码怎么办？", "忘记密码怎么找回？", "联系人工"]
    if any(term in text for term in ["套餐", "价格", "企业版", "专业版", "免费版", "sla"]):
        return ["比较专业版和企业版", "了解企业版 SLA", "申请开通企业版"]
    if any(term in text for term in ["隐私", "数据", "删除账号"]):
        return ["导出个人数据", "删除账号流程", "联系人工"]
    if route == "clarify":
        return ["账号登录问题", "订单支付问题", "套餐价格咨询"]
    return ["继续追问", "转人工处理", "查看相关政策"]
