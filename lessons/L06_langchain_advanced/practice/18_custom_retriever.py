#!/usr/bin/env python3
"""L06 Step 18: custom hybrid retriever.

这个脚本不依赖 Chroma/FAISS，而是用标准库演示 Retriever 设计思想：
关键词匹配 + 本地稀疏向量检索 + 稳定 key 去重 + 融合排序。

建议阅读顺序：
1. 先看 SAMPLE_DOCS：理解检索候选文档。
2. 再看 LocalHybridRetriever：理解 invoke() 如何返回 Document 列表。
3. 最后看 score 组成：关键词分和向量分如何融合。

Usage:
    python practice/18_custom_retriever.py --query "Python 装饰器怎么用？"
"""

from __future__ import annotations

import argparse
import hashlib
import math
import re
from collections import Counter
from typing import Any, Dict, List

from langchain_core.documents import Document
from langchain_core.runnables import Runnable


SAMPLE_DOCS = [
    {"id": "python-001", "content": "Python 是一种高级编程语言，以简洁的语法和丰富生态著称。", "metadata": {"source": "python.txt", "title": "Python 简介"}},
    {"id": "python-002", "content": "装饰器是 Python 中的高级特性，可在不修改原函数代码的情况下增强函数行为。", "metadata": {"source": "python.txt", "title": "Python 装饰器"}},
    {"id": "langchain-001", "content": "LangChain 是一个用于构建 LLM 应用的框架，核心能力包括 LCEL、工具、检索和 Agent。", "metadata": {"source": "langchain.txt", "title": "LangChain 框架"}},
    {"id": "rag-001", "content": "RAG 通过检索外部知识库增强模型回答，适合企业知识库问答。", "metadata": {"source": "rag.txt", "title": "RAG"}},
]


def tokenize(text: str) -> List[str]:
    """中英文混合切词：英文按词，中文按单字。"""
    return re.findall(r"[A-Za-z0-9_./:-]+|[\u4e00-\u9fff]", text.lower())


def stable_key(item: Dict[str, Any]) -> str:
    """生成稳定去重 key。

    优先使用业务 id；没有 id 时使用规范化完整内容 hash。
    这比 content[:100] 更可靠。
    """
    if item.get("id"):
        return str(item["id"])
    normalized = " ".join(str(item["content"]).split()).lower()
    return hashlib.sha1(normalized.encode("utf-8")).hexdigest()


class LocalHybridRetriever(Runnable):
    """本地混合检索器。

    它不是生产检索器，但展示了自定义 Retriever 最关键的工程点：
    候选召回、去重、融合排序、返回 Document。
    """

    def __init__(self, documents: List[Dict[str, Any]], k: int = 3) -> None:
        self.documents = documents
        self.k = k
        self._idf = self._build_idf(documents)
        self._vectors = [self._vectorize(tokenize(doc["content"])) for doc in documents]
        self._norms = [self._norm(vector) for vector in self._vectors]

    def _build_idf(self, documents: List[Dict[str, Any]]) -> Dict[str, float]:
        doc_freq: Counter[str] = Counter()
        for item in documents:
            doc_freq.update(set(tokenize(item["content"])))
        total = max(1, len(documents))
        return {token: math.log((total + 1) / (freq + 1)) + 1.0 for token, freq in doc_freq.items()}

    def _vectorize(self, tokens: List[str]) -> Dict[str, float]:
        counts = Counter(tokens)
        length = max(1, len(tokens))
        return {token: count / length * self._idf.get(token, 1.0) for token, count in counts.items()}

    def _norm(self, vector: Dict[str, float]) -> float:
        return math.sqrt(sum(value * value for value in vector.values()))

    def _cosine(self, left: Dict[str, float], right: Dict[str, float], right_norm: float) -> float:
        left_norm = self._norm(left)
        if left_norm == 0 or right_norm == 0:
            return 0.0
        dot = sum(value * right.get(token, 0.0) for token, value in left.items())
        return dot / (left_norm * right_norm)

    def invoke(self, input: str, config: Dict[str, Any] | None = None, **kwargs: Any) -> List[Document]:
        """执行检索，返回 LangChain Document 列表。"""
        query_tokens = tokenize(input)
        query_vector = self._vectorize(query_tokens)

        candidates = []
        for doc, vector, norm in zip(self.documents, self._vectors, self._norms):
            content_tokens = set(tokenize(doc["content"]))
            keyword_hits = sum(1 for token in set(query_tokens) if token in content_tokens)
            keyword_score = keyword_hits / max(1, len(set(query_tokens)))
            vector_score = self._cosine(query_vector, vector, norm)

            # 融合排序：向量分负责语义，关键词分负责精确命中。
            final_score = 0.6 * vector_score + 0.4 * keyword_score
            if final_score <= 0:
                continue
            candidates.append(
                {
                    "key": stable_key(doc),
                    "content": doc["content"],
                    "metadata": doc["metadata"],
                    "vector_score": vector_score,
                    "keyword_score": keyword_score,
                    "score": final_score,
                }
            )

        # 用稳定 key 去重，并保留分数最高的候选。
        merged: Dict[str, Dict[str, Any]] = {}
        for item in candidates:
            current = merged.get(item["key"])
            if current is None or item["score"] > current["score"]:
                merged[item["key"]] = item

        ranked = sorted(merged.values(), key=lambda item: item["score"], reverse=True)[: self.k]
        return [
            Document(
                page_content=item["content"],
                metadata={
                    **item["metadata"],
                    "score": round(item["score"], 4),
                    "vector_score": round(item["vector_score"], 4),
                    "keyword_score": round(item["keyword_score"], 4),
                },
            )
            for item in ranked
        ]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="L06 custom retriever demo")
    parser.add_argument("--query", default="Python 装饰器怎么用？")
    parser.add_argument("--top-k", type=int, default=3)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    retriever = LocalHybridRetriever(SAMPLE_DOCS, k=args.top_k)
    docs = retriever.invoke(args.query)
    print(f"[QUERY] {args.query}")
    for index, doc in enumerate(docs, 1):
        print(f"\n--- Result {index} ---")
        print(doc.page_content)
        print(doc.metadata)


if __name__ == "__main__":
    main()
