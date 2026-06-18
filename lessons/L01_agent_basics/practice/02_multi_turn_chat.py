#!/usr/bin/env python3
"""L01 Step 4: multi-turn chat with minimal memory.

这个脚本把每轮 user/assistant 消息追加到 messages 中，让模型在下一轮看到上下文。
它不是长期记忆系统，但足以说明“对话状态”是怎样被传回模型的。

建议阅读顺序：
1. 先看 run_chat() 里的 messages 列表：它就是最小多轮记忆。
2. 再看 chat_once()：每次调用都会把完整 messages 发给模型。
3. 最后看 while 循环：理解用户输入和模型回复如何一轮轮追加。

Usage:
    python practice/02_multi_turn_chat.py
    python practice/02_multi_turn_chat.py --system "你是一个资深Python老师。"
"""

from __future__ import annotations

import argparse
import os
import time
from pathlib import Path
from typing import Dict, List

from dotenv import load_dotenv
from openai import APIConnectionError, APIStatusError, APITimeoutError, OpenAI, RateLimitError


DEFAULT_SYSTEM_PROMPT = "你是一个友好的AI助手，回答简洁明了。"
# system prompt 是对话的“角色和行为边界”。
# 命令行 --system 可以临时替换它，适合课堂上观察不同角色设定对回答的影响。


def find_project_root() -> Path:
    """从脚本位置向上找课程根目录，保证从任意目录运行都能加载同一份 .env。"""
    for parent in Path(__file__).resolve().parents:
        if (parent / ".env").exists() or (parent / ".env.example").exists():
            return parent
    raise RuntimeError("Cannot find project root with .env or .env.example")


def load_project_env() -> None:
    root = find_project_root()
    # 同一门课程共用根目录 .env，避免每一讲都复制密钥配置。
    load_dotenv(root / ".env", override=False)


def _read_int_env(name: str, default: int) -> int:
    """读取整数型运行参数，例如最大重试次数。"""
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
    """读取浮点型运行参数，例如请求超时和重试退避秒数。"""
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
    """集中校验 OpenAI 相关环境变量，主流程只关心 client 和 model。"""
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


def chat_once(
    client: OpenAI,
    model: str,
    messages: List[Dict[str, str]],
    temperature: float,
) -> str:
    """发送一次完整上下文，而不是只发送当前这一句话。"""
    # 这个函数故意只做“一次模型调用”。
    # 记忆并不在模型里自动保存，而是由调用方把历史 messages 再次传进来。
    max_attempts = _read_int_env("MULTITURN_MAX_ATTEMPTS", 3)
    request_timeout = _read_float_env("MULTITURN_REQUEST_TIMEOUT_SEC", 40.0)
    backoff_sec = _read_float_env("MULTITURN_RETRY_BACKOFF_SEC", 2.0)

    for attempt in range(1, max_attempts + 1):
        try:
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                # temperature 越高越发散，越低越稳定；聊天演示用 0.7 保留一点自然表达。
                temperature=temperature,
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


def run_chat(system_prompt: str, temperature: float) -> None:
    load_project_env()
    client, model = build_client()

    # messages 就是这个最小聊天机器人的“短期记忆”。
    # 每一轮都把完整列表发给模型，所以列表越长，上下文越完整，token 成本也越高。
    # 这也是后续“记忆压缩、摘要记忆、向量记忆”要解决的问题来源。
    messages: List[Dict[str, str]] = [{"role": "system", "content": system_prompt}]

    print("=" * 60)
    print("  多轮对话程序（输入 quit / exit / q 退出）")
    print(f"  Model: {model}")
    print("=" * 60)

    while True:
        try:
            user_input = input("\n你: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n再见！")
            break

        if not user_input:
            continue

        if user_input.lower() in {"quit", "exit", "q"}:
            print("再见！")
            break

        # 先记录用户输入，再请求模型；否则模型看不到刚刚这一轮问题。
        messages.append({"role": "user", "content": user_input})
        assistant_message = chat_once(client, model, messages, temperature=temperature)
        # 再记录模型回复，下一轮对话才能延续刚刚的回答。
        messages.append({"role": "assistant", "content": assistant_message})

        print(f"\nAI: {assistant_message}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="L01 Step 4: multi-turn chat")
    parser.add_argument("--system", type=str, default=DEFAULT_SYSTEM_PROMPT, help="System prompt")
    parser.add_argument("--temperature", type=float, default=0.7, help="Sampling temperature")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_chat(system_prompt=args.system, temperature=args.temperature)


if __name__ == "__main__":
    main()
