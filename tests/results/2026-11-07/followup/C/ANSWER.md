Implemented `slugify(value: str) -> str` with standard-library accent normalization, lowercase ASCII slugs, collapsed separators, and trimmed hyphens. Unicode symbols separate words. Added `usage.md` after the implementation tests passed.

Verified locally: all 5 supplied tests, 6 additional boundary assertions, and the documented example (`cafe-deja-vu`) passed. Supplied tests are unchanged (SHA-256 checked).

Both plan steps are implemented and locally verified. External integration is unverified because its runner is unavailable; overall verification is partial. No local implementation tasks remain.
