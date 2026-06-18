from __future__ import annotations

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from intelligent_customer.config import PROJECT_ROOT, ensure_runtime_dirs
from intelligent_customer.graph import run_agent
from intelligent_customer.harness.security import check_rate_limit, request_identity, require_admin_key
from intelligent_customer.harness.observability import audit_trace, log_event, metrics_snapshot, recent_events, record_feedback_metrics
from intelligent_customer.schemas import (
    ChatRequest,
    ChatResponse,
    EscalateRequest,
    FeedbackRequest,
    HealthResponse,
    KnowledgeGapUpdateRequest,
    KBDocumentCreateRequest,
    ResetRequest,
    TicketUpdateRequest,
)
from intelligent_customer.tools.evaluation_tool import create_eval_case_from_gap, list_generated_eval_cases, load_eval_report, run_quality_eval
from intelligent_customer.tools.kb_admin_tool import create_kb_document, get_kb_document, list_kb_documents, rebuild_kb
from intelligent_customer.tools.kb_search_tool import kb_search
from intelligent_customer.tools.knowledge_gap_tool import (
    get_knowledge_gap,
    knowledge_gap_stats,
    list_knowledge_gaps,
    record_knowledge_gap,
    update_knowledge_gap,
)
from intelligent_customer.tools.memory_tool import list_sessions, load_memory, reset_memory
from intelligent_customer.tools.ticket_tool import create_ticket, list_tickets, ticket_stats, update_ticket


ensure_runtime_dirs()

KB_COLLECTIONS = {"faq", "policy", "manual", "troubleshoot", "product"}

app = FastAPI(
    title="Intelligent Customer Agent",
    version="1.0.0",
    description="LangGraph + RAG + Harness intelligent customer service agent.",
)
app.mount("/web", StaticFiles(directory=PROJECT_ROOT / "web"), name="web")


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status="ok")


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest, raw_request: Request) -> ChatResponse:
    check_rate_limit(request_identity(raw_request, request.user_id or request.session_id))
    return run_agent(message=request.message, session_id=request.session_id, user_id=request.user_id)


@app.post("/reset")
def reset(request: ResetRequest) -> dict[str, str]:
    reset_memory(request.session_id)
    return {"status": "ok", "session_id": request.session_id}


@app.get("/sessions")
def sessions() -> dict[str, list[dict]]:
    return {"sessions": list_sessions()}


@app.get("/sessions/{session_id}/history")
def session_history(session_id: str) -> dict:
    return load_memory(session_id)


@app.delete("/sessions/{session_id}")
def delete_session(session_id: str) -> dict[str, str]:
    reset_memory(session_id)
    return {"status": "deleted", "session_id": session_id}


@app.get("/tickets")
def tickets(limit: int = 100) -> dict[str, list[dict]]:
    return {"tickets": list_tickets(limit=limit)}


@app.patch("/tickets/{ticket_id}", dependencies=[Depends(require_admin_key)])
def patch_ticket(ticket_id: str, request: TicketUpdateRequest) -> dict:
    ticket = update_ticket(ticket_id=ticket_id, status=request.status, assignee=request.assignee, note=request.note)
    if ticket is None:
        raise HTTPException(status_code=404, detail=f"ticket not found: {ticket_id}")
    log_event(
        ticket.get("trace_id") or "manual",
        ticket.get("session_id") or "unknown",
        "ticket.updated",
        ticket_id=ticket_id,
        status=request.status,
        assignee=request.assignee,
    )
    return ticket


@app.get("/tickets/stats")
def tickets_stats() -> dict:
    return ticket_stats()


@app.post("/escalate")
def escalate(request: EscalateRequest) -> dict:
    ticket = create_ticket(
        {
            "category": "handoff",
            "priority": "normal",
            "trace_id": "manual",
            "session_id": request.session_id,
            "user_id": request.user_id,
            "message": request.message,
            "reason": request.reason,
            "metadata": {"source": "manual_api"},
        }
    )
    return ticket


@app.get("/metrics")
def metrics() -> dict:
    return metrics_snapshot()


@app.post("/feedback")
def feedback(request: FeedbackRequest) -> dict[str, str]:
    log_event(
        request.trace_id,
        request.session_id,
        "feedback.received",
        rating=request.rating,
        comment=request.comment,
    )
    record_feedback_metrics(request.rating)
    if request.rating == "down":
        gap = record_knowledge_gap(
            {
                "trace_id": request.trace_id,
                "session_id": request.session_id,
                "message": request.comment or "用户反馈答案需要改进",
                "reason": "negative_feedback",
                "priority": "high",
                "metadata": {"rating": request.rating},
            }
        )
        log_event(
            request.trace_id,
            request.session_id,
            "knowledge_gap.recorded",
            gap_id=gap.get("gap_id"),
            reason="negative_feedback",
        )
    return {"status": "ok", "trace_id": request.trace_id}


@app.get("/knowledge-gaps")
def knowledge_gaps(limit: int = 100, status: str | None = None) -> dict[str, list[dict]]:
    return {"gaps": list_knowledge_gaps(limit=max(1, min(limit, 500)), status=status)}


@app.get("/knowledge-gaps/stats")
def knowledge_gaps_stats() -> dict:
    return knowledge_gap_stats()


@app.patch("/knowledge-gaps/{gap_id}", dependencies=[Depends(require_admin_key)])
def patch_knowledge_gap(gap_id: str, request: KnowledgeGapUpdateRequest) -> dict:
    gap = update_knowledge_gap(gap_id=gap_id, status=request.status, note=request.note)
    if gap is None:
        raise HTTPException(status_code=404, detail=f"knowledge gap not found: {gap_id}")
    trace_id = gap.get("trace_ids", ["manual"])[-1] if gap.get("trace_ids") else "manual"
    log_event(
        trace_id,
        gap.get("last_session_id") or gap.get("session_id") or "unknown",
        "knowledge_gap.updated",
        gap_id=gap_id,
        status=request.status,
    )
    return gap


@app.post("/knowledge-gaps/{gap_id}/eval-case", dependencies=[Depends(require_admin_key)])
def create_gap_eval_case(gap_id: str) -> dict:
    gap = get_knowledge_gap(gap_id)
    if gap is None:
        raise HTTPException(status_code=404, detail=f"knowledge gap not found: {gap_id}")
    case = create_eval_case_from_gap(gap)
    trace_id = gap.get("trace_ids", ["manual"])[-1] if gap.get("trace_ids") else "manual"
    log_event(
        trace_id,
        gap.get("last_session_id") or gap.get("session_id") or "unknown",
        "eval_case.generated",
        gap_id=gap_id,
        case_id=case["id"],
    )
    return case


@app.get("/eval/generated-cases")
def generated_eval_cases(limit: int = 100) -> dict:
    return list_generated_eval_cases(limit=limit)


@app.get("/kb/docs")
def kb_docs() -> dict[str, list[dict]]:
    return {"documents": list_kb_documents()}


@app.get("/kb/docs/{source_id}")
def kb_doc(source_id: str) -> dict:
    doc = get_kb_document(source_id)
    if doc is None:
        raise HTTPException(status_code=404, detail=f"kb document not found: {source_id}")
    return doc


@app.get("/kb/search")
def kb_search_debug(q: str, collection: str | None = None, k: int = 5) -> dict:
    query = q.strip()
    if not query:
        raise HTTPException(status_code=400, detail="query cannot be empty")
    if len(query) > 500:
        raise HTTPException(status_code=400, detail="query is too long")
    if collection and collection not in KB_COLLECTIONS:
        raise HTTPException(status_code=400, detail=f"unsupported collection: {collection}")

    limit = max(1, min(k, 20))
    selected = [collection] if collection else None
    results = kb_search(query=query, collections=selected, k=limit)
    log_event(
        "kb_search",
        "dashboard",
        "kb.search",
        query=query,
        collection=collection or "auto",
        k=limit,
        result_count=len(results),
        source_ids=[item.get("source_id") for item in results],
    )
    return {"query": query, "collection": collection or "auto", "k": limit, "results": results}


@app.post("/kb/docs", dependencies=[Depends(require_admin_key)])
def create_kb_doc(request: KBDocumentCreateRequest) -> dict:
    doc = create_kb_document(
        title=request.title,
        collection=request.collection,
        content=request.content,
        source_id=request.source_id,
        gap_id=request.gap_id,
    )
    log_event(
        "kb_admin",
        "kb_admin",
        "kb.document_created",
        source_id=doc["source_id"],
        collection=doc["collection"],
        gap_id=request.gap_id,
    )
    if request.gap_id:
        update_knowledge_gap(request.gap_id, status="closed", note=f"已创建知识库文档 {doc['source_id']}")
    return doc


@app.post("/kb/rebuild", dependencies=[Depends(require_admin_key)])
def kb_rebuild() -> dict:
    result = rebuild_kb()
    log_event("kb_admin", "kb_admin", "kb.rebuilt", doc_count=result["doc_count"])
    return result


@app.get("/events/recent")
def events_recent(limit: int = 100) -> dict[str, list[dict]]:
    return {"events": recent_events(limit=max(1, min(limit, 500)))}


@app.get("/eval/report")
def eval_report() -> dict:
    return load_eval_report()


@app.post("/eval/run", dependencies=[Depends(require_admin_key)])
def eval_run() -> dict:
    report = run_quality_eval()
    metrics = report.get("metrics", {})
    log_event(
        "eval",
        "eval",
        "eval.completed",
        overall_score=metrics.get("overall_score"),
        total=metrics.get("total"),
        failure_count=report.get("failure_count"),
    )
    return report


@app.get("/audit/{trace_id}")
def audit(trace_id: str) -> list[dict]:
    events = audit_trace(trace_id)
    if not events:
        raise HTTPException(status_code=404, detail=f"trace_id not found: {trace_id}")
    return events


@app.get("/")
def web_index() -> FileResponse:
    index_path = PROJECT_ROOT / "web" / "index.html"
    if not index_path.exists():
        raise HTTPException(status_code=404, detail="web/index.html not found")
    return FileResponse(index_path)
