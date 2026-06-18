# L09 MCP 协议与工具生态：标准化的 Agent 工具接入

本章学习 MCP（Model Context Protocol）：它把 Agent 与外部工具、数据源、提示模板之间的接入方式标准化。可以把 MCP 理解成 Agent 工具生态里的“USB-C”：工具方实现 MCP Server，Agent/Host 实现 MCP Client，双方通过统一协议发现能力、读取资源、调用工具和处理上下文。

## 本章学习目标

- 理解 MCP 解决的核心问题：碎片化集成、上下文孤岛、协议不统一。
- 掌握 MCP 架构：Host、MCP Client、MCP Server、Transport。
- 理解 MCP 四类原语：Tools、Resources、Prompts、Sampling。
- 用 Python MCP SDK 开发一个笔记管理 MCP Server。
- 用 stdio MCP Client 发现工具、调用工具、读取资源和获取 Prompt。
- 理解如何把 MCP 工具包装进 LangChain/LangGraph Agent。
- 能说明 MCP 与 Function Calling 的区别和协作关系。
- 掌握 MCP 安全、排障、大规模接入和面试高频问题。

## 文件分区

| 分类 | 路径 | 用途 |
| --- | --- | --- |
| 讲义 | [lecture/LECTURE_FULL.md](./lecture/LECTURE_FULL.md) | 第 9 讲完整讲义：MCP 架构、实操、生态和选型 |
| 总结 | [lecture/CHAPTER_SUMMARY.md](./lecture/CHAPTER_SUMMARY.md) | 原语速查、代码地图和排障清单 |
| 课前准备 | [materials/PRECLASS_CHECKLIST.md](./materials/PRECLASS_CHECKLIST.md) | 环境、概念和代码预习检查 |
| 实操代码 | [practice/](./practice/) | MCP Server、stdio Client、LangChain 桥接、安全检查、Sampling 流程 |
| 一键脚本 | [practice/preclass_run.sh](./practice/preclass_run.sh) | 自动执行 L09 环境检查和核心示例 |
| 课堂笔记 | [materials/NOTES_TEMPLATE.md](./materials/NOTES_TEMPLATE.md) | 记录协议角色、原语、调用链路和安全策略 |
| 课后小测 | [materials/MINI_QUIZ.md](./materials/MINI_QUIZ.md) | 检查 MCP 核心概念 |
| 拓展练习 | [materials/EXTENSIONS.md](./materials/EXTENSIONS.md) | update/delete、Sampling callback、远程 Server、审计日志 |
| 面试题库 | [materials/INTERVIEW_QA.md](./materials/INTERVIEW_QA.md) | MCP 分层面试题、系统设计题和排障题 |
| 工程参考 | [resources/](./resources/) | 原语、架构、安全排障、MCP 与 Function Calling 对比 |
| 运行数据 | [data/](./data/) | 笔记 MCP Server 的 JSON 示例数据 |

## 推荐学习路径

1. 阅读 [materials/PRECLASS_CHECKLIST.md](./materials/PRECLASS_CHECKLIST.md)，确认 `mcp` SDK 已安装在 `agent_course` 环境。
2. 阅读 [lecture/LECTURE_FULL.md](./lecture/LECTURE_FULL.md) 的 9.1-9.2，理解 MCP 为什么像 Agent 工具接入的 USB-C。
3. 运行 `practice/30_mcp_stdio_client.py`，观察 Client 如何启动 Server、发现工具、调用工具、读取资源和获取 Prompt。
4. 阅读 `practice/29_mcp_note_server.py`，理解 `@mcp.tool()`、`@mcp.resource()`、`@mcp.prompt()` 的区别。
5. 运行 `practice/31_langchain_mcp_bridge.py`，理解 LangChain Tool 如何转发到 MCP Client。
6. 运行 `practice/32_mcp_safety_checklist.py` 和 `practice/33_mcp_sampling_flow.py`，理解安全治理和 Sampling 审核。
7. 阅读 [resources/MCP_VS_FUNCTION_CALLING.md](./resources/MCP_VS_FUNCTION_CALLING.md)，建立选型判断。
8. 阅读 [materials/INTERVIEW_QA.md](./materials/INTERVIEW_QA.md)，准备 MCP 面试题。
9. 完成 [materials/MINI_QUIZ.md](./materials/MINI_QUIZ.md)，再用 [lecture/CHAPTER_SUMMARY.md](./lecture/CHAPTER_SUMMARY.md) 复盘。

## 快速运行

从课程根目录激活环境：

```bash
source <course-root>/scripts/activate_course.sh
```

进入第 9 章目录：

```bash
cd <course-root>/lessons/L09_mcp_tooling
```

运行 MCP Client：

```bash
python practice/30_mcp_stdio_client.py
```

运行 LangChain 桥接示例：

```bash
python practice/31_langchain_mcp_bridge.py
```

运行安全检查：

```bash
python practice/32_mcp_safety_checklist.py
```

一键预习检查：

```bash
bash practice/preclass_run.sh
```

通过标志：最后看到 `[OK] L09 preclass run completed.`。

## 本章实操说明

- `practice/mcp_common.py`：笔记数据读写、搜索、更新、删除和摘要逻辑。
- `practice/29_mcp_note_server.py`：FastMCP Server，暴露 Tools、Resource 和 Prompt。
- `practice/30_mcp_stdio_client.py`：stdio Client，演示 initialize、list_tools、call_tool、read_resource、get_prompt。
- `practice/31_langchain_mcp_bridge.py`：把 MCP 工具包装成 LangChain Tool，默认不调用真实 LLM。
- `practice/32_mcp_safety_checklist.py`：把 MCP 安全审查做成静态检查器。
- `practice/33_mcp_sampling_flow.py`：模拟 Sampling 的 Client 审核、脱敏和拒绝流程。

## 本章交付物

- 一个可运行的笔记 MCP Server。
- 一次 stdio Client 调用日志。
- 一张 MCP 四类原语对比表。
- 一份 MCP 与 Function Calling 的选型说明。
- 一份 MCP Server 安全接入检查清单。
- 一份排障记录：如果模型看不到工具，应按什么顺序排查。

## 与后续章节的关系

L09 解决“外部能力如何标准化接入 Agent”的问题。L10 会把可复用能力沉淀为 Skill，并进一步讨论 Skill 的边界、授权、安全、重试、延迟和发布回滚；L11 会把评测和部署纳入工程闭环；L12 会把 RAG、记忆、Agent 模式、MCP 和 Skill 组合成端到端项目。
