# Agent Course Studio

`Agent Course Studio` 是本仓库的网页版课程实验室。它直接读取 `lessons/L01-L12` 的课程材料，生成一个可浏览、可搜索、可演示的学习工作台。

## 功能

- 12 章课程路径导航。
- 章节概览、讲义、实战、面试题、资源统一展示。
- 本地搜索，支持按关键词定位章节。
- 本地检索式课程助手，返回带引用的学习建议。
- 浏览器本地学习进度记录。
- 每章实验脚本命令复制。
- 可选的白名单脚本运行接口。

## 快速启动

从仓库根目录运行：

```bash
python3 apps/agent_course_studio/build_course_data.py
python3 apps/agent_course_studio/server.py --host 127.0.0.1 --port 8765
```

打开：

```text
http://127.0.0.1:8765
```

## 重新生成课程索引

当 `lessons/` 下的讲义、面试题、资源或实践脚本发生变化时，重新执行：

```bash
python3 apps/agent_course_studio/build_course_data.py
```

生成文件：

```text
apps/agent_course_studio/web/data/course.json
```

## 实验运行安全边界

网页右侧的“实验运行”默认不会真正执行脚本。这样做是为了避免网页入口意外触发 API 调用、文件写入或长时间任务。

如果确实要启用本地白名单运行：

```bash
AGENT_COURSE_STUDIO_ALLOW_RUN=1 \
python3 apps/agent_course_studio/server.py --host 127.0.0.1 --port 8765
```

运行接口只接受课程索引中已有章节的 `practice/preclass_run.sh`，不会执行浏览器传入的任意 shell 命令。

可选超时配置：

```bash
AGENT_COURSE_STUDIO_RUN_TIMEOUT_SEC=300
```

## 数据脱敏策略

`build_course_data.py` 会在生成网页数据时处理：

- 将本机绝对路径替换成 `<course-root>` 或 `<user-home>`。
- 将常见 API key 形态替换为 `<redacted>`。
- 跳过 `.env`、缓存目录、生成索引和运行态数据。

网页不读取 `.env`，也不会展示本地代理脚本内容。

## 后续升级方向

- 用 FastAPI 替换轻量 server，支持流式日志。
- 将本地检索助手升级为真正 RAG。
- 为 Function Calling、RAG、Memory、LangGraph、Skill 和 L12 增加过程可视化。
- 增加作业提交、评测集和学习报告。
