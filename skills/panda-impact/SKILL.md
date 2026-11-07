---
name: panda-impact
description: Analyze dependencies and compatibility risks of proposed code, API, database, or architecture changes when a developer needs to know affected components, business behavior, rollout risks, and required verification.
---

# Panda Impact

Assess a proposed change before implementation. A defect investigation belongs
with causal debugging; a migration execution plan or ordinary diff review is a
different deliverable. This assessment is read-only by default.

## Inputs and workflow

Use the current and proposed behavior, affected interface or field, motivation,
constraints, and available repository/contracts. If the proposal is ambiguous,
state the alternatives and ask only for the decision that changes the assessment.
Missing consumer or production access limits confidence; it does not establish
that no consumer or stored record exists.

1. **Bound the change.** Identify the old/new contract, affected versions and
   environments, expected benefits, and scope. Cite evidence for current behavior;
   label the target as proposed until approved.
2. **Trace dependencies.** Follow relevant producers and consumers through callers,
   implementations, models, queries, serializers, UI, jobs, events, integrations,
   configuration, and tests. Record precise source paths and the relationship.
   Search beyond the changed declaration; bound each negative search by scope.
3. **Assess boundaries.** Examine stored-data compatibility, constraints and
   transformations; request/response and event contracts; validation, errors and
   state transitions; deployment ordering, mixed versions, background work,
   monitoring, and recovery where relevant. Separate code-defined schema from
   actually observed database contents or deployed versions.
4. **Classify findings.** Use **Confirmed impact** for a demonstrated dependency
   and incompatible change; **Likely impact** when evidence fits but a key boundary
   is unverified; **Possible risk** for a plausible untested condition; **Unknown**
   when evidence cannot decide. State consequence, triggering condition, evidence,
   missing check, and priority. Correlation or an identifier match alone does not
   prove an affected runtime path.
5. **Recommend mitigation.** Prefer the least complicated compatible approach.
   Describe required tests, consumer coordination, migration considerations,
   rollout checks, observability, and rollback limitations proportionate to risk.
   Lossy conversion can require recovery from backup rather than a reverse script;
   do not promise reversibility without evidence.
6. **Validate coverage.** Reconcile each material impact with a mitigation or
   explicit decision. Identify uninspected repositories, external consumers, data,
   or operational state and the smallest observation needed to resolve them.

## Output and boundaries

Deliver proposed change, confirmed dependencies, affected components, data/API
impact, behavioral impact, operational risks, compatibility assessment, recommended
mitigations, verification requirements, and unknowns. Include a small source-backed
dependency diagram only when useful. An assessment is complete when evidence and
coverage limits are clear enough to choose the next safe action.

Do not edit source, execute migrations, modify data, or trigger deployment or
external effects unless separately authorized. Requested analysis documents are
allowed. A handoff carries evidence, confidence, compatibility constraints, missing
checks, and actual permission. This skill does not require Panda Lead or a custom
dependency graph service.

## Success discipline

Identify the requested outcome and evidence of completion. Continue useful authorized work, keep attention on current evidence, and compare the result with the outcome before reporting completion. State any remaining uncertainty or blocker. Anāgataṃsa-ñāṇa: When a contract changes, inspect immediate consumers and stored-data compatibility.
