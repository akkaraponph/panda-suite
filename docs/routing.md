# Routing policy

The authoritative routing table is in [Panda Lead](../skills/panda-lead/SKILL.md).
Its [decision table](../skills/panda-lead/references/routing.md) handles overlaps,
direct invocation, missing capabilities, changed requests, and stale plans.
Its [handoff contract](../skills/panda-lead/references/handoff.md) preserves scope
and authorization between activities.

Routing is a model-followed instruction policy, not a keyword classifier or a
Python routing service. No deterministic runtime dispatch is claimed. The explicit
table makes decisions inspectable; behavior is tested with actual tasks.

Specialists are usable directly. Lead loads metadata first, then the selected
workflow, then conditional references. It does not preload every skill, require
multi-agent execution, or run a reasoning discipline between every activity.
