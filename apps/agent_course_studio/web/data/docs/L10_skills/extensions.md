# L10 拓展练习

## 练习 1：学术论文阅读助手 Skill

按老师作业要求，为“学术论文阅读助手”设计 `SKILL.md`，包含：

- 论文检索。
- 摘要生成。
- 引用提取。

评分维度：

- frontmatter 是否完整。
- 触发条件是否精准。
- 执行步骤是否清晰。
- 注意事项是否覆盖边界情况。
- 是否方便扩展子能力。

## 练习 2：真实 LLM 路由

把 `practice/37_office_skill_router.py` 的规则路由替换为 LLM JSON 路由：

- 输出 `skills` 数组。
- 输出 `reason`。
- 路由失败时回退到规则路由。
- 保留 trace，便于排查误触发。

## 练习 3：给 Weather Skill 加评测集

在 `data/weather_eval.json` 中写入：

- 标准天气问题。
- 未指定城市问题。
- 旅游攻略负例。
- 空气质量问题。

统计：

- 正确触发率。
- 漏触发率。
- 误触发率。

## 练习 4：高风险动作确认机制

修改 `office_skill_router.py`：

- `create_event` 和 `send_email` 只返回 preview。
- 用户传入 `--confirm` 时才把状态改为 `created_mock` / `sent_mock`。
- 记录审计日志到 `data/office_audit.jsonl`。

## 练习 5：代码审查 Skill 增强

为 `36_code_review_skill.py` 增加：

- 硬编码 token 检测。
- 路径遍历检测。
- 空输入处理。
- 多文件输入。
- `--format markdown/json` 输出模式。

## 练习 6：模型升级回滚演练

扩展 `practice/38_model_rollback_playbook.py`：

- 增加 `--scenario false_trigger_spike`。
- 增加按 Skill 维度的指标，例如 `email-notifier` 和 `weather-query` 分开评估。
- 输出一份 runbook markdown。
- 模拟回滚后清理缓存 key。

## 练习 7：网页授权边界增强

扩展 `practice/39_web_instruction_boundary.py`：

- 增加 `--trusted-domain` 参数，把可信域名白名单显式传入。
- 增加网页片段来源定位，例如 `line_no` 或 `section_title`。
- 把审计日志写入 `data/web_instruction_audit.jsonl`。
- 增加一个“申请表提交”场景：生成草稿可以执行，提交动作必须逐项确认。
- 为 prompt injection、HTTP 来源、标题内容不符、跨账号操作分别写评测样本。

## 练习 8：高风险 Skill 误触发演练

扩展 `practice/40_high_risk_skill_incident_response.py`：

- 增加 `--scenario customer_notification`，模拟客户群发误触发。
- 输出一份用户告知 markdown 模板。
- 把事故响应写入 `data/skill_incident_audit.jsonl`。
- 增加 24 小时临时围栏的过期时间和 owner。
- 为每个事故场景补充“复盘后应加入回归集的样本”。

## 练习 9：自动发授权规则表

扩展 `practice/41_auto_send_authorization.py`：

- 把授权策略写入 `data/automation_rules.json`。
- 增加自然语言撤销：“停止自动发日报”。
- 增加“显示所有自动化规则”列表输出。
- 把每次自动执行写入 `data/automation_audit.jsonl`。
- 增加异常环境检测：凌晨、非常用设备、异地登录。

## 练习 10：重试预算与熔断

扩展 `practice/42_retry_strategy_layering.py`：

- 增加 `--scenario circuit_breaker_open`。
- 增加全链路 retry budget 计数器，超过 4 次直接 fail-fast。
- 增加 `idempotency_key` 缺失的非幂等写入场景。
- 输出结构化字段：`retriable`、`failed_step`、`user_action_required`。
- 把每次重试记录写入 `data/retry_trace.jsonl`。

## 练习 11：并行长尾延迟优化

扩展 `practice/43_parallel_tail_latency.py`：

- 增加 `--scenario io_streaming`，模拟大文件下载边读边处理。
- 增加下游 QPS 配额参数，自动计算最大 fan-out 分片数。
- 增加 `pending` 结果的前端轮询响应格式。
- 增加 hedging 的额外成本统计。
- 把每个分支的 trace 写入 `data/parallel_trace.jsonl`。
