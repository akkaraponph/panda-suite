# Normalize labels

`normalize_labels(values)` accepts a list of strings. It trims whitespace,
lowercases labels, skips blanks, and preserves order and every normalized
occurrence. It returns a new list and leaves the input unchanged.

Run from this directory:

```sh
python3 - <<'PY'
from service import normalize_labels
print(normalize_labels([' Alpha ', '', 'ALPHA', ' Beta ']))
PY
```

Executed output:

```text
['alpha', 'alpha', 'beta']
```

The previous implementation used `dict.fromkeys`, which collapsed equal
normalized labels into one dictionary key. Returning the comprehension directly
preserves repeated occurrences.
