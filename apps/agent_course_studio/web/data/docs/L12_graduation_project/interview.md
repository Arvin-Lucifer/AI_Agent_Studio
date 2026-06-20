# L12 面试速查：毕业项目智能客服 Agent

## 1. 你这个毕业项目一句话怎么介绍？

这是一个基于 LangGraph + RAG + FastAPI + Harness 工程实践的智能客服 Agent，支持知识库问答、多轮澄清、意图识别、投诉工单、无法回答转人工、评测脚本、可观测日志、前端客服台和运营 Dashboard。

## 2. 它和普通 RAG Demo 有什么区别？

普通 RAG Demo 通常只有“检索 -> 生成”。本项目有完整客服流程：

- 意图分类。
- 条件路由。
- 多轮记忆。
- 模糊澄清。
- 投诉工单。
- 无证据转人工。
- 评测和质量门禁。
- 可观测和审计回放。

所以它更接近一个生产系统，而不是一次性问答脚本。

## 3. 为什么用 LangGraph？

因为客服流程不是单链路，而是条件分支流程。LangGraph 可以显式表达状态、节点和条件边，例如：

```text
qa -> retrieve -> answer -> evaluate
complaint -> create_ticket
unclear -> clarify
out_of_scope -> human_handoff
```

这样更容易做测试、回放、兜底和后续扩展。

## 4. 你如何防止 Agent 编造答案？

核心策略是“无证据不答”：

- RAG 检索不到证据时转人工。
- 低置信度时澄清或转人工。
- 回答中保留 citation/source。
- 关键规则写进 guardrails 和条件路由，而不是只靠 prompt。
- 用评测集检查 fallback 行为。

## 5. 投诉为什么必须生成工单？

投诉是高风险业务意图，不能只靠自然语言安抚。生成工单可以带来：

- 可追踪。
- 可分派。
- 可设置优先级和 SLA。
- 可审计。
- 可被人工继续处理。

这体现了 Agent 从“聊天”走向“业务执行”。

## 6. Harness Engineering 在项目里体现在哪里？

体现在六类机制：

- 状态：`memory.json`、`tickets.jsonl`、`feature_list.json`、`progress.md`。
- 工具边界：kb search、ticket、memory、observability。
- 上下文：只注入必要证据和摘要。
- 验证：pytest 和独立 eval。
- 机械约束：投诉必工单、无证据不编造。
- 可观测：trace、events、metrics、audit。

## 7. 评测集怎么设计？

要覆盖真实业务分布：

- FAQ 问答。
- 咨询。
- 退款/发票/登录/套餐。
- 投诉。
- 模糊问题。
- 超范围问题。
- 多轮上下文。

指标包括 intent accuracy、route accuracy、ticket success rate、fallback accuracy、clarification accuracy、schema valid rate 等。

## 8. 为什么不能让 Agent 自己评估自己？

因为生成答案的 Agent 和评测器如果是同一个逻辑，很容易自我合理化。生产系统里应当让 evaluator 独立于主回答流程，用规则、金标样本或独立模型做验证。

## 9. 项目的最大工程亮点是什么？

可以从三个角度讲：

1. LangGraph 把客服流程显式状态化。
2. Harness 把关键风险写进代码约束和评测。
3. 可观测闭环让每次回答都能被 trace、审计和复盘。

## 10. 如果继续增强，你会做什么？

优先顺序：

1. 多跳 RAG：处理复杂组合问题。
2. ReAct 兜底：低置信度时有限步数工具推理。
3. MCP：把知识库检索和工单系统标准化开放。
4. Skill：沉淀 `multihop-rag`、`ticket-triage` 等可复用能力。
5. 线上评测：引入用户反馈和 bad case 回流。
