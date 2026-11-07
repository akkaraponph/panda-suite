# Impact assessment: proposed string-to-integer status

The current in-process contract uses `pending` and `approved` strings. requirements.md also requires terminal `rejected`, manager rejection with a non-empty reason, and preservation of existing approval behavior and caller payloads. Proposed integer values, unknown-value behavior, exposure boundary, motivation and rollout scope are unspecified. An internal integer representation with a string boundary adapter and an integer caller contract are different proposals; the latter conflicts with explicit payload preservation and needs a requirement decision.

## Confirmed dependencies and impacts

| Evidence | Confirmed relationship and consequence | Check/mitigation |
|---|---|---|
| service.py:7-8 | Approval compares directly to `pending`; any integer input currently raises ValueError. Probe with 0 demonstrates this, without assuming 0 is the intended code. | Define exhaustive mapping and input normalization; preserve pending eligibility and terminal denial. |
| service.py:9 | Producer returns string `approved` and preserves request fields; changing it to an integer changes caller output. | Preserve string boundary or obtain approval for a breaking contract and coordinate callers. |
| service.py:12-13 | label formats status directly; an integer renders as numeric text (`1: 0` in probe) rather than semantic status. | Map code to stable display text and test all defined statuses. |
| test_service.py:8-10 | Input fixture and assertion depend on strings. A wholesale integer contract invalidates this expectation. | Retain compatibility test and add intended internal/boundary cases, rather than merely rewriting away the existing guarantee. |
| test_service.py:12-14 | Member denial is tested before status validation; auth behavior must remain unchanged. | Verify unauthorized actor handling with all supported status encodings. |
| requirements.md:3-6 | Rejection and terminal approved/rejected rules must work with the mapping; preserving caller payloads constrains exposure. Rejection is not implemented today. | Include rejected in contract decisions and tests without pretending it already exists in code. |

Baseline: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v` passes 2 tests. This establishes current behavior only; it does not validate the proposed conversion. No source changes were made.

## Compatibility and boundary risks

Confirmed: simply replacing incoming status values with integers breaks the current pending comparison; emitting integers breaks the existing string assertion and payload guarantee; display meaning changes without translation. A full implementation has not been supplied, so failures in a future complete patch cannot be asserted beyond these demonstrated dependencies.

Possible risks, not confirmed consumers: external callers may compare strings, schemas may constrain enums, jobs/events/caches may carry old values, and dashboards may group textual statuses. Obtain contracts or representative payloads and consumer inventory to establish actual impact. No HTTP/event interface exists in this fixture; do not invent one.

Unknown: actual database records, database constraints, external consumers, deployed versions, migration volume, target environment and mixed-version compatibility. requirements.md:7 says this fixture has no persistence/network interface. That bounds inspected code; it does not prove the wider product has no stored data or consumers. No migration is currently evidenced or authorized.

If persistence exists elsewhere, inspect types, distinct values, nulls and invalid/historical values before conversion. Mapping must be explicit and lossless where rollback is expected. New codes unknown to old binaries can prevent application rollback; a reverse script alone does not establish recovery. If versions exchange statuses, test old/new producers and consumers in both directions before rollout.

## Recommended next action and required checks

Prefer keeping the caller-facing status strings and translating only at an explicitly needed internal boundary; first confirm the business reason for conversion. Avoid expanding scope to storage or routes without evidence. Decide integer mapping, whether bool is accepted (Python bool is an int subtype), unknown/null/missing/type validation, and whether callers ever receive integers.

Required verification before implementation acceptance: current compatibility tests; pending success; terminal approved/rejected denial; manager/member permissions; reason validation for the requested rejection feature; mapping round-trip for every supported state; invalid/unknown code rejection without partial changes; label outputs; payload field preservation; mixed encodings only if explicitly supported. Search other actual caller repositories and contracts once supplied. If persisted data exists, rehearse conversion and recovery on representative copies and verify mixed-version behavior. Release observability and rollback checks depend on the eventual operational boundary.

Coverage: inspected all supplied service.py, test_service.py and requirements.md; file inventory contains no additional application files. External repositories, production state and databases were not inspected. Assessment supports a compatibility decision, not approval to change code or migrate data.
