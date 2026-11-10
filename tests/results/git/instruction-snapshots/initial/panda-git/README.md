# Panda Git

Use `$panda-git` standalone, `$panda-suite:panda-git` in a Codex plugin, or
`/panda-suite:panda-git` in a Claude plugin after installing this release.
The host reads [SKILL.md](SKILL.md); the command examples are natural-language
requests, not an executable command parser.

```text
$panda-git commit
```

Inspects staged changes and proposes a complete message with scope, risks and
verification gaps. To execute, say “create the commit for these changes”; existing
explicit authorization is honored. Message/review requests alone leave Git state
unchanged. Push, tags, release publication and destructive actions need their own
authorization.

```text
$panda-git Recommend a message for the auth diff; do not stage or commit.
$panda-git Create the commit for src/auth.py and its test; leave my draft alone.
$panda-git Resolve this merge while preserving both validation requirements.
```

Conventional Commits is the fallback after user and repository conventions.
Relevant details load from local references; no Panda Lead or runtime is needed.
