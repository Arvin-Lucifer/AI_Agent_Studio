# 课程章节对齐审视记录

审视日期：2026-06-18

本记录用于对照老师目录，检查当前课程目录命名、主题覆盖和整理状态。原则是：不降低老师原始讲义规模，不为了省工作量缩减章节内容；已经收到老师讲义的章节，需要按讲义主线完整整理，未收到讲义的章节只做主题占位，不冒充已完成。

## 章节主题对齐表

| 老师目录主题 | 当前目录 | 状态 | 本次处理 |
| --- | --- | --- | --- |
| 第1讲：Agent 全景认知 | `lessons/L01_agent_basics` | 已完整整理 | 保持 |
| 第2讲 prompt | `lessons/L02_prompt_engineering` | 已完整整理 | 保持 |
| 第3讲 function calling | `lessons/L03_function_calling` | 已完整整理 | 保持 |
| 第4讲：LangChain 快速上手 | `lessons/L04_langchain_quickstart` | 已完整整理 | 保持 |
| 第5讲 RAG | `lessons/L05_rag` | 已完整整理 | 保持 |
| 第6讲：LangChain 深入实战 | `lessons/L06_langchain_advanced` | 已完整整理 | 目录名可接受，主题已对齐 |
| 第7讲记忆系统 | `lessons/L07_memory_systems` | 已完整整理 | 保持 |
| 第8讲 Agent 模式 | `lessons/L08_agent_modes` | 已完整整理 | 从 `L08_multi_agent` 改名 |
| 第9讲 MCP | `lessons/L09_mcp_tooling` | 已完整整理 | 保持 |
| 第10讲 skill 相关 | `lessons/L10_skills` | 已完整整理 | 从 `L10_eval_and_tuning` 改名；已整理 Skill 主讲义、面试题和全部补充专题 |
| 第11讲评测和部署 | `lessons/L11_eval_and_deployment` | 已完整整理 | 已整理 Agent 评估与调优、FastAPI 部署、流式输出、前端接入、成本监控和安全防护 |
| 第12讲 毕业项目实战 | `lessons/L12_graduation_project` | 已完整整理 | 已归档老师任务包和智能客服 Agent 参考实现 |
| 教辅资料 | `teaching_support/` | 已建立入口 | 新增教辅索引 |

## 当前完整性判断

- L01-L09：已按标准章节结构整理，包含 README、lecture、materials、practice，并根据需要补充 resources/data。
- L10：已根据当前收到的第 10 讲 Skill 主讲义、面试题和全部补充专题整理完成。
- L11：已根据当前收到的评测与部署材料整理完成。
- L12：已根据老师任务包和已完成参考实现整理为毕业项目实战章节。
- 教辅资料：新增 `teaching_support/`，集中索引课程规范、依赖、脚本和共享资源。

## 2026-06-18 总复核结果

本次复核范围覆盖 L01-L10，重点检查章节主题、目录骨架、讲义/摘要/材料/代码同步、面试题归档、依赖环境和运行脚本。

结论：

- L01-L10 的章节主题已与老师目录对齐。
- L01-L10 均具备 `README.md`、`lecture/LECTURE_FULL.md`、`lecture/CHAPTER_SUMMARY.md`、`materials/PRECLASS_CHECKLIST.md`、`materials/NOTES_TEMPLATE.md`、`materials/MINI_QUIZ.md`、`materials/EXTENSIONS.md` 和 `practice/preclass_run.sh`。
- L02-L10 中老师提供或课程需要的面试内容，已统一收拢到 `materials/INTERVIEW_QA.md`；其中部分章节包含工程化补充，文件内已写明来源边界。
- L10 已从“第一批材料”状态更新为“当前收到的完整第 10 讲材料已整理完成”，并同步了 README、完整讲义、资源专题、实操代码、面试题、预习清单、小测和扩展练习。
- L11 已在后续整理中补齐；当前仅 L12 保持主题占位，不冒充已完成讲义。

已执行检查：

- `python -m py_compile` 覆盖 L01-L10 所有 `practice/*.py`。
- `bash -n` 覆盖 L01-L10 所有 `practice/preclass_run.sh` 和公共 shell 脚本。
- Markdown 本地链接检查通过。
- `pip check` 通过。
- L01-L10 的 `practice/preclass_run.sh` 已按章节顺序跑通。

非阻塞提醒：

- L04、L08、L09 运行时出现 LangChain/LangGraph 的 pending deprecation warning，当前不影响课程示例运行；后续升级依赖时可按 warning 提示显式设置 `allowed_objects`。

## 2026-06-18 L11 整理与验证

本次新增整理第 11 讲“评测和部署”，将老师提供的 Agent 评估与调优材料、FastAPI 部署材料统一归入 `lessons/L11_eval_and_deployment`。

已补齐：

- `README.md`
- `lecture/LECTURE_FULL.md`
- `lecture/CHAPTER_SUMMARY.md`
- `materials/PRECLASS_CHECKLIST.md`
- `materials/NOTES_TEMPLATE.md`
- `materials/MINI_QUIZ.md`
- `materials/EXTENSIONS.md`
- `materials/INTERVIEW_QA.md`
- `resources/` 下评估体系、调优手册、部署 runbook、流式前端、成本安全专题
- `practice/` 下评测集、评测器、FastAPI API、SSE 流式 API、成本监控、安全防护和前端页面

已执行检查：

- `python -m py_compile lessons/L11_eval_and_deployment/practice/*.py`
- `bash -n lessons/L11_eval_and_deployment/practice/preclass_run.sh`
- `bash lessons/L11_eval_and_deployment/practice/preclass_run.sh`
- Markdown 本地链接检查通过。
- `pip check` 通过。
- `47_agent_api` 和 `48_agent_api_streaming` 可被 importlib 加载，满足 README 中的 Uvicorn 启动方式。

依赖更新：

- `requirements/deployment.txt` 增加 `sse-starlette`，用于 SSE 流式 API。

## 2026-06-18 L01-L11 二次总审计

本次复核范围覆盖 L01-L11，重点回答“当前收到的课程内容是否覆盖完整，作业和拓展是否同步到位”。

结论：

- L01-L11 均已按标准章节结构整理完成。
- 每章均包含 README、完整讲义、章节总结、课前清单、课堂笔记模板、小测、拓展练习和一键运行脚本。
- L02-L11 已根据老师材料和课程需要整理面试题；L01 当前没有单独面试题文件，但讲义、总结、小测和拓展练习齐备。
- L01-L11 的讲义中均包含课堂作业、课后作业或本章作业入口。
- L01-L11 的 `materials/EXTENSIONS.md` 均非空，已覆盖必做、选做或进阶拓展任务。
- L12 已在后续整理中补齐；当前 L01-L12 均已具备完整课程入口。

已执行检查：

- L01-L11 必备文件检查通过。
- `python -m py_compile` 覆盖 L01-L11 所有 `practice/*.py`。
- `bash -n` 覆盖 L01-L11 所有 `practice/preclass_run.sh` 和公共 shell 脚本。
- Markdown 本地链接检查通过。
- `pip check` 通过。
- L01-L11 的 `practice/preclass_run.sh` 已按章节顺序跑通。

非阻塞提醒：

- L04、L08、L09 仍会出现 LangChain/LangGraph 的 pending deprecation warning，当前不影响运行。该问题属于依赖未来兼容和反序列化安全默认值提醒，可在后续做“输出洁净版”时统一处理。

## 2026-06-18 L12 毕业项目归档与验证

本次将外部毕业项目任务包和智能客服参考实现归并到 `lessons/L12_graduation_project`。

已补齐：

- `README.md`
- `lecture/LECTURE_FULL.md`
- `lecture/CHAPTER_SUMMARY.md`
- `materials/PRECLASS_CHECKLIST.md`
- `materials/NOTES_TEMPLATE.md`
- `materials/MINI_QUIZ.md`
- `materials/EXTENSIONS.md`
- `materials/INTERVIEW_QA.md`
- `resources/project_packet/`：老师任务包、Harness 指南、Codex 任务书、启动 Prompt、Word 原件和 Markdown 摘录
- `resources/PROJECT_INTEGRATION_REVIEW.md`：来源审阅、保留/排除策略和课程归档说明
- `reference_implementation/intelligent_customer_agent/`：智能客服 Agent 参考实现
- `practice/preclass_run.sh`：调用参考实现完成知识库构建、编译、测试和评测

归档时已排除：

- `.env`
- `.venv/`
- `__pycache__/`
- `.pytest_cache/`
- 历史运行日志
- 历史 memory/tickets/knowledge gaps
- 锁文件和生成索引

已执行检查：

- `bash -n lessons/L12_graduation_project/practice/preclass_run.sh`
- `bash lessons/L12_graduation_project/practice/preclass_run.sh`
- 参考实现知识库构建通过：10 documents
- 参考实现测试通过：63 passed
- 参考实现评测通过：32 cases，`overall_score = 1.0`

非阻塞提醒：

- L12 参考实现运行时也会出现 LangGraph 的 `allowed_objects` pending deprecation warning，和 L04/L08/L09 同源，不影响当前课程运行。

## 2026-06-18 Git 前全课程审核

本次在准备提交到 GitHub 前，对课程目录做了一次全量审核。

来源归档：

- 已将外部毕业项目任务包迁移为 `lessons/L12_graduation_project/resources/project_packet/`。
- 已将智能客服参考实现迁移为 `lessons/L12_graduation_project/reference_implementation/intelligent_customer_agent/`。
- 课程主目录只保留整理后的 L12 任务包和干净参考实现。

已执行检查：

- L01-L12 必备文件检查通过。
- Markdown 本地链接检查通过：188 个 Markdown 文件。
- Shell 脚本语法检查通过。
- Python 编译检查通过：120 个 Python 文件。
- `pip check` 通过。
- L01-L12 的 `practice/preclass_run.sh` 全部跑通。
- L12 参考实现测试通过：63 passed。
- L12 参考实现评测通过：32 cases，`overall_score = 1.0`。
- 敏感信息扫描通过：未发现非占位符密钥；本地 `.env` 已由 `.gitignore` 排除。

清理与 Git 准备：

- 已清理 `__pycache__`、`.pytest_cache`、`*.pyc`、`*.lock`。
- 已清理 L12 参考实现运行态：memory、tickets、knowledge gaps、logs、生成索引和 generated eval cases。
- 已补充 `.gitignore`，排除课程运行生成物和 L12 参考实现运行态。

## 后续补强原则

- 新章节必须先读完老师讲义，再按课程标准结构补齐，不提前臆造完整内容。
- 有面试题的章节，题库需要基于老师材料整理，并明确哪些是结构化补充。
- 代码示例必须有导读型注释，关键模块要解释清楚设计目的和工程边界。
- 依赖统一进入 `requirements/` 并安装到 `agent_course` conda 环境。
- 每章完成后必须验证 `practice/preclass_run.sh`、Python 编译和 Markdown 本地链接。
