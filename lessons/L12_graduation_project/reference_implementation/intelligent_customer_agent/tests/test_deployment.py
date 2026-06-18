from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_deployment_files_exist() -> None:
    for path in ["Dockerfile", "docker-compose.yml", ".dockerignore", "Makefile", "scripts/entrypoint.sh"]:
        assert (ROOT / path).exists()


def test_dockerfile_uses_project_api_entrypoint() -> None:
    dockerfile = (ROOT / "Dockerfile").read_text(encoding="utf-8")
    entrypoint = (ROOT / "scripts" / "entrypoint.sh").read_text(encoding="utf-8")
    compose = (ROOT / "docker-compose.yml").read_text(encoding="utf-8")
    assert "python:3.11-slim" in dockerfile
    assert "scripts/entrypoint.sh" in dockerfile
    assert "python scripts/build_kb.py" in entrypoint
    assert "intelligent_customer.api:app" in entrypoint
    assert "8011:8011" in compose
    assert "/health" in compose
    assert "env_file" not in compose
    assert "OPENAI_API_KEY" not in compose


def test_run_api_reload_scope_is_limited() -> None:
    script = (ROOT / "scripts" / "run_api.sh").read_text(encoding="utf-8")
    makefile = (ROOT / "Makefile").read_text(encoding="utf-8")
    assert "--reload-dir intelligent_customer" in script
    assert "--reload-dir web" in script
    assert 'RELOAD="${RELOAD:-1}"' in script
    assert '[ "$RELOAD" = "0" ]' in script
    assert "bash scripts/run_api.sh" in makefile
