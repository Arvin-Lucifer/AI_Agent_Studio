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

export TOOL_MAX_ATTEMPTS="${TOOL_MAX_ATTEMPTS:-3}"
export TOOL_REQUEST_TIMEOUT_SEC="${TOOL_REQUEST_TIMEOUT_SEC:-40}"
export TOOL_RETRY_BACKOFF_SEC="${TOOL_RETRY_BACKOFF_SEC:-2}"

cd "$COURSE_ROOT"
# 全局检查先跑通，再验证工具调用链路。
"$PYTHON_BIN" scripts/check_env.py
"$PYTHON_BIN" scripts/smoke_openai.py

cd "$LESSON_DIR"
# 分别覆盖单工具调用和多工具并发调用两条路径。
"$PYTHON_BIN" practice/05_function_calling.py "北京今天天气怎么样？"
"$PYTHON_BIN" practice/06_parallel_function_calling.py "现在几点了？北京天气怎么样？再帮我算一下 (17 * 23) + (45 / 9)。"

echo "[OK] L03 preclass run completed."
