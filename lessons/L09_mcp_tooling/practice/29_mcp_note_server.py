#!/usr/bin/env python3
"""L09 Step 29: note management MCP Server.

这个脚本对应老师讲义 9.3：开发一个 MCP Server。
它通过 FastMCP 暴露笔记管理能力，覆盖三类常见 primitive：

- Tools：create/list/search/update/delete note，由模型或 Agent 主动调用。
- Resource：notes://summary，由 Host/Client 决定是否注入上下文。
- Prompt：note-review-template，给用户或应用复用提示模板。

重要提醒：stdio transport 下 stdout 是 JSON-RPC 通道，Server 里不要 print 日志。
如果要调试，请写 stderr 或日志文件，否则 Host 可能解析失败。

Usage:
    python practice/29_mcp_note_server.py
    mcp dev practice/29_mcp_note_server.py
"""

from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from mcp_common import (
    create_note as create_note_record,
    delete_note as delete_note_record,
    list_notes as list_note_records,
    notes_summary,
    search_notes as search_note_records,
    seed_demo_notes,
    update_note as update_note_record,
)


mcp = FastMCP("note-manager", log_level="WARNING")


@mcp.tool()
def create_note(title: str, content: str, tags: str = "") -> str:
    """创建一条新笔记。

    Args:
        title: 笔记标题，不能为空。
        content: 笔记正文，不能为空。
        tags: 逗号分隔标签，例如 "MCP,Agent"。
    """
    return create_note_record(title, content, tags).message


@mcp.tool()
def list_notes() -> str:
    """列出所有笔记的标题、摘要、标签和时间。"""
    return list_note_records()


@mcp.tool()
def search_notes(keyword: str) -> str:
    """按关键词搜索笔记，会匹配标题、正文和标签。

    Args:
        keyword: 搜索关键词，不能为空。
    """
    return search_note_records(keyword)


@mcp.tool()
def update_note(note_id: int, title: str = "", content: str = "", tags: str = "") -> str:
    """更新一条笔记；空字段表示不修改。

    Args:
        note_id: 要更新的笔记 ID。
        title: 新标题，可为空。
        content: 新正文，可为空。
        tags: 新标签，逗号分隔，可为空。
    """
    return update_note_record(note_id, title=title, content=content, tags=tags).message


@mcp.tool()
def delete_note(note_id: int) -> str:
    """删除一条笔记。

    Args:
        note_id: 要删除的笔记 ID。
    """
    return delete_note_record(note_id).message


@mcp.tool()
def seed_notes() -> str:
    """重置并写入两条演示笔记，便于课堂重复运行。"""
    seed_demo_notes()
    return "演示笔记已重置。"


@mcp.resource("notes://summary")
def get_notes_summary() -> str:
    """获取笔记统计摘要。"""
    return notes_summary()


@mcp.prompt()
def note_review_template(topic: str = "MCP") -> str:
    """生成笔记复盘提示模板。"""
    return (
        f"请基于我的笔记，复盘主题“{topic}”：\n"
        "1. 提炼 3 个关键概念。\n"
        "2. 找出 2 个容易混淆的点。\n"
        "3. 给出 1 个可以动手实践的小任务。\n"
        "要求：只基于已提供的笔记内容，不要编造来源。"
    )


if __name__ == "__main__":
    mcp.run(transport="stdio")
