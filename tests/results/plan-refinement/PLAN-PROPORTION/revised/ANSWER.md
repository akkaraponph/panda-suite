**Plan: manager rejection**

**Goal:** Add a `reject` function so a manager can reject a pending request with a reason. Existing approval behavior stays the same.

**Scope:** `service.py` and `test_service.py` only. HTTP routes, storage, retention and self-approval rules are out of scope, as `requirements.md` says. The fixture has no persistence or network interface.

**Current behavior** (from `service.py`):
- `approve(request, actor)` raises `PermissionError("manager required")` if the role is not `"manager"`.
- It raises `ValueError("request must be pending")` if the status is not `"pending"`.
- Otherwise it returns `{**request, "status": "approved", "reviewer_id": actor["id"]}`.
- `label(request)` formats the id and status.
- `test_service.py` covers the manager-approves and member-blocked cases. Running `python3 -m unittest` passes 2 tests.

**Decisions (my assumptions, change before execution if wrong):**
1. **Checks run in the same order as `approve`:** role first, then status, then reason. A non-manager therefore gets `PermissionError` even if the reason is also bad.
2. **Reason rule:** a missing reason (`None`), a non-string, an empty string or whitespace only all raise `ValueError("reason required")`. The requirement says "non-empty" but doesn't say whether whitespace counts. I treated it as blank.
3. **Output field name:** `"rejection_reason"`, stored as given without stripping. Nothing in the source fixes this name.
4. **"Terminal" needs no new code:** it comes from the existing `status == "pending"` check in both functions.

**Review focus (inputs that no current test covers):**
1. Rejecting an already approved request → `ValueError`.
2. Approving an already rejected request → `ValueError`.
3. A whitespace-only reason → `ValueError`.
4. A member calling with a valid reason → `PermissionError`.
5. The caller's input dict is not modified, since `approve` returns a copy.

---

**Task 1: Add `reject` to `service.py`** (no prerequisites)

- [ ] Write the tests first, in a new `RejectionTest` class in `test_service.py`:
  - `test_manager_can_reject_pending_with_reason`: `reject({"id": 1, "status": "pending"}, {"id": 2, "role": "manager"}, "duplicate")` returns `status == "rejected"`, `reviewer_id == 2`, `rejection_reason == "duplicate"` and `id == 1`.
  - `test_member_cannot_reject`: a member with reason `"x"` → `PermissionError`.
  - `test_reason_required`: each of `None`, `""` and `"   "` → `ValueError` (one `subTest` per value).
  - `test_cannot_reject_non_pending`: status `"approved"` and status `"rejected"` → `ValueError`.
  - `test_cannot_approve_rejected`: `approve` on status `"rejected"` → `ValueError`.
  - `test_reject_does_not_mutate_input`: the input dict is unchanged after the call.
- [ ] Implement `reject(request, actor, reason)` in `service.py`:
  - Reuse the same `PermissionError` and pending-status `ValueError` messages as `approve`.
  - Then raise `ValueError("reason required")` unless `isinstance(reason, str) and reason.strip()`.
  - Return `{**request, "status": "rejected", "reviewer_id": actor["id"], "rejection_reason": reason}`.
- [ ] Leave `approve` and `label` unchanged. `label` already prints `"1: rejected"`.
- **Accept when:** only managers can reject pending requests, any blank reason is refused, both final states block further decisions, and the payload `approve` returns is unchanged.
- **Verify:** `python3 -m unittest -v`. Success means the existing 2 tests plus the new tests all report `OK`.

**Requirement → check**
- Manager-only → `test_member_cannot_reject`
- Non-empty reason → `test_reason_required`
- Approved/rejected are final → `test_cannot_reject_non_pending` and `test_cannot_approve_rejected`
- Approval behavior and payloads preserved → the existing 2 tests, plus `approve` itself is not edited

**Still open (not decided here):** HTTP route, storage, retention and self-approval rules, because the requirements give no basis for them. There's also no audit or timestamp field, since nothing asks for one.

As you asked, the plan is only in this message: I didn't save it under `.panda-suite/plans/` or change `.gitignore`. Nothing has been implemented. To build it, ask: "Use panda-execute to implement the manager rejection plan above."

---

## ACTIONS

**Files read:**
- `<workspace-root>/PLAN-PROPORTION-new/TASK.txt`
- `<repo>/skills/panda-plan/SKILL.md` (named by TASK.txt; I also listed its folder, which contains only SKILL.md, so there were no references to load)
- `.../PLAN-PROPORTION-new/requirements.md`
- `.../PLAN-PROPORTION-new/service.py`
- `.../PLAN-PROPORTION-new/test_service.py`

**Commands run:**
1. `cat TASK.txt && find . -type f | head -100` in the task directory
2. `cat` on SKILL.md, `ls` of its skill folder, and `cat requirements.md service.py test_service.py`
3. `python3 -m unittest -v 2>&1 | tail -5` in the task directory (result: 2 tests, OK)

**Files created or changed:** None.
