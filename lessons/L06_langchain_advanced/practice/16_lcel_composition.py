#!/usr/bin/env python3
"""L06 Step 16: LCEL composition patterns.

这个脚本展示三种组合方式：
顺序串联、并行执行、条件路由。

建议阅读顺序：
1. run_sequential_chain()：理解上一步输出如何变成下一步输入。
2. run_parallel_chain()：理解多个独立子链如何同时执行。
3. run_branch_chain()：理解如何按输入条件选择不同链路。

Usage:
    python practice/16_lcel_composition.py
"""

from __future__ import annotations

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableBranch, RunnableParallel

from langchain_advanced_common import build_llm


def run_sequential_chain() -> None:
    """顺序链：先生成大纲，再根据大纲写短文。"""
    llm = build_llm()
    parser = StrOutputParser()

    outline_prompt = ChatPromptTemplate.from_template(
        "请为主题「{topic}」生成一个 3 点文章大纲，每点一行。"
    )
    article_prompt = ChatPromptTemplate.from_template(
        "请根据以下大纲，写一篇 200 字以内的短文：\n\n{outline}"
    )

    outline_chain = outline_prompt | llm | parser

    # {"outline": outline_chain} 表示先运行 outline_chain，
    # 并把它的输出放到下一步 prompt 所需的 outline 字段里。
    article_chain = {"outline": outline_chain} | article_prompt | llm | parser

    print("\n=== 顺序链：大纲 -> 文章 ===")
    print(article_chain.invoke({"topic": "AI Agent 的未来"}))


def run_parallel_chain() -> None:
    """并行链：同一段文本同时生成中文和英文摘要。"""
    llm = build_llm()
    parser = StrOutputParser()
    cn_prompt = ChatPromptTemplate.from_template("用中文一句话总结：{text}")
    en_prompt = ChatPromptTemplate.from_template("Summarize in one English sentence: {text}")

    # 两个子链没有依赖关系，所以可以并行。
    parallel_chain = RunnableParallel(
        chinese=cn_prompt | llm | parser,
        english=en_prompt | llm | parser,
    )

    text = "LangChain 是一个用于构建大语言模型应用的开源框架，提供工具调用、记忆管理、检索增强等能力。"
    result = parallel_chain.invoke({"text": text})
    print("\n=== 并行链：双语摘要 ===")
    print(f"中文摘要: {result['chinese']}")
    print(f"英文摘要: {result['english']}")


def run_branch_chain() -> None:
    """分支链：短问题直接答，长问题分步骤答。"""
    llm = build_llm()
    parser = StrOutputParser()
    short_prompt = ChatPromptTemplate.from_template("请直接回答这个问题：{input}")
    long_prompt = ChatPromptTemplate.from_template("这是一个复杂问题，请分步骤详细回答：{input}")

    # RunnableBranch 从上到下判断条件，命中第一个条件就走对应链。
    branch_chain = RunnableBranch(
        (lambda x: len(x["input"]) > 50, long_prompt | llm | parser),
        short_prompt | llm | parser,
    )

    print("\n=== 条件分支：短问题 ===")
    print(branch_chain.invoke({"input": "Python 是什么？"}))
    print("\n=== 条件分支：长问题 ===")
    print(
        branch_chain.invoke(
            {
                "input": "请解释 Python 中装饰器的工作原理，包括闭包概念、常见使用场景和实际开发中的例子。"
            }
        )
    )


def main() -> None:
    run_sequential_chain()
    run_parallel_chain()
    run_branch_chain()


if __name__ == "__main__":
    main()
