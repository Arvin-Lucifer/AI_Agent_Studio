#!/usr/bin/env python3
"""L01 Step 3: first LLM API call.

这个脚本展示最小可用的 LLM 调用链路：
加载 .env -> 构造 OpenAI client -> 发送 messages -> 读取模型回复。

建议阅读顺序：
1. 先看 load_project_env()：理解课程代码如何统一读取根目录 .env。
2. 再看 main() 里的环境变量校验：理解一次 API 调用需要哪些配置。
3. 最后看 client.chat.completions.create(...)：理解 messages 是如何交给模型的。

Usage:
    python practice/01_hello_llm.py
"""

from __future__ import annotations

import os
import time
from pathlib import Path

from dotenv import load_dotenv
from openai import APIConnectionError, APIStatusError, APITimeoutError, OpenAI, RateLimitError


def find_project_root() -> Path:
    """从当前脚本向上寻找课程根目录，避免依赖固定的执行位置。"""
    # 为什么不直接写 ../../.env？
    # 因为学生可能从项目根目录、lesson 目录或 practice 目录运行脚本。
    # 向上查找 .env/.env.example，可以让代码在这些位置都能正常工作。
    for parent in Path(__file__).resolve().parents:
        if (parent / ".env").exists() or (parent / ".env.example").exists():
            return parent
    raise RuntimeError("Cannot find project root with .env or .env.example")


def load_project_env() -> None:
    root = find_project_root()
    # override=False 表示优先保留命令行里已经设置好的环境变量，便于临时调试。
    load_dotenv(root / ".env", override=False)


def _read_int_env(name: str, default: int) -> int:
    """读取整数型配置；配置错误时回退默认值，避免课前检查被小拼写拖住。"""
    raw = os.getenv(name, "").strip()
    if not raw:
        return default
    try:
        value = int(raw)
        if value < 1:
            raise ValueError("must be >= 1")
        return value
    except Exception:
        print(f"[WARN] Invalid {name}={raw!r}, fallback to {default}")
        return default


def _read_float_env(name: str, default: float) -> float:
    """读取浮点型配置，常用于超时时间和重试间隔。"""
    raw = os.getenv(name, "").strip()
    if not raw:
        return default
    try:
        value = float(raw)
        if value <= 0:
            raise ValueError("must be > 0")
        return value
    except Exception:
        print(f"[WARN] Invalid {name}={raw!r}, fallback to {default}")
        return default


def main() -> None:
    load_project_env()

    # API 密钥、网关地址和模型名称都放在 .env 中，代码里不硬编码敏感信息。
    # 这三个变量分别回答：用谁的凭证、请求发到哪里、调用哪个模型。
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    base_url = os.getenv("OPENAI_BASE_URL", "").strip()
    model = os.getenv("OPENAI_MODEL", "").strip()

    if not api_key:
        raise SystemExit("OPENAI_API_KEY is missing. Please set it in .env")
    if not base_url:
        raise SystemExit("OPENAI_BASE_URL is missing. Please set it in .env")
    if not model:
        raise SystemExit("OPENAI_MODEL is missing. Please set it in .env")

    max_attempts = _read_int_env("HELLO_MAX_ATTEMPTS", 3)
    request_timeout = _read_float_env("HELLO_REQUEST_TIMEOUT_SEC", 30.0)
    backoff_sec = _read_float_env("HELLO_RETRY_BACKOFF_SEC", 2.0)

    # OpenAI client 是“和模型服务通信的对象”。
    # L04 之后会看到 LangChain 的 ChatOpenAI，本质上也是对这层调用的封装。
    client = OpenAI(api_key=api_key, base_url=base_url)

    # 真实网络调用可能遇到超时、限流或临时 5xx；初学阶段先掌握最朴素的重试模式。
    for attempt in range(1, max_attempts + 1):
        try:
            # messages 是 Chat Completions 的核心输入：system 定角色，user 给任务。
            # 第一讲先只放 system + user 两条消息；第二个脚本会继续加入 assistant 历史。
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "你是一个友好的AI助手。"},
                    {"role": "user", "content": "用一句话解释什么是AI Agent。"},
                ],
                temperature=0.7,
                timeout=request_timeout,
            )
            # choices[0].message.content 是模型最终文本回复。
            # 后面 Function Calling 章节会看到，message 里还可能带 tool_calls。
            print(response.choices[0].message.content or "")
            return
        except (APITimeoutError, APIConnectionError, RateLimitError) as exc:
            if attempt == max_attempts:
                raise
            sleep_sec = backoff_sec * attempt
            print(
                f"[WARN] attempt {attempt}/{max_attempts} failed: "
                f"{type(exc).__name__}. Retry in {sleep_sec:.1f}s ..."
            )
            time.sleep(sleep_sec)
        except APIStatusError as exc:
            if exc.status_code is not None and exc.status_code >= 500 and attempt < max_attempts:
                sleep_sec = backoff_sec * attempt
                print(
                    f"[WARN] attempt {attempt}/{max_attempts} failed: "
                    f"APIStatusError({exc.status_code}). Retry in {sleep_sec:.1f}s ..."
                )
                time.sleep(sleep_sec)
                continue
            raise


if __name__ == "__main__":
    main()
