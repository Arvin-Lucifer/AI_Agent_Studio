#!/usr/bin/env python3
"""L04 Step 7: build a basic LangChain/LangGraph tool Agent.

这个脚本用 create_agent 重写 L03 的手写工具循环：
模型、工具和 Prompt 仍由我们设计，但工具调用循环交给框架执行。

读代码时请抓住三层：
1. SYSTEM_PROMPT 负责告诉模型“你是谁、什么时候用工具”。
2. DEFAULT_TOOLS 负责告诉模型“你有哪些外部能力”。
3. create_agent 负责执行“模型思考 -> 工具调用 -> 工具结果 -> 最终回答”的循环。

Usage:
    python practice/07_langchain_agent.py "北京天气怎么样？"
    python practice/07_langchain_agent.py --show-trace "现在几点？再算一下 3*7。"
"""

from __future__ import annotations

import argparse
from typing import Any, Dict

from langchain.agents import create_agent

from langchain_common import DEFAULT_TOOLS, build_llm, final_text, print_message_trace


# 这是 Agent 的行为说明书。
# 如果这里不写“需要真实数据或计算时调用工具”，模型可能会凭常识直接回答，
# 学生就观察不到工具调用路径。
SYSTEM_PROMPT = (
    "你是一个有用的助手，可以查天气、看时间、做计算。"
    "需要真实数据或计算时调用工具；不需要工具时直接回答。回答要简洁友好。"
)


def build_agent() -> Any:
    """创建 Agent；这里的一行封装了 L03 手写的循环逻辑。"""
    llm = build_llm()

    # L03 里我们自己写 while 循环、解析 tool_calls、执行工具、回填 tool result。
    # create_agent 把这些通用流程封装起来；我们只需要传入模型、工具和系统提示词。
    return create_agent(
        model=llm,
        tools=DEFAULT_TOOLS,
        system_prompt=SYSTEM_PROMPT,
    )


def run_agent(prompt: str, show_trace: bool = False) -> str:
    """运行一次 Agent；输入仍然是 messages，符合前几讲建立的消息模型。"""
    agent = build_agent()

    # invoke 的输入仍然是 messages，这一点和 L01-L03 保持连续：
    # user 消息进入 Agent，Agent 内部可能追加 assistant/tool 等消息。
    result: Dict[str, Any] = agent.invoke(
        {"messages": [{"role": "user", "content": prompt}]}
    )
    if show_trace:
        # --show-trace 是本节最值得多试的开关：它能看到中间 tool_calls。
        print_message_trace(result)

    # result 是完整状态，不是最终文本；final_text 只取最后一条消息给用户看。
    answer = final_text(result)
    print(f"\n[USER] {prompt}")
    print(f"[ASSISTANT] {answer}")
    return answer


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="L04 basic LangChain Agent")
    parser.add_argument("prompt", nargs="?", default="北京天气怎么样？适合跑步吗？", help="User prompt")
    parser.add_argument("--show-trace", action="store_true", help="Print intermediate messages")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_agent(args.prompt, show_trace=args.show_trace)


if __name__ == "__main__":
    main()
