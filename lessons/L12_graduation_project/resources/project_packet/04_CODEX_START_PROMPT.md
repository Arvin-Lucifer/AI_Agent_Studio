# 可直接复制给 Codex 的启动 Prompt

下面这段可以直接复制给 Codex / GPT 作为项目启动提示。

---

请先阅读当前工作区中的以下文件：

```text
00_INDEX.md
01_ASSIGNMENT_REQUIREMENTS.md
02_HARNESS_ENGINEERING_GUIDE.md
03_CODEX_TASK_BRIEF.md
AGENTS.md
具体实战参考.docx
```

然后从零实现毕业项目：

```text
intelligent_customer_agent
```

项目目标是实现一个 **基于 LangGraph + RAG + FastAPI + Harness 工程实践的智能客服 Agent**。

必须满足老师第 12 讲主要求中的选题 A：

```text
1. 基于知识库回答产品 / 服务问题。
2. 支持多轮对话，能澄清模糊问题。
3. 识别用户意图：问答、投诉、咨询。
4. 无法回答时生成工单转人工。
5. RAG 知识库至少 10 份文档。
6. LangGraph 流程编排：意图分类 -> 路由 -> 处理。
7. FastAPI 部署。
8. 评测集 + 评测脚本。
```

同时尽量按照 Harness 工程风格实现：

```text
1. 使用 feature_list.json、progress.md、init.sh、AGENTS.md 做状态和启动管理。
2. 使用工具边界封装知识库检索、工单创建、记忆读写和日志记录。
3. 使用 guardrails 机械约束关键行为：投诉必走工单、无证据不编造、低置信度转人工。
4. 使用独立评测脚本，不让主 Agent 自评。
5. 记录 trace_id、events.ndjson、metrics，并提供 /metrics、/audit/{trace_id}。
6. 用 LangGraph 显式建模状态、节点和条件边。
```

请按 `03_CODEX_TASK_BRIEF.md` 的 Phase 0 -> Phase 7 顺序实现。优先保证：

```text
可运行 > 可测试 > 可评测 > 可观测 > 高级加分项
```

不要一开始就做所有高级功能。先完成核心闭环：

```text
FastAPI /chat
RAG 知识库
LangGraph 分类与路由
多轮 session 记忆
投诉工单
无法回答转人工
评测脚本
README
```

完成后请运行并修复：

```bash
bash init.sh
python scripts/build_kb.py
pytest -q
python evals/run_eval.py
uvicorn intelligent_customer.api:app --host 0.0.0.0 --port 8011 --reload
```

最终请确保 README 里有完整运行说明、接口示例、评测说明、项目结构说明和答辩亮点总结。
