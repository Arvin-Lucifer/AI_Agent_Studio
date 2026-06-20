# L05 RAG 检索增强生成：让 Agent 拥有专属知识库

本章承接 L03 的工具调用和 L04 的框架化 Agent，把“查资料再回答”做成一条完整链路。学生需要理解 RAG 的离线建库、在线检索、上下文增强、带引用生成，以及 PDF、表格、图片、权限和评估这些真实工程问题。

## 本章学习目标

- 理解 RAG = Retrieval-Augmented Generation，即检索增强生成。
- 能区分不用 RAG 的“闭卷回答”和使用 RAG 的“开卷回答”。
- 掌握离线阶段：文档解析、清洗、切分、索引。
- 掌握在线阶段：问题检索、上下文构造、LLM 生成、引用来源。
- 能跑通一个标准库版本地 RAG 系统，不依赖外部向量库也能理解核心流程。
- 理解 chunk size、overlap、hybrid search、rerank、query rewrite 对效果的影响。
- 理解 BM25 和倒排索引在关键词检索、Hybrid Search 中的作用。
- 能说明 PDF RAG 中页眉页脚、图片、表格、图表、OCR 和可追溯引用的处理方式。
- 能回答 RAG 面试中的基础、工程、Agentic RAG 和企业级安全问题。

## 文件分区

| 分类 | 路径 | 用途 |
| --- | --- | --- |
| 讲义 | [lecture/LECTURE_FULL.md](./lecture/LECTURE_FULL.md) | 第 5 讲完整讲义 |
| 总结 | [lecture/CHAPTER_SUMMARY.md](./lecture/CHAPTER_SUMMARY.md) | 本章核心流程、工程要点和复盘清单 |
| 工程参考 | [resources/](./resources/) | PDF RAG、工程模式与评估排查 |
| 课前准备 | [materials/PRECLASS_CHECKLIST.md](./materials/PRECLASS_CHECKLIST.md) | 环境、概念和预习检查 |
| 实操代码 | [practice/](./practice/) | 本地知识库、索引构建、RAG 问答、chunk 对比 |
| 示例知识库 | [data/knowledge_base/](./data/knowledge_base/) | 由脚本生成的公司政策、技术规范、入职文档 |
| 本地索引 | [data/rag_index/](./data/rag_index/) | 由脚本生成的 JSON 检索索引 |
| 一键脚本 | [practice/preclass_run.sh](./practice/preclass_run.sh) | 自动执行 L05 环境检查和核心示例 |
| 课堂笔记 | [materials/NOTES_TEMPLATE.md](./materials/NOTES_TEMPLATE.md) | 记录检索结果、失败样例和优化思路 |
| 课后小测 | [materials/MINI_QUIZ.md](./materials/MINI_QUIZ.md) | 检查 RAG 原理和工程判断 |
| 拓展练习 | [materials/EXTENSIONS.md](./materials/EXTENSIONS.md) | rerank、rewrite、PDF、真实向量库、评估集 |
| 面试速查 | [materials/INTERVIEW_QA.md](./materials/INTERVIEW_QA.md) | RAG 基础、工程、Agentic RAG、权限和安全面试题 |
| 注释规范 | [../../CODE_COMMENTING_GUIDE.md](../../CODE_COMMENTING_GUIDE.md) | 阅读和编写课程代码时遵循的讲解标准 |

## 推荐学习路径

1. 阅读 [materials/PRECLASS_CHECKLIST.md](./materials/PRECLASS_CHECKLIST.md)，确认 L01-L04 环境仍然可用。
2. 阅读 [lecture/LECTURE_FULL.md](./lecture/LECTURE_FULL.md) 的 5.1-5.3，理解 RAG 的闭卷/开卷比喻和离线/在线两阶段。
3. 运行 `practice/11_prepare_knowledge_base.py`，生成三份示例公司文档。
4. 运行 `practice/12_build_local_index.py`，观察文档如何被切分、索引和检索。
5. 运行 `practice/13_rag_agent.py --question "我入职2年了，有几天年假？" --show-context`，观察上下文如何增强答案。
6. 运行 `practice/14_chunking_compare.py`，比较不同 chunk size 对召回的影响。
7. 阅读 [教辅资料：BM25 和倒排索引简单介绍](../../teaching_support/BM25_INVERTED_INDEX.md)，理解关键词检索为什么又快又能排序。
8. 阅读 [resources/PDF_RAG_PROCESS.md](./resources/PDF_RAG_PROCESS.md)，理解复杂 PDF 不是简单转文本。
9. 阅读 [materials/INTERVIEW_QA.md](./materials/INTERVIEW_QA.md)，准备 RAG 面试题。
10. 完成 [materials/MINI_QUIZ.md](./materials/MINI_QUIZ.md)，再用 [lecture/CHAPTER_SUMMARY.md](./lecture/CHAPTER_SUMMARY.md) 复盘。

## 快速运行

从课程根目录激活环境：

```bash
source <course-root>/scripts/activate_course.sh
```

进入第五章目录：

```bash
cd <course-root>/lessons/L05_rag
```

生成示例知识库：

```bash
python practice/11_prepare_knowledge_base.py
```

构建本地索引并测试检索：

```bash
python practice/12_build_local_index.py --query "年假有几天？"
```

运行 RAG 问答：

```bash
python practice/13_rag_agent.py --question "我入职2年了，有几天年假？" --show-context
```

比较切分策略：

```bash
python practice/14_chunking_compare.py
```

一键预习检查：

```bash
bash practice/preclass_run.sh
```

通过标志：最后看到 `[OK] L05 preclass run completed.`。

## 本章实操说明

- `practice/rag_common.py`：公共文档、切分、索引、检索、上下文构造和 LLM 调用工具。
- `practice/11_prepare_knowledge_base.py`：创建公司政策、技术规范、入职指南三份示例文档。
- `practice/12_build_local_index.py`：用标准库构建 TF-IDF 风格本地检索索引。
- `practice/13_rag_agent.py`：检索相关 chunk，把上下文和问题一起交给 LLM，生成带引用答案。
- `practice/14_chunking_compare.py`：比较不同 chunk size 下的召回结果，理解切分不是随便定一个数字。

## 本章交付物

- 一张 RAG 离线/在线流程图。
- 一次本地知识库构建日志。
- 一次带引用的 RAG 问答结果。
- 一次 chunk size 对比记录。
- 一份 RAG 失败排查清单。
- 一份 PDF RAG 处理方案：页眉页脚、图片、表格、图表、OCR、metadata、引用。
- 一组面试题复盘：RAG vs 微调、Hybrid Search、Reranker、Agentic RAG、权限、安全、评估。

## 与后续章节的关系

L05 把“检索”变成 Agent 的核心工具。L06 会进一步学习 LangChain 分层架构、LCEL 和自定义 Retriever；L07 会讲记忆系统；L08 会把 RAG 放进 Agent 模式和企业知识库架构中；L11 会把 RAG 的检索与生成效果纳入系统评测。
