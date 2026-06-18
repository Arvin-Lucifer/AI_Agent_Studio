#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LESSON_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
COURSE_ROOT="$(cd "$LESSON_DIR/../.." && pwd)"

source "$COURSE_ROOT/scripts/activate_course.sh"

if command -v python >/dev/null 2>&1; then
  PYTHON_BIN="python"
elif command -v python3 >/dev/null 2>&1; then
  PYTHON_BIN="python3"
else
  echo "[ERROR] Neither python nor python3 is available in PATH."
  exit 1
fi

export SMOKE_MAX_ATTEMPTS="${SMOKE_MAX_ATTEMPTS:-3}"
export SMOKE_REQUEST_TIMEOUT_SEC="${SMOKE_REQUEST_TIMEOUT_SEC:-30}"
export SMOKE_RETRY_BACKOFF_SEC="${SMOKE_RETRY_BACKOFF_SEC:-2}"

export LCEL_MAX_RETRIES="${LCEL_MAX_RETRIES:-1}"
export LCEL_REQUEST_TIMEOUT_SEC="${LCEL_REQUEST_TIMEOUT_SEC:-60}"

cd "$COURSE_ROOT"
# 先确认通用环境和模型网关可用。
"$PYTHON_BIN" scripts/check_env.py
"$PYTHON_BIN" scripts/smoke_openai.py

cd "$LESSON_DIR"
# 覆盖 LCEL 基础、Parser、Retriever、Callback 和综合案例。
"$PYTHON_BIN" practice/15_lcel_basics.py
"$PYTHON_BIN" practice/17_output_parsers.py --mode json
"$PYTHON_BIN" practice/18_custom_retriever.py --query "Python 装饰器怎么用？"
"$PYTHON_BIN" practice/19_callbacks.py
"$PYTHON_BIN" practice/20_doc_processor_agent.py

echo "[OK] L06 preclass run completed."
