# L07 课前准备清单

## 1. 环境检查

从课程根目录激活环境：

```bash
source <course-root>/scripts/activate_course.sh
```

检查基础环境：

```bash
python scripts/check_env.py
python scripts/smoke_openai.py
```

## 2. 概念预习

- [ ] 我能解释短期记忆、长期记忆和外部知识的区别。
- [ ] 我知道 `messages` 是最小短期记忆。
- [ ] 我知道 `MemorySaver` 不是生产级长期记忆。
- [ ] 我能解释为什么长期记忆需要“遗忘机制”。
- [ ] 我知道用户画像、事实流、偏好和知识图谱适合不同写入策略。

## 3. 代码预习

```bash
cd <course-root>/lessons/L07_memory_systems
python practice/21_memory_window.py --max-turns 3
python practice/23_long_term_memory_json.py --reset --query Python
```

确认能看到：

- 滑动窗口前后消息数量变化。
- `data/user_memory.json` 被创建。
- 搜索 `Python` 能命中偏好或事实。

## 4. 课前思考

- 如果用户第一轮告诉 Agent 自己的姓名，滑动窗口会不会丢掉它？
- 哪些信息应该写入长期记忆，哪些不应该？
- 用户说“请忘记我的手机号”时，系统应该怎么做？
- 如果用户以前喜欢 Java，现在改用 Python，Agent 应该相信哪条记忆？

## 5. 30 分钟预习路径

1. 0-8 分钟：阅读 README 和讲义 7.1-7.2。
2. 8-14 分钟：运行 `practice/21_memory_window.py`。
3. 14-20 分钟：运行 `practice/22_memory_summary.py`。
4. 20-25 分钟：运行 `practice/23_long_term_memory_json.py --reset --query Python`。
5. 25-30 分钟：阅读 `resources/MEMORY_FORGETTING.md` 的策略表。
