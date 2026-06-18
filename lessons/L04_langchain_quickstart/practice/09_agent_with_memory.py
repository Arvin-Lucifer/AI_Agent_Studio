#!/usr/bin/env python3
"""L04 Step 9: LangGraph Agent with memory.

这个脚本演示 MemorySaver + thread_id：
同一个 thread_id 会延续上下文，不同 thread_id 的会话彼此隔离。

读这段代码时要特别区分：
- MemorySaver：负责保存 Agent 每一步的状态。
- thread_id：负责告诉框架“这次调用属于哪一个会话”。
- SYSTEM_PROMPT：负责告诉模型应该记住用户在当前会话里说过的信息。

Usage:
    python practice/09_agent_with_memory.py --demo
    python practice/09_agent_with_memory.py --thread-id session_1 "我工作的城市天气怎么样？"
"""

from __future__ import annotations

import argparse
from typing import Any, Dict

from langchain.agents import create_agent
from langgraph.checkpoint.memory import MemorySaver

from langchain_common import build_llm, final_text, get_weather


# 这里写“当前会话”很重要：记忆不是全局共享的。
# 真实产品里，一个用户不应该读到另一个用户的上下文。
SYSTEM_PROMPT = (
    "你是一个友好的助手。你可以查询天气。"
    "请记住用户在当前会话中告诉你的姓名、城市和偏好。"
)


def build_agent() -> Any:
    """创建带内存检查点的 Agent；MemorySaver 适合课堂演示，不做持久化。"""
    # MemorySaver 是内存级 checkpointer：
    # 优点是无需数据库，适合课堂演示；缺点是进程结束后记忆会丢。
    # 生产环境会换成 SQLite/Postgres/Redis 等持久化检查点。
    memory = MemorySaver()

    # checkpointer 接入后，Agent 每次 invoke 都可以根据 thread_id 找回历史状态。
    return create_agent(
        model=build_llm(),
        tools=[get_weather],
        system_prompt=SYSTEM_PROMPT,
        checkpointer=memory,
    )


def chat(agent: Any, user_input: str, thread_id: str = "default") -> str:
    """带记忆的单轮调用；thread_id 决定这句话属于哪个会话。"""
    # config.configurable.thread_id 是 LangGraph 记忆机制的关键入口。
    # 同一个 thread_id：继续同一段对话；不同 thread_id：从另一段独立对话开始。
    result: Dict[str, Any] = agent.invoke(
        {"messages": [{"role": "user", "content": user_input}]},
        config={"configurable": {"thread_id": thread_id}},
    )
    answer = final_text(result)
    print(f"\n[{thread_id}] USER: {user_input}")
    print(f"[{thread_id}] AI: {answer}")
    return answer


def run_demo() -> None:
    """演示同一个会话能记住信息，不同会话不会共享私人上下文。"""
    agent = build_agent()

    # 前三轮使用 session_1，模型应该能把“小明”和“北京工作”保留下来。
    chat(agent, "我叫小明，我在北京工作。", "session_1")
    chat(agent, "我工作的城市天气怎么样？", "session_1")
    chat(agent, "我叫什么名字？", "session_1")

    # 第四轮换成 session_2，目的是证明记忆按会话隔离，而不是全局共享。
    chat(agent, "我叫什么名字？", "session_2")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="L04 LangGraph memory demo")
    parser.add_argument("prompt", nargs="?", default="我工作的城市天气怎么样？")
    parser.add_argument("--thread-id", default="session_1", help="Conversation id")
    parser.add_argument("--demo", action="store_true", help="Run multi-turn memory demo")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.demo:
        run_demo()
        return
    agent = build_agent()
    chat(agent, args.prompt, thread_id=args.thread_id)


if __name__ == "__main__":
    main()
