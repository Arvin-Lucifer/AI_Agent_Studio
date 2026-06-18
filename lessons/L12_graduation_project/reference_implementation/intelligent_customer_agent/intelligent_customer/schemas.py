from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field


Intent = Literal["qa", "consult", "complaint", "unclear", "out_of_scope"]
Route = Literal["retrieve", "clarify", "ticket", "human_handoff", "react_fallback", "final"]


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000)
    session_id: str = Field(default="default", min_length=1, max_length=128)
    user_id: str | None = Field(default=None, max_length=128)


class Citation(BaseModel):
    source_id: str
    title: str
    collection: str
    score: float
    snippet: str | None = None


class ChatResponse(BaseModel):
    trace_id: str
    session_id: str
    intent: Intent
    route: Route
    reply: str
    confidence: float = Field(ge=0.0, le=1.0)
    citations: list[Citation] = Field(default_factory=list)
    ticket_id: str | None = None
    need_human: bool = False
    metadata: dict[str, Any] = Field(default_factory=dict)

    model_config = ConfigDict(extra="forbid")


class HealthResponse(BaseModel):
    status: str = "ok"


class ResetRequest(BaseModel):
    session_id: str


class EscalateRequest(BaseModel):
    message: str
    session_id: str = "default"
    user_id: str | None = None
    reason: str = "manual_escalation"


class FeedbackRequest(BaseModel):
    trace_id: str = Field(..., min_length=1, max_length=128)
    session_id: str = Field(..., min_length=1, max_length=128)
    rating: Literal["up", "down"]
    comment: str | None = Field(default=None, max_length=1000)


class TicketUpdateRequest(BaseModel):
    status: Literal["open", "in_progress", "resolved", "closed"]
    assignee: str | None = Field(default=None, max_length=128)
    note: str | None = Field(default=None, max_length=1000)


class KnowledgeGapUpdateRequest(BaseModel):
    status: Literal["open", "reviewing", "closed"]
    note: str | None = Field(default=None, max_length=1000)


class KBDocumentCreateRequest(BaseModel):
    title: str = Field(..., min_length=2, max_length=120)
    collection: Literal["faq", "policy", "manual", "troubleshoot", "product"]
    content: str = Field(..., min_length=10, max_length=8000)
    source_id: str | None = Field(default=None, min_length=2, max_length=80)
    gap_id: str | None = Field(default=None, max_length=128)


class ErrorEnvelope(BaseModel):
    trace_id: str
    error: dict[str, str]
