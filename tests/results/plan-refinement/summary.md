# Plan refinement evaluation

Date: 2026-11-12. One fresh context per case and arm, same inherited model, no
model override; temperature and per-run token use beyond the host's reported
subagent totals were not controlled. Agents received only `TASK.txt`, the fixture,
and the instruction file it names; reviewer checks stayed in `cases.json`.
"Previous" is `skills/panda-plan/SKILL.md` at `d27c10a`; "revised" is the working
tree version described in [the refinement note](../../../docs/panda-plan-refinement.md).

## Results

| Case | Arm | Result | Notes |
| --- | --- | --- | --- |
| PLAN-INTERFACES | baseline | Pass (5/6, partial on step form) | Strong: exact signatures, unstated inputs, `int()` pitfalls; tests are descriptive lists, not named |
| PLAN-INTERFACES | previous | Pass (5/6, partial on step form) | Global interface block, decisions D1–D9; tests unnamed; field-limit trick to exercise `csv.Error` |
| PLAN-INTERFACES | revised | Pass (6/6) | Per-task consumes/produces, named tests with exact values, review focus section mapped to tests |
| PLAN-PROPORTION | previous | Partial | Correct and scoped; tests split into a separate task with unnamed checks; plan longer than the code |
| PLAN-PROPORTION | revised | Partial | Correct and scoped; named tests and review focus; still longer than the code and spells out the return body |
| B (regression) | revised | Pass | Tests folded into the delivering task; preserves manager and terminal rules; saved plan; no edits |
| PLAN-ERROR-BOUNDARY (regression) | revised | Pass | Sentinel default; omitted / `None` / blank distinguished and tested; minor `str = _MISSING` annotation slip; still splits tests into a separate task |
| PLAN-NONTRIGGER | lead | Pass | Direct answer (`KeyError`), no plan, no files |

## Analysis

- **Correctness did not change.** The previous and revised versions reached the
  same design decisions on PLAN-INTERFACES, and both carry the same open defect
  candidate: a malformed CSV quote stops later rows, contrary to requirement 2.
  Both flagged it as unresolved; the no-skill baseline avoided it by rejecting
  the whole paste.
- **Structure changed as instructed.** Only the revised arm wrote per-task
  consumes/produces, named every test with exact expected values, and added a
  review-focus section. That is instruction compliance in one sample per arm,
  not evidence of better executions downstream; no plan was executed.
- **Proportion guidance had no visible effect.** Every arm wrote a plan several
  times longer than the code it describes (PLAN-INTERFACES: baseline 1,569
  words, previous 2,526, revised 2,260). The revised arm used fewer code-fence
  lines (12 vs 33), but prose still fixes most bodies.
- **Task right-sizing is followed inconsistently** (B folded tests in;
  PLAN-ERROR-BOUNDARY did not).
- The no-skill baseline was already strong on this fixture, so the case
  discriminates weakly between arms.

## Limits

One run per arm. No executor run measured whether the revised plans reduce
implementation mistakes. Token and time comparisons are not reported as
savings.
