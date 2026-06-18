#!/usr/bin/env python3
"""Shared helpers for L07 memory system demos.

这个文件是第 7 章的“记忆系统工具箱”：
短期记忆、摘要压缩、长期 JSON 记忆、轻量知识图谱和混合检索都放在这里。

建议阅读顺序：
1. 先看 sliding_window_memory()/smart_memory()：理解短期记忆如何控制上下文长度。
2. 再看 LongTermMemory：理解跨会话信息如何持久化到 JSON。
3. 再看 KnowledgeGraph：理解向量/关键词检索之外，关系记忆如何表达多跳关联。
4. 最后看 HybridLongTermMemory：理解“语义检索 + 图谱扩展”如何组合。
"""

from __future__ import annotations

import json
import math
import os
import re
import time
import uuid
from collections import Counter, deque
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Callable, Dict, Iterable, List, Optional

from dotenv import load_dotenv
from openai import APIConnectionError, APIStatusError, APITimeoutError, OpenAI, RateLimitError


Message = Dict[str, str]


def lesson_dir() -> Path:
    """返回 L07 章节目录，保证从任意工作目录运行时路径稳定。"""
    return Path(__file__).resolve().parents[1]


def data_dir() -> Path:
    """本章所有可再生成数据统一放到 data/，避免污染讲义和代码目录。"""
    target = lesson_dir() / "data"
    target.mkdir(parents=True, exist_ok=True)
    return target


def find_project_root() -> Path:
    """向上寻找课程根目录，用于加载统一 .env。"""
    for parent in Path(__file__).resolve().parents:
        if (parent / ".env").exists() or (parent / ".env.example").exists():
            return parent
    raise RuntimeError("Cannot find project root with .env or .env.example")


def load_project_env() -> None:
    """加载课程根目录 .env；override=False 允许 shell 临时变量覆盖默认配置。"""
    load_dotenv(find_project_root() / ".env", override=False)


def default_json_memory_path() -> Path:
    return data_dir() / "user_memory.json"


def default_hybrid_memory_path() -> Path:
    return data_dir() / "hybrid_memory.json"


def default_kg_path() -> Path:
    return data_dir() / "kg_memory.json"


def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")


def _read_int_env(name: str, default: int) -> int:
    raw = os.getenv(name, "").strip()
    if not raw:
        return default
    try:
        value = int(raw)
        return value if value >= 1 else default
    except Exception:
        print(f"[WARN] Invalid {name}={raw!r}, fallback to {default}")
        return default


def _read_float_env(name: str, default: float) -> float:
    raw = os.getenv(name, "").strip()
    if not raw:
        return default
    try:
        value = float(raw)
        return value if value > 0 else default
    except Exception:
        print(f"[WARN] Invalid {name}={raw!r}, fallback to {default}")
        return default


def build_openai_client() -> tuple[OpenAI, str]:
    """创建 OpenAI 兼容 client，并返回模型名。

    L07 的摘要示例默认可以不调用模型；只有开启 --use-llm 时才会走这里。
    """
    load_project_env()
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    base_url = os.getenv("OPENAI_BASE_URL", "").strip()
    model = os.getenv("OPENAI_MODEL", "").strip()
    missing = [
        name
        for name, value in {
            "OPENAI_API_KEY": api_key,
            "OPENAI_BASE_URL": base_url,
            "OPENAI_MODEL": model,
        }.items()
        if not value
    ]
    if missing:
        raise RuntimeError(f"Missing required env vars: {', '.join(missing)}")
    return OpenAI(api_key=api_key, base_url=base_url), model


def sliding_window_memory(messages: List[Message], max_turns: int = 10) -> List[Message]:
    """滑动窗口：始终保留 system 消息，只保留最近 N 轮 user/assistant 对话。

    这对应老师讲义里的“短期记忆策略一”：
    简单、便宜、稳定，但会丢失早期重要信息，例如用户一开始说的名字。
    """
    system_msgs = [item for item in messages if item.get("role") == "system"]
    other_msgs = [item for item in messages if item.get("role") != "system"]
    keep_count = max(0, max_turns) * 2
    if keep_count and len(other_msgs) > keep_count:
        other_msgs = other_msgs[-keep_count:]
    return system_msgs + other_msgs


def format_conversation(messages: Iterable[Message]) -> str:
    """把 messages 转成摘要模型更容易读的纯文本。"""
    lines = []
    for item in messages:
        role = item.get("role", "unknown")
        content = item.get("content", "")
        if role == "user":
            lines.append(f"用户: {content}")
        elif role == "assistant":
            lines.append(f"助手: {content}")
        elif role == "system":
            lines.append(f"系统: {content}")
    return "\n".join(lines)


def local_summarize_conversation(messages: List[Message], max_points: int = 3) -> str:
    """本地摘要兜底：不调用模型，只抽取早期对话的关键信息。

    课堂上先用它能稳定演示“摘要消息如何替代旧历史”；
    真正需要高质量压缩时，再切换到 llm_summarize_conversation()。
    """
    user_points = [
        item["content"]
        for item in messages
        if item.get("role") == "user" and item.get("content")
    ][:max_points]
    if not user_points:
        return "早期对话没有可摘要的用户关键信息。"
    return "；".join(user_points)


def llm_summarize_conversation(messages: List[Message]) -> str:
    """用 LLM 压缩早期对话。

    摘要压缩的关键风险是“丢细节”和“摘要幻觉”，所以 prompt 明确要求保留事实、
    偏好、约定和未完成任务，不要补充对话里没有的信息。
    """
    client, model = build_openai_client()
    conversation_text = format_conversation(messages)
    request_timeout = _read_float_env("MEMORY_REQUEST_TIMEOUT_SEC", 45.0)
    max_attempts = _read_int_env("MEMORY_MAX_RETRIES", 2)
    backoff_sec = _read_float_env("MEMORY_RETRY_BACKOFF_SEC", 1.5)

    prompt = f"""请用 2-3 句话总结以下对话，保留：
1. 用户身份、偏好、长期有效信息
2. 已达成的决定
3. 未完成任务

不要添加对话中没有的信息。

对话：
{conversation_text}

摘要："""

    for attempt in range(1, max_attempts + 1):
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0,
                timeout=request_timeout,
            )
            return response.choices[0].message.content or ""
        except (APITimeoutError, APIConnectionError, RateLimitError) as exc:
            if attempt >= max_attempts:
                raise
            sleep_sec = backoff_sec * attempt
            print(f"[WARN] summarize failed: {type(exc).__name__}, retry in {sleep_sec:.1f}s")
            time.sleep(sleep_sec)
        except APIStatusError as exc:
            if exc.status_code is not None and exc.status_code >= 500 and attempt < max_attempts:
                sleep_sec = backoff_sec * attempt
                print(f"[WARN] summarize status {exc.status_code}, retry in {sleep_sec:.1f}s")
                time.sleep(sleep_sec)
                continue
            raise
    raise RuntimeError("unreachable")


def smart_memory(
    messages: List[Message],
    max_recent: int = 6,
    summarizer: Callable[[List[Message]], str] = local_summarize_conversation,
) -> List[Message]:
    """摘要压缩：system + 旧对话摘要 + 最近若干条消息。

    这对应老师讲义里的“策略二”。
    和滑动窗口相比，它能保留早期关键信息；代价是摘要可能丢失细节。
    """
    system_msgs = [item for item in messages if item.get("role") == "system"]
    other_msgs = [item for item in messages if item.get("role") != "system"]
    if len(other_msgs) <= max_recent:
        return list(messages)

    old_msgs = other_msgs[:-max_recent]
    recent_msgs = other_msgs[-max_recent:]
    summary = summarizer(old_msgs)
    summary_msg = {
        "role": "system",
        "content": f"之前的对话摘要：{summary}",
    }
    return system_msgs + [summary_msg] + recent_msgs


def default_memory_data() -> Dict[str, Any]:
    """JSON 长期记忆的最小 schema。"""
    return {
        "user_profile": {},
        "facts": [],
        "preferences": [],
        "deleted": [],
    }


class LongTermMemory:
    """基于 JSON 文件的长期记忆。

    这是老师讲义里的 7.3.1 版本的课程化实现：
    - profile 用 key 覆盖，表示“最新画像即真值”。
    - facts/preferences 用 append，表示事件流。
    - search 使用关键词匹配，便于学生先理解写入-检索-回答闭环。
    """

    def __init__(self, filepath: str | Path | None = None) -> None:
        self.filepath = Path(filepath) if filepath else default_json_memory_path()
        self.filepath.parent.mkdir(parents=True, exist_ok=True)
        self.memories = self._load()

    def _load(self) -> Dict[str, Any]:
        if self.filepath.exists():
            try:
                loaded = json.loads(self.filepath.read_text(encoding="utf-8"))
                base = default_memory_data()
                base.update(loaded)
                return base
            except json.JSONDecodeError:
                return default_memory_data()
        return default_memory_data()

    def _save(self) -> None:
        self.filepath.write_text(
            json.dumps(self.memories, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    def update_profile(self, key: str, value: str) -> None:
        """更新用户画像；相同 key 覆盖旧值。"""
        self.memories["user_profile"][key] = {
            "value": value,
            "updated_at": now_iso(),
        }
        self._save()

    def save_fact(
        self,
        fact: str,
        category: str = "general",
        importance: int = 5,
        ttl_days: int | None = None,
    ) -> str:
        """保存一条事实，返回 memory_id。"""
        memory_id = str(uuid.uuid4())
        entry = {
            "id": memory_id,
            "content": fact,
            "category": category,
            "importance": max(1, min(10, importance)),
            "created_at": now_iso(),
            "last_access": None,
            "access_count": 0,
            "expire_at": (
                (datetime.now() + timedelta(days=ttl_days)).isoformat(timespec="seconds")
                if ttl_days
                else None
            ),
        }
        self.memories["facts"].append(entry)
        self._save()
        return memory_id

    def save_preference(self, key: str, value: str, importance: int = 5) -> str:
        """保存用户偏好；偏好可能演变，因此用事件流记录。"""
        memory_id = str(uuid.uuid4())
        self.memories["preferences"].append(
            {
                "id": memory_id,
                "key": key,
                "value": value,
                "importance": max(1, min(10, importance)),
                "created_at": now_iso(),
                "last_access": None,
                "access_count": 0,
            }
        )
        self._save()
        return memory_id

    def _touch(self, entry: Dict[str, Any]) -> None:
        entry["last_access"] = now_iso()
        entry["access_count"] = int(entry.get("access_count") or 0) + 1

    def search(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """简单关键词搜索，并更新访问统计。

        关键词搜索对姓名、ID、技术名很稳定；缺点是没有语义泛化。
        """
        query_lower = query.lower()
        results: List[Dict[str, Any]] = []

        for fact in self.memories["facts"]:
            if query_lower in str(fact.get("content", "")).lower():
                self._touch(fact)
                results.append({"type": "fact", **fact})

        for pref in self.memories["preferences"]:
            haystack = f"{pref.get('key', '')} {pref.get('value', '')}".lower()
            if query_lower in haystack:
                self._touch(pref)
                results.append({"type": "preference", **pref})

        self._save()
        results.sort(
            key=lambda item: (
                int(item.get("importance") or 0),
                int(item.get("access_count") or 0),
            ),
            reverse=True,
        )
        return results[:limit]

    def get_profile_summary(self) -> str:
        """获取用户画像摘要，供 Agent 工具返回给模型。"""
        profile = self.memories["user_profile"]
        if not profile:
            return "暂无用户画像信息。"
        lines = []
        for key, item in profile.items():
            value = item.get("value") if isinstance(item, dict) else item
            lines.append(f"- {key}: {value}")
        return "\n".join(lines)

    def forget(self, query: str) -> int:
        """显式删除：按关键词软删除事实和偏好。

        课程版用软删除保留审计记录；生产系统还要考虑真正物理删除和备份清理。
        """
        query_lower = query.lower()
        deleted_count = 0
        for bucket_name in ("facts", "preferences"):
            kept = []
            for entry in self.memories[bucket_name]:
                rendered = json.dumps(entry, ensure_ascii=False).lower()
                if query_lower in rendered:
                    deleted_count += 1
                    self.memories["deleted"].append(
                        {
                            "type": bucket_name,
                            "entry": entry,
                            "deleted_at": now_iso(),
                            "reason": f"explicit query: {query}",
                        }
                    )
                else:
                    kept.append(entry)
            self.memories[bucket_name] = kept
        self._save()
        return deleted_count

    def cleanup_expired(self) -> int:
        """清理过期事实，对应老师讲义里的 TTL 遗忘策略。"""
        now = datetime.now()
        kept = []
        removed = 0
        for fact in self.memories["facts"]:
            expire_at = fact.get("expire_at")
            if expire_at and datetime.fromisoformat(expire_at) <= now:
                removed += 1
                self.memories["deleted"].append(
                    {
                        "type": "facts",
                        "entry": fact,
                        "deleted_at": now_iso(),
                        "reason": "ttl expired",
                    }
                )
            else:
                kept.append(fact)
        self.memories["facts"] = kept
        self._save()
        return removed


def tokenize(text: str) -> List[str]:
    """中英文混合切词：英文按词，中文按单字。"""
    return re.findall(r"[A-Za-z0-9_./:-]+|[\u4e00-\u9fff]", text.lower())


def sparse_similarity(query: str, document: str) -> float:
    """标准库版稀疏相似度，用于替代 Chroma 演示“语义入口”的思想。"""
    query_tokens = tokenize(query)
    doc_tokens = tokenize(document)
    if not query_tokens or not doc_tokens:
        return 0.0
    q_counts = Counter(query_tokens)
    d_counts = Counter(doc_tokens)
    dot = sum(value * d_counts.get(token, 0) for token, value in q_counts.items())
    q_norm = math.sqrt(sum(value * value for value in q_counts.values()))
    d_norm = math.sqrt(sum(value * value for value in d_counts.values()))
    return dot / (q_norm * d_norm) if q_norm and d_norm else 0.0


class KnowledgeGraph:
    """轻量知识图谱：用 JSON 保存实体和三元组关系。"""

    def __init__(self, filepath: str | Path | None = None) -> None:
        self.filepath = Path(filepath) if filepath else default_kg_path()
        self.filepath.parent.mkdir(parents=True, exist_ok=True)
        self.data = self._load()

    def _load(self) -> Dict[str, Any]:
        default = {"entities": {}, "relations": []}
        if self.filepath.exists():
            try:
                loaded = json.loads(self.filepath.read_text(encoding="utf-8"))
                default.update(loaded)
            except json.JSONDecodeError:
                pass
        return default

    def _save(self) -> None:
        self.filepath.write_text(
            json.dumps(self.data, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    def add_entity(self, name: str, etype: str = "generic", **props: Any) -> None:
        """新增/更新实体；实体用名称 upsert。"""
        node = self.data["entities"].get(name, {"type": etype, "props": {}})
        node["type"] = etype or node.get("type", "generic")
        node["props"].update(props)
        node["props"]["updated_at"] = now_iso()
        self.data["entities"][name] = node
        self._save()

    def get_entity(self, name: str) -> Optional[Dict[str, Any]]:
        return self.data["entities"].get(name)

    def add_relation(self, subject: str, predicate: str, object_: str, **props: Any) -> Dict[str, Any]:
        """新增三元组，并自动补建实体节点。"""
        if subject not in self.data["entities"]:
            self.add_entity(subject)
        if object_ not in self.data["entities"]:
            self.add_entity(object_)
        triple = {
            "id": str(uuid.uuid4()),
            "subject": subject,
            "predicate": predicate,
            "object": object_,
            "props": {**props, "timestamp": now_iso()},
        }
        self.data["relations"].append(triple)
        self._save()
        return triple

    def neighbors(self, name: str, predicate: str | None = None, direction: str = "both") -> List[Dict[str, Any]]:
        """返回与实体相关的三元组。direction 可取 out/in/both。"""
        output = []
        for relation in self.data["relations"]:
            if predicate is not None and relation["predicate"] != predicate:
                continue
            if direction in ("out", "both") and relation["subject"] == name:
                output.append({**relation, "_direction": "out"})
            if direction in ("in", "both") and relation["object"] == name:
                output.append({**relation, "_direction": "in"})
        return output

    def graph_search(self, entity: str, hops: int = 1) -> List[Dict[str, Any]]:
        """从实体出发做 N 跳关系扩展。"""
        if not self.get_entity(entity):
            return []
        seen = set()
        frontier = {entity}
        triples = []
        for _ in range(max(0, hops)):
            next_frontier = set()
            for node in frontier:
                for relation in self.neighbors(node, direction="both"):
                    key = (relation["subject"], relation["predicate"], relation["object"])
                    if key in seen:
                        continue
                    seen.add(key)
                    triples.append(relation)
                    next_frontier.add(
                        relation["object"] if relation["_direction"] == "out" else relation["subject"]
                    )
            frontier = next_frontier - {entity}
            if not frontier:
                break
        return triples

    def find_path(self, src: str, dst: str, max_hops: int = 3) -> List[List[Dict[str, Any]]]:
        """BFS 查找 src 到 dst 的多跳路径。"""
        if not self.get_entity(src) or not self.get_entity(dst):
            return []
        paths = []
        queue = deque([(src, [])])
        while queue:
            node, path = queue.popleft()
            if len(path) >= max_hops:
                continue
            for relation in self.neighbors(node, direction="both"):
                next_node = relation["object"] if relation["_direction"] == "out" else relation["subject"]
                visited = {item["subject"] for item in path} | {item["object"] for item in path}
                if next_node in visited and next_node != dst:
                    continue
                new_path = path + [relation]
                if next_node == dst:
                    paths.append(new_path)
                else:
                    queue.append((next_node, new_path))
        return paths


@dataclass
class SearchHit:
    source: str
    content: str
    score: float
    metadata: Dict[str, Any]


class HybridLongTermMemory:
    """标准库版“语义入口 + 图谱扩展”混合长期记忆。

    老师讲义里给的是 Chroma + KG 版本。为了让课堂默认可运行，这里用 JSON +
    稀疏相似度替代 Chroma；概念保持一致：先找入口，再沿关系扩展。
    """

    def __init__(
        self,
        memory_path: str | Path | None = None,
        kg_path: str | Path | None = None,
    ) -> None:
        self.memory = LongTermMemory(memory_path or default_hybrid_memory_path())
        self.kg = KnowledgeGraph(kg_path or default_kg_path())

    def update_profile(self, key: str, value: str) -> None:
        self.memory.update_profile(key, value)

    def save_preference(self, key: str, value: str, importance: int = 5) -> str:
        return self.memory.save_preference(key, value, importance=importance)

    def save_fact(self, fact: str, category: str = "general", importance: int = 5) -> str:
        return self.memory.save_fact(fact, category=category, importance=importance)

    def add_entity(self, name: str, etype: str = "generic", **props: Any) -> None:
        self.kg.add_entity(name, etype=etype, **props)

    def add_relation(self, subject: str, predicate: str, object_: str, **props: Any) -> Dict[str, Any]:
        """三元组双写：写入 KG，同时写入事实流，方便文本检索命中。"""
        triple = self.kg.add_relation(subject, predicate, object_, **props)
        self.memory.save_fact(
            f"{subject} {predicate} {object_}",
            category="kg_triple",
            importance=7,
        )
        return triple

    def vector_search(self, query: str, k: int = 3) -> List[SearchHit]:
        """本地相似度检索 facts/preferences，模拟 Chroma 的语义检索入口。"""
        hits: List[SearchHit] = []
        for fact in self.memory.memories["facts"]:
            score = sparse_similarity(query, str(fact.get("content", "")))
            if score > 0:
                hits.append(SearchHit("fact", fact["content"], score, fact))
        for pref in self.memory.memories["preferences"]:
            content = f"{pref.get('key')}: {pref.get('value')}"
            score = sparse_similarity(query, content)
            if score > 0:
                hits.append(SearchHit("preference", content, score, pref))
        hits.sort(key=lambda item: item.score, reverse=True)
        return hits[:k]

    def hybrid_search(
        self,
        query: str,
        k: int = 3,
        hops: int = 1,
        anchor_entities: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """混合检索：文本检索找入口，图谱按实体扩展。"""
        vector_hits = self.vector_search(query, k=k)
        anchors: List[str] = list(anchor_entities or [])
        if not anchors:
            known_entities = list(self.kg.data["entities"].keys())
            for hit in vector_hits:
                for entity in known_entities:
                    if entity in hit.content and entity not in anchors:
                        anchors.append(entity)

        graph_hits = []
        for entity in anchors:
            graph_hits.extend(self.kg.graph_search(entity, hops=hops))

        return {
            "query": query,
            "anchors": anchors,
            "vector": vector_hits,
            "graph": graph_hits,
        }
