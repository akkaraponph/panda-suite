# Campaign CLI v1.1 implementation plan

## Goal, scope and sources

Implement REQ-1–REQ-4 in `requirements.md`: opt-in strict guardrail policy shared by the API and CLI, safe reports for timeout/interruption, and explicit v1.1 compatibility gates. This artifact authorizes planning only; no source or test changes have been made.

Constraints: Python 3.9 standard library only; schema_version exactly `1`; exit_code exactly `0` for permissive policy, `0` for strict success, `2` for strict failure. Preserve the report object and CLI JSON fields `schema_version`, `exit_code`, and `guardrails`, with each guardrail's `id` and `status`. One transport evaluation per campaign, no retries, no network publication, no new infrastructure, no configuration mutation, and no swallowing unrelated exceptions. No owners or latency targets have been supplied.

Current evidence: `campaign.py:4` calls `transport.evaluate()` once and always returns exit_code 0 with one `safety` result. `cli.py:8` parses a JSON file, calls the campaign, prints JSON and returns the report code. `test_campaign.py` checks only schema version and unproven status, despite passing a strict config. It does not assert policy, exit codes, error handling, CLI output, or compatibility. The supplied command `python3 -m unittest -v` currently passes its one test under Python 3.14.7; this is baseline evidence only, and does not establish Python 3.9 or v1.1 correctness.

## Contracts and decisions

- Existing API remains `run_campaign(config: dict, transport) -> dict`; CLI remains `main(config_path: str, transport) -> int`. `transport.evaluate()` remains argument-free and returns `proven` or `unproven`.
- Proposed shared pure interface in `campaign.py`: `evaluate_policy(report: dict, *, require_all_proven: bool) -> bool`. The report is schema version 1. Return a policy success boolean, without modifying the report or consulting its existing exit_code. With `False`, return True even for an empty guardrail list. With `True`, return True only for a nonempty guardrail list whose every status equals `proven`; unproven, mixed or empty lists return False. Multiple guardrails must be supported even though the current transport produces one.
- Use the same explicit config interpretation in both callers: omission means False; literal True enables strictness; literal False retains permissive behavior. Proposed defensive interpretation for an explicit JSON null or other non-boolean value is permissive (`config.get("requireAllGuardrailsProven", False) is True`), without coercing strings such as `"false"` to True. This adds no config-validation feature. Non-dict configs remain outside this interface's contract.
- For schema-1 policy input, `guardrails: []` is the specified empty case. Proposed defensive handling treats omitted or null guardrails as no proof (strict False, permissive True); a guardrail lacking status or having null/unknown status cannot prove strict success. Arbitrary malformed report structures and other schema versions are outside the supported input contract; no new public error guarantee is proposed for them.
- `run_campaign` constructs the existing report shape, then sets `exit_code` from `evaluate_policy`. Catch only `TimeoutError` and `InterruptedError` around the single transport call; each produces exactly `[{"id": "safety", "status": "unproven"}]`. Let other exceptions propagate. Strictness never changes whether the transport is invoked.
- `cli.main` retains parsed config locally, calls `run_campaign`, and explicitly applies imported `evaluate_policy` with the same strictness interpretation to set the report's exit_code before printing/returning. This repeats only pure policy evaluation, never transport evaluation. It makes the required shared CLI boundary explicit and keeps returned integer and printed code identical. Preserve existing JSON parsing/file errors; introduce no alternative policy implementation.
- No persistence or schema migration. Existing printed report provides the needed observable policy result; add no telemetry or fields. A release rollback can restore the prior code since there are no data writes, but loses strict enforcement: consumers requiring strictness must pause campaigns or retain v1.1 until enforcement is restored. Permissive runs continue to preserve their existing success-code contract.

## Affected files

| File | Responsibility |
| --- | --- |
| `campaign.py` | Proposed pure policy; existing campaign orchestration and narrow transport recovery |
| `cli.py` | Existing config/JSON boundary; shared policy use and consistent return value |
| `test_campaign.py` | Extend existing unittest coverage with policy, API and CLI cases using stdlib doubles, tempfile and redirected stdout |
| `plan.md` | Execution and release evidence requirements; no separate documentation structure is assumed |

## Ordered work

- [ ] **T1 — Establish and test the shared policy (REQ-1, REQ-2).** No prerequisite. Produce the proposed `evaluate_policy(report: dict, *, require_all_proven: bool) -> bool` export in `campaign.py` and policy tests in `test_campaign.py`. Consume schema-1 reports with `guardrails: list[dict]` containing id/status, with the defensive cases above. Preserve input report equality before/after every evaluation. **C1 (unit):** table-test strict proven-only single/multiple lists => True; strict unproven, mixed in both orders and empty => False; permissive equivalents => True. Check missing/null guardrails and missing/null/unknown status follow the defined defensive behavior. Give reports deliberately conflicting existing exit_code values to prove the policy computes from guardrails, not cached code. These checks reject `all([])`, first-item-only checks, and trusting exit_code. Verification: supplied unittest command; capture test names, results and tested revision after implementation.

- [ ] **T2 — Apply policy and recover transport failures (REQ-1–REQ-3).** Depends on T1's exact pure interface and boolean outcomes. Modify `run_campaign(config: dict, transport) -> dict` in `campaign.py`; extend `test_campaign.py`. Consume caller config and one injected `evaluate()` result or exception; produce the unchanged schema-1 report with policy-derived exit_code. Implement the narrow catch and config interpretation defined above. **C2 (API unit):** cross omission/False/True with proven/unproven and both handled exceptions; expect one safety result, version 1, and codes 0 except strict unproven/recovered failure => 2. Compare complete report keys/values and deep-copied config before/after. Cover null and string flags to reject accidental truthiness. Count evaluate calls (exactly one) on success and each exception; a RuntimeError must propagate after one call. These cases reject hard-coded 0/2, retries, broad exception catches, and flag mutation. Preserve and extend the original regression test. Run the supplied unittest command and retain revision-linked results.

- [ ] **T3 — Integrate the CLI and prove compatibility locally (REQ-1–REQ-4).** Depends on T1's export and T2's final report contract. In `cli.py`, retain parsed config, import the shared function, apply the same flag interpretation and code mapping, then print once and return the same integer. Extend `test_campaign.py` using temporary JSON files, counting injected transports and `contextlib.redirect_stdout`; no provider access. **C3 (CLI integration):** parse stdout using json.loads and assert exact report shape plus equality of returned code and printed exit_code for omitted/False/True flags × proven/unproven/TimeoutError/InterruptedError. Include old config `{}` and a config with an unrelated preserved field; neither may require migration. Check null/string flags per the agreed interpretation. Assert transport is called once. Confirm unrelated transport exceptions propagate and produce no success JSON. Verify the CLI delegates to the shared policy through a stdlib mock wrapper, and integration outcomes match direct API outcomes; source review confirms no duplicate `all`/guardrail policy in CLI. Check the shared-policy wrapper is actually called with the report and expected keyword flag. This rejects a CLI that simply returns 0, changes JSON shape, or silently diverges from campaign policy. **C4 (runtime/compatibility):** run `python3 -m unittest -v`; additionally run the proposed `python3.9 -m unittest -v` on an available Python 3.9 runtime and review imports/syntax for standard-library-only Python 3.9 compatibility. Record exact revision, interpreter and outputs; absence of Python 3.9 leaves C4 evidence incomplete. No new runtime dependency or deployment setup is required by this task.

- [ ] **T4 — Collect release-boundary evidence (REQ-4).** Depends on T3's candidate revision and passing local checks. This is future release work, not an implementation prerequisite. **C5 (live integration):** in the actual release environment with real credentials, identify the existing provider adapter/configuration and run the candidate revision using supported provider inputs that exercise proven and unproven results. Use old/default config plus strict opt-in, checking real transport interoperability, schema-1 report fields, CLI JSON and 0/2 outcomes. Also execute the existing provider-specific compatibility procedure if one is defined there. Store a sanitized transcript/report identifying candidate revision, environment, provider/adapter version, configurations, observed statuses and outcomes, and method of exercising each status. Do not expose credentials. If either result cannot be obtained safely, record the gap and keep the gate blocked; local injected failures cannot replace this evidence. The concrete live invocation must be determined from that environment's adapter/tooling; none is supplied by this synthetic fixture. Do not invent a command or report a live pass. Reconcile evidence with the exact release candidate before assessing release readiness.

## Review focus and traceability

| Implied failure / expected behavior | Owning check |
| --- | --- |
| Empty strict report must fail despite Python's vacuous `all` result | T1 / C1 |
| Later unproven guardrail must fail even if the first is proven | T1 / C1 |
| Timeout and interruption both retain policy-dependent codes and one evaluation | T2 / C2 |
| Unrelated exception must propagate, with no success JSON | T2–T3 / C2–C3 |
| CLI and API agree; old configs/JSON stay compatible | T3 / C3–C4 |

| Requirement | Tasks | Checks | Expected evidence / current gap |
| --- | --- | --- | --- |
| REQ-1 default/permissive/strict, unproven and empty | T1–T3 | C1–C3 | Policy/API/CLI assertions; not yet implemented |
| REQ-2 shared interface and retained schema/JSON | T1–T3 | C1–C4 | Signature/delegation review, exact shape assertions, matching outcomes; pending |
| REQ-3 recovery, single call, no config mutation or swallowed exceptions | T2–T3 | C2–C3 | Counting doubles, input equality, propagation assertions and source review for narrow catch/no network additions; pending |
| REQ-4 compatibility and blocking live gate | T3–T4 | C3–C5 | Revision-linked Python 3.9/local results and real-provider artifact; live credentials/environment unavailable |

## Blocking v1.1 release gates

All gates below are **defined; evidence pending**. None is passed by this plan or the one-test baseline.

| Gate / source | Required condition | Verification / expected evidence | Blocking | Revision / environment |
| --- | --- | --- | --- | --- |
| G1 policy and failure behavior / REQ-1–REQ-3 | All C1–C3 assertions pass; exact interfaces and narrow catch conform | Unittest results plus source review including one-call/no-mutation/no-new-network constraints | Yes: incorrect enforcement or recovery changes caller outcomes | Actual v1.1 candidate revision; local doubles establish only local behavior |
| G2 compatibility / REQ-2, REQ-4 | Old config, permissive API/CLI values and schema-1 shapes preserved; stdlib Python 3.9 supported | C3–C4 revision-linked reports, interpreter version, import/syntax review | Yes: public and runtime promises | Candidate revision; Python 3.9 runtime still requires evidence |
| G3 real provider / REQ-4 | C5 demonstrates provider interoperability and promised report/CLI outcomes in release environment | Sanitized live-check artifact with revision, environment, provider version and observed results; missing scenarios explicitly block | Yes: required live compatibility cannot be proved by mocks | Release environment/credentials unavailable; adapter details and live invocation remain evidence prerequisites |

## Readiness and handoff

**EXECUTION-READY for authorized implementation planning scope.** T1 is the first unblocked task; T1 → T2 → T3 → T4 is acyclic and shares the interface above. No product decision blocks T1–T3. Python 3.9 execution and live release checks remain evidence gaps; T4 cannot execute here. Release readiness has not been assessed and release remains blocked until G1–G3 have evidence for the actual candidate.

All task checkboxes remain unchecked because implementation acceptance evidence does not yet exist. After review, a possible handoff is: “Use panda-execute (native) to implement `plan.md`, preserving its acceptance criteria and unavailable release gates.” Native execution suits the three small, sequential code tasks. This request is plan-only; do not start implementation or provider work without further authorization.
