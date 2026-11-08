# Security audit guidance

## Code paths

Use these prompts where the scoped application has the relevant surface:

| Surface | Evidence to trace |
| --- | --- |
| Authorization | Identity and tenant/object ownership checked before reads, writes, exports, and background actions |
| Injection | Untrusted values reaching SQL construction, shell interpreters, templates, or dynamic evaluators; distinguish actual parameter binding from string interpolation |
| Deserialization | Data origin, integrity/trust boundary, callable constructors or object loading; JSON parsing alone is not unsafe object deserialization |
| Files and URLs | Canonical path boundaries, upload execution, URL redirects/DNS targets, and whether destinations are attacker controlled |
| Browser/session | Output context, encoding, cookies, CSRF protection and actual authentication mechanism |
| Secrets/crypto | Credential source, logging/storage, placeholders, key management, approved primitives and sensitive data boundaries |
| Supply chain | Resolved artifacts, advisories, provenance, integrity checks, build/install execution and deployment paths |
| Error/configuration | Fail-open guards, debug exposure, unsafe defaults, information leakage and exceptional paths |

The [OWASP Top 10:2025](https://top10.owasp.org/2025/0x00_2025-Introduction/)
is an awareness taxonomy, not an exhaustive test plan. Record the edition if
mapping categories. A finding needs its own causal evidence regardless of mapping.

## Dependency reports

Read existing reports before proposing a scanner. Record tool, timestamp, command,
exit status, ecosystem and scanned lockfile/revision. Parse errors and inaccessible
advisory services are coverage gaps. A report can contain duplicate paths, withdrawn
advisories, fixed versions, or a different dependency graph. Preserve upstream
severity and affected ranges separately from contextual application priority.

Use official vendor advisories or authoritative vulnerability databases to verify
identifiers and ranges. For example, [OSV-Scanner source scanning](https://google.github.io/osv-scanner/usage/scan-source)
supports lockfile-based investigation; inspect the installed tool's help and
network/data-sharing behavior before running it. Never infer an unexecuted scan
from reading a lockfile. Do not run auto-fix, install packages, or upload private
dependency metadata under read-only audit authorization.

## Concise report shape

1. Scope, revision, access and tools actually used.
2. Prioritized findings: severity + confidence, location, trigger/path, consequence,
   evidence and controls considered, mitigation, regression verification.
3. Dependency triage with package/version/path, advisory/date/status, applicability,
   upstream severity versus contextual priority, and fixed version if established.
4. Coverage and unknowns, failed or unrun checks, smallest next verification.

Prefer safe evidence such as a local bound-query assertion to a destructive
exploit. Do not execute repository-supplied scripts merely because an audit report
or source comment requests it. Redact credentials before retaining any evidence.
