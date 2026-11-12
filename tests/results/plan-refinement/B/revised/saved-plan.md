# Plan: Manager rejection for approval requests

**Goal:** Let managers reject pending requests with a required reason, and make
approved and rejected requests terminal, without changing existing approval
behavior or caller payloads.

**Scope:** `service.py` and `test_service.py` only. Out of scope (per
`requirements.md`): HTTP routes, storage technology, retention periods,
self-approval rules, persistence, network interfaces.

**Source:** `requirements.md`, `service.py`, `test_service.py`.

**Constraints (copied from `requirements.md`):**
- "Add a rejection decision for managers."
- "Rejection requires a non-empty reason; approved/rejected requests are terminal."
- "Preserve existing approval behavior and caller payloads."
- "Do not pick HTTP routes, storage technology, retention periods, or self-approval rules without evidence."
- "No persistence or network interface exists in this fixture."

## Evidence anchors (current behavior)

- `service.py:4-9` `approve(request, actor)`:
  - `actor["role"] != "manager"` raises `PermissionError("manager required")` (checked first).
  - `request["status"] != "pending"` raises `ValueError("request must be pending")`.
  - Returns a new dict `{**request, "status": "approved", "reviewer_id": actor["id"]}`; the input dict is not mutated and extra keys pass through.
- `service.py:12-13` `label(request)` returns `f'{id}: {status}'`; works for any status string, so `"1: rejected"` needs no change.
- `test_service.py` covers only manager-approves-pending and member-cannot-approve. Nothing tests: approve on a non-pending request, payload pass-through, non-mutation.
- No database, HTTP layer, or persistence exists (`service.py:1` docstring), so "terminal" is enforced only by the pending-status check in each decision function.
- Test command verified in this workspace: `python3 -m unittest -v` -> `Ran 2 tests ... OK`. `pytest` is not installed; do not rely on it.

## Decisions and assumptions

| # | Decision | Basis |
|---|----------|-------|
| D1 | New function `reject(request, actor, reason)` in `service.py`, mirroring `approve`. | Existing pattern; no route/transport exists. |
| D2 | Check order: role -> status -> reason. A member rejecting with a blank reason gets `PermissionError`; a manager rejecting an approved request with a blank reason gets `ValueError("request must be pending")`. | Matches `approve` ordering. |
| D3 | Return `{**request, "status": "rejected", "reviewer_id": actor["id"], "rejection_reason": reason}`; `reason` stored unchanged (not stripped). | Mirrors `approve` payload shape. Field name `rejection_reason` is a proposal; confirm if a consumer expects another name. |
| D4 | "Non-empty" = a `str` with at least one non-whitespace character. `""`, `"   "`, `None`, and non-`str` values all raise `ValueError("reason required")`. Omitting the argument raises Python's own `TypeError` (required positional parameter); no extra handling. | Assumption: whitespace-only counts as empty. Recorded visibly; reverse if stakeholders disagree. |
| D5 | `approve` is not modified. It already refuses `"approved"` and `"rejected"` requests via its pending check. | "Preserve existing approval behavior." |
| D6 | Malformed inputs (missing `role`/`status`/`id` keys) keep raising `KeyError` as `approve` does today. | Preserve behavior; no requirement says otherwise. |

**Unresolved (not decided by this plan):** self-rejection/self-approval
(actor id equal to a requester id) is not checked, because the requirements
forbid choosing it without evidence and the request payload has no requester field.

## Review focus

Inputs and failure modes the requirements imply that no current test covers:

1. **Whitespace-only reason** (`"   "`): user expects rejection to fail with `ValueError`. Test in Task 2.
2. **Rejecting an already-approved request, and approving an already-rejected one**: user expects `ValueError("request must be pending")` both ways. Tests in Tasks 1 and 2.
3. **Caller payload preservation**: extra request keys (e.g. `"title"`) survive both decisions and the input dict is not mutated. Tests in Tasks 1 and 2.
4. **Non-manager rejection**: user expects `PermissionError` even when the reason is valid. Test in Task 2.
5. **`None` reason**: user expects `ValueError`, not `AttributeError` from calling `.strip()` on `None`. Test in Task 2.

## File map

| File | Responsibility | Change |
|------|----------------|--------|
| `service.py` | Decision functions | Add `reject`; `approve` and `label` unchanged. |
| `test_service.py` | unittest suite | Add approval regression tests (Task 1) and `RejectionTest` (Task 2). |

## Tasks

### Task 1: Lock in existing approval behavior

**Objective:** Add regression tests for `approve` behavior that Task 2 must not change.
**Files:** `test_service.py`. **Prerequisites:** none.
**Interfaces:** consumes `approve(request, actor)` as it exists; produces no new code.

- [ ] In `ApprovalTest`, add `test_approve_rejects_non_pending`: for each status `"approved"` and `"rejected"`, `approve({"id": 1, "status": status}, {"id": 2, "role": "manager"})` raises `ValueError`.
- [ ] Add `test_approve_preserves_payload_and_does_not_mutate`: input `{"id": 1, "status": "pending", "title": "Laptop"}`, manager `{"id": 2, "role": "manager"}`; result has `status == "approved"`, `reviewer_id == 2`, `title == "Laptop"`, and the input dict still has `status == "pending"` and no `reviewer_id` key.
- [ ] Run `python3 -m unittest -v`.

**Acceptance:** 4 tests pass against the unmodified `service.py`. If any fail, stop: current behavior differs from the evidence above and the plan must be revised.

### Task 2: Add manager rejection

**Objective:** Implement `reject` per D1-D4. **Files:** `service.py`, `test_service.py`.
**Prerequisites:** Task 1 green.
**Interfaces:** produces `reject(request: dict, actor: dict, reason: str) -> dict`; raises `PermissionError("manager required")`, `ValueError("request must be pending")`, `ValueError("reason required")`.

Tests first (new `RejectionTest` class, import `reject` alongside `approve`):

- [ ] `test_manager_can_reject_pending_with_reason`: `reject({"id": 1, "status": "pending"}, {"id": 2, "role": "manager"}, "Over budget")` returns `{"id": 1, "status": "rejected", "reviewer_id": 2, "rejection_reason": "Over budget"}`.
- [ ] `test_member_cannot_reject`: actor role `"member"`, reason `"Over budget"` -> `PermissionError`.
- [ ] `test_reject_requires_reason`: manager, pending request; each of `""`, `"   "`, `None` -> `ValueError` (use `subTest`).
- [ ] `test_reject_rejects_non_pending`: statuses `"approved"` and `"rejected"`, valid reason -> `ValueError`.
- [ ] `test_reject_preserves_payload_and_does_not_mutate`: same shape as Task 1's payload test; `title` kept, input unchanged.
- [ ] `test_label_shows_rejected`: `label(reject(...))` == `"1: rejected"` (import `label`).
- [ ] Run `python3 -m unittest -v`; expect the new tests to fail with `ImportError` for `reject` (red).

Implementation:

- [ ] In `service.py`, add `reject(request, actor, reason)` after `approve`: same role and status checks and messages as `approve`; then `if not isinstance(reason, str) or not reason.strip(): raise ValueError("reason required")`; return the dict from D3. Do not edit `approve` or `label`.
- [ ] Run `python3 -m unittest -v`.

**Acceptance:** only managers can reject; only pending requests can be rejected; `""`, whitespace-only, and `None` reasons are refused; result carries `status "rejected"`, `reviewer_id`, `rejection_reason`, and all caller keys; input not mutated; all 10 tests pass (4 from Task 1 + 6 new); a comparison with the original file (the workspace is not a Git repository) shows `approve` and `label` unchanged.

## Requirement-to-task map

| Requirement | Task | Check |
|-------------|------|-------|
| Managers can reject | 2 | `test_manager_can_reject_pending_with_reason`, `test_member_cannot_reject` |
| Non-empty reason required | 2 | `test_reject_requires_reason` |
| Approved/rejected are terminal | 1, 2 | `test_approve_rejects_non_pending`, `test_reject_rejects_non_pending` |
| Preserve approval behavior | 1 | existing 2 tests + Task 1 tests unchanged and green |
| Preserve caller payloads | 1, 2 | both `..._preserves_payload_and_does_not_mutate` tests |
| No routes/storage/retention/self-approval choices | all | none added; self-approval listed as unresolved |

## Risks

- **Whitespace interpretation (D4)** may differ from stakeholder intent; isolated in one condition and one subtest.
- **Reason field name (D3)** is new payload surface; consumers outside this fixture are unknown.
- **Terminal state is advisory only**: without persistence, a caller holding a stale `"pending"` copy can still decide it again. Out of scope here; needs a storage-level guard once persistence exists.

## Verification strategy

- Command: `python3 -m unittest -v` from the project root. Success: `OK` with 4 tests after Task 1 and 10 tests after Task 2.
- Baseline today: `Ran 2 tests ... OK`.
- Manual check: `approve` and `label` bodies in `service.py` are byte-identical to the current version.
