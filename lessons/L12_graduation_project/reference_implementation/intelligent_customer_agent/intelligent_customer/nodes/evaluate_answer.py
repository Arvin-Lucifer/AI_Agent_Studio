from __future__ import annotations

from intelligent_customer.harness.guardrails import evaluate_answer_policy
from intelligent_customer.harness.observability import log_event
from intelligent_customer.harness.state import AgentState, NextRoute


def evaluate_answer_node(state: AgentState) -> AgentState:
    next_route, reason = evaluate_answer_policy(
        evidence_count=state.get("evidence_count", 0),
        confidence=state.get("confidence", 0.0),
        message=state["message"],
    )
    log_event(
        state["trace_id"],
        state["session_id"],
        "answer.evaluated",
        next_route=next_route,
        reason=reason,
        confidence=state.get("confidence", 0.0),
        evidence_count=state.get("evidence_count", 0),
    )
    return {
        "next_route": next_route,  # type: ignore[typeddict-item]
        "metadata": {**state.get("metadata", {}), "evaluation_reason": reason},
    }


def evaluation_route_key(state: AgentState) -> NextRoute:
    return state.get("next_route", "human_handoff")

