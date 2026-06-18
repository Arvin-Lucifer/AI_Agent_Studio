from __future__ import annotations

from intelligent_customer.config import TOP_K
from intelligent_customer.harness.observability import log_event
from intelligent_customer.harness.state import AgentState
from intelligent_customer.rag.query_normalizer import expand_query
from intelligent_customer.rag.router import route_collections
from intelligent_customer.tools.context_tool import rewrite_contextual_query
from intelligent_customer.tools.kb_search_tool import kb_search


EXPLICIT_QUERY_TERMS = [
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


def _should_expand_with_history(message: str) -> bool:
    compact = expand_query(message).strip().lower()
    if any(term.lower() in compact for term in EXPLICIT_QUERY_TERMS):
        return False
    return len(compact) <= 12


def _has_explicit_doc_match(message: str, doc: dict) -> bool:
    compact = expand_query(message).strip().lower()
    doc_text = f"{doc.get('title', '')}\n{doc.get('content', '')}".lower()
    return any(term.lower() in compact and term.lower() in doc_text for term in EXPLICIT_QUERY_TERMS)


def retrieval_router_node(state: AgentState) -> AgentState:
    query_info = rewrite_contextual_query(state["message"], state.get("history", []), state.get("memory_summary", ""))
    query = str(query_info["query"])
    if not query_info["rewritten"] and state.get("memory_summary") and _should_expand_with_history(query):
        query = f"{state['memory_summary']} {query}"
    collections = route_collections(query)
    log_event(
        state["trace_id"],
        state["session_id"],
        "rag.collections_routed",
        collections=collections,
        contextual_query=query,
        query_rewritten=query_info["rewritten"],
        context_terms=query_info["context_terms"],
    )
    return {
        "collections": collections,
        "contextual_query": query,
        "metadata": {
            **state.get("metadata", {}),
            "contextual_query": query,
            "query_rewritten": query_info["rewritten"],
            "context_terms": query_info["context_terms"],
        },
    }


def retrieve_docs_node(state: AgentState) -> AgentState:
    query = state.get("contextual_query") or state["message"]
    if query == state["message"] and state.get("memory_summary") and _should_expand_with_history(query):
        query = f"{state['memory_summary']} {query}"
    docs = kb_search(query=query, collections=state.get("collections"), k=TOP_K)
    confidence = 0.0
    if docs:
        top = float(docs[0].get("score", 0.0))
        avg = sum(float(item.get("score", 0.0)) for item in docs[:3]) / min(3, len(docs))
        confidence = min(1.0, round((top * 0.72) + (avg * 0.28) + min(len(docs), 3) * 0.04, 4))
        if _has_explicit_doc_match(state["message"], docs[0]):
            confidence = max(confidence, 0.34)
    log_event(
        state["trace_id"],
        state["session_id"],
        "rag.retrieved",
        collections=state.get("collections", []),
        contextual_query=query,
        evidence_count=len(docs),
        confidence=confidence,
        sources=[item.get("source_id") for item in docs],
    )
    return {
        "retrieved_docs": docs,
        "evidence_count": len(docs),
        "confidence": confidence,
    }
