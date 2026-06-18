#!/usr/bin/env bash
set -euo pipefail

# Must be sourced so conda activation persists in this shell context.
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

# Resilient defaults for unstable network/proxy environments.
export SMOKE_MAX_ATTEMPTS="${SMOKE_MAX_ATTEMPTS:-3}"
export SMOKE_REQUEST_TIMEOUT_SEC="${SMOKE_REQUEST_TIMEOUT_SEC:-30}"
export SMOKE_RETRY_BACKOFF_SEC="${SMOKE_RETRY_BACKOFF_SEC:-2}"

export STRUCTURED_MAX_ATTEMPTS="${STRUCTURED_MAX_ATTEMPTS:-3}"
export STRUCTURED_REQUEST_TIMEOUT_SEC="${STRUCTURED_REQUEST_TIMEOUT_SEC:-40}"
export STRUCTURED_RETRY_BACKOFF_SEC="${STRUCTURED_RETRY_BACKOFF_SEC:-2}"

export ITER_MAX_ATTEMPTS="${ITER_MAX_ATTEMPTS:-3}"
export ITER_REQUEST_TIMEOUT_SEC="${ITER_REQUEST_TIMEOUT_SEC:-40}"
export ITER_RETRY_BACKOFF_SEC="${ITER_RETRY_BACKOFF_SEC:-2}"

cd "$COURSE_ROOT"
# 先确认课程环境和模型网关可用，避免后面的 prompt 实验误判。
"$PYTHON_BIN" scripts/check_env.py
"$PYTHON_BIN" scripts/smoke_openai.py

cd "$LESSON_DIR"
# L02 验证结构化输出解析，以及 V1/V2 prompt 迭代对比。
"$PYTHON_BIN" practice/03_structured_output.py
"$PYTHON_BIN" practice/04_prompt_iteration.py

echo "[OK] L02 preclass run completed."
