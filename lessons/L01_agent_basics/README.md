# L01 Agent 全景认知：从 ChatBot 到自主智能体

本章是课程入口，目标不是一开始就写复杂 Agent，而是建立一套稳定的判断框架：什么是 Agent、它和普通 ChatBot 差在哪里、一个最小 Agent 需要哪些模块，以及如何用 Python 跑通第一个 LLM 调用。

## 本章学习目标

- 能用一句话解释什么是 AI Agent。
- 能说清 ChatBot 与 Agent 的关键差异。
- 理解 Agent 的四个核心模块：LLM、Planning、Tools、Memory。
- 跑通第一个 LLM API 调用和一个多轮对话程序。
- 通过最小示例观察“聊天模式”和“智能体循环模式”的区别。

## 文件分区

| 分类 | 路径 | 用途 |
| --- | --- | --- |
| 讲义 | [lecture/LECTURE_FULL.md](./lecture/LECTURE_FULL.md) | 可直接授课或自学的完整讲义 |
| 总结 | [lecture/CHAPTER_SUMMARY.md](./lecture/CHAPTER_SUMMARY.md) | 本章关键概念、实操结果与复习清单 |
| 课前准备 | [materials/PRECLASS_CHECKLIST.md](./materials/PRECLASS_CHECKLIST.md) | 上课前需要完成的环境、概念和实操检查 |
| 实操代码 | [practice/](./practice/) | LLM 调用、多轮对话、ChatBot vs Agent 对比 |
| 一键脚本 | [practice/preclass_run.sh](./practice/preclass_run.sh) | 自动执行环境检查和非交互式实操 |
| 课堂笔记 | [materials/NOTES_TEMPLATE.md](./materials/NOTES_TEMPLATE.md) | 听课时记录概念、实验结果和疑问 |
| 课后小测 | [materials/MINI_QUIZ.md](./materials/MINI_QUIZ.md) | 检查核心概念是否掌握 |
| 拓展练习 | [materials/EXTENSIONS.md](./materials/EXTENSIONS.md) | 从入门到进阶的课后实践方向 |
| 注释规范 | [../../CODE_COMMENTING_GUIDE.md](../../CODE_COMMENTING_GUIDE.md) | 阅读和编写课程代码时遵循的讲解标准 |

## 推荐学习路径

1. 先看 [materials/PRECLASS_CHECKLIST.md](./materials/PRECLASS_CHECKLIST.md)，确认环境变量、依赖和 API 连通性。
2. 阅读 [lecture/LECTURE_FULL.md](./lecture/LECTURE_FULL.md) 的 1.1-1.4，建立 Agent 全景认知。
3. 阅读 [../../CODE_COMMENTING_GUIDE.md](../../CODE_COMMENTING_GUIDE.md)，了解课程代码里的关键注释会重点解释什么。
4. 运行 `practice/01_hello_llm.py`，确认能完成一次最小 LLM 调用。
5. 运行 `practice/02_multi_turn_chat.py`，观察 `messages` 如何形成最小上下文记忆。
6. 运行 `practice/demo_chatbot_vs_agent.py`，对比普通聊天和 Agent 循环。
7. 完成 [materials/MINI_QUIZ.md](./materials/MINI_QUIZ.md)，再用 [lecture/CHAPTER_SUMMARY.md](./lecture/CHAPTER_SUMMARY.md) 复盘。

## 快速运行

从课程根目录激活环境：

```bash
source <course-root>/scripts/activate_course.sh
```

进入第一章目录：

```bash
cd <course-root>/lessons/L01_agent_basics
```

运行最小 LLM 调用：

```bash
python practice/01_hello_llm.py
```

运行多轮对话：

```bash
python practice/02_multi_turn_chat.py
```

运行 ChatBot 与 Agent 对比示例：

```bash
python practice/demo_chatbot_vs_agent.py --mode both
```

一键预习检查：

```bash
bash practice/preclass_run.sh
```

通过标志：最后看到 `[OK] L01 preclass run completed.`。

## 本章实操说明

- `practice/01_hello_llm.py`：读取根目录 `.env`，发起一次最小 LLM 请求，让模型用一句话解释 AI Agent。
- `practice/02_multi_turn_chat.py`：维护 `messages` 列表，实现最小多轮记忆。
- `practice/demo_chatbot_vs_agent.py`：用模拟任务工具展示 Observe -> Think -> Act -> Reflect 的执行流程。

## 本章交付物

- 一句话定义 AI Agent。
- 一张 ChatBot 与 Agent 的差异表。
- 一次成功的 `practice/01_hello_llm.py` 运行结果。
- 一次多轮对话“记住名字”验证。
- 一个与你自己工作相关的 Agent 场景拆解：目标、所需工具、步骤、潜在失败点和护栏。

## 与后续章节的关系

L01 建立 Agent 全景认知；L02 会深入 Prompt 设计；L03 会进入函数调用和工具机制；后续章节会逐步补上框架、RAG、记忆、Agent 模式、MCP、Skill、评测部署和毕业项目。
