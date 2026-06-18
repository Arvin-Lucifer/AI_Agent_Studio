# L08 Agent 模式：从 RAG/ReAct 到多 Agent 协作

本章按老师给出的总主题“Agent 模式”整理：先学会判断一个任务应该用哪种 Agent 模式，再进入多 Agent 协作系统，最后落到企业知识库问答助手的工程选型和分库分索引策略。

## 本章学习目标

- 理解常见 Agent 模式：Direct、RAG、ReAct、Plan-and-Execute、Reflection、多 Agent。
- 能解释为什么企业知识库问答通常推荐“RAG 为主 + ReAct 为辅”。
- 能用 ReAct、Plan-and-Execute、Reflection、Multi-Agent 四种经典模式解释复杂 Agent 的组织方式。
- 掌握多 Agent 的三种基础协作形态：Supervisor、Sequential、Peer。
- 用 LangGraph 搭建一个“调研员 -> 分析师 -> 撰写员 -> 审核员”的协作流程。
- 理解分库分索引为什么能同时提升效果、安全、成本和运维可控性。
- 能为企业知识库问答助手设计路由层、检索层、Agent 层、答案层和评测回流。

## 文件分区

| 分类 | 路径 | 用途 |
| --- | --- | --- |
| 讲义 | [lecture/LECTURE_FULL.md](./lecture/LECTURE_FULL.md) | 第 8 讲完整讲义：Agent 模式、多 Agent、企业知识库选型 |
| 总结 | [lecture/CHAPTER_SUMMARY.md](./lecture/CHAPTER_SUMMARY.md) | 模式对比、代码地图和设计复盘 |
| 课前准备 | [materials/PRECLASS_CHECKLIST.md](./materials/PRECLASS_CHECKLIST.md) | 环境、概念和代码预习检查 |
| 实操代码 | [practice/](./practice/) | Supervisor 多 Agent、Agent 模式路由、分库分索引检索 |
| 一键脚本 | [practice/preclass_run.sh](./practice/preclass_run.sh) | 自动执行 L08 环境检查和核心示例 |
| 课堂笔记 | [materials/NOTES_TEMPLATE.md](./materials/NOTES_TEMPLATE.md) | 记录模式选型、路由策略、分库设计和多 Agent 流程 |
| 课后小测 | [materials/MINI_QUIZ.md](./materials/MINI_QUIZ.md) | 检查 Agent 模式与企业知识库核心概念 |
| 拓展练习 | [materials/EXTENSIONS.md](./materials/EXTENSIONS.md) | 翻译 Agent、分类器路由、权限过滤、评测集 |
| 面试题库 | [materials/INTERVIEW_QA.md](./materials/INTERVIEW_QA.md) | Agent 模式、多 Agent、企业知识库问答系统设计题 |
| 工程参考 | [resources/](./resources/) | 模式对比、多 Agent 范式、企业知识库和分库分索引设计 |
| 示例数据 | [data/](./data/) | 预留给企业知识库、评测集和多 Agent 运行结果 |

## 推荐学习路径

1. 阅读 [materials/PRECLASS_CHECKLIST.md](./materials/PRECLASS_CHECKLIST.md)，确认 LangGraph、LangChain 和 `.env` 环境可用。
2. 阅读 [lecture/LECTURE_FULL.md](./lecture/LECTURE_FULL.md) 的 8.1-8.2，先建立 Agent 模式选型框架。
3. 阅读 [教辅资料：Agent 设计模式](../../teaching_support/AGENT_DESIGN_PATTERNS.md)，横向理解 ReAct、Plan-and-Execute、Reflection 和 Multi-Agent。
4. 运行 `practice/27_agent_mode_router.py`，观察同一个问答系统如何在 direct、RAG、ReAct 之间选择。
5. 阅读讲义 8.3-8.4，理解 Supervisor、Sequential、Peer 三类多 Agent 协作模式。
6. 运行 `practice/26_supervisor_research_team.py`，观察 LangGraph 如何管理多角色状态流转。
7. 阅读 [resources/ENTERPRISE_KB_AGENT_DESIGN.md](./resources/ENTERPRISE_KB_AGENT_DESIGN.md)，把 RAG/ReAct 选型放到企业知识库场景里理解。
8. 运行 `practice/28_multi_index_retrieval.py`，观察分库路由、权限过滤和统一 rerank。
9. 阅读 [materials/INTERVIEW_QA.md](./materials/INTERVIEW_QA.md)，准备系统设计和面试追问。
10. 完成 [materials/MINI_QUIZ.md](./materials/MINI_QUIZ.md)，再用 [lecture/CHAPTER_SUMMARY.md](./lecture/CHAPTER_SUMMARY.md) 复盘。

## 快速运行

从课程根目录激活环境：

```bash
source <course-root>/scripts/activate_course.sh
```

进入第八章目录：

```bash
cd <course-root>/lessons/L08_agent_modes
```

运行 Agent 模式路由：

```bash
python practice/27_agent_mode_router.py --question "P0工单响应时间和API发布审批有什么共同要求？"
```

运行 Supervisor 多 Agent 团队：

```bash
python practice/26_supervisor_research_team.py --topic "企业知识库问答助手设计"
```

运行分库分索引检索：

```bash
python practice/28_multi_index_retrieval.py --query "API发布需要几人审批？"
```

一键预习检查：

```bash
bash practice/preclass_run.sh
```

通过标志：最后看到 `[OK] L08 preclass run completed.`。

## 本章实操说明

- `practice/agent_mode_common.py`：公共环境加载、mock/LLM 切换、企业知识库示例数据、规则路由、检索和 rerank。
- `practice/26_supervisor_research_team.py`：用 LangGraph 搭建调研员、分析师、撰写员、审核员协作流程。
- `practice/27_agent_mode_router.py`：演示企业知识库问答里 direct / RAG / ReAct 的轻量路由。
- `practice/28_multi_index_retrieval.py`：演示按业务域分库、权限前置过滤和多库召回统一重排。
- `practice/preclass_run.sh`：串联环境检查和三个核心示例。

## 本章交付物

- 一张 Agent 模式选型表：Direct、RAG、ReAct、Plan-and-Execute、多 Agent 分别适合什么任务。
- 一个 Supervisor 多 Agent 流程图，说明每个 Agent 的输入、输出和状态字段。
- 一个企业知识库问答架构图：路由层、检索层、Agent 层、答案层、评测回流。
- 一份分库分索引设计：业务域、敏感等级、数据形态、时效性如何组合。
- 一次运行日志：同一个问题为什么走 RAG 或 ReAct，引用了哪些文档。
- 一份面试题复盘：为什么不推荐纯 Fine-tune、纯 Plan-and-Execute 或大规模多 Agent 辩论。

## 与后续章节的关系

L08 解决“任务应该用哪种 Agent 模式”的问题。L09 会进一步把外部系统通过 MCP/工具协议接入 Agent；L10 会进入 Skill 相关能力组织；L11 会把评测和部署放到工程闭环里；L12 会把 RAG、工具调用、记忆和 Agent 模式组合成毕业项目实战。
