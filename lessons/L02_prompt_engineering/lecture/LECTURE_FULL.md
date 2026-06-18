# 第2讲讲义完整版：Prompt Engineering 进阶 —— Agent 的“灵魂”设计

适用对象：已经完成 L01，准备进入稳定可控 Agent 设计的同学  
学习时长：70-100 分钟（不含作业复盘）  
配套目录：`<course-root>/lessons/L02_prompt_engineering`
章节入口：`README.md`  
章节总结：`CHAPTER_SUMMARY.md`  
参考资源：`resources/SYSTEM_PROMPT_REFERENCES.md`

---

## 2.1 为什么 Prompt 是 Agent 的灵魂？

Agent 的行为本质来自 LLM 输出。  
LLM 输出什么，取决于 Prompt 怎么写。

所以 Prompt 质量，直接决定：

1. Agent 是否理解你的真实需求
2. Agent 是否遵守边界（不做越权行为）
3. Agent 输出是否稳定、可解析、可复用

三种核心 Prompt 类比：

| Prompt 类型 | 类比 | 作用 |
| --- | --- | --- |
| System Prompt | 员工岗位说明书 | 定义 Agent 是谁、能做什么、怎么做 |
| User Prompt | 老板具体指令 | 当前待完成任务 |
| Few-shot Examples | 新员工培训案例 | 用样例约束输出风格与格式 |

关键原则：Prompt 越具体、越明确，Agent 行为越稳定。

---

## 2.2 System Prompt 设计：给 Agent 写岗位说明书

### 设计框架

```text
1) 角色定义：你是谁
2) 能力边界：你能做什么、不能做什么
3) 行为准则：你应该怎么做
4) 输出格式：你必须按什么格式回答
5) 示例（可选）：给几组输入输出样例
```

### 案例：SQL 查询助手

```python
SYSTEM_PROMPT = """
## 角色
你是一个 SQL 查询助手，帮助用户将自然语言问题转换为 SQL 查询语句。

## 能力边界
- 你只处理 SELECT 查询，不执行任何 INSERT、UPDATE、DELETE 操作
- 你基于以下数据库表结构工作：
  - users 表：id, name, email, created_at
  - orders 表：id, user_id, product_name, amount, order_date
  - products 表：id, name, price, category

## 行为准则
1. 先理解用户想查什么数据
2. 如果问题模糊，先问清楚再写 SQL
3. 生成的 SQL 必须语法正确
4. 对复杂查询，先用简短中文解释思路，再给出 SQL

## 输出格式
请按以下格式输出：
**理解**：<一句话概括用户需求>
**SQL**：
<SQL 查询语句>
**说明**：<简要解释这个 SQL 做了什么>
"""
```

更多 System Prompt 案例请看：`resources/SYSTEM_PROMPT_REFERENCES.md`

### 真实产品 System Prompt 阅读方法

本章建议学生从真实产品 prompt 中学习结构，而不是照抄内容。阅读时重点标注六类信息：

1. 身份与角色设定（Identity & Persona）
2. 工具集成规范（Tool Integration）
3. 输出格式约束（Output Formatting）
4. 安全与边界控制（Safety Guardrails）
5. 错误恢复机制（Error Recovery）
6. 上下文管理（Context Management）

推荐优先阅读 `x1xhlol/system-prompts-and-models-of-ai-tools` 中 Cursor、v0、Claude Code、Manus 等产品案例；完整资源清单见 `resources/SYSTEM_PROMPT_REFERENCES.md`。

---

## 2.3 Prompt 设计模式

### 模式一：Few-shot（给例子）

当你希望模型按固定结构输出时，Few-shot 是最直接的稳定器。

```python
messages = [
    {"role": "system", "content": "你是一个情感分析助手，判断用户评论情感。"},
    {"role": "user", "content": "评论：这个产品太棒了，用起来很顺手！"},
    {"role": "assistant", "content": '{"sentiment":"正面","confidence":0.95,"keywords":["太棒了","顺手"]}'},
    {"role": "user", "content": "评论：快递太慢了，等了一周才到。"},
    {"role": "assistant", "content": '{"sentiment":"负面","confidence":0.88,"keywords":["太慢","等了一周"]}'},
    {"role": "user", "content": "评论：产品一般般，没有想象中的好，但价格还行。"},
]
```

### 模式二：CoT（Chain of Thought，分步思考）

示例：

```text
一个班有 30 个学生，其中 40% 是女生，女生中有 50% 戴眼镜，戴眼镜的女生有几个？
请一步一步思考，列出每一步计算过程，最后给出答案。
```

对于复杂推理题，分步提示通常能显著提高正确率。

### 模式三：ReAct（Reasoning + Acting）

Agent 常用执行范式：

```text
Thought: 用户问北京今天天气，我需要调用天气工具。
Action: search_weather(city="北京")
Observation: 晴，15-25C，空气质量良好。
Thought: 信息已足够，可以回答。
Answer: 北京今天天气晴朗，15-25C，适合户外活动。
```

这个模式会在第 3 讲 Function Calling 继续实操。

更多案例和阅读路线见：`resources/SYSTEM_PROMPT_REFERENCES.md`

### 课堂示例集

本章配套了一个可直接用于课堂演示的示例集：`resources/PROMPT_EXAMPLES.md`。其中包含：

1. Few-Shot：情感分类、结构化信息提取、代码生成、工具调用决策
2. CoT：数学推理、逻辑推理、多步骤任务规划、代码调试
3. Zero-Shot CoT：用“请一步一步思考”快速触发推理
4. 示例数量策略：不同任务需要多少 few-shot 示例

课堂建议：讲义正文只讲方法，示例集用于分组练习。每组选择一个示例，改写成自己的业务场景，并记录输出是否稳定。

---

## 2.4 结构化输出：让 Agent 回复可编程

下游程序通常需要 JSON，不是“看起来像 JSON 的文本”。  
所以我们要做两件事：

1. Prompt 里明确要求固定 JSON schema
2. 代码里加解析兜底与失败处理

本章对应脚本：`practice/03_structured_output.py`

运行：

```bash
cd <course-root>/lessons/L02_prompt_engineering
python practice/03_structured_output.py
```

脚本行为：

1. 给定中文会议文本
2. 要求模型输出 `people/locations/dates/summary`
3. 先 `json.loads` 直接解析
4. 失败时尝试提取 JSON 子串再解析

课堂思考：这种实现是否 100% 稳定？  
答案：不是。仍会受模型漂移、输出污染影响，所以第 2.5 和 2.6 的调试与迭代很关键。

---

## 2.5 Prompt 调试技巧（故障排查表）

| 问题 | 可能原因 | 解决方法 |
| --- | --- | --- |
| 输出格式不对 | 格式约束不够清楚 | 增加格式指令 + Few-shot 示例 |
| 回答太啰嗦 | 缺少长度约束 | 加“简洁回答，不超过 XX 字” |
| 不按角色说话 | 角色定义太弱 | 强化角色身份和行为规则 |
| 做了不该做的事 | 没有负向边界 | 明确“不要做 XXX” |
| 输出波动大 | temperature 过高 | 降到 0-0.3 之间 |

调试口诀：  
先控边界，再控格式，最后控稳定性。

---

## 2.6 实操：Prompt 迭代实验

本章对应脚本：`practice/04_prompt_iteration.py`

运行：

```bash
cd <course-root>/lessons/L02_prompt_engineering
python practice/04_prompt_iteration.py
```

脚本会做什么：

1. 准备同一组测试用例  
   - 写请假邮件  
   - 翻译请求（超出助手职责）  
   - 1+1（超出助手职责）
2. 用 V1 Prompt 测一遍（只有简单角色）
3. 用 V2 Prompt 测一遍（有职责边界 + 输出格式）
4. 对比两版差异

预期观察：

1. V1 更容易“什么都答”
2. V2 会对越界请求进行礼貌拒绝
3. V2 格式一致性更高

---

## 2.7 课后作业

### 必做

为“代码 Review 助手”设计 System Prompt，并做 3 个测试用例验证：

1. 输入含代码坏味道（冗余、命名差）
2. 输入存在明显 bug
3. 输入较高质量代码（看模型是否还能提出有效改进）

输出建议至少包含：

1. 发现的问题
2. 修改建议
3. 风险等级
4. 可选改进优先级

同时阅读 `resources/SYSTEM_PROMPT_REFERENCES.md` 中至少一个真实产品 prompt，完成以下标注：

1. 角色定义
2. 能力边界
3. 工具调用规则
4. 输出格式
5. 安全护栏
6. 上下文管理

### 选做

让模型稳定输出 JSON，连续测试 20 次，统计：

1. 一次解析成功率
2. 经过兜底解析后的成功率
3. 失败样本类型（格式错、字段缺失、额外文本污染）

### 进阶选做

选择 `resources/SYSTEM_PROMPT_REFERENCES.md` 中一个真实编码助手 prompt（例如 Claude Code、Cursor、v0 或 Manus），做 1-2 个点的原理解析：

1. 它如何定义自己的角色和能力边界？
2. 它如何描述工具调用规则？
3. 它如何处理安全边界、错误恢复或上下文管理？
4. 哪一条设计可以迁移到你自己的 Agent？

---

## 2.8 面试题与课堂讨论

Prompt Engineering 不只是“写得更顺”，更重要的是能解释为什么这样写、如何评估、如何控制成本和风险。以下问题适合课后复盘，也适合作为面试准备。

### Prompt 改写题

原 prompt：

```text
帮我总结这篇文章，越详细越好。
```

改写方向：

```text
你是一个研究助理。请阅读用户提供的文章，并按以下结构输出：
1. 一句话结论
2. 3-5 个核心观点
3. 关键证据或数据
4. 对目标读者的启发
5. 不确定或需要进一步核实的信息

要求：
- 总字数不超过 800 字
- 不要添加文章中没有的信息
- 如果原文缺少证据，请明确标注“原文未说明”
```

### 高频问题

1. Prompt 很好但 token 太贵，怎么优化？
   - 拆分长 prompt，把稳定规则放到可复用模板里。
   - 删除重复约束，保留最高优先级规则。
   - 用短 few-shot 替代长篇解释。
   - 对长上下文做摘要或检索，只放当前任务需要的信息。

2. 你如何评估一个 Prompt 的效果？
   - 使用固定测试集，覆盖正常、边界、越界、模糊输入。
   - 观察正确率、格式稳定性、越界率、幻觉率、成本和延迟。
   - 保留失败样本，形成 Prompt 回归集。

3. 怎么降低模型幻觉？
   - 明确禁止编造，要求标注不确定信息。
   - 对事实类任务接入检索或工具。
   - 要求引用来源或输出证据字段。
   - 对关键结论做二次校验。

4. Few-shot 示例是越多越好吗？怎么选样本？
   - 不是越多越好。示例过多会增加 token 成本，也可能引入冲突。
   - 优先选择覆盖关键边界的代表性样本。
   - 保持示例风格和目标输出一致。

5. CoT 一定能提升效果吗？什么时候反而有害？
   - CoT 对复杂推理有帮助，但对简单任务可能增加冗余。
   - 当任务需要简洁输出、隐私保护或低延迟时，暴露长推理反而不合适。
   - 生产环境可以要求“先分析再给结论”，但只输出简洁结论和必要依据。

6. JSON mode 还不稳定时怎么办？
   - 降低 temperature。
   - 增加 JSON schema 和 few-shot。
   - 增加解析、字段校验、自动重试和兜底提取。
   - 必要时使用模型/SDK 提供的结构化输出能力。

7. System prompt 很长，user prompt 也很长，怎么分配 token 预算？
   - System prompt 保留稳定规则和安全边界。
   - User prompt 保留当前任务目标和关键输入。
   - 历史上下文做摘要或检索。
   - 示例只保留最能影响输出的 1-3 个。

### 低分回答信号

- 只说“多试几个 prompt”，但没有测试集和指标。
- 只强调“写详细一点”，但不讲边界、格式和失败处理。
- 只看单次输出好不好，不做回归验证。
- 忽略成本、延迟、上下文长度和安全风险。

---

## 课后复盘模板（简版）

1. 我的最佳 Prompt 版本：
2. 我的最高频失败模式：
3. 我做了哪条边界约束后效果提升最大：
4. 我阅读真实产品 prompt 后最想借鉴的一条设计：
5. 下节课前我要保留的 1 条工程化经验：

---

## 一键检查命令

```bash
source <course-root>/use_proxy.sh
bash <course-root>/lessons/L02_prompt_engineering/practice/preclass_run.sh
```

通过标志：最后出现 `[OK] L02 preclass run completed.`
