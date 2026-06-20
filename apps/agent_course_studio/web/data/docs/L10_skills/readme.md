# L10 Skill 相关：让 Agent 能力模块化复用

本章进入 Agent 能力工程化：Tool 只是原子动作，Skill 是围绕稳定用户意图组织起来的能力包。它把触发条件、执行步骤、上下文知识、工具集合、输出格式、安全边界和评测闭环沉淀成可复用模块。

## 本章学习目标

- 理解从 Chatbot 到 Agent 的关键跃迁：裸 LLM 只能“说话”，Agent 需要可复用 Skill 去“做事”。
- 掌握 Tool、Skill、MCP 三层架构：Tool 是原子操作，Skill 是能力包，MCP 是连接标准。
- 能区分 Function Calling、MCP、A2A 的定位：怎么调用、怎么连接、怎么协作。
- 掌握 SKILL.md 结构：元信息层、指令层、执行层。
- 用 DDICE 五步法设计 Skill：Define、Decompose、Instrument、Constrain、Evaluate。
- 跑通天气查询、代码审查、办公助手渐进加载三个 Skill 示例。
- 理解渐进披露：启动时只加载 metadata，触发后再加载完整指令和工具。
- 能从边界、契约、执行、观测、安全和评测六个角度评价一个 Skill。
- 掌握 Tool 层、Skill 层和编排层的重试边界，避免重试风暴。
- 掌握并行编排中的长尾延迟优化：关键路径剥离、提前启动、分片并发、软超时、对冲和缓存。
- 掌握“以后都自动发”的授权落地：窄范围、有时效、可撤销、可审计。
- 掌握“照网页里的要求执行”这类外部内容授权场景：网页内容是数据，不是新的指令源。
- 掌握高风险 Skill 误触发后的损失控制：止血、评估、补救、告知和结构加固。
- 掌握模型升级和 Skill 发布的回滚设计：版本快照、灰度、指标触发和分级回滚。

## 文件分区

| 分类 | 路径 | 用途 |
| --- | --- | --- |
| 讲义 | [lecture/LECTURE_FULL.md](./lecture/LECTURE_FULL.md) | 第 10 讲完整讲义：Skill 概念、设计方法、案例和工程补充专题 |
| 总结 | [lecture/CHAPTER_SUMMARY.md](./lecture/CHAPTER_SUMMARY.md) | 核心概念、代码地图和面试复盘 |
| Skill 示例 | [skills/](./skills/) | `weather-query`、`code-reviewer`、`office-skill` 的 SKILL.md |
| 实操代码 | [practice/](./practice/) | Skill Loader、天气 Skill、代码审查 Skill、办公路由 Skill、重试分层、长尾延迟、自动授权、网页授权边界、事故响应、模型回滚演示 |
| 一键脚本 | [practice/preclass_run.sh](./practice/preclass_run.sh) | 自动执行 L10 环境检查和核心示例 |
| 课前准备 | [materials/PRECLASS_CHECKLIST.md](./materials/PRECLASS_CHECKLIST.md) | 环境、概念和代码预习检查 |
| 课堂笔记 | [materials/NOTES_TEMPLATE.md](./materials/NOTES_TEMPLATE.md) | 记录 Skill 设计、触发规则和评测方案 |
| 课后小测 | [materials/MINI_QUIZ.md](./materials/MINI_QUIZ.md) | 检查 Skill 核心概念 |
| 拓展练习 | [materials/EXTENSIONS.md](./materials/EXTENSIONS.md) | 学术论文 Skill、真实 LLM 路由、评测集和安全机制 |
| 面试题库 | [materials/INTERVIEW_QA.md](./materials/INTERVIEW_QA.md) | Skill 概念、设计、编排、安全、评测和评分标准 |
| 工程参考 | [resources/](./resources/) | Tool/Skill/MCP、DDICE、渐进披露、安全评测、重试分层、长尾延迟、自动授权、网页授权边界、误触发事故响应、模型升级回滚 |
| 运行数据 | [data/](./data/) | 后续 Skill 评测样本和运行 trace |

## 推荐学习路径

1. 阅读 [lecture/LECTURE_FULL.md](./lecture/LECTURE_FULL.md) 的 10.1-10.3，先建立 Tool、Skill、MCP 的层级认知。
2. 阅读 `skills/weather-query/SKILL.md`，理解一个最小 Skill 如何声明触发条件、执行步骤和输出约束。
3. 运行 `practice/34_skill_loader.py`，观察 SKILL.md 如何被发现和解析。
4. 运行 `practice/35_weather_skill_agent.py`，理解 Skill 如何组合天气和空气质量两个 Tool。
5. 运行 `practice/36_code_review_skill.py`，理解代码审查 Skill 如何固化检查维度和输出结构。
6. 运行 `practice/37_office_skill_router.py`，理解路由 Skill + 子 Skill 的渐进披露。
7. 阅读 [resources/SKILL_DESIGN_DDICE.md](./resources/SKILL_DESIGN_DDICE.md)，用 DDICE 方法重新设计一个自己的 Skill。
8. 阅读 [resources/RETRY_STRATEGY_LAYERING.md](./resources/RETRY_STRATEGY_LAYERING.md)，理解 Tool/Skill/编排层各自重试什么。
9. 运行 `practice/42_retry_strategy_layering.py`，观察网络超时、幂等写入、权限错误和重试风暴的分层处理。
10. 阅读 [resources/PARALLEL_TAIL_LATENCY_OPTIMIZATION.md](./resources/PARALLEL_TAIL_LATENCY_OPTIMIZATION.md)，理解并行编排为什么会被最慢分支拖住。
11. 运行 `practice/43_parallel_tail_latency.py`，观察关键路径剥离、分片并发和软超时如何优化 tail latency。
12. 阅读 [resources/AUTO_SEND_AUTHORIZATION_POLICY.md](./resources/AUTO_SEND_AUTHORIZATION_POLICY.md)，理解“以后都自动发”如何落成受限策略。
13. 运行 `practice/41_auto_send_authorization.py`，观察自动授权的接受、降级、拒绝和执行前校验。
14. 阅读 [resources/WEB_INSTRUCTION_AUTHORIZATION.md](./resources/WEB_INSTRUCTION_AUTHORIZATION.md)，理解外部网页内容如何进入 Skill 执行链。
15. 运行 `practice/39_web_instruction_boundary.py`，观察 prompt injection、私域写入和对外动作如何分级处理。
16. 阅读 [resources/HIGH_RISK_SKILL_MISFIRE_RESPONSE.md](./resources/HIGH_RISK_SKILL_MISFIRE_RESPONSE.md)，理解高风险 Skill 误触发后的处置顺序。
17. 运行 `practice/40_high_risk_skill_incident_response.py`，观察不同事故场景如何生成止损和告知方案。
18. 阅读 [resources/MODEL_UPGRADE_ROLLBACK.md](./resources/MODEL_UPGRADE_ROLLBACK.md)，理解模型升级不是只回滚 `model_id`。
19. 运行 `practice/38_model_rollback_playbook.py`，观察 L1-L4 分级回滚决策。
20. 阅读 [教辅资料：AI Native 的工作方式](../../teaching_support/AI_NATIVE_WORKFLOW.md)，理解统一 Skill、统一任务入口和组织级 Agent 的关系。
21. 阅读 [materials/INTERVIEW_QA.md](./materials/INTERVIEW_QA.md)，准备 Skill 面试题。
22. 完成 [materials/MINI_QUIZ.md](./materials/MINI_QUIZ.md)，再用 [lecture/CHAPTER_SUMMARY.md](./lecture/CHAPTER_SUMMARY.md) 复盘。

## 快速运行

```bash
source <course-root>/scripts/activate_course.sh
cd <course-root>/lessons/L10_skills
```

发现 Skill：

```bash
python practice/34_skill_loader.py
```

运行天气 Skill：

```bash
python practice/35_weather_skill_agent.py --query "北京今天天气怎么样？适合出门吗？"
```

运行代码审查 Skill：

```bash
python practice/36_code_review_skill.py
```

运行办公路由 Skill：

```bash
python practice/37_office_skill_router.py
```

运行重试分层演示：

```bash
python practice/42_retry_strategy_layering.py --scenario network_timeout
```

运行并行长尾延迟优化演示：

```bash
python practice/43_parallel_tail_latency.py --scenario critical_path
```

运行自动发授权演示：

```bash
python practice/41_auto_send_authorization.py --scenario daily_report
```

运行网页授权边界演示：

```bash
python practice/39_web_instruction_boundary.py --scenario mixed_prompt_injection
```

运行高风险 Skill 误触发事故响应演示：

```bash
python practice/40_high_risk_skill_incident_response.py --scenario internal_email
```

运行模型升级回滚演示：

```bash
python practice/38_model_rollback_playbook.py --scenario skill_regression
```

一键预习检查：

```bash
bash practice/preclass_run.sh
```

通过标志：最后看到 `[OK] L10 preclass run completed.`。

## 当前整理范围

本版 L10 基于你当前提供的第 10 讲完整材料整理：Skill 主讲义、Agent 开发面试 Skill 题库、模型升级回滚补充、网页授权边界补充、高风险 Skill 误触发补充、“以后都自动发”授权补充、重试策略分层补充，以及并行长尾延迟优化补充。
