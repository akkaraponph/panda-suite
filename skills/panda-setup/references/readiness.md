# Readiness verification and report

## Checks

Run each applicable check with the commands written into the instructions:

| Check | Evidence |
| --- | --- |
| Dependencies resolve | Install exits 0 and the lockfile exists or is unchanged for existing projects |
| Build or ecosystem check | Build, `go build ./...`/`go vet ./...`, Python import/compile |
| Type check | `tsc --noEmit`/framework equivalent, or "not applicable" with a reason |
| Lint | The configured linter runs; if none is configured, say so |
| Meaningful test | At least one test that exercises real behavior passes; an empty suite does not count |
| Smoke | Start the app, request the documented endpoint or page, observe the expected status and content, then stop the process |
| Instructions match | Every command and path in AGENTS.md was run or exists |
| Ignore rules | `git check-ignore` both directions per the gitignore reference |
| No secrets | Tracked files contain only placeholders; `.env` stays untracked |

A generator's successful exit proves only that files were written. Stop any
dev server you started. Prefer an ephemeral port when the default might collide,
and report the port used.

Status vocabulary: **passed**, **failed** (with the actual error), **not run**
(with the reason), **blocked** (with the missing prerequisite). Never infer a
pass from a different check, and never describe one stack as tested because a
different stack passed.

## Readiness labels

- **Ready:** every applicable check passed.
- **Partially configured:** some changes made, some checks failed, not run, or blocked.
- **Audit only:** no files changed; findings and proposed edits listed.

## Report template

```markdown
## Setup result: <Ready | Partially configured | Audit only>

Created/updated: <files, grouped; "none" for an audit>
Stack: <framework@version on runtime@version, package manager@version> (checked <date>)
Start: <exact commands with working directory>

| Check | Command | Status | Notes |
| --- | --- | --- | --- |

Remaining: <user actions, incomplete steps, how to resume>
Sources: <official links used for versions and commands>
```

For a partial failure, also list the step that failed with its error output
summarized, what completed before it, and the exact next command to resume.
