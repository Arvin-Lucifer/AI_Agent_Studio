# LangChain 快速上手工程模式

## 1. 手写循环到框架组件的映射

| 手写 Function Calling | LangChain/LangGraph |
| --- | --- |
| `client.chat.completions.create` | `ChatOpenAI` |
| system/user/tool messages | 图状态里的 `messages` |
| 工具 JSON Schema | `@tool` + 函数签名 + docstring |
| 工具参数解析 | 框架基于 schema 解析 |
| 工具函数映射表 | 工具列表 `tools=[...]` |
| while 循环 | `create_agent` 图执行 |
| 对话历史 | checkpointer + `thread_id` |

## 2. 工具设计 checklist

- 工具名用动词短语，例如 `search_web`、`write_note`、`get_weather`。
- docstring 写清“什么时候用”和“什么时候不用”。
- 参数名贴近业务语言，不要用 `x`、`data`、`input` 这类含糊名字。
- 多参数工具用 Pydantic schema 写字段说明。
- 工具返回尽量结构化，至少要有错误信息和关键字段。
- 工具内部要做权限、路径、类型、长度和异常控制。

## 3. Prompt 设计 checklist

- 说明 Agent 的身份和可用能力。
- 说明什么时候应该调用工具。
- 说明工具结果不足时如何回答。
- 说明回答风格和证据要求。
- 对高风险动作加入确认或拒绝规则。

## 4. 记忆设计 checklist

- `thread_id` 应该来自真实业务会话，例如 `user_id:session_id`。
- 不同用户、不同会话必须隔离。
- 内存记忆只适合演示和短进程实验。
- 生产环境要考虑持久化、过期、清理、隐私和审计。

## 5. 搜索 Agent 常见问题

- 搜索词不准：打印工具实际收到的 query，分析模型如何改写问题。
- 搜索结果弱相关：增加 rerank、过滤和来源可信度判断。
- 搜索结果冲突：要求模型列出冲突点，不要强行合并。
- REPL 崩溃：在循环内加 `try/except`，对单次错误做恢复。
- 固定 `thread_id`：改为用户和会话相关 ID。
- 模拟数据太理想：逐步加入空结果、脏数据和错误结果测试。
