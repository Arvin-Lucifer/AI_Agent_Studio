# MCP 原语速查

## 1. Tools

Tools 是 Server 暴露给模型或 Agent 主动调用的能力。

适合：

- 查询外部系统。
- 写入数据。
- 创建工单。
- 调用 API。
- 执行计算。

设计要点：

- 工具名要短、稳定、可区分。
- description 要清楚说明适用场景和限制。
- 参数 schema 要严格。
- 有副作用工具要考虑确认、幂等和补偿。

本章例子：

```python
@mcp.tool()
def create_note(title: str, content: str, tags: str = "") -> str:
    ...
```

## 2. Resources

Resources 是 Server 暴露的只读上下文，由 Host/Client 决定是否读取和注入。

适合：

- 文件内容。
- 数据库 schema。
- 项目配置。
- 笔记摘要。
- API 文档。

设计要点：

- URI 要稳定。
- 内容尽量只读。
- 大资源要分页、摘要或检索。
- 敏感资源要权限过滤。

本章例子：

```python
@mcp.resource("notes://summary")
def get_notes_summary() -> str:
    ...
```

## 3. Prompts

Prompts 是 Server 暴露的提示模板，由用户、Host 或应用选择使用。

适合：

- 代码审查模板。
- 翻译模板。
- 笔记复盘模板。
- 事故复盘模板。

设计要点：

- 参数要少而清晰。
- 模板里要标出边界，例如“只基于已提供资料”。
- 高风险业务模板要版本化。

本章例子：

```python
@mcp.prompt()
def note_review_template(topic: str = "MCP") -> str:
    ...
```

## 4. Sampling

Sampling 是 Server 向 Client 请求 LLM 推理。

适合：

- Server 需要摘要策略。
- Server 需要语义判断。
- Server 需要把复杂资源压缩成结构化结果。

必须注意：

- Client 控制是否允许。
- Client 控制模型和参数。
- Client 可以脱敏、改写或拒绝。
- 需要频率限制和审计。

本章例子：

```bash
python practice/33_mcp_sampling_flow.py
```

## 5. 选择表

| 需求 | 推荐原语 |
| --- | --- |
| 模型需要主动执行动作 | Tool |
| 应用要读取只读上下文 | Resource |
| 用户要复用提示模板 | Prompt |
| Server 需要模型帮忙思考 | Sampling |
| 大文件需要按需读取 | Resource + search Tool |
| 有副作用业务操作 | Tool + 确认 + 审计 |
