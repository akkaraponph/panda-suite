# Branches, history and recovery

Follow the repository's existing branching model. Before creating a branch,
establish its base, upstream, naming policy and worktree occupancy; do not impose
a new GitFlow/trunk model. Check detached/unborn state and preserve local edits
before switching. Prefer a new explicit branch over guessing where work belongs.

Before amend, squash, rebase, reset, cleanup or recovery, inspect status, relevant
graph and reflog, publication state and the exact affected range. Record original
revision IDs and preserve recoverable work with an appropriate backup ref and
patch/untracked-file copy when the authorized operation could lose it. A branch
backup alone does not preserve index/worktree/untracked content. Do not stash,
reset, clean or discard edits as an automatic convenience.

Use a revert for an authorized undo on shared history unless a rewrite is explicitly
approved. An ordinary commit request does not authorize amend. Amending published
commits, rewriting shared history, deleting refs and destructive cleanup require
authorization for those effects; uncertain publication state stays uncertain.
Use reflog to locate lost commits and inspect the candidate before proposing a
recovery branch. Recover without resetting over current edits where possible.

For an authorized push, confirm remote identity, branch, target and current state.
Use explicit refs. Force-push requires explicit rewrite permission; prefer a lease
against a verified expected remote revision, and stop on a lease rejection to
inspect concurrent work. Never escalate a rejected push to unconditional force.
After a timeout or error, inspect the actual remote ref before retrying.

Tagging and publishing a release are separate actions from committing. When both
are authorized, verify version sources, checks, release notes, tag target and tag
availability first. Do not move an existing release tag silently. Publish only
the intended ref/assets and verify the remote tag and resulting release URL.
