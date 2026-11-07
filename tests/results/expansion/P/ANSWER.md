# Release handoff — BLOCKED

Scope is the complete before.py to after.py replacement, evaluated against context.md. No version, commit SHA, production environment, runtime configuration, operational owner or author-supplied test evidence is available. No deployment, publication, tag or announcement occurred.

This is a behavioral authorization change, not just formatting. before.py:2-3 rejects callers whose actor_id differs from owner_id. after.py removes that check and keeps actor_id unused. context.md:5-6 requires owner-only cancellation and explicitly says there is no separate authorization layer. Any caller can now cancel another user's unshipped order. This is a mandatory blocking defect, irrespective of missing production evidence.

## Draft release notes and known issue

Adds a cancellation docstring. Also removes the owner permission check, allowing unauthorized cancellation; the candidate must not ship in this state. Shipped-order cancellation remains denied, but unauthorized shipped callers now see ValueError rather than the former PermissionError. There are no other changes in the supplied complete boundary. No migration, new dependency or configuration change is evidenced.

## Verification evidence

Read full before.py, after.py and context.md. Ran a local Python runpy probe against the exact supplied files, with actor 10 as owner and actor 20 as non-owner, for pending and shipped statuses. Results:

| Scenario | before.py | after.py | Requirement |
|---|---|---|---|
| Owner, pending | cancelled | cancelled | Satisfies |
| Owner, shipped | ValueError already shipped | Same | Preserved |
| Non-owner, pending | PermissionError owner required | cancelled | FAIL: owner-only cancellation |
| Non-owner, shipped | PermissionError owner required | ValueError already shipped | Permission ordering changed |

This executed behavioral probe is current local evidence only, not a production or project test-suite pass. Test evidence supplied by author: unavailable. Production configuration, integration tests, CI and operational readiness: Not Run / unknown. No project tooling or deployment command is supplied, so none is invented.

## Gates and ordered deployment checklist (proposed, not executed)

1. BLOCKING: restore owner authorization semantics in a separately authorized fix and review the complete resulting diff. Owner-only cancellation must hold without relying on an absent external authorization layer.
2. BLOCKING: on the exact final revision, pass regression tests for owner/non-owner and shipped/unshipped combinations, preserved denial ordering, unchanged input/preserved output fields, plus the relevant project suite when provided. Today's failing candidate probe cannot transfer to a corrected revision.
3. BLOCKING for deployment: identify exact release revision/version, target environment, verified project commands, operational owner and deployment authority; obtain relevant CI/review evidence and check configuration and runtime dependencies. Missing names are not sign-offs.
4. Confirm whether cancellation causes durable effects elsewhere in the target system and how unauthorized effects would be detected and repaired. No such external effects can be proven from these pure functions alone.
5. Once gates pass and deployment is explicitly authorized, record the prior artifact/configuration, validate recovery compatibility, deploy using verified project tooling, and run post-deployment checks below. No migration is indicated by the supplied source; check target release contents rather than assume a database operation.

## Recovery and post-deployment verification

Retain the prior known artifact and configuration. An application rollback to the prior implementation reinstates the owner check; actual feasibility and deployment commands remain unverified. If unauthorized cancellations have already affected persisted or downstream state, application rollback alone will not undo them: assess affected records/events and obtain a targeted recovery plan. Do not promise data restoration from the code diff.

Post-deployment checks in an approved test context must confirm an owner can cancel an unshipped order, a non-owner cannot, shipped orders stay uncancelled, and denied operations cause no state change. Observe authorization failures and unexpected cancellations with available target monitoring. Stop rollout and initiate recovery upon any unauthorized cancellation, changed denial semantics outside the approved contract, or failed cancellation safety check. Exact monitoring and acceptable operational thresholds require target evidence.

Readiness is BLOCKED due to the reproduced owner-only requirement failure. Missing production and broader test evidence are additional unresolved deployment gates; they do not downgrade the known blocker to UNKNOWN or conditionally ready. Preparation is complete; shipping remains unauthorized and blocked.
