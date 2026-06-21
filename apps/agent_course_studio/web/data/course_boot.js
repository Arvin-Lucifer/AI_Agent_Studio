window.AGENT_COURSE_DATA = {
  "schemaVersion": 1,
  "contentVersion": "eb6b8cbf5203478d",
  "course": {
    "name": "AgentCraft Studio",
    "subtitle": "AI Agent 开发实战工作台",
    "description": "从 Agent 基础、Prompt、Function Calling、LangChain、RAG、Memory、MCP、Skill，到评测部署和智能客服毕业项目，把知识练成可交付作品。"
  },
  "stats": {
    "lessonCount": 12,
    "practiceCount": 72,
    "resourceCount": 48,
    "interviewCount": 11,
    "fileCount": 336
  },
  "lessons": [
    {
      "id": "L01_agent_basics",
      "code": "L01",
      "title": "L01 Agent 全景认知：从 ChatBot 到自主智能体",
      "intro": "本章是课程入口，目标不是一开始就写复杂 Agent，而是建立一套稳定的判断框架：什么是 Agent、它和普通 ChatBot 差在哪里、一个最小 Agent 需要哪些模块，以及如何用 Python 跑通第一个 LLM 调用。",
      "topics": [
        "Agent 基础",
        "ChatBot vs Agent",
        "LLM 调用",
        "Planning",
        "Tools",
        "Memory"
      ],
      "goals": [
        "能用一句话解释什么是 AI Agent。",
        "能说清 ChatBot 与 Agent 的关键差异。",
        "理解 Agent 的四个核心模块：LLM、Planning、Tools、Memory。",
        "跑通第一个 LLM API 调用和一个多轮对话程序。",
        "通过最小示例观察“聊天模式”和“智能体循环模式”的区别。"
      ],
      "deliverables": [
        "一句话定义 AI Agent。",
        "一张 ChatBot 与 Agent 的差异表。",
        "一次成功的 `practice/01_hello_llm.py` 运行结果。",
        "一次多轮对话“记住名字”验证。",
        "一个与你自己工作相关的 Agent 场景拆解：目标、所需工具、步骤、潜在失败点和护栏。"
      ],
      "docs": [
        {
          "key": "readme",
          "label": "章节入口",
          "path": "lessons/L01_agent_basics/README.md",
          "contentPath": "data/docs/L01_agent_basics/readme.md",
          "excerpt": "# L01 Agent 全景认知：从 ChatBot 到自主智能体 本章是课程入口，目标不是一开始就写复杂 Agent，而是建立一套稳定的判断框架：什么是 Agent、它和普通 ChatBot 差在哪里、一个最小 Agent 需要哪些模块，以及如何用 Python 跑通第一个 LLM 调用。 ## 本章学习目标 - 能用一句话解释什么是 AI Agent。 - 能说清 ChatBot 与 Agent 的关键差异。 - 理解 Agent 的四个核心模块：LLM、Planning、Tools、Memory。 - 跑通第一个 LLM API 调用和一个多轮对话程序。 - 通过最小示例观察“聊天模式”和“智能体循环模式”的区别。 ## 文件分区 | 分类 | 路径 | 用途 | | --- | --- | --- | | 讲义 | [lecture/LECTURE_FULL.md](./lecture/LECTURE_FULL.md) "
        },
        {
          "key": "lecture",
          "label": "完整讲义",
          "path": "lessons/L01_agent_basics/lecture/LECTURE_FULL.md",
          "contentPath": "data/docs/L01_agent_basics/lecture.md",
          "excerpt": "# 第1讲讲义完整版：Agent 全景认知 —— 从 ChatBot 到自主智能体 适用对象：第一次系统学习 Agent 的同学 学习时长：60-90 分钟（不含拓展实操） 配套目录：`<course-root>/lessons/L01_agent_basics` 章节入口：`README.md` 章节总结：`CHAPTER_SUMMARY.md` --- ## 1.1 什么是 AI Agent？ 一句话理解：AI Agent 是一个“能自己想、自己做”的 AI 程序。 ### 生活化例子：订火锅 场景：你饿了，想吃火锅。 - 普通 ChatBot：你问“附近有什么火锅店？”，它给你推荐文本。到这里就结束，你还要自己比价格、看评分、打电话订位。 - AI Agent：你说“帮我订今晚 7 点火锅，2 个人，人均 100 以内”。它会自动搜索、筛选、比较、调用订位接口，并把确认信息返回给你。 ### ChatBot 与 Agent"
        },
        {
          "key": "summary",
          "label": "章节总结",
          "path": "lessons/L01_agent_basics/lecture/CHAPTER_SUMMARY.md",
          "contentPath": "data/docs/L01_agent_basics/summary.md",
          "excerpt": "# L01 章节总结：Agent 全景认知 ## 一句话总结 AI Agent 是以 LLM 为核心，能够理解目标、规划步骤、调用工具、利用记忆并持续调整行为的智能程序。它和普通 ChatBot 最大的区别是：ChatBot 偏向回答问题，Agent 偏向完成任务。 ## 核心概念 | 概念 | 本章理解 | | --- | --- | | LLM | Agent 的“大脑”，负责理解、推理和生成决策 | | Planning | 把复杂目标拆成可执行步骤，降低任务失败率 | | Tools | Agent 的“手脚”，连接搜索、计算、文件、API 等外部能力 | | Memory | 保存上下文、历史结果和用户偏好，让 Agent 不只看当前一句话 | | Agent Loop | Observe -> Think/Plan -> Act -> Reflect 的循环执行模式 | ## ChatBot 与 Agent 的关键差"
        },
        {
          "key": "preclass",
          "label": "课前准备",
          "path": "lessons/L01_agent_basics/materials/PRECLASS_CHECKLIST.md",
          "contentPath": "data/docs/L01_agent_basics/preclass.md",
          "excerpt": "# L01 课前准备清单（按讲义 1.1 ~ 1.6） ## 一、环境就绪（必须完成） - [ ] 执行 `source <course-root>/use_proxy.sh`（如需代理） - [ ] 执行 `source <course-root>/scripts/activate_course.sh` - [ ] 执行 `python <course-root>/scripts/check_env.py` - [ ] 执行 `python <course-root>/scripts/smoke_openai.py` - [ ] 确认 `.env` 中 `OPENAI_API_KEY`、`OPENAI_BASE_URL`、`OPENAI_MODEL` 有效 ## 二、实操准备（必须完成） - [ ] 进入 `cd <course-root>/lessons/L01_agent_basics` - [ ] 运行 `python "
        },
        {
          "key": "quiz",
          "label": "课后小测",
          "path": "lessons/L01_agent_basics/materials/MINI_QUIZ.md",
          "contentPath": "data/docs/L01_agent_basics/quiz.md",
          "excerpt": "# L01 课后小测（讲义版） 请先独立作答，再看参考答案。 1. 用一句话定义 AI Agent。 2. ChatBot 与 Agent 的核心差异是什么？ 3. Agent 的四个核心模块分别是什么？ 4. 为什么说 Tools 是 Agent 的“手脚”？ 5. 在 Agent 流程中，Planning 的价值是什么？ 6. 多轮对话里，`messages` 列表为什么能形成“最小记忆”？ 7. 举一个“只用 Prompt 就够”的任务。 8. 举一个“必须用 Agent 更合适”的任务。 9. 说出两个常见失败模式。 10. 你当前工作里，有什么任务可以改造成 Agent 流程？至少写 2 个步骤。 ## 参考答案（示例） 1. AI Agent 是以 LLM 为核心，具备规划、工具调用和记忆能力的智能程序。 2. ChatBot 主要回答问题；Agent 以“完成任务”为目标并可自主执行。 3. LLM、Plannin"
        },
        {
          "key": "extensions",
          "label": "拓展作业",
          "path": "lessons/L01_agent_basics/materials/EXTENSIONS.md",
          "contentPath": "data/docs/L01_agent_basics/extensions.md",
          "excerpt": "# L01 拓展练习（讲义 1.6 对齐） ## 必做练习 - 运行 `practice/02_multi_turn_chat.py`，连续对话 5 轮以上，观察模型是否保持上下文。 - 在 `practice/02_multi_turn_chat.py` 里修改 system prompt，分别扮演： - Python 教师 - 健身教练 - 面试官 - 记录每个角色的回答风格差异（语气、结构、建议方式）。 ## 入门拓展（约 30 分钟） - 把 `practice/01_hello_llm.py` 的用户问题改成你工作中的真实问题。 - 把 `practice/demo_chatbot_vs_agent.py` 的目标替换成你的日常场景。 - 对比“纯回答”与“工具增强”的可执行性差异。 ## 进阶拓展（约 60-90 分钟） - 给 `practice/02_multi_turn_chat.py` 增加一条命令（如 `c"
        }
      ],
      "practiceFiles": [
        {
          "name": "01_hello_llm.py",
          "path": "lessons/L01_agent_basics/practice/01_hello_llm.py",
          "size": "5.4 KB"
        },
        {
          "name": "02_multi_turn_chat.py",
          "path": "lessons/L01_agent_basics/practice/02_multi_turn_chat.py",
          "size": "7.0 KB"
        },
        {
          "name": "demo_chatbot_vs_agent.py",
          "path": "lessons/L01_agent_basics/practice/demo_chatbot_vs_agent.py",
          "size": "13.2 KB"
        },
        {
          "name": "preclass_run.sh",
          "path": "lessons/L01_agent_basics/practice/preclass_run.sh",
          "size": "1.5 KB"
        }
      ],
      "resourceFiles": [],
      "materialFiles": [
        {
          "name": "EXTENSIONS.md",
          "path": "lessons/L01_agent_basics/materials/EXTENSIONS.md",
          "size": "1.4 KB"
        },
        {
          "name": "MINI_QUIZ.md",
          "path": "lessons/L01_agent_basics/materials/MINI_QUIZ.md",
          "size": "1.5 KB"
        },
        {
          "name": "NOTES_TEMPLATE.md",
          "path": "lessons/L01_agent_basics/materials/NOTES_TEMPLATE.md",
          "size": "835 B"
        },
        {
          "name": "PRECLASS_CHECKLIST.md",
          "path": "lessons/L01_agent_basics/materials/PRECLASS_CHECKLIST.md",
          "size": "2.0 KB"
        }
      ],
      "dataFiles": [],
      "preclassCommand": "cd lessons/L01_agent_basics && bash practice/preclass_run.sh",
      "fileCount": 11,
      "searchText": "# L01 Agent 全景认知：从 ChatBot 到自主智能体 本章是课程入口，目标不是一开始就写复杂 Agent，而是建立一套稳定的判断框架：什么是 Agent、它和普通 ChatBot 差在哪里、一个最小 Agent 需要哪些模块，以及如何用 Python 跑通第一个 LLM 调用。 ## 本章学习目标 - 能用一句话解释什么是 AI Agent。 - 能说清 ChatBot 与 Agent 的关键差异。 - 理解 Agent 的四个核心模块：LLM、Planning、Tools、Memory。 - 跑通第一个 LLM API 调用和一个多轮对话程序。 - 通过最小示例观察“聊天模式”和“智能体循环模式”的区别。 ## 文件分区 | 分类 | 路径 | 用途 | | --- | --- | --- | | 讲义 | [lecture/LECTURE_FULL.md](./lecture/LECTURE_FULL.md) | 可直接授课或自学的完整讲义 | | 总结 | [lecture/CHAPTER_SUMMARY.md](./lecture/CHAPTER_SUMMARY.md) | 本章关键概念、实操结果与复习清单 | | 课前准备 | [materials/PRECLASS_CHECKLIST.md](./materials/PRECLASS_CHECKLIST.md) | 上课前需要完成的环境、概念和实操检查 | | 实操代码 | [practice/](./practice/) | LLM 调用、多轮对话、ChatBot vs Agent 对比 | | 一键脚本 | [practice/preclass_run.sh](./practice/preclass_run.sh) | 自动执行环境检查和非交互式实操 | | 课堂笔记 | [materials/NOTES_TEMPLATE.md](./materials/NOTES_TEMPLATE.md) | 听课时记录概念、实验结果和疑问 | | 课后小测 | [materials/MINI_QUIZ.md](./materials/MINI_QUIZ.md) | 检查核心概念是否掌握 | | 拓展练习 | [materials/EXTENSIONS.md](./materials/EXTENSIONS.md) | 从入门到进阶的课后实践方向 | | 注释规范 | [../../CODE_COMMENTING_GUIDE.md](../../CODE_COMMENTING_GUIDE.md) | 阅读和编写课程代码时遵循的讲解标准 | ## 推荐学习路径 1. 先看 [materials/PRECLASS_CHECKLIST.md](./materials/PRECLASS_CHECKLIST.md)，确认环境变量、依赖和 API 连通性。 2. 阅读 [lecture/LECTURE_FULL.md](./lecture/LECTURE_FULL.md) 的 1.1-1.4，建立 Agent 全景认知。 3. 阅读 [../../CODE_COMMENTING_GUIDE.md](../../CODE_COMMENTING_GUIDE.md)，了解课程代码里的关键注释会重点解释什么。 4. 运行 `practice/01_hello_llm.py`，确认能完成一次最小 LLM 调用。 5. 运行 `practice/02_multi_turn_chat.py`，观察 `messages` 如何形成最小上下文记忆。 6. 运行 `practice/demo_chatbot_vs_agent.py`，对比普通聊天和 Agent 循环。 7. 完成 [materials/MINI_QUIZ.md](./materials/MINI_QUIZ.md)，再用 [lecture/CHAPTER_SUMMARY.md](./lecture/CHAPTER_SUMMARY.md) 复盘。 ## 快速运行 从课程根目录激活环境： ```bash source <course-root>/scripts/activate_course.sh ``` 进入第一章目录： ```bash cd <course-root>/lessons/L01_agent_basics ``` 运行最小 LLM 调用： ```bash python practice/01_hello_llm.py ``` 运行多轮对话： ```bash python practice/02_multi_turn_chat.py ``` 运行 ChatBot 与 Agent 对比示例： ```bash python practice/demo_chatbot_vs_agent.py --mode both ``` 一键预习检查： ```bash bash practice/preclass_run.sh ``` 通过标志：最后看到 `[OK] L01 preclass run completed.`。 ## 本章实操说明 - `practice/01_hello_llm.py`：读取根目录 `.env`，发起"
    },
    {
      "id": "L02_prompt_engineering",
      "code": "L02",
      "title": "L02 Prompt Engineering 进阶：System Prompt 与 Agent 行为设计",
      "intro": "本章承接 L01 的 Agent 全景认知，进入“如何控制 Agent 行为”的核心问题。学生需要掌握 System Prompt 的结构、边界、输出格式、工具调用约束，并通过真实产品 prompt 案例学习工业级写法。",
      "topics": [
        "Prompt Engineering",
        "System Prompt",
        "Few-shot",
        "CoT",
        "ReAct",
        "结构化输出"
      ],
      "goals": [
        "理解为什么 Prompt 决定 Agent 的行为上限。",
        "掌握 System Prompt 的岗位说明书写法。",
        "学会三种关键模式：Few-shot、CoT、ReAct。",
        "能让模型稳定输出可编程的 JSON 结构。",
        "学会用测试用例迭代 Prompt 质量。",
        "能阅读真实产品 System Prompt，并抽取可复用设计模式。"
      ],
      "deliverables": [
        "一版“代码 Review 助手”的 System Prompt。",
        "三个测试用例：代码坏味道、明显 bug、高质量代码。",
        "一次 `practice/03_structured_output.py` 的 JSON 输出记录。",
        "一次 V1/V2 Prompt 对比记录，至少指出 2 个改进点。",
        "一份真实产品 System Prompt 阅读笔记，标注角色、边界、工具、输出格式、安全护栏和上下文管理。",
        "一份编码助手 prompt 原理解析，写出 1-2 个可迁移设计点。",
        "一份 Few-Shot/CoT 示例改写作业，说明示例数量、覆盖边界和成本取舍。",
        "一组面试题复盘：Prompt 改写、token 成本、评估方法、幻觉控制、few-shot 样本选择、CoT 边界、JSON 稳定性和上下文预算。"
      ],
      "docs": [
        {
          "key": "readme",
          "label": "章节入口",
          "path": "lessons/L02_prompt_engineering/README.md",
          "contentPath": "data/docs/L02_prompt_engineering/readme.md",
          "excerpt": "# L02 Prompt Engineering 进阶：System Prompt 与 Agent 行为设计 本章承接 L01 的 Agent 全景认知，进入“如何控制 Agent 行为”的核心问题。学生需要掌握 System Prompt 的结构、边界、输出格式、工具调用约束，并通过真实产品 prompt 案例学习工业级写法。 ## 本章学习目标 - 理解为什么 Prompt 决定 Agent 的行为上限。 - 掌握 System Prompt 的岗位说明书写法。 - 学会三种关键模式：Few-shot、CoT、ReAct。 - 能让模型稳定输出可编程的 JSON 结构。 - 学会用测试用例迭代 Prompt 质量。 - 能阅读真实产品 System Prompt，并抽取可复用设计模式。 ## 文件分区 | 分类 | 路径 | 用途 | | --- | --- | --- | | 讲义 | [lecture/LECTURE_F"
        },
        {
          "key": "lecture",
          "label": "完整讲义",
          "path": "lessons/L02_prompt_engineering/lecture/LECTURE_FULL.md",
          "contentPath": "data/docs/L02_prompt_engineering/lecture.md",
          "excerpt": "# 第2讲讲义完整版：Prompt Engineering 进阶 —— Agent 的“灵魂”设计 适用对象：已经完成 L01，准备进入稳定可控 Agent 设计的同学 学习时长：70-100 分钟（不含作业复盘） 配套目录：`<course-root>/lessons/L02_prompt_engineering` 章节入口：`README.md` 章节总结：`CHAPTER_SUMMARY.md` 参考资源：`resources/SYSTEM_PROMPT_REFERENCES.md` --- ## 2.1 为什么 Prompt 是 Agent 的灵魂？ Agent 的行为本质来自 LLM 输出。 LLM 输出什么，取决于 Prompt 怎么写。 所以 Prompt 质量，直接决定： 1. Agent 是否理解你的真实需求 2. Agent 是否遵守边界（不做越权行为） 3. Agent 输出是否稳定、可解析、可复用 三种核"
        },
        {
          "key": "summary",
          "label": "章节总结",
          "path": "lessons/L02_prompt_engineering/lecture/CHAPTER_SUMMARY.md",
          "contentPath": "data/docs/L02_prompt_engineering/summary.md",
          "excerpt": "# L02 章节总结：System Prompt 与 Prompt 迭代 ## 一句话总结 Prompt 是 Agent 的行为说明书。System Prompt 定义身份、能力边界、行为准则、输出格式和示例；测试用例和迭代机制决定它能否从“看起来能用”变成“稳定可复用”。 ## System Prompt 五要素 | 要素 | 作用 | 常见写法 | | --- | --- | --- | | 角色定义 | 让模型知道自己是谁 | “你是一个代码 Review 助手” | | 能力边界 | 明确能做什么、不能做什么 | “只审查代码，不生成业务承诺” | | 行为准则 | 规定执行顺序和判断标准 | “先指出风险，再给修改建议” | | 输出格式 | 让结果可读、可比、可解析 | Markdown 表格、JSON schema、固定字段 | | 示例 | 稳定风格和边界 | Few-shot 输入输出样例 | ## 三种关键模"
        },
        {
          "key": "preclass",
          "label": "课前准备",
          "path": "lessons/L02_prompt_engineering/materials/PRECLASS_CHECKLIST.md",
          "contentPath": "data/docs/L02_prompt_engineering/preclass.md",
          "excerpt": "# L02 课前准备清单（按讲义 2.1 ~ 2.7） ## 一、环境就绪（必须完成） - [ ] 执行 `source <course-root>/use_proxy.sh`（如需代理） - [ ] 执行 `source <course-root>/scripts/activate_course.sh` - [ ] 执行 `python <course-root>/scripts/check_env.py` - [ ] 执行 `python <course-root>/scripts/smoke_openai.py` - [ ] 确认 `.env` 中 `OPENAI_API_KEY`、`OPENAI_BASE_URL`、`OPENAI_MODEL` 有效 ## 二、实操准备（必须完成） - [ ] 进入 `cd <course-root>/lessons/L02_prompt_engineering` - [ ] 运行 `p"
        },
        {
          "key": "quiz",
          "label": "课后小测",
          "path": "lessons/L02_prompt_engineering/materials/MINI_QUIZ.md",
          "contentPath": "data/docs/L02_prompt_engineering/quiz.md",
          "excerpt": "# L02 课后小测（讲义版） 请先独立作答，再看参考答案。 1. 为什么说 Prompt 是 Agent 的灵魂？ 2. System Prompt 的 5 个关键组成是什么？ 3. Few-shot 主要解决什么问题？ 4. CoT 在什么任务上更有价值？ 5. ReAct 与普通问答最大的不同是什么？ 6. 为什么工程里经常要求模型输出 JSON？ 7. 当输出格式不稳定时，至少说出两个改进手段。 8. 你会如何验证一个 Prompt 版本是否优于旧版本？ 9. 阅读真实产品 System Prompt 时，至少应该标注哪 4 类信息？ 10. Prompt 很好但 token 太贵时，可以从哪些方向优化？ 11. Few-shot 示例是越多越好吗？为什么？ 12. CoT 在什么情况下可能反而不适合？ 13. 设计 Few-Shot 示例时，至少说出三个原则。 14. Zero-Shot CoT 的典型触发语是什么？ "
        },
        {
          "key": "extensions",
          "label": "拓展作业",
          "path": "lessons/L02_prompt_engineering/materials/EXTENSIONS.md",
          "contentPath": "data/docs/L02_prompt_engineering/extensions.md",
          "excerpt": "# L02 拓展练习（讲义 2.7 对齐） ## 必做练习 - 为“代码 Review 助手”设计一版 System Prompt。 - 准备 3 个测试用例进行验证。 - 记录每个用例的输出是否满足：边界、格式、可执行建议。 - 阅读 `resources/SYSTEM_PROMPT_REFERENCES.md`，任选一个真实产品 prompt 做结构标注。 - 阅读 `resources/PROMPT_EXAMPLES.md`，任选一个 Few-Shot 或 CoT 示例改写成自己的业务场景。 ## 入门拓展（约 30 分钟） - 在 `practice/03_structured_output.py` 中新增字段 `risks`（风险点列表）。 - 对比 `temperature=0` 与 `temperature=0.7` 的结构化成功率差异。 - 为 JSON 输出增加字段缺失校验（例如 people/summary "
        },
        {
          "key": "interview",
          "label": "面试题",
          "path": "lessons/L02_prompt_engineering/materials/INTERVIEW_QA.md",
          "contentPath": "data/docs/L02_prompt_engineering/interview.md",
          "excerpt": "# L02 面试题速查：Prompt Engineering 本文件用于面试前快速复习。完整解释和课堂讨论见 [LECTURE_FULL.md](../lecture/LECTURE_FULL.md) 的 2.8，以及 [CHAPTER_SUMMARY.md](../lecture/CHAPTER_SUMMARY.md) 的面试题速查。 ## 来源说明 - 题目来源：来自老师第 2 讲讲义中的“2.8 面试题与课堂讨论”和章节总结里的“面试题速查”。 - 整理方式：不是逐字摘抄，而是把老师讲义中的问题、回答要点和课堂讨论整理成更适合复习的问答格式。 - 补充内容：少量表达如“回归集”“分层模型”等属于工程化补充，用于帮助面试表达更完整；不应理解为老师原文。 ## 1. 如何改写一个模糊 Prompt？ 原 prompt： ```text 帮我总结这篇文章，越详细越好。 ``` 改写思路： - 补充角色：你是研究助理、代码 Rev"
        },
        {
          "key": "resource:PROMPT_EXAMPLES",
          "label": "资源：PROMPT_EXAMPLES",
          "path": "lessons/L02_prompt_engineering/resources/PROMPT_EXAMPLES.md",
          "contentPath": "data/docs/L02_prompt_engineering/resource_PROMPT_EXAMPLES.md",
          "excerpt": "# L02 示例集：Few-Shot 与 CoT Prompt 这个文档用于课堂演示和课后练习。主讲义负责讲概念，这里集中放可直接改写的 prompt 示例。 ## 一、Few-Shot Prompting 示例 ### 1. 情感分类（基础） ```text 请判断以下评论的情感倾向（正面/负面/中性）。 示例1： 评论：\"这家餐厅的牛排太好吃了，服务也很周到！\" 情感：正面 示例2： 评论：\"等了40分钟才上菜，而且菜是冷的。\" 情感：负面 示例3： 评论：\"这家店在市中心，交通比较方便。\" 情感：中性 现在请判断： 评论：\"虽然价格偏贵，但食材新鲜、摆盘精致，整体体验超出预期。\" 情感： ``` ### 2. 结构化信息提取（中级） ```text 从用户描述中提取关键信息，输出 JSON 格式。 示例1"
        },
        {
          "key": "resource:SYSTEM_PROMPT_REFERENCES",
          "label": "资源：SYSTEM_PROMPT_REFERENCES",
          "path": "lessons/L02_prompt_engineering/resources/SYSTEM_PROMPT_REFERENCES.md",
          "contentPath": "data/docs/L02_prompt_engineering/resource_SYSTEM_PROMPT_REFERENCES.md",
          "excerpt": "# L02 参考资源：System Prompt 案例与阅读路线 > 跨章节外部资源统一索引见：[教辅资料：外部学习资源索引](../../../teaching_support/EXTERNAL_LEARNING_RESOURCES.md)。 > GitHub stars 会持续变化，课堂以链接页面实时信息为准，不建议在作业中写死 star 数。 > 使用提醒：部分资源来自泄露、逆向工程或社区收集。课堂使用时建议学习结构和设计模式，不建议复制专有 prompt，不要用于绕过产品安全策略或提取他人系统提示。 ## 一、真实产品 System Prompt 合集 这类仓库适合学习工业级 Agent 如何处理身份、工具调用、安全边界、多轮上下文和输出约束。 | 仓库 | 适合学习什么 | | --- | --- |"
        }
      ],
      "practiceFiles": [
        {
          "name": "03_structured_output.py",
          "path": "lessons/L02_prompt_engineering/practice/03_structured_output.py",
          "size": "7.4 KB"
        },
        {
          "name": "04_prompt_iteration.py",
          "path": "lessons/L02_prompt_engineering/practice/04_prompt_iteration.py",
          "size": "6.8 KB"
        },
        {
          "name": "preclass_run.sh",
          "path": "lessons/L02_prompt_engineering/practice/preclass_run.sh",
          "size": "1.5 KB"
        }
      ],
      "resourceFiles": [
        {
          "name": "PROMPT_EXAMPLES.md",
          "path": "lessons/L02_prompt_engineering/resources/PROMPT_EXAMPLES.md",
          "size": "8.9 KB"
        },
        {
          "name": "SYSTEM_PROMPT_REFERENCES.md",
          "path": "lessons/L02_prompt_engineering/resources/SYSTEM_PROMPT_REFERENCES.md",
          "size": "4.2 KB"
        }
      ],
      "materialFiles": [
        {
          "name": "EXTENSIONS.md",
          "path": "lessons/L02_prompt_engineering/materials/EXTENSIONS.md",
          "size": "1.9 KB"
        },
        {
          "name": "INTERVIEW_QA.md",
          "path": "lessons/L02_prompt_engineering/materials/INTERVIEW_QA.md",
          "size": "3.8 KB"
        },
        {
          "name": "MINI_QUIZ.md",
          "path": "lessons/L02_prompt_engineering/materials/MINI_QUIZ.md",
          "size": "2.1 KB"
        },
        {
          "name": "NOTES_TEMPLATE.md",
          "path": "lessons/L02_prompt_engineering/materials/NOTES_TEMPLATE.md",
          "size": "1.1 KB"
        },
        {
          "name": "PRECLASS_CHECKLIST.md",
          "path": "lessons/L02_prompt_engineering/materials/PRECLASS_CHECKLIST.md",
          "size": "2.3 KB"
        }
      ],
      "dataFiles": [],
      "preclassCommand": "cd lessons/L02_prompt_engineering && bash practice/preclass_run.sh",
      "fileCount": 13,
      "searchText": "# L02 Prompt Engineering 进阶：System Prompt 与 Agent 行为设计 本章承接 L01 的 Agent 全景认知，进入“如何控制 Agent 行为”的核心问题。学生需要掌握 System Prompt 的结构、边界、输出格式、工具调用约束，并通过真实产品 prompt 案例学习工业级写法。 ## 本章学习目标 - 理解为什么 Prompt 决定 Agent 的行为上限。 - 掌握 System Prompt 的岗位说明书写法。 - 学会三种关键模式：Few-shot、CoT、ReAct。 - 能让模型稳定输出可编程的 JSON 结构。 - 学会用测试用例迭代 Prompt 质量。 - 能阅读真实产品 System Prompt，并抽取可复用设计模式。 ## 文件分区 | 分类 | 路径 | 用途 | | --- | --- | --- | | 讲义 | [lecture/LECTURE_FULL.md](./lecture/LECTURE_FULL.md) | 可直接授课或自学的完整讲义 | | 总结 | [lecture/CHAPTER_SUMMARY.md](./lecture/CHAPTER_SUMMARY.md) | 本章关键概念、设计模式与复盘清单 | | 参考资源 | [resources/SYSTEM_PROMPT_REFERENCES.md](./resources/SYSTEM_PROMPT_REFERENCES.md) | System Prompt GitHub 资源、阅读路线和安全提醒 | | 外部教辅 | [../../teaching_support/EXTERNAL_LEARNING_RESOURCES.md](../../teaching_support/EXTERNAL_LEARNING_RESOURCES.md) | hello-agents、真实产品 prompt、Few-Shot/CoT、Claude.md 和 AI-native 工作方式 | | 示例集 | [resources/PROMPT_EXAMPLES.md](./resources/PROMPT_EXAMPLES.md) | Few-Shot、CoT、工具调用决策和示例数量策略 | | 课前准备 | [materials/PRECLASS_CHECKLIST.md](./materials/PRECLASS_CHECKLIST.md) | 上课前需要完成的环境、概念和实操检查 | | 实操代码 | [practice/](./practice/) | 结构化输出与 Prompt 迭代实验 | | 一键脚本 | [practice/preclass_run.sh](./practice/preclass_run.sh) | 自动执行环境检查和非交互式实操 | | 课堂笔记 | [materials/NOTES_TEMPLATE.md](./materials/NOTES_TEMPLATE.md) | 听课时记录 Prompt 版本、实验结果和失败模式 | | 课后小测 | [materials/MINI_QUIZ.md](./materials/MINI_QUIZ.md) | 检查核心概念是否掌握 | | 拓展练习 | [materials/EXTENSIONS.md](./materials/EXTENSIONS.md) | Prompt 实验台、回归集和评估练习 | | 面试速查 | [materials/INTERVIEW_QA.md](./materials/INTERVIEW_QA.md) | Prompt 改写、评估、幻觉、few-shot、CoT 和 JSON 稳定性 | | 注释规范 | [../../CODE_COMMENTING_GUIDE.md](../../CODE_COMMENTING_GUIDE.md) | 阅读和编写课程代码时遵循的讲解标准 | ## 推荐学习路径 1. 先看 [materials/PRECLASS_CHECKLIST.md](./materials/PRECLASS_CHECKLIST.md)，确认 L01 环境仍然可用。 2. 阅读 [lecture/LECTURE_FULL.md](./lecture/LECTURE_FULL.md) 的 2.1-2.5，掌握 System Prompt 五要素。 3. 阅读 [resources/SYSTEM_PROMPT_REFERENCES.md](./resources/SYSTEM_PROMPT_REFERENCES.md)，选择 1-2 个真实产品 prompt 做结构标注。 4. 阅读 [../../teaching_support/EXTERNAL_LEARNING_RESOURCES.md](../../teaching_support/EXTERNAL_LEARNING_RESOURCES.md)，了解老师推荐的外部资料如何对应本章和后续章节。 5. 阅读 [resources/PROMPT_EXAMPLES.md](./resources/PROMPT_EXAMPLES.m"
    },
    {
      "id": "L03_function_calling",
      "code": "L03",
      "title": "L03 Function Calling 核心机制：给 Agent 装上手脚",
      "intro": "本章从“会回答”的 LLM 进入“能执行”的 Agent。学生需要理解 Function Calling 的工作流程、工具 schema 的设计方法、工具执行循环、并发工具调用，以及真实系统里工具选择、报错恢复和脏数据治理的问题。",
      "topics": [
        "Function Calling",
        "Tool Schema",
        "并发工具",
        "错误恢复",
        "脏数据治理"
      ],
      "goals": [
        "理解 Function Calling 是什么，以及模型和代码分别负责什么。",
        "学会用 JSON Schema 定义工具名称、描述和参数。",
        "跑通一个能查天气、看时间、做计算的最小工具型 Agent。",
        "理解多个 tool calls 的串行与并发执行差异。",
        "掌握工具数量变多时提升调用准确率的方法。",
        "能处理工具执行失败、权限错误、空结果、噪声结果和多源冲突。"
      ],
      "deliverables": [
        "一个新增工具的 function schema。",
        "一次基础 Function Calling 运行日志。",
        "一次并发工具调用运行日志。",
        "一份工具准确率优化方案：动态注入、工具边界、路由层、风险分级、指标评估。",
        "一份错误恢复方案：错误分类、自动修复、有限重试、fallback、用户澄清、partial success。",
        "一份噪声结果治理方案：清洗、过滤、归一化、rerank、交叉验证、证据约束。"
      ],
      "docs": [
        {
          "key": "readme",
          "label": "章节入口",
          "path": "lessons/L03_function_calling/README.md",
          "contentPath": "data/docs/L03_function_calling/readme.md",
          "excerpt": "# L03 Function Calling 核心机制：给 Agent 装上手脚 本章从“会回答”的 LLM 进入“能执行”的 Agent。学生需要理解 Function Calling 的工作流程、工具 schema 的设计方法、工具执行循环、并发工具调用，以及真实系统里工具选择、报错恢复和脏数据治理的问题。 ## 本章学习目标 - 理解 Function Calling 是什么，以及模型和代码分别负责什么。 - 学会用 JSON Schema 定义工具名称、描述和参数。 - 跑通一个能查天气、看时间、做计算的最小工具型 Agent。 - 理解多个 tool calls 的串行与并发执行差异。 - 掌握工具数量变多时提升调用准确率的方法。 - 能处理工具执行失败、权限错误、空结果、噪声结果和多源冲突。 ## 文件分区 | 分类 | 路径 | 用途 | | --- | --- | --- | | 讲义 | [lecture/LE"
        },
        {
          "key": "lecture",
          "label": "完整讲义",
          "path": "lessons/L03_function_calling/lecture/LECTURE_FULL.md",
          "contentPath": "data/docs/L03_function_calling/lecture.md",
          "excerpt": "# 第3讲讲义完整版：Function Calling 核心机制 —— 给 Agent 装上手脚 适用对象：已经完成 L01/L02，理解 Agent 基础和 Prompt 设计的同学 学习时长：90-120 分钟（不含拓展实操） 配套目录：`<course-root>/lessons/L03_function_calling` 章节入口：`README.md` 章节总结：`CHAPTER_SUMMARY.md` --- ## 3.1 什么是 Function Calling？ 到目前为止，我们的 AI 主要只能“说”，不能“做”。它能写出很好的分析文字，但如果你问它“现在几点了？”，它如果没有外部工具，就只能猜一个时间。 Function Calling 就是让模型把自然语言请求转换成可执行工具调用的能力。 核心要点： 1. 模型本身不直接执行函数。 2. 模型输出“我要调用哪个工具、传什么参数”。 3. 你的代码负责真正执行"
        },
        {
          "key": "summary",
          "label": "章节总结",
          "path": "lessons/L03_function_calling/lecture/CHAPTER_SUMMARY.md",
          "contentPath": "data/docs/L03_function_calling/summary.md",
          "excerpt": "# L03 章节总结：Function Calling 核心机制 ## 一句话总结 Function Calling 让模型从“生成文本”升级为“选择工具并传参”。模型负责决策，代码负责执行；成熟系统还必须处理工具选择准确率、错误恢复、安全风控、观测指标和噪声结果治理。 ## 四步流程 1. 定义工具：名称、描述、参数 schema。 2. 发送用户请求和工具列表给模型。 3. 模型返回 tool calls。 4. 程序执行工具，把结果写回模型，模型生成最终回复。 ## 本章实操 | 脚本 | 作用 | | --- | --- | | `practice/05_function_calling.py` | 基础 Function Calling：天气、时间、计算 | | `practice/06_parallel_function_calling.py` | 并发执行多个独立 tool calls | ## 工具 Schema"
        },
        {
          "key": "preclass",
          "label": "课前准备",
          "path": "lessons/L03_function_calling/materials/PRECLASS_CHECKLIST.md",
          "contentPath": "data/docs/L03_function_calling/preclass.md",
          "excerpt": "# L03 课前准备清单 ## 一、环境就绪 - [ ] 执行 `source <course-root>/scripts/activate_course.sh` - [ ] 执行 `python <course-root>/scripts/check_env.py` - [ ] 执行 `python <course-root>/scripts/smoke_openai.py` - [ ] 确认 `.env` 中 `OPENAI_API_KEY`、`OPENAI_BASE_URL`、`OPENAI_MODEL` 有效 ## 二、实操准备 - [ ] 进入 `cd <course-root>/lessons/L03_function_calling` - [ ] 运行 `python practice/05_function_calling.py --demo` - [ ] 运行 `python practice/06_paral"
        },
        {
          "key": "quiz",
          "label": "课后小测",
          "path": "lessons/L03_function_calling/materials/MINI_QUIZ.md",
          "contentPath": "data/docs/L03_function_calling/quiz.md",
          "excerpt": "# L03 课后小测 请先独立作答，再看参考答案。 1. Function Calling 的核心流程是哪 4 步？ 2. 模型会不会直接执行函数？为什么？ 3. Function Calling 和 prompt 要求输出 JSON 有什么区别？ 4. function schema 设计有哪些原则？ 5. schema 太复杂会带来什么问题？ 6. 多轮 tool calling 如何避免死循环？ 7. 工具很多时如何提升工具选择准确率？ 8. 工具执行报错有哪些常见类型？ 9. 哪些错误适合重试，哪些不适合？ 10. 如何防止模型调用高危函数？ 11. 如何评估 function calling 做得好不好？ 12. 工具结果不可靠时，为什么不能直接喂给模型？ ## 参考答案（示例） 1. 定义工具、发送用户请求、模型返回 tool calls、代码执行工具并回写结果。 2. 不会。模型只输出调用意图，实际执行由程序代码完"
        },
        {
          "key": "extensions",
          "label": "拓展作业",
          "path": "lessons/L03_function_calling/materials/EXTENSIONS.md",
          "contentPath": "data/docs/L03_function_calling/extensions.md",
          "excerpt": "# L03 拓展练习 ## 必做练习 - 给 `practice/05_function_calling.py` 增加 `search_news(keyword)` 工具。 - 给 `practice/05_function_calling.py` 增加 `translate(text, target_lang)` 工具。 - 为每个新工具写清楚 description、参数和 required 字段。 - 准备至少 5 个输入，记录工具选择是否正确。 ## 入门拓展（约 30 分钟） - 给天气工具增加本地缓存，重复查询同一城市时复用结果。 - 给工具调用循环增加 `max_steps`，避免无限 tool calling。 - 为未知工具返回 `{\"error\": \"unknown tool\"}`，让模型自我修复。 ## 进阶拓展（约 60-90 分钟） - 给并发脚本增加结构化日志：`trace_id`、`tool_nam"
        },
        {
          "key": "interview",
          "label": "面试题",
          "path": "lessons/L03_function_calling/materials/INTERVIEW_QA.md",
          "contentPath": "data/docs/L03_function_calling/interview.md",
          "excerpt": "# L03 面试题速查：Function Calling 本文件把第 3 讲的面试问题收拢成一个入口。深入展开见： - [TOOL_CALLING_ACCURACY.md](../resources/TOOL_CALLING_ACCURACY.md) - [TOOL_ERROR_RECOVERY.md](../resources/TOOL_ERROR_RECOVERY.md) - [NOISY_TOOL_RESULTS.md](../resources/NOISY_TOOL_RESULTS.md) ## 来源说明 - 题目来源：来自老师第 3 讲讲义的“3.13 面试题”。 - 回答来源：其中“工具很多时如何提升准确率”“工具报错后怎么恢复”“脏数据/噪声结果怎么处理”主要来自老师给的三份专题材料。 - 整理方式：本文件不是老师逐字题库，而是把老师原题和专题内容压缩成面试速查版。 - 补充内容：Function Calling "
        },
        {
          "key": "resource:NOISY_TOOL_RESULTS",
          "label": "资源：NOISY_TOOL_RESULTS",
          "path": "lessons/L03_function_calling/resources/NOISY_TOOL_RESULTS.md",
          "contentPath": "data/docs/L03_function_calling/resource_NOISY_TOOL_RESULTS.md",
          "excerpt": "# L03 专题：工具结果不可靠或噪声很大时怎么办 工具返回的是 observation，不是 truth。成熟 Agent 要做的不是“拿到结果就说”，而是先把 observation 处理成可信 evidence。 ## 一、面试官在考什么 1. 是否意识到工具输出不等于事实。 2. 是否理解噪声的不同来源。 3. 是否会做结果治理，而不是把脏数据直接喂给模型。 4. 是否知道什么时候继续推理，什么时候停下来。 5. 是否有生产化评估思维。 ## 二、噪声类型 | 类型 | 典型问题 | | --- | --- | | 召回噪声 | 搜回来很多弱相关结果 | | 结构噪声 | 网页广告、导航栏、页脚、OCR 错字、表格错位 | | 冲突噪声 | 多个系统返回关键字段不一致 | | 数据质量问题 | 缺字段、"
        },
        {
          "key": "resource:TOOL_CALLING_ACCURACY",
          "label": "资源：TOOL_CALLING_ACCURACY",
          "path": "lessons/L03_function_calling/resources/TOOL_CALLING_ACCURACY.md",
          "contentPath": "data/docs/L03_function_calling/resource_TOOL_CALLING_ACCURACY.md",
          "excerpt": "# L03 专题：如何提升 Function Calling 准确率 当系统里可用工具越来越多时，问题会从“会不会调工具”升级成“如何选对工具、少选错工具、少漏选工具，同时控制延迟、成本和安全风险”。 ## 一、为什么工具一多准确率会变差 1. 工具语义重叠 例如 `search_web`、`search_docs`、`search_order`、`search_customer` 都叫搜索，模型很难区分。 2. 描述过长、过像、过泛 “用于查询各种信息”“支持多种检索能力”这类描述在工具少时还能凑合，工具一多就失效。 3. 暴露工具太多 把 80 个工具一次性塞给模型，本质上是在让模型做全量搜索，注意力分散且选择空间过大。 4. 工具成本不对称 查缓存和发邮件不是一个风险级别；读操作和写操作也不能同权暴露。 "
        },
        {
          "key": "resource:TOOL_ERROR_RECOVERY",
          "label": "资源：TOOL_ERROR_RECOVERY",
          "path": "lessons/L03_function_calling/resources/TOOL_ERROR_RECOVERY.md",
          "contentPath": "data/docs/L03_function_calling/resource_TOOL_ERROR_RECOVERY.md",
          "excerpt": "# L03 专题：工具执行报错后，怎么让 Agent 更稳 真实线上系统里，工具调用失败不是异常情况，而是常态。高质量 Agent 不是永不出错，而是出错后可控、可恢复、可解释。 ## 一、核心回答框架 1. 先对错误分类，不同错误不同处理。 2. 对可恢复错误做有限自动恢复。 3. 对不可恢复错误及时降级或中止。 4. 对写操作保证幂等和确认，避免误执行。 5. 记录观测数据，支持复盘和持续优化。 ## 二、错误分类 | 类型 | 典型场景 | 稳定处理 | | --- | --- | --- | | 参数错误 | 日期格式错、缺字段、枚举非法 | schema 校验、自动归一化、必要时澄清 | | 用户输入不足 | 重名、缺订单号、联系人不明确 | 向用户补充询问 | | 下游瞬时故障 | timeout、"
        }
      ],
      "practiceFiles": [
        {
          "name": "05_function_calling.py",
          "path": "lessons/L03_function_calling/practice/05_function_calling.py",
          "size": "15.4 KB"
        },
        {
          "name": "06_parallel_function_calling.py",
          "path": "lessons/L03_function_calling/practice/06_parallel_function_calling.py",
          "size": "5.5 KB"
        },
        {
          "name": "preclass_run.sh",
          "path": "lessons/L03_function_calling/practice/preclass_run.sh",
          "size": "1.3 KB"
        }
      ],
      "resourceFiles": [
        {
          "name": "NOISY_TOOL_RESULTS.md",
          "path": "lessons/L03_function_calling/resources/NOISY_TOOL_RESULTS.md",
          "size": "3.4 KB"
        },
        {
          "name": "TOOL_CALLING_ACCURACY.md",
          "path": "lessons/L03_function_calling/resources/TOOL_CALLING_ACCURACY.md",
          "size": "4.3 KB"
        },
        {
          "name": "TOOL_ERROR_RECOVERY.md",
          "path": "lessons/L03_function_calling/resources/TOOL_ERROR_RECOVERY.md",
          "size": "3.3 KB"
        }
      ],
      "materialFiles": [
        {
          "name": "EXTENSIONS.md",
          "path": "lessons/L03_function_calling/materials/EXTENSIONS.md",
          "size": "1.5 KB"
        },
        {
          "name": "INTERVIEW_QA.md",
          "path": "lessons/L03_function_calling/materials/INTERVIEW_QA.md",
          "size": "4.4 KB"
        },
        {
          "name": "MINI_QUIZ.md",
          "path": "lessons/L03_function_calling/materials/MINI_QUIZ.md",
          "size": "2.1 KB"
        },
        {
          "name": "NOTES_TEMPLATE.md",
          "path": "lessons/L03_function_calling/materials/NOTES_TEMPLATE.md",
          "size": "892 B"
        },
        {
          "name": "PRECLASS_CHECKLIST.md",
          "path": "lessons/L03_function_calling/materials/PRECLASS_CHECKLIST.md",
          "size": "1.2 KB"
        }
      ],
      "dataFiles": [],
      "preclassCommand": "cd lessons/L03_function_calling && bash practice/preclass_run.sh",
      "fileCount": 14,
      "searchText": "# L03 Function Calling 核心机制：给 Agent 装上手脚 本章从“会回答”的 LLM 进入“能执行”的 Agent。学生需要理解 Function Calling 的工作流程、工具 schema 的设计方法、工具执行循环、并发工具调用，以及真实系统里工具选择、报错恢复和脏数据治理的问题。 ## 本章学习目标 - 理解 Function Calling 是什么，以及模型和代码分别负责什么。 - 学会用 JSON Schema 定义工具名称、描述和参数。 - 跑通一个能查天气、看时间、做计算的最小工具型 Agent。 - 理解多个 tool calls 的串行与并发执行差异。 - 掌握工具数量变多时提升调用准确率的方法。 - 能处理工具执行失败、权限错误、空结果、噪声结果和多源冲突。 ## 文件分区 | 分类 | 路径 | 用途 | | --- | --- | --- | | 讲义 | [lecture/LECTURE_FULL.md](./lecture/LECTURE_FULL.md) | 第 3 讲完整讲义 | | 总结 | [lecture/CHAPTER_SUMMARY.md](./lecture/CHAPTER_SUMMARY.md) | 本章核心机制、工程要点和面试框架 | | 课前准备 | [materials/PRECLASS_CHECKLIST.md](./materials/PRECLASS_CHECKLIST.md) | 环境、概念和实操检查 | | 实操代码 | [practice/](./practice/) | 基础 Function Calling 与并发工具调用示例 | | 一键脚本 | [practice/preclass_run.sh](./practice/preclass_run.sh) | 环境检查和 L03 非交互式实操 | | 课堂笔记 | [materials/NOTES_TEMPLATE.md](./materials/NOTES_TEMPLATE.md) | 记录工具 schema、调用日志和错误恢复策略 | | 课后小测 | [materials/MINI_QUIZ.md](./materials/MINI_QUIZ.md) | 检查核心概念和工程判断 | | 拓展练习 | [materials/EXTENSIONS.md](./materials/EXTENSIONS.md) | 新工具、缓存、路由、鲁棒性和观测练习 | | 面试速查 | [materials/INTERVIEW_QA.md](./materials/INTERVIEW_QA.md) | Function Calling 高频问题与回答框架 | | 工程参考 | [resources/](./resources/) | 工具准确率、错误恢复、噪声治理三类专题 | | 注释规范 | [../../CODE_COMMENTING_GUIDE.md](../../CODE_COMMENTING_GUIDE.md) | 阅读和编写课程代码时遵循的讲解标准 | ## 推荐学习路径 1. 阅读 [lecture/LECTURE_FULL.md](./lecture/LECTURE_FULL.md) 的 3.1-3.4，理解 Function Calling 基础流程。 2. 阅读 [../../CODE_COMMENTING_GUIDE.md](../../CODE_COMMENTING_GUIDE.md)，了解工具 schema、注册表、tool_call_id 和并发代码的注释标准。 3. 运行 `practice/05_function_calling.py`，观察模型如何选择工具和传参。 4. 运行 `practice/06_parallel_function_calling.py`，观察多个工具调用如何并发执行。 5. 阅读 [resources/TOOL_CALLING_ACCURACY.md](./resources/TOOL_CALLING_ACCURACY.md)，理解工具很多时如何提升选择准确率。 6. 阅读 [resources/TOOL_ERROR_RECOVERY.md](./resources/TOOL_ERROR_RECOVERY.md)，理解错误分类、有限重试、降级和 partial success。 7. 阅读 [resources/NOISY_TOOL_RESULTS.md](./resources/NOISY_TOOL_RESULTS.md)，理解工具返回不可靠时如何做 evidence processing。 8. 阅读 [materials/INTERVIEW_QA.md](./materials/INTERVIEW_QA.md)，准备工具调用面试回答。 9. 完成 [materials/MINI_QUIZ.md](./materials/MINI_QUIZ.md)，再用 [lecture/CHAPTER_SUMMARY.md](./lecture/CHAPTER_SUMMARY.md) 复盘。 ## 快速运行 从课程根目录激活环境： ```ba"
    },
    {
      "id": "L04_langchain_quickstart",
      "code": "L04",
      "title": "L04 LangChain 快速上手：Agent 开发的瑞士军刀",
      "intro": "本章承接 L03 的手写 Function Calling 循环，目标是让学生理解为什么需要 Agent 框架，以及如何用 LangChain/LangGraph 把模型、工具、Prompt、记忆和执行循环组合起来。",
      "topics": [
        "LangChain",
        "LangGraph",
        "自定义工具",
        "Agent 记忆",
        "搜索 Agent"
      ],
      "goals": [
        "理解 LangChain 主要解决什么重复劳动。",
        "能把 L03 手写工具循环映射到 Model、Prompt、Tools、Memory、Agent 五个组件。",
        "掌握 `@tool`、Pydantic 参数 schema、`create_agent` 的基础用法。",
        "跑通一个能查天气、看时间、做计算的 LangChain Agent。",
        "理解 `MemorySaver` 与 `thread_id` 如何支持多轮对话记忆。",
        "能说清 LangChain 与 LangGraph 的区别和选型边界。"
      ],
      "deliverables": [
        "一张 L03 手写代码到 LangChain 组件的映射表。",
        "一次 `practice/07_langchain_agent.py` 的工具调用日志。",
        "一个带 Pydantic 参数 schema 的自定义工具。",
        "一次同一 `thread_id` 与不同 `thread_id` 的记忆对比结果。",
        "一份 LangChain 与 LangGraph 选型说明。",
        "一个“搜索信息 -> 保存笔记 -> 查看笔记”的课后扩展方案。"
      ],
      "docs": [
        {
          "key": "readme",
          "label": "章节入口",
          "path": "lessons/L04_langchain_quickstart/README.md",
          "contentPath": "data/docs/L04_langchain_quickstart/readme.md",
          "excerpt": "# L04 LangChain 快速上手：Agent 开发的瑞士军刀 本章承接 L03 的手写 Function Calling 循环，目标是让学生理解为什么需要 Agent 框架，以及如何用 LangChain/LangGraph 把模型、工具、Prompt、记忆和执行循环组合起来。 ## 本章学习目标 - 理解 LangChain 主要解决什么重复劳动。 - 能把 L03 手写工具循环映射到 Model、Prompt、Tools、Memory、Agent 五个组件。 - 掌握 `@tool`、Pydantic 参数 schema、`create_agent` 的基础用法。 - 跑通一个能查天气、看时间、做计算的 LangChain Agent。 - 理解 `MemorySaver` 与 `thread_id` 如何支持多轮对话记忆。 - 能说清 LangChain 与 LangGraph 的区别和选型边界。 ## 文件分区 "
        },
        {
          "key": "lecture",
          "label": "完整讲义",
          "path": "lessons/L04_langchain_quickstart/lecture/LECTURE_FULL.md",
          "contentPath": "data/docs/L04_langchain_quickstart/lecture.md",
          "excerpt": "# 第 4 讲：LangChain 快速上手 —— Agent 开发的瑞士军刀 ## 4.1 为什么需要框架？ 在第 3 讲中，我们手写了 Function Calling 的完整循环。它能跑，也很适合帮助学生理解底层机制，但工程上会逐渐暴露出重复劳动： - 手动维护 `messages`。 - 手动解析模型返回的 `tool_calls`。 - 手动调用 Python 函数。 - 手动把工具结果带着 `tool_call_id` 塞回对话历史。 - 手动处理多轮、记忆、更多工具、错误恢复和日志。 LangChain/LangGraph 的价值，就是把这些常见 Agent 开发模式封装成可复用组件。你仍然要理解底层机制，但写业务时可以把精力放到工具设计、Prompt 设计、状态管理和效果评估上。 一个类比： - 手写 Function Calling 像自己用砖头砌房子，所有承重结构都要自己管。 - LangChain 像使用预"
        },
        {
          "key": "summary",
          "label": "章节总结",
          "path": "lessons/L04_langchain_quickstart/lecture/CHAPTER_SUMMARY.md",
          "contentPath": "data/docs/L04_langchain_quickstart/summary.md",
          "excerpt": "# L04 章节总结：LangChain 快速上手 ## 一句话总结 L04 的重点不是“框架比手写更高级”，而是理解框架帮我们封装了哪些重复流程，以及哪些关键设计仍然必须由开发者负责。 ## 核心概念 | 概念 | 本章理解 | | --- | --- | | Model | 用 `ChatOpenAI` 封装课程 `.env` 中的模型配置 | | Prompt | 约束 Agent 的角色、工具使用边界和回答风格 | | Tools | 用 `@tool` 把 Python 函数暴露给模型 | | Memory | 用 `MemorySaver` 和 `thread_id` 保存会话历史 | | Agent | 用 `create_agent` 组合模型、工具、Prompt 和循环 | ## 本章代码地图 - `practice/langchain_common.py`：公共模型构造、基础工具和安全计算。 - `pract"
        },
        {
          "key": "preclass",
          "label": "课前准备",
          "path": "lessons/L04_langchain_quickstart/materials/PRECLASS_CHECKLIST.md",
          "contentPath": "data/docs/L04_langchain_quickstart/preclass.md",
          "excerpt": "# L04 课前准备清单 ## 1. 环境检查 从课程根目录激活环境： ```bash source <course-root>/scripts/activate_course.sh ``` 安装 LangChain 相关依赖： ```bash cd <course-root> pip install -r requirements/langchain.txt ``` 检查基础环境： ```bash python scripts/check_env.py python scripts/smoke_openai.py ``` ## 2. 概念预习 - 复习 L03 的 Function Calling 循环。 - 能说出 `tool_calls`、工具执行、`tool_call_id` 的作用。 - 阅读 [../../../CODE_COMMENTING_GUIDE.md](../../../CODE_COMMENTING_GU"
        },
        {
          "key": "quiz",
          "label": "课后小测",
          "path": "lessons/L04_langchain_quickstart/materials/MINI_QUIZ.md",
          "contentPath": "data/docs/L04_langchain_quickstart/quiz.md",
          "excerpt": "# L04 课后小测 ## 选择/简答 1. LangChain 主要帮开发者省掉了哪些重复劳动？ 2. `@tool` 装饰器会把普通 Python 函数转换成什么？ 3. 为什么工具函数的 docstring 会影响 Agent 行为？ 4. `create_agent` 大致封装了哪些流程？ 5. `MemorySaver` 和 `thread_id` 分别解决什么问题？ 6. 为什么 `MemorySaver` 不适合作为生产级长期记忆？ 7. LangChain 和 LangGraph 的核心区别是什么？ 8. 搜索 Agent 为什么需要注明来源和不确定性？ ## 参考答案要点 1. 模型封装、Prompt 管理、工具 schema、工具调用循环、消息状态、记忆和基础编排。 2. 转换成模型可见、框架可执行的 `BaseTool`。 3. 模型会根据工具名、描述和参数说明判断是否调用以及如何传参。 4. 模型推理、工"
        },
        {
          "key": "extensions",
          "label": "拓展作业",
          "path": "lessons/L04_langchain_quickstart/materials/EXTENSIONS.md",
          "contentPath": "data/docs/L04_langchain_quickstart/extensions.md",
          "excerpt": "# L04 拓展练习 ## 必做：笔记工具 Agent 在 `practice/10_search_agent.py` 的基础上增加两个工具： 1. `write_note(title, content)`：把内容保存为 Markdown 文件。 2. `list_notes()`：列出已保存的笔记标题和路径。 要求： - 笔记只能写入本章目录下的 `materials/generated_notes/`。 - 标题要做文件名清洗，避免路径穿越。 - 保存成功后返回结构化信息：标题、路径、字符数。 - 实现“搜索信息 -> 保存笔记 -> 查看笔记”的完整流程。 ## 选做：真实搜索 API 把 mock `search_web` 替换成真实搜索 API，例如 Tavily、SerpAPI 或公司内部搜索服务。 要求： - API key 放在 `.env`。 - 搜索结果保留标题、摘要、URL、时间。 - 空结果和超时要有明确"
        },
        {
          "key": "interview",
          "label": "面试题",
          "path": "lessons/L04_langchain_quickstart/materials/INTERVIEW_QA.md",
          "contentPath": "data/docs/L04_langchain_quickstart/interview.md",
          "excerpt": "# L04 面试题速查：LangChain 快速上手 本章面试重点不是“背 API”，而是能解释框架解决了什么重复劳动，以及 LangChain 和 LangGraph 的边界。 ## 来源说明 - 题目来源：主要来自老师第 4 讲讲义中的“4.9 LangChain 是什么”和“4.10 LangChain 和 LangGraph 的区别”。 - 参考来源：LangChain/LangGraph 对比部分参考本章 [LANGCHAIN_LANGGRAPH_COMPARISON.md](../resources/LANGCHAIN_LANGGRAPH_COMPARISON.md)。 - 整理方式：前 3 题是对老师讲义内容的归纳整理；后 3 题结合本章代码示例和框架使用重点补充成面试表达。 - 补充边界：`@tool`、Pydantic schema、MemorySaver、thread_id 等问题来自本章实践代码和讲义主题，"
        },
        {
          "key": "resource:FRAMEWORK_PATTERNS",
          "label": "资源：FRAMEWORK_PATTERNS",
          "path": "lessons/L04_langchain_quickstart/resources/FRAMEWORK_PATTERNS.md",
          "contentPath": "data/docs/L04_langchain_quickstart/resource_FRAMEWORK_PATTERNS.md",
          "excerpt": "# LangChain 快速上手工程模式 ## 1. 手写循环到框架组件的映射 | 手写 Function Calling | LangChain/LangGraph | | --- | --- | | `client.chat.completions.create` | `ChatOpenAI` | | system/user/tool messages | 图状态里的 `messages` | | 工具 JSON Schema | `@tool` + 函数签名 + docstring | | 工具参数解析 | 框架基于 schema 解析 | | 工具函数映射表 | 工具列表 `tools=[...]` | | while 循环 | `create_agent` 图执行 | | 对话历史 | checkpo"
        },
        {
          "key": "resource:LANGCHAIN_LANGGRAPH_COMPARISON",
          "label": "资源：LANGCHAIN_LANGGRAPH_COMPARISON",
          "path": "lessons/L04_langchain_quickstart/resources/LANGCHAIN_LANGGRAPH_COMPARISON.md",
          "contentPath": "data/docs/L04_langchain_quickstart/resource_LANGCHAIN_LANGGRAPH_COMPARISON.md",
          "excerpt": "# LangChain 与 LangGraph 对比 ## 一句话区别 LangChain 是“组件库 + 链式框架”，适合快速搭建简单 LLM 应用；LangGraph 是“图编排引擎”，适合有状态、可循环、多分支、可持久化的复杂 Agent 工作流。 ## 核心定位 | 框架 | 定位 | 典型能力 | | --- | --- | --- | | LangChain | LLM 应用组件库 | 模型封装、Prompt、工具、RAG、链式组合 | | LangGraph | Agent 图编排引擎 | State、节点、边、循环、条件路由、检查点、人机协作 | ## 关键区别 | 维度 | LangChain | LangGraph | | --- | --- | --- | | 核心抽象 | Chain、组"
        },
        {
          "key": "resource:SEARCH_AGENT_ENGINEERING_NOTES",
          "label": "资源：SEARCH_AGENT_ENGINEERING_NOTES",
          "path": "lessons/L04_langchain_quickstart/resources/SEARCH_AGENT_ENGINEERING_NOTES.md",
          "contentPath": "data/docs/L04_langchain_quickstart/resource_SEARCH_AGENT_ENGINEERING_NOTES.md",
          "excerpt": "# 搜索问答 Agent 工程化补充 ## 1. 当前 demo 的边界 `practice/10_search_agent.py` 使用模拟搜索数据，适合课堂解释工具调用流程，但不代表真实搜索系统已经完成。 主要边界： - 搜索结果是 mock 数据，不保证时效性。 - 没有网页抓取和正文抽取。 - 没有来源可信度评分。 - 没有 rerank 和多源交叉验证。 - 没有持久化记忆。 ## 2. 如何改为流式输出 思路： 1. 创建 Agent 时仍然使用 `create_agent`。 2. 调用时使用 `agent.stream(...)` 而不是 `agent.invoke(...)`。 3. 使用 `stream_mode=\"updates\"` 观察每个节点更新。 4. 在 UI 中区分工具调用过程和"
        }
      ],
      "practiceFiles": [
        {
          "name": "07_langchain_agent.py",
          "path": "lessons/L04_langchain_quickstart/practice/07_langchain_agent.py",
          "size": "3.0 KB"
        },
        {
          "name": "08_custom_tools.py",
          "path": "lessons/L04_langchain_quickstart/practice/08_custom_tools.py",
          "size": "5.1 KB"
        },
        {
          "name": "09_agent_with_memory.py",
          "path": "lessons/L04_langchain_quickstart/practice/09_agent_with_memory.py",
          "size": "3.6 KB"
        },
        {
          "name": "10_search_agent.py",
          "path": "lessons/L04_langchain_quickstart/practice/10_search_agent.py",
          "size": "6.6 KB"
        },
        {
          "name": "langchain_common.py",
          "path": "lessons/L04_langchain_quickstart/practice/langchain_common.py",
          "size": "9.5 KB"
        },
        {
          "name": "preclass_run.sh",
          "path": "lessons/L04_langchain_quickstart/practice/preclass_run.sh",
          "size": "1.4 KB"
        }
      ],
      "resourceFiles": [
        {
          "name": "FRAMEWORK_PATTERNS.md",
          "path": "lessons/L04_langchain_quickstart/resources/FRAMEWORK_PATTERNS.md",
          "size": "2.0 KB"
        },
        {
          "name": "LANGCHAIN_LANGGRAPH_COMPARISON.md",
          "path": "lessons/L04_langchain_quickstart/resources/LANGCHAIN_LANGGRAPH_COMPARISON.md",
          "size": "1.9 KB"
        },
        {
          "name": "SEARCH_AGENT_ENGINEERING_NOTES.md",
          "path": "lessons/L04_langchain_quickstart/resources/SEARCH_AGENT_ENGINEERING_NOTES.md",
          "size": "1.4 KB"
        }
      ],
      "materialFiles": [
        {
          "name": "EXTENSIONS.md",
          "path": "lessons/L04_langchain_quickstart/materials/EXTENSIONS.md",
          "size": "1.5 KB"
        },
        {
          "name": "INTERVIEW_QA.md",
          "path": "lessons/L04_langchain_quickstart/materials/INTERVIEW_QA.md",
          "size": "3.3 KB"
        },
        {
          "name": "MINI_QUIZ.md",
          "path": "lessons/L04_langchain_quickstart/materials/MINI_QUIZ.md",
          "size": "1.3 KB"
        },
        {
          "name": "NOTES_TEMPLATE.md",
          "path": "lessons/L04_langchain_quickstart/materials/NOTES_TEMPLATE.md",
          "size": "993 B"
        },
        {
          "name": "PRECLASS_CHECKLIST.md",
          "path": "lessons/L04_langchain_quickstart/materials/PRECLASS_CHECKLIST.md",
          "size": "1.1 KB"
        }
      ],
      "dataFiles": [],
      "preclassCommand": "cd lessons/L04_langchain_quickstart && bash practice/preclass_run.sh",
      "fileCount": 17,
      "searchText": "# L04 LangChain 快速上手：Agent 开发的瑞士军刀 本章承接 L03 的手写 Function Calling 循环，目标是让学生理解为什么需要 Agent 框架，以及如何用 LangChain/LangGraph 把模型、工具、Prompt、记忆和执行循环组合起来。 ## 本章学习目标 - 理解 LangChain 主要解决什么重复劳动。 - 能把 L03 手写工具循环映射到 Model、Prompt、Tools、Memory、Agent 五个组件。 - 掌握 `@tool`、Pydantic 参数 schema、`create_agent` 的基础用法。 - 跑通一个能查天气、看时间、做计算的 LangChain Agent。 - 理解 `MemorySaver` 与 `thread_id` 如何支持多轮对话记忆。 - 能说清 LangChain 与 LangGraph 的区别和选型边界。 ## 文件分区 | 分类 | 路径 | 用途 | | --- | --- | --- | | 讲义 | [lecture/LECTURE_FULL.md](./lecture/LECTURE_FULL.md) | 第 4 讲完整讲义 | | 总结 | [lecture/CHAPTER_SUMMARY.md](./lecture/CHAPTER_SUMMARY.md) | 本章概念、代码结构与复盘清单 | | 工程参考 | [resources/](./resources/) | 框架映射、LangChain/LangGraph 对比和搜索 Agent 工程化说明 | | 课前准备 | [materials/PRECLASS_CHECKLIST.md](./materials/PRECLASS_CHECKLIST.md) | 环境、依赖和预习检查 | | 实操代码 | [practice/](./practice/) | LangChain Agent、自定义工具、记忆、搜索问答示例 | | 一键脚本 | [practice/preclass_run.sh](./practice/preclass_run.sh) | 自动执行 L04 环境检查和核心示例 | | 课堂笔记 | [materials/NOTES_TEMPLATE.md](./materials/NOTES_TEMPLATE.md) | 记录框架组件、运行日志和疑问 | | 课后小测 | [materials/MINI_QUIZ.md](./materials/MINI_QUIZ.md) | 检查核心概念和面试表达 | | 拓展练习 | [materials/EXTENSIONS.md](./materials/EXTENSIONS.md) | 笔记工具、流式输出、真实搜索 API 和评估练习 | | 面试速查 | [materials/INTERVIEW_QA.md](./materials/INTERVIEW_QA.md) | LangChain、LangGraph、工具、记忆和框架边界 | | 注释规范 | [../../CODE_COMMENTING_GUIDE.md](../../CODE_COMMENTING_GUIDE.md) | 阅读和编写课程代码时遵循的讲解标准 | ## 推荐学习路径 1. 先看 [materials/PRECLASS_CHECKLIST.md](./materials/PRECLASS_CHECKLIST.md)，确认 `langchain`、`langchain-openai`、`langgraph` 已安装。 2. 阅读 [lecture/LECTURE_FULL.md](./lecture/LECTURE_FULL.md) 的 4.1-4.4，理解为什么从手写循环迁移到框架。 3. 运行 `practice/07_langchain_agent.py`，观察 `create_agent` 如何接管工具调用循环。 4. 阅读并运行 `practice/08_custom_tools.py --describe`，理解 `@tool` 和 Pydantic 参数 schema。 5. 运行 `practice/09_agent_with_memory.py --demo`，观察 `thread_id` 对多轮记忆的影响。 6. 运行 `practice/10_search_agent.py --question \"请先搜索一下 AI Agent 有哪些典型应用？\"`，理解搜索问答 Agent 的结构。 7. 阅读 [resources/LANGCHAIN_LANGGRAPH_COMPARISON.md](./resources/LANGCHAIN_LANGGRAPH_COMPARISON.md)，理解框架选型边界。 8. 阅读 [materials/INTERVIEW_QA.md](./materials/INTERVIEW_QA.md)，准备 LangChain/LangGraph 面试表达。 9. 完成 [materials/MINI_QUIZ.md](./materials/MINI_QUIZ.md)，再"
    },
    {
      "id": "L05_rag",
      "code": "L05",
      "title": "L05 RAG 检索增强生成：让 Agent 拥有专属知识库",
      "intro": "本章承接 L03 的工具调用和 L04 的框架化 Agent，把“查资料再回答”做成一条完整链路。学生需要理解 RAG 的离线建库、在线检索、上下文增强、带引用生成，以及 PDF、表格、图片、权限和评估这些真实工程问题。",
      "topics": [
        "RAG",
        "BM25",
        "倒排索引",
        "Chunk",
        "Hybrid Search",
        "PDF RAG"
      ],
      "goals": [
        "理解 RAG = Retrieval-Augmented Generation，即检索增强生成。",
        "能区分不用 RAG 的“闭卷回答”和使用 RAG 的“开卷回答”。",
        "掌握离线阶段：文档解析、清洗、切分、索引。",
        "掌握在线阶段：问题检索、上下文构造、LLM 生成、引用来源。",
        "能跑通一个标准库版本地 RAG 系统，不依赖外部向量库也能理解核心流程。",
        "理解 chunk size、overlap、hybrid search、rerank、query rewrite 对效果的影响。",
        "理解 BM25 和倒排索引在关键词检索、Hybrid Search 中的作用。",
        "能说明 PDF RAG 中页眉页脚、图片、表格、图表、OCR 和可追溯引用的处理方式。"
      ],
      "deliverables": [
        "一张 RAG 离线/在线流程图。",
        "一次本地知识库构建日志。",
        "一次带引用的 RAG 问答结果。",
        "一次 chunk size 对比记录。",
        "一份 RAG 失败排查清单。",
        "一份 PDF RAG 处理方案：页眉页脚、图片、表格、图表、OCR、metadata、引用。",
        "一组面试题复盘：RAG vs 微调、Hybrid Search、Reranker、Agentic RAG、权限、安全、评估。"
      ],
      "docs": [
        {
          "key": "readme",
          "label": "章节入口",
          "path": "lessons/L05_rag/README.md",
          "contentPath": "data/docs/L05_rag/readme.md",
          "excerpt": "# L05 RAG 检索增强生成：让 Agent 拥有专属知识库 本章承接 L03 的工具调用和 L04 的框架化 Agent，把“查资料再回答”做成一条完整链路。学生需要理解 RAG 的离线建库、在线检索、上下文增强、带引用生成，以及 PDF、表格、图片、权限和评估这些真实工程问题。 ## 本章学习目标 - 理解 RAG = Retrieval-Augmented Generation，即检索增强生成。 - 能区分不用 RAG 的“闭卷回答”和使用 RAG 的“开卷回答”。 - 掌握离线阶段：文档解析、清洗、切分、索引。 - 掌握在线阶段：问题检索、上下文构造、LLM 生成、引用来源。 - 能跑通一个标准库版本地 RAG 系统，不依赖外部向量库也能理解核心流程。 - 理解 chunk size、overlap、hybrid search、rerank、query rewrite 对效果的影响。 - 理解 BM25 和倒排索引在"
        },
        {
          "key": "lecture",
          "label": "完整讲义",
          "path": "lessons/L05_rag/lecture/LECTURE_FULL.md",
          "contentPath": "data/docs/L05_rag/lecture.md",
          "excerpt": "# 第 5 讲：RAG 检索增强生成 —— 让 Agent 拥有专属知识库 ## 5.1 什么是 RAG？ RAG = Retrieval-Augmented Generation，中文叫“检索增强生成”。 不要被名字吓到，可以用一个很直观的比喻理解： - 不用 RAG 的 LLM：闭卷考试。模型只能靠参数里已有的知识回答，遇到没学过、过期或私有知识时容易编造。 - 使用 RAG 的 LLM：开卷考试。回答前先翻资料，找到相关段落，再基于资料回答。 RAG 的核心思路： ```text 用户问题 ↓ 先从知识库检索相关内容 ↓ 把检索内容 + 用户问题 一起给 LLM ↓ LLM 基于资料生成答案 ``` 例子： ```text 用户问题：我们公司的年假政策是什么？ 检索结果： 资料1：员工入职满 1 年享有 5 天年假。 资料2：年假需提前 3 个工作日申请。 增强后的 prompt： 根据以下资料回答问题： 资料1：员工入职"
        },
        {
          "key": "summary",
          "label": "章节总结",
          "path": "lessons/L05_rag/lecture/CHAPTER_SUMMARY.md",
          "contentPath": "data/docs/L05_rag/summary.md",
          "excerpt": "# L05 章节总结：RAG 检索增强生成 ## 一句话总结 RAG 的本质是：让模型回答前先查资料，并要求它基于查到的资料回答。 ## 核心流程 | 阶段 | 关键动作 | | --- | --- | | 离线建库 | 文档接入、解析、清洗、切分、embedding、建索引 | | 在线问答 | Query rewrite、检索、rerank、上下文构造、生成、引用 | ## 本章代码地图 - `practice/rag_common.py`：本地 RAG 公共逻辑。 - `practice/11_prepare_knowledge_base.py`：生成示例文档。 - `practice/12_build_local_index.py`：构建标准库版本地索引。 - `practice/13_rag_agent.py`：检索上下文并调用 LLM 生成答案。 - `practice/14_chunking_compare.py`"
        },
        {
          "key": "preclass",
          "label": "课前准备",
          "path": "lessons/L05_rag/materials/PRECLASS_CHECKLIST.md",
          "contentPath": "data/docs/L05_rag/preclass.md",
          "excerpt": "# L05 课前准备清单 ## 1. 环境检查 激活课程环境： ```bash source <course-root>/scripts/activate_course.sh ``` 基础检查： ```bash cd <course-root> python scripts/check_env.py python scripts/smoke_openai.py ``` 本章练习代码默认使用 Python 标准库 + OpenAI SDK，可在未安装向量库时运行。若要尝试 Chroma/FAISS 生产路线，可安装： ```bash pip install -r requirements/rag.txt ``` ## 2. 概念预习 - RAG = 检索 + 增强 + 生成。 - 离线阶段：解析、清洗、切分、索引。 - 在线阶段：query、检索、rerank、上下文、生成。 - Chunk size 和 overlap 会影响召"
        },
        {
          "key": "quiz",
          "label": "课后小测",
          "path": "lessons/L05_rag/materials/MINI_QUIZ.md",
          "contentPath": "data/docs/L05_rag/quiz.md",
          "excerpt": "# L05 课后小测 ## 简答题 1. RAG 的三个单词分别是什么意思？ 2. RAG 和 Fine-tuning 的区别是什么？ 3. RAG 的离线阶段包含哪些步骤？ 4. RAG 的在线阶段包含哪些步骤？ 5. Chunk size 过大和过小分别有什么问题？ 6. 为什么 RAG 需要引用来源？ 7. Hybrid Search 为什么常用于企业知识库？ 8. Reranker 和 Embedding 检索有什么区别？ 9. PDF RAG 中页眉页脚为什么可能污染检索？ 10. 知识库没有答案时，RAG 系统应该怎么做？ ## 参考答案要点 1. Retrieval、Augmented、Generation。 2. RAG 在推理时接入外部知识，微调通过训练改变模型参数。 3. 数据接入、解析、清洗、切分、embedding、索引。 4. query 理解、检索、rerank、上下文构造、生成、引用。 5. 过大噪"
        },
        {
          "key": "extensions",
          "label": "拓展作业",
          "path": "lessons/L05_rag/materials/EXTENSIONS.md",
          "contentPath": "data/docs/L05_rag/extensions.md",
          "excerpt": "# L05 拓展练习 ## 必做：自带文档 RAG 用你自己的 3-5 个文档替换 `data/knowledge_base/` 中的示例文档，重新构建索引。 要求： - 至少 5 个测试问题。 - 记录 TopK 检索结果。 - 标注答案是否被引用支撑。 - 至少分析 1 个失败样例。 ## 必做：Rewrite 或 Rerank 二选一： - Rewrite：把用户问题改写成更适合检索的 query。 - Rerank：对初步召回结果重新排序，例如增加关键词命中分、标题命中分、来源权重。 记录优化前后对比。 ## 选做：chunk size 对比 对比 `chunk_size=200/500/1000`： - Top1 是否命中。 - TopK 是否有正确 chunk。 - 上下文噪声是否增加。 - 最终答案是否变好。 ## 选做：接入真实向量库 将标准库本地索引替换成 Chroma 或 FAISS。 建议路线： 1. 安装"
        },
        {
          "key": "interview",
          "label": "面试题",
          "path": "lessons/L05_rag/materials/INTERVIEW_QA.md",
          "contentPath": "data/docs/L05_rag/interview.md",
          "excerpt": "# L05 面试题速查：RAG ## 来源说明 - 题目来源：来自老师提供的“RAG 相关面试题”材料。 - 整理方式：本文件基本保留老师材料的题目结构和回答要点，只做了目录归位、标题统一和少量格式整理。 - 补充边界：如后续增加课堂案例或项目经验，应在新增段落中单独标注“补充案例”，避免和老师原始题库混淆。 ## 基础概念 ### 1. 什么是 RAG？解决什么问题？ RAG 是 Retrieval-Augmented Generation，即检索增强生成。它在模型生成答案前，先从外部知识库检索相关资料，再把资料作为上下文交给模型回答。 解决： - 知识更新。 - 私有知识访问。 - 降低幻觉。 - 来源可追溯。 ### 2. 一个典型 RAG 系统包含哪些模块？ 数据接入、数据清洗、文档切分、embedding、索引存储、query rewrite、retrieval、rerank、上下文构造、生成答案、引用与评估。 ###"
        },
        {
          "key": "resource:PDF_RAG_PROCESS",
          "label": "资源：PDF_RAG_PROCESS",
          "path": "lessons/L05_rag/resources/PDF_RAG_PROCESS.md",
          "contentPath": "data/docs/L05_rag/resource_PDF_RAG_PROCESS.md",
          "excerpt": "# PDF RAG 切分处理流程 PDF 做 RAG 的核心原则不是“转成纯文本后直接切”，而是先做版面解析和结构还原，再决定哪些信息进入 chunk、哪些进入 metadata、哪些作为独立资源索引、哪些可以丢弃。 ## 1. PDF 信息分类 | 信息类型 | 推荐处理 | | --- | --- | | 正文文本 | 清洗后进入主 chunk | | 标题/章节/页码/文档名 | 进入 metadata，必要时拼入 chunk 前缀 | | 图片/图表/表格 | 转成可检索文本描述或结构化数据 | | 页眉/页脚/水印 | 无语义重复内容删除，有价值信息入 metadata | | 脚注/图注/表注 | 与对应正文、图表或表格关联 | ## 2. 页眉页脚 常见页眉页脚包括公司名、文档标题、章节名、页码、"
        },
        {
          "key": "resource:RAG_ENGINEERING_PATTERNS",
          "label": "资源：RAG_ENGINEERING_PATTERNS",
          "path": "lessons/L05_rag/resources/RAG_ENGINEERING_PATTERNS.md",
          "contentPath": "data/docs/L05_rag/resource_RAG_ENGINEERING_PATTERNS.md",
          "excerpt": "# RAG 工程模式与排查清单 ## 1. 标准 RAG 架构 ```text 数据源 ↓ 解析清洗 ↓ Chunking ↓ Embedding / 关键词索引 / 结构化索引 ↓ Retriever ↓ Reranker ↓ Context Builder ↓ LLM ↓ Answer + Citations ``` ## 2. 效果差时如何排查 - 数据源：知识库是否真的有答案？文档是否过期、缺失、冲突？ - 解析：PDF 表格、图片、标题、页眉页脚是否处理正确？ - 切分：chunk 是否过大、过小、缺标题、缺 overlap？ - 检索：TopK 是否太小？query 是否需要 rewrite？是否需要 hybrid search？ - 重排：正确 chunk 是否被 reranker 排到前面？ -"
        }
      ],
      "practiceFiles": [
        {
          "name": "11_prepare_knowledge_base.py",
          "path": "lessons/L05_rag/practice/11_prepare_knowledge_base.py",
          "size": "1.2 KB"
        },
        {
          "name": "12_build_local_index.py",
          "path": "lessons/L05_rag/practice/12_build_local_index.py",
          "size": "1.7 KB"
        },
        {
          "name": "13_rag_agent.py",
          "path": "lessons/L05_rag/practice/13_rag_agent.py",
          "size": "1.9 KB"
        },
        {
          "name": "14_chunking_compare.py",
          "path": "lessons/L05_rag/practice/14_chunking_compare.py",
          "size": "1.7 KB"
        },
        {
          "name": "rag_common.py",
          "path": "lessons/L05_rag/practice/rag_common.py",
          "size": "16.2 KB"
        },
        {
          "name": "preclass_run.sh",
          "path": "lessons/L05_rag/practice/preclass_run.sh",
          "size": "1.3 KB"
        }
      ],
      "resourceFiles": [
        {
          "name": "PDF_RAG_PROCESS.md",
          "path": "lessons/L05_rag/resources/PDF_RAG_PROCESS.md",
          "size": "4.5 KB"
        },
        {
          "name": "RAG_ENGINEERING_PATTERNS.md",
          "path": "lessons/L05_rag/resources/RAG_ENGINEERING_PATTERNS.md",
          "size": "1.8 KB"
        }
      ],
      "materialFiles": [
        {
          "name": "EXTENSIONS.md",
          "path": "lessons/L05_rag/materials/EXTENSIONS.md",
          "size": "1.4 KB"
        },
        {
          "name": "INTERVIEW_QA.md",
          "path": "lessons/L05_rag/materials/INTERVIEW_QA.md",
          "size": "7.0 KB"
        },
        {
          "name": "MINI_QUIZ.md",
          "path": "lessons/L05_rag/materials/MINI_QUIZ.md",
          "size": "1.3 KB"
        },
        {
          "name": "NOTES_TEMPLATE.md",
          "path": "lessons/L05_rag/materials/NOTES_TEMPLATE.md",
          "size": "993 B"
        },
        {
          "name": "PRECLASS_CHECKLIST.md",
          "path": "lessons/L05_rag/materials/PRECLASS_CHECKLIST.md",
          "size": "1.1 KB"
        }
      ],
      "dataFiles": [
        {
          "name": "company_policy.txt",
          "path": "lessons/L05_rag/data/knowledge_base/company_policy.txt",
          "size": "669 B"
        },
        {
          "name": "onboarding.txt",
          "path": "lessons/L05_rag/data/knowledge_base/onboarding.txt",
          "size": "903 B"
        },
        {
          "name": "tech_guide.txt",
          "path": "lessons/L05_rag/data/knowledge_base/tech_guide.txt",
          "size": "973 B"
        }
      ],
      "preclassCommand": "cd lessons/L05_rag && bash practice/preclass_run.sh",
      "fileCount": 19,
      "searchText": "# L05 RAG 检索增强生成：让 Agent 拥有专属知识库 本章承接 L03 的工具调用和 L04 的框架化 Agent，把“查资料再回答”做成一条完整链路。学生需要理解 RAG 的离线建库、在线检索、上下文增强、带引用生成，以及 PDF、表格、图片、权限和评估这些真实工程问题。 ## 本章学习目标 - 理解 RAG = Retrieval-Augmented Generation，即检索增强生成。 - 能区分不用 RAG 的“闭卷回答”和使用 RAG 的“开卷回答”。 - 掌握离线阶段：文档解析、清洗、切分、索引。 - 掌握在线阶段：问题检索、上下文构造、LLM 生成、引用来源。 - 能跑通一个标准库版本地 RAG 系统，不依赖外部向量库也能理解核心流程。 - 理解 chunk size、overlap、hybrid search、rerank、query rewrite 对效果的影响。 - 理解 BM25 和倒排索引在关键词检索、Hybrid Search 中的作用。 - 能说明 PDF RAG 中页眉页脚、图片、表格、图表、OCR 和可追溯引用的处理方式。 - 能回答 RAG 面试中的基础、工程、Agentic RAG 和企业级安全问题。 ## 文件分区 | 分类 | 路径 | 用途 | | --- | --- | --- | | 讲义 | [lecture/LECTURE_FULL.md](./lecture/LECTURE_FULL.md) | 第 5 讲完整讲义 | | 总结 | [lecture/CHAPTER_SUMMARY.md](./lecture/CHAPTER_SUMMARY.md) | 本章核心流程、工程要点和复盘清单 | | 工程参考 | [resources/](./resources/) | PDF RAG、工程模式与评估排查 | | 课前准备 | [materials/PRECLASS_CHECKLIST.md](./materials/PRECLASS_CHECKLIST.md) | 环境、概念和预习检查 | | 实操代码 | [practice/](./practice/) | 本地知识库、索引构建、RAG 问答、chunk 对比 | | 示例知识库 | [data/knowledge_base/](./data/knowledge_base/) | 由脚本生成的公司政策、技术规范、入职文档 | | 本地索引 | [data/rag_index/](./data/rag_index/) | 由脚本生成的 JSON 检索索引 | | 一键脚本 | [practice/preclass_run.sh](./practice/preclass_run.sh) | 自动执行 L05 环境检查和核心示例 | | 课堂笔记 | [materials/NOTES_TEMPLATE.md](./materials/NOTES_TEMPLATE.md) | 记录检索结果、失败样例和优化思路 | | 课后小测 | [materials/MINI_QUIZ.md](./materials/MINI_QUIZ.md) | 检查 RAG 原理和工程判断 | | 拓展练习 | [materials/EXTENSIONS.md](./materials/EXTENSIONS.md) | rerank、rewrite、PDF、真实向量库、评估集 | | 面试速查 | [materials/INTERVIEW_QA.md](./materials/INTERVIEW_QA.md) | RAG 基础、工程、Agentic RAG、权限和安全面试题 | | 注释规范 | [../../CODE_COMMENTING_GUIDE.md](../../CODE_COMMENTING_GUIDE.md) | 阅读和编写课程代码时遵循的讲解标准 | ## 推荐学习路径 1. 阅读 [materials/PRECLASS_CHECKLIST.md](./materials/PRECLASS_CHECKLIST.md)，确认 L01-L04 环境仍然可用。 2. 阅读 [lecture/LECTURE_FULL.md](./lecture/LECTURE_FULL.md) 的 5.1-5.3，理解 RAG 的闭卷/开卷比喻和离线/在线两阶段。 3. 运行 `practice/11_prepare_knowledge_base.py`，生成三份示例公司文档。 4. 运行 `practice/12_build_local_index.py`，观察文档如何被切分、索引和检索。 5. 运行 `practice/13_rag_agent.py --question \"我入职2年了，有几天年假？\" --show-context`，观察上下文如何增强答案。 6. 运行 `practice/14_chunking_compare.py`，比较不同 chunk size 对召回的影响。 7. 阅读 [教辅资料：BM25 和倒排索引简单介绍](../../teaching_support/BM25_INVERTED_INDEX.md)，理解关键"
    },
    {
      "id": "L06_langchain_advanced",
      "code": "L06",
      "title": "L06 LangChain 深入：LCEL、Parser、Retriever 与 Callback",
      "intro": "本章承接 L04 的 LangChain 快速上手和 L05 的 RAG，深入 LangChain 的核心抽象：分层架构、LCEL 管道、链组合、结构化输出、自定义 Retriever、Callback 观测，以及一个智能文档处理综合案例。",
      "topics": [
        "LCEL",
        "Retriever",
        "Output Parser",
        "Callback",
        "LangChain 架构"
      ],
      "goals": [
        "理解 LangChain 分层架构：基础层、模型层、能力层、编排层、应用层。",
        "掌握 LCEL 管道语法：`prompt | llm | output_parser`。",
        "学会串联、并行、分支三类链组合方式。",
        "使用 `PydanticOutputParser` 和 `JsonOutputParser` 获取结构化输出。",
        "理解自定义 Retriever 的设计，尤其是关键词 + 语义/本地索引的融合思路。",
        "使用 Callback 记录 chain、LLM、retriever、错误和耗时。",
        "综合构建一个智能文档处理 Agent，输出摘要、关键词、行动项和结构化报告。"
      ],
      "deliverables": [
        "一张 LangChain 分层架构图。",
        "一张 LCEL 数据流图。",
        "一次 LCEL 基础链运行结果。",
        "一个 Pydantic Output Parser 示例。",
        "一个自定义 Retriever 去重/融合方案分析。",
        "一次 Callback 事件日志。",
        "一份智能文档处理报告。"
      ],
      "docs": [
        {
          "key": "readme",
          "label": "章节入口",
          "path": "lessons/L06_langchain_advanced/README.md",
          "contentPath": "data/docs/L06_langchain_advanced/readme.md",
          "excerpt": "# L06 LangChain 深入：LCEL、Parser、Retriever 与 Callback 本章承接 L04 的 LangChain 快速上手和 L05 的 RAG，深入 LangChain 的核心抽象：分层架构、LCEL 管道、链组合、结构化输出、自定义 Retriever、Callback 观测，以及一个智能文档处理综合案例。 ## 本章学习目标 - 理解 LangChain 分层架构：基础层、模型层、能力层、编排层、应用层。 - 掌握 LCEL 管道语法：`prompt | llm | output_parser`。 - 学会串联、并行、分支三类链组合方式。 - 使用 `PydanticOutputParser` 和 `JsonOutputParser` 获取结构化输出。 - 理解自定义 Retriever 的设计，尤其是关键词 + 语义/本地索引的融合思路。 - 使用 Callback 记录 chain、LL"
        },
        {
          "key": "lecture",
          "label": "完整讲义",
          "path": "lessons/L06_langchain_advanced/lecture/LECTURE_FULL.md",
          "contentPath": "data/docs/L06_langchain_advanced/lecture.md",
          "excerpt": "# 第 6 讲：LangChain 深入 —— Agent 开发核心框架 ## 6.1 为什么要深入学 LangChain？ 第 4 讲中，我们用 LangChain 快速搭建了一个简单 Agent。但 LangChain 的能力远不止工具调用。它是目前 Agent 开发中最成熟、生态最丰富的框架之一。 本讲目标： - 理解 LangChain 的分层架构。 - 掌握 LCEL 管道语法。 - 学会组合 Chain：串联、并行、分支。 - 使用 Output Parser 实现结构化输出。 - 设计自定义 Retriever。 - 使用 Callback 监控运行过程。 - 综合搭建智能文档处理 Agent。 ## 6.2 LangChain 分层架构 LangChain 不是一个单一库，而是一套模块化框架体系。 ```text 应用层 LangGraph（复杂流程编排） ↑ 编排层 Chain（链式调用）、Agent（自主决策"
        },
        {
          "key": "summary",
          "label": "章节总结",
          "path": "lessons/L06_langchain_advanced/lecture/CHAPTER_SUMMARY.md",
          "contentPath": "data/docs/L06_langchain_advanced/summary.md",
          "excerpt": "# L06 章节总结：LangChain 深入 ## 一句话总结 L06 的重点是掌握 LangChain 的核心连接方式 LCEL，以及让链路可组合、可解析、可检索、可观测。 ## 核心概念 | 概念 | 本章理解 | | --- | --- | | Runnable | LangChain 组件统一调用协议 | | LCEL | 用 `|` 组合组件的表达式语言 | | Output Parser | 把模型输出转成文本、JSON 或 Pydantic 对象 | | Retriever | 将 query 转换成相关文档列表 | | Callback | 观察 chain、llm、tool、retriever 的运行事件 | | RunnableParallel | 并行执行多个子链 | | RunnableBranch | 条件路由 | | RunnableLambda | 把普通函数接入链 | ## 本章代码地图 - `"
        },
        {
          "key": "preclass",
          "label": "课前准备",
          "path": "lessons/L06_langchain_advanced/materials/PRECLASS_CHECKLIST.md",
          "contentPath": "data/docs/L06_langchain_advanced/preclass.md",
          "excerpt": "# L06 课前准备清单 ## 1. 环境检查 ```bash source <course-root>/scripts/activate_course.sh cd <course-root> python scripts/check_env.py python scripts/smoke_openai.py ``` 确认依赖： - `langchain` - `langchain-core` - `langchain-openai` - `langgraph` - `pydantic` ## 2. 概念预习 - 复习 L04：`create_agent`、`@tool`、`MemorySaver`。 - 复习 L05：Retriever、chunk、RAG 检索链路。 - 阅读 [resources/LANGCHAIN_LAYERED_ARCHITECTURE.md](../resources/LANGCHAIN_LAYERE"
        },
        {
          "key": "quiz",
          "label": "课后小测",
          "path": "lessons/L06_langchain_advanced/materials/MINI_QUIZ.md",
          "contentPath": "data/docs/L06_langchain_advanced/quiz.md",
          "excerpt": "# L06 课后小测 ## 简答题 1. LangChain 的五层架构分别是什么？ 2. LCEL 中 `|` 的作用是什么？ 3. `prompt | llm | StrOutputParser()` 的数据流是什么？ 4. `RunnableParallel` 适合什么场景？ 5. `RunnableBranch` 适合什么场景？ 6. Pydantic Output Parser 相比 JSON Parser 有什么优势？ 7. 自定义 Retriever 常见需求有哪些？ 8. 为什么 `content[:100]` 不适合作为去重 key？ 9. Callback 能监控哪些事件？ 10. 生产级 Callback 还需要补哪些能力？ ## 参考答案要点 1. 基础层、模型层、能力层、编排层、应用层。 2. 把 Runnable 组件按输入输出连接成链。 3. 输入 dict -> Prompt 生成 message"
        },
        {
          "key": "extensions",
          "label": "拓展作业",
          "path": "lessons/L06_langchain_advanced/materials/EXTENSIONS.md",
          "contentPath": "data/docs/L06_langchain_advanced/extensions.md",
          "excerpt": "# L06 拓展练习 ## 必做：新增 LCEL 链 在 `16_lcel_composition.py` 中新增一条链： ```text 输入文章 -> 翻译英文 -> 摘要 -> 改写成商务风格 ``` 要求： - 每一步用独立 prompt。 - 打印每一步中间结果。 - 分析串联链的错误传播风险。 ## 必做：自定义 Parser 结构 在 `17_output_parsers.py` 中新增一个 Pydantic 模型，例如： - 会议纪要结构。 - Bug 报告结构。 - 需求分析结构。 要求字段有描述、类型和必要校验。 ## 选做：Retriever 融合排序 改进 `18_custom_retriever.py`： - 增加标题命中权重。 - 增加 source 权威权重。 - 把去重 key 改为 `source + chunk_id`。 - 打印每个候选的分数组成。 ## 选做：Callback 日志持久化 "
        },
        {
          "key": "interview",
          "label": "面试题",
          "path": "lessons/L06_langchain_advanced/materials/INTERVIEW_QA.md",
          "contentPath": "data/docs/L06_langchain_advanced/interview.md",
          "excerpt": "# L06 面试题速查：LangChain 深入 本章面试重点是 LCEL、结构化输出、自定义 Retriever 和 Callback 可观测性。不要只说“会用 LangChain”，要能讲清输入输出如何流动、复杂链路如何调试。 ## 来源说明 - 题目来源：老师第 6 讲提供的是 LangChain 深入讲义内容，包括分层架构、LCEL、Output Parser、自定义 Retriever、Callback 和智能文档处理案例；并没有单独提供一份“面试题清单”。 - 整理方式：本文件是基于老师第 6 讲主题和本章配套代码整理出的面试速查，不是老师逐字面试题。 - 补充边界：生产级 Callback、Retriever 权限过滤、run_id 隔离、日志持久化等属于工程化补充，用于帮助学生把课堂概念转成面试表达。 ## 1. LCEL 是什么？ LCEL 是 LangChain Expression Language，用统一"
        },
        {
          "key": "resource:CALLBACK_OBSERVABILITY",
          "label": "资源：CALLBACK_OBSERVABILITY",
          "path": "lessons/L06_langchain_advanced/resources/CALLBACK_OBSERVABILITY.md",
          "contentPath": "data/docs/L06_langchain_advanced/resource_CALLBACK_OBSERVABILITY.md",
          "excerpt": "# Callback 机制与可观测性 Callback 的作用是观察 LangChain 运行过程：链什么时候开始、模型什么时候调用、工具是否被执行、检索是否命中、哪里报错、耗时和 token 如何。 ## 常见用途 - 运行观测：记录 chain、llm、tool、retriever 的开始、结束、耗时、输入输出摘要。 - Token 与成本统计：统计 prompt、completion、total token，并换算成本。 - 调试排错：定位哪一步最慢、哪一步报错、工具为什么被调用。 - 流式输出：在 `on_llm_new_token` 中实时展示 token。 - 质量审计：记录 prompt、工具参数、模型回复，用于复盘幻觉和错误工具调用。 - 安全合规：检查敏感词、PII、越权工具调用、危险指令。 "
        },
        {
          "key": "resource:LANGCHAIN_LAYERED_ARCHITECTURE",
          "label": "资源：LANGCHAIN_LAYERED_ARCHITECTURE",
          "path": "lessons/L06_langchain_advanced/resources/LANGCHAIN_LAYERED_ARCHITECTURE.md",
          "contentPath": "data/docs/L06_langchain_advanced/resource_LANGCHAIN_LAYERED_ARCHITECTURE.md",
          "excerpt": "# LangChain 分层架构 ## 1. 分层图 ```text 应用层 典型组件：LangGraph 作用：复杂流程编排、状态图、多分支、多 Agent ↑ 基于下层能力构建 编排层 典型组件：Chain、Agent 作用：链式调用、自主决策、任务流程 ↑ 基于下层能力构建 能力层 典型组件：Retriever、Memory、Tool、Output Parser 作用：检索、记忆、工具调用、结构化输出 ↑ 基于下层能力构建 模型层 典型组件：ChatModel、LLM、Embedding 作用：封装不同厂商的模型 API ↑ 基于下层能力构建 基础层 典型组件：langchain-core、Runnable、LCEL 作用：统一调用协议，像 USB 接口标准一样连接各种组件 ``` ## 2. 各层类比 "
        },
        {
          "key": "resource:LCEL_DATA_FLOW",
          "label": "资源：LCEL_DATA_FLOW",
          "path": "lessons/L06_langchain_advanced/resources/LCEL_DATA_FLOW.md",
          "contentPath": "data/docs/L06_langchain_advanced/resource_LCEL_DATA_FLOW.md",
          "excerpt": "# LCEL 管道数据流 LCEL 的核心表达是： ```python chain = prompt | llm | output_parser ``` ## 数据流 ```text {\"role\": \"...\", \"question\": \"...\"} │ ▼ ┌────────────────┐ │ Prompt │ │ 填充模板变量 │ │ 生成 messages │ └───────┬────────┘ │ messages ▼ ┌────────────────┐ │ LLM / ChatModel │ │ 调用模型生成回复 │ └───────┬────────┘ │ AIMessage ▼ ┌────────────────┐ │ OutputParser │ │ 从消息中提取结果 │ └─────"
        },
        {
          "key": "resource:RETRIEVER_DESIGN_NOTES",
          "label": "资源：RETRIEVER_DESIGN_NOTES",
          "path": "lessons/L06_langchain_advanced/resources/RETRIEVER_DESIGN_NOTES.md",
          "contentPath": "data/docs/L06_langchain_advanced/resource_RETRIEVER_DESIGN_NOTES.md",
          "excerpt": "# 自定义 Retriever 设计笔记 ## 为什么要自定义 Retriever？ 默认向量检索适合语义相似问题，但真实项目常常需要： - 关键词强匹配，例如错误码、API 路径、函数名。 - 权限过滤。 - 多知识源路由。 - 元数据过滤，例如版本、部门、文档状态。 - 多路召回融合，例如向量 + BM25 + 标题匹配。 - 去重和 rerank。 ## 去重方案分析 不要简单使用 `content[:100]` 作为去重 key。 问题： - 前缀相同但后文不同，会误判重复。 - 前缀不同但内容相同，会漏去重。 - 没有归一化，空格、大小写、页眉差异会造成重复。 更好的方案： 1. 优先使用业务稳定 ID，例如 `source + chunk_index`。 2. 没有 ID 时使用规范化后的完整内容 "
        }
      ],
      "practiceFiles": [
        {
          "name": "15_lcel_basics.py",
          "path": "lessons/L06_langchain_advanced/practice/15_lcel_basics.py",
          "size": "1.5 KB"
        },
        {
          "name": "16_lcel_composition.py",
          "path": "lessons/L06_langchain_advanced/practice/16_lcel_composition.py",
          "size": "3.5 KB"
        },
        {
          "name": "17_output_parsers.py",
          "path": "lessons/L06_langchain_advanced/practice/17_output_parsers.py",
          "size": "3.8 KB"
        },
        {
          "name": "18_custom_retriever.py",
          "path": "lessons/L06_langchain_advanced/practice/18_custom_retriever.py",
          "size": "6.4 KB"
        },
        {
          "name": "19_callbacks.py",
          "path": "lessons/L06_langchain_advanced/practice/19_callbacks.py",
          "size": "3.4 KB"
        },
        {
          "name": "20_doc_processor_agent.py",
          "path": "lessons/L06_langchain_advanced/practice/20_doc_processor_agent.py",
          "size": "4.6 KB"
        },
        {
          "name": "langchain_advanced_common.py",
          "path": "lessons/L06_langchain_advanced/practice/langchain_advanced_common.py",
          "size": "3.8 KB"
        },
        {
          "name": "preclass_run.sh",
          "path": "lessons/L06_langchain_advanced/practice/preclass_run.sh",
          "size": "1.3 KB"
        }
      ],
      "resourceFiles": [
        {
          "name": "CALLBACK_OBSERVABILITY.md",
          "path": "lessons/L06_langchain_advanced/resources/CALLBACK_OBSERVABILITY.md",
          "size": "1.7 KB"
        },
        {
          "name": "LANGCHAIN_LAYERED_ARCHITECTURE.md",
          "path": "lessons/L06_langchain_advanced/resources/LANGCHAIN_LAYERED_ARCHITECTURE.md",
          "size": "1.5 KB"
        },
        {
          "name": "LCEL_DATA_FLOW.md",
          "path": "lessons/L06_langchain_advanced/resources/LCEL_DATA_FLOW.md",
          "size": "1.4 KB"
        },
        {
          "name": "RETRIEVER_DESIGN_NOTES.md",
          "path": "lessons/L06_langchain_advanced/resources/RETRIEVER_DESIGN_NOTES.md",
          "size": "1.3 KB"
        }
      ],
      "materialFiles": [
        {
          "name": "EXTENSIONS.md",
          "path": "lessons/L06_langchain_advanced/materials/EXTENSIONS.md",
          "size": "1.1 KB"
        },
        {
          "name": "INTERVIEW_QA.md",
          "path": "lessons/L06_langchain_advanced/materials/INTERVIEW_QA.md",
          "size": "3.8 KB"
        },
        {
          "name": "MINI_QUIZ.md",
          "path": "lessons/L06_langchain_advanced/materials/MINI_QUIZ.md",
          "size": "1.3 KB"
        },
        {
          "name": "NOTES_TEMPLATE.md",
          "path": "lessons/L06_langchain_advanced/materials/NOTES_TEMPLATE.md",
          "size": "808 B"
        },
        {
          "name": "PRECLASS_CHECKLIST.md",
          "path": "lessons/L06_langchain_advanced/materials/PRECLASS_CHECKLIST.md",
          "size": "966 B"
        }
      ],
      "dataFiles": [],
      "preclassCommand": "cd lessons/L06_langchain_advanced && bash practice/preclass_run.sh",
      "fileCount": 20,
      "searchText": "# L06 LangChain 深入：LCEL、Parser、Retriever 与 Callback 本章承接 L04 的 LangChain 快速上手和 L05 的 RAG，深入 LangChain 的核心抽象：分层架构、LCEL 管道、链组合、结构化输出、自定义 Retriever、Callback 观测，以及一个智能文档处理综合案例。 ## 本章学习目标 - 理解 LangChain 分层架构：基础层、模型层、能力层、编排层、应用层。 - 掌握 LCEL 管道语法：`prompt | llm | output_parser`。 - 学会串联、并行、分支三类链组合方式。 - 使用 `PydanticOutputParser` 和 `JsonOutputParser` 获取结构化输出。 - 理解自定义 Retriever 的设计，尤其是关键词 + 语义/本地索引的融合思路。 - 使用 Callback 记录 chain、LLM、retriever、错误和耗时。 - 综合构建一个智能文档处理 Agent，输出摘要、关键词、行动项和结构化报告。 ## 文件分区 | 分类 | 路径 | 用途 | | --- | --- | --- | | 讲义 | [lecture/LECTURE_FULL.md](./lecture/LECTURE_FULL.md) | 第 6 讲完整讲义 | | 总结 | [lecture/CHAPTER_SUMMARY.md](./lecture/CHAPTER_SUMMARY.md) | 本章核心抽象、代码地图和复盘清单 | | 工程参考 | [resources/](./resources/) | LangChain 分层、LCEL 数据流、Callback 能力清单 | | 课前准备 | [materials/PRECLASS_CHECKLIST.md](./materials/PRECLASS_CHECKLIST.md) | 环境、概念和预习检查 | | 实操代码 | [practice/](./practice/) | LCEL、Parser、Retriever、Callback、综合案例 | | 一键脚本 | [practice/preclass_run.sh](./practice/preclass_run.sh) | 自动执行 L06 环境检查和核心示例 | | 课堂笔记 | [materials/NOTES_TEMPLATE.md](./materials/NOTES_TEMPLATE.md) | 记录链路、输出结构、回调事件和失败点 | | 课后小测 | [materials/MINI_QUIZ.md](./materials/MINI_QUIZ.md) | 检查核心概念和面试表达 | | 拓展练习 | [materials/EXTENSIONS.md](./materials/EXTENSIONS.md) | 更复杂分支、日志持久化、成本统计、文档处理增强 | | 面试速查 | [materials/INTERVIEW_QA.md](./materials/INTERVIEW_QA.md) | LCEL、Parser、Retriever、Callback 和文档处理案例 | | 注释规范 | [../../CODE_COMMENTING_GUIDE.md](../../CODE_COMMENTING_GUIDE.md) | 阅读和编写课程代码时遵循的讲解标准 | ## 推荐学习路径 1. 阅读 [materials/PRECLASS_CHECKLIST.md](./materials/PRECLASS_CHECKLIST.md)，确认 L04/L05 的环境仍然可用。 2. 阅读 [resources/LANGCHAIN_LAYERED_ARCHITECTURE.md](./resources/LANGCHAIN_LAYERED_ARCHITECTURE.md)，建立分层框架图。 3. 运行 `practice/15_lcel_basics.py`，理解 `prompt | llm | parser` 的数据流。 4. 运行 `practice/16_lcel_composition.py`，观察串联、并行和条件分支。 5. 运行 `practice/17_output_parsers.py`，学习 Pydantic 和 JSON 两种结构化输出。 6. 运行 `practice/18_custom_retriever.py`，理解自定义 Retriever 和去重/融合排序。 7. 运行 `practice/19_callbacks.py`，观察 Callback 记录的链路事件。 8. 运行 `practice/20_doc_processor_agent.py`，完成智能文档处理综合案例。 9. 阅读 [materials/INTERVIEW_QA.md](./materials/INTERVIEW_QA.md)，准备 LangChain 深入面试表达。 ## 快速运行 从课程根目录激活环境： ```bash source <course-root>/scripts/a"
    },
    {
      "id": "L07_memory_systems",
      "code": "L07",
      "title": "L07 记忆系统：让 Agent 越用越懂你",
      "intro": "本章承接 L04 的会话记忆和 L05/L06 的检索能力，系统讲清 Agent 的记忆设计：短期记忆、长期记忆、外部知识、知识图谱、记忆检索策略和遗忘机制。",
      "topics": [
        "Memory",
        "短期记忆",
        "长期记忆",
        "摘要记忆",
        "混合记忆"
      ],
      "goals": [
        "理解 Agent 记忆三层架构：短期记忆、长期记忆、外部知识。",
        "掌握短期记忆的滑动窗口和摘要压缩策略。",
        "用 JSON 文件实现跨会话长期记忆。",
        "理解向量记忆、知识图谱记忆和混合检索的差异。",
        "把长期记忆封装为工具接入 LangChain Agent。",
        "理解记忆遗忘：TTL、LRU/LFU、衰减、重要性、摘要压缩、去重和显式删除。",
        "能说明记忆污染、隐私合规、跨用户隔离和记忆更新的一致性问题。"
      ],
      "deliverables": [
        "一张 Agent 记忆三层架构图。",
        "一次滑动窗口前后消息对比。",
        "一次摘要压缩前后消息对比。",
        "一个 JSON 长期记忆文件。",
        "一个知识图谱多跳路径示例。",
        "一个长期记忆 Agent 的两轮运行日志。",
        "一份记忆遗忘策略设计：profile、preferences、facts、KG、隐私字段分别怎么处理。"
      ],
      "docs": [
        {
          "key": "readme",
          "label": "章节入口",
          "path": "lessons/L07_memory_systems/README.md",
          "contentPath": "data/docs/L07_memory_systems/readme.md",
          "excerpt": "# L07 记忆系统：让 Agent 越用越懂你 本章承接 L04 的会话记忆和 L05/L06 的检索能力，系统讲清 Agent 的记忆设计：短期记忆、长期记忆、外部知识、知识图谱、记忆检索策略和遗忘机制。 ## 本章学习目标 - 理解 Agent 记忆三层架构：短期记忆、长期记忆、外部知识。 - 掌握短期记忆的滑动窗口和摘要压缩策略。 - 用 JSON 文件实现跨会话长期记忆。 - 理解向量记忆、知识图谱记忆和混合检索的差异。 - 把长期记忆封装为工具接入 LangChain Agent。 - 理解记忆遗忘：TTL、LRU/LFU、衰减、重要性、摘要压缩、去重和显式删除。 - 能说明记忆污染、隐私合规、跨用户隔离和记忆更新的一致性问题。 ## 文件分区 | 分类 | 路径 | 用途 | | --- | --- | --- | | 讲义 | [lecture/LECTURE_FULL.md](./lecture/LECTURE"
        },
        {
          "key": "lecture",
          "label": "完整讲义",
          "path": "lessons/L07_memory_systems/lecture/LECTURE_FULL.md",
          "contentPath": "data/docs/L07_memory_systems/lecture.md",
          "excerpt": "# 第 7 讲：记忆系统 —— 让 Agent 越用越懂你 学习时长：90-120 分钟 配套代码：`practice/21_memory_window.py` 到 `practice/25_agent_with_long_memory.py` 章节总结：[CHAPTER_SUMMARY.md](./CHAPTER_SUMMARY.md) ## 7.1 为什么记忆这么重要？ 想象一下，你每天都要和一个同事合作，但他每天早上都忘了昨天说过的所有事。项目背景、你的偏好、之前做过的决定，都要重新解释一遍。 没有记忆的 Agent 就是这样：每次交互都像第一次见面。记忆让 Agent 从“一次性工具”变成“持续成长的助手”。 Agent 的记忆可以分为三层： ```text 短期记忆 Working Memory 当前对话上下文，像工作台，正在处理当前任务。 长期记忆 Long-term Memory 跨对话保存的信息，像笔记本，记录用"
        },
        {
          "key": "summary",
          "label": "章节总结",
          "path": "lessons/L07_memory_systems/lecture/CHAPTER_SUMMARY.md",
          "contentPath": "data/docs/L07_memory_systems/summary.md",
          "excerpt": "# L07 章节总结：记忆系统 ## 一句话总结 Agent 记忆不是把所有历史都塞给模型，而是根据记忆类型选择保存、检索、压缩、更新和遗忘策略。 ## 核心概念 | 概念 | 本章理解 | | --- | --- | | 短期记忆 | 当前会话上下文，受上下文窗口限制 | | 长期记忆 | 跨会话保存用户画像、偏好、事实和任务结果 | | 外部知识 | RAG 知识库、数据库、文档系统 | | 滑动窗口 | 只保留最近 N 轮，简单但会丢早期关键信息 | | 摘要压缩 | 把旧对话折叠成摘要，节省 token 但会丢细节 | | 用户画像 | key/value 型记忆，适合 upsert 覆盖 | | 事实流 | 事件型记忆，适合 append、检索和审计 | | 知识图谱 | 用实体-关系-实体表达结构化关系和多跳推理 | | 遗忘机制 | 主动删除、过期、压缩或合并记忆，避免噪声和合规风险 | ## 本章代码地图 - `"
        },
        {
          "key": "preclass",
          "label": "课前准备",
          "path": "lessons/L07_memory_systems/materials/PRECLASS_CHECKLIST.md",
          "contentPath": "data/docs/L07_memory_systems/preclass.md",
          "excerpt": "# L07 课前准备清单 ## 1. 环境检查 从课程根目录激活环境： ```bash source <course-root>/scripts/activate_course.sh ``` 检查基础环境： ```bash python scripts/check_env.py python scripts/smoke_openai.py ``` ## 2. 概念预习 - [ ] 我能解释短期记忆、长期记忆和外部知识的区别。 - [ ] 我知道 `messages` 是最小短期记忆。 - [ ] 我知道 `MemorySaver` 不是生产级长期记忆。 - [ ] 我能解释为什么长期记忆需要“遗忘机制”。 - [ ] 我知道用户画像、事实流、偏好和知识图谱适合不同写入策略。 ## 3. 代码预习 ```bash cd <course-root>/lessons/L07_memory_systems python practice"
        },
        {
          "key": "quiz",
          "label": "课后小测",
          "path": "lessons/L07_memory_systems/materials/MINI_QUIZ.md",
          "contentPath": "data/docs/L07_memory_systems/quiz.md",
          "excerpt": "# L07 课后小测 ## 题目 1. Agent 记忆三层架构分别是什么？ 2. 滑动窗口记忆的优点和缺点是什么？ 3. 摘要压缩为什么可能带来信息漂移？ 4. 用户画像为什么适合 upsert？ 5. facts 和 preferences 为什么更适合 append？ 6. 向量检索和知识图谱在记忆系统里分别解决什么问题？ 7. `MemorySaver` 和长期记忆有什么区别？ 8. 为什么长期记忆必须有遗忘机制？ 9. 说出三种遗忘策略，并说明适用场景。 10. 用户要求删除个人隐私信息时，系统应该如何处理？ ## 参考答案 1. 短期记忆、长期记忆、外部知识。 2. 优点是简单稳定、成本可控；缺点是早期重要信息可能被裁掉。 3. 摘要会压缩细节，多次压缩可能丢失事实或引入不存在的信息。 4. 用户画像通常以最新值为准，例如姓名、职位、团队，因此同 key 覆盖更合理。 5. 事实和偏好是事件流，保留历史有利于溯源、冲"
        },
        {
          "key": "extensions",
          "label": "拓展作业",
          "path": "lessons/L07_memory_systems/materials/EXTENSIONS.md",
          "contentPath": "data/docs/L07_memory_systems/extensions.md",
          "excerpt": "# L07 拓展练习 ## 1. Token 预算裁剪 把 `21_memory_window.py` 从“按轮数裁剪”改成“按 token 预算裁剪”。 要求： - system 消息必须保留。 - 最近消息优先保留。 - 输出裁剪前后估算 token 数。 ## 2. 结构化摘要 修改 `22_memory_summary.py`，让摘要输出 JSON： ```json { \"user_profile\": {}, \"preferences\": [], \"open_tasks\": [], \"decisions\": [] } ``` ## 3. 记忆冲突合并 在 `23_long_term_memory_json.py` 中实现： ```text 用户以前喜欢 Java 用户现在主要用 Python ``` 要求新偏好能覆盖旧偏好，旧偏好进入历史记录。 ## 4. 遗忘 API 给 JSON 长期记忆增加： - `forget_"
        },
        {
          "key": "interview",
          "label": "面试题",
          "path": "lessons/L07_memory_systems/materials/INTERVIEW_QA.md",
          "contentPath": "data/docs/L07_memory_systems/interview.md",
          "excerpt": "# L07 面试题题库：Agent 记忆系统 Memory ## 来源说明 - 题目来源：来自老师补充的“记忆相关面试题”题库，并结合第 7 讲记忆系统讲义统一整理。 - 整理方式：保留老师题库的难度分层和核心回答要点，做了标题、表格、结构化表达和少量措辞统一。 - 补充边界：跨用户隔离、审计、权限继承、Prompt Injection 持久化等内容来自老师题库，本文件只做课程化归纳；如后续加入项目经验，会单独标注为“工程补充”。 ## 一、简单难度：基础概念 ### 1. 什么是 Agent 的记忆系统？它解决什么问题？ Agent 记忆系统是让智能体在多轮对话、长期使用或任务执行过程中，保存、检索和利用历史信息的能力。 它主要解决： - 上下文窗口有限：模型一次只能看到有限 token，重要信息需要外部化存储并按需召回。 - 个性化：记住用户偏好、工作习惯、常用工具和表达风格。 - 任务连续性：用户隔几天回来后，Agent "
        },
        {
          "key": "resource:CHROMA_MEMORY_OPTIONAL",
          "label": "资源：CHROMA_MEMORY_OPTIONAL",
          "path": "lessons/L07_memory_systems/resources/CHROMA_MEMORY_OPTIONAL.md",
          "contentPath": "data/docs/L07_memory_systems/resource_CHROMA_MEMORY_OPTIONAL.md",
          "excerpt": "# Chroma 长期记忆可选实现说明 老师讲义中给出了基于 Chroma 的长期记忆版本。本课程默认练习使用标准库 JSON，是为了保证没有安装 `chromadb` 时也能跑通主线。 ## 什么时候使用 Chroma 适合： - 记忆量较大。 - 需要语义检索。 - 用户表达和存储文本不完全一致。 - 需要持久化向量索引。 不适合： - 只有几十条结构化画像。 - 需要强一致精确查询。 - 没有权限过滤和删除治理。 ## Collection 设计 建议拆成三个 collection： | Collection | 写入语义 | 说明 | | --- | --- | --- | | `user_profile` | upsert | key/value 画像，同 key 覆盖 | | `facts` | a"
        },
        {
          "key": "resource:MEMORY_ARCHITECTURE",
          "label": "资源：MEMORY_ARCHITECTURE",
          "path": "lessons/L07_memory_systems/resources/MEMORY_ARCHITECTURE.md",
          "contentPath": "data/docs/L07_memory_systems/resource_MEMORY_ARCHITECTURE.md",
          "excerpt": "# Agent 记忆三层架构 ## 三层划分 ```text 短期记忆 Working Memory 当前对话上下文，通常是 messages 或 checkpointer。 长期记忆 Long-term Memory 跨会话保存用户画像、偏好、事实和任务结果。 外部知识 External Knowledge 企业知识库、数据库、文档系统、搜索系统。 ``` ## 类比 | 层级 | 类比 | 典型实现 | | --- | --- | --- | | 短期记忆 | 工作台 | messages、MemorySaver、summary buffer | | 长期记忆 | 笔记本 | JSON、SQLite、Postgres、Chroma、Redis | | 外部知识 | 图书馆 | RAG、数据库、搜索 API、"
        },
        {
          "key": "resource:MEMORY_FORGETTING",
          "label": "资源：MEMORY_FORGETTING",
          "path": "lessons/L07_memory_systems/resources/MEMORY_FORGETTING.md",
          "contentPath": "data/docs/L07_memory_systems/resource_MEMORY_FORGETTING.md",
          "excerpt": "# 记忆遗忘机制 长期记忆必须支持遗忘。遗忘不是缺陷，而是主动的记忆治理。 ## 为什么要遗忘 1. 存储和索引成本会持续增长。 2. 低质量旧记忆会污染检索结果。 3. 用户偏好和事实会变化。 4. 隐私与合规要求用户可删除个人数据。 ## 八类策略 | 策略 | 一句话 | 适用场景 | | --- | --- | --- | | TTL | 超过时间自动过期 | 临时事实、新闻、短期任务 | | 滑动窗口 | 只保留最近 N 条 | 短期上下文 | | 衰减函数 | 记忆强度随时间下降，命中后增强 | 长期偏好、人格化记忆 | | LRU/LFU | 淘汰最近最少使用或最少访问 | 容量有限场景 | | 重要性打分 | 低重要性优先遗忘 | 长期事实流 | | 摘要压缩 | 多条折叠成摘要 | 长对话和长"
        },
        {
          "key": "resource:MEMORY_RETRIEVAL_STRATEGIES",
          "label": "资源：MEMORY_RETRIEVAL_STRATEGIES",
          "path": "lessons/L07_memory_systems/resources/MEMORY_RETRIEVAL_STRATEGIES.md",
          "contentPath": "data/docs/L07_memory_systems/resource_MEMORY_RETRIEVAL_STRATEGIES.md",
          "excerpt": "# 记忆检索策略 核心问题：从海量记忆中找到“对的那条”。 ## 策略对比 | 策略 | 优点 | 缺点 | 适用场景 | | --- | --- | --- | --- | | 关键词检索 | 精确、便宜、可解释 | 无语义泛化 | 姓名、ID、项目名、技术名 | | 向量检索 | 语义理解强 | 对精确字段可能不稳定 | 偏好、事实、自然语言记忆 | | 知识图谱 | 支持关系和多跳 | 构建成本高 | 人-项目-组织-技术关系 | | 多路召回 | 覆盖全面 | 成本和复杂度更高 | 生产级个人助手 | ## 推荐生产流程 ```text query -> 意图判断：是否需要记忆 -> 用户权限过滤 -> 多路召回：关键词 + 向量 + 图谱 -> 去重 -> 按相关性、时间、重要性、可信度重排 -> 构"
        }
      ],
      "practiceFiles": [
        {
          "name": "21_memory_window.py",
          "path": "lessons/L07_memory_systems/practice/21_memory_window.py",
          "size": "2.5 KB"
        },
        {
          "name": "22_memory_summary.py",
          "path": "lessons/L07_memory_systems/practice/22_memory_summary.py",
          "size": "3.1 KB"
        },
        {
          "name": "23_long_term_memory_json.py",
          "path": "lessons/L07_memory_systems/practice/23_long_term_memory_json.py",
          "size": "2.5 KB"
        },
        {
          "name": "24_hybrid_memory_graph.py",
          "path": "lessons/L07_memory_systems/practice/24_hybrid_memory_graph.py",
          "size": "3.8 KB"
        },
        {
          "name": "25_agent_with_long_memory.py",
          "path": "lessons/L07_memory_systems/practice/25_agent_with_long_memory.py",
          "size": "6.0 KB"
        },
        {
          "name": "memory_common.py",
          "path": "lessons/L07_memory_systems/practice/memory_common.py",
          "size": "23.5 KB"
        },
        {
          "name": "preclass_run.sh",
          "path": "lessons/L07_memory_systems/practice/preclass_run.sh",
          "size": "643 B"
        }
      ],
      "resourceFiles": [
        {
          "name": "CHROMA_MEMORY_OPTIONAL.md",
          "path": "lessons/L07_memory_systems/resources/CHROMA_MEMORY_OPTIONAL.md",
          "size": "1.8 KB"
        },
        {
          "name": "MEMORY_ARCHITECTURE.md",
          "path": "lessons/L07_memory_systems/resources/MEMORY_ARCHITECTURE.md",
          "size": "1.1 KB"
        },
        {
          "name": "MEMORY_FORGETTING.md",
          "path": "lessons/L07_memory_systems/resources/MEMORY_FORGETTING.md",
          "size": "1.9 KB"
        },
        {
          "name": "MEMORY_RETRIEVAL_STRATEGIES.md",
          "path": "lessons/L07_memory_systems/resources/MEMORY_RETRIEVAL_STRATEGIES.md",
          "size": "1.2 KB"
        }
      ],
      "materialFiles": [
        {
          "name": "EXTENSIONS.md",
          "path": "lessons/L07_memory_systems/materials/EXTENSIONS.md",
          "size": "1.2 KB"
        },
        {
          "name": "INTERVIEW_QA.md",
          "path": "lessons/L07_memory_systems/materials/INTERVIEW_QA.md",
          "size": "23.7 KB"
        },
        {
          "name": "MINI_QUIZ.md",
          "path": "lessons/L07_memory_systems/materials/MINI_QUIZ.md",
          "size": "1.6 KB"
        },
        {
          "name": "NOTES_TEMPLATE.md",
          "path": "lessons/L07_memory_systems/materials/NOTES_TEMPLATE.md",
          "size": "1.0 KB"
        },
        {
          "name": "PRECLASS_CHECKLIST.md",
          "path": "lessons/L07_memory_systems/materials/PRECLASS_CHECKLIST.md",
          "size": "1.6 KB"
        }
      ],
      "dataFiles": [
        {
          "name": "hybrid_memory.json",
          "path": "lessons/L07_memory_systems/data/hybrid_memory.json",
          "size": "1.9 KB"
        },
        {
          "name": "kg_memory.json",
          "path": "lessons/L07_memory_systems/data/kg_memory.json",
          "size": "1.5 KB"
        },
        {
          "name": "user_memory.json",
          "path": "lessons/L07_memory_systems/data/user_memory.json",
          "size": "1.3 KB"
        }
      ],
      "preclassCommand": "cd lessons/L07_memory_systems && bash practice/preclass_run.sh",
      "fileCount": 22,
      "searchText": "# L07 记忆系统：让 Agent 越用越懂你 本章承接 L04 的会话记忆和 L05/L06 的检索能力，系统讲清 Agent 的记忆设计：短期记忆、长期记忆、外部知识、知识图谱、记忆检索策略和遗忘机制。 ## 本章学习目标 - 理解 Agent 记忆三层架构：短期记忆、长期记忆、外部知识。 - 掌握短期记忆的滑动窗口和摘要压缩策略。 - 用 JSON 文件实现跨会话长期记忆。 - 理解向量记忆、知识图谱记忆和混合检索的差异。 - 把长期记忆封装为工具接入 LangChain Agent。 - 理解记忆遗忘：TTL、LRU/LFU、衰减、重要性、摘要压缩、去重和显式删除。 - 能说明记忆污染、隐私合规、跨用户隔离和记忆更新的一致性问题。 ## 文件分区 | 分类 | 路径 | 用途 | | --- | --- | --- | | 讲义 | [lecture/LECTURE_FULL.md](./lecture/LECTURE_FULL.md) | 第 7 讲完整讲义 | | 总结 | [lecture/CHAPTER_SUMMARY.md](./lecture/CHAPTER_SUMMARY.md) | 记忆架构、代码地图和复盘清单 | | 课前准备 | [materials/PRECLASS_CHECKLIST.md](./materials/PRECLASS_CHECKLIST.md) | 环境、概念和预习检查 | | 实操代码 | [practice/](./practice/) | 滑动窗口、摘要、JSON 记忆、图谱记忆、长期记忆 Agent | | 一键脚本 | [practice/preclass_run.sh](./practice/preclass_run.sh) | 自动执行 L07 环境检查和核心示例 | | 课堂笔记 | [materials/NOTES_TEMPLATE.md](./materials/NOTES_TEMPLATE.md) | 记录记忆策略、检索结果和遗忘设计 | | 课后小测 | [materials/MINI_QUIZ.md](./materials/MINI_QUIZ.md) | 检查记忆系统核心概念 | | 拓展练习 | [materials/EXTENSIONS.md](./materials/EXTENSIONS.md) | Chroma、遗忘 API、冲突合并、隐私治理 | | 面试题库 | [materials/INTERVIEW_QA.md](./materials/INTERVIEW_QA.md) | Agent 记忆系统分难度题库、系统设计题和追问题 | | 工程参考 | [resources/](./resources/) | 记忆架构、检索策略、遗忘机制、Chroma 可选实现 | | 运行数据 | [data/](./data/) | JSON 记忆和知识图谱示例数据 | ## 推荐学习路径 1. 阅读 [materials/PRECLASS_CHECKLIST.md](./materials/PRECLASS_CHECKLIST.md)，确认 L04/L06 的 LangChain 环境可用。 2. 阅读 [lecture/LECTURE_FULL.md](./lecture/LECTURE_FULL.md) 的 7.1-7.2，理解短期记忆为什么会受上下文窗口限制。 3. 运行 `practice/21_memory_window.py`，观察滑动窗口如何丢失早期信息。 4. 运行 `practice/22_memory_summary.py`，观察摘要压缩如何保留早期关键信息。 5. 运行 `practice/23_long_term_memory_json.py --reset --query Python`，理解长期记忆的写入、搜索和持久化。 6. 运行 `practice/24_hybrid_memory_graph.py --reset --query Python --anchor 小明`，理解语义入口和知识图谱多跳扩展。 7. 阅读 [resources/MEMORY_FORGETTING.md](./resources/MEMORY_FORGETTING.md)，理解为什么长期记忆必须有遗忘机制。 8. 选择性运行 `practice/25_agent_with_long_memory.py --demo --reset`，观察 Agent 如何主动写入和读取长期记忆。 9. 阅读 [materials/INTERVIEW_QA.md](./materials/INTERVIEW_QA.md)，准备记忆系统面试题和系统设计题。 10. 完成 [materials/MINI_QUIZ.md](./materials/MINI_QUIZ.md)，再用 [lecture/CHAPTER_SUMMARY.md](./lecture/CHAPTER_SUMMARY.md) 复盘。 ## 快速运行 从课程根目录激活环境： ```bash source <course-root>/scripts/activate_course.sh ```"
    },
    {
      "id": "L08_agent_modes",
      "code": "L08",
      "title": "L08 Agent 模式：从 RAG/ReAct 到多 Agent 协作",
      "intro": "本章按老师给出的总主题“Agent 模式”整理：先学会判断一个任务应该用哪种 Agent 模式，再进入多 Agent 协作系统，最后落到企业知识库问答助手的工程选型和分库分索引策略。",
      "topics": [
        "Agent 模式",
        "Multi-Agent",
        "ReAct",
        "Supervisor",
        "分库分索引"
      ],
      "goals": [
        "理解常见 Agent 模式：Direct、RAG、ReAct、Plan-and-Execute、Reflection、多 Agent。",
        "能解释为什么企业知识库问答通常推荐“RAG 为主 + ReAct 为辅”。",
        "能用 ReAct、Plan-and-Execute、Reflection、Multi-Agent 四种经典模式解释复杂 Agent 的组织方式。",
        "掌握多 Agent 的三种基础协作形态：Supervisor、Sequential、Peer。",
        "用 LangGraph 搭建一个“调研员 -> 分析师 -> 撰写员 -> 审核员”的协作流程。",
        "理解分库分索引为什么能同时提升效果、安全、成本和运维可控性。",
        "能为企业知识库问答助手设计路由层、检索层、Agent 层、答案层和评测回流。"
      ],
      "deliverables": [
        "一张 Agent 模式选型表：Direct、RAG、ReAct、Plan-and-Execute、多 Agent 分别适合什么任务。",
        "一个 Supervisor 多 Agent 流程图，说明每个 Agent 的输入、输出和状态字段。",
        "一个企业知识库问答架构图：路由层、检索层、Agent 层、答案层、评测回流。",
        "一份分库分索引设计：业务域、敏感等级、数据形态、时效性如何组合。",
        "一次运行日志：同一个问题为什么走 RAG 或 ReAct，引用了哪些文档。",
        "一份面试题复盘：为什么不推荐纯 Fine-tune、纯 Plan-and-Execute 或大规模多 Agent 辩论。"
      ],
      "docs": [
        {
          "key": "readme",
          "label": "章节入口",
          "path": "lessons/L08_agent_modes/README.md",
          "contentPath": "data/docs/L08_agent_modes/readme.md",
          "excerpt": "# L08 Agent 模式：从 RAG/ReAct 到多 Agent 协作 本章按老师给出的总主题“Agent 模式”整理：先学会判断一个任务应该用哪种 Agent 模式，再进入多 Agent 协作系统，最后落到企业知识库问答助手的工程选型和分库分索引策略。 ## 本章学习目标 - 理解常见 Agent 模式：Direct、RAG、ReAct、Plan-and-Execute、Reflection、多 Agent。 - 能解释为什么企业知识库问答通常推荐“RAG 为主 + ReAct 为辅”。 - 能用 ReAct、Plan-and-Execute、Reflection、Multi-Agent 四种经典模式解释复杂 Agent 的组织方式。 - 掌握多 Agent 的三种基础协作形态：Supervisor、Sequential、Peer。 - 用 LangGraph 搭建一个“调研员 -> 分析师 -> 撰写员 -> 审核员”"
        },
        {
          "key": "lecture",
          "label": "完整讲义",
          "path": "lessons/L08_agent_modes/lecture/LECTURE_FULL.md",
          "contentPath": "data/docs/L08_agent_modes/lecture.md",
          "excerpt": "# 第8讲 Agent 模式：从 RAG/ReAct 到多 Agent 协作 第 8 讲的总题目是“Agent 模式”。这一章不是只讲“多 Agent”，而是要解决一个更前置的问题：面对一个真实任务，我们到底应该选择哪种 Agent 形态。 有些问题只需要模型直接回答，有些问题必须先检索企业知识库，有些问题需要多步推理和工具调用，还有些复杂任务适合拆成多个角色协作。模式选错了，系统就会在准确率、成本、延迟和可维护性之间一起失控。 ## 8.1 为什么要学习 Agent 模式 Agent 不是越复杂越好。工程里的核心判断是：用刚好足够的模式解决问题。 一个客服机器人问“你是谁”，直接回答就够；问“我入职 3 年有几天年假”，需要查企业制度；问“P0 工单响应时间和 API 发布审批有什么共同要求”，就可能需要跨库检索和多步综合；要写一份行业研报，则适合拆成调研、分析、写作、审核多个角色。 常见模式可以粗略分成六类： | 模式 | "
        },
        {
          "key": "summary",
          "label": "章节总结",
          "path": "lessons/L08_agent_modes/lecture/CHAPTER_SUMMARY.md",
          "contentPath": "data/docs/L08_agent_modes/summary.md",
          "excerpt": "# L08 章节总结 ## 一句话总结 第 8 章讲的是 Agent 模式选型：企业问答优先用 RAG 保证可信和可追溯，用 ReAct 处理多跳长尾；复杂产出型任务再用多 Agent 做角色分工和质量控制。 ## 模式速查 | 模式 | 什么时候用 | 什么时候别用 | | --- | --- | --- | | Direct | 通用问答、格式转换、无需私域知识 | 涉及企业制度、实时数据、审计要求 | | RAG | 企业知识库、制度问答、可引用答案 | 多跳、跨源、计算型问题 | | ReAct | 多步检索、工具调用、跨源融合 | 高频简单问题 | | Plan-and-Execute | 长流程任务、自动化项目 | 单次知识库问答 | | Reflection | 高风险输出、自检修正 | 低价值高频问答 | | Multi-Agent | 研报、方案、复杂协作 | 职责不清或流程很短的任务 | ## 企业知识库推荐"
        },
        {
          "key": "preclass",
          "label": "课前准备",
          "path": "lessons/L08_agent_modes/materials/PRECLASS_CHECKLIST.md",
          "contentPath": "data/docs/L08_agent_modes/preclass.md",
          "excerpt": "# L08 课前准备清单 ## 1. 环境检查 从课程根目录激活环境： ```bash source <course-root>/scripts/activate_course.sh ``` 检查基础环境： ```bash python scripts/check_env.py python scripts/smoke_openai.py ``` 进入第 8 章目录并运行预习脚本： ```bash cd <course-root>/lessons/L08_agent_modes bash practice/preclass_run.sh ``` 确认最后看到： ```text [OK] L08 preclass run completed. ``` ## 2. 概念预习 - [ ] 我能解释 Direct、RAG、ReAct、Plan-and-Execute、Reflection、Multi-Agent 的区别。 - [ ] 我"
        },
        {
          "key": "quiz",
          "label": "课后小测",
          "path": "lessons/L08_agent_modes/materials/MINI_QUIZ.md",
          "contentPath": "data/docs/L08_agent_modes/quiz.md",
          "excerpt": "# L08 课后小测 ## 题目 1. Direct、RAG、ReAct 三种模式的主要区别是什么？ 2. 为什么企业知识库问答通常以 RAG 为主？ 3. 单轮 RAG 在哪些场景下会失效？ 4. 为什么不推荐用纯 Fine-tune 做企业知识库问答主干？ 5. Supervisor、Sequential、Peer 三种多 Agent 模式分别是什么？ 6. 多 Agent 系统为什么必须有明确的状态协议？ 7. 为什么多 Agent 或 Reflection 大循环不适合所有问答场景？ 8. 企业知识库为什么要分库分索引？ 9. 多库召回后为什么需要统一 rerank？ 10. 权限过滤为什么应该前置到检索阶段？ ## 参考答案 1. Direct 直接生成，不接私域知识；RAG 先检索再生成，强调证据和引用；ReAct 在推理和行动之间循环，适合多步工具调用和跨源融合。 2. 因为企业知识通常私域、频繁更新、需要可追溯，"
        },
        {
          "key": "extensions",
          "label": "拓展作业",
          "path": "lessons/L08_agent_modes/materials/EXTENSIONS.md",
          "contentPath": "data/docs/L08_agent_modes/extensions.md",
          "excerpt": "# L08 拓展练习 ## 练习 1：增加 Translator Agent 在 `practice/26_supervisor_research_team.py` 中增加一个 `translator_agent`： - 输入：最终中文报告。 - 输出：英文摘要或英文全文。 - 要求：只有审核通过后才进入翻译。 - 思考：翻译结果是否还需要 Reviewer 再审核一次？ ## 练习 2：增加“澄清问题”模式 在 `practice/27_agent_mode_router.py` 中增加 `clarify` 模式： - 当问题缺少关键实体，例如“这个流程怎么走？”时，不直接检索。 - 先返回澄清问题，例如“请问你指的是 HR 入职流程、财务报销流程，还是研发发布流程？” - 记录：哪些规则容易误判？是否需要 LLM 分类器？ ## 练习 3：新增业务域和权限等级 在 `practice/agent_mode_common.py"
        },
        {
          "key": "interview",
          "label": "面试题",
          "path": "lessons/L08_agent_modes/materials/INTERVIEW_QA.md",
          "contentPath": "data/docs/L08_agent_modes/interview.md",
          "excerpt": "# L08 面试题库：Agent 模式、多 Agent 与企业知识库问答 说明：本题库基于老师第 8 讲“多 Agent 协作系统”和补充材料“企业知识库问答助手设计要点：Agent 模式选型与分库分索引策略”整理，并做了面试表达层面的结构化补充。补充内容用于帮助回答更完整，不替代原讲义观点。 ## 一、基础题 ### 1. 什么是 Agent 模式选型？ Agent 模式选型是指根据任务复杂度、知识来源、工具需求、可追溯要求、成本和延迟，选择 Direct、RAG、ReAct、Plan-and-Execute、Reflection 或 Multi-Agent 等模式。 面试回答要点： - 不同任务不应默认上最复杂的 Agent。 - 企业问答通常先判断是否需要私域知识。 - 需要多步检索、跨源融合或计算时，再升级到 ReAct。 - 需要角色分工和多阶段质量控制时，再考虑多 Agent。 ### 2. 企业知识库问答为什么推荐"
        },
        {
          "key": "resource:AGENT_MODE_PATTERNS",
          "label": "资源：AGENT_MODE_PATTERNS",
          "path": "lessons/L08_agent_modes/resources/AGENT_MODE_PATTERNS.md",
          "contentPath": "data/docs/L08_agent_modes/resource_AGENT_MODE_PATTERNS.md",
          "excerpt": "# Agent 模式选型速查 四种经典 Agent 设计模式的完整教辅讲解见 [Agent 设计模式](../../../teaching_support/AGENT_DESIGN_PATTERNS.md)。本文件更偏工程选型速查。 ## 1. 先用问题复杂度筛选 ```text 是否需要私域/实时知识？ 否 -> Direct 是 -> 是否单一事实查询？ 是 -> RAG 否 -> 是否需要多步、跨源、计算或工具？ 是 -> ReAct 否 -> RAG + 查询改写 是否需要长流程规划？ 是 -> Plan-and-Execute 是否需要多角色专业分工或质量审核？ 是 -> Multi-Agent 是否需要高风险自检？ 是 -> Reflection，但必须限制轮数和预算 ``` ## 2. 模式对比表"
        },
        {
          "key": "resource:ENTERPRISE_KB_AGENT_DESIGN",
          "label": "资源：ENTERPRISE_KB_AGENT_DESIGN",
          "path": "lessons/L08_agent_modes/resources/ENTERPRISE_KB_AGENT_DESIGN.md",
          "contentPath": "data/docs/L08_agent_modes/resource_ENTERPRISE_KB_AGENT_DESIGN.md",
          "excerpt": "# 企业知识库问答助手设计要点 本文档整理第 8 章补充材料中的两个核心设计问题： 1. Agent 模式选型。 2. 分库分索引策略。 ## 1. Agent 模式选型 ### 1.1 推荐模式 推荐使用： ```text RAG 为主 + ReAct 为辅 ``` RAG 负责把企业私域知识可靠地注入上下文，ReAct 负责处理单轮 RAG 难以覆盖的多跳、跨源、模糊和计算型长尾问题。 ### 1.2 为什么 RAG 是主干 企业知识库问答有四个关键要求： - 数据私域性：企业制度、合同、工单、研发文档通常不在通用模型训练集中。 - 可溯源：合规、审计和责任归属要求答案能追溯到文档、版本和 chunk。 - 知识时效：制度、流程、价格和接口会变化，检索更新比微调更新更轻。 - 幻觉抑制：相比纯 LLM 直答"
        },
        {
          "key": "resource:MULTI_AGENT_DESIGN_PATTERNS",
          "label": "资源：MULTI_AGENT_DESIGN_PATTERNS",
          "path": "lessons/L08_agent_modes/resources/MULTI_AGENT_DESIGN_PATTERNS.md",
          "contentPath": "data/docs/L08_agent_modes/resource_MULTI_AGENT_DESIGN_PATTERNS.md",
          "excerpt": "# 多 Agent 协作设计范式 ## 1. Supervisor 模式 Supervisor 模式由一个主管调度多个专家 Agent。 ```text User -> Supervisor -> Researcher -> Analyst -> Writer -> Reviewer -> Final Answer ``` 适合： - 问题可能落到不同业务域。 - 需要动态选择工具或专家。 - 需要质量审核和返工。 风险： - Supervisor 判断错会导致全局错误。 - 专家输出格式不稳定会影响后续节点。 - 如果返工条件不清晰，容易循环。 设计建议： - Supervisor 输出结构化路由决策。 - 每个专家 Agent 的输入输出都固定。 - 所有循环都设置最大次数。 ## 2. Sequentia"
        },
        {
          "key": "resource:MULTI_INDEX_STRATEGY",
          "label": "资源：MULTI_INDEX_STRATEGY",
          "path": "lessons/L08_agent_modes/resources/MULTI_INDEX_STRATEGY.md",
          "contentPath": "data/docs/L08_agent_modes/resource_MULTI_INDEX_STRATEGY.md",
          "excerpt": "# 分库分索引实施清单 这份清单用于把企业知识库从“一个大向量库”拆成可治理的多库架构。 ## 1. 建库前调查 | 问题 | 记录 | | --- | --- | | 有哪些业务域？ | | | 每个域的 owner 是谁？ | | | 数据源在哪里？ | | | 更新频率是多少？ | | | 敏感等级如何划分？ | | | 是否需要跨地域部署？ | | ## 2. Collection 命名建议 ```text kb_{domain}_{data_type}_{sensitivity}_{region} ``` 示例： ```text kb_hr_policy_internal_cn kb_finance_expense_confidential_cn kb_engineering_api_internal"
        }
      ],
      "practiceFiles": [
        {
          "name": "26_supervisor_research_team.py",
          "path": "lessons/L08_agent_modes/practice/26_supervisor_research_team.py",
          "size": "6.2 KB"
        },
        {
          "name": "27_agent_mode_router.py",
          "path": "lessons/L08_agent_modes/practice/27_agent_mode_router.py",
          "size": "4.9 KB"
        },
        {
          "name": "28_multi_index_retrieval.py",
          "path": "lessons/L08_agent_modes/practice/28_multi_index_retrieval.py",
          "size": "2.0 KB"
        },
        {
          "name": "agent_mode_common.py",
          "path": "lessons/L08_agent_modes/practice/agent_mode_common.py",
          "size": "8.6 KB"
        },
        {
          "name": "preclass_run.sh",
          "path": "lessons/L08_agent_modes/practice/preclass_run.sh",
          "size": "667 B"
        }
      ],
      "resourceFiles": [
        {
          "name": "AGENT_MODE_PATTERNS.md",
          "path": "lessons/L08_agent_modes/resources/AGENT_MODE_PATTERNS.md",
          "size": "2.7 KB"
        },
        {
          "name": "ENTERPRISE_KB_AGENT_DESIGN.md",
          "path": "lessons/L08_agent_modes/resources/ENTERPRISE_KB_AGENT_DESIGN.md",
          "size": "6.9 KB"
        },
        {
          "name": "MULTI_AGENT_DESIGN_PATTERNS.md",
          "path": "lessons/L08_agent_modes/resources/MULTI_AGENT_DESIGN_PATTERNS.md",
          "size": "2.9 KB"
        },
        {
          "name": "MULTI_INDEX_STRATEGY.md",
          "path": "lessons/L08_agent_modes/resources/MULTI_INDEX_STRATEGY.md",
          "size": "2.5 KB"
        }
      ],
      "materialFiles": [
        {
          "name": "EXTENSIONS.md",
          "path": "lessons/L08_agent_modes/materials/EXTENSIONS.md",
          "size": "2.2 KB"
        },
        {
          "name": "INTERVIEW_QA.md",
          "path": "lessons/L08_agent_modes/materials/INTERVIEW_QA.md",
          "size": "10.4 KB"
        },
        {
          "name": "MINI_QUIZ.md",
          "path": "lessons/L08_agent_modes/materials/MINI_QUIZ.md",
          "size": "1.9 KB"
        },
        {
          "name": "NOTES_TEMPLATE.md",
          "path": "lessons/L08_agent_modes/materials/NOTES_TEMPLATE.md",
          "size": "2.0 KB"
        },
        {
          "name": "PRECLASS_CHECKLIST.md",
          "path": "lessons/L08_agent_modes/materials/PRECLASS_CHECKLIST.md",
          "size": "2.9 KB"
        }
      ],
      "dataFiles": [
        {
          "name": "README.md",
          "path": "lessons/L08_agent_modes/data/README.md",
          "size": "445 B"
        }
      ],
      "preclassCommand": "cd lessons/L08_agent_modes && bash practice/preclass_run.sh",
      "fileCount": 18,
      "searchText": "# L08 Agent 模式：从 RAG/ReAct 到多 Agent 协作 本章按老师给出的总主题“Agent 模式”整理：先学会判断一个任务应该用哪种 Agent 模式，再进入多 Agent 协作系统，最后落到企业知识库问答助手的工程选型和分库分索引策略。 ## 本章学习目标 - 理解常见 Agent 模式：Direct、RAG、ReAct、Plan-and-Execute、Reflection、多 Agent。 - 能解释为什么企业知识库问答通常推荐“RAG 为主 + ReAct 为辅”。 - 能用 ReAct、Plan-and-Execute、Reflection、Multi-Agent 四种经典模式解释复杂 Agent 的组织方式。 - 掌握多 Agent 的三种基础协作形态：Supervisor、Sequential、Peer。 - 用 LangGraph 搭建一个“调研员 -> 分析师 -> 撰写员 -> 审核员”的协作流程。 - 理解分库分索引为什么能同时提升效果、安全、成本和运维可控性。 - 能为企业知识库问答助手设计路由层、检索层、Agent 层、答案层和评测回流。 ## 文件分区 | 分类 | 路径 | 用途 | | --- | --- | --- | | 讲义 | [lecture/LECTURE_FULL.md](./lecture/LECTURE_FULL.md) | 第 8 讲完整讲义：Agent 模式、多 Agent、企业知识库选型 | | 总结 | [lecture/CHAPTER_SUMMARY.md](./lecture/CHAPTER_SUMMARY.md) | 模式对比、代码地图和设计复盘 | | 课前准备 | [materials/PRECLASS_CHECKLIST.md](./materials/PRECLASS_CHECKLIST.md) | 环境、概念和代码预习检查 | | 实操代码 | [practice/](./practice/) | Supervisor 多 Agent、Agent 模式路由、分库分索引检索 | | 一键脚本 | [practice/preclass_run.sh](./practice/preclass_run.sh) | 自动执行 L08 环境检查和核心示例 | | 课堂笔记 | [materials/NOTES_TEMPLATE.md](./materials/NOTES_TEMPLATE.md) | 记录模式选型、路由策略、分库设计和多 Agent 流程 | | 课后小测 | [materials/MINI_QUIZ.md](./materials/MINI_QUIZ.md) | 检查 Agent 模式与企业知识库核心概念 | | 拓展练习 | [materials/EXTENSIONS.md](./materials/EXTENSIONS.md) | 翻译 Agent、分类器路由、权限过滤、评测集 | | 面试题库 | [materials/INTERVIEW_QA.md](./materials/INTERVIEW_QA.md) | Agent 模式、多 Agent、企业知识库问答系统设计题 | | 工程参考 | [resources/](./resources/) | 模式对比、多 Agent 范式、企业知识库和分库分索引设计 | | 示例数据 | [data/](./data/) | 预留给企业知识库、评测集和多 Agent 运行结果 | ## 推荐学习路径 1. 阅读 [materials/PRECLASS_CHECKLIST.md](./materials/PRECLASS_CHECKLIST.md)，确认 LangGraph、LangChain 和 `.env` 环境可用。 2. 阅读 [lecture/LECTURE_FULL.md](./lecture/LECTURE_FULL.md) 的 8.1-8.2，先建立 Agent 模式选型框架。 3. 阅读 [教辅资料：Agent 设计模式](../../teaching_support/AGENT_DESIGN_PATTERNS.md)，横向理解 ReAct、Plan-and-Execute、Reflection 和 Multi-Agent。 4. 运行 `practice/27_agent_mode_router.py`，观察同一个问答系统如何在 direct、RAG、ReAct 之间选择。 5. 阅读讲义 8.3-8.4，理解 Supervisor、Sequential、Peer 三类多 Agent 协作模式。 6. 运行 `practice/26_supervisor_research_team.py`，观察 LangGraph 如何管理多角色状态流转。 7. 阅读 [resources/ENTERPRISE_KB_AGENT_DESIGN.md](./resources/ENTERPRISE_KB_AGENT_DESIGN.md)，把 RAG/ReAct 选型放到企业知识库场景里理解。 8. 运行 `practice/28_multi_index_retrieva"
    },
    {
      "id": "L09_mcp_tooling",
      "code": "L09",
      "title": "L09 MCP 协议与工具生态：标准化的 Agent 工具接入",
      "intro": "本章学习 MCP（Model Context Protocol）：它把 Agent 与外部工具、数据源、提示模板之间的接入方式标准化。可以把 MCP 理解成 Agent 工具生态里的“USB-C”：工具方实现 MCP Server，Agent/Host 实现 MCP Client，双方通过统一协议发现能力、读取资源、调用工具和处理上下文。",
      "topics": [
        "MCP",
        "Tools",
        "Resources",
        "Prompt",
        "Sampling",
        "安全审计"
      ],
      "goals": [
        "理解 MCP 解决的核心问题：碎片化集成、上下文孤岛、协议不统一。",
        "掌握 MCP 架构：Host、MCP Client、MCP Server、Transport。",
        "理解 MCP 四类原语：Tools、Resources、Prompts、Sampling。",
        "用 Python MCP SDK 开发一个笔记管理 MCP Server。",
        "用 stdio MCP Client 发现工具、调用工具、读取资源和获取 Prompt。",
        "理解如何把 MCP 工具包装进 LangChain/LangGraph Agent。",
        "能说明 MCP 与 Function Calling 的区别和协作关系。",
        "掌握 MCP 安全、排障、大规模接入和面试高频问题。"
      ],
      "deliverables": [
        "一个可运行的笔记 MCP Server。",
        "一次 stdio Client 调用日志。",
        "一张 MCP 四类原语对比表。",
        "一份 MCP 与 Function Calling 的选型说明。",
        "一份 MCP Server 安全接入检查清单。",
        "一份排障记录：如果模型看不到工具，应按什么顺序排查。"
      ],
      "docs": [
        {
          "key": "readme",
          "label": "章节入口",
          "path": "lessons/L09_mcp_tooling/README.md",
          "contentPath": "data/docs/L09_mcp_tooling/readme.md",
          "excerpt": "# L09 MCP 协议与工具生态：标准化的 Agent 工具接入 本章学习 MCP（Model Context Protocol）：它把 Agent 与外部工具、数据源、提示模板之间的接入方式标准化。可以把 MCP 理解成 Agent 工具生态里的“USB-C”：工具方实现 MCP Server，Agent/Host 实现 MCP Client，双方通过统一协议发现能力、读取资源、调用工具和处理上下文。 ## 本章学习目标 - 理解 MCP 解决的核心问题：碎片化集成、上下文孤岛、协议不统一。 - 掌握 MCP 架构：Host、MCP Client、MCP Server、Transport。 - 理解 MCP 四类原语：Tools、Resources、Prompts、Sampling。 - 用 Python MCP SDK 开发一个笔记管理 MCP Server。 - 用 stdio MCP Client 发现工具、调用工具、"
        },
        {
          "key": "lecture",
          "label": "完整讲义",
          "path": "lessons/L09_mcp_tooling/lecture/LECTURE_FULL.md",
          "contentPath": "data/docs/L09_mcp_tooling/lecture.md",
          "excerpt": "# 第9讲 MCP 协议与工具生态：标准化的 Agent 工具接入 ## 9.1 什么是 MCP MCP 是 Model Context Protocol，中文可以叫模型上下文协议。 它要解决的问题，可以先用一个生活类比理解：没有统一接口时，不同品牌的电子设备需要不同充电线；有了 USB-C 后，一根线可以连接很多设备。Agent 开发里也有类似问题： - 不同模型有不同的工具调用格式。 - 不同数据源有不同接入方式。 - 每接一个新工具，都要写一套适配代码。 - 工具、资源、提示模板和上下文管理缺少统一协议。 MCP 就是 Agent 工具生态里的“USB-C”。工具方实现 MCP Server，Agent 应用实现 MCP Client，双方通过统一协议完成能力发现、工具调用、资源读取、提示模板获取和必要的模型请求。 老师材料里的核心比喻很准确：MCP 不是某一个工具，而是一套标准化接入方式。 ## 9.2 MCP 解决什么"
        },
        {
          "key": "summary",
          "label": "章节总结",
          "path": "lessons/L09_mcp_tooling/lecture/CHAPTER_SUMMARY.md",
          "contentPath": "data/docs/L09_mcp_tooling/summary.md",
          "excerpt": "# L09 章节总结 ## 一句话总结 MCP 是 Agent 工具生态的标准化接入协议：它让 Host/Client 用统一方式连接 MCP Server，发现 Tools、读取 Resources、复用 Prompts，并在受控条件下处理 Sampling。 ## 架构速查 ```text Host / Agent App -> MCP Client A -> MCP Server A -> MCP Client B -> MCP Server B -> MCP Client C -> MCP Server C ``` | 角色 | 作用 | | --- | --- | | Host | LLM 应用本体，管理多个 MCP Client | | Client | 与单个 Server 建立连接，做握手、能力协商和消息路由 | | Server | 暴露工具、资源、提示模板等能力 | | Transport | stdio 或"
        },
        {
          "key": "preclass",
          "label": "课前准备",
          "path": "lessons/L09_mcp_tooling/materials/PRECLASS_CHECKLIST.md",
          "contentPath": "data/docs/L09_mcp_tooling/preclass.md",
          "excerpt": "# L09 课前准备清单 ## 1. 环境检查 从课程根目录激活环境： ```bash source <course-root>/scripts/activate_course.sh ``` 检查基础环境： ```bash python scripts/check_env.py python scripts/smoke_openai.py python -c \"from mcp.server.fastmcp import FastMCP; print('mcp ok')\" ``` 进入第 9 章目录： ```bash cd <course-root>/lessons/L09_mcp_tooling ``` 运行一键脚本： ```bash bash practice/preclass_run.sh ``` 确认最后看到： ```text [OK] L09 preclass run completed. ``` ## 2. 概念预习"
        },
        {
          "key": "quiz",
          "label": "课后小测",
          "path": "lessons/L09_mcp_tooling/materials/MINI_QUIZ.md",
          "contentPath": "data/docs/L09_mcp_tooling/quiz.md",
          "excerpt": "# L09 课后小测 ## 题目 1. MCP 主要解决什么问题？ 2. Host、MCP Client、MCP Server 分别是什么？ 3. stdio transport 的基本通信流程是什么？ 4. MCP 的四类原语分别是什么？ 5. Tools 和 Resources 的关键区别是什么？ 6. Sampling 为什么需要 Client 审核？ 7. MCP 和 Function Calling 的本质区别是什么？ 8. 模型看不到 MCP 工具时，列出 5 个可能原因。 9. 为什么 MCP Server 的 stdout 不能随便打印日志？ 10. 大规模 Agent 集群接入 MCP 可能遇到哪些瓶颈？ ## 参考答案 1. MCP 解决 LLM 应用与外部工具、数据源、提示模板之间接入碎片化的问题，用统一协议做能力发现、上下文读取和工具调用。 2. Host 是 LLM 应用本体；Client 是 Host"
        },
        {
          "key": "extensions",
          "label": "拓展作业",
          "path": "lessons/L09_mcp_tooling/materials/EXTENSIONS.md",
          "contentPath": "data/docs/L09_mcp_tooling/extensions.md",
          "excerpt": "# L09 拓展练习 ## 练习 1：完善笔记 Server 的参数校验 修改 `practice/29_mcp_note_server.py` 和 `practice/mcp_common.py`： - 限制标题最长 80 个字符。 - 限制正文最长 2000 个字符。 - 限制标签最多 5 个。 - 对不存在的 `note_id` 返回清晰错误。 ## 练习 2：增加按标签筛选工具 新增工具： ```python @mcp.tool() def search_notes_by_tag(tag: str) -> str: ... ``` 要求： - 标签匹配大小写不敏感。 - 没有结果时明确返回“未找到”。 - 在 `30_mcp_stdio_client.py` 中调用一次。 ## 练习 3：把笔记存储换成 SQLite 把 `data/notes.json` 替换为 SQLite： - 表字段：`id, title, co"
        },
        {
          "key": "interview",
          "label": "面试题",
          "path": "lessons/L09_mcp_tooling/materials/INTERVIEW_QA.md",
          "contentPath": "data/docs/L09_mcp_tooling/interview.md",
          "excerpt": "# L09 面试题库：MCP 协议与工具生态 说明：本题库基于老师提供的 MCP 讲义和 15 道 MCP 面试题整理，并补充了课程代码中的实战回答角度。补充内容用于帮助面试表达更完整，不替代原讲义观点。 ## 一、基础级：概念理解 ### 1. 什么是 MCP？它解决的核心问题是什么？ MCP 是 Model Context Protocol，用于标准化 LLM 应用与外部工具、数据源和上下文能力之间的连接方式。 它解决三个核心问题： - 碎片化集成：每个应用接每个工具都写适配，会形成 M x N 问题；MCP 希望降为 M + N。 - 上下文孤岛：文件、数据库、API、知识库缺少统一上下文供给方式。 - 协议不统一：Function Calling、插件、API 直调各自为政，MCP 提供统一通信和生命周期管理。 类比：MCP 之于 AI 应用，类似 USB-C 之于外设。 ### 2. MCP 的核心架构包含哪些角色？ "
        },
        {
          "key": "resource:MCP_ARCHITECTURE_PATTERNS",
          "label": "资源：MCP_ARCHITECTURE_PATTERNS",
          "path": "lessons/L09_mcp_tooling/resources/MCP_ARCHITECTURE_PATTERNS.md",
          "contentPath": "data/docs/L09_mcp_tooling/resource_MCP_ARCHITECTURE_PATTERNS.md",
          "excerpt": "# MCP 架构模式 ## 1. 本地 stdio 模式 ```text Host -> spawn subprocess -> MCP Server over stdio ``` 适合： - 本地文件系统。 - 本地 SQLite。 - IDE 插件。 - 个人工具。 优点： - 开发简单。 - 权限容易限制在本地进程。 - 适合快速调试。 风险： - stdout 日志污染协议。 - 进程频繁启动有开销。 - 不适合大规模远程共享。 ## 2. 远程 Streamable HTTP 模式 ```text Host/Client -> HTTPS -> Remote MCP Server ``` 适合： - 企业内部共享工具。 - 多用户服务。 - 需要负载均衡和独立部署的能力。 关键要求： - HTTPS。"
        },
        {
          "key": "resource:MCP_PRIMITIVES",
          "label": "资源：MCP_PRIMITIVES",
          "path": "lessons/L09_mcp_tooling/resources/MCP_PRIMITIVES.md",
          "contentPath": "data/docs/L09_mcp_tooling/resource_MCP_PRIMITIVES.md",
          "excerpt": "# MCP 原语速查 ## 1. Tools Tools 是 Server 暴露给模型或 Agent 主动调用的能力。 适合： - 查询外部系统。 - 写入数据。 - 创建工单。 - 调用 API。 - 执行计算。 设计要点： - 工具名要短、稳定、可区分。 - description 要清楚说明适用场景和限制。 - 参数 schema 要严格。 - 有副作用工具要考虑确认、幂等和补偿。 本章例子： ```python @mcp.tool() def create_note(title: str, content: str, tags: str = \"\") -> str: ... ``` ## 2. Resources Resources 是 Server 暴露的只读上下文，由 Host/Client 决定是否"
        },
        {
          "key": "resource:MCP_SECURITY_AND_TROUBLESHOOTING",
          "label": "资源：MCP_SECURITY_AND_TROUBLESHOOTING",
          "path": "lessons/L09_mcp_tooling/resources/MCP_SECURITY_AND_TROUBLESHOOTING.md",
          "contentPath": "data/docs/L09_mcp_tooling/resource_MCP_SECURITY_AND_TROUBLESHOOTING.md",
          "excerpt": "# MCP 安全与排障清单 ## 1. 安全原则 MCP 安全模型可以压缩成三句话： - 最小权限。 - 用户知情。 - 全程可审计。 ## 2. 接入前安全检查 | 检查项 | 问题 | | --- | --- | | Server 来源 | 是否来自可信仓库或内部团队？ | | Tool 描述 | 是否包含 prompt injection 或隐藏指令？ | | Roots | 是否只暴露必要目录？ | | Transport | 远程 Server 是否使用 HTTPS 和鉴权？ | | Sampling | 是否默认关闭或受策略控制？ | | 副作用工具 | 是否需要确认、幂等或补偿？ | | 审计日志 | 是否记录工具、参数、用户、结果和错误？ | ## 3. 常见攻击与防御 | 攻击 | 描述 | "
        },
        {
          "key": "resource:MCP_VS_FUNCTION_CALLING",
          "label": "资源：MCP_VS_FUNCTION_CALLING",
          "path": "lessons/L09_mcp_tooling/resources/MCP_VS_FUNCTION_CALLING.md",
          "contentPath": "data/docs/L09_mcp_tooling/resource_MCP_VS_FUNCTION_CALLING.md",
          "excerpt": "# MCP 与 Function Calling 对比 ## 1. 一句话区别 ```text Function Calling 关注模型如何调用函数。 MCP 关注外部能力如何被标准化接入、发现、调用和治理。 ``` Function Calling 是模型能力；MCP 是应用与工具之间的协议。 ## 2. 调用链路 Function Calling： ```text 应用注册函数 schema -> 模型选择函数并生成参数 -> 应用执行函数 -> 工具结果回传模型 ``` MCP： ```text Host/Client 连接 Server -> initialize 能力协商 -> list_tools/list_resources/list_prompts -> call_tool/read_reso"
        }
      ],
      "practiceFiles": [
        {
          "name": "29_mcp_note_server.py",
          "path": "lessons/L09_mcp_tooling/practice/29_mcp_note_server.py",
          "size": "3.2 KB"
        },
        {
          "name": "30_mcp_stdio_client.py",
          "path": "lessons/L09_mcp_tooling/practice/30_mcp_stdio_client.py",
          "size": "4.2 KB"
        },
        {
          "name": "31_langchain_mcp_bridge.py",
          "path": "lessons/L09_mcp_tooling/practice/31_langchain_mcp_bridge.py",
          "size": "4.8 KB"
        },
        {
          "name": "32_mcp_safety_checklist.py",
          "path": "lessons/L09_mcp_tooling/practice/32_mcp_safety_checklist.py",
          "size": "4.5 KB"
        },
        {
          "name": "33_mcp_sampling_flow.py",
          "path": "lessons/L09_mcp_tooling/practice/33_mcp_sampling_flow.py",
          "size": "3.0 KB"
        },
        {
          "name": "mcp_common.py",
          "path": "lessons/L09_mcp_tooling/practice/mcp_common.py",
          "size": "6.4 KB"
        },
        {
          "name": "preclass_run.sh",
          "path": "lessons/L09_mcp_tooling/practice/preclass_run.sh",
          "size": "681 B"
        }
      ],
      "resourceFiles": [
        {
          "name": "MCP_ARCHITECTURE_PATTERNS.md",
          "path": "lessons/L09_mcp_tooling/resources/MCP_ARCHITECTURE_PATTERNS.md",
          "size": "2.1 KB"
        },
        {
          "name": "MCP_PRIMITIVES.md",
          "path": "lessons/L09_mcp_tooling/resources/MCP_PRIMITIVES.md",
          "size": "2.2 KB"
        },
        {
          "name": "MCP_SECURITY_AND_TROUBLESHOOTING.md",
          "path": "lessons/L09_mcp_tooling/resources/MCP_SECURITY_AND_TROUBLESHOOTING.md",
          "size": "2.4 KB"
        },
        {
          "name": "MCP_VS_FUNCTION_CALLING.md",
          "path": "lessons/L09_mcp_tooling/resources/MCP_VS_FUNCTION_CALLING.md",
          "size": "2.1 KB"
        }
      ],
      "materialFiles": [
        {
          "name": "EXTENSIONS.md",
          "path": "lessons/L09_mcp_tooling/materials/EXTENSIONS.md",
          "size": "2.1 KB"
        },
        {
          "name": "INTERVIEW_QA.md",
          "path": "lessons/L09_mcp_tooling/materials/INTERVIEW_QA.md",
          "size": "10.7 KB"
        },
        {
          "name": "MINI_QUIZ.md",
          "path": "lessons/L09_mcp_tooling/materials/MINI_QUIZ.md",
          "size": "1.9 KB"
        },
        {
          "name": "NOTES_TEMPLATE.md",
          "path": "lessons/L09_mcp_tooling/materials/NOTES_TEMPLATE.md",
          "size": "1.3 KB"
        },
        {
          "name": "PRECLASS_CHECKLIST.md",
          "path": "lessons/L09_mcp_tooling/materials/PRECLASS_CHECKLIST.md",
          "size": "2.4 KB"
        }
      ],
      "dataFiles": [
        {
          "name": "README.md",
          "path": "lessons/L09_mcp_tooling/data/README.md",
          "size": "404 B"
        },
        {
          "name": "notes.json",
          "path": "lessons/L09_mcp_tooling/data/notes.json",
          "size": "1.1 KB"
        }
      ],
      "preclassCommand": "cd lessons/L09_mcp_tooling && bash practice/preclass_run.sh",
      "fileCount": 21,
      "searchText": "# L09 MCP 协议与工具生态：标准化的 Agent 工具接入 本章学习 MCP（Model Context Protocol）：它把 Agent 与外部工具、数据源、提示模板之间的接入方式标准化。可以把 MCP 理解成 Agent 工具生态里的“USB-C”：工具方实现 MCP Server，Agent/Host 实现 MCP Client，双方通过统一协议发现能力、读取资源、调用工具和处理上下文。 ## 本章学习目标 - 理解 MCP 解决的核心问题：碎片化集成、上下文孤岛、协议不统一。 - 掌握 MCP 架构：Host、MCP Client、MCP Server、Transport。 - 理解 MCP 四类原语：Tools、Resources、Prompts、Sampling。 - 用 Python MCP SDK 开发一个笔记管理 MCP Server。 - 用 stdio MCP Client 发现工具、调用工具、读取资源和获取 Prompt。 - 理解如何把 MCP 工具包装进 LangChain/LangGraph Agent。 - 能说明 MCP 与 Function Calling 的区别和协作关系。 - 掌握 MCP 安全、排障、大规模接入和面试高频问题。 ## 文件分区 | 分类 | 路径 | 用途 | | --- | --- | --- | | 讲义 | [lecture/LECTURE_FULL.md](./lecture/LECTURE_FULL.md) | 第 9 讲完整讲义：MCP 架构、实操、生态和选型 | | 总结 | [lecture/CHAPTER_SUMMARY.md](./lecture/CHAPTER_SUMMARY.md) | 原语速查、代码地图和排障清单 | | 课前准备 | [materials/PRECLASS_CHECKLIST.md](./materials/PRECLASS_CHECKLIST.md) | 环境、概念和代码预习检查 | | 实操代码 | [practice/](./practice/) | MCP Server、stdio Client、LangChain 桥接、安全检查、Sampling 流程 | | 一键脚本 | [practice/preclass_run.sh](./practice/preclass_run.sh) | 自动执行 L09 环境检查和核心示例 | | 课堂笔记 | [materials/NOTES_TEMPLATE.md](./materials/NOTES_TEMPLATE.md) | 记录协议角色、原语、调用链路和安全策略 | | 课后小测 | [materials/MINI_QUIZ.md](./materials/MINI_QUIZ.md) | 检查 MCP 核心概念 | | 拓展练习 | [materials/EXTENSIONS.md](./materials/EXTENSIONS.md) | update/delete、Sampling callback、远程 Server、审计日志 | | 面试题库 | [materials/INTERVIEW_QA.md](./materials/INTERVIEW_QA.md) | MCP 分层面试题、系统设计题和排障题 | | 工程参考 | [resources/](./resources/) | 原语、架构、安全排障、MCP 与 Function Calling 对比 | | 运行数据 | [data/](./data/) | 笔记 MCP Server 的 JSON 示例数据 | ## 推荐学习路径 1. 阅读 [materials/PRECLASS_CHECKLIST.md](./materials/PRECLASS_CHECKLIST.md)，确认 `mcp` SDK 已安装在 `agent_course` 环境。 2. 阅读 [lecture/LECTURE_FULL.md](./lecture/LECTURE_FULL.md) 的 9.1-9.2，理解 MCP 为什么像 Agent 工具接入的 USB-C。 3. 运行 `practice/30_mcp_stdio_client.py`，观察 Client 如何启动 Server、发现工具、调用工具、读取资源和获取 Prompt。 4. 阅读 `practice/29_mcp_note_server.py`，理解 `@mcp.tool()`、`@mcp.resource()`、`@mcp.prompt()` 的区别。 5. 运行 `practice/31_langchain_mcp_bridge.py`，理解 LangChain Tool 如何转发到 MCP Client。 6. 运行 `practice/32_mcp_safety_checklist.py` 和 `practice/33_mcp_sampling_flow.py`，理解安全治理和 Sampling 审核。 7. 阅读 [resources/MCP_VS_FUNCTION_CALLING.md](./resources/MCP_VS_"
    },
    {
      "id": "L10_skills",
      "code": "L10",
      "title": "L10 Skill 相关：让 Agent 能力模块化复用",
      "intro": "本章进入 Agent 能力工程化：Tool 只是原子动作，Skill 是围绕稳定用户意图组织起来的能力包。它把触发条件、执行步骤、上下文知识、工具集合、输出格式、安全边界和评测闭环沉淀成可复用模块。",
      "topics": [
        "Skill",
        "DDICE",
        "授权边界",
        "重试分层",
        "长尾延迟",
        "模型回滚"
      ],
      "goals": [
        "理解从 Chatbot 到 Agent 的关键跃迁：裸 LLM 只能“说话”，Agent 需要可复用 Skill 去“做事”。",
        "掌握 Tool、Skill、MCP 三层架构：Tool 是原子操作，Skill 是能力包，MCP 是连接标准。",
        "能区分 Function Calling、MCP、A2A 的定位：怎么调用、怎么连接、怎么协作。",
        "掌握 SKILL.md 结构：元信息层、指令层、执行层。",
        "用 DDICE 五步法设计 Skill：Define、Decompose、Instrument、Constrain、Evaluate。",
        "跑通天气查询、代码审查、办公助手渐进加载三个 Skill 示例。",
        "理解渐进披露：启动时只加载 metadata，触发后再加载完整指令和工具。",
        "能从边界、契约、执行、观测、安全和评测六个角度评价一个 Skill。"
      ],
      "deliverables": [
        "能用一张图或一段话解释 Tool、Skill、MCP 三层分工。",
        "完成一个包含 `SKILL.md`、触发条件、工具清单、执行步骤和输出约束的自定义 Skill。",
        "跑通天气查询、代码审查和办公助手三个 Skill 示例，并能说明每个示例的工程边界。",
        "给一个高风险 Skill 写出授权策略、确认策略、审计字段和误触发处置流程。",
        "给一个 Skill 发布变更写出灰度、指标、回滚和复盘方案。",
        "完成本章小测、拓展作业和面试题复盘。"
      ],
      "docs": [
        {
          "key": "readme",
          "label": "章节入口",
          "path": "lessons/L10_skills/README.md",
          "contentPath": "data/docs/L10_skills/readme.md",
          "excerpt": "# L10 Skill 相关：让 Agent 能力模块化复用 本章进入 Agent 能力工程化：Tool 只是原子动作，Skill 是围绕稳定用户意图组织起来的能力包。它把触发条件、执行步骤、上下文知识、工具集合、输出格式、安全边界和评测闭环沉淀成可复用模块。 ## 本章学习目标 - 理解从 Chatbot 到 Agent 的关键跃迁：裸 LLM 只能“说话”，Agent 需要可复用 Skill 去“做事”。 - 掌握 Tool、Skill、MCP 三层架构：Tool 是原子操作，Skill 是能力包，MCP 是连接标准。 - 能区分 Function Calling、MCP、A2A 的定位：怎么调用、怎么连接、怎么协作。 - 掌握 SKILL.md 结构：元信息层、指令层、执行层。 - 用 DDICE 五步法设计 Skill：Define、Decompose、Instrument、Constrain、Evaluate。 - 跑"
        },
        {
          "key": "lecture",
          "label": "完整讲义",
          "path": "lessons/L10_skills/lecture/LECTURE_FULL.md",
          "contentPath": "data/docs/L10_skills/lecture.md",
          "excerpt": "# 第10讲 Skill 相关：让 Agent 能力模块化复用 本章聚焦 Skill 的基础认知、设计方法、典型案例和工程化治理：从天气查询、代码审查、办公助手渐进加载，到重试分层、并行长尾延迟、自动授权、网页指令边界、误触发止损和模型升级回滚。 ## 10.1 从 Chatbot 到 Agent：Skill 是关键跃迁 一个裸 LLM 只能“说话”，但 Agent 需要“做事”。Skill 就是赋予 Agent 行动能力的标准化封装。 | 维度 | Chatbot，无 Skill | Agent，有 Skill | | --- | --- | --- | | 能力 | 仅文本生成 | 搜索、计算、调用 API、操作文件 | | 边界 | 受模型知识截止日期限制 | 可以访问实时数据和外部系统 | | 协作 | 单轮问答 | 多步规划和工具调用循环 | | 价值 | 辅助思考 | 替代一部分执行动作 | Skill 的重点不是“"
        },
        {
          "key": "summary",
          "label": "章节总结",
          "path": "lessons/L10_skills/lecture/CHAPTER_SUMMARY.md",
          "contentPath": "data/docs/L10_skills/summary.md",
          "excerpt": "# L10 章节总结 ## 一句话总结 Skill 是围绕稳定用户意图封装的能力包。Tool 回答“能做什么动作”，Skill 回答“能完成哪类任务”，Workflow 回答“这次目标如何组合能力”。 ## 核心分层 | 层级 | 作用 | 例子 | | --- | --- | --- | | Tool | 原子动作 | `get_weather(city)` | | Skill | 有触发条件、执行流程和上下文的能力包 | `weather-query` | | MCP | Skill/工具生态的连接标准 | MCP Server 暴露 Tools/Resources/Prompts | | Workflow | 面向具体目标的流程编排 | 会议总结 -> 抽取待办 -> 写入任务系统 | ## DDICE 五步法 1. Define：定义场景，谁用、何时用、替代什么人工动作。 2. Decompose：拆解任务，拆到稳定子步"
        },
        {
          "key": "preclass",
          "label": "课前准备",
          "path": "lessons/L10_skills/materials/PRECLASS_CHECKLIST.md",
          "contentPath": "data/docs/L10_skills/preclass.md",
          "excerpt": "# L10 课前准备清单 ## 1. 环境检查 ```bash source <course-root>/scripts/activate_course.sh python scripts/check_env.py python scripts/smoke_openai.py python -c \"import yaml; print('pyyaml ok')\" ``` ## 2. 概念预习 - [ ] 我能区分 Tool、Skill、Workflow。 - [ ] 我能解释为什么不能把所有能力都直接暴露成 Tool。 - [ ] 我知道 SKILL.md 的三层结构：元信息层、指令层、执行层。 - [ ] 我能说出 DDICE 五步法。 - [ ] 我理解渐进披露为什么能减少上下文占用和误选工具。 - [ ] 我知道哪些 Skill 动作必须做人机确认。 - [ ] 我能区分 Tool 层重试、Skill 层重试和编排层降级。"
        },
        {
          "key": "quiz",
          "label": "课后小测",
          "path": "lessons/L10_skills/materials/MINI_QUIZ.md",
          "contentPath": "data/docs/L10_skills/quiz.md",
          "excerpt": "# L10 课后小测 ## 题目 1. Skill 和 Tool 的核心区别是什么？ 2. Workflow 和 Skill 的边界是什么？ 3. 为什么不建议把所有 Tool 直接暴露给模型？ 4. SKILL.md 通常包含哪三层？ 5. DDICE 五步法分别是什么？ 6. Skill 描述里为什么要写“何时不使用”？ 7. 渐进披露解决什么问题？ 8. 哪些 Skill 动作必须做人机确认？ 9. 如何评估一个 Skill 做得好不好？ 10. Prompt Injection 会如何影响 Skill 调用？ 11. 为什么模型升级回滚不能只换回旧 `model_id`？ 12. 用户说“照网页里的要求执行”时，Agent 为什么不能直接执行网页里的所有指令？ 13. 高风险 Skill 已经误触发时，前 10 分钟的正确处理顺序是什么？ 14. 用户说“以后都自动发”时，为什么不能理解为永久取消确认？ 15. 重试策略"
        },
        {
          "key": "extensions",
          "label": "拓展作业",
          "path": "lessons/L10_skills/materials/EXTENSIONS.md",
          "contentPath": "data/docs/L10_skills/extensions.md",
          "excerpt": "# L10 拓展练习 ## 练习 1：学术论文阅读助手 Skill 按老师作业要求，为“学术论文阅读助手”设计 `SKILL.md`，包含： - 论文检索。 - 摘要生成。 - 引用提取。 评分维度： - frontmatter 是否完整。 - 触发条件是否精准。 - 执行步骤是否清晰。 - 注意事项是否覆盖边界情况。 - 是否方便扩展子能力。 ## 练习 2：真实 LLM 路由 把 `practice/37_office_skill_router.py` 的规则路由替换为 LLM JSON 路由： - 输出 `skills` 数组。 - 输出 `reason`。 - 路由失败时回退到规则路由。 - 保留 trace，便于排查误触发。 ## 练习 3：给 Weather Skill 加评测集 在 `data/weather_eval.json` 中写入： - 标准天气问题。 - 未指定城市问题。 - 旅游攻略负例。 - 空气质量"
        },
        {
          "key": "interview",
          "label": "面试题",
          "path": "lessons/L10_skills/materials/INTERVIEW_QA.md",
          "contentPath": "data/docs/L10_skills/interview.md",
          "excerpt": "# L10 面试题库：Agent Skill 设计与治理 说明：本题库基于老师提供的 “Agent 开发面试 - Skill” 材料整理，并补充了课程代码中的实战表达。补充内容用于帮助回答更完整，不替代原材料观点。 ## 一、基础认知题 ### 1. 什么是 Agent 中的 Skill？它和 Tool、Workflow 有什么区别？ Skill 是面向某类稳定用户意图的能力封装。它通常不只是一次工具调用，而是围绕任务目标组织的一组输入约束、执行流程、错误处理、结果结构和使用规则。 - Tool 回答“我能做什么动作”，例如读文件、查天气、写数据库。 - Skill 回答“我能完成哪类任务”，例如天气出行建议、代码审查、会议纪要总结。 - Workflow 回答“为了完成这次目标，如何组合能力”，可能编排多个 Skill 和 Tool。 ### 2. 为什么 Agent 系统需要 Skill，而不是把所有能力都直接暴露成 Too"
        },
        {
          "key": "resource:AUTO_SEND_AUTHORIZATION_POLICY",
          "label": "资源：AUTO_SEND_AUTHORIZATION_POLICY",
          "path": "lessons/L10_skills/resources/AUTO_SEND_AUTHORIZATION_POLICY.md",
          "contentPath": "data/docs/L10_skills/resource_AUTO_SEND_AUTHORIZATION_POLICY.md",
          "excerpt": "# “以后都自动发”：授权边界与落地 用户说“以后都自动发”时，不是在取消确认，而是在授予一个受限的自动执行权限。 正确处理方式是把这句口头授权翻译成： ```text 窄范围 + 有时效 + 可撤销 + 可审计 ``` 的策略对象，而不是从此无脑执行。 ## 1. 先判断：这句话能不能接 不是所有“自动发”都能自动化。先过三道闸。 | 维度 | 可以自动化 | 需降级或拒绝 | | --- | --- | --- | | 影响范围 | 私人、小范围，例如自己日历、个人任务、固定小群 | 群发、对外、跨部门广播 | | 可逆性 | 可撤回、可删除、可修改 | 不可逆，例如打款、合同、删除数据 | | 合规风险 | 内部常规操作 | 财务、权限变更、审批流 | | 用户身份 | 本人操作本人资源 | 代他人操作、"
        },
        {
          "key": "resource:HIGH_RISK_SKILL_MISFIRE_RESPONSE",
          "label": "资源：HIGH_RISK_SKILL_MISFIRE_RESPONSE",
          "path": "lessons/L10_skills/resources/HIGH_RISK_SKILL_MISFIRE_RESPONSE.md",
          "contentPath": "data/docs/L10_skills/resource_HIGH_RISK_SKILL_MISFIRE_RESPONSE.md",
          "excerpt": "# 高风险 Skill 误触发：事后损失控制 高风险 Skill 误触发已经发生时，第一优先级不是追责，也不是马上改代码，而是： ```text 止损 -> 评估影响 -> 分级补救 -> 透明告知 -> 结构加固 ``` 误触发事故的损失大小，很大程度取决于前 10 分钟的处置质量。 ## 1. 黄金 5 分钟：先止血 误触发发生后，第一目标是防止继续扩散。 ### 1.1 立刻切断同类执行 - 熔断该 Skill：对当前用户、会话、租户或全局停用该能力。 - 冻结相关自动化规则：如果是授权类任务，暂停同 scope 的规则。 - 检查队列和排期：取消尚未执行的后续批次。 注意：先停，再查。不要在搞清楚根因之前让系统继续自动执行。 ### 1.2 锁定影响面 立刻拉取调用日志： - 时间。 - Skill 名"
        },
        {
          "key": "resource:MODEL_UPGRADE_ROLLBACK",
          "label": "资源：MODEL_UPGRADE_ROLLBACK",
          "path": "lessons/L10_skills/resources/MODEL_UPGRADE_ROLLBACK.md",
          "contentPath": "data/docs/L10_skills/resource_MODEL_UPGRADE_ROLLBACK.md",
          "excerpt": "# 模型升级回滚：不只是换回旧版本 模型升级回滚和传统服务回滚最大的差别是：问题往往不是“崩了”，而是“不一样了”。不崩的退化最难发现，也最难定义回滚标准。 回滚设计的核心，是让“发现 -> 决策 -> 执行”三步都有可操作依据。 ## 1. 回滚的三个前置条件 没有下面三件事，回滚只能靠感觉。 ### 1.1 版本即快照，而不是单一参数 一个可回滚的“模型版本”应包含： - 模型标识：model id 和权重版本。 - Prompt 模板。 - 工具描述。 - Skill 列表和 Skill 描述。 - 关键参数：temperature、top_p、max_tokens、超时。 - 路由或分类器 threshold。 - 后处理规则：过滤、校验、格式化。 只换模型不换配套，属于伪回滚。线上很多“回滚无效”，根"
        },
        {
          "key": "resource:PARALLEL_TAIL_LATENCY_OPTIMIZATION",
          "label": "资源：PARALLEL_TAIL_LATENCY_OPTIMIZATION",
          "path": "lessons/L10_skills/resources/PARALLEL_TAIL_LATENCY_OPTIMIZATION.md",
          "contentPath": "data/docs/L10_skills/resource_PARALLEL_TAIL_LATENCY_OPTIMIZATION.md",
          "excerpt": "# 并行编排中的长尾延迟优化 多个子步骤都能并行时，整体耗时往往不是平均值决定的，而是由最慢的那个分支决定的。 ```text parallel_latency = max(branch_latency) ``` 这就是 tail latency。一个分支拖到 P99，整个 Skill 的 P99 也会被拖上去。 优化目标有两个： 1. 让慢分支变快。 2. 让慢分支不阻塞整体交付。 ## 1. 先诊断：慢的根因决定策略 没有 trace 数据就谈优化，基本是在猜。 | 根因 | 识别特征 | 适用优化 | | --- | --- | --- | | IO 等待 | CPU 空闲，网络或磁盘活跃 | 流式处理、分片、预取 | | 数据量大 | 耗时随输入规模线性增长 | 分页并发、MapReduce | | 服"
        },
        {
          "key": "resource:PROGRESSIVE_DISCLOSURE",
          "label": "资源：PROGRESSIVE_DISCLOSURE",
          "path": "lessons/L10_skills/resources/PROGRESSIVE_DISCLOSURE.md",
          "contentPath": "data/docs/L10_skills/resource_PROGRESSIVE_DISCLOSURE.md",
          "excerpt": "# Skill 渐进披露 ## 1. 为什么需要渐进披露 如果启动时把所有 Skill 的完整说明和所有工具 schema 都塞进上下文，会有三个问题： - 上下文被挤占。 - 模型面对过大的 action space，误选工具概率上升。 - 高风险工具过早暴露，安全边界变差。 渐进披露的核心是： ```text 启动时只加载 metadata 触发后加载 SKILL.md 执行时按需加载脚本、工具和参考资料 ``` ## 2. 本章办公助手示例 ```text office-router -> schedule-manager -> email-notifier -> doc-generator ``` 第一步只加载 `office-router` 的路由规则。命中后，再加载对应子 Skill 的完整指令。 "
        },
        {
          "key": "resource:RETRY_STRATEGY_LAYERING",
          "label": "资源：RETRY_STRATEGY_LAYERING",
          "path": "lessons/L10_skills/resources/RETRY_STRATEGY_LAYERING.md",
          "contentPath": "data/docs/L10_skills/resource_RETRY_STRATEGY_LAYERING.md",
          "excerpt": "# 重试策略：Tool 层、Skill 层与编排层的边界 重试策略不是“哪里失败就哪里多试几次”。正确答案是：Tool 层和 Skill 层都需要重试，但职责完全不同；编排层原则上不重试，只做补偿、降级和用户告知。 如果三层都随手加 3 次重试，很容易写出： ```text 3 x 3 x 3 = 27 次调用 ``` 这种代码看起来“更稳定”，实际会把下游打挂。 ## 1. 分层原则：按失败语义划分 | 层级 | 重试什么 | 重试依据 | 典型次数 | | --- | --- | --- | --- | | Tool 层 | 瞬时性、物理性故障 | 网络、协议、传输层信号 | 2-3 次，毫秒级退避 | | Skill 层 | 业务语义可恢复错误 | 业务错误码 + 上下文判断 | 0-1 次，秒级退避 |"
        },
        {
          "key": "resource:SKILL_DESIGN_DDICE",
          "label": "资源：SKILL_DESIGN_DDICE",
          "path": "lessons/L10_skills/resources/SKILL_DESIGN_DDICE.md",
          "contentPath": "data/docs/L10_skills/resource_SKILL_DESIGN_DDICE.md",
          "excerpt": "# Skill 设计方法：DDICE DDICE 是第 10 章的 Skill 设计五步法。 ## 1. Define：定义场景 回答： - 谁使用？ - 什么时候使用？ - 替代什么人工动作？ - 错误成本有多高？ - 是否高频或高价值？ 产物： ```text 用户: 触发场景: 不触发场景: 业务价值: 风险等级: ``` ## 2. Decompose：任务拆解 把任务拆成稳定步骤。 示例：天气查询 ```text 解析城市 -> 查询天气 -> 查询空气质量 -> 生成出行建议 ``` 示例：会议待办 ```text 读取会议内容 -> 总结结论 -> 抽取行动项 -> preview -> 写入任务系统 ``` ## 3. Instrument：工具化 判断每一步由什么承载： | 步骤类型 | 推荐"
        },
        {
          "key": "resource:SKILL_SAFETY_AND_EVALUATION",
          "label": "资源：SKILL_SAFETY_AND_EVALUATION",
          "path": "lessons/L10_skills/resources/SKILL_SAFETY_AND_EVALUATION.md",
          "contentPath": "data/docs/L10_skills/resource_SKILL_SAFETY_AND_EVALUATION.md",
          "excerpt": "# Skill 安全与评测 ## 1. 高风险动作 必须谨慎处理： - 对外发送：邮件、消息、通知。 - 写入修改：创建任务、更新文档、批量改记录。 - 删除不可逆。 - 高成本批量 API。 - 从非结构化内容推断后直接执行。 ## 2. 四层防护 | 层级 | 防护 | | --- | --- | | 触发层 | 描述清晰、负例、提高高风险阈值 | | 参数层 | schema 校验、格式校验、对象存在性校验 | | 策略层 | 权限、配额、白名单、preview、确认 | | 执行层 | 幂等键、审计日志、可撤销、沙箱 | ## 3. 重试分层 重试策略要按失败语义分层： - Tool 层：网络超时、HTTP 502/503/504、429、token 过期等物理抖动。 - Skill 层：异步任务未就绪"
        },
        {
          "key": "resource:TOOL_SKILL_MCP_LAYERS",
          "label": "资源：TOOL_SKILL_MCP_LAYERS",
          "path": "lessons/L10_skills/resources/TOOL_SKILL_MCP_LAYERS.md",
          "contentPath": "data/docs/L10_skills/resource_TOOL_SKILL_MCP_LAYERS.md",
          "excerpt": "# Tool、Skill、MCP 分层 ## 1. 三层定位 | 层级 | 回答的问题 | 典型形态 | | --- | --- | --- | | Tool | 我能做什么动作？ | 函数、API、命令 | | Skill | 我能完成哪类任务？ | SKILL.md + 工具包 + 流程 | | MCP | 外部能力如何被连接和发现？ | MCP Client/Server | ## 2. 关系图 ```text 用户意图 -> Skill 路由 -> 加载 SKILL.md -> 选择执行流程 -> 调用一个或多个 Tool -> 本地函数 / API / MCP Server ``` ## 3. 和 Workflow 的区别 Workflow 面向一次具体目标，可能把多个 Skill 和 Tool 编排"
        },
        {
          "key": "resource:WEB_INSTRUCTION_AUTHORIZATION",
          "label": "资源：WEB_INSTRUCTION_AUTHORIZATION",
          "path": "lessons/L10_skills/resources/WEB_INSTRUCTION_AUTHORIZATION.md",
          "contentPath": "data/docs/L10_skills/resource_WEB_INSTRUCTION_AUTHORIZATION.md",
          "excerpt": "# “照网页里的要求执行”：外部内容授权边界 这个场景的本质是：用户把一部分“任务说明”交给网页，但不等于把 Agent 的指令权交给网页。 处理关键不是一律禁止，也不是照单全收，而是明确区分： - 什么可以由网页内容决定。 - 什么必须由用户确认。 - 什么即使用户说“照网页执行”也不能直接执行。 ## 1. 先拆解用户真实意图 “照网页里的要求执行”通常包含四种不同意图，授权边界完全不同。 | 用户真实意图 | 示例 | 授权程度 | | --- | --- | --- | | 按网页内容生成或总结 | “按这个教程帮我写个类似的” | 内容参考，不涉及动作 | | 按网页步骤操作自己的资源 | “照这个文档创建表格” | 私域资源，中等风险 | | 按网页表单或要求填写提交 | “按这个申请表要求填” |"
        }
      ],
      "practiceFiles": [
        {
          "name": "34_skill_loader.py",
          "path": "lessons/L10_skills/practice/34_skill_loader.py",
          "size": "1.4 KB"
        },
        {
          "name": "35_weather_skill_agent.py",
          "path": "lessons/L10_skills/practice/35_weather_skill_agent.py",
          "size": "1.6 KB"
        },
        {
          "name": "36_code_review_skill.py",
          "path": "lessons/L10_skills/practice/36_code_review_skill.py",
          "size": "1.3 KB"
        },
        {
          "name": "37_office_skill_router.py",
          "path": "lessons/L10_skills/practice/37_office_skill_router.py",
          "size": "3.0 KB"
        },
        {
          "name": "38_model_rollback_playbook.py",
          "path": "lessons/L10_skills/practice/38_model_rollback_playbook.py",
          "size": "6.2 KB"
        },
        {
          "name": "39_web_instruction_boundary.py",
          "path": "lessons/L10_skills/practice/39_web_instruction_boundary.py",
          "size": "11.5 KB"
        },
        {
          "name": "40_high_risk_skill_incident_response.py",
          "path": "lessons/L10_skills/practice/40_high_risk_skill_incident_response.py",
          "size": "10.8 KB"
        },
        {
          "name": "41_auto_send_authorization.py",
          "path": "lessons/L10_skills/practice/41_auto_send_authorization.py",
          "size": "11.3 KB"
        },
        {
          "name": "42_retry_strategy_layering.py",
          "path": "lessons/L10_skills/practice/42_retry_strategy_layering.py",
          "size": "9.0 KB"
        },
        {
          "name": "43_parallel_tail_latency.py",
          "path": "lessons/L10_skills/practice/43_parallel_tail_latency.py",
          "size": "13.6 KB"
        },
        {
          "name": "skill_common.py",
          "path": "lessons/L10_skills/practice/skill_common.py",
          "size": "10.2 KB"
        },
        {
          "name": "preclass_run.sh",
          "path": "lessons/L10_skills/practice/preclass_run.sh",
          "size": "1.0 KB"
        }
      ],
      "resourceFiles": [
        {
          "name": "AUTO_SEND_AUTHORIZATION_POLICY.md",
          "path": "lessons/L10_skills/resources/AUTO_SEND_AUTHORIZATION_POLICY.md",
          "size": "5.4 KB"
        },
        {
          "name": "HIGH_RISK_SKILL_MISFIRE_RESPONSE.md",
          "path": "lessons/L10_skills/resources/HIGH_RISK_SKILL_MISFIRE_RESPONSE.md",
          "size": "6.5 KB"
        },
        {
          "name": "MODEL_UPGRADE_ROLLBACK.md",
          "path": "lessons/L10_skills/resources/MODEL_UPGRADE_ROLLBACK.md",
          "size": "5.9 KB"
        },
        {
          "name": "PARALLEL_TAIL_LATENCY_OPTIMIZATION.md",
          "path": "lessons/L10_skills/resources/PARALLEL_TAIL_LATENCY_OPTIMIZATION.md",
          "size": "5.6 KB"
        },
        {
          "name": "PROGRESSIVE_DISCLOSURE.md",
          "path": "lessons/L10_skills/resources/PROGRESSIVE_DISCLOSURE.md",
          "size": "1.2 KB"
        },
        {
          "name": "RETRY_STRATEGY_LAYERING.md",
          "path": "lessons/L10_skills/resources/RETRY_STRATEGY_LAYERING.md",
          "size": "5.6 KB"
        },
        {
          "name": "SKILL_DESIGN_DDICE.md",
          "path": "lessons/L10_skills/resources/SKILL_DESIGN_DDICE.md",
          "size": "1.5 KB"
        },
        {
          "name": "SKILL_SAFETY_AND_EVALUATION.md",
          "path": "lessons/L10_skills/resources/SKILL_SAFETY_AND_EVALUATION.md",
          "size": "5.2 KB"
        },
        {
          "name": "TOOL_SKILL_MCP_LAYERS.md",
          "path": "lessons/L10_skills/resources/TOOL_SKILL_MCP_LAYERS.md",
          "size": "1.2 KB"
        },
        {
          "name": "WEB_INSTRUCTION_AUTHORIZATION.md",
          "path": "lessons/L10_skills/resources/WEB_INSTRUCTION_AUTHORIZATION.md",
          "size": "5.0 KB"
        }
      ],
      "materialFiles": [
        {
          "name": "EXTENSIONS.md",
          "path": "lessons/L10_skills/materials/EXTENSIONS.md",
          "size": "3.8 KB"
        },
        {
          "name": "INTERVIEW_QA.md",
          "path": "lessons/L10_skills/materials/INTERVIEW_QA.md",
          "size": "15.0 KB"
        },
        {
          "name": "MINI_QUIZ.md",
          "path": "lessons/L10_skills/materials/MINI_QUIZ.md",
          "size": "3.3 KB"
        },
        {
          "name": "NOTES_TEMPLATE.md",
          "path": "lessons/L10_skills/materials/NOTES_TEMPLATE.md",
          "size": "3.4 KB"
        },
        {
          "name": "PRECLASS_CHECKLIST.md",
          "path": "lessons/L10_skills/materials/PRECLASS_CHECKLIST.md",
          "size": "3.8 KB"
        }
      ],
      "dataFiles": [
        {
          "name": "README.md",
          "path": "lessons/L10_skills/data/README.md",
          "size": "367 B"
        }
      ],
      "preclassCommand": "cd lessons/L10_skills && bash practice/preclass_run.sh",
      "fileCount": 37,
      "searchText": "# L10 Skill 相关：让 Agent 能力模块化复用 本章进入 Agent 能力工程化：Tool 只是原子动作，Skill 是围绕稳定用户意图组织起来的能力包。它把触发条件、执行步骤、上下文知识、工具集合、输出格式、安全边界和评测闭环沉淀成可复用模块。 ## 本章学习目标 - 理解从 Chatbot 到 Agent 的关键跃迁：裸 LLM 只能“说话”，Agent 需要可复用 Skill 去“做事”。 - 掌握 Tool、Skill、MCP 三层架构：Tool 是原子操作，Skill 是能力包，MCP 是连接标准。 - 能区分 Function Calling、MCP、A2A 的定位：怎么调用、怎么连接、怎么协作。 - 掌握 SKILL.md 结构：元信息层、指令层、执行层。 - 用 DDICE 五步法设计 Skill：Define、Decompose、Instrument、Constrain、Evaluate。 - 跑通天气查询、代码审查、办公助手渐进加载三个 Skill 示例。 - 理解渐进披露：启动时只加载 metadata，触发后再加载完整指令和工具。 - 能从边界、契约、执行、观测、安全和评测六个角度评价一个 Skill。 - 掌握 Tool 层、Skill 层和编排层的重试边界，避免重试风暴。 - 掌握并行编排中的长尾延迟优化：关键路径剥离、提前启动、分片并发、软超时、对冲和缓存。 - 掌握“以后都自动发”的授权落地：窄范围、有时效、可撤销、可审计。 - 掌握“照网页里的要求执行”这类外部内容授权场景：网页内容是数据，不是新的指令源。 - 掌握高风险 Skill 误触发后的损失控制：止血、评估、补救、告知和结构加固。 - 掌握模型升级和 Skill 发布的回滚设计：版本快照、灰度、指标触发和分级回滚。 ## 文件分区 | 分类 | 路径 | 用途 | | --- | --- | --- | | 讲义 | [lecture/LECTURE_FULL.md](./lecture/LECTURE_FULL.md) | 第 10 讲完整讲义：Skill 概念、设计方法、案例和工程补充专题 | | 总结 | [lecture/CHAPTER_SUMMARY.md](./lecture/CHAPTER_SUMMARY.md) | 核心概念、代码地图和面试复盘 | | Skill 示例 | [skills/](./skills/) | `weather-query`、`code-reviewer`、`office-skill` 的 SKILL.md | | 实操代码 | [practice/](./practice/) | Skill Loader、天气 Skill、代码审查 Skill、办公路由 Skill、重试分层、长尾延迟、自动授权、网页授权边界、事故响应、模型回滚演示 | | 一键脚本 | [practice/preclass_run.sh](./practice/preclass_run.sh) | 自动执行 L10 环境检查和核心示例 | | 课前准备 | [materials/PRECLASS_CHECKLIST.md](./materials/PRECLASS_CHECKLIST.md) | 环境、概念和代码预习检查 | | 课堂笔记 | [materials/NOTES_TEMPLATE.md](./materials/NOTES_TEMPLATE.md) | 记录 Skill 设计、触发规则和评测方案 | | 课后小测 | [materials/MINI_QUIZ.md](./materials/MINI_QUIZ.md) | 检查 Skill 核心概念 | | 拓展练习 | [materials/EXTENSIONS.md](./materials/EXTENSIONS.md) | 学术论文 Skill、真实 LLM 路由、评测集和安全机制 | | 面试题库 | [materials/INTERVIEW_QA.md](./materials/INTERVIEW_QA.md) | Skill 概念、设计、编排、安全、评测和评分标准 | | 工程参考 | [resources/](./resources/) | Tool/Skill/MCP、DDICE、渐进披露、安全评测、重试分层、长尾延迟、自动授权、网页授权边界、误触发事故响应、模型升级回滚 | | 运行数据 | [data/](./data/) | 后续 Skill 评测样本和运行 trace | ## 推荐学习路径 1. 阅读 [lecture/LECTURE_FULL.md](./lecture/LECTURE_FULL.md) 的 10.1-10.3，先建立 Tool、Skill、MCP 的层级认知。 2. 阅读 `skills/weather-query/SKILL.md`，理解一个最小 Skill 如何声明触发条件、执行步骤和输出约束。 3. 运行 `practice/34_skill_loader.py`，观察 SKILL.md 如何被发现和解析。 4. 运行 `practice/35_weather_skill_agent.p"
    },
    {
      "id": "L11_eval_and_deployment",
      "code": "L11",
      "title": "L11 评测和部署：从 Demo 能跑到生产可用",
      "intro": "本章把 Agent 从“本地能跑”推进到“可评估、可调优、可服务化、可观测”。前半部分讲评测与调优，后半部分讲 FastAPI 部署、流式输出、前端接入、成本监控和安全防护。",
      "topics": [
        "评测",
        "部署",
        "FastAPI",
        "SSE",
        "成本监控",
        "安全护栏"
      ],
      "goals": [
        "理解为什么 Agent 不能只靠“问几个问题感觉不错”就上线。",
        "掌握准确性、完整性、相关性、安全性、效率成本和鲁棒性六类评估维度。",
        "能构建覆盖事实问答、闲聊、边界输入、Prompt 注入和完整性问题的评测数据集。",
        "能运行自动化评测，并检查关键词、工具调用、安全红线和分类得分。",
        "能识别幻觉、死循环、工具误调、格式错乱、Prompt 注入等常见翻车场景。",
        "能用 FastAPI 将 Agent 封装成 REST API，并提供健康检查。",
        "能用 SSE 实现流式输出，并用 HTML 页面接入。",
        "能理解 Gunicorn、Nginx、SSE 代理配置、成本监控和输入安全防护。"
      ],
      "deliverables": [
        "一份 Agent 评测数据集。",
        "一份自动化评测报告 JSON。",
        "一张“翻车场景 -> 诊断 -> 修复”的调优表。",
        "一个 FastAPI `/chat` 接口。",
        "一个 SSE `/chat/stream` 接口。",
        "一个可接入流式 API 的 HTML 页面。",
        "一份成本监控摘要。",
        "一份部署前安全检查清单。"
      ],
      "docs": [
        {
          "key": "readme",
          "label": "章节入口",
          "path": "lessons/L11_eval_and_deployment/README.md",
          "contentPath": "data/docs/L11_eval_and_deployment/readme.md",
          "excerpt": "# L11 评测和部署：从 Demo 能跑到生产可用 本章把 Agent 从“本地能跑”推进到“可评估、可调优、可服务化、可观测”。前半部分讲评测与调优，后半部分讲 FastAPI 部署、流式输出、前端接入、成本监控和安全防护。 > 说明：老师材料中“Agent 评估与调优”标题写作第 10 讲；在当前课程总目录中，第 10 讲已用于 Skill 相关内容，因此这里按你提供的要求归入 L11“评测和部署”。 ## 本章学习目标 - 理解为什么 Agent 不能只靠“问几个问题感觉不错”就上线。 - 掌握准确性、完整性、相关性、安全性、效率成本和鲁棒性六类评估维度。 - 能构建覆盖事实问答、闲聊、边界输入、Prompt 注入和完整性问题的评测数据集。 - 能运行自动化评测，并检查关键词、工具调用、安全红线和分类得分。 - 能识别幻觉、死循环、工具误调、格式错乱、Prompt 注入等常见翻车场景。 - 能用 FastAPI 将 Ag"
        },
        {
          "key": "lecture",
          "label": "完整讲义",
          "path": "lessons/L11_eval_and_deployment/lecture/LECTURE_FULL.md",
          "contentPath": "data/docs/L11_eval_and_deployment/lecture.md",
          "excerpt": "# 第11讲：Agent 评测和部署 —— 从“能跑”到“好用” 本章由两条主线组成：第一条是 Agent 评估与调优，解决“怎么证明它真的好用”；第二条是服务化部署，解决“怎么让别人稳定使用它”。 ## 11.1 为什么需要评估 搭了一个 Agent，问几个问题，效果还不错，然后直接上线，是很危险的。 没有系统化评估，就不知道 Agent 在什么情况下会翻车。生产环境中的翻车代价可能很高： - 回答错误，导致用户做出错误决策。 - 泄露系统提示词或敏感信息。 - 调错工具，触发不该触发的动作。 - 进入工具调用死循环，造成延迟和成本失控。 - 面对恶意输入时绕过安全边界。 评估的目的不是追求一个漂亮分数，而是建立一套可重复的“考试机制”：每次改 prompt、换模型、加工具、改 RAG 策略，都能用同一批问题判断是否真的变好。 ## 11.2 Agent 的评估维度 Agent 的评估不像传统软件只有“对/错”。它同时包含答案"
        },
        {
          "key": "summary",
          "label": "章节总结",
          "path": "lessons/L11_eval_and_deployment/lecture/CHAPTER_SUMMARY.md",
          "contentPath": "data/docs/L11_eval_and_deployment/summary.md",
          "excerpt": "# L11 章节总结：评测和部署 ## 一句话 Agent 从 Demo 到生产，需要两件事：用评测证明它好用，用部署让它稳定可用。 ## 评估维度 | 维度 | 关注点 | | --- | --- | | 准确性 | 答案是否正确 | | 完整性 | 是否遗漏关键信息 | | 相关性 | 是否紧扣问题 | | 安全性 | 是否泄露信息、越权或被注入 | | 效率/成本 | 工具次数、token、延迟 | | 鲁棒性 | 空输入、长输入、恶意输入 | ## 评测集要包含 - 正常事实问答。 - 闲聊和不该调用工具的请求。 - 空输入、超长输入。 - Prompt Injection。 - 多子问题完整性。 - 无答案拒答。 ## 代码地图 - `practice/eval_deploy_common.py`：评测数据结构、mock Agent、评分器、成本和安全工具。 - `practice/44_eval_dataset.py"
        },
        {
          "key": "preclass",
          "label": "课前准备",
          "path": "lessons/L11_eval_and_deployment/materials/PRECLASS_CHECKLIST.md",
          "contentPath": "data/docs/L11_eval_and_deployment/preclass.md",
          "excerpt": "# L11 课前检查清单 ## 环境 - [ ] 已激活 `agent_course` conda 环境。 - [ ] 已安装 `requirements/core.txt`、`requirements/langchain.txt` 和 `requirements/deployment.txt`。 - [ ] `fastapi`、`uvicorn`、`sse-starlette` 可导入。 检查命令： ```bash source <course-root>/scripts/activate_course.sh python -c \"import fastapi, uvicorn, sse_starlette; print('ok')\" ``` ## 概念 - [ ] 我能说出 Agent 评估的六个维度。 - [ ] 我知道为什么只做关键词匹配不够。 - [ ] 我知道为什么要检查工具调用 trace。 - [ ] 我能解释 "
        },
        {
          "key": "quiz",
          "label": "课后小测",
          "path": "lessons/L11_eval_and_deployment/materials/MINI_QUIZ.md",
          "contentPath": "data/docs/L11_eval_and_deployment/quiz.md",
          "excerpt": "# L11 小测 1. 为什么 Agent 不能只靠手工问几个问题就上线？ 2. Agent 评估至少包含哪六个维度？ 3. 为什么 `expected_tool` 要参与评测？ 4. 关键词匹配会产生哪两类问题？ 5. 安全评估为什么不应该只作为总分里的普通权重？ 6. 幻觉、死循环、工具误调分别怎么修复？ 7. `/health` 接口为什么不应该调用模型？ 8. SSE 流式输出相比一次性返回有什么好处？ 9. Nginx 代理 SSE 时为什么要关闭 `proxy_buffering`？ 10. 部署后需要记录哪些成本和安全字段？ ## 参考答案 1. 手工样例无法覆盖边界、安全、工具误调和长尾问题。 2. 准确性、完整性、相关性、安全性、效率/成本、鲁棒性。 3. Agent 的过程也重要，工具调错可能导致成本、安全和答案风险。 4. 假阳性和假阴性。 5. 严重安全失败应作为 hard gate，而不是被平均分掩盖。"
        },
        {
          "key": "extensions",
          "label": "拓展作业",
          "path": "lessons/L11_eval_and_deployment/materials/EXTENSIONS.md",
          "contentPath": "data/docs/L11_eval_and_deployment/extensions.md",
          "excerpt": "# L11 拓展练习 ## 练习 1：扩展评测集 在 `practice/eval_deploy_common.py` 中新增 10 条 case，至少覆盖： - 无答案拒答。 - 工具失败。 - 多工具问题。 - Prompt Injection。 - 超长输入。 - 引用正确率。 运行： ```bash python practice/45_eval_runner.py ``` ## 练习 2：接入真实 RAG Agent 把 `MockAgent` 替换成 L05 的 RAG Agent。 要求返回结构： ```json { \"answer\": \"...\", \"tool_calls\": [\"search_knowledge_base\"], \"citations\": [\"...\"], \"elapsed_ms\": 1200 } ``` ## 练习 3：实现 `/chat/rag` 基于 `practice/47_agent_a"
        },
        {
          "key": "interview",
          "label": "面试题",
          "path": "lessons/L11_eval_and_deployment/materials/INTERVIEW_QA.md",
          "contentPath": "data/docs/L11_eval_and_deployment/interview.md",
          "excerpt": "# L11 面试题速查：Agent 评测和部署 ## 来源说明 - 题目来源：基于老师提供的 Agent 评估与调优材料、部署材料，以及本章配套代码整理。 - 整理方式：不是逐字摘抄，而是把课堂内容整理成面试可表达的问答。 - 补充边界：CI 门禁、日志字段、SSE 事件设计、Nginx 细节和成本监控属于工程化补充。 ## 一、评估与调优 ### 1. 为什么 Agent 需要系统化评估？ 因为 Agent 的失败往往不是程序崩溃，而是回答错误、工具误调、幻觉、安全越界或成本失控。只手工问几个问题无法覆盖边界场景，也无法判断改 prompt 或换模型后是否整体退化。 ### 2. Agent 评估有哪些核心维度？ 准确性、完整性、相关性、安全性、效率/成本、鲁棒性。生产系统还会进一步拆出引用正确率、工具选择准确率、参数准确率、拒答正确率和用户满意度。 ### 3. 如何设计 Agent 评测集？ 每条 case 至少包含问题、"
        },
        {
          "key": "resource:COST_AND_SAFETY_MONITORING",
          "label": "资源：COST_AND_SAFETY_MONITORING",
          "path": "lessons/L11_eval_and_deployment/resources/COST_AND_SAFETY_MONITORING.md",
          "contentPath": "data/docs/L11_eval_and_deployment/resource_COST_AND_SAFETY_MONITORING.md",
          "excerpt": "# 成本监控与安全防护 部署后的 Agent 不只是“能访问”，还要可控。 ## 1. 成本指标 至少记录： - 请求数。 - 输入 token。 - 输出 token。 - 平均延迟。 - P95/P99 延迟。 - 工具调用次数。 - 单请求估算成本。 成本异常常见原因： - 简单问题走复杂 Agent。 - 工具调用死循环。 - 历史上下文无限增长。 - RAG 检索塞入过多 chunk。 - 没有缓存高频问题。 ## 2. 成本控制方法 - 简单问题走轻量模型。 - 设置最大上下文长度。 - 限制最大工具步数。 - 对高频问题做缓存。 - RAG top_k 和 chunk 长度可配置。 - 长任务异步化，不占用同步请求。 ## 3. 安全防护 输入侧： - 检测 Prompt Injection 模式"
        },
        {
          "key": "resource:EVALUATION_SYSTEM_DESIGN",
          "label": "资源：EVALUATION_SYSTEM_DESIGN",
          "path": "lessons/L11_eval_and_deployment/resources/EVALUATION_SYSTEM_DESIGN.md",
          "contentPath": "data/docs/L11_eval_and_deployment/resource_EVALUATION_SYSTEM_DESIGN.md",
          "excerpt": "# Agent 评估体系设计 Agent 评估的目标不是证明“这次演示能跑”，而是回答三个问题： 1. 它在哪些场景稳定可用？ 2. 它在哪些场景容易翻车？ 3. 每次调优后，是整体变好了，还是只是修好了一个样例？ ## 1. 评估维度 | 维度 | 衡量什么 | 示例 | | --- | --- | --- | | 准确性 | 回答是否正确 | 年假天数是否符合制度 | | 完整性 | 是否遗漏关键信息 | 部署流程是否漏掉审批或回滚 | | 相关性 | 是否紧扣问题 | 技术问题是否跑到闲聊 | | 安全性 | 是否泄露敏感信息或执行越权动作 | Prompt Injection 是否成功 | | 效率/成本 | 工具调用次数、耗时、token | 简单问题是否调用 10 次工具 | | 鲁棒性 | 对空输"
        },
        {
          "key": "resource:FAILURE_TUNING_PLAYBOOK",
          "label": "资源：FAILURE_TUNING_PLAYBOOK",
          "path": "lessons/L11_eval_and_deployment/resources/FAILURE_TUNING_PLAYBOOK.md",
          "contentPath": "data/docs/L11_eval_and_deployment/resource_FAILURE_TUNING_PLAYBOOK.md",
          "excerpt": "# Agent 翻车场景与调优手册 Agent 调优的第一步不是改 prompt，而是先判断翻车类型。 ## 常见场景 | 翻车场景 | 症状 | 修复方法 | | --- | --- | --- | | 幻觉 | 编造不存在的信息 | 只基于检索结果回答，无证据拒答，强制引用 | | 死循环 | 反复调用同一个工具 | 设置最大步数，检测重复 tool call，失败后降级 | | 工具误调 | 该查知识库却去计算 | 优化工具描述，加“何时不用”，做工具选择评测 | | 格式错乱 | JSON 不合法或字段缺失 | 使用 schema、few-shot、解析失败有限重试 | | Prompt 注入 | 用户绕过约束或索要系统提示词 | 输入校验、外部内容当数据、高风险确认 | | 成本失控 | 简单问题走复"
        },
        {
          "key": "resource:FASTAPI_DEPLOYMENT_RUNBOOK",
          "label": "资源：FASTAPI_DEPLOYMENT_RUNBOOK",
          "path": "lessons/L11_eval_and_deployment/resources/FASTAPI_DEPLOYMENT_RUNBOOK.md",
          "contentPath": "data/docs/L11_eval_and_deployment/resource_FASTAPI_DEPLOYMENT_RUNBOOK.md",
          "excerpt": "# FastAPI 部署 Runbook 本章部署目标：把本地命令行 Agent 变成可被网页或 API 调用的服务。 ## 1. 本地运行 在课程环境中： ```bash source <course-root>/scripts/activate_course.sh cd <course-root>/lessons/L11_eval_and_deployment/practice uvicorn 47_agent_api:app --host 0.0.0.0 --port 8000 --reload ``` 健康检查： ```bash curl http://localhost:8000/health ``` 对话接口： ```bash curl -X POST http://localhost:8000/c"
        },
        {
          "key": "resource:STREAMING_FRONTEND_NOTES",
          "label": "资源：STREAMING_FRONTEND_NOTES",
          "path": "lessons/L11_eval_and_deployment/resources/STREAMING_FRONTEND_NOTES.md",
          "contentPath": "data/docs/L11_eval_and_deployment/resource_STREAMING_FRONTEND_NOTES.md",
          "excerpt": "# 流式输出与前端接入 流式输出解决的是体验问题：Agent 可能需要检索、工具调用和多步推理，如果用户只能等最终结果，体感延迟会很高。 ## 1. SSE 事件设计 推荐事件类型： ```json {\"type\": \"tool_call\", \"tool\": \"search_knowledge_base\"} {\"type\": \"token\", \"content\": \"根据公司制度\"} {\"type\": \"done\", \"session_id\": \"user_001\"} {\"type\": \"error\", \"message\": \"...\"} ``` 这样前端可以分别展示： - 工具调用状态。 - 打字机文本。 - 完成标记。 - 错误提示。 ## 2. 为什么不用一次性返回 一次性返回的问题： - 用户不知道系统"
        }
      ],
      "practiceFiles": [
        {
          "name": "44_eval_dataset.py",
          "path": "lessons/L11_eval_and_deployment/practice/44_eval_dataset.py",
          "size": "767 B"
        },
        {
          "name": "45_eval_runner.py",
          "path": "lessons/L11_eval_and_deployment/practice/45_eval_runner.py",
          "size": "1.4 KB"
        },
        {
          "name": "46_failure_tuning_playbook.py",
          "path": "lessons/L11_eval_and_deployment/practice/46_failure_tuning_playbook.py",
          "size": "2.0 KB"
        },
        {
          "name": "47_agent_api.py",
          "path": "lessons/L11_eval_and_deployment/practice/47_agent_api.py",
          "size": "2.7 KB"
        },
        {
          "name": "48_agent_api_streaming.py",
          "path": "lessons/L11_eval_and_deployment/practice/48_agent_api_streaming.py",
          "size": "3.4 KB"
        },
        {
          "name": "49_cost_monitor.py",
          "path": "lessons/L11_eval_and_deployment/practice/49_cost_monitor.py",
          "size": "1004 B"
        },
        {
          "name": "50_safety_guardrails.py",
          "path": "lessons/L11_eval_and_deployment/practice/50_safety_guardrails.py",
          "size": "884 B"
        },
        {
          "name": "eval_deploy_common.py",
          "path": "lessons/L11_eval_and_deployment/practice/eval_deploy_common.py",
          "size": "11.6 KB"
        },
        {
          "name": "preclass_run.sh",
          "path": "lessons/L11_eval_and_deployment/practice/preclass_run.sh",
          "size": "632 B"
        },
        {
          "name": "chat_frontend.html",
          "path": "lessons/L11_eval_and_deployment/practice/chat_frontend.html",
          "size": "3.5 KB"
        }
      ],
      "resourceFiles": [
        {
          "name": "COST_AND_SAFETY_MONITORING.md",
          "path": "lessons/L11_eval_and_deployment/resources/COST_AND_SAFETY_MONITORING.md",
          "size": "1.5 KB"
        },
        {
          "name": "EVALUATION_SYSTEM_DESIGN.md",
          "path": "lessons/L11_eval_and_deployment/resources/EVALUATION_SYSTEM_DESIGN.md",
          "size": "3.4 KB"
        },
        {
          "name": "FAILURE_TUNING_PLAYBOOK.md",
          "path": "lessons/L11_eval_and_deployment/resources/FAILURE_TUNING_PLAYBOOK.md",
          "size": "2.0 KB"
        },
        {
          "name": "FASTAPI_DEPLOYMENT_RUNBOOK.md",
          "path": "lessons/L11_eval_and_deployment/resources/FASTAPI_DEPLOYMENT_RUNBOOK.md",
          "size": "2.8 KB"
        },
        {
          "name": "STREAMING_FRONTEND_NOTES.md",
          "path": "lessons/L11_eval_and_deployment/resources/STREAMING_FRONTEND_NOTES.md",
          "size": "1.3 KB"
        }
      ],
      "materialFiles": [
        {
          "name": "EXTENSIONS.md",
          "path": "lessons/L11_eval_and_deployment/materials/EXTENSIONS.md",
          "size": "1.3 KB"
        },
        {
          "name": "INTERVIEW_QA.md",
          "path": "lessons/L11_eval_and_deployment/materials/INTERVIEW_QA.md",
          "size": "5.2 KB"
        },
        {
          "name": "MINI_QUIZ.md",
          "path": "lessons/L11_eval_and_deployment/materials/MINI_QUIZ.md",
          "size": "1.4 KB"
        },
        {
          "name": "NOTES_TEMPLATE.md",
          "path": "lessons/L11_eval_and_deployment/materials/NOTES_TEMPLATE.md",
          "size": "1.8 KB"
        },
        {
          "name": "PRECLASS_CHECKLIST.md",
          "path": "lessons/L11_eval_and_deployment/materials/PRECLASS_CHECKLIST.md",
          "size": "1.3 KB"
        }
      ],
      "dataFiles": [
        {
          "name": "README.md",
          "path": "lessons/L11_eval_and_deployment/data/README.md",
          "size": "398 B"
        },
        {
          "name": "cost_summary.json",
          "path": "lessons/L11_eval_and_deployment/data/cost_summary.json",
          "size": "146 B"
        },
        {
          "name": "eval_dataset.json",
          "path": "lessons/L11_eval_and_deployment/data/eval_dataset.json",
          "size": "1.8 KB"
        },
        {
          "name": "eval_results.json",
          "path": "lessons/L11_eval_and_deployment/data/eval_results.json",
          "size": "5.3 KB"
        }
      ],
      "preclassCommand": "cd lessons/L11_eval_and_deployment && bash practice/preclass_run.sh",
      "fileCount": 27,
      "searchText": "# L11 评测和部署：从 Demo 能跑到生产可用 本章把 Agent 从“本地能跑”推进到“可评估、可调优、可服务化、可观测”。前半部分讲评测与调优，后半部分讲 FastAPI 部署、流式输出、前端接入、成本监控和安全防护。 > 说明：老师材料中“Agent 评估与调优”标题写作第 10 讲；在当前课程总目录中，第 10 讲已用于 Skill 相关内容，因此这里按你提供的要求归入 L11“评测和部署”。 ## 本章学习目标 - 理解为什么 Agent 不能只靠“问几个问题感觉不错”就上线。 - 掌握准确性、完整性、相关性、安全性、效率成本和鲁棒性六类评估维度。 - 能构建覆盖事实问答、闲聊、边界输入、Prompt 注入和完整性问题的评测数据集。 - 能运行自动化评测，并检查关键词、工具调用、安全红线和分类得分。 - 能识别幻觉、死循环、工具误调、格式错乱、Prompt 注入等常见翻车场景。 - 能用 FastAPI 将 Agent 封装成 REST API，并提供健康检查。 - 能用 SSE 实现流式输出，并用 HTML 页面接入。 - 能理解 Gunicorn、Nginx、SSE 代理配置、成本监控和输入安全防护。 ## 文件分区 | 分类 | 路径 | 用途 | | --- | --- | --- | | 讲义 | [lecture/LECTURE_FULL.md](./lecture/LECTURE_FULL.md) | 第 11 讲完整讲义：评测、调优、API、流式和部署 | | 总结 | [lecture/CHAPTER_SUMMARY.md](./lecture/CHAPTER_SUMMARY.md) | 核心概念、代码地图和上线检查 | | 实操代码 | [practice/](./practice/) | 评测集、评测器、FastAPI、SSE、成本、安全示例 | | 前端页面 | [practice/chat_frontend.html](./practice/chat_frontend.html) | 调用流式 API 的最小 HTML 页面 | | 一键脚本 | [practice/preclass_run.sh](./practice/preclass_run.sh) | 自动执行 L11 本地检查和核心示例 | | 课前准备 | [materials/PRECLASS_CHECKLIST.md](./materials/PRECLASS_CHECKLIST.md) | 环境、概念和代码预习 | | 课堂笔记 | [materials/NOTES_TEMPLATE.md](./materials/NOTES_TEMPLATE.md) | 记录评测指标、调优策略和部署方案 | | 课后小测 | [materials/MINI_QUIZ.md](./materials/MINI_QUIZ.md) | 检查评测与部署核心概念 | | 拓展练习 | [materials/EXTENSIONS.md](./materials/EXTENSIONS.md) | 真实 RAG API、CI 评测、流式前端和监控扩展 | | 面试题库 | [materials/INTERVIEW_QA.md](./materials/INTERVIEW_QA.md) | Agent 评估、调优、部署、安全和成本面试题 | | 工程参考 | [resources/](./resources/) | 评估体系、调优手册、部署 runbook、流式前端、成本安全 | | 运行数据 | [data/](./data/) | 评测数据集、评测结果和成本摘要 | ## 推荐学习路径 1. 阅读 [lecture/LECTURE_FULL.md](./lecture/LECTURE_FULL.md) 的 11.1-11.4，理解 Agent 评估为什么比传统单元测试更复杂。 2. 运行 `practice/44_eval_dataset.py`，查看评测集如何覆盖事实、闲聊、边界、安全和完整性。 3. 运行 `practice/45_eval_runner.py`，观察关键词、工具调用和安全检查如何组合成评测结果。 4. 阅读 [resources/EVALUATION_SYSTEM_DESIGN.md](./resources/EVALUATION_SYSTEM_DESIGN.md)，理解为什么关键词匹配只是 baseline。 5. 运行 `practice/46_failure_tuning_playbook.py`，复盘常见翻车场景和修复策略。 6. 运行 `practice/47_agent_api.py --self-test`，理解 Agent 如何封装成 REST API。 7. 运行 `practice/48_agent_api_streaming.py --self-test`，理解 SSE 事件流。 8. 阅读 [resources/FASTAPI_DEPLOYMENT_RUNBOOK.md](./resources/FASTAPI_DEPLOYMENT_RUNBOOK.md)，理解本地、Gunicorn 和 Ng"
    },
    {
      "id": "L12_graduation_project",
      "code": "L12",
      "title": "L12 毕业项目实战：智能客服 Agent",
      "intro": "本章把前 11 讲的能力收束到一个端到端项目：**基于 LangGraph + RAG + FastAPI + Harness 工程实践的智能客服 Agent**。",
      "topics": [
        "毕业项目",
        "智能客服",
        "LangGraph",
        "RAG",
        "FastAPI",
        "Harness"
      ],
      "goals": [
        "能把“需求 -> 技术方案 -> 测试设计 -> Harness 约束 -> 实现 -> 评测 -> 部署 -> 答辩”串成闭环。",
        "理解毕业项目为什么选择智能客服 Agent，以及它如何覆盖 RAG、Memory、Agent 模式、评测部署和 Skill 思维。",
        "掌握 LangGraph 状态机在真实项目中的节点拆分、条件路由、兜底和可观测设计。",
        "能使用参考实现完成本地运行、自动测试、评测脚本、FastAPI 服务和前端展示。",
        "能把项目亮点整理成答辩和面试表达。"
      ],
      "deliverables": [
        "一份项目需求说明：选题、用户目标、范围和验收标准。",
        "一份技术方案：LangGraph 流程、RAG 检索、记忆、工单、可观测、部署。",
        "一份测试与评测设计：单元测试、接口测试、业务评测集和质量门禁。",
        "一个可运行项目：FastAPI、RAG、LangGraph、前端页面、Dashboard。",
        "一次完整验证记录：`pytest -q`、`python evals/run_eval.py`、API `/health` 和 `/chat`。",
        "一份答辩稿：项目定位、架构亮点、困难与取舍、后续迭代。"
      ],
      "docs": [
        {
          "key": "readme",
          "label": "章节入口",
          "path": "lessons/L12_graduation_project/README.md",
          "contentPath": "data/docs/L12_graduation_project/readme.md",
          "excerpt": "# L12 毕业项目实战：智能客服 Agent 本章把前 11 讲的能力收束到一个端到端项目：**基于 LangGraph + RAG + FastAPI + Harness 工程实践的智能客服 Agent**。 它不是单轮 RAG Demo，而是一个可以运行、测试、评测、部署、演示和答辩的完整工程：知识库问答、多轮澄清、意图识别、投诉工单、无法回答转人工、可观测日志、质量门禁、前端客服台和运营 Dashboard。 ## 本章学习目标 - 能把“需求 -> 技术方案 -> 测试设计 -> Harness 约束 -> 实现 -> 评测 -> 部署 -> 答辩”串成闭环。 - 理解毕业项目为什么选择智能客服 Agent，以及它如何覆盖 RAG、Memory、Agent 模式、评测部署和 Skill 思维。 - 掌握 LangGraph 状态机在真实项目中的节点拆分、条件路由、兜底和可观测设计。 - 能使用参考实现完成本地运行、自动"
        },
        {
          "key": "lecture",
          "label": "完整讲义",
          "path": "lessons/L12_graduation_project/lecture/LECTURE_FULL.md",
          "contentPath": "data/docs/L12_graduation_project/lecture.md",
          "excerpt": "# 第 12 讲：毕业项目实战 —— 智能客服 Agent ## 12.1 为什么毕业项目选择智能客服 Agent？ 智能客服 Agent 是一个非常适合收束本课程的项目，因为它天然需要把前面章节的能力串起来： - 需要 Prompt 约束回答边界。 - 需要 Function Calling / Tool 封装知识库检索、工单、记忆和日志。 - 需要 RAG 解决私域知识问答。 - 需要 Memory 支持多轮会话。 - 需要 Agent 模式处理澄清、转人工和兜底。 - 需要 LangGraph 显式编排流程。 - 需要评测和部署证明系统不是一次性 Demo。 老师任务包给出的最终选题是： ```text 选题 A：智能客服 Agent ``` 核心目标： ```text 基于 LangGraph + RAG + FastAPI + Harness 工程实践，实现一个可运行、可测试、可评测、可部署、可答辩的智能客服 Agen"
        },
        {
          "key": "summary",
          "label": "章节总结",
          "path": "lessons/L12_graduation_project/lecture/CHAPTER_SUMMARY.md",
          "contentPath": "data/docs/L12_graduation_project/summary.md",
          "excerpt": "# L12 章节总结：毕业项目实战 ## 一句话目标 实现一个基于 LangGraph + RAG + FastAPI + Harness 的智能客服 Agent，证明它可运行、可测试、可评测、可部署、可观测、可答辩。 ## 核心闭环 ```text 需求 -> PRD/TRD/TDD -> Harness -> 实现 -> 测试 -> 评测 -> 部署 -> 监控 -> 复盘 ``` ## 必须掌握 - 智能客服 Agent 的最低验收：RAG、LangGraph、FastAPI、评测集、评测脚本。 - Harness 思维：状态、工具边界、上下文、验证、机械约束和可观测性。 - LangGraph 流程：加载记忆、意图分类、路由、检索、回答、评估、澄清、工单、转人工。 - RAG 安全边界：有证据才答，无证据转人工或澄清。 - 评测方式：独立评测器，不让主 Agent 自评。 - 答辩表达：讲设计取舍，不只罗列技术名词。 #"
        },
        {
          "key": "preclass",
          "label": "课前准备",
          "path": "lessons/L12_graduation_project/materials/PRECLASS_CHECKLIST.md",
          "contentPath": "data/docs/L12_graduation_project/preclass.md",
          "excerpt": "# L12 课前准备清单 ## 环境检查 - [ ] 已激活 `agent_course` conda 环境。 - [ ] 已安装课程依赖：`core.txt`、`langchain.txt`、`deployment.txt`。 - [ ] 能运行 `python --version`，版本为 Python 3.11+。 - [ ] 能运行 `python -c \"import fastapi, langgraph, pydantic, pytest\"`。 ## 文档阅读 - [ ] 阅读 `resources/project_packet/01_ASSIGNMENT_REQUIREMENTS.md`。 - [ ] 阅读 `resources/project_packet/02_HARNESS_ENGINEERING_GUIDE.md`。 - [ ] 阅读 `resources/project_packet/PRACTICE_R"
        },
        {
          "key": "quiz",
          "label": "课后小测",
          "path": "lessons/L12_graduation_project/materials/MINI_QUIZ.md",
          "contentPath": "data/docs/L12_graduation_project/quiz.md",
          "excerpt": "# L12 课后小测 1. 为什么毕业项目不能只做“用户问题 -> LLM 回答”？ 2. 智能客服 Agent 的四个核心功能是什么？ 3. 本项目为什么要求至少 10 份知识库文档？ 4. LangGraph 在本项目里解决了什么问题？ 5. 投诉类问题为什么必须走工单，而不是直接回答一句“已收到”？ 6. 无知识库证据时，系统应该怎么做？ 7. Harness Engineering 和 Prompt Engineering 的区别是什么？ 8. 为什么评测脚本要独立于主 Agent？ 9. `trace_id` 在可观测性中有什么价值？ 10. 如果要把本项目抽成 MCP 或 Skill，你会优先抽哪个能力？为什么？"
        },
        {
          "key": "extensions",
          "label": "拓展作业",
          "path": "lessons/L12_graduation_project/materials/EXTENSIONS.md",
          "contentPath": "data/docs/L12_graduation_project/extensions.md",
          "excerpt": "# L12 拓展练习 ## 必做巩固 1. 新增一份知识库文档，运行： ```bash python scripts/build_kb.py python evals/run_eval.py ``` 2. 新增两条评测用例：一条正常问答，一条无法回答转人工。 3. 在 Dashboard 或 `/audit/{trace_id}` 中回放一次完整请求。 4. 修改一条业务规则后，补充对应测试。 ## 进阶增强 1. 多跳 RAG：为复杂问题加入子问题拆解，保留 `max_hops <= 3`。 2. ReAct 兜底：只在低置信度或多跳失败时触发，保留 `max_steps <= 4`。 3. RRF 融合：将多个 collection 的召回结果统一重排。 4. 监控增强：增加 P50/P95、意图分布、工单率、低置信度率。 5. 安全增强：为更多管理接口加权限、限流和审计。 ## MCP / Skill 加分项 1. 设计 "
        },
        {
          "key": "interview",
          "label": "面试题",
          "path": "lessons/L12_graduation_project/materials/INTERVIEW_QA.md",
          "contentPath": "data/docs/L12_graduation_project/interview.md",
          "excerpt": "# L12 面试速查：毕业项目智能客服 Agent ## 1. 你这个毕业项目一句话怎么介绍？ 这是一个基于 LangGraph + RAG + FastAPI + Harness 工程实践的智能客服 Agent，支持知识库问答、多轮澄清、意图识别、投诉工单、无法回答转人工、评测脚本、可观测日志、前端客服台和运营 Dashboard。 ## 2. 它和普通 RAG Demo 有什么区别？ 普通 RAG Demo 通常只有“检索 -> 生成”。本项目有完整客服流程： - 意图分类。 - 条件路由。 - 多轮记忆。 - 模糊澄清。 - 投诉工单。 - 无证据转人工。 - 评测和质量门禁。 - 可观测和审计回放。 所以它更接近一个生产系统，而不是一次性问答脚本。 ## 3. 为什么用 LangGraph？ 因为客服流程不是单链路，而是条件分支流程。LangGraph 可以显式表达状态、节点和条件边，例如： ```text qa -> "
        },
        {
          "key": "resource:PROJECT_INTEGRATION_REVIEW",
          "label": "资源：PROJECT_INTEGRATION_REVIEW",
          "path": "lessons/L12_graduation_project/resources/PROJECT_INTEGRATION_REVIEW.md",
          "contentPath": "data/docs/L12_graduation_project/resource_PROJECT_INTEGRATION_REVIEW.md",
          "excerpt": "# L12 来源审阅与归档说明 ## 一、来源目录 本次 L12 整理合并了两个外部目录： | 来源 | 角色 | 归档位置 | | --- | --- | --- | | `<archived-source>/agent_course_2026_final/codex_customer_agent_packet` | 老师毕业项目任务包、Harness 要求、Codex 任务书和 Word 实战参考 | `resources/project_packet/` | | `<archived-source>/intelligent_customer_agent` | 已完成的智能客服 Agent 参考实现 | `reference_implementation/intelligent_customer_agent"
        }
      ],
      "practiceFiles": [
        {
          "name": "preclass_run.sh",
          "path": "lessons/L12_graduation_project/practice/preclass_run.sh",
          "size": "647 B"
        }
      ],
      "resourceFiles": [
        {
          "name": "PROJECT_INTEGRATION_REVIEW.md",
          "path": "lessons/L12_graduation_project/resources/PROJECT_INTEGRATION_REVIEW.md",
          "size": "3.3 KB"
        }
      ],
      "materialFiles": [
        {
          "name": "EXTENSIONS.md",
          "path": "lessons/L12_graduation_project/materials/EXTENSIONS.md",
          "size": "1.4 KB"
        },
        {
          "name": "INTERVIEW_QA.md",
          "path": "lessons/L12_graduation_project/materials/INTERVIEW_QA.md",
          "size": "3.3 KB"
        },
        {
          "name": "MINI_QUIZ.md",
          "path": "lessons/L12_graduation_project/materials/MINI_QUIZ.md",
          "size": "663 B"
        },
        {
          "name": "NOTES_TEMPLATE.md",
          "path": "lessons/L12_graduation_project/materials/NOTES_TEMPLATE.md",
          "size": "811 B"
        },
        {
          "name": "PRECLASS_CHECKLIST.md",
          "path": "lessons/L12_graduation_project/materials/PRECLASS_CHECKLIST.md",
          "size": "1.3 KB"
        }
      ],
      "dataFiles": [],
      "preclassCommand": "cd lessons/L12_graduation_project && bash practice/preclass_run.sh",
      "fileCount": 117,
      "searchText": "# L12 毕业项目实战：智能客服 Agent 本章把前 11 讲的能力收束到一个端到端项目：**基于 LangGraph + RAG + FastAPI + Harness 工程实践的智能客服 Agent**。 它不是单轮 RAG Demo，而是一个可以运行、测试、评测、部署、演示和答辩的完整工程：知识库问答、多轮澄清、意图识别、投诉工单、无法回答转人工、可观测日志、质量门禁、前端客服台和运营 Dashboard。 ## 本章学习目标 - 能把“需求 -> 技术方案 -> 测试设计 -> Harness 约束 -> 实现 -> 评测 -> 部署 -> 答辩”串成闭环。 - 理解毕业项目为什么选择智能客服 Agent，以及它如何覆盖 RAG、Memory、Agent 模式、评测部署和 Skill 思维。 - 掌握 LangGraph 状态机在真实项目中的节点拆分、条件路由、兜底和可观测设计。 - 能使用参考实现完成本地运行、自动测试、评测脚本、FastAPI 服务和前端展示。 - 能把项目亮点整理成答辩和面试表达。 ## 文件分区 | 分类 | 路径 | 用途 | | --- | --- | --- | | 讲义 | [lecture/LECTURE_FULL.md](./lecture/LECTURE_FULL.md) | 毕业项目完整讲解：选题、验收、架构、实现路线和答辩 | | 总结 | [lecture/CHAPTER_SUMMARY.md](./lecture/CHAPTER_SUMMARY.md) | 本章关键闭环、检查清单和答辩要点 | | 任务包 | [resources/project_packet/](./resources/project_packet/) | 老师项目要求、Harness 指南、Codex 任务书、启动 Prompt 和 Word 原件 | | 实战参考摘录 | [resources/project_packet/PRACTICE_REFERENCE_EXTRACT.md](./resources/project_packet/PRACTICE_REFERENCE_EXTRACT.md) | 从 `具体实战参考.docx` 抽取的可读 Markdown 路线 | | 归档审阅 | [resources/PROJECT_INTEGRATION_REVIEW.md](./resources/PROJECT_INTEGRATION_REVIEW.md) | 两个来源目录的内容审阅、保留/排除策略和课程归档说明 | | 参考实现 | [reference_implementation/intelligent_customer_agent/](./reference_implementation/intelligent_customer_agent/) | 可运行的智能客服 Agent 完整项目 | | 课前准备 | [materials/PRECLASS_CHECKLIST.md](./materials/PRECLASS_CHECKLIST.md) | 环境、文档、命令和演示准备清单 | | 课堂笔记 | [materials/NOTES_TEMPLATE.md](./materials/NOTES_TEMPLATE.md) | 记录需求、架构、评测、问题和答辩素材 | | 课后小测 | [materials/MINI_QUIZ.md](./materials/MINI_QUIZ.md) | 检查毕业项目关键概念 | | 拓展练习 | [materials/EXTENSIONS.md](./materials/EXTENSIONS.md) | 多跳 RAG、ReAct、MCP/Skill、监控和安全增强 | | 面试速查 | [materials/INTERVIEW_QA.md](./materials/INTERVIEW_QA.md) | 项目答辩和 Agent 开发面试问答 | | 一键检查 | [practice/preclass_run.sh](./practice/preclass_run.sh) | 构建知识库、运行测试和评测参考实现 | ## 推荐学习路径 1. 阅读 [resources/project_packet/01_ASSIGNMENT_REQUIREMENTS.md](./resources/project_packet/01_ASSIGNMENT_REQUIREMENTS.md)，确认老师硬性要求。 2. 阅读 [resources/project_packet/02_HARNESS_ENGINEERING_GUIDE.md](./resources/project_packet/02_HARNESS_ENGINEERING_GUIDE.md)，理解本项目为什么不能只靠 Prompt。 3. 阅读 [resources/project_packet/PRACTICE_REFERENCE_EXTRACT.md](./resources/project_packet/PRACTICE_REFERENCE_EXTRACT.md)，把 Word 实战路线转成 6 轮"
    }
  ],
  "supportDocs": [
    {
      "key": "support:AGENT_DESIGN_PATTERNS",
      "title": "Agent 设计模式",
      "path": "teaching_support/AGENT_DESIGN_PATTERNS.md",
      "excerpt": "# Agent 设计模式 AI Agent 的设计模式，本质是在回答一个问题： > 当大模型不只是回答文本，而是要规划、调用工具、反思修正、多人协作时，系统应该如何组织执行过程？ 这份教辅资料聚焦四种经典模式： 1. ReAct：边思考边行动。 2. Plan-and-Execute：先规划，再执行。 3. Reflection：先生成，再反思修正。 4. Multi-Agent：多个 Agent 分工协作。 一句话区分： - ReAct 解决“边查边做”。 - Plan-and-Execute 解决“复杂任务先拆解”。 - Reflection 解决“做完检查和改进”。 - Multi-Agent 解决“多角色协作完成复杂任务”。 ## 一、ReAct 模式 ### 1. 核心思想 ReAct = Reasoning + Acting。 它让模型在任务执行过程中交替进行： ```text Thought -> Action -",
      "contentPath": "data/docs/teaching_support/support_AGENT_DESIGN_PATTERNS.md"
    },
    {
      "key": "support:AI_NATIVE_WORKFLOW",
      "title": "AI Native 的工作方式",
      "path": "teaching_support/AI_NATIVE_WORKFLOW.md",
      "excerpt": "# AI Native 的工作方式 这份教辅资料总结一线 AI-native 团队的组织实践。它关注的不是“员工会不会用 AI 工具”，而是组织是否围绕 **agent、context、loop** 重新设计工作方式。 一句话： > AI-native 不是把 AI 加进旧流程，而是围绕 agent、context 和 loop 重构组织执行系统。 ## 一、结论先看 1. Agent 已从“个人助手”演化为“组织执行单元”。很多团队不再是员工各自用 AI，而是由公司统一建设、维护和治理核心 agent。 2. Human in the loop 正在被压缩为 Human at the beginning and the end。人负责设定方向、验收结果，执行中的拆解、研究、实现、联动逐步交给 AI 闭环完成。 3. Context 管理正在替代传统知识管理。文档、聊天、会议记录、代码库、ticket、历史决策被视为同一个上下文",
      "contentPath": "data/docs/teaching_support/support_AI_NATIVE_WORKFLOW.md"
    },
    {
      "key": "support:BM25_INVERTED_INDEX",
      "title": "BM25 和倒排索引简单介绍",
      "path": "teaching_support/BM25_INVERTED_INDEX.md",
      "excerpt": "# BM25 和倒排索引简单介绍 这份教辅资料用于帮助学生理解关键词检索的底层逻辑。它不追求复杂公式，而是解释 BM25 为什么比朴素关键词计数更可靠，以及倒排索引为什么能让搜索变快。 适合配合第 5 讲 RAG、Hybrid Search、关键词检索、企业知识库检索一起讲。 ## 一、BM25 核心原理 BM25 做的事情很朴素：**给查询词和文档算相关性分数，分数越高越相关。** 它主要看三件事： 1. 词越稀有，权重越高。 2. 词出现次数越多，分数越高，但会封顶。 3. 文档越长，惩罚越重。 最终分数可以理解为：**每个查询词对文档的贡献加起来。** ### 1. 稀有词更重要 查询： ```text 苹果 手机 ``` 语料里的情况： - “手机”：100 篇文档都有，很常见，权重低。 - “苹果”：只有 5 篇文档有，很稀有，权重高。 BM25 的行为： - 文档出现“苹果”，分数涨得明显。 - 文档只出现“手机”，",
      "contentPath": "data/docs/teaching_support/support_BM25_INVERTED_INDEX.md"
    },
    {
      "key": "support:COMMON_DESIGN_PATTERNS",
      "title": "常见设计模式：工厂、发布订阅、装饰器、桥接",
      "path": "teaching_support/COMMON_DESIGN_PATTERNS.md",
      "excerpt": "# 常见设计模式：工厂、发布订阅、装饰器、桥接 这份教辅资料总结四种常见工程设计模式：工厂模式、发布订阅模式、装饰器模式、桥接模式。它们不是 Agent 独有概念，但在 Agent 工程里经常出现： - 工厂模式：根据配置创建模型、工具、Retriever、Skill。 - 发布订阅模式：把工具调用、评测事件、日志和监控解耦。 - 装饰器模式：给工具或 API 增加日志、权限、缓存、重试、限流。 - 桥接模式：把“抽象能力”和“具体实现”拆开，例如同一个 Agent 支持不同模型、不同检索后端。 ## 一、工厂模式 ### 1. 核心思想 工厂模式把对象创建逻辑封装起来。调用者不用关心具体怎么 `new`，只通过统一入口拿到需要的对象。 一句话： > 工厂模式解决“创建逻辑和使用逻辑耦合”的问题。 ### 2. 适用场景 - 创建逻辑复杂，需要根据条件决定实例化哪个类。 - 希望调用方和具体类解耦。 - 新增类型时，只扩展工厂，",
      "contentPath": "data/docs/teaching_support/support_COMMON_DESIGN_PATTERNS.md"
    },
    {
      "key": "support:EXTERNAL_LEARNING_RESOURCES",
      "title": "外部学习资源索引：你能够额外获取到什么？",
      "path": "teaching_support/EXTERNAL_LEARNING_RESOURCES.md",
      "excerpt": "# 外部学习资源索引：你能够额外获取到什么？ 这份教辅资料用于统一收纳课程之外的延伸阅读链接。它的作用不是替代课程讲义，而是告诉学生：每个外部资源适合放在哪一章之后读、应该重点看什么、不要误用什么。 > 使用提醒：外部链接内容、访问权限和 GitHub stars 都会变化，课堂以链接页面实时信息为准。涉及真实产品 prompt 的资料，只建议学习结构、边界设计和工程模式，不建议复制专有 prompt，也不要用于绕过产品安全策略。 ## 一、Agent 入门与经典范式 | 资源 | 适合章节 | 推荐看点 | | --- | --- | --- | | [datawhalechina/hello-agents](https://github.com/datawhalechina/hello-agents) | L01、L03、L08 | 从 Chatbot 到 Agent 的基础概念、经典范式、工具调用和案例结构 | 阅读建议：",
      "contentPath": "data/docs/teaching_support/support_EXTERNAL_LEARNING_RESOURCES.md"
    },
    {
      "key": "support:README",
      "title": "教辅资料",
      "path": "teaching_support/README.md",
      "excerpt": "# 教辅资料 本目录作为课程教辅资料入口，不重复搬运已有文件，统一索引课程规范、环境说明、运行脚本和共享资源。 ## 课程组织规范 - [章节目录规范](../LESSON_STRUCTURE_GUIDE.md) - [代码注释规范](../CODE_COMMENTING_GUIDE.md) - [课程总览 README](../README.md) ## 环境与依赖 - [依赖管理说明](../requirements/README.md) - [核心依赖](../requirements/core.txt) - [LangChain 依赖](../requirements/langchain.txt) - [RAG 依赖](../requirements/rag.txt) - [MCP 依赖](../requirements/mcp.txt) - [部署依赖](../requirements/deployment.txt) ",
      "contentPath": "data/docs/teaching_support/support_README.md"
    }
  ]
};
