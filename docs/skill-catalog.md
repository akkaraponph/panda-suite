# Skill catalog

For every skill's inputs, example prompt, expected result and authorization limits,
read the [complete usage guide](usage.md).

The [README catalog](../README.md) lists all twenty-four skills and independent
installation methods. [Lead](../skills/panda-lead/SKILL.md) is the authoritative
routing table; [expansion decisions](expansion.md) explain the new ownership
boundaries of that milestone. [Research addition](panda-research.md) describes
the standalone evidence-gathering capability and its evaluation limits.

Examples: “clarify this approval policy” selects Requirements; “what breaks if
status changes type?” selects Impact; “add regression tests” selects Test;
“prepare this release” selects Release; “evaluate this SKILL.md” selects Skill Lab;
“initialize a Go + Fiber backend” or “prepare this repository for agents” selects Setup.
An approved feature can skip requirements and planning already completed.
Investigation-only incidents remain read-only.

Dedicated security audits select Sec; resource profiling and optimization diffs
select Perf. General Review and Simplify keep their existing responsibilities.
See [v1.1.0 evaluation and standardization](v1.1.0.md).

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

Git owns repository operations and commit conventions. Release owns readiness;
Review owns changed-code defects. Craft, Refactor and Execute load Git guidance
when their authorized task reaches Git, with a standalone fallback if absent.
See [Git design and trials](panda-git.md).
