# Using Panda Suite

Use this guide after following the [installation instructions](../README.md).
Open the repository you want to work on in your agent. Skills are instructions
applied by that agent; installing them does not start services or execute tasks.
Only install one copy of a skill name to avoid ambiguous selection.

## Invoke a skill

| Installation | Lead | Specialist example |
| --- | --- | --- |
| Codex standalone | `$panda-lead` | `$panda-test` |
| Codex plugin | Select `panda-suite:panda-lead`, or use `$panda-suite:panda-lead` | Select `panda-suite:panda-test`, or use `$panda-suite:panda-test` |
| Claude Code plugin | `/panda-suite:panda-lead` | `/panda-suite:panda-test` |
| Claude Code standalone | `/panda-lead` | `/panda-test` |

The examples below use standalone Codex names. Substitute the selector for your
installation. Discovery was checked on Codex 0.159.2 and Claude Code 2.1.251;
interactive plugin invocation was not exercised. If a typed selector is not
recognized, choose its discovered name in the host skill picker. Other hosts
must use their documented instruction-loading mechanism.

Include the desired outcome, relevant files or URL, constraints, and whether
changes are allowed. Paths in prompts below are examples to replace with actual
project files. Do not paste secrets, production records, or credentials into a
prompt. A skill can inspect accessible files; it cannot infer missing permissions
or access tools that the host does not provide.

## Choose a workflow

Start with Lead if unsure, or invoke a specialist directly. A specialist does not
require Lead. Lead selects only necessary activities and skips completed work.

```text
$panda-lead Implement the approved feature in docs/approval-plan.md, review the
change, add meaningful tests, and prepare release notes. Local code and docs may
change. Do not deploy, publish, push tags, or change production data.
```

Expect implementation and verification evidence plus a release-preparation handoff,
not deployment. A simple question can be answered directly. You can request only a
plan or review without authorizing implementation.

For idea requests, expect options and a recommendation before a finished artifact.
Before suggesting another skill, tool, or component, Lead checks existing coverage;
keeping the current approach is a valid recommendation. An explicit creation
request still authorizes the requested artifact without reopening settled choices.

## Product discovery and requirements

### Panda Brainstorm

Provide the user problem, existing system context, and constraints. Use this when
the direction is undecided; use Requirements when you need testable business rules.

```text
$panda-brainstorm Our five-person support team approves refunds manually.
Compare extending the existing admin application with a separate approval service.
Inspect src/refunds first. Recommend a direction with assumptions and trade-offs.
Do not implement or create an execution plan.
```

Expect a problem statement, goals/non-goals, alternatives, recommendation, risks,
and open decisions. Exploration does not authorize source changes.

Recommendations consider existing capabilities and may favor no addition. If you
challenge a suggestion, expect reassessment of its premise and deciding evidence,
with speculative opportunities distinguished from demonstrated gaps.

### Panda Research

Provide a bounded technical question, relevant source paths or URLs, versions,
constraints, and the decision it informs. Use it when investigation is the main
task; other skills still gather ordinary evidence themselves.

```text
$panda-research Check whether the SDK version pinned in this repository supports
our required authentication flow. Compare implementation and official versioned
documentation. Cite deciding claims, explain contradictions and unknowns, and
save docs/auth-research.md. Do not change code or install dependencies.
```

Expect a direct answer, supporting findings and citations, relevant versions/dates,
uncertainty, and decision implications. Research is read-only except for requested
notes; small answers need no saved file. Use Brainstorm to explore a direction,
Debugger for a causal failure, Impact for a proposed change, and Write for a guide.
See [scope and verification](panda-research.md).

### Panda Requirements

Provide stakeholder requests, current workflow, actors, known policy, and constraints.

```text
$panda-requirements Refine docs/customer-request.md into requirements for multiple
approvals. Inspect the existing service. Ordering, quorum, self-approval and edit
invalidation are undecided. Give identified requirements, permissions, acceptance
criteria, conflicts and open decisions. Do not choose those policies or implement.
```

Expect a Requirements Analysis: business goal, scope, actors, functional and relevant
quality requirements, business rules, acceptance, edge cases, and open questions.
It is suitable input to Plan; unspecified business rules remain open.

## Design and implementation

### Panda Impact

Provide the exact proposed change and source/contracts available for tracing.

```text
$panda-impact Analyze replacing order_status strings with integer codes. Trace
models, queries, API responses, UI callers, jobs and tests that actually exist.
Separate confirmed dependencies from possible external consumers and unknowns.
Assess compatibility, migration/recovery risks and required verification. Read-only.
```

Expect affected components, confidence-labeled impacts, compatibility/data/API and
operational risks, mitigations, checks, and unknowns. No migration or source edit occurs.

### Panda Plan

Provide agreed requirements, source, compatibility constraints, and any design.

```text
$panda-plan Plan docs/approval-requirements.md against src/approvals and its tests.
Include ordered tasks, dependencies, file locations, acceptance criteria and
verification per task. Preserve existing callers. Save docs/approval-plan.md;
do not implement the feature.
```

Expect an actionable plan, evidence anchors, risks and unresolved decisions. A
request to save a plan authorizes that document, not application changes.

Where error contracts matter, expect omitted, null, empty, and invalid inputs to
be distinguished. Proposed signatures must be capable of producing the promised
errors; for example, a required Python argument omitted by a caller normally raises
`TypeError` before function validation can raise `ValueError`.

### Panda Spec

Provide requirements, source, audience/language, and an existing template if available.

```text
$panda-spec เขียน Backend Technical Specification ภาษาไทยจาก
docs/approval-requirements.md และ src/approvals ใช้ template ของโครงการ
แยกพฤติกรรมปัจจุบัน ข้อเสนอ และประเด็นที่ยังต้องตัดสินใจ
ระบุ interface, validation, permission, error และ test strategy เท่าที่มีหลักฐาน
บันทึกที่ docs/approval-spec.md โดยไม่แก้ application code
```

Expect current/proposed technical contracts, relevant failure/data/operational
considerations, verification strategy and open decisions. English works too.
For an ADR, request context, options, decision status, consequences and revisit
conditions. A recommendation is not recorded as stakeholder approval.

### Panda Execute

Provide an approved plan or a clearly scoped implementation request and acceptance.

```text
$panda-execute Implement docs/approval-plan.md. Preserve existing API callers,
update relevant tests, and run the repository checks. Report actual commands,
acceptance status and unrun checks. Do not deploy or publish.
```

Expect scoped changes, per-task progress, actual verification and remaining risks.
An explicit implementation request already authorizes relevant workspace edits.
Material scope/requirement/risk changes require a new decision.

Verification derives expected outcomes from acceptance rules as well as existing
tests. A green supplied suite may leave a required behavior unchecked; expect
focused checks for those gaps and a separate statement of acceptance completeness.
Restrictions on editing supplied tests remain in force.

## Quality and investigation

### Panda Test

Provide expected behavior, implementation, existing tests and allowed test scope.

```text
$panda-test Add regression tests for owner-only cancellation in src/orders.py.
Use existing unittest conventions. Cover owner success, non-owner rejection,
shipped orders and unchanged state on failure. Run them. You may change tests
and local fixtures; do not modify application code to make a failing test pass.
```

Expect test scope/scenarios, test files, execution results, coverage gaps and risks.
A discovered defect can produce a useful failing test. An unavailable real database
means integration is Not Run; a mock does not become real integration evidence.

### Panda Debugger

Provide expected/actual behavior, reproduction clues, failing test/log/trace or source.

```text
$panda-debugger Investigate why transfer returns success but balances remain
unchanged. Inspect src/transfers and run the available local regression. Show the
causal trace, evidence and CONFIRMED/LIKELY/UNKNOWN confidence. Propose the smallest
fix and its verification. Do not edit application code or tests.
```

Expect a supported cause analysis, reproduction status, fix proposal, test status
and remaining risks. To authorize repair in the same request, say “investigate and
fix”; no second approval is needed for that scope. Missing evidence stays explicit.
The detailed technique remains in its skill-local `references/` documents.

### Panda Sec

Supply a diff/base or bounded code scope, security expectations, lockfiles and
available dependency reports.

```text
$panda-sec Audit src/api and dependency-audit.json against the resolved lockfile.
Trace attack conditions and controls. Rank supported vulnerabilities with severity,
confidence, locations, evidence, fixes and regression checks. Redact secret values.
Do not edit, install scanners, use credentials, upload data or scan externally.
```

Expect a scoped vulnerability report and dependency applicability triage, including
failed/unrun scans and coverage limits. This is a dedicated audit; ordinary diff
review still checks security defects without invoking Sec automatically.

### Panda Perf

Supply the slow operation, workload sizes, runtime, resource target if known,
source/tests and available CPU, memory, query-count or plan evidence.

```text
$panda-perf Analyze src/events.py for repeated lookups and memory retention.
Produce a minimal optimization diff preserving order, duplicates and permissions.
Run safe local equivalence and repeated synthetic comparisons; label missing
production evidence. Do not apply the patch or change database schema.
```

Expect ranked cost evidence, concrete diffs, semantic and resource trade-offs,
actual comparisons and unverified checks. To apply edits, request the optimization
explicitly. A sequential scan or high RSS alone does not prove a bottleneck/leak.
Production load tests, profiling and database operations require matching scope.

### Panda Review

Provide the PR, diff, or explicit comparison boundary and intended behavior.

```text
$panda-review Review the current branch against origin/main for the owner-only
cancellation requirement. Trace changed behavior and callers. Report material
defects with severity, precise location, trigger, evidence, impact and correction.
Do not fix code.
```

Expect prioritized actionable findings or a concise no-significant-findings result
with review limits. Speculation is not presented as a confirmed vulnerability or
measured performance failure. Review authorization does not authorize repairs.

Review compares changed behavior with the contract even when supplied tests pass.
Expect a concrete triggering case for a supported defect; correct changes should
receive no invented finding merely because a test gap exists.

### Panda Simplify

Provide the artifact, demonstrated use cases and invariants to preserve.

```text
$panda-simplify Assess src/messages for unnecessary factories and forwarding
adapters. It serves one admin greeting flow. Preserve the permission check,
public call shape and exact output. Recommend a simpler design, trade-offs,
regression risks and verification. Do not edit.
```

Expect concrete complexity costs and a smaller alternative with preserved
invariants. Fewer lines alone are not success. Say “apply the simplification” if
you also want bounded edits and verification.

### Buddhist Method

Use at a specific uncertainty, repeated failure, complexity decision or pressure point.

```text
$buddhist-method Check the claim that approve() persists to PostgreSQL before
we describe it in release notes. Inspect the source and actual test evidence.
Separate established behavior from assumptions. Do not change code.
```

Expect evidence-based judgment and visible uncertainty, not a mandatory philosophical
report. Original terminology and technique Markdown remain inside the main skill.
Lead does not load this method as a stage between every activity.

## Documentation and delivery

### Panda Write

Provide audience, document purpose/language, source paths and output location.
For an update, provide the existing document; for a review, state whether edits
are authorized. Preserve established language and format unless asked to change them.

```text
$panda-write Write docs/approvals-guide.md for new backend developers using the
current src/approvals implementation. Include a runnable example and actual error
behavior. Rejection is only proposed, so do not document it as implemented.
Use clear English. Do not modify application code.
```

Expect the requested document, evidence anchors, checked examples and explicit gaps.
Thai documentation is supported. Each integration is traced independently;
implementation, configuration, deployed state, and remote contracts stay distinct.
Exact unresolved facts use `Pending Confirmation` with the evidence needed.
Review-only requests return findings without edits. Substantial architecture
explanations and handovers use conditional guidance without imposing chapters
on short guides. See the [Write refinement report](panda-write-refinement.md).
Use Spec for implementation-oriented design and
Manual for user interactions rather than automatically invoking all three.

### Panda Manual

Provide an accessible test application or supplied UI evidence, role, journey,
language and permitted actions. Browser access is optional, not assumed.

```text
$panda-manual Document saving a draft at http://127.0.0.1:8765 for a test user.
Observe actual labels and outcomes; capture useful screenshots with synthetic
data. Save docs/draft-manual.md. Do not send messages, publish or delete records.
If the browser is unavailable, make a labeled draft from supplied evidence only.
```

Expect prerequisites, ordered steps/outcomes, supported validation/recovery paths,
actual captures if available and observed/documented/unverified distinctions.
See the [browser-observed example](../tests/results/browser-manual/manual.md).

### Panda Release

Provide release boundary/version, target, requirements, test/review evidence and
known migration/configuration changes. Missing evidence is acceptable input.

```text
$panda-release Prepare the change from origin/main to HEAD for staging. Inspect
the diff, acceptance criteria and available test results. Produce release notes,
deployment/recovery checklists, blockers and post-deploy checks. Classify READY,
CONDITIONALLY READY, BLOCKED or UNKNOWN with evidence. Do not deploy, tag, publish,
apply migrations or send announcements.
```

Expect a reviewable readiness decision and preparation artifacts. No discovered
issue is not sufficient evidence for READY. A known mandatory failure is BLOCKED;
insufficient deciding evidence is UNKNOWN. Preparation does not execute the release.

## Maintaining skills

### Panda Skill Lab

Provide the skill, target task/failure mode, observed outputs and available host tools.

```text
$panda-skill-lab Evaluate whether panda-plan catches contradictions between
proposed signatures and promised errors. First inspect existing coverage. Design
blind baseline and skill cases with identical inputs, tools and model settings,
fresh contexts per arm, and nonactivation/scope cases. If no runner is available,
deliver the protocol and mark comparisons Not Run. Do not edit skills yet.
```

Expect purpose/failure mode, contract, cases, actual results where run, comparison
limits, weaknesses and narrowly justified improvements. Ask explicitly to create
or edit a skill when wanted. No simulated baseline, fabricated benchmark or token
savings is acceptable. See [evaluation instructions](../tests/evaluation.md).

Historical failures may already have instruction corrections. Expect inspection
of the current skill before more rules are proposed. A locally validated fixture
with green tests and an uncovered contract defect establishes a useful test case,
not an improvement in model behavior. Use fresh contexts and a correct control
for behavioral comparisons. See [v1.1.1 scope and evidence](v1.1.1.md).

## Practice locally

The [scenario list](../tests/scenarios/cases.json) provides example tasks and reviewer
checks; keep those checks hidden from agents when evaluating. Prepare a disposable
task workspace from the Suite checkout:

```sh
python3 scripts/prepare-evaluation.py --case EXP-TEST --arm specialist --destination /tmp/panda-test-practice
```

Open that directory in your agent and follow `TASK.txt`. The fixture deliberately
contains an authorization defect: a useful test should fail. Use a fresh destination
for another attempt; preparation refuses existing directories. Do not mistake the
intentionally broken fixture tests for failing Suite tooling checks.

## Troubleshooting and stopping conditions

- Skill absent: confirm the installation directory or plugin is enabled; refresh
  or restart the host. Check that the complete directory includes `SKILL.md`.
- Duplicate names: choose one installation method and review old copies before
  removing or replacing them. The copy utility refuses existing skill names.
- Missing browser, database, telemetry or runner: provide the smallest missing
  evidence or accept a labeled draft/Not Run result. Do not invent observations.
- Changed instructions mid-task: state the new scope explicitly; prior constraints
  remain unless replaced. Consequential actions require authorization covering them.
- Proposed design described as current: request source anchors and explicit
  current/proposed/open distinctions before relying on the artifact.
