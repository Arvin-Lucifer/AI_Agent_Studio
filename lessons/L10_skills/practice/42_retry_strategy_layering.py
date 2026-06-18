#!/usr/bin/env python3
"""L10 Step 42: retry strategy across Tool, Skill, and orchestration layers.

这个脚本对应“重试策略应该放在 Skill 层还是 Tool 层”。
它用可重复的 mock 场景演示：

1. Tool 层重试网络、HTTP 5xx、429、token 过期等物理层抖动。
2. Skill 层处理业务可恢复错误，例如幂等写入超时后先查再写。
3. 参数错误、权限错误、业务冲突不重试。
4. 编排层不继续叠重试，只做补偿、降级和用户告知。

Usage:
    python practice/42_retry_strategy_layering.py --scenario network_timeout
    python practice/42_retry_strategy_layering.py --scenario idempotent_write_timeout
    python practice/42_retry_strategy_layering.py --scenario permission_denied
    python practice/42_retry_strategy_layering.py --scenario retry_storm
"""

from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
from enum import Enum
from typing import Dict, List

from skill_common import dump_json


class Layer(str, Enum):
    TOOL = "tool"
    SKILL = "skill"
    ORCHESTRATION = "orchestration"
    NONE = "no_retry"


@dataclass(frozen=True)
class RetryScenario:
    name: str
    error: str
    status_code: int | None
    operation: str
    idempotent: bool
    has_retry_after: bool = False
    can_query_by_client_token: bool = False
    async_not_ready: bool = False


@dataclass(frozen=True)
class RetryStep:
    layer: str
    attempt: int
    action: str
    wait: str
    result: str


@dataclass(frozen=True)
class RetryReview:
    scenario: str
    retry_layer: str
    retriable: bool
    total_attempts_budget: int
    actual_attempts: int
    steps: List[RetryStep]
    orchestrator_action: str
    reason: str


SCENARIOS: Dict[str, RetryScenario] = {
    "network_timeout": RetryScenario(
        name="network_timeout",
        error="network_timeout",
        status_code=None,
        operation="read_weather_api",
        idempotent=True,
    ),
    "http_503": RetryScenario(
        name="http_503",
        error="http_503",
        status_code=503,
        operation="read_doc_api",
        idempotent=True,
    ),
    "rate_limited": RetryScenario(
        name="rate_limited",
        error="rate_limited",
        status_code=429,
        operation="search_api",
        idempotent=True,
        has_retry_after=True,
    ),
    "idempotent_write_timeout": RetryScenario(
        name="idempotent_write_timeout",
        error="unknown_write_timeout",
        status_code=None,
        operation="create_base_record",
        idempotent=True,
        can_query_by_client_token=True,
    ),
    "async_not_ready": RetryScenario(
        name="async_not_ready",
        error="transcript_not_ready",
        status_code=None,
        operation="fetch_meeting_minutes",
        idempotent=True,
        async_not_ready=True,
    ),
    "permission_denied": RetryScenario(
        name="permission_denied",
        error="permission_denied",
        status_code=403,
        operation="update_doc",
        idempotent=True,
    ),
    "bad_request": RetryScenario(
        name="bad_request",
        error="bad_request",
        status_code=400,
        operation="send_email",
        idempotent=True,
    ),
    "retry_storm": RetryScenario(
        name="retry_storm",
        error="naive_retry_storm",
        status_code=503,
        operation="call_downstream_service",
        idempotent=True,
    ),
}


def choose_retry_layer(scenario: RetryScenario) -> tuple[Layer, str]:
    """按失败语义选择哪一层处理重试。"""
    if scenario.status_code in {400, 401, 403, 404, 422}:
        return Layer.NONE, "4xx 语义错误，重试不会解决，应直接上抛。"
    if scenario.error in {"network_timeout", "connection_reset", "dns_error"}:
        return Layer.TOOL, "网络/传输层瞬时故障，靠近失败点在 Tool 层重试。"
    if scenario.status_code in {502, 503, 504}:
        return Layer.TOOL, "HTTP 5xx 属于下游瞬时不可用，Tool 层做短退避重试。"
    if scenario.status_code == 429:
        return Layer.TOOL, "429 要尊重 Retry-After，由 Tool 层控制退避。"
    if scenario.async_not_ready:
        return Layer.SKILL, "异步任务未就绪，需要 Skill 层按业务总时长轮询。"
    if scenario.error == "unknown_write_timeout" and scenario.can_query_by_client_token:
        return Layer.SKILL, "幂等写入未知状态，需要 Skill 层先按 client_token 查询再决定。"
    return Layer.NONE, "无法判断可恢复性，默认不重试并上抛。"


def simulate_tool_retry(scenario: RetryScenario) -> List[RetryStep]:
    """Tool 层只处理物理层抖动，示例中不真实 sleep。"""
    if scenario.status_code == 429:
        return [
            RetryStep("tool", 1, "respect Retry-After header", "Retry-After: 2s", "success_after_wait")
        ]
    if scenario.status_code in {502, 503, 504}:
        return [
            RetryStep("tool", 1, "call downstream", "0ms", "http_503"),
            RetryStep("tool", 2, "retry with exponential backoff + jitter", "200ms +/- jitter", "success"),
        ]
    return [
        RetryStep("tool", 1, "call downstream", "0ms", "network_timeout"),
        RetryStep("tool", 2, "retry with exponential backoff + jitter", "200ms +/- jitter", "network_timeout"),
        RetryStep("tool", 3, "retry with exponential backoff + jitter", "500ms +/- jitter", "success"),
    ]


def simulate_skill_retry(scenario: RetryScenario) -> List[RetryStep]:
    """Skill 层根据业务上下文恢复，不做盲目多次调用。"""
    if scenario.async_not_ready:
        return [
            RetryStep("skill", 1, "poll transcript status", "2s", "not_ready"),
            RetryStep("skill", 2, "poll transcript status within total timeout", "5s", "ready"),
        ]
    if scenario.can_query_by_client_token:
        return [
            RetryStep("skill", 1, "query by client_token before retrying write", "0ms", "not_found"),
            RetryStep("skill", 2, "retry idempotent write with same client_token", "1s", "success"),
        ]
    return [RetryStep("skill", 1, "no safe business recovery", "0ms", "failed")]


def simulate_no_retry(scenario: RetryScenario, reason: str) -> List[RetryStep]:
    return [
        RetryStep(
            "no_retry",
            0,
            f"raise {scenario.error}",
            "0ms",
            reason,
        )
    ]


def simulate_retry_storm() -> RetryReview:
    """展示三层各 3 次为什么会变成 27 次。"""
    steps = [
        RetryStep("tool", 3, "naive tool retries", "200/500/1000ms", "still_failed"),
        RetryStep("skill", 3, "naive skill retries whole tool call", "1s/2s/4s", "still_failed"),
        RetryStep("orchestration", 3, "naive orchestration retries whole skill", "manual loop", "27_attempts"),
        RetryStep("budget", 4, "cap total attempts and open circuit breaker", "fail-fast", "degraded"),
    ]
    return RetryReview(
        scenario="retry_storm",
        retry_layer=Layer.ORCHESTRATION.value,
        retriable=False,
        total_attempts_budget=4,
        actual_attempts=27,
        steps=steps,
        orchestrator_action="不要叠加重试；打开熔断，返回降级结果或告知用户稍后再试。",
        reason="三层各 3 次会放大为 27 次调用，违反 retry budget。",
    )


def review_retry_strategy(scenario: RetryScenario) -> RetryReview:
    if scenario.name == "retry_storm":
        return simulate_retry_storm()

    layer, reason = choose_retry_layer(scenario)
    budget = 4
    if layer == Layer.TOOL:
        steps = simulate_tool_retry(scenario)
        orchestrator_action = "接收 Tool 结果；如果仍失败，按 Skill 返回的 retriable 做降级，不再编排层重试。"
        retriable = True
    elif layer == Layer.SKILL:
        steps = simulate_skill_retry(scenario)
        orchestrator_action = "等待 Skill 返回结构化结果；编排层只做下一步决策。"
        retriable = True
    else:
        steps = simulate_no_retry(scenario, reason)
        orchestrator_action = "直接补偿、降级或告知用户补充权限/参数。"
        retriable = False

    return RetryReview(
        scenario=scenario.name,
        retry_layer=layer.value,
        retriable=retriable,
        total_attempts_budget=budget,
        actual_attempts=len([step for step in steps if step.attempt > 0]),
        steps=steps,
        orchestrator_action=orchestrator_action,
        reason=reason,
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="L10 retry strategy layering demo")
    parser.add_argument("--scenario", choices=sorted(SCENARIOS), default="network_timeout")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    review = review_retry_strategy(SCENARIOS[args.scenario])
    print(
        dump_json(
            {
                **asdict(review),
                "core_rule": "Tool 层管物理抖动，Skill 层管业务可恢复，编排层只决策不叠重试。",
            }
        )
    )


if __name__ == "__main__":
    main()
