#!/usr/bin/env python3
"""L07 Step 21: short-term memory with sliding window.

这个脚本对应老师讲义 7.2 的“策略一：滑动窗口”。
它演示如何只保留最近 N 轮对话，同时始终保留 system 消息。

建议阅读顺序：
1. 先看 build_demo_messages()：理解一段长对话长什么样。
2. 再看 sliding_window_memory() 的调用：理解 N 轮对话如何换算成消息条数。
3. 最后看输出：观察早期信息为什么会被丢失。

Usage:
    python practice/21_memory_window.py
    python practice/21_memory_window.py --max-turns 3
"""

from __future__ import annotations

import argparse
from typing import List

from memory_common import Message, sliding_window_memory


def build_demo_messages(total_turns: int = 12) -> List[Message]:
    """构造一段长对话。

    第 1 轮故意放入“用户姓名”，用于观察滑动窗口的缺点：
    只保留最近 N 轮时，早期但重要的信息可能被裁掉。
    """
    messages: List[Message] = [{"role": "system", "content": "你是一个耐心的 Python 学习助手。"}]
    for index in range(1, total_turns + 1):
        if index == 1:
            user_content = "我叫小明，想系统学习 Python。"
        else:
            user_content = f"第 {index} 个问题：请解释一个 Python 知识点。"
        messages.append({"role": "user", "content": user_content})
        messages.append({"role": "assistant", "content": f"第 {index} 个回答：这是对应的解释。"})
    return messages


def print_messages(title: str, messages: List[Message]) -> None:
    print(f"\n=== {title} ({len(messages)} 条) ===")
    for index, item in enumerate(messages, 1):
        print(f"{index:02d}. {item['role']}: {item['content']}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="L07 sliding window memory demo")
    parser.add_argument("--max-turns", type=int, default=5, help="Keep latest N user/assistant turns")
    parser.add_argument("--total-turns", type=int, default=12, help="Build N demo turns")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    messages = build_demo_messages(total_turns=args.total_turns)
    trimmed = sliding_window_memory(messages, max_turns=args.max_turns)

    print_messages("裁剪前", messages)
    print_messages(f"裁剪后：最近 {args.max_turns} 轮", trimmed)
    print("\n观察点：system 消息仍在，但第 1 轮里的姓名可能已经被裁掉。")


if __name__ == "__main__":
    main()
