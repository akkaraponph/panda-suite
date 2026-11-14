# Manager rejection implementation plan

## Goal, scope, sources and constraints

Add manager rejection to the existing in-memory service while preserving approval and caller payloads. Sources: `requirements.md`, `service.py`, and `test_service.py`. No implementation or test execution is authorized by this plan.

Requirements: **R1** managers can reject pending requests; **R2** rejection requires a non-empty reason; **R3** approved and rejected requests are terminal; **R4** preserve approval behavior and caller payloads; **R5** introduce no HTTP routes, storage technology, retention policy, or self-approval policy. No persistence or network interface exists.

Established behavior: `approve(request, actor)` checks manager role before pending status, raises `PermissionError("manager required")` or `ValueError("request must be pending")`, and returns a shallow copy with `status="approved"` and `reviewer_id=actor["id"]`. `label(request)` displays ID and status. The current tests check successful approval status and member denial only; they do not prove payload preservation, terminal behavior, error messages, or immutability.

Proposed local contract choices, rather than existing guarantees:

- Add `reject(request, actor, reason=None)` alongside `approve`; leave `approve` and `label` signatures intact. Do not introduce a shared decision dispatcher or require callers to reshape payloads.
- Check role, then pending status, then reason, preserving existing authorization/state error semantics. Rejection uses the same role and status messages as approval.
- Treat a reason as a string of length greater than zero. Omitted, `None`, empty string, and non-string values raise `ValueError("rejection reason required")`. Whitespace-only strings are non-empty and accepted literally; trimming or a non-blank policy is not in the requirement. Store the exact string, without normalization.
- Return `{**request, "status": "rejected", "reviewer_id": actor["id"], "rejection_reason": reason}`. `rejection_reason` is a proposed new output key; it records the required reason in the only existing representation. Preserve other keys and do not mutate either input. Existing keys overwritten by the decision are `status`, `reviewer_id`, and, for rejection, `rejection_reason`.
- Keep the existing mapping-based input convention and malformed mapping behavior; adding general schema validation is outside scope. Add no self-review restriction: a manager whose ID matches a requester field is treated like any manager.

## File map

- `service.py`: add the rejection function and a concise explanation of its reason contract. Keep approval and label behavior.
- `test_service.py`: extend the existing standard-library `unittest` suite to cover rejection and preserved approval behavior.

## Ordered work

- [ ] **T1 — Add rejection with preserved approval compatibility.** Requirements R1–R5. Prerequisites: none. Consumes existing `request`/`actor` mappings, `approve(request, actor)` and the contract above; produces proposed `reject(request, actor, reason=None)` returning a new request dictionary or the specified exception. Keep all changes in the two mapped files.

  Acceptance and verification (all planned, not yet run):

  | Check | Observable acceptance condition and test inputs | Incorrect implementation rejected |
  | --- | --- | --- |
  | V1 | Manager + pending + `"duplicate"` returns exact expected mapping: rejected status, manager reviewer ID, exact `rejection_reason`, and preserved ID/custom fields. Assert full mapping equality and unchanged input mappings. | Drops caller fields, mutates the original, or forgets to record the reason. |
  | V2 | Manager + pending rejects omission, `None`, `""`, `False`, `0`, `[]`, and `{}` with `ValueError` and exact reason message. Accept `" "` and `" reason "` and assert exact stored strings. Use separate omitted-argument call and explicit-value subtests. | Uses truthiness alone, accepts non-string values, trims strings, or lets omitted arguments become accidental Python `TypeError`. |
  | V3 | Member + pending + valid/invalid reason raises `PermissionError("manager required")`. Member + terminal status also raises that error. | Validates reason/state before authorization or allows non-manager rejection. |
  | V4 | For each terminal status `approved` and `rejected`, both `approve` and `reject` by a manager raise `ValueError("request must be pending")`; rejection with an invalid reason still reports the state error. Assert the original mappings remain unchanged. Retain the existing non-pending status guard. | Allows re-approval, terminal reversal, repeated rejection, or changes validation order. |
  | V5 | Existing approval tests remain green. Add full-output equality for approval with custom payload fields; assert reviewer replacement, original request/actor unchanged, unchanged `approve(request, actor)` calling convention, and exact role/state exception messages. An unrelated existing `rejection_reason` key remains preserved by approval. | Rewrites approval around a new required argument, drops fields, changes exceptions, or sanitizes existing payloads. |
  | V6 | `label` returns `"1: approved"` and `"1: rejected"` for corresponding mappings. Manager/requester matching IDs can approve or reject pending mappings under the same guards. Inspect the diff for service/tests-only behavior and absence of infrastructure or policy additions. | Breaks the label helper or introduces an unsupported self-review rule/infrastructure. |

  Run `python3 -m unittest -v test_service` from the fixture directory after implementation. This is a proposed invocation of the standard-library test runner, derived from the existing `unittest` module, not a repository-provided script; Python availability has not been checked. Required evidence is verbose test output with all V1–V6 assertions passing against the implemented revision, plus a source diff review for R5. Exceptions should be checked with type and message, rather than only broad raises assertions. No database, network, or third-party fixtures are required.

## Review focus and traceability

Review omission versus explicit null versus empty versus invalid types (V2); authorization precedence when multiple inputs are invalid (V3); both terminal statuses across both operations (V4); full payload preservation and non-mutation (V1/V5); and literal whitespace behavior (V2). All belong to T1.

| Requirement | Task | Checks | Expected evidence |
| --- | --- | --- | --- |
| R1 | T1 | V1, V3 | Exact rejected output and manager-only error assertions |
| R2 | T1 | V2 | Separate omitted/null/empty/type/whitespace assertions |
| R3 | T1 | V4 | Both terminal statuses rejected by both decisions |
| R4 | T1 | V1, V5, V6 | Existing and expanded tests plus unchanged public signatures |
| R5 | T1 | V6 | Source diff review; no infrastructure or self-review policy |

## Compatibility gate and recovery

**G1 — defined; evidence pending.** Blocking compatibility gate: all V1–V6 assertions and the R5 diff review must pass against the actual implemented revision in a local Python environment before accepting this change. Existing green tests alone are insufficient. No deployment environment or release revision was supplied. With no persistence or external effects, code rollback is feasible; an in-memory rejected mapping already returned to a caller is not automatically reverted by a code rollback. No migration, retention, or telemetry work is justified here.

## Readiness and handoff

**EXECUTION-READY** under the explicit proposed contracts above. First unblocked task: T1. No prerequisite cycles or unresolved implementation blockers. Evidence gaps: implementation, Python availability, all planned checks, and the compatibility gate remain unverified. This plan does not assert release readiness.

The workspace is not a Git repository (`git rev-parse --show-toplevel` failed with exit 128), so no repository ignore rule applies. This plan is saved to the explicitly requested `ANSWER.md` destination.

Implementation handoff, without starting implementation: use panda-execute to implement T1 from `ANSWER.md` after review. Native execution is sufficient for this single localized task with one new function and no inter-task contracts. The current request authorizes planning only.
