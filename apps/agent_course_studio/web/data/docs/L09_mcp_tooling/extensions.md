# L09 拓展练习

## 练习 1：完善笔记 Server 的参数校验

修改 `practice/29_mcp_note_server.py` 和 `practice/mcp_common.py`：

- 限制标题最长 80 个字符。
- 限制正文最长 2000 个字符。
- 限制标签最多 5 个。
- 对不存在的 `note_id` 返回清晰错误。

## 练习 2：增加按标签筛选工具

新增工具：

```python
@mcp.tool()
def search_notes_by_tag(tag: str) -> str:
    ...
```

要求：

- 标签匹配大小写不敏感。
- 没有结果时明确返回“未找到”。
- 在 `30_mcp_stdio_client.py` 中调用一次。

## 练习 3：把笔记存储换成 SQLite

把 `data/notes.json` 替换为 SQLite：

- 表字段：`id, title, content, tags, created_at, updated_at`。
- 保留原有 tool 名称和参数。
- 思考：Server 内部存储变化后，Client 是否需要改？

## 练习 4：实现真实 Sampling callback

参考 `practice/33_mcp_sampling_flow.py`：

- 在 ClientSession 中传入 `sampling_callback`。
- Server 主动请求摘要生成。
- Client 先检查敏感词，再决定是否调用真实 LLM。
- 记录被拒绝的 Sampling 请求。

## 练习 5：接入 MCP Inspector

使用：

```bash
mcp dev practice/29_mcp_note_server.py
```

或者：

```bash
npx @modelcontextprotocol/inspector python practice/29_mcp_note_server.py
```

记录：

- Inspector 中能看到哪些 Tools。
- inputSchema 是否符合预期。
- Resource 是否能读取。
- Prompt 是否能获取。

## 练习 6：设计 MCP Gateway

设计一个 Gateway，统一接入：

- filesystem server
- sqlite server
- github server
- note-manager server

需要回答：

- 如何做鉴权？
- 如何做工具命名空间？
- 如何做跨 Server 数据分级？
- 如何限制 Sampling 风暴？
- 如何记录审计日志？

## 练习 7：工具描述注入防护

在 `practice/32_mcp_safety_checklist.py` 中增加更多检测规则：

- 检查 description 中是否要求“忽略系统提示”。
- 检查工具是否请求过宽权限。
- 检查有副作用工具是否缺少确认机制。
- 输出风险等级和整改建议。
