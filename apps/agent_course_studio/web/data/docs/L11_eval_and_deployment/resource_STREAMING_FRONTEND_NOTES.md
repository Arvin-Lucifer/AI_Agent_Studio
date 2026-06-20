# 流式输出与前端接入

流式输出解决的是体验问题：Agent 可能需要检索、工具调用和多步推理，如果用户只能等最终结果，体感延迟会很高。

## 1. SSE 事件设计

推荐事件类型：

```json
{"type": "tool_call", "tool": "search_knowledge_base"}
{"type": "token", "content": "根据公司制度"}
{"type": "done", "session_id": "user_001"}
{"type": "error", "message": "..."}
```

这样前端可以分别展示：

- 工具调用状态。
- 打字机文本。
- 完成标记。
- 错误提示。

## 2. 为什么不用一次性返回

一次性返回的问题：

- 用户不知道系统是否卡住。
- 工具调用过程不可见。
- 长回答体验差。
- 前端无法做中途状态展示。

## 3. 前端解析要点

前端需要处理：

- SSE 分块可能把一条 JSON 拆开，必须用 buffer。
- 不要用 `innerHTML` 直接拼用户输入。
- 工具事件和 token 事件分开展示。
- 请求失败时给出明确错误状态。

本章的 `practice/chat_frontend.html` 是最小可用版本，重点展示数据流，不追求复杂 UI。

## 4. Nginx 注意事项

SSE 需要关闭代理缓冲：

```nginx
proxy_buffering off;
proxy_cache off;
proxy_read_timeout 86400s;
```

否则后端已经逐块发送，浏览器仍可能等缓冲满了才看到内容。
