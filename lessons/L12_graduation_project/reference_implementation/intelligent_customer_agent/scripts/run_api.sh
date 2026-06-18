#!/usr/bin/env bash
set -euo pipefail

PORT="${PORT:-8011}"
RELOAD="${RELOAD:-1}"

if [ "$RELOAD" = "0" ]; then
  exec uvicorn intelligent_customer.api:app --host 0.0.0.0 --port "$PORT"
fi

exec uvicorn intelligent_customer.api:app \
  --host 0.0.0.0 \
  --port "$PORT" \
  --reload \
  --reload-dir intelligent_customer \
  --reload-dir web
