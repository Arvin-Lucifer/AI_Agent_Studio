#!/usr/bin/env python3
"""L04 Step 10: search question-answering Agent.

这个脚本用模拟搜索工具搭建一个更贴近业务的 Agent：
它可以搜索信息、总结 URL、做计算，并用 MemorySaver 保存会话上下文。

请把这个示例看成“搜索 Agent 的骨架”：
1. 工具层：search_web/summarize_url/calculate 提供外部能力。
2. Prompt 层：SYSTEM_PROMPT 规定什么时候搜索、如何说明来源。
3. 会话层：MemorySaver + thread_id 保存多轮上下文。
4. 交互层：ask/run_repl 负责命令行输入输出和错误兜底。

Usage:
    python practice/10_search_agent.py --question "AI Agent 有哪些典型应用？"
    python practice/10_search_agent.py
"""

from __future__ import annotations

import argparse
from typing import Any, Dict

from langchain.agents import create_agent
from langchain_core.tools import tool
from langgraph.checkpoint.memory import MemorySaver

from langchain_common import build_llm, calculate, final_text


@tool
def search_web(query: str) -> str:
    """搜索互联网获取信息。当需要查找不确定事实、最新信息或背景资料时使用。"""
    # 这里故意打印 query，帮助学生观察模型如何把用户问题改写成搜索词。
    # 很多 Agent 问题不是“工具坏了”，而是“模型生成的搜索词偏了”。
    print(f"\n[DEBUG] search query: {query!r}")

    # 课堂版先用 mock_results，让学习重点停留在 Agent 流程。
    # 接入真实搜索 API 时，建议返回 title/url/snippet/published_at 等结构化字段。
    mock_results = {
        "ai": "AI Agent 典型应用包括客服自动化、数据分析助手、代码助手、个人工作流助理和企业知识库问答。",
        "agent": "Agent 系统通常由模型、工具、记忆、规划和评估模块组成，正在从演示走向实际工作流。",
        "python": "Python 新版本持续提升性能、类型标注和开发体验，生态仍然是 AI 工程的重要基础。",
        "langchain": "LangChain 提供模型、Prompt、工具、RAG 和 Agent 组件，LangGraph 提供复杂图编排能力。",
        "default": f"搜索 '{query}' 的模拟结果：找到若干相关资料，但需要进一步核验来源。",
    }
    lowered = query.lower()
    # 这个匹配逻辑故意保持简单，方便学生看懂。
    # 真实搜索系统会有召回、重排、过滤和来源可信度判断。
    for key, value in mock_results.items():
        if key != "default" and key in lowered:
            return value
    return mock_results["default"]


@tool
def summarize_url(url: str) -> str:
    """获取并总结指定 URL 的网页内容。课堂版返回模拟摘要，真实项目可接入网页抓取。"""
    # 即便是示例，也要做最基本的输入校验。
    # 工具边界越清楚，Agent 越不容易把错误输入继续传下去。
    if not url.startswith(("http://", "https://")):
        return "错误：URL 必须以 http:// 或 https:// 开头"
    return f"网页 {url} 的模拟摘要：这是一篇关于 AI 工程实践的文章，重点讨论工具调用、记忆和评估。"


# 这个 Prompt 的重点不是“让模型更会写”，而是约束证据使用：
# 哪些问题需要搜索、搜索结果不足时怎么说、回答里如何区分工具结果和模型概括。
SYSTEM_PROMPT = """你是一个智能搜索问答助手。

## 工作方式
1. 对于你确定的基础知识，可以直接回答。
2. 对于不确定、需要背景资料或可能变化的问题，先使用搜索工具。
3. 回答时说明信息来自工具结果还是你的概括。
4. 如果搜索结果不足，要明确说明不足，不要编造来源。

## 回答风格
- 简洁明了，重点突出。
- 复杂信息用列表组织。
- 必要时给出下一步建议。
"""


def build_agent() -> Any:
    """创建搜索 Agent；MemorySaver 保存同一 thread_id 下的多轮上下文。"""
    # 搜索问答通常是连续会话：用户会追问“展开第二点”“保存刚才的结果”。
    # 因此这里接入 MemorySaver，后续扩展笔记工具时也能复用同一上下文。
    memory = MemorySaver()

    # tools 里混合了本文件定义的搜索/URL 工具，以及 common 里的安全计算工具。
    # 这展示了框架化后的组合方式：工具可以来自不同模块，只要满足 BaseTool 协议即可。
    return create_agent(
        model=build_llm(),
        tools=[search_web, summarize_url, calculate],
        system_prompt=SYSTEM_PROMPT,
        checkpointer=memory,
    )


def ask(agent: Any, question: str, thread_id: str) -> str:
    """执行一次搜索问答；thread_id 用于区分不同用户或会话。"""
    # 非交互式调用适合脚本验证和自动化测试。
    # 例如 preclass_run.sh 就用 --question 跑一条固定问题，确认搜索链路可用。
    result: Dict[str, Any] = agent.invoke(
        {"messages": [{"role": "user", "content": question}]},
        config={"configurable": {"thread_id": thread_id}},
    )
    answer = final_text(result)
    print(f"\n[USER] {question}")
    print(f"[ASSISTANT] {answer}")
    return answer


def run_repl(thread_id: str) -> None:
    """交互式运行；循环内捕获异常，避免一次工具错误导致整个 REPL 退出。"""
    agent = build_agent()
    print("=" * 60)
    print("  智能搜索问答 Agent（输入 quit / exit / q 退出）")
    print("=" * 60)
    while True:
        try:
            user_input = input("\n你: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n再见！")
            break

        if not user_input:
            continue
        if user_input.lower() in {"quit", "exit", "q"}:
            print("再见！")
            break

        try:
            # 把 try/except 放在循环内部：
            # 单次模型或工具失败只影响当前问题，不会让整个课堂 demo 退出。
            ask(agent, user_input, thread_id)
        except Exception as exc:
            print(f"[ERROR] {type(exc).__name__}: {exc}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="L04 search QA Agent")
    parser.add_argument("--question", default="", help="Run one non-interactive question")
    parser.add_argument("--thread-id", default="search_session", help="Conversation id")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.question:
        # --question 模式方便课前脚本、CI 或讲师快速验证，不需要人工输入。
        agent = build_agent()
        ask(agent, args.question, args.thread_id)
        return
    run_repl(args.thread_id)


if __name__ == "__main__":
    main()
