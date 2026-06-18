#!/usr/bin/env python3
"""L05 Step 14: compare chunk sizes.

这个脚本帮助学生观察：chunk_size 不是随便填一个数字。
同一个问题，在不同切分粒度下可能召回不同内容。

建议阅读顺序：
1. 先看 CHUNK_SIZES：本实验比较哪些切分粒度。
2. 再看 QUESTIONS：这些问题覆盖政策、技术规范和入职流程。
3. 最后看每个 Top1：判断 chunk 是否足够精确、是否带噪声。

Usage:
    python practice/14_chunking_compare.py
"""

from __future__ import annotations

from rag_common import build_index, ensure_sample_docs, load_documents, retrieve, split_documents


CHUNK_SIZES = [200, 500, 1000]
QUESTIONS = [
    "我入职2年了，有几天年假？",
    "代码提交有什么规范？",
    "新员工入职第一天要做什么？",
    "试用期多长？怎么转正？",
]


def main() -> None:
    ensure_sample_docs()
    docs = load_documents()

    for chunk_size in CHUNK_SIZES:
        print(f"\n{'=' * 80}")
        print(f"chunk_size={chunk_size}, chunk_overlap=50")
        print("=" * 80)

        chunks = split_documents(docs, chunk_size=chunk_size, chunk_overlap=50)
        index = build_index(chunks)
        print(f"chunks: {index['chunk_count']}")

        for question in QUESTIONS:
            results = retrieve(index, question, top_k=1)
            if not results:
                print(f"\n[QUESTION] {question}\nTop1: <no result>")
                continue
            top = results[0]
            preview = top["text"].replace("\n", " ")[:160]
            print(f"\n[QUESTION] {question}")
            print(f"Top1: {top['chunk_id']} | score={top['score']:.4f}")
            print(f"Preview: {preview}")


if __name__ == "__main__":
    main()
