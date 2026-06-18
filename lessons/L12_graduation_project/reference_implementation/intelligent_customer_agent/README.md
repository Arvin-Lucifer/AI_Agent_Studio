# Intelligent Customer Agent

基于 LangGraph + RAG + FastAPI + Harness 工程实践的智能客服 Agent。项目实现第 12 讲选题 A：知识库问答、多轮对话、意图识别、投诉工单、无法回答转人工、评测集与评测脚本。

## 运行环境

本机已验证可复用 conda 环境 `agent_course`：

```bash
bash init.sh
conda activate agent_course
```

课程归档版不会携带真实 `.env`。如需实验 API 配置，请从 `.env.example` 复制一份本地 `.env` 并填写自己的密钥；源码和文档不会展示真实密钥。即使没有 API Key，本项目也会使用离线规则 + RAG 路径运行测试和评测。

默认演示使用离线 grounded RAG 摘要，速度稳定、评测可复现。如果需要在线 LLM 润色，可以在本地运行时的 `.env` 中配置 `OPENAI_API_KEY`、`OPENAI_BASE_URL`、`OPENAI_MODEL`，并显式设置 `USE_LLM_ANSWERS=1`。LLM 只会在“已有知识库证据”的前提下组织客服回答；投诉、无证据、低置信度和超范围问题仍由 guardrails 接管，不会因为接入 LLM 而绕过工单或人工兜底。

生产演示时可以设置：

```bash
ADMIN_API_KEY=<your-admin-key>
RATE_LIMIT_PER_MINUTE=60
```

设置 `ADMIN_API_KEY` 后，工单状态更新、知识缺口状态更新、知识库新增和索引重建都需要请求头 `X-Admin-Key`。Dashboard 顶部可以输入 Admin Key，浏览器会保存在本地 localStorage 中。

## 常用命令

```bash
python scripts/build_kb.py
pytest -q
python evals/run_eval.py
bash scripts/run_api.sh
```

`scripts/run_api.sh` 默认启用 reload，但只监控 `intelligent_customer/` 和 `web/`，避免评测、日志或运行期数据变化导致服务反复重启。需要更接近生产的稳定进程时可运行：

```bash
RELOAD=0 bash scripts/run_api.sh
```

也可以使用 Makefile：

```bash
make build-kb
make test
make eval
make run
```

当前服务地址：

```text
http://127.0.0.1:8011
```

## Docker 部署

本项目提供 Dockerfile 和 docker-compose，适合答辩现场说明“如何交付部署”。

```bash
docker compose up --build
```

如果构建时出现类似：

```text
proxyconnect tcp: dial tcp 127.0.0.1:11451: connect: connection refused
```

说明 Docker daemon 正在使用本机代理但代理没有运行。处理方式是关闭 Docker 代理配置、启动对应代理，或先手动拉取基础镜像：

```bash
docker pull python:3.11-slim
```

启动后访问：

```text
http://127.0.0.1:8011/
http://127.0.0.1:8011/web/dashboard.html
```

容器启动时会自动执行：

```text
python scripts/build_kb.py
uvicorn intelligent_customer.api:app --host 0.0.0.0 --port 8011
```

Docker Compose 默认不注入 `.env`，避免 `docker compose config` 或日志中意外暴露密钥；容器演示默认走离线 RAG。需要在线 LLM 时，请在安全的部署环境中显式传入环境变量或使用私有 compose override。

Compose 会挂载：

```text
./data -> /app/data
./logs -> /app/logs
```

因此工单、记忆、知识缺口、日志和运行期新增知识文档都能保留在宿主机目录。

停止后台服务：

```bash
kill $(cat logs/uvicorn.pid)
```

## API 示例

健康检查：

```bash
curl http://127.0.0.1:8011/health
```

聊天：

```bash
curl -X POST http://127.0.0.1:8011/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"我想退款，怎么处理？","session_id":"demo","user_id":"u001"}'
```

投诉会强制生成工单：

```bash
curl -X POST http://127.0.0.1:8011/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"我要投诉，你们客服态度差","session_id":"demo"}'
```

工单会自动抽取订单号、联系方式掩码、问题类型、紧急程度和 SLA。例如：

```bash
curl -X POST http://127.0.0.1:8011/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"我要投诉，订单号 ORD202606050001 重复扣费，请联系 13812345678。","session_id":"demo"}'
```

如果用户第一次没有提供订单号或联系方式，Agent 会先创建工单并提示继续补充；同一 session 后续发送“订单号是 XXX，手机号 XXX”会自动补充到原工单，而不是重新创建工单。

可观测接口：

```bash
curl http://127.0.0.1:8011/metrics
curl http://127.0.0.1:8011/audit/{trace_id}
curl http://127.0.0.1:8011/tickets
curl http://127.0.0.1:8011/events/recent
curl http://127.0.0.1:8011/knowledge-gaps
curl http://127.0.0.1:8011/kb/docs
curl -G http://127.0.0.1:8011/kb/search \
  --data-urlencode "q=退款多久到账" \
  -d "collection=policy" \
  -d "k=5"
```

质量门禁评测：

```bash
curl http://127.0.0.1:8011/eval/report
curl -X POST http://127.0.0.1:8011/eval/run \
  -H "X-Admin-Key: <your-admin-key>"
```

`/eval/run` 会调用独立评测脚本生成 `evals/eval_report.json`，评测期间会临时关闭 LLM 回答以保持可复现，结束后恢复原运行环境。

答案反馈：

```bash
curl -X POST http://127.0.0.1:8011/feedback \
  -H "Content-Type: application/json" \
  -d '{"trace_id":"trace_xxx","session_id":"demo","rating":"up"}'
```

工单状态更新：

```bash
curl -X PATCH http://127.0.0.1:8011/tickets/TICKET_ID \
  -H "Content-Type: application/json" \
  -H "X-Admin-Key: <your-admin-key>" \
  -d '{"status":"in_progress","assignee":"ops-demo","note":"开始跟进"}'
```

知识缺口处理：

```bash
curl http://127.0.0.1:8011/knowledge-gaps/stats
curl -X PATCH http://127.0.0.1:8011/knowledge-gaps/KG_ID \
  -H "Content-Type: application/json" \
  -H "X-Admin-Key: <your-admin-key>" \
  -d '{"status":"reviewing","note":"准备补充知识库"}'
```

知识库运营：

```bash
curl -X POST http://127.0.0.1:8011/kb/docs \
  -H "Content-Type: application/json" \
  -H "X-Admin-Key: <your-admin-key>" \
  -d '{"title":"新知识","collection":"faq","content":"这里填写经过人工确认的标准答案。"}'

curl -X POST http://127.0.0.1:8011/kb/rebuild \
  -H "X-Admin-Key: <your-admin-key>"
```

前端页面：

```text
http://127.0.0.1:8011/
http://127.0.0.1:8011/web/dashboard.html
```

聊天页支持会话恢复、新会话、会话列表、Enter 发送、中文输入法组合状态保护、发送中状态、失败重试、消息时间、响应耗时、引用展示、工单展示、trace/工单号复制、带原因的答案反馈和下一步快捷动作。会话列表不再只显示 session_id，而是显示业务标题、更新时间、最后 intent/route、工单号和人工状态，并支持关键词搜索和按待人工、有工单、RAG 已回答、需澄清筛选，方便客服在多个会话间切换。界面增加了用户/AI 身份标识、intent/route 状态色、输入焦点态和发送“处理中”状态，更接近真实客服工作台。短追问会结合当前 session 的上下文改写检索查询，例如先问“专业版和企业版有什么区别？”，再问“那 SLA 呢？”，系统会带着上轮产品版本语境继续检索。系统还会把“钱什么时候退回来”“短信码收不到”“开票抬头填错”“一直转圈打不开”等口语说法归一化到退款、验证码、发票和登录故障等知识库概念；生成答案时会按用户问题对证据句重新排序，优先返回最相关句子。引用卡片会显示知识库证据片段，桌面端右侧 Session Insight 面板会同步展示当前意图、路由、置信度、响应耗时、证据数、工单号、上下文查询、引用来源和下一步动作。
Dashboard 支持指标、工单状态处理、知识缺口管理、知识库文档创建、索引重建、近期事件和审计回放。Search Lab 可以直接输入用户问题，查看 RAG 命中的文档、分数和证据片段，用来判断回答不理想时到底是知识缺口、检索问题还是生成策略问题。
Dashboard 还提供 Quality Gate 面板，可以直接查看最新评测分数、失败用例和各项准确率，并通过 Admin Key 触发一次完整回归评测。

## 评测说明

评测集位于 `evals/eval_dataset.jsonl`，覆盖 FAQ、咨询、退款、故障、投诉、模糊问题、超范围问题和多轮上下文。评测脚本会自动关闭 LLM 回答，使用确定性的离线 RAG 路径，避免网络、模型波动或 token 消耗影响复现。

运行：

```bash
python evals/run_eval.py
```

也可以在服务启动后通过 Dashboard 的 Quality Gate 面板查看/触发评测，或调用：

```bash
curl http://127.0.0.1:8011/eval/report
curl -X POST http://127.0.0.1:8011/eval/run \
  -H "X-Admin-Key: <your-admin-key>"
curl http://127.0.0.1:8011/eval/generated-cases
```

输出文件：

```text
evals/eval_report.json
evals/generated_eval_cases.jsonl
```

`generated_eval_cases.jsonl` 保存从 knowledge gap 自动生成的待评审评测草稿，不会默认污染主基准评测集。运营可以在 Dashboard 的 Knowledge Gaps 面板点击“转评测”，生成草稿后再人工确认 expected 字段并合入主评测集。

已验证指标：

```text
total = 32
overall_score = 1.0
schema_valid_rate = 1.0
ticket_success_rate = 1.0
```

## 项目结构

```text
intelligent_customer_agent/
├── intelligent_customer/
│   ├── api.py                  # FastAPI app
│   ├── graph.py                # LangGraph 状态机
│   ├── schemas.py              # Pydantic schema
│   ├── nodes/                  # LangGraph 节点
│   ├── rag/                    # 知识库构建、检索、路由
│   ├── tools/                  # kb_search、ticket、memory、eval 工具边界
│   └── harness/                # guardrails、observability、state、file_lock、privacy
├── data/
│   ├── knowledge_base/         # 10 份 Markdown 知识库
│   ├── memory.json             # session 记忆
│   └── tickets.jsonl           # 投诉/人工工单
├── evals/
│   ├── eval_dataset.jsonl
│   ├── generated_eval_cases.jsonl
│   └── run_eval.py
├── tests/
├── docs/
├── web/
├── logs/
├── feature_list.json
├── progress.md
├── init.sh
├── Dockerfile
├── docker-compose.yml
├── Makefile
└── README.md
```

## 答辩亮点

1. 用 LangGraph 显式表达客服流程：意图分类 -> 条件路由 -> RAG/澄清/工单/人工 -> 记忆与日志。
2. RAG 默认离线可跑，知识库检索结果带 source/citation，避免没有 API Key 时无法验收。
3. Harness guardrails 写入代码：投诉必工单、无证据不编造、低置信度转人工、模糊问题澄清。
4. 评测脚本独立于主 Agent，不让 Agent 自评，指标可复现。
5. 可观测闭环完整：trace_id、events.ndjson、metrics.json、`/metrics`、`/audit/{trace_id}`。
6. 保留 `.env` 和 LLM 配置入口，可在后续扩展真实 LLM、多跳 RAG、ReAct 或 MCP/Skill。
7. 前端不再是一次性 demo：支持历史恢复、会话切换、引用和工单状态展示，更贴近客服工作台。
8. 生产反馈闭环：用户可对答案反馈，运营页可处理工单并回放 trace，便于持续改进知识库和规则。
9. 知识缺口闭环：低置信度转人工和用户差评会沉淀为 knowledge gaps，运营可以在 Dashboard 评审、关闭并回放证据链。
10. 知识库运营闭环：Dashboard 可以把 gap 转成新知识文档，调用 `/kb/rebuild` 后立即进入 RAG 检索路径。
11. 部署运维闭环：Dockerfile、docker-compose、healthcheck、Makefile 和 entrypoint 让项目能从本地演示走向容器交付。
12. 安全护栏闭环：可选 Admin Key 保护管理写接口，`/chat` 有基础速率限制，Docker Compose 默认不注入 `.env` 防止密钥泄露。
13. 智能工单闭环：投诉/转人工会自动抽取订单号、联系方式掩码、问题类型、紧急程度和 SLA，Dashboard 可直接展示。
14. 多轮工单补充：用户后续补充订单号或联系方式时，LangGraph 会更新当前 session 的打开工单。
15. SLA 监控闭环：工单自动计算 `due_at`、`minutes_to_due` 和 `overdue`，Dashboard 会高亮超时工单。
16. 质量门禁闭环：`/eval/report`、`/eval/run` 和 Dashboard Quality Gate 把独立评测从命令行带到运维界面，便于答辩现场展示回归质量。
17. 并发持久化护栏：memory、tickets、knowledge gaps、events 和 metrics 的本地 JSON/JSONL 读写增加 sidecar 文件锁，减少多请求并发写入时的丢更新风险。
18. 上下文追问体验：短追问会根据 session history 改写检索查询，回复会返回 suggested_actions，前端可一键继续问下一个自然问题。
19. 隐私脱敏护栏：审计事件、工单正文和工单备注会自动遮罩手机号、邮箱和长数字凭证，保留 `contact_masked` 供客服跟进，降低日志泄露风险。
20. 聊天内工单状态闭环：用户可在同一会话中问“查看工单状态”，或直接提供工单号查询进度，LangGraph 会返回状态、SLA、负责人和缺失字段提示。
21. 人工接手摘要：工单 metadata 自动包含 handoff summary、最近对话、证据来源、缺失字段和下一步建议，Dashboard 工单卡片直接展示接手摘要。
22. Session Insight 面板：聊天页右侧实时展示路由、置信度、证据、工单、上下文查询和建议动作，让状态从一次性气泡变成持续可见的工作台信息。
23. 证据片段引用：`Citation` schema 增加 `snippet`，聊天页引用卡片直接展示命中的知识库摘录，提升 RAG 回答的可解释性和可信度。
24. 缺口转评测闭环：knowledge gap 可一键生成 `generated_eval_cases.jsonl` 草稿，把差评/转人工问题纳入后续回归评测。
25. RAG 检索调试闭环：`/kb/search` 和 Dashboard Search Lab 展示命中文档、分数、source_id 和证据片段，方便定位“不聪明”的根因。
26. 客服台体验闭环：聊天页持续展示消息时间、响应耗时和健康状态轮询，并兼容中文输入法下的 Enter 发送。
27. 口语理解闭环：查询归一化把“退钱/短信码/开票/一直转圈”等真实用户说法映射到知识库概念，减少误判超范围和无效转人工。
28. 操作恢复闭环：聊天页支持失败重试、复制 trace/工单号和带原因的差评反馈，让客服台更适合持续运营。
29. 视觉体验闭环：聊天页使用身份头像、状态色 chip、输入焦点态和发送处理中状态，降低“临时 demo 感”。
30. 会话状态闭环：`/sessions` 返回标题、更新时间、最后 intent/route、工单号和人工状态，侧边栏可持续展示多会话状态。
31. 会话队列闭环：侧边栏支持关键词搜索和按待人工、有工单、RAG 已回答、需澄清筛选，适合多会话运营。
32. 答案相关性闭环：RAG 命中文档后按问题相关性重排证据句，减少“找到了文档但先答偏”的情况。
