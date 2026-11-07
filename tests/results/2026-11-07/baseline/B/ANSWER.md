The current service is a pair of pure functions; add rejection at that boundary. Keep `approve(request, actor)` and `label(request)` compatible. The existing two approval tests pass locally (`python3 -B -m unittest -v`). No implementation was made.

1. Add `reject(request, actor, reason)` in `service.py`.
   - Require `actor["role"] == "manager"`, using the existing `PermissionError("manager required")` behavior.
   - Require `request["status"] == "pending"`, using the existing `ValueError("request must be pending")` behavior. Preserve the authorization-before-state validation order.
   - Require a string reason containing at least one non-whitespace character; raise `ValueError` for an invalid reason. Use `strip()` for validation, and preserve the caller's supplied text in the returned rejection result.
   - Return a new mapping preserving the request's other fields, with `status="rejected"`, `reviewer_id=actor["id"]`, and the supplied text under `rejection_reason` (a proposed additive result field). Do not change approval payloads or mutate either input.
   - Acceptance: a manager can reject a pending request with a valid reason; members cannot; empty, whitespace-only, or non-string reasons fail; inputs remain unchanged and unrelated request fields survive.
   - Verification: add focused unit tests for each condition, including the complete returned mapping, the unchanged input mappings, and authorization/state validation precedence.

2. Cover the complete terminal-state transition matrix while preserving approval behavior.
   - Keep the existing approval guard requiring pending status. Apply the same guard to rejection; no separate state engine is needed.
   - Acceptance: managers can approve or reject pending requests. Neither operation can act on approved or rejected requests. Approval still returns the same fields and leaves existing caller data intact. `label()` renders a rejected request using its existing generic formatting.
   - Verification: retain the two existing tests; add approval/rejection tests for both terminal states, non-manager tests for both operations, an approval payload/input regression assertion, and a rejected-label assertion. Run `python3 -B -m unittest -v` and require all tests to pass.

3. Document the local rejection call and its errors.
   - Acceptance: a short usage example shows a pending request, manager actor, non-empty reason, rejected result, and terminal-state behavior. Existing approval calls remain valid. The proposed `rejection_reason` field is described explicitly.
   - Verification: execute the documented example and check its output against the unit-tested result contract; record the command and result.

HTTP routes, persistence, retention, and self-approval rules remain outside this change because the fixture supplies no evidence for them. No network or persistence verification is claimed.
