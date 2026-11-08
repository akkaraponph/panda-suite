# Dependency security report

The supplied evidence does **not** support the author's claim that both historical critical/high rows prove the deployed app is vulnerable. Neither row establishes a current dependency vulnerability within this scope.

Scope: static triage of the supplied synthetic dependency evidence and deployment context using instructions/panda-sec/SKILL.md and its audit guidance. No revision identifier or production access is supplied.

| Advisory | Historical report, 2026-09-01 | Supplied current evidence | Disposition |
|---|---|---|---|
| SYN-001 | app-parser 2.3.0; upstream Critical; affected <2.4.0; fixed 2.4.0 | Root production dependency resolves to 2.4.1. Authoritative vendor snapshot dated 2026-11-01 retains active status and the same range/fix. | Confirmed version mismatch: 2.4.1 is outside the affected range. This advisory establishes neither an affected current installation nor a deployed exploit path. No contextual Critical finding. |
| SYN-002 | build-helper 1.1.0; upstream High; affected <1.2.0; historical fix 1.2.0 | Root development dependency remains 1.1.0, numerically within the historical range. The authoritative 2026-11-01 snapshot withdraws the advisory because the reported vulnerability could not be substantiated. Development tooling is not shipped. | No supported current High vulnerability. Development compromise can matter, but this evidence establishes none. Retain the historical range and fix for traceability; do not present them as a required current security repair. |

The old fixture-auditor audit completed on 2026-09-01 but supplies no command, ecosystem, scanned lockfile or revision. Its app-parser version differs from lock.json. It is historical evidence, not proof about this deployment.

The later recorded command `fixture-auditor scan lock.json` **Failed**, exit status 2, because the advisory service was unavailable; no current scan results were produced. Its date is unspecified. This is a coverage gap, not a clean scan. No scanner was run during this review.

Checks actually performed: read supplied files and statically compared ecosystem, dependency names, root paths, resolved versions, scopes, affected ranges, dates, statuses and fixes. app.py was read as supplied context; source-code vulnerability assessment is outside this dependency-report request. No exploitation was observed or tested. No network, installation, payload execution, credential use, auto-fix or source modification occurred.

Confidence is high in these two advisory dispositions based on the supplied authoritative snapshot and lockfile. Deployment contents are supplied assertions without independent artifact/runtime verification. A broader advisory inventory, transitive graph, provenance and reachable vulnerable dependency API paths are unavailable. This result does not establish whole-system security.

Next verification: when separately authorized and the service is available, rerun the scanner against this exact lockfile and record timestamp, tool version, revision and exit status. Confirm the deployed artifact contains app-parser 2.4.1 and excludes development tooling. Reconcile new results with current advisory status and actual reachability before assigning application severity. Neither supplied row justifies an automatic fix.
