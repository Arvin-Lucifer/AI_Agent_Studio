from __future__ import annotations

from pathlib import Path

from intelligent_customer.config import KB_DIR
from intelligent_customer.rag.kb_builder import build_kb_index
from intelligent_customer.rag.retriever import clear_index_cache, search_kb


def setup_module() -> None:
    build_kb_index()
    clear_index_cache()


def test_knowledge_base_has_at_least_ten_documents() -> None:
    docs = list(Path(KB_DIR).glob("*.md"))
    assert len(docs) >= 10


def test_refund_query_retrieves_policy() -> None:
    results = search_kb("退款需要几天到账？")
    assert results
    assert any(item["collection"] == "policy" for item in results)
    assert any(item["source_id"] == "policy_01" for item in results)


def test_login_failure_retrieves_troubleshoot() -> None:
    results = search_kb("登录失败收不到验证码")
    assert results
    assert any(item["collection"] == "troubleshoot" for item in results)
    assert any(item["source_id"] == "troubleshoot_01" for item in results)

