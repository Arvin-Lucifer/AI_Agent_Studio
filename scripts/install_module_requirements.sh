#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 1 ]]; then
  echo "Usage: $0 <core|langchain|rag|deployment|all>"
  exit 1
fi

module="$1"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
COURSE_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
req_file="$COURSE_ROOT/requirements/${module}.txt"

if [[ ! -f "$req_file" ]]; then
  echo "Unknown module: $module"
  exit 1
fi

source "$COURSE_ROOT/scripts/activate_course.sh"
python -m pip install -r "$req_file"

echo "[OK] Installed requirements: $req_file"
