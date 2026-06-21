# Deployment

This project is designed to publish a static public website and a static Agent Course Studio through GitHub Pages.

## Local Preview

Build the public site:

```bash
python3 scripts/build_public_site.py
```

Start a local static server:

```bash
python3 -m http.server 8780 --directory docs
```

Open:

```text
http://127.0.0.1:8780
http://127.0.0.1:8780/studio/
```

## GitHub Pages

After pushing to GitHub, enable Pages from repository settings:

1. Open `Settings`.
2. Open `Pages`.
3. Under `Build and deployment`, set `Source` to `GitHub Actions`.
4. Run the `Deploy GitHub Pages` workflow, or push to `main`.

The workflow will:

1. Check out the repository.
2. Run `python3 scripts/build_public_site.py`.
3. Run `python3 scripts/validate_project.py`.
4. Validate local HTML links, public assets, SVG XML and sensitive text patterns.
5. Upload the generated `docs/` folder as the Pages artifact.
6. Deploy the artifact.

## Expected Public URLs

The final URL is controlled by GitHub Pages. For this repository it is expected to look like:

```text
https://arvin-lucifer.github.io/agent_course_2026/
https://arvin-lucifer.github.io/agent_course_2026/studio/
```

If a custom domain is configured later, add it in GitHub Pages settings and update the repository About URL.

## Validation

Run this before publishing:

```bash
python3 scripts/build_public_site.py
python3 scripts/validate_project.py
node --check apps/agent_course_studio/web/app.js
python3 -m py_compile apps/agent_course_studio/build_course_data.py apps/agent_course_studio/server.py scripts/build_public_site.py scripts/validate_project.py
git diff --check
```

## Notes

- `docs/index.html`, `docs/site.css`, `docs/studio/`, and `docs/assets/favicon.svg` are generated build outputs and are ignored by Git.
- `docs/robots.txt` and `docs/sitemap.xml` are generated build outputs and are ignored by Git.
- `docs/assets/*.png` and `docs/assets/*.svg` diagrams are source assets used by README and the public site.
- The static Studio runs in safe static mode; it does not execute local scripts.
