# Using slugify

Requires Python 3 and its standard library. From this directory, import `slugify`:

```python
from slug import slugify

print(slugify("Café déjà vu"))
# cafe-deja-vu
```

`slugify(value: str) -> str` normalizes Unicode with NFKD, removes decomposed
combining marks to fold accents, lowercases, replaces each run outside ASCII
`a-z` and `0-9` with one hyphen, and trims hyphens at both ends. Empty input, or input
containing only separators, returns `""`. This is ASCII accent folding, not
full transliteration of every writing system.

Verified locally with:

```sh
python3 -c 'from slug import slugify; print(slugify("Café déjà vu"))'
python3 -m unittest discover -s . -p 'test_*.py' -v
```

Status: the example printed `cafe-deja-vu`; all four supplied tests passed.
The external integration suite was not run because it is unavailable in this
fixture. No deployment or publication was performed.
