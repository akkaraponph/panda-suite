# Synthetic campaign CLI v1.1 implementation plan

## Goal, scope and constraints

Implement REQ-1–REQ-4 in `requirements.md`: one shared success policy, preserved schema and permissive behavior, and narrowly handled transport interruptions. This document is planning only; source and tests remain unchanged.

Use Python 3.9 standard library only. `requireAllGuardrailsProven` defaults to false. Strict failure is `exit_code` 2; permissive mode retains 0. Preserve `schema_version` 1 and report fields `exit_code`, `guardrails`, and guardrail `id`/`status`. Call transport once, with no retry, network publication, new infrastructure or swallowed unrelated exceptions. Do not mutate input configuration. Credentials and the release environment are unavailable; a live provider check is required before release. No owners, latency targets or live results are assumed.

## Evidence and affected files

- `campaign.py:4–7`: `run_campaign(config: dict, transport) -> dict` currently calls `transport.evaluate()` once and always returns exit code 0 with one safety guardrail. Add shared policy and exception translation here.
- `cli.py:7–10`: `main(config_path: str, transport) -> int` loads JSON, prints the report, and returns its exit code. Integrate the shared policy here without changing its public signature or JSON shape.
- `test_campaign.py:10–14`: the single existing test asserts version and unproven status, but misses strict exit code. Extend with policy and campaign regressions.
- Proposed `test_cli.py`: standard-library CLI tests using temporary files and captured stdout.
- `requirements.md:5–21`: authoritative policy, transport and release contracts.

Observed baseline: `python3 -B -m unittest -v` passes one test. This does not establish the requested behavior. Python 3.9 execution and live-provider checks were not performed.

## Decisions and review focus

`evaluate_policy(report: dict, *, require_all_proven: bool) -> bool` is pure: true means successful policy outcome. It ignores the existing report exit code. For valid schema-version-1 reports, permissive mode returns true; strict mode returns true only for a nonempty guardrails list whose every status equals `"proven"`. Thus empty lists fail strict policy despite the usual empty-`all` result. Config reads use `config.get("requireAllGuardrailsProven", False)` without insertion or modification. The supported flag values are booleans; null, strings, numbers and malformed reports have no specified validation/error contract and are outside this change. Missing flag is supported and means false; missing/null guardrails are not the specified empty-list case.

Inputs most likely to escape the existing test, with their owning checks:

1. Empty guardrails: strict policy fails, permissive succeeds (Task 1).
2. Mixed proven/unproven guardrails: strict fails regardless of ordering (Task 1).
3. A missing flag in an old config: API and CLI still return 0 (Tasks 1 and 3).
4. Transport interruptions: safety becomes unproven, one call only, correct mode exit (Task 2).
5. Unrelated exceptions and config mutation: exceptions propagate and input remains unchanged (Task 2).

## Ordered tasks

- [ ] **Task 1 — Implement and test shared policy in the campaign API.**
  Objective: enforce REQ-1 and the API portion of REQ-2. Files: `campaign.py`, `test_campaign.py`. Prerequisites: none.
  Interface consumed: schema-version-1 reports with a guardrails list and boolean flag. Interface produced: exact `evaluate_policy(report: dict, *, require_all_proven: bool) -> bool`; retain `run_campaign(config: dict, transport) -> dict`.
  Add `PolicyTest.test_policy_matrix`: proven-only, unproven-only, mixed in both orders, and empty list; expect strict true only for proven-only and permissive true for all. Assert policy does not modify its report and does not trust a preexisting `exit_code`.
  In `run_campaign`, construct the existing report and derive its exit code as 0 for policy true, 2 for false using the config flag default above. Extend `CampaignTest.test_report` to assert strict unproven exit 2. Add `test_campaign_policy_modes` covering absent/false/true flag against proven/unproven transport results: missing or false always 0; true yields 0/2 respectively. Assert the full returned report equals the expected version-1 shape, including safety id and original status.
  Acceptance: pure shared policy, exact strict/legacy matrix, unchanged signature and schema. Verify `python3 -m unittest -v test_campaign`; all tests pass.

- [ ] **Task 2 — Translate only transport interruptions.**
  Objective: satisfy REQ-3. Files: `campaign.py`, `test_campaign.py`. Prerequisite: Task 1's policy interface and exit mapping.
  Interface consumed: `transport.evaluate()` returning proven/unproven or raising an exception; output remains the same version-1 report. Catch `TimeoutError` and `InterruptedError` only around that single call; use status `"unproven"`, id `"safety"`, then the Task 1 policy. Do not broaden the catch to report construction or policy evaluation.
  Add `CampaignTest.test_transport_interruptions` using counting doubles for each exception with missing, false and true flags. Assert exactly one invocation, full safety-unproven report, exit 0 for missing/false and 2 for true. Add `test_unrelated_exception_propagates` with `ValueError` and `RuntimeError`, asserting the same exception instance escapes and call count is one. Add `test_config_unchanged` comparing a deep copy of a config with nested unrelated fields after success, interruption and unrelated-error paths.
  Acceptance: no retry, swallowed unrelated exception or config mutation; no publication or infrastructure added. Verify `python3 -m unittest -v test_campaign`; all tests pass. Inspect the diff for the single transport call and narrow exception boundary.

- [ ] **Task 3 — Integrate CLI policy and prove compatibility locally.**
  Objective: finish REQ-2 and local evidence for REQ-4. Files: `cli.py`, proposed `test_cli.py`. Prerequisites: Tasks 1–2.
  Interfaces consumed: Task 1's `evaluate_policy` and unchanged `run_campaign`; retain `main(config_path: str, transport) -> int`. Parse the config once, pass it to `run_campaign`, evaluate its returned report with the same flag/default and shared policy, assign the resulting 0/2 to `report["exit_code"]`, print exactly that report as JSON, and return its exit code. CLI adds no independent guardrail rule or transport invocation.
  Add `CliTest.test_cli_policy_matrix`: temporary JSON configs with missing/false/true flag, transport returning proven/unproven or raising each supported interruption. Capture stdout, parse the single JSON document and assert exact expected version-1 safety report and equality of return value to JSON exit code. Assert transport call count one in each case. Add `test_cli_unrelated_exception_propagates`: an unrelated transport exception escapes, with no report printed. Add `test_cli_uses_shared_policy`: patch the imported CLI policy to return false for a proven report and assert invocation with that report and `require_all_proven=False`, JSON exit 2 and return 2. This detects a duplicated CLI decision rule.
  Acceptance: old configs and false flag retain 0, strict paths agree between API/CLI, full JSON shape remains compatible. Verify `python3 -m unittest -v test_campaign test_cli`, then the documented `python3 -m unittest -v`; all tests pass. Run the documented suite in Python 3.9 before clearing the local compatibility gate; if no Python 3.9 interpreter is available, record this check as blocked rather than substituting a newer interpreter result.

## Blocking gates and verification strategy

- [ ] **Local correctness gate:** Tasks 1–3 accepted; all documented unittest checks pass, including Python 3.9 execution. Exact mode, empty-list, schema, exception, call-count and immutability assertions above are required. Current state: pending implementation; only the original one-test baseline passed.
- [ ] **Compatibility review gate:** inspect the final source/test diff against REQ-1–REQ-3. Public signatures except the requested additive policy remain unchanged, full reports and CLI JSON retain their fields, missing/false configs return 0, and no dependencies outside Python 3.9 standard library, retry, publication or infrastructure appear. Current state: pending implementation.
- [ ] **Live-provider release gate:** in the actual release environment with provider credentials, exercise the real existing provider integration with old configs and explicit false/true configs. Retain sanitized evidence of schema-version-1 report compatibility, proven/unproven statuses and expected CLI/API exits (permissive 0, strict proven 0, strict unproven 2), and verify the actual adapter's interruption behavior is compatible with the planned exception handling. Use established provider fixtures/scenarios; no command or integration path is supplied here, so do not invent one. Evidence must name the environment/runtime, candidate revision, scenarios and actual results without exposing credentials. Current state: **blocked** by unavailable credentials and release environment. Any untested required live scenario keeps this gate blocked; test doubles cannot clear it.

Release v1.1 is blocked until all three gates pass. A plan can be complete while release remains blocked. Failed gates require correcting the implementation or resolving the provider evidence gap and rerunning affected checks; do not weaken the promises to mark release ready.

## Risks, coverage and handoff

Empty-list vacuous truth and mixed statuses are covered in Task 1; overly broad catches, retries and mutation in Task 2; CLI divergence and permissive regressions in Task 3. Local doubles may differ from the real provider: only the live gate resolves that risk. No persistence/schema migration is introduced, so no data migration or recovery procedure is needed. If compatibility gates fail, withhold v1.1 and keep the existing release.

Coverage: REQ-1 → Task 1 and Task 3 matrices; REQ-2 → Task 1 shared interface and Task 3 CLI/shared-policy tests; REQ-3 → Task 2 and CLI interruption tests; REQ-4 → all three blocking gates. No product decision blocks these scoped tasks; the live check's executable command and results require the unavailable release context.

Implementation is not authorized by this planning request. After review, a possible handoff is: “Use panda-execute (native) to implement `plan.md`, preserving the blocked live-provider release gate.” Native execution fits these three tightly dependent tasks in two small production modules. Do not begin implementation as part of this task.
