# L12 章节总结：毕业项目实战

## 一句话目标

实现一个基于 LangGraph + RAG + FastAPI + Harness 的智能客服 Agent，证明它可运行、可测试、可评测、可部署、可观测、可答辩。

## 核心闭环

```text
需求 -> PRD/TRD/TDD -> Harness -> 实现 -> 测试 -> 评测 -> 部署 -> 监控 -> 复盘
```

## 必须掌握

- 智能客服 Agent 的最低验收：RAG、LangGraph、FastAPI、评测集、评测脚本。
- Harness 思维：状态、工具边界、上下文、验证、机械约束和可观测性。
- LangGraph 流程：加载记忆、意图分类、路由、检索、回答、评估、澄清、工单、转人工。
- RAG 安全边界：有证据才答，无证据转人工或澄清。
- 评测方式：独立评测器，不让主 Agent 自评。
- 答辩表达：讲设计取舍，不只罗列技术名词。

## 参考实现亮点

- 10 份 Markdown 知识库。
- 分库检索和口语化 query normalization。
- 投诉工单、工单状态查询、多轮工单补充。
- 反馈、知识缺口、知识库运营闭环。
- 前端客服台和 Dashboard。
- Docker、Admin Key、限流、PII 脱敏、本地文件锁。
- `pytest` + `evals/run_eval.py` + Dashboard Quality Gate。

## 检查命令

```bash
cd <course-root>/lessons/L12_graduation_project
bash practice/preclass_run.sh

cd reference_implementation/intelligent_customer_agent
bash scripts/run_api.sh
```

## 答辩三句话

1. 我不是做了一个单轮 RAG，而是用 LangGraph 把客服流程建模成可观测、可评测的状态机。
2. 系统用 Harness 约束关键风险：投诉必工单、无证据不编造、低置信度转人工。
3. 项目通过测试、评测、日志、Dashboard 和 Docker 部署证明它具备工程闭环。

