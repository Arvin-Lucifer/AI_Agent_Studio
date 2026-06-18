from __future__ import annotations

from intelligent_customer.harness.guardrails import is_ambiguous_message
from intelligent_customer.harness.observability import log_event
from intelligent_customer.harness.state import AgentState
from intelligent_customer.rag.query_normalizer import expand_query
from intelligent_customer.schemas import Intent


COMPLAINT_KEYWORDS = [
    "投诉",
    "差评",
    "赔偿",
    "欺骗",
    "虚假",
    "态度差",
    "没人处理",
    "维权",
    "监管",
    "生气",
    "不满意",
]
CONSULT_KEYWORDS = [
    "咨询",
    "了解",
    "多少钱",
    "价格",
    "套餐",
    "版本",
    "政策",
    "适合",
    "购买",
    "开通",
    "企业版",
    "专业版",
    "免费版",
    "sla",
    "售后",
]
DOMAIN_KEYWORDS = [
    "账号",
    "注册",
    "登录",
    "密码",
    "验证码",
    "订单",
    "发票",
    "开票",
    "支付",
    "退款",
    "退回",
    "退钱",
    "退货",
    "换货",
    "隐私",
    "数据",
    "安全",
    "权限",
    "报表",
    "同步",
    "自动化",
    "首次",
    "配置",
    "使用",
    "删除",
    "开通",
    "故障",
    "失败",
    "异常",
    "打不开",
    "转圈",
    "客服",
    "服务",
]
OUT_OF_SCOPE_KEYWORDS = [
    "天气",
    "股票",
    "基金",
    "彩票",
    "电影",
    "菜谱",
    "写代码",
    "论文",
    "医疗",
    "诊断",
    "法律",
    "房价",
    "机票",
]


def classify_text(message: str, memory_summary: str = "") -> Intent:
    current = message.strip().lower()
    expanded_current = expand_query(current).lower()
    text = expand_query(f"{memory_summary} {message}").lower()
    if any(keyword in current for keyword in COMPLAINT_KEYWORDS):
        return "complaint"
    if any(keyword in current for keyword in OUT_OF_SCOPE_KEYWORDS):
        return "out_of_scope"
    if "对公转账" in expanded_current:
        return "qa"
    if is_ambiguous_message(current) and not any(keyword in text for keyword in DOMAIN_KEYWORDS):
        return "unclear"
    if any(keyword in expanded_current for keyword in CONSULT_KEYWORDS):
        return "consult"
    if any(keyword in text for keyword in DOMAIN_KEYWORDS):
        return "qa"
    if is_ambiguous_message(current):
        return "unclear"
    return "out_of_scope"


def classify_intent_node(state: AgentState) -> AgentState:
    intent = classify_text(state["message"], state.get("memory_summary", ""))
    log_event(
        state["trace_id"],
        state["session_id"],
        "intent.classified",
        intent=intent,
    )
    return {"intent": intent}
