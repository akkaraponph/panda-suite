# Implementation plan

Add manager rejection to the existing in-memory service. Preserve `approve(request, actor)`, its return shape, its errors, and existing dictionary payloads. Planning only; no implementation is authorized by this artifact.

## Current evidence

- `requirements.md`: managers may reject; a non-empty reason is required; approved/rejected requests are terminal. No HTTP, storage, retention, or self-approval policy is requested.
- `service.py:4–9`: `approve` checks manager permission before pending status, raises `PermissionError` / `ValueError`, and returns a copied dictionary containing the existing fields plus approved status and reviewer ID. Its pending-only check already prevents approving a rejected request.
- `service.py:12–13`: `label` displays any status without special cases; it can already display rejected requests.
- `test_service.py:6–14`: two approval tests cover manager success and member denial. Baseline `python3 -m unittest -v` passed both tests. Terminal states, payload preservation, and labels currently lack coverage.

## Proposed contract and assumptions

Add `reject(request, actor, reason)` without changing existing callers. Use a required explicit argument so existing request/actor dictionaries need no new input fields. Return `{**request, "status": "rejected", "reviewer_id": actor["id"], "rejection_reason": reason}`. This field name and function signature are design proposals, not existing contracts.

Validate manager role first, pending status second, and reason last. Match approval's existing permission/status errors. Require a string whose `strip()` is non-empty; raise `ValueError("rejection reason required")` for `None`, non-string, empty, or whitespace-only values. Preserve an accepted reason verbatim. Omitting the required argument produces Python's ordinary `TypeError`; the reason-validation promise applies to supplied values. These choices make “non-empty” mean meaningful text without silently rewriting the reason.

Do not add a self-review restriction: the fixture supplies no requester identity or existing policy. Preserve its exact-role check and treatment of all non-pending statuses. No shared abstraction, new module, persistence, network endpoint, migration, or deployment mechanism is needed.

## Ordered work

### 1. Lock existing approval and payload compatibility

**Objective/files:** Extend `test_service.py` against the existing behavior in `service.py`; leave the approval implementation unchanged. **Prerequisites:** none.

**Acceptance criteria:** Existing approval tests remain intact. Assert the complete approval result, including reviewer ID and arbitrary caller fields, and assert request/actor inputs are unchanged. Managers cannot approve either approved or rejected requests, receiving the existing pending-status `ValueError`. Non-managers receive `PermissionError`, including when status is terminal, preserving validation order. Pending requests remain approvable with the original two arguments and no reason field.

**Verification:** Run `python3 -m unittest -v` before adding rejection. The expanded compatibility tests must pass against the current implementation. This separates existing behavior from new rejection assertions.

### 2. Add rejection and focused behavior coverage

**Objective/files:** Add `reject` beside `approve` in `service.py`; import and test it in `test_service.py`. **Prerequisites:** task 1; use the explicit proposed contract above.

**Acceptance criteria:** A manager can reject a pending request with a meaningful reason; the complete result contains rejected status, manager reviewer ID, and the supplied reason. Other existing fields survive, unrelated caller fields need no schema changes, and neither input dictionary is mutated. Non-managers cannot reject. `None`, non-string, empty, and whitespace-only supplied reasons raise the specified `ValueError`; accepted surrounding whitespace is preserved. Both permission and status checks occur before reason validation, matching the stated precedence. Terminal requests cannot be rejected, including repeat rejection and rejection after approval. Invalid attempts leave inputs unchanged. Existing `approve` signature and output remain unchanged.

**Verification:** Add focused rejection tests using the existing `unittest` style, with table-driven `subTest` cases where useful for reasons, roles, and statuses. Check exception types and promised messages, full successful output, and input immutability. Run `python3 -m unittest -v`; new tests should fail before the new function exists and pass after implementation, alongside task 1's regressions.

### 3. Verify decision transitions and the existing display caller

**Objective/files:** Add integration-level function tests in `test_service.py` using `approve`, `reject`, and `label`. No `label` implementation change is expected. **Prerequisites:** task 2.

**Acceptance criteria:** Feed an actual approval result and an actual rejection result into both decision functions. All four subsequent decision attempts fail with the pending-status `ValueError` for a manager; use a valid reason when calling `reject` so the test detects the state guard. Labels remain `"<id>: pending"`, `"<id>: approved"`, and `"<id>: rejected"`. The original pending dictionary still has its original status after either decision, consistent with the existing copy-returning interface.

**Verification:** Run `python3 -m unittest -v` for the full fixture suite. Review the final diff to confirm only the rejection function and relevant tests were introduced, existing function signatures/payload contracts remain compatible, and no infrastructure or policy choices were added. This is a future execution check; no diff or implementation is claimed here.

## Coverage, risks, and boundaries

| Requirement | Tasks/checks |
| --- | --- |
| Manager rejection | 2: success and permission tests |
| Required non-empty reason | 2: invalid-type/empty/whitespace and valid-reason tests |
| Approved/rejected terminal states | 1–3: direct status checks and actual returned-result transition matrix |
| Preserve approval and caller payloads | 1–3: exact result, unchanged inputs, original arguments, display caller |
| Avoid unsupported interface/storage/policy decisions | Scope and final diff review in 3 |

The main compatibility risk is changing approval while extracting common logic; avoid refactoring it for this small addition and retain explicit regression tests. Reason validation and error precedence are specified above to avoid ambiguous tests. Only supplied fixture callers are known; the new reason field is additive and existing callers remain valid.

Terminality is enforced on the request value passed to these pure functions. An old pending dictionary can still be reused because the service returns copies and has no persistence or authoritative store; do not claim durable or concurrent transition enforcement. Adding that would require a separately scoped design. No unresolved decision blocks this bounded plan. Rollback, if needed after later implementation, removes the additive rejection function and its new tests; there is no stored data migration. Existing exceptions are sufficient observability for this fixture.

This plan is one fresh-context evaluation sample; it is not evidence of general reliability.
