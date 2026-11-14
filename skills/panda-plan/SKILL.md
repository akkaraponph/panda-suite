---
name: panda-plan
description: Create engineering implementation plans from requirements and existing source when the user needs ordered tasks, dependencies, acceptance criteria, risks, and verification before execution.
---

# Panda Plan

Convert agreed requirements into work an engineer can execute. Exploration of an
unclear product need belongs before planning; a technical contract alone is a
specification, not an execution plan.

## Inputs and workflow

Use the requirements, repository, constraints, and requested scope. An existing
design or spec is optional. If source is unavailable, identify the affected
unknowns and label any proposed file layout as provisional.

1. **Understand requirements.** Extract intended behavior, non-goals,
   compatibility promises, and mandatory acceptance conditions. Keep supplied
   requirement IDs; assign concise IDs where needed for cross-references. Resolve
   ambiguities that materially change correctness or scope; label confirmed
   facts with sources, proposed choices, assumptions, and unresolved decisions.
2. **Inspect the system.** Read relevant source, callers, test assertions,
   configuration, and project instructions. Cite paths for current behavior.
   Reuse existing capabilities and the simplest architecture meeting the need.
3. **Define scope and contracts.** Identify affected interfaces, source of truth,
   data ownership, invariants, module/dependency direction, and failure/recovery
   behavior where relevant. For changed public boundaries, state compatibility
   promises and their checks, including error semantics and version/migration
   constraints. Include rollback feasibility and observability where needed.
   For independent subsystems, propose separate plans with testable deliverables;
   keep shared contracts and prerequisites explicit.
4. **Order coherent tasks.** Follow real dependencies. Give each task a stable
   ID, action title, outcome, requirement references, affected files/components,
   prerequisites, observable acceptance conditions, and verification. State
   preserved versus changed behavior and exclusions where they affect execution.
   Each dependent task states what it consumes and produces, with exact names,
   types/signatures and compatibility constraints, so its implementer can act
   from that task and the plan's constraints alone. Label new interfaces proposed;
   established interfaces must match source. Fold setup, tests and documentation
   into the useful behavior they support. Split when parts can be accepted
   independently; a task need not equal one commit or one test.
5. **Plan discriminating verification.** For each critical behavior, identify a
   plausible incorrect implementation and the assertion or check that rejects it.
   Specify test level, relevant normal/failure inputs, expected results, needed
   fixtures/dependencies and existing regressions. Prioritize authorization,
   state, invalid inputs, duplicates, concurrency, rollback, dependency failure
   or idempotency only when relevant. Inspect assertions: a green suite may
   leave acceptance conditions untested. Confirm commands from repository tooling;
   label proposed commands and unavailable environments. Checks remain planned
   until executed; planning observations do not prove future implementation.
   Test-first sequencing is optional; choose it only when useful.
6. **Check the plan.** Trace every mandatory requirement to a task and every
   acceptance condition to a check and expected evidence, or an explicit evidence
   gap. For complex work, use a compact Requirement → Task → Check → Evidence
   table; for a small change, put those links in its single task. Check prerequisite
   IDs exist, order has no cycles, and cross-task names, types and error outcomes
   agree. Resolve placeholders with concrete decisions or explicit blockers;
   specify signatures and exact required values, leaving ordinary implementation
   bodies to the implementer. Check relevant regressions and material risks have
   checks, mitigations or open decisions.
   Where omission, null, empty, and invalid values have different outcomes,
   specify them separately. Check that the proposed language or framework can
   actually deliver the promised error at the stated boundary; leave unresolved
   policy explicit rather than assigning an accidental runtime behavior.
   When an authoritative scope decision changes an existing proposal, apply it
   throughout the artifact. Reconcile the goal, scope, constraints, file map,
   review focus, tasks, dependencies, risks, traceability, release gates, acceptance
   checklist, verification, and handoff; remove stale work and checks. Keep a brief decision note only
   when future readers need to know why scope changed. Before delivery, search
   for names and terms from the removed scope and resolve every remaining
   reference, including references that imply the work is still required.

## Output and completion

Save the plan as Markdown at `.panda-suite/plans/YYYY-MM-DD-<topic>.md`, using
the current local date and a short lowercase hyphenated topic. Create the directory
when needed. An explicit user-requested destination takes precedence. Avoid
overwriting an unrelated existing plan; choose a distinct descriptive filename.
When the user requests an answer only in chat, honor that format. If the workspace
cannot be written, provide the plan in the response and explain the limitation.

When saving a plan inside `.panda-suite` in a Git repository, ensure the
repository root `.gitignore` ignores `/.panda-suite/`. Create the file if needed,
preserve existing entries, and avoid adding a duplicate when an existing rule
already covers the directory. Verify the intended plan path with `git check-ignore`.
Ignore rules do not remove files already tracked by Git; report any tracked
`.panda-suite` files and leave the index unchanged. If the ignore rule cannot be
updated or verified, report that limitation. Respect an explicit request to track
the plan or a repository instruction requiring it.

Start with title, goal, scope, source/specification and constraints, carrying
project-wide constraints with exact required values. Map affected files and
responsibilities, then ordered tasks with Markdown checkboxes for actionable work.
For substantial changes add a review focus: up to five likely implied but untested
inputs/failures, expected behavior, and the owning task's check; say when none
remain. A localized change can use one short task with its source, contract,
acceptance and checks inline, without separate matrices or ceremonial sections.
Write decisions and expected evidence, not implementation transcripts.

For a defined release, deployment, migration or compatibility boundary, read
[release gate planning](references/release-gates.md) and define proportional gates.
Otherwise omit release gates. Planning defines what must be verified;
`panda-release`, when requested and available, assesses the actual revision and
its evidence. `panda-execute` owns implementation and check execution; `panda-test`
owns separately requested test work. These skills are optional, not dependencies.

Before delivery apply step 6 and assess **plan readiness**:

- **EXECUTION-READY:** no unresolved decision blocks authorized implementation.
- **PARTIALLY READY:** name tasks that can start and decisions/prerequisites blocking others.
- **BLOCKED:** critical scope or contract decisions prevent execution.

Assess readiness across every task in the saved execution scope; name blocked
task IDs rather than labeling that entire scope ready. Name the first unblocked
task and any evidence gaps. An unavailable release
check may leave implementation ready while release evidence remains missing.
These labels do not assess release readiness; defined gates are not passed gates.
A task checkbox records completion only after its required acceptance checks
produce evidence. Link the saved plan and identify unresolved decisions/checks.
Saving a plan requires no commit.

## Execution handoff

When a plan is saved and implementation is a relevant next step, end the
user-facing response with a request to review the plan and, unless already chosen,
a choice of how `panda-execute` should run it. Put the review/mode request in the
response, not only inside the saved plan:

- **Subagent-driven:** a fresh agent implements each task and a fresh reviewer
  checks it before the next starts, then one whole-change review. Most thorough;
  costs a fresh context per task and review. Offer only when the host can delegate.
- **Native:** this session implements every task, then one review of the whole
  change (by a fresh reviewer when the host can delegate). Cheapest and fastest;
  no independent review until the end.

Recommend one in a sentence grounded in the plan: how many tasks, how much they
depend on each other's interfaces, and what a shipped mistake would cost. Give a
ready-to-use request such as “Use panda-execute (native) to implement
`.panda-suite/plans/<filename>.md`.” When the user already named a mode, keep it
and ask only for the review. When the user asked for a chat-only answer or no
execution, mention the handoff without the menu. Wait for the user's answer:
saving a plan, or choosing a mode in advance, does not by itself authorize
starting implementation unless the user's request already did.

Do not estimate duration without evidence. Planning authorizes the requested plan
artifact, not application implementation. Do not edit source or tests. Do not
require Panda Lead. A handoff to execution preserves acceptance criteria, current
artifacts, decisions, unknowns, and the user's actual authorization; a generated
plan alone is not approval to execute it.

## Success discipline

Identify the requested outcome and evidence of completion. Continue useful authorized work, keep attention on current evidence, and compare the result with the outcome before reporting completion. State any remaining uncertainty or blocker. Vīmaṃsā: Before finishing, map each acceptance condition to a task and a check.
