# LangChain 分层架构

## 1. 分层图

```text
应用层
  典型组件：LangGraph
  作用：复杂流程编排、状态图、多分支、多 Agent
        ↑ 基于下层能力构建

编排层
  典型组件：Chain、Agent
  作用：链式调用、自主决策、任务流程
        ↑ 基于下层能力构建

能力层
  典型组件：Retriever、Memory、Tool、Output Parser
  作用：检索、记忆、工具调用、结构化输出
        ↑ 基于下层能力构建

模型层
  典型组件：ChatModel、LLM、Embedding
  作用：封装不同厂商的模型 API
        ↑ 基于下层能力构建

基础层
  典型组件：langchain-core、Runnable、LCEL
  作用：统一调用协议，像 USB 接口标准一样连接各种组件
```

## 2. 各层类比

| 层级 | 核心组件 | 作用 | 类比 |
| --- | --- | --- | --- |
| 基础层 | Runnable / LCEL | 统一调用协议 | USB 接口标准 |
| 模型层 | ChatModel / LLM / Embedding | 封装模型 API | 不同品牌发动机 |
| 能力层 | Tool / Retriever / Memory / Output Parser | 提供功能模块 | 各种零部件 |
| 编排层 | Chain / Agent | 组装工作流 | 组装成整车 |
| 应用层 | LangGraph | 复杂流程编排 | 自动驾驶系统 |

## 3. 学习建议

- 先掌握 LCEL，因为它是组件之间的连接方式。
- 再掌握 Output Parser，因为结构化输出是 Agent 工程化的基础。
- 然后理解 Retriever，因为 RAG 和 Agent 工具常常依赖检索。
- 最后学习 Callback，因为复杂链路必须能观察和调试。
