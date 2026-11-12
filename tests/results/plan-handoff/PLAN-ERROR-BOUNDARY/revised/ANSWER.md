# Plan: `reject(request, actor, reason)` in `service.py`

**Goal:** add a manager-only rejection to the approval service. The existing `approve` behavior and payloads stay the same.

**Source:** `requirements.md`, `service.py` (`approve`, `label`) and `test_service.py`, which has 2 tests. I ran `python3 -m unittest -v` before planning and both tests pass.

**Constraints from the requirements:**
- Only managers can reject.
- Only `pending` requests can be rejected. `approved` and `rejected` are final.
- A reason is required, and it can't be empty.
- Callers must keep getting the same payloads they get today.
- Don't add HTTP, storage, retention or self-approval rules. This fixture has none of them.

## The signature problem

With `def reject(request, actor, reason)`, a caller who leaves out `reason` gets a **`TypeError`** from Python before your code runs. That breaks the rule that a missing reason must raise `ValueError`. So the reason needs a private sentinel default:

```python
_MISSING = object()
def reject(request, actor, reason=_MISSING): ...
```

This keeps the three cases apart, each with its own `ValueError` message:

| Call | Detected by | Raises |
|---|---|---|
| reason left out | `reason is _MISSING` | `ValueError("reason required")` |
| `reason=None` | `reason is None` | `ValueError("reason must not be None")` |
| `""` or whitespace only | `isinstance(reason, str) and not reason.strip()` | `ValueError("reason must not be blank")` |

The tests should check each message (`assertRaisesRegex`), so that one case can't silently cover for another.

## Files

- `service.py`: add `_MISSING` and `reject`. Leave `approve` and `label` unchanged.
- `test_service.py`: add a `RejectionTest` class. Leave the current tests alone.

## Task 1: Add `reject` and its tests (no prerequisites)

- [ ] **Tests first**, in a new `RejectionTest`:
  - `test_manager_can_reject_pending`: the result has `status == "rejected"`, `reviewer_id == 2`, and every other input key unchanged.
  - `test_member_cannot_reject`: raises `PermissionError`.
  - `test_cannot_reject_approved` and `test_cannot_reject_rejected`: each raises `ValueError` matching "pending".
  - `test_omitted_reason`, `test_none_reason`, `test_empty_reason` (`""`) and `test_whitespace_reason` (`"   "`): each raises `ValueError` with its own message from the table.
  - `test_reject_does_not_mutate_input`: the original dict still has `status == "pending"`.
- [ ] **Code**, in `service.py`: `reject(request, actor, reason=_MISSING)`.
  - Check in the same order as `approve`: role (`PermissionError("manager required")`), then status (`ValueError("request must be pending")`), then reason.
  - Return `{**request, "status": "rejected", "reviewer_id": actor["id"], <reason key>: reason}`.
- [ ] **Verify:** run `python3 -m unittest -v`. All new tests pass, and the two existing approval tests pass unchanged.

**Done when:** only managers can reject, only `pending` requests can be rejected, the three reason cases each raise their own `ValueError`, and `approve` and `label` behave as before.

## Things to test that the requirements imply

1. **Error order.** A member rejecting with a blank reason: the plan raises `PermissionError`, since the role is checked first. Add a test for this.
2. **Whitespace-only reason.** I'm treating it as blank, which is an assumption (see the decisions below).
3. **Final states.** Rejecting a request that is already `rejected` raises `ValueError`. The current tests don't check this for `approve` either.

## Decisions for the API owner

1. **Reason key name** in the returned payload. Nothing in the source sets it. I'd propose `"rejection_reason"`.
2. **Whitespace-only text.** Is `"   "` blank? The plan says yes. Also, should the saved reason be stripped, or kept exactly as sent?
3. **Non-string reasons** such as `5` or `[]`. The requirements don't say. Options are `TypeError` or `ValueError`. Until you decide, leave this untested rather than letting it pick up whatever Python happens to do.
4. **Error order** when there are several faults (role, then status, then reason) copies `approve`. Please confirm.

You asked for a plan in chat with no implementation, so I haven't saved a plan file. Once the decisions above are settled, panda-execute can carry out Task 1.

---

## ACTIONS
- **Files read:**
  - `TASK.txt`
  - `requirements.md`
  - `service.py`
  - `test_service.py`
  - `<repo>/skills/panda-plan/SKILL.md`
- **Commands run** (in the task directory):
  - `cat` on the files above, plus `find . -type f` to list them.
  - `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v`: 2 tests ran, OK.
  - `git status`: the directory is not a git repository.
- **Files created or changed:** none.
