#!/usr/bin/env python3
"""L09 Step 31: wrap MCP tools for a LangChain/LangGraph Agent.

这个脚本对应老师讲义 9.5：将 MCP 接入 LangChain Agent。
为了让依赖保持轻量，本例不引入额外 adapter，而是演示最核心的桥接思路：

LangChain Tool -> MCP Client -> MCP Server -> 业务函数 -> 返回给 Agent。

默认运行不会调用真实 LLM，只直接演示 LangChain Tool 包装后的调用。
如需课堂演示 Agent 自动选择工具，可以加 --use-llm。

Usage:
    python practice/31_langchain_mcp_bridge.py
    python practice/31_langchain_mcp_bridge.py --use-llm
"""

from __future__ import annotations

import argparse
import asyncio
import os
import sys
from pathlib import Path
from typing import Any, Dict

from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


LESSON_DIR = Path(__file__).resolve().parents[1]
PROJECT_ROOT = LESSON_DIR.parents[1]
SERVER_PATH = Path(__file__).with_name("29_mcp_note_server.py")


def _content_to_text(result: Any) -> str:
    items = getattr(result, "content", None) or getattr(result, "contents", None) or []
    texts = [getattr(item, "text", "") for item in items if getattr(item, "text", "")]
    return "\n".join(texts) if texts else str(result)


async def call_mcp_tool(tool_name: str, arguments: Dict[str, Any]) -> str:
    """调用 MCP 工具。

    课堂版每次调用都启动一次 stdio Server，代码最直观；生产环境应复用连接池。
    """
    server_params = StdioServerParameters(command=sys.executable, args=[str(SERVER_PATH)])
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            result = await session.call_tool(tool_name, arguments=arguments)
            return _content_to_text(result)


def call_mcp_tool_sync(tool_name: str, arguments: Dict[str, Any]) -> str:
    return asyncio.run(call_mcp_tool(tool_name, arguments))


@tool
def create_note_via_mcp(title: str, content: str, tags: str = "") -> str:
    """通过 MCP Server 创建笔记。title 是标题，content 是正文，tags 是逗号分隔标签。"""
    return call_mcp_tool_sync("create_note", {"title": title, "content": content, "tags": tags})


@tool
def search_notes_via_mcp(keyword: str) -> str:
    """通过 MCP Server 搜索笔记。keyword 是搜索关键词。"""
    return call_mcp_tool_sync("search_notes", {"keyword": keyword})


@tool
def list_notes_via_mcp() -> str:
    """通过 MCP Server 列出所有笔记。"""
    return call_mcp_tool_sync("list_notes", {})


def build_llm() -> ChatOpenAI:
    load_dotenv(PROJECT_ROOT / ".env", override=False)
    missing = [
        name
        for name in ["OPENAI_API_KEY", "OPENAI_BASE_URL", "OPENAI_MODEL"]
        if not os.getenv(name, "").strip()
    ]
    if missing:
        raise RuntimeError(f"Missing required env vars: {', '.join(missing)}")
    return ChatOpenAI(
        model=os.environ["OPENAI_MODEL"],
        temperature=0,
        api_key=os.environ["OPENAI_API_KEY"],
        base_url=os.environ["OPENAI_BASE_URL"],
    )


def run_tool_demo() -> None:
    print("=== DIRECT LANGCHAIN TOOL CALLS ===")
    print(create_note_via_mcp.invoke(
        {
            "title": "LangChain MCP 桥接",
            "content": "LangChain Tool 可以把调用转发给 MCP Client，再由 MCP Server 执行业务能力。",
            "tags": "LangChain,MCP",
        }
    ))
    print()
    print(search_notes_via_mcp.invoke({"keyword": "MCP"}))


def run_agent_demo() -> None:
    agent = create_react_agent(
        model=build_llm(),
        tools=[create_note_via_mcp, search_notes_via_mcp, list_notes_via_mcp],
        prompt=(
            "你是一个智能笔记助手。你可以通过 MCP 工具创建、搜索和列出笔记。"
            "回答时请简洁说明你调用了哪个工具。"
        ),
    )
    result = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": "帮我创建一条笔记，标题是 MCP 桥接心得，内容是 MCP 可以作为 LangChain Agent 的工具接入层。",
                }
            ]
        }
    )
    print(result["messages"][-1].content)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="L09 LangChain to MCP bridge demo")
    parser.add_argument("--use-llm", action="store_true", help="Run a real LangGraph ReAct Agent")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.use_llm:
        run_agent_demo()
    else:
        run_tool_demo()


if __name__ == "__main__":
    main()
