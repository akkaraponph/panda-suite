# Snapshot Consistency Plan

**Goal:** Keep the current Dynamic document snapshot correct after Master File sync: invalidate it before rebuilding, and use relational data if rebuilding fails. Preserve historical revisions.

**Scope:** Runtime snapshot invalidation, refresh orchestration, read fallback, and their regression checks. No application implementation is authorized by this planning task.

**Sources and precedence:** `requirements.md` defines runtime behavior and the Python constraint. `scope-decision.md` is authoritative: runtime correctness only; startup migration and legacy snapshot repair are deferred and excluded. This decision replaces the earlier repair proposal throughout this plan.

**Constraints:** Python 3 standard library only; add no dependencies. Historical revisions must remain unchanged. Do not change source or tests while revising this plan.

**Evidence limits:** Only the supplied planning fixtures are available. Source, callers, assertions, repository tooling, and a release revision/environment have not been inspected. Paths and the existing helper signature below come from the previous plan and must be confirmed in Task 1. No checks were executed. Its prior “Complete” status for Task 1 is an unverified report, not acceptance evidence.

## Runtime contracts and file map

- `cache.py`: current snapshot invalidation and read behavior. The previously reported interface is `invalidate_current(version_id: str) -> bool`; retain its signature and confirm its actual return semantics before depending on them. Do not interpret `False` as success or failure without inspecting the implementation. Invalidation must remove or render unusable the current snapshot before refresh starts, without altering historical revisions.
- `sync.py`: after a successful Master File sync, invalidate the affected current snapshot, then rebuild it from updated relational data. Existing refresh and read entry points and signatures are not supplied; reuse and record them during Task 1 rather than introducing a new public API.
- `test_sync.py`: proposed location for orchestration/failure regression assertions, subject to actual test layout. Existing cache/read tests should hold invalidation, history, and fallback checks where those behaviors belong.

A failed rebuild must leave the current snapshot unavailable; subsequent reads must return relational values, never the previous snapshot or a partially rebuilt value. Publish a replacement only after a successful rebuild. Restrict all mutations to the affected current revision. Preserve existing sync failure behavior and public signatures; the requested change concerns snapshot consistency after successful sync. No schema, public API, or dependency change is proposed.

## Review focus

- A populated stale snapshot can mask an incorrect refresh-before-invalidation order: check the invalidation event and cache miss at rebuild entry (Task 2, C2).
- A rebuild that fails after beginning work can leave stale or partial data readable: force that failure and read through the actual application read path (Task 2, C3).
- Current and historical snapshots can share a document identity: seed both and verify history remains unchanged on success and failure (Tasks 1–2, C1/C4).
- A successful rebuild can still use pre-sync values: seed distinct old and updated relational values and assert the resulting snapshot and read match the updated values (Task 2, C4).

## Ordered tasks

### Task 1: Confirm and verify current-only invalidation

- [ ] **Outcome:** Establish the existing invalidation/read/refresh contracts and verify that current invalidation preserves history.

**Requirements:** R1, R3, R4 below. **Prerequisites:** None. **Files:** `cache.py`, existing cache/read tests, and relevant callers/tooling when available; file names beyond `cache.py` remain provisional.

**Consumes:** The previously reported `invalidate_current(version_id: str) -> bool` and existing current/historical revision selection.

**Produces:** A verified helper with the same signature, plus recorded actual boolean semantics, refresh/read signatures, and runnable test commands for Task 2. If the helper is already correct, retain it and verify its behavior; change it only as needed for the runtime requirements during later authorized execution.

**Acceptance / C1:** Seed an affected current snapshot, a historical revision for the same document, and an unrelated snapshot. Invoke invalidation for the current version. Assert the affected current snapshot cannot be read as a snapshot, the historical and unrelated snapshots are unchanged, and the actual boolean result matches the established contract. Inspect absent-current behavior so Task 2 does not misclassify a legitimate cache miss as an error. This rejects broad deletion and ineffective invalidation.

**Verification:** Unit tests using standard-library `unittest` and existing storage fixtures. Inspect discovery configuration before running the proposed command `python3 -m unittest -v`; choose the repository's actual command if different. Required evidence: command, revision, assertions and result, with actual API semantics recorded. Prior completion remains unverified until this evidence exists.

### Task 2: Refresh after sync and preserve relational fallback

- [ ] **Outcome:** Refresh the affected current snapshot from updated relational state after sync, with safe reads after failure.

**Requirements:** R1–R4. **Prerequisite:** Task 1; consumes its verified `invalidate_current(version_id: str) -> bool`, boolean semantics, existing refresh/read signatures, and confirmed test command. **Files:** `sync.py`, the existing snapshot read path if needed, `test_sync.py` or its confirmed equivalent, and cache/read regressions.

**Produces:** Existing post-sync orchestration that calls current invalidation before the existing refresh entry point for the affected `version_id: str`, and the existing read path returning relational data on a current snapshot miss. Reuse existing interfaces; do not add a public function based on an unverified name or signature.

**Acceptance and checks:**

- **C2 — order:** Seed an old populated snapshot and updated relational values. Trigger successful Master File sync through the real orchestration path. At refresh entry, assert invalidation has already occurred and the old snapshot is unavailable. Assert the affected current version is the target. Reject implementations that only invalidate after refresh or skip invalidation when refresh succeeds.
- **C3 — failure and fallback:** Inject a refresh failure after rebuild has begun. Assert no old or partial current snapshot remains readable, then read through the actual application read path and assert the updated relational values are returned. A mock proving only that a fallback function was called is insufficient. Use existing failure handling and avoid publishing partial snapshots.
- **C4 — successful refresh and history:** Assert a successful refresh publishes current values equal to the updated relational data and subsequent reads return them. Compare historical snapshot contents before and after both successful and failed refresh; assert no change. Also retain the unrelated snapshot control from C1. Reject rebuilding from pre-sync data or mutating history.
- **C5 — constraints/regressions:** Inspect the implementation diff for third-party dependencies and unintended public signature/schema changes. Run confirmed existing cache, read, and sync regressions as well as C1–C4. Record actual assertions covered; a suite exit code alone is insufficient.

**Verification:** Standard-library unit/integration tests against the available storage fixture, using mocks only to inject failure or observe order. No external service requirement is established. If real storage cannot be exercised, label that evidence gap rather than calling a mocked read/storage interaction sufficient proof of persistence behavior.

## Traceability

| Requirement / source | Task | Check | Expected evidence |
| --- | --- | --- | --- |
| R1: Correct current snapshot after sync; invalidate before rebuild (`requirements.md`) | 1, 2 | C1, C2, C4 | Current-only invalidation assertions, observed event order, updated successful snapshot/read values |
| R2: Rebuild failure falls back to relational data (`requirements.md`) | 2 | C3 | Injected failure, unavailable stale/partial snapshot, application read equals updated relational values |
| R3: Preserve historical revisions (`requirements.md`) | 1, 2 | C1, C4 | Before/after historical contents unchanged under invalidation, refresh success and failure |
| R4: Python 3 standard library only, no dependencies (`requirements.md`) | 1, 2 | C5 | Diff review and confirmed regression command/results without added packages |
| R5: Runtime-only authorization (`scope-decision.md`) | 1, 2 | C5 and plan scope review | Diff and plan contain only runtime work and supporting verification |

## Acceptance checklist

- [ ] C1 verifies current-only invalidation and preserves history.
- [ ] C2 proves invalidation precedes rebuilding after sync.
- [ ] C3 proves failed rebuild leaves a miss and reads updated relational data.
- [ ] C4 proves successful refresh uses updated data and history survives both outcomes.
- [ ] C5 verifies standard-library constraints, compatibility and relevant regressions within the runtime-only scope.

## Release gates — defined; evidence pending

These gates apply to the actual runtime change revision. No gate has passed, and this plan does not assess release readiness.

| Gate / requirement or risk | Required condition | Verification / expected evidence | Blocking | Revision / environment |
| --- | --- | --- | --- | --- |
| GATE-RUNTIME / R1, R2: stale or partial current reads | Invalidate before rebuild; successful rebuild uses updated data; failed rebuild leaves a miss and relational reads | C2–C4 results, including storage-backed read assertions and injected failure evidence | Yes: core runtime correctness | Actual release revision and supported Python/storage environment not supplied; capture with evidence |
| GATE-HISTORY / R3: historical data mutation | Current operations leave historical revisions unchanged on success and failure | C1/C4 before-and-after snapshot assertions | Yes: mandatory preservation | Same actual revision and storage fixture as runtime checks |
| GATE-CONSTRAINTS / R4, R5: unauthorized changes or compatibility regression | Standard library only; runtime scope; existing public signatures preserved; relevant regressions pass | C5 diff review and confirmed test results | Yes: explicit constraints | Actual release diff, dependency metadata if present, and confirmed repository command |

**Deployment verification:** On the release revision, run the confirmed runtime checks above against the supported storage test environment. In a representative deployment environment, sync a controlled document with distinct old/current relational values; verify the new current read and preserved historical contents. Verify failure fallback through controlled failure injection in a test environment. Capture revision, environment and assertion results. Deployment access and those results remain evidence gaps.

**Rollback and risks:** Reverting runtime code cannot restore correct refresh behavior; relational data remains the fallback source when the current snapshot is unavailable. Test failure paths before rollout. Historical mutation would breach the plan's invariant; it is prevented and checked, not accepted as a repair step. No schema/data migration is included, and existing legacy snapshot state is not corrected by this change. Existing invalidation failure and sync error handling must be inspected in Task 1; preserve established behavior unless it prevents the required ordering, in which case record the conflict before dependent implementation.

## Readiness and handoff

**EXECUTION-READY for Task 1; PARTIALLY READY for the entire plan.** Task 2 depends on Task 1 confirming source contracts and invalidation result/error semantics. The first unblocked task is Task 1. No product scope decision remains open, but source evidence, confirmed commands, implementation acceptance results, release revision and deployment evidence are missing. Task checkboxes remain unchecked until the required evidence exists.

Review this revised plan before implementation. A future native `panda-execute` run is proportionate for two closely dependent runtime tasks; request: “Use panda-execute (native) to implement `implementation-plan.md`.” This handoff does not authorize implementation or claim the gates have passed.
