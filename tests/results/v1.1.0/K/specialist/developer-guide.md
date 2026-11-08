# Approval service developer guide

`service.py` provides two Python functions. It has no HTTP server, database,
network interface, or persistence. Run the example from this directory with
Python 3; the service uses no third-party libraries.

## Run an approval

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

Verified output:

```text
{'id': 1, 'status': 'approved', 'reviewer_id': 2}
1: approved
{'id': 1, 'status': 'pending'}
```

## Current behavior

- `approve(request, actor)` first checks `actor["role"]`. Any value other than
  `"manager"` raises `PermissionError("manager required")`.
- It then checks `request["status"]`. Any value other than `"pending"` raises
  `ValueError("request must be pending")`.
- On success, it returns a new dictionary containing the request fields, with
  `status` set to `"approved"` and `reviewer_id` set to `actor["id"]`. Existing
  values for these two fields are overwritten. The input request is unchanged;
  the copy is shallow.
- `label(request)` returns `"<id>: <status>"` using the request's `id` and `status`.
- Required keys are accessed directly. Missing keys raise `KeyError` when that
  access is reached; there is no separate payload validation layer.

The caller supplies the actor and request. The module does not authenticate the
actor or save the returned approval.

## Proposed rejection behavior

`requirements.md` proposes a manager rejection decision with a non-empty reason,
terminal approved/rejected states, and preservation of existing approval behavior
and caller payloads. Rejection is not implemented. The current approval function
already refuses any non-pending status, but there is no rejection function or
general decision lifecycle. No routes, storage technology, retention policy, or
self-approval rule is specified or implemented.

## Verification and evidence

Run `python3 -m unittest -v`. The two existing tests verify approval by a manager
and denial for a member. Both passed, and the usage example above ran successfully.
The tests do not cover every behavior documented here.

| Claim | Source |
| --- | --- |
| Approval checks, returned copy, and errors | `service.py`, `approve` |
| Display string | `service.py`, `label` |
| Existing test coverage | `test_service.py`, `ApprovalTest` |
| Proposed rejection and scope constraints | `requirements.md` |
