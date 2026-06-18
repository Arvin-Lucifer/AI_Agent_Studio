#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
COURSE_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
ENV_NAME="${CONDA_ENV_NAME:-agent_course}"

if command -v conda >/dev/null 2>&1; then
  eval "$(conda shell.bash hook)"
elif [[ -n "${CONDA_EXE:-}" ]]; then
  source "$(dirname "$(dirname "$CONDA_EXE")")/etc/profile.d/conda.sh"
elif [[ -f "$HOME/miniconda3/etc/profile.d/conda.sh" ]]; then
  source "$HOME/miniconda3/etc/profile.d/conda.sh"
elif [[ -f "$HOME/anaconda3/etc/profile.d/conda.sh" ]]; then
  source "$HOME/anaconda3/etc/profile.d/conda.sh"
else
  echo "[ERROR] Conda was not found. Please install Miniconda/Anaconda or initialize conda first." >&2
  return 1 2>/dev/null || exit 1
fi

conda activate "$ENV_NAME"
cd "$COURSE_ROOT"

echo "[OK] Activated conda env: $ENV_NAME"
echo "[OK] Workspace: $COURSE_ROOT"
python --version
