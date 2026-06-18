#!/usr/bin/env python3
"""L07 Step 25: connect long-term memory to a LangChain Agent.

这个脚本对应老师讲义 7.4：把长期记忆接入 Agent。
当前版本使用课程统一的 LangChain 1.2 `create_agent` API，保持和 L04/L06 一致。

建议阅读顺序：
1. 先看 MEMORY：理解长期记忆是跨会话 JSON 文件，不是 MemorySaver。
2. 再看四个 @tool：理解 Agent 通过工具写入和读取长期记忆。
3. 最后看 run_demo()：观察“先保存信息，再基于记忆回答”的闭环。

Usage:
    python practice/25_agent_with_long_memory.py --demo --reset
    python practice/25_agent_with_long_memory.py "我叫小明，是后端工程师，喜欢 Python"
"""

from __future__ import annotations

import argparse
from typing import Any, Dict

from langchain.agents import create_agent
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver

from memory_common import (
    LongTermMemory,
    default_json_memory_path,
    load_project_env,
    _read_float_env,
    _read_int_env,
)

import os


# MEMORY 是长期记忆：写入 JSON 文件，进程结束后仍然存在。
# MemorySaver 是短期/会话检查点：保存 Agent 当前 thread_id 的消息状态。
# 这两个层次故意都保留，帮助学生区分“对话上下文”和“跨会话记忆”。
MEMORY = LongTermMemory(default_json_memory_path())


def build_llm() -> ChatOpenAI:
    """创建课程统一 ChatOpenAI 模型对象。"""
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
        timeout=_read_float_env("MEMORY_AGENT_TIMEOUT_SEC", 60.0),
        max_retries=_read_int_env("MEMORY_AGENT_MAX_RETRIES", 1),
    )


@tool
def save_user_profile(key: str, value: str) -> str:
    """保存或更新用户画像字段，例如姓名、职业、所在团队。"""
    MEMORY.update_profile(key, value)
    return f"已更新用户画像：{key}={value}"


@tool
def save_user_preference(key: str, value: str) -> str:
    """保存用户偏好，例如回答风格、常用语言、学习偏好。"""
    memory_id = MEMORY.save_preference(key, value, importance=7)
    return f"已保存偏好：{key}={value}，memory_id={memory_id}"


@tool
def save_user_fact(fact: str, category: str = "general") -> str:
    """保存一条关于用户或项目的事实，例如负责项目、团队技术栈。"""
    memory_id = MEMORY.save_fact(fact, category=category, importance=7)
    return f"已保存事实：{fact}，memory_id={memory_id}"


@tool
def recall_user_memory(query: str) -> str:
    """查询用户画像、偏好和事实。当需要个性化回答时使用。"""
    results = MEMORY.search(query, limit=5)
    profile = MEMORY.get_profile_summary()
    return f"用户画像：\n{profile}\n\n检索 query={query!r} 的结果：\n{results}"


SYSTEM_PROMPT = """你是一个具有长期记忆能力的个人助手。

重要规则：
1. 当用户告诉你姓名、职业、偏好、项目背景等长期有效信息时，主动调用工具保存。
2. 当回答需要个性化背景时，先调用 recall_user_memory 查询。
3. 不要编造记忆；如果记忆里没有，就明确说明需要用户补充。
4. 长期记忆可能包含过期信息，涉及关键结论时要保守表达。
"""


def build_agent() -> Any:
    """创建带短期检查点和长期记忆工具的 Agent。"""
    return create_agent(
        model=build_llm(),
        tools=[save_user_profile, save_user_preference, save_user_fact, recall_user_memory],
        system_prompt=SYSTEM_PROMPT,
        checkpointer=MemorySaver(),
    )


def final_text(result: Dict[str, Any]) -> str:
    messages = result.get("messages", [])
    return str(getattr(messages[-1], "content", "")) if messages else ""


def chat(agent: Any, user_input: str, thread_id: str = "l07-demo") -> str:
    """运行一次 Agent。

    thread_id 控制短期会话上下文；JSON 文件控制长期记忆。
    """
    result = agent.invoke(
        {"messages": [{"role": "user", "content": user_input}]},
        config={"configurable": {"thread_id": thread_id}},
    )
    return final_text(result)


def run_demo(reset: bool = False) -> None:
    if reset and default_json_memory_path().exists():
        default_json_memory_path().unlink()
        global MEMORY
        MEMORY = LongTermMemory(default_json_memory_path())

    agent = build_agent()
    first = "我叫小明，是一个后端工程师，最常用的语言是 Python，喜欢简洁回答但要有代码示例。"
    second = "根据我的技术栈，推荐两个适合我继续学习的 AI Agent 框架。"
    print(f"[USER] {first}")
    print(f"[ASSISTANT] {chat(agent, first)}")
    print(f"\n[USER] {second}")
    print(f"[ASSISTANT] {chat(agent, second)}")
    print(f"\n[MEMORY FILE] {default_json_memory_path()}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="L07 Agent with long-term memory")
    parser.add_argument("prompt", nargs="?", default="")
    parser.add_argument("--demo", action="store_true", help="Run two-turn demo")
    parser.add_argument("--reset", action="store_true", help="Reset JSON memory before demo")
    parser.add_argument("--thread-id", default="l07-demo", help="Short-term conversation id")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.demo or not args.prompt:
        run_demo(reset=args.reset)
        return
    agent = build_agent()
    print(chat(agent, args.prompt, thread_id=args.thread_id))


if __name__ == "__main__":
    main()
