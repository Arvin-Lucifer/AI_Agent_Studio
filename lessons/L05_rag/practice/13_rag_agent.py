#!/usr/bin/env python3
"""L05 Step 13: answer questions with retrieved context.

这个脚本对应 RAG 的“在线问答”阶段：
用户问题 -> 检索相关 chunk -> 构造上下文 -> LLM 基于上下文回答。

建议阅读顺序：
1. 先看 retrieve() 的结果：模型回答前到底查到了什么。
2. 再看 format_context()：chunk 如何带着来源进入 prompt。
3. 最后看 answer_with_context()：LLM 如何被要求只基于资料回答。

Usage:
    python practice/13_rag_agent.py --question "我入职2年了，有几天年假？" --show-context
    python practice/13_rag_agent.py --question "代码提交有什么规范？" --no-llm --show-context
"""

from __future__ import annotations

import argparse

from rag_common import answer_with_context, ensure_index, format_context, retrieve


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="L05 local RAG QA")
    parser.add_argument("--question", default="我入职2年了，有几天年假？", help="User question")
    parser.add_argument("--top-k", type=int, default=3, help="Number of retrieved chunks")
    parser.add_argument("--show-context", action="store_true", help="Print retrieved context")
    parser.add_argument("--no-llm", action="store_true", help="Only print retrieval results, do not call LLM")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    index = ensure_index()
    results = retrieve(index, args.question, top_k=args.top_k)
    context = format_context(results)

    print(f"\n[QUESTION] {args.question}")
    if args.show_context or args.no_llm:
        print("\n=== RETRIEVED CONTEXT ===")
        print(context)

    if args.no_llm:
        print("\n[INFO] --no-llm enabled, stop after retrieval.")
        return

    answer = answer_with_context(args.question, context)
    print("\n=== RAG ANSWER ===")
    print(answer)


if __name__ == "__main__":
    main()
