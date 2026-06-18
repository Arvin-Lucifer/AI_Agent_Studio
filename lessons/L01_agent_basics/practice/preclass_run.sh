#!/usr/bin/env bash
set -euo pipefail

# Must be sourced so conda env activation persists in this shell.
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

# More resilient defaults for unstable network/proxy environments.
export SMOKE_MAX_ATTEMPTS="${SMOKE_MAX_ATTEMPTS:-3}"
export SMOKE_REQUEST_TIMEOUT_SEC="${SMOKE_REQUEST_TIMEOUT_SEC:-30}"
export SMOKE_RETRY_BACKOFF_SEC="${SMOKE_RETRY_BACKOFF_SEC:-2}"

export HELLO_MAX_ATTEMPTS="${HELLO_MAX_ATTEMPTS:-3}"
export HELLO_REQUEST_TIMEOUT_SEC="${HELLO_REQUEST_TIMEOUT_SEC:-30}"
export HELLO_RETRY_BACKOFF_SEC="${HELLO_RETRY_BACKOFF_SEC:-2}"

export DEMO_MAX_ATTEMPTS="${DEMO_MAX_ATTEMPTS:-3}"
export DEMO_REQUEST_TIMEOUT_SEC="${DEMO_REQUEST_TIMEOUT_SEC:-40}"
export DEMO_RETRY_BACKOFF_SEC="${DEMO_RETRY_BACKOFF_SEC:-2}"

cd "$COURSE_ROOT"
# 先做全局环境和 API 连通性检查，再进入本讲练习脚本。
"$PYTHON_BIN" scripts/check_env.py
"$PYTHON_BIN" scripts/smoke_openai.py

cd "$LESSON_DIR"
# L01 验证最小 LLM 调用，以及 ChatBot 与 Agent 思维流程差异。
"$PYTHON_BIN" practice/01_hello_llm.py
"$PYTHON_BIN" practice/demo_chatbot_vs_agent.py --mode both

echo "[OK] L01 preclass run completed."
