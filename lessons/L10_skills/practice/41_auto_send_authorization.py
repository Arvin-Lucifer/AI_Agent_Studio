#!/usr/bin/env python3
"""L10 Step 41: bounded authorization for "send automatically next time".

这个脚本对应“以后都自动发”的补充内容。
它演示如何把一句口头授权落成可执行的策略对象：

1. 先判断这类自动化能不能接。
2. 接受时生成窄范围、有时效、有上限、可撤销、可审计的规则。
3. 每次执行前检查 scope、expiry、quota、异常风险和首次 dry-run。
4. 超出范围或高风险时退回单次确认或拒绝。

Usage:
    python practice/41_auto_send_authorization.py --scenario daily_report
    python practice/41_auto_send_authorization.py --scenario scope_drift
    python practice/41_auto_send_authorization.py --scenario vendor_payment
"""

from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
from datetime import date, timedelta
from enum import Enum
from typing import Dict, List

from skill_common import dump_json


TODAY = date(2026, 6, 18)


class Decision(str, Enum):
    CREATE_POLICY = "create_limited_policy"
    REQUIRE_CONFIRMATION = "require_single_confirmation"
    REJECT = "reject_automation"


@dataclass(frozen=True)
class AuthorizationScenario:
    name: str
    user_request: str
    action: str
    target: str
    target_count: int
    content_template: str
    time_window: str
    reversible: bool
    compliance_sensitive: bool
    acts_for_self: bool
    cross_department_or_external: bool
    first_execution: bool = True
    execution_target: str | None = None
    execution_target_count: int | None = None
    execution_template: str | None = None
    execution_time_window: str | None = None
    current_total_sent: int = 0
    revoked: bool = False


@dataclass(frozen=True)
class AutomationPolicy:
    rule_id: str
    action: str
    scope: Dict[str, str | int]
    limits: Dict[str, int]
    expiry: str
    revoke_hint: str
    audit: bool
    first_run_requires_dry_run: bool


@dataclass(frozen=True)
class AuthorizationReview:
    scenario: str
    decision: str
    reasons: List[str]
    policy: AutomationPolicy | None
    user_reply: str
    execution_checklist: List[str]
    execution_decision: str
    audit_preview: Dict[str, str | int] | None


SCENARIOS: Dict[str, AuthorizationScenario] = {
    "daily_report": AuthorizationScenario(
        name="daily_report",
        user_request="以后工作日早上都自动给项目群发日报。",
        action="send_im_notification",
        target="group_id=project-daily",
        target_count=1,
        content_template="日报模板",
        time_window="workday 09:00-10:00",
        reversible=True,
        compliance_sensitive=False,
        acts_for_self=True,
        cross_department_or_external=False,
        first_execution=True,
    ),
    "scope_drift": AuthorizationScenario(
        name="scope_drift",
        user_request="以后工作日早上都自动给项目群发日报。",
        action="send_im_notification",
        target="group_id=project-daily",
        target_count=1,
        content_template="日报模板",
        time_window="workday 09:00-10:00",
        reversible=True,
        compliance_sensitive=False,
        acts_for_self=True,
        cross_department_or_external=False,
        first_execution=False,
        execution_target="group_id=project-daily,group_id=pm,group_id=sales,group_id=rd,group_id=ops",
        execution_target_count=5,
        execution_template="日报模板",
        execution_time_window="workday 09:00-10:00",
        current_total_sent=3,
    ),
    "cross_department_broadcast": AuthorizationScenario(
        name="cross_department_broadcast",
        user_request="以后所有跨部门周报都自动发到 8 个群。",
        action="send_im_notification",
        target="multi_group=broadcast",
        target_count=8,
        content_template="跨部门周报",
        time_window="friday 17:00-18:00",
        reversible=True,
        compliance_sensitive=False,
        acts_for_self=True,
        cross_department_or_external=True,
    ),
    "vendor_payment": AuthorizationScenario(
        name="vendor_payment",
        user_request="以后供应商账单都自动打款。",
        action="transfer_money",
        target="vendor_account=*",
        target_count=1,
        content_template="付款授权",
        time_window="anytime",
        reversible=False,
        compliance_sensitive=True,
        acts_for_self=True,
        cross_department_or_external=True,
    ),
    "delegate_privacy": AuthorizationScenario(
        name="delegate_privacy",
        user_request="以后老板让我发给客户的内容你都自动代我发。",
        action="send_external_email",
        target="customer_emails=*",
        target_count=20,
        content_template="客户邮件",
        time_window="anytime",
        reversible=False,
        compliance_sensitive=True,
        acts_for_self=False,
        cross_department_or_external=True,
    ),
}


def evaluate_request(scenario: AuthorizationScenario) -> tuple[Decision, List[str]]:
    """先判断这句“以后自动”能不能接。"""
    reasons: List[str] = []

    if scenario.cross_department_or_external or scenario.target_count > 3:
        reasons.append("影响范围较大、跨部门或对外，不能接受永久自动。")
    if not scenario.reversible:
        reasons.append("动作不可逆或撤回成本高，不能免确认自动执行。")
    if scenario.compliance_sensitive:
        reasons.append("涉及财务、权限、审批或合规风险，必须走确认/审批。")
    if not scenario.acts_for_self:
        reasons.append("不是本人操作本人资源，可能涉及他人隐私或代操作。")

    if any("财务" in reason or "不可逆" in reason or "他人隐私" in reason for reason in reasons):
        return Decision.REJECT, reasons
    if reasons:
        return Decision.REQUIRE_CONFIRMATION, reasons
    return Decision.CREATE_POLICY, ["请求属于小范围、可逆、低合规风险、本人资源，可落成受限自动化策略。"]


def build_policy(scenario: AuthorizationScenario) -> AutomationPolicy:
    """把口头授权翻译成持久化规则对象。"""
    rule_id = f"auto-{scenario.action}-{scenario.name}"
    return AutomationPolicy(
        rule_id=rule_id,
        action=scenario.action,
        scope={
            "target": scenario.target,
            "target_count": scenario.target_count,
            "content_template": scenario.content_template,
            "time_window": scenario.time_window,
        },
        limits={"max_per_day": 1, "max_total": 30},
        expiry=(TODAY + timedelta(days=90)).isoformat(),
        revoke_hint=f"说“停止自动发{scenario.content_template.replace('模板', '')}”可随时撤销",
        audit=True,
        first_run_requires_dry_run=True,
    )


def build_user_reply(policy: AutomationPolicy | None, decision: Decision, scenario: AuthorizationScenario) -> str:
    if decision == Decision.CREATE_POLICY and policy:
        return (
            f"好的，已记住：之后在 {policy.scope['time_window']} 给 {policy.scope['target']} "
            f"发送{policy.scope['content_template']}时自动执行。授权范围仅限此场景，"
            f"{policy.expiry} 到期或发满 {policy.limits['max_total']} 次会再次确认。"
            f"想随时关闭，说“{policy.revoke_hint.split('说“', 1)[1].split('”', 1)[0]}”即可。"
        )
    if decision == Decision.REQUIRE_CONFIRMATION:
        return "这个请求影响范围较大，我可以保存为草稿或每次提醒你确认，但不能设为无确认自动发送。"
    return "这个请求涉及不可逆、合规或代他人操作风险，不能接受“以后都自动”的口头授权。"


def validate_execution(policy: AutomationPolicy | None, scenario: AuthorizationScenario) -> tuple[str, List[str]]:
    """每次自动执行前都做范围、时效、配额和风险校验。"""
    if policy is None:
        return "not_executable", ["没有可执行的自动化策略。"]

    checklist = [
        "规则未撤销。",
        "规则未过期。",
        "本次目标、模板、时间窗口在授权 scope 内。",
        "未触发收件人突增、敏感词、异常时间等风险信号。",
        "未超过每日频率和总次数上限。",
    ]

    if scenario.revoked:
        return "blocked_revoked", ["规则已撤销。"]
    if scenario.current_total_sent >= policy.limits["max_total"]:
        return "requires_renewal", ["已达到总次数上限，需要续期确认。"]
    if scenario.first_execution and policy.first_run_requires_dry_run:
        return "dry_run_then_confirm_first_execution", ["首次真实执行需要 dry-run 预览和确认，避免规则理解偏差。"]

    execution_target = scenario.execution_target or scenario.target
    execution_count = scenario.execution_target_count or scenario.target_count
    execution_template = scenario.execution_template or scenario.content_template
    execution_time = scenario.execution_time_window or scenario.time_window

    if execution_target != policy.scope["target"] or execution_count != policy.scope["target_count"]:
        return "requires_confirmation_scope_changed", ["本次目标或收件人数量超出授权 scope。"]
    if execution_template != policy.scope["content_template"]:
        return "requires_confirmation_template_changed", ["本次内容模板变化，不能沿用原授权。"]
    if execution_time != policy.scope["time_window"]:
        return "requires_confirmation_time_changed", ["本次执行时间不在授权窗口内。"]

    return "auto_execute_allowed", checklist


def build_audit_preview(policy: AutomationPolicy | None, scenario: AuthorizationScenario) -> Dict[str, str | int] | None:
    if policy is None:
        return None
    return {
        "time": f"{TODAY.isoformat()}T09:05:00",
        "rule_id": policy.rule_id,
        "action": policy.action,
        "target": scenario.execution_target or scenario.target,
        "target_count": scenario.execution_target_count or scenario.target_count,
        "content_template": scenario.execution_template or scenario.content_template,
        "result": "pending_dry_run_or_confirm",
    }


def review_authorization(scenario: AuthorizationScenario) -> AuthorizationReview:
    decision, reasons = evaluate_request(scenario)
    policy = build_policy(scenario) if decision == Decision.CREATE_POLICY else None
    execution_decision, checklist = validate_execution(policy, scenario)
    return AuthorizationReview(
        scenario=scenario.name,
        decision=decision.value,
        reasons=reasons,
        policy=policy,
        user_reply=build_user_reply(policy, decision, scenario),
        execution_checklist=checklist,
        execution_decision=execution_decision,
        audit_preview=build_audit_preview(policy, scenario),
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="L10 bounded auto-send authorization demo")
    parser.add_argument("--scenario", choices=sorted(SCENARIOS), default="daily_report")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    review = review_authorization(SCENARIOS[args.scenario])
    print(
        dump_json(
            {
                **asdict(review),
                "core_rule": "以后都自动发，是受限期内免确认，不是无限期无范围执行。",
            }
        )
    )


if __name__ == "__main__":
    main()
