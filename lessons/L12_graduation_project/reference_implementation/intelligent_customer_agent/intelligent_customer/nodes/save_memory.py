from __future__ import annotations

import time

from intelligent_customer.harness.observability import log_event, record_chat_metrics
from intelligent_customer.harness.state import AgentState
from intelligent_customer.tools.memory_tool import save_memory


def save_memory_node(state: AgentState) -> AgentState:
    latency_ms = round((time.perf_counter() - float(state.get("started_at", time.perf_counter()))) * 1000, 2)
    metadata = {
        "trace_id": state["trace_id"],
        "intent": state.get("intent"),
        "route": state.get("route"),
        "confidence": state.get("confidence", 0.0),
        "ticket_id": state.get("ticket_id"),
        "need_human": state.get("need_human", False),
        "citations": state.get("citations", []),
        "evidence_count": state.get("evidence_count", 0),
        "answer_mode": state.get("metadata", {}).get("answer_mode", "extractive"),
        "contextual_query": state.get("metadata", {}).get("contextual_query"),
        "query_rewritten": state.get("metadata", {}).get("query_rewritten", False),
        "context_terms": state.get("metadata", {}).get("context_terms", []),
        "suggested_actions": state.get("metadata", {}).get("suggested_actions", []),
        "latency_ms": latency_ms,
    }
    save_memory(state["session_id"], state["message"], state.get("answer", ""), metadata)
    log_event(
        state["trace_id"],
        state["session_id"],
        "memory.saved",
        route=state.get("route"),
        latency_ms=latency_ms,
    )
    record_chat_metrics(
        intent=str(state.get("intent", "out_of_scope")),
        route=str(state.get("route", "human_handoff")),
        latency_ms=latency_ms,
        ticket_id=state.get("ticket_id"),
    )
    log_event(
        state["trace_id"],
        state["session_id"],
        "chat.response",
        intent=state.get("intent"),
        route=state.get("route"),
        confidence=state.get("confidence", 0.0),
        ticket_id=state.get("ticket_id"),
        need_human=state.get("need_human", False),
    )
    return {"latency_ms": latency_ms}
