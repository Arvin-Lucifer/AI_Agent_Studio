#!/usr/bin/env python3
"""Build the public GitHub Pages site for Agent Course 2026.

The course content still lives in ``lessons/`` and the Studio app still lives in
``apps/agent_course_studio``. This script creates a deployable ``docs/`` folder:

- ``docs/index.html``: product-facing public landing page.
- ``docs/studio/``: static export of Agent Course Studio.

GitHub Pages can publish this folder directly, while local development can keep
using the original Studio server when the optional runner API is needed.
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS_DIR = ROOT / "docs"
ASSETS_DIR = DOCS_DIR / "assets"
STUDIO_SOURCE = ROOT / "apps" / "agent_course_studio" / "web"
STUDIO_EXPORT = DOCS_DIR / "studio"
COURSE_DATA = STUDIO_SOURCE / "data" / "course.json"
PUBLIC_BASE_URL = "https://arvin-lucifer.github.io/agent_course_2026/"


def run_build_course_data() -> None:
    subprocess.run(
        [sys.executable, str(ROOT / "apps" / "agent_course_studio" / "build_course_data.py")],
        cwd=ROOT,
        check=True,
    )


def load_course_data() -> dict:
    return json.loads(COURSE_DATA.read_text(encoding="utf-8"))


def export_studio() -> None:
    if STUDIO_EXPORT.exists():
        shutil.rmtree(STUDIO_EXPORT)
    shutil.copytree(
        STUDIO_SOURCE,
        STUDIO_EXPORT,
        ignore=shutil.ignore_patterns("__pycache__", "*.pyc"),
    )
    index_path = STUDIO_EXPORT / "index.html"
    index_html = index_path.read_text(encoding="utf-8")
    static_flag = '    <script>window.AGENT_COURSE_STATIC_EXPORT = true;</script>\n'
    if "AGENT_COURSE_STATIC_EXPORT" not in index_html:
        index_html = index_html.replace('    <script src="./app.js"></script>\n', static_flag + '    <script src="./app.js"></script>\n')
        index_path.write_text(index_html, encoding="utf-8")


def write_public_home(data: dict) -> None:
    stats = data["stats"]
    lessons = data["lessons"]
    lesson_rows = "\n".join(
        f"""
        <tr>
          <td>{lesson['code']}</td>
          <td>{escape_html(lesson['title'])}</td>
          <td>{escape_html(' / '.join(lesson.get('topics', [])[:3]))}</td>
          <td>{len(lesson.get('practiceFiles', []))}</td>
        </tr>
        """.rstrip()
        for lesson in lessons
    )
    support_count = len(data.get("supportDocs", []))
    html = f"""<!doctype html>
<html lang="zh-CN">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Agent Course 2026 | Agent 开发课程实验室</title>
    <meta
      name="description"
      content="从 Prompt、Function Calling、LangChain、RAG、Memory、MCP、Skill 到评测部署和智能客服毕业项目的 Agent 开发课程。"
    />
    <link rel="canonical" href="{PUBLIC_BASE_URL}" />
    <meta property="og:title" content="Agent Course 2026" />
    <meta property="og:description" content="完整的 AI Agent 开发学习路径、课程实验室和毕业项目工作区。" />
    <meta property="og:type" content="website" />
    <meta property="og:url" content="{PUBLIC_BASE_URL}" />
    <meta property="og:image" content="{PUBLIC_BASE_URL}assets/course-roadmap.png" />
    <meta name="twitter:card" content="summary_large_image" />
    <link rel="icon" href="assets/favicon.svg" type="image/svg+xml" />
    <link rel="stylesheet" href="site.css" />
    <script type="application/ld+json">
      {{
        "@context": "https://schema.org",
        "@type": "Course",
        "name": "Agent Course 2026",
        "description": "面向 AI Agent 开发学习、工程实践、面试准备和毕业项目展示的完整课程。",
        "provider": {{
          "@type": "Organization",
          "name": "Agent Course Studio"
        }},
        "hasCourseInstance": {{
          "@type": "CourseInstance",
          "courseMode": "online",
          "courseWorkload": "12 lessons"
        }}
      }}
    </script>
  </head>
  <body>
    <header class="site-nav">
      <a class="brand" href="./" aria-label="Agent Course 2026 home">
        <span>AC</span>
        <strong>Agent Course 2026</strong>
      </a>
      <nav aria-label="Primary">
        <a href="#curriculum">课程路线</a>
        <a href="#studio">Studio</a>
        <a href="#project">毕业项目</a>
        <a href="studio/">打开实验室</a>
      </nav>
    </header>

    <main>
      <section class="hero">
        <img src="assets/course-roadmap.png" alt="Agent Course roadmap" />
        <div class="hero-copy">
          <p class="eyebrow">AI Agent Development Learning Lab</p>
          <h1>从课程资料到可运行 Agent 产品工作台</h1>
          <p>
            12 章课程覆盖 Prompt、工具调用、LangChain、RAG、记忆系统、MCP、Skill、评测部署与智能客服毕业项目。
          </p>
          <div class="hero-actions">
            <a class="primary" href="studio/">打开 Agent Course Studio</a>
            <a class="secondary" href="https://github.com/Arvin-Lucifer/agent_course_2026">查看 GitHub 仓库</a>
          </div>
        </div>
      </section>

      <section class="metrics" aria-label="课程规模">
        <div><strong>{stats['lessonCount']}</strong><span>章节</span></div>
        <div><strong>{stats['practiceCount']}</strong><span>实践文件</span></div>
        <div><strong>{stats['resourceCount']}</strong><span>资源材料</span></div>
        <div><strong>{support_count}</strong><span>教辅专题</span></div>
      </section>

      <section id="studio" class="split-section">
        <div>
          <p class="eyebrow">Public Studio</p>
          <h2>公开访问优先，本地运行进阶</h2>
          <p>
            静态 Studio 可以直接托管在 GitHub Pages；如果需要运行课程脚本，再切回本地 server，并由白名单 runner 控制风险。
          </p>
          <ul class="check-list">
            <li>课程导航、讲义、实战、面试题和资源统一展示。</li>
            <li>本地检索式课程助手附带引用来源。</li>
            <li>浏览器保存学习进度，不需要登录即可试用。</li>
            <li>真实脚本运行默认关闭，不暴露密钥和本机路径。</li>
          </ul>
        </div>
        <img src="assets/studio-architecture.png" alt="Agent Course Studio architecture" />
      </section>

      <section id="curriculum" class="curriculum">
        <div class="section-heading">
          <p class="eyebrow">Curriculum</p>
          <h2>12 章 Agent 工程路径</h2>
          <p>从基础认知到生产化部署，最后用智能客服 Agent 串起完整项目交付。</p>
        </div>
        <div class="table-shell">
          <table>
            <thead>
              <tr>
                <th>章节</th>
                <th>主题</th>
                <th>关键词</th>
                <th>实战数</th>
              </tr>
            </thead>
            <tbody>
{lesson_rows}
            </tbody>
          </table>
        </div>
      </section>

      <section class="split-section reverse">
        <img src="assets/capability-matrix.png" alt="Capability coverage matrix" />
        <div>
          <p class="eyebrow">Capability Matrix</p>
          <h2>面向面试和工程落地的能力矩阵</h2>
          <p>
            课程不是只讲概念，而是把模型控制、工具执行、知识检索、状态管理、协议接入、Skill 工程和评测部署都落到可运行代码。
          </p>
          <div class="capability-grid">
            <span>Prompt</span><span>Function Calling</span><span>RAG</span><span>Memory</span>
            <span>MCP</span><span>Skill</span><span>Evaluation</span><span>Deployment</span>
          </div>
        </div>
      </section>

      <section id="project" class="project-band">
        <p class="eyebrow">Graduation Project</p>
        <h2>最终交付：智能客服 Agent</h2>
        <p>
          L12 把 LangGraph 状态机、RAG 知识库、多轮澄清、投诉工单、人工兜底、FastAPI 服务和评测脚本整合成一个可答辩项目。
        </p>
        <a class="primary" href="studio/#L12_graduation_project/overview">查看毕业项目章节</a>
      </section>
    </main>

    <footer>
      <span>Agent Course 2026</span>
      <span>Built from course content · Static-first · Runner-safe</span>
    </footer>
  </body>
</html>
"""
    (DOCS_DIR / "index.html").write_text(html, encoding="utf-8")


def write_crawler_files() -> None:
    sitemap = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>{PUBLIC_BASE_URL}</loc>
  </url>
  <url>
    <loc>{PUBLIC_BASE_URL}studio/</loc>
  </url>
</urlset>
"""
    robots = f"""User-agent: *
Allow: /

Sitemap: {PUBLIC_BASE_URL}sitemap.xml
"""
    (DOCS_DIR / "sitemap.xml").write_text(sitemap, encoding="utf-8")
    (DOCS_DIR / "robots.txt").write_text(robots, encoding="utf-8")


def write_site_css() -> None:
    css = """html {
  scroll-behavior: smooth;
}

:root {
  --bg: #f7f5ef;
  --ink: #17202a;
  --muted: #667085;
  --line: #dedbd2;
  --surface: #fffdf8;
  --teal: #0f766e;
  --coral: #c2410c;
  --blue: #2556a3;
  --amber: #b7791f;
  font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI",
    "Noto Sans CJK SC", "Microsoft YaHei", sans-serif;
}

* {
  box-sizing: border-box;
}

body {
  margin: 0;
  color: var(--ink);
  background: var(--bg);
}

a {
  color: inherit;
  text-decoration: none;
}

.site-nav {
  position: sticky;
  top: 0;
  z-index: 10;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
  padding: 14px 34px;
  background: rgba(247, 245, 239, 0.92);
  border-bottom: 1px solid var(--line);
  backdrop-filter: blur(16px);
}

.brand {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  font-weight: 800;
}

.brand span {
  display: grid;
  place-items: center;
  width: 36px;
  height: 36px;
  border-radius: 7px;
  background: var(--ink);
  color: #fffdf8;
}

.site-nav nav {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  color: #3f4852;
  font-size: 14px;
  font-weight: 700;
}

.hero {
  position: relative;
  min-height: 620px;
  display: grid;
  align-items: end;
  padding: 56px 34px;
  overflow: hidden;
}

.hero::after {
  content: "";
  position: absolute;
  inset: 0;
  background: linear-gradient(90deg, rgba(23, 32, 42, 0.86), rgba(23, 32, 42, 0.45), rgba(23, 32, 42, 0.08));
}

.hero img {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.hero-copy {
  position: relative;
  z-index: 1;
  max-width: 780px;
  color: #fffdf8;
}

.eyebrow {
  margin: 0 0 10px;
  color: var(--coral);
  font-size: 13px;
  font-weight: 900;
  letter-spacing: 0;
}

.hero .eyebrow {
  color: #f7c9b6;
}

h1,
h2 {
  margin: 0;
  letter-spacing: 0;
}

h1 {
  font-size: clamp(44px, 7vw, 86px);
  line-height: 0.98;
  max-width: 860px;
}

h2 {
  font-size: clamp(30px, 4vw, 48px);
  line-height: 1.08;
}

p {
  color: #46515d;
  font-size: 17px;
  line-height: 1.75;
}

.hero p {
  max-width: 720px;
  color: #e8ecef;
  font-size: 19px;
}

.hero-actions,
.project-band {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  align-items: center;
}

.primary,
.secondary {
  display: inline-flex;
  align-items: center;
  min-height: 44px;
  border-radius: 7px;
  padding: 0 16px;
  font-weight: 900;
}

.primary {
  background: var(--teal);
  color: #fff;
}

.secondary {
  border: 1px solid rgba(255, 253, 248, 0.58);
  color: #fffdf8;
}

.metrics {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 12px;
  padding: 16px 34px 0;
  max-width: 1220px;
  margin: 0 auto;
}

.metrics div,
.table-shell,
.project-band,
.split-section {
  border: 1px solid var(--line);
  background: rgba(255, 253, 248, 0.88);
  border-radius: 8px;
}

.metrics div {
  padding: 20px;
}

.metrics strong {
  display: block;
  font-size: 42px;
  line-height: 1;
}

.metrics span {
  color: var(--muted);
  font-weight: 800;
}

.split-section,
.curriculum,
.project-band {
  max-width: 1220px;
  margin: 16px auto 0;
}

.split-section {
  display: grid;
  grid-template-columns: minmax(0, 0.9fr) minmax(0, 1.1fr);
  gap: 24px;
  padding: 28px;
  align-items: center;
}

.split-section.reverse {
  grid-template-columns: minmax(0, 1.1fr) minmax(0, 0.9fr);
}

.split-section img {
  width: 100%;
  border-radius: 8px;
  border: 1px solid var(--line);
}

.check-list {
  display: grid;
  gap: 10px;
  padding-left: 20px;
  color: #3f4852;
  line-height: 1.6;
}

.curriculum {
  padding: 28px;
}

.section-heading {
  max-width: 760px;
}

.table-shell {
  margin-top: 18px;
  overflow: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
  min-width: 780px;
}

th,
td {
  padding: 13px 14px;
  border-bottom: 1px solid var(--line);
  text-align: left;
  vertical-align: top;
}

th {
  color: var(--teal);
  font-size: 13px;
}

td {
  color: #374151;
  font-size: 14px;
}

.capability-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 18px;
}

.capability-grid span {
  border-radius: 999px;
  border: 1px solid rgba(15, 118, 110, 0.22);
  background: #d9f1ed;
  color: #0b625c;
  padding: 8px 12px;
  font-size: 13px;
  font-weight: 800;
}

.project-band {
  display: block;
  padding: 36px;
}

.project-band .primary {
  margin-top: 10px;
}

footer {
  max-width: 1220px;
  margin: 18px auto 0;
  padding: 0 0 32px;
  display: flex;
  justify-content: space-between;
  gap: 12px;
  color: var(--muted);
  font-size: 13px;
}

@media (max-width: 860px) {
  .site-nav {
    align-items: flex-start;
    flex-direction: column;
    padding: 12px 16px;
  }

  .hero {
    min-height: 560px;
    padding: 36px 18px;
  }

  .hero::after {
    background: rgba(23, 32, 42, 0.78);
  }

  .metrics,
  .split-section,
  .split-section.reverse {
    grid-template-columns: 1fr;
  }

  .metrics,
  .split-section,
  .curriculum,
  .project-band,
  footer {
    margin-left: 10px;
    margin-right: 10px;
    padding-left: 18px;
    padding-right: 18px;
  }

  .metrics {
    padding-top: 12px;
  }

  footer {
    display: grid;
  }
}
"""
    (DOCS_DIR / "site.css").write_text(css, encoding="utf-8")


def write_favicon() -> None:
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    favicon = """<svg width="64" height="64" viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect width="64" height="64" rx="14" fill="#17202A"/>
  <text x="14" y="40" fill="#FFFDF8" font-family="Arial,sans-serif" font-size="24" font-weight="800">AC</text>
</svg>
"""
    (ASSETS_DIR / "favicon.svg").write_text(favicon, encoding="utf-8")


def escape_html(value: str) -> str:
    return (
        value.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def main() -> None:
    run_build_course_data()
    data = load_course_data()
    write_favicon()
    write_public_home(data)
    write_crawler_files()
    write_site_css()
    export_studio()
    print("[OK] Built public site in docs/")
    print("[OK] Built static Studio in docs/studio/")


if __name__ == "__main__":
    main()
