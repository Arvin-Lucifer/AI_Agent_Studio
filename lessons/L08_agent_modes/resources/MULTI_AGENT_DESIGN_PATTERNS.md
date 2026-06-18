# 多 Agent 协作设计范式

## 1. Supervisor 模式

Supervisor 模式由一个主管调度多个专家 Agent。

```text
User
  -> Supervisor
      -> Researcher
      -> Analyst
      -> Writer
      -> Reviewer
  -> Final Answer
```

适合：

- 问题可能落到不同业务域。
- 需要动态选择工具或专家。
- 需要质量审核和返工。

风险：

- Supervisor 判断错会导致全局错误。
- 专家输出格式不稳定会影响后续节点。
- 如果返工条件不清晰，容易循环。

设计建议：

- Supervisor 输出结构化路由决策。
- 每个专家 Agent 的输入输出都固定。
- 所有循环都设置最大次数。

## 2. Sequential 模式

Sequential 模式是固定流水线。

```text
Input
  -> Step 1 Agent
  -> Step 2 Agent
  -> Step 3 Agent
  -> Output
```

适合：

- 流程天然固定。
- 每一步产物都是下一步输入。
- 对稳定性要求高于灵活性。

例子：

- 调研 -> 分析 -> 写作 -> 审核。
- 提取需求 -> 生成方案 -> 生成代码 -> 生成测试。
- 检索证据 -> 生成答案 -> 引用校验。

## 3. Peer 模式

Peer 模式中多个 Agent 平等地产生观点，再由汇总器整合。

```text
Question
  -> Agent A
  -> Agent B
  -> Agent C
  -> Aggregator
  -> Final Answer
```

适合：

- 创意发散。
- 方案比较。
- 复杂评审。

风险：

- 成本高。
- 输出冲突多。
- 讨论可能很长但收益有限。

生产系统中 Peer 模式通常要配合证据评分、投票规则或人工审核。

## 4. 本章 LangGraph 示例

`practice/26_supervisor_research_team.py` 是 Supervisor/Sequential 混合：

```text
START
  -> researcher
  -> analyst
  -> writer
  -> reviewer
  -> approved ? END : writer
```

每个节点只负责一个职责：

| 节点 | 读取字段 | 写入字段 |
| --- | --- | --- |
| researcher | topic | research_data |
| analyst | research_data | analysis |
| writer | topic, research_data, analysis, review_feedback | report |
| reviewer | report, revision_count | review_feedback, is_approved, revision_count |

这个设计的好处是：任何一步出错，都能通过 state 和 trace 快速定位。

## 5. 多 Agent 反模式

常见反模式：

- 角色只有名字不同，职责没有真正不同。
- 每个 Agent 都能调用所有工具。
- 没有统一状态协议，靠自然语言互相转述。
- 没有最大轮数，Reviewer 和 Writer 无限返工。
- 没有日志，只能看到最终答案，看不到中间决策。
- 把简单问答也放进多 Agent 流程，造成高延迟和高成本。

## 6. 最小可用设计模板

```text
任务目标:
输入:
输出:

Agent 列表:
  - name:
    responsibility:
    input_fields:
    output_fields:
    tools:
    failure_policy:

State Schema:
  - field:
    owner:
    meaning:

Control Flow:
  - start:
  - edges:
  - conditional_edges:
  - max_iterations:

Observability:
  - trace_id:
  - node_latency:
  - tool_calls:
  - citations:
  - errors:
```
