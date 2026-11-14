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

## Traceability

| Requirement | Task | Verification | Expected evidence |
| --- | --- | --- | --- |
| Runtime invalidation | Task 2 | Runtime order and fallback checks | Assertions pass |
| Repair legacy snapshots | Task 3 | Startup migration scope check | Migration evidence |

## Release gates (defined, not passed)

| Gate / risk | Acceptance condition | Verification / evidence | Blocking |
| --- | --- | --- | --- |
| GATE-RUNTIME / stale reads | Invalidation precedes refresh; fallback works | Runtime order/failure assertions | Yes |
| GATE-LEGACY / stale legacy rows | Startup migration repairs current rows | Task 3 migration check and startup result | Yes |
