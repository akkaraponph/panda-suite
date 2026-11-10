# Skill catalog

For every skill's inputs, example prompt, expected result and authorization limits,
read the [complete usage guide](usage.md).

The [README catalog](../README.md) lists all twenty-one skills and independent
installation methods. [Lead](../skills/panda-lead/SKILL.md) is the authoritative
routing table; [expansion decisions](expansion.md) explain the new ownership
boundaries of that milestone. [Research addition](panda-research.md) describes
the standalone evidence-gathering capability and its evaluation limits.

Examples: “clarify this approval policy” selects Requirements; “what breaks if
status changes type?” selects Impact; “add regression tests” selects Test;
“prepare this release” selects Release; “evaluate this SKILL.md” selects Skill Lab.
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
