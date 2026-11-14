# Panda Setup: contract and evaluation

## Purpose and evidence

The request asks for one skill that initializes new projects and prepares existing
ones for agent-assisted development: current versions, a minimal working structure,
agent instructions, ignore rules, and verified commands. No existing Panda skill
owns that outcome. Execute implements authorized changes, Plan orders work, Write
documents, and Plan/Write/Refactor each touch `.panda-suite/` only for their own
artifacts. The hypothesized failure is an agent that creates folders or templates,
relies on remembered versions, or reports "ready" without running the documented
commands. Baseline runs below test that hypothesis rather than assume it.

## Contract

`panda-setup` triggers on new-project initialization, existing-repository
preparation, and setup readiness audits. Ordinary feature work in a configured
project is a non-trigger (Lead routes it directly or to Execute).

- **Modes are inferred**, not selected: empty destination → new project; existing
  sources → preserve and reconcile; "audit/preview/do not change" → read-only report.
- **Authorization:** an explicit setup request covers reversible in-project edits
  and local verification. Commits, pushes, deployment, global installs, host or user
  configuration, real credentials, deletion and index rewrites remain separate.
- **Versions:** verified at setup time from official docs and registry metadata;
  latest compatible stable for new projects, no upgrades or prereleases unasked,
  conflicts explained. The skill text contains no version numbers.
- **Architecture:** smallest working structure in each framework's conventions;
  explicit user preferences win; no speculative layers or infrastructure.
- **Harness:** `AGENTS.md` as the source of truth; another host file only when that
  host is selected or detected and its behavior is verified; existing rules kept
  verbatim; no claimed capability that was not found.
- **Ignore rules:** existing content preserved; the suite's `/.panda-suite/`
  convention reused; examples and lockfiles kept trackable; both directions
  verified with `git check-ignore`; already-tracked files reported, never untracked.
- **Readiness:** "Ready" only when install, build/check, type check, lint, a
  behavioral test, and a live smoke request or page load all pass; otherwise
  "Partially configured" with failed step, completed work, and resume commands.

Any stack is supported through one generic procedure,
`references/stack-discovery.md`: identify the components, find official setup
sources and registry metadata, inspect generator behavior before running it,
add a meaningful test, verify from a clean state, and stop with a specific gap
when evidence is insufficient. Shared references cover discovery and versions,
the agent harness, gitignore and artifacts, readiness, and combined projects.
Optional stack notes (Go + Fiber, Fastify, FastAPI, React/Vue + Vite, Next.js)
record pitfalls observed below; setup never depends on a note existing. An
earlier draft distinguished "maintained profiles" from "researched paths"; it
was removed so that every stack follows the same evidence standard.
No template files, helper scripts, configuration format, or runtime were added:
official generators and package managers already provide that capability, and
the observed failures were judgment and verification gaps rather than missing
boilerplate. Lead routes setup requests; the skill does not require Lead.

## Stack note evidence (maintainer runs, 2026-11-14)

Each noted stack's commands were exercised directly in a scratch directory before
writing its reference. This validates the reference content on this machine,
not model behavior. Versions are what the registries reported that day; the
skill itself does not record them.

| Stack | Observed | Finding carried into the reference |
| --- | --- | --- |
| Go + Fiber | `go get` Fiber v3.7.0 (module `go 1.26.0`) on Go 1.27.1; `cmd/` + `internal/httpapi`; `gofmt`, `go vet`, `go build`, `go test` (via `app.Test`), live `/health` | Majors differ in import path and handler signature; read the module `go` directive |
| Node + Fastify | Fastify 5.12.8, TypeScript 7.0.2, Node 26.8.2; `tsc --noEmit`, `node --test` with `inject`, build, live `/health` | Unscoped `node --test` would also run compiled tests after a build |
| Python + FastAPI | FastAPI 0.162.7 with uv 0.11.18; ruff check/format; live `/health` | `uv init` creates a nested Git repository; first pytest run **failed** with `ModuleNotFoundError: app` until `pythonpath` was configured |
| React + Vite | create-vite 9.3.4 `react-ts`; build (includes `tsc -b`), oxlint, added Vitest + Testing Library counter test, `vite preview` page | Template has no test runner; generator has a destructive overwrite option |
| Vue + Vite | create-vue 3.24.0 `--ts --vitest --eslint`; `vue-tsc`, ESLint, single-run Vitest, build | Generated lint script applies `--fix`; test script watches by default; RC flag exists |
| Next.js | create-next-app 16.4.6 with explicit flags; ESLint, `tsc --noEmit`, build, `next start` page returned 200 with content | Generator writes an `AGENTS.md` block that `next dev` re-adds; generated `.gitignore` uses `.env*`, which ignores `.env.example`; `--yes` reuses saved preferences |

Combined layout was exercised only by the blind model runs below.

## Cases and protocol

Twenty `SETUP-*` cases in `tests/scenarios/cases.json` cover each noted
stack, a stack with no note (Rust + Axum), a combined repository, an existing project with custom architecture and
instructions (including a missing referenced file), tracked `.env` and
`.panda-suite` artifacts with a duplicated user ignore line, a tracking-policy
negation, repeated setup, offline documentation, a missing team tool (Poetry), a
Node 16 pin against current Next.js, a read-only audit, an explicit
handler/service/repository preference, an unavailable agent host (Cursor), a
failing private registry, and nonactivation. `tests/fixtures/project-setup` and
`project-setup-repeat` create the repositories; `tests/reviewer/check_setup.py`
validates fixtures and grades objective boundaries (index, history, preserved
rules, policy, registry, untouched files). Prepare arms with
`scripts/prepare-evaluation.py`; task agents read only `TASK.txt`.

## Actual results and limits

Fourteen fresh-context runs are summarized in
[setup results](../tests/results/setup/summary.md). All workspaces passed the
objective boundary grader. Observed differences against the existing Panda
workflow baseline (installed Panda Suite 1.6.0, no setup skill):

- With the skill, both new-project runs (combined, Next.js) produced `AGENTS.md`,
  reconciled ignore rules including `/.panda-suite/`, verified ignore behavior in
  both directions, and reported versions with sources. Baselines produced working
  applications but omitted some or all of these.
- On tracked `.env` and Panda plans, the skill added ignore rules and reported the
  index problem with exact commands; the baseline asked instead of adding rules.
- On Next.js, the skill kept `.env.example` trackable; the baseline's ignore file
  would hide it, and the baseline replaced the user's README.
- On the runtime conflict, both arms stopped and offered equivalent choices; the
  skill added no material behavioral advantage there.
- The skill arm on the existing project found a weak `make check`; one baseline
  arm was contaminated, so that pair is not a fair comparison.
- A baseline found a real Next.js type-check gap the reference missed; the
  reference was corrected and the fix was not re-run with a fresh agent.

After the generic stack-discovery revision, a Rust + Axum run (no stack note)
reached Ready with sources, clean-state verification and a live request.

Limits: one run per arm, no repeated sampling, no baseline for audit,
partial-failure or nonactivation cases, and eleven cases not run as model trials (Rust + Axum is one stack, not proof for all).
Five single stacks were exercised only by maintainer runs. No claim of time,
quality or token savings follows. Claude Code `plugin validate` passed and the
Codex app-server listed `panda-setup` in plugin and standalone discovery;
interactive invocation through either host was not exercised.
