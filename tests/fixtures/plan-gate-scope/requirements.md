# Snapshot consistency requirements

Keep the current Dynamic document snapshot correct after Master File sync.
Invalidate the current snapshot before rebuilding it. If rebuilding fails,
reads must fall back to relational data. Preserve historical revisions.

Python 3 standard library only for this fixture. Do not add dependencies.
