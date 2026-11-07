---
name: panda-lead
description: Coordinate engineering and product delivery when a request spans discovery, planning, implementation, review, or documentation, or the user wants help choosing a Panda workflow.
---

# Panda Lead

Select the smallest workflow that delivers the user's requested outcome. This
skill coordinates; specialists own their methods. A focused explanation or tiny
edit can be handled directly without another skill or a project plan.

## Route and act

1. Identify the requested outcome, evidence, constraints, and existing
   authorization. Inspect relevant current artifacts before asking for missing
   information. Ask only where ambiguity materially affects correctness or scope.
2. Respect an explicitly named specialist. Otherwise use the table below. For
   overlap, route by the artifact the user wants, not by a keyword in their prompt.
3. Load only the selected skill through the host's documented discovery or
   instruction-reading mechanism. Use native delegation when available,
   authorized, and helpful. Reading instructions is not programmatic invocation.
   If a skill is absent, say so and explain any ordinary assistance you can still
   provide; never claim that the absent skill ran.
4. For a compound request, order dependent activities and carry forward a compact
   [handoff](references/handoff.md). A feature build may need plan → execute;
   an existing approved plan needs execute. Add review or documentation when
   requested or required by the project's acceptance criteria. Run independent
   activities separately only when host capabilities and authorization permit.
5. Compare delivered artifacts and actual verification with the requested
   outcome. Report implemented, verified, partially verified, blocked, or not
   started work accurately. Include remaining decisions or risks.

| Requested outcome | Skill |
| --- | --- |
| Explore an idea, assumptions, alternatives | `panda-brainstorm` |
| Clarify business rules, actors, acceptance | `panda-requirements` |
| Design, add, run, or assess tests | `panda-test` |
| Trace proposed change dependencies | `panda-impact` |
| Prepare release readiness | `panda-release` |
| Create or evaluate Agent Skills | `panda-skill-lab` |
| Ordered implementation work and acceptance criteria | `panda-plan` |
| Implement authorized work | `panda-execute` |
| Diagnose unexpected behavior | `panda-debugger` |
| Find defects in a change | `panda-review` |
| Assess unnecessary complexity | `panda-simplify` |
| README, developer guide, runbook | `panda-write` |
| Technical contracts or design specification | `panda-spec` |
| User journey instructions | `panda-manual` |

Use `buddhist-method` only at a relevant uncertainty, repeated failure, pressure,
or complexity decision. Do not load it as a mandatory stage. For routing conflicts
or changed requests, read [routing decisions](references/routing.md).

Investigation, planning, review, and recommendations do not authorize source
changes. An explicit implementation request authorizes relevant reversible edits;
carry that permission forward without asking again. Destructive operations,
publication, deployment, production changes, and external side effects require
authorization covering those actions. A new request can narrow earlier scope.

Skip satisfied activities. Requirements define what; Plan orders work; Impact traces what may break. Test owns test effectiveness; Debugger owns causal investigation. Release preparation never implies deployment. Use Review for focused security review, Debugger for telemetry investigation, Plan for migration planning, Brainstorm for usability exploration, and Spec for ADRs until distinct workflows justify separate skills.

## Success discipline

Identify the requested outcome and evidence of completion. Continue useful authorized work, keep attention on current evidence, and compare the result with the outcome before reporting completion. State any remaining uncertainty or blocker. Chanda: When the request changes, identify the current outcome and carry forward evidence and authorization.
