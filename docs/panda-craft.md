# Panda Craft — composition contract and evaluation

## Purpose and evidence

Craft implements the user's supplied “Panda Craft — Skill Composition & Execution
Harness” proposal as an optional explicit composition workflow. It keeps the
Compose → Execute → Verify intent, Iddhipāda 4 discipline, evidence-based correction
and completion status without a runtime or mandatory Buddhist Method dependency.
The Buddhist terminology and working disciplines are grounded in the existing
Buddhist Method; see [source notices](../SOURCE_NOTICES.md).

The target failure is losing a shared acceptance requirement, evidence or
permission boundary between selected specialists. Historical Suite evaluations
record a green-suite Unicode contract violation, and current Execute/Test already
contain corrections. This does not establish that another skill improves behavior.
Lead also already coordinates explicit specialists. Craft is an authorized optional
entry point; its distinct incremental value remains a hypothesis.

## Contract and integration

- Trigger: explicit Craft coordination of selected Panda or external specialists.
- Non-triggers: ordinary specialist invocation, small explanations, general
  workflow selection, or a request merely mentioning the word “craft”.
- Inputs: task, named skills, relevant current artifacts, criteria, constraints
  and allowed actions. Missing material requirements prompt a targeted question.
- Method: establish intent; load real selected instructions; order activities;
  preserve scope and compact handoffs; perform authorized work; examine acceptance
  evidence and correct within specialist budgets.
- Outputs: artifacts, skills actually loaded, actual checks, unmet criteria,
  implementation completeness and a scoped verification classification.
- Permission: source changes follow the task, not the selected skill name;
  consequential operations need authorization covering them.

The core is independently copyable; peer skills are supplied by the host or
ordinary assistance is explicitly limited. No upstream instructions were changed.
Catalog, Lead routing, English/Thai README, usage guide, site list and validator
include Craft. Version 1.4.0 packages this addition; release readiness and commands
are recorded in the [release verification](../tests/results/craft/release-verification.md).
No global installation or plugin-cache refresh is implied by publication.

The name and description conform to the [Agent Skills specification](https://agentskills.io/specification).
The host's discovered names determine invocation; examples distinguish standalone
`$panda-craft` from Codex plugin `$panda-suite:panda-craft`. Reading multiple skill
files is not programmatic invocation. Structural validity, discovery and useful
behavior are separate claims.

## Blind scenarios

Reviewer checks live in `tests/scenarios/cases.json`; task preparation copies only
`tests/fixtures/craft-composition` and the task prompt. Reviewer controls remain
outside the fixture. Cases cover:

| Case | Boundary |
| --- | --- |
| CRAFT-DELIVER | Implementation plus executed usage example; green-suite contract gap |
| CRAFT-READONLY | Investigation with testing guidance does not authorize fixes |
| CRAFT-MISSING | Selected specialist unavailable; no fabricated invocation |
| CRAFT-CONFLICT | Supplied tests pass but requirement and source disagree |
| CRAFT-AMBIGUOUS | Uniqueness conflicts with preserving every occurrence |
| CRAFT-TOOLS | Static-only tools; no fabricated execution |
| CRAFT-BUDGET | Exhausted external specialist verification budget |
| CRAFT-NONTRIGGER | Focused explanation without composition |

Example preparation from the repository root:

```sh
python3 scripts/prepare-evaluation.py --case CRAFT-DELIVER --arm baseline --destination /tmp/craft-direct-fresh
python3 scripts/prepare-evaluation.py --case CRAFT-DELIVER --arm lead --destination /tmp/craft-lead-fresh
python3 scripts/prepare-evaluation.py --case CRAFT-DELIVER --arm specialist --destination /tmp/craft-candidate-fresh
```

The baseline task explicitly selects Execute/Test; the Lead arm adds current Lead
and the specialist arm adds Craft. Use fresh contexts for each case and arm. Keep
model/settings, source snapshots, tools, permissions and budget equal; expose only
selected instructions and fixtures. Freeze/hash inputs and instructions before
comparative runs. The synthetic budget case tests instruction compliance, not
actual Impeccable rendering; real UI composition remains a separate host trial.
The missing-skill case uses an explicitly unavailable synthetic name.

Record actual answers, commands/results, loaded paths and authorized artifacts.
Assess correctness, completion, evidence, scope, verification honesty and useful
coordination. Keep reviewer controls and prior outputs away from task agents.
Repeat across cases before drawing conclusions. Measure tokens/time only when
exposed; word counts and metadata estimates do not establish savings.

## Verification and limits

A reviewer-only fixture check must confirm that the faulty normalizer passes all
three supplied tests but loses repeated normalized labels, while the correct
control passes those tests and preserves repetitions. This proves case behavior,
not model compliance. Standalone installation and blind preparation are covered
by tooling checks. Results and current behavioral status are recorded below after
execution. No benefit or overhead claim follows from packaging or a small trial.

### Actual checks — 2026-11-10 (Asia/Bangkok)

| Check | Observed result |
| --- | --- |
| Suite validator | PASS: 22 skills, references, manifests and scenario coverage |
| Tooling suite | PASS: 30 tests, including all 24 Craft case/arm blind preparations |
| Reviewer fixture control | PASS: defective and correct implementations both pass 3 supplied tests; duplicate probe distinguishes them |
| Pinned upstream verification | PASS: hashes unchanged |
| Documentation | PASS: 37 pages, 22 skill guides, 1,855 internal links |
| Codex 0.159.2 discovery | PASS: Craft in plugin and standalone inventories |
| Claude Code 2.1.251 | PASS: both manifests valid; inventory contains 22 skills including Craft |
| Diff whitespace | PASS |

### Actual bounded behavioral trial

Native fresh-context agents each performed CRAFT-DELIVER: direct Execute/Test,
then Craft plus the same specialists, in separate workspaces. No model override
was set. Settings were inherited; exact provider model identifier, temperature,
per-run budget, consumption and reliable elapsed measurements were unavailable.
Instruction-path restrictions were prompt-based, not an OS sandbox. Agent run
records list their actual loaded paths and commands; these are agent-authored
records, not complete raw harness transcripts. Final answers are retained as
plain text with links normalized to artifact names.

| Arm | Actual result and independent review |
| --- | --- |
| Direct specialists | Delivered service.py and usage.md; 3 supplied tests and 5 focused cases reported passed; independently rerun suite, duplicate/input-preservation probe, and usage example passed; supplied tests unchanged |
| Craft + specialists | Delivered service.py and usage.md; 3 supplied tests and 5 focused cases reported passed; independently rerun suite, duplicate/input-preservation probe, and usage example passed; supplied tests unchanged |

Both runs exposed the previously green-suite duplicate defect before fixing it.
Both accurately left external integration unrun. Craft explicitly separated local
verification from external integration; the direct arm also gave an accurate
acceptance/limitation account. No added correctness or completion benefit was
observed in this one pair. It is insufficient to establish reliability, equivalence
or overhead. Current Execute/Test already addressed this failure mode.

Artifacts and post-run hashes are retained under `tests/results/craft/`: fixture
inputs, task prompts, delivered files, run records, normalized final answers and
reviewer rerun output. Post-run hashes establish retained state, not absence of
transient changes. Instruction snapshots were collected after the runs. The
candidate additionally reconstructed its originally loaded Craft text from its
read output; raw byte identity is not independently established. A usage example
was added to the final skill during the trial and is absent from that loaded text;
core workflow wording is unchanged. The final example addition has structural
validation, not a fresh behavioral rerun. Keep this condition visible.

Lead comparison, seven other Craft cases, repeated samples, real Impeccable UI
composition and native interactive plugin invocation: **Not Run**. No task token,
speed, or cost improvement is claimed. The next useful evaluation is the
read-only/conflict/budget cases against direct specialists and current Lead,
using frozen instruction snapshots and repeated fresh contexts. Revise the skill
only where those results demonstrate a weakness.

Stored paths were subsequently normalized for publication at the user’s request;
see the [path provenance note](../tests/results/path-normalization.md). Craft’s
artifact hashes now cover normalized records. Behavioral results are unchanged.
