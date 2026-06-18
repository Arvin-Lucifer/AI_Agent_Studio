#!/usr/bin/env python3
"""Shared helpers for L09 MCP demos.

第 9 章的重点是“标准化工具接入”。为了让 MCP Server、Client、LangChain
包装示例都复用同一套业务逻辑，本文件只负责笔记数据的读写和搜索。

建议阅读顺序：
1. 先看 DATA_DIR/NOTES_FILE：理解工具数据落在哪里。
2. 再看 create_note()/update_note()/delete_note()：理解 MCP tool 背后的真实业务函数。
3. 最后看 notes_summary()：理解只读数据为什么更适合暴露成 MCP Resource。
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Iterable, List


LESSON_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = LESSON_DIR / "data"
NOTES_FILE = DATA_DIR / "notes.json"


@dataclass(frozen=True)
class NoteOperationResult:
    """统一工具返回结构，方便 Server/Client/Agent 三处复用。"""

    ok: bool
    message: str


def ensure_data_dir() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)


def load_notes() -> List[Dict[str, Any]]:
    """读取 JSON 笔记。

    课堂示例用 JSON 文件降低环境门槛；生产系统通常会换成数据库或文档服务。
    """
    ensure_data_dir()
    if not NOTES_FILE.exists():
        return []
    try:
        data = json.loads(NOTES_FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []
    return data if isinstance(data, list) else []


def save_notes(notes: Iterable[Dict[str, Any]]) -> None:
    ensure_data_dir()
    NOTES_FILE.write_text(
        json.dumps(list(notes), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def reset_notes() -> None:
    """清空课堂数据，主要给 preclass_run.sh 和测试使用。"""
    save_notes([])


def _next_id(notes: List[Dict[str, Any]]) -> int:
    existing_ids = [int(note.get("id", 0)) for note in notes if str(note.get("id", "")).isdigit()]
    return max(existing_ids, default=0) + 1


def _parse_tags(tags: str) -> List[str]:
    return [item.strip() for item in tags.split(",") if item.strip()]


def create_note(title: str, content: str, tags: str = "") -> NoteOperationResult:
    title = title.strip()
    content = content.strip()
    if not title:
        return NoteOperationResult(False, "创建失败：标题不能为空。")
    if not content:
        return NoteOperationResult(False, "创建失败：内容不能为空。")

    notes = load_notes()
    note = {
        "id": _next_id(notes),
        "title": title,
        "content": content,
        "tags": _parse_tags(tags),
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "updated_at": None,
    }
    notes.append(note)
    save_notes(notes)
    return NoteOperationResult(True, f"笔记创建成功：ID={note['id']}，标题={title}")


def update_note(note_id: int, title: str = "", content: str = "", tags: str = "") -> NoteOperationResult:
    """更新笔记；空参数表示不修改对应字段。"""
    notes = load_notes()
    for note in notes:
        if int(note.get("id", -1)) != note_id:
            continue
        if title.strip():
            note["title"] = title.strip()
        if content.strip():
            note["content"] = content.strip()
        if tags.strip():
            note["tags"] = _parse_tags(tags)
        note["updated_at"] = datetime.now().isoformat(timespec="seconds")
        save_notes(notes)
        return NoteOperationResult(True, f"笔记更新成功：ID={note_id}")
    return NoteOperationResult(False, f"更新失败：未找到 ID={note_id} 的笔记。")


def delete_note(note_id: int) -> NoteOperationResult:
    notes = load_notes()
    kept = [note for note in notes if int(note.get("id", -1)) != note_id]
    if len(kept) == len(notes):
        return NoteOperationResult(False, f"删除失败：未找到 ID={note_id} 的笔记。")
    save_notes(kept)
    return NoteOperationResult(True, f"笔记删除成功：ID={note_id}")


def list_notes() -> str:
    notes = load_notes()
    if not notes:
        return "暂无笔记。"

    lines = [f"共 {len(notes)} 条笔记："]
    for note in notes:
        content = str(note.get("content", ""))
        preview = content[:60] + ("..." if len(content) > 60 else "")
        tags = ", ".join(note.get("tags", [])) if note.get("tags") else "无"
        updated = note.get("updated_at") or "未更新"
        lines.append(
            f"[{note['id']}] {note['title']}\n"
            f"    摘要: {preview}\n"
            f"    标签: {tags}\n"
            f"    创建: {note.get('created_at', '')}\n"
            f"    更新: {updated}"
        )
    return "\n\n".join(lines)


def search_notes(keyword: str) -> str:
    keyword = keyword.strip().lower()
    if not keyword:
        return "搜索失败：关键词不能为空。"

    results = []
    for note in load_notes():
        haystack = f"{note.get('title', '')}\n{note.get('content', '')}\n{' '.join(note.get('tags', []))}".lower()
        if keyword in haystack:
            results.append(note)

    if not results:
        return f"未找到包含 '{keyword}' 的笔记。"

    lines = [f"找到 {len(results)} 条相关笔记："]
    for note in results:
        lines.append(f"[{note['id']}] {note['title']}: {note['content'][:100]}")
    return "\n".join(lines)


def notes_summary() -> str:
    """生成只读统计摘要，适合做 Resource。"""
    notes = load_notes()
    if not notes:
        return "暂无笔记数据。"

    tag_counts: Dict[str, int] = {}
    for note in notes:
        for tag in note.get("tags", []):
            tag_counts[tag] = tag_counts.get(tag, 0) + 1

    tags = ", ".join(f"{tag}({count})" for tag, count in sorted(tag_counts.items())) or "无"
    return (
        "笔记统计：\n"
        f"- 总数: {len(notes)} 条\n"
        f"- 标签: {tags}\n"
        f"- 最新笔记: {notes[-1].get('title', '')}\n"
        f"- 数据文件: {NOTES_FILE}"
    )


def seed_demo_notes() -> None:
    """写入稳定演示数据，保证课堂脚本每次输出可预测。"""
    reset_notes()
    create_note(
        "MCP 学习笔记",
        "MCP 用 Client-Server 架构统一接入 Tools、Resources、Prompts 和 Sampling。",
        "MCP,协议",
    )
    create_note(
        "Function Calling 对比",
        "Function Calling 更关注模型如何填函数参数；MCP 更关注工具和上下文如何标准化接入。",
        "Agent,工具调用",
    )
