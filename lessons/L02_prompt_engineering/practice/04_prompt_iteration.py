#!/usr/bin/env python3
"""L02 Step 4: prompt iteration experiment (V1 vs V2).

这个实验让学员直观看到：更清晰的职责边界和输出格式，通常会带来更稳定的行为。

建议阅读顺序：
1. 先看 TEST_CASES：它定义了我们要用什么问题评估 prompt。
2. 再看 PROMPT_V1 / PROMPT_V2：比较角色、边界、拒答和输出格式的差异。
3. 最后看 test_prompt()：理解如何用同一批测试用例做 prompt 回归测试。

Usage:
    python practice/04_prompt_iteration.py
"""

from __future__ import annotations

import os
import time
from pathlib import Path
from typing import List

from dotenv import load_dotenv
from openai import APIConnectionError, APIStatusError, APITimeoutError, OpenAI, RateLimitError


# 测试集故意混入非邮件任务，用来观察 prompt 是否能守住能力边界。
# 一个好的 prompt 不只是“会做该做的事”，也要“拒绝不该做的事”。
TEST_CASES = [
    "帮我写一封请假邮件，明天有事",
    "把这段文字翻译成英文：今天天气真好",
    "1+1等于几？",
]

# V1 只有角色，没有边界、格式和拒答规则，容易“什么都答”。
# 它是一个故意设计得比较弱的 baseline。
PROMPT_V1 = "你是一个邮件写作助手。"

# V2 把职责、拒答范围和输出格式显式写清楚，便于对比提示词迭代效果。
# 读 V2 时请观察三层约束：能做什么、不能做什么、输出长什么样。
PROMPT_V2 = """你是一个专业的邮件写作助手。

## 职责
- 只处理邮件相关的请求（写邮件、改邮件、邮件建议）
- 对于非邮件相关的请求，礼貌拒绝并说明你只能帮助处理邮件

## 输出格式
邮件格式如下：
---
主题：<邮件主题>
正文：
<邮件正文>
---
"""


def find_project_root() -> Path:
    """向上定位课程根目录，这样脚本不依赖当前工作目录。"""
    for parent in Path(__file__).resolve().parents:
        if (parent / ".env").exists() or (parent / ".env.example").exists():
            return parent
    raise RuntimeError("Cannot find project root with .env or .env.example")


def load_project_env() -> None:
    root = find_project_root()
    # Prompt 实验也要复用同一模型配置，否则 V1/V2 的对比会混入模型差异。
    load_dotenv(root / ".env", override=False)


def _read_int_env(name: str, default: int) -> int:
    """读取整数型运行配置，例如最大重试次数。"""
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
    """读取浮点型运行配置，例如超时秒数和退避时间。"""
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


def build_client() -> tuple[OpenAI, str]:
    """把 client 构造和环境变量校验收在一起，主实验流程更清楚。"""
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    base_url = os.getenv("OPENAI_BASE_URL", "").strip()
    model = os.getenv("OPENAI_MODEL", "").strip()

    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is missing. Please set it in .env")
    if not base_url:
        raise RuntimeError("OPENAI_BASE_URL is missing. Please set it in .env")
    if not model:
        raise RuntimeError("OPENAI_MODEL is empty. Please set it in .env")

    return OpenAI(api_key=api_key, base_url=base_url), model


def ask_once(client: OpenAI, model: str, system_prompt: str, user_input: str) -> str:
    """用同一个 user_input 测不同 system_prompt，保证对比变量单一。"""
    # 实验设计里的关键原则：一次只改变一个变量。
    # 这里 user_input、model、temperature 都保持一致，只替换 system_prompt。
    max_attempts = _read_int_env("ITER_MAX_ATTEMPTS", 3)
    request_timeout = _read_float_env("ITER_REQUEST_TIMEOUT_SEC", 40.0)
    backoff_sec = _read_float_env("ITER_RETRY_BACKOFF_SEC", 2.0)

    for attempt in range(1, max_attempts + 1):
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    # system_prompt 是本实验唯一真正被比较的变量。
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_input},
                ],
                temperature=0,
                timeout=request_timeout,
            )
            return response.choices[0].message.content or ""
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

    return ""


def test_prompt(client: OpenAI, model: str, system_prompt: str, test_cases: List[str]) -> None:
    """批量跑测试用例，把输入和输出直接打印，方便课堂现场观察差异。"""
    # 这个函数是最小 prompt eval：
    # 没有复杂评分器，但已经具备“固定测试集 + 多版本对比”的基本形态。
    print(f"\n{'=' * 60}")
    print(f"System Prompt Preview: {system_prompt[:80]}...")
    print("=" * 60)

    for idx, user_input in enumerate(test_cases, 1):
        output = ask_once(client, model, system_prompt, user_input)
        print(f"\n--- 测试 {idx} ---")
        print(f"输入: {user_input}")
        print(f"输出: {output}")


def main() -> None:
    load_project_env()
    client, model = build_client()

    print(f"Using model: {model}")
    # 先跑 V1，再跑 V2。课堂上可以让学生先预测差异，再看实际输出。
    print("\n[对比实验] V1 Prompt")
    test_prompt(client, model, PROMPT_V1, TEST_CASES)

    print("\n[对比实验] V2 Prompt")
    test_prompt(client, model, PROMPT_V2, TEST_CASES)


if __name__ == "__main__":
    main()
