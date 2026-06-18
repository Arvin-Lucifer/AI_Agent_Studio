# Intent Classifier Prompt

默认实现使用规则分类，真实 LLM 接入时保持以下输出：

```json
{"intent": "qa|consult|complaint|unclear|out_of_scope", "reason": "..."}
```
