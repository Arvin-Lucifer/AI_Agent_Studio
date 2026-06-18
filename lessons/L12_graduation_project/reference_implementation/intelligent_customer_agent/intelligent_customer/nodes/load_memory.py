from __future__ import annotations

from intelligent_customer.harness.observability import log_event
from intelligent_customer.harness.state import AgentState
from intelligent_customer.tools.memory_tool import load_memory


def load_memory_node(state: AgentState) -> AgentState:
    session = load_memory(state["session_id"])
    update: AgentState = {
        "history": session.get("messages", []),
        "memory_summary": session.get("summary", ""),
    }
    log_event(
        state["trace_id"],
        state["session_id"],
        "memory.loaded",
        message_count=len(update["history"]),
    )
    return update

