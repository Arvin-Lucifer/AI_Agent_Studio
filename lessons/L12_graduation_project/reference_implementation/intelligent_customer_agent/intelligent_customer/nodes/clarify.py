from __future__ import annotations

from intelligent_customer.harness.observability import log_event
from intelligent_customer.harness.state import AgentState
from intelligent_customer.tools.context_tool import suggest_next_actions


def clarify_node(state: AgentState) -> AgentState:
    question = (
        "为了准确处理，请您补充一下具体业务场景：是账号登录、订单支付、退款售后、套餐价格，"
        "还是产品使用故障？"
    )
    log_event(
        state["trace_id"],
        state["session_id"],
        "fallback.triggered",
        fallback_type="clarification",
    )
    return {
        "route": "clarify",
        "answer": question,
        "need_clarification": True,
        "clarification_question": question,
        "need_human": False,
        "confidence": max(float(state.get("confidence", 0.0)), 0.2),
        "citations": [],
        "metadata": {
            **state.get("metadata", {}),
            "suggested_actions": suggest_next_actions(state["message"], "clarify"),
        },
    }
