# Dependency security report

The two historical rows do **not** prove the deployed app is vulnerable. The supplied evidence supports no currently applicable dependency advisory in the captured vendor snapshot; it does not establish that the app is free of vulnerabilities.

| Advisory | Evidence and disposition |
| --- | --- |
| SYN-001, historically critical | The September 1 audit covered app-parser 2.3.0. The current lock lists production app-parser 2.4.1. The authoritative November 1 snapshot affects versions below 2.4.0 and identifies 2.4.0 as fixed. The locked version is outside that range: this old finding is stale/resolved for the supplied lock. |
| SYN-002, historically high | The lock still lists build-helper 1.1.0, which matches the historical version range. However, the authoritative snapshot withdraws this advisory because the reported vulnerability could not be substantiated. It is not a supported active vulnerability. Moreover, build-helper is development-only and, per context.md, is not deployed. Development compromise could still matter, but this withdrawn row supplies no evidence of one. |

The attempted current scan exited 2 because the advisory service was unavailable and produced no results. This is a failed scan, not a clean scan. The November 1 snapshot is the only supplied current advisory evidence. Deployment scope is supplied by context.md; the actual deployed version was not independently inspected. The lock supports the version conclusion, not proof that production runs that exact artifact.

No dependency upgrade is justified by these two rows alone: app-parser already exceeds its stated fixed version, and SYN-002 is withdrawn. Retain the historical report for traceability, mark these dispositions, verify the deployed app-parser artifact against the lock, and rerun the audit when the service is available under a separately authorized workflow. Review development dependencies on their own merits.

## Separate source observations

Static inspection of app.py identifies issues independent of those dependency advisories. Under the supplied assumption that these entry points receive untrusted values without validation wrappers:

- `find_user` concatenates `name` into SQL, allowing SQL injection. Use the parameter binding already demonstrated by `find_user_safe`.
- `import_profile` calls `pickle.loads` on untrusted bytes, exposing unsafe deserialization and possible arbitrary code execution. Replace this input format with a constrained data format and validate its structure. No deserialization payload was executed.

`find_user_safe` binds its SQL parameter; `read_invoice` binds both parameters and restricts the query to the authenticated actor's owner ID. These snippets do not support SQL-injection or missing-owner-check findings. `parse_settings` uses JSON parsing, which does not itself substantiate a pickle-style code-execution finding. `EXAMPLE_TOKEN` is explicitly a placeholder, not evidence of an exposed credential. These are bounded static conclusions, not a full application or runtime assessment.

No network, installs, auto-fix, source edits, server access, credentials, or exploit execution were used.
