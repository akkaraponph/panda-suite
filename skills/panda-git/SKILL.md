---
name: panda-git
description: Inspect Git repository state, recommend or create meaningful commits, and handle branching, conflicts, history, and recovery when a task explicitly involves Git operations or commit messages.
---

# Panda Git

Understand the actual changes before choosing a commit type or changing history.
Own Git operations and commit conventions; ordinary implementation, code review,
release readiness and deployment retain their own scope. A coding task alone
does not authorize a commit or activate a full Git workflow.

## Keep commit work in Git scope

A request to commit, review a commit, or write a commit message authorizes Git
work only. Inspect and describe code issues that affect the requested commit,
but do not edit, refactor, repair, or otherwise amend source code unless the user
also explicitly asks for those code changes. If a fix is needed before a safe or
accurate commit, report the finding and ask whether to make that fix; do not
silently change the purpose or contents of the request. Preserve user-provided
scope, intent, and constraints when selecting files and writing the message.

Never use `git commit --amend`, rewrite an existing commit, or fold changes into
an earlier commit unless the user explicitly requests that history change. A
plain request to “commit my code” means create a new commit for the requested
changes, subject to the scope and index checks below.

## Establish scope and state

Identify the repository, desired operation, intended paths or revisions, applicable
repository instructions, and authorization already present in the conversation.
Inspect current state with [repository inspection](references/repository-inspection.md).
Separate index, worktree, untracked files, and ongoing merge/rebase state. Ask only
when an unresolved boundary changes which content or history would be modified;
continue safe inspection meanwhile. Missing Git, an inaccessible repository, or
failed commands limit the result; report the failure instead of inventing state.

## Choose the operation

- **Message only:** inspect the requested diff and relevant source, determine its
  purpose and compatibility impact, and return a message without changing Git state.
  If only a description or patch is supplied, label the recommendation provisional.
- **Commit review:** `$panda-git commit` defaults to a proposal. Show the complete
  recommended message, intended paths/file count, type and scope rationale,
  breaking changes, verification evidence or gaps, and material risks. With no
  execution authorization, say “Proposal only; no commit performed.”
- **Commit execution:** an explicit request to create the commit, including prior
  authorization in this conversation, permits execution after the review checks.
  Do not ask again for an already authorized scoped action. A shorthand review
  invocation alone does not supply execution permission. Stage only intended
  paths/hunks, inspect the full resulting index, and check it matches the approved
  scope before committing. Unexpected staged content requires resolving scope,
  not silently committing it or unstaging someone else's work. Commit execution
  does not authorize source edits, fixes, or `--amend`.
- **Conflicts:** use [conflict resolution](references/conflict-resolution.md) for
  authorized merges, rebases or cherry-picks. Preserve both sides' requirements;
  unresolved semantic conflicts need a decision before continuing.
- **Branches, history or recovery:** use [history and recovery](references/history-and-recovery.md).
  Inspect topology and preserve recoverable state before any authorized rewrite.

## Commit policy

For every recommended or executed commit, read
[commit conventions](references/commit-conventions.md). Explicit user convention
instructions take precedence over repository policy, then the Panda default:
Conventional Commits. Repository hooks still apply; a requested format does not
authorize bypassing an enforced check.

Classify from intent and actual diff, never filenames alone. Do not default to
`feat` or `fix` without evidence. Prefer one logical change per commit; recommend
separating unrelated purposes without manufacturing unnecessary commits. Passing
tests alone do not establish behavior preservation or absence of breaking changes.

## Mutation boundaries

Commit/message authority does not grant push, tag, release, deployment, hook bypass,
destructive cleanup, or published-history rewrite authority. Honor authorization
already covering each operation, including an explicit combined delivery request.
Review cannot authorize execution by itself.

Preserve unrelated edits and existing staging. Use explicit paths or hunks rather
than blind `git add .`. Before committing, inspect the exact proposed index and
check paths, file sizes, ignore rules and file contents for sensitive material.

Do not commit a file over 10 MiB without explicit user confirmation naming that
file. Report its path and size and pause before staging or committing it. Treat
the threshold as a review trigger, not proof that smaller files are safe.

Never include a detected secret or credential (for example, a populated `.env`,
private key, token, password or credential store) in a commit. Keep it out of the
index, do not print its value, and tell the user the path and type of concern. Ask
the user how to proceed; confirmation to commit does not make a secret safe to
publish. For sensitive configuration or credential-like files whose contents or
purpose are uncertain, exclude them and request explicit path-specific confirmation
before including them. Do not expose values when summarizing the concern.

Check proposed files against applicable `.gitignore` rules and review whether
unignored generated, local, cache, build, data, or environment-specific files
appear to belong there. List each such candidate with a short reason and ask the
user to confirm its inclusion before committing it. Do not add or force-add these
files while confirmation is pending. Existing tracking or staging is not consent.

Also inspect intended content for unrelated changes; redact sensitive findings in
output. Do not claim this is a comprehensive secret scan. Run normal hooks; diagnose
a failure before a bounded retry and never bypass hooks without explicit permission.
Avoid raw remote URLs or configuration dumps that could disclose credentials.

## Verify and finish

After a commit, inspect `git status --short`, `git log -1 --format=fuller` and
`git show --stat --oneline HEAD`; confirm the committed patch matches the intended
change. Report hash, complete message, checks actually run, and remaining changes.
After other operations, verify the requested branch, graph, conflict state or
remote reference with the relevant command. Command failure or uncertain remote
completion requires inspecting actual state before retrying. Report proposed,
executed and verified operations separately, including unrun checks and blockers.

Other Panda skills may load this guidance when their authorized task reaches Git
work. It needs no parent coordinator, programmatic invocation, or separate agent.
