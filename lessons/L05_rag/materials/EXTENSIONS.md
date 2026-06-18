# L05 拓展练习

## 必做：自带文档 RAG

用你自己的 3-5 个文档替换 `data/knowledge_base/` 中的示例文档，重新构建索引。

要求：

- 至少 5 个测试问题。
- 记录 TopK 检索结果。
- 标注答案是否被引用支撑。
- 至少分析 1 个失败样例。

## 必做：Rewrite 或 Rerank

二选一：

- Rewrite：把用户问题改写成更适合检索的 query。
- Rerank：对初步召回结果重新排序，例如增加关键词命中分、标题命中分、来源权重。

记录优化前后对比。

## 选做：chunk size 对比

对比 `chunk_size=200/500/1000`：

- Top1 是否命中。
- TopK 是否有正确 chunk。
- 上下文噪声是否增加。
- 最终答案是否变好。

## 选做：接入真实向量库

将标准库本地索引替换成 Chroma 或 FAISS。

建议路线：

1. 安装 `requirements/rag.txt`。
2. 使用 embedding 模型向量化 chunk。
3. 建立持久化向量库。
4. 保留原来的 metadata 和引用格式。

## 进阶：PDF RAG

选择一份 PDF，设计处理方案：

- 是否扫描版？
- 页眉页脚如何清洗？
- 表格如何保结构？
- 图片和图表如何描述？
- 页码、bbox、caption 如何进入 metadata？

## 进阶：Agentic RAG

把 `search_knowledge_base` 设计成 Agent 工具，让 Agent 自己判断什么时候检索、检索什么、是否需要多轮检索。
