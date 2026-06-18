#!/usr/bin/env python3
"""L07 Step 22: short-term memory with summary compression.

这个脚本对应老师讲义 7.2 的“策略二：摘要压缩”。
它把较早的对话压缩成一条 system 摘要，再保留最近几轮原文。

建议阅读顺序：
1. 先看 build_learning_dialogue()：理解哪些信息应该被摘要保留。
2. 再看 smart_memory()：理解“旧摘要 + 新上下文”的消息结构。
3. 最后试试 --use-llm：观察 LLM 摘要和本地兜底摘要的区别。

Usage:
    python practice/22_memory_summary.py
    python practice/22_memory_summary.py --use-llm
"""

from __future__ import annotations

import argparse
from typing import List

from memory_common import (
    Message,
    llm_summarize_conversation,
    local_summarize_conversation,
    smart_memory,
)


def build_learning_dialogue() -> List[Message]:
    """构造老师讲义里的 Python 学习场景。"""
    return [
        {"role": "system", "content": "你是一个耐心的 Python 助手。"},
        {"role": "user", "content": "我想学 Python，应该先学什么？"},
        {"role": "assistant", "content": "建议先从变量、条件判断、循环和函数开始。"},
        {"role": "user", "content": "变量和列表有什么区别？"},
        {"role": "assistant", "content": "变量是名字，列表是一种可以存多个值的数据结构。"},
        {"role": "user", "content": "那 for 循环一般怎么用？"},
        {"role": "assistant", "content": "可以用 for 遍历列表，比如依次处理每个元素。"},
        {"role": "user", "content": "函数参数和返回值我总是容易混。"},
        {"role": "assistant", "content": "参数是输入，返回值是输出，可以把函数理解成一个加工厂。"},
        {"role": "user", "content": "能不能最后再给我一个学习顺序？"},
        {"role": "assistant", "content": "可以，最后我会给你一个从基础到实战的学习路线。"},
    ]


def print_messages(title: str, messages: List[Message]) -> None:
    print(f"\n=== {title} ({len(messages)} 条) ===")
    for index, item in enumerate(messages, 1):
        print(f"{index:02d}. {item['role']}: {item['content']}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="L07 summary memory demo")
    parser.add_argument("--max-recent", type=int, default=4, help="Keep latest N non-system messages")
    parser.add_argument("--use-llm", action="store_true", help="Use LLM to summarize old messages")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    messages = build_learning_dialogue()
    summarizer = llm_summarize_conversation if args.use_llm else local_summarize_conversation
    compressed = smart_memory(messages, max_recent=args.max_recent, summarizer=summarizer)

    print_messages("压缩前", messages)
    print_messages("压缩后", compressed)
    mode = "LLM 摘要" if args.use_llm else "本地摘要兜底"
    print(f"\n摘要模式：{mode}")
    print("观察点：摘要能保留早期关键信息，但细节可能不可逆地丢失。")


if __name__ == "__main__":
    main()
