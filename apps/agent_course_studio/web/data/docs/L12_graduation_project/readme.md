# L12 毕业项目实战：智能客服 Agent

本章把前 11 讲的能力收束到一个端到端项目：**基于 LangGraph + RAG + FastAPI + Harness 工程实践的智能客服 Agent**。

它不是单轮 RAG Demo，而是一个可以运行、测试、评测、部署、演示和答辩的完整工程：知识库问答、多轮澄清、意图识别、投诉工单、无法回答转人工、可观测日志、质量门禁、前端客服台和运营 Dashboard。

## 本章学习目标

- 能把“需求 -> 技术方案 -> 测试设计 -> Harness 约束 -> 实现 -> 评测 -> 部署 -> 答辩”串成闭环。
- 理解毕业项目为什么选择智能客服 Agent，以及它如何覆盖 RAG、Memory、Agent 模式、评测部署和 Skill 思维。
- 掌握 LangGraph 状态机在真实项目中的节点拆分、条件路由、兜底和可观测设计。
- 能使用参考实现完成本地运行、自动测试、评测脚本、FastAPI 服务和前端展示。
- 能把项目亮点整理成答辩和面试表达。

## 文件分区

| 分类 | 路径 | 用途 |
| --- | --- | --- |
| 讲义 | [lecture/LECTURE_FULL.md](./lecture/LECTURE_FULL.md) | 毕业项目完整讲解：选题、验收、架构、实现路线和答辩 |
| 总结 | [lecture/CHAPTER_SUMMARY.md](./lecture/CHAPTER_SUMMARY.md) | 本章关键闭环、检查清单和答辩要点 |
| 任务包 | [resources/project_packet/](./resources/project_packet/) | 老师项目要求、Harness 指南、Codex 任务书、启动 Prompt 和 Word 原件 |
| 实战参考摘录 | [resources/project_packet/PRACTICE_REFERENCE_EXTRACT.md](./resources/project_packet/PRACTICE_REFERENCE_EXTRACT.md) | 从 `具体实战参考.docx` 抽取的可读 Markdown 路线 |
| 归档审阅 | [resources/PROJECT_INTEGRATION_REVIEW.md](./resources/PROJECT_INTEGRATION_REVIEW.md) | 两个来源目录的内容审阅、保留/排除策略和课程归档说明 |
| 参考实现 | [reference_implementation/intelligent_customer_agent/](./reference_implementation/intelligent_customer_agent/) | 可运行的智能客服 Agent 完整项目 |
| 课前准备 | [materials/PRECLASS_CHECKLIST.md](./materials/PRECLASS_CHECKLIST.md) | 环境、文档、命令和演示准备清单 |
| 课堂笔记 | [materials/NOTES_TEMPLATE.md](./materials/NOTES_TEMPLATE.md) | 记录需求、架构、评测、问题和答辩素材 |
| 课后小测 | [materials/MINI_QUIZ.md](./materials/MINI_QUIZ.md) | 检查毕业项目关键概念 |
| 拓展练习 | [materials/EXTENSIONS.md](./materials/EXTENSIONS.md) | 多跳 RAG、ReAct、MCP/Skill、监控和安全增强 |
| 面试速查 | [materials/INTERVIEW_QA.md](./materials/INTERVIEW_QA.md) | 项目答辩和 Agent 开发面试问答 |
| 一键检查 | [practice/preclass_run.sh](./practice/preclass_run.sh) | 构建知识库、运行测试和评测参考实现 |

## 推荐学习路径

1. 阅读 [resources/project_packet/01_ASSIGNMENT_REQUIREMENTS.md](./resources/project_packet/01_ASSIGNMENT_REQUIREMENTS.md)，确认老师硬性要求。
2. 阅读 [resources/project_packet/02_HARNESS_ENGINEERING_GUIDE.md](./resources/project_packet/02_HARNESS_ENGINEERING_GUIDE.md)，理解本项目为什么不能只靠 Prompt。
3. 阅读 [resources/project_packet/PRACTICE_REFERENCE_EXTRACT.md](./resources/project_packet/PRACTICE_REFERENCE_EXTRACT.md)，把 Word 实战路线转成 6 轮迭代计划。
4. 阅读 [lecture/LECTURE_FULL.md](./lecture/LECTURE_FULL.md)，理解毕业项目的架构和验收方式。
5. 进入 [reference_implementation/intelligent_customer_agent/](./reference_implementation/intelligent_customer_agent/) 阅读 `README.md`、`docs/PRD.md`、`docs/TRD.md`、`docs/TDD.md`、`docs/HARNESS.md`。
6. 运行 `bash practice/preclass_run.sh`，确认知识库构建、测试和评测可复现。
7. 启动参考实现，打开聊天页和 Dashboard 做演示。
8. 阅读 [materials/INTERVIEW_QA.md](./materials/INTERVIEW_QA.md)，把项目亮点整理成答辩话术。

## 快速运行

从课程根目录激活环境：

```bash
source <course-root>/scripts/activate_course.sh
```

进入 L12 目录：

```bash
cd <course-root>/lessons/L12_graduation_project
```

运行一键检查：

```bash
bash practice/preclass_run.sh
```

进入参考实现并启动服务：

```bash
cd reference_implementation/intelligent_customer_agent
python scripts/build_kb.py
bash scripts/run_api.sh
```

默认服务地址：

```text
http://127.0.0.1:8011
http://127.0.0.1:8011/web/dashboard.html
```

## 参考实现说明

参考实现保留了完整项目代码，但为了课程归档已经清理：

- 未复制 `.env`，只保留 `.env.example`。
- 未复制 `.venv`、`.pytest_cache`、`__pycache__`。
- 未复制运行日志、锁文件和历史会话/工单/知识缺口数据。
- 保留 `evals/eval_report.json` 作为已验证质量门禁结果；重新运行 `python evals/run_eval.py` 会更新它。

首次运行时，项目会按需生成：

```text
data/kb_index.json
data/memory.json
data/tickets.jsonl
data/knowledge_gaps.jsonl
logs/events.ndjson
logs/metrics.json
```

## 本章交付物

- 一份项目需求说明：选题、用户目标、范围和验收标准。
- 一份技术方案：LangGraph 流程、RAG 检索、记忆、工单、可观测、部署。
- 一份测试与评测设计：单元测试、接口测试、业务评测集和质量门禁。
- 一个可运行项目：FastAPI、RAG、LangGraph、前端页面、Dashboard。
- 一次完整验证记录：`pytest -q`、`python evals/run_eval.py`、API `/health` 和 `/chat`。
- 一份答辩稿：项目定位、架构亮点、困难与取舍、后续迭代。

## 与前面章节的关系

L12 是全课程收束：

- L02：System Prompt、结构化输出、Few-Shot/CoT。
- L03：Function Calling 和工具边界。
- L05：RAG、Hybrid Search、引用和知识库治理。
- L06：LangChain/LangGraph 编排。
- L07：会话记忆和上下文管理。
- L08：RAG + ReAct 的 Agent 模式选型。
- L09：MCP 工具生态作为可选加分项。
- L10：Skill、授权、安全、重试和工程边界。
- L11：评测、部署、监控、回滚和成本安全。

最终目标不是“代码能跑一次”，而是让 Agent 项目具备可复现、可评测、可追踪、可解释和可答辩的工程闭环。
