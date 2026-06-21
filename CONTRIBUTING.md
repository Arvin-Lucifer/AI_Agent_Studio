# Contributing

感谢你改进 Agent Course 2026。这个仓库同时是课程内容、代码实践和公开展示产品，所以提交前需要同时关注内容质量、运行质量和安全边界。

## Content Principles

- 课程内容优先来自老师讲义和已整理材料。
- 合理补充必须服务于教学目标，不能把补充内容伪装成老师原文。
- 每章保持稳定结构：`README.md`、`lecture/`、`materials/`、`practice/`、可选 `resources/` 和 `data/`。
- 实战代码要有必要注释，尤其是 Agent 循环、工具调用、RAG、Memory、Skill、评测和部署相关模块。

## Development Workflow

```bash
python3 apps/agent_course_studio/build_course_data.py
python3 scripts/build_public_site.py
python3 scripts/validate_project.py
node --check apps/agent_course_studio/web/app.js
python3 -m py_compile apps/agent_course_studio/build_course_data.py apps/agent_course_studio/server.py scripts/build_public_site.py scripts/validate_project.py
git diff --check
```

## What To Avoid

- 不提交 `.env`、真实 API key、代理脚本、生成索引或运行态缓存。
- 不把个人绝对路径写进公开文档。
- 不在网页 runner 中开放任意命令执行。
- 不做与当前章节无关的大规模重构。

## Pull Request Checklist

- 课程索引已重新生成。
- 公开站点已重新生成。
- 新增或修改的代码有必要教学注释。
- README、Studio 和课程目录口径一致。
- 本地验证脚本通过。
