# Actual actions

1. Read `TASK.txt`, `requirements.md`, `service.py`, and `test_service.py` with `cat` (exit 0).
2. Ran these local commands in this folder, in sequence (combined command exit 0):

```sh
python3 -m unittest discover -s . -p 'test_*.py'
nl -ba service.py
nl -ba requirements.md
python3 - <<'PY'
from service import approve
request = {'id': 1, 'status': 'pending', 'description': 'example'}
result = approve(request, {'id': 2, 'role': 'manager'})
print('result =', result)
print('original =', request)
print('same object =', result is request)
try:
    approve({'id': 1, 'status': 'approved'}, {'id': 2, 'role': 'manager'})
except ValueError as error:
    print('nonpending =', type(error).__name__, str(error))
PY
```

Test output:

```text
..
Ran 2 tests in 0.000s
OK
```

Direct-call output:

```text
result = {'id': 1, 'status': 'approved', 'description': 'example', 'reviewer_id': 2}
original = {'id': 1, 'status': 'pending', 'description': 'example'}
same object = False
nonpending = ValueError request must be pending
```

The numbered source shows the role check on service.py lines 5–6, status check on lines 7–8, dictionary return on line 9, and label on lines 12–13. requirements.md line 7 states no persistence or network interface exists. The entire provided service contains no database or HTTP implementation.

3. Wrote `ANSWER.md` and `ACTIONS.md` only. No application source or tests were edited, and no production or network calls were made. No PostgreSQL server, HTTP deployment, or implementation outside this folder was inspected.
