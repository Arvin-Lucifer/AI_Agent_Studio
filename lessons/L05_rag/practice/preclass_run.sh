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

export RAG_MAX_ATTEMPTS="${RAG_MAX_ATTEMPTS:-2}"
export RAG_REQUEST_TIMEOUT_SEC="${RAG_REQUEST_TIMEOUT_SEC:-60}"
export RAG_RETRY_BACKOFF_SEC="${RAG_RETRY_BACKOFF_SEC:-2}"

cd "$COURSE_ROOT"
# 先确认全局环境和模型网关可用。
"$PYTHON_BIN" scripts/check_env.py
"$PYTHON_BIN" scripts/smoke_openai.py

cd "$LESSON_DIR"
# 依次验证知识库生成、索引构建、检索增强回答和 chunk 对比。
"$PYTHON_BIN" practice/11_prepare_knowledge_base.py
"$PYTHON_BIN" practice/12_build_local_index.py --query "年假有几天？"
"$PYTHON_BIN" practice/13_rag_agent.py --question "我入职2年了，有几天年假？" --show-context
"$PYTHON_BIN" practice/14_chunking_compare.py

echo "[OK] L05 preclass run completed."
