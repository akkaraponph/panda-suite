# Specification structure

Use the sections that change an implementer's decisions. This is a menu, not a
requirement to fill unknown sections with plausible details.

1. **Context and scope:** audience, problem, requirements, non-goals, constraints.
2. **Current behavior:** component responsibilities and source anchors. Describe
   observed runtime evidence separately from static code analysis.
3. **Proposed design:** changed responsibilities and interfaces; rationale and
   rejected alternatives when the trade-off matters.
4. **Contracts:** input/output fields, types, validation, errors, permissions,
   compatibility, and versioning. State whether a contract exists or is proposed.
5. **Data and consistency:** keys/constraints, transactions, concurrency,
   idempotency, asynchronous ordering, and external failure recovery, if relevant.
6. **Operations:** supported capacity/reliability requirements, configuration,
   observability, rollout, migrations, recovery or rollback. Unmeasured values
   stay requirements or open decisions, not invented benchmarks.
7. **Verification:** acceptance criteria and tests, separating planned checks from
   checks already run and their results.
8. **Open decisions:** question, impact, evidence/owner needed, and whether it blocks
   implementation. Do not assign a person without supplied ownership evidence.

Example distinction for a pure in-memory approval function:

| Topic | Current / ปัจจุบัน | Proposed / ข้อเสนอ | Open / รอข้อสรุป |
| --- | --- | --- | --- |
| Decision | Manager approves pending request | Add manager rejection with non-empty reason | Self-approval policy absent |
| Storage | Returns a new mapping; no persistence code | No storage change required by this scope | Persistence design requires separate requirements |
| Interface | Python function call | Preserve current caller shape | HTTP route is not established |

For an ADR, compress to context, decision/status, evidence, alternatives, and
consequences. For an API spec, emphasize actual/proposed contracts and error
semantics. Keep speculative implementation choices out of the current-state text.
