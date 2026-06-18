"""L11 Step 47: wrap an Agent as a FastAPI REST API.

Run self-test:
    python practice/47_agent_api.py --self-test

Run server manually:
    uvicorn practice.47_agent_api:app --host 0.0.0.0 --port 8000

The classroom API uses ``MockAgent`` so it is deterministic.  Replace it with a
real RAG/Tool Agent after the request/response contract is stable.
"""

from __future__ import annotations

import argparse

from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient
from pydantic import BaseModel, Field

from eval_deploy_common import MockAgent, sanitize_input


agent = MockAgent()
app = FastAPI(title="L11 Agent API", version="1.0.0")


class ChatRequest(BaseModel):
    """External API contract for one Agent turn."""

    message: str = Field(..., min_length=0, max_length=4000)
    session_id: str = Field(default="default", min_length=1, max_length=128)


class ChatResponse(BaseModel):
    """Keep response structured so frontend, tests, and logs can consume it."""

    reply: str
    session_id: str
    tool_calls: list[str]
    elapsed_ms: int
    safety_flags: list[str]


@app.get("/health")
async def health() -> dict:
    """Health checks should be cheap and never call the model."""

    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    """Run one Agent turn behind a stable HTTP boundary."""

    cleaned, flags = sanitize_input(request.message)
    try:
        run = agent(cleaned)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    return ChatResponse(
        reply=run.answer,
        session_id=request.session_id,
        tool_calls=run.tool_calls,
        elapsed_ms=run.elapsed_ms,
        safety_flags=flags,
    )


def self_test() -> None:
    """Exercise the API without starting a real server."""

    client = TestClient(app)
    health_resp = client.get("/health")
    chat_resp = client.post(
        "/chat",
        json={"message": "我入职2年了，有几天年假？", "session_id": "user_001"},
    )
    print("[HEALTH]", health_resp.status_code, health_resp.json())
    print("[CHAT]", chat_resp.status_code, chat_resp.json())
    assert health_resp.status_code == 200
    assert chat_resp.status_code == 200
    assert "5天" in chat_resp.json()["reply"]


def main() -> None:
    parser = argparse.ArgumentParser(description="L11 FastAPI Agent API")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        self_test()
    else:
        print("Run: uvicorn practice.47_agent_api:app --host 0.0.0.0 --port 8000")


if __name__ == "__main__":
    main()
