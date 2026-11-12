# Snapshot Consistency Implementation Plan

**Goal:** Invalidate the current snapshot before refresh so failed refreshes
fall back to relational values.
**Constraints:** Python 3 standard library only; preserve historical snapshots.

## Review focus

- Invalidation failure behavior is unspecified by the requirements; preserve and
  report the failure rather than claiming refresh ordering succeeded.
- Refresh failure must leave a cache miss (Task 2).
- Startup migration must repair legacy rows (Task 3).

## File map

- `snapshot.py`: completed current-snapshot invalidation.
- `sync.py`, `test_sync.py`: invalidate then refresh.
- `migration.py`, `test_migration.py`, `startup.py`: legacy repair.

## Tasks

### Task 1: Invalidate current snapshot

**Status:** Complete.
**Produces:** `invalidate_current(version_id) -> bool` in `snapshot.py`.
**Check:** `python3 -m unittest -v`.

### Task 2: Invalidate before post-sync refresh

**Status:** Not started.
**Files:** `sync.py`, `test_sync.py`.
**Accept when:** invalidation precedes refresh and refresh failure leaves a
cache miss; historical values remain unchanged.
**Check:** `python3 -m unittest -v`.

### Task 3: Repair legacy rows at startup

**Status:** Not started.
**Files:** `migration.py`, `test_migration.py`, `startup.py`.
**Accept when:** only current affected rows are removed and startup fails on
migration errors.
**Check:** migration scope and startup wiring tests.

## Acceptance checklist

- [ ] Invalidation precedes refresh.
- [ ] Failed refresh reads relational values.
- [ ] Startup migration repairs legacy rows.

## Deployment verification

Run the migration and verify repaired current rows and preserved history.
