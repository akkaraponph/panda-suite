# Repository inspection

Use the requested checkout; confirm its root before proposing mutations. Inspect
only what the operation needs, using explicit `git -C <path>` when outside it.

```sh
git rev-parse --show-toplevel
git status --short --branch
git branch --show-current
git rev-parse --git-dir --git-common-dir
git worktree list --porcelain
git diff --cached --stat
git --no-pager diff --cached --no-ext-diff --no-textconv
git --no-pager diff --no-ext-diff --no-textconv
git ls-files --others --exclude-standard
git log -8 --format='%h %s'
git diff --cached --check
```

An empty branch name indicates detached HEAD, not permission to invent a target.
The Git directory/common directory distinction reveals linked worktrees. Reuse a
suitable checkout unless user or repository instructions call for isolation.
Determine whether HEAD exists before using HEAD-based ranges in a new repository.
Inspect untracked content intended for inclusion; ordinary diff omits it. For
large changes, paginate by file/hunk and account for every intended file rather
than silently treating truncated output as a complete review.

Inspect branch tracking and relevant graph for remote operations. Local tracking
refs may be stale; a network fetch requires access and is not proof of a push.
Avoid dumping remote URLs with embedded tokens. Status, names and stats are a
summary; source/diffs establish intent and the index establishes commit content.
