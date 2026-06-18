"""L11 Step 48: expose a streaming Agent API with SSE.

Run self-test:
    python practice/48_agent_api_streaming.py --self-test

The endpoint emits three event types:
- ``tool_call`` when the Agent uses a tool;
- ``token`` for response chunks;
- ``done`` when the turn is complete.
"""

from __future__ import annotations

import argparse
import asyncio
import json
from collections.abc import AsyncIterator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from sse_starlette.sse import EventSourceResponse

from eval_deploy_common import MockAgent, sanitize_input


agent = MockAgent()
app = FastAPI(title="L11 Agent Streaming API", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=0, max_length=4000)
    session_id: str = Field(default="default", min_length=1, max_length=128)


def chunk_text(text: str, chunk_size: int = 12) -> list[str]:
    """Split text into small chunks to mimic token streaming."""

    return [text[i : i + chunk_size] for i in range(0, len(text), chunk_size)] or [""]


async def iter_agent_events(message: str, session_id: str) -> AsyncIterator[dict]:
    """Yield SSE-compatible event dictionaries.

    In a real LLM integration this function would listen to ``astream_events``.
    The mock version keeps the event shape the same without requiring a network
    call during tests.
    """

    cleaned, flags = sanitize_input(message)
    run = agent(cleaned)

    if flags:
        yield {
            "event": "message",
            "data": json.dumps({"type": "safety", "flags": flags}, ensure_ascii=False),
        }

    for tool_name in run.tool_calls:
        yield {
            "event": "message",
            "data": json.dumps({"type": "tool_call", "tool": tool_name}, ensure_ascii=False),
        }
        await asyncio.sleep(0)

    for chunk in chunk_text(run.answer):
        yield {
            "event": "message",
            "data": json.dumps({"type": "token", "content": chunk}, ensure_ascii=False),
        }
        await asyncio.sleep(0)

    yield {
        "event": "message",
        "data": json.dumps({"type": "done", "session_id": session_id}, ensure_ascii=False),
    }


@app.post("/chat/stream")
async def chat_stream(request: ChatRequest) -> EventSourceResponse:
    """Return an SSE stream for browser or CLI clients."""

    return EventSourceResponse(iter_agent_events(request.message, request.session_id))


async def collect_self_test_events() -> list[dict]:
    events = []
    async for event in iter_agent_events("代码合并到主分支前需要做什么？", "test"):
        events.append(event)
    return events


def self_test() -> None:
    events = asyncio.run(collect_self_test_events())
    print("[STREAM EVENTS]")
    for event in events:
        print(event)
    assert any('"type": "tool_call"' in event["data"] for event in events)
    assert any('"type": "done"' in event["data"] for event in events)


def main() -> None:
    parser = argparse.ArgumentParser(description="L11 streaming Agent API")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        self_test()
    else:
        print("Run: uvicorn practice.48_agent_api_streaming:app --host 0.0.0.0 --port 8000")


if __name__ == "__main__":
    main()
