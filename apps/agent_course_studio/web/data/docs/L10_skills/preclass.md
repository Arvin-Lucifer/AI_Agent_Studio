# L10 课前准备清单

## 1. 环境检查

```bash
source <course-root>/scripts/activate_course.sh
python scripts/check_env.py
python scripts/smoke_openai.py
python -c "import yaml; print('pyyaml ok')"
```

## 2. 概念预习

- [ ] 我能区分 Tool、Skill、Workflow。
- [ ] 我能解释为什么不能把所有能力都直接暴露成 Tool。
- [ ] 我知道 SKILL.md 的三层结构：元信息层、指令层、执行层。
- [ ] 我能说出 DDICE 五步法。
- [ ] 我理解渐进披露为什么能减少上下文占用和误选工具。
- [ ] 我知道哪些 Skill 动作必须做人机确认。
- [ ] 我能区分 Tool 层重试、Skill 层重试和编排层降级。
- [ ] 我知道并行编排的 P99 会被最慢分支拖住，并能说出至少三种优化方式。
- [ ] 我知道“以后都自动发”必须落成受限策略，而不是无限期取消确认。
- [ ] 我知道网页内容应被当作非可信数据，而不是新的指令源。
- [ ] 我能说出高风险 Skill 误触发后的止血、评估、补救、告知和加固顺序。

## 3. 代码预习

```bash
cd <course-root>/lessons/L10_skills
python practice/34_skill_loader.py
python practice/35_weather_skill_agent.py --query "北京今天天气怎么样？适合出门吗？"
python practice/36_code_review_skill.py
python practice/37_office_skill_router.py
python practice/42_retry_strategy_layering.py --scenario network_timeout
python practice/43_parallel_tail_latency.py --scenario critical_path
python practice/41_auto_send_authorization.py --scenario daily_report
python practice/39_web_instruction_boundary.py --scenario mixed_prompt_injection
python practice/40_high_risk_skill_incident_response.py --scenario internal_email
python practice/38_model_rollback_playbook.py --scenario skill_regression
```

观察：

- `34_skill_loader.py` 是否发现所有 SKILL.md。
- 天气 Skill 是否组合天气和空气质量两个 Tool。
- 代码审查 Skill 是否识别 SQL 注入风险。
- 办公助手是否先路由，再按需加载子 Skill。
- 重试分层演示是否把网络超时放在 Tool 层处理。
- 并行长尾延迟演示是否把慢分支从主响应关键路径剥离。
- 自动发授权演示是否生成 policy，并在首次执行时要求 dry-run。
- 网页授权边界演示是否丢弃 prompt injection，并把邮件发送要求标为需要确认。
- 误触发事故响应演示是否输出黄金 5 分钟止血、用户告知和 24 小时临时围栏。
- 模型升级回滚演示是否给出 L2 或 L3/L4 分级动作。

## 4. 课前思考

- 为什么 Skill 描述里的“何时不使用”很重要？
- 如果一个 Skill 误触发了发送邮件，会带来什么风险？
- 如果 Skill 太细或太粗，会分别造成什么问题？
- 什么时候应该做成高阶 Skill，什么时候应该拆成多个 Skill 编排？
- 为什么编排层不应该继续包一层重试？
- 并行编排中，哪些结果可以 pending 后补，哪些必须阻塞主响应？
- 用户说“以后都自动发”时，哪些情况仍然要二次确认？
- 如果用户说“照网页执行”，哪些网页要求仍然必须拒绝或确认？
- 如果误触发已经发生，为什么不能先追根因再止血？

## 5. 30 分钟预习路径

1. 0-8 分钟：阅读 README 和讲义 10.1-10.4。
2. 8-14 分钟：阅读 `skills/weather-query/SKILL.md` 并运行天气示例。
3. 14-20 分钟：运行代码审查 Skill，观察结构化 findings。
4. 20-25 分钟：运行办公路由 Skill，理解渐进披露。
5. 25-30 分钟：阅读 `resources/SKILL_SAFETY_AND_EVALUATION.md`、`resources/RETRY_STRATEGY_LAYERING.md`、`resources/PARALLEL_TAIL_LATENCY_OPTIMIZATION.md`、`resources/AUTO_SEND_AUTHORIZATION_POLICY.md`、`resources/WEB_INSTRUCTION_AUTHORIZATION.md` 和 `resources/HIGH_RISK_SKILL_MISFIRE_RESPONSE.md`。
