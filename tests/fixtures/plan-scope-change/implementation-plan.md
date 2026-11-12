# Snapshot Consistency Plan

**Goal:** Make current snapshots correct after Master File sync and repair old
stale snapshots at startup.

**Constraints:** Python 3 standard library only. Preserve historical revisions.

## Review focus

- Runtime refresh failure falls back to relational values (Task 2).
- Startup migration excludes historical revisions (Task 3).

## File map

- `cache.py`: current snapshot operations.
- `migration.py`: one-time legacy repair.
- `sync.py`: post-sync refresh orchestration.

## Tasks

### Task 1: Invalidate current snapshot

**Status:** Complete.
**Produces:** `invalidate_current(version_id: str) -> bool` in `cache.py`.
**Check:** `python3 -m unittest -v`.

### Task 2: Refresh current snapshot after sync

**Status:** Not started.
**Depends on:** Task 1.
**Files:** `sync.py`, `test_sync.py`.
**Accept when:** invalidation runs before refresh; refresh failure leaves a cache
miss and does not cause a stale value to be returned.
**Check:** `python3 -m unittest -v`.

### Task 3: Repair legacy snapshots on startup

**Status:** Not started.
**Files:** `migration.py`, `test_migration.py`, `startup.py`.
**Accept when:** migration deletes only current affected revisions and startup
fails if repair fails.
**Check:** migration scope and startup wiring tests.

## Acceptance checklist

- [ ] Runtime invalidation precedes refresh.
- [ ] Failed refresh falls back to relational values.
- [ ] Startup migration repairs legacy snapshots and preserves historical rows.

## Deployment verification

Run the startup migration, then query current and historical snapshot rows.
