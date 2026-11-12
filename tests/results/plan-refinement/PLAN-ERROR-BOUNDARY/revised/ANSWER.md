## Plan: manager rejection in `service.py` (chat only, per your request; nothing saved)

**Goal:** Add `reject` next to `approve`. Only managers can reject, and only pending requests. A missing reason, `None`, and blank text must each raise `ValueError`.

**Evidence:**
- `service.py`: `approve` checks the role first and raises `PermissionError("manager required")`. It then checks the status and raises `ValueError("request must be pending")`. It returns `{**request, "status": "approved", "reviewer_id": actor["id"]}`.
- `test_service.py` has two `unittest` tests. `python3 -B -m unittest -v` passes both (2 OK).
- `requirements.md`: the reason must be non-empty, approved and rejected are final, and current approval behaviour and caller payloads must not change. HTTP, storage, retention and self-approval rules are out of scope.

**Signature decision (the main risk):** a plain `def reject(request, actor, reason)` cannot meet the contract. If the caller leaves `reason` out, Python raises `TypeError` before the function runs, not `ValueError`. Use a private sentinel instead:

```python
_MISSING = object()
def reject(request, actor, reason=_MISSING) -> dict
```

The three cases are then told apart inside the function, each with its own `ValueError` message:
- **Omitted** (`reason is _MISSING`): `ValueError("reason is required")`
- **`None`** (`reason is None`): `ValueError("reason must not be None")`
- **Blank** (a string where `reason.strip() == ""`, which covers `""` and `"   "`): `ValueError("reason must not be blank")`

**Review focus (cases that need their own tests):**
1. Leaving the reason out raises `ValueError`, not `TypeError`.
2. A whitespace-only reason is treated as blank (this is my assumption; see the decisions below).
3. Rejecting an approved or rejected request raises `ValueError`.
4. A member gets `PermissionError` even if their reason is valid.
5. `approve` behaves exactly as before.

### Task 1: Add `reject` to `service.py`
- [ ] Add `_MISSING` and `reject(request, actor, reason=_MISSING)` with checks in the same order as `approve`:
  1. Role check: `PermissionError("manager required")`.
  2. Status check: `ValueError("request must be pending")`.
  3. Reason checks: the three cases above.
- [ ] Return `{**request, "status": "rejected", "reviewer_id": actor["id"], "reason": reason}`. Keep the reason exactly as the caller sent it; do not strip it.
- [ ] Leave `approve` and `label` unchanged.
- **Interface it provides:** `reject(request: dict, actor: dict, reason: str = _MISSING) -> dict`. Task 2 uses it.
- **Accept when:** a manager rejecting a pending request with `"duplicate"` gets back `status == "rejected"`, `reviewer_id == 2` and `reason == "duplicate"`, and the input dict is not changed.

### Task 2: Tests in `test_service.py` (depends on Task 1)
- [ ] `test_manager_can_reject_pending_with_reason`: checks the return value from Task 1's acceptance line.
- [ ] `test_member_cannot_reject`: raises `PermissionError`.
- [ ] `test_reject_requires_pending`: run once with `"approved"` and once with `"rejected"` (via `subTest`); both raise `ValueError`.
- [ ] `test_reject_without_reason_raises_value_error`: calls `reject(req, mgr)` and asserts `ValueError`. Checking for `ValueError` also fails if Python raises `TypeError`.
- [ ] `test_reject_none_reason`, `test_reject_empty_reason` (`""`) and `test_reject_whitespace_reason` (`"   "`): each asserts `ValueError` and checks the message, so the three cases stay distinct.
- [ ] `test_approve_unchanged`: `approve` still returns the same payload and has no `reason` key.
- **Verify:** `python3 -B -m unittest -v` passes all tests: the 2 existing ones plus the new ones.

**Decisions still open (I made assumptions; please confirm):**
- Whitespace-only counts as blank. I assumed yes.
- Which error wins when a request breaks several rules: I assumed the same order as `approve` (role, then status, then reason).
- Non-string reasons such as `123`: not specified. I suggest `TypeError` or leaving them unchecked until the API owner decides.
- Whether adding a `reason` field to the rejected payload is acceptable to callers.
- Self-rejection rules, HTTP routes and storage are left out, as the requirements say.

---

## ACTIONS
- **Files read:**
  - `<workspace-root>/PLAN-ERROR-BOUNDARY-new/TASK.txt`
  - `<workspace-root>/PLAN-ERROR-BOUNDARY-new/requirements.md`
  - `<workspace-root>/PLAN-ERROR-BOUNDARY-new/service.py`
  - `<workspace-root>/PLAN-ERROR-BOUNDARY-new/test_service.py`
  - `<repo>/skills/panda-plan/SKILL.md` (named in TASK.txt)
- **Commands run:**
  - `cat` on the files above, plus `find . -type f`.
  - `ls -R` on the `skills/panda-plan` folder, which contains only `SKILL.md`.
  - `python3 -B -m unittest -v` in the workspace (2 tests OK; `-B` so no bytecode files were written).
  - `ls -a` to confirm no files were added.
- **Files created or changed:** none. The skill's default is to save the plan under `.panda-suite/plans/`, but the task asked for the plan in chat only, so nothing was saved and `.gitignore` was not touched.
