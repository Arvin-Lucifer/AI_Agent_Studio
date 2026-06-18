#!/usr/bin/env python3
"""Minimal lesson-1 demo: ChatBot vs Agent loop.

ChatBot 只根据用户目标直接回答；Agent 则拆成 Observe/Think/Act/Reflect：
先规划要不要用工具，再执行工具，最后把工具结果转成行动建议。

建议阅读顺序：
1. 先看 run_chatbot_mode()：普通 ChatBot 只把目标交给模型直接回答。
2. 再看 run_agent_mode()：Agent 会先输出 JSON 计划，再执行工具，再反思生成答案。
3. 最后看 print_agent_logs()：观察 Observe/Think/Act/Reflect 四个阶段的日志。

Usage:
    python practice/demo_chatbot_vs_agent.py --mode both
    python practice/demo_chatbot_vs_agent.py --mode agent --goal "帮我安排今天的工作计划"
"""

from __future__ import annotations

import argparse
import json
import os
import re
import time
from pathlib import Path
from typing import Any, Dict, List

from dotenv import load_dotenv
from openai import APIConnectionError, APIStatusError, APITimeoutError, OpenAI, RateLimitError


DEFAULT_GOAL = "我今天有很多任务，帮我排优先级并给出可执行日程。"

# 这里用 mock 任务模拟真实外部系统。
# 在真实产品里，这些数据可能来自日历、工单系统、项目管理工具或数据库。
MOCK_TASKS = [
    {"title": "完成客户周报", "deadline": "today 17:00", "importance": "high", "estimate_min": 50},
    {"title": "回复两封普通邮件", "deadline": "today", "importance": "low", "estimate_min": 15},
    {"title": "准备明天分享会的提纲", "deadline": "tomorrow 10:00", "importance": "high", "estimate_min": 40},
    {"title": "修复线上登录小 bug", "deadline": "today", "importance": "medium", "estimate_min": 35},
]


def find_project_root() -> Path:
    """向上寻找课程根目录，支持从项目根目录或 lesson 目录运行脚本。"""
    for parent in Path(__file__).resolve().parents:
        if (parent / ".env").exists() or (parent / ".env.example").exists():
            return parent
    raise RuntimeError("Cannot find project root with .env or .env.example")


def load_project_env() -> None:
    root = find_project_root()
    env_path = root / ".env"
    # 这个 demo 需要真实模型调用，所以启动时先加载根目录 .env。
    load_dotenv(env_path, override=False)


def build_client() -> tuple[OpenAI, str]:
    """创建 OpenAI client；把环境变量缺失集中报错，便于学员定位配置问题。"""
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    base_url = os.getenv("OPENAI_BASE_URL", "").strip()
    model = os.getenv("OPENAI_MODEL", "").strip()

    missing = []
    if not api_key:
        missing.append("OPENAI_API_KEY")
    if not base_url:
        missing.append("OPENAI_BASE_URL")
    if not model:
        missing.append("OPENAI_MODEL")
    if missing:
        raise RuntimeError(f"Missing required env vars: {', '.join(missing)}")

    client = OpenAI(api_key=api_key, base_url=base_url)
    return client, model


def _read_int_env(name: str, default: int) -> int:
    """读取整数型重试配置，保证课堂网络不稳时仍有最小恢复能力。"""
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
    """读取浮点型超时/退避配置。"""
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


def llm_text(client: OpenAI, model: str, messages: List[Dict[str, str]], temperature: float = 0.2) -> str:
    """统一封装一次文本生成调用，后面的 ChatBot 和 Agent 都复用它。"""
    # 统一入口的好处：重试、超时、错误处理只写一次。
    # run_chatbot_mode 和 run_agent_mode 的差异就能集中体现在 prompt 与流程上。
    max_attempts = _read_int_env("DEMO_MAX_ATTEMPTS", 3)
    request_timeout = _read_float_env("DEMO_REQUEST_TIMEOUT_SEC", 40.0)
    backoff_sec = _read_float_env("DEMO_RETRY_BACKOFF_SEC", 2.0)

    for attempt in range(1, max_attempts + 1):
        try:
            resp = client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                timeout=request_timeout,
            )
            content = resp.choices[0].message.content
            return content or ""
        except (APITimeoutError, APIConnectionError, RateLimitError) as exc:
            if attempt == max_attempts:
                raise
            sleep_sec = backoff_sec * attempt
            print(
                f"[WARN] LLM attempt {attempt}/{max_attempts} failed: "
                f"{type(exc).__name__}. Retry in {sleep_sec:.1f}s ..."
            )
            time.sleep(sleep_sec)
        except APIStatusError as exc:
            if exc.status_code is not None and exc.status_code >= 500 and attempt < max_attempts:
                sleep_sec = backoff_sec * attempt
                print(
                    f"[WARN] LLM attempt {attempt}/{max_attempts} failed: "
                    f"APIStatusError({exc.status_code}). Retry in {sleep_sec:.1f}s ..."
                )
                time.sleep(sleep_sec)
                continue
            raise

    return ""


def extract_json_object(text: str) -> Dict[str, Any]:
    """解析规划器输出的 JSON；模型多说了几句时，尝试从文本中抠出 JSON 对象。"""
    # 这里对应 L02 的结构化输出主题：
    # prompt 要求 JSON 不代表模型永远只输出 JSON，所以工程代码仍要解析和兜底。
    text = text.strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # 这是教学用兜底：真实生产系统更建议使用严格结构化输出或 schema 校验。
    match = re.search(r"\{.*\}", text, flags=re.DOTALL)
    if match:
        return json.loads(match.group(0))

    raise ValueError(f"No valid JSON object found in planner output: {text}")


def score_task(task: Dict[str, Any]) -> int:
    """给模拟任务打分，让工具输出具备可解释的优先级。"""
    # 这个打分规则故意简单透明：重要性 + 截止时间 + 预估耗时。
    # 重点不是优化排序算法，而是让工具返回的数据对 Agent 有帮助。
    score = 0
    importance = str(task.get("importance", "")).lower()
    deadline = str(task.get("deadline", "")).lower()

    if "high" in importance:
        score += 50
    elif "medium" in importance:
        score += 25

    if "today" in deadline:
        score += 30
    elif "tomorrow" in deadline:
        score += 10

    estimate = int(task.get("estimate_min", 30))
    if estimate <= 30:
        score += 8
    elif estimate <= 60:
        score += 5

    return score


def tool_list_today_tasks(_: Dict[str, Any]) -> Dict[str, Any]:
    """模拟一个外部工具：真实项目里这里可能是日历、工单或数据库查询。"""
    ranked = sorted(
        [{**t, "priority_score": score_task(t)} for t in MOCK_TASKS],
        key=lambda x: x["priority_score"],
        reverse=True,
    )
    return {
        "timezone": "Asia/Shanghai",
        "date": "today",
        "tasks": ranked,
    }


def run_tool(action: str, action_input: Dict[str, Any]) -> Dict[str, Any]:
    """根据 planner 给出的 action 路由到具体工具。"""
    # 这是第 3 讲 Function Calling 之前的“手写工具路由”雏形：
    # 模型输出 action，代码负责把 action 变成真实函数调用。
    if action == "list_today_tasks":
        return tool_list_today_tasks(action_input)
    raise ValueError(f"Unsupported tool action: {action}")


def run_chatbot_mode(client: OpenAI, model: str, goal: str) -> str:
    """普通 ChatBot：没有工具，也没有显式的 Think/Act 阶段。"""
    # ChatBot 模式刻意要求“不调用任何工具”。
    # 它可能回答得像样，但不知道 MOCK_TASKS 里的真实任务列表。
    messages = [
        {"role": "system", "content": "You are a concise assistant."},
        {
            "role": "user",
            "content": (
                "请直接回答，不调用任何工具。\n"
                f"用户目标：{goal}\n"
                "给一个简洁可执行建议（最多6条）。"
            ),
        },
    ]
    return llm_text(client, model, messages)


def run_agent_mode(client: OpenAI, model: str, goal: str) -> Dict[str, Any]:
    """最小 Agent 循环：Observe -> Think -> Act -> Reflect。"""
    # Observe：用户目标进入系统。
    # Think：planner 选择下一步 action。
    # Act：代码执行工具。
    # Reflect：模型基于工具结果整理最终答案。
    planner_messages = [
        {
            "role": "system",
            "content": (
                # 要求 planner 只输出 JSON，是为了让代码能稳定读取 action 和 action_input。
                "You are a planning module in an agent loop. "
                "You must output ONE JSON object only.\n"
                "Allowed actions: list_today_tasks, final_answer.\n"
                "JSON schema:\n"
                "{\"thought\": str, \"action\": str, \"action_input\": object}\n"
                "If you need external data, choose list_today_tasks first."
            ),
        },
        {
            "role": "user",
            "content": f"Goal: {goal}",
        },
    ]
    planner_raw = llm_text(client, model, planner_messages)
    # planner_raw 是模型文本，必须先解析成 dict，代码才能读取 action/action_input。
    planner_obj = extract_json_object(planner_raw)

    action = str(planner_obj.get("action", "")).strip()
    action_input = planner_obj.get("action_input", {})
    if not isinstance(action_input, dict):
        action_input = {}

    # logs 不是业务必需，但它能把 Agent 的每一步展示出来，适合课堂讲解和调试。
    logs: Dict[str, Any] = {
        "observe": goal,
        "think": planner_obj,
        "act": None,
        "reflect": None,
    }

    if action == "final_answer":
        # 有些目标不需要工具，planner 可以直接 final_answer。
        # 这体现了 Agent 不是“每次都必须调用工具”，而是按需行动。
        answer = str(action_input.get("answer", "")).strip()
        if not answer:
            answer = "Planner chose final_answer directly, but no answer content was provided."
        logs["reflect"] = answer
        return logs

    # Act：执行 planner 选择的工具，并把工具原始结果保留下来。
    tool_output = run_tool(action, action_input)
    logs["act"] = {
        "tool": action,
        "tool_input": action_input,
        "tool_output": tool_output,
    }

    # Reflect：把工具结果转成用户真正需要的自然语言答案。
    # 这一步很像真实 Agent 里的“结果综合”：工具只给数据，模型负责解释和组织。
    reflector_messages = [
        {
            "role": "system",
            "content": (
                "You are the reflection/finalization step of an agent loop. "
                "Generate a clear action plan with concrete order and time blocks."
            ),
        },
        {
            "role": "user",
            "content": (
                f"Goal: {goal}\n"
                f"Tool output JSON: {json.dumps(tool_output, ensure_ascii=False)}\n"
                "请输出：\n"
                "1) 按优先级排序\n"
                "2) 今天的执行计划（带时间块）\n"
                "3) 如果时间不够，哪些任务可延后"
            ),
        },
    ]
    final_answer = llm_text(client, model, reflector_messages)
    logs["reflect"] = final_answer
    return logs


def print_agent_logs(logs: Dict[str, Any]) -> None:
    """打印 Agent 四阶段日志，让学生能看到普通回答背后的执行轨迹。"""
    print("\n=== AGENT LOOP LOG ===")
    print(f"[Observe] {logs.get('observe')}")
    think = logs.get("think")
    print(f"[Think] {json.dumps(think, ensure_ascii=False)}")
    act = logs.get("act")
    if act is None:
        print("[Act] skipped")
    else:
        print(f"[Act] {json.dumps(act, ensure_ascii=False)}")
    print("[Reflect]")
    print(logs.get("reflect"))


def main() -> None:
    parser = argparse.ArgumentParser(description="Lesson-1 demo: ChatBot vs Agent")
    parser.add_argument("--mode", choices=["chatbot", "agent", "both"], default="both")
    parser.add_argument("--goal", type=str, default=DEFAULT_GOAL)
    args = parser.parse_args()

    load_project_env()
    client, model = build_client()

    print(f"Using model: {model}")
    print(f"Goal: {args.goal}")

    if args.mode in {"chatbot", "both"}:
        chatbot_answer = run_chatbot_mode(client, model, args.goal)
        print("\n=== CHATBOT OUTPUT ===")
        print(chatbot_answer)

    if args.mode in {"agent", "both"}:
        logs = run_agent_mode(client, model, args.goal)
        print_agent_logs(logs)


if __name__ == "__main__":
    main()
