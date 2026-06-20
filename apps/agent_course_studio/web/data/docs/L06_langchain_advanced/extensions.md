# L06 拓展练习

## 必做：新增 LCEL 链

在 `16_lcel_composition.py` 中新增一条链：

```text
输入文章 -> 翻译英文 -> 摘要 -> 改写成商务风格
```

要求：

- 每一步用独立 prompt。
- 打印每一步中间结果。
- 分析串联链的错误传播风险。

## 必做：自定义 Parser 结构

在 `17_output_parsers.py` 中新增一个 Pydantic 模型，例如：

- 会议纪要结构。
- Bug 报告结构。
- 需求分析结构。

要求字段有描述、类型和必要校验。

## 选做：Retriever 融合排序

改进 `18_custom_retriever.py`：

- 增加标题命中权重。
- 增加 source 权威权重。
- 把去重 key 改为 `source + chunk_id`。
- 打印每个候选的分数组成。

## 选做：Callback 日志持久化

改进 `19_callbacks.py`：

- 将事件写入 JSONL 文件。
- 给每次运行分配 run_id。
- 记录耗时、输入摘要、输出摘要、错误。

## 进阶：文档处理 Agent

改进 `20_doc_processor_agent.py`：

- 增加风险点提取。
- 增加受众定制报告。
- 把报告保存成 Markdown。
- 接入 L05 的 RAG 检索作为背景知识。
