# L04 面试题速查：LangChain 快速上手

本章面试重点不是“背 API”，而是能解释框架解决了什么重复劳动，以及 LangChain 和 LangGraph 的边界。

## 来源说明

- 题目来源：主要来自老师第 4 讲讲义中的“4.9 LangChain 是什么”和“4.10 LangChain 和 LangGraph 的区别”。
- 参考来源：LangChain/LangGraph 对比部分参考本章 [LANGCHAIN_LANGGRAPH_COMPARISON.md](../resources/LANGCHAIN_LANGGRAPH_COMPARISON.md)。
- 整理方式：前 3 题是对老师讲义内容的归纳整理；后 3 题结合本章代码示例和框架使用重点补充成面试表达。
- 补充边界：`@tool`、Pydantic schema、MemorySaver、thread_id 等问题来自本章实践代码和讲义主题，不是老师原文逐字题目。

## 1. LangChain 是什么？

参考回答：

```text
LangChain 是一个用于构建 LLM 应用的开发框架，帮助开发者把模型、Prompt、工具、检索、记忆和链式流程组合起来。它让我们不用每次从零手写模型调用、工具封装、输出解析和流程编排。
```

它主要解决：

- LLM 调用封装。
- Prompt 模板管理。
- 工具封装。
- RAG 检索增强。
- 简单链式任务编排。
- 对话记忆。
- 回调、调试和可观测性。

## 2. 为什么第 3 讲手写 Function Calling 后还需要 LangChain？

手写循环能帮助理解底层机制，但真实项目会不断重复：

- 组装 Prompt。
- 维护工具 schema。
- 执行工具调用循环。
- 管理对话状态。
- 处理模型和工具输入输出。
- 加日志和异常处理。

LangChain 的价值是把这些常见部件抽象成可复用组件，让开发者把精力放到业务工具、流程边界和可靠性上。

## 3. LangChain 和 LangGraph 的区别？

一句话：

```text
LangChain 更像组件库和链式框架，适合快速搭建模型、工具、检索和简单 Agent；LangGraph 是图编排引擎，适合有状态、循环、多分支、可恢复、可人工介入的复杂 Agent 工作流。
```

选型：

| 场景 | 更适合 |
| --- | --- |
| 单轮问答 | LangChain |
| 简单工具 Agent | LangChain |
| 简单 RAG | LangChain 或 LangGraph |
| 多轮循环任务 | LangGraph |
| 多 Agent 协作 | LangGraph |
| 需要 checkpoint / human-in-the-loop | LangGraph |

## 4. `@tool` 和 Pydantic 参数 schema 有什么价值？

`@tool` 让普通 Python 函数变成模型可理解、框架可调度的工具。Pydantic schema 让参数类型、必填字段、描述和校验规则更明确，减少模型乱传参，也方便代码侧做错误提示和恢复。

## 5. MemorySaver 和 thread_id 解决什么问题？

MemorySaver 保存对话状态，`thread_id` 用来区分不同会话。

如果没有 `thread_id`：

- 不同用户的上下文可能混在一起。
- 同一个用户的多条任务线无法隔离。
- 调试时很难复现状态。

## 6. 使用框架是不是就不需要理解 Function Calling？

不是。

框架只是隐藏样板代码，不会替你决定：

- 工具边界是否合理。
- 参数 schema 是否清晰。
- 高危工具是否需要确认。
- 错误后如何恢复。
- 什么时候应该停止循环。

面试中可以这样收束：

```text
LangChain 提升开发效率，但工程可靠性仍取决于工具设计、状态管理、权限控制、错误恢复和评估体系。
```
