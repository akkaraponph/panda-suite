# Chat-only trial answers (retained excerpts)

These are exact answer excerpts retained by the parent from tool-delivered final
responses, not raw transcripts. Full answers were returned in the host session;
the agents correctly created no task files. They were not rerun to create records.

## PLAN-PROPORTION / original

> - [ ] **Add and verify rejection as one deliverable.** In `service.py`, introduce `reject(request, actor, reason)`; no prerequisites. Mirror approval’s permission and pending-status checks, then require a string whose stripped value is nonempty, raising `ValueError("reason required")` otherwise. Return a copied request with `status="rejected"`, `reviewer_id=actor["id"]`, and `reason` preserved as supplied. Proposed interface decisions: reason is a separate required argument; a missing argument produces Python’s `TypeError`; explicit `None`, non-string, empty, and whitespace-only values produce the stated `ValueError`. In `test_service.py`, verify manager success, member denial, each invalid-reason case, extra-field preservation, and unchanged inputs.
> - [ ] **Verify terminal states and compatibility.** Depends on `reject(request, actor, reason)`. Extend `test_service.py` to assert that both `approve` and `reject` reject requests already `"approved"` or `"rejected"` with `ValueError("request must be pending")`. Retain existing approval tests; additionally verify approval’s copied payload, reviewer ID, and unchanged input, plus `label` displaying `"rejected"`.

Agent reported loading TASK.txt, original instruction snapshot, requirements,
service and tests, then running `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v`
(two tests passed). Source/config remained unchanged by final-state comparison.

## PLAN-PROPORTION / candidate v1

> - [ ] **T1 — Add and verify rejection** (no prerequisites).
>   - Update `service.py` with proposed `reject(request, actor, reason=None)`. Follow approval’s validation order: non-managers raise `PermissionError("manager required")`; non-pending requests raise `ValueError("request must be pending")`.
>   - Proposed reason contract: omission, `None`, non-string, empty, or whitespace-only values raise `ValueError("rejection reason required")`. Preserve valid reason text.
>   - Return a new dictionary preserving request fields, setting `status="rejected"`, `reviewer_id=actor["id"]`, and proposed `rejection_reason=reason`. Leave inputs and `approve` unchanged.
>   - Extend `test_service.py`: assert the full rejection result, preservation of unrelated payload fields, and unchanged inputs; reject unauthorized actors and every invalid reason above. Check both approval and rejection refuse both terminal statuses (`approved`, `rejected`), and authorization takes precedence over other validation errors. Strengthen approval coverage to assert its full existing output and payload preservation.
>   - Verify with `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest test_service`. These assertions catch ignored reasons, payload loss, accidental mutation, terminal-state reopening, and approval regressions.
>
> **EXECUTION-READY:** T1 is the first unblocked task. Existing baseline: 2 tests pass. New behavior remains unimplemented and its checks remain planned. Handoff to panda-execute would preserve these contracts; this request authorizes planning only.

Agent reported loading TASK.txt, candidate instruction snapshot, requirements,
service and tests; running the quoted command (two passed); no file changes.

## PLAN-ERROR-BOUNDARY / candidate v1

> The default lets omitted arguments reach validation; a mandatory `reason` parameter would instead cause Python to raise `TypeError`.

Proposed code in the actual answer:

```python
_MISSING = object()

def reject(request, actor, reason=_MISSING):
    ...
```

> | Input | Expected |
> |---|---|
> | Omitted reason (`_MISSING`) | `ValueError`: reason missing |
> | Explicit `None` | `ValueError`: reason null |
> | `""` or whitespace-only text | `ValueError`: reason blank |
> | Other nonstring value | Proposed: `ValueError`: reason must be text |
> | Nonblank string | Return rejection result |

> Add unit tests asserting each error separately, successful result fields and payload preservation, unchanged input, member denial, and refusal of both approved and rejected requests. Run the existing approval tests too. Planned verification: `python -m unittest -v`; checks have not been executed.

Agent reported only cat/rg reads of TASK, candidate instructions and fixture files;
no files written or tests run. Parent notes the `python` executable availability
was not verified; the error/signature contract passes, command confirmation is partial.

## PLAN-EVIDENCE-BOUNDARY / candidate v1

> The claim “the green suite proves it is release-ready” remains **unverified**. The existing test checks only `schema_version` and one guardrail status. It does not assert strict exit codes, policy evaluation, CLI output, transport failures or compatibility. No tests were run here.

> **C1:** directly test the helper with multiple proven guardrails, mixed proven/unproven guardrails, all unproven guardrails and an empty list, in both modes. Expected strict outcomes are respectively `True`, `False`, `False`, `False`; every permissive outcome is `True`. These assertions reject first-item-only checks and the vacuous truth of `all([])`.

> All gates are **defined; evidence pending**. The candidate revision is currently unspecified.

> **Plan readiness: PARTIALLY READY.** T1 is the first task that can start in an authorized implementation session. Local checks and live release evidence remain unexecuted; the live gate requires credentials and the release environment. Release readiness has not been established. This chat-only plan can be handed to `panda-execute` if implementation is subsequently requested.

Actual answer included T1 policy, T2 recovery/CLI, T3 future release collection;
G1 strict, G2 failures, G3 compatibility, G4 live and G5 evidence freshness.
These task/gate names are a parent summary, not quoted answer text. The live-task
separation issue recurred here; it was addressed in candidate v2.
Agent reported only cat/rg reads, no tests or file changes. No original paired
arm for this case was run.

## PLAN-NONTRIGGER / Lead

> When a SKU already exists, `Inventory.add_item` raises `KeyError("duplicate sku: <sku>")` and leaves the existing item unchanged.

Agent reported only TASK.txt, Lead and inventory.py loaded; cat/rg reads succeeded;
no Plan instruction load, writes or plan creation. Parent compared original fixture
files and found no changes.
