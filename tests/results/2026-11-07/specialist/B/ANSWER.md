Plan only; no source or test changes made.

Evidence: `requirements.md` requires manager rejection, a reason, terminal decisions, and payload compatibility. `service.py:4` exposes `approve(request, actor)`, enforces manager/pending checks, and returns a copied payload with reviewer ID. `service.py:12` formats a label. `test_service.py` covers manager approval and member denial. Baseline: `python3 -m unittest -v` passes 2 tests.

1. Preserve and document approval compatibility in `test_service.py`.
   Prerequisite: existing service inspected.
   Accept when approval still returns all caller fields with `status="approved"` and `reviewer_id`, leaves request/actor inputs unchanged, and denies nonmanagers and nonpending statuses. Cover both approved and rejected states as terminal, with exact existing permission/status exception behavior.
   Verify: run `python3 -m unittest -v`; existing and added regression tests pass against the current approval implementation.
2. Add manager rejection in `service.py` and focused tests in `test_service.py`.
   Depends on task 1. Proposed interface: `reject(request, actor, reason)` returning the copied request with `status="rejected"`, `reviewer_id`, and `rejection_reason`. Keep the existing approval signature and payload contract. Proposed reason contract: a string containing at least one non-whitespace character; reject missing, empty, whitespace-only, and nonstring reasons with ValueError. Preserve the accepted reason text. These additions are design proposals rather than existing contracts.
   Accept when a manager can reject only a pending request with a valid reason; a nonmanager receives PermissionError; invalid reasons and nonpending requests receive ValueError; arbitrary caller fields survive and inputs remain unchanged. Follow approval's permission-before-status check order.
   Verify: `python3 -m unittest -v` with success, role, reason, status, payload, and immutability tests.
3. Verify all decision transitions and label compatibility.
   Depends on task 2. Accept when pending → approved and pending → rejected succeed for managers; approved/rejected → either decision fail; `label()` continues to format both statuses without special handling. Existing callers can still call approve with exactly two arguments.
   Verify: table-driven transition tests, label assertions, and full `python3 -m unittest -v` suite. Inspect the final diff for source/test scope and any approval signature or payload changes.

Requirement coverage: manager decision/reason → task 2; terminal decisions → tasks 1 and 3; existing behavior and payloads → tasks 1–3. The only new dependency is the additive rejection function; no storage, network, migrations, deployment, retention, or self-approval policy is needed. Risks are accidental payload mutation, weakening existing approval authorization, and ambiguous reason semantics; tests address the first two and the explicit proposal above makes the third reviewable. No duration estimate or execution authorization is implied.
