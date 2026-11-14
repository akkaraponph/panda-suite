# Gitignore and Panda artifacts

## Defaults

Track: source, dependency manifests, lockfiles, shared agent instructions,
example configuration (`.env.example`), and durable architecture documents.

Ignore: local secrets (`.env`, `.env.local`, `.env.*.local`), generated build
output, dependency directories, caches, coverage, editor/OS noise only when the
project lacks it, and temporary Panda working artifacts.

Panda Suite skills write plans, specs, and drafts under `.panda-suite/` at the
repository root, and the suite's convention is a root rule `/.panda-suite/`.
Use that rule; do not invent another artifact directory. Create subdirectories
under it only when a file needs them. Durable documents the team wants versioned
belong in tracked project docs, or in `.panda-suite/` only under an explicit
repository policy (see below).

## Editing rules

- Read the existing `.gitignore` (and nested ones) first; add only missing
  patterns, grouped under a short comment. Never reorder or delete user lines.
- Prefer anchored, specific patterns (`/dist/`, `/.panda-suite/`) over broad
  ones (`*.json`, `docs/`). Do not ignore lockfiles or example env files.
- Do not add a pattern that a negation (`!`) in the file would contradict
  without reporting it.
- Respect an explicit repository policy that tracks selected Panda artifacts
  (for example `!/.panda-suite/decisions/`); keep it and explain the effect.

## Verify with Git

Check representative paths in both directions:

```sh
git check-ignore -v .env node_modules/x dist/x .panda-suite/plans/x.md
git check-ignore -v .env.example package-lock.json AGENTS.md src/main.ts || echo "not ignored (expected)"
git status --short --ignored
```

Use paths that exist or would exist in this project. `check-ignore` succeeding
on the second list is a defect. To list what would become tracked, use
`git ls-files --others --exclude-standard`; do not stage, intent-to-add, or
reset the index during setup.

## Already-tracked files

Ignore rules do not untrack files. Run `git ls-files` for `.panda-suite/`,
`.env*` (excluding examples), build output, and other ignored categories. Report
each tracked path, why it matters, and the command the user could run
(`git rm --cached <path>`), but do not change the index or history. A tracked
secret also needs rotation advice; never print its value.
