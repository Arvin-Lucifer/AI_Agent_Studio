#!/usr/bin/env python3
"""L02 Step 3: structured output with JSON parsing fallback.

Prompt 可以要求模型输出 JSON，但工程代码仍然要负责解析、兜底和错误报告。
这正是结构化输出从“提示词技巧”走向“可靠程序接口”的关键一步。

建议阅读顺序：
1. 先看 SYSTEM_PROMPT：它定义了模型输出的字段契约。
2. 再看 extract_json_object()：它展示代码如何处理“不完全听话”的模型输出。
3. 最后看 extract_info()：它把模型调用、JSON 解析和错误兜底串起来。

Usage:
    python practice/03_structured_output.py
"""

from __future__ import annotations

import json
import os
import re
import time
from pathlib import Path
from typing import Any, Dict

from dotenv import load_dotenv
from openai import APIConnectionError, APIStatusError, APITimeoutError, OpenAI, RateLimitError


# 这段 system prompt 相当于“输出契约”：告诉模型字段、类型和禁止额外文本。
# 读 prompt 时重点看四件事：角色、任务、字段名、输出限制。
SYSTEM_PROMPT = """你是一个信息提取助手。
用户会给你一段文本，你需要从中提取结构化信息。

请严格按照以下 JSON 格式输出，不要输出任何其他内容：
{
  "people": ["提到的人名列表"],
  "locations": ["提到的地点列表"],
  "dates": ["提到的日期列表"],
  "summary": "一句话摘要"
}
"""

# SAMPLE_TEXT 是固定测试样本。
# 固定输入能减少随机变量，方便课堂上比较 prompt 或解析逻辑的变化。
SAMPLE_TEXT = """
2024年3月15日，张三和李四在北京参加了人工智能大会。
会议期间，他们与来自上海的王五讨论了大模型的最新进展。
会后，团队计划于4月1日在深圳举办一场技术研讨会。
"""


def find_project_root() -> Path:
    """从当前文件向上找课程根目录，保证 .env 加载路径稳定。"""
    for parent in Path(__file__).resolve().parents:
        if (parent / ".env").exists() or (parent / ".env.example").exists():
            return parent
    raise RuntimeError("Cannot find project root with .env or .env.example")


def load_project_env() -> None:
    root = find_project_root()
    # 结构化输出实验也复用根目录 .env，保证 L01-L04 都走同一套模型配置。
    load_dotenv(root / ".env", override=False)


def _read_int_env(name: str, default: int) -> int:
    """读取整数型运行配置；配置无效时给出警告并使用默认值。"""
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
    """读取浮点型运行配置，例如超时秒数。"""
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
    """创建模型客户端，并在缺少必要环境变量时尽早失败。"""
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


def extract_json_object(text: str) -> Dict[str, Any]:
    """把模型文本转成 dict；先按纯 JSON 解析，失败后再尝试提取 JSON 片段。"""
    # 第一层：理想情况，模型只输出 JSON，json.loads 直接成功。
    text = text.strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # 兜底只适合教学和低风险场景；生产系统建议配合更严格的 schema 校验。
    # 第二层：模型可能在 JSON 前后加解释文字，这里尝试提取第一个 JSON 对象。
    # 注意这个正则不是通用 JSON 解析器，只是让初学者先看到“兜底意识”。
    match = re.search(r"\{.*\}", text, flags=re.DOTALL)
    if not match:
        raise ValueError("No JSON object found in model output.")
    return json.loads(match.group(0))


def extract_info(client: OpenAI, model: str, text: str) -> Dict[str, Any]:
    """执行一次信息抽取：调用模型、解析 JSON，并把可恢复错误转成结构化 error。"""
    # 这个函数体现“Prompt + 程序”的分工：
    # Prompt 负责尽量让模型输出 JSON，程序负责检查 JSON 是否真的可用。
    max_attempts = _read_int_env("STRUCTURED_MAX_ATTEMPTS", 3)
    request_timeout = _read_float_env("STRUCTURED_REQUEST_TIMEOUT_SEC", 40.0)
    backoff_sec = _read_float_env("STRUCTURED_RETRY_BACKOFF_SEC", 2.0)

    for attempt in range(1, max_attempts + 1):
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    # system 给输出契约，user 给待抽取文本。
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": text},
                ],
                temperature=0,
                timeout=request_timeout,
            )
            result_text = response.choices[0].message.content or ""
            # 这一步是结构化输出最关键的工程动作：
            # 不要把模型文本直接当 dict 用，必须显式解析。
            return extract_json_object(result_text)
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
        except ValueError as exc:
            # 解析失败不是网络错误，不需要盲目重试；直接返回结构化 error 更利于调试。
            return {"error": str(exc)}
        except json.JSONDecodeError as exc:
            return {"error": f"JSON decode failed: {exc}"}

    return {"error": "Unknown extraction failure"}


def main() -> None:
    load_project_env()
    client, model = build_client()
    print(f"Using model: {model}")
    result = extract_info(client, model, SAMPLE_TEXT)
    # ensure_ascii=False 保留中文；indent=2 让 JSON 更适合课堂投屏阅读。
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
