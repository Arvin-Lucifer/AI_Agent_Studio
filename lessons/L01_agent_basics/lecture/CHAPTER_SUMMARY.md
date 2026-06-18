# L01 章节总结：Agent 全景认知

## 一句话总结

AI Agent 是以 LLM 为核心，能够理解目标、规划步骤、调用工具、利用记忆并持续调整行为的智能程序。它和普通 ChatBot 最大的区别是：ChatBot 偏向回答问题，Agent 偏向完成任务。

## 核心概念

| 概念 | 本章理解 |
| --- | --- |
| LLM | Agent 的“大脑”，负责理解、推理和生成决策 |
| Planning | 把复杂目标拆成可执行步骤，降低任务失败率 |
| Tools | Agent 的“手脚”，连接搜索、计算、文件、API 等外部能力 |
| Memory | 保存上下文、历史结果和用户偏好，让 Agent 不只看当前一句话 |
| Agent Loop | Observe -> Think/Plan -> Act -> Reflect 的循环执行模式 |

## ChatBot 与 Agent 的关键差异

| 维度 | ChatBot | Agent |
| --- | --- | --- |
| 目标 | 回答用户问题 | 完成用户目标 |
| 行为方式 | 一问一答 | 可拆解任务并连续执行 |
| 外部能力 | 通常不调用工具 | 可以调用工具或系统接口 |
| 上下文 | 依赖当前对话 | 可结合短期记忆、长期记忆和任务状态 |
| 风险点 | 答错、幻觉、上下文遗忘 | 工具失败、循环失控、越权操作、成本不可控 |

## 本章实操复盘

1. `practice/01_hello_llm.py`
   - 目标：确认 `.env`、模型接口和最小请求链路可用。
   - 关键点：从课程根目录读取 `OPENAI_API_KEY`、`OPENAI_BASE_URL`、`OPENAI_MODEL`。

2. `practice/02_multi_turn_chat.py`
   - 目标：体验最小多轮记忆。
   - 关键点：每一轮用户和助手消息都被加入 `messages`，下一轮请求时模型能看到历史上下文。

3. `practice/demo_chatbot_vs_agent.py`
   - 目标：对比“直接回答”和“调用工具后再回答”的差异。
   - 关键点：Agent 模式会经历观察、思考、行动和复盘，并输出中间日志。

## 常见误区

- 误区一：会聊天就是 Agent。  
  修正：Agent 必须面向目标执行，通常还需要规划、工具和状态管理。

- 误区二：工具越多越智能。  
  修正：工具必须有清晰边界、参数约束、失败处理和调用记录。

- 误区三：多轮对话就是长期记忆。  
  修正：`messages` 只是最小短期上下文，真正长期记忆需要写入、检索、更新和清理策略。

- 误区四：Agent 可以完全自动执行。  
  修正：真实系统需要权限控制、人工确认、最大步数、超时和回退策略。

## 进入下一章前的检查

- 我能用一句话定义 AI Agent。
- 我能说出 ChatBot 与 Agent 至少 3 个差异。
- 我能解释 LLM、Planning、Tools、Memory 的作用。
- 我能跑通 `practice/01_hello_llm.py`。
- 我能用 `practice/02_multi_turn_chat.py` 解释最小记忆。
- 我能读懂 `practice/demo_chatbot_vs_agent.py` 输出中的 Observe、Think、Act、Reflect。

## 个人场景复盘模板

把一个真实任务改造成 Agent 流程时，建议这样写：

```text
任务目标：
输入信息：
需要的工具：
执行步骤：
可能失败的地方：
需要的护栏：
最终输出形式：
```
