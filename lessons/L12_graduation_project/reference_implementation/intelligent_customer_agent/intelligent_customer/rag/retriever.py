from __future__ import annotations

import json
import math
from functools import lru_cache
from pathlib import Path
from typing import Any

from intelligent_customer.config import KB_DIR, KB_INDEX_PATH
from intelligent_customer.rag.kb_builder import build_kb_index, tokenize
from intelligent_customer.rag.query_normalizer import expand_query
from intelligent_customer.rag.router import route_collections


def _load_index(path: Path = KB_INDEX_PATH) -> dict[str, Any]:
    if not path.exists():
        build_kb_index(KB_DIR, path)
    return json.loads(path.read_text(encoding="utf-8"))


@lru_cache(maxsize=1)
def load_index_cached() -> dict[str, Any]:
    return _load_index()


def clear_index_cache() -> None:
    load_index_cached.cache_clear()


def _score_document(query: str, query_tokens: list[str], doc: dict[str, Any]) -> float:
    if not query_tokens:
        return 0.0
    doc_tokens = doc.get("tokens", [])
    doc_token_set = set(doc_tokens)
    raw = 0.0
    for token in set(query_tokens):
        if len(token) == 1:
            raw += 0.35 if token in doc_token_set else 0.0
        elif token in doc_token_set:
            raw += 1.2
    lowered_doc = f"{doc.get('title', '')}\n{doc.get('content', '')}".lower()
    lowered_query = query.lower()
    for term in set([t for t in query_tokens if len(t) >= 2]):
        if term in lowered_doc:
            raw += 1.8
    if doc.get("title", "").lower() and any(part in lowered_query for part in doc["title"].lower().split()):
        raw += 0.8
    length_penalty = math.log(len(doc_tokens) + 10)
    return raw / max(length_penalty, 1.0)


def _snippet(content: str, query_tokens: list[str], max_chars: int = 280) -> str:
    lines = [line.strip() for line in content.splitlines() if line.strip() and not line.startswith("#")]
    scored: list[tuple[int, str]] = []
    for line in lines:
        score = sum(1 for token in set(query_tokens) if len(token) >= 2 and token in line.lower())
        if score:
            scored.append((score, line))
    chosen = [line for _, line in sorted(scored, reverse=True)[:3]] or lines[:3]
    text = " ".join(chosen)
    return text[:max_chars]


def search_kb(query: str, collections: list[str] | None = None, k: int = 4) -> list[dict[str, Any]]:
    index = load_index_cached()
    docs = index.get("documents", [])
    expanded_query = expand_query(query)
    selected = collections or route_collections(expanded_query)
    query_tokens = tokenize(expanded_query)
    results: list[dict[str, Any]] = []
    for doc in docs:
        if selected and doc.get("collection") not in selected:
            continue
        raw_score = _score_document(expanded_query, query_tokens, doc)
        if raw_score <= 0:
            continue
        score = max(0.0, min(1.0, raw_score / 3.2))
        results.append(
            {
                "source_id": doc["source_id"],
                "title": doc["title"],
                "collection": doc["collection"],
                "score": round(score, 4),
                "content": _snippet(doc["content"], query_tokens),
                "path": doc["path"],
            }
        )
    results.sort(key=lambda item: item["score"], reverse=True)
    return results[:k]
