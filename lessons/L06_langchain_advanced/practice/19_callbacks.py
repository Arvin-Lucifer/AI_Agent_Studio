#!/usr/bin/env python3
"""L06 Step 19: callbacks for observability.

这个脚本展示 Callback 如何观察 LCEL 链路：
chain 开始/结束、LLM 开始/结束、错误事件、耗时和 token。

建议阅读顺序：
1. 先看 AgentMonitor：它定义了我们关心哪些事件。
2. 再看 chain.invoke(..., config={"callbacks": [...]})：Callback 是如何接入的。
3. 最后看 summary：为什么复杂 Agent 需要可观测性。

Usage:
    python practice/19_callbacks.py
"""

from __future__ import annotations

import time
from typing import Any, Dict

from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from langchain_advanced_common import build_llm, summarize_text


class AgentMonitor(BaseCallbackHandler):
    """监控 LangChain 运行过程的回调处理器。"""

    def __init__(self) -> None:
        self.chain_starts = 0
        self.llm_calls = 0
        self.errors = 0
        self.total_tokens = 0
        self.started_at = time.perf_counter()

    def on_chain_start(self, serialized: Dict[str, Any] | None, inputs: Dict[str, Any], **kwargs: Any) -> None:
        self.chain_starts += 1
        # LangChain 内部某些 Runnable 节点可能不给 serialized。
        # Callback 代码要比业务代码更健壮，否则观测系统本身会干扰主链路。
        serialized = serialized or {}
        name = serialized.get("name") or serialized.get("id") or "chain"
        print(f"[CALLBACK] chain_start #{self.chain_starts}: {name} input={summarize_text(inputs)}")

    def on_chain_end(self, outputs: Dict[str, Any], **kwargs: Any) -> None:
        print(f"[CALLBACK] chain_end output={summarize_text(outputs)}")

    def on_llm_start(self, serialized: Dict[str, Any], prompts: list[str], **kwargs: Any) -> None:
        self.llm_calls += 1
        print(f"[CALLBACK] llm_start #{self.llm_calls}: prompt={summarize_text(prompts[0] if prompts else '')}")

    def on_llm_end(self, response: Any, **kwargs: Any) -> None:
        llm_output = getattr(response, "llm_output", None) or {}
        token_usage = llm_output.get("token_usage") or {}
        tokens = int(token_usage.get("total_tokens") or 0)
        self.total_tokens += tokens
        print(f"[CALLBACK] llm_end tokens={tokens}")

    def on_chain_error(self, error: BaseException, **kwargs: Any) -> None:
        self.errors += 1
        print(f"[CALLBACK] chain_error {type(error).__name__}: {error}")

    def on_llm_error(self, error: BaseException, **kwargs: Any) -> None:
        self.errors += 1
        print(f"[CALLBACK] llm_error {type(error).__name__}: {error}")

    def summary(self) -> Dict[str, Any]:
        return {
            "chain_starts": self.chain_starts,
            "llm_calls": self.llm_calls,
            "errors": self.errors,
            "total_tokens": self.total_tokens,
            "elapsed_sec": round(time.perf_counter() - self.started_at, 3),
        }


def main() -> None:
    monitor = AgentMonitor()
    llm = build_llm()
    prompt = ChatPromptTemplate.from_template("用 80 字解释：{topic}")
    chain = prompt | llm | StrOutputParser()

    print("=== 运行 Chain（带 Callback） ===")
    result = chain.invoke({"topic": "什么是 LangChain 的 LCEL"}, config={"callbacks": [monitor]})
    print(f"\n[RESULT] {result}")
    print("\n=== 监控摘要 ===")
    print(monitor.summary())


if __name__ == "__main__":
    main()
