# MCP 架构模式

## 1. 本地 stdio 模式

```text
Host
  -> spawn subprocess
  -> MCP Server over stdio
```

适合：

- 本地文件系统。
- 本地 SQLite。
- IDE 插件。
- 个人工具。

优点：

- 开发简单。
- 权限容易限制在本地进程。
- 适合快速调试。

风险：

- stdout 日志污染协议。
- 进程频繁启动有开销。
- 不适合大规模远程共享。

## 2. 远程 Streamable HTTP 模式

```text
Host/Client
  -> HTTPS
  -> Remote MCP Server
```

适合：

- 企业内部共享工具。
- 多用户服务。
- 需要负载均衡和独立部署的能力。

关键要求：

- HTTPS。
- OAuth 或内部鉴权。
- 会话管理。
- 速率限制。
- 审计日志。

## 3. MCP Gateway 模式

```text
Agents
  -> MCP Gateway
      -> Auth
      -> Tool Registry
      -> Context Store
      -> Audit Log
      -> Server Pool
```

适合：

- 多 Agent 协作。
- 多团队共享工具。
- 企业内部工具平台。
- 统一安全治理。

核心组件：

- Tool Registry：登记工具、版本、owner、风险等级。
- Auth：按用户、租户、部门、角色授权。
- Context Store：共享上下文和资源摘要。
- Session Manager：管理多 Agent 会话。
- Proxy/Pool：复用连接，降低连接数。
- Audit：记录调用链路。

## 4. 分层工具加载

大规模工具生态会让工具描述占满上下文。可以分两层加载：

```text
第一层：工具目录摘要
第二层：按需加载工具完整 schema
```

适合：

- 工具数量超过几十个。
- 工具描述很长。
- 多业务域共用一个 Agent 平台。

## 5. 跨 Server 事务

当一个任务需要操作多个 Server，例如：

```text
创建订单 -> 扣库存 -> 付款 -> 发通知
```

MCP 本身不保证跨 Server 原子事务。可以使用 Saga 模式：

- 每一步都是本地事务。
- 每一步有补偿操作。
- 失败时逆序补偿。

但要注意：

- Saga 只保证最终一致性。
- 补偿逻辑复杂。
- 回滚也可能失败。
- 不适合金融核心交易、秒杀库存、医疗航空等强一致场景。
