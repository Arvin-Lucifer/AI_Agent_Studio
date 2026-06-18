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
python practice/34_skill_loader.py
python practice/35_weather_skill_agent.py --query "北京今天天气怎么样？适合出门吗？"
python practice/36_code_review_skill.py
python practice/37_office_skill_router.py
python practice/42_retry_strategy_layering.py --scenario network_timeout
python practice/43_parallel_tail_latency.py --scenario critical_path
python practice/41_auto_send_authorization.py --scenario daily_report
python practice/39_web_instruction_boundary.py --scenario mixed_prompt_injection
python practice/40_high_risk_skill_incident_response.py --scenario internal_email
python practice/38_model_rollback_playbook.py --scenario skill_regression

echo "[OK] L10 preclass run completed."
