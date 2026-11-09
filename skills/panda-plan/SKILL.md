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

1. **Understand requirements.** Extract the intended behavior, non-goals,
   compatibility promises, and acceptance conditions. Resolve ambiguities that
   materially change the plan; record smaller assumptions visibly.
2. **Inspect the system.** Read relevant source, callers, tests, configuration,
   and project instructions. Find existing patterns and capabilities before
   introducing components. Cite paths for current behavior.
3. **Define scope and dependencies.** Identify affected interfaces, data and
   transaction boundaries, integrations, and deployment concerns where relevant.
   Separate known existing contracts from design proposals and open decisions.
4. **Order coherent tasks.** Follow real dependencies. Use milestones only for
   meaningful deliverable boundaries. Each task contains an objective, relevant
   files/components if known, prerequisites, concrete acceptance criteria, and
   verification. Include migrations, rollback/recovery, and observability only
   where the change needs them.
5. **Check the plan.** Map every requirement to a task and every material risk to
   a check or explicit unresolved decision. Check proposed signatures against
   promised error outcomes. Confirm tests can detect the intended
   behavior and important regressions. Do not invent commands without checking
   the repository; mark proposed commands or unavailable checks accurately.
   Where omission, null, empty, and invalid values have different outcomes,
   specify them separately. Check that the proposed language or framework can
   actually deliver the promised error at the stated boundary; leave unresolved
   policy explicit rather than assigning an accidental runtime behavior.

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

Start the document with a title, goal, scope, relevant source or specification,
and constraints. Map the affected files and responsibilities before the tasks.
Include evidence anchors, ordered tasks, dependencies, risks, decisions, and a
verification strategy. Use Markdown checkboxes for actionable steps. Each task
names its objective, affected files or components, prerequisites, acceptance
criteria, and concrete checks. Specify interfaces and expected check results
where they matter. Scale detail to the work and mark unknown paths or commands
as provisional. A task can use this format:

> Add manager rejection in `service.py`; depends on the agreed terminal-state
> contract. Accept when only managers can reject pending requests and a blank
> reason is rejected. Verify with focused permission/status/reason tests and the
> existing approval suite. Persistence is outside the supplied service's scope.

Before delivery, check that each requirement maps to a task, task interfaces
agree, material risks have checks or decisions, and proposed verification can
detect the relevant failures. Link the saved plan in the response and identify
any unresolved decisions or checks. Saving a plan does not require a commit.
When a plan is saved and implementation is a relevant next step, suggest using
`panda-execute` with the saved plan path. Include a ready-to-use request such as
“Use panda-execute to implement `.panda-suite/plans/<filename>.md`.” Preserve
any implementation authorization the user has already given and do not imply
that saving a plan alone authorizes execution.

Do not estimate duration without evidence. Planning authorizes the requested plan
artifact, not application implementation. Do not edit source or tests. Do not
require Panda Lead. A handoff to execution preserves acceptance criteria, current
artifacts, decisions, unknowns, and the user's actual authorization; a generated
plan alone is not approval to execute it.

## Success discipline

Identify the requested outcome and evidence of completion. Continue useful authorized work, keep attention on current evidence, and compare the result with the outcome before reporting completion. State any remaining uncertainty or blocker. Vīmaṃsā: Before finishing, map each acceptance condition to a task and a check.
