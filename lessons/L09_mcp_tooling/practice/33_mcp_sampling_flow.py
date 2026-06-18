#!/usr/bin/env python3
"""L09 Step 33: understand MCP Sampling flow.

Sampling 是 MCP 里最容易讲抽象的部分：它允许 Server 向 Client 请求一次 LLM 推理。
真实实现需要 ClientSession 提供 sampling_callback，并由 Client 决定是否转发给模型。

这个脚本不连接真实 LLM，而是把安全流程跑一遍：
Server request -> Client policy review -> optional human review -> model response -> Server result。
这样学生能先理解“谁发起、谁批准、谁控制模型和上下文”。

Usage:
    python practice/33_mcp_sampling_flow.py
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass
class SamplingRequest:
    server_name: str
    purpose: str
    messages: List[str]
    max_tokens: int


@dataclass
class SamplingDecision:
    allowed: bool
    reason: str
    redacted_messages: List[str]


def review_sampling_request(request: SamplingRequest) -> SamplingDecision:
    """Client 侧策略审核。

    重点：Sampling 不是 Server 想调模型就调模型，Client 可以拒绝、改写或脱敏。
    """
    joined = "\n".join(request.messages).lower()
    if "api_key" in joined or "password" in joined or "密钥" in joined:
        return SamplingDecision(False, "请求中疑似包含敏感凭据，拒绝 Sampling。", [])
    if request.max_tokens > 1000:
        return SamplingDecision(False, "max_tokens 超过课堂策略上限。", [])

    redacted = [message.replace("/workspace", "<WORKSPACE>") for message in request.messages]
    return SamplingDecision(True, "通过策略审核，可转发给模型。", redacted)


def mock_model_response(messages: List[str]) -> str:
    """模拟 Client 调用 LLM 后返回给 Server 的结果。"""
    return "建议摘要：这组笔记主要讨论 MCP 的标准化工具接入、Resources 与 Tools 的区别，以及安全审核。"


def main() -> None:
    requests = [
        SamplingRequest(
            server_name="note-manager",
            purpose="根据笔记生成摘要策略",
            messages=["请总结 /workspace/agent_course_2026 中关于 MCP 的笔记。"],
            max_tokens=300,
        ),
        SamplingRequest(
            server_name="unknown-server",
            purpose="分析配置",
            messages=["请读取这段配置：OPENAI_API_KEY=<redacted>"],
            max_tokens=300,
        ),
    ]

    for request in requests:
        print(f"=== Sampling from {request.server_name} ===")
        print(f"purpose: {request.purpose}")
        decision = review_sampling_request(request)
        print(f"decision: {'ALLOW' if decision.allowed else 'DENY'}")
        print(f"reason: {decision.reason}")
        if decision.allowed:
            print("redacted_messages:")
            for message in decision.redacted_messages:
                print(f"- {message}")
            print(f"model_result: {mock_model_response(decision.redacted_messages)}")
        print()


if __name__ == "__main__":
    main()
