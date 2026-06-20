# 第1讲讲义完整版：Agent 全景认知 —— 从 ChatBot 到自主智能体

适用对象：第一次系统学习 Agent 的同学
学习时长：60-90 分钟（不含拓展实操）
配套目录：`<course-root>/lessons/L01_agent_basics`
章节入口：`README.md`
章节总结：`CHAPTER_SUMMARY.md`

---

## 1.1 什么是 AI Agent？

一句话理解：AI Agent 是一个“能自己想、自己做”的 AI 程序。

### 生活化例子：订火锅

场景：你饿了，想吃火锅。

- 普通 ChatBot：你问“附近有什么火锅店？”，它给你推荐文本。到这里就结束，你还要自己比价格、看评分、打电话订位。
- AI Agent：你说“帮我订今晚 7 点火锅，2 个人，人均 100 以内”。它会自动搜索、筛选、比较、调用订位接口，并把确认信息返回给你。

### ChatBot 与 Agent 的核心区别

| 对比维度 | 普通 ChatBot | AI Agent |
| --- | --- | --- |
| 核心能力 | 回答问题 | 完成任务 |
| 交互方式 | 一问一答 | 给目标，自动执行 |
| 有没有“手脚” | 没有，只能说 | 有，能调用工具做事 |
| 有没有“记忆” | 通常没有 | 有，能记住上下文和历史 |
| 能不能自主决策 | 不能，等你问 | 能，自己拆解步骤并执行 |

### 正式定义

AI Agent 是一个以大语言模型（LLM）为“大脑”，具备自主规划、工具调用、记忆管理能力的智能程序。它能根据用户目标，自主拆解任务、调用外部工具、根据执行结果动态调整策略，最终完成复杂任务。

---

## 1.2 Agent 的核心架构

可以把 Agent 理解成一个“能干的员工”：

```text
你（用户）给出任务目标
       ↓
   ┌───────────┐
   │  🧠 大脑   │  ← LLM：理解任务、做出决策
   │   (LLM)   │
   └─────┬─────┘
         │ 思考：这个任务要分几步？先做什么？
         ↓
   ┌───────────┐
   │  📋 规划   │  ← Planning：把大任务拆成小步骤
   │ Planning  │
   └─────┬─────┘
         │ 执行每一步
         ↓
   ┌───────────┐
   │  🔧 工具   │  ← Tools：搜索、计算、读写文件、调 API
   │  Tools    │
   └─────┬─────┘
         │ 记录执行结果
         ↓
   ┌───────────┐
   │  💾 记忆   │  ← Memory：上下文、历史任务、用户偏好
   │  Memory   │
   └─────┬─────┘
         ↓
      返回最终结果
```

### 四个核心模块的通俗解释

| 模块 | 类比 | 作用 |
| --- | --- | --- |
| LLM（大脑） | 员工的思维能力 | 理解需求、推理分析、生成决策 |
| Planning（规划） | 员工的工作计划 | 把复杂任务拆成可执行步骤 |
| Tools（工具） | 员工的办公软件与系统权限 | 搜索、查库、发请求、执行动作 |
| Memory（记忆） | 员工笔记本 | 保存上下文、历史结果、用户偏好 |

---

## 1.3 典型 Agent 产品拆解

### 案例一：Manus（通用任务 Agent）

目标：“帮我分析某行业市场数据并出报告”

1. 理解需求（LLM）
2. 拆解子任务：搜集数据 -> 清洗 -> 分析 -> 生成图表 -> 写报告（Planning）
3. 调用搜索引擎、分析工具、图表工具（Tools）
4. 记录中间结果并组装终稿（Memory）

### 案例二：Cursor / GitHub Copilot（代码 Agent）

目标：“帮我写一个用户登录功能”

1. 理解需求：前端表单 + 后端 API + 数据库校验
2. 规划步骤：模型 -> 接口 -> 页面 -> 测试
3. 调用工具：读取项目上下文、写代码、运行测试
4. 记住项目结构与编码风格

### 案例三：电商客服 Agent

目标：“我要退货”

1. 理解意图：退货
2. 规划流程：查订单 -> 校验条件 -> 生成退货单 -> 通知物流
3. 调用订单系统、退货接口、通知服务
4. 记录处理状态与用户历史

---

## 1.4 Agent 技术栈全景

```text
基础层    Python + HTTP/API 基础
模型层    OpenAI API / 兼容接口
框架层    LangChain -> LangGraph
能力层    Prompt / Tools / RAG / Memory
协议层    MCP（Model Context Protocol）
工程层    FastAPI + 评测 + 部署 + 监控
```

本讲我们重点完成基础层与模型层的最小闭环，顺带理解能力层中的“最小记忆”。

---

## 1.5 实操：搭建开发环境与第一个 LLM API 调用

讲义原文使用 `venv`，课程仓库使用 `conda`。两者都可行，这里给出仓库推荐路径。

### Step 0：启用代理并激活环境（推荐）

```bash
source <course-root>/use_proxy.sh
source <conda-root>/etc/profile.d/conda.sh
conda activate agent_course
```

### Step 1：安装核心依赖

```bash
cd <course-root>
python -m pip install openai langchain langchain-openai python-dotenv
```

### Step 2：配置 API Key

在项目根目录准备 `.env`：

```env
OPENAI_API_KEY=<your-api-key>
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_MODEL=gpt-5.4
```

如果你用兼容接口（豆包、DeepSeek 等），替换 `OPENAI_BASE_URL` 与 `OPENAI_API_KEY` 即可。

### Step 3：第一个 API 调用

运行示例：

```bash
cd <course-root>/lessons/L01_agent_basics
python practice/01_hello_llm.py
```

示例脚本：`practice/01_hello_llm.py`
目标：让模型“一句话解释什么是 AI Agent”。

### Step 4：实现多轮对话（最小记忆）

运行示例：

```bash
cd <course-root>/lessons/L01_agent_basics
python practice/02_multi_turn_chat.py
```

测试建议：

1. 先告诉它你的名字。
2. 连续聊 3-5 轮。
3. 再问“我叫什么名字？”。

它能记住，是因为每轮对话都在 `messages` 里持续累积并再次发送给模型，这就是最小可用记忆。

### Step 5（本仓库额外演示）：ChatBot vs Agent 对比

```bash
python practice/demo_chatbot_vs_agent.py --mode both
```

这个示例会展示：

- ChatBot 模式：直接文本回答
- Agent 模式：Observe -> Think -> Act -> Reflect，并输出循环日志

---

## 1.6 课后作业

### 必做

1. 运行 `practice/02_multi_turn_chat.py`，连续对话 5 轮以上，观察上下文记忆表现。
2. 修改 system prompt，让 AI 分别扮演：
   - Python 教师
   - 健身教练
3. 对比不同角色下的回答风格差异（语气、结构、建议类型）。

### 选做

思考一个你工作中可以交给 Agent 的任务，并写出：

1. 目标是什么
2. 需要哪些工具
3. 执行步骤如何拆解
4. 哪一步最可能失败，以及你的护栏策略

---

## 课后复盘模板（简版）

1. 我最清晰的收获：
2. 我最困惑的问题：
3. 我想先做的一个 Agent 小项目：
4. 我要先实现的一个工具调用：

---

## 附：常见问题（FAQ）

### Q1：我必须用 `venv` 吗？

不是。`venv` 与 `conda` 都可以，只要依赖隔离干净即可。本仓库默认使用 `conda`。

### Q2：为什么 API 能偶发超时？

常见原因是网络代理链路抖动。本仓库脚本已加入重试与超时参数，稳定性更高。

### Q3：为什么要先学 ChatBot 再学 Agent？

因为 Agent 本质是在 ChatBot 基础上，加入了“任务执行能力、工具能力和记忆能力”。先掌握一问一答，再进入自动执行，会更稳。

---

## 一键检查命令

```bash
source <course-root>/use_proxy.sh
bash <course-root>/lessons/L01_agent_basics/practice/preclass_run.sh
```

通过标志：最后看到 `[OK] L01 preclass run completed.`
