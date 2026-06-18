# 第 12 讲：毕业项目实战 —— 智能客服 Agent

## 12.1 为什么毕业项目选择智能客服 Agent？

智能客服 Agent 是一个非常适合收束本课程的项目，因为它天然需要把前面章节的能力串起来：

- 需要 Prompt 约束回答边界。
- 需要 Function Calling / Tool 封装知识库检索、工单、记忆和日志。
- 需要 RAG 解决私域知识问答。
- 需要 Memory 支持多轮会话。
- 需要 Agent 模式处理澄清、转人工和兜底。
- 需要 LangGraph 显式编排流程。
- 需要评测和部署证明系统不是一次性 Demo。

老师任务包给出的最终选题是：

```text
选题 A：智能客服 Agent
```

核心目标：

```text
基于 LangGraph + RAG + FastAPI + Harness 工程实践，实现一个可运行、可测试、可评测、可部署、可答辩的智能客服 Agent。
```

## 12.2 最低验收标准

项目最低要满足以下要求：

| 编号 | 验收项 | 说明 |
| --- | --- | --- |
| R1 | 知识库问答 | `data/knowledge_base/` 至少 10 份文档 |
| R2 | RAG 检索 | 能检索相关证据，并尽量返回 source/citation |
| R3 | 多轮会话 | 支持 `session_id` 和历史上下文 |
| R4 | 澄清能力 | 模糊问题不能编造，要追问 |
| R5 | 意图识别 | 至少识别问答、咨询、投诉、模糊、超范围 |
| R6 | 投诉工单 | 投诉必须进入工单流程 |
| R7 | 无法回答 | 无证据或低置信度时转人工 |
| R8 | LangGraph | 用状态机显式编排，不只是普通函数顺序调用 |
| R9 | FastAPI | 至少提供 `/health` 和 `/chat` |
| R10 | 评测 | 有 `eval_dataset.jsonl` 和 `run_eval.py` |
| R11 | README | 能让助教独立复现 |

最低标准对应的是“能交作业”。高分项目还要讲清楚工程化闭环。

## 12.3 Harness 工程视角

Harness Engineering 的核心不是写更长的 prompt，而是用工程系统约束 Agent。

本项目的 Harness 可以拆成六层：

| 层级 | 在本项目中的落点 |
| --- | --- |
| 持久状态 | `feature_list.json`、`progress.md`、`memory.json`、`tickets.jsonl` |
| 工具边界 | `kb_search`、`create_ticket`、`load_memory`、`save_memory`、`log_event` |
| 上下文工程 | 只注入当前问题、摘要和 RAG top-k 证据，不塞全量知识库 |
| 反馈验证 | pytest、评测集、独立评测脚本 |
| 机械约束 | 投诉必工单、无证据不编造、低置信度兜底 |
| 可观测性 | `trace_id`、`events.ndjson`、`metrics.json`、审计回放 |

一句话：

```text
Prompt 让模型知道该怎么做，Harness 让系统保证它不能乱做。
```

## 12.4 推荐架构

智能客服 Agent 的主流程：

```text
START
  -> load_memory
  -> classify_intent
  -> route_intent
      -> qa / consult: retrieve_docs -> generate_answer -> evaluate_answer
      -> complaint: create_ticket
      -> unclear: clarify
      -> out_of_scope: human_handoff
  -> save_memory
  -> log_metrics
  -> END
```

参考实现中还增加了：

- `maybe_update_ticket`：同一会话里补充订单号或联系方式时更新原工单。
- `maybe_ticket_status`：用户查询工单状态时直接返回进度。
- `retrieval_router`：按 FAQ、Policy、Manual、Troubleshoot、Product 分库路由。
- `evaluate_answer`：根据证据数量、置信度和 route 判断是否需要澄清或转人工。

## 12.5 RAG 设计

本项目的 RAG 不是只做“向量库查一下”，而是要有可解释、可评测、可调试的检索闭环。

关键点：

1. 知识库至少 10 份 Markdown 文档，覆盖 FAQ、政策、产品、手册和故障排查。
2. 检索结果必须带 `source_id`、`title`、`collection`、`score`、`snippet`。
3. 无证据或低置信度时不要强答。
4. Dashboard 或调试接口最好能展示命中文档和分数。
5. 口语化问题要做 query normalization，例如“退钱”“短信码”“一直转圈”要映射到知识库概念。

## 12.6 工单与人工兜底

智能客服项目最容易出问题的地方，是系统“看起来答了”，但其实没有证据。

因此要把工单和人工兜底作为一等公民：

- 投诉类问题必须生成投诉工单。
- 超范围问题生成人工处理单或礼貌拒答。
- 低置信度问题记录知识缺口，后续补知识库。
- 工单要有状态、优先级、SLA、trace 和必要字段。

参考实现还做了：

- 订单号抽取。
- 联系方式脱敏。
- 多轮工单补充。
- 工单状态查询。
- Dashboard 工单处理。

## 12.7 评测与质量门禁

毕业项目必须有评测脚本，不能只靠“我试了几个问题还行”。

评测至少覆盖：

- FAQ 问答。
- 咨询问题。
- 退款/发票/登录/套餐等业务问题。
- 投诉工单。
- 模糊问题澄清。
- 超范围转人工。
- 多轮上下文。

指标可以包括：

- intent accuracy
- route accuracy
- ticket success rate
- fallback accuracy
- clarification accuracy
- keyword hit rate
- schema valid rate
- overall score

关键要求：

```text
评测器独立于主 Agent，不让主 Agent 自评。
```

## 12.8 部署与演示

参考实现提供两种演示方式：

1. 本地 Uvicorn：

```bash
python scripts/build_kb.py
bash scripts/run_api.sh
```

2. Docker Compose：

```bash
docker compose up --build
```

演示时建议展示：

- `/health` 健康检查。
- `/chat` 业务问答。
- 投诉工单。
- 模糊问题澄清。
- 超范围转人工。
- 前端客服台。
- Dashboard 指标、审计、工单和质量门禁。

## 12.9 六轮迭代路线

从老师 Word 实战参考中抽取出的迭代路线：

1. PRD -> TRD -> TDD -> Harness，完成基础智能客服 Agent。
2. 补齐前后端项目。
3. 添加记忆系统、ReAct、多跳 RAG、分库索引和路由。
4. 添加可观测数据和监控大盘。
5. 抽取 MCP 和 Skill。
6. 形成项目总结，用于答辩和面试。

参考实现已经完成 1-4 轮，并覆盖部分高分运营闭环；MCP/Skill 抽取建议作为扩展练习。

## 12.10 答辩表达

答辩不要只讲“我用了 LangGraph、FastAPI、RAG”。要讲清楚为什么这么设计。

推荐结构：

1. 项目定位：这是一个生产级智能客服 Agent，不是单轮问答 Demo。
2. 架构主线：LangGraph 显式编排客服流程。
3. 可信回答：RAG 证据、引用、无证据兜底。
4. 稳定性：投诉必工单、低置信度转人工、步数上限。
5. 质量证明：pytest + eval + Dashboard Quality Gate。
6. 可观测：trace、events、metrics、audit replay。
7. 可运营：反馈、知识缺口、知识库新增、索引重建。
8. 后续扩展：MCP/Skill、多跳 RAG、ReAct 兜底。

## 12.11 本章作业

必做：

1. 跑通参考实现的测试和评测。
2. 启动 FastAPI 服务，完成一次问答、一次投诉、一次模糊澄清、一次超范围转人工。
3. 截取或记录一个 `trace_id`，在 Dashboard 或 `/audit/{trace_id}` 中回放。
4. 阅读 `feature_list.json`，挑选 3 个功能说明其验收方式。
5. 写一页答辩稿，说明项目定位、架构亮点和质量证明。

选做：

1. 增加一份知识库文档，并重建索引。
2. 增加 2 条评测用例，运行 `python evals/run_eval.py`。
3. 设计 `kb-retrieval` MCP 的接口文档。
4. 将某个子能力抽成 Skill，例如 `multihop-rag` 或 `ticket-triage`。

