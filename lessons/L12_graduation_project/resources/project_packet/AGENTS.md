# AGENTS.md

本文件是给 Codex 的项目级长期规则。请把它放在最终项目仓库根目录。

## 1. Repository Mission

实现一个毕业项目：

```text
基于 LangGraph + RAG + FastAPI + Harness 工程实践的智能客服 Agent。
```

项目必须满足老师第 12 讲选题 A 的要求：知识库问答、多轮澄清、意图识别、投诉工单、无法回答转人工、RAG 知识库、LangGraph 编排、FastAPI 部署、评测集和评测脚本。

## 2. Read First

开始编码前必须阅读：

```text
01_ASSIGNMENT_REQUIREMENTS.md
02_HARNESS_ENGINEERING_GUIDE.md
03_CODEX_TASK_BRIEF.md
具体实战参考.docx
```

实现时以 `03_CODEX_TASK_BRIEF.md` 为直接任务说明。

## 3. Non-negotiable Requirements

必须满足：

```text
1. 选择并实现智能客服 Agent，不做 B 或 C。
2. 至少 10 份知识库文档。
3. 使用 LangGraph 显式编排流程。
4. 提供 FastAPI 服务。
5. 提供 eval_dataset.jsonl 和 run_eval.py。
6. 投诉类问题必须生成工单。
7. 无知识库证据时不得编造答案。
8. 低置信度必须澄清、ReAct 兜底或转人工。
9. 所有 API 响应必须结构化。
10. 不允许硬编码 API Key。
```

## 4. Engineering Style

遵循 Harness 风格：

```text
持久状态：feature_list.json、progress.md、memory.json、tickets.jsonl。
工具边界：kb_search、create_ticket、load_memory、save_memory、log_event。
反馈验证：pytest、evals/run_eval.py、schema 校验。
机械约束：guardrails.py、条件路由、Pydantic schema。
可观测性：trace_id、events.ndjson、metrics、audit replay。
增量推进：一次只完成一个 feature，并记录进度。
```

## 5. Development Workflow

每次开发按顺序执行：

```text
1. 查看 feature_list.json，选择一个 passes=false 的功能。
2. 实现该功能。
3. 写或更新测试。
4. 运行相关测试。
5. 如果通过，更新 feature_list.json 和 progress.md。
6. 如果失败，记录失败原因和下一步。
```

不要只说“完成了”，必须能用命令验证。

## 6. Preferred Commands

```bash
bash init.sh
python scripts/build_kb.py
pytest -q
python evals/run_eval.py
uvicorn intelligent_customer.api:app --host 0.0.0.0 --port 8011 --reload
```

## 7. Coding Rules

```text
1. Python 3.11+。
2. Pydantic v2。
3. FastAPI 路由和业务逻辑分离。
4. LangGraph 节点尽量保持单一职责。
5. 工具函数输入输出结构化。
6. 配置统一从 config.py 和环境变量读取。
7. 不要把全量知识库塞进 prompt。
8. 保持无 API Key 的 mock / fallback 测试路径。
9. README、PRD、TRD、TDD、HARNESS 文档使用中文。
10. 代码注释可以中英混合，但接口字段尽量英文。
```

## 8. Guardrail Rules

必须机械执行：

```text
complaint -> create_ticket
unclear -> clarify
out_of_scope -> human_handoff
qa / consult -> retrieve_docs
no evidence -> human_handoff or clarify
low confidence -> clarify / react_fallback / human_handoff
react_fallback -> max_steps <= 4
multihop -> max_hops <= 3
```

## 9. Definition of Done

完成前必须确认：

```text
1. bash init.sh 成功。
2. pytest -q 通过。
3. python evals/run_eval.py 能生成 eval_report.json。
4. API 能启动，/health 返回 ok。
5. /chat 对 FAQ、咨询、投诉、模糊、超范围问题均有合理输出。
6. data/tickets.jsonl 能看到工单。
7. logs/events.ndjson 能看到 trace。
8. README 能让助教按步骤跑起来。
```
