# MCP 与 Function Calling 对比

## 1. 一句话区别

```text
Function Calling 关注模型如何调用函数。
MCP 关注外部能力如何被标准化接入、发现、调用和治理。
```

Function Calling 是模型能力；MCP 是应用与工具之间的协议。

## 2. 调用链路

Function Calling：

```text
应用注册函数 schema
  -> 模型选择函数并生成参数
  -> 应用执行函数
  -> 工具结果回传模型
```

MCP：

```text
Host/Client 连接 Server
  -> initialize 能力协商
  -> list_tools/list_resources/list_prompts
  -> call_tool/read_resource/get_prompt
  -> Server 返回标准化结果
```

## 3. 对比表

| 维度 | Function Calling | MCP |
| --- | --- | --- |
| 核心目标 | 让模型输出结构化函数参数 | 用统一协议接入工具和上下文能力 |
| 关注重点 | 调哪个函数、参数是否正确 | 能力如何暴露、发现、调用和治理 |
| 主要角色 | 模型 + 宿主应用函数 | Host + Client + Server |
| 能力范围 | 函数调用为主 | Tools、Resources、Prompts、Sampling |
| 生命周期 | 通常以单次调用为主 | 支持连接、能力协商、通知、会话 |
| 适用规模 | 小到中等、单应用 | 中大型、多工具、多系统 |
| 常见风险 | 参数错误、函数误选 | 协议治理、安全、跨 Server 数据流 |

## 4. 什么时候选 Function Calling

- 只有少量固定函数。
- 工具都在你的应用进程内。
- 主要关注参数生成准确率。
- 需要快速做 Demo。
- 没有跨应用复用诉求。

## 5. 什么时候选 MCP

- 工具和数据源会持续增加。
- 多个 Agent 或多个应用要复用工具。
- 需要 Resources、Prompts、Sampling，而不仅是函数。
- 需要统一鉴权、审计、注册、热更新和治理。
- 正在搭建平台化 Agent 工具生态。

## 6. 实战建议

成熟系统不必二选一。

常见组合：

```text
底层：MCP Server 标准化接入工具和上下文
中层：MCP Client/Adapter 转成应用可用工具
上层：模型通过 Function Calling / Tool Calling 决定调哪个工具
```

也就是说，MCP 可以是能力接入层，Function Calling 可以是模型决策层。
