from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from intelligent_customer.config import PROJECT_ROOT
from intelligent_customer.harness.file_lock import locked_path
from intelligent_customer.harness.privacy import mask_sensitive_text


EVAL_DIR = PROJECT_ROOT / "evals"
DATASET_PATH = EVAL_DIR / "eval_dataset.jsonl"
REPORT_PATH = EVAL_DIR / "eval_report.json"
GENERATED_CASES_PATH = EVAL_DIR / "generated_eval_cases.jsonl"


def _relative(path: Path) -> str:
    return path.relative_to(PROJECT_ROOT).as_posix()


def _dataset_count() -> int:
    if not DATASET_PATH.exists():
        return 0
    return sum(1 for line in DATASET_PATH.read_text(encoding="utf-8").splitlines() if line.strip())


def _jsonl_rows(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return rows


def _write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def _mtime_iso(path: Path) -> str | None:
    if not path.exists():
        return None
    return datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc).isoformat()


def normalize_eval_report(report: dict[str, Any]) -> dict[str, Any]:
    metrics = report.get("metrics")
    results = report.get("results")
    if metrics is None:
        metrics = {key: value for key, value in report.items() if key != "cases"}
    if results is None:
        results = report.get("cases", [])
    failures = [
        item
        for item in results
        if not all(bool(value) for value in item.get("checks", {}).values())
    ]
    return {
        "status": "ok",
        "generated_at": _mtime_iso(REPORT_PATH),
        "dataset_cases": _dataset_count(),
        "report_path": _relative(REPORT_PATH),
        "dataset_path": _relative(DATASET_PATH),
        "metrics": metrics,
        "failure_count": len(failures),
        "results": results,
    }


def load_eval_report() -> dict[str, Any]:
    if not REPORT_PATH.exists():
        return {
            "status": "missing",
            "generated_at": None,
            "dataset_cases": _dataset_count(),
            "report_path": _relative(REPORT_PATH),
            "dataset_path": _relative(DATASET_PATH),
            "metrics": {},
            "failure_count": 0,
            "results": [],
        }
    report = json.loads(REPORT_PATH.read_text(encoding="utf-8"))
    return normalize_eval_report(report)


def run_quality_eval() -> dict[str, Any]:
    from evals.run_eval import run_eval

    run_eval()
    return load_eval_report()


def list_generated_eval_cases(limit: int = 100) -> dict[str, Any]:
    with locked_path(GENERATED_CASES_PATH):
        rows = _jsonl_rows(GENERATED_CASES_PATH)
    return {
        "cases": rows[-max(1, min(limit, 500)) :][::-1],
        "total": len(rows),
        "path": _relative(GENERATED_CASES_PATH),
    }


def create_eval_case_from_gap(gap: dict[str, Any]) -> dict[str, Any]:
    gap_id = str(gap["gap_id"])
    message = mask_sensitive_text(str(gap.get("last_message") or gap.get("message") or ""))
    route = str(gap.get("route") or "human_handoff")
    intent = str(gap.get("intent") or ("out_of_scope" if route == "human_handoff" else "qa"))
    expected_human = route in {"human_handoff", "ticket"} or gap.get("reason") in {"needs_human", "negative_feedback"}
    expected_ticket = route in {"human_handoff", "ticket"}
    case = {
        "id": f"generated_{gap_id}",
        "source_gap_id": gap_id,
        "status": "draft",
        "review_required": True,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "message": message,
        "session_id": f"generated_{gap_id}",
        "expected_intent": intent,
        "expected_route": route if route in {"retrieve", "clarify", "ticket", "human_handoff", "final"} else "human_handoff",
        "expected_keywords": [],
        "expected_ticket": expected_ticket,
        "expected_human": expected_human,
        "notes": "由 knowledge gap 自动生成，请人工确认 expected_* 字段后再合入主评测集。",
    }
    with locked_path(GENERATED_CASES_PATH):
        rows = _jsonl_rows(GENERATED_CASES_PATH)
        rows = [row for row in rows if row.get("source_gap_id") != gap_id]
        rows.append(case)
        _write_jsonl(GENERATED_CASES_PATH, rows)
    return case
