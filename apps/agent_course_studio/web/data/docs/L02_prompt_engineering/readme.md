# L02 Prompt Engineering 进阶：System Prompt 与 Agent 行为设计

本章承接 L01 的 Agent 全景认知，进入“如何控制 Agent 行为”的核心问题。学生需要掌握 System Prompt 的结构、边界、输出格式、工具调用约束，并通过真实产品 prompt 案例学习工业级写法。

## 本章学习目标

- 理解为什么 Prompt 决定 Agent 的行为上限。
- 掌握 System Prompt 的岗位说明书写法。
- 学会三种关键模式：Few-shot、CoT、ReAct。
- 能让模型稳定输出可编程的 JSON 结构。
- 学会用测试用例迭代 Prompt 质量。
- 能阅读真实产品 System Prompt，并抽取可复用设计模式。

## 文件分区

| 分类 | 路径 | 用途 |
| --- | --- | --- |
| 讲义 | [lecture/LECTURE_FULL.md](./lecture/LECTURE_FULL.md) | 可直接授课或自学的完整讲义 |
| 总结 | [lecture/CHAPTER_SUMMARY.md](./lecture/CHAPTER_SUMMARY.md) | 本章关键概念、设计模式与复盘清单 |
| 参考资源 | [resources/SYSTEM_PROMPT_REFERENCES.md](./resources/SYSTEM_PROMPT_REFERENCES.md) | System Prompt GitHub 资源、阅读路线和安全提醒 |
| 外部教辅 | [../../teaching_support/EXTERNAL_LEARNING_RESOURCES.md](../../teaching_support/EXTERNAL_LEARNING_RESOURCES.md) | hello-agents、真实产品 prompt、Few-Shot/CoT、Claude.md 和 AI-native 工作方式 |
| 示例集 | [resources/PROMPT_EXAMPLES.md](./resources/PROMPT_EXAMPLES.md) | Few-Shot、CoT、工具调用决策和示例数量策略 |
| 课前准备 | [materials/PRECLASS_CHECKLIST.md](./materials/PRECLASS_CHECKLIST.md) | 上课前需要完成的环境、概念和实操检查 |
| 实操代码 | [practice/](./practice/) | 结构化输出与 Prompt 迭代实验 |
| 一键脚本 | [practice/preclass_run.sh](./practice/preclass_run.sh) | 自动执行环境检查和非交互式实操 |
| 课堂笔记 | [materials/NOTES_TEMPLATE.md](./materials/NOTES_TEMPLATE.md) | 听课时记录 Prompt 版本、实验结果和失败模式 |
| 课后小测 | [materials/MINI_QUIZ.md](./materials/MINI_QUIZ.md) | 检查核心概念是否掌握 |
| 拓展练习 | [materials/EXTENSIONS.md](./materials/EXTENSIONS.md) | Prompt 实验台、回归集和评估练习 |
| 面试速查 | [materials/INTERVIEW_QA.md](./materials/INTERVIEW_QA.md) | Prompt 改写、评估、幻觉、few-shot、CoT 和 JSON 稳定性 |
| 注释规范 | [../../CODE_COMMENTING_GUIDE.md](../../CODE_COMMENTING_GUIDE.md) | 阅读和编写课程代码时遵循的讲解标准 |

## 推荐学习路径

1. 先看 [materials/PRECLASS_CHECKLIST.md](./materials/PRECLASS_CHECKLIST.md)，确认 L01 环境仍然可用。
2. 阅读 [lecture/LECTURE_FULL.md](./lecture/LECTURE_FULL.md) 的 2.1-2.5，掌握 System Prompt 五要素。
3. 阅读 [resources/SYSTEM_PROMPT_REFERENCES.md](./resources/SYSTEM_PROMPT_REFERENCES.md)，选择 1-2 个真实产品 prompt 做结构标注。
4. 阅读 [../../teaching_support/EXTERNAL_LEARNING_RESOURCES.md](../../teaching_support/EXTERNAL_LEARNING_RESOURCES.md)，了解老师推荐的外部资料如何对应本章和后续章节。
5. 阅读 [resources/PROMPT_EXAMPLES.md](./resources/PROMPT_EXAMPLES.md)，选一个 Few-Shot 或 CoT 示例改写成自己的业务场景。
6. 阅读 [../../CODE_COMMENTING_GUIDE.md](../../CODE_COMMENTING_GUIDE.md)，了解结构化输出、解析兜底和测试代码的注释标准。
7. 运行 `practice/03_structured_output.py`，观察 JSON 输出和解析兜底。
8. 运行 `practice/04_prompt_iteration.py`，对比 V1/V2 Prompt 在边界和格式上的差异。
9. 阅读 [materials/INTERVIEW_QA.md](./materials/INTERVIEW_QA.md)，准备 Prompt Engineering 面试表达。
10. 完成 [materials/MINI_QUIZ.md](./materials/MINI_QUIZ.md)，再用 [lecture/CHAPTER_SUMMARY.md](./lecture/CHAPTER_SUMMARY.md) 复盘。

## 快速运行

从课程根目录激活环境：

```bash
source <course-root>/scripts/activate_course.sh
```

进入第二章目录：

```bash
cd <course-root>/lessons/L02_prompt_engineering
```

运行结构化输出实验：

```bash
python practice/03_structured_output.py
```

运行 Prompt 迭代实验：

```bash
python practice/04_prompt_iteration.py
```

一键预习检查：

```bash
bash practice/preclass_run.sh
```

通过标志：最后看到 `[OK] L02 preclass run completed.`。

## 本章实操说明

- `practice/03_structured_output.py`：让模型从文本中抽取 `people/locations/dates/summary`，并进行 JSON 解析兜底。
- `practice/04_prompt_iteration.py`：对比简单 Prompt 和带边界/格式约束 Prompt 的输出差异。
- `resources/SYSTEM_PROMPT_REFERENCES.md`：提供真实产品 System Prompt、Prompt 工程教程、角色/开发者 Prompt 的分层阅读路线。
- `resources/PROMPT_EXAMPLES.md`：提供 Few-Shot、CoT、Agent 规划和工具调用决策示例。

## 本章交付物

- 一版“代码 Review 助手”的 System Prompt。
- 三个测试用例：代码坏味道、明显 bug、高质量代码。
- 一次 `practice/03_structured_output.py` 的 JSON 输出记录。
- 一次 V1/V2 Prompt 对比记录，至少指出 2 个改进点。
- 一份真实产品 System Prompt 阅读笔记，标注角色、边界、工具、输出格式、安全护栏和上下文管理。
- 一份编码助手 prompt 原理解析，写出 1-2 个可迁移设计点。
- 一份 Few-Shot/CoT 示例改写作业，说明示例数量、覆盖边界和成本取舍。
- 一组面试题复盘：Prompt 改写、token 成本、评估方法、幻觉控制、few-shot 样本选择、CoT 边界、JSON 稳定性和上下文预算。

## 与后续章节的关系

L02 解决“如何让模型稳定按规则行动”；L03 会把这些规则接到函数调用和工具机制上；后续的 RAG、记忆、Agent 模式、MCP、Skill、评测部署，都需要稳定的 Prompt 规范作为底座。
