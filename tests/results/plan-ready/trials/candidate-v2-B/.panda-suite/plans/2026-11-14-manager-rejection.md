# Manager rejection implementation plan

## Goal and scope

Add manager rejection to the existing in-memory approval service, with a required non-empty reason and terminal approved/rejected states. Preserve existing approval behavior and dictionary caller payloads. Implement only service behavior and its unit tests; this document does not authorize implementation.

Source: `requirements.md`; current implementation: `service.py`; existing assertions: `test_service.py`. No HTTP server, database, persistence, or network interface exists. Do not introduce routes, storage technology, retention policy, self-approval rules, deployment work, or new infrastructure. Existing same-ID manager approval remains allowed; rejection must not introduce an actor/request ownership restriction.

Requirements used below:

- R1: Managers can reject a pending request.
- R2: Rejection requires a non-empty reason.
- R3: Approved and rejected requests are terminal.
- R4: Preserve approval behavior and caller payloads.
- R5: Keep the change within this service and avoid unsupported policy/infrastructure decisions.

## Current behavior and affected files

`service.py:approve(request, actor)` checks `actor["role"]` first, raising `PermissionError("manager required")` for non-managers; it then requires `request["status"] == "pending"`, raising `ValueError("request must be pending")` otherwise. It returns a shallow dictionary copy with `status="approved"` and `reviewer_id=actor["id"]`. `label(request)` formats the ID and status.

`test_service.py` currently asserts only the approved status for a manager and a `PermissionError` for a member. It does not assert reviewer identity, payload preservation, input immutability, terminal-state handling, error text, or rejection behavior.

Affected files:

| File | Responsibility |
| --- | --- |
| `service.py` | Add the rejection operation; preserve `approve` and `label` contracts. |
| `test_service.py` | Add rejection and compatibility assertions using existing `unittest` tooling. |

## Proposed contract choices

These are concrete implementation choices within the requested scope, not established interfaces:

- Add `reject(request, actor, reason=None) -> dict`, alongside the unchanged `approve(request, actor)`. Both inputs remain dictionaries with the existing keys and value conventions; do not wrap or migrate caller payloads.
- Validate in this order: manager role, pending status, reason. Reuse exactly `PermissionError("manager required")` and `ValueError("request must be pending")` for the first two failures.
- A valid reason is a `str` with `reason.strip()` non-empty. Omitted reason, `None`, `""`, whitespace-only strings, and non-string values raise `ValueError("rejection reason required")` at the function boundary. The default `None` makes omission reach the intended validation rather than Python's missing-argument `TypeError`. Valid text is stored unchanged; whitespace stripping is only a validation check.
- Return `{**request, "status": "rejected", "reviewer_id": actor["id"], "rejection_reason": reason}`. Thus unrelated fields and nested values are preserved with existing shallow-copy semantics; decision-owned output keys take the specified new values. Do not mutate either input dictionary.
- Both operations reject every non-`pending` status, including `approved` and `rejected`. No repeated-decision success or silent transition is introduced.
- Leave malformed/missing existing actor/request keys under their existing dictionary access behavior; broader schema validation is excluded. No concurrency, transaction, audit-log, or persistence guarantee is introduced. Returned dictionaries remain the caller's responsibility, as today.

## Ordered work

- [ ] **T1 — Add rejection and prove decision compatibility**

  **Outcome:** A manager can return a rejected request with its reason; terminal requests cannot be decided again. Existing callers keep the same approval API and payload shape.

  **Requirements:** R1–R5. **Prerequisites:** none. **Files:** `service.py`, `test_service.py`.

  **Consumes:** Established `approve(request, actor)` dictionary contract and `label(request)`; request keys `id` and `status`, actor keys `id` and `role`. **Produces:** Proposed `reject(request, actor, reason=None) -> dict` with the exact output keys, validation precedence, and exceptions specified above. No dependent tasks or new subsystem interfaces.

  **Acceptance and discriminating verification** — Add unit tests in `test_service.py`, using fixtures with manager `{id: 2, role: "manager"}`, member `{id: 3, role: "member"}`, and pending request `{id: 1, status: "pending", custom: {keep: True}}` (Python dictionaries with quoted keys). Each check below must assert the stated outputs, rather than only that the call succeeds.

  | Check | Acceptance / expected evidence | Incorrect implementation rejected |
  | --- | --- | --- |
  | C1 (R1, R2) | Reject pending as manager with `"  insufficient details  "`; assert the full returned dictionary has unchanged `id`/`custom`, rejected status, reviewer ID 2, and the exact original reason in `rejection_reason`. | Wrong reviewer, missing reason, normalization that changes submitted text, or dropped payload fields. |
  | C2 (R1) | Reject pending as member with a valid reason; assert `PermissionError` and exact `manager required` message. Also use member + terminal request + missing reason and expect the same permission error. | Unauthorized rejection or changed authorization precedence. |
  | C3 (R2) | For pending manager requests, test omission, explicit `None`, empty string, spaces/tabs/newlines, integer 0, integer 1, boolean, list, and dictionary; each must raise `ValueError` with exact `rejection reason required` text. Valid single-character string succeeds. | Truthiness-only checks, accepting whitespace/non-string values, or accidental `AttributeError`/`TypeError`. |
  | C4 (R3) | For each operation and each input status `approved`, `rejected`, and an unknown status, assert `ValueError("request must be pending")`; rejection uses a valid reason. Also test terminal manager rejection with an invalid reason and expect the status error. | Allowing one terminal transition, treating only one terminal status as blocked, or changed validation precedence. |
  | C5 (R4) | Approve pending as manager; assert full returned dictionary, including reviewer ID and unrelated payload fields. Reject pending similarly. Snapshot both inputs and assert equality after success and after each failure path. Assert each successful result is a different dictionary from the request and retains the original nested `custom` object. | Mutating inputs, replacing shallow-copy semantics, or returning only decision fields. |
  | C6 (R4, R5) | Preserve existing member-approval regression with exact permission message, including member + terminal status. For both operations, a manager whose ID matches the request ID can decide a pending request. Assert `label` outputs `"1: approved"` and `"1: rejected"` on returned decisions. Review diff for unchanged `approve` signature and absence of infrastructure or ownership restrictions. | Approval compatibility regression, invented self-approval policy, or breaking existing label consumers. |

  **Verification command:** `python3 -B -m unittest -v test_service` from the fixture root. This command is confirmed runnable here; implementation must run it after adding the assertions. Expected evidence: all existing and new unit tests pass, with assertions covering C1–C6; inspect the final diff for R5. Failure tests must also cover input immutability as specified by C5. No external dependency is needed.

  **Risk and mitigation:** The current suite is too weak to prove compatibility; C4–C6 explicitly protect it. Added `reject` key/signature choices are proposed in this plan and must stay consistent between implementation and tests. In-memory copies cannot enforce durable terminal state across independently retained caller dictionaries; that limitation remains unchanged and persistence is outside scope.

## Readiness and evidence

**EXECUTION-READY.** T1 is the first unblocked task; no unresolved scope or contract decision prevents implementation under the proposed choices above. Every requirement maps to T1 and checks C1–C6. There are no task dependency cycles.

Planning evidence: `python3 -B -m unittest -v test_service` passed the two existing tests on 2026-11-14. This proves only the baseline; the new acceptance checks remain planned and T1 stays unchecked until their results exist. No release/deployment/migration boundary is requested, so no release gates are defined.

The fixture is not inside a Git repository (`git rev-parse --show-toplevel` failed with “not a git repository”). The skill's Git-only `.gitignore` and `git check-ignore` steps therefore do not apply here; no index or ignore rules were changed.

Implementation handoff, if separately authorized: use panda-execute to implement this saved plan. No execution is requested in this task.
