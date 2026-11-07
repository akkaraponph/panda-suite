# Routing decisions

| Condition | Decision |
| --- | --- |
| User directly names a specialist | Use it; Lead is optional and does not become a prerequisite. |
| Spec versus plan | Spec defines contracts and design; plan defines ordered changes. Produce the requested artifact. |
| Write versus spec versus manual | General developer/operator docs → Write; implementation-oriented design → Spec; user interactions → Manual. |
| Debug versus review | Existing failure needing causal explanation → Debugger; defects in a diff → Review. |
| Review versus simplify | Correctness and material risks → Review; unnecessary structure and simpler alternatives → Simplify. |
| Missing requirement | Inspect existing evidence; ask a targeted question only if it changes correctness, scope, or risk. |
| Request changes mid-task | Preserve the original objective unless replaced; apply new limits immediately and reassess only affected activities. |
| Specialist unavailable | Report the limitation; load available instructions through documented host support, or offer ordinary assistance with that limitation stated. |
| Findings invalidate a plan | Record the contradiction, revise dependent tasks, and seek a decision only for material scope, requirement, or risk changes. |
| Independent activities | Use sequential work by default; optional native delegation needs no custom agent infrastructure. |

Examples:

- “Explain this function” → inspect and explain directly.
- “Investigate this payment failure. Do not edit” → Debugger, read-only.
- “Build this feature, review it, update the README” → Plan if needed, Execute,
  Review, Write. No brainstorm when requirements are already clear.
- “Implement this approved plan” → Execute; preserve existing authorization.
- “Write a Thai backend specification” → Spec; no application implementation.
- “Create a user manual without browser access” → Manual; label evidence limits.

Prevent loops: specialists need not invoke Lead, and Lead does not restart itself
after a handoff. Load each workflow once for its activity; revisit only when new
evidence changes the task.
