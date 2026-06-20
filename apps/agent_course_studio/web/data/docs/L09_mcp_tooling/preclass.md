# L09 课前准备清单

## 1. 环境检查

从课程根目录激活环境：

```bash
source <course-root>/scripts/activate_course.sh
```

检查基础环境：

```bash
python scripts/check_env.py
python scripts/smoke_openai.py
python -c "from mcp.server.fastmcp import FastMCP; print('mcp ok')"
```

进入第 9 章目录：

```bash
cd <course-root>/lessons/L09_mcp_tooling
```

运行一键脚本：

```bash
bash practice/preclass_run.sh
```

确认最后看到：

```text
[OK] L09 preclass run completed.
```

## 2. 概念预习

- [ ] 我能解释 MCP 为什么像 Agent 工具生态里的 USB-C。
- [ ] 我知道 Host、MCP Client、MCP Server 的区别。
- [ ] 我知道 stdio 和 Streamable HTTP 分别适合什么场景。
- [ ] 我能说出 Tools、Resources、Prompts、Sampling 四类原语。
- [ ] 我能解释 Tools 和 Resources 的边界。
- [ ] 我知道 MCP 与 Function Calling 不是同一个层级的问题。
- [ ] 我能说出至少 3 个 MCP 安全风险。

## 3. 代码预习

运行 MCP Client：

```bash
python practice/30_mcp_stdio_client.py
```

观察：

- `TOOLS` 中有哪些工具。
- `RESOURCES` 中是否看到 `notes://summary`。
- `PROMPTS` 中是否看到 `note_review_template`。
- `CREATE NOTE` 和 `SEARCH NOTES` 是否成功。

运行 LangChain 桥接：

```bash
python practice/31_langchain_mcp_bridge.py
```

观察：

- LangChain Tool 是否能把调用转发给 MCP Server。
- 课堂版为什么每次调用会启动一次 stdio Server。

运行安全和 Sampling 示例：

```bash
python practice/32_mcp_safety_checklist.py
python practice/33_mcp_sampling_flow.py
```

观察：

- 哪些配置被判定为高风险。
- Sampling 请求为什么可能被 Client 拒绝。

## 4. 课前思考

- 如果模型看不到 MCP Server 暴露的工具，第一步应该查什么？
- 为什么 stdio Server 不应该把普通日志写到 stdout？
- 只读数据应该设计为 Tool 还是 Resource？
- Sampling 为什么不能由 Server 无条件调用模型？
- 什么时候用 Function Calling 足够，什么时候应该升级到 MCP？

## 5. 30 分钟预习路径

1. 0-8 分钟：阅读 README 和讲义 9.1-9.4。
2. 8-14 分钟：运行 `practice/30_mcp_stdio_client.py`。
3. 14-20 分钟：阅读 `practice/29_mcp_note_server.py` 的装饰器。
4. 20-24 分钟：运行 `practice/31_langchain_mcp_bridge.py`。
5. 24-30 分钟：阅读 `resources/MCP_SECURITY_AND_TROUBLESHOOTING.md` 的排障清单。
