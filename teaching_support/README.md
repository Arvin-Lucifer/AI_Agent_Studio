# 教辅资料

本目录作为课程教辅资料入口，不重复搬运已有文件，统一索引课程规范、环境说明、运行脚本和共享资源。

## 课程组织规范

- [章节目录规范](../LESSON_STRUCTURE_GUIDE.md)
- [代码注释规范](../CODE_COMMENTING_GUIDE.md)
- [课程总览 README](../README.md)

## 环境与依赖

- [依赖管理说明](../requirements/README.md)
- [核心依赖](../requirements/core.txt)
- [LangChain 依赖](../requirements/langchain.txt)
- [RAG 依赖](../requirements/rag.txt)
- [MCP 依赖](../requirements/mcp.txt)
- [部署依赖](../requirements/deployment.txt)

## 运行脚本

- [激活课程环境](../scripts/activate_course.sh)
- [环境检查](../scripts/check_env.py)
- [OpenAI 连通性检查](../scripts/smoke_openai.py)
- [按模块安装依赖](../scripts/install_module_requirements.sh)

## 共享资源

- `../shared/data/`：跨章节可复用数据。
- `../shared/notebooks/`：实验笔记和快速验证。
- `../shared/utils/`：跨章节通用辅助函数。

## 教辅专题

- [BM25 和倒排索引简单介绍](./BM25_INVERTED_INDEX.md)：用通俗案例解释关键词检索、TF-IDF、BM25、倒排索引，以及它们和 RAG Hybrid Search 的关系。
- [Agent 设计模式](./AGENT_DESIGN_PATTERNS.md)：系统讲解 ReAct、Plan-and-Execute、Reflection、Multi-Agent 四种经典模式及其适用场景、局限和调试方法。
- [常见设计模式：工厂、发布订阅、装饰器、桥接](./COMMON_DESIGN_PATTERNS.md)：整理四种通用工程设计模式，并说明它们在 Agent 工程中的对应应用。
- [AI Native 的工作方式](./AI_NATIVE_WORKFLOW.md)：总结 AI-native 团队如何围绕 agent、context、loop、skill 和验收机制重构组织工作方式。
- [外部学习资源索引：你能够额外获取到什么？](./EXTERNAL_LEARNING_RESOURCES.md)：汇总 hello-agents、真实产品 System Prompt、Few-Shot/CoT、Claude.md 和 AI-native 工作方式等延伸阅读。

## 使用原则

- 教辅资料服务于课程整体，不替代每章自己的 README。
- 每章新增依赖必须进入 `requirements/`，不要散落在单章目录。
- 每章完成后都要跑对应 `practice/preclass_run.sh`，并清理缓存。
