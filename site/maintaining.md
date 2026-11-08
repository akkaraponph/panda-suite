# Maintaining this documentation site

The site is published on GitHub Pages. Its pages are generated from the repository's existing documentation and skill usage examples. No browser framework or runtime service is required.

## Build locally

From the repository root, use Python 3.10 or later:

```sh
python3 -m venv .venv-docs
.venv-docs/bin/python -m pip install -r requirements-docs.txt
.venv-docs/bin/python scripts/build-docs.py
.venv-docs/bin/python scripts/check-docs.py
python3 -m http.server 8000 --directory dist
```

Open `http://localhost:8000`. The build creates `dist/`, which is ignored by Git.

## Update content

- Edit `docs/usage.md` to update the copyable prompts and skill guides. The builder extracts each specialist section from this file.
- Edit `README.md` to update installation instructions. The builder extracts its installation section.
- Edit `site/index.md` for the home page and `site/assets/` for styles and behavior.
- Update the page list in `scripts/build-docs.py` when adding a guide. Add new skills to the usage guide and the builder's skill list together.
- Keep commands grounded in actual host and installer behavior. Discovery checks do not prove interactive invocation.

The builder checks that every packaged skill has a usage page. The link checker checks all generated internal page, asset, and fragment links. Source links lead back to GitHub; repository-relative links that are not published pages also lead to GitHub.

## Publish

The `.github/workflows/docs.yml` workflow builds and checks the site on pull requests. Pushes to `main` that change site inputs also deploy to the `github-pages` environment. It can be run manually from GitHub Actions.

Repository Settings → Pages must use **GitHub Actions** as the source. Deployment follows the [GitHub Pages custom workflow](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages) model.

## Content evidence

| Published content | Repository evidence |
| --- | --- |
| Installation commands and limitations | `README.md`, `scripts/install-skills.py`, plugin manifests |
| Skill prompts, inputs, expected results, boundaries | `docs/usage.md`, each `skills/*/SKILL.md` |
| Version and skill inventory | `plugin.json`, packaged `skills/` directories |
| Routing and handoff | `docs/routing.md`, `docs/skill-contract.md` |
| Historical check results and limitations | `docs/verification.md`, linked repository reports |
| Attribution and licensing | `SOURCE_NOTICES.md`, `upstream-lock.json` |

The site build and link check verify the generated documentation. They do not execute the example agent prompts or repeat the historical skill evaluations.
