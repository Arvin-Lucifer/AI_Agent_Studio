from __future__ import annotations

from typing import Any, Literal, TypedDict

from intelligent_customer.schemas import Intent, Route


NextRoute = Literal["final", "clarify", "human_handoff", "ticket"]


class AgentState(TypedDict, total=False):
    trace_id: str
    session_id: str
    user_id: str | None
    message: str
    history: list[dict[str, Any]]
    memory_summary: str
    intent: Intent
    route: Route
    next_route: NextRoute
    collections: list[str]
    contextual_query: str
    retrieved_docs: list[dict[str, Any]]
    evidence_count: int
    confidence: float
    answer: str
    citations: list[dict[str, Any]]
    need_clarification: bool
    clarification_question: str | None
    ticket_id: str | None
    ticket_payload: dict[str, Any] | None
    ticket_updated: bool
    ticket_status_checked: bool
    need_human: bool
    errors: list[str]
    metadata: dict[str, Any]
    started_at: float
    latency_ms: float
