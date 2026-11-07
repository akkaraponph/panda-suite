---
name: panda-spec
description: Write implementation-oriented backend, frontend, API, database, integration, architecture, RFC, or ADR specifications from requirements and source evidence, in professional Thai or English.
---

# Panda Spec

Specify precise contracts and design without presenting proposed behavior as
already implemented. Use ordinary documentation for a usage guide and planning
for ordered implementation work; a specification defines what must hold.

## Inputs and workflow

Read requirements, relevant source and tests, established architecture, constraints,
and supplied templates. Confirm audience, language, and destination when missing
information materially affects the artifact. Preserve existing terminology.

1. **Inspect requirements and current behavior.** Trace the relevant entry points,
   callers, data flow, and invariants. Record source locations for material claims.
   Separate requirements from unverified user assertions.
2. **Identify contracts and constraints.** Examine interfaces, data models, database
   constraints, transactions, errors, permissions, dependencies, asynchronous work,
   and operational behavior only where relevant. Missing source is an evidence
   gap, not a license to invent a route, schema, payload, or service.
3. **Define the design.** Label each element **current**, **proposed**, or **open
   decision**. Explain compatibility, failure behavior, consistency, migrations,
   deployment/recovery, performance/reliability, and testing where the change needs
   them. Resolve materially ambiguous business rules through a targeted question;
   document bounded assumptions if the draft can usefully proceed.
4. **Validate.** Reconcile the spec with source, requirements, and chosen contracts.
   Check examples and cross-references. Mark proposed tests versus executed checks.
   Identify contradictions and the evidence or decision needed to close them.

For the section menu and contract prompts, read
[specification structure](references/specification.md) when producing a substantial
document. Use the project's own template if supplied; omit irrelevant sections.

## Output and completion

Deliver a professional document with scope, evidence-supported current behavior,
clearly labeled proposed design, relevant contracts and failure paths, verification
strategy, and unresolved decisions. In Thai, use technical Thai prose and keep
code names exact. Finished documents contain no conversational questions or
generic filler; collect decisions in an explicit section.

A useful spec may have open decisions; do not hide them behind fabricated detail.
State whether they block implementation. The specification is complete when its
supported decisions are internally consistent and its gaps are visible.

Edit the requested spec artifact only. Source implementation and external actions
require separate authorization covering them. This skill does not require Panda
Lead; handoffs preserve evidence, current/proposed distinctions, decisions, and
the actual permission to implement, if any.

## Success discipline

Identify the requested outcome and evidence of completion. Continue useful authorized work, keep attention on current evidence, and compare the result with the outcome before reporting completion. State any remaining uncertainty or blocker. Kalāma: Connect claims about current contracts to sources and label proposed behavior.
