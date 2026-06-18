from __future__ import annotations

import re
from typing import Any


PHONE_RE = re.compile(r"(?<!\d)(1[3-9]\d)(\d{4})(\d{4})(?!\d)")
EMAIL_RE = re.compile(r"([A-Za-z0-9._%+-]{1,3})[A-Za-z0-9._%+-]*(@[A-Za-z0-9.-]+\.[A-Za-z]{2,})")
LONG_NUMBER_RE = re.compile(r"(?<![A-Za-z0-9])(\d{4})\d{4,}(\d{2,4})(?![A-Za-z0-9])")


def mask_sensitive_text(text: str) -> str:
    masked = PHONE_RE.sub(r"\1****\3", text)
    masked = EMAIL_RE.sub(r"\1***\2", masked)
    masked = LONG_NUMBER_RE.sub(r"\1****\2", masked)
    return masked


def sanitize_value(value: Any) -> Any:
    if isinstance(value, str):
        return mask_sensitive_text(value)
    if isinstance(value, list):
        return [sanitize_value(item) for item in value]
    if isinstance(value, tuple):
        return tuple(sanitize_value(item) for item in value)
    if isinstance(value, dict):
        return {key: sanitize_value(item) for key, item in value.items()}
    return value


def sanitize_fields(fields: dict[str, Any]) -> dict[str, Any]:
    return {key: sanitize_value(value) for key, value in fields.items()}
