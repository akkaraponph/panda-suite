# Developer guide: current approval service

`service.py` provides two Python functions. It has no HTTP server or database, so calling it does not persist a decision. Rejection is a proposal in `requirements.md`; no reject function exists yet.

`approve(request, actor)` requires `actor["role"] == "manager"` and `request["status"] == "pending"`. It checks the role first and raises `PermissionError("manager required")` for other roles. A non-pending status raises `ValueError("request must be pending")`.

On success, it returns a new dictionary containing the request fields, with `status` set to `"approved"` and `reviewer_id` set to `actor["id"]`. It leaves the original dictionary unchanged. The copy is shallow, so nested values remain shared. Inputs have no explicit schema validation; missing required keys can raise `KeyError`.

`label(request)` returns `<id>: <status>` using the request’s `id` and `status` fields.

Run this example with Python 3 from the directory containing `service.py`:

```sh
python3 -B - <<'PY'
from service import approve, label

request = {"id": 1, "status": "pending", "title": "Office supplies"}
actor = {"id": 2, "role": "manager"}

approved = approve(request, actor)
print(approved)
print(label(approved))
print(request["status"])
PY
```

Expected output, confirmed by running the example:

```text
{'id': 1, 'status': 'approved', 'title': 'Office supplies', 'reviewer_id': 2}
1: approved
pending
```

Run the existing tests with `python3 -B -m unittest -v`. Both supplied tests passed: manager approval and member denial. They do not test rejection. The proposed manager rejection with a non-empty reason and terminal approved/rejected states has not been implemented; this guide documents only the current code.
