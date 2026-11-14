# Campaign CLI v1.1 implementation plan

## Goal, scope, sources and constraints

Implement REQ-1–REQ-4 using Python 3.9 standard library only. Preserve existing API signatures, schema_version 1, report fields and CLI JSON. No retries, network publication, new infrastructure, configuration mutation or swallowed unrelated exceptions. This artifact authorizes no implementation.

Sources: requirements.md, campaign.py, cli.py and test_campaign.py; panda-plan instructions and its release-gates reference. The requested destination is plan.md.

Current behavior: run_campaign calls transport.evaluate() once and returns exit_code 0 and one safety guardrail. Exceptions propagate. cli.main loads JSON, calls run_campaign, prints the report and returns its exit_code. The supplied test checks only schema_version and status. Baseline `python3 -m unittest -v` passed one test; it does not establish v1.1 acceptance. New checks below remain planned.

## Contracts and file responsibilities

- Preserve `run_campaign(config: dict, transport) -> dict` in campaign.py and `main(config_path: str, transport) -> int` in cli.py.
- Add proposed `evaluate_policy(report: dict, *, require_all_proven: bool) -> bool` in campaign.py. For schema_version 1 reports with a guardrails list of id/status dictionaries: permissive mode returns true; strict mode returns true only for a nonempty list whose every status is exactly `"proven"`. Empty, unproven, mixed and unknown statuses fail strict policy. Ignore report.exit_code when computing policy; do not mutate the report.
- Read `config.get("requireAllGuardrailsProven", False)`. Omitted and false preserve legacy permissive behavior; true selects strict behavior. The scope covers boolean settings. Null, strings, numbers, malformed JSON, missing/malformed report fields and unsupported schema versions have no new validation or compatibility promise; do not introduce an error policy for them. Empty guardrails is a valid helper input with the explicit outcome above.
- run_campaign calls transport.evaluate() exactly once. Catch only TimeoutError and InterruptedError from that call and substitute `"unproven"`; unrelated exceptions propagate unchanged. Keep the exception boundary around the transport call only.
- Construct the existing report: `{"schema_version": 1, "exit_code": 0 or 2, "guardrails": [{"id": "safety", "status": status}]}`. Set exit_code to 0 when evaluate_policy returns true and 2 otherwise. No new fields or schema migration.
- cli.main uses the returned report and its policy-derived exit_code as the sole JSON/return-value source. Delegation to run_campaign shares the policy outcome; do not duplicate policy logic in cli.py. Preserve one printed JSON report and existing config file loading.
- Extend test_campaign.py; add proposed test_cli.py using unittest, tempfile, contextlib, io and json. No real-provider adapter or process entry point is required. Direct helper tests cover empty/multiple results because the campaign transport currently returns one status.

## Ordered tasks

- [ ] **T1 — Add shared policy and campaign recovery** (REQ-1, REQ-2, REQ-3). No prerequisites. Implement the proposed evaluate_policy signature and integrate it into the established run_campaign signature using the contracts above. Inputs: schema_version 1 report dictionaries, boolean settings, transport.evaluate(). Output: unchanged report shape with integer exit_code 0/2 from the shared policy. Extend test_campaign.py and retain its existing regression.
  - **C1, policy unit matrix:** permissive returns true for empty, proven, unproven and mixed lists. Strict returns false for empty, all-unproven, unknown-status and mixed lists in both orders; true for one and multiple proven guardrails. Include distinct ids and assert report equals a deep copy after evaluation. Rejects vacuous `all([])` success, first-only checks, “any proven” and truthiness-based status checks.
  - **C2, campaign integration:** cross omitted/false/true settings with proven/unproven transport results. Expected codes: omitted 0/0; false 0/0; true 0/2. Assert exact report dictionary, preserved status and config equality to a deep copy. Rejects an unused helper, changed report shape or accidental default strictness.
  - **C3, failure/recovery:** cross each TimeoutError and InterruptedError with omitted/false/true settings. Expected exact report has safety/unproven, schema_version 1 and code 0/0/2 respectively. Count exactly one evaluate() call on normal and caught-failure paths; assert unchanged config. An unrelated RuntimeError instance must propagate as that same instance after one call. Rejects retries, broad catches and synthetic proven results.
  - Acceptance: C1–C3 plus the original test pass, with unchanged signatures. Review the diff for the narrow catch boundary and absence of retry, publication, infrastructure and mutation. Run `python3 -m unittest -v` under Python 3.9.
  - Produces for T2: `run_campaign(config: dict, transport) -> dict` returning schema_version 1, integer policy-derived exit_code 0/2 and guardrails containing id/status; unrelated exceptions still propagate.

- [ ] **T2 — Verify CLI and old-config compatibility** (REQ-1–REQ-4). Depends on T1 and consumes its exact report/exception contract. Preserve cli.main(config_path: str, transport) -> int and delegation; change cli.py only if necessary. Add test_cli.py with temporary JSON config files and captured stdout.
  - **C4, CLI integration:** cross `{}`, an old config with an unrelated key, explicit false and true with proven/unproven outcomes and each caught exception. Assert main's returned integer equals parsed JSON exit_code; assert exact report shape, status, schema_version 1 and exactly one printed JSON report. Only strict unproven/failure cases return 2; permissive cases return 0. Assert one transport call. Rejects CLI policy drift, unconditional success and incompatible output.
  - **C5, propagation and runtime regression:** unrelated RuntimeError propagates unchanged through main, prints no report and calls transport once. Run the full original/expanded unittest suite on Python 3.9; review signatures and imports for the standard-library-only constraint. A newer interpreter does not prove Python 3.9 compatibility.
  - Acceptance: C1–C5 pass and review confirms one policy implementation and preserved permissive/API/CLI/schema contracts. Established command: `python3 -m unittest -v`; record interpreter version. If python3 is not 3.9, use an available Python 3.9 equivalent command (environment-specific, proposed), or leave this evidence pending.

## Review focus

| Original-test gap | Required outcome | Owning check |
| --- | --- | --- |
| Empty strict results | false | T1/C1 |
| Later unproven guardrail | mixed list fails in either order | T1/C1 |
| Timeout/cancellation and retries | one evaluation, unproven; strict 2/permissive 0 | T1/C3, T2/C4 |
| Broad exception swallowing | unrelated exception propagates unchanged | T1/C3, T2/C5 |
| CLI divergence | returned integer equals policy code in JSON | T2/C4 |

## Traceability

| Requirement | Tasks | Checks / expected evidence |
| --- | --- | --- |
| REQ-1 default, strict, all and empty | T1, T2 | C1–C2 policy/config matrices, C4 CLI matrix; passing test output |
| REQ-2 shared interface, report and JSON | T1, T2 | C1–C2, C4–C5 plus diff review of signatures and single policy implementation |
| REQ-3 recovery and exclusions | T1, T2 | C2–C3 config/call-count/exception assertions, C4–C5 CLI failures; scoped diff review |
| REQ-4 v1.1 compatibility and gates | T1, T2, G1–G2 | C2/C4 old configs, C5 Python 3.9 run, release-revision evidence and live-provider artifact |

Dependency graph: T1 → T2; no missing prerequisites or cycles. Task checkboxes remain unchecked until their acceptance evidence exists.

## Blocking release gates — defined; evidence pending

Future release checks are separate from implementation tasks.

| Gate / source | Required condition | Verification / expected evidence | Blocking | Revision / environment |
| --- | --- | --- | --- | --- |
| G1 functionality and compatibility, REQ-1–REQ-4 | C1–C5 pass; original API/schema/CLI and permissive config behavior preserved; narrow recovery with no retries/mutation | Full unittest output, Python version, actual candidate revision identifier, diff review against pre-change revision. Doubles establish only injected-transport behavior. | Yes: mandatory functional and compatibility acceptance | Actual v1.1 candidate under Python 3.9; candidate revision does not yet exist |
| G2 live provider compatibility, REQ-4 | Actual provider transport works with v1.1 and old configurations; schema_version 1 and permissive API/CLI code 0 remain compatible | Future credentialed evaluation through the real release transport. Capture sanitized config, observed status/report, CLI return/JSON, provider/environment identity, Python version and release revision; compare old-config behavior with prior release. Verify policy against observed provider status; document scenarios the provider cannot exercise. Local doubles cannot replace this evidence. | Yes: explicitly required live check | Credentials and release environment unavailable. Record actual adapter/environment and candidate revision when available. No live result claimed. |

No gate is passed by this plan, and no release READY assessment is made. G1/G2 evidence is pending. No owner or latency target was supplied or invented.

Rollback: no persisted state or migration is introduced. Reverting code restores prior permissive behavior but removes strict enforcement and timeout/interruption recovery; it cannot retain the v1.1 strict guarantee. Planned code adds no publication or irreversible action. Future live checks must use the authorized provider environment and record any effects of the actual adapter.

## Readiness and handoff

**EXECUTION-READY** for T1 and T2: no unresolved decision blocks implementation. First unblocked task: T1. Python 3.9 execution and live-provider compatibility are evidence gaps. Unavailable release credentials/environment do not block implementation/local tests, but G2 blocks release.

Review the plan before implementation. No execution is authorized by this request. A later handoff can say: “Use panda-execute (native) to implement plan.md.” Native execution fits these two tasks sharing one report/policy contract, followed by a whole-change review. Release verification remains separate.
