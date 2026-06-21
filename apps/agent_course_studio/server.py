#!/usr/bin/env python3
"""Local server for AgentCraft Studio.

The server intentionally stays small: it serves the static web app and exposes a
single optional whitelist runner endpoint. Real command execution is disabled by
default and must be explicitly enabled with AGENT_COURSE_STUDIO_ALLOW_RUN=1.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import time
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

from build_course_data import APP_DIR, COURSE_ROOT, OUTPUT_PATH, build


WEB_DIR = APP_DIR / "web"
RUN_TIMEOUT_SEC = int(os.getenv("AGENT_COURSE_STUDIO_RUN_TIMEOUT_SEC", "180"))


def load_course_data() -> dict[str, Any]:
    if not OUTPUT_PATH.exists():
        data = build()
        OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        return data
    return json.loads(OUTPUT_PATH.read_text(encoding="utf-8"))


def lesson_by_id(lesson_id: str) -> dict[str, Any] | None:
    for lesson in load_course_data().get("lessons", []):
        if lesson.get("id") == lesson_id:
            return lesson
    return None


class StudioHandler(SimpleHTTPRequestHandler):
    server_version = "AgentCourseStudio/1.0"

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, directory=str(WEB_DIR), **kwargs)

    def end_headers(self) -> None:
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def do_GET(self) -> None:  # noqa: N802 - http.server uses this name
        if self.path == "/api/health":
            self.write_json({"ok": True, "runnerEnabled": runner_enabled()})
            return
        if self.path == "/api/course":
            self.write_json(load_course_data())
            return
        super().do_GET()

    def do_POST(self) -> None:  # noqa: N802 - http.server uses this name
        if self.path != "/api/runs":
            self.write_json({"error": "Not found"}, status=HTTPStatus.NOT_FOUND)
            return

        payload = self.read_json_body()
        lesson_id = str(payload.get("lessonId", ""))
        lesson = lesson_by_id(lesson_id)
        if not lesson:
            self.write_json({"error": f"Unknown lesson: {lesson_id}"}, status=HTTPStatus.BAD_REQUEST)
            return

        command = lesson.get("preclassCommand") or ""
        lesson_dir = COURSE_ROOT / "lessons" / lesson_id
        if not command or not (lesson_dir / "practice" / "preclass_run.sh").exists():
            self.write_json({"error": "This lesson has no preclass runner."}, status=HTTPStatus.BAD_REQUEST)
            return

        if not runner_enabled():
            self.write_json(
                {
                    "ok": False,
                    "runnerEnabled": False,
                    "message": "真实执行默认关闭。设置 AGENT_COURSE_STUDIO_ALLOW_RUN=1 后重启服务即可启用。",
                    "command": command,
                },
                status=HTTPStatus.FORBIDDEN,
            )
            return

        started = time.time()
        try:
            completed = subprocess.run(
                ["bash", "practice/preclass_run.sh"],
                cwd=lesson_dir,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                timeout=RUN_TIMEOUT_SEC,
                check=False,
            )
            self.write_json(
                {
                    "ok": completed.returncode == 0,
                    "runnerEnabled": True,
                    "lessonId": lesson_id,
                    "command": command,
                    "returnCode": completed.returncode,
                    "durationSec": round(time.time() - started, 2),
                    "output": scrub_output(completed.stdout),
                }
            )
        except subprocess.TimeoutExpired as exc:
            self.write_json(
                {
                    "ok": False,
                    "runnerEnabled": True,
                    "lessonId": lesson_id,
                    "command": command,
                    "returnCode": None,
                    "durationSec": RUN_TIMEOUT_SEC,
                    "output": scrub_output(exc.stdout or "") + "\n[TIMEOUT] 运行超时，已停止等待。",
                },
                status=HTTPStatus.REQUEST_TIMEOUT,
            )

    def read_json_body(self) -> dict[str, Any]:
        length = int(self.headers.get("Content-Length", "0"))
        if length <= 0:
            return {}
        raw = self.rfile.read(length).decode("utf-8")
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            return {}
        return data if isinstance(data, dict) else {}

    def write_json(self, data: dict[str, Any], status: HTTPStatus = HTTPStatus.OK) -> None:
        body = json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def runner_enabled() -> bool:
    return os.getenv("AGENT_COURSE_STUDIO_ALLOW_RUN") == "1"


def scrub_output(text: str) -> str:
    text = text.replace(str(COURSE_ROOT), "<course-root>")
    text = text.replace(str(Path.home()), "<user-home>")
    return text[-30_000:]


def main() -> None:
    parser = argparse.ArgumentParser(description="Serve AgentCraft Studio locally.")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8765)
    args = parser.parse_args()

    if not OUTPUT_PATH.exists():
        load_course_data()

    httpd = ThreadingHTTPServer((args.host, args.port), StudioHandler)
    print(f"[OK] AgentCraft Studio: http://{args.host}:{args.port}")
    print(f"[OK] Runner enabled: {runner_enabled()}")
    httpd.serve_forever()


if __name__ == "__main__":
    main()
