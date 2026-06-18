from __future__ import annotations

from intelligent_customer.config import TOP_K
from intelligent_customer.rag.retriever import search_kb
from intelligent_customer.rag.router import route_collections


def kb_search(query: str, collections: list[str] | None = None, k: int = TOP_K) -> list[dict]:
    selected = collections or route_collections(query)
    return search_kb(query=query, collections=selected, k=k)
