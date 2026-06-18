# 具体实战参考摘录

本文件从 `具体实战参考.docx` 抽取核心路线，便于在 Markdown 中阅读和链接。Word 原件仍保留在本目录。

## 一、六轮迭代路线

1. 第 1 轮：`PRD -> TRD -> TDD -> Harness` 全流程，完成基本功能，并启动 FastAPI 查看效果。
2. 第 2 轮：补齐前后端项目完整性。
3. 第 3 轮：添加记忆系统、ReAct、多跳 RAG、分库索引和路由；同步更新需求文档和技术方案。
4. 第 4 轮：添加可观测数据和监控大盘；同步更新需求文档和技术方案设计文档。
5. 第 5 轮：抽取 MCP 和 Skill。
6. 第 6 轮：形成项目总结，可用于答辩和面试。

## 二、项目定位

基于 LangGraph 的企业级智能客服 Agent，融合分库 RAG、多跳推理、ReAct 兜底、跨会话记忆、端到端可观测性，并通过 MCP/Skill 抽取实现跨项目复用。

## 三、架构要点

### 1. 编排架构

采用 LangGraph 状态机取代单层 LCEL，将以下流程建模为条件跳转 DAG：

```text
意图分类 -> 路由检索 -> 单跳/多跳 RAG -> ReAct 兜底 -> 工单生成
```

节点间状态显式持久化，便于补偿、回放与灰度。

### 2. 检索层

按 FAQ、Policy、Manual、Troubleshoot 等 collection 分索引。

建议两层路由：

- L1：关键词正则，覆盖高频流量。
- L2：LLM 或更复杂分类器兜底处理长尾。

多源结果可用 RRF 融合，避免不同 embedding 或不同检索器分数不可比。

### 3. 多跳 RAG

用连接词、问题长度和问号数量启发式预判复杂问题，再拆解子问题、串联检索和证据合成。必须保留 `max_hops` 硬上限，避免短问题无意义拆解。

### 4. ReAct 兜底

触发条件：

- 意图模糊。
- 多跳失败。
- RAG 置信度低于阈值。

循环结构：

```text
Thought -> Action -> Observation -> Thought ... -> Final Answer
```

工具集建议：

- `kb_search`
- `ticket_create`
- `profile_lookup`

稳态保障：

- JSON 解析容错。
- 未知 action 自纠。
- 步数硬上限。
- 出现 Final Answer 或步数耗尽后转工单兜底。

可观测要求：

- 每步 Thought、Action、Observation 都写入 NDJSON 事件。
- Dashboard 可按 `trace_id` 完整回放。

### 5. 跨会话记忆

建议采用历史问答摘要、时间衰减和终点写摘要。匿名用户应默认短路，避免不必要的隐私持久化。

### 6. 可观测与监控大盘

建议用 `trace_id` 贯穿主链路，NDJSON 记录原子事件，Timer 采集 latency/error，滚动聚合 P50/P95/QPS、多跳率和 ReAct 触发率。

前端可用纯 HTML/CSS/JS 做 KPI 卡、分布图和审计回放。

### 7. 工程化扩展

可将“路由 + 检索 + 索引重建”抽取为 `kb-retrieval` MCP，将“多跳 RAG 工作流”沉淀为 `multihop-rag` Skill，建立 “Skill 调 MCP” 的分层复用契约。

## 四、面试可讲三件事

1. LangGraph 节点如何取舍。
2. L1/L2 路由 + RRF 的成本和鲁棒性平衡。
3. ReAct 步数硬上限、工单兜底、NDJSON 全链路回放如何形成稳定闭环。

## 五、和当前参考实现的对应关系

当前 `reference_implementation/intelligent_customer_agent/` 已完整覆盖基础功能、前后端、记忆、分库检索、可观测数据、Dashboard、质量门禁和部署运维。

MCP 与 Skill 抽取仍建议作为扩展练习处理：先写设计文档和边界，再考虑真正拆成独立服务或 Skill 包。

