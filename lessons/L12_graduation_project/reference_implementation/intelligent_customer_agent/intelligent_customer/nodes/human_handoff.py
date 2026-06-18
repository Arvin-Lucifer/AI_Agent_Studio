from __future__ import annotations

from intelligent_customer.harness.observability import log_event
from intelligent_customer.harness.state import AgentState
from intelligent_customer.nodes.create_ticket import create_ticket_node


def human_handoff_node(state: AgentState) -> AgentState:
    log_event(
        state["trace_id"],
        state["session_id"],
        "fallback.triggered",
        fallback_type="human_handoff",
        confidence=state.get("confidence", 0.0),
    )
    handoff_state = {**state, "intent": state.get("intent", "out_of_scope")}
    return create_ticket_node(handoff_state)  # type: ignore[arg-type]

