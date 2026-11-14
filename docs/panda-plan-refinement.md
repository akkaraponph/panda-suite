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

## Scope-change refinement

Review of the Master File snapshot plan found a concrete propagation failure:
after the user narrowed work to runtime-only, the plan still required a legacy
repair migration in its task list, review focus, file map, deployment check, and
final acceptance checklist. The progress ledger recorded that the migration had
been removed, so the saved plan and its execution record also disagreed.

`panda-plan` now treats an authoritative scope decision as applying across the
whole artifact and searches for stale references to removed work. `panda-execute`
updates the saved plan when the user has already made that decision, removes
descoped work and checks, then continues with remaining authorized tasks. It
asks only when the user's direction leaves scope unsettled.

Blind cases `PLAN-SCOPE-REVISION` and `EXEC-SCOPE-REVISION` cover plan editing
and execution after scope narrowing. The execution fixture starts with a green
suite that does not detect missing invalidation; hidden checks must inspect the
behavior and final plan, not treat passing tests as sufficient. Existing plan
resume and execution-contract cases remain controls. The fixtures were validated
locally: both initial execution-fixture tests pass, while a direct probe confirms
the baseline `sync_and_refresh` never calls invalidation; the 30 tooling tests,
skill validator, and Codex discovery check pass. Fresh-context baseline/skill
model runs are **Not Run**, so behavioral improvement is not yet established.

## Execution readiness and release gate refinement (2026-11-14)

### Baseline capability audit

Inspection covered Plan, Execute, Test, Release, Requirements, Spec, Impact and
Git; skill contracts/routing; scenario catalog, fixtures, preparation/validation
scripts and prior plan-refinement/handoff results. Working tree was clean before
this work. The user-referenced `RTK.md` was unavailable in the workspace, checked
ancestor locations and local skill directories; no instructions were inferred.

| Capability | Current support | Evidence | Identified weakness | Action |
| --- | --- | --- | --- | --- |
| Repository inspection | Supported | Plan steps 1–2 read source, callers, tests, config | No confirmed absence | Preserve, explicitly inspect assertions |
| Requirement traceability | Partial | Step 6 maps requirements to tasks | No explicit check-to-evidence chain | Extend acceptance/check/evidence links; inline for small work |
| Architecture decisions | Supported, some details implicit | Step 3 covers boundaries, proposals and unknowns | Ownership, invariants and dependency direction implicit | Make relevant contracts explicit |
| Task decomposition | Supported, inconsistent results | Step 4 uses testable deliverables; historical proportion runs partial | Oversized plans and test-only splits persisted | Consolidate contract; one inline task for localized work |
| Cross-task interfaces | Supported | Exact consumes/produces signatures in step 4 | Already supported | Preserve; check prerequisite IDs and cycles |
| Verification planning | Supported | Step 6 checks commands/errors/regressions; PLAN-ERROR-BOUNDARY | B's signature defect already corrected | Preserve correction without restating it |
| Risk-based test planning | Partial | Review focus and risks mapped to checks | No explicit plausible wrong implementation/check pair | Add discriminating assertions and fixture needs |
| Release gate definition | Partial | Deployment concerns mentioned; Release owns assessment | No Plan gate structure or evidence-pending boundary | Conditional local gate reference |
| Execution handoff | Supported | Markdown, modes, review and permission boundaries; prior handoff results | No demonstrated consumer defect | Preserve; no Execute edits |
| Scope change handling | Supported, newest correction unevaluated | Whole-artifact reconciliation and stale-term search | New traceability/gates also need reconciliation | Extend existing rule and scenario |
| Plan quality validation | Supported, readiness implicit | Requirement/interface/error/risk checks | No explicit readiness outcome or available-task identification | Plan-only readiness labels |


The release and traceability gaps are instruction gaps found by inspection, not
recorded causal model failures. Historical failures of proportion and scope
propagation remain in the earlier sections and result artifacts. The existing
scope correction was retained rather than rewritten as another warning.

### Contract and implementation

Plan still translates sufficiently agreed requirements into ordered implementation
work. Focused explanations, unclear business policy, standalone specifications,
implementation and actual release assessment retain their existing boundaries.
Inputs are requirements, source, constraints and optional specs; unavailable source
keeps proposed paths provisional. Output remains ordinary Markdown, with stable
task IDs, observable acceptance, relevant contracts and evidence expectations.

The revised workflow co-locates task design, discriminating verification and plan
validation instead of repeating those contracts in the output section. Small work
can use one task without a matrix, review-focus section or release ceremony.
Complex work gets concise Requirement → Task → Check → Evidence links. New
interfaces stay proposed; established interfaces must match inspected source.
Optional test-first sequencing is not a requirement.

`references/release-gates.md` is loaded only for release/deployment/migration or
compatibility boundaries. Each gate links a requirement/risk to an observable
condition, method, expected evidence, blocking status and known revision/environment
constraints. Owners and numerical targets are supplied facts, never inventions.
Gates start **defined; evidence pending**. Missing live evidence can block release
without blocking implementation. Plan readiness labels describe the plan only.

Plan defines future acceptance gates. Execute implements and records checks; Test
owns separately requested test design/execution; Release assesses actual revision
and environment evidence. No peer skill or external framework is required.
No integration defect justified editing Execute or Release or changing routing.
The discovery description remains appropriate to ordered planning work.

Format was checked against the [Agent Skills specification](https://agentskills.io/specification)
on 2026-11-14: matching lowercase folder/name, YAML name/description, Markdown body
and a skill-local conditional reference. Repository validation and real Codex
plugin/standalone discovery are distinct checks, not proof of model performance.

### Evaluation design and artifacts

[Current trial report](../tests/results/plan-ready/comparison.md) separates actual
answers, structural checks and unrun work. Original and candidate instruction
snapshots are retained. The original is the working-tree skill at the start of
this change; historical results above are not relabeled as this comparison.

Reuse existing B, PLAN-ERROR-BOUNDARY, PLAN-INTERFACES, PLAN-PROPORTION,
PLAN-NONTRIGGER, PLAN-HANDOFF/PRESET, EXEC-PLAN-RESUME/SUBAGENT and scope-revision
cases. New scenarios cover only uncovered combinations:

- `PLAN-RELEASE-GATES`: shared policy interface/task quality, ineffective green
  tests, functional/config/report/CLI compatibility gates, timeout/cancellation,
  and missing live-provider evidence in one synthetic versioned CLI.
- `PLAN-EVIDENCE-BOUNDARY`: read-only planning under unavailable test execution,
  credentials and environment; a claimed green suite is not release proof.
- `PLAN-GATE-SCOPE-REVISION`: scope narrowing must remove stale gates and evidence
  links as well as tasks. Its fixture extends the original scope fixture; the
  original is unchanged, so changed inputs are explicit.

The proposed PLAN-TASK-QUALITY, PLAN-TEST-EFFECTIVENESS, PLAN-DEPENDENCY-FAILURE,
PLAN-SMALL-CHANGE and PLAN-HANDOFF-CONSISTENCY behaviors reuse these and existing
cases rather than duplicating prompts for coverage counts. Reviewer expectations
stay in `tests/scenarios/cases.json`, outside blind workspaces. The correct
control and `tests/reviewer/check_plan.py` also remain outside task fixtures.
Both faulty and correct controls pass the ordinary suite; strict-unproven policy
fails only for the faulty one. This demonstrates a discriminating fixture, not
that any model will propose the right check.

### Compatibility and limits

The default `.panda-suite/plans/YYYY-MM-DD-<topic>.md`, explicit destinations,
chat-only output, collision handling, ignore/tracked-file behavior, checkboxes,
authorization and native/subagent modes are preserved. Existing resume/scope
contracts require no new parser or metadata. Scope reconciliation now names
traceability and release gates explicitly.

No token, latency or reliability savings are claimed. Word counts and instruction
snapshots cannot establish token savings; fresh runs remain a small sample and
self-reported command records are not raw host transcripts. Real release-provider
compatibility in the synthetic example is intentionally unavailable. No release,
installation, commit, push or production action is part of this refinement.

The first gate-planning trial exposed a new readiness inconsistency: an unavailable
live-release task appeared in an execution-ready task list. A second revision
separates future release checks from implementation scope and names blocked task
IDs. V1 handoff and v2 B trials also omitted required user-facing mode/review
prompts. A third revision makes the response location explicit in the existing
handoff opener; its result and all earlier partial outcomes remain in the trial
report. These are observed trial failures; they do not establish causality or
reliability from a single rerun.
