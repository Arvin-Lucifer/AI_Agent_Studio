# 课程依赖管理说明

所有依赖统一安装到 `agent_course` conda 环境中。

## 安装顺序

```bash
source <conda-root>/etc/profile.d/conda.sh
conda activate agent_course

pip install -r requirements/core.txt
pip install -r requirements/langchain.txt
pip install -r requirements/rag.txt
pip install -r requirements/mcp.txt
pip install -r requirements/deployment.txt
```

也可以一次性安装：

```bash
pip install -r requirements/all.txt
```

## 文件职责

| 文件 | 用途 |
| --- | --- |
| `core.txt` | L01-L03 基础能力：OpenAI SDK、dotenv、Pydantic、测试和服务基础包 |
| `langchain.txt` | L04、L06、L07 起使用的 LangChain / LangGraph 生态 |
| `rag.txt` | L05 RAG、L07 可选 Chroma 记忆等检索相关依赖 |
| `mcp.txt` | L09 MCP 协议与工具生态相关依赖 |
| `local-embeddings.txt` | 可选本地 embedding 依赖，可能安装较大的 PyTorch/CUDA 包 |
| `deployment.txt` | L11 部署和演示界面相关依赖 |
| `all.txt` | 聚合安装入口 |

## 新增依赖规则

- 先判断依赖属于哪个主题，再放入对应文件。
- 不在单章目录下新增零散 `requirements.txt`。
- 默认课堂主线依赖应尽量轻；重依赖或可选依赖需要在 README 或资源文档中明确标注。
- `sentence-transformers` 这类会拉取 PyTorch/CUDA 的依赖不要放进默认 `rag.txt`，除非课程主线明确需要。
- 新增依赖后，在 `agent_course` 环境中运行本章 `practice/preclass_run.sh` 验证。
