# Actions: specialist/F

## Evaluation provenance

This task and F, G, J, K in both arms were completed in one shared evaluator context. They are eight artifacts, not eight independent samples. The corresponding raw fixtures and directed skill instructions were available together. No grading answers, cases.json, baseline results, Suite documentation, or other agents' work was accessed. No Suite source was edited.

## Instruction loads

Instructions were read through exec_command using cat, not invoked programmatically. The selected workflow is panda-spec.

```sh
cat '/Users/akkaraponph/Workspaces/codespaces/panda-lead/skills/panda-spec/SKILL.md'
```

Result: exit 0; read the entire selected specialist instruction. Instructions were initially loaded in a shared batch containing the four selected specialists and panda-lead, all relevant to the assigned tasks.

```sh
cat /Users/akkaraponph/Workspaces/codespaces/panda-lead/skills/panda-spec/references/specification.md
```

Result: exit 0; read the specification section menu and current/proposed/open decision prompts.

No other specialist references were loaded for this task. The short manual did not need the substantial-guide reference. Host using-superpowers/SKILL.md was read once; its SUBAGENT-STOP says dispatched subagents ignore that workflow. RTK.md was absent at cwd and checked ancestor paths.

## Initial metadata and raw evidence

A shared initial rg --files inventory displayed case filenames, including names outside the assignment, without reading those cases' contents. TASK.txt and raw sources for only F, G, J, K in both arms were read using cat/nl. The following captured per-workspace reread is the exact raw evidence used to check the draft. Skill instructions and case text are not runtime verification.

Working directory: `/tmp/panda-suite-evals-specialist/F`

```sh
nl -ba TASK.txt
nl -ba service.py
nl -ba requirements.md
nl -ba test_service.py
shasum -a 256 service.py requirements.md test_service.py
```

Exit code: 0

```text
     1	Use panda-spec. Read its instructions at /Users/akkaraponph/Workspaces/codespaces/panda-lead/skills/panda-spec/SKILL.md through available instruction-loading tools. Load only relevant references or specialist instructions. Do not claim a programmatic skill invocation.
     2	
     3	เขียน Backend Technical Specification ภาษาไทยจาก service.py และ requirements.md แยกพฤติกรรมปัจจุบันกับการออกแบบที่เสนอ ระบุข้อที่ยังตัดสินใจไม่ได้ ห้ามแก้ source code
     1	"""Small, current approval service. No HTTP server or database is implemented."""
     2	
     3	
     4	def approve(request, actor):
     5	    if actor["role"] != "manager":
     6	        raise PermissionError("manager required")
     7	    if request["status"] != "pending":
     8	        raise ValueError("request must be pending")
     9	    return {**request, "status": "approved", "reviewer_id": actor["id"]}
    10	
    11	
    12	def label(request):
    13	    return f'{request["id"]}: {request["status"]}'
     1	# Approval change request
     2	
     3	Current behavior is in `service.py`. Add a rejection decision for managers.
     4	Rejection requires a non-empty reason; approved/rejected requests are terminal.
     5	Preserve existing approval behavior and caller payloads. Do not pick HTTP routes,
     6	storage technology, retention periods, or self-approval rules without evidence.
     7	No persistence or network interface exists in this fixture.
     1	import unittest
     2	
     3	from service import approve
     4	
     5	
     6	class ApprovalTest(unittest.TestCase):
     7	    def test_manager_can_approve_pending(self):
     8	        self.assertEqual("approved", approve(
     9	            {"id": 1, "status": "pending"}, {"id": 2, "role": "manager"}
    10	        )["status"])
    11	
    12	    def test_member_cannot_approve(self):
    13	        with self.assertRaises(PermissionError):
    14	            approve({"id": 1, "status": "pending"}, {"id": 2, "role": "member"})
3abe1fb9453956e6e60fd81880903c4e5640154f7cfc37008c313f48210eb364  service.py
1dd3e304aa550a3ae07fe36658b671e2254958e3d3db3742aa3c93a06a2c3971  requirements.md
24f9120d22ff5a819a424564aec3f2689b1a0fd74a10270daa05f1fb17cb9325  test_service.py
```

## Before/after fixture check

Before artifact creation, in the same working directory:

```sh
shasum -a 256 service.py requirements.md test_service.py
```

Exit code: 0

```text
3abe1fb9453956e6e60fd81880903c4e5640154f7cfc37008c313f48210eb364  service.py
1dd3e304aa550a3ae07fe36658b671e2254958e3d3db3742aa3c93a06a2c3971  requirements.md
24f9120d22ff5a819a424564aec3f2689b1a0fd74a10270daa05f1fb17cb9325  test_service.py
```

The hashes from the captured reread after ANSWER.md creation match these values exactly. Source/test/requirements and supplied fixtures remain unchanged.

## Executed verification

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v
```

Exit code: 0

```text
test_manager_can_approve_pending (test_service.ApprovalTest.test_manager_can_approve_pending) ... ok
test_member_cannot_approve (test_service.ApprovalTest.test_member_cannot_approve) ... ok

----------------------------------------------------------------------
Ran 2 tests in 0.000s

OK
```

These are the two existing approval tests, not rejection tests. Proposed acceptance checks in ANSWER.md were not written or run.

## Artifact writes and supported outcome

Used tools.apply_patch to add only ANSWER.md and this ACTIONS.md in this workspace. ANSWER.md is the actual final response for this case. Source was preserved; local Python commands used PYTHONDONTWRITEBYTECODE=1. No tools were installed and no external actions were performed.

Produced a Thai technical specification separating current behavior, proposed rejection design, proposed verification, and open decisions. No missing HTTP/storage policy was invented.

## Instruction assessment

No material instruction conflict prevented completion. The instructions provided explicit evidence and source-change boundaries. This shared-context run does not measure independent repeatability or establish a performance advantage for either arm.

