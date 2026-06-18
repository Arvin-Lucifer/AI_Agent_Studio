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

export LC_MAX_RETRIES="${LC_MAX_RETRIES:-2}"
export LC_REQUEST_TIMEOUT_SEC="${LC_REQUEST_TIMEOUT_SEC:-45}"

cd "$COURSE_ROOT"
# 先检查通用环境和模型网关，再进入 LangChain 示例。
"$PYTHON_BIN" scripts/check_env.py
"$PYTHON_BIN" scripts/smoke_openai.py

cd "$LESSON_DIR"
# 08 不调用模型，只展示工具 schema，适合作为快速静态检查。
"$PYTHON_BIN" practice/08_custom_tools.py --describe

# 07 和 10 分别验证基础工具 Agent 与搜索 Agent 的非交互式调用。
"$PYTHON_BIN" practice/07_langchain_agent.py "北京天气怎么样？再帮我算一下 (12 + 8) * 3。"
"$PYTHON_BIN" practice/10_search_agent.py --question "请先搜索一下 AI Agent 有哪些典型应用？"

echo "[OK] L04 preclass run completed."
