# L06 章节总结：LangChain 深入

## 一句话总结

L06 的重点是掌握 LangChain 的核心连接方式 LCEL，以及让链路可组合、可解析、可检索、可观测。

## 核心概念

| 概念 | 本章理解 |
| --- | --- |
| Runnable | LangChain 组件统一调用协议 |
| LCEL | 用 `|` 组合组件的表达式语言 |
| Output Parser | 把模型输出转成文本、JSON 或 Pydantic 对象 |
| Retriever | 将 query 转换成相关文档列表 |
| Callback | 观察 chain、llm、tool、retriever 的运行事件 |
| RunnableParallel | 并行执行多个子链 |
| RunnableBranch | 条件路由 |
| RunnableLambda | 把普通函数接入链 |

## 本章代码地图

- `15_lcel_basics.py`：最小 LCEL 链。
- `16_lcel_composition.py`：串联、并行、分支。
- `17_output_parsers.py`：Pydantic/JSON 输出解析。
- `18_custom_retriever.py`：本地 Hybrid Retriever。
- `19_callbacks.py`：监控回调。
- `20_doc_processor_agent.py`：智能文档处理综合案例。

## 必须记住的工程判断

- LCEL 的关键是组件输入输出类型能接上。
- Parser 不是装饰品，而是把自由文本变成可编程对象。
- Retriever 不只是向量搜索，真实系统常常需要 hybrid、权限、去重、rerank。
- Callback 是复杂 Agent 的可观测性基础。
- 并行链能提升效率，但要注意成本和失败处理。

## 复盘问题

- `prompt | llm | parser` 中每一步输入输出是什么？
- `RunnableParallel` 和顺序链有什么区别？
- Pydantic Parser 相比 JSON Parser 有什么优势？
- 为什么 `content[:100]` 不是可靠去重 key？
- Callback 在生产系统中能做哪些事情？
