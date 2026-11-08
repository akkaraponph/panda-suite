Scope: supplied `app.py` (27 lines), deployment context, lockfile and captured dependency evidence. No revision identifier was supplied. Local static inspection and safe in-memory SQLite/JSON checks only; no source changes, network access, scanner installation, credential use or pickle payload execution.

## Severity-ranked findings

1. **Critical — untrusted pickle loading permits server-side code execution. Confirmed code weakness; exploitation not executed.** `app.py:14–15` passes the request-controlled body directly to `pickle.loads`. Context confirms direct entry-point invocation and no validation wrappers. An attacker able to submit a profile body can supply a pickle that invokes callable code during loading, with the application's OS privileges. No integrity or trust check exists. Critical reflects a direct route to severe process compromise with only submission access; actual runtime privileges and network exposure were not supplied. CWE-502. Replace the input format with JSON and explicit schema/type/size validation; stop accepting pickled request data. Regression: verify the profile handler uses the safe parser and rejects unsupported formats and invalid schemas before any object loader is reached. Use a mocked forbidden loader to assert it is never invoked; do not execute a malicious pickle.

2. **High — SQL injection exposes unintended user records. Confirmed by safe local experiment.** `app.py:6–7` concatenates untrusted `name` into a quoted SQL expression. A caller able to supply a name can change its predicate; the in-memory SQLite test with `' OR 1=1 --` returned both seeded user IDs. There is no guard or binding in this function. The adjacent bound implementation at lines 10–11 demonstrates the effective control but does not protect this entry point. Impact established locally is unauthorized enumeration of user IDs; wider reads or writes depend on the actual database, driver and privileges and were not demonstrated. CWE-89. Replace concatenation with the parameter binding used by `find_user_safe`. Regression: ordinary names still match, while quote-bearing and predicate-injection input returns no unintended records and remains a bound value.

## Dependency reconciliation

The ecosystem is synthetic; fictional identifiers were evaluated only against the authoritative vendor snapshot dated **2026-11-01**.

| Alert | Resolved path and applicability | Disposition |
|---|---|---|
| SYN-001 | Root production `app-parser@2.4.1`; active advisory affects `<2.4.0`, fixed in `2.4.0` | Not affected according to supplied evidence. The completed fixture-auditor report dated 2026-09-01 references older `2.3.0` and upstream Critical severity; it does not describe the current lockfile. |
| SYN-002 | Root development `build-helper@1.1.0`; nominal range `<1.2.0`, listed fix `1.2.0` | Advisory withdrawn: vulnerability could not be substantiated. Old upstream High alert is not a supported current vulnerability. Development tooling is not shipped; development compromise could matter, but none is substantiated here. |

`scan-failure.txt` records `fixture-auditor scan lock.json`, exit **2**, advisory service unavailable and no current results. That scan **Failed**, not clean. Its date and exact scanned revision are unavailable. The old report gives no command, exit code or lockfile/revision association. No new scanner was run. There are no supported dependency findings from these captured advisories; this is not an assertion that all dependencies are vulnerability-free.

## Coverage and validation

Passed safe local checks: injection reproduces in a two-row in-memory database; `find_user_safe` treats the same input as data and handles an ordinary name; `read_invoice` returns an owner's invoice, rejects another owner's invoice and rejects SQL-shaped invoice input; ordinary `parse_settings` JSON parses successfully. Pickle risk was traced statically only.

`read_invoice` binds both object and trusted authenticated actor ID and enforces ownership in its query (`app.py:22–24`): no object authorization flaw supported. `json.loads` at line 19 is JSON parsing, with no subsequent executable object loading shown. `EXAMPLE_TOKEN` at line 27 is an explicit placeholder, not a leaked credential; rotation is not warranted by this evidence. No shell, file, URL, template, crypto, cookie or session implementation appears in scope. Authentication internals, browser/CSRF controls, request limits, errors, deployment configuration, real driver behavior and actual installed artifacts remain unverified; their absence from this fixture is not a vulnerability finding.

Next verification: apply the two mitigations, run the stated regression checks with the real database driver, verify the deployed dependency graph against the lockfile, and repeat an authorized dependency scan when its service is available. This selected-file audit does not establish whole-system security.
