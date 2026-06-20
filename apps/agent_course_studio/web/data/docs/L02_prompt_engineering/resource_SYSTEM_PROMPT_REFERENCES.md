# L02 参考资源：System Prompt 案例与阅读路线

> 跨章节外部资源统一索引见：[教辅资料：外部学习资源索引](../../../teaching_support/EXTERNAL_LEARNING_RESOURCES.md)。
> GitHub stars 会持续变化，课堂以链接页面实时信息为准，不建议在作业中写死 star 数。
> 使用提醒：部分资源来自泄露、逆向工程或社区收集。课堂使用时建议学习结构和设计模式，不建议复制专有 prompt，不要用于绕过产品安全策略或提取他人系统提示。

## 一、真实产品 System Prompt 合集

这类仓库适合学习工业级 Agent 如何处理身份、工具调用、安全边界、多轮上下文和输出约束。

| 仓库 | 适合学习什么 |
| --- | --- |
| [x1xhlol/system-prompts-and-models-of-ai-tools](https://github.com/x1xhlol/system-prompts-and-models-of-ai-tools) | 覆盖 Cursor、Windsurf、Claude Code、v0、Manus、Lovable、Devin、Perplexity、Replit 等大量产品，是本章重点推荐阅读材料 |
| [asgeirtj/system_prompts_leaks](https://github.com/asgeirtj/system_prompts_leaks) | 按模型和产品整理主流系统提示，更新频繁，适合观察不同厂商的提示结构差异 |
| [dontriskit/awesome-ai-system-prompts](https://github.com/dontriskit/awesome-ai-system-prompts) | 不只收集 prompt，还包含真实案例分析和最佳实践总结 |
| [EliFuzz/awesome-system-prompts](https://github.com/EliFuzz/awesome-system-prompts) | 聚焦 AI coding agents，按平台和版本归档，适合学习编码助手的工具定义和版本管理 |

## 二、Prompt 工程教程与最佳实践

| 仓库 | 适合学习什么 |
| --- | --- |
| [ai-boost/awesome-prompts](https://github.com/ai-boost/awesome-prompts) | 收集大量角色与 Agent prompt，也包含 prompt attack/protect 和论文资源 |
| [promptslab/Awesome-Prompt-Engineering](https://github.com/promptslab/Awesome-Prompt-Engineering) | Prompt Engineering 论文、教程和工具链资源清单，适合作为延伸阅读 |
| [baz-scm/awesome-reviewers](https://github.com/baz-scm/awesome-reviewers) | 专注代码审查场景的 ready-to-use system prompts，和本章作业“代码 Review 助手”高度相关 |

## 三、ChatGPT 角色扮演与开发者 Prompt

| 仓库 | 适合学习什么 |
| --- | --- |
| [mustvlad/ChatGPT-System-Prompts](https://github.com/mustvlad/ChatGPT-System-Prompts) | 入门理解 System Prompt 的基本结构：角色、边界、输出格式 |
| [PickleBoxer/dev-chatgpt-prompts](https://github.com/PickleBoxer/dev-chatgpt-prompts) | 面向开发者的 ChatGPT prompt 集合，适合寻找小型任务模板 |

## 四、推荐学习路径

1. 入门：先看 [mustvlad/ChatGPT-System-Prompts](https://github.com/mustvlad/ChatGPT-System-Prompts)，理解 System Prompt 的基础结构。
2. 进阶：阅读 [x1xhlol/system-prompts-and-models-of-ai-tools](https://github.com/x1xhlol/system-prompts-and-models-of-ai-tools) 中 Cursor、v0、Claude Code、Manus 等产品案例。
3. 总结模式：精读 [dontriskit/awesome-ai-system-prompts](https://github.com/dontriskit/awesome-ai-system-prompts) 的最佳实践分析，关注以下六类模式：
   - 身份与角色设定（Identity & Persona）
   - 工具集成规范（Tool Integration）
   - 输出格式约束（Output Formatting）
   - 安全与边界控制（Safety Guardrails）
   - 错误恢复机制（Error Recovery）
   - 上下文管理（Context Management）
4. 实践：从 [ai-boost/awesome-prompts](https://github.com/ai-boost/awesome-prompts) 或 [baz-scm/awesome-reviewers](https://github.com/baz-scm/awesome-reviewers) 选一个模板，改造成自己的业务场景。

## 五、课堂阅读任务

任选一个真实产品 System Prompt，完成以下标注：

```text
仓库/产品：
适用场景：
角色定义：
能力边界：
工具调用规则：
输出格式：
安全护栏：
错误恢复：
上下文管理：
我能借鉴的一条设计：
我不会直接复制的一条内容：
```

## 六、重点推荐

优先阅读 [x1xhlol/system-prompts-and-models-of-ai-tools](https://github.com/x1xhlol/system-prompts-and-models-of-ai-tools)。它目前是同类主题里规模最大、覆盖面最广的资料之一，适合作为学生第一次接触真实产品 System Prompt 的主参考。
