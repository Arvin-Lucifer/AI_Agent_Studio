# L11 拓展练习

## 练习 1：扩展评测集

在 `practice/eval_deploy_common.py` 中新增 10 条 case，至少覆盖：

- 无答案拒答。
- 工具失败。
- 多工具问题。
- Prompt Injection。
- 超长输入。
- 引用正确率。

运行：

```bash
python practice/45_eval_runner.py
```

## 练习 2：接入真实 RAG Agent

把 `MockAgent` 替换成 L05 的 RAG Agent。

要求返回结构：

```json
{
  "answer": "...",
  "tool_calls": ["search_knowledge_base"],
  "citations": ["..."],
  "elapsed_ms": 1200
}
```

## 练习 3：实现 `/chat/rag`

基于 `practice/47_agent_api.py` 新增接口：

```text
POST /chat/rag
```

要求：

- 接收 `message` 和 `session_id`。
- 返回答案、引用、检索片段和耗时。
- 空输入返回 400。

## 练习 4：前端增强

扩展 `practice/chat_frontend.html`：

- 显示工具调用时间。
- 显示引用来源。
- 增加错误状态。
- 增加“清空会话”按钮。

## 练习 5：CI 评测门禁

写一个脚本，当平均分低于 0.8 或安全 case 失败时退出非 0。

适合接入 CI/CD：

```bash
python practice/45_eval_runner.py
```

## 练习 6：部署 Runbook

为你的云服务器写一份部署说明，包含：

- 代码上传。
- 环境变量。
- Gunicorn 启动命令。
- Nginx 配置。
- 健康检查。
- 回滚步骤。
