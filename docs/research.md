# Repository and packaging research

Inspected on 2026-11-07. The supplied briefs define the product and authorize
implementation in this repository. Neither upstream repository is modified.

## Upstream findings

| Project | Inspected revision | Findings |
| --- | --- | --- |
| [Panda Debugger](https://github.com/akkaraponph/panda-debugger) | `0b9f367954d59c44ee5e033859e29af0347f9267` | One skill in `skills/panda-debugger`, four progressive references, three text scenarios, two runnable defective fixtures, evaluation rubric, Claude/Codex manifests and marketplaces. No LICENSE file in the tracked tree. |
| [Buddhist Method](https://github.com/akkaraponph/buddhist-method) | `525a52fffa9db11fddfd3e4cb10c58c9efaa4e24` | Root skill, two references, English/Thai READMEs, MIT license, and pressure-test report. README installation examples point at `nai0om/buddhist-method`; Suite pins the requested `akkaraponph` repository and preserves original text. |

Debugger's causal confidence is separate from reproduction status. Its fix gate
already recognizes prior explicit authorization; there is no need for a second
approval after an investigation-and-fix request. Preserve its report, confidence
labels, and reference loading rather than writing a competing debugger.

Buddhist Method's core triggers and extended principles cover claim checking,
diagnosis, current state, discarded approaches, cause removal, pressure, sizing,
long-task attention, failed retries, delivery completeness, and bounded foresight.
Its reported 14 pressure runs have no skill-absent control. They are upstream
evidence with stated limits, not evidence of Panda Suite improvement.

## Integration alternatives

| Option | Benefit | Cost / decision |
| --- | --- | --- |
| Independent installation | No copied upstream files | Users must coordinate two extra installs; discovery differs. Supported as an alternative, not the default package. |
| Submodule | Revision pin and clear history | Recursive checkout and packaging traversal are easy to miss. Rejected for the initial package. |
| Subtree | Ordinary checkout includes source | Adds merge/update machinery and upstream layout still needs discovery adaptation. Unnecessary here. |
| Controlled vendoring | Offline clean checkout, exact skill folders, preserved references | Requires lock and drift checks. Selected for these small repositories. |
| Wrapper | Can adapt invocation | Risks a competing workflow and cannot make absent skills available. No wrapper workflow. |
| One plugin | One installation exposes all skills | Host-specific manifests remain necessary. Selected on top of vendoring. |

All tracked upstream files are retained. Executable skill files are placed in
`skills/`; remaining upstream material is archived under the primary skill directories.
The lock maps every original path to its destination and records SHA-256 hashes.
Debugger's absent license is recorded rather than replaced with a guessed license.

## Platform evidence

- [Agent Skills specification](https://agentskills.io/specification): directory
  name matches frontmatter name; required name and description; YAML parsing;
  progressive references. Format validity alone does not prove host discovery.
- [OpenAI packaging](https://developers.openai.com/plugins/build/plugins): root
  `plugin.json` with Agent Plugins schema; fixed `skills/` directory; optional
  `extensions.com.openai`; legacy `.codex-plugin/plugin.json` is a fallback.
- [Codex local skill discovery](https://learn.chatgpt.com/docs/build-skills):
  `.agents/skills` at repository and user scope; symlinked folders supported.
- [Claude manifest reference](https://code.claude.com/docs/en/plugins-reference):
  `.claude-plugin/plugin.json`, default root `skills/`, paths contained in package.

Local CLIs inspected: Codex 0.159.2 and Claude Code 2.1.251. Their plugin command
help is available. Installation and live discovery are evaluated separately from
manifest parsing; see `docs/verification.md` for actual results and limits.
