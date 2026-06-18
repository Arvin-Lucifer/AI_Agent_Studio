#!/usr/bin/env python3
"""L10 Step 40: incident response for high-risk Skill misfires.

这个脚本对应“高风险 Skill 误触发：事后损失控制”。
它不模拟真实发送或删除，而是把事故响应流程结构化输出：

1. 黄金 5 分钟：熔断、冻结规则、取消队列、拉日志。
2. 损失评估：可逆性、扩散性、下游关联。
3. 分场景补救：撤销、澄清、人工反向流程、下游止扩散。
4. 透明告知：事实、措施、残余影响、用户建议。
5. 临时围栏：确认、dry-run、冷却、限流。
6. 复盘产出：触发原因、防线缺口、加固动作。

Usage:
    python practice/40_high_risk_skill_incident_response.py --scenario internal_email
    python practice/40_high_risk_skill_incident_response.py --scenario permission_change
    python practice/40_high_risk_skill_incident_response.py --scenario downstream_workflow
"""

from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
from enum import Enum
from typing import Dict, List

from skill_common import dump_json


class OperationType(str, Enum):
    REVERSIBLE_WRITE = "reversible_write"
    DELIVERED_MESSAGE = "delivered_message"
    MONEY_OR_PERMISSION = "money_or_permission"
    DOWNSTREAM_WORKFLOW = "downstream_workflow"


@dataclass(frozen=True)
class IncidentScenario:
    name: str
    skill_name: str
    user_query: str
    operation_type: OperationType
    targets_total: int
    succeeded: int
    read_or_consumed: int
    queued_remaining: int
    downstream_triggered: bool
    reversible: bool
    external_object: bool
    compliance_sensitive: bool


@dataclass(frozen=True)
class IncidentResponse:
    scenario: str
    severity: str
    golden_5_minutes: List[str]
    impact_assessment: Dict[str, str]
    remediation_plan: List[str]
    user_notification: Dict[str, str]
    temporary_fences_24h: List[str]
    postmortem_outputs_1_to_3_days: List[str]
    core_rule: str


SCENARIOS: Dict[str, IncidentScenario] = {
    "internal_email": IncidentScenario(
        name="internal_email",
        skill_name="email-notifier",
        user_query="整理一下今天的项目日程",
        operation_type=OperationType.DELIVERED_MESSAGE,
        targets_total=15,
        succeeded=3,
        read_or_consumed=1,
        queued_remaining=12,
        downstream_triggered=False,
        reversible=False,
        external_object=True,
        compliance_sensitive=False,
    ),
    "permission_change": IncidentScenario(
        name="permission_change",
        skill_name="permission-manager",
        user_query="帮我检查这个项目成员权限",
        operation_type=OperationType.MONEY_OR_PERMISSION,
        targets_total=2,
        succeeded=2,
        read_or_consumed=2,
        queued_remaining=0,
        downstream_triggered=False,
        reversible=False,
        external_object=False,
        compliance_sensitive=True,
    ),
    "downstream_workflow": IncidentScenario(
        name="downstream_workflow",
        skill_name="task-sync",
        user_query="把会议纪要整理一下",
        operation_type=OperationType.DOWNSTREAM_WORKFLOW,
        targets_total=8,
        succeeded=8,
        read_or_consumed=4,
        queued_remaining=5,
        downstream_triggered=True,
        reversible=True,
        external_object=True,
        compliance_sensitive=False,
    ),
    "reversible_doc": IncidentScenario(
        name="reversible_doc",
        skill_name="doc-generator",
        user_query="帮我生成会议纪要模板",
        operation_type=OperationType.REVERSIBLE_WRITE,
        targets_total=1,
        succeeded=1,
        read_or_consumed=0,
        queued_remaining=0,
        downstream_triggered=False,
        reversible=True,
        external_object=False,
        compliance_sensitive=False,
    ),
}


def decide_severity(incident: IncidentScenario) -> str:
    """按老师材料中的升级信号判断事故等级。"""
    if incident.compliance_sensitive or incident.operation_type == OperationType.MONEY_OR_PERMISSION:
        return "P0_escalate_immediately"
    if incident.external_object or incident.targets_total > 9 or incident.downstream_triggered:
        return "P1_escalate_oncall"
    if incident.succeeded > 0:
        return "P2_local_containment"
    return "P3_observe"


def build_golden_5_minutes(incident: IncidentScenario) -> List[str]:
    actions = [
        f"熔断 `{incident.skill_name}`：至少对当前用户/会话停用该 Skill。",
        "冻结同 scope 自动化规则，避免同类授权继续执行。",
        f"取消队列和排期：当前仍有 {incident.queued_remaining} 个后续批次待检查。",
        "拉取调用日志：时间、参数、目标、成功数、失败数、trace_id。",
        "判断事故状态：确认是一次性误触发，还是仍在持续轮询/定时执行。",
    ]
    if incident.queued_remaining > 0 or incident.downstream_triggered:
        actions.insert(3, "优先切流并暂停下游 worker，防止扩散。")
    return actions


def assess_impact(incident: IncidentScenario) -> Dict[str, str]:
    reversibility = "可逆" if incident.reversible else "不可逆或不建议硬撤"
    spread = "已扩散" if incident.read_or_consumed > 0 or incident.external_object else "未扩散或扩散很小"
    downstream = "已触发下游" if incident.downstream_triggered else "未发现下游连锁"
    decision = "静默回滚 + 事后告知"
    if incident.downstream_triggered:
        decision = "先停下游，再回溯上游补救"
    elif not incident.reversible or incident.read_or_consumed > 0:
        decision = "不要硬撤，走澄清/补偿路径"
    return {
        "reversibility": reversibility,
        "spread": spread,
        "downstream": downstream,
        "recommended_decision": decision,
    }


def build_remediation(incident: IncidentScenario) -> List[str]:
    """根据误触发类型给出补救策略。"""
    if incident.operation_type == OperationType.REVERSIBLE_WRITE:
        return [
            "先导出或截图保留证据副本。",
            "删除误创建对象，或标记为作废。",
            "撤销动作写入审计日志，便于后续对账。",
        ]
    if incident.operation_type == OperationType.DELIVERED_MESSAGE:
        return [
            "检查消息/邮件是否仍在撤回窗口内，能撤回的立即撤回。",
            "对已读或超时不可撤回的目标发送补充说明。",
            "外部邮件使用 `[更正]` 或 `[Correction]` 标题发送更正邮件。",
        ]
    if incident.operation_type == OperationType.MONEY_OR_PERMISSION:
        return [
            "立即走人工反向流程：退款、权限回收、订单取消或审批撤销。",
            "不要用另一个自动化去修复自动化的错。",
            "同步合规、风控、财务或权限系统 owner。",
        ]
    if incident.operation_type == OperationType.DOWNSTREAM_WORKFLOW:
        return [
            "沿调用链回溯：Skill -> Webhook -> 第三方系统。",
            "先暂停最下游 worker/webhook，防止继续扩散。",
            "逐级撤销可逆对象；第三方不可控时联系对方 owner。",
        ]
    raise ValueError(f"Unsupported operation type: {incident.operation_type}")


def build_user_notification(incident: IncidentScenario) -> Dict[str, str]:
    """四段式用户告知：事实、措施、残余影响、用户建议。"""
    fact = (
        f"刚才在你说“{incident.user_query}”时，系统误触发了 `{incident.skill_name}`，"
        f"目标数 {incident.targets_total}，已成功执行 {incident.succeeded} 个。"
    )
    measures = "已熔断该 Skill、冻结同类自动化规则，并开始取消未执行队列。"
    residual = (
        f"目前确认 {incident.read_or_consumed} 个目标可能已经看到或消费了结果；"
        f"仍有 {incident.queued_remaining} 个后续批次需要确认是否取消成功。"
    )
    advice = "如需进一步澄清，我可以生成一段对受影响方的说明；后续同类操作会先展示 dry-run 并请求确认。"
    if incident.operation_type == OperationType.MONEY_OR_PERMISSION:
        advice = "这类操作将转人工处理；我会提供误触发参数和审计链路，供权限/合规负责人核对。"
    return {
        "what_happened": fact,
        "measures_taken": measures,
        "residual_impact": residual,
        "user_action_suggestion": advice,
    }


def build_temporary_fences(incident: IncidentScenario) -> List[str]:
    fences = [
        f"`{incident.skill_name}` 降级为强制单次确认。",
        "相似语义请求改为 dry-run，只展示将要执行什么。",
        "同用户其他高风险 Skill 进入预防性冷却窗口。",
        "该 Skill 调用频率压到安全水位，并设置熔断阈值。",
    ]
    if incident.external_object:
        fences.append("对外发送类动作增加收件人白名单和批量上限。")
    if incident.compliance_sensitive:
        fences.append("资金/权限/合规类动作临时切到人工审批。")
    return fences


def build_postmortem_outputs(incident: IncidentScenario) -> List[str]:
    return [
        "定位用户 query 与 Skill description 的语义重叠点。",
        "补充负例触发词和更高置信度门槛。",
        "检查前置校验、确认机制、限流、熔断和撤销能力缺口。",
        "把本次 case 加入安全回归集。",
        "输出明确 owner、截止时间和验证方式的改动清单。",
        f"为 `{incident.skill_name}` 补充一键暂停和一键审计入口。",
    ]


def build_incident_response(incident: IncidentScenario) -> IncidentResponse:
    return IncidentResponse(
        scenario=incident.name,
        severity=decide_severity(incident),
        golden_5_minutes=build_golden_5_minutes(incident),
        impact_assessment=assess_impact(incident),
        remediation_plan=build_remediation(incident),
        user_notification=build_user_notification(incident),
        temporary_fences_24h=build_temporary_fences(incident),
        postmortem_outputs_1_to_3_days=build_postmortem_outputs(incident),
        core_rule="误触发后的正确顺序：切断 -> 评估 -> 补救 -> 告知 -> 加固。",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="L10 high-risk Skill misfire incident response demo")
    parser.add_argument("--scenario", choices=sorted(SCENARIOS), default="internal_email")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    incident = SCENARIOS[args.scenario]
    response = build_incident_response(incident)
    print(
        dump_json(
            {
                "incident": asdict(incident),
                "response": asdict(response),
            }
        )
    )


if __name__ == "__main__":
    main()
