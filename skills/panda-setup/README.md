# Panda Setup

Use `$panda-setup` standalone, `$panda-suite:panda-setup` in a Codex plugin, or
`/panda-suite:panda-setup` in a Claude plugin. The host reads [SKILL.md](SKILL.md);
the examples are natural-language requests, not an executable command parser.

```text
$panda-setup Initialize a Go + Fiber backend in ./api with a health endpoint.
$panda-setup Set up a React frontend and Go backend in one repository.
$panda-setup Prepare this existing project for Panda Suite.
$panda-setup Audit this repository's setup readiness. Do not change files.
```

The skill infers new-project, existing-project, or audit behavior from the
request and the destination. It checks current official documentation and
package metadata, creates or adapts the smallest working structure, writes or
reconciles `AGENTS.md` and `.gitignore`, and runs the real install, build, type
check, lint, test, and smoke commands before calling a project ready.

Any stack works: the skill finds each stack's official setup path, generator
behavior, and commands at setup time. Optional notes record pitfalls already
seen for Go + Fiber, Fastify, FastAPI, React/Vue + Vite and Next.js; setup does
not depend on them. Commits, pushes, deployment, global installs and
host configuration changes need separate authorization. No Panda Lead needed.
