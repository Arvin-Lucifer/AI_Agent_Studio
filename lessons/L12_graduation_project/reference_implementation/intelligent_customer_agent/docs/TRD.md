# TRD：技术方案

## 架构概览

请求进入 FastAPI 后，由 `intelligent_customer.graph.run_agent` 调用 LangGraph 状态机。状态机节点包括：

1. `load_memory`
2. `classify_intent`
3. `route_intent`
4. `retrieval_router`
5. `retrieve_docs`
6. `generate_answer`
7. `evaluate_answer`
8. `clarify`
9. `create_ticket`
10. `human_handoff`
11. `save_memory`

## RAG 方案

默认使用离线关键词检索，知识库文档通过 `scripts/build_kb.py` 构建为 `data/kb_index.json`。检索结果包含 `source_id`、`title`、`collection`、`score`、`content` 和 `path`。

在线演示默认使用离线 grounded 摘要生成，避免外部 API 抖动影响体验。如果 `.env` 显式设置 `USE_LLM_ANSWERS=1`，`generate_answer` 节点会在检索证据存在时调用 OpenAI-compatible API 做 grounded answer 生成。LLM 只能看到当前问题、会话摘要和 top-k 证据；无证据、投诉、超范围和低置信度仍由 LangGraph guardrails 路由到澄清、工单或人工。

分库路由按关键词选择 FAQ、Policy、Manual、Troubleshoot、Product collection。无明确关键词时检索全库，保证本地无 API Key 也能评测。

## Guardrails

- `complaint -> ticket`
- `unclear -> clarify`
- `out_of_scope -> human_handoff`
- `qa/consult -> retrieve`
- `no evidence -> human_handoff`
- `low confidence -> clarify/human_handoff`

关键规则落在 `harness/guardrails.py` 和 LangGraph 条件边中。

## 状态与可观测性

- 会话记忆：`data/memory.json`
- 工单：`data/tickets.jsonl`
- 事件日志：`logs/events.ndjson`
- 聚合指标：`logs/metrics.json`
- API 暴露：`/metrics`、`/audit/{trace_id}`
- 用户反馈：`POST /feedback` 写入事件流并更新反馈指标。
- 工单运营：`PATCH /tickets/{ticket_id}` 支持 `open`、`in_progress`、`resolved`、`closed` 状态流转。
- 智能工单：创建工单时通过规则抽取订单号、联系方式掩码、问题类型、紧急程度、优先级和 SLA。
- 多轮工单补充：`load_memory` 后会进入 `maybe_update_ticket` 节点；若当前 session 有打开工单且用户补充订单号/联系方式，则更新原工单并直接结束本轮。
- SLA 监控：工单创建时写入 `due_at`，列表和统计接口动态计算 `minutes_to_due` 与 `overdue`，Dashboard 对超时工单做高亮。
- 知识缺口：低置信度转人工和差评会写入 `data/knowledge_gaps.jsonl`，通过 `/knowledge-gaps` 和 `/knowledge-gaps/stats` 暴露，支持评审和关闭。
- 知识库运营：`/kb/docs` 支持查看和新增 Markdown 文档，`/kb/rebuild` 重建索引并清理检索缓存，使新知识立即进入 RAG。

## 前端工作台

`web/index.html` 是纯 HTML/CSS/JS 客服工作台，支持会话列表、会话恢复、新会话、Enter 发送、发送中状态、引用卡片、工单状态、trace 信息和答案反馈。`web/dashboard.html` 面向运营和答辩展示，支持指标、工单处理、知识缺口管理、知识库文档创建、索引重建、近期事件和审计回放。它们直接调用 FastAPI，不引入构建链，便于答辩现场展示。

## 部署方案

项目提供 Dockerfile、docker-compose、Makefile 和 `scripts/entrypoint.sh`。容器启动时先构建知识库索引，再启动 `uvicorn intelligent_customer.api:app`。Compose 挂载 `data/` 和 `logs/`，保证工单、记忆、知识缺口和运行日志可持久化。健康检查调用 `/health`。

## 安全方案

管理写接口使用可选 Admin Key。未设置 `ADMIN_API_KEY` 时保持课堂演示便利；设置后，`PATCH /tickets/{ticket_id}`、`PATCH /knowledge-gaps/{gap_id}`、`POST /kb/docs` 和 `POST /kb/rebuild` 必须携带 `X-Admin-Key`。`/chat` 使用内存滑动窗口限流，防止单个 session 或客户端短时间刷爆服务。
