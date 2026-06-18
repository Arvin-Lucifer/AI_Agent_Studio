# LCEL 管道数据流

LCEL 的核心表达是：

```python
chain = prompt | llm | output_parser
```

## 数据流

```text
{"role": "...", "question": "..."}
        │
        ▼
┌────────────────┐
│ Prompt          │
│ 填充模板变量     │
│ 生成 messages    │
└───────┬────────┘
        │ messages
        ▼
┌────────────────┐
│ LLM / ChatModel │
│ 调用模型生成回复  │
└───────┬────────┘
        │ AIMessage
        ▼
┌────────────────┐
│ OutputParser    │
│ 从消息中提取结果  │
└───────┬────────┘
        │ str / dict / Pydantic model
        ▼
最终结果
```

## 常见组合方式

| 方式 | 组件 | 用途 |
| --- | --- | --- |
| 顺序串联 | `a | b | c` | 一个步骤输出作为下一步输入 |
| 并行执行 | `RunnableParallel` | 同时跑多个子链 |
| 条件路由 | `RunnableBranch` | 根据输入选择不同链路 |
| 自定义转换 | `RunnableLambda` | 把普通 Python 函数接入链路 |

## 读代码时重点看

- 每个组件接收什么输入。
- 每个组件输出什么类型。
- 管道左右两端的类型是否能接上。
- 输出解析器把模型消息变成了什么结构。
