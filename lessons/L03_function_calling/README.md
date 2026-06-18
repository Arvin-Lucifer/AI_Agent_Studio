# L03 Function Calling 核心机制：给 Agent 装上手脚

本章从“会回答”的 LLM 进入“能执行”的 Agent。学生需要理解 Function Calling 的工作流程、工具 schema 的设计方法、工具执行循环、并发工具调用，以及真实系统里工具选择、报错恢复和脏数据治理的问题。

## 本章学习目标

- 理解 Function Calling 是什么，以及模型和代码分别负责什么。
- 学会用 JSON Schema 定义工具名称、描述和参数。
- 跑通一个能查天气、看时间、做计算的最小工具型 Agent。
- 理解多个 tool calls 的串行与并发执行差异。
- 掌握工具数量变多时提升调用准确率的方法。
- 能处理工具执行失败、权限错误、空结果、噪声结果和多源冲突。

## 文件分区

| 分类 | 路径 | 用途 |
| --- | --- | --- |
| 讲义 | [lecture/LECTURE_FULL.md](./lecture/LECTURE_FULL.md) | 第 3 讲完整讲义 |
| 总结 | [lecture/CHAPTER_SUMMARY.md](./lecture/CHAPTER_SUMMARY.md) | 本章核心机制、工程要点和面试框架 |
| 课前准备 | [materials/PRECLASS_CHECKLIST.md](./materials/PRECLASS_CHECKLIST.md) | 环境、概念和实操检查 |
| 实操代码 | [practice/](./practice/) | 基础 Function Calling 与并发工具调用示例 |
| 一键脚本 | [practice/preclass_run.sh](./practice/preclass_run.sh) | 环境检查和 L03 非交互式实操 |
| 课堂笔记 | [materials/NOTES_TEMPLATE.md](./materials/NOTES_TEMPLATE.md) | 记录工具 schema、调用日志和错误恢复策略 |
| 课后小测 | [materials/MINI_QUIZ.md](./materials/MINI_QUIZ.md) | 检查核心概念和工程判断 |
| 拓展练习 | [materials/EXTENSIONS.md](./materials/EXTENSIONS.md) | 新工具、缓存、路由、鲁棒性和观测练习 |
| 面试速查 | [materials/INTERVIEW_QA.md](./materials/INTERVIEW_QA.md) | Function Calling 高频问题与回答框架 |
| 工程参考 | [resources/](./resources/) | 工具准确率、错误恢复、噪声治理三类专题 |
| 注释规范 | [../../CODE_COMMENTING_GUIDE.md](../../CODE_COMMENTING_GUIDE.md) | 阅读和编写课程代码时遵循的讲解标准 |

## 推荐学习路径

1. 阅读 [lecture/LECTURE_FULL.md](./lecture/LECTURE_FULL.md) 的 3.1-3.4，理解 Function Calling 基础流程。
2. 阅读 [../../CODE_COMMENTING_GUIDE.md](../../CODE_COMMENTING_GUIDE.md)，了解工具 schema、注册表、tool_call_id 和并发代码的注释标准。
3. 运行 `practice/05_function_calling.py`，观察模型如何选择工具和传参。
4. 运行 `practice/06_parallel_function_calling.py`，观察多个工具调用如何并发执行。
5. 阅读 [resources/TOOL_CALLING_ACCURACY.md](./resources/TOOL_CALLING_ACCURACY.md)，理解工具很多时如何提升选择准确率。
6. 阅读 [resources/TOOL_ERROR_RECOVERY.md](./resources/TOOL_ERROR_RECOVERY.md)，理解错误分类、有限重试、降级和 partial success。
7. 阅读 [resources/NOISY_TOOL_RESULTS.md](./resources/NOISY_TOOL_RESULTS.md)，理解工具返回不可靠时如何做 evidence processing。
8. 阅读 [materials/INTERVIEW_QA.md](./materials/INTERVIEW_QA.md)，准备工具调用面试回答。
9. 完成 [materials/MINI_QUIZ.md](./materials/MINI_QUIZ.md)，再用 [lecture/CHAPTER_SUMMARY.md](./lecture/CHAPTER_SUMMARY.md) 复盘。

## 快速运行

从课程根目录激活环境：

```bash
source <course-root>/scripts/activate_course.sh
```

进入第三章目录：

```bash
cd <course-root>/lessons/L03_function_calling
```

运行基础工具调用：

```bash
python practice/05_function_calling.py --demo
```

运行并发工具调用：

```bash
python practice/06_parallel_function_calling.py --demo
```

一键预习检查：

```bash
bash practice/preclass_run.sh
```

通过标志：最后看到 `[OK] L03 preclass run completed.`。

## 本章交付物

- 一个新增工具的 function schema。
- 一次基础 Function Calling 运行日志。
- 一次并发工具调用运行日志。
- 一份工具准确率优化方案：动态注入、工具边界、路由层、风险分级、指标评估。
- 一份错误恢复方案：错误分类、自动修复、有限重试、fallback、用户澄清、partial success。
- 一份噪声结果治理方案：清洗、过滤、归一化、rerank、交叉验证、证据约束。

## 与后续章节的关系

L03 是工具型 Agent 的基础。L04-L06 会把工具调用放进框架和状态图；L05 的 RAG 本质上也是一种检索工具；L07 之后的记忆、Agent 模式、MCP、Skill、评测部署都需要稳定的工具调用机制。
