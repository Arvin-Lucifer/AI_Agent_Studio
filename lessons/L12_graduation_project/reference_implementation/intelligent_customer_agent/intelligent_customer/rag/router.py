from __future__ import annotations

from collections import OrderedDict

from intelligent_customer.rag.query_normalizer import expand_query


COLLECTION_KEYWORDS: dict[str, list[str]] = {
    "faq": ["注册", "登录", "密码", "验证码", "账号", "订单", "发票", "开票", "支付方式", "找回", "对公转账"],
    "policy": ["退款", "退货", "换货", "隐私", "数据", "安全", "政策", "退订", "退费", "删除账号", "删除", "退回", "退钱"],
    "manual": ["开通", "首次", "使用", "配置", "权限", "报表", "自动化", "高级功能", "同步", "成员"],
    "troubleshoot": ["失败", "打不开", "异常", "故障", "无法登录", "验证码", "短信码", "支付失败", "订单异常", "扣款", "未支付", "对公转账", "转圈"],
    "product": ["套餐", "价格", "版本", "免费版", "专业版", "企业版", "sla", "售后", "支持范围", "收费"],
}


def route_collections(query: str) -> list[str]:
    lowered = expand_query(query).lower()
    matched: OrderedDict[str, None] = OrderedDict()
    for collection, keywords in COLLECTION_KEYWORDS.items():
        if any(keyword.lower() in lowered for keyword in keywords):
            matched[collection] = None
    if not matched:
        for collection in ["faq", "policy", "manual", "troubleshoot", "product"]:
            matched[collection] = None
    return list(matched.keys())
