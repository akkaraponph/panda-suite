---
name: panda-requirements
description: Refine business requests and stakeholder expectations into testable software requirements when actors, permissions, workflow rules, acceptance criteria, or scope are incomplete or conflicting.
---

# Panda Requirements

Define what the system must accomplish before choosing its implementation.
Use this for requirements refinement; use planning for ordered engineering tasks,
or specification writing for agreed technical contracts. A clear small change
does not need a separate requirements exercise.

## Inputs and workflow

Start with the business request and available stakeholder, workflow, source, and
policy evidence. Read supplied material before asking for information. If a
missing decision changes permissions, money, state transitions, or acceptance,
ask the stakeholder a targeted question; a useful draft may retain it as open.

1. **Understand the problem.** Identify the business goal, stakeholders, actors,
   current and desired workflow, constraints, scope, and non-goals. Separate the
   underlying need from a suggested architecture or feature.
2. **Classify premises.** Mark confirmed requirements with their source. Keep
   assumptions, proposed behavior, conflicts, and missing information distinct.
   Stakeholder requests can conflict; do not silently choose one as approved.
3. **Analyze rules.** Examine actor permissions, states and allowed transitions,
   ordering, required/optional data, validation, exceptions, failures, and external
   dependencies. Include duplicate or concurrent actions when relevant. Existing
   source establishes current behavior, not automatic stakeholder approval of it.
4. **Define functional requirements.** Give each meaningful requirement a stable
   identifier, description, actor/component, expected behavior, constraints, and
   acceptance criteria. Group related rules instead of inflating trivial work
   into many requirements. Keep proposed rules visibly proposed.
5. **Define relevant quality requirements.** Consider security, reliability,
   auditability, accessibility, performance, retention, and maintainability only
   where the outcome needs them. Record a missing target as a decision; never
   invent an availability percentage, latency budget, or retention period.
6. **Check acceptance and completeness.** Use observable statements, optionally
   Given/When/Then. Cover relevant actors, denied operations, state boundaries,
   invalid data, and failure outcomes. Resolve contradictions or identify who must
   decide them; do not invent ownership. Every confirmed requirement needs a
   testable outcome, and every open material rule needs its impact stated.

## Output and boundaries

Produce a Requirements Analysis with problem statement, business goal, scope and
non-goals, actors/permissions, identified functional requirements, business rules,
relevant non-functional requirements, acceptance criteria, edge cases, and open
questions. Omit irrelevant quality categories rather than fabricating detail.
Completion means confirmed behavior is testable and unresolved decisions are
visible, including whether they block planning.

Requirements analysis authorizes its requested document, not application changes
or stakeholder decisions. Do not implement, migrate data, or perform external
actions. A handoff to `panda-plan`, if requested and available, carries identifiers,
sources, constraints, decisions, unknowns, and actual authorization. This skill
works independently; no master or peer skill is required.

## Success discipline

Identify the requested outcome and evidence of completion. Continue useful authorized work, keep attention on current evidence, and compare the result with the outcome before reporting completion. State any remaining uncertainty or blocker. Kalāma: When requirements conflict, preserve their sources and identify the decision needed.
