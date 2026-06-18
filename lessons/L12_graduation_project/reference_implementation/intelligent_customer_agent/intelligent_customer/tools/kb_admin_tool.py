from __future__ import annotations

import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from intelligent_customer.config import KB_DIR, ensure_runtime_dirs
from intelligent_customer.rag.kb_builder import build_kb_index, parse_frontmatter
from intelligent_customer.rag.retriever import clear_index_cache


def _safe_source_id(value: str) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9_\-]+", "_", value.strip().lower()).strip("_")
    return cleaned[:80] or f"kb_{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}"


def _doc_path(source_id: str) -> Path:
    return KB_DIR / f"{source_id}.md"


def _unique_source_id(source_id: str) -> str:
    candidate = _safe_source_id(source_id)
    if not _doc_path(candidate).exists():
        return candidate
    suffix = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
    return _safe_source_id(f"{candidate}_{suffix}")


def _read_doc(path: Path) -> dict[str, Any]:
    raw = path.read_text(encoding="utf-8")
    metadata, body = parse_frontmatter(raw)
    source_id = metadata.get("source_id") or path.stem
    return {
        "source_id": source_id,
        "title": metadata.get("title") or path.stem,
        "collection": metadata.get("collection") or path.stem.split("_", 1)[0],
        "updated_at": metadata.get("updated_at") or "",
        "path": str(path),
        "content": body,
        "char_count": len(body),
    }


def list_kb_documents() -> list[dict[str, Any]]:
    ensure_runtime_dirs()
    docs = [_read_doc(path) for path in sorted(KB_DIR.glob("*.md"))]
    return sorted(docs, key=lambda item: (item["collection"], item["source_id"]))


def get_kb_document(source_id: str) -> dict[str, Any] | None:
    ensure_runtime_dirs()
    for path in sorted(KB_DIR.glob("*.md")):
        doc = _read_doc(path)
        if doc["source_id"] == source_id or path.stem == source_id:
            return doc
    return None


def create_kb_document(
    title: str,
    collection: str,
    content: str,
    source_id: str | None = None,
    gap_id: str | None = None,
) -> dict[str, Any]:
    ensure_runtime_dirs()
    base_source = source_id or f"{collection}_{title}"
    final_source_id = _unique_source_id(base_source)
    updated_at = datetime.now(timezone.utc).date().isoformat()
    body = content.strip()
    frontmatter = "\n".join(
        [
            "---",
            f"title: {title.strip()}",
            f"collection: {collection}",
            f"source_id: {final_source_id}",
            f"updated_at: {updated_at}",
            f"gap_id: {gap_id}" if gap_id else "",
            "---",
            "",
        ]
    )
    text = f"{frontmatter}{body}\n"
    path = _doc_path(final_source_id)
    path.write_text(text, encoding="utf-8")
    index = build_kb_index()
    clear_index_cache()
    doc = _read_doc(path)
    doc["index_doc_count"] = index["doc_count"]
    return doc


def rebuild_kb() -> dict[str, Any]:
    index = build_kb_index()
    clear_index_cache()
    return {"status": "ok", "doc_count": index["doc_count"]}
