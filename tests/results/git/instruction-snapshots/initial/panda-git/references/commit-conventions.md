# Commit conventions

Read the diff, relevant contracts/callers, and verification evidence before
classifying. Inspect repository contribution rules, commitlint configuration and
recent history for supported scopes and format; history is evidence, not authority
to override a written rule. If policy is genuinely conflicting, expose the conflict.

## Default format

```text
<type>(<optional scope>)<optional !>: <subject>

<optional body>

<optional footers>
```

The actual header is, for example, `fix(auth): reject expired access tokens`.
Type and subject are required; scope, body and footers are conditional. Prefer a
header at most 72 characters and keep every message line at most 100 characters.
Use an imperative present-tense subject beginning with a lowercase letter and no
trailing period. These length/style requirements are Panda defaults, not mandatory
rules of the [Conventional Commits specification](https://www.conventionalcommits.org/en/v1.0.0/).
Follow an applicable user or repository override.

| Type | Intent established by the change |
| --- | --- |
| `feat` | Introduce functionality |
| `fix` | Correct defective behavior |
| `docs` | Documentation only |
| `style` | Formatting with no behavior change |
| `refactor` | Restructure without observable behavior changes |
| `perf` | Improve performance while preserving supported behavior |
| `test` | Add or improve tests |
| `chore` | Routine maintenance not covered by a more specific type |
| `ci` | CI/CD workflow changes |
| `build` | Build system or dependency changes |
| `revert` | Reverse an identified earlier change |
| `wip` | Unfinished work only when requested or allowed by repository policy |

`wip` is a nonstandard extension; avoid it in permanent shared history by default.
Tests accompanying a defect correction belong to `fix`, rather than making that
commit `test`. A file called README can contain executable behavior; inspect it.
Split unrelated work when possible; otherwise explain the primary purpose and
the secondary changes. Do not label behavior changes `refactor` because tests pass.

Use an existing repository scope where meaningful, otherwise the smallest affected
domain. Omit scope when it adds no clarity. Use a body for nontrivial changes to
explain the reason, previous limitation, new behavior and relevant tradeoff, rather
than repeating the header. Do not invent motivation or test results.

## Breaking changes and footers

Check public signatures, supported behavior, configuration, storage formats and
consumer compatibility independently of the selected type. Any type can break
compatibility. Panda's default uses both `!` before the colon and a
`BREAKING CHANGE:` footer describing the removed contract and migration. The
upstream specification permits either marker; requiring both is a local default.
If the removal's intent is unclear, flag it instead of asserting it is approved.

Include issue references only when supplied or verified as associated with this
change. Use a closing trailer only when the change actually resolves the issue;
otherwise use the repository's non-closing reference. Preserve required trailers
such as sign-off only with accurate attribution and authorized identity.

```text
fix(counting): prevent duplicate round results

Ignore repeated events with the same round ID so retries cannot increase
the round total more than once.
```

Append `Closes #128` only with evidence that the change resolves that real issue.
For a revert, identify the actual reverted revision and intent; do not fabricate
a hash or use `revert` for an unrelated fix.

## Final review

Validate the full message against the applicable format, configured types/scopes,
header and line limits, subject, breaking markers, body accuracy and trailers.
Review the exact staged diff again before execution, including mode changes,
deletions, binaries and newly tracked files. A staged stat alone is insufficient.
Use a safely written message file with `git commit --file <path>` for multiline
messages, avoiding shell interpolation of message content. Never invent passed
checks or silently suppress hooks to make the commit succeed.
