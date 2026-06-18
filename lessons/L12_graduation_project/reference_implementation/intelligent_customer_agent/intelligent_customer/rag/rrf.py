from __future__ import annotations

from typing import Any


def reciprocal_rank_fusion(result_lists: list[list[dict[str, Any]]], k: int = 60) -> list[dict[str, Any]]:
    fused: dict[str, dict[str, Any]] = {}
    for results in result_lists:
        for rank, item in enumerate(results, start=1):
            key = item["source_id"]
            current = fused.setdefault(key, {**item, "rrf_score": 0.0})
            current["rrf_score"] += 1.0 / (k + rank)
            current["score"] = max(float(current.get("score", 0.0)), float(item.get("score", 0.0)))
    return sorted(fused.values(), key=lambda item: item["rrf_score"], reverse=True)
