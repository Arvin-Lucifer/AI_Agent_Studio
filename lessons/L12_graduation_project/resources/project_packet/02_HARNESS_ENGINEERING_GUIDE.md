# Harness 工程实践指南整理版

本文件用于把老师要求参考的 Harness 工程实践，整理成 Codex 可以直接执行的项目工程规范。

## 1. 核心思想

Harness Engineering 的核心不是“写更长的 prompt”，而是给 AI Agent 搭建一套工程系统，使它具备：

```text
状态持久化
工具边界
上下文管理
反馈循环
验证守护
机械约束
可观测性
持续迭代能力
```

一句话总结：

```text
不要只靠 prompt 让 Agent 听话，而要用工程系统让正确行为更容易发生、错误行为更难发生。
```

在毕业项目里，这意味着不能只做：

```text
用户问题 -> LLM 直接回答
```

而要做成：

```text
任务状态 -> LangGraph 工作流 -> 工具调用 -> 验证器 -> 日志 / 评测 -> 失败兜底
```

---

## 2. Harness 与 Prompt / Context / Framework 的关系

可以用三层理解：

| 层级 | 关注点 | 例子 |
|---|---|---|
| Prompt Engineering | 怎么说清楚 | system prompt、few-shot 示例、输出格式要求 |
| Context Engineering | 给模型看什么 | 知识库片段、会话摘要、短规则、按需加载上下文 |
| Harness Engineering | 系统如何约束、测量和修复 Agent 行为 | 工具权限、状态文件、验证器、日志、测试、Hook、工作流 |

在本项目中：

```text
Prompt 负责局部生成质量。
Context 负责控制输入信息质量。
Harness 负责端到端工程可靠性。
```

---

## 3. Harness 的六层架构

### 3.1 第一层：持久状态

LLM 调用本身是无状态的，因此项目必须有外部状态文件。

在本毕业项目中应落实为：

```text
feature_list.json       # 功能清单和完成状态
progress.md             # 每次开发 / 运行 / 评测进度记录
init.sh                 # 一键初始化环境
AGENTS.md               # 给 Codex 的项目规则
.env.example            # 环境变量模板
logs/                   # 运行日志
```

`feature_list.json` 推荐格式：

```json
[
  {
    "id": "F001",
    "category": "core",
    "description": "实现 FastAPI /chat 接口",
    "passes": false,
    "check": "pytest tests/test_api.py"
  }
]
```

要求：

```text
1. 每个功能应有明确验收方式。
2. Codex 每完成一项，应更新 passes 字段或在 progress.md 记录原因。
3. 不允许只口头说“完成了”，必须能跑测试或评测验证。
```

---

### 3.2 第二层：执行环境

Agent 不能只有文本输出，还要有可控工具。对于智能客服 Agent，工具应当边界清晰。

推荐工具：

```text
kb_search(query, collections, k)       # 只能检索知识库
create_ticket(payload)                 # 只能创建工单
load_memory(session_id)                # 读取会话记忆
save_memory(session_id, messages)      # 写入会话记忆
log_event(trace_id, event, fields)     # 记录可观测事件
run_eval()                             # 运行评测
```

工具边界要求：

```text
1. 工具输入输出必须结构化，优先使用 Pydantic schema。
2. 不允许在工具里隐藏复杂副作用。
3. 不允许硬编码 API Key。
4. 文件写入必须限制在项目目录下。
5. 工单、记忆、日志都应有明确存储位置。
```

---

### 3.3 第三层：上下文工程

上下文不是越多越好，噪声会污染推理。

本项目的上下文注入策略：

| 类型 | 是否注入 prompt | 说明 |
|---|---|---|
| Agent 角色和输出格式 | 始终注入 | 简短、稳定。 |
| 当前用户问题 | 始终注入 | 核心输入。 |
| 最近会话摘要 | 按需注入 | 避免把所有历史对话塞进去。 |
| RAG top-k 片段 | 按需注入 | 只注入检索命中的片段。 |
| 全量知识库 | 不注入 | 应通过检索工具获取。 |
| 全量日志 | 不注入 | 日志用于可观测，不进入普通问答 prompt。 |
| 评测历史 | 不注入 | 防止污染答案。 |

原则：

```text
1. prompt 应短小、结构化。
2. 知识只通过 RAG top-k 注入。
3. 多轮历史应摘要化。
4. 复杂规则尽量写成代码 guardrail，而不是塞进 prompt。
```

---

### 3.4 第四层：反馈与验证

不要让生成答案的 Agent 自己判断“我答得很好”。

本项目应至少提供三类验证：

```text
L0：代码级验证
- lint / typecheck / import check
- pytest 单元测试

L1：接口级验证
- FastAPI /health
- FastAPI /chat
- 工单接口
- 评测脚本能运行

L2：业务级验证
- 意图分类是否正确
- RAG 回答是否有证据
- 投诉是否生成工单
- 无法回答是否转人工
- 模糊问题是否澄清
```

评测脚本推荐输出：

```json
{
  "total": 30,
  "intent_accuracy": 0.90,
  "ticket_success_rate": 1.00,
  "fallback_accuracy": 0.88,
  "clarification_accuracy": 0.85,
  "schema_valid_rate": 1.00,
  "overall_score": 0.91
}
```

关键要求：

```text
Evaluator 必须独立于主回答流程。
主 Agent 负责生成，Evaluator 负责验收。
```

---

### 3.5 第五层：机械化约束

写在文档里的规则只是建议，写在代码里的约束才是法律。

本项目必须机械执行这些约束：

```text
1. complaint 意图必须进入 create_ticket 节点。
2. 没有检索证据时，不能编造产品 / 政策答案。
3. 低置信度回答必须澄清或转人工。
4. out_of_scope 问题必须转人工或礼貌拒答。
5. FastAPI 响应必须符合统一 schema。
6. 所有请求必须生成 trace_id。
7. ReAct / 修复循环 / 多跳循环必须有最大轮数。
```

可以用以下方式实现：

```text
guardrails.py
router.py
Pydantic schema
LangGraph conditional edge
pytest 测试
评测脚本
```

---

### 3.6 第六层：编排

本项目应使用 LangGraph 作为核心编排，而不是普通 if-else 直接串起来。

推荐主流程：

```text
START
  -> load_memory
  -> classify_intent
  -> route_by_intent
      -> qa / consult: retrieve_docs -> generate_answer -> evaluate_answer
      -> complaint: collect_ticket_info -> create_ticket
      -> unclear: ask_clarifying_question
      -> out_of_scope / low_confidence: human_handoff
  -> save_memory
  -> log_metrics
  -> END
```

如果实现增强项，可扩展为：

```text
retrieve_docs
  -> maybe_multihop
  -> generate_answer
  -> evaluate_answer
  -> if low confidence: react_fallback
  -> if still failed: create_ticket / human_handoff
```

---

## 4. Harness 思想如何映射到智能客服 Agent

| Harness 能力 | 在智能客服项目中的落地 |
|---|---|
| 持久状态 | `feature_list.json`、`progress.md`、`data/memory.json`、`data/tickets.jsonl`。 |
| 工具编排 | RAG 检索工具、工单工具、记忆工具、日志工具。 |
| 上下文管理 | 只注入当前问题、会话摘要、检索证据，不注入全量知识库。 |
| 反馈循环 | `evals/run_eval.py`、`tests/`、回答置信度评估。 |
| 验证守护 | 投诉强制工单、低置信度兜底、无证据不编造。 |
| 可观测性 | `trace_id`、`logs/events.ndjson`、`/metrics`、`/audit/{trace_id}`。 |
| 编排 | LangGraph 节点和条件边。 |

---

## 5. 本项目必须避免的反模式

Codex 实现时要特别避免：

```text
1. 只写一个巨大 prompt，没有工程约束。
2. 只做 notebook 或命令行 demo，没有 FastAPI。
3. 只做单轮 RAG，不支持 session。
4. 自称完成，但没有测试和评测脚本。
5. 单元测试通过，但 API 启动失败。
6. 投诉类问题被当成普通问答回答。
7. 知识库查不到时编造答案。
8. ReAct / 多跳循环没有最大轮数。
9. 所有文档都塞进 prompt，导致上下文污染。
10. API Key 写死在代码里。
```

---

## 6. 推荐最小 Harness 升级路径

如果时间有限，按这个顺序实现：

```text
1. 先做 core MVP：RAG + LangGraph + FastAPI + 工单 + 评测。
2. 再补 Harness 文件：feature_list.json、progress.md、init.sh、AGENTS.md。
3. 再补 guardrails：低置信度、无证据、投诉强制工单。
4. 再补 observability：events.ndjson、metrics、trace_id。
5. 再补前端聊天页面。
6. 最后做 ReAct、多跳 RAG、MCP/Skill。
```

优先级原则：

```text
可运行 > 可评测 > 可观测 > 高级炫技。
```
