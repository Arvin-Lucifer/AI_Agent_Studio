# MCP 安全与排障清单

## 1. 安全原则

MCP 安全模型可以压缩成三句话：

- 最小权限。
- 用户知情。
- 全程可审计。

## 2. 接入前安全检查

| 检查项 | 问题 |
| --- | --- |
| Server 来源 | 是否来自可信仓库或内部团队？ |
| Tool 描述 | 是否包含 prompt injection 或隐藏指令？ |
| Roots | 是否只暴露必要目录？ |
| Transport | 远程 Server 是否使用 HTTPS 和鉴权？ |
| Sampling | 是否默认关闭或受策略控制？ |
| 副作用工具 | 是否需要确认、幂等或补偿？ |
| 审计日志 | 是否记录工具、参数、用户、结果和错误？ |

## 3. 常见攻击与防御

| 攻击 | 描述 | 防御 |
| --- | --- | --- |
| Tool Poisoning | 工具描述里藏“忽略系统提示”等指令 | 审查 description，UI 展示完整描述 |
| Cross-Server 泄露 | Server A 输出被传给 Server B | 数据分级、隔离、审计 |
| Sampling 滥用 | Server 请求模型窃取上下文 | 限频、脱敏、人工审核 |
| Resource Prompt Injection | 资源内容诱导模型越权 | 资源内容与指令隔离标记 |
| Supply Chain | 安装恶意 Server 包 | 可信来源、锁版本、代码审计 |

## 4. 模型看不到工具的排障顺序

1. Server 是否能直接启动。
2. 依赖是否安装在正确环境。
3. Host 配置的 command/args 是否正确。
4. stdio stdout 是否被普通日志污染。
5. `initialize` 是否成功。
6. Server 是否声明 tools capability。
7. `tools/list` 是否返回空。
8. 装饰器是否执行，模块是否导入。
9. inputSchema 是否合法。
10. 权限、roots 或 Server 策略是否拦截。
11. 用 MCP Inspector 独立验证。

## 5. stdio 日志规则

stdio 模式里：

```text
stdin  -> Client 发给 Server 的 JSON-RPC
stdout -> Server 发给 Client 的 JSON-RPC
stderr -> 日志
```

因此 Server 不应该把普通日志、print 调试信息写到 stdout。

## 6. 超时与重试

| 类型 | 是否可重试 | 建议 |
| --- | --- | --- |
| 只读查询 | 可以谨慎重试 | 设置短超时和退避 |
| 有副作用工具 | 不要盲目重试 | 使用幂等键或人工确认 |
| Resource 读取 | 可重试 | 大资源分页 |
| Sampling | 谨慎重试 | 控制预算和频率 |

## 7. 课堂工具

运行安全检查示例：

```bash
python practice/32_mcp_safety_checklist.py
```

运行 Sampling 审核示例：

```bash
python practice/33_mcp_sampling_flow.py
```
