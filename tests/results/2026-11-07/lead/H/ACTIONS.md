# Actual actions and evidence

Evaluation context is shared across assigned cases; these are not independent samples. All operations use supplied local artifacts. Instructions were loaded by reading files, not by a programmatic skill invocation.

Relevant skill/reference paths read:
- skills/panda-lead/SKILL.md

Initial case artifact SHA-256:
- TASK.txt: c1e059eb1543ceb7bca538546cfcaa957c87d6f4fed48f43544680901c597cd4
- service.py: 3abe1fb9453956e6e60fd81880903c4e5640154f7cfc37008c313f48210eb364
- test_service.py: 24f9120d22ff5a819a424564aec3f2689b1a0fd74a10270daa05f1fb17cb9325
- requirements.md: 1dd3e304aa550a3ae07fe36658b671e2254958e3d3db3742aa3c93a06a2c3971

```sh
cat skills/panda-lead/SKILL.md
```

Exit status: 0

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

```sh
cat TASK.txt service.py test_service.py requirements.md
```

Exit status: 0

```text
Use panda-lead. Read its instructions at skills/panda-lead/SKILL.md through available instruction-loading tools. Load only relevant references or specialist instructions. Do not claim a programmatic skill invocation.

Explain what label(request) in service.py does.
"""Small, current approval service. No HTTP server or database is implemented."""


def approve(request, actor):
    if actor["role"] != "manager":
        raise PermissionError("manager required")
    if request["status"] != "pending":
        raise ValueError("request must be pending")
    return {**request, "status": "approved", "reviewer_id": actor["id"]}


def label(request):
    return f'{request["id"]}: {request["status"]}'
import unittest

from service import approve


class ApprovalTest(unittest.TestCase):
    def test_manager_can_approve_pending(self):
        self.assertEqual("approved", approve(
            {"id": 1, "status": "pending"}, {"id": 2, "role": "manager"}
        )["status"])

    def test_member_cannot_approve(self):
        with self.assertRaises(PermissionError):
            approve({"id": 1, "status": "pending"}, {"id": 2, "role": "member"})
# Approval change request

Current behavior is in `service.py`. Add a rejection decision for managers.
Rejection requires a non-empty reason; approved/rejected requests are terminal.
Preserve existing approval behavior and caller payloads. Do not pick HTTP routes,
storage technology, retention periods, or self-approval rules without evidence.
No persistence or network interface exists in this fixture.

```

```sh
python3 -c 'from service import label; print(label({'"'"'id'"'"':7,'"'"'status'"'"':'"'"'pending'"'"'}))'
```

Exit status: 0

```text
7: pending

```

```sh
python3 -c 'from pathlib import Path; import hashlib; print('"'"'service.py'"'"',hashlib.sha256(Path('"'"'service.py'"'"').read_bytes()).hexdigest()); print('"'"'test_service.py'"'"',hashlib.sha256(Path('"'"'test_service.py'"'"').read_bytes()).hexdigest())'
```

Exit status: 0

```text
service.py 3abe1fb9453956e6e60fd81880903c4e5640154f7cfc37008c313f48210eb364
test_service.py 24f9120d22ff5a819a424564aec3f2689b1a0fd74a10270daa05f1fb17cb9325

```

Final hashes above match the initial artifact hashes for the listed read-only source/tests (or, for M, unchanged plan/tests). Python may create local __pycache__ files; no production state was accessed. ANSWER.md is the actual final response for this workspace.

Shared-context instruction provenance: earlier batched reads across assigned cases also loaded these absolute paths; these loads are not independent evaluations:
- skills/panda-lead/SKILL.md
- skills/panda-debugger/SKILL.md
- skills/buddhist-method/SKILL.md
- skills/panda-execute/SKILL.md
- skills/panda-review/SKILL.md
- skills/panda-write/SKILL.md
- skills/panda-manual/SKILL.md
- skills/panda-lead/references/handoff.md
- skills/panda-debugger/references/investigation-guide.md
- skills/panda-debugger/references/backend-evidence.md
- skills/panda-debugger/references/report-template.md

No grading cases, Suite documentation, baseline results, or other evaluator outputs were read. No Suite repository files changed. A requested RTK.md was absent from the current workspace and checked parent locations.
