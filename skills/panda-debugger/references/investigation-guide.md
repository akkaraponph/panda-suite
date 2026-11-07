# Investigation guide

Use this guide when a bug spans several components or the visible exception may be downstream of the defect.

## Evidence ledger

For each material statement, identify its basis:

| Kind | Meaning | Example |
|---|---|---|
| Observation | Directly seen in supplied artifacts or a command's output | A stack trace names `service.go:42`; a test failed with a specific assertion. |
| Inference | Follows from observations and code, but was not directly observed | A missing commit likely explains unchanged balances. |
| Hypothesis | A possible cause still needing a discriminating check | A duplicate worker may be processing the same job. |
| Unknown | Evidence or access is missing | The production database isolation level is unavailable. |

Quote only the relevant log lines and cite repository paths with line numbers where possible. Do not treat example snippets, comments, or an expected test result as proof of runtime behavior.

## Phase gates

### Understand → Reproduce

State what should happen, what happened, affected conditions, and which evidence supports those statements. If expected behavior is unclear, infer it only when code, tests, or a specification establishes it; otherwise ask a targeted question.

### Reproduce → Trace

Record exact steps or commands and outcomes. If reproduction is unsafe, unavailable, or too costly, say so. A stack trace supplied by the user is evidence of a reported failure, not a reproduction performed by the agent.

### Trace → Root cause

Map input → entry point → transformations and dependencies → failure. Inspect callers and producers of bad values, error propagation, and state transitions. For a database operation, inspect the start, use, commit or rollback, and error checks of a transaction. For asynchronous work, inspect delivery, deduplication, acknowledgement, and shared-state boundaries. Focus on the relevant boundaries rather than exhaustively tracing unrelated code.

### Root cause → Fix

For each candidate, ask: Does it explain the observed behavior? What evidence contradicts it? What check would distinguish it from competing explanations? Mark the cause CONFIRMED, LIKELY, or UNKNOWN. A LIKELY cause supports a conditional recommendation; it does not support a claim that the defect was proven.

For an investigation-only request, finish the causal explanation and a file-level fix and test plan, then ask for approval before editing. Do not use an approval question in place of investigation. If the user explicitly requested implementation, proceed under that authorization.

### Fix → Verify

Connect the change to the causal mechanism. Check the original failure, normal behavior, and the important boundary cases. Use existing test conventions. Report each test as Passed, Failed, Not Run, or Blocked with its actual command or reason. A static review may support a proposal, but cannot establish a runtime fix.

## If investigation stalls

Provide the current causal trace, confidence level, and the smallest missing artifact or experiment that would resolve the uncertainty. Do not fill gaps with invented implementation details or a generic list of possible causes.
