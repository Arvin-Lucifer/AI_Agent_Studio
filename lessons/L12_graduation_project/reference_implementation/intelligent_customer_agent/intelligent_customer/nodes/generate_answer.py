from __future__ import annotations

import re

from intelligent_customer.harness.observability import log_event
from intelligent_customer.harness.privacy import mask_sensitive_text
from intelligent_customer.harness.state import AgentState
from intelligent_customer.llm import generate_grounded_answer
from intelligent_customer.rag.query_normalizer import expand_query
from intelligent_customer.rag.kb_builder import tokenize
from intelligent_customer.tools.context_tool import suggest_next_actions


EXPLICIT_TERMS = [
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
    "隐私",
    "删除账号",
    "权限",
    "报表",
    "自动化",
    "故障",
    "失败",
]


def _citation_from_doc(doc: dict) -> dict:
    snippet = str(doc.get("content", "")).strip()
    return {
        "source_id": doc["source_id"],
        "title": doc["title"],
        "collection": doc["collection"],
        "score": float(doc["score"]),
        "snippet": mask_sensitive_text(snippet[:220]) if snippet else None,
    }


def _has_explicit_match(message: str, doc: dict) -> bool:
    compact = expand_query(message).strip().lower()
    doc_text = f"{doc.get('title', '')}\n{doc.get('content', '')}".lower()
    return any(term.lower() in compact and term.lower() in doc_text for term in EXPLICIT_TERMS)


def _supporting_docs(message: str, docs: list[dict]) -> list[dict]:
    explicit = [doc for doc in docs if _has_explicit_match(message, doc)]
    if explicit:
        return explicit[:3]
    return docs[:3]


def _with_sentence_punctuation(text: str) -> str:
    cleaned = text.strip(" \n\t-。；;")
    if not cleaned:
        return cleaned
    if cleaned[-1] in "。！？":
        return cleaned
    return f"{cleaned}。"


def _sentence_score(message: str, sentence: str, doc: dict) -> float:
    expanded = expand_query(message).lower()
    sentence_lower = sentence.lower()
    query_terms = {term for term in tokenize(expanded) if len(term) >= 2}
    explicit_terms = {term.lower() for term in EXPLICIT_TERMS if term.lower() in expanded}
    score = 0.0
    matched_explicit = 0
    for term in query_terms:
        if term in sentence_lower:
            score += 0.7 if len(term) <= 2 else 1.0
    for term in explicit_terms:
        if term in sentence_lower:
            matched_explicit += 1
            score += 2.2
    if any(term in expanded for term in ["退款", "退回", "到账", "退换货"]) and any(
        term in sentence_lower for term in ["3 到 7", "工作日", "原路退回"]
    ):
        score += 4.0
    if any(term in expanded for term in ["验证码", "短信码", "收不到"]) and any(
        term in sentence_lower for term in ["10 分钟", "安全限制", "频繁请求"]
    ):
        score += 9.0
    if "发票" in expanded and any(term in sentence_lower for term in ["30 天", "发票抬头"]):
        score += 3.0
    if "sla" in expanded and any(term in sentence_lower for term in ["99.9", "4 小时"]):
        score += 3.0
    if matched_explicit >= 2:
        score += 1.0
    title = str(doc.get("title", "")).lower()
    if title and any(term in title for term in query_terms):
        score += 0.4
    score += float(doc.get("score", 0.0)) * 0.25
    return score


def _sentences_from_docs(message: str, docs: list[dict]) -> list[str]:
    candidates: list[tuple[float, int, int, str]] = []
    fallback: list[str] = []
    seen: set[str] = set()
    for doc_idx, doc in enumerate(docs[:3]):
        content = str(doc.get("content", "")).strip()
        parts = re.split(r"(?<=[。！？；])\s*", content)
        for sentence_idx, part in enumerate(parts):
            text = part.strip(" \n\t-。；;")
            if not text:
                continue
            if len(text) < 8:
                continue
            if text in seen:
                continue
            seen.add(text)
            fallback.append(text)
            score = _sentence_score(message, text, doc)
            candidates.append((score, doc_idx, sentence_idx, text))
    if not candidates:
        return []
    if max(score for score, _, _, _ in candidates) <= 0:
        return fallback[:5]
    candidates.sort(key=lambda item: (-item[0], item[1], item[2]))
    return [text for _, _, _, text in candidates[:5]]


def _answer_prefix(message: str, docs: list[dict]) -> str:
    text = expand_query(message).lower()
    top_collection = str(docs[0].get("collection", "")) if docs else ""
    if any(word in text for word in ["退款", "退费", "退货"]):
        return "可以，我查到的退款处理规则是："
    if any(word in text for word in ["密码", "验证码", "登录"]):
        return "可以，账号登录相关的处理方式是："
    if any(word in text for word in ["发票", "订单", "支付", "扣款", "对公转账"]):
        return "可以，订单和支付相关信息如下："
    if any(word in text for word in ["套餐", "价格", "企业版", "专业版", "免费版", "sla"]):
        return "从当前产品资料看："
    if top_collection == "troubleshoot":
        return "可以，建议按下面步骤排查："
    if top_collection == "policy":
        return "我查到的政策说明是："
    return "我查到的知识库信息如下："


def _followup_hint(message: str) -> str:
    text = expand_query(message).lower()
    if any(word in text for word in ["退款", "订单", "发票", "支付", "扣款", "对公转账"]):
        return "如果需要继续处理，请准备订单号、付款凭证或发票信息。"
    if any(word in text for word in ["登录", "密码", "验证码", "账号"]):
        return "如果仍无法处理，请提供账号、手机号后四位或错误截图，方便人工核验。"
    if any(word in text for word in ["套餐", "价格", "企业版", "专业版"]):
        return "如果要进一步报价，可以补充团队人数、调用量和部署方式。"
    return "如果需要继续定位，请补充账号、订单号、截图或具体操作路径。"


def _compose_extractive_answer(message: str, docs: list[dict]) -> str:
    sentences = _sentences_from_docs(message, docs)
    if not sentences:
        return "我查到了相关资料，但片段不够完整。为避免误导，建议补充更多背景后继续确认。"
    bullet_lines = "\n".join([f"{idx}. {_with_sentence_punctuation(sentence)}" for idx, sentence in enumerate(sentences[:4], start=1)])
    titles = "、".join([f"《{doc['title']}》" for doc in docs[:2]])
    return f"{_answer_prefix(message, docs)}\n{bullet_lines}\n\n依据来源：{titles}。\n{_followup_hint(message)}"


def generate_answer_node(state: AgentState) -> AgentState:
    raw_docs = state.get("retrieved_docs", [])
    support_query = state.get("contextual_query") or state["message"]
    docs = _supporting_docs(support_query, raw_docs)
    answer_mode = "extractive"
    if not docs:
        answer = "我没有在当前知识库中找到足够证据。为避免误导，我会为您转人工处理。"
        citations: list[dict] = []
    else:
        llm_answer = generate_grounded_answer(
            message=state["message"],
            evidence=docs,
            memory_summary=state.get("memory_summary", ""),
        )
        if llm_answer:
            answer = llm_answer
            answer_mode = "llm_grounded"
        else:
            answer = _compose_extractive_answer(state["message"], docs)
        citations = [_citation_from_doc(doc) for doc in docs[:3]]
    suggestions = suggest_next_actions(support_query, route=str(state.get("route", "retrieve")))
    log_event(
        state["trace_id"],
        state["session_id"],
        "answer.generated",
        evidence_count=len(docs),
        citation_count=len(citations),
        answer_mode=answer_mode,
        suggested_actions=suggestions,
    )
    return {
        "answer": answer,
        "citations": citations,
        "metadata": {**state.get("metadata", {}), "answer_mode": answer_mode, "suggested_actions": suggestions},
    }
