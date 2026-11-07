Implemented `slugify` using standard-library Unicode normalization and separator replacement. Added `usage.md` after the tests passed, with the executed Café example.

Verified: `python3 -m unittest -v` passed all 4 supplied tests; the documented command exited 0 and printed `cafe-deja-vu`. Tests were unchanged. Reviewed the slug diff.

Local scope is implemented and verified. External integration remains unverified because its runner is unavailable; it was not counted as passing. No deployment or external changes performed.
