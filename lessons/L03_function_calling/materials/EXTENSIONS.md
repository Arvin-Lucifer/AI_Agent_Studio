# L03 拓展练习

## 必做练习

- 给 `practice/05_function_calling.py` 增加 `search_news(keyword)` 工具。
- 给 `practice/05_function_calling.py` 增加 `translate(text, target_lang)` 工具。
- 为每个新工具写清楚 description、参数和 required 字段。
- 准备至少 5 个输入，记录工具选择是否正确。

## 入门拓展（约 30 分钟）

- 给天气工具增加本地缓存，重复查询同一城市时复用结果。
- 给工具调用循环增加 `max_steps`，避免无限 tool calling。
- 为未知工具返回 `{"error": "unknown tool"}`，让模型自我修复。

## 进阶拓展（约 60-90 分钟）

- 给并发脚本增加结构化日志：`trace_id`、`tool_name`、`duration_ms`、`status`。
- 给工具执行增加错误分类：参数错误、权限错误、瞬时错误、空结果。
- 为客服 Agent 设计一套路由策略：customer/refund/ticket/docs/action。

## 高阶拓展（半天）

- 实现一个 tool registry，把工具 metadata 向量化，并按用户请求召回 top-k。
- 为高风险写操作增加 confirmation flow。
- 设计一套 function calling 评估集，统计工具选择准确率、参数准确率、任务完成率和延迟。
- 为噪声工具结果实现 evidence processing：清洗、过滤、归一化、rerank、冲突检测。

## 复盘问题

- 哪个工具最容易被误调？为什么？
- 哪个参数最容易抽错？如何改 schema？
- 哪类错误可以自动恢复，哪类必须问用户？
- 如果工具结果冲突，最终答案应该怎么表达？
