# Public Launch Checklist

Use this checklist before sharing the repository or public website.

## Content

- [ ] Root README explains the course value in under one minute.
- [ ] Public website opens from `docs/index.html`.
- [ ] Static Studio opens from `docs/studio/index.html`.
- [ ] `docs/robots.txt` and `docs/sitemap.xml` are generated.
- [ ] L01-L12 all have learning goals, recommended path, quick run and deliverables.
- [ ] L12 graduation project has a clear demo story and acceptance checklist.

## Engineering

- [ ] `python3 scripts/build_public_site.py`
- [ ] `python3 scripts/validate_project.py`
- [ ] `node --check apps/agent_course_studio/web/app.js`
- [ ] `python3 -m py_compile apps/agent_course_studio/build_course_data.py apps/agent_course_studio/server.py scripts/build_public_site.py scripts/validate_project.py`
- [ ] `git diff --check`

## Security

- [ ] `.env` is not tracked.
- [ ] No real API keys, PATs, proxy URLs or local absolute paths are present.
- [ ] Studio runner is disabled by default.
- [ ] Public site uses static data only.

## Distribution

- [ ] GitHub Pages source is set to `docs/`, or a GitHub Actions Pages workflow is enabled.
- [ ] README images render on GitHub.
- [ ] Public URL is added to the GitHub repository About section.
- [ ] A short demo video or screenshots are prepared for sharing.
