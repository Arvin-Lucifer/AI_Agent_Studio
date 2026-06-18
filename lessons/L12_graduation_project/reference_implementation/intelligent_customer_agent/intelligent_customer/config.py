from __future__ import annotations

import os
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
ENV_PATH = PROJECT_ROOT / ".env"
DATA_DIR = PROJECT_ROOT / "data"
KB_DIR = DATA_DIR / "knowledge_base"
KB_INDEX_PATH = DATA_DIR / "kb_index.json"
MEMORY_PATH = DATA_DIR / "memory.json"
TICKETS_PATH = DATA_DIR / "tickets.jsonl"
KNOWLEDGE_GAPS_PATH = DATA_DIR / "knowledge_gaps.jsonl"
LOG_DIR = PROJECT_ROOT / "logs"
EVENTS_PATH = LOG_DIR / "events.ndjson"
METRICS_PATH = LOG_DIR / "metrics.json"


def _load_dotenv(path: Path = ENV_PATH) -> None:
    if not path.exists():
        return
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


_load_dotenv()

MIN_CONFIDENCE = float(os.getenv("MIN_CONFIDENCE", "0.28"))
TOP_K = int(os.getenv("RAG_TOP_K", "4"))
MAX_HISTORY_MESSAGES = int(os.getenv("MAX_HISTORY_MESSAGES", "20"))

LLM_MODEL = os.getenv("LLM_MODEL") or os.getenv("OPENAI_MODEL", "mock-rule-based")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "")
LLM_TIMEOUT_SECONDS = float(os.getenv("LLM_TIMEOUT_SECONDS", "5"))
ADMIN_API_KEY = os.getenv("ADMIN_API_KEY", "")
RATE_LIMIT_PER_MINUTE = int(os.getenv("RATE_LIMIT_PER_MINUTE", "60"))


def llm_answers_enabled() -> bool:
    value = os.getenv("USE_LLM_ANSWERS", "").strip().lower()
    if value in {"0", "false", "no", "off"}:
        return False
    if value in {"1", "true", "yes", "on"}:
        return bool(OPENAI_API_KEY)
    return False


def ensure_runtime_dirs() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    KB_DIR.mkdir(parents=True, exist_ok=True)
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    if not MEMORY_PATH.exists():
        MEMORY_PATH.write_text("{}", encoding="utf-8")
    if not TICKETS_PATH.exists():
        TICKETS_PATH.write_text("", encoding="utf-8")
    if not KNOWLEDGE_GAPS_PATH.exists():
        KNOWLEDGE_GAPS_PATH.write_text("", encoding="utf-8")
    if not EVENTS_PATH.exists():
        EVENTS_PATH.write_text("", encoding="utf-8")
