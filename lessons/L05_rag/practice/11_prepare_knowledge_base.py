#!/usr/bin/env python3
"""L05 Step 11: prepare a small local knowledge base.

这个脚本对应 RAG 的“数据接入”阶段：
先准备几份可检索文档，后面的索引构建和问答都基于这些文档。

建议阅读顺序：
1. 先看 rag_common.SAMPLE_DOCS：理解示例知识库内容。
2. 再看 ensure_sample_docs()：理解文档如何落到 data/knowledge_base/。
3. 最后看打印结果：确认每个文件都已创建。

Usage:
    python practice/11_prepare_knowledge_base.py
    python practice/11_prepare_knowledge_base.py --overwrite
"""

from __future__ import annotations

import argparse

from rag_common import default_kb_dir, ensure_sample_docs


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="L05 prepare sample knowledge base")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing sample documents")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    paths = ensure_sample_docs(overwrite=args.overwrite)
    print(f"[OK] data/knowledge_base: {default_kb_dir()}")
    for path in paths:
        print(f"- {path.name}")


if __name__ == "__main__":
    main()
