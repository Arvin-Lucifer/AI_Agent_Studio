#!/usr/bin/env python3
"""Shared helpers for L08 Agent mode demos.

第 8 章的总主题是“Agent 模式”：什么时候用单 Agent、RAG、ReAct、多 Agent，
以及企业知识库问答里如何做路由和分库分索引。

建议阅读顺序：
1. 先看 build_llm()/run_role_prompt()：理解示例如何在 mock 和真实 LLM 之间切换。
2. 再看 KNOWLEDGE_BASES：理解企业知识库为什么要按业务域拆开。
3. 最后看 retrieve_from_domains()/rerank_hits()：理解多库召回后为什么还要统一重排。
"""

from __future__ import annotations

import os
import re
from collections import Counter
from pathlib import Path
from typing import Any, Dict, Iterable, List

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI


def find_project_root() -> Path:
    """从当前文件向上寻找课程根目录，保证所有示例使用同一份 .env。"""
    for parent in Path(__file__).resolve().parents:
        if (parent / ".env").exists() or (parent / ".env.example").exists():
            return parent
    raise RuntimeError("Cannot find project root with .env or .env.example")


def load_project_env() -> None:
    """加载课程根目录 .env；不覆盖 shell 中临时设置的环境变量。"""
    load_dotenv(find_project_root() / ".env", override=False)


def _read_int_env(name: str, default: int) -> int:
    raw = os.getenv(name, "").strip()
    if not raw:
        return default
    try:
        value = int(raw)
        return value if value >= 1 else default
    except Exception:
        print(f"[WARN] Invalid {name}={raw!r}, fallback to {default}")
        return default


def _read_float_env(name: str, default: float) -> float:
    raw = os.getenv(name, "").strip()
    if not raw:
        return default
    try:
        value = float(raw)
        return value if value > 0 else default
    except Exception:
        print(f"[WARN] Invalid {name}={raw!r}, fallback to {default}")
        return default


def build_llm() -> ChatOpenAI:
    """创建 ChatOpenAI；仅在脚本显式传入 --use-llm 时调用。"""
    load_project_env()
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    base_url = os.getenv("OPENAI_BASE_URL", "").strip()
    model = os.getenv("OPENAI_MODEL", "").strip()
    missing = [
        name
        for name, value in {
            "OPENAI_API_KEY": api_key,
            "OPENAI_BASE_URL": base_url,
            "OPENAI_MODEL": model,
        }.items()
        if not value
    ]
    if missing:
        raise RuntimeError(f"Missing required env vars: {', '.join(missing)}")
    return ChatOpenAI(
        model=model,
        temperature=0.2,
        api_key=api_key,
        base_url=base_url,
        timeout=_read_float_env("AGENT_MODE_TIMEOUT_SEC", 60.0),
        max_retries=_read_int_env("AGENT_MODE_MAX_RETRIES", 1),
    )


def run_role_prompt(role: str, prompt: str, fallback: str, use_llm: bool = False) -> str:
    """运行一个角色 Agent。

    默认 mock 是为了让第 8 章课前脚本稳定、低成本；真实课堂演示可以加 --use-llm。
    """
    if not use_llm:
        return fallback
    llm = build_llm()
    response = llm.invoke(f"你是{role}。\n\n{prompt}")
    return str(response.content)


def tokenize(text: str) -> List[str]:
    """中英文混合切词，服务于课堂版关键词检索。"""
    return re.findall(r"[A-Za-z0-9_./:-]+|[\u4e00-\u9fff]", text.lower())


def keyword_score(query: str, content: str) -> float:
    query_tokens = set(tokenize(query))
    if not query_tokens:
        return 0.0
    content_tokens = set(tokenize(content))
    return sum(1 for token in query_tokens if token in content_tokens) / len(query_tokens)


# 课堂版分库数据：真实企业里会替换为独立 collection/index、数据库、工单系统或文档平台。
# 每条数据都带 domain/sensitivity/version，方便演示“分库 + 元数据过滤 + 统一 rerank”。
KNOWLEDGE_BASES: Dict[str, List[Dict[str, Any]]] = {
    "hr": [
        {
            "doc_id": "hr-001",
            "title": "年假政策",
            "content": "入职满1年享有5天年假，满3年享有10天，满5年享有15天。",
            "sensitivity": "internal",
            "version": "2026.01",
            "tags": ["休假", "年假"],
        },
        {
            "doc_id": "hr-002",
            "title": "入职流程",
            "content": "新员工第一天领取工卡、完成 HR 手续，并由 IT 分配账号。",
            "sensitivity": "internal",
            "version": "2026.01",
            "tags": ["入职"],
        },
    ],
    "finance": [
        {
            "doc_id": "fin-001",
            "title": "差旅报销",
            "content": "差旅报销需在出差结束后10个工作日内提交发票和审批单。",
            "sensitivity": "confidential",
            "version": "2026.02",
            "tags": ["报销", "差旅"],
        }
    ],
    "engineering": [
        {
            "doc_id": "eng-001",
            "title": "API 发布规范",
            "content": "生产 API 发布需要至少2人审批，并准备回滚方案。",
            "sensitivity": "internal",
            "version": "2026.03",
            "tags": ["API", "发布"],
        },
        {
            "doc_id": "eng-002",
            "title": "PR 规范",
            "content": "每个 PR 建议不超过500行变更，并写明测试方式和影响范围。",
            "sensitivity": "internal",
            "version": "2026.03",
            "tags": ["代码", "PR"],
        },
    ],
    "support": [
        {
            "doc_id": "sup-001",
            "title": "客户工单 SLA",
            "content": "P0 工单需15分钟内响应，P1 工单需2小时内响应。",
            "sensitivity": "internal",
            "version": "hot",
            "tags": ["工单", "SLA"],
        }
    ],
}


DOMAIN_KEYWORDS = {
    "hr": ["年假", "入职", "员工", "休假", "病假"],
    "finance": ["报销", "发票", "预算", "付款", "差旅"],
    "engineering": ["api", "代码", "发布", "pr", "回滚", "接口"],
    "support": ["工单", "客户", "sla", "投诉", "售后"],
}


def route_domains(query: str, max_domains: int = 2) -> List[str]:
    """规则路由：用关键词把问题收敛到 1-2 个业务域。

    企业场景里规则路由通常覆盖高频 60% 流量，便宜、稳定、可解释。
    """
    query_lower = query.lower()
    scores = []
    for domain, keywords in DOMAIN_KEYWORDS.items():
        score = sum(1 for keyword in keywords if keyword.lower() in query_lower)
        if score:
            scores.append((domain, score))
    if not scores:
        return ["hr", "engineering"][:max_domains]
    scores.sort(key=lambda item: item[1], reverse=True)
    return [domain for domain, _ in scores[:max_domains]]


def retrieve_from_domains(
    query: str,
    domains: Iterable[str],
    allowed_sensitivity: Iterable[str] = ("public", "internal"),
) -> List[Dict[str, Any]]:
    """从多个业务域并行召回候选文档。

    这里用循环模拟多库并行；真实实现会对多个 collection/index 并发查询。
    """
    allowed = set(allowed_sensitivity)
    hits: List[Dict[str, Any]] = []
    for domain in domains:
        for doc in KNOWLEDGE_BASES.get(domain, []):
            if doc["sensitivity"] not in allowed:
                continue
            score = keyword_score(query, f"{doc['title']} {doc['content']} {' '.join(doc['tags'])}")
            if score > 0:
                hits.append({**doc, "domain": domain, "raw_score": score})
    return hits


def rerank_hits(query: str, hits: List[Dict[str, Any]], top_k: int = 3) -> List[Dict[str, Any]]:
    """统一 rerank。

    不同库的原始分数不可直接比较，因此多库召回后必须重新排序或归一。
    """
    query_tokens = Counter(tokenize(query))
    ranked = []
    for hit in hits:
        content = f"{hit['title']} {hit['content']}"
        content_tokens = Counter(tokenize(content))
        overlap = sum(min(count, content_tokens.get(token, 0)) for token, count in query_tokens.items())
        final_score = 0.7 * float(hit["raw_score"]) + 0.3 * (overlap / max(1, sum(query_tokens.values())))
        ranked.append({**hit, "score": round(final_score, 4)})
    return sorted(ranked, key=lambda item: item["score"], reverse=True)[:top_k]


def format_citations(hits: Iterable[Dict[str, Any]]) -> str:
    """把检索结果格式化为可追溯引用。"""
    lines = []
    for item in hits:
        lines.append(
            f"- [{item['domain']}/{item['doc_id']} v{item['version']}] {item['title']}: {item['content']}"
        )
    return "\n".join(lines) if lines else "- 未找到可引用证据"
