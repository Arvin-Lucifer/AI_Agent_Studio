# Chroma 长期记忆可选实现说明

老师讲义中给出了基于 Chroma 的长期记忆版本。本课程默认练习使用标准库 JSON，是为了保证没有安装 `chromadb` 时也能跑通主线。

## 什么时候使用 Chroma

适合：

- 记忆量较大。
- 需要语义检索。
- 用户表达和存储文本不完全一致。
- 需要持久化向量索引。

不适合：

- 只有几十条结构化画像。
- 需要强一致精确查询。
- 没有权限过滤和删除治理。

## Collection 设计

建议拆成三个 collection：

| Collection | 写入语义 | 说明 |
| --- | --- | --- |
| `user_profile` | upsert | key/value 画像，同 key 覆盖 |
| `facts` | add | 事实流，事件式累计 |
| `preferences` | add | 偏好流，后续合并/衰减 |

## 写入语义

- `update_profile()` 用 `upsert(ids=[key])`。
- `save_fact()` 用 `add(ids=[uuid])`。
- `save_preference()` 用 `add(ids=[uuid])`。

## 检索语义

```text
query
  -> facts collection query
  -> preferences collection query
  -> 合并 distance
  -> 按距离、重要性、时间重排
```

## 与知识图谱配合

Chroma 负责语义入口，知识图谱负责关系扩展：

```text
向量命中：用户中心项目
图谱扩展：用户中心项目 -> 使用 -> FastAPI -> 属于类型 -> Web 框架
```

## 课程环境说明

`requirements/rag.txt` 中包含 `chromadb` 和 `langchain-chroma`。若要尝试：

```bash
pip install -r requirements/rag.txt
```

再把 `practice/24_hybrid_memory_graph.py` 中的标准库检索替换为 Chroma collection query。

如果要使用本地 embedding 模型，再额外安装：

```bash
pip install -r requirements/local-embeddings.txt
```

注意：本地 embedding 依赖可能安装 PyTorch/CUDA，体积明显更大；课堂默认主线不依赖它。
