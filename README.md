# Panda Suite

Version **1.7.0** · 25 independent skills

![Cyberpunk Panda Suite branding](images/branding.png)

Independent Agent Skills for engineering and product delivery, coordinated when
useful by **Panda Lead**. Think clearly. Build carefully. Ship confidently.

The suite covers discovery, planning, design, implementation, debugging, review,
verification, documentation, and delivery handoff. It is Markdown instructions
plus small maintenance tools. It does not run an agent service or require
multi-agent execution.

[Documentation site](https://akkaraponph.github.io/panda-suite/) · [ภาษาไทย](README.th.md) · [Architecture](docs/architecture.md) ·
[Verification and limitations](docs/verification.md)

Start with the [complete usage guide](docs/usage.md): invocation syntax, inputs,
copyable examples and expected outputs for every skill.

Current release: [v1.7.0](docs/v1.7.0.md).

[Panda Craft](docs/panda-craft.md) composes explicitly selected specialists around
a shared outcome, compact handoffs and acceptance evidence.

## Skills

| Skill | Use it for |
| --- | --- |
| `panda-requirements` | Clarify actors, business rules and testable acceptance |
| `panda-test` | Design, add, run and assess effective tests |
| `panda-impact` | Trace dependencies and compatibility before a change |
| `panda-release` | Prepare evidence-based release readiness without deployment |
| `panda-skill-lab` | Design and evaluate skills with honest baseline comparisons |
| `panda-lead` | Select the smallest workflow and coordinate requested activities |
| `panda-git` | Inspect Git state, classify commit messages, and perform authorized Git operations |
| `panda-setup` | Initialize or prepare projects for agent-assisted development with current versions, agent instructions, ignore rules and verified commands |
| `panda-craft` | Compose explicitly selected specialists with shared acceptance and outcome verification |
| `panda-logo` | Create, refine, audit, and package brand assets with verified SVG and raster exports. See the [usage guide](docs/panda-logo.md) |
| `panda-brainstorm` | Explore a problem, constraints, assumptions, and alternatives |
| `panda-research` | Answer technical questions and verify capabilities with traceable evidence |
| `panda-learn` | Learn unfamiliar code through source tracing, mental models and optional guided practice |
| `panda-plan` | Define ordered tasks, dependencies, acceptance, and verification |
| `panda-execute` | Implement authorized work and report actual verification |
| `panda-debugger` | Investigate a failure and establish causal confidence; preserved upstream |
| `panda-sec` | Audit vulnerabilities, secrets, and dependency report applicability |
| `panda-perf` | Profile performance and memory; produce verified optimization diffs |
| `panda-review` | Find material defects in a bounded change |
| `panda-simplify` | Assess unnecessary complexity while preserving invariants |
| `panda-refactor` | Carry structural improvements from assessment through behavior-preserving changes and verification |
| `buddhist-method` | Apply optional reasoning discipline at relevant decision points; preserved upstream |
| `panda-write` | Create, review, and update accurate engineering documentation |
| `panda-spec` | Specify current and proposed technical contracts in Thai or English |
| `panda-manual` | Document observed user journeys or label supplied-evidence drafts |

Specialists work independently. A function explanation needs no project plan.
Brainstorming does not authorize implementation. Debugging does not automatically
start planning or documentation. Buddhist Method is optional rather than a stage
between every activity. Requirements, research, testing, impact, release, and skill evaluation are supported.

## Security and performance

`panda-sec` audits scoped code or diffs and triages dependency reports. Findings
include severity, confidence, attack conditions, source evidence, mitigations,
and regression checks. It validates scanner matches, redacts potential secrets,
and reports missing coverage without claiming whole-system security.

`panda-perf` traces algorithmic cost, memory retention, redundant queries, N+1
patterns, and query plans. It delivers concrete optimization diffs, preserves
behavior, and separates static hypotheses from representative measurements.
Analysis is read-only; requested local optimizations may be applied and tested.

See [v1.1.0 scope and verification](docs/v1.1.0.md) for trials, shared quality
checks, and remaining limits.

## Research and documentation

`panda-research` investigates bounded engineering questions using primary sources,
versioned documentation, and repository evidence. It returns a direct answer,
citations, contradictions, and explicit unknowns. A saved note is optional.

`panda-write` creates, reviews, and updates engineering documentation in English
or Thai. It traces each integration independently and separates implementation,
configuration, deployment, and external guarantees. Substantial handovers can load
additional guidance; small guides stay small.

See the [Research contract and checks](docs/panda-research.md) and
[Write refinement and checks](docs/panda-write-refinement.md). Both work without
Lead. Research answers a question; Brainstorm explores directions; Write produces
documentation; Spec defines proposed contracts and design.

## Install from this checkout

Use one method to avoid duplicate skill names. Check out the versioned release:

```sh
git clone --branch v1.7.0 https://github.com/akkaraponph/panda-suite.git
cd panda-suite
```

Run the commands below from that checkout. All source files are included; no
recursive checkout or bootstrap is needed. This is source distribution, not a
published package-registry release.

**License status:** original Suite files use MIT; Buddhist Method retains its MIT
license. The pinned Panda Debugger revision has no LICENSE file. Its public
redistribution terms remain unresolved; the Suite license does not cover it.
See [source notices](SOURCE_NOTICES.md).

### Claude Code

From this repository, load without installing:

```sh
claude --plugin-dir "$PWD"
```

Then use `/panda-suite:panda-lead` or a specialist such as
`/panda-suite:panda-review`.

For persistent local marketplace installation:

```sh
claude plugin marketplace add "$PWD"
claude plugin install panda-suite@panda-suite
```

The local plugin and marketplace manifests were validated with Claude Code
2.1.251, and its component inventory discovers all 22 skills. Persistent
installation and interactive model invocation were not exercised.

### OpenAI Codex

For local plugin installation:

```sh
codex plugin marketplace add "$PWD"
codex plugin add panda-suite@panda-suite
```

Use the installed skill selector. Codex 0.159.2's plugin inventory exposes
`panda-suite:panda-lead` and `panda-suite:panda-review`; select those names, or
reference `$panda-suite:panda-lead` in your request.

The portable root manifest and all 21 plugin skill paths were read by the
actual Codex app-server. Standalone discovery below was also tested. Persistent
plugin installation and interactive invocation were not exercised, and no global
user configuration was changed during validation.

### Standalone skills and compatible hosts

The copy utility uses Python 3.10+ and the standard library. Choose your host's
documented discovery directory. For a Codex project:

```sh
python3 scripts/install-skills.py --destination /path/to/project/.agents/skills --all
```

For selected user-level Codex skills:

```sh
python3 scripts/install-skills.py --destination "$HOME/.agents/skills" --skill panda-lead --skill panda-plan --skill panda-execute
```

For a standalone Claude Code specialist:

```sh
python3 scripts/install-skills.py --destination "$HOME/.claude/skills" --skill panda-spec
```

The installer copies complete directories and refuses existing names, including
late directory collisions. It does not overwrite a previous installation. Review
and back up an old copy before replacing it. An I/O error during copying can leave
a partial newly created directory; inspect it before retrying. Restart or refresh
the host if a new skill does not appear.

Standalone Codex invocation uses `$panda-lead`, `$panda-plan`, or `$panda-spec`;
standalone Claude Code uses `/panda-lead`, `/panda-plan`, or `/panda-spec`.
Other Agent Skills hosts need their own documented discovery/instruction-loading
mechanism. Format validation alone does not prove those runtimes are compatible.

## Examples

These prompts use standalone Codex names; use your installation's selector above.

```text
$panda-lead Explain what this function does.

$panda-learn ./src Teach me how a request reaches storage. Start with the
mental model and trace actual code. Read-only; offer guided practice only if useful.

$panda-sec Audit src and the supplied dependency report. Rank supported
vulnerabilities, redact secrets, and give fixes and checks. Do not edit or scan externally.

$panda-perf Analyze this slow operation and propose a concrete optimization diff.
Preserve behavior; run safe local comparisons and state workload limits.

$panda-research Check whether the pinned SDK supports our authentication flow.
Cite version-specific evidence and unresolved claims. Do not change code.

$panda-write Review docs/integration-guide.md against the implementation.
Check each integration separately and report corrections. Do not edit files.

$panda-plan Plan a manager rejection flow from requirements.md and the existing
service. Include acceptance criteria. Do not implement it.

$panda-debugger Investigate why this transfer returns success but balances stay
unchanged. Show evidence and confidence. Do not edit code.

$panda-execute Implement the approved plan in docs/plan.md. Run the relevant
checks and report any unverified acceptance criteria.

$panda-review Review this diff for material defects. Do not fix it yet.

$panda-spec เขียน Backend Technical Specification ภาษาไทยจาก source code
แยกพฤติกรรมปัจจุบัน ข้อเสนอ และประเด็นที่ยังต้องตัดสินใจ

$panda-manual Document the test application's draft-save journey. Use actual
browser observations and screenshots when available; label anything unverified.
```

For “implement this feature, review it, and update the README,” Lead can use
Plan when needed → Execute → Review → Write. It carries the objective, evidence,
artifacts, decisions, unknowns, next action, and authorization between activities.
It loads specialists as needed through real host capabilities. If a skill or tool
is missing, it reports the limitation rather than claiming an invocation.
See [routing](docs/routing.md) and [skill contract](docs/skill-contract.md).

## Authorization and evidence

Investigation, planning, review, and simplification recommendations preserve
application source unless changes were requested. An explicit implementation or
fix request already authorizes relevant reversible edits; the suite does not ask
for that approval twice. Material scope, requirement, or risk changes need a new
decision. Destructive operations, production changes, external side effects,
deployment, and publication need authorization covering those actions.

Browser manuals distinguish observed steps from supplied documentation. Missing
browser access produces a labeled draft. Proposed tests remain not run until
executed; passing a small test suite does not establish every acceptance rule.

## Validate and evaluate

The Research and Write additions pass structural validation and Codex discovery.
Their baseline/skill behavioral comparisons are **Not Run**. The v1.1.0 tooling suite corrects the stale restore-test target and adds
scenario-integrity and standalone-installation regressions for all skills.
See the reports above for scope and evidence limits.

Maintenance dependencies are separate from skill use:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python scripts/validate-skills.py
python3 scripts/vendor-upstreams.py
.venv/bin/python -m unittest discover -s tests -p 'test_tooling.py' -v
```

Optional host checks:

```sh
claude plugin validate .claude-plugin/plugin.json
claude plugin validate .claude-plugin/marketplace.json
claude --plugin-dir "$PWD" plugin details panda-suite
python3 tests/check_codex_discovery.py
```

See [evaluation instructions](tests/evaluation.md) and the
[recorded results](tests/results/2026-11-07/summary.md). The original comparative
exercise contains real successes and failures: three execution answers passed
four tests while missing a Unicode separator rule, and a compound run later
corrected it. Shared evaluator contexts prevent causal improvement claims.
No speed or token-saving claim is made.

A [browser-observed sample manual](tests/results/browser-manual/manual.md) includes
an actual screenshot from the local synthetic fixture.

## Maintain and extend

Read [upstream integration](docs/integration.md) before changing vendored files.
`python3 scripts/vendor-upstreams.py --restore` restores missing pinned files,
checks downloaded bytes, and refuses local changes. It does not update versions.
Keep new capabilities small, independently usable, and backed by meaningful
scenarios. Follow the [extension contract](docs/skill-contract.md).

Packaging sources: [Agent Skills specification](https://agentskills.io/specification),
[OpenAI plugin packaging](https://developers.openai.com/plugins/build/plugins),
[Codex skill discovery](https://learn.chatgpt.com/docs/build-skills), and
[Claude plugin reference](https://code.claude.com/docs/en/plugins-reference).

## Attribution

[Panda Debugger](https://github.com/akkaraponph/panda-debugger) supplies the existing
investigation workflow, confidence classification, references, tests, and report.
[Buddhist Method](https://github.com/akkaraponph/buddhist-method) supplies the
trigger-based reasoning discipline, terminology, references, and original pressure
evaluation. Exact revisions and file mappings are in `upstream-lock.json`.
Suite-specific research and trade-offs are in [repository findings](docs/research.md).

## Essential expansion

The five essential skills and their boundaries are described in the [expansion report](docs/expansion.md). Panda Debugger and Buddhist Method are primary Suite skills; their technique Markdown remains under each skill’s `references/`. Source attribution and pinned-byte verification remain in place. No runtime or persistent handoff store was added.

Version 1.2.0 added `panda-refactor`; its behavioral comparisons remain **Not Run**.
Version 1.3.0 adds `panda-learn` from the supplied learning/mentor proposal.
See [Learn's contract and evaluation](docs/panda-learn.md) for actual paired task
results and their limits. Learning remains read-only by default; concise questions
need no mandatory quiz, document or project workflow.

Version 1.4.0 adds `panda-craft` for explicitly selected skill composition. See
[Craft’s contract and evaluation](docs/panda-craft.md) and [release notes](docs/v1.4.0.md).
The single direct/Craft trial pair passed in both arms; no incremental benefit is
established. Stored machine-specific paths are normalized for portability.
