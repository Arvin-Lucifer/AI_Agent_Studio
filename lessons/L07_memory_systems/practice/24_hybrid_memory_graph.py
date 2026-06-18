#!/usr/bin/env python3
"""L07 Step 24: hybrid long-term memory with graph relations.

这个脚本对应老师讲义 7.3.3 的“向量检索 + 知识图谱”思想。
课堂默认版不用 Chroma，而是用标准库稀疏检索模拟“语义入口”，再用 JSON KG 做多跳扩展。

建议阅读顺序：
1. 先看 seed_hybrid_memory()：理解实体、关系和事实如何双写。
2. 再看 vector_search() 输出：理解文本检索如何找入口。
3. 最后看 graph_search()/find_path()：理解图谱如何做关系扩展和路径推理。

Usage:
    python practice/24_hybrid_memory_graph.py --reset
    python practice/24_hybrid_memory_graph.py --query Python --anchor 小明
"""

from __future__ import annotations

import argparse

from memory_common import HybridLongTermMemory, default_hybrid_memory_path, default_kg_path


def seed_hybrid_memory(memory: HybridLongTermMemory) -> None:
    """写入老师讲义里的小明、用户中心项目、FastAPI 关系网络。"""
    memory.update_profile("name", "小明")
    memory.update_profile("role", "后端工程师")
    memory.save_preference("编程语言", "喜欢用 Python", importance=8)
    memory.save_preference("回答风格", "喜欢简洁的回答，带代码示例", importance=7)

    memory.add_entity("小明", etype="person")
    memory.add_entity("用户中心项目", etype="project")
    memory.add_entity("FastAPI", etype="tech")
    memory.add_entity("团队A", etype="org")
    memory.add_entity("Web 框架", etype="category")

    memory.add_relation("小明", "负责", "用户中心项目")
    memory.add_relation("小明", "属于", "团队A")
    memory.add_relation("用户中心项目", "使用", "FastAPI")
    memory.add_relation("FastAPI", "属于类型", "Web 框架")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="L07 hybrid memory graph demo")
    parser.add_argument("--query", default="Python", help="Text query")
    parser.add_argument("--anchor", default="小明", help="Graph anchor entity")
    parser.add_argument("--hops", type=int, default=2, help="Graph expansion hops")
    parser.add_argument("--reset", action="store_true", help="Recreate demo files")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    for path in (default_hybrid_memory_path(), default_kg_path()):
        if args.reset and path.exists():
            path.unlink()

    memory = HybridLongTermMemory()
    if args.reset or not memory.kg.data["relations"]:
        seed_hybrid_memory(memory)

    print(f"[MEMORY FILE] {default_hybrid_memory_path()}")
    print(f"[KG FILE] {default_kg_path()}")

    print(f"\n=== 文本检索：query={args.query!r} ===")
    for index, hit in enumerate(memory.vector_search(args.query, k=3), 1):
        print(f"{index}. [{hit.source}] score={hit.score:.4f} {hit.content}")

    print(f"\n=== 图谱扩展：anchor={args.anchor!r}, hops={args.hops} ===")
    for relation in memory.kg.graph_search(args.anchor, hops=args.hops):
        print(f"({relation['subject']}) -[{relation['predicate']}]-> ({relation['object']})")

    print(f"\n=== 路径推理：{args.anchor!r} -> 'FastAPI' ===")
    paths = memory.kg.find_path(args.anchor, "FastAPI", max_hops=3)
    for path in paths:
        chain = " -> ".join(
            f"({item['subject']})-[{item['predicate']}]->({item['object']})"
            for item in path
        )
        print(chain)
    if not paths:
        print("没有找到路径。")

    print(f"\n=== 混合检索：query={args.query!r}, anchor={args.anchor!r} ===")
    result = memory.hybrid_search(args.query, k=3, hops=args.hops, anchor_entities=[args.anchor])
    print(f"入口实体：{result['anchors']}")
    print("图谱扩展结果数：", len(result["graph"]))


if __name__ == "__main__":
    main()
