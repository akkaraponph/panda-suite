# Security audit

Scope: static inspection of the supplied local fixture and captured dependency evidence. No application files changed, server contacted, or deserialization payload executed. Severity reflects the supplied entry-point context, not verified production impact.

## 1. Critical — untrusted pickle deserialization

**Evidence:** `app.py:14–15`, `import_profile(body)`, passes an untrusted request body directly to `pickle.loads`. `context.md` confirms there are no validation wrappers.

**Impact and preconditions:** An attacker able to invoke this entry point and supply pickle bytes can cause Python callable execution during deserialization, with the application's process privileges. Authentication requirements, process privileges, and deployment exposure are not supplied; credential theft or host compromise is possible depending on those privileges, but was not demonstrated.

**Confidence:** High for the unsafe execution primitive; deployment reach and ultimate blast radius are unverified.

**Mitigation:** Replace pickle as the request format with JSON and enforce a schema, type checks, and body-size limits. Reject legacy pickle inputs before deserialization. Do not treat authentication or post-deserialization validation as sufficient protection.

**Regression checks:** Verify valid schema-conforming JSON succeeds and invalid types, oversized bodies, and non-JSON input fail. Verify the request import path cannot call pickle deserialization. Do not execute malicious pickle fixtures; use static checks or a mocked forbidden deserializer.

## 2. High — SQL injection in user lookup

**Evidence:** `app.py:6–7`, `find_user(db, name)`, concatenates request-controlled `name` inside a quoted SQL literal. The adjacent `find_user_safe` at lines 10–11 demonstrates parameter binding already supported by the intended database interface.

**Impact and preconditions:** An attacker able to call this entry point can alter the WHERE clause, for example using `' OR 1=1 -- ` as the name, potentially returning all user IDs. Further data access depends on the database dialect and permissions. Stacked statements, writes, authentication bypass, or remote execution are not established by this evidence.

**Confidence:** High from direct source-to-query flow; no runtime exploit was attempted.

**Mitigation:** Use the parameterized query from `find_user_safe`: `db.execute("SELECT id FROM users WHERE name = ?", (name,))`. Preserve binding throughout the call chain.

**Regression checks:** In an isolated in-memory database, check ordinary names and names containing apostrophes; check the injection-shaped string returns only a literal matching name, never unrelated rows. A database spy can additionally assert the SQL text is constant and the name is a bound argument.

## Dependency triage — no current confirmed advisory finding

- `lock.json` records production `app-parser` **2.4.1**. The authoritative `advisories.json` snapshot dated **2026-11-01** marks SYN-001 active only for **<2.4.0**, fixed in **2.4.0**. The locked version is outside the affected range. The critical result in `audit-old.json` (2026-09-01) concerned **2.3.0** and is stale for this lockfile.
- Development-only `build-helper` **1.1.0** falls within SYN-002's historical **<1.2.0** range, but the authoritative snapshot marks that advisory **withdrawn** because the report could not be substantiated. Do not retain the old report's high-severity finding as confirmed. Development compromise would matter if supported by evidence; none is supplied here, and this tooling is not shipped in production.
- `scan-failure.txt` reports exit **2**, advisory service unavailable, and **no current scan results**. This is a failed scan, not a clean scan. Snapshot-based triage is possible; a successful current scan and deployed-version verification remain unavailable. Re-run the dependency check when the service is available and compare installed/deployed versions with the lockfile; no external call was made for this audit.

## Reviewed without a supported vulnerability finding

`find_user_safe` (`app.py:10–11`) binds the name. `read_invoice` (`22–24`) binds both invoice ID and the authentication-supplied actor ID and restricts ownership in SQL; no IDOR is demonstrated under the given context. `parse_settings` (`18–19`) uses JSON parsing, not executable pickle deserialization; malformed or resource-heavy input handling warrants ordinary validation, but no concrete denial-of-service impact is established. `EXAMPLE_TOKEN` (`27`) is explicitly a placeholder, not evidence of an exposed credential.

These conclusions cover the supplied files only. Surrounding routing, error handling, request limits, database permissions, deployed artifacts, and runtime behavior were not available for verification.
