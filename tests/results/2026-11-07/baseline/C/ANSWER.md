Implemented `slugify(value: str) -> str` with standard-library Unicode normalization, ASCII folding, lowercase conversion, hyphen collapsing, and edge trimming.

All four supplied tests pass with `python3 -B -m unittest -v`. Added `usage.md` after those tests passed, with an executed example producing `cafe-deja-vu` (exit 0). Tests were unchanged. The external integration runner was unavailable and was not run.
