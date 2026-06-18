#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_DIR"

ENV_NAME="${CONDA_ENV_NAME:-agent_course}"

mkdir -p data/knowledge_base logs evals tests web docs scripts
touch data/memory.json data/tickets.jsonl data/knowledge_gaps.jsonl logs/events.ndjson

if [ ! -s data/memory.json ]; then
  printf '{}\n' > data/memory.json
fi

if command -v conda >/dev/null 2>&1; then
  if conda env list | awk '{print $1}' | grep -qx "$ENV_NAME"; then
    echo "Using existing conda env: $ENV_NAME"
    conda run -n "$ENV_NAME" python -m pip install -r requirements.txt
  else
    echo "Creating conda env: $ENV_NAME"
    conda create -y -n "$ENV_NAME" python=3.11
    conda run -n "$ENV_NAME" python -m pip install -r requirements.txt
  fi
  echo
  echo "Activate before running project commands:"
  echo "  conda activate $ENV_NAME"
else
  PYTHON_BIN="${PYTHON_BIN:-python3}"
  if ! command -v "$PYTHON_BIN" >/dev/null 2>&1; then
    echo "python3 not found and conda not found. Please install Python 3.11+." >&2
    exit 1
  fi
  "$PYTHON_BIN" -m pip install -r requirements.txt
fi

echo
echo "Next commands:"
echo "  python scripts/build_kb.py"
echo "  pytest -q"
echo "  python evals/run_eval.py"
echo "  bash scripts/run_api.sh"
