#!/usr/bin/env python3
"""L08 Step 26: Supervisor-style multi-agent research team.

这个脚本对应老师讲义 8.3：用 LangGraph 搭建一个 AI 研报团队。
它演示 Supervisor/流水线混合模式：调研员 -> 分析师 -> 撰写员 -> 审核员，
审核不通过则回到撰写员，最多修改 2 次，避免死循环。

建议阅读顺序：
1. 先看 TeamState：理解 Agent 之间通过哪些字段交接。
2. 再看四个 *_agent：理解每个 Agent 的单一职责。
3. 最后看 add_conditional_edges：理解审核通过/返工的控制流。

Usage:
    python practice/26_supervisor_research_team.py
    python practice/26_supervisor_research_team.py --topic "企业知识库问答助手" --use-llm
"""

from __future__ import annotations

import argparse
from typing import Literal, TypedDict

from langgraph.graph import END, START, StateGraph

from agent_mode_common import run_role_prompt


class TeamState(TypedDict, total=False):
    topic: str
    research_data: str
    analysis: str
    report: str
    review_feedback: str
    is_approved: bool
    revision_count: int
    use_llm: bool


def researcher_agent(state: TeamState) -> dict:
    """调研员：负责搜集和整理信息。"""
    topic = state["topic"]
    fallback = (
        f"主题：{topic}\n"
        "- 行业概况：企业正在把知识库、工单、制度和研发文档接入 AI 助手。\n"
        "- 关键数据点：知识更新频繁；权限要求高；答案需要引用来源。\n"
        "- 当前趋势：RAG 主干、混合检索、按域分库、轻量 Agent 路由。\n"
        "- 主要挑战：权限隔离、检索噪声、跨源融合、无证据时拒答。"
    )
    prompt = f"请针对主题“{topic}”整理行业概况、关键数据点、趋势和挑战。"
    return {"research_data": run_role_prompt("资深行业调研员", prompt, fallback, state.get("use_llm", False))}


def analyst_agent(state: TeamState) -> dict:
    """分析师：基于调研数据提炼机会、风险和判断。"""
    fallback = (
        "关键趋势分析：企业知识库问答正在从单轮 RAG 走向 RAG + ReAct 的混合模式。\n"
        "机会点：分库分索引能提升召回质量，引用和审计能提升可信度。\n"
        "风险提醒：多 Agent 或大循环会增加 token、延迟和错误传播。\n"
        "量化预测：优先治理高频 60%-80% 问题，可先获得明显 ROI。"
    )
    prompt = f"基于调研数据做分析：\n{state['research_data']}"
    return {"analysis": run_role_prompt("数据分析师", prompt, fallback, state.get("use_llm", False))}


def writer_agent(state: TeamState) -> dict:
    """撰写员：把调研和分析组织成最终报告。"""
    feedback_hint = f"\n修改意见：{state.get('review_feedback', '')}" if state.get("review_feedback") else ""
    fallback = (
        f"# {state['topic']}简版研报\n\n"
        "## 摘要\n"
        "企业知识库问答助手应以 RAG 保证可信与可追溯，以 ReAct 处理多跳、跨源和计算型长尾问题。\n\n"
        "## 行业概况\n"
        f"{state['research_data']}\n\n"
        "## 趋势分析\n"
        f"{state['analysis']}\n\n"
        "## 结论建议\n"
        "建议先按业务域完成 3-5 个核心库的分库分索引，再用规则路由和 rerank 跑通闭环。"
    )
    prompt = (
        f"主题：{state['topic']}\n调研数据：{state['research_data']}\n"
        f"分析结论：{state['analysis']}{feedback_hint}\n请写一份 500 字以内报告。"
    )
    return {"report": run_role_prompt("专业报告撰写专家", prompt, fallback, state.get("use_llm", False))}


def reviewer_agent(state: TeamState) -> dict:
    """审核员：质量把关，并决定是否返工。"""
    revision_count = state.get("revision_count", 0) + 1
    report = state.get("report", "")
    has_required_parts = all(keyword in report for keyword in ["摘要", "趋势", "结论"])
    is_approved = has_required_parts or revision_count >= 3
    fallback = (
        "评分：8/10\n状态：APPROVED\n修改建议：报告结构完整，建议补充更多真实数据引用。"
        if is_approved
        else "评分：6/10\n状态：NEEDS_REVISION\n修改建议：请补充摘要、趋势分析和结论建议。"
    )
    prompt = f"请审核以下报告并输出 APPROVED 或 NEEDS_REVISION：\n{report}"
    feedback = run_role_prompt("严格的报告审核员", prompt, fallback, state.get("use_llm", False))
    approved_by_content = "APPROVED" in feedback and "NEEDS_REVISION" not in feedback
    if revision_count >= 3:
        approved_by_content = True
        feedback += "\n备注：已达到最大修改次数，强制结束。"
    return {
        "review_feedback": feedback,
        "is_approved": approved_by_content,
        "revision_count": revision_count,
    }


def supervisor_route(state: TeamState) -> Literal["end", "revise"]:
    """主管决策：审核通过结束，否则回到 writer。"""
    return "end" if state.get("is_approved", False) else "revise"


def build_graph():
    graph = StateGraph(TeamState)
    graph.add_node("researcher", researcher_agent)
    graph.add_node("analyst", analyst_agent)
    graph.add_node("writer", writer_agent)
    graph.add_node("reviewer", reviewer_agent)
    graph.add_edge(START, "researcher")
    graph.add_edge("researcher", "analyst")
    graph.add_edge("analyst", "writer")
    graph.add_edge("writer", "reviewer")
    graph.add_conditional_edges("reviewer", supervisor_route, {"end": END, "revise": "writer"})
    return graph.compile()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="L08 supervisor multi-agent research team")
    parser.add_argument("--topic", default="企业知识库问答助手设计")
    parser.add_argument("--use-llm", action="store_true", help="Use real LLM instead of deterministic mock")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    team = build_graph()
    result = team.invoke({"topic": args.topic, "revision_count": 0, "use_llm": args.use_llm})
    print("=== FINAL REPORT ===")
    print(result["report"])
    print("\n=== REVIEW ===")
    print(result["review_feedback"])
    print(f"\nrevision_count={result['revision_count']}")


if __name__ == "__main__":
    main()
