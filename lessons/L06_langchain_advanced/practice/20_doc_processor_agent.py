#!/usr/bin/env python3
"""L06 Step 20: intelligent document processing Agent.

这个综合案例把本讲内容串起来：
Pydantic Parser、RunnableParallel、RunnableLambda、LCEL 管道和报告生成。

建议阅读顺序：
1. 先看 DocumentAnalysis / ActionItems：两个结构化输出契约。
2. 再看三个子链：analysis_chain、action_chain、tldr_chain。
3. 最后看 full_chain：并行结果如何汇总成最终报告。

Usage:
    python practice/20_doc_processor_agent.py
"""

from __future__ import annotations

from typing import List

from langchain_core.output_parsers import PydanticOutputParser, StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda, RunnableParallel
from pydantic import BaseModel, Field

from langchain_advanced_common import SAMPLE_DOCUMENT, build_llm


class DocumentAnalysis(BaseModel):
    """文档基本分析结构。"""

    title: str = Field(description="文档推断标题")
    summary: str = Field(description="100 字以内摘要")
    keywords: List[str] = Field(description="5 个以内关键词")
    sentiment: str = Field(description="情感倾向：正面/中性/负面")
    category: str = Field(description="文档类别：技术/商业/新闻/学术/其他")
    key_points: List[str] = Field(description="3-5 个核心要点")


class ActionItems(BaseModel):
    """从文档中提取可执行建议。"""

    actions: List[str] = Field(description="待办事项或建议")
    priority: str = Field(description="优先级：高/中/低")
    target_audience: str = Field(description="目标读者群体")


def build_analysis_chain(llm: object):
    parser = PydanticOutputParser(pydantic_object=DocumentAnalysis)
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "你是文档分析专家。请按指定格式输出。\n{format_instructions}"),
            ("user", "请分析这篇文档：\n\n{document}"),
        ]
    )
    # 这里用 dict runnable 给 prompt 同时提供 document 和 format_instructions。
    return (
        {
            "document": lambda item: item["document"],
            "format_instructions": lambda _: parser.get_format_instructions(),
        }
        | prompt
        | llm
        | parser
    )


def build_action_chain(llm: object):
    parser = PydanticOutputParser(pydantic_object=ActionItems)
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "你是行动规划专家。请从文档中提取可执行行动项。\n{format_instructions}"),
            ("user", "请从这篇文档中提取行动项：\n\n{document}"),
        ]
    )
    return (
        {
            "document": lambda item: item["document"],
            "format_instructions": lambda _: parser.get_format_instructions(),
        }
        | prompt
        | llm
        | parser
    )


def build_tldr_chain(llm: object):
    prompt = ChatPromptTemplate.from_template("用一句话（不超过30字）概括这篇文档：\n\n{document}")
    return prompt | llm | StrOutputParser()


def generate_report(results: dict) -> str:
    """把三个并行子链的结果合并成 Markdown 报告。"""
    analysis: DocumentAnalysis = results["analysis"]
    actions: ActionItems = results["actions"]
    tldr: str = results["tldr"]

    lines = [
        "# 文档智能分析报告",
        "",
        f"一句话总结：{tldr}",
        "",
        "## 基本信息",
        f"- 标题：{analysis.title}",
        f"- 类别：{analysis.category}",
        f"- 情感：{analysis.sentiment}",
        f"- 关键词：{', '.join(analysis.keywords)}",
        "",
        "## 摘要",
        analysis.summary,
        "",
        "## 核心要点",
    ]
    lines.extend([f"{index}. {point}" for index, point in enumerate(analysis.key_points, 1)])
    lines.extend(
        [
            "",
            f"## 行动建议（优先级：{actions.priority}）",
            f"目标读者：{actions.target_audience}",
        ]
    )
    lines.extend([f"{index}. {action}" for index, action in enumerate(actions.actions, 1)])
    return "\n".join(lines)


def main() -> None:
    llm = build_llm()
    parallel_processor = RunnableParallel(
        analysis=build_analysis_chain(llm),
        actions=build_action_chain(llm),
        tldr=build_tldr_chain(llm),
    )

    # RunnableLambda 把普通 Python 函数接入 LCEL。
    full_chain = parallel_processor | RunnableLambda(generate_report)

    print("正在分析文档（三个子链并行执行）...")
    report = full_chain.invoke({"document": SAMPLE_DOCUMENT})
    print(report)


if __name__ == "__main__":
    main()
