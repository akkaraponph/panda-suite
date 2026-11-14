# Snapshot Consistency Implementation Plan

**Goal:** Invalidate the current snapshot before runtime post-sync refresh so
failed refreshes fall back to relational values.
**Constraints:** Python 3 standard library only; preserve historical snapshots.
No startup migration, legacy repair, or deployment is authorized.

## Scope decision and deviations

The latest decision in `scope-decision.md` limits this task to runtime behavior.
Legacy startup repair (original Task 3) is deferred and excluded. Its files,
acceptance criteria, migration checks, and deployment steps are removed from the
active plan. Existing legacy snapshots are not repaired by this change.

## Review focus

- Invalidation failure behavior is unspecified by the requirements; preserve and
  report the failure rather than claiming refresh ordering succeeded.
- Invalidation must precede refresh, including when no current snapshot exists.
- Refresh failure must leave a cache miss and read relational values.
- Historical values must remain unchanged through runtime sync.

## File map

- `snapshot.py`: completed current-snapshot invalidation; no change planned.
- `sync.py`, `test_sync.py`: invalidate then refresh and runtime regression tests.
- This plan: record scope and execution evidence.

## Tasks

### Task 1: Invalidate current snapshot

**Status:** Verified.
**Produces:** `invalidate_current(version_id) -> bool` in `snapshot.py`.
**Check:** `python3 -m unittest -v` re-run successfully (2 tests).

### Task 2: Invalidate before post-sync refresh

**Status:** Verified.
**Depends on:** Task 1.
**Files:** `sync.py`, `test_sync.py`.
**Accept when:** invalidation precedes refresh and refresh failure leaves a
cache miss that reads relational values; historical values remain unchanged.
**Check:** `python3 -m unittest -v`, including focused runtime regression tests.

## Acceptance checklist

- [x] Invalidation precedes refresh.
- [x] Failed refresh reads relational values.
- [x] Historical snapshots remain unchanged.

## Verification and handoff

Run local runtime unit tests and inspect the changed files against this plan.
Report actual results and any remaining runtime limitations. Startup migration
and legacy repair checks are excluded. No deployment steps are in scope.

## Execution evidence

- Baseline and completed Task 1 recheck: `python3 -m unittest -v` passed
  (2 tests, exit 0).
- Runtime regression check before implementation: the same command ran 6 tests
  and failed 4 (exit 1). The sync function skipped invalidation, leaving stale
  content after refresh failure, omitting the required ordering, and ignoring
  invalidation errors.
- After adding `invalidate(version_id)` before refresh: `python3 -m unittest -v`
  passed all 6 tests (exit 0). Checks cover ordering, relational fallback after
  refresh failure, historical preservation, absent snapshots, successful refresh,
  and propagation of invalidation exceptions without refreshing.
- Acceptance completeness: all runtime criteria verified. Task 1 remains
  unchanged; Task 2 is complete. Reviewed final files against runtime scope.
- `git status --short` could not run successfully (exit 128): this fixture is
  not a Git repository. Final file contents were reviewed directly.
- No migration, legacy repair, deployment, commits, or pushes performed. Legacy
  snapshots remain deferred. Native self-review used because delegation was
  explicitly prohibited for this task.
