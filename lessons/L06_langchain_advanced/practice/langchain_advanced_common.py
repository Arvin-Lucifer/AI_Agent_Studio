#!/usr/bin/env python3
"""Shared helpers for L06 LangChain advanced demos.

这个文件负责第六章所有示例的公共能力：加载 .env、创建 ChatOpenAI、提供示例文本。

建议阅读顺序：
1. 先看 build_llm()：理解 LangChain 模型对象如何复用课程 .env。
2. 再看 SAMPLE_DOCUMENT：后面的文档处理案例都会使用它。
3. 最后看 summarize_text()：Callback 示例会用它打印输入输出摘要。
"""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI


SAMPLE_DOCUMENT = """
随着大语言模型技术的快速发展，AI Agent 正在成为企业数字化转型的重要方向。
与传统聊天机器人不同，AI Agent 不只回答问题，还能进行任务规划、调用工具、检索知识库并执行多步工作流。

目前主要挑战包括：
1. 幻觉问题：Agent 有时会生成不准确或缺少依据的信息。
2. 成本控制：多轮推理、检索和工具调用会带来较高的 API 成本。
3. 安全性：恶意输入可能诱导 Agent 泄露信息或执行危险操作。
4. 可观测性：复杂链路中很难定位是哪一步出错。

建议企业在引入 AI Agent 时：
- 从小场景开始试点，逐步扩大应用范围。
- 建立评测体系，持续监控 Agent 表现。
- 重视数据安全、权限控制和隐私保护。
- 培养内部 Agent 开发人才，形成可维护的工程规范。
"""


def find_project_root() -> Path:
    """从脚本位置向上寻找课程根目录，保证所有示例都加载同一份 .env。"""
    for parent in Path(__file__).resolve().parents:
        if (parent / ".env").exists() or (parent / ".env.example").exists():
            return parent
    raise RuntimeError("Cannot find project root with .env or .env.example")


def load_project_env() -> None:
    """加载课程根目录 .env；不覆盖 shell 中临时设置的环境变量。"""
    load_dotenv(find_project_root() / ".env", override=False)


def _read_int_env(name: str, default: int) -> int:
    raw = os.getenv(name, "").strip()
    if not raw:
        return default
    try:
        value = int(raw)
        return value if value >= 1 else default
    except Exception:
        print(f"[WARN] Invalid {name}={raw!r}, fallback to {default}")
        return default


def _read_float_env(name: str, default: float) -> float:
    raw = os.getenv(name, "").strip()
    if not raw:
        return default
    try:
        value = float(raw)
        return value if value > 0 else default
    except Exception:
        print(f"[WARN] Invalid {name}={raw!r}, fallback to {default}")
        return default


def build_llm() -> ChatOpenAI:
    """创建 ChatOpenAI。

    L06 所有 LCEL 示例都使用这个入口，避免在每个文件里重复写 api_key/base_url/model。
    """
    load_project_env()
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    base_url = os.getenv("OPENAI_BASE_URL", "").strip()
    model = os.getenv("OPENAI_MODEL", "").strip()
    missing = [
        name
        for name, value in {
            "OPENAI_API_KEY": api_key,
            "OPENAI_BASE_URL": base_url,
            "OPENAI_MODEL": model,
        }.items()
        if not value
    ]
    if missing:
        raise RuntimeError(f"Missing required env vars: {', '.join(missing)}")

    return ChatOpenAI(
        model=model,
        temperature=0,
        api_key=api_key,
        base_url=base_url,
        timeout=_read_float_env("LCEL_REQUEST_TIMEOUT_SEC", 60.0),
        max_retries=_read_int_env("LCEL_MAX_RETRIES", 1),
    )


def summarize_text(text: object, limit: int = 120) -> str:
    """把任意输入输出压缩成适合日志展示的短文本。"""
    rendered = str(text).replace("\n", " ")
    return rendered[:limit] + ("..." if len(rendered) > limit else "")
