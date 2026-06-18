# 智能体开发课程工作区（2026）

这是本课程的统一实践目录，覆盖从基础认知到工程部署的完整学习路径。

## 目录结构

- `lessons/`：每一讲对应一个目录
- `shared/data/`：可复用数据与资料
- `shared/notebooks/`：实验笔记与快速验证
- `shared/utils/`：通用辅助脚本
- `teaching_support/`：教辅资料入口，索引课程规范、依赖和运行脚本
- `requirements/`：按主题拆分的依赖文件
- `scripts/`：环境初始化与健康检查脚本
- `COURSE_ALIGNMENT_REVIEW.md`：章节主题与老师目录对齐记录
- `LESSON_STRUCTURE_GUIDE.md`：每一讲的目录组织规范
- `CODE_COMMENTING_GUIDE.md`：课程代码注释与讲解规范

## 每讲目录约定

每一讲优先保持少量稳定入口：

- `lecture/`：完整讲义和章节总结
- `materials/`：课前清单、笔记模板、小测、拓展练习、面试速查
- `practice/`：可运行代码和本章一键脚本
- `resources/`：专题参考资料，可选
- `data/`：示例数据或生成索引，可选

详细规则见 `LESSON_STRUCTURE_GUIDE.md`。

## 快速开始

所有课程依赖统一安装在 `agent_course` conda 环境中。不要在系统 Python、其他项目环境或临时虚拟环境里安装本课程依赖。
文档中的 `<course-root>` 指你 clone 后的本仓库根目录，`<conda-root>` 指本机 Miniconda/Anaconda 安装目录。

1. 激活课程环境

```bash
source <conda-root>/etc/profile.d/conda.sh
conda activate agent_course
```

2. 安装核心依赖

```bash
pip install -r requirements/core.txt
```

3. 按课程进度安装扩展依赖

```bash
pip install -r requirements/langchain.txt
pip install -r requirements/rag.txt
pip install -r requirements/mcp.txt
pip install -r requirements/deployment.txt
```

4. 准备环境变量

```bash
cp .env.example .env
# 然后填写你自己的密钥配置
```

5. 运行本地检查

```bash
python scripts/check_env.py
python scripts/smoke_openai.py
```

## 建议学习节奏

- 第 1-3 讲：基础认知、提示工程、函数调用
- 第 4-6 讲：框架上手、检索增强、深入编排
- 第 7-9 讲：记忆系统、Agent 模式、MCP 工具接入协议
- 第 10-12 讲：Skill 相关、评测和部署、毕业项目实战

## 使用约定

- 密钥只放在 `.env` 中
- 本目录与其他项目隔离，避免依赖冲突
- 环境相关内容统一整理到 `requirements/`、`scripts/` 和 `agent_course` conda 环境中
- 每章必须完成材料、代码、依赖、运行验证和缓存清理后，再推进下一章
- 每讲练习代码都应包含必要教学注释，关键模块遵循 `CODE_COMMENTING_GUIDE.md`
