# L09 课后小测

## 题目

1. MCP 主要解决什么问题？
2. Host、MCP Client、MCP Server 分别是什么？
3. stdio transport 的基本通信流程是什么？
4. MCP 的四类原语分别是什么？
5. Tools 和 Resources 的关键区别是什么？
6. Sampling 为什么需要 Client 审核？
7. MCP 和 Function Calling 的本质区别是什么？
8. 模型看不到 MCP 工具时，列出 5 个可能原因。
9. 为什么 MCP Server 的 stdout 不能随便打印日志？
10. 大规模 Agent 集群接入 MCP 可能遇到哪些瓶颈？

## 参考答案

1. MCP 解决 LLM 应用与外部工具、数据源、提示模板之间接入碎片化的问题，用统一协议做能力发现、上下文读取和工具调用。
2. Host 是 LLM 应用本体；Client 是 Host 内负责连接某个 Server 的协议客户端；Server 是工具或数据源侧，暴露 Tools、Resources、Prompts 等能力。
3. Host 启动 Server 子进程，Client 通过 stdin 发送 JSON-RPC，Server 通过 stdout 返回响应，stderr 用于日志。
4. Tools、Resources、Prompts、Sampling。
5. Tools 通常由模型主动调用，可有副作用；Resources 通常由 Host/Client 控制读取，应是只读上下文。
6. 因为 Sampling 是 Server 请求 Client 调用 LLM，可能泄露上下文或产生额外成本，Client 必须能拒绝、脱敏、限频和审核。
7. Function Calling 是模型输出结构化函数参数的能力；MCP 是应用与工具/资源通信的开放协议。
8. Server 启动失败、stdout 污染、initialize 失败、tools capability 未声明、tools/list 为空、schema 非法、路径配置错误、虚拟环境缺依赖、权限限制过严。
9. 因为 stdout 是 stdio transport 的 JSON-RPC 通道，普通日志会污染协议消息，导致 Host 解析失败。
10. 连接数爆炸、工具描述占满上下文、Sampling 风暴、跨 Server 数据泄露、跨 Server 事务一致性、审计和权限治理复杂。
