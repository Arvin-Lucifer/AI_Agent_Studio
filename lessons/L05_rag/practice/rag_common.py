#!/usr/bin/env python3
"""Shared helpers for L05 local RAG demos.

这个文件是第五章的“本地 RAG 小引擎”。
它故意只使用 Python 标准库 + OpenAI SDK，避免学生在第一次学习 RAG 时被向量库依赖卡住。

建议阅读顺序：
1. 先看 SAMPLE_DOCS：理解知识库里有哪些原始资料。
2. 再看 split_documents()：理解长文档如何变成 chunk。
3. 再看 build_index()/retrieve()：理解索引和检索的最小实现。
4. 最后看 answer_with_context()：理解检索上下文如何增强模型回答。
"""

from __future__ import annotations

import json
import math
import os
import re
import time
from collections import Counter
from pathlib import Path
from typing import Any, Dict, Iterable, List

from dotenv import load_dotenv
from openai import APIConnectionError, APIStatusError, APITimeoutError, OpenAI, RateLimitError


# 课堂版知识库：三份公司内部文档。
# 真实项目里，这些内容可能来自飞书文档、Confluence、PDF、数据库、工单系统或代码仓库。
SAMPLE_DOCS = [
    {
        "filename": "company_policy.txt",
        "content": """公司员工手册 - 休假政策

一、年假
1. 员工入职满1年后，可享有5天带薪年假。
2. 入职满3年，年假增加至10天。
3. 入职满5年，年假增加至15天。
4. 年假需提前3个工作日向直属领导申请。
5. 未使用的年假不可跨年累积。

二、病假
1. 员工每年享有10天带薪病假。
2. 连续病假超过3天需提供医院证明。
3. 病假期间工资按基本工资的80%发放。

三、事假
1. 事假为无薪假期。
2. 每月事假不超过3天。
3. 需提前1个工作日申请。

四、婚假
1. 员工结婚可享有3天婚假。
2. 晚婚（男满25周岁，女满23周岁）增加7天。
""",
    },
    {
        "filename": "tech_guide.txt",
        "content": """公司技术规范指南

一、代码提交规范
1. 所有代码必须通过 Code Review 后才能合并到主分支。
2. Commit 信息格式：[类型] 简短描述。
   类型包括：feat（新功能）、fix（修复）、docs（文档）、refactor（重构）。
3. 每个 PR 不超过 500 行代码变更。
4. PR 描述必须包含：变更说明、测试方式、影响范围。

二、部署流程
1. 开发环境：代码合并到 dev 分支后自动部署。
2. 测试环境：通过 CI 测试后，手动触发部署到 staging。
3. 生产环境：需要至少 2 人审批，通过发布系统部署。
4. 每次发布必须有回滚方案。

三、API 设计规范
1. RESTful 风格，使用标准 HTTP 方法。
2. 接口路径使用小写字母和连字符。
3. 必须包含版本号，如 /api/v1/users。
4. 返回格式统一：{"code": 0, "message": "ok", "data": {...}}。
5. 错误码规范：4xx 为客户端错误，5xx 为服务端错误。
""",
    },
    {
        "filename": "onboarding.txt",
        "content": """新员工入职指南

一、入职第一天
1. 9:00 到前台领取工卡和办公用品。
2. 9:30 HR 进行入职手续办理（带身份证、银行卡、学历证明）。
3. 10:30 IT 部门分配电脑和账号。
4. 14:00 部门负责人介绍团队成员。
5. 15:00 导师带领熟悉办公环境。

二、入职第一周
1. 完成公司文化培训（线上课程，约3小时）。
2. 完成信息安全培训（线上考试，90分合格）。
3. 与导师制定试用期目标。
4. 了解团队的工作流程和工具使用。

三、试用期
1. 试用期为3个月。
2. 每月进行一次导师面谈。
3. 试用期结束前一周进行转正答辩。
4. 转正需要直属领导和部门负责人审批。

四、常用系统
1. 邮箱：使用公司域名邮箱。
2. 即时通讯：飞书。
3. 代码仓库：GitLab。
4. 项目管理：Jira。
5. 文档协作：飞书文档。
""",
    },
]


def lesson_dir() -> Path:
    """返回 L05 章节目录，保证脚本从任意工作目录运行时路径都稳定。"""
    return Path(__file__).resolve().parents[1]


def find_project_root() -> Path:
    """向上寻找课程根目录，用于加载统一的 .env。"""
    for parent in Path(__file__).resolve().parents:
        if (parent / ".env").exists() or (parent / ".env.example").exists():
            return parent
    raise RuntimeError("Cannot find project root with .env or .env.example")


def load_project_env() -> None:
    """加载课程根目录 .env；override=False 方便临时环境变量覆盖。"""
    load_dotenv(find_project_root() / ".env", override=False)


def default_kb_dir() -> Path:
    # L05 的运行数据统一放到 data/ 下，避免和课程讲义、练习代码混在同一层。
    return lesson_dir() / "data" / "knowledge_base"


def default_index_path() -> Path:
    # 索引是可再生成产物，也放到 data/ 下；删除后重新运行 12_build_local_index.py 即可恢复。
    return lesson_dir() / "data" / "rag_index" / "local_index.json"


def ensure_sample_docs(kb_dir: Path | None = None, overwrite: bool = False) -> List[Path]:
    """生成示例知识库文档。

    overwrite=False 是为了保护学生后续自己替换的文档。
    """
    target_dir = kb_dir or default_kb_dir()
    target_dir.mkdir(parents=True, exist_ok=True)

    written: List[Path] = []
    for item in SAMPLE_DOCS:
        path = target_dir / item["filename"]
        if overwrite or not path.exists():
            path.write_text(item["content"], encoding="utf-8")
        written.append(path)
    return written


def load_documents(kb_dir: Path | None = None) -> List[Dict[str, str]]:
    """读取知识库中的 txt 文档，返回统一的 document dict。"""
    target_dir = kb_dir or default_kb_dir()
    docs: List[Dict[str, str]] = []
    for path in sorted(target_dir.glob("*.txt")):
        docs.append({"source": path.name, "content": path.read_text(encoding="utf-8")})
    return docs


def normalize_text(text: str) -> str:
    """做最小文本清洗：统一换行、去掉过多空白。"""
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    return text.strip()


def split_text(text: str, chunk_size: int = 300, chunk_overlap: int = 50) -> List[str]:
    """把长文本切成 chunk。

    这不是生产级语义切分器，但保留了 RAG 最重要的两个概念：
    chunk_size 控制每块最大长度，chunk_overlap 缓解上下文被切断。
    """
    text = normalize_text(text)
    pieces = [piece.strip() for piece in re.split(r"\n\s*\n", text) if piece.strip()]

    chunks: List[str] = []
    current = ""

    def flush() -> None:
        nonlocal current
        if current.strip():
            chunks.append(current.strip())
        current = ""

    for piece in pieces:
        # 如果单个段落过长，就按字符窗口硬切。真实项目会优先按标题/句子/语义边界切。
        if len(piece) > chunk_size:
            flush()
            start = 0
            while start < len(piece):
                chunks.append(piece[start:start + chunk_size].strip())
                start += max(1, chunk_size - chunk_overlap)
            continue

        candidate = f"{current}\n\n{piece}".strip() if current else piece
        if len(candidate) <= chunk_size:
            current = candidate
        else:
            flush()
            # 新 chunk 带上上一块末尾 overlap 字符，减少“定义在上一块、细节在下一块”的断裂。
            if chunks and chunk_overlap > 0:
                current = f"{chunks[-1][-chunk_overlap:]}\n\n{piece}".strip()
            else:
                current = piece
    flush()
    return [chunk for chunk in chunks if chunk]


def split_documents(
    docs: Iterable[Dict[str, str]],
    chunk_size: int = 300,
    chunk_overlap: int = 50,
) -> List[Dict[str, Any]]:
    """把文档列表切成带 metadata 的 chunk 列表。"""
    chunks: List[Dict[str, Any]] = []
    for doc in docs:
        for index, text in enumerate(split_text(doc["content"], chunk_size, chunk_overlap), 1):
            chunk_id = f"{doc['source']}#chunk-{index:03d}"
            chunks.append(
                {
                    "chunk_id": chunk_id,
                    "source": doc["source"],
                    "text": text,
                    "metadata": {
                        "source": doc["source"],
                        "chunk_index": index,
                        "chunk_size": chunk_size,
                        "chunk_overlap": chunk_overlap,
                    },
                }
            )
    return chunks


def tokenize(text: str) -> List[str]:
    """把中英文文本转成检索 token。

    中文没有空格，所以这里把汉字按单字切；英文、数字、路径保留为词。
    生产系统会使用更好的分词、embedding 或 BM25。
    """
    return re.findall(r"[A-Za-z0-9_./:-]+|[\u4e00-\u9fff]", text.lower())


def build_index(chunks: List[Dict[str, Any]]) -> Dict[str, Any]:
    """构建一个轻量 TF-IDF 风格索引。

    这不是向量数据库替代品；它只是把“文本 -> 数字特征 -> 相似度检索”的思想讲清楚。
    """
    tokenized = [tokenize(item["text"]) for item in chunks]
    doc_freq: Counter[str] = Counter()
    for tokens in tokenized:
        doc_freq.update(set(tokens))

    total = max(1, len(chunks))
    idf = {token: math.log((total + 1) / (freq + 1)) + 1.0 for token, freq in doc_freq.items()}

    indexed_chunks = []
    for item, tokens in zip(chunks, tokenized):
        vector = vectorize_tokens(tokens, idf)
        indexed = dict(item)
        indexed["tokens"] = tokens
        indexed["vector"] = vector
        indexed["norm"] = vector_norm(vector)
        indexed_chunks.append(indexed)

    return {"version": 1, "chunk_count": len(indexed_chunks), "idf": idf, "chunks": indexed_chunks}


def vectorize_tokens(tokens: List[str], idf: Dict[str, float]) -> Dict[str, float]:
    """把 token 列表变成稀疏向量 dict。"""
    if not tokens:
        return {}
    counts = Counter(tokens)
    length = len(tokens)
    return {token: (count / length) * idf.get(token, 1.0) for token, count in counts.items()}


def vector_norm(vector: Dict[str, float]) -> float:
    return math.sqrt(sum(value * value for value in vector.values()))


def cosine_similarity(left: Dict[str, float], left_norm: float, right: Dict[str, float], right_norm: float) -> float:
    """计算两个稀疏向量的余弦相似度。"""
    if left_norm == 0 or right_norm == 0:
        return 0.0
    if len(left) > len(right):
        left, right = right, left
    dot = sum(value * right.get(token, 0.0) for token, value in left.items())
    return dot / (left_norm * right_norm)


def save_index(index: Dict[str, Any], index_path: Path | None = None) -> Path:
    target = index_path or default_index_path()
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(index, ensure_ascii=False, indent=2), encoding="utf-8")
    return target


def load_index(index_path: Path | None = None) -> Dict[str, Any]:
    target = index_path or default_index_path()
    return json.loads(target.read_text(encoding="utf-8"))


def build_and_save_index(
    kb_dir: Path | None = None,
    index_path: Path | None = None,
    chunk_size: int = 300,
    chunk_overlap: int = 50,
) -> Dict[str, Any]:
    """加载文档、切分、建索引并保存，是离线建库阶段的最小闭环。"""
    ensure_sample_docs(kb_dir)
    docs = load_documents(kb_dir)
    chunks = split_documents(docs, chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    index = build_index(chunks)
    save_index(index, index_path)
    return index


def ensure_index(index_path: Path | None = None) -> Dict[str, Any]:
    """如果本地索引不存在，就自动构建一份。"""
    target = index_path or default_index_path()
    if not target.exists():
        return build_and_save_index(index_path=target)
    return load_index(target)


def retrieve(index: Dict[str, Any], query: str, top_k: int = 3) -> List[Dict[str, Any]]:
    """根据 query 检索最相似的 chunk。"""
    query_vector = vectorize_tokens(tokenize(query), index.get("idf", {}))
    query_norm = vector_norm(query_vector)
    results: List[Dict[str, Any]] = []
    for chunk in index.get("chunks", []):
        score = cosine_similarity(query_vector, query_norm, chunk.get("vector", {}), float(chunk.get("norm", 0.0)))
        if score > 0:
            item = dict(chunk)
            item["score"] = score
            results.append(item)
    return sorted(results, key=lambda item: item["score"], reverse=True)[:top_k]


def format_context(results: List[Dict[str, Any]]) -> str:
    """把检索结果整理成 LLM 可读、可引用的上下文。"""
    if not results:
        return "未检索到相关资料。"
    blocks = []
    for index, item in enumerate(results, 1):
        blocks.append(
            "\n".join(
                [
                    f"[资料{index}]",
                    f"来源：{item['source']}",
                    f"片段：{item['chunk_id']}",
                    f"相关度：{item['score']:.4f}",
                    item["text"],
                ]
            )
        )
    return "\n\n".join(blocks)


def read_int_env(name: str, default: int) -> int:
    raw = os.getenv(name, "").strip()
    if not raw:
        return default
    try:
        value = int(raw)
        return value if value >= 1 else default
    except Exception:
        print(f"[WARN] Invalid {name}={raw!r}, fallback to {default}")
        return default


def read_float_env(name: str, default: float) -> float:
    raw = os.getenv(name, "").strip()
    if not raw:
        return default
    try:
        value = float(raw)
        return value if value > 0 else default
    except Exception:
        print(f"[WARN] Invalid {name}={raw!r}, fallback to {default}")
        return default


def build_client() -> tuple[OpenAI, str]:
    """创建 OpenAI client，用于最后的生成阶段。"""
    load_project_env()
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    base_url = os.getenv("OPENAI_BASE_URL", "").strip()
    model = os.getenv("OPENAI_MODEL", "").strip()
    missing = [name for name, value in {
        "OPENAI_API_KEY": api_key,
        "OPENAI_BASE_URL": base_url,
        "OPENAI_MODEL": model,
    }.items() if not value]
    if missing:
        raise RuntimeError(f"Missing required env vars: {', '.join(missing)}")
    return OpenAI(api_key=api_key, base_url=base_url), model


def answer_with_context(question: str, context: str) -> str:
    """把检索上下文和用户问题一起交给 LLM，生成带引用的答案。"""
    client, model = build_client()
    max_attempts = read_int_env("RAG_MAX_ATTEMPTS", 2)
    request_timeout = read_float_env("RAG_REQUEST_TIMEOUT_SEC", 60.0)
    backoff_sec = read_float_env("RAG_RETRY_BACKOFF_SEC", 2.0)

    system_prompt = (
        "你是公司内部知识库问答助手。只能基于用户提供的资料回答。"
        "如果资料中没有答案，请明确说无法从现有资料确认。"
        "回答后必须列出引用来源，格式为：来源：文件名#chunk。"
    )
    user_prompt = f"""请根据以下资料回答问题。

资料：
{context}

问题：
{question}
"""

    for attempt in range(1, max_attempts + 1):
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0,
                timeout=request_timeout,
            )
            return response.choices[0].message.content or ""
        except (APITimeoutError, APIConnectionError, RateLimitError) as exc:
            if attempt == max_attempts:
                raise
            sleep_sec = backoff_sec * attempt
            print(f"[WARN] attempt {attempt}/{max_attempts} failed: {type(exc).__name__}. Retry in {sleep_sec:.1f}s ...")
            time.sleep(sleep_sec)
        except APIStatusError as exc:
            if exc.status_code is not None and exc.status_code >= 500 and attempt < max_attempts:
                sleep_sec = backoff_sec * attempt
                print(f"[WARN] attempt {attempt}/{max_attempts} failed: APIStatusError({exc.status_code}). Retry in {sleep_sec:.1f}s ...")
                time.sleep(sleep_sec)
                continue
            raise

    raise RuntimeError("unreachable RAG retry state")
