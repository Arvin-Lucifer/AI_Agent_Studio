#!/usr/bin/env python3
"""L10 Step 43: optimize tail latency in parallel Skill orchestration.

这个脚本对应“多个子步骤并行但其中一个慢得多，如何优化”。
它不真实 sleep，而是用模拟耗时展示：

1. 并行总耗时由最慢分支决定。
2. 关键路径剥离可以先返回快结果，慢结果后台补齐。
3. 提前启动可以消除隐藏串行等待。
4. 分片并发可以把大任务拆成多个较短任务。
5. 软超时可以先返回降级结果。
6. Hedging 可以用额外调用成本压低 P99 尖刺。

Usage:
    python practice/43_parallel_tail_latency.py --scenario critical_path
    python practice/43_parallel_tail_latency.py --scenario fanout
    python practice/43_parallel_tail_latency.py --scenario hedged_timeout
"""

from __future__ import annotations

import argparse
import math
from dataclasses import asdict, dataclass
from enum import Enum
from typing import Dict, List

from skill_common import dump_json


class RootCause(str, Enum):
    IO_WAIT = "io_wait"
    LARGE_DATA = "large_data"
    SLOW_DOWNSTREAM = "slow_downstream"
    FAKE_PARALLEL = "fake_parallel"


@dataclass(frozen=True)
class Branch:
    name: str
    duration_ms: int
    blocking: bool
    root_cause: str
    note: str


@dataclass(frozen=True)
class OptimizationReview:
    scenario: str
    baseline_parallel_ms: int
    optimized_initial_response_ms: int
    optimized_full_completion_ms: int
    bottleneck: str
    root_cause: str
    strategy: str
    trace: List[Dict[str, str | int | bool]]
    tradeoffs: List[str]
    recommendation: List[str]


SCENARIOS: Dict[str, List[Branch]] = {
    "critical_path": [
        Branch("extract_action_items", 1200, True, RootCause.IO_WAIT.value, "主响应需要"),
        Branch("generate_summary", 1600, True, RootCause.IO_WAIT.value, "主响应需要"),
        Branch("render_cover_image", 18000, False, RootCause.SLOW_DOWNSTREAM.value, "可后台补齐"),
        Branch("archive_to_drive", 4500, False, RootCause.IO_WAIT.value, "可后台归档"),
    ],
    "speculative_start": [
        Branch("validate_request", 700, True, RootCause.IO_WAIT.value, "入口校验"),
        Branch("prefetch_template", 3000, True, RootCause.IO_WAIT.value, "只依赖用户输入，可提前启动"),
        Branch("prefetch_permissions", 1800, True, RootCause.IO_WAIT.value, "只依赖用户身份，可提前启动"),
        Branch("create_doc", 1200, True, RootCause.IO_WAIT.value, "依赖校验和模板"),
    ],
    "fanout": [
        Branch("write_1000_records", 20000, True, RootCause.LARGE_DATA.value, "随记录数线性增长"),
    ],
    "hedged_timeout": [
        Branch("fetch_transcript", 2200, True, RootCause.IO_WAIT.value, "可先返回"),
        Branch("generate_minutes_summary", 9000, False, RootCause.SLOW_DOWNSTREAM.value, "超过软超时后 pending"),
    ],
    "hedging": [
        Branch("read_profile_primary", 4200, True, RootCause.SLOW_DOWNSTREAM.value, "P95 后仍未返回"),
        Branch("read_profile_backup", 1800, True, RootCause.SLOW_DOWNSTREAM.value, "对冲副本"),
    ],
    "cache_precompute": [
        Branch("render_weekly_report", 7000, True, RootCause.LARGE_DATA.value, "可按参数指纹缓存"),
        Branch("load_cached_report", 80, True, RootCause.IO_WAIT.value, "缓存命中"),
    ],
    "fake_parallel": [
        Branch("fetch_20_pages_sequential_loop", 10000, True, RootCause.FAKE_PARALLEL.value, "内部 for 循环串行"),
    ],
}


def build_trace(branches: List[Branch]) -> List[Dict[str, str | int | bool]]:
    return [
        {
            "step_name": branch.name,
            "duration_ms": branch.duration_ms,
            "blocking": branch.blocking,
            "root_cause": branch.root_cause,
            "note": branch.note,
        }
        for branch in branches
    ]


def baseline_latency(branches: List[Branch]) -> int:
    """并行 join 的基线耗时由最慢分支决定。"""
    return max(branch.duration_ms for branch in branches)


def find_bottleneck(branches: List[Branch]) -> Branch:
    return max(branches, key=lambda branch: branch.duration_ms)


def review_critical_path(branches: List[Branch]) -> OptimizationReview:
    blocking_ms = max(branch.duration_ms for branch in branches if branch.blocking)
    full_ms = baseline_latency(branches)
    bottleneck = find_bottleneck(branches)
    return OptimizationReview(
        scenario="critical_path",
        baseline_parallel_ms=full_ms,
        optimized_initial_response_ms=blocking_ms,
        optimized_full_completion_ms=full_ms,
        bottleneck=bottleneck.name,
        root_cause=bottleneck.root_cause,
        strategy="critical_path_decoupling",
        trace=build_trace(branches),
        tradeoffs=[
            "用户先拿到主结果，但部分字段会显示 pending。",
            "需要通知、轮询或 WebSocket 承接后补结果。",
        ],
        recommendation=[
            "把 render_cover_image 和 archive_to_drive 标记为 non_blocking。",
            "主响应在 extract_action_items 与 generate_summary 完成后返回。",
            "慢分支完成后追加通知或更新前端状态。",
        ],
    )


def review_speculative_start(branches: List[Branch]) -> OptimizationReview:
    sequential_ms = sum(branch.duration_ms for branch in branches)
    optimized_ms = max(700, 3000, 1800) + 1200
    bottleneck = find_bottleneck(branches)
    return OptimizationReview(
        scenario="speculative_start",
        baseline_parallel_ms=sequential_ms,
        optimized_initial_response_ms=optimized_ms,
        optimized_full_completion_ms=optimized_ms,
        bottleneck=bottleneck.name,
        root_cause=bottleneck.root_cause,
        strategy="speculative_start",
        trace=build_trace(branches),
        tradeoffs=[
            "提前启动会消耗一些可能用不到的下游调用。",
            "需要在校验失败时取消或忽略预取结果。",
        ],
        recommendation=[
            "入口处同时启动 validate_request、prefetch_template、prefetch_permissions。",
            "校验通过后直接 create_doc，避免模板和权限预取串行等待。",
        ],
    )


def review_fanout(branches: List[Branch]) -> OptimizationReview:
    original = branches[0]
    shard_count = 10
    per_shard_ms = math.ceil(original.duration_ms / shard_count)
    merge_ms = 600
    optimized = per_shard_ms + merge_ms
    return OptimizationReview(
        scenario="fanout",
        baseline_parallel_ms=original.duration_ms,
        optimized_initial_response_ms=optimized,
        optimized_full_completion_ms=optimized,
        bottleneck=original.name,
        root_cause=original.root_cause,
        strategy="fan_out_sharding",
        trace=build_trace(branches)
        + [
            {
                "step_name": "write_10_shards_parallel",
                "duration_ms": per_shard_ms,
                "blocking": True,
                "root_cause": RootCause.LARGE_DATA.value,
                "note": "10 个 100 条批次并发写入",
            },
            {
                "step_name": "merge_results",
                "duration_ms": merge_ms,
                "blocking": True,
                "root_cause": "aggregation",
                "note": "合并每个 shard 的写入结果",
            },
        ],
        tradeoffs=[
            "吞吐提升会增加瞬时 QPS。",
            "必须保证 shard_count x QPS 不超过下游配额。",
        ],
        recommendation=[
            "把 1000 条拆成 10 个 100 条批次。",
            "设置并发上限和失败 shard 重试策略。",
            "对每个 shard 使用 idempotency_key。",
        ],
    )


def review_hedged_timeout(branches: List[Branch]) -> OptimizationReview:
    transcript = next(branch for branch in branches if branch.name == "fetch_transcript")
    summary = next(branch for branch in branches if branch.name == "generate_minutes_summary")
    soft_timeout_ms = 5000
    initial = max(transcript.duration_ms, soft_timeout_ms)
    return OptimizationReview(
        scenario="hedged_timeout",
        baseline_parallel_ms=max(transcript.duration_ms, summary.duration_ms),
        optimized_initial_response_ms=initial,
        optimized_full_completion_ms=summary.duration_ms,
        bottleneck=summary.name,
        root_cause=summary.root_cause,
        strategy="soft_timeout_degrade",
        trace=build_trace(branches)
        + [
            {
                "step_name": "soft_timeout",
                "duration_ms": soft_timeout_ms,
                "blocking": True,
                "root_cause": "policy",
                "note": "超过 5s 先返回逐字稿，summary pending",
            }
        ],
        tradeoffs=[
            "用户先看到降级结果，不是最终完整结果。",
            "需要后补更新机制和失败提示。",
        ],
        recommendation=[
            "5s 内没有生成精要时先返回 transcript。",
            "summary 完成后异步覆盖或追加。",
            "UI 中显式标记 summary=pending。",
        ],
    )


def review_hedging(branches: List[Branch]) -> OptimizationReview:
    primary = branches[0]
    backup = branches[1]
    p95_threshold_ms = 1500
    optimized = p95_threshold_ms + backup.duration_ms
    return OptimizationReview(
        scenario="hedging",
        baseline_parallel_ms=primary.duration_ms,
        optimized_initial_response_ms=min(primary.duration_ms, optimized),
        optimized_full_completion_ms=min(primary.duration_ms, optimized),
        bottleneck=primary.name,
        root_cause=primary.root_cause,
        strategy="hedging",
        trace=build_trace(branches)
        + [
            {
                "step_name": "start_backup_at_p95",
                "duration_ms": p95_threshold_ms,
                "blocking": True,
                "root_cause": "tail_spike",
                "note": "主请求到 P95 仍未返回，启动对冲副本",
            }
        ],
        tradeoffs=[
            "会增加额外调用成本。",
            "只适合只读、幂等、下游有余量的请求。",
            "需要取消慢副本或去重结果。",
        ],
        recommendation=[
            "只对只读查询启用 hedging。",
            "达到 P95 阈值后发第二个请求，取先返回结果。",
            "对高成本或非幂等写操作禁用。",
        ],
    )


def review_cache_precompute(branches: List[Branch]) -> OptimizationReview:
    render = branches[0]
    cache = branches[1]
    return OptimizationReview(
        scenario="cache_precompute",
        baseline_parallel_ms=render.duration_ms,
        optimized_initial_response_ms=cache.duration_ms,
        optimized_full_completion_ms=cache.duration_ms,
        bottleneck=render.name,
        root_cause=render.root_cause,
        strategy="cache_and_precompute",
        trace=build_trace(branches),
        tradeoffs=[
            "缓存需要失效策略。",
            "预计算会消耗后台资源。",
        ],
        recommendation=[
            "按 user_id + 参数指纹缓存报告。",
            "周期性任务提前预计算高频报告。",
            "缓存未命中时降级为后台生成并通知。",
        ],
    )


def review_fake_parallel(branches: List[Branch]) -> OptimizationReview:
    original = branches[0]
    concurrency = 5
    optimized = math.ceil(original.duration_ms / concurrency)
    return OptimizationReview(
        scenario="fake_parallel",
        baseline_parallel_ms=original.duration_ms,
        optimized_initial_response_ms=optimized,
        optimized_full_completion_ms=optimized,
        bottleneck=original.name,
        root_cause=original.root_cause,
        strategy="make_inner_loop_concurrent",
        trace=build_trace(branches)
        + [
            {
                "step_name": "fetch_pages_with_concurrency_5",
                "duration_ms": optimized,
                "blocking": True,
                "root_cause": RootCause.FAKE_PARALLEL.value,
                "note": "把内部顺序 for 循环改成有上限的并发",
            }
        ],
        tradeoffs=[
            "需要处理并发错误合并。",
            "需要控制并发数，避免下游限流。",
        ],
        recommendation=[
            "检查 trace，确认耗时是否约等于页数 x 单页延迟。",
            "把内部循环改成 bounded concurrency。",
            "对失败页返回 partial_success。",
        ],
    )


def review_scenario(name: str) -> OptimizationReview:
    branches = SCENARIOS[name]
    if name == "critical_path":
        return review_critical_path(branches)
    if name == "speculative_start":
        return review_speculative_start(branches)
    if name == "fanout":
        return review_fanout(branches)
    if name == "hedged_timeout":
        return review_hedged_timeout(branches)
    if name == "hedging":
        return review_hedging(branches)
    if name == "cache_precompute":
        return review_cache_precompute(branches)
    if name == "fake_parallel":
        return review_fake_parallel(branches)
    raise ValueError(f"Unsupported scenario: {name}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="L10 parallel tail latency optimization demo")
    parser.add_argument("--scenario", choices=sorted(SCENARIOS), default="critical_path")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    review = review_scenario(args.scenario)
    print(
        dump_json(
            {
                **asdict(review),
                "core_rule": "要么让慢分支变快，要么让慢分支不阻塞主响应。",
            }
        )
    )


if __name__ == "__main__":
    main()
