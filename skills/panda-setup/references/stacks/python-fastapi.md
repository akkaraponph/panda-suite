# Python + FastAPI

Sources to check at setup time: [Python release status](https://devguide.python.org/versions/),
[FastAPI documentation](https://fastapi.tiangolo.com/) (first steps, testing,
bigger applications) and [release notes](https://fastapi.tiangolo.com/release-notes/),
package metadata at `https://pypi.org/pypi/fastapi/json` (`info.version`,
`info.requires_python`), and the selected package manager's docs (for example
[uv](https://docs.astral.sh/uv/)).

## Version decisions

- Pick a Python version supported upstream and by FastAPI's `requires_python`.
- Use the existing package manager and lock format (uv, Poetry, pip-tools,
  plain requirements). For a new project, use uv when installed; otherwise use
  the standard library `venv` plus pip and say so. Do not install uv globally unasked.
- FastAPI is pre-1.0; minor releases can change behavior. Pin through the
  lockfile and read release notes when adding to an existing project.

## Structure

```text
app/__init__.py
app/main.py          FastAPI() instance and routers
tests/test_*.py      TestClient-based tests
pyproject.toml
```

Add `app/routers/` or domain modules when there are several resource groups.
Add database, settings, or auth modules only when required.

`uv init` creates its own Git repository unless told otherwise (`--vcs none`);
use that inside an existing repository. With an `app/` package and a `tests/`
directory, pytest may not import `app` by default: configure
`[tool.pytest.ini_options] pythonpath = ["."]` (or the project's existing
equivalent) and confirm by running the tests.

## Commands (uv example)

```sh
uv init --app --vcs none <dir>
uv add "fastapi[standard]"
uv add --dev pytest ruff
uv run pytest
uv run ruff check . && uv run ruff format --check .
uv run fastapi dev app/main.py        # development
uv run fastapi run app/main.py --port <port>   # smoke
```

Type checking (mypy, pyright) only if configured or requested. Smoke: request
the health route and `/docs` returns 200.

Ignore: `.venv/`, `__pycache__/`, `.pytest_cache/`, `.ruff_cache/`, `.env`.
Track `pyproject.toml`, the lockfile, and `.python-version`.
