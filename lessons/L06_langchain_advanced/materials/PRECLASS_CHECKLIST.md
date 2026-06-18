# L06 课前准备清单

## 1. 环境检查

```bash
source <course-root>/scripts/activate_course.sh
cd <course-root>
python scripts/check_env.py
python scripts/smoke_openai.py
```

确认依赖：

- `langchain`
- `langchain-core`
- `langchain-openai`
- `langgraph`
- `pydantic`

## 2. 概念预习

- 复习 L04：`create_agent`、`@tool`、`MemorySaver`。
- 复习 L05：Retriever、chunk、RAG 检索链路。
- 阅读 [resources/LANGCHAIN_LAYERED_ARCHITECTURE.md](../resources/LANGCHAIN_LAYERED_ARCHITECTURE.md)。
- 阅读 [resources/LCEL_DATA_FLOW.md](../resources/LCEL_DATA_FLOW.md)。

## 3. 课前运行

```bash
cd <course-root>/lessons/L06_langchain_advanced
python practice/15_lcel_basics.py
python practice/17_output_parsers.py --mode json
```

## 4. 课前思考

- `prompt | llm | parser` 中每一步输出什么类型？
- 为什么结构化输出比自由文本更适合程序调用？
- 为什么复杂 Agent 一定需要 Callback 或 trace？
