from __future__ import annotations

from intelligent_customer.harness.guardrails import evaluate_answer_policy, route_for_intent
from intelligent_customer.graph import run_agent
from intelligent_customer.tools.memory_tool import reset_memory


def test_complaint_intent_forced_to_ticket() -> None:
    assert route_for_intent("complaint") == "ticket"


def test_no_evidence_triggers_handoff_policy() -> None:
    route, reason = evaluate_answer_policy(evidence_count=0, confidence=0.0, message="知识库没有的问题")
    assert route == "human_handoff"
    assert reason == "no_evidence"


def test_low_confidence_ambiguous_triggers_clarify() -> None:
    route, reason = evaluate_answer_policy(evidence_count=1, confidence=0.01, message="这个怎么办")
    assert route == "clarify"
    assert reason == "low_confidence_ambiguous"


def test_out_of_scope_does_not_fabricate_answer() -> None:
    reset_memory("test_guardrail_oos")
    response = run_agent("帮我诊断一种疾病。", session_id="test_guardrail_oos")
    assert response.route == "human_handoff"
    assert response.need_human is True
    assert response.ticket_id
    assert not response.citations

