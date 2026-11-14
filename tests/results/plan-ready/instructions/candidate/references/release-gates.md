# Release gate planning

Derive gates from requirements and concrete risks at the requested release,
deployment, migration or compatibility boundary. Reuse task verification IDs;
keep a small change's gate inline rather than expanding a generic checklist.

For each applicable gate record:

| Gate / requirement or risk | Required condition | Verification / expected evidence | Blocking | Revision / environment |
| --- | --- | --- | --- | --- |
| Stable ID and source | Observable pass/fail outcome | Check ID or method and future evidence | Yes/No with reason | Known constraints or explicit unknown |

Select only relevant risks: functional acceptance; public API/CLI/config/report
compatibility; security/permissions; data integrity, migrations and mixed versions;
timeouts, cancellation, recovery, concurrency or idempotency; required telemetry;
usage or operator documentation. Explain rollback/recovery limits for irreversible
changes. Include responsible roles only when actually identified. Requirements
supply targets; missing policy, environments, performance budgets or sign-offs
remain decisions or evidence gaps.

Mark gates **defined; evidence pending** at planning time. For unavailable checks,
name the future method, expected artifact and environment/revision needed; label
mock-backed evidence by its actual boundary. A green suite or zero exit status
proves only its assertions, not every acceptance condition. Never report release
READY from a plan. Release assessment must inspect the actual release revision,
evidence freshness and unresolved blockers; no release tool invocation is required
to write these gates.

When scope changes, reconcile gate sources, conditions, checks and traceability
with the remaining tasks; remove gates for excluded requirements.
