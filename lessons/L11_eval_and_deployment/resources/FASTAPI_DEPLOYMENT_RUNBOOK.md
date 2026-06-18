# FastAPI 部署 Runbook

本章部署目标：把本地命令行 Agent 变成可被网页或 API 调用的服务。

## 1. 本地运行

在课程环境中：

```bash
source <course-root>/scripts/activate_course.sh
cd <course-root>/lessons/L11_eval_and_deployment/practice
uvicorn 47_agent_api:app --host 0.0.0.0 --port 8000 --reload
```

健康检查：

```bash
curl http://localhost:8000/health
```

对话接口：

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "我入职2年了，有几天年假？", "session_id": "user_001"}'
```

## 2. 流式 API

```bash
cd <course-root>/lessons/L11_eval_and_deployment/practice
uvicorn 48_agent_api_streaming:app --host 0.0.0.0 --port 8000
```

流式接口：

```bash
curl -N -X POST http://localhost:8000/chat/stream \
  -H "Content-Type: application/json" \
  -d '{"message": "代码合并到主分支前需要做什么？", "session_id": "user_001"}'
```

## 3. 云服务器部署流程

示例流程：

```bash
scp practice/47_agent_api.py root@your-server:/root/project/
scp practice/48_agent_api_streaming.py root@your-server:/root/project/
scp practice/chat_frontend.html root@your-server:/root/project/index.html
scp -r practice/eval_deploy_common.py root@your-server:/root/project/
scp requirements/deployment.txt root@your-server:/root/project/
```

服务器上：

```bash
python3 -m venv venv
source venv/bin/activate
pip install fastapi uvicorn gunicorn sse-starlette python-dotenv pydantic
gunicorn 48_agent_api_streaming:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000
```

## 4. Nginx 代理配置

SSE 流式接口必须关闭缓冲：

```nginx
server {
    listen 80;
    server_name your-domain-or-ip;

    root /var/www/myapp;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /api/ {
        proxy_pass http://127.0.0.1:8000/;
        proxy_http_version 1.1;

        proxy_buffering off;
        proxy_cache off;

        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        proxy_set_header Connection '';
        chunked_transfer_encoding on;

        proxy_read_timeout 86400s;
        proxy_send_timeout 86400s;
    }
}
```

检查和重载：

```bash
sudo nginx -t
sudo systemctl reload nginx
```

## 5. 上线前检查

- `/health` 不调用模型，且能快速返回。
- API 有输入长度限制。
- 高风险动作有人机确认。
- 日志记录 session_id、延迟、工具调用和错误类型。
- 不记录明文密钥和敏感用户数据。
- SSE 经 Nginx 后仍能逐块返回。
- Gunicorn worker 数量与机器资源匹配。
- 有回滚命令和旧版本包。
