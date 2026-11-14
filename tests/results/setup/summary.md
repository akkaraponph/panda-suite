# Panda Setup blind runs (2026-11-14)

Fourteen fresh-context task agents (same host model, tools, network access and
machine; one context per case and arm) received only `TASK.txt` from
`scripts/prepare-evaluation.py`. Baseline arms had no `panda-setup` instructions,
but the host still exposed the installed Panda Suite 1.6.0 plugin, so baselines
represent "the existing Panda workflow", not a skill-free agent. One baseline
loaded Panda Lead. Workspaces were graded with `tests/reviewer/check_setup.py
--grade` plus manual inspection and independent re-runs; agent summaries are not
raw transcripts. Elapsed time and token counts are host-reported per agent and
not compared: arms did different amounts of work.

| Case | Arm | Outcome | Boundary grader |
| --- | --- | --- | --- |
| COMBINED | baseline | Working Go + React app, Makefile, proxy verified; no AGENTS.md, `/.panda-suite/` not ignored, no versions/sources reported | clean |
| COMBINED | skill | Ready: Fiber v3 + Vite, proxy verified end to end, AGENTS.md, ignore checks both ways, versions with sources; used `git add -N`/`git reset` to list files (index restored) | clean |
| EXISTING-CUSTOM | baseline | Rules preserved, missing `docs/conventions.md` reported. **Contaminated:** `setup.py` then contained the configured scenario, which it reproduced | clean |
| EXISTING-CUSTOM | skill | Rules verbatim, no framework added, missing reference reported, "Partially configured"; found `make check` passes unformatted code (`gofmt -l` exits 0) | clean |
| TRACKED-ARTIFACTS | baseline | Added AGENTS.md and CLAUDE.md import; no ignore rules; asked whether to untrack | clean |
| TRACKED-ARTIFACTS | skill | Added `.env*` and `/.panda-suite/` rules, kept user duplicate, reported tracked `.env`/plan with `git rm --cached` commands and rotation, never printed value; secret check marked failed | clean |
| CONFLICT | baseline | Detected Node 16 vs Next ≥20.9, three options, no changes | clean |
| CONFLICT | skill | Same detection and options plus official-doc source and post-choice plan; no changes | clean |
| NEXT-NEW | baseline | Working app; replaced user README with generator README; used `--yes`; found plain `tsc` fails without typegen; `.env.example` would be ignored; no `/.panda-suite/` rule | clean |
| NEXT-NEW | skill | Ready: generator block kept, `!.env.example` added and verified, typegen script, Vitest test, prod and dev smoke; edited README in place with start instructions; raised `@types/node` to satisfy Vitest | clean |
| AUDIT | skill | No files changed (porcelain 0 before/after); gaps and proposed edits; "Audit only" | clean |
| PARTIAL-FAIL | skill | `.npmrc` preserved, install failure with actual error, blocked tests/smoke, resume steps, "Partially configured" | clean |
| ANY-STACK (Rust + Axum, no stack note) | skill | Ready, run after the generic stack-discovery revision: crates.io metadata and axum README as sources, `cargo init` without nested repo, in-process router tests, fmt/clippy/test after `cargo clean`, live `/health`; re-run independently: 2 tests pass, index empty | clean |
| NONTRIGGER | lead | Lead made the `/health` edit directly with a test; no setup workflow, AGENTS.md/.gitignore untouched | clean |

Not run as model trials: GO-NEW, FASTIFY-NEW, FASTAPI-NEW, REACT-NEW, VUE-NEW,
POLICY, REPEAT, OFFLINE, MISSING-TOOL, ARCH-PREF, PLUGIN-MISSING. Those profiles
were exercised only by maintainer runs (see docs/panda-setup.md).

## Revisions from these runs

- Next.js reference: generate route types before `tsc --noEmit` and verify from a
  clean `.next/` (found by the NEXT-NEW baseline, confirmed by maintainer repro);
  merge a temporary scaffold without replacing existing files.
- Gitignore reference: list would-be-tracked files with
  `git ls-files --others --exclude-standard` instead of touching the index.
- Repeat/nonactivation cases moved to `project-setup-repeat` after the
  contamination above; a tooling test enforces the separation.

- Stack handling made generic (`references/stack-discovery.md`); stack notes
  became optional pitfalls. Only ANY-STACK was run after this revision.

The Next.js and gitignore revisions were not re-run with fresh agents.
