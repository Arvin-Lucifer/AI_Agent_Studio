# L01 课前准备清单（按讲义 1.1 ~ 1.6）

## 一、环境就绪（必须完成）

- [ ] 执行 `source <course-root>/use_proxy.sh`（如需代理）
- [ ] 执行 `source <course-root>/scripts/activate_course.sh`
- [ ] 执行 `python <course-root>/scripts/check_env.py`
- [ ] 执行 `python <course-root>/scripts/smoke_openai.py`
- [ ] 确认 `.env` 中 `OPENAI_API_KEY`、`OPENAI_BASE_URL`、`OPENAI_MODEL` 有效

## 二、实操准备（必须完成）

- [ ] 进入 `cd <course-root>/lessons/L01_agent_basics`
- [ ] 运行 `python practice/01_hello_llm.py`
- [ ] 运行 `python practice/02_multi_turn_chat.py`
- [ ] 在多轮对话里至少完成 5 轮并验证“记住名字”场景
- [ ] 运行 `python practice/demo_chatbot_vs_agent.py --mode both` 并观察两种输出差异

## 三、核心概念预热（必须完成）

- [ ] 我可以用一句话解释什么是 AI Agent
- [ ] 我能说清 ChatBot 与 Agent 的 3 个以上差异
- [ ] 我可以解释 Agent 四大模块：LLM、Planning、Tools、Memory
- [ ] 我可以说出智能体循环：观察、思考、行动、复盘
- [ ] 我可以列出至少 2 个常见风险：幻觉、工具失败、循环不收敛、上下文超限

## 四、准备一个个人场景（必须完成）

示例：

- “整理今天的会议结论并生成行动项”
- “把待办按优先级排好并安排 2 小时专注时段”
- “阅读 3 份资料并输出对比表”

## 五、30 分钟预习路径（建议）

1. 0-8 分钟：阅读 README 的 1.1 ~ 1.4，理解 Agent 全景
2. 8-15 分钟：运行 `practice/01_hello_llm.py`，确认 API 可用
3. 15-22 分钟：运行 `practice/02_multi_turn_chat.py`，体验最小记忆
4. 22-30 分钟：运行 `practice/demo_chatbot_vs_agent.py --mode both` + 完成 `MINI_QUIZ.md`

## 六、上课可提问题（建议）

- 什么时候只用 Prompt 就够了，什么时候必须上 Agent？
- 第一个可上线的 Agent，最小可靠架构应该包含哪些护栏？
- 除了“回答看起来不错”，还能用哪些指标评估 Agent？
