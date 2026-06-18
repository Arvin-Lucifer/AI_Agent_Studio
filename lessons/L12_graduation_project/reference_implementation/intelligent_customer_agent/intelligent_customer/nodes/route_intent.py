from __future__ import annotations

from intelligent_customer.harness.guardrails import route_for_intent
from intelligent_customer.harness.observability import log_event
from intelligent_customer.harness.state import AgentState


def route_intent_node(state: AgentState) -> AgentState:
    route = route_for_intent(state["intent"])
    log_event(
        state["trace_id"],
        state["session_id"],
        "route.decided",
        intent=state["intent"],
        route=route,
    )
    return {"route": route}


def route_key(state: AgentState) -> str:
    return state.get("route", "human_handoff")

