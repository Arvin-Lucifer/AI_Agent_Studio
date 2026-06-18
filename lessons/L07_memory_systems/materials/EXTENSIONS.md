# L07 拓展练习

## 1. Token 预算裁剪

把 `21_memory_window.py` 从“按轮数裁剪”改成“按 token 预算裁剪”。

要求：

- system 消息必须保留。
- 最近消息优先保留。
- 输出裁剪前后估算 token 数。

## 2. 结构化摘要

修改 `22_memory_summary.py`，让摘要输出 JSON：

```json
{
  "user_profile": {},
  "preferences": [],
  "open_tasks": [],
  "decisions": []
}
```

## 3. 记忆冲突合并

在 `23_long_term_memory_json.py` 中实现：

```text
用户以前喜欢 Java
用户现在主要用 Python
```

要求新偏好能覆盖旧偏好，旧偏好进入历史记录。

## 4. 遗忘 API

给 JSON 长期记忆增加：

- `forget_profile(key)`
- `forget_fact(memory_id)`
- `forget_preference(memory_id)`
- `show_deleted()`

## 5. Chroma 可选实现

安装 `chromadb` 后，参考 [CHROMA_MEMORY_OPTIONAL.md](../resources/CHROMA_MEMORY_OPTIONAL.md)，把 JSON 检索替换成向量检索。

## 6. 跨用户隔离

把 `data/user_memory.json` 改成：

```text
data/users/{user_id}/memory.json
```

要求：

- 不同 user_id 的记忆不能互相检索。
- `thread_id` 不能直接当可信 user_id。
- user_id 需要来自登录态或可信认证系统。
