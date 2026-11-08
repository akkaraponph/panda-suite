# Panda Write refinement

Date: 2026-11-08.

## Evidence and design

The user requested adapting ideas from the local standalone `panda-write` project.
Its `SKILL.md` and `README.md` were inspected at clean revision
`8cf10e834e24d93332a592f5bdd1b459fbae265c` in
`/Users/akkaraponph/Workspaces/codespaces/panda-write`. That repository was read
only. Its independent integration tracing, evidence categories, uncertainty
handling, Thai technical prose, and engineering document structure informed this
revision. The Suite instructions were adapted rather than copying the full README;
the standalone project is not a new pinned vendor snapshot.

The previous Suite skill already required evidence, safe example checks, and
current/proposed distinctions. Instruction inspection identified these gaps:

| Earlier instruction | Refinement |
| --- | --- |
| Generic evidence gathering | Trace entry points and each feature/integration independently |
| Current/proposed/unknown distinction | Separate implementation, configuration, deployed state, external contracts, and confirmed requirements |
| General missing-evidence handling | Continue verified sections; mark precise facts `Pending Confirmation` with needed evidence and no guessed behavior |
| Create/maintain documentation | Explicit review-only findings and conservative updates respecting language, sections, and supported content |
| General diagrams advice | Verify traced paths and distinguish logical relationships from physical deployment |
| Generic section list | Conditional skill-local section menu for substantial architecture, integration, and handover documents |

These are observable instruction gaps and proposed remedies, not independently
observed behavioral failures or proof of improvement. Broad claims about lower
token use or higher accuracy would be unsupported.

## Contract and boundaries

Inputs remain audience, purpose, language, destination, sources, and conventions.
Write owns current-system documentation, maintenance, and document review.
Spec owns proposed contracts/design; Manual owns user journeys; Research owns
standalone investigation. Focused explanations need no documentation workflow.
English and Thai remain supported. Requested or existing language takes precedence;
otherwise the Suite's clear-English default remains. The standalone project's
Thai-only default and full specification outline were not imposed on every guide.

The workflow gathers evidence, chooses scope and structure, drafts or reviews,
verifies, and refines. Outputs are the requested artifact or located findings,
source anchors, actual verification, and precise gaps. Review alone authorizes no
edits. Documentation work preserves application source unless separately requested.
Requested artifacts, existing scope, and external-action authorization carry
forward. Essential instructions remain local to the skill; the new reference is
only loaded for substantial engineering documents.

The matching directory/frontmatter format follows the
[Agent Skills specification](https://agentskills.io/specification), checked during
the Research addition on the same date. Existing `skills/` host discovery is retained.

## Blind scenarios and comparison

Six `WRITE-*` cases in the reviewer-only scenario catalog cover normal Thai
handover, conflicting document claims/review-only permission, conservative English
updates, missing deployment evidence, unavailable execution tools, and a focused
explanation that should bypass Write. The synthetic fixture has two deliberately
different local integration paths, unsupported documentation, and an established
template. No real provider, credentials, runtime, or network is needed.

Prepare new workspaces with the existing tool, for example:

```sh
python3 scripts/prepare-evaluation.py --case WRITE-REVIEW --arm baseline --destination /tmp/panda-write-review-baseline
python3 scripts/prepare-evaluation.py --case WRITE-REVIEW --arm specialist --destination /tmp/panda-write-review-specialist
```

Task agents receive only prepared fixture/TASK.txt and relevant instructions,
without the reviewer catalog, this report, or other answers. Use fresh contexts
per arm, comparable model/settings, access, tools, and budgets. Save answers,
actions, loaded paths, and artifacts. Score per-feature correctness, evidence
boundaries, citations, precise uncertainty, language/template preservation,
verification honesty, and scope. For `WRITE-NONTRIGGER`, compare baseline and Lead
rather than forcing Write. Case K remains the English short-guide regression.

Baseline/revised behavioral comparison: **Not Run**. No independent model trials
were launched. Instruction changes address inspected gaps; their effect on task
quality and context consumption is unmeasured. The smallest next trial is an
isolated comparison on `WRITE-REVIEW`, followed by K and the nonactivation case.

## Actual verification

| Check | Result |
| --- | --- |
| Suite structural validator | Passed: seventeen skills, metadata, references, manifests, and scenario coverage |
| Pinned upstream integrity | Passed; source snapshots unchanged |
| Codex CLI 0.159.2 discovery | Passed: all seventeen skills through portable plugin and temporary standalone repository |
| Blind workspace preparation | Passed: twenty-one case/arm workspaces for six new cases plus K; reviewer catalog excluded and prompts preserved |
| Standalone Write installation into a temporary directory | Passed: skill and conditional reference copied identically, local links resolve without peers |
| Tooling unittest suite | Twenty-three passed; existing `test_restore_refuses_modified_upstream` failure remains. It was reproduced on untouched HEAD during the preceding Research addition |
| Diff whitespace check | Passed |

These checks verify packaging and evaluation preparation, not generated document
quality. Installed plugin cache, standalone source project, and global settings
were not updated.
