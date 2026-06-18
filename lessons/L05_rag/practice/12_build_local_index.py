#!/usr/bin/env python3
"""L05 Step 12: build a local RAG retrieval index.

这个脚本对应 RAG 的“离线建库”阶段：
文档 -> 清洗 -> chunk -> 数字特征 -> 本地索引。

建议阅读顺序：
1. 先看 build_and_save_index()：它串起离线建库流程。
2. 再看 retrieve()：它模拟在线阶段的 TopK 召回。
3. 最后观察打印结果：判断检索是否命中了正确来源。

Usage:
    python practice/12_build_local_index.py --query "年假有几天？"
"""

from __future__ import annotations

import argparse

from rag_common import build_and_save_index, default_index_path, retrieve


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="L05 build local RAG index")
    parser.add_argument("--query", default="年假有几天？", help="Query used to test retrieval")
    parser.add_argument("--chunk-size", type=int, default=300, help="Max characters per chunk")
    parser.add_argument("--chunk-overlap", type=int, default=50, help="Overlap characters between chunks")
    parser.add_argument("--top-k", type=int, default=3, help="Number of chunks to retrieve")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    index = build_and_save_index(chunk_size=args.chunk_size, chunk_overlap=args.chunk_overlap)
    print(f"[OK] index saved: {default_index_path()}")
    print(f"[OK] chunks: {index['chunk_count']}")

    print(f"\n[QUERY] {args.query}")
    results = retrieve(index, args.query, top_k=args.top_k)
    for rank, item in enumerate(results, 1):
        print(f"\n--- Top {rank} | score={item['score']:.4f} | {item['chunk_id']} ---")
        print(item["text"][:300])


if __name__ == "__main__":
    main()
