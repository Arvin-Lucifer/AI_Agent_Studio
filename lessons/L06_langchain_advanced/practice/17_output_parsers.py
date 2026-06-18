#!/usr/bin/env python3
"""L06 Step 17: structured output parsers.

这个脚本展示两种结构化输出：
PydanticOutputParser 和 JsonOutputParser。

建议阅读顺序：
1. 先看 BookReview / EventInfo：它们定义了期望输出结构。
2. 再看 parser.get_format_instructions()：Parser 会生成格式说明注入 Prompt。
3. 最后看 chain.invoke() 的返回值类型：Pydantic 是对象，JSON 是 dict。

Usage:
    python practice/17_output_parsers.py --mode pydantic
    python practice/17_output_parsers.py --mode json
"""

from __future__ import annotations

import argparse
from typing import List, Optional

from langchain_core.output_parsers import JsonOutputParser, PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

from langchain_advanced_common import build_llm


class BookReview(BaseModel):
    """Pydantic 模型就是结构化输出契约。"""

    title: str = Field(description="书名")
    author: str = Field(description="作者")
    rating: int = Field(description="评分，1-5 分", ge=1, le=5)
    summary: str = Field(description="一句话书评")
    tags: List[str] = Field(description="标签列表，如：编程、入门、实践")


class EventInfo(BaseModel):
    """JSON 模式下也可以用这个结构讲解字段含义。"""

    person: Optional[str] = Field(description="人名，无法确定时为 null")
    action: Optional[str] = Field(description="做了什么")
    location: Optional[str] = Field(description="在哪里")
    time: Optional[str] = Field(description="什么时候")


def run_pydantic_parser() -> None:
    llm = build_llm()
    parser = PydanticOutputParser(pydantic_object=BookReview)
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "你是一个图书评论专家。请按照指定格式输出。\n{format_instructions}"),
            ("user", "请评价这本书：{book_name}"),
        ]
    )

    # 注意这里不是直接让模型“输出 JSON”。
    # parser.get_format_instructions() 会把字段和格式要求注入 prompt。
    chain = prompt | llm | parser
    result = chain.invoke(
        {
            "book_name": "《Python编程：从入门到实践》",
            "format_instructions": parser.get_format_instructions(),
        }
    )

    print("=== Pydantic Parser Result ===")
    print(f"书名: {result.title}")
    print(f"作者: {result.author}")
    print(f"评分: {result.rating}/5")
    print(f"书评: {result.summary}")
    print(f"标签: {', '.join(result.tags)}")
    print(f"字典: {result.model_dump()}")


def run_json_parser() -> None:
    llm = build_llm()
    parser = JsonOutputParser()
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """从用户输入的句子中提取信息，输出 JSON 格式：
{{
  "person": "人名或 null",
  "action": "做了什么或 null",
  "location": "在哪里或 null",
  "time": "什么时候或 null"
}}
不要输出 JSON 以外的文字。""",
            ),
            ("user", "{sentence}"),
        ]
    )
    chain = prompt | llm | parser

    print("=== JSON Parser Results ===")
    for sentence in ["昨天张三在公司完成了项目汇报", "小明下周要去上海出差", "今天天气真好"]:
        result = chain.invoke({"sentence": sentence})
        print(f"输入: {sentence}")
        print(f"输出: {result}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="L06 output parser demo")
    parser.add_argument("--mode", choices=["pydantic", "json", "both"], default="both")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.mode in {"pydantic", "both"}:
        run_pydantic_parser()
    if args.mode in {"json", "both"}:
        run_json_parser()


if __name__ == "__main__":
    main()
