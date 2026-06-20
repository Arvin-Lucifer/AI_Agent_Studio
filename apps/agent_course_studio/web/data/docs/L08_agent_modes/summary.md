# L08 章节总结

## 一句话总结

第 8 章讲的是 Agent 模式选型：企业问答优先用 RAG 保证可信和可追溯，用 ReAct 处理多跳长尾；复杂产出型任务再用多 Agent 做角色分工和质量控制。

## 模式速查

| 模式 | 什么时候用 | 什么时候别用 |
| --- | --- | --- |
| Direct | 通用问答、格式转换、无需私域知识 | 涉及企业制度、实时数据、审计要求 |
| RAG | 企业知识库、制度问答、可引用答案 | 多跳、跨源、计算型问题 |
| ReAct | 多步检索、工具调用、跨源融合 | 高频简单问题 |
| Plan-and-Execute | 长流程任务、自动化项目 | 单次知识库问答 |
| Reflection | 高风险输出、自检修正 | 低价值高频问答 |
| Multi-Agent | 研报、方案、复杂协作 | 职责不清或流程很短的任务 |

## 企业知识库推荐架构

```text
用户问题
  -> 路由层：direct / RAG / ReAct
  -> 检索层：BM25 + 向量 + 元数据过滤 + rerank
  -> Agent 层：必要时多步检索或工具调用
  -> 答案层：引用来源、无证据拒答
  -> 评测回流：命中率、忠实度、引用正确率、bad case
```

关键原则：

- RAG 是主干，因为企业知识私域、频繁更新、需要溯源。
- ReAct 是兜底，用来处理多跳、模糊、跨源和计算型问题。
- 工具数量建议收敛到 5 个以内，步数上限建议 3-5 步。
- 无证据时回答“未找到”，不要编造。

## 分库分索引复盘

为什么要分库：

- 权限隔离：不同部门和敏感等级不能混在一起。
- 语料异构：制度、代码、工单、表格需要不同切片策略。
- 更新频率不同：热数据和冷数据不应该绑在一个更新节奏里。
- 效果调优：同一关键词在不同业务域含义不同。

推荐主线：

```text
业务域为主键
  + 数据形态
  + 敏感等级
  + 时效性
  -> 独立 collection/index
  -> 统一 metadata schema
  -> 多库召回
  -> 统一 rerank
  -> 权限审计
```

统一元数据字段建议：

```text
doc_id, domain, sensitivity, owner_dept, valid_from, valid_to,
source_url, version, lang, tags
```

## 多 Agent 代码地图

- `practice/agent_mode_common.py`：公共工具，包含 `.env` 加载、mock/LLM 切换、示例知识库、规则路由、检索和 rerank。
- `practice/26_supervisor_research_team.py`：LangGraph 多 Agent 研报团队。
- `practice/27_agent_mode_router.py`：企业知识库问答的 direct / RAG / ReAct 路由。
- `practice/28_multi_index_retrieval.py`：分库分索引、权限过滤和统一重排演示。

## LangGraph 流程

```text
START
  -> researcher: topic -> research_data
  -> analyst: research_data -> analysis
  -> writer: research_data + analysis -> report
  -> reviewer: report -> review_feedback + is_approved
  -> approved ? END : writer
```

要重点看三个点：

- `TeamState` 是 Agent 之间的交接协议。
- 每个 Agent 只写自己负责的字段。
- `revision_count` 用来限制返工轮数，避免无限循环。

## 常见误区

- 以为 Agent 越复杂越高级。真实系统里简单路径更稳定、更便宜。
- 把所有企业文档塞进一个向量库。这样会同时伤害权限、安全、召回和调优。
- 在答案生成后再做权限过滤。正确做法是在检索前和检索中就过滤。
- 让多 Agent 自由聊天。生产系统要有状态协议、终止条件和可观测日志。
- 把 Fine-tune 当知识更新手段。知识库问答更适合检索更新和版本化索引。

## 复盘问题

1. 为什么企业知识库问答推荐 RAG 为主，而不是纯 Fine-tune？
2. 什么问题应该从单轮 RAG 升级到 ReAct？
3. 分库分索引比单库方案解决了哪些工程问题？
4. 多库召回后为什么不能直接比较原始向量分数？
5. Supervisor、Sequential、Peer 三种多 Agent 模式分别适合什么场景？
6. 多 Agent 系统如何避免无限循环和责任不清？
