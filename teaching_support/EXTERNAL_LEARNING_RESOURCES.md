# 外部学习资源索引：你能够额外获取到什么？

这份教辅资料用于统一收纳课程之外的延伸阅读链接。它的作用不是替代课程讲义，而是告诉学生：每个外部资源适合放在哪一章之后读、应该重点看什么、不要误用什么。

> 使用提醒：外部链接内容、访问权限和 GitHub stars 都会变化，课堂以链接页面实时信息为准。涉及真实产品 prompt 的资料，只建议学习结构、边界设计和工程模式，不建议复制专有 prompt，也不要用于绕过产品安全策略。

## 一、Agent 入门与经典范式

| 资源 | 适合章节 | 推荐看点 |
| --- | --- | --- |
| [datawhalechina/hello-agents](https://github.com/datawhalechina/hello-agents) | L01、L03、L08 | 从 Chatbot 到 Agent 的基础概念、经典范式、工具调用和案例结构 |

阅读建议：

1. 在 L01 之后先看 Agent 基础概念，建立“模型 + 工具 + 记忆 + 规划”的整体印象。
2. 在 L03 之后关注工具调用、函数调用和执行闭环。
3. 在 L08 之后回看 ReAct、Plan-and-Execute、Reflection、Multi-Agent 等模式，和本课程的 Agent 模式章节做对照。

## 二、真实产品 System Prompt

| 资源 | 适合章节 | 推荐看点 |
| --- | --- | --- |
| [x1xhlol/system-prompts-and-models-of-ai-tools](https://github.com/x1xhlol/system-prompts-and-models-of-ai-tools) | L02、L04、L06、L10 | 真实产品如何写身份设定、工具规则、上下文边界、安全约束和输出格式 |
| [dontriskit/awesome-ai-system-prompts](https://github.com/dontriskit/awesome-ai-system-prompts) | L02、L10、L11 | System Prompt 的优秀案例、设计原则和可复用结构 |

课堂使用方式：

1. 不要求学生背 prompt，而是拆解 prompt 的结构。
2. 标注角色定义、任务边界、工具调用规则、输出格式、安全护栏和错误恢复。
3. 对比不同产品：编码助手、搜索助手、网页生成工具、通用聊天工具的 prompt 重点并不一样。
4. 最后把其中一条设计模式改写进自己的业务场景。

建议标注模板：

```text
资源/产品：
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

## 三、Few-Shot 与 CoT 案例

| 资源 | 适合章节 | 推荐看点 |
| --- | --- | --- |
| [Few-shot & CoT 案例](https://docs.qq.com/doc/DSW1aaUdZaHJBdEJX?no_promotion=1&is_blank_or_template=blank) | L02 | 示例选择、示例数量、推理步骤、边界样本和输出格式控制 |

阅读建议：

1. 先判断案例属于 Few-Shot、CoT、Few-Shot + CoT 还是 Zero-Shot CoT。
2. 观察示例是否覆盖正例、反例、边界情况和容易混淆的输入。
3. 思考每个案例的成本：示例越多，token 成本越高；推理越长，延迟越高。
4. 把一个案例改写成本课程中的 Agent 场景，例如工具路由、结构化输出或面试题评估。

## 四、Claude.md、Skill 与协作规范

| 资源 | 适合章节 | 推荐看点 |
| --- | --- | --- |
| [70 行 CLAUDE.md](https://github.com/forrestchang/andrej-karpathy-skills/blob/main/CLAUDE.md) | L10、L11、L12 | 如何用很短的项目规则约束 coding agent 的工作方式 |
| [36Kr 翻译解读](https://36kr.com/p/3774954488349441) | L10、L11、L12 | 如何把 agent 规则写成团队协作规范，而不是临时聊天提示 |

课堂使用方式：

1. 把 CLAUDE.md 当作“项目级 system prompt”来读。
2. 关注规则是否足够短、足够明确、能否被 agent 每次执行。
3. 思考哪些内容应该进入仓库规则，哪些内容应该留在一次性 prompt。
4. L12 毕业项目可以要求学生提交自己的 `CLAUDE.md` 或 `AGENTS.md` 风格协作规则。

## 五、AI Native 工作方式

| 资源 | 适合章节 | 推荐看点 |
| --- | --- | --- |
| [大家都怎么用 AI 工作的](https://docs.qq.com/doc/DSVZhTW9kTWJDTUdv?no_promotion=1&is_blank_or_template=blank) | L10、L11、L12 | 团队如何把 AI 放进真实工作流，而不是只做单点工具 |
| [AI 工作方式补充资料](https://docs.qq.com/doc/DSVN5VmxGQ1B0eEZz) | L10、L11、L12 | 结合具体案例理解任务入口、上下文管理、验收机制和协作闭环 |
| [教辅资料：AI Native 的工作方式](./AI_NATIVE_WORKFLOW.md) | L10、L11、L12 | 本课程内已经整理好的 AI-native 工作方式讲义 |

阅读建议：

1. 重点看“任务如何被描述清楚”，而不是只看用了哪个工具。
2. 关注团队如何管理上下文、验收结果、沉淀可复用 skill。
3. 对照 L10：哪些工作可以沉淀成 Skill，哪些只能是临时任务。
4. 对照 L11：哪些 AI 工作流需要评测、监控、灰度和回滚。

## 六、推荐阅读路线

1. L01 后：读 [hello-agents](https://github.com/datawhalechina/hello-agents)，建立 Agent 全局概念。
2. L02 后：读真实产品 System Prompt 资料和 Few-Shot/CoT 案例，学习提示词结构化设计。
3. L03-L04 后：回看 hello-agents 中工具调用和 Agent 框架相关内容。
4. L08 后：结合 [Agent 设计模式](./AGENT_DESIGN_PATTERNS.md) 对照 ReAct、Plan-and-Execute、Reflection、Multi-Agent。
5. L10 后：读 70 行 CLAUDE.md 和 AI 工作方式资料，理解 Skill、项目规则和组织工作流。
6. L11-L12 后：把外部资料转成自己的项目规范、评测清单、部署策略和答辩材料。

## 七、课堂使用原则

1. 外部资源用于“扩展视野”，课程交付仍以本仓库每章 README、讲义、实践代码和作业为准。
2. 真实产品 prompt 只学结构，不复制专有内容，不做 prompt 泄露或绕过安全策略的练习。
3. 腾讯文档类资源可能需要登录或权限，课前需要老师确认访问是否正常。
4. GitHub 仓库内容更新很快，引用时不要在作业中写死 star 数、文件行号或非稳定路径。
5. 每次阅读外部资料，都要产出一个自己的改写版本：Prompt 模板、Skill 规范、评测表、项目规则或架构图。
