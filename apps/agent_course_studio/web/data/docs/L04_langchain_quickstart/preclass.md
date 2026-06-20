# L04 课前准备清单

## 1. 环境检查

从课程根目录激活环境：

```bash
source <course-root>/scripts/activate_course.sh
```

安装 LangChain 相关依赖：

```bash
cd <course-root>
pip install -r requirements/langchain.txt
```

检查基础环境：

```bash
python scripts/check_env.py
python scripts/smoke_openai.py
```

## 2. 概念预习

- 复习 L03 的 Function Calling 循环。
- 能说出 `tool_calls`、工具执行、`tool_call_id` 的作用。
- 阅读 [../../../CODE_COMMENTING_GUIDE.md](../../../CODE_COMMENTING_GUIDE.md)，理解本章代码注释重点。
- 预习 [resources/LANGCHAIN_LANGGRAPH_COMPARISON.md](../resources/LANGCHAIN_LANGGRAPH_COMPARISON.md)。

## 3. 代码预习

```bash
cd <course-root>/lessons/L04_langchain_quickstart
python practice/08_custom_tools.py --describe
```

确认能看到工具名称、参数 schema 和描述。

## 4. 课前思考

- 如果不用框架，L03 的哪部分代码最容易重复？
- 工具描述写得含糊，会带来什么问题？
- 为什么记忆不能只用一个全局列表？
- 如果搜索工具返回错误内容，Agent 应该直接相信吗？
