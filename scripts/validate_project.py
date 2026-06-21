#!/usr/bin/env python3
"""Validate Agent Course 2026 before publishing.

The checks are intentionally dependency-free so they can run locally and in
GitHub Actions:

- Course manifest shape.
- Required lesson README sections.
- Public site image references.
- SVG XML validity.
- Basic secret/local-path leakage scan.
"""

from __future__ import annotations

import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from xml.etree import ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
COURSE_JSON = ROOT / "apps" / "agent_course_studio" / "web" / "data" / "course.json"
README = ROOT / "README.md"
DOCS_INDEX = ROOT / "docs" / "index.html"
STUDIO_INDEX = ROOT / "docs" / "studio" / "index.html"
ROBOTS_TXT = ROOT / "docs" / "robots.txt"
SITEMAP_XML = ROOT / "docs" / "sitemap.xml"

REQUIRED_README_SECTIONS = [
    "本章学习目标",
    "推荐学习路径",
    "快速运行",
    "本章交付物",
]

FORBIDDEN_PATTERNS = [
    re.compile(r"/home/" + "xuyunpeng"),
    re.compile(r"\b4090\b"),
    re.compile(r"127\.0\.0\.1:24680"),
    re.compile(r"right\.codes"),
    re.compile(r"vveai"),
    re.compile(r"sk-[A-Za-z0-9_-]{20,}"),
    re.compile(r"AIza[0-9A-Za-z_-]{35}"),
    re.compile(r"ghp_[0-9A-Za-z]{36}"),
    re.compile(r"github_pat_[0-9A-Za-z_]{30,}"),
    re.compile(r"(OPENAI_API_KEY|ANTHROPIC_API_KEY|GEMINI_API_KEY|ADMIN_API_KEY)=([^<\s].+)"),
]

SCAN_EXTENSIONS = {".md", ".py", ".js", ".json", ".html", ".css", ".svg", ".yml", ".yaml", ".txt"}
SCAN_DIRS = ["README.md", "WEB_COURSE_PRODUCT_PLAN.md", "apps", "docs", "lessons", "teaching_support", "requirements", "scripts", ".github"]
SKIP_PARTS = {"__pycache__", ".git", "rag_index", ".pytest_cache"}


class LocalReferenceParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.refs: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        for name, value in attrs:
            if name in {"href", "src"} and value:
                self.refs.append(value)


def fail(message: str) -> None:
    print(f"[FAIL] {message}", file=sys.stderr)
    raise SystemExit(1)


def check_course_manifest() -> None:
    if not COURSE_JSON.exists():
        fail("course.json is missing; run scripts/build_public_site.py")
    data = json.loads(COURSE_JSON.read_text(encoding="utf-8"))
    stats = data.get("stats", {})
    lessons = data.get("lessons", [])
    if "generatedAt" in data:
        fail("course.json should use deterministic contentVersion, not generatedAt")
    if not re.fullmatch(r"[0-9a-f]{16}", str(data.get("contentVersion", ""))):
        fail("course.json contentVersion is missing or malformed")
    if stats.get("lessonCount") != 12 or len(lessons) != 12:
        fail(f"expected 12 lessons, got stats={stats.get('lessonCount')} len={len(lessons)}")
    codes = [lesson.get("code") for lesson in lessons]
    if codes != [f"L{i:02d}" for i in range(1, 13)]:
        fail(f"unexpected lesson codes: {codes}")
    if stats.get("practiceCount", 0) < 60:
        fail("practiceCount looks too low")
    if stats.get("resourceCount", 0) < 40:
        fail("resourceCount looks too low")
    print("[OK] course manifest")


def check_lesson_readmes() -> None:
    for readme in sorted((ROOT / "lessons").glob("L*/README.md")):
        text = readme.read_text(encoding="utf-8")
        missing = [section for section in REQUIRED_README_SECTIONS if section not in text]
        if missing:
            fail(f"{readme.relative_to(ROOT)} missing sections: {', '.join(missing)}")
    print("[OK] lesson README sections")


def check_public_site() -> None:
    for path in [DOCS_INDEX, STUDIO_INDEX, ROBOTS_TXT, SITEMAP_XML]:
        if not path.exists():
            fail(f"{path.relative_to(ROOT)} is missing")
    readme = README.read_text(encoding="utf-8")
    docs_index = DOCS_INDEX.read_text(encoding="utf-8")
    for image in [
        "docs/assets/course-roadmap.png",
        "docs/assets/studio-architecture.png",
        "docs/assets/capability-matrix.png",
        "docs/assets/site-preview.png",
        "docs/assets/studio-preview.png",
    ]:
        if image not in readme:
            fail(f"README does not reference {image}")
        if not (ROOT / image).exists():
            fail(f"{image} is missing")
    for local_ref in ["assets/course-roadmap.png", "assets/studio-architecture.png", "assets/capability-matrix.png"]:
        if local_ref not in docs_index:
            fail(f"docs/index.html does not reference {local_ref}")
    print("[OK] public site files")


def check_html_local_references() -> None:
    html_files = sorted((ROOT / "docs").rglob("*.html"))
    for html_file in html_files:
        parser = LocalReferenceParser()
        parser.feed(html_file.read_text(encoding="utf-8", errors="ignore"))
        for ref in parser.refs:
            if should_skip_ref(ref):
                continue
            target = resolve_ref(html_file.parent, ref)
            if not target.exists():
                fail(f"{html_file.relative_to(ROOT)} references missing file: {ref}")
    print("[OK] HTML local references")


def should_skip_ref(ref: str) -> bool:
    if ref.startswith(("#", "http://", "https://", "mailto:", "tel:", "data:")):
        return True
    return False


def resolve_ref(base_dir: Path, ref: str) -> Path:
    path_part = ref.split("#", 1)[0].split("?", 1)[0]
    target = (base_dir / path_part).resolve()
    if ref.endswith("/") or path_part.endswith("/"):
        target = target / "index.html"
    return target


def check_svgs() -> None:
    for svg in sorted((ROOT / "docs" / "assets").glob("*.svg")):
        try:
            ET.parse(svg)
        except ET.ParseError as exc:
            fail(f"{svg.relative_to(ROOT)} is invalid XML: {exc}")
    print("[OK] SVG XML")


def iter_scan_files() -> list[Path]:
    files: list[Path] = []
    self_path = Path(__file__).resolve()
    for entry in SCAN_DIRS:
        path = ROOT / entry
        if path.is_file():
            if path.resolve() != self_path:
                files.append(path)
            continue
        if path.is_dir():
            for child in path.rglob("*"):
                if (
                    child.is_file()
                    and child.resolve() != self_path
                    and child.suffix in SCAN_EXTENSIONS
                    and not any(part in SKIP_PARTS for part in child.parts)
                ):
                    files.append(child)
    return files


def check_sensitive_text() -> None:
    for path in iter_scan_files():
        text = path.read_text(encoding="utf-8", errors="ignore")
        for pattern in FORBIDDEN_PATTERNS:
            if pattern.search(text):
                fail(f"sensitive/local pattern found in {path.relative_to(ROOT)}: {pattern.pattern}")
    print("[OK] sensitive text scan")


def main() -> None:
    check_course_manifest()
    check_lesson_readmes()
    check_public_site()
    check_html_local_references()
    check_svgs()
    check_sensitive_text()
    print("[OK] project validation complete")


if __name__ == "__main__":
    main()
