# Agent harness

## Instruction files

Use `AGENTS.md` as the shared source of truth when the selected hosts support
it. Add another host's file only when that host is selected or detected and its
current documentation confirms the behavior. Some hosts read `AGENTS.md`
directly; others need their own file or an import. When a host file is needed or
already exists, prefer a short import or pointer to `AGENTS.md` over copying
its body. Check the host's current documentation rather than assuming.

Keep the file concise and actionable. Include only what exists:

- **Purpose and stack:** one or two sentences; frameworks and runtimes, with
  versions left to manifests.
- **Layout:** source locations and real boundaries (for example "API in
  `backend/`, web app in `web/`; the web app calls the API through `/api`").
- **Commands:** setup, dev, build, test, type check, lint, exactly as run
  during verification, with the working directory.
- **Environment:** variables, where the example file lives, and that real
  values stay in untracked local files.
- **Testing expectations:** where tests live and what a change should add.
- **Conventions:** project-specific rules only; skip generic advice the
  framework or linter already enforces.
- **Done means:** the checks to run before reporting a change complete.
- **Artifacts:** durable decisions go in tracked project docs (for example
  `docs/decisions/`) when the team wants them; temporary agent working files go
  in the ignored `.panda-suite/` directory.
- **Panda skills (only if available):** a short map such as "new feature with
  unclear rules → panda-requirements or panda-plan; bug → panda-debugger;
  review a diff → panda-review". State that small changes can be made directly.
  Omit this section when no Panda skills are installed or selected.

## Existing instructions

Read the whole existing file first. Keep user rules verbatim. Add missing
sections or fill missing facts in place. When an existing rule conflicts with
what setup found (a documented command that fails, a path that no longer
exists), do not delete it: report the conflict and either correct it with
evidence or ask. On repeated runs, update sections rather than appending
duplicates.

## Skills, plugins, and services

Keep three categories separate in instructions and reports:

1. **Application dependencies:** installed through the project's package manager.
2. **Agent skills and plugins:** loaded by the agent host.
3. **External services and MCP connections:** require accounts or credentials.

Detect what is already available (host plugin list commands, skill directories
such as `.agents/skills/` or `.claude/skills/`, existing configuration) before
recommending anything. Use only the host's documented mechanisms. Installing
into user or global host configuration requires explicit authorization; within
the project, prefer documented project-scoped options. Do not copy the whole
Panda Suite into an application repository by default. Never write invented
plugin configuration files or claim an installation that was not observed.

If a needed host capability or CLI is unavailable, list the exact remaining
commands or steps, mark them **incomplete**, and keep instructions from
referring to the missing capability as if it existed.

## Limits

Do not create a custom agent runtime, scheduler, delegation framework,
mandatory hooks, or a required lifecycle such as brainstorm → requirements →
plan → execute → review → release for every change.
