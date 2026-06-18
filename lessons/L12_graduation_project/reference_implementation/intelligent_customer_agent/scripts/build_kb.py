from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from intelligent_customer.rag.kb_builder import build_kb_index
from intelligent_customer.rag.retriever import clear_index_cache


def main() -> int:
    index = build_kb_index()
    clear_index_cache()
    print(f"Built knowledge base index: {index['doc_count']} documents")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
