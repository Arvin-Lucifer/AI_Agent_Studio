# 分库分索引实施清单

这份清单用于把企业知识库从“一个大向量库”拆成可治理的多库架构。

## 1. 建库前调查

| 问题 | 记录 |
| --- | --- |
| 有哪些业务域？ |  |
| 每个域的 owner 是谁？ |  |
| 数据源在哪里？ |  |
| 更新频率是多少？ |  |
| 敏感等级如何划分？ |  |
| 是否需要跨地域部署？ |  |

## 2. Collection 命名建议

```text
kb_{domain}_{data_type}_{sensitivity}_{region}
```

示例：

```text
kb_hr_policy_internal_cn
kb_finance_expense_confidential_cn
kb_engineering_api_internal_cn
kb_support_ticket_internal_cn
```

## 3. 切片参数模板

| 业务域 | 数据类型 | chunk 粒度 | overlap | 特殊处理 |
| --- | --- | --- | --- | --- |
| HR | 制度 | 章节 | 100-150 token | 保留标题层级 |
| Finance | 报销制度 | 条款 | 100-150 token | 保留有效期 |
| Engineering | API 文档 | 接口级 | 少量 | 签名、参数、示例同块 |
| Support | 工单 | 整条 | 0 | 保留优先级和时间 |
| Legal | 合同 | 条款级 | 150 token | 保留合同编号 |

## 4. Metadata 必填字段

```json
{
  "doc_id": "eng-001",
  "domain": "engineering",
  "sensitivity": "internal",
  "owner_dept": "platform",
  "valid_from": "2026-01-01",
  "valid_to": null,
  "source_url": "https://example.local/wiki/eng-001",
  "version": "2026.03",
  "lang": "zh",
  "tags": ["API", "发布"]
}
```

## 5. 检索流程

```text
query
  -> normalize
  -> route domains
  -> build permission filter
  -> parallel retrieve
  -> rerank
  -> citation packing
  -> answer generation
```

## 6. 权限过滤检查

- [ ] 检索请求里包含 `tenant_id`。
- [ ] 检索请求里包含用户角色或部门。
- [ ] 检索 filter 包含 `sensitivity`。
- [ ] 机密库有独立鉴权。
- [ ] 日志里不记录原始机密内容。
- [ ] 越权问题有测试用例。

## 7. 评测集覆盖

每个业务域至少准备：

- 10 条单跳事实题。
- 5 条多跳题。
- 5 条无答案拒答题。
- 5 条越权拦截图。
- 5 条版本冲突题。

每条评测样例建议包含：

```json
{
  "question": "",
  "allowed_domains": [],
  "user_role": "",
  "expected_doc_ids": [],
  "expected_answer_contains": [],
  "should_refuse": false
}
```

## 8. 上线前验收

- [ ] top-k 检索命中率达标。
- [ ] 引用正确率达标。
- [ ] 无证据拒答达标。
- [ ] 越权拦截达标。
- [ ] P95 延迟达标。
- [ ] 单次问答成本可接受。
- [ ] bad case 能追溯到路由、检索、rerank 或生成层。
