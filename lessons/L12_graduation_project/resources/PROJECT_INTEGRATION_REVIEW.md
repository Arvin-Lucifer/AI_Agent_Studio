# L12 来源审阅与归档说明

## 一、来源目录

本次 L12 整理合并了两个外部目录：

| 来源 | 角色 | 归档位置 |
| --- | --- | --- |
| `<archived-source>/agent_course_2026_final/codex_customer_agent_packet` | 老师毕业项目任务包、Harness 要求、Codex 任务书和 Word 实战参考 | `resources/project_packet/` |
| `<archived-source>/intelligent_customer_agent` | 已完成的智能客服 Agent 参考实现 | `reference_implementation/intelligent_customer_agent/` |

## 二、任务包审阅结论

任务包明确要求第 12 讲选择：

```text
选题 A：智能客服 Agent
```

硬性要求包括：

- RAG 知识库，至少 10 份文档。
- LangGraph 流程编排。
- FastAPI 部署。
- 评测集和评测脚本。
- 支持多轮对话、意图识别、投诉工单、无法回答转人工。

Harness 工程要求强调：

- 状态持久化。
- 工具边界。
- 上下文管理。
- 反馈与验证。
- 机械化 guardrails。
- 可观测性。

## 三、参考实现审阅结论

参考实现已经覆盖核心验收项，并包含多项高分能力：

- FastAPI `/health`、`/chat`、`/metrics`、`/audit/{trace_id}`。
- 10 份 Markdown 知识库。
- LangGraph 状态机和条件路由。
- 意图分类、RAG、澄清、工单、人工兜底。
- 会话记忆、工单状态查询、多轮工单补充。
- 答案反馈、知识缺口、知识库运营和索引重建。
- 独立评测脚本、评测报告和 Dashboard 质量门禁。
- 前端聊天工作台和运营 Dashboard。
- Dockerfile、docker-compose、Makefile 和部署测试。
- Admin Key、限流、PII 脱敏和本地文件锁。

## 四、归档时保留的内容

参考实现保留：

- 源码：`intelligent_customer/`
- 知识库：`data/knowledge_base/`
- 项目文档：`docs/`
- 评测集和评测脚本：`evals/`
- 测试：`tests/`
- 前端：`web/`
- 部署文件：`Dockerfile`、`docker-compose.yml`、`Makefile`
- Harness 文件：`AGENTS.md`、`feature_list.json`、`progress.md`、`init.sh`
- 环境模板：`.env.example`

## 五、归档时排除的内容

为保证课程目录干净、可复现、无密钥风险，参考实现未复制：

- `.env`
- `.venv/`
- `.venv.no-pip.*/`
- `__pycache__/`
- `.pytest_cache/`
- `*.pyc`
- `logs/*`
- `data/*.lock`
- `evals/*.lock`
- 历史 `data/memory.json`
- 历史 `data/tickets.jsonl`
- 历史 `data/knowledge_gaps.jsonl`
- 生成索引 `data/kb_index.json`
- 生成草稿 `evals/generated_eval_cases.jsonl`

这些文件会在运行 `init.sh`、`scripts/build_kb.py`、`pytest` 或 `evals/run_eval.py` 时按需重新生成。

## 六、课程组织方式

L12 不把参考实现拆散到 `practice/`，而是保留为完整工程：

```text
reference_implementation/intelligent_customer_agent/
```

原因：

1. 这是一个完整项目，目录边界比普通章节练习更重要。
2. FastAPI、前端、Docker、测试和评测都依赖项目根目录。
3. 保留原工程结构更适合学生做答辩和二次开发。
4. L12 的 `practice/preclass_run.sh` 只负责调用参考实现的构建、测试和评测命令。

## 七、当前状态

L12 已从占位章节升级为完整毕业项目章节。当前完成：

- 老师任务包归档。
- Word 实战路线 Markdown 摘录。
- 智能客服 Agent 参考实现归档。
- L12 课程 README、讲义、材料和一键检查脚本补齐。

