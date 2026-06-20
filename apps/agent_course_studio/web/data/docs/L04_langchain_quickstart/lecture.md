# 第 4 讲：LangChain 快速上手 —— Agent 开发的瑞士军刀

## 4.1 为什么需要框架？

在第 3 讲中，我们手写了 Function Calling 的完整循环。它能跑，也很适合帮助学生理解底层机制，但工程上会逐渐暴露出重复劳动：

- 手动维护 `messages`。
- 手动解析模型返回的 `tool_calls`。
- 手动调用 Python 函数。
- 手动把工具结果带着 `tool_call_id` 塞回对话历史。
- 手动处理多轮、记忆、更多工具、错误恢复和日志。

LangChain/LangGraph 的价值，就是把这些常见 Agent 开发模式封装成可复用组件。你仍然要理解底层机制，但写业务时可以把精力放到工具设计、Prompt 设计、状态管理和效果评估上。

一个类比：

- 手写 Function Calling 像自己用砖头砌房子，所有承重结构都要自己管。
- LangChain 像使用预制构件，基础结构已经搭好，你重点决定房间如何分、门窗开在哪里、哪些地方需要加固。

## 4.2 LangChain 核心概念

LangChain 生态里概念很多，但入门阶段先抓住 5 个：

| 概念 | 一句话解释 | 对应 L03 手写代码 |
| --- | --- | --- |
| Model | 大语言模型调用封装 | `client.chat.completions.create(...)` |
| Prompt | 给模型的角色、任务、边界和输出约束 | `messages` 里的 system/user 内容 |
| Tools | Agent 可以调用的外部能力 | `get_weather`、`calculate` 等函数 |
| Memory | 对话或任务状态的保存机制 | 手动维护 `messages` 列表 |
| Agent | 把模型、工具、Prompt、记忆和循环串起来 | `run_agent()` 主循环 |

可以把 Agent 看成如下结构：

```text
┌──────────────────────────────────────┐
│              Agent                   │
│  一个能根据目标自主决策和行动的程序       │
│                                      │
│  ┌──────────┐  ┌──────────┐          │
│  │  Model   │  │  Tools   │          │
│  └──────────┘  └──────────┘          │
│  ┌──────────┐  ┌──────────┐          │
│  │  Prompt  │  │  Memory  │          │
│  └──────────┘  └──────────┘          │
└──────────────────────────────────────┘
```

## 4.3 安装与准备

课程已经把 LangChain 相关依赖放在根目录的 `requirements/langchain.txt`：

```bash
cd <course-root>
pip install -r requirements/langchain.txt
```

本章代码使用：

- `langchain-openai`：把 OpenAI 兼容接口封装成 LangChain 模型。
- `langchain-core`：提供 `@tool`、消息和基础抽象。
- `langchain.agents`：提供当前 LangChain 1.x 推荐的 `create_agent` 入口。
- `langgraph`：提供记忆检查点和底层 Agent 图执行能力。

注意：原始讲义示例中写死了 `gpt-4o-mini`，本课程代码统一从根目录 `.env` 读取 `OPENAI_MODEL`，这样可以跟你刚更新的模型配置保持一致。

## 4.4 用 LangChain 搭建一个 Agent

第 3 讲我们写了工具 schema、函数映射、循环、结果回填。现在可以用 `create_agent` 接管这些通用流程。当前 LangChain 1.x 的 Agent 入口更偏 LangChain 风格，底层仍然使用 LangGraph 的图执行与检查点能力。

本章基础示例在 [practice/07_langchain_agent.py](../practice/07_langchain_agent.py)。

核心代码结构如下：

```python
from langchain.agents import create_agent

from langchain_common import DEFAULT_TOOLS, build_llm, final_text

SYSTEM_PROMPT = "你是一个有用的助手，可以查天气、看时间、做计算。"

llm = build_llm()
agent = create_agent(
    model=llm,
    tools=DEFAULT_TOOLS,
    system_prompt=SYSTEM_PROMPT,
)

result = agent.invoke(
    {"messages": [{"role": "user", "content": "北京天气怎么样？适合跑步吗？"}]}
)
print(final_text(result))
```

对比一下：

| 维度 | L03 手写版 | L04 LangChain 版 |
| --- | --- | --- |
| 工具定义 | JSON Schema + 函数 + 映射字典 | `@tool` 装饰器自动生成工具说明 |
| 消息管理 | 手动维护 `messages` | 框架管理图状态中的消息 |
| 工具调用循环 | `while` 循环、解析 `tool_calls`、回填结果 | `create_agent` 内置 |
| 记忆 | 自己传历史消息 | `MemorySaver` + `thread_id` |
| 适合教学点 | 理解底层协议 | 快速搭建可用 Agent |

## 4.5 自定义工具的进阶写法

工具是 Agent 的“手脚”。LangChain 的 `@tool` 可以把普通函数转换成模型可调用的工具。

### 方式一：简单工具

```python
from langchain_core.tools import tool

@tool
def search_web(query: str) -> str:
    """在互联网上搜索信息。当需要查找最新资讯或事实性问题时使用。"""
    return f"搜索 {query} 的模拟结果..."
```

模型真正看到的是工具名、描述和参数 schema，而不是函数源码。

### 方式二：多个参数，用 Pydantic 定义输入结构

```python
from pydantic import BaseModel, Field
from langchain_core.tools import tool

class TranslateInput(BaseModel):
    text: str = Field(description="要翻译的文本")
    target_lang: str = Field(description="目标语言，如 English、Japanese、French")

@tool(args_schema=TranslateInput)
def translate(text: str, target_lang: str) -> str:
    """将文本翻译成指定目标语言。"""
    return f"[翻译成 {target_lang}] {text}"
```

Pydantic schema 的价值是让参数边界更清楚，尤其适合多参数工具、枚举参数、路径参数和业务对象参数。

### 方式三：带安全边界的复杂工具

比如文件读取工具不应该允许任意读取系统文件。本章 [practice/08_custom_tools.py](../practice/08_custom_tools.py) 里限制了：

- 只能读取课程目录下的文件。
- 只允许 `.txt` 和 `.md`。
- 内容过长会截断。
- 文件不存在或越界时返回明确错误。

这类约束非常重要，因为工具一旦接入真实文件、数据库、支付、邮件或工单系统，就不再只是“模型会不会调用”的问题，而是“调用错了会不会造成损失”的问题。

## 4.6 给 Agent 添加对话记忆

第 1 讲我们用 `messages` 列表实现最小多轮记忆。LangGraph 里可以用 `MemorySaver` 做检查点记忆：

```python
from langgraph.checkpoint.memory import MemorySaver
from langchain.agents import create_agent

memory = MemorySaver()

agent = create_agent(
    model=llm,
    tools=[get_weather],
    system_prompt="你是一个友好的助手。记住用户告诉你的所有信息。",
    checkpointer=memory,
)
```

调用时通过 `thread_id` 区分会话：

```python
agent.invoke(
    {"messages": [{"role": "user", "content": "我叫小明，我在北京工作"}]},
    config={"configurable": {"thread_id": "session_1"}},
)
```

关键点：

- 同一个 `thread_id` 会共享历史上下文。
- 不同 `thread_id` 彼此隔离。
- `MemorySaver` 是内存级检查点，进程结束后会丢失；生产系统需要 SQLite、Postgres、Redis 或其他持久化方案。

本章示例见 [practice/09_agent_with_memory.py](../practice/09_agent_with_memory.py)。

## 4.7 案例实战：智能搜索问答 Agent

搜索问答 Agent 的典型结构：

1. 用户提出问题。
2. Agent 判断是否需要搜索。
3. 需要时调用 `search_web(query)`。
4. 如果用户给 URL，则调用 `summarize_url(url)`。
5. 如果涉及计算，则调用 `calculate(expression)`。
6. 最后把工具结果整理成自然语言答案。

本章使用模拟搜索数据，避免课堂依赖外部搜索 API：

```python
@tool
def search_web(query: str) -> str:
    """搜索互联网获取信息。当需要查找不确定事实、最新信息或实时数据时使用。"""
    mock_results = {
        "AI": "AI Agent 正在从演示阶段进入更多实际工作流...",
        "Python": "Python 新版本持续改进性能、类型标注和开发体验...",
    }
    ...
```

完整代码见 [practice/10_search_agent.py](../practice/10_search_agent.py)。

这个示例要特别观察三个工程点：

- REPL 循环内需要 `try/except`，否则一次工具错误会让程序退出。
- `thread_id` 不应该永远写死，真实系统要用 `user_id:session_id`。
- 搜索结果是弱证据，回答时要区分“工具返回了什么”和“模型推断了什么”。

## 4.8 课后作业

必做：在搜索 Agent 基础上增加笔记工具。

1. `write_note(title, content)`：把信息保存为本地 Markdown 笔记。
2. `list_notes()`：列出已保存的笔记。
3. 实现“搜索信息 -> 保存笔记 -> 查看笔记”的完整流程。

选做：

- 接入真实搜索 API，例如 Tavily 或 SerpAPI，替换模拟搜索。
- 改为流式输出，让用户先看到工具调用过程，再看到最终回答。
- 给搜索 Agent 增加错误恢复、权限控制、日志记录和效果评估。

## 4.9 面试题：LangChain 是什么？

参考回答：

LangChain 是一个用于构建 LLM 应用的开发框架，主要帮助开发者把大模型与外部数据、工具、记忆、流程控制等能力结合起来。

它主要解决：

- LLM 调用封装。
- Prompt 管理。
- RAG 检索增强生成。
- Agent 工具调用。
- 多步骤链式任务编排。
- 对话记忆管理。
- 应用评估与可观测性。

## 4.10 面试题：LangChain 和 LangGraph 的区别？

一句话回答：

LangChain 更像“组件库 + 链式框架”，适合快速搭简单流程；LangGraph 是“图编排引擎”，专门解决有状态、循环、多分支、可持久化的复杂 Agent 工作流。两者同属一个生态，不是替代关系，而是互补关系。

具体对比见 [resources/LANGCHAIN_LANGGRAPH_COMPARISON.md](../resources/LANGCHAIN_LANGGRAPH_COMPARISON.md)。
