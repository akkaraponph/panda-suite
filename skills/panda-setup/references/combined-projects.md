# Combined projects

Use with [stack discovery](stack-discovery.md) for each application.

## Layout

Default to one repository with one directory per application, named by role:

```text
backend/    (or api/)  own manifest, lockfile, tests
web/        (or frontend/) own manifest, lockfile, tests
AGENTS.md   root instructions: both apps, how they talk, commands per directory
.gitignore  root rules; keep generator-written nested ignores only if useful
```

Use an existing layout when one exists. Add workspace tooling (npm/pnpm
workspaces, Go workspaces, a task runner, Turborepo, Nx) only for a concrete
benefit, such as shared TypeScript packages or a single CI entry point the team
requested. Two different ecosystems rarely need orchestration beyond documented
per-directory commands. A root Makefile or script is optional; when added, it
must only call commands that were verified.

Run generators with their nested-Git option disabled (or remove only the nested
`.git` the generator just created, after confirming it is new and empty of history).

## Communication

Choose and document one development path:

- **Dev proxy (recommended for browser apps):** the frontend dev server proxies
  `/api` to the backend port, avoiding CORS during development. Document the
  production equivalent as a deployment decision still to make.
- **Explicit base URL:** a frontend env variable (for example `VITE_API_URL`)
  with an example file, plus a backend CORS allowlist read from env.

Verify the path end to end: start both, request the backend through the
frontend's proxy or configured URL, and observe the expected response. Record
both ports in the instructions.

Version decisions are independent per application; report each.
