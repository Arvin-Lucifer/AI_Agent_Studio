from __future__ import annotations

from intelligent_customer.rag.query_normalizer import expand_query
from intelligent_customer.tools.context_tool import rewrite_contextual_query, suggest_next_actions


def test_rewrite_contextual_query_uses_recent_user_topic() -> None:
    history = [
        {"role": "user", "content": "专业版和企业版有什么区别？"},
        {"role": "assistant", "content": "从当前产品资料看..."},
    ]
    rewritten = rewrite_contextual_query("那 SLA 呢？", history)
    assert rewritten["rewritten"] is True
    assert "企业版" in rewritten["query"] or "专业版" in rewritten["query"]
    assert "SLA" in rewritten["query"]


def test_rewrite_contextual_query_leaves_standalone_question_unchanged() -> None:
    rewritten = rewrite_contextual_query("忘记密码怎么找回？", [])
    assert rewritten["rewritten"] is False
    assert rewritten["query"] == "忘记密码怎么找回？"


def test_suggest_next_actions_follow_domain() -> None:
    assert "了解企业版 SLA" in suggest_next_actions("企业版价格是多少？", "retrieve")
    assert "补充订单号" in suggest_next_actions("我要投诉", "ticket", need_human=True, ticket_id="T-1")


def test_expand_query_maps_colloquial_customer_words() -> None:
    assert "退款" in expand_query("钱什么时候能退回来？")
    assert "验证码" in expand_query("短信码一直收不到")
    assert "发票" in expand_query("开票抬头填错了")
    assert "登录失败" in expand_query("一直转圈打不开页面")
