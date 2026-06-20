# 第9讲 MCP 协议与工具生态：标准化的 Agent 工具接入

## 9.1 什么是 MCP

MCP 是 Model Context Protocol，中文可以叫模型上下文协议。

它要解决的问题，可以先用一个生活类比理解：没有统一接口时，不同品牌的电子设备需要不同充电线；有了 USB-C 后，一根线可以连接很多设备。Agent 开发里也有类似问题：

- 不同模型有不同的工具调用格式。
- 不同数据源有不同接入方式。
- 每接一个新工具，都要写一套适配代码。
- 工具、资源、提示模板和上下文管理缺少统一协议。

MCP 就是 Agent 工具生态里的“USB-C”。工具方实现 MCP Server，Agent 应用实现 MCP Client，双方通过统一协议完成能力发现、工具调用、资源读取、提示模板获取和必要的模型请求。

老师材料里的核心比喻很准确：MCP 不是某一个工具，而是一套标准化接入方式。

## 9.2 MCP 解决什么工程问题

第一，解决碎片化集成。

没有 MCP 时，M 个 Agent 应用接 N 个工具，常常要写 M x N 套适配。MCP 的目标是让工具方实现一次 MCP Server，应用方实现一次 MCP Client，把复杂度降成 M + N。

第二，解决上下文孤岛。

Agent 不只需要调用函数，还需要读取文件、数据库 schema、知识库片段、提示模板、运行环境等上下文。MCP 把这些能力用统一原语表达。

第三，解决生命周期和治理问题。

工具不是一次函数调用就完事。生产系统还要考虑能力协商、动态工具列表、资源订阅、权限边界、日志审计、超时、sampling 审核和跨 Server 数据流。

## 9.3 MCP 架构

MCP 是 Client-Server 架构。

```text
┌──────────────┐     MCP / JSON-RPC     ┌──────────────┐
│  MCP Client  │  <==================>  │  MCP Server  │
│  Agent 侧    │                        │  工具侧      │
│  发送请求     │                        │  提供工具     │
│  接收结果     │                        │  返回数据     │
└──────────────┘                        └──────────────┘
```

完整一些看，有三个角色：

| 角色 | 作用 | 例子 |
| --- | --- | --- |
| Host | LLM 应用本体，管理多个 Client | Claude Desktop、IDE 插件、Agent 平台 |
| MCP Client | 与某个 Server 1:1 连接，负责协议握手、消息路由、能力协商 | Agent 内的协议客户端 |
| MCP Server | 暴露工具、资源、提示模板等能力 | 文件系统、SQLite、GitHub、笔记服务 |

一个 Host 可以连接多个 MCP Server：

```text
Agent / Host
  -> MCP Client A -> filesystem server
  -> MCP Client B -> sqlite server
  -> MCP Client C -> github server
  -> MCP Client D -> note-manager server
```

MCP 还有一层 Transport，也就是 Client 和 Server 怎么通信。

| Transport | 机制 | 适用场景 |
| --- | --- | --- |
| stdio | Host 启动 Server 子进程，通过 stdin/stdout 传 JSON-RPC | 本地开发、本地工具 |
| Streamable HTTP | HTTP POST + SSE/流式响应 | 远程 Server、服务化部署、负载均衡 |

本章练习使用 stdio，因为它最适合本地课堂演示。

## 9.4 MCP 的四类原语

MCP 常见原语包括 Tools、Resources、Prompts、Sampling。

| 原语 | 调用方向 | 谁控制 | 用途 | 例子 |
| --- | --- | --- | --- | --- |
| Tools | Server 暴露，模型可调用 | 模型/Agent | 执行动作或查询 | create_note、query_database |
| Resources | Server 暴露，应用读取 | Host/Client | 注入上下文，只读资源 | notes://summary、file://README.md |
| Prompts | Server 暴露，用户或应用选择 | 用户/Host | 复用提示模板 | 代码审查模板、复盘模板 |
| Sampling | Server 请求 Client 调模型 | Client 控制 | Server 需要 LLM 推理 | Server 请求生成摘要策略 |

Tools 和 Resources 最容易混淆。

Tools 通常由模型主动决定是否调用，可以有副作用，例如创建笔记、发消息、写数据库。Resources 通常由应用层决定是否注入上下文，应尽量只读、确定、可缓存。

Sampling 是最需要安全意识的原语。它不是 Server 想调用模型就能调用模型，而是 Server 向 Client 发起请求，Client 可以拒绝、修改消息、脱敏、限制模型和参数，也可以要求人工确认。

## 9.5 实操一：开发笔记管理 MCP Server

本章第一个核心文件是 `practice/29_mcp_note_server.py`。

它用 `FastMCP` 暴露一个笔记管理 Server：

- `create_note`：创建笔记。
- `list_notes`：列出笔记。
- `search_notes`：搜索笔记。
- `update_note`：更新笔记。
- `delete_note`：删除笔记。
- `seed_notes`：重置演示数据。
- `notes://summary`：读取笔记统计摘要。
- `note_review_template`：获取笔记复盘 Prompt。

Server 的业务逻辑不直接写在 Server 文件里，而是放在 `practice/mcp_common.py`。这样做有两个好处：

- MCP Server 只负责协议暴露，业务函数可以单独测试。
- LangChain 桥接示例也能复用同一套笔记数据。

stdio 模式下有一个重要规则：不要随便往 stdout 打日志。因为 stdout 是 MCP JSON-RPC 通道，如果 Server 把普通日志写进 stdout，Host 可能无法解析协议帧。调试信息应该写 stderr 或日志文件。

运行 Server：

```bash
python practice/29_mcp_note_server.py
```

用 Inspector 调试：

```bash
mcp dev practice/29_mcp_note_server.py
```

或者：

```bash
npx @modelcontextprotocol/inspector python practice/29_mcp_note_server.py
```

## 9.6 实操二：MCP Client 调用 Server

第二个核心文件是 `practice/30_mcp_stdio_client.py`。

它展示了 MCP Client 的基本流程：

```text
配置 Server 启动参数
  -> stdio_client 启动 Server 子进程
  -> ClientSession initialize
  -> list_tools
  -> call_tool
  -> list_resources / read_resource
  -> list_prompts / get_prompt
```

对应代码中的关键对象：

- `StdioServerParameters`：告诉 Client 如何启动 Server。
- `stdio_client`：建立 stdio transport。
- `ClientSession`：封装 MCP 协议会话。
- `session.initialize()`：初始化握手和能力协商。
- `session.call_tool()`：调用工具。
- `session.read_resource()`：读取资源。
- `session.get_prompt()`：获取 Prompt。

运行：

```bash
python practice/30_mcp_stdio_client.py
```

你会看到它列出工具、资源、Prompt，并创建、搜索、读取笔记摘要。

## 9.7 实操三：将 MCP 接入 LangChain Agent

第三个核心文件是 `practice/31_langchain_mcp_bridge.py`。

老师讲义里提到，可以把 MCP 工具接入 LangChain Agent。实际工程里可以使用 adapter 库自动转换，本章为了讲清底层思路，手动做一层包装：

```text
LangChain Tool
  -> MCP Client
  -> MCP Server
  -> 业务函数
  -> 工具结果返回 Agent
```

默认运行不调用真实 LLM，只直接调用 LangChain Tool：

```bash
python practice/31_langchain_mcp_bridge.py
```

如果要演示 Agent 自动选择工具，可以运行：

```bash
python practice/31_langchain_mcp_bridge.py --use-llm
```

这个例子有一个工程提示：课堂版每次工具调用都会启动一次 stdio Server，便于阅读；生产系统应该复用连接、维护会话池，避免频繁拉起进程。

## 9.8 Sampling 如何理解

Sampling 允许 MCP Server 向 Client 请求一次 LLM 推理。它常见于 Server 自己需要“判断、摘要、规划”的场景。

流程可以理解为：

```text
Server
  -> create_message request
  -> Client 策略审核
  -> 可选用户确认
  -> Client 调用 LLM
  -> Client 返回结果给 Server
```

安全边界很重要：

- Client 可以拒绝任何 Sampling 请求。
- Client 可以修改或脱敏 messages。
- Client 控制使用哪个模型和参数。
- Client 可以限制频率、token 和上下文范围。
- 高风险请求可以要求人类确认。

本章用 `practice/33_mcp_sampling_flow.py` 模拟这个审核流程。真实项目中，可以通过 `ClientSession` 的 `sampling_callback` 实现。

## 9.9 MCP 生态

常见 MCP Server 类型包括：

| Server | 功能 | 场景 |
| --- | --- | --- |
| filesystem | 文件读写 | 让 Agent 操作本地项目文件 |
| sqlite | SQLite 查询 | 让 Agent 查询本地数据库 |
| github | GitHub 操作 | Issue、PR、代码仓库管理 |
| slack | Slack 消息 | 团队消息检索和发送 |
| browser/puppeteer | 浏览器控制 | 网页自动化和信息采集 |
| custom business server | 内部系统 | 工单、CRM、知识库、日历 |

生态丰富是一方面，生产接入更重要的是治理：Server 来源是否可信、权限是否最小化、日志是否可审计、工具描述是否安全、是否支持超时和失败恢复。

## 9.10 MCP 与 Function Calling 的区别

很多同学会把 MCP 和 Function Calling 当成一回事。它们都与“让模型调用外部能力”有关，但定位不同。

Function Calling 关注：模型如何根据用户意图选择函数并填对参数。

MCP 关注：外部工具、资源、提示模板和上下文能力如何用统一协议被发现、连接、调用和治理。

一句话：

```text
Function Calling 是模型调函数的能力。
MCP 是应用与工具通信的协议。
```

选型建议：

- 少量固定函数、快速 Demo、单应用内能力：优先 Function Calling。
- 多工具、多数据源、需要资源读取、提示模板、能力发现和平台治理：考虑 MCP。
- 成熟系统可以同时用：底层 MCP 统一接能力，上层模型仍通过 tool/function calling 决定调用什么。

## 9.11 MCP 安全与排障

安全原则：

- 最小权限。
- 用户知情。
- 可审计。
- 能力协商。
- Roots 限制访问范围。
- Sampling 默认谨慎开启。

常见攻击：

| 攻击 | 描述 | 防御 |
| --- | --- | --- |
| Tool Poisoning | 工具描述里藏提示注入 | 审查 description，UI 展示完整描述 |
| Cross-Server 泄露 | Server A 输出被传给 Server B | 数据分级、Client 侧审计 |
| Sampling 滥用 | Server 借 Sampling 窃取上下文 | 限频、脱敏、人工审核 |
| Resource Prompt Injection | 资源内容诱导模型越权 | 资源与指令隔离标记 |
| Supply Chain | 安装恶意 Server | 可信来源、代码审计、沙箱 |

如果模型“看不到工具”，优先排查：

1. Server 是否启动成功。
2. stdio 是否被 stdout 日志污染。
3. initialize 是否成功。
4. Server 是否声明 tools capability。
5. `tools/list` 是否为空。
6. tool inputSchema 是否合法。
7. Host 配置里的 command/args 是否正确。
8. 虚拟环境和依赖是否正确。
9. 权限或路径是否错误。
10. 用 MCP Inspector 独立连接 Server 验证协议层。

## 9.12 本章作业

必做：

1. 运行 `practice/30_mcp_stdio_client.py`，记录 tools/resources/prompts 输出。
2. 阅读 `practice/29_mcp_note_server.py`，解释 Tools 和 Resource 的区别。
3. 修改 `update_note` 或 `delete_note`，增加更严格的参数校验。
4. 运行 `practice/33_mcp_sampling_flow.py`，说明为什么 Client 可以拒绝 Sampling。

选做：

1. 实现一个 TODO 管理 MCP Server。
2. 给笔记 MCP Server 增加按标签筛选工具。
3. 把 notes 数据迁移到 SQLite。
4. 用 `sampling_callback` 做一个真实 Sampling 最小示例。
5. 设计一个 MCP Gateway，统一管理多个 Server 的鉴权、路由和审计。

## 9.13 本章核心结论

MCP 的价值不是“又多一种工具调用方式”，而是让工具、资源、提示模板和上下文能力有统一接入协议。

Function Calling 解决的是一次调用中“调哪个函数、传什么参数”；MCP 解决的是系统层面“外部能力如何标准化暴露、发现、调用、治理和复用”。

做单个 Demo 时，Function Calling 往往更快；做平台化 Agent 工具生态时，MCP 的标准化价值会越来越明显。
