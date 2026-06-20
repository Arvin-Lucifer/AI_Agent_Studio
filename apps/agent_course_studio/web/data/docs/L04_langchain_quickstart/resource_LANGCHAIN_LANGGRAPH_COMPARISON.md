# LangChain 与 LangGraph 对比

## 一句话区别

LangChain 是“组件库 + 链式框架”，适合快速搭建简单 LLM 应用；LangGraph 是“图编排引擎”，适合有状态、可循环、多分支、可持久化的复杂 Agent 工作流。

## 核心定位

| 框架 | 定位 | 典型能力 |
| --- | --- | --- |
| LangChain | LLM 应用组件库 | 模型封装、Prompt、工具、RAG、链式组合 |
| LangGraph | Agent 图编排引擎 | State、节点、边、循环、条件路由、检查点、人机协作 |

## 关键区别

| 维度 | LangChain | LangGraph |
| --- | --- | --- |
| 核心抽象 | Chain、组件 | Graph、State、Node、Edge |
| 流程结构 | 更适合线性流程 | 支持循环、分支、并行 |
| 状态管理 | 依赖 Memory 或手动传参 | 原生共享 State 和 Checkpointer |
| 人机介入 | 支持有限 | 更适合暂停、审批、编辑状态后继续 |
| 复杂 Agent | 快速原型方便 | 生产级编排更强 |
| 学习曲线 | 较低 | 中等，需要理解图和状态 |

## 怎么选

| 场景 | 建议 |
| --- | --- |
| 单轮问答 | LangChain |
| 固定流程：翻译 -> 摘要 -> 格式化 | LangChain |
| 简单 RAG 问答 | LangChain 或 LangGraph 都可以 |
| ReAct Agent 原型 | `create_agent` |
| 需要条件路由 | LangGraph |
| 需要循环迭代 | LangGraph |
| 需要断点恢复 | LangGraph |
| 需要人工审批 | LangGraph |
| 多 Agent 协作 | LangGraph |

## 面试表达模板

可以这样回答：

LangChain 解决的是 LLM 应用开发中的组件复用问题，比如模型封装、Prompt、工具、RAG 和简单链式流程。LangGraph 解决的是复杂 Agent 的流程控制和状态管理问题，比如循环、分支、持久化检查点、人机介入和多 Agent 协作。实际项目里两者通常配合使用：LangChain 提供组件，LangGraph 负责把组件编排成可靠的有状态工作流。
