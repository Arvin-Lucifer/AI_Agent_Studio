#!/usr/bin/env python3
"""L06 Step 15: LCEL basics.

这个脚本展示最小 LCEL 链：
输入 dict -> Prompt -> LLM -> OutputParser -> str。

建议阅读顺序：
1. 先看 prompt：它把 role/question 填进消息模板。
2. 再看 chain = prompt | llm | parser：理解 LCEL 管道。
3. 最后看 invoke 输入：它必须提供模板所需变量。

Usage:
    python practice/15_lcel_basics.py
"""

from __future__ import annotations

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from langchain_advanced_common import build_llm


def main() -> None:
    llm = build_llm()

    # Prompt 是管道第一站：输入 dict 进入模板，输出 ChatModel 可读的 messages。
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "你是一个{role}，请用 120 字以内的简洁专业语言回答。"),
            ("user", "{question}"),
        ]
    )

    # OutputParser 是管道最后一站：把 AIMessage 解析成普通字符串。
    parser = StrOutputParser()

    # LCEL 的核心就是把 Runnable 用 | 串起来。
    # 读这行时请关注类型变化：dict -> messages -> AIMessage -> str。
    chain = prompt | llm | parser

    result = chain.invoke(
        {
            "role": "Python 技术专家",
            "question": "什么是装饰器？请用简单的例子解释。",
        }
    )
    print(result)


if __name__ == "__main__":
    main()
