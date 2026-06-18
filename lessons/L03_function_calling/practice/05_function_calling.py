#!/usr/bin/env python3
"""L03: basic Function Calling demo.

这个脚本演示 Function Calling 的完整闭环：
模型选择工具 -> 代码执行工具 -> 工具结果回填给模型 -> 模型生成最终回答。

建议阅读顺序：
1. 先看 TOOLS：理解模型能看到的工具说明书长什么样。
2. 再看 TOOL_FUNCTIONS / tool_result_for()：理解工具名如何映射到真实 Python 函数。
3. 最后看 run_agent()：理解 assistant tool_calls 和 tool result 如何一轮轮回填。

Usage:
    python practice/05_function_calling.py --demo
    python practice/05_function_calling.py "北京今天天气怎么样？"
"""

from __future__ import annotations

import argparse
import ast
import json
import operator
import os
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Dict, List

from dotenv import load_dotenv
from openai import APIConnectionError, APIStatusError, APITimeoutError, OpenAI, RateLimitError


# 课堂版用固定 mock 天气数据，避免依赖真实天气 API。
# 真实项目里，get_weather 通常会调用第三方 API 或公司内部服务。
WEATHER_DATA = {
    "北京": {"temp": "15-25°C", "weather": "晴", "humidity": "30%"},
    "上海": {"temp": "18-22°C", "weather": "多云", "humidity": "65%"},
    "深圳": {"temp": "22-30°C", "weather": "阵雨", "humidity": "80%"},
}

# TOOLS 是“给模型看的工具说明书”，不是 Python 函数本身。
# 模型会根据 name/description/parameters 决定是否调用工具以及传什么参数。
# 读每个工具 schema 时重点看三处：
# 1. name：模型返回 tool_call 时会使用这个名字。
# 2. description：模型判断“什么时候用这个工具”的主要依据。
# 3. parameters：模型需要按这个 JSON Schema 生成参数。
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "查询指定城市的当前天气，包括温度、天气状况和湿度。当用户询问天气、穿衣建议或出行建议时使用。不用于查询空气质量或历史天气。",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "城市名称，如：北京、上海、深圳"},
                },
                "required": ["city"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "获取当前日期、时间和星期。当用户询问现在几点、今天日期、今天星期几时使用。",
            "parameters": {"type": "object", "properties": {}},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "进行安全的数学计算，支持加减乘除、括号和百分号。不用于单位换算或复杂金融分析。",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {"type": "string", "description": "数学表达式，如：(1+2)*3"},
                },
                "required": ["expression"],
            },
        },
    },
]

SYSTEM_PROMPT = (
    "你是一个有用的助手，可以查天气、看时间、做计算。"
    "需要真实数据或计算时调用工具；不需要工具时直接回答。回答要简洁友好。"
)
# system prompt 负责整体策略，TOOLS 负责可调用能力。
# 两者要互相配合：prompt 说“需要真实数据时调用工具”，TOOLS 才告诉模型有哪些工具可用。


def find_project_root() -> Path:
    """向上寻找课程根目录，保证 .env 可以被稳定加载。"""
    for parent in Path(__file__).resolve().parents:
        if (parent / ".env").exists() or (parent / ".env.example").exists():
            return parent
    raise RuntimeError("Cannot find project root with .env or .env.example")


def load_project_env() -> None:
    # Function Calling 示例仍然复用课程根目录 .env，保证模型和网关配置统一。
    load_dotenv(find_project_root() / ".env", override=False)


def read_int_env(name: str, default: int) -> int:
    """读取整数型运行配置；无效值回退默认值。"""
    raw = os.getenv(name, "").strip()
    if not raw:
        return default
    try:
        value = int(raw)
        return value if value >= 1 else default
    except Exception:
        print(f"[WARN] Invalid {name}={raw!r}, fallback to {default}")
        return default


def read_float_env(name: str, default: float) -> float:
    """读取浮点型运行配置；常用于超时和重试退避。"""
    raw = os.getenv(name, "").strip()
    if not raw:
        return default
    try:
        value = float(raw)
        return value if value > 0 else default
    except Exception:
        print(f"[WARN] Invalid {name}={raw!r}, fallback to {default}")
        return default


def build_client() -> tuple[OpenAI, str]:
    """创建 OpenAI client，同时检查 Function Calling demo 必需的环境变量。"""
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    base_url = os.getenv("OPENAI_BASE_URL", "").strip()
    model = os.getenv("OPENAI_MODEL", "").strip()
    missing = [name for name, value in {
        "OPENAI_API_KEY": api_key,
        "OPENAI_BASE_URL": base_url,
        "OPENAI_MODEL": model,
    }.items() if not value]
    if missing:
        raise RuntimeError(f"Missing required env vars: {', '.join(missing)}")
    return OpenAI(api_key=api_key, base_url=base_url), model


def get_weather(city: str) -> str:
    """模拟天气工具；真实系统里通常会调用天气 API 或内部服务。"""
    data = WEATHER_DATA.get(city, {"temp": "未知", "weather": "未知", "humidity": "未知"})
    # 工具返回 JSON 字符串，方便模型按字段读取城市、温度、天气和湿度。
    return json.dumps({"city": city, **data}, ensure_ascii=False)


def get_current_time() -> str:
    """返回当前本地时间；工具结果统一使用 JSON 字符串，方便模型读取。"""
    now = datetime.now()
    weekdays = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
    return json.dumps(
        {
            "date": now.strftime("%Y年%m月%d日"),
            "time": now.strftime("%H:%M:%S"),
            "weekday": weekdays[now.weekday()],
        },
        ensure_ascii=False,
    )


def safe_eval(expression: str) -> float:
    """只允许基础数学 AST 节点，避免直接 eval 带来的代码执行风险。"""
    # 用户可能让 calculate 执行任意字符串。
    # 如果直接 eval，会把用户输入当 Python 代码运行；AST 白名单只允许数学表达式。
    operators: Dict[type, Callable[[Any, Any], Any]] = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Mod: operator.mod,
        ast.Pow: operator.pow,
    }
    unary_operators: Dict[type, Callable[[Any], Any]] = {
        ast.UAdd: operator.pos,
        ast.USub: operator.neg,
    }

    def eval_node(node: ast.AST) -> Any:
        # 递归解释 AST：遇到不在白名单里的节点就拒绝。
        if isinstance(node, ast.Expression):
            return eval_node(node.body)
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return node.value
        if isinstance(node, ast.BinOp) and type(node.op) in operators:
            return operators[type(node.op)](eval_node(node.left), eval_node(node.right))
        if isinstance(node, ast.UnaryOp) and type(node.op) in unary_operators:
            return unary_operators[type(node.op)](eval_node(node.operand))
        raise ValueError("unsupported expression")

    parsed = ast.parse(expression, mode="eval")
    return eval_node(parsed)


def calculate(expression: str) -> str:
    """数学计算工具；异常也包装成 JSON，让 Agent 有机会基于错误继续处理。"""
    try:
        # 让用户可以写 22% 这种自然表达，内部转换成除以 100。
        normalized = expression.replace("%", "/100")
        result = safe_eval(normalized)
        return json.dumps({"expression": expression, "result": result}, ensure_ascii=False)
    except Exception as exc:
        return json.dumps({"expression": expression, "error": str(exc)}, ensure_ascii=False)


# 这是“工具注册表”：模型返回的是工具名，代码用它找到真正要执行的 Python 函数。
# 注意它和 TOOLS 的区别：
# - TOOLS 给模型看，描述“有哪些工具可以选”。
# - TOOL_FUNCTIONS 给代码用，负责“选中工具后到底执行哪个函数”。
TOOL_FUNCTIONS: Dict[str, Callable[..., str]] = {
    "get_weather": get_weather,
    "get_current_time": get_current_time,
    "calculate": calculate,
}


def parse_tool_args(raw: str) -> Dict[str, Any]:
    """把模型给出的 arguments 字符串转成 dict；解析失败时返回空参数。"""
    # tool_call.function.arguments 在协议里是 JSON 字符串，不是 Python dict。
    # 所以每次执行工具前都要显式 json.loads。
    try:
        data = json.loads(raw or "{}")
        return data if isinstance(data, dict) else {}
    except json.JSONDecodeError:
        return {}


def tool_result_for(name: str, args: Dict[str, Any]) -> str:
    """执行指定工具，并把未知工具、参数错误和运行异常都转成可读 JSON。"""
    func = TOOL_FUNCTIONS.get(name)
    if func is None:
        # 模型理论上只能选 TOOLS 里的工具，但工程代码仍要防御未知工具名。
        return json.dumps({"error": "unknown tool", "tool_name": name}, ensure_ascii=False)
    try:
        return func(**args)
    except TypeError as exc:
        # 参数缺失或参数名不匹配时，不要让程序崩掉；把错误交回模型或日志。
        return json.dumps({"error": "invalid arguments", "detail": str(exc)}, ensure_ascii=False)
    except Exception as exc:
        return json.dumps({"error": type(exc).__name__, "detail": str(exc)}, ensure_ascii=False)


def assistant_message_to_dict(message: Any) -> Dict[str, Any]:
    """把 SDK 的消息对象转成可重新放入 messages 的普通 dict。"""
    # 有 tool_calls 的 assistant 消息必须原样写回 messages。
    # 后面的 role=tool 消息会通过 tool_call_id 和这里的 tool_calls 对应起来。
    data: Dict[str, Any] = {"role": "assistant", "content": message.content}
    if message.tool_calls:
        data["tool_calls"] = [tool_call.model_dump() for tool_call in message.tool_calls]
    return data


def chat_once(client: OpenAI, model: str, messages: List[Dict[str, Any]]) -> Any:
    """发送一次带 tools 的请求；模型可以选择直接回答，也可以返回 tool_calls。"""
    max_attempts = read_int_env("TOOL_MAX_ATTEMPTS", 3)
    request_timeout = read_float_env("TOOL_REQUEST_TIMEOUT_SEC", 40.0)
    backoff_sec = read_float_env("TOOL_RETRY_BACKOFF_SEC", 2.0)
    for attempt in range(1, max_attempts + 1):
        try:
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                # tools 参数就是 Function Calling 和普通聊天调用的关键区别。
                # 传入后，模型可以选择返回 tool_calls，而不是直接输出最终文本。
                tools=TOOLS,
                timeout=request_timeout,
            )
            return response.choices[0].message
        except (APITimeoutError, APIConnectionError, RateLimitError) as exc:
            if attempt == max_attempts:
                raise
            sleep_sec = backoff_sec * attempt
            print(f"[WARN] attempt {attempt}/{max_attempts} failed: {type(exc).__name__}. Retry in {sleep_sec:.1f}s ...")
            time.sleep(sleep_sec)
        except APIStatusError as exc:
            if exc.status_code is not None and exc.status_code >= 500 and attempt < max_attempts:
                sleep_sec = backoff_sec * attempt
                print(f"[WARN] attempt {attempt}/{max_attempts} failed: APIStatusError({exc.status_code}). Retry in {sleep_sec:.1f}s ...")
                time.sleep(sleep_sec)
                continue
            raise
    raise RuntimeError("unreachable chat retry state")


def run_agent(user_input: str, max_steps: int = 4) -> str:
    """运行最小工具 Agent；max_steps 防止模型反复要求调用工具导致死循环。"""
    load_project_env()
    client, model = build_client()
    # messages 保存完整轨迹：用户问题、模型的 tool_call 决策、工具结果和最终回答。
    # 这是手写 Agent 最核心的数据结构，L04 的 create_agent 会把这部分封装起来。
    messages: List[Dict[str, Any]] = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_input},
    ]

    print(f"\n[USER] {user_input}")
    message = chat_once(client, model, messages)

    for step in range(1, max_steps + 1):
        # 没有 tool_calls 表示模型认为已经可以直接回答用户。
        if not message.tool_calls:
            answer = message.content or ""
            print(f"[ASSISTANT] {answer}")
            return answer

        print(f"[AGENT] step={step}, tool_calls={len(message.tool_calls)}")
        # 必须先把 assistant 的 tool_calls 写回历史，否则后续 tool 消息没有上下文归属。
        messages.append(assistant_message_to_dict(message))
        for tool_call in message.tool_calls:
            # 每个 tool_call 都包含：id、function.name、function.arguments。
            # id 用于协议关联，name 用于查注册表，arguments 用于传给真实函数。
            name = tool_call.function.name
            args = parse_tool_args(tool_call.function.arguments)
            print(f"[TOOL CALL] {name}({args})")
            result = tool_result_for(name, args)
            print(f"[TOOL RESULT] {result}")
            # tool_call_id 用来告诉模型：这条工具结果对应前面哪一次工具调用。
            messages.append({"role": "tool", "tool_call_id": tool_call.id, "content": result})

        # 把工具结果交回模型，让它基于真实执行结果继续推理或生成最终答案。
        message = chat_once(client, model, messages)

    final = "工具调用轮次超过上限，已停止以避免循环。"
    # 到达这里通常意味着模型一直要求继续调用工具。
    # max_steps 是最小安全阀，真实系统还会加预算、超时和风险控制。
    print(f"[ASSISTANT] {final}")
    return final


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="L03 basic Function Calling demo")
    parser.add_argument("prompt", nargs="?", default="", help="User prompt")
    parser.add_argument("--demo", action="store_true", help="Run demo prompts")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    demo_prompts = [
        "北京今天天气怎么样？",
        "现在几点了？今天星期几？",
        "帮我算一下，如果一个月工资 15000，扣除 22% 的税和社保，实际到手多少？",
        "给我一句学习 Agent 的鼓励。",
        "现在几点了？北京天气怎么样？适不适合出门？",
    ]
    if args.demo:
        for prompt in demo_prompts:
            run_agent(prompt)
        return
    if not args.prompt:
        raise SystemExit("Please provide a prompt or use --demo")
    run_agent(args.prompt)


if __name__ == "__main__":
    main()
