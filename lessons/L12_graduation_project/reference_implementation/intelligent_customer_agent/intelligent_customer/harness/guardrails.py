from __future__ import annotations

from intelligent_customer.config import MIN_CONFIDENCE
from intelligent_customer.schemas import Intent, Route


AMBIGUOUS_WORDS = ["这个", "那个", "怎么弄", "怎么办", "有问题", "帮我看看", "处理一下", "不了解"]


def route_for_intent(intent: Intent) -> Route:
    if intent == "complaint":
        return "ticket"
    if intent == "unclear":
        return "clarify"
    if intent == "out_of_scope":
        return "human_handoff"
    if intent in {"qa", "consult"}:
        return "retrieve"
    return "human_handoff"


def is_ambiguous_message(message: str) -> bool:
    compact = message.strip()
    if len(compact) <= 4:
        return True
    return any(word in compact for word in AMBIGUOUS_WORDS)


def evaluate_answer_policy(evidence_count: int, confidence: float, message: str) -> tuple[str, str]:
    if evidence_count <= 0:
        return "human_handoff", "no_evidence"
    if confidence < MIN_CONFIDENCE:
        if is_ambiguous_message(message):
            return "clarify", "low_confidence_ambiguous"
        return "human_handoff", "low_confidence"
    return "final", "pass"


def guardrail_summary(intent: Intent, route: Route, evidence_count: int, confidence: float) -> dict[str, object]:
    return {
        "complaint_forced_ticket": intent != "complaint" or route == "ticket",
        "has_evidence": evidence_count > 0,
        "confidence_pass": confidence >= MIN_CONFIDENCE,
        "min_confidence": MIN_CONFIDENCE,
    }
