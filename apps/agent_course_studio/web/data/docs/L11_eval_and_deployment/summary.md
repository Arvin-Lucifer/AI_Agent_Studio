# L11 章节总结：评测和部署

## 一句话

Agent 从 Demo 到生产，需要两件事：用评测证明它好用，用部署让它稳定可用。

## 评估维度

| 维度 | 关注点 |
| --- | --- |
| 准确性 | 答案是否正确 |
| 完整性 | 是否遗漏关键信息 |
| 相关性 | 是否紧扣问题 |
| 安全性 | 是否泄露信息、越权或被注入 |
| 效率/成本 | 工具次数、token、延迟 |
| 鲁棒性 | 空输入、长输入、恶意输入 |

## 评测集要包含

- 正常事实问答。
- 闲聊和不该调用工具的请求。
- 空输入、超长输入。
- Prompt Injection。
- 多子问题完整性。
- 无答案拒答。

## 代码地图

- `practice/eval_deploy_common.py`：评测数据结构、mock Agent、评分器、成本和安全工具。
- `practice/44_eval_dataset.py`：生成评测数据集。
- `practice/45_eval_runner.py`：运行自动化评测并保存结果。
- `practice/46_failure_tuning_playbook.py`：常见翻车场景和修复策略。
- `practice/47_agent_api.py`：FastAPI 同步接口。
- `practice/48_agent_api_streaming.py`：SSE 流式接口。
- `practice/49_cost_monitor.py`：成本监控。
- `practice/50_safety_guardrails.py`：Prompt 注入输入防护。
- `practice/chat_frontend.html`：最小前端页面。

## 常见翻车

- 幻觉：无证据编造。
- 死循环：重复调用同一个工具。
- 工具误调：不该查知识库却查了，或该查却没查。
- 格式错乱：JSON 不合法。
- Prompt 注入：绕过系统约束。
- 成本失控：简单请求走复杂链路。

## 部署关键点

- `/health` 必须轻量，不能调用模型。
- API 请求和响应要结构化。
- 流式输出用 SSE 时，Nginx 要关闭缓冲。
- Gunicorn 管理多个 Uvicorn worker。
- 日志里记录 session_id、延迟、工具调用、安全标记和错误类型。
- 密钥只放环境变量，不写进代码和日志。

## 面试金句

> Agent 评估不能只看最终答案，还要看工具选择、参数、引用、安全和成本。

> 部署不是把脚本挂到服务器上，而是让 Agent 具备健康检查、日志、监控、限流、回滚和安全边界。
