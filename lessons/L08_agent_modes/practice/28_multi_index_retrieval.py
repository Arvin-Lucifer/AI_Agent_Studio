#!/usr/bin/env python3
"""L08 Step 28: multi-index retrieval strategy for enterprise KB.

这个脚本对应补充材料里的“分库分索引策略”。
它演示为什么企业知识库不能只有一个大向量库：权限、语料形态、更新频率和效果调优
都会要求按业务域拆分 collection/index。

建议阅读顺序：
1. 先看 route_domains()：理解业务域路由如何减少检索范围。
2. 再看 retrieve_from_domains()：理解权限过滤为什么必须前置。
3. 最后看 rerank_hits()：理解多库分数不可比，必须统一重排。

Usage:
    python practice/28_multi_index_retrieval.py --query "API发布需要几人审批？"
    python practice/28_multi_index_retrieval.py --query "差旅报销需要什么材料？" --include-confidential
"""

from __future__ import annotations

import argparse

from agent_mode_common import format_citations, rerank_hits, retrieve_from_domains, route_domains


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="L08 multi-index retrieval demo")
    parser.add_argument("--query", default="API发布需要几人审批？")
    parser.add_argument("--include-confidential", action="store_true", help="Allow confidential docs")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    domains = route_domains(args.query, max_domains=3)
    allowed = ("public", "internal", "confidential") if args.include_confidential else ("public", "internal")
    raw_hits = retrieve_from_domains(args.query, domains, allowed_sensitivity=allowed)
    ranked = rerank_hits(args.query, raw_hits, top_k=5)

    print(f"[QUERY] {args.query}")
    print(f"[ROUTED DOMAINS] {domains}")
    print(f"[ALLOWED SENSITIVITY] {allowed}")
    print("\n[RAW HITS]")
    for item in raw_hits:
        print(f"- {item['domain']}/{item['doc_id']} raw_score={item['raw_score']:.4f} {item['title']}")
    print("\n[RERANKED]")
    print(format_citations(ranked))


if __name__ == "__main__":
    main()
