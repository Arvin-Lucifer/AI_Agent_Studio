# Callback 机制与可观测性

Callback 的作用是观察 LangChain 运行过程：链什么时候开始、模型什么时候调用、工具是否被执行、检索是否命中、哪里报错、耗时和 token 如何。

## 常见用途

- 运行观测：记录 chain、llm、tool、retriever 的开始、结束、耗时、输入输出摘要。
- Token 与成本统计：统计 prompt、completion、total token，并换算成本。
- 调试排错：定位哪一步最慢、哪一步报错、工具为什么被调用。
- 流式输出：在 `on_llm_new_token` 中实时展示 token。
- 质量审计：记录 prompt、工具参数、模型回复，用于复盘幻觉和错误工具调用。
- 安全合规：检查敏感词、PII、越权工具调用、危险指令。
- 用户行为埋点：统计问题类型、工具命中率、检索命中率、失败率。
- 运维告警：在 `on_chain_error`、`on_tool_error`、`on_llm_error` 中上报异常。

## 按对象区分

| 类型 | 适合做什么 |
| --- | --- |
| LLM callbacks | token 统计、流式输出、prompt 记录、成本核算 |
| Chain callbacks | 阶段监控、总耗时、步骤边界 |
| Tool callbacks | 工具入参、出参、失败原因、命中率 |
| Retriever callbacks | 召回数量、相关性、检索延迟、空召回 |
| Error callbacks | 异常采集、报警、重试、降级 |

## 当前课程示例已做到

- chain 开始/结束记录。
- LLM 开始/结束记录。
- 错误事件记录。
- run 级别耗时统计。
- 简单 token 汇总。

## 生产级还需要

- run_id 级状态隔离。
- 日志持久化。
- 成本换算。
- OpenTelemetry / LangSmith / Prometheus 接入。
- 告警和熔断。
- 隐私脱敏。
