**Plan: manager rejection (chat only, nothing saved)**

Goal: add a manager-only `reject` decision to `service.py`. Rejection needs a non-empty reason, and both approved and rejected requests become final. Approval behavior and caller payloads stay exactly as they are.

What exists today:
- In `service.py`, `approve(request, actor)` checks the actor's role first and raises `PermissionError` if they aren't a manager. It then raises `ValueError` if the status isn't `pending`. Otherwise it returns `{**request, "status": "approved", "reviewer_id": actor["id"]}`.
- Because `approve` only accepts `pending` requests, a rejected request can't be approved once `reject` exists. That gives us the "final state" rule for free.
- `label(request)` formats any status and needs no change.
- `test_service.py` has 2 unittest tests. `python3 -m unittest -v` passes: 2 tests, OK.

Out of scope, as `requirements.md` says: HTTP routes, storage, retention periods and self-approval rules. There is no persistence or network layer to change.

**Task 1: Add `reject(request, actor, reason)` in `service.py`**
- [ ] Check in the same order and with the same exceptions as `approve`:
  1. Role is not `manager` → `PermissionError`
  2. Status is not `pending` → `ValueError`
  3. Reason is invalid → `ValueError`
- [ ] Return `{**request, "status": "rejected", "reviewer_id": actor["id"], "rejection_reason": reason}`. The field name `rejection_reason` is my proposal; see decisions below.
- [ ] Leave `approve` and `label` unchanged.
- Done when: only managers can reject, only `pending` requests can be rejected, a blank reason fails, and the input dict is not modified.

**Task 2: Add tests in `test_service.py`** (needs Task 1)
- [ ] A manager rejects a pending request: status is `rejected`, and `reviewer_id` and the reason are set.
- [ ] A member trying to reject → `PermissionError`.
- [ ] Rejecting a request that is already `approved` or `rejected` → `ValueError`.
- [ ] An approved or rejected request can't be rejected or approved again. In particular, `approve` on a rejected request → `ValueError`.
- [ ] The reason is checked case by case:
  - `""` → `ValueError`
  - whitespace only → `ValueError` (assumption, see below)
  - `None` → `ValueError`
  - leaving the argument out → `TypeError`, because `reason` is a required positional argument
- [ ] A member with a blank reason → `PermissionError`. This pins down the check order.
- [ ] `label` shows `1: rejected`.
- Verify: `python3 -m unittest -v`. The 2 existing tests plus the new ones should all pass.

**Decisions to confirm (recorded as assumptions):**
1. **Whitespace-only reason:** I treat it as blank and reject it. The requirement only says "non-empty".
2. **Output field name:** `rejection_reason` is proposed. Nothing in the repo sets a name, and callers may depend on it.
3. **Non-string reason** (for example `123`): the plan rejects it with `ValueError`. Accepting it is the alternative.
4. **Error type for a bad reason:** `ValueError`, to match how `approve` reports a wrong status.

**Risks:**
- A shared helper for the role and status checks could quietly change how `approve` behaves. The existing tests plus the new "approve after reject" test would catch that.

Every requirement maps to a task: manager-only and reason rules go to Task 1, final states to Tasks 1 and 2 (relying on the existing `approve` check), and preserving approval behavior to the unchanged `approve` plus the existing tests.

When you're ready, you can say: "Use panda-execute to implement the manager rejection plan above." This plan doesn't authorize the code changes by itself.

---

**ACTIONS**

Files read:
- `<workspace-root>/PLAN-PROPORTION-old/TASK.txt`
- `<workspace-root>/old-skill/panda-plan/SKILL.md` (the only file in that skill folder, so no references were loaded)
- `<workspace-root>/PLAN-PROPORTION-old/requirements.md`
- `<workspace-root>/PLAN-PROPORTION-old/service.py`
- `<workspace-root>/PLAN-PROPORTION-old/test_service.py`

Commands run:
- `cat TASK.txt && find . -type f` (in the project directory)
- `cat` of `old-skill/panda-plan/SKILL.md`, `ls -R old-skill/panda-plan`, `cat requirements.md service.py test_service.py`
- `python3 -m unittest -v` (2 tests, OK) and `git status` (not a git repository)
- `find . -name '__pycache__' -o -name '*.pyc'` (refused by the rtk wrapper; nothing ran)
- `ls -a` and `/bin/ls -a` on the project directory, confirming the test run left no `__pycache__`

Files created or changed: none. As requested, the plan was given only in chat and no `.panda-suite` file was saved.
