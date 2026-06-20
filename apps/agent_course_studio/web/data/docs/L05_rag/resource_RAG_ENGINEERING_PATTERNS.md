# RAG 工程模式与排查清单

## 1. 标准 RAG 架构

```text
数据源
  ↓
解析清洗
  ↓
Chunking
  ↓
Embedding / 关键词索引 / 结构化索引
  ↓
Retriever
  ↓
Reranker
  ↓
Context Builder
  ↓
LLM
  ↓
Answer + Citations
```

## 2. 效果差时如何排查

- 数据源：知识库是否真的有答案？文档是否过期、缺失、冲突？
- 解析：PDF 表格、图片、标题、页眉页脚是否处理正确？
- 切分：chunk 是否过大、过小、缺标题、缺 overlap？
- 检索：TopK 是否太小？query 是否需要 rewrite？是否需要 hybrid search？
- 重排：正确 chunk 是否被 reranker 排到前面？
- 上下文：是否放入太多噪声？是否截断关键证据？
- Prompt：是否要求仅基于上下文回答？是否要求无答案时拒答？
- 生成：LLM 是否错误合并证据？是否需要答案自检？

## 3. 常用优化手段

- Query Rewrite：补全指代、统一术语、扩展同义词。
- Multi-query：从多个角度检索并合并结果。
- Hybrid Search：向量召回 + 关键词召回。关键词召回常用 BM25 和倒排索引，入门解释见 [BM25 和倒排索引简单介绍](../../../teaching_support/BM25_INVERTED_INDEX.md)。
- Rerank：粗召回后精排。
- Context Compression：只保留相关句子或关键事实。
- Citation Check：验证答案引用是否真的支持结论。
- No-answer Gate：低置信检索时拒答或追问。

## 4. 企业级治理

- 权限：chunk 继承文档 ACL，检索和上下文注入前都要校验。
- 缓存：按用户或权限集合隔离，避免缓存泄露。
- 版本：记录更新时间、版本号、文档状态、Owner。
- 审计：记录 query、命中文档、权限过滤、最终答案和引用。
- 安全：防 RAG Prompt Injection，把检索内容当数据而不是指令。
