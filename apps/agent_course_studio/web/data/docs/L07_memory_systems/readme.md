# L07 记忆系统：让 Agent 越用越懂你

本章承接 L04 的会话记忆和 L05/L06 的检索能力，系统讲清 Agent 的记忆设计：短期记忆、长期记忆、外部知识、知识图谱、记忆检索策略和遗忘机制。

## 本章学习目标

- 理解 Agent 记忆三层架构：短期记忆、长期记忆、外部知识。
- 掌握短期记忆的滑动窗口和摘要压缩策略。
- 用 JSON 文件实现跨会话长期记忆。
- 理解向量记忆、知识图谱记忆和混合检索的差异。
- 把长期记忆封装为工具接入 LangChain Agent。
- 理解记忆遗忘：TTL、LRU/LFU、衰减、重要性、摘要压缩、去重和显式删除。
- 能说明记忆污染、隐私合规、跨用户隔离和记忆更新的一致性问题。

## 文件分区

| 分类 | 路径 | 用途 |
| --- | --- | --- |
| 讲义 | [lecture/LECTURE_FULL.md](./lecture/LECTURE_FULL.md) | 第 7 讲完整讲义 |
| 总结 | [lecture/CHAPTER_SUMMARY.md](./lecture/CHAPTER_SUMMARY.md) | 记忆架构、代码地图和复盘清单 |
| 课前准备 | [materials/PRECLASS_CHECKLIST.md](./materials/PRECLASS_CHECKLIST.md) | 环境、概念和预习检查 |
| 实操代码 | [practice/](./practice/) | 滑动窗口、摘要、JSON 记忆、图谱记忆、长期记忆 Agent |
| 一键脚本 | [practice/preclass_run.sh](./practice/preclass_run.sh) | 自动执行 L07 环境检查和核心示例 |
| 课堂笔记 | [materials/NOTES_TEMPLATE.md](./materials/NOTES_TEMPLATE.md) | 记录记忆策略、检索结果和遗忘设计 |
| 课后小测 | [materials/MINI_QUIZ.md](./materials/MINI_QUIZ.md) | 检查记忆系统核心概念 |
| 拓展练习 | [materials/EXTENSIONS.md](./materials/EXTENSIONS.md) | Chroma、遗忘 API、冲突合并、隐私治理 |
| 面试题库 | [materials/INTERVIEW_QA.md](./materials/INTERVIEW_QA.md) | Agent 记忆系统分难度题库、系统设计题和追问题 |
| 工程参考 | [resources/](./resources/) | 记忆架构、检索策略、遗忘机制、Chroma 可选实现 |
| 运行数据 | [data/](./data/) | JSON 记忆和知识图谱示例数据 |

## 推荐学习路径

1. 阅读 [materials/PRECLASS_CHECKLIST.md](./materials/PRECLASS_CHECKLIST.md)，确认 L04/L06 的 LangChain 环境可用。
2. 阅读 [lecture/LECTURE_FULL.md](./lecture/LECTURE_FULL.md) 的 7.1-7.2，理解短期记忆为什么会受上下文窗口限制。
3. 运行 `practice/21_memory_window.py`，观察滑动窗口如何丢失早期信息。
4. 运行 `practice/22_memory_summary.py`，观察摘要压缩如何保留早期关键信息。
5. 运行 `practice/23_long_term_memory_json.py --reset --query Python`，理解长期记忆的写入、搜索和持久化。
6. 运行 `practice/24_hybrid_memory_graph.py --reset --query Python --anchor 小明`，理解语义入口和知识图谱多跳扩展。
7. 阅读 [resources/MEMORY_FORGETTING.md](./resources/MEMORY_FORGETTING.md)，理解为什么长期记忆必须有遗忘机制。
8. 选择性运行 `practice/25_agent_with_long_memory.py --demo --reset`，观察 Agent 如何主动写入和读取长期记忆。
9. 阅读 [materials/INTERVIEW_QA.md](./materials/INTERVIEW_QA.md)，准备记忆系统面试题和系统设计题。
10. 完成 [materials/MINI_QUIZ.md](./materials/MINI_QUIZ.md)，再用 [lecture/CHAPTER_SUMMARY.md](./lecture/CHAPTER_SUMMARY.md) 复盘。

## 快速运行

从课程根目录激活环境：

```bash
source <course-root>/scripts/activate_course.sh
```

进入第七章目录：

```bash
cd <course-root>/lessons/L07_memory_systems
```

运行滑动窗口：

```bash
python practice/21_memory_window.py --max-turns 3
```

运行摘要压缩：

```bash
python practice/22_memory_summary.py
```

运行 JSON 长期记忆：

```bash
python practice/23_long_term_memory_json.py --reset --query Python
```

运行图谱混合记忆：

```bash
python practice/24_hybrid_memory_graph.py --reset --query Python --anchor 小明
```

一键预习检查：

```bash
bash practice/preclass_run.sh
```

通过标志：最后看到 `[OK] L07 preclass run completed.`。

## 本章实操说明

- `practice/memory_common.py`：公共路径、短期记忆、摘要、JSON 长期记忆、知识图谱和混合检索。
- `practice/21_memory_window.py`：滑动窗口短期记忆。
- `practice/22_memory_summary.py`：摘要压缩短期记忆，默认本地摘要，可用 `--use-llm` 调 LLM。
- `practice/23_long_term_memory_json.py`：JSON 长期记忆，支持 profile、facts、preferences、search、forget。
- `practice/24_hybrid_memory_graph.py`：标准库版“语义检索入口 + 知识图谱扩展”。
- `practice/25_agent_with_long_memory.py`：把长期记忆封装为工具接入 LangChain Agent。

## 本章交付物

- 一张 Agent 记忆三层架构图。
- 一次滑动窗口前后消息对比。
- 一次摘要压缩前后消息对比。
- 一个 JSON 长期记忆文件。
- 一个知识图谱多跳路径示例。
- 一个长期记忆 Agent 的两轮运行日志。
- 一份记忆遗忘策略设计：profile、preferences、facts、KG、隐私字段分别怎么处理。

## 与后续章节的关系

L07 解决 Agent 如何跨轮次、跨会话积累上下文。L08 的 Agent 模式需要判断哪些任务要共享或隔离记忆；L09 的 MCP 工具接入需要决定哪些外部系统成为可检索记忆；L10 的 Skill 设计需要明确哪些记忆能力可以模块化复用。
