# L06 面试题速查：LangChain 深入

本章面试重点是 LCEL、结构化输出、自定义 Retriever 和 Callback 可观测性。不要只说“会用 LangChain”，要能讲清输入输出如何流动、复杂链路如何调试。

## 来源说明

- 题目来源：老师第 6 讲提供的是 LangChain 深入讲义内容，包括分层架构、LCEL、Output Parser、自定义 Retriever、Callback 和智能文档处理案例；并没有单独提供一份“面试题清单”。
- 整理方式：本文件是基于老师第 6 讲主题和本章配套代码整理出的面试速查，不是老师逐字面试题。
- 补充边界：生产级 Callback、Retriever 权限过滤、run_id 隔离、日志持久化等属于工程化补充，用于帮助学生把课堂概念转成面试表达。

## 1. LCEL 是什么？

LCEL 是 LangChain Expression Language，用统一的 `Runnable` 协议把 Prompt、模型、Parser、Retriever、普通函数等组件组合起来。

典型管道：

```python
chain = prompt | llm | output_parser
```

回答重点：

- `prompt` 把 dict 输入变成 messages。
- `llm` 把 messages 变成 AIMessage。
- `output_parser` 把 AIMessage 变成字符串、JSON 或 Pydantic 对象。

## 2. LCEL 相比手写函数调用有什么优势？

- 组件输入输出协议统一。
- 支持串联、并行、分支和流式输出。
- 容易接入 callback、retry、batch。
- 便于把链拆成可测试的小模块。
- 代码更接近“数据流图”。

## 3. `RunnableParallel` 适合什么场景？

适合多个子任务可以同时执行、彼此不依赖的场景，例如：

- 同时生成中文摘要和英文摘要。
- 同时做文档分类、行动项抽取和 TLDR。
- 同时检索多个知识源。

注意点：

- 并行会增加瞬时 API 并发和成本。
- 子链失败要有降级策略。
- 输出结构要稳定，方便后续汇总。

## 4. Output Parser 有什么价值？

LLM 默认输出自由文本，程序很难稳定消费。Output Parser 的作用是把模型输出变成可编程对象。

常见选择：

- `StrOutputParser`：只要文本。
- `JsonOutputParser`：需要轻量 JSON。
- `PydanticOutputParser`：需要字段类型、校验和业务对象。

面试表达：

```text
Parser 不是格式装饰，而是把自然语言结果接入工程系统的边界层。
```

## 5. 自定义 Retriever 要考虑什么？

核心不是“写一个搜索函数”，而是保证召回结果可解释、可去重、可排序、可追溯。

要点：

- 支持稳定 metadata：source、title、id、score。
- 不用 `content[:100]` 这类脆弱去重 key。
- 向量检索和关键词检索可以融合。
- 权限过滤要发生在上下文注入前。
- 结果要保留来源，方便引用和审计。

## 6. Callback 在生产里能做什么？

Callback 是复杂 Agent 的可观测性入口。

用途：

- 记录 chain / LLM / tool / retriever 的开始和结束。
- 统计 token、成本和耗时。
- 定位慢步骤和报错步骤。
- 记录检索命中、工具入参、模型输出摘要。
- 对异常做告警。
- 支持审计、脱敏和安全检查。

## 7. Callback 示例和生产系统差在哪里？

课程示例主要展示事件流。生产级还需要：

- run_id 级状态隔离。
- 日志持久化。
- 成本换算。
- OpenTelemetry、LangSmith 或 Prometheus 接入。
- PII 脱敏。
- 告警、熔断和重试策略。

## 8. 智能文档处理 Agent 如何设计？

可按并行子链设计：

1. 分类与摘要链：输出标题、类别、摘要、关键词。
2. 行动项链：抽取任务、负责人、优先级。
3. TLDR 链：给出一句话结论。
4. 报告链：把结构化结果汇总成最终报告。

高质量设计要强调：

- 子链输出结构化。
- 并行提升速度。
- 最终汇总有统一 schema。
- Callback 记录每个阶段耗时和失败点。
