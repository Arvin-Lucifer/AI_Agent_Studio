# L05 章节总结：RAG 检索增强生成

## 一句话总结

RAG 的本质是：让模型回答前先查资料，并要求它基于查到的资料回答。

## 核心流程

| 阶段 | 关键动作 |
| --- | --- |
| 离线建库 | 文档接入、解析、清洗、切分、embedding、建索引 |
| 在线问答 | Query rewrite、检索、rerank、上下文构造、生成、引用 |

## 本章代码地图

- `practice/rag_common.py`：本地 RAG 公共逻辑。
- `practice/11_prepare_knowledge_base.py`：生成示例文档。
- `practice/12_build_local_index.py`：构建标准库版本地索引。
- `practice/13_rag_agent.py`：检索上下文并调用 LLM 生成答案。
- `practice/14_chunking_compare.py`：比较不同 chunk size 的检索效果。

## 必须记住的工程判断

- RAG 不是微调模型，它是在推理时注入外部知识。
- Chunk 不是越大越好，也不是越小越好，要用评估集调参。
- 检索对不代表最终答案一定对，LLM 可能用错上下文。
- 纯向量检索不是万能的，生产系统常用 hybrid search + rerank。
- PDF RAG 要保留结构、表格、图片描述、页码、bbox、caption 和权限信息。
- 没有证据时，好的 RAG 应该拒答或追问，而不是编造。

## 复盘问题

- RAG 解决了 LLM 的哪些问题？
- 离线阶段和在线阶段分别做什么？
- chunk size 过大/过小分别有什么风险？
- 为什么需要引用来源？
- 为什么 RAG 还需要权限控制？
- 如果检索结果正确但答案错误，应该排查哪里？
