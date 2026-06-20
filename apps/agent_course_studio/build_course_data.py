#!/usr/bin/env python3
"""Build the static data file used by Agent Course Studio.

The builder treats the existing lesson folders as the source of truth. It reads
Markdown and practice files, extracts a compact manifest, and writes one JSON
file that the browser app can load without a backend.
"""

from __future__ import annotations

import json
import re
import shutil
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


APP_DIR = Path(__file__).resolve().parent
COURSE_ROOT = APP_DIR.parents[1]
LESSONS_DIR = COURSE_ROOT / "lessons"
OUTPUT_PATH = APP_DIR / "web" / "data" / "course.json"
BOOT_PATH = APP_DIR / "web" / "data" / "course_boot.js"
DOCS_OUTPUT_DIR = APP_DIR / "web" / "data" / "docs"

MAX_DOC_CHARS = 48_000
MAX_SEARCH_CHARS = 2_200

SKIP_NAMES = {
    ".env",
    ".venv",
    "__pycache__",
    ".pytest_cache",
    ".ipynb_checkpoints",
    "rag_index",
    "kb_index.json",
    "memory.json",
    "tickets.jsonl",
    "knowledge_gaps.jsonl",
}

TOPIC_MAP = {
    "L01": ["Agent 基础", "ChatBot vs Agent", "LLM 调用", "Planning", "Tools", "Memory"],
    "L02": ["Prompt Engineering", "System Prompt", "Few-shot", "CoT", "ReAct", "结构化输出"],
    "L03": ["Function Calling", "Tool Schema", "并发工具", "错误恢复", "脏数据治理"],
    "L04": ["LangChain", "LangGraph", "自定义工具", "Agent 记忆", "搜索 Agent"],
    "L05": ["RAG", "BM25", "倒排索引", "Chunk", "Hybrid Search", "PDF RAG"],
    "L06": ["LCEL", "Retriever", "Output Parser", "Callback", "LangChain 架构"],
    "L07": ["Memory", "短期记忆", "长期记忆", "摘要记忆", "混合记忆"],
    "L08": ["Agent 模式", "Multi-Agent", "ReAct", "Supervisor", "分库分索引"],
    "L09": ["MCP", "Tools", "Resources", "Prompt", "Sampling", "安全审计"],
    "L10": ["Skill", "DDICE", "授权边界", "重试分层", "长尾延迟", "模型回滚"],
    "L11": ["评测", "部署", "FastAPI", "SSE", "成本监控", "安全护栏"],
    "L12": ["毕业项目", "智能客服", "LangGraph", "RAG", "FastAPI", "Harness"],
}


@dataclass(frozen=True)
class DocSpec:
    key: str
    label: str
    path: str


DOC_SPECS = [
    DocSpec("readme", "章节入口", "README.md"),
    DocSpec("lecture", "完整讲义", "lecture/LECTURE_FULL.md"),
    DocSpec("summary", "章节总结", "lecture/CHAPTER_SUMMARY.md"),
    DocSpec("preclass", "课前准备", "materials/PRECLASS_CHECKLIST.md"),
    DocSpec("quiz", "课后小测", "materials/MINI_QUIZ.md"),
    DocSpec("extensions", "拓展作业", "materials/EXTENSIONS.md"),
    DocSpec("interview", "面试题", "materials/INTERVIEW_QA.md"),
]


def read_text(path: Path, limit: int | None = MAX_DOC_CHARS) -> str:
    if not path.exists() or not path.is_file():
        return ""
    text = path.read_text(encoding="utf-8", errors="ignore")
    text = normalize_generated_text(scrub_sensitive(text))
    if limit and len(text) > limit:
        return text[:limit].rstrip() + "\n\n> 内容较长，网页预览已截断；完整内容请查看仓库原文件。"
    return text


def scrub_sensitive(text: str) -> str:
    """Remove machine-local paths and obvious secret-like values from public data."""
    text = re.sub(r"/home/[A-Za-z0-9._-]+/agent_course_2026", "<course-root>", text)
    text = re.sub(r"/home/[A-Za-z0-9._-]+", "<user-home>", text)
    text = re.sub(r"sk-[A-Za-z0-9_-]{20,}", "sk-<redacted>", text)
    text = re.sub(r"(OPENAI_API_KEY|ANTHROPIC_API_KEY|GEMINI_API_KEY|ADMIN_API_KEY)=([^<\s].+)", r"\1=<redacted>", text)
    return text


def normalize_generated_text(text: str) -> str:
    """Keep generated public Markdown stable and diff-check friendly."""
    lines = [line.rstrip() for line in text.splitlines()]
    return "\n".join(lines).rstrip() + "\n"


def first_heading(text: str, fallback: str) -> str:
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("# "):
            return stripped[2:].strip()
    return fallback


def first_paragraph(text: str) -> str:
    lines: list[str] = []
    in_heading = True
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            if lines:
                break
            continue
        if in_heading and line.startswith("#"):
            continue
        in_heading = False
        if line.startswith("|") or line.startswith("```"):
            if lines:
                break
            continue
        lines.append(line)
    return " ".join(lines)[:260]


def extract_section_list(text: str, heading_keyword: str, max_items: int = 8) -> list[str]:
    lines = text.splitlines()
    start = None
    for idx, line in enumerate(lines):
        if line.lstrip("# ").strip().startswith(heading_keyword):
            start = idx + 1
            break
    if start is None:
        return []

    items: list[str] = []
    for line in lines[start:]:
        stripped = line.strip()
        if stripped.startswith("## ") or stripped.startswith("# "):
            break
        if stripped.startswith("- "):
            items.append(stripped[2:].strip())
        if len(items) >= max_items:
            break
    return items


def list_files(base: Path, patterns: Iterable[str]) -> list[dict[str, str]]:
    files: list[dict[str, str]] = []
    for pattern in patterns:
        for path in sorted(base.glob(pattern)):
            if not path.is_file() or should_skip(path):
                continue
            files.append(
                {
                    "name": path.name,
                    "path": rel(path),
                    "size": human_size(path.stat().st_size),
                }
            )
    return files


def should_skip(path: Path) -> bool:
    return any(part in SKIP_NAMES for part in path.parts)


def human_size(size: int) -> str:
    if size < 1024:
        return f"{size} B"
    if size < 1024 * 1024:
        return f"{size / 1024:.1f} KB"
    return f"{size / 1024 / 1024:.1f} MB"


def rel(path: Path) -> str:
    return path.relative_to(COURSE_ROOT).as_posix()


def doc_output_path(lesson_id: str, key: str) -> Path:
    safe_key = re.sub(r"[^A-Za-z0-9_.-]+", "_", key)
    return DOCS_OUTPUT_DIR / lesson_id / f"{safe_key}.md"


def write_doc_content(lesson_id: str, key: str, content: str) -> str:
    output = doc_output_path(lesson_id, key)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(content, encoding="utf-8")
    return output.relative_to(APP_DIR / "web").as_posix()


def collect_docs(lesson_dir: Path) -> list[dict[str, str]]:
    docs: list[dict[str, str]] = []
    lesson_id = lesson_dir.name
    for spec in DOC_SPECS:
        path = lesson_dir / spec.path
        if not path.exists():
            continue
        content = read_text(path)
        docs.append(
            {
                "key": spec.key,
                "label": spec.label,
                "path": rel(path),
                "contentPath": write_doc_content(lesson_id, spec.key, content),
                "excerpt": compact(content, 420),
            }
        )
    for path in sorted((lesson_dir / "resources").glob("*.md")):
        content = read_text(path)
        key = f"resource:{path.stem}"
        docs.append(
            {
                "key": key,
                "label": f"资源：{path.stem}",
                "path": rel(path),
                "contentPath": write_doc_content(lesson_id, key, content),
                "excerpt": compact(content, 360),
            }
        )
    return docs


def compact(text: str, limit: int) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    return text[:limit]


def collect_lesson(lesson_dir: Path) -> dict:
    lesson_id = lesson_dir.name
    lesson_code = lesson_id.split("_", 1)[0]
    readme = read_text(lesson_dir / "README.md", limit=None)
    docs = collect_docs(lesson_dir)
    practice_files = list_files(lesson_dir / "practice", ["*.py", "*.sh", "*.html"])
    resource_files = list_files(lesson_dir / "resources", ["*.md", "*.json", "*.txt"])
    material_files = list_files(lesson_dir / "materials", ["*.md"])
    data_files = list_files(lesson_dir / "data", ["**/*"])
    preclass = lesson_dir / "practice" / "preclass_run.sh"

    searchable_text = "\n\n".join([readme, *[doc["excerpt"] for doc in docs]])
    return {
        "id": lesson_id,
        "code": lesson_code,
        "title": first_heading(readme, lesson_id),
        "intro": first_paragraph(readme),
        "topics": TOPIC_MAP.get(lesson_code, []),
        "goals": extract_section_list(readme, "本章学习目标"),
        "deliverables": extract_section_list(readme, "本章交付物"),
        "docs": docs,
        "practiceFiles": practice_files,
        "resourceFiles": resource_files,
        "materialFiles": material_files,
        "dataFiles": data_files[:16],
        "preclassCommand": f"cd {rel(lesson_dir)} && bash practice/preclass_run.sh" if preclass.exists() else "",
        "fileCount": count_lesson_files(lesson_dir),
        "searchText": compact(searchable_text, MAX_SEARCH_CHARS),
    }


def count_lesson_files(lesson_dir: Path) -> int:
    count = 0
    for path in lesson_dir.rglob("*"):
        if path.is_file() and not should_skip(path):
            count += 1
    return count


def collect_support_docs() -> list[dict[str, str]]:
    support_dir = COURSE_ROOT / "teaching_support"
    docs: list[dict[str, str]] = []
    if not support_dir.exists():
        return docs
    for path in sorted(support_dir.glob("*.md")):
        content = read_text(path)
        key = f"support:{path.stem}"
        docs.append(
            {
                "key": key,
                "title": first_heading(content, path.stem),
                "path": rel(path),
                "excerpt": compact(content, 420),
                "contentPath": write_doc_content("teaching_support", key, content),
            }
        )
    return docs


def build() -> dict:
    lessons = [collect_lesson(path) for path in sorted(LESSONS_DIR.glob("L*_*")) if path.is_dir()]
    support_docs = collect_support_docs()
    stats = {
        "lessonCount": len(lessons),
        "practiceCount": sum(len(lesson["practiceFiles"]) for lesson in lessons),
        "resourceCount": sum(len(lesson["resourceFiles"]) for lesson in lessons) + len(support_docs),
        "interviewCount": sum(1 for lesson in lessons for doc in lesson["docs"] if doc["key"] == "interview"),
        "fileCount": sum(lesson["fileCount"] for lesson in lessons),
    }
    return {
        "schemaVersion": 1,
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "course": {
            "name": "Agent Course Studio",
            "subtitle": "面向 Agent 开发学习的课程实验室",
            "description": "从 Agent 基础、Prompt、Function Calling、LangChain、RAG、Memory、MCP、Skill，到评测部署和毕业项目的完整学习路径。",
        },
        "stats": stats,
        "lessons": lessons,
        "supportDocs": support_docs,
    }


def main() -> None:
    if DOCS_OUTPUT_DIR.exists():
        shutil.rmtree(DOCS_OUTPUT_DIR)
    data = build()
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    json_text = json.dumps(data, ensure_ascii=False, indent=2)
    OUTPUT_PATH.write_text(json_text, encoding="utf-8")
    BOOT_PATH.write_text(f"window.AGENT_COURSE_DATA = {json_text};\n", encoding="utf-8")
    print(f"[OK] Wrote {OUTPUT_PATH.relative_to(COURSE_ROOT)}")
    print(f"[OK] Wrote {BOOT_PATH.relative_to(COURSE_ROOT)}")
    print(
        "[OK] Lessons: {lessonCount}, practice files: {practiceCount}, resources: {resourceCount}".format(
            **data["stats"]
        )
    )


if __name__ == "__main__":
    main()
