# L05 课前准备清单

## 1. 环境检查

激活课程环境：

```bash
source <course-root>/scripts/activate_course.sh
```

基础检查：

```bash
cd <course-root>
python scripts/check_env.py
python scripts/smoke_openai.py
```

本章练习代码默认使用 Python 标准库 + OpenAI SDK，可在未安装向量库时运行。若要尝试 Chroma/FAISS 生产路线，可安装：

```bash
pip install -r requirements/rag.txt
```

## 2. 概念预习

- RAG = 检索 + 增强 + 生成。
- 离线阶段：解析、清洗、切分、索引。
- 在线阶段：query、检索、rerank、上下文、生成。
- Chunk size 和 overlap 会影响召回质量。
- 引用来源是 RAG 和普通聊天的重要区别。

## 3. 代码预习

```bash
cd <course-root>/lessons/L05_rag
python practice/11_prepare_knowledge_base.py
python practice/12_build_local_index.py --query "年假有几天？"
```

## 4. 课前思考

- 为什么不能把整份文档都塞给模型？
- 如果知识库里没有答案，RAG 应该怎么回答？
- 为什么 PDF 不能简单转纯文本？
- 如果检索结果正确但最终答案错误，可能是哪一环出问题？
