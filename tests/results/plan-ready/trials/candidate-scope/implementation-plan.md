# Snapshot Consistency Implementation Plan

**Goal:** Keep the current Dynamic document snapshot correct after Master File sync.

**Scope:** Runtime invalidation, rebuild, and relational read fallback only.
Legacy snapshot repair is deferred and outside the authorized scope; do not add
startup migration or repair work.

**Sources:** `scope-decision.md` is authoritative for scope; `requirements.md`
defines runtime behavior. The previous plan records Task 1 as complete, but this
fixture contains no source, tests, or test output to verify that status.

**Constraints:** Python 3 standard library only; add no dependencies. Preserve
historical revisions. Restrict invalidation and rebuilding to the current
snapshot for the affected document/version; never invalidate historical rows.

## Requirements and runtime contract

- **R1:** After Master File sync, invalidate the affected current snapshot before
  attempting its rebuild.
- **R2:** If rebuilding fails, leave that snapshot absent and serve reads from
  relational data; do not return the pre-sync stale snapshot.
- **R3:** Preserve historical revisions on both successful and failed rebuilds.
- **R4:** Use only Python 3 standard library capabilities and existing project code.

The supplied plan names `invalidate_current(version_id: str) -> bool` in
`cache.py`. Treat this as a recorded interface pending source confirmation, not
a newly verified API. Its required postcondition is that the affected current
snapshot cannot be read after successful invalidation. Confirm the meaning of
its boolean return before wiring the caller. An invalidation failure must not
be treated as successful invalidation or permit rebuilding to proceed while a
stale current snapshot remains readable. Existing failure signaling, rebuild and
read signatures must be inspected before choosing integration details.

## Provisional file map

No source files are supplied. Confirm these paths and responsibilities in the
implementation repository before editing; do not create replacement modules
merely because these names appear here.

| File/component | Responsibility |
| --- | --- |
| `cache.py` | Current snapshot invalidation and current-versus-historical selection |
| `sync.py` | Invalidation followed by rebuild after successful Master File sync |
| Existing document read component, path to locate | Relational fallback on a current snapshot miss |
| `test_sync.py` and existing cache/read tests, paths to confirm | Runtime ordering, failure fallback, and historical regression coverage |

## Review focus

- A rebuild spy alone can pass while reads still serve stale data: Task 2 must
  read through the real document read boundary after a failed rebuild.
- An overly broad delete can satisfy the current-cache miss check while losing
  history: Tasks 1 and 2 must assert historical contents are unchanged.
- A caller may ignore an invalidation failure: Task 2 must verify that rebuild
  is not attempted when invalidation fails.

## Ordered tasks

### Task 1: Confirm the existing current snapshot invalidation contract

- [ ] Verify the previously recorded implementation and its acceptance evidence.

**Prior status:** Recorded complete in the supplied plan; not verified here.
**Requirements:** R1, R3, R4.
**Prerequisites:** Access to the implementation source and test tooling.
**Consumes:** `version_id: str` identifying the affected current snapshot, plus
existing current/historical selection rules from source.
**Produces:** Confirmed `invalidate_current(version_id: str) -> bool` contract,
including return/error meaning, and evidence that invalidation removes only the
affected current snapshot. If source differs, reconcile the interface in this
plan and its caller before Task 2; do not introduce a second competing API.
**Affected components:** `cache.py` and its existing tests, paths provisional.
**Acceptance and checks:** Seed an affected current snapshot, a historical
revision and an unrelated current snapshot. Invoke invalidation and assert only
the affected current snapshot is absent, the other contents are unchanged, and
the observed return matches the documented success contract. Inspect failure
behavior and identify the caller-visible failure signal. Confirm no new
third-party dependency is required.

### Task 2: Make the post-sync runtime path consistent

- [ ] Integrate invalidation, rebuild, and relational fallback with regression coverage.

**Requirements:** R1–R4.
**Depends on:** Task 1's confirmed invalidation signature and failure semantics.
**Consumes:** The affected `version_id: str`, confirmed invalidation behavior,
and the existing rebuild and document-read interfaces identified from source.
**Produces:** A post-sync path that invalidates before rebuilding and a read path
that returns relational values after a failed rebuild leaves a cache miss.
Preserve existing public signatures and historical revision behavior.
**Affected components:** `sync.py`, existing cache/read components if needed,
`test_sync.py` and relevant existing regression tests; paths provisional.
**Acceptance and discriminating checks:**

| Scenario | Expected assertion | Incorrect implementation rejected |
| --- | --- | --- |
| Sync changes relational value from A to B with cached A; rebuild succeeds | Invalidation occurs before rebuild, current read returns B, rebuilt snapshot contains B | Rebuilding before invalidation or retaining stale A |
| Same fixture; rebuild fails | Current snapshot remains absent and a read through the document API returns relational B | Logging failure while retaining or restoring A; fallback that never reaches relational data |
| Invalidation fails | Rebuild is not called; caller observes the established failure signal | Ignoring failure and continuing with a readable stale snapshot |
| Success and rebuild-failure cases include historical and unrelated snapshots | Their stored values remain byte-for-byte unchanged | Deleting all versions or unrelated current snapshots |

Use unit-level call-order checks for orchestration and integration-level checks
through existing cache and document-read boundaries for data results. Stub only
the rebuild failure; retain the real cache-miss/fallback path in that test. Keep
existing successful-sync and historical-read regressions passing. Record the
actual test names, assertions and results as implementation evidence.

## Verification and traceability

`python3 -m unittest -v` is the command proposed by the supplied plan. It has not
been confirmed against repository tooling or executed here because no source or
tests are supplied. Confirm discovery runs the relevant tests, record their
names/count, and use the repository's actual command if different. A zero-test
success is not acceptance evidence.

| Requirement | Task | Required evidence |
| --- | --- | --- |
| R1 | 1, 2 | Current-only invalidation assertions and observed invalidation-before-rebuild ordering |
| R2 | 2 | Failed rebuild leaves a miss; public read returns updated relational value B |
| R3 | 1, 2 | Historical and unrelated snapshot contents unchanged across invalidation and rebuild outcomes |
| R4 | 1, 2 | Source/dependency diff confirms standard-library-only changes |

All checks above are planned, not passed. No deployment action is part of this
plan.

## Acceptance checklist

- [ ] Confirm source paths, invalidation return/error contract, rebuild/read interfaces, and test command.
- [ ] Runtime invalidation precedes rebuild for the affected current snapshot.
- [ ] Failed rebuild leaves a cache miss and reads return relational values.
- [ ] Invalidation failure does not proceed to rebuild.
- [ ] Historical revisions and unrelated snapshots remain unchanged.
- [ ] No third-party dependencies are introduced.
- [ ] Required regression checks have recorded passing evidence.

## Readiness and handoff

**PARTIALLY READY:** Scope and required runtime outcomes are settled. Task 1 is
the first unblocked verification activity once the implementation repository is
available. Task 2 depends on confirming Task 1's recorded interface and locating
the existing rebuild/read boundaries. Source absence is an evidence gap; this
fixture does not establish implementation or test completion.

Review this revised plan before implementation. A later request can use
`panda-execute` in native mode to implement `implementation-plan.md`; the two
tasks share one small runtime contract. This planning request does not authorize
source or test edits.
