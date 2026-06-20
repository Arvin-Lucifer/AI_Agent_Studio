# 第 6 讲：LangChain 深入 —— Agent 开发核心框架

## 6.1 为什么要深入学 LangChain？

第 4 讲中，我们用 LangChain 快速搭建了一个简单 Agent。但 LangChain 的能力远不止工具调用。它是目前 Agent 开发中最成熟、生态最丰富的框架之一。

本讲目标：

- 理解 LangChain 的分层架构。
- 掌握 LCEL 管道语法。
- 学会组合 Chain：串联、并行、分支。
- 使用 Output Parser 实现结构化输出。
- 设计自定义 Retriever。
- 使用 Callback 监控运行过程。
- 综合搭建智能文档处理 Agent。

## 6.2 LangChain 分层架构

LangChain 不是一个单一库，而是一套模块化框架体系。

```text
应用层    LangGraph（复杂流程编排）
          ↑
编排层    Chain（链式调用）、Agent（自主决策）
          ↑
能力层    Retriever、Memory、Tool、Output Parser
          ↑
模型层    ChatModel、LLM、Embedding
          ↑
基础层    langchain-core（Runnable / LCEL 协议）
```

| 层级 | 核心组件 | 作用 | 类比 |
| --- | --- | --- | --- |
| 基础层 | Runnable / LCEL | 统一调用协议 | USB 接口标准 |
| 模型层 | ChatModel / LLM / Embedding | 封装模型 API | 不同品牌发动机 |
| 能力层 | Retriever / Memory / Tool / Output Parser | 提供功能模块 | 各种零部件 |
| 编排层 | Chain / Agent | 把模块组装成工作流 | 组装成整车 |
| 应用层 | LangGraph | 复杂流程编排 | 自动驾驶系统 |

详见 [resources/LANGCHAIN_LAYERED_ARCHITECTURE.md](../resources/LANGCHAIN_LAYERED_ARCHITECTURE.md)。

## 6.3 LCEL：LangChain 的管道语法

LCEL = LangChain Expression Language。它用 `|` 把组件串起来：

```python
chain = prompt | llm | output_parser
```

数据流：

```text
输入 dict
  ↓
Prompt：填充模板，生成 messages
  ↓
LLM：调用模型，生成 AIMessage
  ↓
OutputParser：解析输出
  ↓
最终结果
```

基础示例见 [practice/15_lcel_basics.py](../practice/15_lcel_basics.py)。

## 6.4 链的组合与分支

LCEL 的强大之处在于可组合：

- 顺序串联：第一步输出作为第二步输入。
- 并行执行：多个子链同时跑。
- 条件路由：根据输入选择不同处理方式。
- 自定义转换：用 `RunnableLambda` 把普通函数接入链路。

示例见 [practice/16_lcel_composition.py](../practice/16_lcel_composition.py)。

## 6.5 Output Parser：结构化输出

Agent 工程中经常需要模型输出 JSON 或 Pydantic 对象，而不是自由文本。

常用方式：

- `StrOutputParser`：提取纯文本。
- `JsonOutputParser`：解析 JSON。
- `PydanticOutputParser`：解析并校验成 Pydantic 模型。

Pydantic Parser 的优点：

- 字段有类型。
- 字段有描述。
- 可以校验范围，如评分 1-5。
- 下游代码拿到的是对象，不是脆弱字符串。

示例见 [practice/17_output_parsers.py](../practice/17_output_parsers.py)。

## 6.6 自定义 Retriever

第 5 讲中我们学习了 RAG。真实项目里，默认检索器往往不够，需要自定义 Retriever。

常见原因：

- 需要关键词 + 语义混合检索。
- 需要权限过滤。
- 需要元数据过滤。
- 需要多知识库路由。
- 需要自定义去重和 rerank。

本章练习使用本地文档实现一个 Hybrid Retriever，避免依赖未安装的 Chroma/FAISS，同时讲清混合检索思想。

示例见 [practice/18_custom_retriever.py](../practice/18_custom_retriever.py) 和 [resources/RETRIEVER_DESIGN_NOTES.md](../resources/RETRIEVER_DESIGN_NOTES.md)。

## 6.7 Callback：监控 Agent 每一步

当链路变复杂后，不能只看最终答案。你需要知道：

- 哪条 chain 开始/结束？
- LLM 调用了几次？
- 哪一步最慢？
- 哪里报错？
- token 和成本是多少？
- retriever 是否空召回？

LangChain Callback 用于这些观测。

示例见 [practice/19_callbacks.py](../practice/19_callbacks.py) 和 [resources/CALLBACK_OBSERVABILITY.md](../resources/CALLBACK_OBSERVABILITY.md)。

## 6.8 综合案例：智能文档处理 Agent

综合案例会把本章内容串起来：

1. 输入一段文章。
2. 并行执行三个子链：
   - 文档结构化分析。
   - 行动项提取。
   - 一句话总结。
3. 用 `RunnableLambda` 汇总为报告。

示例见 [practice/20_doc_processor_agent.py](../practice/20_doc_processor_agent.py)。

## 6.9 课后作业

必做：

1. 修改 `16_lcel_composition.py`，新增一个“翻译 + 摘要 + 风格改写”的链。
2. 修改 `17_output_parsers.py`，定义自己的 Pydantic 输出结构。
3. 修改 `18_custom_retriever.py`，增加标题命中加权。
4. 修改 `19_callbacks.py`，把事件写入 JSONL 文件。

选做：

- 为文档处理 Agent 增加错误恢复。
- 为 Callback 增加成本估算。
- 把综合案例接入 L05 的 RAG 检索。
- 把文档处理结果保存为 Markdown 报告。
