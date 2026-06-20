# L11 课前检查清单

## 环境

- [ ] 已激活 `agent_course` conda 环境。
- [ ] 已安装 `requirements/core.txt`、`requirements/langchain.txt` 和 `requirements/deployment.txt`。
- [ ] `fastapi`、`uvicorn`、`sse-starlette` 可导入。

检查命令：

```bash
source <course-root>/scripts/activate_course.sh
python -c "import fastapi, uvicorn, sse_starlette; print('ok')"
```

## 概念

- [ ] 我能说出 Agent 评估的六个维度。
- [ ] 我知道为什么只做关键词匹配不够。
- [ ] 我知道为什么要检查工具调用 trace。
- [ ] 我能解释 `/health` 为什么不应该调用模型。
- [ ] 我知道 SSE 和一次性返回的差别。
- [ ] 我知道 Nginx 代理 SSE 时为什么要关闭缓冲。

## 代码预习

```bash
cd <course-root>/lessons/L11_eval_and_deployment
bash practice/preclass_run.sh
```

观察点：

- `data/eval_dataset.json` 是否生成。
- `data/eval_results.json` 是否生成。
- `/chat` self-test 是否返回 `5天`。
- 流式 self-test 是否包含 `tool_call` 和 `done`。
- 成本和安全脚本是否输出结构化结果。

## 预习阅读

1. [lecture/LECTURE_FULL.md](../lecture/LECTURE_FULL.md)
2. [resources/EVALUATION_SYSTEM_DESIGN.md](../resources/EVALUATION_SYSTEM_DESIGN.md)
3. [resources/FASTAPI_DEPLOYMENT_RUNBOOK.md](../resources/FASTAPI_DEPLOYMENT_RUNBOOK.md)
