# Panda Plan refinement

Date: 2026-11-12.

## Evidence and design

The earlier evaluation recorded one Plan defect (case B, 2026-11-07): an
omitted-argument error promise that conflicted with the proposed signature. Step
"Check the plan" already carries a correction for it, covered by
`PLAN-ERROR-BOUNDARY`; this revision leaves that wording unchanged.

The remaining changes close instruction gaps found by inspection. They target
hypothesized failures, not observed ones:

| Earlier instruction | Refinement |
| --- | --- |
| "Task interfaces agree" checked only at the end | Dependent tasks state what they consume and produce, with exact names and signatures |
| No guidance on task size | Each task ends in an independently testable deliverable; setup and docs fold into the task that needs them |
| "Scale detail to the work" | Each step decides exactly one thing; placeholders ("TBD", "handle edge cases") and pasted implementations are both defects |
| Requirements mapped to tasks | Review focus: up to five implied but untested inputs or failure modes, each with a test in the owning task |
| Constraints listed | Project-wide constraints copied with exact values |
| One plan per request | Independent subsystems get separate plans |

Not adopted: mandatory test-first steps and per-step commits (execution and Git
policy belong to Panda Execute and Panda Git), an execution-method menu (Plan
already hands off to Panda Execute), and a different save path.

## Evaluation

New blind cases: `PLAN-INTERFACES` (multi-task import against the new
`plan-import` fixture), `PLAN-PROPORTION` (plan length versus code), and
`PLAN-NONTRIGGER` (focused question; no plan). The fixture's two supplied tests
pass locally; that validates the fixture, not model behavior.

Eight fresh runs on 2026-11-12 are saved in
[tests/results/plan-refinement](../tests/results/plan-refinement/summary.md).
The revised wording passed both regressions (`B`, `PLAN-ERROR-BOUNDARY`) and the
nonactivation case. On `PLAN-INTERFACES` it produced the requested structure
(per-task interfaces, named tests, review focus) where the previous version and
the no-skill baseline did not, but design correctness was the same. The
proportion guidance had no visible effect; every arm wrote plans much longer
than the code. One run per arm, so no claim of improved plan quality or lower
token use is made from this sample.

## Execution handoff (second revision)

The user asked Plan to end by offering an execution mode and Execute to treat a
saved plan as a binding contract. Plan now asks for review and offers
**subagent-driven** or **native** execution through `panda-execute`, with a
recommendation grounded in the plan; it keeps a mode the user already named and
omits the menu for chat-only answers. Execute now follows a saved plan's names,
tests, and values exactly, checks off boxes only after checks pass, resumes from
the first unchecked task after re-running finished checks, records deviations in
the plan, and runs to completion without pausing between tasks. Subagent-driven
mode uses a fresh implementer and reviewer per task, re-runs checks itself, and
falls back to native when the host cannot delegate.

New cases: `PLAN-HANDOFF`, `PLAN-HANDOFF-PRESET`, `EXEC-PLAN-RESUME`, and
`EXEC-PLAN-SUBAGENT`, with the `plan-execute` fixture (Task 1 already done).
Results are in
[tests/results/plan-handoff](../tests/results/plan-handoff/summary.md): the mode
offer appeared only with the revision; both Execute versions completed the plan,
but only the revised one left finished work unchanged. One run per arm.
