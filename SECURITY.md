# Security Policy

Agent Course 2026 是教学项目，但它包含模型调用、工具执行、RAG、Memory、MCP、Skill 和部署相关示例，因此必须保持清晰的安全边界。

## Supported Scope

- 课程内容和公开站点。
- Agent Course Studio 静态前端。
- 本地 Studio server 和白名单 runner。
- L12 智能客服 Agent 参考实现。

## Secrets

- 不要提交 `.env`。
- 不要提交真实 API key、Personal Access Token、代理地址或账户凭据。
- `.env.example` 只能保留占位符。
- 如果误提交密钥，应立即撤销密钥，并清理 Git 历史。

## Runner Boundary

Studio 的真实脚本运行默认关闭。即使开启，也只能执行课程生成的白名单脚本：

- 不允许浏览器提交任意 shell 命令。
- 不读取或展示 `.env` 内容。
- 必须有超时控制。
- 必须返回受控日志，而不是开放本机文件系统。

## Reporting

如果你发现敏感信息、越权执行、公开站点泄露或课程示例里的安全问题，请优先私下联系维护者；不要先公开复现细节。
