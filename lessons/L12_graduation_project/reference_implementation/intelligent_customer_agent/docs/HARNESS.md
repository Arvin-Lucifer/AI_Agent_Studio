# HARNESS：工程约束说明

## 持久状态

- `feature_list.json` 记录功能验收项。
- `progress.md` 记录开发进度。
- `data/memory.json` 保存多轮 session。
- `data/tickets.jsonl` 保存投诉和转人工工单。

## 工具边界

- `kb_search` 只负责知识库检索。
- `create_ticket` 只负责写入工单。
- `extract_ticket_fields` 只负责工单字段抽取和联系方式掩码。
- `maybe_update_ticket` 只负责同一 session 内打开工单的信息补充。
- `load_memory/save_memory` 只负责会话记忆。
- `log_event/record_chat_metrics` 只负责观测数据。
- `record_feedback_metrics` 只记录答案反馈统计。
- `update_ticket` 只负责工单生命周期更新。
- `record_knowledge_gap/list_knowledge_gaps/update_knowledge_gap` 只负责知识缺口沉淀和状态流转。
- `create_kb_document/rebuild_kb` 只负责知识库文档写入和索引重建。

## 机械约束

所有关键行为通过代码约束，而不是只靠提示词：

- 投诉必走工单节点。
- 无证据或低置信度不能生成产品结论。
- 模糊问题必须澄清。
- 超范围问题必须转人工。
- LLM 只允许在已有 RAG 证据时润色回答，不能替代路由和 guardrail。

## 反馈闭环

项目提供 pytest 和独立 eval 两层验证。运行顺序：

```bash
bash init.sh
python scripts/build_kb.py
pytest -q
python evals/run_eval.py
```

生产运行时还提供用户反馈和工单状态流转：

- 用户在聊天页点击反馈后写入 `feedback.received` 事件。
- Dashboard 可将工单推进到处理中或已解决，并写入 `ticket.updated` 事件。
- 低置信度转人工和差评会进入 `knowledge_gap.recorded` 或 `knowledge_gap.updated` 链路。
- 运营可将 gap 转为 Markdown 知识文档并重建索引，形成 `gap -> kb doc -> eval/retrieval` 改进闭环。
- `/events/recent` 与 `/audit/{trace_id}` 共同支持运营回放。
- 用户在后续消息补充订单号或联系方式时，系统更新原工单并记录 `ticket.enriched` 事件。
- 工单列表和统计接口会计算 SLA 到期状态，支持运营优先处理超时工单。

## 部署与运维

- Dockerfile 固化 Python 3.11 运行环境。
- `scripts/entrypoint.sh` 统一执行目录初始化、知识库索引构建和 API 启动。
- `docker-compose.yml` 暴露 8011 端口并挂载 `data/`、`logs/`。
- Healthcheck 使用 `/health`，便于容器编排系统判断服务状态。

## 安全边界

- 设置 `ADMIN_API_KEY` 后，工单更新、知识缺口更新、知识库新增和索引重建必须携带 `X-Admin-Key`。
- `/chat` 使用轻量内存限流，默认每个身份每分钟 60 次，可通过 `RATE_LIMIT_PER_MINUTE` 配置。
- Docker Compose 默认不读取 `.env`，避免 API Key 在 compose config 或日志中泄露。
