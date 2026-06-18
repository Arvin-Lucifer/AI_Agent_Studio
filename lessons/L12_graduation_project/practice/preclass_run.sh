#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LESSON_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
PROJECT_DIR="$LESSON_DIR/reference_implementation/intelligent_customer_agent"

cd "$PROJECT_DIR"

echo "[L12] Building knowledge base index..."
python scripts/build_kb.py

echo "[L12] Compiling reference implementation..."
find intelligent_customer evals scripts -name "*.py" -print0 | xargs -0 python -m py_compile

echo "[L12] Running tests..."
python -m pytest -q

echo "[L12] Running quality evaluation..."
python evals/run_eval.py

echo "[OK] L12 graduation project reference implementation passed."

