# Delivery run

Workspace: `/tmp/panda-craft-baseline-20261110` (physical path
`/private/tmp/panda-craft-baseline-20261110`). No network, installation,
publication, global configuration changes, or delegation was used.
Exact model identifier and consumption are unavailable to this runner.

## Instructions and scope

Read `/tmp/panda-craft-baseline-20261110/TASK.txt`, `brief.md`, `incident.md`,
`service.py`, and `test_service.py`.
Selected specialist instructions read:

- `skills/panda-execute/SKILL.md`
- `skills/panda-test/SKILL.md`

TASK.txt directs this run to brief.md, which authorizes implementation and
usage documentation. incident.md describes a separate investigation-only scope;
the explicit task-selected brief governed this delivery. No AGENTS.md or RTK.md
was found inside the task workspace. No other suite files were inspected.

## Exact commands and results

All shell commands ran in the task workspace. Read commands below returned
the actual fixture or instruction contents; they did not modify files.

1. `pwd; cat TASK.txt; rg --files -g 'RTK.md' -g 'AGENTS.md' -g '!node_modules' -g '!vendor'`
   — exit 1: printed physical workspace path and TASK.txt; rg found no matches.
2. `cat skills/panda-execute/SKILL.md`
   — exit 0; read Panda Execute instructions.
3. `ls -la; cat brief.md; rg --files`
   — exit 0; listed the five fixture files and TASK.txt, and read the brief.
4. `cat skills/panda-test/SKILL.md`
   — exit 0; read Panda Test instructions.
5. `cat service.py test_service.py incident.md; git status --short`
   — exit 128 after printing the three files: `fatal: not a git repository (or any of the parent directories): .git`.
   Git diff/status was unavailable; the initial source was a dict.fromkeys-wrapped
   comprehension. The supplied test file was not edited.
6. `python3 -m unittest -v`
   — exit 0; 3 tests ran, all OK (trim/lowercase, blanks, unchanged input).
7. Baseline regression:

```sh
python3 - <<'PY'
from service import normalize_labels
values = [' Alpha ', 'ALPHA', '', ' beta ', 'alpha']
actual = normalize_labels(values)
expected = ['alpha', 'alpha', 'beta', 'alpha']
print(f'actual={actual!r}')
print(f'expected={expected!r}')
assert actual == expected, 'Every normalized occurrence must be preserved'
PY
```

Exit 1. Actual output:

```text
actual=['alpha', 'beta']
expected=['alpha', 'alpha', 'beta', 'alpha']
Traceback (most recent call last):
  File "<stdin>", line 7, in <module>
AssertionError: Every normalized occurrence must be preserved
```

8. Applied a local patch replacing `return list(dict.fromkeys(` and `))` with
   `return [` and `]` in service.py. The generator expression became a list
   comprehension; normalization and filtering stayed unchanged. Tool succeeded.
9. `python3 -m unittest -v`
   — exit 0; 3 tests ran, all OK.
10. Focused acceptance checks:

```sh
python3 - <<'PY'
from service import normalize_labels
cases = [
    ([], []),
    (['', ' ', '\t\n'], []),
    ([' Alpha ', 'ALPHA', '', ' beta ', 'alpha'], ['alpha', 'alpha', 'beta', 'alpha']),
    ([' B ', 'a', 'B', ' c ', 'A'], ['b', 'a', 'b', 'c', 'a']),
    (['\tMiXeD\n', 'é', ' É '], ['mixed', 'é', 'é']),
]
for values, expected in cases:
    original = values.copy()
    actual = normalize_labels(values)
    assert actual == expected, (values, actual, expected)
    assert values == original, (values, original)
print('PASS: 5 focused cases cover empty input, whitespace blanks, trim/lowercase, order, repeated occurrences, and unchanged input.')
PY
```

Exit 0, printed the PASS line exactly as above. This includes the previously
failing duplicate case and asserts unchanged input for every case.

11. Executed the exact example command reproduced in usage.md; exit 0 with
    the two output lines reproduced there.
12. Applied a local patch creating usage.md and this RUN.md. Tool succeeded.
13. `cat service.py usage.md; wc -l RUN.md; python3 -m unittest -v`
    — exit 0; inspected the final implementation and example documentation;
    RUN.md had 108 lines before this log entry; all 3 supplied tests passed again.
14. Applied a local patch recording the final inspection in RUN.md. Tool succeeded.

## Acceptance and limitations

Implemented and locally verified: trim, lowercase, skip blanks, preserve order,
preserve every normalized occurrence, and leave input unchanged. Supplied suite
alone missed duplicates; the baseline regression exposed the defect and passed
after the fix as part of the focused checks. usage.md contains an executed example.
The fix only removes deduplication; no unrelated application code was changed.

The external integration runner is unavailable per brief.md and was not run.
Only list-of-string behavior was in scope. No permanent test additions were
needed: focused checks ran as disposable stdin scripts, preserving supplied tests.
