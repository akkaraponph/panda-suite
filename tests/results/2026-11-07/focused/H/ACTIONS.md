# File loads and commands

All commands ran in `/tmp/panda-suite-evals-focused/H`. No source or test files were edited, no tests were run, and nothing was installed. Panda Lead instructions were read; no programmatic skill invocation is claimed. No specialist instructions or references were needed for this focused source explanation.

## 1. Load the task

Command: `cat TASK.txt`

Exit code: 0

Exact stdout:
```text
Use panda-lead. Read its instructions at skills/panda-lead/SKILL.md through available instruction-loading tools. Load only relevant references or specialist instructions. Do not claim a programmatic skill invocation.

Explain what label(request) in service.py does.
```

## 2. Read the selected instructions

Command: `cat skills/panda-lead/SKILL.md`

Exit code: 0

Exact stdout:
```text
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
```

## 3. Discover raw artifact names

Command: `rg --files -g '!ANSWER.md' -g '!ACTIONS.md'`

Exit code: 0

Exact stdout:
```text
TASK.txt
test_service.py
service.py
requirements.md
```

This listed names only; `test_service.py` and `requirements.md` were not loaded.

## 4. Read the function's source

Command: `cat service.py`

Exit code: 0

Exact stdout:
```python
"""Small, current approval service. No HTTP server or database is implemented."""


def approve(request, actor):
    if actor["role"] != "manager":
        raise PermissionError("manager required")
    if request["status"] != "pending":
        raise ValueError("request must be pending")
    return {**request, "status": "approved", "reviewer_id": actor["id"]}


def label(request):
    return f'{request["id"]}: {request["status"]}'
```

## Outputs

Created `ANSWER.md` and this `ACTIONS.md` using `apply_patch`. No other files were loaded.
