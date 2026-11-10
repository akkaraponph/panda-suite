---
name: panda-refactor
description: Assess, plan, or implement structural improvements to existing code while preserving observable behavior and supported contracts. Use for refactoring responsibilities, dependencies, duplication, or module boundaries with baseline checks and incremental verification; respect requests limited to analysis or planning.
---

# Panda Refactor

Carry a bounded structural improvement from evidence through verification. Combine
complexity assessment, planning, scoped implementation, and effective testing
around the behavior that must remain stable. This workflow is complete on its own;
Panda Lead and peer skills are optional.

## Resolve the requested outcome

Read the target, project instructions, relevant callers/tests/configuration,
existing plans, and working-tree state. Start locally and expand with dependency
and risk evidence. Preserve unrelated user edits. Identify the concrete maintenance
problem and completion condition; adequate existing code may warrant no change.

| Request | Deliverable and editing boundary |
| --- | --- |
| ANALYZE: assess opportunities | Evidence-backed findings and priorities; source/tests unchanged |
| DESIGN: compare structures | Current/proposed responsibilities, alternatives and trade-offs; write only a requested artifact |
| PLAN: order the work | Incremental plan with files, prerequisites, invariants and checks; no source/test edits |
| EXECUTE: refactor the target | Relevant reversible code/test changes, baseline and incremental verification |
| REVIEW: inspect a refactor diff | Material compatibility/correctness findings; read-only unless repairs requested |
| QUICK: concise assessment or bounded edit | Depth modifier on the requested outcome; preserves its permissions and necessary checks |

Infer the outcome from natural language; mode names are optional. An explicit
implementation request authorizes scoped local work without a second approval of
its internal plan. Analysis and planning alone do not authorize implementation.
External effects, destructive operations, production changes and publication need
authorization covering those actions. A material contract/scope decision is distinct
from routine reversible engineering choices.

## Preservation loop

1. **Discover the problem and contract.** Trace responsibilities, public entry
   points and consumers. Cite concrete complexity costs rather than stylistic
   preferences. Identify observable inputs/outputs, errors, permissions, state and
   side effects. Distinguish current observations, documented requirements,
   interpretations and unknowns. For public API/import moves, state or transaction
   changes, concurrency, or conflicting source/tests/requirements, read
   [compatibility guidance](references/compatibility.md).
2. **Define invariants and resolve contradictions.** Map each material behavior
   to evidence and a check. Include supported imports/call shapes and relevant
   ordering, mutation, failure, retry or event guarantees. If existing behavior
   violates requirements, disclose the pre-existing defect: preserving it during
   a pure refactor and correcting it are different outcomes. Obtain a decision
   only when existing authorization does not cover the behavioral choice. Avoid
   silently fixing the defect or turning it into an intended contract through a
   characterization test. Continue independent useful work while that choice is
   unresolved.
3. **Choose the smallest useful structure.** Respect domain language and existing
   conventions. Compare no change, a minimal improvement, and a larger structural
   alternative only when the decision warrants them. Justify abstractions with
   actual coupling, responsibilities or necessary variation. Explain the concrete
   benefit; fewer lines or architectural elegance alone is insufficient.
4. **Establish baseline and order changes.** Before code edits, run relevant
   existing checks and record pre-existing failures. Inspect assertions against
   requirements; green tests may omit a material contract. Add discriminating
   tests for meaningful gaps when authorized, asserting observable outcomes
   rather than private structure. Use a compact sequence for small work; for
   substantial work, order tasks with dependencies, acceptance and verification.
   Reuse satisfactory completed discovery/plans instead of restarting them.
5. **Implement and verify increments when authorized.** Make one coherent change,
   inspect the diff, run relevant checks, and reconcile the invariants before the
   next dependent change. Investigate a new unexplained failure before continuing
   affected work. Preserve tests' meaningful assertions; do not weaken tests or
   alter business rules to achieve green. Keep unrelated fixes and cleanup out
   of scope. Adapt implementation-coupled tests only with an explanation and
   preserved coverage of their behavioral purpose.
6. **Check completion and stop.** Review the final diff, affected consumers and
   invariant/check mapping. Use compilation, type checks, focused tests, contracts,
   integration or differential checks as warranted. Differential equality can
   preserve an existing bug; passing tests bound confidence to exercised behavior.
   Stop when the requested objective is met, including a justified no-change
   conclusion. Report unverified boundaries without claiming universal equivalence.

For a persisted plan, default to `.panda-suite/plans/YYYY-MM-DD-<topic>.md` using
the current local date; honor an explicit destination or chat-only request.
Preserve existing files and ensure root `.gitignore` covers `/.panda-suite/`;
verify with `git check-ignore`. Report already tracked plan artifacts and leave
the index unchanged. Scope a planning-only request to its plan and this ignore
configuration; source and tests remain unchanged.

## Conditional specialist knowledge

Use available peer instructions through the host's documented discovery/loading
mechanism only when deeper help is useful for the current activity:

- `panda-simplify`: substantial or disputed complexity assessment and alternatives.
- `panda-plan`: multi-component dependencies and a durable implementation plan.
- `panda-execute`: complex implementation and acceptance tracking.
- `panda-test`: coverage gaps, boundary selection and test effectiveness.
- `panda-impact`: deeper dependency and compatibility assessment.
- `panda-review`: requested diff review or a required completion review.

Load relevant guidance, not every peer as a mandatory chain. Carry objective,
invariants, evidence, artifacts, decisions, unknowns and authorization between
activities. Missing peers do not block the core workflow or require installation.
Reading instructions is not a programmatic skill invocation. Peers need not
redispatch through Lead or restart Refactor.

A general complexity assessment belongs with Simplify; a plan-only deliverable
with Plan; an existing approved implementation plan with Execute; test-only work
with Test; general diff review with Review. Respect direct Refactor invocation
within its requested scope. Causal defects and measured performance optimization
belong with Debugger and Perf respectively; structural changes alone establish
neither a diagnosis nor a speed improvement.

## Limits and report

If tools or dependencies are unavailable, identify the exact unrun check and use
feasible static or focused evidence. A baseline failure is not a new regression;
report it separately and avoid unrelated repair. Pause affected changes when a
material compatibility uncertainty cannot be resolved. Bound consumer searches:
no local reference does not establish that a public interface has no consumers.

Scale the report to the work: objective, evidence-backed problem, changes or
recommendation, concrete structural benefit, preserved contracts, actual commands
and results, outstanding decisions and risks. For checks use **PASS**, **FAIL**,
**NOT RUN**, or **BLOCKED** with reasons. Report implementation separately as
implemented, partially implemented or not started. A passing suite does not imply
all acceptance conditions were verified. Claim performance improvements only with
measurements. No additional architecture report is required for a small extraction.

## Git handoff

When authorized work reaches commit messages or Git operations, load available
`panda-git` guidance for classification and repository safety. Instruction loading
is not a separate-agent invocation. If unavailable, report that limit and apply
repository conventions and ordinary Git safety directly; no mandatory dependency
is introduced. Preserve existing authorization: implementation alone does not
authorize commits, pushes, or published-history rewrites.

## Success discipline

Compare the requested outcome with delivered work and the invariant/check mapping.
Preserve unfavorable evidence and revise the approach when it contradicts the
preferred structure. Completion requires useful structural change or justified
advice and an honest account of verified behavior, not an expanding rewrite.
