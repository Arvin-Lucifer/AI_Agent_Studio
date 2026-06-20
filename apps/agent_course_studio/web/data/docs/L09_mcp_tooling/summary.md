# L09 章节总结

## 一句话总结

MCP 是 Agent 工具生态的标准化接入协议：它让 Host/Client 用统一方式连接 MCP Server，发现 Tools、读取 Resources、复用 Prompts，并在受控条件下处理 Sampling。

## 架构速查

```text
Host / Agent App
  -> MCP Client A -> MCP Server A
  -> MCP Client B -> MCP Server B
  -> MCP Client C -> MCP Server C
```

| 角色 | 作用 |
| --- | --- |
| Host | LLM 应用本体，管理多个 MCP Client |
| Client | 与单个 Server 建立连接，做握手、能力协商和消息路由 |
| Server | 暴露工具、资源、提示模板等能力 |
| Transport | stdio 或 Streamable HTTP 等通信方式 |

## 四类原语

| 原语 | 谁用 | 作用 | 本章代码 |
| --- | --- | --- | --- |
| Tools | 模型/Agent 主动调用 | 执行动作或查询 | `create_note`, `search_notes` |
| Resources | Host/Client 控制读取 | 提供只读上下文 | `notes://summary` |
| Prompts | 用户/Host 选择 | 复用提示模板 | `note_review_template` |
| Sampling | Server 请求，Client 审核 | Server 需要 LLM 推理 | `33_mcp_sampling_flow.py` |

## 代码地图

- `practice/mcp_common.py`：笔记业务逻辑和 JSON 数据存储。
- `practice/29_mcp_note_server.py`：FastMCP Server，暴露 Tools、Resource、Prompt。
- `practice/30_mcp_stdio_client.py`：stdio Client，演示 initialize、list、call、read、get。
- `practice/31_langchain_mcp_bridge.py`：LangChain Tool -> MCP Client -> MCP Server。
- `practice/32_mcp_safety_checklist.py`：MCP Server 接入安全检查。
- `practice/33_mcp_sampling_flow.py`：Sampling 审核和脱敏流程模拟。

## MCP 与 Function Calling

| 维度 | Function Calling | MCP |
| --- | --- | --- |
| 定位 | 模型输出结构化函数参数 | 应用与工具/资源通信的协议 |
| 关注点 | 调哪个函数、参数是否正确 | 能力如何暴露、发现、调用和治理 |
| 能力范围 | 函数调用为主 | Tools、Resources、Prompts、Sampling |
| 适合规模 | 小到中等、单应用集成 | 中大型、多系统工具生态 |
| 常见用法 | 快速 Demo、固定函数 | 平台化 Agent、工具复用、上下文接入 |

一句话：Function Calling 是“调用动作”，MCP 是“能力接口标准”。

## 排障优先级

如果 Host 或模型看不到 MCP 工具：

1. Server 是否能独立启动。
2. stdio stdout 是否被日志污染。
3. `initialize` 是否成功。
4. Server 是否声明 tools capability。
5. `tools/list` 是否返回工具。
6. inputSchema 是否合法。
7. command/args 路径是否正确。
8. 虚拟环境是否包含依赖。
9. 权限和 roots 是否限制过严。
10. 用 MCP Inspector 验证协议层。

## 安全原则

- 最小权限：roots、工具白名单、敏感数据过滤。
- 用户知情：高风险工具调用和 Sampling 可审核。
- 可审计：记录 Server、tool、arguments、resource、result 和错误。
- 隔离：不同 Server、不同租户、不同敏感等级隔离。
- 不信任工具描述：审查 description 里的 prompt injection。

## 复盘问题

1. 为什么 MCP 可以缓解 M x N 工具适配问题？
2. Tools 和 Resources 的边界是什么？
3. Sampling 为什么必须由 Client 控制？
4. stdio transport 为什么不能随便向 stdout 打日志？
5. MCP 和 Function Calling 在成熟 Agent 平台里如何配合？
