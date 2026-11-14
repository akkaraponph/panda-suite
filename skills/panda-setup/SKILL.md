---
name: panda-setup
description: Initialize a new project or prepare an existing repository for agent-assisted development, including stack and version selection from current official sources, minimal working structure, agent instructions, Git ignore rules, and verified commands; or audit setup readiness without changes.
---

# Panda Setup

Deliver a usable development starting point: a minimal application or adapted
repository whose documented commands actually work, plus concise agent
instructions and correct ignore rules. Folders, templates, or documentation
alone are not a setup. Ordinary feature work on an already configured project
is outside this skill; implement it directly or with an execution workflow.

## Infer the request

- **New project:** empty or absent destination. Create a minimal working app.
- **Existing project:** preserve its architecture, dependencies, package
  manager, lockfiles, and user-owned configuration. Add or reconcile missing
  setup. Never silently migrate frameworks, switch package managers, or upgrade
  major versions; propose those separately.
- **Readiness audit:** the user asks to inspect, audit, recommend, preview, or
  "do not change". Inspect and report gaps with proposed edits; change nothing.

Infer the mode from the request and the destination. Do not ask the user to pick
a mode or learn command syntax.

## Authorization

An explicit setup request authorizes reversible edits inside the target
project: generated or adapted source, dependency installation into the project,
agent instruction files, `.gitignore`, example environment files, and local
verification. It does not authorize commits, pushes, deployment, global tool
installation, changes to user/global host configuration, real credentials,
paid or external services, deleting user files, or rewriting the Git index.
Ask only for an unresolved consequential choice or an action outside this scope,
and continue independent work meanwhile.

## Workflow

1. **Inspect before asking.** Read existing instructions (AGENTS.md and files it
   references, host-specific files), manifests, lockfiles, version pins, source
   layout, scripts, CI, `.gitignore`, and Git status. Record missing referenced
   files accurately. Use [discovery and versions](references/discovery-and-versions.md).
2. **Resolve material requirements.** Ask only questions whose answers change
   the setup: what is built, backend/frontend/both, required frameworks,
   destination, project or module name, persistence/auth/integrations needed
   now, deployment constraints, agent hosts, team conventions. Offer two or three
   plain-language choices with a recommendation; state defaults for low-impact
   decisions and proceed.
3. **Select stack and versions from current evidence.** Any stack is supported:
   follow [stack discovery](references/stack-discovery.md) to find its official
   setup path, and load a stack note below only if one matches. Verify runtime support, release status, compatibility,
   and official scaffolding commands from official documentation or package
   metadata at setup time. Prefer the latest compatible stable release; never a
   prerelease unless requested; never an upgrade of an existing app unless asked.
   Explain conflicts between docs, pins, and installed runtimes before choosing.
4. **Create or adapt the smallest working structure.** Follow framework
   conventions; add folders only with useful files; add databases, auth,
   containers, queues, or deployment config only when required. Use official
   generators only in an empty destination or after confirming their overwrite
   behavior. Explicit user architecture preferences win over defaults.
5. **Configure the agent harness.** Create or reconcile AGENTS.md and any
   selected host file per [agent harness](references/agent-harness.md).
   Preserve existing rules; describe only commands, paths, and capabilities that
   exist. Distinguish app dependencies, agent skills/plugins, and external
   services; never simulate an installation.
6. **Configure ignore rules** per [gitignore and artifacts](references/gitignore-and-artifacts.md):
   preserve existing content, avoid duplicates, keep examples trackable, verify
   with Git, and report already-tracked sensitive or temporary files without
   changing the index.
7. **Verify and report** per [readiness](references/readiness.md). Run the
   actual install, build/check, type check, lint, tests, and a smoke request or
   page load. Only a project that passes every applicable check is "ready".

## Stack notes (optional)

Setup never depends on a note existing. For several applications in one
repository, also read [combined projects](references/combined-projects.md).
Notes record pitfalls already observed for some stacks; load one only when it
matches, and still verify current facts:
[Go + Fiber](references/stacks/go-fiber.md),
[Node.js + Fastify](references/stacks/node-fastify.md),
[Python + FastAPI](references/stacks/python-fastapi.md),
[React + Vite](references/stacks/react-vite.md),
[Vue + Vite](references/stacks/vue-vite.md),
[Next.js](references/stacks/nextjs.md).

## Repeatability and failure

Running setup again must preserve customizations and add no duplicate rules,
instruction sections, dependencies, scripts, or files. Inspect each file before
writing; edit in place rather than overwriting. When a step fails (missing tool,
unreachable registry, documentation unavailable, failing check), stop the
dependent steps, keep completed work, and report completed changes, the failed
step with its actual error, remaining work, and how to resume. Never install a
missing toolchain globally unasked; give the exact command instead. A remembered
version or command is not current evidence; label it unverified.

## Report

Finish with: created or updated files; selected stack, versions, and why;
how to start development; each check as passed, failed, not run, or blocked
with the command used; remaining user actions; and source links for
version-sensitive decisions. This skill needs no Panda Lead or other specialist;
other Panda skills are optional follow-ups for later work.

## Success discipline

Identify the requested outcome and evidence of completion. Continue useful authorized work, keep attention on current evidence, and compare the result with the outcome before reporting completion. State any remaining uncertainty or blocker. Sacca: Call the project ready only when its documented commands were run and behaved as stated.
