# L11 评测和部署：从 Demo 能跑到生产可用

本章把 Agent 从“本地能跑”推进到“可评估、可调优、可服务化、可观测”。前半部分讲评测与调优，后半部分讲 FastAPI 部署、流式输出、前端接入、成本监控和安全防护。

> 说明：老师材料中“Agent 评估与调优”标题写作第 10 讲；在当前课程总目录中，第 10 讲已用于 Skill 相关内容，因此这里按你提供的要求归入 L11“评测和部署”。

## 本章学习目标

- 理解为什么 Agent 不能只靠“问几个问题感觉不错”就上线。
- 掌握准确性、完整性、相关性、安全性、效率成本和鲁棒性六类评估维度。
- 能构建覆盖事实问答、闲聊、边界输入、Prompt 注入和完整性问题的评测数据集。
- 能运行自动化评测，并检查关键词、工具调用、安全红线和分类得分。
- 能识别幻觉、死循环、工具误调、格式错乱、Prompt 注入等常见翻车场景。
- 能用 FastAPI 将 Agent 封装成 REST API，并提供健康检查。
- 能用 SSE 实现流式输出，并用 HTML 页面接入。
- 能理解 Gunicorn、Nginx、SSE 代理配置、成本监控和输入安全防护。

## 文件分区

| 分类 | 路径 | 用途 |
| --- | --- | --- |
| 讲义 | [lecture/LECTURE_FULL.md](./lecture/LECTURE_FULL.md) | 第 11 讲完整讲义：评测、调优、API、流式和部署 |
| 总结 | [lecture/CHAPTER_SUMMARY.md](./lecture/CHAPTER_SUMMARY.md) | 核心概念、代码地图和上线检查 |
| 实操代码 | [practice/](./practice/) | 评测集、评测器、FastAPI、SSE、成本、安全示例 |
| 前端页面 | [practice/chat_frontend.html](./practice/chat_frontend.html) | 调用流式 API 的最小 HTML 页面 |
| 一键脚本 | [practice/preclass_run.sh](./practice/preclass_run.sh) | 自动执行 L11 本地检查和核心示例 |
| 课前准备 | [materials/PRECLASS_CHECKLIST.md](./materials/PRECLASS_CHECKLIST.md) | 环境、概念和代码预习 |
| 课堂笔记 | [materials/NOTES_TEMPLATE.md](./materials/NOTES_TEMPLATE.md) | 记录评测指标、调优策略和部署方案 |
| 课后小测 | [materials/MINI_QUIZ.md](./materials/MINI_QUIZ.md) | 检查评测与部署核心概念 |
| 拓展练习 | [materials/EXTENSIONS.md](./materials/EXTENSIONS.md) | 真实 RAG API、CI 评测、流式前端和监控扩展 |
| 面试题库 | [materials/INTERVIEW_QA.md](./materials/INTERVIEW_QA.md) | Agent 评估、调优、部署、安全和成本面试题 |
| 工程参考 | [resources/](./resources/) | 评估体系、调优手册、部署 runbook、流式前端、成本安全 |
| 运行数据 | [data/](./data/) | 评测数据集、评测结果和成本摘要 |

## 推荐学习路径

1. 阅读 [lecture/LECTURE_FULL.md](./lecture/LECTURE_FULL.md) 的 11.1-11.4，理解 Agent 评估为什么比传统单元测试更复杂。
2. 运行 `practice/44_eval_dataset.py`，查看评测集如何覆盖事实、闲聊、边界、安全和完整性。
3. 运行 `practice/45_eval_runner.py`，观察关键词、工具调用和安全检查如何组合成评测结果。
4. 阅读 [resources/EVALUATION_SYSTEM_DESIGN.md](./resources/EVALUATION_SYSTEM_DESIGN.md)，理解为什么关键词匹配只是 baseline。
5. 运行 `practice/46_failure_tuning_playbook.py`，复盘常见翻车场景和修复策略。
6. 运行 `practice/47_agent_api.py --self-test`，理解 Agent 如何封装成 REST API。
7. 运行 `practice/48_agent_api_streaming.py --self-test`，理解 SSE 事件流。
8. 阅读 [resources/FASTAPI_DEPLOYMENT_RUNBOOK.md](./resources/FASTAPI_DEPLOYMENT_RUNBOOK.md)，理解本地、Gunicorn 和 Nginx 部署路径。
9. 运行 `practice/49_cost_monitor.py` 和 `practice/50_safety_guardrails.py`，理解成本和安全不是上线后的附加题。
10. 阅读 [教辅资料：AI Native 的工作方式](../../teaching_support/AI_NATIVE_WORKFLOW.md)，理解评测、部署和验收机制在组织级 AI 闭环中的位置。
11. 阅读 [materials/INTERVIEW_QA.md](./materials/INTERVIEW_QA.md)，准备评测与部署面试题。

## 快速运行

```bash
source <course-root>/scripts/activate_course.sh
cd <course-root>/lessons/L11_eval_and_deployment
```

一键预习检查：

```bash
bash practice/preclass_run.sh
```

单独运行评测：

```bash
python practice/44_eval_dataset.py
python practice/45_eval_runner.py
```

测试同步 API：

```bash
python practice/47_agent_api.py --self-test
```

启动同步 API 服务：

```bash
cd practice
uvicorn 47_agent_api:app --host 0.0.0.0 --port 8000 --reload
```

启动流式 API 服务：

```bash
cd practice
uvicorn 48_agent_api_streaming:app --host 0.0.0.0 --port 8000
```

打开前端页面：

```bash
cd practice
python -m http.server 8001
```

然后访问 `http://localhost:8001/chat_frontend.html`。

## 本章交付物

- 一份 Agent 评测数据集。
- 一份自动化评测报告 JSON。
- 一张“翻车场景 -> 诊断 -> 修复”的调优表。
- 一个 FastAPI `/chat` 接口。
- 一个 SSE `/chat/stream` 接口。
- 一个可接入流式 API 的 HTML 页面。
- 一份成本监控摘要。
- 一份部署前安全检查清单。

## 与后续章节的关系

L11 让 Agent 从课程示例进入工程闭环：评测发现问题，调优修复问题，部署让多人访问，监控让系统可持续运行。L12 会把前面所有模块组合成毕业项目实战，并要求同时交付代码、评测结果、部署说明和项目复盘。
