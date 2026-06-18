from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from intelligent_customer.graph import run_agent
from intelligent_customer.rag.kb_builder import build_kb_index
from intelligent_customer.rag.retriever import clear_index_cache
from intelligent_customer.schemas import ChatResponse
from intelligent_customer.tools.memory_tool import reset_memory


EVAL_DIR = Path(__file__).resolve().parent
DATASET_PATH = EVAL_DIR / "eval_dataset.jsonl"
REPORT_PATH = EVAL_DIR / "eval_report.json"


class _OfflineEvalMode:
    def __enter__(self) -> None:
        self._previous = os.environ.get("USE_LLM_ANSWERS")
        os.environ["USE_LLM_ANSWERS"] = "0"

    def __exit__(self, exc_type: object, exc: object, tb: object) -> None:
        if self._previous is None:
            os.environ.pop("USE_LLM_ANSWERS", None)
        else:
            os.environ["USE_LLM_ANSWERS"] = self._previous


def load_dataset(path: Path = DATASET_PATH) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


def _keyword_hit(reply: str, keywords: list[str]) -> bool:
    if not keywords:
        return True
    normalized = reply.lower()
    return any(keyword.lower() in normalized for keyword in keywords)


def evaluate_cases(cases: list[dict[str, Any]]) -> dict[str, Any]:
    with _OfflineEvalMode():
        build_kb_index()
        clear_index_cache()
        for session_id in sorted({case["session_id"] for case in cases}):
            reset_memory(session_id)

        results: list[dict[str, Any]] = []
        counters = {
            "intent": 0,
            "route": 0,
            "ticket": 0,
            "fallback": 0,
            "clarification": 0,
            "keyword": 0,
            "schema": 0,
        }

        for case in cases:
            response = run_agent(case["message"], session_id=case["session_id"], user_id="eval")
            schema_ok = isinstance(response, ChatResponse) and bool(response.trace_id)
            intent_ok = response.intent == case["expected_intent"]
            route_ok = response.route == case["expected_route"]
            ticket_ok = bool(response.ticket_id) == bool(case["expected_ticket"])
            fallback_ok = bool(response.need_human) == bool(case["expected_human"])
            clarification_ok = True
            if case["expected_route"] == "clarify":
                clarification_ok = "补充" in response.reply or "具体" in response.reply
            keyword_ok = _keyword_hit(response.reply, case.get("expected_keywords", []))

            counters["schema"] += int(schema_ok)
            counters["intent"] += int(intent_ok)
            counters["route"] += int(route_ok)
            counters["ticket"] += int(ticket_ok)
            counters["fallback"] += int(fallback_ok)
            counters["clarification"] += int(clarification_ok)
            counters["keyword"] += int(keyword_ok)

            results.append(
                {
                    "id": case["id"],
                    "intent": response.intent,
                    "route": response.route,
                    "ticket_id": response.ticket_id,
                    "need_human": response.need_human,
                    "confidence": response.confidence,
                    "checks": {
                        "schema": schema_ok,
                        "intent": intent_ok,
                        "route": route_ok,
                        "ticket": ticket_ok,
                        "fallback": fallback_ok,
                        "clarification": clarification_ok,
                        "keyword": keyword_ok,
                    },
                }
            )

    total = len(cases) or 1
    metrics = {
        "total": len(cases),
        "intent_accuracy": round(counters["intent"] / total, 4),
        "route_accuracy": round(counters["route"] / total, 4),
        "ticket_success_rate": round(counters["ticket"] / total, 4),
        "fallback_accuracy": round(counters["fallback"] / total, 4),
        "clarification_accuracy": round(counters["clarification"] / total, 4),
        "keyword_hit_rate": round(counters["keyword"] / total, 4),
        "schema_valid_rate": round(counters["schema"] / total, 4),
    }
    score_keys = [
        "intent_accuracy",
        "route_accuracy",
        "ticket_success_rate",
        "fallback_accuracy",
        "clarification_accuracy",
        "keyword_hit_rate",
        "schema_valid_rate",
    ]
    metrics["overall_score"] = round(sum(metrics[key] for key in score_keys) / len(score_keys), 4)
    return {"metrics": metrics, "results": results}


def run_eval() -> dict[str, Any]:
    report = evaluate_cases(load_dataset())
    REPORT_PATH.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    return {
        **report["metrics"],
        "cases": report["results"],
    }


def main() -> int:
    report = run_eval()
    metrics = {key: value for key, value in report.items() if key != "cases"}
    print(json.dumps(metrics, ensure_ascii=False, indent=2))
    print(f"Wrote {REPORT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
