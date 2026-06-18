# L01 拓展练习（讲义 1.6 对齐）

## 必做练习

- 运行 `practice/02_multi_turn_chat.py`，连续对话 5 轮以上，观察模型是否保持上下文。
- 在 `practice/02_multi_turn_chat.py` 里修改 system prompt，分别扮演：
  - Python 教师
  - 健身教练
  - 面试官
- 记录每个角色的回答风格差异（语气、结构、建议方式）。

## 入门拓展（约 30 分钟）

- 把 `practice/01_hello_llm.py` 的用户问题改成你工作中的真实问题。
- 把 `practice/demo_chatbot_vs_agent.py` 的目标替换成你的日常场景。
- 对比“纯回答”与“工具增强”的可执行性差异。

## 进阶拓展（约 60-90 分钟）

- 给 `practice/02_multi_turn_chat.py` 增加一条命令（如 `clear`）用于重置会话记忆。
- 给 `practice/demo_chatbot_vs_agent.py` 增加第二个工具（如简单日历/待办工具）。
- 增加最大步数护栏（如 `max_steps=3`）避免循环不收敛。

## 高阶拓展（半天）

- 把模拟工具替换为真实工具（搜索接口、日历 API、本地数据库）。
- 设计一个小型评估表：正确性、可执行性、延迟、成本。
- 准备 10 组输入，对比 ChatBot 模式与 Agent 模式表现。

## 复盘问题

- 在你的业务场景里，瓶颈是模型推理，还是工具能力？
- 哪一步最容易失败？你准备加什么护栏？
