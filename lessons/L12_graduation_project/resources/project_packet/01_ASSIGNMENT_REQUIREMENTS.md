# 第 12 讲毕业项目主要求整理版

## 1. 作业背景

第 12 讲是综合实战，需要从给定的三个 Agent 项目中选择一个，端到端完成一个生产级 Agent 应用。

本项目最终建议选择：

```text
选题 A：智能客服 Agent
```

原因：老师的主作业要求、Harness 工程实践指南、以及具体实战参考 Word 文档都最适合落到“智能客服 Agent”这个方向上。它也最容易完整覆盖 RAG、LangGraph、FastAPI、评测集、评测脚本、多轮对话、工单兜底和可观测性。

---

## 2. 三个可选项目

### 2.1 选题 A：智能客服 Agent

#### 功能需求

```text
1. 基于知识库回答产品 / 服务相关问题。
2. 支持多轮对话，能澄清模糊问题。
3. 识别用户意图：问答、投诉、咨询。
4. 无法回答时，生成工单转人工。
```

#### 技术要求

```text
1. RAG 知识库，至少 10 份文档。
2. LangGraph 流程编排：意图分类 -> 路由 -> 处理。
3. FastAPI 部署。
4. 评测集 + 评测脚本。
```

#### 本项目采用该选题

本项目应围绕这个选题实现完整应用，而不是只做单轮 RAG 问答 demo。

---

### 2.2 选题 B：自动化办公 Agent

#### 功能需求

```text
1. 读取邮件 / 消息，提取待办事项。
2. 按优先级排序待办。
3. 自动创建任务，输出到文件或 API。
4. 生成每日工作摘要。
```

#### 技术要求

```text
1. 多工具：邮件解析工具、任务创建工具、摘要生成工具。
2. 记忆系统：记住已处理的邮件、用户偏好。
3. LangGraph 流程编排。
4. FastAPI 部署。
```

---

### 2.3 选题 C：代码助手 Agent

#### 功能需求

```text
1. 根据自然语言描述生成代码。
2. 自动运行代码并检测错误。
3. 如果报错，自动修复后重试。
4. 生成代码解释文档。
```

#### 技术要求

```text
1. 工具：代码生成、代码执行沙箱、错误分析。
2. LangGraph 流程：生成 -> 执行 -> 检查 -> 修复循环。
3. 最大重试次数控制。
4. FastAPI 部署。
```

---

## 3. 本项目的硬性验收条件

Codex 实现时必须优先满足以下条件。

| 编号 | 验收项 | 最低要求 |
|---|---|---|
| R1 | 选题 | 必须实现智能客服 Agent，即选题 A。 |
| R2 | 知识库 | `data/knowledge_base/` 下至少 10 份 Markdown 文档，覆盖 FAQ、政策、产品说明、使用手册、故障排查等。 |
| R3 | RAG | 能从知识库检索相关片段，并基于证据回答。回答应尽量带 source / citation 信息。 |
| R4 | 多轮对话 | 支持 `session_id`，同一个会话内能读取历史上下文或摘要。 |
| R5 | 澄清能力 | 对模糊问题不能直接编造答案，应追问澄清。 |
| R6 | 意图识别 | 至少识别 `qa`、`consult`、`complaint`、`unclear`、`out_of_scope`。主要求里明确的是问答、投诉、咨询，额外增加模糊和超范围用于生产兜底。 |
| R7 | 投诉处理 | 投诉类问题必须进入工单流程，生成结构化工单并保存。 |
| R8 | 无法回答 | 无知识库证据、低置信度、超出服务范围时，应生成工单或转人工，不允许强行编造。 |
| R9 | LangGraph | 必须使用 LangGraph 显式编排流程，不能只是普通函数顺序调用。 |
| R10 | FastAPI | 必须提供可启动的 API 服务，至少包含 `/health` 和 `/chat`。 |
| R11 | 评测集 | 必须提供 `evals/eval_dataset.jsonl`，覆盖问答、咨询、投诉、模糊、无法回答等场景。 |
| R12 | 评测脚本 | 必须提供 `evals/run_eval.py`，能运行并输出评测指标。 |
| R13 | README | 必须说明安装、启动、接口、示例请求、评测方法和项目结构。 |

---

## 4. 建议补充的高分项

以下不是主文档最小要求，但符合老师希望参考 Harness 风格完成作业的方向。

| 加分项 | 建议实现 |
|---|---|
| Harness 状态文件 | `feature_list.json`、`progress.md`、`init.sh`、`AGENTS.md`。 |
| 独立 Evaluator | 评测脚本不要让生成答案的 Agent 自评；应由独立逻辑检查意图、工单、fallback、引用等。 |
| 可观测性 | 写入 `logs/events.ndjson`、`logs/metrics.json`，提供 `/metrics`、`/audit/{trace_id}`。 |
| 前端页面 | 纯 HTML/CSS/JS 聊天页面即可，能展示 session 历史和工单弹窗更好。 |
| 分库检索 | FAQ / Policy / Manual / Troubleshoot / Product 分 collection 或分目录检索。 |
| ReAct 兜底 | 只在低置信度、复杂问题、多跳失败时触发，必须有最大轮数。 |
| 多跳 RAG | 对复杂组合问题拆分子问题，逐步检索后合成答案。 |
| MCP / Skill | 可作为最后加分项，不应影响核心功能可运行。 |

---

## 5. 最终交付物清单

Codex 最终应该生成以下内容。

```text
intelligent_customer_agent/
├── README.md
├── requirements.txt
├── init.sh
├── AGENTS.md
├── feature_list.json
├── progress.md
├── .env.example
├── docs/
│   ├── PRD.md
│   ├── TRD.md
│   ├── TDD.md
│   └── HARNESS.md
├── app/ 或 intelligent_customer/
│   ├── main.py / api.py
│   ├── config.py
│   ├── schemas.py
│   ├── graph.py
│   ├── nodes/
│   ├── rag/
│   ├── tools/
│   └── harness/
├── data/
│   ├── knowledge_base/        # 至少 10 份文档
│   ├── memory.json
│   └── tickets.jsonl
├── evals/
│   ├── eval_dataset.jsonl
│   ├── run_eval.py
│   └── eval_report.json       # 运行后生成
├── tests/
├── logs/                      # 运行后生成
└── web/                       # 可选：前端与监控大盘
```

---

## 6. 项目一句话定位

```text
这是一个基于 LangGraph 的智能客服 Agent，不只是单轮 RAG 问答，而是具备知识库检索、意图分类、条件路由、多轮记忆、投诉工单、无法回答转人工、评测脚本和可观测日志的端到端生产级 Agent 应用。
```
