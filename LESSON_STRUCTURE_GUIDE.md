# 课程章节目录规范

为了让学生第一次打开章节目录时不迷路，每一讲优先使用少量、稳定、语义清晰的目录。不要因为单个文件新建一个同级子目录。

## 标准结构

```text
lessons/Lxx_topic/
├── README.md
├── lecture/
│   ├── LECTURE_FULL.md
│   └── CHAPTER_SUMMARY.md
├── materials/
│   ├── PRECLASS_CHECKLIST.md
│   ├── NOTES_TEMPLATE.md
│   ├── MINI_QUIZ.md
│   ├── EXTENSIONS.md
│   └── INTERVIEW_QA.md  # 可选：本章面试题速查
├── practice/
│   ├── *.py
│   └── preclass_run.sh
├── resources/      # 可选：专题参考、图解、工程模式、长篇说明
└── data/           # 可选：示例数据、生成索引、可删除的本地运行产物
```

## 目录职责

| 目录 | 放什么 | 不放什么 |
| --- | --- | --- |
| `lecture/` | 完整讲义、章节总结 | 练习代码、运行产物 |
| `materials/` | 课前清单、课堂笔记模板、课后小测、拓展练习、面试题速查 | 大篇幅专题参考 |
| `practice/` | 可运行代码、一键运行脚本、示例入口 | 长篇讲义、面试题 |
| `resources/` | 架构图说明、专题文章、工程清单、长篇参考资料 | 临时运行数据、面试速查 |
| `data/` | 示例知识库、索引、可再生成文件 | 需要长期阅读的课程正文 |

## 新增文件判断

1. 如果文件服务于课堂讲解，优先放 `lecture/`。
2. 如果文件服务于学习流程、作业、小测、笔记，优先放 `materials/`。
3. 如果文件能被 `python` 或 `bash` 直接运行，优先放 `practice/`。
4. 如果文件是面试速查、复习问答、回答模板，放 `materials/INTERVIEW_QA.md`。
5. 如果文件是补充阅读、工程专题、图表说明、长篇参考资料，放 `resources/`。
6. 如果文件是脚本生成的样例数据或索引，放 `data/`。
7. 只有当某类文件稳定增长到 3 个以上，并且学生需要单独理解它们时，才考虑新增目录。

## README 写法

每章 `README.md` 保持三件事：

1. 本章学什么。
2. 先看什么、再跑什么。
3. 每个目录/关键文件的用途。

不要把 README 写成文件清单的复制品。文件清单可以有，但重点应该是学习路线。

## 脚本约定

- 每章的一键检查脚本统一命名为 `practice/preclass_run.sh`。
- 脚本从课程根目录和章节目录运行都应尽量稳定。
- 生成文件默认进入本章 `data/`，避免污染讲义和代码目录。

## 环境约定

- 所有课程依赖统一安装在 `agent_course` conda 环境中。
- 新增依赖必须先归类到 `requirements/` 下的对应文件，例如 `core.txt`、`langchain.txt`、`rag.txt`、`mcp.txt` 或 `deployment.txt`。
- 不在单章目录里散落 `requirements.txt`、临时安装脚本或环境说明。
- 每章 `materials/PRECLASS_CHECKLIST.md` 只写本章需要确认的依赖，不重新发明环境安装流程。
- 可选依赖要明确标注“可选”，并说明默认示例是否依赖它。默认课堂主线应尽量可稳定运行。

## 单章完成标准

每一章整理完成后，必须至少完成以下检查，再进入下一章：

1. 目录符合标准结构：`lecture/`、`materials/`、`practice/`，按需使用 `resources/` 和 `data/`。
2. README、完整讲义、章节总结、课前清单、笔记模板、小测、拓展练习已补齐。
3. 如有面试内容，统一整理到 `materials/INTERVIEW_QA.md`，并标注来源边界。
4. 练习代码包含导读型注释，关键模块能讲清“为什么这样写”。
5. 新增依赖已整理到 `requirements/`，并在 `agent_course` conda 环境中验证。
6. 运行 `python -m py_compile practice/*.py`。
7. 运行 `bash -n practice/preclass_run.sh`。
8. 至少跑通本章核心示例或完整 `practice/preclass_run.sh`。
9. 检查 Markdown 本地链接。
10. 清理 `__pycache__` 等缓存产物。

## 后续章节约定

L07-L12 继续按这个结构补齐。除非某一章确实需要 Web 应用、服务端部署或大型项目结构，否则不要恢复 `prep/`、`notes/`、`assessment/`、`extensions/`、`scripts/` 这些分散目录。
