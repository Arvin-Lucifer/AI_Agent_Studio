import os
import time

from dotenv import load_dotenv
from openai import APIConnectionError, APIStatusError, APITimeoutError, OpenAI, RateLimitError


def _read_int_env(name: str, default: int) -> int:
    raw = os.getenv(name, "").strip()
    if not raw:
        return default
    try:
        value = int(raw)
        if value < 1:
            raise ValueError("must be >= 1")
        return value
    except Exception:
        print(f"[WARN] Invalid {name}={raw!r}, fallback to {default}")
        return default


def _read_float_env(name: str, default: float) -> float:
    raw = os.getenv(name, "").strip()
    if not raw:
        return default
    try:
        value = float(raw)
        if value <= 0:
            raise ValueError("must be > 0")
        return value
    except Exception:
        print(f"[WARN] Invalid {name}={raw!r}, fallback to {default}")
        return default


def main():
    load_dotenv()

    api_key = os.getenv("OPENAI_API_KEY")
    base_url = os.getenv("OPENAI_BASE_URL")
    model = os.getenv("OPENAI_MODEL", "gpt-5.3-codex")

    if not api_key:
        raise SystemExit("OPENAI_API_KEY is missing. Please set it in .env")
    if not base_url:
        raise SystemExit("OPENAI_BASE_URL is missing. Please set it in .env")

    max_attempts = _read_int_env("SMOKE_MAX_ATTEMPTS", 3)
    request_timeout = _read_float_env("SMOKE_REQUEST_TIMEOUT_SEC", 30.0)
    backoff_sec = _read_float_env("SMOKE_RETRY_BACKOFF_SEC", 2.0)

    client = OpenAI(api_key=api_key, base_url=base_url)

    for attempt in range(1, max_attempts + 1):
        try:
            resp = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are a concise assistant."},
                    {"role": "user", "content": "Reply with exactly: setup_ok"},
                ],
                temperature=0,
                timeout=request_timeout,
            )
            print(resp.choices[0].message.content)
            return
        except (APITimeoutError, APIConnectionError, RateLimitError) as exc:
            if attempt == max_attempts:
                raise
            sleep_sec = backoff_sec * attempt
            print(
                f"[WARN] attempt {attempt}/{max_attempts} failed: "
                f"{type(exc).__name__}. Retry in {sleep_sec:.1f}s ..."
            )
            time.sleep(sleep_sec)
        except APIStatusError as exc:
            # Retry only transient server-side errors.
            if exc.status_code is not None and exc.status_code >= 500 and attempt < max_attempts:
                sleep_sec = backoff_sec * attempt
                print(
                    f"[WARN] attempt {attempt}/{max_attempts} failed: "
                    f"APIStatusError({exc.status_code}). Retry in {sleep_sec:.1f}s ..."
                )
                time.sleep(sleep_sec)
                continue
            raise


if __name__ == "__main__":
    main()
