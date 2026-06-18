#!/usr/bin/env python3
"""L04 Step 8: custom LangChain tools.

这个脚本展示三种常见工具写法：
简单单参数工具、多参数 Pydantic schema 工具、带安全边界的文件读取工具。

建议先运行 --describe，不调用模型，只观察工具 schema。
这样学生会先理解“模型看到了什么”，再去观察“模型怎么选择工具”。

Usage:
    python practice/08_custom_tools.py --describe
    python practice/08_custom_tools.py "把 Agent 翻译成 English"
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any, Dict, List

from langchain.agents import create_agent
from langchain_core.tools import BaseTool, tool
from pydantic import BaseModel, Field

from langchain_common import build_llm, describe_tools, final_text, find_project_root


@tool
def search_web(query: str) -> str:
    """在互联网上搜索信息。当需要查找最新资讯、事实性问题或背景资料时使用。"""
    # 方式一：最简单的 @tool。
    # LangChain 会把 query: str 变成一个字符串参数，把 docstring 变成工具描述。
    # 课堂示例先用 mock，后续可替换 Tavily、SerpAPI 或内部搜索服务。
    return f"搜索 '{query}' 的模拟结果：找到若干与 AI Agent 和 LangChain 相关的资料。"


class TranslateInput(BaseModel):
    """多参数工具建议显式写 schema，让模型知道每个字段应该填什么。"""

    # 方式二：当工具需要多个参数时，Field(description=...) 很关键。
    # 模型会根据这些字段说明决定 text 和 target_lang 分别应该填什么。
    text: str = Field(description="要翻译的文本")
    target_lang: str = Field(description="目标语言，如 English, Japanese, French")


@tool(args_schema=TranslateInput)
def translate(text: str, target_lang: str) -> str:
    """将文本翻译成指定目标语言。"""
    return f"[翻译成 {target_lang}] {text}"


@tool
def read_course_file(filepath: str) -> str:
    """读取课程目录下的 .txt 或 .md 文件。只能用于查看课程资料，不读取系统敏感文件。"""
    # 方式三：带安全边界的工具。
    # 一旦工具能读文件、写文件、查数据库，就必须先限制作用范围，再谈智能。
    project_root = find_project_root()
    requested = (project_root / filepath).resolve()

    # 防止路径穿越：工具只能读取课程目录内部文件。
    # 例如用户让 Agent 读取 ../../.ssh/id_rsa，这里会被拒绝。
    if project_root not in requested.parents and requested != project_root:
        return "错误：只能读取课程目录下的文件"
    # 文件类型白名单可以降低误读二进制文件、配置文件或敏感文件的风险。
    if requested.suffix.lower() not in {".txt", ".md"}:
        return "错误：只支持读取 .txt 和 .md 文件"
    if not requested.exists():
        return f"错误：文件不存在：{filepath}"

    content = requested.read_text(encoding="utf-8")
    # 工具返回内容太长会挤占上下文窗口，也会让模型难以抓重点。
    # 先截断是最朴素的上下文预算控制，后续 RAG 章节会讲更系统的切分与检索。
    if len(content) > 1000:
        return content[:1000] + "\n...(文件内容过长，已截断)"
    return content


# 工具列表就是这个 Agent 的能力边界。
# 加一个工具，Agent 能做的事就多一类；工具太多，也会增加选错工具的概率。
CUSTOM_TOOLS: List[BaseTool] = [search_web, translate, read_course_file]

# 这里故意写成“工具演示助手”，让模型优先展示工具选择，而不是泛泛聊天。
SYSTEM_PROMPT = (
    "你是一个工具演示助手。根据用户请求选择搜索、翻译或读取课程文件。"
    "如果工具无法完成，要说明原因。"
)


def run_agent(prompt: str) -> str:
    """把自定义工具交给 Agent，观察模型如何根据描述选择工具。"""
    # 对比 07：这里只换了工具列表和 system_prompt，Agent 执行框架完全不变。
    # 这就是框架的好处：业务能力通过工具扩展，通用循环不用重写。
    agent = create_agent(
        model=build_llm(),
        tools=CUSTOM_TOOLS,
        system_prompt=SYSTEM_PROMPT,
    )
    result: Dict[str, Any] = agent.invoke(
        {"messages": [{"role": "user", "content": prompt}]}
    )
    answer = final_text(result)
    print(f"\n[USER] {prompt}")
    print(f"[ASSISTANT] {answer}")
    return answer


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="L04 custom tools demo")
    parser.add_argument("prompt", nargs="?", default="把 LangChain 是 Agent 开发框架 翻译成 English")
    parser.add_argument("--describe", action="store_true", help="Print tool schemas without calling model")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.describe:
        # --describe 不会调用模型，也不会消耗 API；适合先讲工具 schema。
        describe_tools(CUSTOM_TOOLS)
        return
    run_agent(args.prompt)


if __name__ == "__main__":
    main()
