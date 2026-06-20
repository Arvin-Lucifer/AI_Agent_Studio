# L08 课前准备清单

## 1. 环境检查

从课程根目录激活环境：

```bash
source <course-root>/scripts/activate_course.sh
```

检查基础环境：

```bash
python scripts/check_env.py
python scripts/smoke_openai.py
```

进入第 8 章目录并运行预习脚本：

```bash
cd <course-root>/lessons/L08_agent_modes
bash practice/preclass_run.sh
```

确认最后看到：

```text
[OK] L08 preclass run completed.
```

## 2. 概念预习

- [ ] 我能解释 Direct、RAG、ReAct、Plan-and-Execute、Reflection、Multi-Agent 的区别。
- [ ] 我知道企业知识库问答为什么通常以 RAG 为主。
- [ ] 我知道哪些问题需要从单轮 RAG 升级到 ReAct。
- [ ] 我能说出 Supervisor、Sequential、Peer 三种多 Agent 模式。
- [ ] 我理解多 Agent 之间为什么要用明确的 `State` 传递信息。
- [ ] 我知道分库分索引要同时考虑业务域、数据形态、敏感等级和时效性。

## 3. 代码预习

先运行 Agent 模式路由：

```bash
python practice/27_agent_mode_router.py --question "我入职3年有几天年假？"
python practice/27_agent_mode_router.py --question "P0工单响应时间和API发布审批有什么共同要求？"
```

观察输出里的：

- `[MODE]` 是 `rag` 还是 `react`。
- `[TRACE]` 里路由到了哪些业务域。
- `[CITATIONS]` 是否有可追溯来源。

再运行多 Agent 团队：

```bash
python practice/26_supervisor_research_team.py --topic "企业知识库问答助手设计"
```

观察输出里的：

- 调研、分析、写作、审核是否通过状态字段串起来。
- `revision_count` 是否限制返工次数。

最后运行分库分索引演示：

```bash
python practice/28_multi_index_retrieval.py --query "API发布需要几人审批？"
python practice/28_multi_index_retrieval.py --query "差旅报销需要什么材料？"
python practice/28_multi_index_retrieval.py --query "差旅报销需要什么材料？" --include-confidential
```

对比第二条和第三条，理解权限过滤为什么必须发生在检索阶段。

## 4. 课前思考

- 一个企业知识库问答助手，为什么不应该所有问题都走 ReAct？
- 为什么单个大向量库不适合承载 HR、财务、研发、客服的所有文档？
- 多 Agent 中如果 Writer 和 Reviewer 反复互相修改，系统应该怎么停下来？
- 如果用户没有财务权限，却问“差旅报销需要什么材料”，系统应该在什么阶段拦截？
- RAG 查不到证据时，答案层应该怎么表达？

## 5. 30 分钟预习路径

1. 0-8 分钟：阅读 README 和讲义 8.1-8.2。
2. 8-14 分钟：运行 `practice/27_agent_mode_router.py`，理解模式路由。
3. 14-20 分钟：运行 `practice/26_supervisor_research_team.py`，理解 LangGraph 多 Agent。
4. 20-25 分钟：运行 `practice/28_multi_index_retrieval.py`，理解分库和权限过滤。
5. 25-30 分钟：阅读 `resources/ENTERPRISE_KB_AGENT_DESIGN.md` 的架构和落地节奏。
