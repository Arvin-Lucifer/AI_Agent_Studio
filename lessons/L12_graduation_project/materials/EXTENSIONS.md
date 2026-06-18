# L12 拓展练习

## 必做巩固

1. 新增一份知识库文档，运行：

```bash
python scripts/build_kb.py
python evals/run_eval.py
```

2. 新增两条评测用例：一条正常问答，一条无法回答转人工。
3. 在 Dashboard 或 `/audit/{trace_id}` 中回放一次完整请求。
4. 修改一条业务规则后，补充对应测试。

## 进阶增强

1. 多跳 RAG：为复杂问题加入子问题拆解，保留 `max_hops <= 3`。
2. ReAct 兜底：只在低置信度或多跳失败时触发，保留 `max_steps <= 4`。
3. RRF 融合：将多个 collection 的召回结果统一重排。
4. 监控增强：增加 P50/P95、意图分布、工单率、低置信度率。
5. 安全增强：为更多管理接口加权限、限流和审计。

## MCP / Skill 加分项

1. 设计 `kb-retrieval` MCP：
   - `search_kb`
   - `list_collections`
   - `rebuild_index`
   - `get_document`
2. 设计 `ticket-management` MCP：
   - `create_ticket`
   - `update_ticket`
   - `list_tickets`
   - `get_ticket_status`
3. 设计 `multihop-rag` Skill：
   - 输入：用户问题、可用 collections、最大 hops。
   - 输出：子问题、证据、最终答案、置信度。
   - 约束：无证据不答，超步数转人工。

## 答辩材料

整理一页项目亮点：

- 我解决了什么真实问题。
- 我的架构为什么不是 Demo。
- 我的质量证明是什么。
- 我如何处理失败和兜底。
- 我下一步会怎么产品化。

