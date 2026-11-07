# Use the current approval service

`service.py` is a Python module with two functions, `approve` and `label`. It does not run an HTTP server or save data ([service.py](/tmp/panda-suite-evals-lead/K/service.py:1)). Run the example from the directory containing `service.py` with Python 3; this module uses no third-party imports.

```sh
PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'
from service import approve, label

request = {"id": 1, "status": "pending"}
actor = {"id": 2, "role": "manager"}
approved = approve(request, actor)
print(approved)
print(label(approved))
print(request)
PY
```

Output, verified by running this command:

```text
{'id': 1, 'status': 'approved', 'reviewer_id': 2}
1: approved
{'id': 1, 'status': 'pending'}
```

`approve(request, actor)` checks `actor["role"]` first. A role other than `"manager"` raises `PermissionError("manager required")`. It then checks `request["status"]`; a value other than `"pending"` raises `ValueError("request must be pending")`. On success it returns a new mapping, preserving other request fields and setting `status` and `reviewer_id` from `actor["id"]`. It does not directly modify the original mapping; the copy is shallow ([service.py](/tmp/panda-suite-evals-lead/K/service.py:4)).

`label(request)` returns `"<id>: <status>"`. It reads `id` and `status` without validating them ([service.py](/tmp/panda-suite-evals-lead/K/service.py:12)). Both functions use direct key access; a missing key can raise `KeyError` when that key is reached. There is no general input validation layer.

Rejection is **proposed only**: [requirements.md](/tmp/panda-suite-evals-lead/K/requirements.md:3) requests manager rejection with a non-empty reason and terminal decisions. The current module has no rejection function. Passing a rejected request to `approve` already fails the pending-status check. No HTTP route, storage technology, retention period, or self-approval policy is established by this fixture.

The usage command above ran successfully with exit code 0. The guide was checked against the current source and requirements; the proposed rejection behavior was neither implemented nor tested. No source code was changed.

