# Agent 设计模式

AI Agent 的设计模式，本质是在回答一个问题：

> 当大模型不只是回答文本，而是要规划、调用工具、反思修正、多人协作时，系统应该如何组织执行过程？

这份教辅资料聚焦四种经典模式：

1. ReAct：边思考边行动。
2. Plan-and-Execute：先规划，再执行。
3. Reflection：先生成，再反思修正。
4. Multi-Agent：多个 Agent 分工协作。

一句话区分：

- ReAct 解决“边查边做”。
- Plan-and-Execute 解决“复杂任务先拆解”。
- Reflection 解决“做完检查和改进”。
- Multi-Agent 解决“多角色协作完成复杂任务”。

## 一、ReAct 模式

### 1. 核心思想

ReAct = Reasoning + Acting。

它让模型在任务执行过程中交替进行：

```text
Thought -> Action -> Observation -> Thought -> Action -> Observation -> Final Answer
```

也就是：

1. Thought：模型思考下一步要做什么。
2. Action：模型选择并调用工具。
3. Observation：系统把工具返回结果交给模型。
4. Final Answer：模型判断信息足够后输出最终答案。

ReAct 的关键不是“模型会思考”，而是：**模型可以基于工具反馈动态调整下一步动作。**

### 2. 典型流程

```text
用户输入
  -> LLM 判断是否需要工具
  -> 调用工具
  -> 读取工具返回
  -> 再次判断是否继续调用工具
  -> 输出最终答案
```

### 3. 适用场景

ReAct 适合路径不完全固定、但每一步可以通过工具获得反馈的任务：

- 实时信息查询。
- 搜索问答。
- 数据库查询。
- API 调用。
- 订单、物流、库存查询。
- 简单运维助手。
- 文件检索与摘要。

### 4. 案例：订单未发货原因查询

用户问题：

```text
帮我查一下订单 123456 为什么还没发货。
```

可用工具：

```text
get_order(order_id)
get_inventory(sku_id)
get_logistics(order_id)
```

执行过程：

```text
Thought: 需要先查询订单状态。
Action: get_order(order_id="123456")
Observation: 订单状态为待发货，SKU 为 A001。

Thought: 订单待发货，可能与库存或仓库处理有关，需要查询库存。
Action: get_inventory(sku_id="A001")
Observation: SKU A001 当前库存不足，预计明天补货。

Thought: 已经找到未发货原因，可以回答用户。
Final Answer: 订单 123456 尚未发货的原因是商品 A001 当前库存不足，预计明天补货后发出。
```

### 5. 优点

- 简单、通用，容易实现。
- 能动态调用工具。
- 可解释性相对较好，因为可以看到中间步骤。
- 适合“模型不知道，但工具知道”的问题。
- 适合边查边答、边执行边修正。

典型优势：

> ReAct 让 LLM 从“只会回答”变成“可以行动并根据反馈继续决策”。

### 6. 局限性

- 容易陷入循环：模型可能反复调用同一个工具，不知道何时停止。
- 工具调用不可控：可能调错工具、填错参数、多调或漏调。
- 长任务规划能力弱：更像“走一步看一步”，容易局部最优。
- 成本和延迟不稳定：每多一次工具调用，就多一次模型推理和工具耗时。
- 依赖工具描述质量：工具说明不清楚时，模型容易误用工具。

### 7. 调试技巧

- 限制最大迭代次数，例如 `max_iterations = 5`。
- 优化工具描述：工具名、用途、入参、返回值、适用边界都要清楚。
- 结构化工具返回，优先 JSON，而不是大段自然语言。
- 明确终止条件：信息足够时停止调用工具并输出最终答案。
- 记录 Trace：Thought、Action、Observation、参数、耗时和最终答案。
- 给工具增加可理解的错误提示，便于模型恢复。

工具描述示例：

```text
search_web(query: str): 当问题需要实时信息、外部网页信息或模型未知事实时使用。
输入应是简洁搜索关键词，返回相关网页标题、摘要和链接。
不适合用于数学计算。
```

## 二、Plan-and-Execute 模式

### 1. 核心思想

Plan-and-Execute 是先规划，再执行。

通常拆成两个角色：

- Planner：把用户目标拆解为可执行步骤。
- Executor：按照计划逐步执行，每一步可以调用工具或子链路。

典型流程：

```text
用户目标
  -> Planner 生成计划
  -> Executor 执行 Step 1
  -> Executor 执行 Step 2
  -> Executor 执行 Step 3
  -> 汇总最终结果
```

### 2. 适用场景

适合复杂、长链路、多步骤任务：

- 竞品调研。
- 研究报告。
- 课程设计。
- 数据分析。
- 自动化办公。
- 复杂代码生成。
- 项目规划。
- 多资料整合。

### 3. 案例：生成 Agent 课程大纲

用户任务：

```text
帮我设计一门 2 天的 AI Agent 开发训练营课程。
```

Planner 输出计划：

1. 明确目标学员画像和前置知识。
2. 设计课程目标和学习成果。
3. 拆分 Day 1：Agent 基础、Prompt、Tool Calling、ReAct。
4. 拆分 Day 2：RAG Agent、Plan-and-Execute、Reflection、Multi-Agent、工程化。
5. 设计实战项目和课后作业。
6. 输出完整课程大纲。

Executor 按步骤执行，最后汇总课程方案。

### 4. 案例：竞品调研报告

用户任务：

```text
调研 LangChain、LlamaIndex、AutoGen，并输出企业选型建议。
```

计划可以是：

1. 分别调研三个框架的核心定位。
2. 对比 RAG、Agent、多模型协作、生态成熟度、工程化能力。
3. 分析企业落地时的成本、风险和适用边界。
4. 输出对比表和选型建议。

如果只用 ReAct，容易查到哪算哪。Plan-and-Execute 能保证整体结构更完整。

### 5. 优点

- 全局结构清晰。
- 适合复杂长任务。
- 任务拆解能力强。
- 输出更完整、更有层次。
- 比纯 ReAct 更容易控制整体方向。

典型优势：

> Plan-and-Execute 把“我要完成什么”先变成“我应该分几步完成”。

### 6. 局限性

- 计划错误会放大：第一步计划错，后续执行可能整体跑偏。
- 计划粒度难控制：太粗没有指导意义，太细增加成本。
- 执行中变化适应不足：如果发现假设不成立，需要重新规划。
- 延迟较高：规划、执行、汇总通常需要多轮模型调用。
- 计划与执行可能脱节：Planner 写得好，不代表 Executor 能完成。

### 7. 调试技巧

- 让计划结构化，每一步包含 `task`、`expected_output`、`required_tool`、`success_criteria`。
- 加入 Plan Review：执行前检查计划是否覆盖用户目标、是否冗余、是否可执行。
- 支持 Re-plan：某一步失败或发现新信息时允许重新规划。
- 控制计划粒度，通常 3-7 步较适合教学和多数业务场景。
- 分离 Planner 和 Executor，不要让一个提示词同时承担所有职责。
- 每一步都要有明确产出，避免“调研一下”“分析一下”这种不可检查步骤。

结构化计划示例：

```json
{
  "goal": "输出企业级 Agent 框架对比报告",
  "steps": [
    {
      "id": 1,
      "task": "调研 LangChain 的核心能力和适用场景",
      "expected_output": "核心能力、生态成熟度、适用场景",
      "success_criteria": "至少覆盖 RAG、Agent、LangGraph、生态四个方面"
    },
    {
      "id": 2,
      "task": "调研 LlamaIndex 的核心能力和适用场景",
      "expected_output": "核心能力、生态成熟度、适用场景",
      "success_criteria": "至少覆盖数据连接、索引、RAG、企业应用四个方面"
    }
  ]
}
```

## 三、Reflection 模式

### 1. 核心思想

Reflection 是生成后自我检查、自我改进。

常见流程：

```text
Generate -> Reflect / Critique -> Revise -> Final Answer
```

也可以循环多轮：

```text
生成初稿 -> 反思问题 -> 修改 -> 再反思 -> 再修改 -> 最终输出
```

Reflection 的核心价值是让 Agent 不只“产出”，还要“检查产出是否满足要求”。

### 2. 适用场景

适合对质量要求高的任务：

- 代码生成。
- 代码审查。
- 技术方案设计。
- 长文写作。
- 文案润色。
- 复杂推理。
- 安全检查。
- 结构化输出校验。

### 3. 案例：代码生成与自检

用户任务：

```text
写一个 Python 函数，判断字符串是否是有效邮箱。
```

第一轮生成：

```python
def is_email(s):
    return "@" in s
```

Reflection：

```text
这个实现过于简单，只判断 @，不能校验用户名、域名、后缀，也没有处理空字符串和非字符串输入。
```

Revision：

```python
import re

def is_email(s: str) -> bool:
    if not isinstance(s, str):
        return False
    pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
    return re.match(pattern, s) is not None
```

### 4. 案例：技术方案评审

用户任务：

```text
设计一个企业知识库问答系统。
```

初稿：

```text
文档入库 -> 向量检索 -> LLM 回答
```

Reflection：

```text
方案缺少权限控制、增量更新、引用来源、评估体系、缓存、日志追踪和安全审计。
```

修订后：

```text
文档接入 -> 清洗 -> 切分 -> 权限绑定 -> 向量化
  -> 混合检索 -> Rerank -> Prompt 组装 -> LLM 生成
  -> 来源引用 -> 日志追踪 -> 反馈评估
```

### 5. 优点

- 能提升输出质量。
- 能发现遗漏点。
- 适合代码、方案、报告等高质量任务。
- 可以降低低级错误。
- 可作为其他 Agent 模式的质量检查环节。

典型优势：

> Reflection 相当于给 Agent 加了一道“自检”和“返工”机制。

### 6. 局限性

- 不保证一定更正确：模型可能反思错，甚至把正确答案改错。
- 容易变啰嗦：反思常倾向补充更多内容，导致答案失焦。
- 成本和延迟增加：至少多一次模型调用。
- 对事实性错误帮助有限：如果缺少外部事实，仅靠反思无法保证正确。
- 可能过度修改：修改时偏离用户原始需求。

### 7. 调试技巧

- 给 Critic 明确检查清单：正确性、边界条件、安全性、性能、可读性。
- 限制修改范围：只修复明确指出的问题，不添加无关功能。
- 设置最大反思轮数，通常 1-2 轮足够。
- 分离 Generator、Critic、Reviser。
- 要求批评有依据，避免泛泛而谈。
- 事实问题要接工具：涉及外部事实时，Reflection 应结合搜索、数据库或知识库。

代码检查清单示例：

```text
请从以下维度检查代码：
1. 是否满足需求。
2. 是否覆盖边界条件。
3. 是否有异常处理。
4. 是否存在安全问题。
5. 是否有明显性能问题。
6. 是否易读、易维护。
```

## 四、Multi-Agent 模式

### 1. 核心思想

Multi-Agent 是让多个 Agent 分工协作，每个 Agent 承担不同角色或能力。

典型结构：

```text
用户任务
  -> Planner Agent
  -> Researcher Agent
  -> Writer / Coder Agent
  -> Reviewer Agent
  -> Summarizer / Judge Agent
  -> 最终输出
```

它的本质是：**把复杂任务拆给多个具备不同职责的智能体协作完成。**

### 2. 常见形态

#### Supervisor-Worker

一个主管 Agent 调度多个 Worker Agent。

```text
Supervisor
├── Researcher
├── Analyst
├── Coder
└── Writer
```

适合企业级任务编排。

#### Debate

多个 Agent 从不同立场辩论，最后由 Judge 裁决。

```text
Agent A：支持方案一
Agent B：支持方案二
Judge：综合判断并输出结论
```

适合架构评审、方案论证、风险分析。

#### Writer-Critic

一个 Agent 生成，一个 Agent 审查。

```text
Writer -> Critic -> Writer -> Final
```

这是 Reflection 的多 Agent 版本。

#### Role-Based Collaboration

按真实团队角色拆分：

```text
产品经理 Agent
架构师 Agent
开发 Agent
测试 Agent
运维 Agent
```

适合模拟软件开发流程。

### 3. 适用场景

- 软件开发。
- 研究报告。
- 自动化办公。
- 架构评审。
- 复杂决策支持。
- 多角色内容生产。
- 企业级智能助手平台。

### 4. 案例：生成技术文章

用户任务：

```text
写一篇面向初学者的 LangChain Agent 教程。
```

多 Agent 分工：

- Planner Agent：设计文章大纲。
- Researcher Agent：补充资料和案例。
- Writer Agent：撰写正文。
- Reviewer Agent：检查准确性和可读性。
- Editor Agent：润色格式。

执行过程：

```text
用户任务
  -> Planner 生成大纲
  -> Researcher 补充知识点
  -> Writer 写初稿
  -> Reviewer 提修改意见
  -> Editor 输出最终文章
```

### 5. 案例：企业知识库架构评审

用户任务：

```text
企业知识库问答系统应该用纯向量检索，还是混合检索？
```

多 Agent 分工：

- Vector Advocate：支持纯向量检索，强调语义召回。
- Hybrid Advocate：支持混合检索，强调关键词、编号、人名、术语的精确匹配。
- Cost Analyst：分析成本和复杂度。
- Security Reviewer：分析权限控制和数据安全。
- Judge：综合裁决。

最终结论可能是：

> 生产环境建议优先采用混合检索 + Rerank。企业文档中存在大量专有名词、编号、条款、人名和系统名，仅靠向量检索容易漏召回；混合检索可以兼顾语义召回和精确匹配。

### 6. 优点

- 分工明确。
- 适合复杂任务。
- 可以模拟真实团队协作。
- 不同 Agent 可以使用不同工具、模型和提示词。
- 可以引入 Reviewer、Judge 等制衡机制。
- 更容易覆盖多视角问题。

典型优势：

> Multi-Agent 把一个“大而全”的 Agent 拆成多个“小而专”的 Agent。

### 7. 局限性

- 通信成本高：Agent 越多，中间消息越多，token 成本越高。
- 协作容易失控：可能重复工作、讨论过长、没有结论。
- 不一定优于单 Agent：简单任务使用 Multi-Agent 反而过度设计。
- 调试难度高：需要追踪每个 Agent 的输入、输出和责任边界。
- 最终汇总可能失真：Summarizer 可能遗漏或扭曲中间结论。

### 8. 调试技巧

- 明确每个 Agent 的职责边界。
- 限制通信轮数，例如最多讨论 3 轮，每个 Agent 每轮最多 5 条要点。
- 使用结构化消息传递，减少大段散文式沟通。
- 设置统一最终裁决者，由 Judge 或 Supervisor 输出最终答案。
- 避免过度多 Agent，简单任务优先使用单 Agent 或 Reflection。
- 记录每个 Agent 的 Trace，定位错误来源。

结构化消息示例：

```json
{
  "agent": "Researcher",
  "findings": [
    "LangChain 支持 Chain、Agent、RAG 等能力",
    "LangGraph 更适合复杂状态流"
  ],
  "uncertainties": [
    "具体版本 API 需要确认"
  ],
  "next_action": "交给 Writer 生成初稿"
}
```

## 五、四种模式对比

| 模式 | 核心思想 | 适合场景 | 主要优点 | 主要风险 | 调试重点 |
| --- | --- | --- | --- | --- | --- |
| ReAct | 边思考边行动 | 搜索、查询、工具调用 | 简单灵活，可动态使用工具 | 容易循环、工具调用不可控、局部最优 | 限制迭代次数、优化工具描述、记录 Trace |
| Plan-and-Execute | 先规划再执行 | 长任务、复杂任务、调研报告 | 全局结构清晰，任务拆解能力强 | 计划错误会放大，延迟较高 | 结构化计划、Plan Review、支持 Re-plan |
| Reflection | 生成后反思修正 | 代码、方案、写作、质量检查 | 能提升质量，发现遗漏点 | 可能反思错，答案变啰嗦 | 明确检查清单、限制修改范围、控制轮数 |
| Multi-Agent | 多角色协作 | 软件开发、复杂研究、架构评审 | 分工明确，多视角覆盖 | 通信成本高，调试复杂，汇总可能失真 | 明确职责边界、限制通信轮数、设置 Judge |

## 六、如何选择模式

### 1. 任务简单、流程固定

优先使用普通 Chain，不一定需要 Agent。

示例：

```text
把这段文本总结成 100 字。
```

### 2. 需要工具调用，但任务不复杂

优先使用 ReAct。

示例：

```text
查一下订单状态，并告诉用户原因。
```

### 3. 任务复杂，需要先拆步骤

优先使用 Plan-and-Execute。

示例：

```text
帮我做一份竞品调研报告。
```

### 4. 输出质量要求高

加入 Reflection。

示例：

```text
生成技术方案，并检查是否遗漏安全、权限、成本和可观测性设计。
```

### 5. 任务需要多角色协作

使用 Multi-Agent。

示例：

```text
模拟产品、架构、开发、测试、运维共同评审一个系统方案。
```

### 6. 生产系统建议

生产环境中通常不会只使用一种模式，而是组合使用：

```text
Router -> Planner -> ReAct Executor -> Reflection Reviewer -> Final Answer
```

或者：

```text
Supervisor -> 多个 Worker Agent -> Judge -> Final Answer
```

## 七、教学和面试使用建议

### 1. 课堂讲解顺序

建议按以下顺序讲：

1. ReAct：理解 Agent 为什么能调用工具。
2. Plan-and-Execute：理解复杂任务为什么要先规划。
3. Reflection：理解 Agent 如何自我检查和改进。
4. Multi-Agent：理解多个 Agent 如何协作。

这个顺序符合从简单到复杂的认知路径。

### 2. 面试题设计

基础题：

```text
请解释 ReAct、Plan-and-Execute、Reflection、Multi-Agent 四种 Agent 模式的区别。
```

场景题：

```text
如果要做一个企业知识库问答助手，你会选择哪种 Agent 模式？为什么？
```

工程题：

```text
ReAct Agent 在生产环境中容易出现哪些问题？你会如何调试？
```

架构题：

```text
如果要做一个能自动完成竞品调研报告的 Agent，你会如何设计？是否需要 Multi-Agent？
```

追问题：

- Plan-and-Execute 和 ReAct 的区别是什么？
- Reflection 是否一定能提升答案质量？
- Multi-Agent 是否一定比单 Agent 更强？

### 3. 学生回答模板

建议训练学生按这个结构回答：

1. 先定义模式。
2. 说明典型流程。
3. 给一个实际案例。
4. 讲适用场景。
5. 讲局限性。
6. 讲工程调试技巧。

### 4. 一句话记忆法

- ReAct：边想边做。
- Plan-and-Execute：先想清楚再做。
- Reflection：做完检查再改。
- Multi-Agent：多人分工协作。

## 八、结论

四种模式没有绝对优劣，关键是匹配任务复杂度和工程约束：

1. ReAct 适合工具调用和动态查询。
2. Plan-and-Execute 适合复杂长任务和结构化交付。
3. Reflection 适合提升输出质量和减少遗漏。
4. Multi-Agent 适合多角色、多视角、复杂协作任务。

生产实践中更常见的是组合模式，而不是单一模式。

例如：先用 Planner 拆任务，再用 ReAct Executor 调工具，最后用 Reflection Reviewer 检查结果；如果任务足够复杂，再引入 Multi-Agent 做分工协作。

## 延伸阅读

- Hello Agents：<https://github.com/datawhalechina/hello-agents/blob/main/docs/chapter4/%E7%AC%AC%E5%9B%9B%E7%AB%A0%20%E6%99%BA%E8%83%BD%E4%BD%93%E7%BB%8F%E5%85%B8%E8%8C%83%E5%BC%8F%E6%9E%84%E5%BB%BA.md>
