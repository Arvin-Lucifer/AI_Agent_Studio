from __future__ import annotations

import os
import time
from collections import defaultdict, deque

from fastapi import Header, HTTPException, Request

from intelligent_customer.config import RATE_LIMIT_PER_MINUTE


_REQUEST_BUCKETS: dict[str, deque[float]] = defaultdict(deque)


def require_admin_key(x_admin_key: str | None = Header(default=None)) -> None:
    expected = os.getenv("ADMIN_API_KEY", "")
    if not expected:
        return
    if x_admin_key != expected:
        raise HTTPException(status_code=401, detail="invalid admin key")


def check_rate_limit(identity: str, limit: int = RATE_LIMIT_PER_MINUTE) -> None:
    if limit <= 0:
        return
    now = time.time()
    bucket = _REQUEST_BUCKETS[identity]
    while bucket and now - bucket[0] > 60:
        bucket.popleft()
    if len(bucket) >= limit:
        raise HTTPException(status_code=429, detail="rate limit exceeded")
    bucket.append(now)


def request_identity(request: Request, fallback: str) -> str:
    forwarded = request.headers.get("x-forwarded-for", "").split(",", 1)[0].strip()
    client = forwarded or (request.client.host if request.client else "unknown")
    return f"{client}:{fallback}"
