# L02 课前准备清单（按讲义 2.1 ~ 2.7）

## 一、环境就绪（必须完成）

- [ ] 执行 `source <course-root>/use_proxy.sh`（如需代理）
- [ ] 执行 `source <course-root>/scripts/activate_course.sh`
- [ ] 执行 `python <course-root>/scripts/check_env.py`
- [ ] 执行 `python <course-root>/scripts/smoke_openai.py`
- [ ] 确认 `.env` 中 `OPENAI_API_KEY`、`OPENAI_BASE_URL`、`OPENAI_MODEL` 有效

## 二、实操准备（必须完成）

- [ ] 进入 `cd <course-root>/lessons/L02_prompt_engineering`
- [ ] 运行 `python practice/03_structured_output.py`
- [ ] 观察结构化输出是否可被 `json.loads` 解析
- [ ] 运行 `python practice/04_prompt_iteration.py`
- [ ] 记录 V1 与 V2 Prompt 的输出差异（至少 2 点）
- [ ] 阅读 `resources/SYSTEM_PROMPT_REFERENCES.md`，选择一个真实产品 prompt 做结构标注
- [ ] 阅读 `resources/PROMPT_EXAMPLES.md`，任选一个 Few-Shot 或 CoT 示例改写成自己的场景

## 三、核心概念预热（必须完成）

- [ ] 我可以解释为什么 Prompt 是 Agent 的“灵魂”
- [ ] 我可以说出 3 类 Prompt：System / User / Few-shot
- [ ] 我可以复述 System Prompt 的 5 要素
- [ ] 我可以解释 Few-shot、CoT、ReAct 三种模式的区别
- [ ] 我可以说明为什么结构化输出对工程落地重要

## 四、准备一个真实业务场景（必须完成）

示例：

- “代码 Review 助手：输入代码，输出改进建议与风险等级”
- “客服意图识别：输入用户消息，输出 JSON 分类与置信度”
- “会议纪要抽取：输入文本，输出 action items JSON”

## 五、30 分钟预习路径（建议）

1. 0-8 分钟：阅读 README 的 2.1 ~ 2.3，建立 Prompt 框架
2. 8-14 分钟：运行 `practice/03_structured_output.py`，看结构化输出与解析兜底
3. 14-20 分钟：运行 `practice/04_prompt_iteration.py`，比较 V1/V2 差异
4. 20-24 分钟：阅读 `resources/SYSTEM_PROMPT_REFERENCES.md` 的推荐学习路径
5. 24-28 分钟：阅读 `resources/PROMPT_EXAMPLES.md` 的 Few-Shot/CoT 使用原则
6. 28-30 分钟：完成 `MINI_QUIZ.md`

## 六、上课可提问题（建议）

- 在生产环境里，怎么评估 Prompt 是否“足够稳定”？
- 什么时候应该增加 Few-shot，什么时候应该简化 Prompt？
- JSON 输出失败时，应该重试还是回退到兜底逻辑？
