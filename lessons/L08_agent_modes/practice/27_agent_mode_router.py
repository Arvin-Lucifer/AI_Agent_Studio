#!/usr/bin/env python3
"""L08 Step 27: choose Agent mode for enterprise knowledge-base QA.

这个脚本对应用户补充材料里的“RAG 为主 + ReAct 为辅”。
它不追求复杂模型，而是演示一个工程判断：先用轻量路由决定
direct answer / single RAG / ReAct multi-step，避免所有问题都上重型 Agent。

建议阅读顺序：
1. 先看 classify_question()：理解如何把问题分到不同 Agent 模式。
2. 再看 answer_with_rag()：理解 RAG 主干如何强制引用来源。
3. 最后看 answer_with_react()：理解多跳/跨源/计算问题如何用有限步 ReAct 兜底。

Usage:
    python practice/27_agent_mode_router.py --question "我入职3年有几天年假？"
    python practice/27_agent_mode_router.py --question "P0工单响应时间和API发布审批有什么共同要求？"
"""

from __future__ import annotations

import argparse
from typing import Dict, List

from agent_mode_common import format_citations, rerank_hits, retrieve_from_domains, route_domains


def classify_question(question: str) -> str:
    """轻量路由：决定使用 direct / rag / react。

    企业问答里不建议所有请求都走 ReAct，大多数问题单轮 RAG 就够。
    """
    lower = question.lower()
    multi_hop_markers = ["共同", "比较", "分别", "和", "跨", "同时"]
    compute_markers = ["多少", "合计", "平均", "比例", "增长"]
    if any(marker in lower for marker in multi_hop_markers) and any(
        keyword in lower for keyword in ["工单", "api", "年假", "报销", "审批"]
    ):
        return "react"
    if any(keyword in lower for keyword in ["年假", "入职", "报销", "api", "工单", "pr", "发布"]):
        return "rag"
    if any(marker in lower for marker in compute_markers):
        return "react"
    return "direct"


def answer_direct(question: str) -> Dict[str, object]:
    return {
        "mode": "direct",
        "answer": f"这是通用问题，可直接回答：{question}",
        "citations": [],
        "trace": ["direct: no private knowledge required"],
    }


def answer_with_rag(question: str) -> Dict[str, object]:
    domains = route_domains(question, max_domains=2)
    hits = rerank_hits(question, retrieve_from_domains(question, domains), top_k=3)
    if not hits:
        return {
            "mode": "rag",
            "answer": "未找到可引用证据，不能编造答案。",
            "citations": [],
            "trace": [f"route_domains={domains}", "retrieval=empty"],
        }
    return {
        "mode": "rag",
        "answer": f"根据检索证据回答：{hits[0]['content']}",
        "citations": hits,
        "trace": [f"route_domains={domains}", f"retrieved={len(hits)}"],
    }


def answer_with_react(question: str, max_steps: int = 3) -> Dict[str, object]:
    """有限步 ReAct：拆解 -> 多库检索 -> 综合。

    这里用规则模拟 ReAct trace，重点是讲清“为什么纯 RAG 不够”。
    """
    trace: List[str] = []
    all_hits: List[Dict[str, object]] = []
    sub_queries = [question]
    if "工单" in question and "api" in question.lower():
        sub_queries = ["P0 工单响应时间", "API 发布审批要求"]
    elif "年假" in question and "报销" in question:
        sub_queries = ["年假政策", "差旅报销要求"]

    for step, sub_query in enumerate(sub_queries[:max_steps], 1):
        domains = route_domains(sub_query, max_domains=2)
        trace.append(f"step {step}: search {sub_query!r} in domains={domains}")
        all_hits.extend(retrieve_from_domains(sub_query, domains))

    ranked = rerank_hits(question, all_hits, top_k=4)
    if not ranked:
        return {
            "mode": "react",
            "answer": "多步检索后仍未找到足够证据，建议澄清问题或补充业务域。",
            "citations": [],
            "trace": trace,
        }
    summary = "；".join(item["content"] for item in ranked)
    return {
        "mode": "react",
        "answer": f"经过多步检索和证据合并：{summary}",
        "citations": ranked,
        "trace": trace,
    }


def answer(question: str) -> Dict[str, object]:
    mode = classify_question(question)
    if mode == "direct":
        return answer_direct(question)
    if mode == "rag":
        return answer_with_rag(question)
    return answer_with_react(question)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="L08 Agent mode router")
    parser.add_argument("--question", default="我入职3年有几天年假？")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    result = answer(args.question)
    print(f"[QUESTION] {args.question}")
    print(f"[MODE] {result['mode']}")
    print("\n[TRACE]")
    for item in result["trace"]:
        print(f"- {item}")
    print("\n[ANSWER]")
    print(result["answer"])
    print("\n[CITATIONS]")
    print(format_citations(result["citations"]))


if __name__ == "__main__":
    main()
