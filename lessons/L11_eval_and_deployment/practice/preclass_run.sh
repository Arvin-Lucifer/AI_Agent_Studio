#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LESSON_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
COURSE_ROOT="$(cd "$LESSON_DIR/../.." && pwd)"

source "$COURSE_ROOT/scripts/activate_course.sh"

cd "$COURSE_ROOT"
python scripts/check_env.py

cd "$LESSON_DIR"
python practice/44_eval_dataset.py
python practice/45_eval_runner.py
python practice/46_failure_tuning_playbook.py
python practice/47_agent_api.py --self-test
python practice/48_agent_api_streaming.py --self-test
python practice/49_cost_monitor.py
python practice/50_safety_guardrails.py

echo "[OK] L11 preclass run completed."
