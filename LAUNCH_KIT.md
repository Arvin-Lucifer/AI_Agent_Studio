# Launch Kit

这份文档用于把 AgentCraft Studio 2026 从“已经整理好的仓库”推到“别人愿意点开、看懂、收藏、运行”的状态。

## 1. GitHub About 建议

在 GitHub 仓库右侧 `About` 区域填写：

```text
AI Agent development forge with 12 lessons, an interactive Studio, and an intelligent customer Agent showcase.
```

Website:

```text
https://arvin-lucifer.github.io/agent_course_2026/
```

Topics 建议：

```text
ai-agent
agent
prompt-engineering
function-calling
langchain
langgraph
rag
mcp
skills
evaluation
ai-education
python
```

## 2. 三个公开入口

| 入口 | 用途 |
| --- | --- |
| `https://arvin-lucifer.github.io/agent_course_2026/` | 对外首页，适合放在 GitHub About、简历和社交平台 |
| `https://arvin-lucifer.github.io/agent_course_2026/studio/` | 静态 Studio，适合让别人快速浏览课程内容 |
| `https://arvin-lucifer.github.io/agent_course_2026/showcase/` | L12 项目展示页，适合面试、答辩和作品集 |

## 3. 一句话介绍

```text
AgentCraft Studio 2026 是一个 AI Agent 开发实战工作台：12 章系统路径、交互式 Studio、面试题库、代码实践和一个端到端智能客服 Agent 毕业项目。
```

更短版本：

```text
把 AI Agent 知识练成可运行、可评测、可展示的工程作品。
```

## 4. 1 分钟 Demo 脚本

0-10 秒：

```text
这是 AgentCraft Studio 2026，一个面向 AI Agent 开发的实战工作台，不只是资料合集，而是从学习、练习、面试到毕业项目的一条完整路径。
```

10-25 秒：

```text
首页先展示 12 章路线：Prompt、Function Calling、LangChain、RAG、Memory、MCP、Skill、评测部署，最后收束到智能客服 Agent。
```

25-40 秒：

```text
进入 Studio 后，可以按章节看讲义、实战代码、小测挑战、面试题和资源，还能用本地课程助手按引用检索内容。
```

40-55 秒：

```text
最后看 L12 Showcase：这里展示了智能客服 Agent 的运行链路、LangGraph 状态机、RAG 证据引用、工单兜底和评测回归。
```

55-60 秒：

```text
所以它既能自学，也能授课，还能作为 AI Agent 工程作品对外展示。
```

## 5. 分享文案

中文短文案：

```text
整理了一个 AI Agent 开发实战工作台：AgentCraft Studio 2026。
它覆盖 Prompt、Function Calling、LangChain、RAG、Memory、MCP、Skill、评测部署，并带一个智能客服 Agent 毕业项目。
在线预览：https://arvin-lucifer.github.io/agent_course_2026/
```

英文短文案：

```text
I built AgentCraft Studio 2026: a practical AI Agent development forge with 12 lessons, an interactive Studio, interview prep, runnable practice code, and an intelligent customer Agent showcase.
Live preview: https://arvin-lucifer.github.io/agent_course_2026/
```

## 6. Demo 视频建议

建议录制 60-90 秒，不要一上来讲文件树。

镜头顺序：

1. 打开公开首页，停在路线图和三张体验卡。
2. 点击 `进入 AgentCraft Studio`，展示章节导航、挑战、面试和搜索。
3. 点击 L12，展示智能客服 Agent 项目卡片。
4. 打开 `/showcase/`，讲架构、运行命令和答辩要点。
5. 回到 README，展示本地运行和校验命令。

录屏前先运行：

```bash
python3 scripts/build_public_site.py
python3 -m http.server 8780 --directory docs
```

本地录屏地址：

```text
http://127.0.0.1:8780/
http://127.0.0.1:8780/studio/
http://127.0.0.1:8780/showcase/
```

## 7. 分享图片

README 和公开首页使用同一张社交预览卡：

```text
docs/assets/agentcraft-social-card.png
```

它适合用作 GitHub README 首图、社交平台配图和链接预览图。

## 8. 发布前最后动作

- 在 GitHub About 中填写 Description、Website 和 Topics。
- 确认 README 顶部三个在线入口都能打开。
- 确认 `docs/assets/agentcraft-social-card.png`、`site-preview.png`、`showcase-preview.png`、`studio-preview.png` 在 GitHub README 中正常显示。
- 在社交平台或简历中优先放首页链接，其次放 `/showcase/`。
- 每次内容更新后运行质量门禁：

```bash
python3 scripts/build_public_site.py
python3 scripts/validate_project.py
node --check apps/agent_course_studio/web/app.js
python3 -m py_compile apps/agent_course_studio/build_course_data.py apps/agent_course_studio/server.py scripts/build_public_site.py scripts/validate_project.py
git diff --check
```
