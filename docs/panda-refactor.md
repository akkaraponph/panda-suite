# Panda Refactor: design and evaluation

Version 1.2.0 adds a standalone refactoring skill. Its user-facing
purpose is one bounded structural improvement carried through baseline checks,
incremental changes and compatibility verification. Simplify, Plan, Execute and
Test already cover the component methods; better completion or easier use through
this entry point remains a hypothesis, not a demonstrated capability gap.

## Contract and design

The [skill](../skills/panda-refactor/SKILL.md) owns the preservation loop and works
when copied alone. Optional peer guidance deepens only the current activity.
There is no orchestrator runtime, mandatory peer chain, global configuration or
new dependency. The supplied principal-engineer draft informed the contract;
role titles and mandatory architecture alternatives were replaced by concrete
completion checks. QUICK controls depth, not authorization.

Analysis and review are read-only; design writes only a requested artifact;
planning writes its plan; explicit implementation permits scoped reversible
code/test changes. Public behavior, supported imports, permissions, errors,
mutation and relevant side-effect boundaries are explicit invariants. Existing
source/requirement conflicts are disclosed before a behavioral choice; refactoring
does not silently authorize a defect correction. Tests establish bounded evidence,
not universal equivalence or measured speed improvement.

The discovery format was checked against the primary
[Agent Skills specification](https://agentskills.io/specification) on 2026-11-10.
Directory/name matching and local references are validated separately from host
inventory and task behavior.

## Evaluation inputs

`tests/scenarios/cases.json` contains reviewer-only expectations. Nineteen new
`REFACTOR-*` cases cover small implementation, module boundaries, transaction/event
ordering, analysis, planning, review, green-suite gaps, conflicting requirements,
wrong assumptions, missing consumers, unavailable execution, baseline failures,
user edits, scope pressure, quick work, nonactivation, test-only routing,
standalone use and a justified no-change conclusion.

Seven small standard-library fixture directories under `tests/fixtures/refactor-*`
keep source, requirements and ordinary tests separate from reviewer checks.
Green and Conflict have identical passing ordinary tests; a duplicate/order check
passes the correct control and fails the defective implementation. The Review
fixture changes guard/formatting order; its oracle passes Before and fails After.
Effects checks state atomicity and event timing. Baseline intentionally includes
one unrelated failure; it is not part of default tooling test discovery.

Validate fixture distinctions from the repository root:

```sh
python3 -B tests/reviewer/check_refactor.py
```

This executes synthetic fixtures, not model comparisons. To verify a delivered
implementation independently, run the reviewer outside the task context:

```sh
python3 -B tests/reviewer/check_refactor.py --target /tmp/refactor-green-output --kind labels
python3 -B tests/reviewer/check_refactor.py --target /tmp/refactor-small-output --kind greeting
```

Run Effects' supplied tests against delivered code as well. Keep original supplied
tests intact as reviewer inputs if a task changes its local test files.

## Blind run protocol

Prepare a fresh workspace for each case and arm; use new destinations:

```sh
python3 scripts/prepare-evaluation.py --case REFACTOR-SMALL --arm baseline --destination /tmp/refactor-small-baseline
python3 scripts/prepare-evaluation.py --case REFACTOR-SMALL --arm specialist --destination /tmp/refactor-small-candidate
python3 scripts/prepare-evaluation.py --case REFACTOR-NONTRIGGER --arm lead --destination /tmp/refactor-nontrigger-lead
```

Preparation is not isolation: generated task files contain absolute instruction
paths into the checkout. Before a real trial, expose only allowed instruction
snapshots in an isolated runner and rewrite those paths to that snapshot. Exclude
the repository scenario catalog, this report, reviewer checks, previous answers
and current chat from task access. Do not claim blindness from copying alone.

Use these arms with the same neutral task, model/settings, budget, tools and inputs:

1. Baseline: no Panda instructions.
2. Existing workflow: frozen pre-change Lead and existing peers, no Refactor.
3. Candidate standalone: Refactor and its local reference only.
4. Candidate with peers: Refactor plus the existing peer inventory.
5. Candidate routed: updated Lead/catalog, for routing/nonactivation cases.

For Existing workflow, use a pre-change Git revision or the local ignored
`.panda-suite/refactor-before/` snapshot captured before implementation. Record
revision or hashes. Do not use updated Lead as the old workflow. For standalone,
copy only `skills/panda-refactor/`, then update TASK.txt to its isolated location.
For peer trials expose the same inventory as the control plus Refactor; no
mandatory loading. Use documented manual preparation rather than adding a runtime.

Before DIRTY, initialize a disposable Git fixture, commit its baseline, append
`# user-owned note: retain this` to service.py and create untracked notes.txt.
Record hashes/content before the task. This setup is reviewer preparation, not
an instruction for the task agent to create its own pre-existing edits.
TOOLS requires a genuinely read-only tool policy; a prompt alone is not tool
isolation. Record any missing enforcement as a trial limitation.

Start with SMALL, BOUNDARY, GREEN, CONFLICT, ANALYZE, PLAN, TOOLS and NONTRIGGER;
then cover remaining risks before release-readiness claims. Forced skill prompts
cannot establish natural activation; use the routed arm for that question.

Save actual tasks, instruction hashes/loaded paths, model settings or unknowns,
commands and raw results, before/after diffs and delivered artifacts. Rate
correctness, usefulness, completion, scope, test effectiveness, verification
honesty and unnecessary loading as pass/partial/fail/not applicable with evidence.
Re-execute delivered code using reviewer checks. Record time/tokens only when
exposed reliably. Preserve unfavorable results and changed conditions.

A material behavior regression or unauthorized edit rejects that candidate
revision. If the candidate adds no observed value, merge its useful guidance into
existing skills or retain only an explicitly justified convenience entry point.
A small sample cannot establish universal superiority.

## Status and limits

Implementation has local package, fixture and discovery results
recorded in the [implementation verification record](../tests/results/refactor/verification.md).
Behavioral comparisons across all five arms are **Not Run**. The repository has
preparation and discovery tooling but no configured isolated comparative model
runner. Available Codex/Claude CLIs alone do not establish comparable settings,
blind access or a controlled experiment; no substitute model answers were invented.
Behavior-driven refinement remains pending actual trials. No improvement,
speed/token savings or universal language-coverage claim follows from this work.

The 1.2.0 release packages these instructions and evaluation scenarios. Behavioral
comparisons remain unrun. No pinned upstream or frozen historical evaluation
artifact is changed; no new runtime or migration is required.
