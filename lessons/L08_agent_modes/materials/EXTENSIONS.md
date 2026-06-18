# L08 拓展练习

## 练习 1：增加 Translator Agent

在 `practice/26_supervisor_research_team.py` 中增加一个 `translator_agent`：

- 输入：最终中文报告。
- 输出：英文摘要或英文全文。
- 要求：只有审核通过后才进入翻译。
- 思考：翻译结果是否还需要 Reviewer 再审核一次？

## 练习 2：增加“澄清问题”模式

在 `practice/27_agent_mode_router.py` 中增加 `clarify` 模式：

- 当问题缺少关键实体，例如“这个流程怎么走？”时，不直接检索。
- 先返回澄清问题，例如“请问你指的是 HR 入职流程、财务报销流程，还是研发发布流程？”
- 记录：哪些规则容易误判？是否需要 LLM 分类器？

## 练习 3：新增业务域和权限等级

在 `practice/agent_mode_common.py` 的 `KNOWLEDGE_BASES` 中新增 `legal` 或 `sales`：

- 至少 2 条文档。
- 至少 1 条 `confidential`。
- 给 `DOMAIN_KEYWORDS` 增加关键词。
- 用 `practice/28_multi_index_retrieval.py` 验证权限过滤。

## 练习 4：把规则路由升级为分类器路由

实现一个 `classify_domains_with_llm(query)`：

- 输出候选业务域列表。
- 输出置信度。
- 输出是否需要 ReAct。
- 要求失败时回退到规则路由。

建议输出格式：

```json
{
  "domains": ["engineering", "support"],
  "mode": "react",
  "confidence": 0.86,
  "reason": "问题同时涉及工单 SLA 和 API 发布审批"
}
```

## 练习 5：增加引用正确率评测

新建一个小型评测集：

```json
[
  {
    "question": "P0工单多久内响应？",
    "expected_doc_id": "sup-001",
    "expected_answer_contains": "15分钟"
  }
]
```

实现一个脚本统计：

- 检索是否命中 `expected_doc_id`。
- 答案是否包含关键事实。
- 无证据问题是否拒答。
- 越权问题是否没有泄露机密内容。

## 练习 6：设计生产审计日志

为每次企业知识库问答记录：

- user_id
- tenant_id
- query
- selected_mode
- routed_domains
- allowed_sensitivity
- retrieved_doc_ids
- cited_doc_ids
- answer_hash
- latency_ms
- error_type

思考：哪些字段可以进普通日志，哪些字段必须脱敏或加密？
