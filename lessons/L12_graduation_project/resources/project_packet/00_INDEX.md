# Codex 项目资料包索引

这个资料包用于交给 Codex / GPT，让它快速理解毕业作业目标，并按 Harness 工程风格实现一个生产级 Agent 应用。

## 资料包包含什么

| 文件 | 用途 |
|---|---|
| `01_ASSIGNMENT_REQUIREMENTS.md` | 老师第 12 讲毕业项目主要求的 Markdown 整理版，明确三选一题目和本项目选择方向。 |
| `02_HARNESS_ENGINEERING_GUIDE.md` | Harness 工程实践指南的 Codex 可读整理版，强调状态、约束、反馈、评测和可观测性。 |
| `03_CODEX_TASK_BRIEF.md` | 给 Codex 的正式任务目标书：要做什么、怎么做、接口是什么、验收标准是什么。 |
| `04_CODEX_START_PROMPT.md` | 可直接复制给 Codex 的启动提示词。 |
| `AGENTS.md` | 建议放到目标仓库根目录，作为 Codex 的项目级长期规则。 |

## 还需要一起提供的文件

请把老师给的 Word 文档也一起提供给 Codex：

```text
具体实战参考.docx
```

这个 Word 文档不用转换成 Markdown，但它是实现蓝图，Codex 应该重点参考其中的多轮迭代路线：

```text
第 1 轮：PRD -> TRD -> TDD -> Harness，完成基础智能客服 Agent
第 2 轮：补齐前后端项目
第 3 轮：添加记忆系统、ReAct、多跳 RAG、分库索引和路由
第 4 轮：添加可观测数据和监控大盘
第 5 轮：抽取 MCP 和 Skill，作为可选加分项
第 6 轮：形成项目总结，用于答辩 / 面试表达
```

## 建议使用方式

把这些 Markdown 文件和 `具体实战参考.docx` 放到同一个新仓库或同一个 Codex 工作区里，然后对 Codex 说：

```text
请先阅读 00_INDEX.md、01_ASSIGNMENT_REQUIREMENTS.md、02_HARNESS_ENGINEERING_GUIDE.md、03_CODEX_TASK_BRIEF.md、AGENTS.md，以及老师的 具体实战参考.docx。然后按 03_CODEX_TASK_BRIEF.md 的要求，从零实现这个毕业项目。优先保证核心功能可运行、可测试、可评测，再做前端、监控大盘、ReAct、多跳 RAG、MCP/Skill 等增强项。
```

## 最终项目一句话目标

实现一个 **基于 LangGraph + RAG + FastAPI + Harness 工程实践的智能客服 Agent**，支持知识库问答、多轮澄清、意图识别、投诉工单、无法回答转人工、评测脚本和可观测日志。
