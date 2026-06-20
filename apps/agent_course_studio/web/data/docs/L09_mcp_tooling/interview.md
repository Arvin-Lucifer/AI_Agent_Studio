# L09 面试题库：MCP 协议与工具生态

说明：本题库基于老师提供的 MCP 讲义和 15 道 MCP 面试题整理，并补充了课程代码中的实战回答角度。补充内容用于帮助面试表达更完整，不替代原讲义观点。

## 一、基础级：概念理解

### 1. 什么是 MCP？它解决的核心问题是什么？

MCP 是 Model Context Protocol，用于标准化 LLM 应用与外部工具、数据源和上下文能力之间的连接方式。

它解决三个核心问题：

- 碎片化集成：每个应用接每个工具都写适配，会形成 M x N 问题；MCP 希望降为 M + N。
- 上下文孤岛：文件、数据库、API、知识库缺少统一上下文供给方式。
- 协议不统一：Function Calling、插件、API 直调各自为政，MCP 提供统一通信和生命周期管理。

类比：MCP 之于 AI 应用，类似 USB-C 之于外设。

### 2. MCP 的核心架构包含哪些角色？

核心角色：

- Host：LLM 应用本体，例如桌面应用、IDE、Agent 平台。
- MCP Client：Host 内部的协议客户端，与某个 Server 保持 1:1 连接。
- MCP Server：工具或数据源侧，暴露 Tools、Resources、Prompts 等能力。
- Transport：通信方式，例如 stdio 或 Streamable HTTP。

关键设计：一个 Host 可以持有多个 Client，每个 Client 连接一个 Server，从而实现隔离、并行和治理。

### 3. MCP 协议定义了哪些常见原语？用途是什么？

| 原语 | 方向 | 用途 | 示例 |
| --- | --- | --- | --- |
| Tools | Server 暴露，模型调用 | 可执行函数或动作 | `query_database`, `create_note` |
| Resources | Server 暴露，应用读取 | 只读上下文 | 文件内容、数据库 schema |
| Prompts | Server 暴露，用户/应用选择 | 预定义提示模板 | 代码审查模板 |
| Sampling | Server 请求 Client | Server 需要 LLM 推理 | 生成摘要策略 |

核心区分：Tools 由模型自主决定调用；Resources 由应用层控制是否注入上下文。

### 4. MCP 的传输层支持哪些方式？

常见方式：

- stdio：Host 启动本地 Server 子进程，通过 stdin/stdout 传 JSON-RPC，适合本地开发和本地工具。
- Streamable HTTP：通过 HTTP POST 和 SSE/流式响应通信，适合远程 Server、负载均衡和服务化部署。

stdio 模式下，stdout 是协议通道，日志应写 stderr。

## 二、中等级：设计理解与实战

### 5. MCP 的能力协商机制如何工作？为什么重要？

能力协商发生在 `initialize` 阶段。Client 和 Server 声明自己支持的能力，例如 tools、resources、prompts、sampling、roots 等。

重要性：

- 向后兼容：未声明能力不可用，旧版本不会被新能力破坏。
- 按需启用：不需要的能力不打开。
- 安全边界：Client 可以拒绝 Server 的 Sampling。
- 动态感知：listChanged 让 Client 知道工具或资源列表发生变化。

### 6. Tools 和 Resources 都能提供数据，实际设计中如何选择？

| 维度 | Tools | Resources |
| --- | --- | --- |
| 调用者 | 模型自主决定 | 应用或用户控制 |
| 副作用 | 可以有 | 应只读 |
| 成本 | 可能较高 | 通常较低 |
| 确定性 | 可能受时间和外部系统影响 | URI 到内容应稳定 |
| 例子 | 执行 SQL、创建工单 | 数据库 schema、文件内容 |

常见错误：把稳定只读上下文设计成 Tool，导致模型频繁、不必要地调用。更好的做法是设计为 Resource，由 Host 在合适时机注入。

### 7. MCP Sampling 是什么？

Sampling 是 MCP 中 Server 向 Client 请求 LLM 推理的机制。它让 Server 在需要摘要、判断、规划时，可以请求 Client 帮它调用模型。

安全机制：

- Client 可以拒绝。
- Client 可以修改或脱敏 messages。
- Client 控制模型和参数。
- Client 可以要求人工审核。
- Client 可以限制频率和 token。

回答时要强调：Sampling 不是 Server 无条件调用模型，控制权在 Client。

### 8. Roots 的作用是什么？

Roots 是 Client 暴露给 Server 的根路径或根 URL，告诉 Server 可以访问哪些范围。

作用：

- 安全边界：限制 Server 访问范围。
- 上下文锚定：Server 能正确解析相对路径。
- 多工作区支持：Client 可以暴露多个 roots。
- 动态更新：项目切换时通知 Server。

示例：只暴露 `file:///project/myapp`，而不是 `file:///`。

## 三、高级级：架构设计与排障

### 9. 用户反馈 MCP Server 启动后模型看不到工具，如何排查？

按优先级排查：

1. Server 是否启动成功，是否立即崩溃。
2. stdio stdout 是否被普通日志污染。
3. initialize 是否成功。
4. Server 是否声明 tools capability。
5. `tools/list` 是否返回空。
6. 装饰器是否注册，模块是否真正导入。
7. inputSchema 是否符合 JSON Schema。
8. Host 配置中的 command/args 是否正确。
9. 虚拟环境依赖和权限是否正确。
10. 用 MCP Inspector 独立连接 Server 验证协议层。

### 10. MCP 的安全模型如何设计？

核心原则：最小权限、用户知情、可审计。

安全层次：

- 传输层：stdio 本地隔离；HTTP 使用 HTTPS/OAuth。
- 能力边界：初始化能力协商，未声明能力不可用。
- Roots 限制：Server 只能访问授权根目录。
- 用户控制：高风险 Tools 和 Sampling 可确认。
- 审计日志：记录工具调用、资源读取、参数、结果和错误。

常见攻击：

- Tool Poisoning：工具描述里藏提示注入。
- Cross-Server 数据泄露：一个 Server 的结果被传给另一个 Server。
- Sampling 滥用：Server 借模型请求窃取上下文。
- Resource Prompt Injection：资源内容诱导模型越权。
- Supply Chain：安装恶意 MCP Server。

### 11. 如何设计支持多 Agent 协作的 MCP 架构？

可以使用 MCP Gateway 模式：

- Context Store：跨 Agent 共享上下文，可以通过 Resource 暴露。
- Tool Registry：统一工具注册和发现。
- Session Manager：管理多 Agent 会话和上下文交接。
- Auth/Audit：统一鉴权和审计。
- Proxy/Connection Pool：复用连接，避免 N x M 连接爆炸。

关键设计：

- 每个 Agent 使用独立 Client 身份。
- 工具命名空间避免冲突，例如 `agent_id.tool_name` 或 `server.tool_name`。
- 上下文使用摘要和引用，不共享所有原始内容。
- Sampling 设置深度、频率和超时限制。

### 12. MCP 与 OpenAI Function Calling / Plugin 有什么本质区别？

| 维度 | MCP | Function Calling | Plugin |
| --- | --- | --- | --- |
| 定位 | 开放协议 | 模型能力 | 平台生态能力 |
| 关注点 | 工具/资源如何接入和治理 | 函数参数如何生成 | REST API 接入平台 |
| 通信 | Client 与 Server 双向协议 | 模型输出函数调用参数 | 平台调用外部 API |
| 能力 | Tools、Resources、Prompts、Sampling | Functions | REST API |
| 适合 | 多工具、多数据源、平台化 Agent | 少量固定函数 | 平台特定扩展 |

一句话：Function Calling 是模型调函数的能力，MCP 是应用与工具通信的协议。

### 13. 如何实现 MCP Server 热更新？

思路：

- 工具注册表使用内存字典或配置中心。
- 监听配置文件或远程注册中心变化。
- 变更后发送 `tools/list_changed` 通知。
- Client 收到通知后重新调用 `tools/list`。

注意：

- 正在执行的工具调用不要中断。
- inputSchema 变更需要兼容旧调用。
- 工具描述中建议包含版本号。
- 高风险工具新增需要审批。

### 14. MCP 消息 ID 有什么作用？如何处理乱序响应和超时？

MCP 基于 JSON-RPC。请求带唯一 `id`，响应用同一个 `id` 匹配。

作用：

- 请求和响应关联。
- 区分请求和通知，无 `id` 的消息通常是通知。
- 支持并发请求和乱序响应。

处理方式：

- Client 维护 `pending_requests` 字典，`id -> Future`。
- 响应到达时按 `id` resolve。
- 查询类超时可重试。
- 有副作用工具超时后不能盲目重试。
- 不同请求类型设置不同超时。

## 四、专家级：前沿与权衡

### 15. MCP 在大规模 Agent 集群中可能遇到哪些瓶颈？如何解决？

瓶颈一：连接数爆炸。

- 问题：N 个 Agent x M 个 Server 形成 N x M 连接。
- 方案：MCP Proxy、连接池、多路复用。

瓶颈二：上下文窗口溢出。

- 问题：工具描述和资源内容太多。
- 方案：分层工具加载，先加载摘要，按需加载完整 schema。

瓶颈三：Sampling 风暴。

- 问题：多个 Server 同时请求模型。
- 方案：令牌桶限流、优先级队列、预算控制、人审策略。

瓶颈四：跨 Server 事务一致性。

- 问题：一个任务操作多个 Server，失败后难以原子回滚。
- 方案：Saga + 补偿操作，但要认识到 Saga 只保证最终一致性，不适合金融核心、秒杀库存、医疗航空等强一致场景。

瓶颈五：安全审计复杂。

- 问题：跨 Server 数据流很难追踪。
- 方案：统一 trace_id、数据分级、工具调用审计、输出脱敏。

### 16. 当 MCP Server 返回的 Resource 超过模型上下文窗口，如何设计？

策略组合：

- 分页读取：cursor、offset、limit。
- 摘要 + 详情双层：默认返回 metadata 和摘要，按需调用 detail。
- 服务端检索：提供 search tool，只回传 top-k 片段。
- 字段投影：只返回模型需要的字段。
- 流式返回：远程传输下用 SSE 增量推送。
- 缓存：热数据做 LRU 缓存。

反模式：一次性把 100MB 日志塞进 Resource content。

## 五、开放设计题

### 17. 设计一个企业内部 MCP 工具平台，你会怎么做？

可以从以下方面回答：

- Server Registry：登记所有 MCP Server、owner、版本、权限等级。
- Auth Gateway：统一鉴权，按用户、部门、租户授权。
- Tool Review：审查 tool description、inputSchema、副作用和风险等级。
- Context Policy：控制 Resources 注入范围和敏感数据脱敏。
- Sampling Policy：限制频率、token、模型、审核方式。
- Observability：统一 trace、metrics、audit logs。
- Evaluation：统计工具选择准确率、调用成功率、越权拦截率和延迟。

### 18. 如何判断项目该不该上 MCP？

适合 MCP：

- 工具数量持续增长。
- 多个 Agent 或多个应用要复用同一能力。
- 不只需要函数调用，还需要资源读取、提示模板和上下文治理。
- 有权限、审计、安全和平台化诉求。

暂时不需要 MCP：

- 只有少量固定函数。
- 只做快速 Demo。
- 工具都在应用进程内。
- 没有跨系统复用需求。

实践建议：先用 Function Calling 验证需求闭环，工具生态复杂后再升级为 MCP Server。
