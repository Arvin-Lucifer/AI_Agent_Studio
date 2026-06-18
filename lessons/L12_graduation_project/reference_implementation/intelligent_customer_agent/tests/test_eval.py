from __future__ import annotations

import os

import pytest

from evals.run_eval import evaluate_cases, load_dataset


def test_eval_dataset_can_load() -> None:
    cases = load_dataset()
    assert len(cases) >= 20
    assert {"id", "message", "expected_intent", "expected_route"}.issubset(cases[0])


def test_eval_outputs_metrics_for_subset() -> None:
    cases = load_dataset()[:5]
    report = evaluate_cases(cases)
    metrics = report["metrics"]
    assert metrics["total"] == 5
    assert "intent_accuracy" in metrics
    assert "overall_score" in metrics


def test_eval_restores_llm_answer_flag(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("USE_LLM_ANSWERS", "1")
    evaluate_cases(load_dataset()[:1])
    assert os.environ["USE_LLM_ANSWERS"] == "1"
