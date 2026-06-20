# Agent 记忆三层架构

## 三层划分

```text
短期记忆 Working Memory
当前对话上下文，通常是 messages 或 checkpointer。

长期记忆 Long-term Memory
跨会话保存用户画像、偏好、事实和任务结果。

外部知识 External Knowledge
企业知识库、数据库、文档系统、搜索系统。
```

## 类比

| 层级 | 类比 | 典型实现 |
| --- | --- | --- |
| 短期记忆 | 工作台 | messages、MemorySaver、summary buffer |
| 长期记忆 | 笔记本 | JSON、SQLite、Postgres、Chroma、Redis |
| 外部知识 | 图书馆 | RAG、数据库、搜索 API、业务系统 |

## 常见误区

1. 把所有历史都塞进 prompt。
2. 把 `MemorySaver` 当生产长期记忆。
3. 只做向量检索，不区分画像、偏好和事实。
4. 没有删除机制。
5. 不做用户隔离。

## 推荐最小架构

```text
User input
  -> 短期上下文管理：窗口 / 摘要
  -> 长期记忆检索：profile + preference + facts
  -> 外部知识检索：RAG / DB
  -> LLM 生成
  -> 记忆写入判断：是否保存新事实/偏好
  -> 审计与遗忘策略
```
