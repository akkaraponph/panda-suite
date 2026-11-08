# Panda Research addition

Date: 2026-11-08.

## Purpose and contract

The user requested a standalone engineering research skill after considering its
boundary with Brainstorm, Impact, and Write. The target failure modes are treating
an unsupported premise as fact, applying the wrong documentation version,
equating repository configuration with deployed behavior, and hiding uncertainty
behind a plausible summary. These are design hypotheses for this addition, not
failures measured in a baseline run.

[Panda Research](../skills/panda-research/SKILL.md) answers bounded engineering
questions from repository evidence, official documentation, specifications, and
papers. Inputs are the question, decision, versions, sources, constraints, and
desired output. The workflow bounds the question, gathers primary evidence,
checks premises and contradictions, synthesizes cited findings, and checks that
each deciding claim is supported or explicitly unresolved.

Outputs are a direct answer, findings with citations, uncertainty, and decision
implications. Requested notes follow project conventions; small answers need no
file. Research remains read-only except for requested artifacts. Experiments,
installation, implementation, external data sharing, publication, and deployment
require authorization covering the action. No peer skill or runtime is required.

Brainstorm owns exploring directions; Debugger owns causal defects; Impact owns
dependencies of a proposed change; Write owns developer documentation. Ordinary
evidence gathering remains inside each existing workflow. A focused explanation
does not require research. Lead has both a direct research route and overlap rules.

## Implementation and discovery

The new directory uses matching name/description YAML frontmatter and Markdown
instructions, checked against the [Agent Skills specification](https://agentskills.io/specification)
on 2026-11-08. The existing canonical `skills/` discovery layout and manifests
are retained. The validator catalog, English/Thai README catalogs, usage guide,
Lead route, and scenario catalog include Research, bringing the suite to seventeen
skills. This changes the checkout; it does not update an installed cached plugin.

## Evaluation protocol

The reviewer-only [scenario catalog](../tests/scenarios/cases.json) defines nine
`RESEARCH-*` cases: capability, conflicting evidence, missing deployment access,
ambiguity, unavailable live tools, wrong premise, authorized note, analysis-only
scope, and nonactivation. The synthetic local fixture contains versioned SDK
references, application configuration, and an unsupported team claim. It does not
represent a real provider or require network access.

Prepare each case and arm into a new directory with the existing utility:

```sh
python3 scripts/prepare-evaluation.py --case RESEARCH-CONFLICT --arm baseline --destination /tmp/panda-research-conflict-baseline
python3 scripts/prepare-evaluation.py --case RESEARCH-CONFLICT --arm specialist --destination /tmp/panda-research-conflict-specialist
python3 scripts/prepare-evaluation.py --case RESEARCH-CONFLICT --arm lead --destination /tmp/panda-research-conflict-lead
```

Give task agents only the prepared fixture/TASK.txt and relevant skill instructions,
with no access to the reviewer catalog, this evaluation discussion, or other arms.
Use fresh contexts with comparable model/settings, tools, access, and budgets per
case/arm. For `RESEARCH-NONTRIGGER`, compare baseline and Lead routing; forcing
Research would defeat the nonactivation check. Save actual answers, actions,
loaded paths, artifacts, and exposed settings. Score claim correctness, citation
support, version/freshness handling, contradictions, uncertainty, scope, completion,
and usefulness using the [evaluation guide](../tests/evaluation.md).

## Results and limits

Checks run for this addition:

| Check | Actual result |
| --- | --- |
| `.venv/bin/python scripts/validate-skills.py` | Passed: seventeen skills, local references, manifests, and scenario coverage |
| `python3 scripts/vendor-upstreams.py` | Passed: pinned upstream hashes unchanged |
| `python3 tests/check_codex_discovery.py` | Passed on Codex CLI 0.159.2: all seventeen skills, including Research, discovered through portable plugin and temporary standalone repository |
| Disposable fixture preparation | Passed: all nine cases prepared for three arms, twenty-seven workspaces; prompts match catalog tasks and reviewer catalog is excluded |
| Standalone Research copy | Passed: only the requested skill copied, with identical instruction bytes |
| Tooling unittest suite | Twenty-three passed, one failed: `test_restore_refuses_modified_upstream` |
| Untouched `git archive HEAD` reproduction | The same restore test fails before this addition; it mutates the adapted Debugger skill rather than the pinned vendor file checked by restore. No unrelated test or vendor behavior was changed |
| `git diff --check` | Passed |

Baseline and skill behavioral runs: **Not Run**. No independent task-performing
model trials were launched for this addition. Comparative benefit, routing
reliability, elapsed model time, and token overhead are unmeasured. Prepared
fixtures and structural/discovery checks do not establish behavioral improvement.
Live web research and interactive plugin invocation remain untested. The smallest
useful next evaluation is an isolated baseline/specialist pair for
`RESEARCH-CONFLICT`, followed by the Lead nonactivation case.
