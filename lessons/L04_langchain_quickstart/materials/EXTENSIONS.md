# L04 拓展练习

## 必做：笔记工具 Agent

在 `practice/10_search_agent.py` 的基础上增加两个工具：

1. `write_note(title, content)`：把内容保存为 Markdown 文件。
2. `list_notes()`：列出已保存的笔记标题和路径。

要求：

- 笔记只能写入本章目录下的 `materials/generated_notes/`。
- 标题要做文件名清洗，避免路径穿越。
- 保存成功后返回结构化信息：标题、路径、字符数。
- 实现“搜索信息 -> 保存笔记 -> 查看笔记”的完整流程。

## 选做：真实搜索 API

把 mock `search_web` 替换成真实搜索 API，例如 Tavily、SerpAPI 或公司内部搜索服务。

要求：

- API key 放在 `.env`。
- 搜索结果保留标题、摘要、URL、时间。
- 空结果和超时要有明确错误信息。
- 回答时引用来源，不要编造链接。

## 选做：流式输出

参考 [resources/SEARCH_AGENT_ENGINEERING_NOTES.md](../resources/SEARCH_AGENT_ENGINEERING_NOTES.md)，把 `invoke` 改为 `stream`。

观察：

- 用户能否看到工具调用过程？
- 工具结果和最终回答是否能区分？
- 流式输出失败时是否能恢复？

## 进阶：效果评估

构造 10 个测试问题，至少包含：

- 不需要工具的问题。
- 需要天气/时间/计算的问题。
- 需要搜索的问题。
- 搜索结果为空的问题。
- 搜索结果冲突的问题。

记录：

- 工具选择是否正确。
- 参数是否正确。
- 最终回答是否忠实于工具结果。
- 错误时是否能优雅降级。
