# L09 课堂笔记模板

## 一、MCP 基本理解

MCP 解决的问题：

- 

USB-C 类比：

- 

## 二、架构角色

| 角色 | 职责 | 本章例子 |
| --- | --- | --- |
| Host |  |  |
| MCP Client |  |  |
| MCP Server |  |  |
| Transport |  |  |

stdio 流程：

```text
Host 启动 Server 子进程 ->
Client 通过 stdin 发送 JSON-RPC ->
Server 通过 stdout 返回响应 ->
stderr 用于日志
```

## 三、四类原语

| 原语 | 调用方 | 是否可有副作用 | 适合场景 | 本章代码 |
| --- | --- | --- | --- | --- |
| Tools |  |  |  |  |
| Resources |  |  |  |  |
| Prompts |  |  |  |  |
| Sampling |  |  |  |  |

Tools 和 Resources 的区别：

- 

## 四、调用链路记录

运行命令：

```bash

```

发现的工具：

- 

发现的资源：

- 

调用结果：

```text

```

## 五、MCP 与 Function Calling

| 维度 | Function Calling | MCP |
| --- | --- | --- |
| 定位 |  |  |
| 关注点 |  |  |
| 适合场景 |  |  |
| 风险 |  |  |

我的选型规则：

- 

## 六、安全与排障

高风险配置：

- 

排障顺序：

1. 
2. 
3. 

Sampling 审核策略：

- 

## 七、面试题复盘

- MCP 解决的核心问题是什么？
- Tools 和 Resources 如何选择？
- 模型看不到工具时怎么排查？
- MCP 在大规模 Agent 平台里会遇到哪些瓶颈？
