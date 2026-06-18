# L04 章节总结：LangChain 快速上手

## 一句话总结

L04 的重点不是“框架比手写更高级”，而是理解框架帮我们封装了哪些重复流程，以及哪些关键设计仍然必须由开发者负责。

## 核心概念

| 概念 | 本章理解 |
| --- | --- |
| Model | 用 `ChatOpenAI` 封装课程 `.env` 中的模型配置 |
| Prompt | 约束 Agent 的角色、工具使用边界和回答风格 |
| Tools | 用 `@tool` 把 Python 函数暴露给模型 |
| Memory | 用 `MemorySaver` 和 `thread_id` 保存会话历史 |
| Agent | 用 `create_agent` 组合模型、工具、Prompt 和循环 |

## 本章代码地图

- `practice/langchain_common.py`：公共模型构造、基础工具和安全计算。
- `practice/07_langchain_agent.py`：基础 LangChain 工具 Agent。
- `practice/08_custom_tools.py`：自定义工具、Pydantic schema、安全文件读取。
- `practice/09_agent_with_memory.py`：多轮记忆和会话隔离。
- `practice/10_search_agent.py`：模拟搜索问答 Agent。

## 从 L03 到 L04 的迁移

| L03 手写内容 | L04 框架封装 |
| --- | --- |
| `TOOLS` JSON schema | `@tool` 自动生成工具 schema |
| `TOOL_FUNCTIONS` 注册表 | LangChain 工具列表 |
| `run_agent()` 循环 | `create_agent` |
| 手动追加 tool result | 图执行器自动处理 |
| 手动传历史 messages | `MemorySaver` + `thread_id` |

## 必须记住的工程判断

- 框架省掉样板代码，但不会替你设计好工具边界。
- 工具 docstring 很重要，因为模型会用它判断何时调用工具。
- 多参数工具建议用 Pydantic schema，参数说明越清晰，调用越稳定。
- `MemorySaver` 是课堂演示用内存记忆，生产环境需要持久化检查点。
- 搜索结果、文件内容和工具返回都可能不可靠，最终回答要保留证据意识。

## 复盘问题

- 为什么 `@tool` 的 docstring 会影响工具选择？
- `create_agent` 替我们做了哪些事情？
- 同一个 `thread_id` 和不同 `thread_id` 的行为有什么差别？
- 什么时候用 LangChain 足够，什么时候应该直接使用 LangGraph？
- 如果搜索工具返回脏数据，Agent 应该如何降低错误传播？
