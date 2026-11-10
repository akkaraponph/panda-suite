# Conflict resolution

Identify the operation already in progress from status and Git's operation state.
Inspect unmerged paths (`git diff --name-only --diff-filter=U`, `git ls-files -u`),
base/ours/theirs entries and relevant callers/tests. In rebase, “ours” represents
the rebased-onto history; do not assume it means the user's original branch.

Resolve each hunk from the intended contracts on both sides. Handle rename/delete,
binary, generated and lockfile conflicts with the repository's actual tooling;
regenerate only when authorized and understood. Whole-file ours/theirs selection
needs evidence that discarding the other changes is intended. If intent conflicts,
show the concrete alternatives and obtain the needed decision while preserving state.

After authorized edits, check unresolved entries and leftover markers, inspect the
merged diff and run relevant tests. Stage only resolved intended paths. Continue
the operation only within existing authorization; a conflict-resolution request
does not authorize pushing rewritten history. If checks or hooks fail, preserve
the failure and diagnose before retrying. Aborting can discard resolution work:
inspect and preserve it before an explicitly authorized abort.
