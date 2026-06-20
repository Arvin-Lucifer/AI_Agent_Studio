# L04 LangChain 快速上手：Agent 开发的瑞士军刀

本章承接 L03 的手写 Function Calling 循环，目标是让学生理解为什么需要 Agent 框架，以及如何用 LangChain/LangGraph 把模型、工具、Prompt、记忆和执行循环组合起来。

## 本章学习目标

- 理解 LangChain 主要解决什么重复劳动。
- 能把 L03 手写工具循环映射到 Model、Prompt、Tools、Memory、Agent 五个组件。
- 掌握 `@tool`、Pydantic 参数 schema、`create_agent` 的基础用法。
- 跑通一个能查天气、看时间、做计算的 LangChain Agent。
- 理解 `MemorySaver` 与 `thread_id` 如何支持多轮对话记忆。
- 能说清 LangChain 与 LangGraph 的区别和选型边界。

## 文件分区

| 分类 | 路径 | 用途 |
| --- | --- | --- |
| 讲义 | [lecture/LECTURE_FULL.md](./lecture/LECTURE_FULL.md) | 第 4 讲完整讲义 |
| 总结 | [lecture/CHAPTER_SUMMARY.md](./lecture/CHAPTER_SUMMARY.md) | 本章概念、代码结构与复盘清单 |
| 工程参考 | [resources/](./resources/) | 框架映射、LangChain/LangGraph 对比和搜索 Agent 工程化说明 |
| 课前准备 | [materials/PRECLASS_CHECKLIST.md](./materials/PRECLASS_CHECKLIST.md) | 环境、依赖和预习检查 |
| 实操代码 | [practice/](./practice/) | LangChain Agent、自定义工具、记忆、搜索问答示例 |
| 一键脚本 | [practice/preclass_run.sh](./practice/preclass_run.sh) | 自动执行 L04 环境检查和核心示例 |
| 课堂笔记 | [materials/NOTES_TEMPLATE.md](./materials/NOTES_TEMPLATE.md) | 记录框架组件、运行日志和疑问 |
| 课后小测 | [materials/MINI_QUIZ.md](./materials/MINI_QUIZ.md) | 检查核心概念和面试表达 |
| 拓展练习 | [materials/EXTENSIONS.md](./materials/EXTENSIONS.md) | 笔记工具、流式输出、真实搜索 API 和评估练习 |
| 面试速查 | [materials/INTERVIEW_QA.md](./materials/INTERVIEW_QA.md) | LangChain、LangGraph、工具、记忆和框架边界 |
| 注释规范 | [../../CODE_COMMENTING_GUIDE.md](../../CODE_COMMENTING_GUIDE.md) | 阅读和编写课程代码时遵循的讲解标准 |

## 推荐学习路径

1. 先看 [materials/PRECLASS_CHECKLIST.md](./materials/PRECLASS_CHECKLIST.md)，确认 `langchain`、`langchain-openai`、`langgraph` 已安装。
2. 阅读 [lecture/LECTURE_FULL.md](./lecture/LECTURE_FULL.md) 的 4.1-4.4，理解为什么从手写循环迁移到框架。
3. 运行 `practice/07_langchain_agent.py`，观察 `create_agent` 如何接管工具调用循环。
4. 阅读并运行 `practice/08_custom_tools.py --describe`，理解 `@tool` 和 Pydantic 参数 schema。
5. 运行 `practice/09_agent_with_memory.py --demo`，观察 `thread_id` 对多轮记忆的影响。
6. 运行 `practice/10_search_agent.py --question "请先搜索一下 AI Agent 有哪些典型应用？"`，理解搜索问答 Agent 的结构。
7. 阅读 [resources/LANGCHAIN_LANGGRAPH_COMPARISON.md](./resources/LANGCHAIN_LANGGRAPH_COMPARISON.md)，理解框架选型边界。
8. 阅读 [materials/INTERVIEW_QA.md](./materials/INTERVIEW_QA.md)，准备 LangChain/LangGraph 面试表达。
9. 完成 [materials/MINI_QUIZ.md](./materials/MINI_QUIZ.md)，再用 [lecture/CHAPTER_SUMMARY.md](./lecture/CHAPTER_SUMMARY.md) 复盘。

## 快速运行

从课程根目录激活环境：

```bash
source <course-root>/scripts/activate_course.sh
```

进入第四章目录：

```bash
cd <course-root>/lessons/L04_langchain_quickstart
```

查看自定义工具 schema：

```bash
python practice/08_custom_tools.py --describe
```

运行基础 LangChain Agent：

```bash
python practice/07_langchain_agent.py "北京天气怎么样？适合跑步吗？"
```

运行带记忆 Agent：

```bash
python practice/09_agent_with_memory.py --demo
```

运行搜索问答 Agent：

```bash
python practice/10_search_agent.py --question "请先搜索一下 Python 有哪些新变化？"
```

一键预习检查：

```bash
bash practice/preclass_run.sh
```

通过标志：最后看到 `[OK] L04 preclass run completed.`。

## 本章实操说明

- `practice/langchain_common.py`：公共环境加载、模型构造和基础工具，避免每个示例重复样板代码。
- `practice/07_langchain_agent.py`：用 `create_agent` 重写 L03 的天气、时间和计算 Agent。
- `practice/08_custom_tools.py`：展示简单工具、多参数工具、安全文件读取工具的写法。
- `practice/09_agent_with_memory.py`：用 `MemorySaver` 和 `thread_id` 区分不同会话记忆。
- `practice/10_search_agent.py`：用模拟搜索工具构建搜索问答 Agent，并加入 REPL 异常兜底。

## 本章交付物

- 一张 L03 手写代码到 LangChain 组件的映射表。
- 一次 `practice/07_langchain_agent.py` 的工具调用日志。
- 一个带 Pydantic 参数 schema 的自定义工具。
- 一次同一 `thread_id` 与不同 `thread_id` 的记忆对比结果。
- 一份 LangChain 与 LangGraph 选型说明。
- 一个“搜索信息 -> 保存笔记 -> 查看笔记”的课后扩展方案。

## 与后续章节的关系

L04 让学生快速使用框架搭建 Agent；L05 会把检索增强生成作为更系统的数据工具接入；L06 会继续深入 LangChain 分层架构、LCEL 管道、输出解析、自定义 Retriever 和 Callback 可观测性。
