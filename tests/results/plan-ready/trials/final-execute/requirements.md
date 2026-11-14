# Synthetic campaign CLI v1.1

Use Python 3.9 standard library only. Plan; do not implement.

REQ-1: Existing config field requireAllGuardrailsProven defaults to false.
When true, success requires every guardrail to be proven. Unproven or empty
results must produce exit_code 2. When false, retain legacy exit_code 0.
REQ-2: Add a shared proposed interface in campaign.py:
evaluate_policy(report: dict, *, require_all_proven: bool) -> bool.
It consumes schema_version 1 reports. run_campaign and cli.main must use the
same policy outcome; callers must receive the existing report shape and CLI JSON.
Preserve schema_version, exit_code and guardrails with id/status fields.
REQ-3: Transport TimeoutError or InterruptedError returns an unproven safety
report. Strict mode returns 2; permissive mode returns 0. Call the transport
once, with no retry, network publication, new infrastructure or swallowed unrelated
exceptions. Do not mutate the input configuration.
REQ-4: Release v1.1 promises old configurations, CLI return values in permissive
mode, and schema_version 1 reports remain compatible. Define blocking gates.
A live provider check is required before release; credentials and the release
environment are unavailable here. Do not invent owners, latency targets or live
results. Local test doubles cannot establish live-provider compatibility.

The existing unittest command is: python3 -m unittest -v.
