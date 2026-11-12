---
name: panda-execute
description: Implement an approved engineering plan or explicitly requested scoped changes, preserving task dependencies, existing conventions, acceptance criteria, and honest verification status.
---

# Panda Execute

Deliver authorized changes and evidence of their behavior. Use this for
implementation; planning-only, investigation-only, and review requests do not
authorize it. No master skill is required.

## Before changing files

Read the plan, acceptance criteria, project instructions, current source, tests,
and working-tree state. Preserve existing user edits. A clear request to implement
or fix counts as authorization for relevant reversible changes; do not ask again.
For a clear small change without a plan file, state a compact task sequence and
proceed. Ask when missing requirements materially change correctness or scope.

## Executing a saved plan

A saved plan is the contract. Implement every task in order with the files,
names, signatures, tests, and values it states; do not rename, merge, or redesign
silently. Track progress in the plan file itself: check off a task's boxes only
after its checks pass, so a later session can resume. On resume, re-run the
checks of tasks already marked done, then continue from the first unchecked
task. Record any necessary deviation under a "Deviations" heading in the plan
with its reason, following the contradiction rule below. Keep going until every
task is verified or a precise blocker remains; do not pause between tasks to ask
whether to continue.

Use the mode the user chose. With none named, run native and mention that a
subagent-driven run is available.

- **Native:** run the execution loop below for each task in this session, then
  review the whole diff against the plan, using a fresh reviewer when the host
  can delegate.
- **Subagent-driven:** for each task, give a fresh implementer only that task's
  text, its interfaces note, the plan's constraints, and the relevant paths.
  Re-run the task's checks yourself; a subagent's report is not evidence. Then
  give a fresh reviewer the task, the plan's acceptance criteria, and the diff;
  fix material findings before the next task. Run tasks that touch the same
  files one at a time. Finish with one whole-change review. If the host cannot
  delegate, say so and run native.

## Execution loop

1. Select the next unblocked task in dependency order. Name its objective and
   acceptance criteria. Re-check current implementation before editing.
2. Make the smallest coherent change following existing conventions. Preserve
   required compatibility, validation, error handling, and business rules. Avoid
   unrelated refactoring. Add or update tests when they meaningfully detect the
   changed behavior or regression.
3. Run the task's relevant checks using the actual repository commands. Inspect
   output and exit status. Check supplied tests against each acceptance rule;
   exercise uncovered input boundaries before calling the task verified.
   Derive expected outcomes from the contract, independently of the implementation
   and test names. If a required behavior is missing from the suite, run a focused
   discriminating check; keep supplied tests intact when their modification is
   outside scope. Report a green suite separately from acceptance completeness.
   On failure, establish what executed, the failing state,
   and its cause before changing code. If helpful and available, use the existing
   `panda-debugger` instructions; its absence does not block ordinary diagnosis.
4. Compare results with acceptance criteria. Record **implemented**, **verified**,
   **partially verified**, **blocked**, or **not started** and continue with work
   whose dependencies are satisfied. Preserve actual commands and failure details.
5. Review the completed diff for omissions, unwanted changes, and remaining risk.
   Finish only when the requested scope is delivered or the remaining blocker is
   stated precisely. A failed check is not a completed verification gate.

If evidence contradicts the plan, stop affected work and explain the contradiction
and revised approach. Obtain a decision when the revision materially changes
scope, requirements, or risk; continue already authorized independent work.
Destructive actions, production changes, deployment, publishing, and external side
effects require authorization covering those actions. Local implementation alone
does not authorize them.

## Delivery report

State what changed and why, acceptance status, executed checks and actual results,
unrun checks with reasons, incomplete tasks, and material risks. Never call a test
passed before it finishes successfully. Missing tools support a precise limitation,
not an invented result. Pass current paths, decisions, evidence, remaining work,
and authorization into any requested review or documentation activity.

## Git handoff

When authorized work reaches commit messages or Git operations, load available
`panda-git` guidance for classification and repository safety. Instruction loading
is not a separate-agent invocation. If unavailable, report that limit and apply
repository conventions and ordinary Git safety directly; no mandatory dependency
is introduced. Preserve existing authorization: implementation alone does not
authorize commits, pushes, or published-history rewrites.

## Success discipline

Identify the requested outcome and evidence of completion. Continue useful authorized work, keep attention on current evidence, and compare the result with the outcome before reporting completion. State any remaining uncertainty or blocker. Appamāda: Under pressure, recheck remaining acceptance criteria and the completeness of deliverables.
