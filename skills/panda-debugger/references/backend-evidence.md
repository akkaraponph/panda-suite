# Backend evidence and confidence

Use this guide when a backend defect involves an API, database, queue, transaction, external service, or concurrent worker.

Adapt the boundary checks to the actual system. An entry point may be an HTTP request, RPC call, command, scheduled job, event, or embedded function; storage may not be a SQL database. Use the logs, traces, state tools, and test harness that the project actually provides.

## Follow one failing operation

1. Identify the request, job, or event ID and the input that triggered the failure. Correlate logs, traces, and database or queue observations for that operation when access is available.
2. Trace entry point → validation → service logic → state change or dependency → failure. Note where errors are handled and where the symptom becomes visible.
3. Inspect the relevant boundary: transaction begin and commit or rollback, affected rows, retries and acknowledgements, external side effects, locks or idempotency, and configuration differences. Check only boundaries that matter to this failure.
4. Name competing explanations and choose a safe check that separates them. A focused test, controlled reproduction, or observed trace can establish the causal chain. A matching stack trace or repeated symptom by itself cannot.

Do not inspect or change production records without authorization. When runtime access is missing, use source and supplied logs to narrow the cause, then state the smallest additional observation needed.

## Confidence labels

- **CONFIRMED:** The evidence shows how this mechanism produced the reported failure. Give the input, key state transition, and result, or cite a focused experiment that rules out the main alternative.
- **LIKELY:** The code and observations fit this mechanism, but an important causal step or competing explanation remains untested. Name that missing check.
- **UNKNOWN:** The available evidence cannot rank the explanations reliably. List the next useful observation without guessing.

The status of a symptom and the status of a cause can differ: a failure can be reproduced while its cause remains **LIKELY**. Separate the primary cause from factors that made the failure more likely or more damaging.
