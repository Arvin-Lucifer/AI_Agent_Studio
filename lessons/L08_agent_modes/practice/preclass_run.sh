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
python practice/26_supervisor_research_team.py --topic "企业知识库问答助手设计"
python practice/27_agent_mode_router.py --question "P0工单响应时间和API发布审批有什么共同要求？"
python practice/28_multi_index_retrieval.py --query "API发布需要几人审批？"

echo "[OK] L08 preclass run completed."
