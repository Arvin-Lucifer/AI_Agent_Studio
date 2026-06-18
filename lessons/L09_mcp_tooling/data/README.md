# L09 示例数据目录

`practice/29_mcp_note_server.py` 默认把笔记写入本目录下的 `notes.json`。

这个数据文件由课堂脚本自动生成，不需要手动维护。

后续可以扩展：

- `notes.sqlite`：把 JSON 存储迁移到 SQLite。
- `audit_logs/`：记录 MCP 工具调用和资源读取审计日志。
- `sampling_logs/`：记录被允许或拒绝的 Sampling 请求。
