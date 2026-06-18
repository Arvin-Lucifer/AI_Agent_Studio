# AGENTS.md

## Mission

实现基于 LangGraph + RAG + FastAPI + Harness 工程实践的智能客服 Agent，满足第 12 讲选题 A。

## Non-Negotiable Rules

1. 知识库至少 10 份 Markdown 文档。
2. 使用 LangGraph 显式建模状态、节点和条件边。
3. 投诉必须走工单。
4. 无证据、低置信度、超范围必须澄清或转人工，不能编造。
5. FastAPI 响应必须结构化，并包含 trace_id、intent、route、confidence、ticket_id、need_human。
6. 评测脚本独立于主 Agent，不让主 Agent 自评。
7. 密钥只允许出现在 `.env`，源码和 README 不展示真实密钥。

## Preferred Commands

```bash
bash init.sh
conda activate agent_course
python scripts/build_kb.py
pytest -q
python evals/run_eval.py
uvicorn intelligent_customer.api:app --host 0.0.0.0 --port 8011 --reload
```

## Definition Of Done

`bash init.sh`、知识库构建、pytest、评测脚本、FastAPI 启动均成功；README 能让助教独立复现；logs 和 tickets 可审计。

