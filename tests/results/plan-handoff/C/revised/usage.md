# slugify usage

`slugify(value: str) -> str` in `slug.py` turns text into a URL slug using only the
Python standard library. It folds accents to ASCII, lowercases, collapses every run of
non-alphanumeric characters (including Unicode symbols such as emoji and dashes) into a
single hyphen, and trims leading and trailing hyphens. Input with no letters or digits
returns an empty string.

## Example

```python
from slug import slugify

slugify("Café déjà vu — 2024!")  # "cafe-deja-vu-2024"
```

## Verification

| Check | Command | Status |
| --- | --- | --- |
| Example above | `python3 -c 'from slug import slugify; print(slugify("Café déjà vu — 2024!"))'` | Passed: printed `cafe-deja-vu-2024` |
| Supplied unit tests | `python3 -m unittest -v test_slug` | Passed: 5 tests, exit 0 |
| External integration suite | Not run | Not verified: the runner was unavailable |

## Limitation

Letters with no Unicode decomposition to ASCII, such as `ß`, `ø`, or non-Latin scripts,
are treated as separators rather than transliterated. For example, `slugify("Straße")`
returns `"stra-e"`.
