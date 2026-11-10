# Compatibility boundaries

Use only the boundaries touched by the proposed refactor. Record behavior,
evidence, affected consumer and discriminating check; unknowns remain explicit.

| Boundary | Preserve and verify where applicable |
| --- | --- |
| Public APIs and imports | Names, call signatures, defaults, return shape, documented exports and consumers beyond the edited declaration |
| Errors and authorization | Exception type/message, validation precedence, permission guard timing; denied operations have no protected side effects |
| Collections and state | Order, duplicates, input mutation, aliasing, copy semantics and failed-operation state |
| Storage and transactions | Transaction owner, commit/rollback, atomicity and connection lifetime; extraction must not accidentally move commit ownership |
| Events and integrations | Payload compatibility, publish timing, ordering, retry/idempotency and dependency failures |
| Concurrency | Ownership, locking, cancellation and race assumptions; sequential unit tests do not establish race safety |
| Dynamic consumers | Reflection, plugins, monkeypatching and serialized/import names supported by evidence |

For a helper claimed to be unused, search declarations, imports, callers, exports
and relevant configuration. A supplied consumer outweighs a confident premise.
Unknown external consumers limit confidence; use a compatibility-preserving shape
where feasible instead of assuming their absence.

When source, tests and requirements conflict, reproduce the smallest discrepancy
where tools allow. Record which behavior predates the refactor. Do not interpret
a green suite as the requirement, or an old implementation as automatically correct.
A request to preserve behavior does not silently authorize fixing a known defect.
Separate the structural work from that decision and explain any blocked step.

For example, a label normalizer may promise to preserve duplicates while its
existing implementation deduplicates. A characterization test can document the
observed defect for investigation, but must not redefine deduplication as the
intended contract. Correcting it changes behavior. Conversely, if the original
preserves duplicates, “simplifying” it through a set is a regression even when
ordinary unique-input tests stay green.

Capture stable observable behavior before extraction when meaningful coverage is
missing. Pair differential comparisons with requirement-derived checks: comparing
two wrong implementations can establish equality without correctness. Test failure
paths as well as success when moving side effects or transaction boundaries.
