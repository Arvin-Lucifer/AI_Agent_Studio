import importlib
import os
import platform
import sys

from dotenv import load_dotenv


def mask_secret(value: str) -> str:
    if not value:
        return "<unset>"
    if len(value) <= 8:
        return "***"
    return value[:4] + "..." + value[-4:]


def check_imports(modules):
    results = []
    for mod in modules:
        try:
            importlib.import_module(mod)
            results.append((mod, True, "ok"))
        except Exception as exc:
            results.append((mod, False, f"{type(exc).__name__}: {exc}"))
    return results


def main():
    load_dotenv()

    print("=== Runtime ===")
    print(f"Python: {sys.version.split()[0]}")
    print(f"Platform: {platform.platform()}")
    print(f"Executable: {sys.executable}")

    print("\n=== Environment Variables ===")
    api_key = os.getenv("OPENAI_API_KEY", "")
    base_url = os.getenv("OPENAI_BASE_URL", "")
    model = os.getenv("OPENAI_MODEL", "")
    print(f"OPENAI_API_KEY: {mask_secret(api_key)}")
    print(f"OPENAI_BASE_URL: {base_url or '<unset>'}")
    print(f"OPENAI_MODEL: {model or '<unset>'}")

    print("\n=== Imports ===")
    modules = [
        "openai",
        "dotenv",
        "rich",
        "fastapi",
        "langchain",
        "langchain_openai",
        "langgraph",
    ]
    for mod, ok, detail in check_imports(modules):
        status = "OK" if ok else "MISSING"
        print(f"{mod:<12} {status}  {detail}")


if __name__ == "__main__":
    main()
