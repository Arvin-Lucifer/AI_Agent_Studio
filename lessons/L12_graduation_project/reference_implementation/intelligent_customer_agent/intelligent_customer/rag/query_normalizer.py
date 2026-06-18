from __future__ import annotations


ALIAS_RULES: list[tuple[str, list[str]]] = [
    ("退款 到账 退换货", ["退回来", "退回", "钱什么时候", "什么时候返钱", "返钱", "退钱", "买错", "买错套餐", "能退吗"]),
    ("验证码 登录失败", ["短信码", "验证码收不到", "收不到码", "收不到短信", "动态码", "校验码"]),
    ("发票 发票抬头", ["开票", "票据", "抬头", "税号"]),
    ("登录失败 打不开 登录页 网络代理", ["打不开页面", "打不开登录页", "一直转圈", "页面转圈", "进不去", "登不上"]),
    ("权限 报表", ["看不到报表", "成员看不到", "没有权限", "权限没生效", "报表看不到"]),
    ("支付 扣款 订单 未支付", ["扣了钱", "扣款了", "钱扣了", "显示未支付", "没支付成功"]),
    ("套餐 价格 专业版 企业版", ["怎么收费", "收费吗", "多少钱", "贵不贵", "买哪个版本"]),
    ("隐私 删除账号 数据安全", ["注销账号", "销号", "删除个人信息", "删除数据"]),
]


def canonical_terms_for(text: str) -> list[str]:
    lowered = text.lower()
    terms: list[str] = []
    for canonical, aliases in ALIAS_RULES:
        if any(alias.lower() in lowered for alias in aliases):
            terms.extend(canonical.split())
    return _dedupe(terms)


def expand_query(text: str) -> str:
    terms = canonical_terms_for(text)
    if not terms:
        return text
    lowered = text.lower()
    missing = [term for term in terms if term.lower() not in lowered]
    if not missing:
        return text
    return f"{text} {' '.join(missing)}"


def _dedupe(items: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        key = item.lower()
        if key in seen:
            continue
        seen.add(key)
        result.append(item)
    return result
