# Routing policy

The authoritative routing table is in [Panda Lead](../skills/panda-lead/SKILL.md).
Its [decision table](../skills/panda-lead/references/routing.md) handles overlaps,
direct invocation, missing capabilities, changed requests, and stale plans.
Its [handoff contract](../skills/panda-lead/references/handoff.md) preserves scope
and authorization between activities.

Lead matches exploration, recommendation, and artifact creation to the request.
Before recommending an addition, it checks what existing capabilities cover and
identifies the unmet outcome. A challenged recommendation calls for reassessing
its premise before proposing a replacement. No addition is a valid conclusion;
an explicit artifact request still authorizes scoped creation. See the
[v1.1.1 refinement and verification](v1.1.1.md).

Routing is a model-followed instruction policy, not a keyword classifier or a
Python routing service. No deterministic runtime dispatch is claimed. The explicit
table makes decisions inspectable; behavior is tested with actual tasks.

Specialists are usable directly. Lead loads metadata first, then the selected
workflow, then conditional references. It does not preload every skill, require
multi-agent execution, or run a reasoning discipline between every activity.

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

Craft is an optional explicitly requested composition workflow for selected Panda
or external specialists. Lead retains general workflow selection and coordination;
Craft focuses on their shared outcome contract, handoffs and acceptance evidence.
Neither is a prerequisite for the other. This overlap is intentional; added
behavioral benefit remains an evaluation question. See [Craft design and checks](panda-craft.md).
