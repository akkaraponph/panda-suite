# Actual actions

All commands used the supplied specialist directory as their working directory.

1. Ran `pwd; rg --files -g 'TASK.txt' -g 'AGENTS.md' -g 'RTK.md' -g 'SKILL.md'`.
   Result: confirmed the specialist directory and found `TASK.txt` and
   `instructions/panda-write/SKILL.md`; no local AGENTS.md or RTK.md was listed.
2. Ran `cat TASK.txt; rg --files`.
   Result: read the task and listed the six supplied files (task, source, test,
   requirements, skill, and engineering-document reference).
3. Ran `cat instructions/panda-write/SKILL.md; cat service.py; cat test_service.py; cat requirements.md`.
   Result: read the supplied skill and all relevant implementation, test, and
   proposal evidence. The engineering-document reference was not loaded because
   the requested short guide does not require substantial architecture guidance.
4. Ran `python3 -m unittest -v`.
   Result: `test_manager_can_approve_pending` and `test_member_cannot_approve`
   both passed; 2 tests, `OK`.
5. Ran this example:

   ```sh
   python3 - <<'PY'
   from service import approve, label
   request = {"id": 1, "status": "pending"}
   actor = {"id": 2, "role": "manager"}
   approved = approve(request, actor)
   print(approved)
   print(label(approved))
   print(request)
   PY
   ```

   Result (exit 0):

   ```text
   {'id': 1, 'status': 'approved', 'reviewer_id': 2}
   1: approved
   {'id': 1, 'status': 'pending'}
   ```
6. Used `apply_patch` to create `developer-guide.md`, `ANSWER.md`, and this log.
   No application source or existing tests were edited. Python execution may
   create its normal `__pycache__` runtime files.
