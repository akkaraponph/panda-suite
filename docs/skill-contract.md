# Skill contract and extension

Each skill provides its identity and triggers in YAML frontmatter, then the
inputs, workflow, outputs, completion conditions, scope, missing-information
behavior, and integration boundaries needed to perform its task. Those elements
need not be repeated as mechanical headings.

Essential rules are local to each skill so copying a specialist directory alone
does not break it. A specialist may name an optional peer capability, but does
not require another skill, a parent folder, or Panda Lead. Skill-local references
contain conditional detail. This file is maintainer guidance, not a required
runtime dependency.

Evidence distinguishes direct observations, source-based inference, proposals,
assumptions, and unknowns. Verification includes actual commands/results or an
explicit not-run/blocked reason. Artifact creation does not imply permission to
change application code, deploy, publish, or trigger external side effects.

To add a capability:

1. Establish a distinct user need and test scenario that existing skills do not
   cover. Prefer improving an existing skill over adding an overlapping one.
2. Create one independently usable `skills/<name>/SKILL.md` with a matching name
   and a precise discovery description. Put necessary references inside it.
3. Add the route, catalog expectation in the validator, a meaningful scenario,
   and documentation. Avoid mandatory cyclic dependencies.
4. Validate metadata and references, test direct and routed behavior, and report
   what the comparison actually supports. Keep baseline failures and successes.

The essential expansion adds requirements, testing, impact, release, and skill evaluation. Advanced standalone skills require a demonstrated distinct need.
