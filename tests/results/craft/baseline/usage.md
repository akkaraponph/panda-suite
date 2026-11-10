# Normalize labels

`normalize_labels` accepts a list of strings, trims leading and trailing
whitespace, lowercases each label, and skips blank labels. It preserves order
and every normalized occurrence without changing the input list.

Executed locally from this directory with `python3`:

```sh
python3 - <<'PY'
from service import normalize_labels
labels = [' Alpha ', '', 'ALPHA', ' Beta ', 'alpha']
print(normalize_labels(labels))
print(labels)
PY
```

Actual output (exit 0):

```text
['alpha', 'alpha', 'beta', 'alpha']
[' Alpha ', '', 'ALPHA', ' Beta ', 'alpha']
```

Local verification: the three supplied unit tests and five focused acceptance
cases passed. The external integration runner is unavailable and was not run.
