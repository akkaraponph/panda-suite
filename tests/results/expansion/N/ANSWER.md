# Requirements Analysis

Business goal: allow multiple approvals of one request; the customer's reason for requiring multiple decisions and the success measure remain unspecified. Actors evidenced today are managers and members; the request owner is not represented in supplied payloads. Source establishes current behavior, not approval of new policy.

Scope: refine approval/rejection and their interaction. No code, data model, HTTP route, storage, retention, or self-approval policy is selected. There is no persistence or network interface (requirements.md:7).

## Evidence and conflict

service.py:4-9 permits a manager to approve a pending request, immediately returns status `approved` and a single `reviewer_id`, and preserves other request fields. Non-managers receive PermissionError and non-pending requests ValueError. service.py:12-13 displays the status as text. Two baseline tests pass, covering manager approval and member denial only.

requirements.md:3-6 requires manager rejection with a non-empty reason, terminal approved/rejected states, and preservation of approval behavior and caller payloads. These are requested requirements, not implemented rejection behavior. Immediate approval by one manager conflicts with a multi-approval completion rule if more than one decision is necessary. A single reviewer_id also cannot unambiguously represent several reviewers. Stakeholder resolution is required; do not quietly replace the existing contract.

## Identified requirements and acceptance

| ID | Status/source | Actor and expected result | Acceptance |
|---|---|---|---|
| FR-01 | Confirmed customer goal; detailed rules open | Support multiple approval decisions on one request | Once ordering, quorum and distinctness rules are approved, exercise at least two eligible decisions and verify each is accounted for and completion occurs exactly under the approved rule. This is a conditional acceptance template, not an executable final policy. |
| FR-02 | Confirmed requirements.md:3-4 | Manager can reject with non-empty reason | Given an eligible request and manager, rejection with a valid reason produces terminal rejected status; empty reason fails without changing the request. Exact eligible states and whitespace-only meaning remain open. |
| FR-03 | Confirmed requirements.md:4 | Approved and rejected requests are terminal | Given either terminal status, subsequent approval or rejection is denied and leaves prior decisions unchanged. This also prevents editing a terminal request into a nonterminal state unless stakeholders explicitly revise the requirement. |
| FR-04 | Confirmed requirements.md:5; compatibility conflict | Preserve caller payloads and existing approval behavior | Existing id/status/other caller fields remain readable and existing callers' expected approval result remains valid, unless a specifically approved compatibility change supersedes it. One-manager completion cannot be signed off alongside a higher quorum until the conflict is resolved. |
| FR-05 | Current behavior service.py:5-8; preservation requested | Approval requires manager role and pending status | Member approval raises PermissionError; non-pending approval raises ValueError; the original request is unchanged. Any multi-stage exception requires approval. |

Manager-only rejection implies non-manager rejection must be denied. Specific rejection error types and function interface are undecided. Do not infer permission for request creators or administrators not evidenced here.

## Decisions needed before complete planning/acceptance

- Ordering: must decisions follow named stages, or may eligible approvers act in any order? This changes allowed transitions and early/late decision tests.
- Quorum: how many approvals, from which eligible people/roles, with distinct-person or stage constraints; what if too few eligible people exist? This defines terminal completion and duplicate/concurrent behavior.
- Self-approval: may the requester approve, and where is requester identity obtained? This controls permission and payload compatibility. Current code lacks owner identity; absence of a check is not policy approval.
- Edits: which edits are allowed before completion, and do they invalidate all/some/no earlier decisions? This changes decision validity, resubmission and stale-action tests.
- Rejection interaction: can any eligible manager reject immediately, does a rejection stop all approvals, and is a reason of spaces valid? Terminal rejection is required, but eligibility and precedence need decisions.
- Compatibility conflict: does multiple approvals mean mandatory additional approvals, optional recorded approvals, or a separately opted-in flow? Which existing response fields and reviewer_id meaning must remain? Resolve before designing the interface.
- Repeats/concurrency: should duplicate decisions be rejected or treated as the same decision; how should approval versus rejection arriving together resolve? Do not count one actor twice or silently declare a winner without policy.

Relevant quality proposals (not approved): auditable attribution to request revision and decision maker; atomic accounting so concurrent actions cannot accidentally satisfy a quorum; consistent denial without partial changes. Retention, latency and availability targets have no evidence and are not specified.

Additional acceptance matrix after decisions: authorized/unauthorized/self actors, first/intermediate/final decision, out-of-order action, duplicate, simultaneous decisions, rejection reason absent/empty/whitespace, decision on either terminal state, edits before/after decisions and stale approvals. Missing keys/invalid role/status types also need a validation contract rather than accidental KeyError behavior.

A useful refinement draft is complete, but policy-dependent implementation planning and final acceptance remain blocked by the named business decisions. Decision owner is not supplied; route these questions to the customer/stakeholder with approval authority. No policy was selected and no implementation was authorized.
