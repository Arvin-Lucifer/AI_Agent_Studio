# 搜索问答 Agent 工程化补充

## 1. 当前 demo 的边界

`practice/10_search_agent.py` 使用模拟搜索数据，适合课堂解释工具调用流程，但不代表真实搜索系统已经完成。

主要边界：

- 搜索结果是 mock 数据，不保证时效性。
- 没有网页抓取和正文抽取。
- 没有来源可信度评分。
- 没有 rerank 和多源交叉验证。
- 没有持久化记忆。

## 2. 如何改为流式输出

思路：

1. 创建 Agent 时仍然使用 `create_agent`。
2. 调用时使用 `agent.stream(...)` 而不是 `agent.invoke(...)`。
3. 使用 `stream_mode="updates"` 观察每个节点更新。
4. 在 UI 中区分工具调用过程和最终回答。

伪代码：

```python
for chunk in agent.stream(
    {"messages": [{"role": "user", "content": question}]},
    config={"configurable": {"thread_id": thread_id}},
    stream_mode="updates",
):
    print(chunk)
```

## 3. 如何优化 demo

- 启动期校验 `.env` 和模型配置。
- REPL 循环内捕获异常，避免一次错误退出程序。
- `thread_id` 改成 `f"{user_id}:{session_id}"`。
- 搜索工具返回结构化字段：标题、摘要、URL、时间、来源。
- 回答时要求引用来源，搜索结果不足时明确说明不足。
- 加入空结果、超时、脏数据和冲突结果测试。
- 记录每次工具调用：工具名、参数、耗时、返回长度、错误类型。
