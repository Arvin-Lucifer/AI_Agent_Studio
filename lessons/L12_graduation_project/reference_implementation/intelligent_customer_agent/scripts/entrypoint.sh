#!/usr/bin/env bash
set -euo pipefail

mkdir -p data/knowledge_base logs

if [ ! -s data/memory.json ]; then
  printf '{}\n' > data/memory.json
fi

touch data/tickets.jsonl data/knowledge_gaps.jsonl logs/events.ndjson

python scripts/build_kb.py

exec uvicorn intelligent_customer.api:app --host 0.0.0.0 --port "${PORT:-8011}"
