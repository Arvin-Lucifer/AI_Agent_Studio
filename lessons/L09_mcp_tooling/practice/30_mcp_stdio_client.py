#!/usr/bin/env python3
"""L09 Step 30: connect to an MCP Server through stdio.

这个脚本对应老师讲义 9.4：MCP Client 如何连接 Server 并调用工具。
它会启动 29_mcp_note_server.py 作为子进程，通过 stdio 发送 JSON-RPC 消息。

建议阅读顺序：
1. 先看 server_params：Host/Client 如何启动本地 Server。
2. 再看 session.initialize()：MCP 连接建立时先做握手和能力协商。
3. 最后看 list_tools()/call_tool()/read_resource()/list_prompts()：理解四类能力如何发现和调用。

Usage:
    python practice/30_mcp_stdio_client.py
"""

from __future__ import annotations

import argparse
import asyncio
import sys
from pathlib import Path
from typing import Any

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


SERVER_PATH = Path(__file__).with_name("29_mcp_note_server.py")


def _content_to_text(result: Any) -> str:
    """兼容 ToolResult / ResourceResult / PromptResult 的文本提取。

    MCP 返回对象会带 content 或 contents 字段；课堂代码只需要把文本展示清楚。
    """
    parts = []
    items = getattr(result, "content", None) or getattr(result, "contents", None) or []
    for item in items:
        text = getattr(item, "text", None)
        if text is not None:
            parts.append(text)
            continue
        blob = getattr(item, "blob", None)
        if blob is not None:
            parts.append(str(blob))
    messages = getattr(result, "messages", None) or []
    for message in messages:
        content = getattr(message, "content", None)
        text = getattr(content, "text", None)
        if text is not None:
            parts.append(text)
    return "\n".join(parts) if parts else str(result)


async def run_demo(reset: bool) -> None:
    server_params = StdioServerParameters(
        command=sys.executable,
        args=[str(SERVER_PATH)],
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            tools = await session.list_tools()
            print("=== TOOLS ===")
            for tool in tools.tools:
                print(f"- {tool.name}: {tool.description}")

            resources = await session.list_resources()
            print("\n=== RESOURCES ===")
            for resource in resources.resources:
                print(f"- {resource.uri}: {resource.name or resource.description}")

            prompts = await session.list_prompts()
            print("\n=== PROMPTS ===")
            for prompt in prompts.prompts:
                print(f"- {prompt.name}: {prompt.description}")

            if reset:
                result = await session.call_tool("seed_notes", arguments={})
                print("\n=== RESET ===")
                print(_content_to_text(result))

            result = await session.call_tool(
                "create_note",
                arguments={
                    "title": "MCP Client 调用记录",
                    "content": "通过 stdio Client 调用了 MCP Server 的 create_note 工具。",
                    "tags": "MCP,Client",
                },
            )
            print("\n=== CREATE NOTE ===")
            print(_content_to_text(result))

            result = await session.call_tool("search_notes", arguments={"keyword": "MCP"})
            print("\n=== SEARCH NOTES ===")
            print(_content_to_text(result))

            result = await session.read_resource("notes://summary")
            print("\n=== RESOURCE notes://summary ===")
            print(_content_to_text(result))

            prompt = await session.get_prompt("note_review_template", arguments={"topic": "MCP"})
            print("\n=== PROMPT note_review_template ===")
            print(_content_to_text(prompt))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="L09 MCP stdio client demo")
    parser.add_argument("--no-reset", action="store_true", help="Do not reset demo notes before running")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    asyncio.run(run_demo(reset=not args.no_reset))


if __name__ == "__main__":
    main()
