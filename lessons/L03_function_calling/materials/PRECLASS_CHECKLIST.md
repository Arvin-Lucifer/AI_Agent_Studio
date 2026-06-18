# L03 课前准备清单

## 一、环境就绪

- [ ] 执行 `source <course-root>/scripts/activate_course.sh`
- [ ] 执行 `python <course-root>/scripts/check_env.py`
- [ ] 执行 `python <course-root>/scripts/smoke_openai.py`
- [ ] 确认 `.env` 中 `OPENAI_API_KEY`、`OPENAI_BASE_URL`、`OPENAI_MODEL` 有效

## 二、实操准备

- [ ] 进入 `cd <course-root>/lessons/L03_function_calling`
- [ ] 运行 `python practice/05_function_calling.py --demo`
- [ ] 运行 `python practice/06_parallel_function_calling.py --demo`
- [ ] 记录一次 tool call 的工具名、参数和返回结果

## 三、核心概念预热

- [ ] 我能解释 Function Calling 和纯文本 JSON 输出的区别
- [ ] 我能写出一个简单 function schema
- [ ] 我能说清模型负责决策、代码负责执行
- [ ] 我能列出至少 5 类工具调用失败类型
- [ ] 我能说出至少 3 个工具安全风险

## 四、30 分钟预习路径

1. 0-8 分钟：阅读 README 和讲义 3.1-3.3
2. 8-16 分钟：运行 `practice/05_function_calling.py --demo`
3. 16-22 分钟：运行 `practice/06_parallel_function_calling.py --demo`
4. 22-26 分钟：阅读 `resources/TOOL_ERROR_RECOVERY.md`
5. 26-30 分钟：完成 `MINI_QUIZ.md`
