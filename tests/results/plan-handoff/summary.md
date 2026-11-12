# Plan handoff and plan-driven execution evaluation

Date: 2026-11-12. One fresh context per case and arm, same inherited model, no
model override. Agents saw only `TASK.txt`, the fixture, and the instruction file
it names; reviewer checks stayed in `cases.json`. "Previous" is the working-tree
`panda-plan` / `panda-execute` before the execution-handoff change; "revised"
adds the handoff menu to Plan and the saved-plan contract and modes to Execute.
Each agent was told the user could not reply, so a question ends its answer.

Execution workspaces were graded with [verify_exec.py](verify_exec.py), which
checks exact plan names, reason strings, test names, untouched originals, plan
checkboxes, and a real unittest run. On the unfinished fixture it passes 4/22
checks (control).

## Results

| Case | Arm | Result | Notes |
| --- | --- | --- | --- |
| PLAN-HANDOFF | previous | Fail (handoff checks) | Saved plan; generic "Use panda-execute" line; no review ask, no mode choice |
| PLAN-HANDOFF | revised | Pass | Asks for review, offers native and subagent-driven, recommends native from task count, coupling and cost; ready request with mode and path; waits |
| PLAN-HANDOFF-PRESET | previous | Pass (weak) | Carried "with subagents" into its request; review implied, not asked |
| PLAN-HANDOFF-PRESET | revised | Pass | Keeps the chosen mode without a menu; asks only for review |
| EXEC-PLAN-RESUME | previous | 30/30 graded; partial on contract | Silently rewrote already-checked Task 1 (whitespace lines) without a Deviations note; briefly wrote a sibling directory outside the workspace |
| EXEC-PLAN-RESUME | revised | 30/30; pass | Re-ran Task 1 checks, left Task 1 code untouched, finished Tasks 2–3 without pausing, raised the whitespace question instead of changing done work |
| EXEC-PLAN-SUBAGENT | revised | 30/30; pass | Fresh implementer and reviewer per task plus whole-change review; re-ran tests itself after each task; boxes checked |
| C (regression) | revised | Pass | 5 supplied tests pass, tests unchanged; symbols separate words; disclosed `Straße` → `stra-e` limit |
| PLAN-ERROR-BOUNDARY (regression) | revised | Pass | Chat-only: no menu, sentinel boundary kept |

## Analysis

- **The requested behavior appears only with the revision.** The previous Plan
  never offered an execution mode unprompted; the revised one did, with a
  plan-grounded recommendation, and suppressed the menu for chat-only and
  preset cases.
- **Execution outcome did not differ on the graded checks.** Both Execute
  versions finished every task with exact names; the fixture's plan was
  explicit enough that the previous version followed it too. The visible
  difference is plan discipline: the previous version changed completed work
  without recording it in the plan.
- **Subagent-driven mode works in this host** when delegation is available; the
  no-delegation fallback was not exercised.
- PLAN-HANDOFF-PRESET discriminates weakly.

## Limits

One run per arm. No run measured whether subagent-driven mode catches more
defects than native mode. The fallback path without delegation and a mid-plan
contradiction are untested.
