---
name: panda-release
description: Prepare release notes, readiness assessments, deployment checklists, rollback considerations, and delivery handoffs when changes need verification against a defined release boundary and target environment.
---

# Panda Release

Prepare an evidence-based delivery decision. Release preparation does not authorize
deployment. A merged change is not proof of successful verification or rollout.

## Inputs and workflow

Establish version, target environment, release branch/commit range or PR set,
requirements, acceptance criteria, test evidence, reviews, and available operational
constraints. Inspect existing artifacts before requesting missing information.
If the boundary or target remains unclear, state it and limit the assessment rather
than inventing a version or deployed state.

1. **Identify scope.** Inspect the actual change range and relevant issues, features,
   fixes, migrations, configuration, dependencies, and documentation. Separate
   included changes from unrelated work and unsupported release claims.
2. **Verify contents.** Trace requirements and acceptance criteria to implementation,
   test evidence, unresolved review findings, and documentation. Record each check's
   command/scope, environment, revision, actual outcome, and applicability to this
   release. Stale or different-revision evidence is not silently transferable.
3. **Evaluate delivery risk.** Assess breaking contracts, mixed service versions,
   migrations, data integrity, required configuration/access, feature flags,
   dependencies, external integrations, and rollback feasibility where relevant.
   Check whether application rollback remains compatible with changed data.
4. **Define proportional gates.** Identify the required tests, defect resolution,
   review, migration rehearsal, configuration, recovery strategy, operational owner,
   and post-deploy checks needed for this risk. Do not invent sign-off or ownership.
   Each unresolved gate names the evidence or decision needed and whether it blocks.
5. **Produce artifacts.** Prepare a source-supported change summary/release notes,
   ordered deployment checklist, relevant migration checklist, recovery/rollback
   considerations, known issues, and post-deployment verification with stop criteria.
   Commands remain proposed until executed; verify syntax against project tooling.
6. **Assess readiness.** Use the labels below and explain the deciding evidence.
   Absence of discovered defects is insufficient to establish readiness.

| Status | Meaning |
| --- | --- |
| **READY** | Release scope is known and all required evidence/gates are satisfied |
| **CONDITIONALLY READY** | Named residual risks require an explicit acceptance decision; no unresolved mandatory blocker is disguised as optional |
| **BLOCKED** | A known mandatory gate fails or a blocking defect/requirement remains |
| **UNKNOWN** | Evidence is insufficient to assess readiness; identify the deciding checks |

## Output and authorization

Deliver release scope, change summary, verification evidence, compatibility,
deployment requirements, rollback considerations, known issues, readiness, and
next actions. Completion means the preparation artifacts and limits are reviewable,
not that the release has shipped. If tools are missing, mark checks **Not Run** or
**Blocked** with reasons; do not convert them into passes.

Do not create/push release tags, publish packages, deploy services, change production
configuration, apply migrations, or send announcements without explicit authorization
covering those actions and the host's safety constraints. Preparing requested local
documents is allowed. This skill stands alone; handoffs preserve scope/revision,
evidence freshness, unresolved gates, ownership unknowns, and actual authorization.

## Success discipline

Identify the requested outcome and evidence of completion. Continue useful authorized work, keep attention on current evidence, and compare the result with the outcome before reporting completion. State any remaining uncertainty or blocker. Sati-Sampajañña: Match verification evidence to the release revision and environment.
