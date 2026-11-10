# Routing decisions

| Condition | Decision |
| --- | --- |
| User directly names a specialist | Use it; Lead is optional and does not become a prerequisite. |
| Research versus brainstorm | Establish what evidence supports → Research; explore which direction to take → Brainstorm. Ordinary evidence gathering stays within the active workflow. |
| Research versus debugger versus impact | Standalone technical question → Research; causal defect investigation → Debugger; proposed change dependencies → Impact. |
| Research versus write | Evidence-backed answer or research note → Research; developer/operator documentation → Write. A focused explanation needs neither automatically. |
| Spec versus plan | Spec defines contracts and design; plan defines ordered changes. Produce the requested artifact. |
| Write versus spec versus manual | General developer/operator docs → Write; implementation-oriented design → Spec; user interactions → Manual. |
| Debug versus review | Existing failure needing causal explanation → Debugger; defects in a diff → Review. |
| Perf versus debugger versus simplify | Resource cost and optimization diffs → Perf; functional failure cause → Debugger; unnecessary structure → Simplify. General review still catches concrete performance defects. |
| Sec versus review | Dedicated vulnerability/secret/dependency audit → Sec; general changed-code correctness (including security defects) → Review. Do not run both automatically. |
| Refactor versus simplify / plan / execute / test / review | Complete behavior-preserving structural improvement → Refactor; general complexity assessment → Simplify; plan-only → Plan; existing approved plan → Execute; test-only → Test; general diff review → Review. Respect direct invocation and read-only limits; skip satisfied stages and avoid peer redispatch loops. |
| Review versus simplify | Correctness and material risks → Review; unnecessary structure and simpler alternatives → Simplify. |
| Missing requirement | Inspect existing evidence; ask a targeted question only if it changes correctness, scope, or risk. |
| Request changes mid-task | Preserve the original objective unless replaced; apply new limits immediately and reassess only affected activities. |
| User challenges a recommendation | Reassess its premise against the evidence and existing coverage before proposing a replacement. |
| Specialist unavailable | Report the limitation; load available instructions through documented host support, or offer ordinary assistance with that limitation stated. |
| Findings invalidate a plan | Record the contradiction, revise dependent tasks, and seek a decision only for material scope, requirement, or risk changes. |
| Independent activities | Use sequential work by default; optional native delegation needs no custom agent infrastructure. |

## Recommending additions

Before recommending another skill, tool, component, or workflow, inspect relevant
existing coverage. State the unmet outcome and why using or extending an existing
capability would be insufficient. A new name or broader role alone does not
establish a distinct capability. Recommend no addition when existing coverage
satisfies the need; label unverified gaps as hypotheses.

For idea requests, provide options, trade-offs, and a recommendation at that level.
For explicit creation or implementation requests, deliver the authorized artifact
without repeating an already settled exploration. Route substantive Agent Skill
design or evaluation to `panda-skill-lab`; ordinary recommendations need no formal
benchmark. This coverage check is local to the proposed addition, not a full audit.

Examples:

- “Check whether this SDK version supports our authentication flow” → Research.
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
