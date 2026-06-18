# TDD：测试与评测设计

## 单元与接口测试

- `tests/test_api.py`：验证 `/health`、`/chat` schema、投诉工单、metrics/audit。
- `tests/test_graph.py`：验证意图路由到 RAG、工单、澄清和转人工。
- `tests/test_rag.py`：验证知识库文档数量、退款和登录失败检索效果。
- `tests/test_guardrails.py`：验证无证据不编造、低置信度 fallback、投诉强制工单。
- `tests/test_eval.py`：验证评测集可读、评测脚本输出指标。

## 独立评测

`evals/run_eval.py` 不调用主 Agent 自评，而是用规则检查：

- intent accuracy
- route accuracy
- ticket success rate
- fallback accuracy
- clarification accuracy
- keyword hit rate
- schema valid rate

评测结果写入 `evals/eval_report.json`。

