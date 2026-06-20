# L06 LangChain 深入：LCEL、Parser、Retriever 与 Callback

本章承接 L04 的 LangChain 快速上手和 L05 的 RAG，深入 LangChain 的核心抽象：分层架构、LCEL 管道、链组合、结构化输出、自定义 Retriever、Callback 观测，以及一个智能文档处理综合案例。

## 本章学习目标

- 理解 LangChain 分层架构：基础层、模型层、能力层、编排层、应用层。
- 掌握 LCEL 管道语法：`prompt | llm | output_parser`。
- 学会串联、并行、分支三类链组合方式。
- 使用 `PydanticOutputParser` 和 `JsonOutputParser` 获取结构化输出。
- 理解自定义 Retriever 的设计，尤其是关键词 + 语义/本地索引的融合思路。
- 使用 Callback 记录 chain、LLM、retriever、错误和耗时。
- 综合构建一个智能文档处理 Agent，输出摘要、关键词、行动项和结构化报告。

## 文件分区

| 分类 | 路径 | 用途 |
| --- | --- | --- |
| 讲义 | [lecture/LECTURE_FULL.md](./lecture/LECTURE_FULL.md) | 第 6 讲完整讲义 |
| 总结 | [lecture/CHAPTER_SUMMARY.md](./lecture/CHAPTER_SUMMARY.md) | 本章核心抽象、代码地图和复盘清单 |
| 工程参考 | [resources/](./resources/) | LangChain 分层、LCEL 数据流、Callback 能力清单 |
| 课前准备 | [materials/PRECLASS_CHECKLIST.md](./materials/PRECLASS_CHECKLIST.md) | 环境、概念和预习检查 |
| 实操代码 | [practice/](./practice/) | LCEL、Parser、Retriever、Callback、综合案例 |
| 一键脚本 | [practice/preclass_run.sh](./practice/preclass_run.sh) | 自动执行 L06 环境检查和核心示例 |
| 课堂笔记 | [materials/NOTES_TEMPLATE.md](./materials/NOTES_TEMPLATE.md) | 记录链路、输出结构、回调事件和失败点 |
| 课后小测 | [materials/MINI_QUIZ.md](./materials/MINI_QUIZ.md) | 检查核心概念和面试表达 |
| 拓展练习 | [materials/EXTENSIONS.md](./materials/EXTENSIONS.md) | 更复杂分支、日志持久化、成本统计、文档处理增强 |
| 面试速查 | [materials/INTERVIEW_QA.md](./materials/INTERVIEW_QA.md) | LCEL、Parser、Retriever、Callback 和文档处理案例 |
| 注释规范 | [../../CODE_COMMENTING_GUIDE.md](../../CODE_COMMENTING_GUIDE.md) | 阅读和编写课程代码时遵循的讲解标准 |

## 推荐学习路径

1. 阅读 [materials/PRECLASS_CHECKLIST.md](./materials/PRECLASS_CHECKLIST.md)，确认 L04/L05 的环境仍然可用。
2. 阅读 [resources/LANGCHAIN_LAYERED_ARCHITECTURE.md](./resources/LANGCHAIN_LAYERED_ARCHITECTURE.md)，建立分层框架图。
3. 运行 `practice/15_lcel_basics.py`，理解 `prompt | llm | parser` 的数据流。
4. 运行 `practice/16_lcel_composition.py`，观察串联、并行和条件分支。
5. 运行 `practice/17_output_parsers.py`，学习 Pydantic 和 JSON 两种结构化输出。
6. 运行 `practice/18_custom_retriever.py`，理解自定义 Retriever 和去重/融合排序。
7. 运行 `practice/19_callbacks.py`，观察 Callback 记录的链路事件。
8. 运行 `practice/20_doc_processor_agent.py`，完成智能文档处理综合案例。
9. 阅读 [materials/INTERVIEW_QA.md](./materials/INTERVIEW_QA.md)，准备 LangChain 深入面试表达。

## 快速运行

从课程根目录激活环境：

```bash
source <course-root>/scripts/activate_course.sh
```

进入第六章目录：

```bash
cd <course-root>/lessons/L06_langchain_advanced
```

运行 LCEL 基础：

```bash
python practice/15_lcel_basics.py
```

运行结构化输出：

```bash
python practice/17_output_parsers.py --mode pydantic
```

运行自定义 Retriever 静态演示：

```bash
python practice/18_custom_retriever.py --query "Python 装饰器怎么用？"
```

运行 Callback 监控：

```bash
python practice/19_callbacks.py
```

一键预习检查：

```bash
bash practice/preclass_run.sh
```

通过标志：最后看到 `[OK] L06 preclass run completed.`。

## 本章实操说明

- `practice/langchain_advanced_common.py`：统一模型构造、环境加载和示例文档。
- `practice/15_lcel_basics.py`：最小 LCEL 链。
- `practice/16_lcel_composition.py`：顺序链、并行链、条件分支。
- `practice/17_output_parsers.py`：Pydantic/JSON Output Parser。
- `practice/18_custom_retriever.py`：本地 Hybrid Retriever，避免依赖 Chroma。
- `practice/19_callbacks.py`：可观测回调处理器。
- `practice/20_doc_processor_agent.py`：并行子链 + 结构化解析 + 报告生成。

## 本章交付物

- 一张 LangChain 分层架构图。
- 一张 LCEL 数据流图。
- 一次 LCEL 基础链运行结果。
- 一个 Pydantic Output Parser 示例。
- 一个自定义 Retriever 去重/融合方案分析。
- 一次 Callback 事件日志。
- 一份智能文档处理报告。

## 与后续章节的关系

L06 是 LangChain 组件深入；L07 会进一步讲长期记忆和上下文管理；L08 会进入 Agent 模式和多 Agent 协作；L09 会进入 MCP 工具生态；L10 会把可复用能力沉淀为 Skill。
