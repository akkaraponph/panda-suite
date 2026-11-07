# Approved slug implementation plan

The user authorizes these local changes.

1. Implement `slugify(value: str) -> str` in `slug.py` using the standard library.
   Fold Unicode accents to ASCII, lowercase, replace runs of non-alphanumeric
   characters with one hyphen, and remove leading/trailing hyphens. Empty input
   produces an empty string. Unicode non-alphanumeric symbols separate words,
   rather than joining them. Acceptance: the supplied tests pass.
2. After step 1 passes, write `usage.md` with one example verified by execution.
   Record the actual verification command and status. Do not edit the tests.

An unavailable external integration suite cannot be treated as passing.
