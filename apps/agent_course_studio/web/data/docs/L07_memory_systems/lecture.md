# 第 7 讲：记忆系统 —— 让 Agent 越用越懂你

学习时长：90-120 分钟
配套代码：`practice/21_memory_window.py` 到 `practice/25_agent_with_long_memory.py`
章节总结：[CHAPTER_SUMMARY.md](./CHAPTER_SUMMARY.md)

## 7.1 为什么记忆这么重要？

想象一下，你每天都要和一个同事合作，但他每天早上都忘了昨天说过的所有事。项目背景、你的偏好、之前做过的决定，都要重新解释一遍。

没有记忆的 Agent 就是这样：每次交互都像第一次见面。记忆让 Agent 从“一次性工具”变成“持续成长的助手”。

Agent 的记忆可以分为三层：

```text
短期记忆 Working Memory
当前对话上下文，像工作台，正在处理当前任务。

长期记忆 Long-term Memory
跨对话保存的信息，像笔记本，记录用户画像、偏好、历史任务。

外部知识 External Knowledge
知识库、数据库、文档系统，像图书馆，需要时检索。
```

详细图解见 [MEMORY_ARCHITECTURE.md](../resources/MEMORY_ARCHITECTURE.md)。

## 7.2 短期记忆：对话上下文管理

短期记忆最直观的实现就是把历史 `messages` 传给 LLM。问题在于上下文窗口有限，历史过长后必须裁剪或压缩。

### 策略一：滑动窗口

滑动窗口只保留最近 N 轮对话，并始终保留 system 消息。

示例代码见：

```bash
python practice/21_memory_window.py --max-turns 3
```

优点：

- 实现简单。
- 成本稳定。
- 适合当前任务只依赖最近上下文的场景。

缺点：

- 早期但重要的信息会被丢掉。
- 例如用户第一轮说了姓名或长期偏好，后面可能被窗口裁掉。

### 策略二：摘要压缩

摘要压缩把较早的对话压缩为一条 summary，再保留最近几轮原文：

```text
system 原始规则
system 之前的对话摘要
最近几轮 user/assistant 消息
```

示例代码见：

```bash
python practice/22_memory_summary.py
python practice/22_memory_summary.py --use-llm
```

优点：

- 能保留早期关键信息。
- token 成本比全量历史低。

缺点：

- 摘要可能丢失细节。
- 摘要可能引入幻觉。
- 多次摘要会发生信息漂移。

## 7.3 长期记忆：跨会话信息持久化

短期记忆解决单次会话内的连贯性。真实 Agent 还需要跨会话记住：

- 用户姓名、角色、偏好。
- 历史任务结果。
- 项目背景。
- 用户常用工具、技术栈和工作方式。

### 7.3.1 JSON 长期记忆

最小长期记忆可以直接用 JSON 文件实现：

```text
user_profile: 画像字段，适合覆盖更新
facts: 事实流，适合追加
preferences: 偏好流，适合追加、合并、衰减
deleted: 软删除审计记录
```

示例代码见：

```bash
python practice/23_long_term_memory_json.py --reset --query Python
```

关键设计：

- `update_profile()` 使用覆盖语义，因为姓名、角色等画像字段通常以最新值为准。
- `save_fact()` 使用追加语义，因为事实是事件流，需要保留历史。
- `save_preference()` 也使用追加语义，因为偏好会变化，后续可以通过合并或衰减处理。
- `forget()` 提供显式删除入口，避免长期记忆变成无法控制的隐私风险。

### 7.3.2 Chroma 向量长期记忆

老师讲义给出了 Chroma 版本：把 `user_profile`、`facts`、`preferences` 拆成三个 collection，并复用 OpenAI 兼容 embedding。

这类设计的价值是：

- 搜索从关键词匹配升级为语义检索。
- 搜 “Python” 也可能召回 “FastAPI 后端技术栈”。
- facts/preferences 可以按语义相似度召回。
- profile 使用 upsert，facts/preferences 使用 add。

当前课程默认代码不强制依赖 Chroma，因为本地环境可能没有安装 `chromadb`。可选实现说明见 [CHROMA_MEMORY_OPTIONAL.md](../resources/CHROMA_MEMORY_OPTIONAL.md)。

### 7.3.3 知识图谱长期记忆

向量检索擅长语义相似，但不擅长表达实体之间的关系。知识图谱用三元组表示关系：

```text
小明 -> 负责 -> 用户中心项目
用户中心项目 -> 使用 -> FastAPI
FastAPI -> 属于类型 -> Web 框架
```

这样 Agent 可以做多跳推理：

```text
小明 -> 负责 -> 用户中心项目 -> 使用 -> FastAPI
```

推理出：小明负责的项目使用了 FastAPI。

示例代码见：

```bash
python practice/24_hybrid_memory_graph.py --reset --query Python --anchor 小明
```

本章默认实现使用 JSON 知识图谱和标准库稀疏检索，目的是让学生先理解“向量找入口，图谱沿关系扩展”的思想。

## 7.4 把长期记忆接入 Agent

长期记忆接入 Agent 的关键是把记忆读写封装成工具：

- `save_user_profile`
- `save_user_preference`
- `save_user_fact`
- `recall_user_memory`

示例代码见：

```bash
python practice/25_agent_with_long_memory.py --demo --reset
```

要区分两种记忆：

| 类型 | 示例 | 生命周期 |
| --- | --- | --- |
| 短期会话记忆 | `MemorySaver` + `thread_id` | 进程内检查点 |
| 长期用户记忆 | JSON/Chroma/KG | 跨进程、跨会话 |

Agent 的 system prompt 要明确：

1. 什么时候主动保存用户信息。
2. 什么时候读取用户记忆。
3. 不要编造不存在的记忆。
4. 长期记忆可能过期，关键结论要保守。

## 7.5 记忆检索策略

核心问题是：从海量记忆中找到“对的那条”。

| 策略 | 优点 | 缺点 | 适用场景 |
| --- | --- | --- | --- |
| 纯向量检索 | 语义理解强 | 可能漏精确匹配 | 通用记忆检索 |
| 关键词检索 | 精确稳定 | 无语义理解 | 姓名、ID、技术名 |
| 知识图谱 | 关系推理强 | 构建成本高 | 多实体、多跳关系 |
| 多路召回 | 覆盖全面 | 成本更高 | 生产环境推荐 |

详细说明见 [MEMORY_RETRIEVAL_STRATEGIES.md](../resources/MEMORY_RETRIEVAL_STRATEGIES.md)。

## 7.6 记忆遗忘

长期记忆不能只增不减。

为什么必须遗忘：

1. 存储和索引成本会持续增长。
2. 旧记忆和低质量记忆会污染 TopK。
3. 用户画像和偏好会变化。
4. 隐私与合规要求用户可删除个人数据。

常见策略：

- TTL / 时间窗口。
- 滑动窗口。
- 衰减函数。
- LRU / LFU。
- 重要性打分。
- 摘要压缩。
- 去重和一致性合并。
- 显式删除 / 软删除。

不同记忆类型适合不同策略：

| 记忆类型 | 推荐策略 |
| --- | --- |
| 会话短期上下文 | 滑动窗口 + 摘要 |
| 用户画像 | upsert 覆盖 + 软删除 |
| 偏好 | 衰减 + 一致性合并 |
| 事实流 | 重要性打分 + LRU + TTL |
| 知识图谱三元组 | 一致性合并 + 显式删除 |
| 隐私字段 | 显式删除 + 强制 TTL |

详细说明见 [MEMORY_FORGETTING.md](../resources/MEMORY_FORGETTING.md)。

## 7.7 课堂练习

1. 修改 `21_memory_window.py`，让窗口按 token 预算裁剪，而不是按轮数裁剪。
2. 修改 `22_memory_summary.py`，让摘要保留“用户身份、偏好、未完成任务”三个字段。
3. 给 `23_long_term_memory_json.py` 增加 `--show-deleted` 参数，查看软删除审计记录。
4. 给 `24_hybrid_memory_graph.py` 增加一个实体和两条关系，观察多跳路径是否变化。
5. 运行 `25_agent_with_long_memory.py`，观察 Agent 是否会主动调用保存工具。

## 7.8 面试讨论

面试时不要只说“我把历史消息存起来”。更好的回答是：

- 先区分短期记忆、长期记忆和外部知识。
- 再说明不同记忆类型的写入语义：profile 覆盖、facts 追加、preferences 演化、KG 显式关系。
- 然后讲检索策略：关键词、向量、图谱、多路召回和 rerank。
- 最后讲安全和治理：跨用户隔离、隐私删除、过期、冲突合并、审计。

完整面试题库见 [INTERVIEW_QA.md](../materials/INTERVIEW_QA.md)。
