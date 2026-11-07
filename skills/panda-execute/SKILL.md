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

## Success discipline

Identify the requested outcome and evidence of completion. Continue useful authorized work, keep attention on current evidence, and compare the result with the outcome before reporting completion. State any remaining uncertainty or blocker. Appamāda: Under pressure, recheck remaining acceptance criteria and the completeness of deliverables.
