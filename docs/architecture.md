# Panda Suite architecture

Panda Suite is twenty-four independent instruction skills. Panda Lead is a small
router; the host model and its existing tools perform work. There is no server,
database, scheduler, agent loop, or programmatic skill invocation API.

The supplied briefs are the implementation specification. The initial catalog and the five essential expansion skills are in scope.

## Decisions

1. **Use Markdown skills with progressive references.** Each specialist can be
   copied alone and carries its own workflow, outputs, limits, and essential
   authorization rules. No mandatory shared file outside the skill directory.
2. **Route by requested artifact and authorization.** Exploration, execution, and
   delivery describe user expectations; they are not runtime services. A focused
   explanation is answered directly. Explicit specialist invocation wins.
3. **Keep upstream skills unchanged.** Vendored files retain exact bytes and
   original identity. Additional provenance and evaluation notes live outside
   their instructions. See [research](research.md) and [integration](integration.md).
4. **Use native host capabilities.** Load selected instructions through documented
   discovery; delegate only when available, authorized, and useful. Reading a
   file is described as instruction loading, not a simulated tool invocation.
5. **Use one portable manifest and a Claude compatibility manifest.** Both point
   to the same twenty-four folders. A Codex fallback is added only if local testing
   demonstrates that this installed CLI needs it. No MCP or hooks are needed.
6. **Evaluate claims at the correct level.** Validators prove package invariants;
   real fixture tasks test behavior. No performance or token-saving claim follows
   from scenario presence, word counts, or a single successful model response.

## Boundaries

Brainstorm explores problems and options. Plan defines ordered engineering work.
Spec defines technical contracts and current/proposed behavior. Execute changes
authorized source. Review identifies defects. Simplify assesses unnecessary
complexity. Write documents engineering evidence. Manual documents observed user
journeys. Debugger owns causal investigation. Buddhist Method is consulted at
decision points; it is never a compulsory pipeline stage.

Skill dependencies are optional and flow outward from Lead to specialists.
Specialists do not route back to Lead or require each other. A compact handoff
preserves evidence, artifacts, decisions, unknowns, next action, and authorization.
Only a material scope, requirement, or risk change needs a new decision from the
user when implementation is already authorized.

Refactor owns bounded structural improvement through baseline, incremental edits
and compatibility verification. Simplify retains general complexity assessment;
Plan, Execute, Test and Review retain their focused deliverables. Direct Refactor
requests can stop at analysis or planning. Peer guidance is optional, with no
mandatory chain or new runtime. See the [Refactor design and evaluation](panda-refactor.md).

Learn owns understanding unfamiliar existing code through source tracing, adaptive
teaching and optional practice. Research owns bounded evidence questions; Write
owns requested engineering documents; Debugger owns causal failures. A tiny
explanation stays direct unless a specialist is explicitly selected. Learning does
not authorize application edits or execution. See [Learn design and trials](panda-learn.md).

Setup owns project initialization, existing-repository preparation and setup
readiness audits: current-version selection, minimal structure, agent
instructions, ignore rules and verified commands. It does not start a lifecycle
for later feature work. See [Setup design and evaluation](panda-setup.md).

Craft is an optional explicitly requested composition workflow for selected Panda
or external specialists. Lead retains general workflow selection and coordination;
Craft focuses on their shared outcome contract, handoffs and acceptance evidence.
Neither is a prerequisite for the other. This overlap is intentional; added
behavioral benefit remains an evaluation question. See [Craft design and checks](panda-craft.md).
