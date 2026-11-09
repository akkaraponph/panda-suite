---
name: panda-review
description: Review a pull request, diff, or bounded code change for material correctness, security, reliability, data integrity, compatibility, and regression risks with precise evidence.
---

# Panda Review

Find actionable defects introduced or exposed by a change. Complexity advice
without a changed-code defect is a different task. Review does not authorize fixes. A dedicated vulnerability, secret, or dependency
audit belongs with the security audit workflow; ordinary diff review still checks
security defects within the change.

## Inputs and workflow

Use a diff or explicit old/new baseline, intended behavior, repository context,
and relevant tests. If the comparison point is missing, inspect available Git
state and ask only if the review range remains ambiguous. State the reviewed
range; do not imply a whole-system audit from a small diff.

1. **Understand intent.** Read requirements and repository guidance. Inspect the
   diff and affected callers, contracts, state transitions, and tests.
2. **Trace behavior.** Check validation, authentication/authorization, errors,
   transactions, concurrency, data integrity, API compatibility, and operational
   behavior where relevant. Inspect performance only against a concrete workload
   or mechanism; speculation is a risk to verify, not a measured failure.
   Derive expected behavior from the contract before relying on existing tests.
   For changed behavior, check whether assertions distinguish a plausible defect
   from the required result; passing tests alone do not establish correctness.
3. **Validate candidates.** Identify the triggering inputs or conditions. Trace
   through the real code and existing guards; run a focused safe reproduction
   when useful. Reject findings already prevented by the implementation or based
   solely on preference. Mark missing runtime evidence accurately.
4. **Report by impact.** Prioritize material defects over style. Use precise file
   and line locations in the changed code plus supporting callers when needed.
   Separate confirmed issues from risks requiring a further check.

## Findings and completion

Each material finding includes:

- **Severity:** critical, high, medium, or low, with the practical impact. Critical
  means immediate severe compromise/data loss; high affects core correctness or
  security; medium affects a bounded path; low is a limited-impact defect.
- **Location and issue:** file/line and the faulty behavior.
- **Trigger and evidence:** affected input/state and the causal code path or
  actual reproduction, including existing mitigations considered.
- **Impact and correction:** the consequence and smallest appropriate repair.

For example, removal of an owner check allows a non-owner to cancel an unshipped
order when no caller guard exists. Cite the changed function and that caller
contract rather than simply saying “missing security.”

If no significant issues are supported, say so concisely and identify verification
limits. Do not invent findings to fill a report. Report checks actually run and
remaining uncertainty. Keep application files unchanged unless fixes are explicitly
requested. External or destructive verification needs appropriate authorization.
This workflow is independently usable; a handoff need only carry the reviewed
baseline, evidence, unresolved risks, proposed corrections, and permission status.

## Success discipline

Identify the requested outcome and evidence of completion. Continue useful authorized work, keep attention on current evidence, and compare the result with the outcome before reporting completion. State any remaining uncertainty or blocker. Upekkhā: Under pressure to approve, inspect the relevant guards and report supported findings.
