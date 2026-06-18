from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from intelligent_customer.config import KB_DIR, KB_INDEX_PATH


KNOWN_TERMS = [
    "注册", "登录", "密码", "找回密码", "验证码", "账号", "订单", "发票", "支付", "退款",
    "退换货", "隐私", "数据", "安全", "开通", "首次使用", "高级功能", "自动化",
    "登录失败", "支付失败", "订单异常", "套餐", "价格", "sla", "售后", "人工客服",
    "企业版", "专业版", "免费版", "同步", "报表", "权限", "投诉", "工单",
    "扣款", "未支付", "对公转账", "删除账号", "删除", "到账", "订单异常",
]


@dataclass
class KnowledgeDocument:
    source_id: str
    title: str
    collection: str
    updated_at: str
    path: str
    content: str
    tokens: list[str]


def parse_frontmatter(raw: str) -> tuple[dict[str, str], str]:
    if not raw.startswith("---"):
        return {}, raw
    parts = raw.split("---", 2)
    if len(parts) < 3:
        return {}, raw
    metadata: dict[str, str] = {}
    for line in parts[1].splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            metadata[key.strip()] = value.strip()
    return metadata, parts[2].strip()


def tokenize(text: str) -> list[str]:
    lowered = text.lower()
    tokens = re.findall(r"[a-z0-9]+|[\u4e00-\u9fff]", lowered)
    chinese = "".join(re.findall(r"[\u4e00-\u9fff]", lowered))
    bigrams = [chinese[i : i + 2] for i in range(max(0, len(chinese) - 1))]
    trigrams = [chinese[i : i + 3] for i in range(max(0, len(chinese) - 2))]
    known = [term.lower() for term in KNOWN_TERMS if term.lower() in lowered]
    return tokens + bigrams + trigrams + known


def build_kb_index(kb_dir: Path = KB_DIR, output_path: Path = KB_INDEX_PATH) -> dict[str, Any]:
    docs: list[KnowledgeDocument] = []
    for path in sorted(kb_dir.glob("*.md")):
        raw = path.read_text(encoding="utf-8")
        metadata, body = parse_frontmatter(raw)
        title = metadata.get("title") or path.stem
        collection = metadata.get("collection") or path.stem.split("_", 1)[0]
        source_id = metadata.get("source_id") or path.stem
        updated_at = metadata.get("updated_at") or ""
        doc_text = f"{title}\n{body}".strip()
        docs.append(
            KnowledgeDocument(
                source_id=source_id,
                title=title,
                collection=collection,
                updated_at=updated_at,
                path=str(path.relative_to(kb_dir.parent.parent)),
                content=body,
                tokens=tokenize(doc_text),
            )
        )

    index = {
        "version": 1,
        "doc_count": len(docs),
        "documents": [doc.__dict__ for doc in docs],
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(index, ensure_ascii=False, indent=2), encoding="utf-8")
    return index
