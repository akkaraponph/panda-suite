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
   When requirements span independent subsystems, propose one plan per subsystem,
   each yielding working, testable software.
4. **Order coherent tasks.** Follow real dependencies. Use milestones only for
   meaningful deliverable boundaries. Each task contains an objective, relevant
   files/components if known, prerequisites, concrete acceptance criteria, and
   verification. Include migrations, rollback/recovery, and observability only
   where the change needs them. Size a task so it ends in an independently
   testable deliverable: fold setup, configuration, and documentation into the
   task that needs them, and split only where a reviewer could accept one part
   and reject the other. When later tasks depend on earlier ones, give each task
   an interfaces note: what it consumes and produces, with exact names and
   signatures, because an implementer may see only their own task.
5. **Write decisions, not code.** Each step lets the implementer write exactly
   one reasonable thing. A test step names the test and its assertions with the
   requirement's exact values; a code step names the file, signature, and pinned
   values, with a body only for an algorithm the signature and tests leave open;
   a verification step names the command and the result that means success.
   Replace lines that decide nothing ("TBD", "handle edge cases", "add
   validation", a type no task defines). A plan longer than the code it describes
   has written the code instead.
6. **Check the plan.** Map every requirement to a task and every material risk to
   a check or explicit unresolved decision. Check that names, types, and
   signatures used in later tasks match where they are defined. Check proposed signatures against
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
and constraints; copy project-wide constraints with exact values from the source
requirement. Add a review focus: up to five inputs or failure modes the
requirements imply but no task yet tests, most likely first, each with the
behavior a reasonable user expects, and add its test to the owning task. Say
when the check found none. Map the affected files and responsibilities before the tasks.
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
agree, material risks have checks or decisions, proposed verification can
detect the relevant failures, and no step is a placeholder or a code transcript. Link the saved plan in the response and identify
any unresolved decisions or checks. Saving a plan does not require a commit.

## Execution handoff

When a plan is saved and implementation is a relevant next step, ask the user to
review the plan and, unless they already chose, how `panda-execute` should run it:

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
