#!/usr/bin/env python3
"""L07 Step 23: long-term memory persisted as JSON.

这个脚本对应老师讲义 7.3.1 的 JSON 长期记忆。
它演示跨会话保存用户画像、偏好和事实，并支持关键词检索和显式遗忘。

建议阅读顺序：
1. 先看 seed_memory()：理解 profile/facts/preferences 三类记忆的区别。
2. 再看 LongTermMemory.search()：理解最小检索如何工作。
3. 最后试试 --forget：理解长期记忆为什么必须支持删除。

Usage:
    python practice/23_long_term_memory_json.py --reset
    python practice/23_long_term_memory_json.py --query Python
    python practice/23_long_term_memory_json.py --forget Python
"""

from __future__ import annotations

import argparse

from memory_common import LongTermMemory, default_json_memory_path


def seed_memory(memory: LongTermMemory) -> None:
    """写入老师讲义里的示例记忆。"""
    memory.update_profile("name", "小明")
    memory.update_profile("role", "后端工程师")
    memory.save_preference("编程语言", "喜欢用 Python", importance=8)
    memory.save_preference("回答风格", "喜欢简洁的回答，带代码示例", importance=7)
    memory.save_fact("小明负责用户中心项目", "work", importance=8)
    memory.save_fact("团队用 FastAPI 做后端", "tech", importance=7)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="L07 JSON long-term memory demo")
    parser.add_argument("--query", default="Python", help="Keyword to search")
    parser.add_argument("--reset", action="store_true", help="Recreate demo memory file")
    parser.add_argument("--forget", default="", help="Soft delete memories containing keyword")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    path = default_json_memory_path()
    if args.reset and path.exists():
        path.unlink()

    memory = LongTermMemory(path)
    if args.reset or not path.exists() or not memory.memories["facts"]:
        seed_memory(memory)

    if args.forget:
        deleted = memory.forget(args.forget)
        print(f"[FORGET] query={args.forget!r}, deleted={deleted}")

    print(f"[MEMORY FILE] {path}")
    print("\n=== 用户画像 ===")
    print(memory.get_profile_summary())

    print(f"\n=== 搜索：{args.query!r} ===")
    results = memory.search(args.query)
    for index, item in enumerate(results, 1):
        print(f"{index}. [{item['type']}] {item}")
    if not results:
        print("没有命中。")


if __name__ == "__main__":
    main()
