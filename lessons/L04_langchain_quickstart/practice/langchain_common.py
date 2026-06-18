#!/usr/bin/env python3
"""Shared helpers for L04 LangChain demos.

这个文件集中放置环境加载、模型构造和基础工具，避免每个示例重复样板代码。
学生阅读时可以把它理解为“课程版 LangChain 小工具箱”。

建议阅读顺序：
1. 先看 build_llm()：理解 LangChain 如何复用课程 .env 中的模型配置。
2. 再看 @tool 标注的三个工具：理解“普通函数如何变成模型可调用工具”。
3. 最后看 final_text()/print_message_trace()：理解 Agent 执行结果怎么被取出和观察。
"""

from __future__ import annotations

import ast
import json
import operator
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Dict, Iterable, List

from dotenv import load_dotenv
from langchain_core.tools import BaseTool, tool
from langchain_openai import ChatOpenAI


# 课堂里先用固定 mock 数据，目的是把注意力放在工具调用协议上。
# 真实项目中，这里通常会换成天气 API、数据库查询或公司内部服务。
WEATHER_DATA = {
    "北京": {"temp": "15-25°C", "weather": "晴", "humidity": "30%"},
    "上海": {"temp": "18-22°C", "weather": "多云", "humidity": "65%"},
    "深圳": {"temp": "22-30°C", "weather": "阵雨", "humidity": "80%"},
}


def find_project_root() -> Path:
    """从当前文件向上寻找课程根目录，保证所有示例都加载同一份 .env。"""
    for parent in Path(__file__).resolve().parents:
        if (parent / ".env").exists() or (parent / ".env.example").exists():
            return parent
    raise RuntimeError("Cannot find project root with .env or .env.example")


def load_project_env() -> Path:
    """加载课程根目录的 .env，并返回根目录路径供工具做路径校验。"""
    root = find_project_root()
    # override=False 很重要：如果你在 shell 里临时指定了环境变量，它不会被 .env 覆盖。
    # 这让同一份代码可以在“课堂默认配置”和“临时调试配置”之间自然切换。
    load_dotenv(root / ".env", override=False)
    return root


def read_int_env(name: str, default: int) -> int:
    """读取整数型运行配置；无效值回退默认值，避免课堂演示被配置细节卡住。"""
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
    """读取浮点型运行配置，例如 LangChain 请求超时时间。"""
    raw = os.getenv(name, "").strip()
    if not raw:
        return default
    try:
        value = float(raw)
        return value if value > 0 else default
    except Exception:
        print(f"[WARN] Invalid {name}={raw!r}, fallback to {default}")
        return default


def build_llm() -> ChatOpenAI:
    """根据课程 .env 创建 ChatOpenAI；这是 LangChain 对模型调用的封装层。"""
    load_project_env()

    # 这里和 L01-L03 的 OpenAI client 构造是一一对应的：
    # L03: OpenAI(api_key=..., base_url=...) + chat.completions.create(...)
    # L04: ChatOpenAI(...)，后续交给 LangChain Agent 调用。
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    base_url = os.getenv("OPENAI_BASE_URL", "").strip()
    model = os.getenv("OPENAI_MODEL", "").strip()
    missing = [
        name
        for name, value in {
            "OPENAI_API_KEY": api_key,
            "OPENAI_BASE_URL": base_url,
            "OPENAI_MODEL": model,
        }.items()
        if not value
    ]
    if missing:
        raise RuntimeError(f"Missing required env vars: {', '.join(missing)}")

    # temperature=0 让课堂演示更稳定；timeout/max_retries 则让网络抖动时更容易恢复。
    # 注意：这里仍然使用 OpenAI 兼容接口，只是被包装成 LangChain 的模型对象。
    return ChatOpenAI(
        model=model,
        temperature=0,
        api_key=api_key,
        base_url=base_url,
        timeout=read_float_env("LC_REQUEST_TIMEOUT_SEC", 45.0),
        max_retries=read_int_env("LC_MAX_RETRIES", 2),
    )


@tool
def get_weather(city: str) -> str:
    """查询指定城市的当前天气，包括温度、天气状况和湿度。"""
    # @tool 会读取函数名、类型标注和 docstring，生成模型可见的工具 schema。
    # 因此函数名和 docstring 不是随便写的，它们会直接影响模型是否选对工具。
    data = WEATHER_DATA.get(city, {"temp": "未知", "weather": "未知", "humidity": "未知"})
    # 工具返回 JSON 字符串，是为了让模型看到结构化字段，而不是一段难解析的自然语言。
    return json.dumps({"city": city, **data}, ensure_ascii=False)


@tool
def get_current_time() -> str:
    """获取当前日期、时间和星期。"""
    # 这是一个“零参数工具”：模型只需要决定是否调用，不需要补充额外参数。
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
    """只允许基础数学 AST 节点，避免示例代码使用危险的 eval。"""
    # 不直接 eval(expression) 的原因：
    # 用户输入可能是任意字符串，eval 会把字符串当 Python 代码执行，风险极高。
    # AST 白名单的做法是：先把表达式解析成语法树，只允许数字和基础运算节点通过。
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
        # 只解释白名单节点；变量、函数调用、属性访问都会被拒绝。
        if isinstance(node, ast.Expression):
            return eval_node(node.body)
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return node.value
        if isinstance(node, ast.BinOp) and type(node.op) in operators:
            return operators[type(node.op)](eval_node(node.left), eval_node(node.right))
        if isinstance(node, ast.UnaryOp) and type(node.op) in unary_operators:
            return unary_operators[type(node.op)](eval_node(node.operand))
        raise ValueError("unsupported expression")

    return eval_node(ast.parse(expression, mode="eval"))


@tool
def calculate(expression: str) -> str:
    """进行安全的数学计算，支持加减乘除、括号、取余和乘方。"""
    try:
        # 允许用户写百分号，比如 22%，内部转成 /100 后再进入安全计算。
        normalized = expression.replace("%", "/100")
        result = safe_eval(normalized)
        return json.dumps({"expression": expression, "result": result}, ensure_ascii=False)
    except Exception as exc:
        # 工具失败时不要直接抛异常给 Agent 主循环。
        # 返回结构化 error，模型才有机会解释失败原因或请求用户改写输入。
        return json.dumps({"expression": expression, "error": str(exc)}, ensure_ascii=False)


# 这一组工具对齐 L03 的基础能力，供多个 LangChain Agent 示例复用。
# 读者可以把它理解成“给 Agent 装上的三只手”：查天气、看时间、做计算。
DEFAULT_TOOLS: List[BaseTool] = [get_weather, get_current_time, calculate]


def final_text(result: Dict[str, Any]) -> str:
    """从 LangChain/LangGraph Agent 的 result 中取最后一条消息内容。"""
    # create_agent 返回的不是单纯字符串，而是一个包含 messages 的状态字典。
    # 最后一条消息通常就是模型给用户的最终回答。
    messages = result.get("messages", [])
    if not messages:
        return ""
    return str(getattr(messages[-1], "content", messages[-1]))


def describe_tools(tools: Iterable[BaseTool]) -> None:
    """打印工具元数据，帮助学生看到模型实际获得的工具说明。"""
    # 这个函数适合课上先跑一遍：
    # python practice/08_custom_tools.py --describe
    # 学生会直观看到 @tool + 类型标注 + Pydantic schema 最终变成了什么。
    for item in tools:
        print(f"\n[TOOL] {item.name}")
        print(f"description: {item.description}")
        print(f"args: {json.dumps(item.args, ensure_ascii=False, indent=2)}")


def print_message_trace(result: Dict[str, Any]) -> None:
    """打印 Agent 消息轨迹，适合调试模型是否真的调用了工具。"""
    # 如果只看最终回答，很难判断 Agent 是否真的调用了工具。
    # trace 会把中间消息、tool_calls 等信息打印出来，对理解 ReAct 流程很有帮助。
    print("\n=== MESSAGE TRACE ===")
    for index, message in enumerate(result.get("messages", []), 1):
        role = getattr(message, "type", type(message).__name__)
        content = getattr(message, "content", "")
        tool_calls = getattr(message, "tool_calls", None)
        print(f"\n[{index}] {role}")
        if content:
            print(content)
        if tool_calls:
            print(f"tool_calls: {json.dumps(tool_calls, ensure_ascii=False)}")
