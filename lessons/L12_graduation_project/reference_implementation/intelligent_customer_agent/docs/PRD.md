# PRD：智能客服 Agent

## 项目定位

本项目实现一个基于 LangGraph + RAG + FastAPI + Harness 工程实践的智能客服 Agent。它不是单轮问答 demo，而是覆盖知识库问答、多轮会话、意图分类、投诉工单、无法回答转人工、评测脚本和可观测日志的端到端应用。

## 用户目标

1. 用户能询问账号、订单、退款、发票、套餐、故障排查等产品或服务问题。
2. 用户描述模糊时，系统能追问澄清，而不是编造答案。
3. 用户投诉时，系统必须创建投诉工单。
4. 知识库没有证据或置信度低时，系统必须转人工并生成工单。
5. 助教能通过 API、测试和评测脚本验证项目行为。

## 核心范围

- FastAPI `/chat`、`/health`、`/metrics`、`/audit/{trace_id}`。
- RAG 知识库：至少 10 份 Markdown 文档。
- LangGraph 编排：加载记忆、意图分类、路由、检索、回答、评估、澄清、工单、保存记忆。
- Harness 文件：`feature_list.json`、`progress.md`、`init.sh`、`AGENTS.md`。
- 评测集和独立评测脚本。

## 不做范围

- 不依赖外部 LLM 才能运行。
- 不把 API Key 写入源码或 README。
- 不做无限循环 ReAct；高级能力仅作为后续扩展。

