from __future__ import annotations

import time
from uuid import uuid4

from langgraph.graph import END, START, StateGraph

from intelligent_customer.config import ensure_runtime_dirs
from intelligent_customer.harness.observability import log_event
from intelligent_customer.harness.state import AgentState
from intelligent_customer.nodes.clarify import clarify_node
from intelligent_customer.nodes.classify_intent import classify_intent_node
from intelligent_customer.nodes.create_ticket import create_ticket_node
from intelligent_customer.nodes.evaluate_answer import evaluate_answer_node, evaluation_route_key
from intelligent_customer.nodes.generate_answer import generate_answer_node
from intelligent_customer.nodes.human_handoff import human_handoff_node
from intelligent_customer.nodes.load_memory import load_memory_node
from intelligent_customer.nodes.maybe_ticket_status import maybe_ticket_status_node, ticket_status_route_key
from intelligent_customer.nodes.maybe_update_ticket import maybe_update_ticket_node, ticket_update_route_key
from intelligent_customer.nodes.retrieve_docs import retrieve_docs_node
from intelligent_customer.nodes.retrieval_router import retrieval_router_node
from intelligent_customer.nodes.route_intent import route_intent_node, route_key
from intelligent_customer.nodes.save_memory import save_memory_node
from intelligent_customer.schemas import ChatRequest, ChatResponse


def build_graph():
    workflow = StateGraph(AgentState)
    workflow.add_node("load_memory", load_memory_node)
    workflow.add_node("maybe_update_ticket", maybe_update_ticket_node)
    workflow.add_node("maybe_ticket_status", maybe_ticket_status_node)
    workflow.add_node("classify_intent", classify_intent_node)
    workflow.add_node("route_intent", route_intent_node)
    workflow.add_node("retrieval_router", retrieval_router_node)
    workflow.add_node("retrieve_docs", retrieve_docs_node)
    workflow.add_node("generate_answer", generate_answer_node)
    workflow.add_node("evaluate_answer", evaluate_answer_node)
    workflow.add_node("clarify", clarify_node)
    workflow.add_node("create_ticket", create_ticket_node)
    workflow.add_node("human_handoff", human_handoff_node)
    workflow.add_node("save_memory", save_memory_node)

    workflow.add_edge(START, "load_memory")
    workflow.add_edge("load_memory", "maybe_update_ticket")
    workflow.add_conditional_edges(
        "maybe_update_ticket",
        ticket_update_route_key,
        {
            "updated": "save_memory",
            "continue": "maybe_ticket_status",
        },
    )
    workflow.add_conditional_edges(
        "maybe_ticket_status",
        ticket_status_route_key,
        {
            "answered": "save_memory",
            "continue": "classify_intent",
        },
    )
    workflow.add_edge("classify_intent", "route_intent")
    workflow.add_conditional_edges(
        "route_intent",
        route_key,
        {
            "retrieve": "retrieval_router",
            "clarify": "clarify",
            "ticket": "create_ticket",
            "human_handoff": "human_handoff",
            "react_fallback": "human_handoff",
            "final": "save_memory",
        },
    )
    workflow.add_edge("retrieval_router", "retrieve_docs")
    workflow.add_edge("retrieve_docs", "generate_answer")
    workflow.add_edge("generate_answer", "evaluate_answer")
    workflow.add_conditional_edges(
        "evaluate_answer",
        evaluation_route_key,
        {
            "final": "save_memory",
            "clarify": "clarify",
            "human_handoff": "human_handoff",
            "ticket": "create_ticket",
        },
    )
    workflow.add_edge("clarify", "save_memory")
    workflow.add_edge("create_ticket", "save_memory")
    workflow.add_edge("human_handoff", "save_memory")
    workflow.add_edge("save_memory", END)
    return workflow.compile()


agent_graph = build_graph()


def run_agent(message: str, session_id: str = "default", user_id: str | None = None) -> ChatResponse:
    ensure_runtime_dirs()
    trace_id = f"trace_{uuid4().hex[:16]}"
    initial_state: AgentState = {
        "trace_id": trace_id,
        "session_id": session_id,
        "user_id": user_id,
        "message": message,
        "history": [],
        "memory_summary": "",
        "retrieved_docs": [],
        "evidence_count": 0,
        "confidence": 0.0,
        "answer": "",
        "citations": [],
        "need_clarification": False,
        "clarification_question": None,
        "ticket_id": None,
        "ticket_payload": None,
        "need_human": False,
        "errors": [],
        "metadata": {},
        "started_at": time.perf_counter(),
    }
    log_event(trace_id, session_id, "chat.request", message=message, user_id=user_id)
    final_state = agent_graph.invoke(initial_state)
    return ChatResponse(
        trace_id=trace_id,
        session_id=session_id,
        intent=final_state.get("intent", "out_of_scope"),
        route=final_state.get("route", "human_handoff"),
        reply=final_state.get("answer", ""),
        confidence=round(float(final_state.get("confidence", 0.0)), 4),
        citations=final_state.get("citations", []),
        ticket_id=final_state.get("ticket_id"),
        need_human=bool(final_state.get("need_human", False)),
        metadata={
            **final_state.get("metadata", {}),
            "latency_ms": final_state.get("latency_ms", 0.0),
            "evidence_count": final_state.get("evidence_count", 0),
            "need_clarification": final_state.get("need_clarification", False),
        "collections": final_state.get("collections", []),
        "contextual_query": final_state.get("metadata", {}).get("contextual_query", final_state.get("contextual_query", message)),
        "query_rewritten": final_state.get("metadata", {}).get("query_rewritten", False),
        "context_terms": final_state.get("metadata", {}).get("context_terms", []),
        "suggested_actions": final_state.get("metadata", {}).get("suggested_actions", []),
        "model": "rule-grounded-rag",
    },
    )


def invoke_agent(request: ChatRequest) -> ChatResponse:
    return run_agent(message=request.message, session_id=request.session_id, user_id=request.user_id)
