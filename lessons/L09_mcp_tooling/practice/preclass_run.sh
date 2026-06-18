#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LESSON_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
COURSE_ROOT="$(cd "$LESSON_DIR/../.." && pwd)"

source "$COURSE_ROOT/scripts/activate_course.sh"

cd "$COURSE_ROOT"
python scripts/check_env.py
python scripts/smoke_openai.py
python - <<'PY'
from mcp.server.fastmcp import FastMCP
from mcp import ClientSession, StdioServerParameters
print("[OK] MCP SDK imports")
PY

cd "$LESSON_DIR"
python practice/30_mcp_stdio_client.py
python practice/31_langchain_mcp_bridge.py
python practice/32_mcp_safety_checklist.py
python practice/33_mcp_sampling_flow.py

echo "[OK] L09 preclass run completed."
