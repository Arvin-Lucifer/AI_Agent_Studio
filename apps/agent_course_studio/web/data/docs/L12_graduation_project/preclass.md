# L12 课前准备清单

## 环境检查

- [ ] 已激活 `agent_course` conda 环境。
- [ ] 已安装课程依赖：`core.txt`、`langchain.txt`、`deployment.txt`。
- [ ] 能运行 `python --version`，版本为 Python 3.11+。
- [ ] 能运行 `python -c "import fastapi, langgraph, pydantic, pytest"`。

## 文档阅读

- [ ] 阅读 `resources/project_packet/01_ASSIGNMENT_REQUIREMENTS.md`。
- [ ] 阅读 `resources/project_packet/02_HARNESS_ENGINEERING_GUIDE.md`。
- [ ] 阅读 `resources/project_packet/PRACTICE_REFERENCE_EXTRACT.md`。
- [ ] 阅读 `reference_implementation/intelligent_customer_agent/README.md`。
- [ ] 阅读参考实现的 `docs/PRD.md`、`docs/TRD.md`、`docs/TDD.md`、`docs/HARNESS.md`。

## 运行准备

- [ ] 确认参考实现没有 `.env`；如需在线 LLM，先从 `.env.example` 复制并填写自己的本地 `.env`。
- [ ] 知道默认离线路径不需要 API Key，也可以完成测试和评测。
- [ ] 运行 `bash practice/preclass_run.sh`。
- [ ] 记录测试和评测输出。

## 上课前应能回答

1. 为什么本项目选择智能客服 Agent？
2. 最低验收标准有哪些？
3. Harness 和 Prompt Engineering 的区别是什么？
4. 为什么投诉必须走工单？
5. 为什么评测器不能让主 Agent 自评？
