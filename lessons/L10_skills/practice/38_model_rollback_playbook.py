#!/usr/bin/env python3
"""L10 Step 38: model upgrade rollback playbook.

这个脚本对应“模型升级回滚”补充内容。
它用 mock 数据演示一个成熟回滚系统应该具备的三件事：

1. 版本即快照：模型、Prompt、Skill、参数、阈值、后处理一起绑定。
2. 指标可对照：新旧版本对比，而不是凭感觉。
3. 回滚有分级：L1 参数调节、L2 局部切流、L3 灰度回退、L4 全量回滚。

Usage:
    python practice/38_model_rollback_playbook.py --scenario skill_regression
    python practice/38_model_rollback_playbook.py --scenario security_incident
"""

from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
from typing import Dict, Literal

from skill_common import dump_json


RollbackLevel = Literal["NONE", "L1", "L2", "L3", "L4"]


@dataclass(frozen=True)
class VersionSnapshot:
    """可回滚版本必须是完整快照，而不是单个 model id。"""

    version_id: str
    model_id: str
    prompt_bundle: str
    skill_manifest: str
    temperature: float
    router_threshold: float
    postprocess_rules: str
    traffic_percent: int


@dataclass(frozen=True)
class Metrics:
    error_rate: float
    p99_latency_ms: int
    skill_success_rate: float
    task_completion_rate: float
    false_trigger_rate: float
    user_abort_rate: float
    injection_block_rate: float
    external_misfire_rate: float


@dataclass(frozen=True)
class RollbackDecision:
    level: RollbackLevel
    trigger: str
    action: str
    runbook: list[str]


BASELINE = Metrics(
    error_rate=0.01,
    p99_latency_ms=2200,
    skill_success_rate=0.92,
    task_completion_rate=0.88,
    false_trigger_rate=0.03,
    user_abort_rate=0.08,
    injection_block_rate=0.97,
    external_misfire_rate=0.001,
)


SCENARIOS: Dict[str, Metrics] = {
    "healthy": Metrics(0.012, 2300, 0.91, 0.875, 0.032, 0.085, 0.97, 0.001),
    "skill_regression": Metrics(0.018, 2400, 0.79, 0.74, 0.08, 0.15, 0.96, 0.001),
    "latency_incident": Metrics(0.018, 5200, 0.88, 0.83, 0.04, 0.12, 0.96, 0.001),
    "security_incident": Metrics(0.02, 2600, 0.84, 0.8, 0.05, 0.14, 0.82, 0.02),
}


OLD_VERSION = VersionSnapshot(
    version_id="agent-skill-2026.06.01",
    model_id="gpt-5.3",
    prompt_bundle="prompt-bundle-v12",
    skill_manifest="skills-v8",
    temperature=0.2,
    router_threshold=0.74,
    postprocess_rules="postprocess-v5",
    traffic_percent=80,
)


NEW_VERSION = VersionSnapshot(
    version_id="agent-skill-2026.06.18",
    model_id="gpt-5.4",
    prompt_bundle="prompt-bundle-v13",
    skill_manifest="skills-v9",
    temperature=0.2,
    router_threshold=0.68,
    postprocess_rules="postprocess-v6",
    traffic_percent=20,
)


def decide_rollback(baseline: Metrics, current: Metrics, affected_skill: str = "email-notifier") -> RollbackDecision:
    """根据硬红线和软红线给出回滚动作。"""
    if current.external_misfire_rate > baseline.external_misfire_rate * 5 or (
        baseline.injection_block_rate - current.injection_block_rate
    ) > 0.1:
        return RollbackDecision(
            level="L4",
            trigger="安全硬红线：对外误发率上升或 injection 拦截率明显下降。",
            action="全量回滚到旧版本快照，并冻结重新发布窗口。",
            runbook=[
                "配置中心一键切回旧版本快照。",
                "清理新版本相关缓存 key。",
                "暂停所有写入/对外类高风险 Skill 灰度。",
                "封存触发 case，通知 oncall 和业务 owner。",
            ],
        )

    if current.p99_latency_ms >= baseline.p99_latency_ms * 2:
        return RollbackDecision(
            level="L3",
            trigger="性能硬红线：P99 延迟翻倍。",
            action="将新版本灰度比例降到 0%，保留影子流量继续对照。",
            runbook=[
                "灰度比例从当前值降到 0%。",
                "检查模型网关、工具下游和重试放大。",
                "保留 1% shadow mode 收集差异。",
            ],
        )

    if current.skill_success_rate <= baseline.skill_success_rate - 0.10:
        return RollbackDecision(
            level="L2",
            trigger="Skill 成功率低于基线 10 个百分点以上。",
            action=f"仅将问题 Skill `{affected_skill}` 切回旧版描述、阈值和工具配置。",
            runbook=[
                f"按 Skill 维度将 `{affected_skill}` 路由到旧版本快照。",
                "保留其他 Skill 的新版本流量。",
                "回放金标 case，确认误触发和漏触发恢复。",
            ],
        )

    if current.false_trigger_rate > baseline.false_trigger_rate * 1.5:
        return RollbackDecision(
            level="L1",
            trigger="误触发率上升，但影响面局部。",
            action="提高路由 threshold，收紧 Skill description 触发条件。",
            runbook=[
                "router_threshold 上调 0.03-0.08。",
                "补充负例描述和黑名单触发词。",
                "观察 30 分钟误触发率和漏触发率。",
            ],
        )

    return RollbackDecision(
        level="NONE",
        trigger="未触发回滚阈值。",
        action="继续灰度观察。",
        runbook=["保持当前灰度比例，继续收集 shadow 对照和用户反馈。"],
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="L10 model rollback playbook demo")
    parser.add_argument("--scenario", choices=sorted(SCENARIOS), default="skill_regression")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    current = SCENARIOS[args.scenario]
    decision = decide_rollback(BASELINE, current)
    print(
        dump_json(
            {
                "scenario": args.scenario,
                "old_version_snapshot": asdict(OLD_VERSION),
                "new_version_snapshot": asdict(NEW_VERSION),
                "baseline_metrics": asdict(BASELINE),
                "current_metrics": asdict(current),
                "decision": asdict(decision),
                "note": "回滚对象是完整版本快照，不是只换 model_id。",
            }
        )
    )


if __name__ == "__main__":
    main()
