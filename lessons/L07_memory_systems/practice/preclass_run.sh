#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LESSON_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
COURSE_ROOT="$(cd "$LESSON_DIR/../.." && pwd)"

source "$COURSE_ROOT/scripts/activate_course.sh"

cd "$COURSE_ROOT"

python scripts/check_env.py
python scripts/smoke_openai.py

cd "$LESSON_DIR"

python practice/21_memory_window.py --max-turns 3 --total-turns 8
python practice/22_memory_summary.py --max-recent 4
python practice/23_long_term_memory_json.py --reset --query Python
python practice/24_hybrid_memory_graph.py --reset --query Python --anchor 小明

echo "[OK] L07 preclass run completed."
