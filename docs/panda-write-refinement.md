# Panda Write refinement

Date: 2026-11-08.

## Evidence and design

The user requested adapting ideas from the local standalone `panda-write` project.
Its `SKILL.md` and `README.md` were inspected at clean revision
`8cf10e834e24d93332a592f5bdd1b459fbae265c` in
`../panda-write`. That repository was read
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

## Ask-first and document prose (2026-11-12)

User-reported failure: drafts filled unknown facts or unrequested content instead
of asking, and placed conversational absence/contrast sentences ("There is no X,
but there is Y") in the finished document. Earlier text said to ask only when an
answer was necessary and otherwise mark `Pending Confirmation`, which defaulted
toward writing through gaps.

| Change | Instruction |
| --- | --- |
| Named source of truth | Each section comes from code, a user-referenced source, or the user's answer |
| Ask first | Ask before drafting when source, scope, audience, content, or a material fact is unclear or conflicting |
| Gaps | `Pending Confirmation` only when the user authorized continuing or the answer is known to be unavailable |
| No extras | Ask before adding sections, examples, features, recommendations, or background beyond the sources |
| Prose | No absence/contrast narration in the document; material absences as plain facts; gaps reported in the reply |

New blind cases: `WRITE-ASK-SOURCE`, `WRITE-ASK-UNKNOWN`, `WRITE-EXACT-CODE`.
Existing `WRITE-MISSING`, `WRITE-UPDATE`, and `WRITE-THAI-PATHS` authorize or
establish unavailable gaps, so they keep the `Pending Confirmation` path.
Behavioral baseline/skill comparison: **Not Run**.

### Evaluation (2026-11-12)

Arms: `old` = `SKILL.md` at `d27c10a`; `new` = this revision. One fresh Sonnet
subagent per case/arm, workspaces from `scripts/prepare-evaluation.py`, answer
keys withheld. Single turn, so asking ends the run. One sample per arm, so
model variance is not controlled.

| Case | old | new |
| --- | --- | --- |
| `WRITE-ASK-SOURCE` | Wrote README.md, chose code over guide.md and imported Operator notes without asking | Asked which source of truth; named the three conflicts; no file |
| `WRITE-ASK-UNKNOWN` | Edited guide.md with "do not implement rate limiting: there is no throttling... This is a retry count, not a rate limit" | Asked for the rate-limit source; guide.md unchanged |
| `WRITE-EXACT-CODE` | Proceeded; added secret-store advice, "reads no files...", "does not validate", Scope and limits section, invented Pending items | Proceeded; tighter, but kept a "Limits of this document" section with absence prose |
| `WRITE-MISSING` (regression) | Continued with Pending Confirmation, no file changes | Same; no blocking question |

After adding the Refine rule that deletes "limits/not covered/does not define"
notes, two reruns of `WRITE-EXACT-CODE` (new) produced no limits section and
reported transport gaps in chat. Both still added a placeholder `export` example;
one added "Keep the value secret".

## Saved output under `.panda-suite/docs/` (2026-11-12)

Request: save new documents under `.panda-suite/` like Panda Spec, support
user-requested `.docx`/`.pdf`, and keep outputs out of commits because exports
can be large. Earlier instructions named no default destination, so new guides
landed at the project root or only in chat.

Contract: new documents go to `.panda-suite/docs/YYYY-MM-DD-<topic>.<ext>`;
Markdown by default, requested exports kept beside their Markdown source;
convert only with existing tools and ask before installing; explicit path,
in-place update, and chat-only requests take precedence; never stage or commit
`.panda-suite/` output or edit ignore files unasked; say when Git would track it.
Ignoring `.panda-suite/` stays the user's decision.

Evaluation: same method as above, old = `9c53436`. `WRITE-SAVE-GIT` workspaces
were initialized as Git repositories with the fixture committed and no ignore file.
No docx/pdf converter (pandoc, python-docx, LibreOffice) was installed on the host.

| Case | old | new |
| --- | --- | --- |
| `WRITE-SAVE-DEFAULT` | `integrations-guide.md` at root | `.panda-suite/docs/2026-11-12-integrations-guide.md` |
| `WRITE-SAVE-DOCX` | `integrations-handover.docx` at root, hand-built from stdlib XML, no Markdown source | `.docx` (via macOS `textutil`) plus `.md` source in `.panda-suite/docs/`; no installs |
| `WRITE-SAVE-PATH` | `docs/integrations.md` only | Same |
| `WRITE-SAVE-GIT` | Guide in chat only; asked where to save | Saved in `.panda-suite/docs/`; index and history unchanged; ignore files untouched; reported Git would track `.panda-suite/` |
| `WRITE-UPDATE` (regression) | Edited `guide.md` in place | Same; nothing created under `.panda-suite/` |

Observed weakness: in the non-Git default case the new arm still advised adding
`.panda-suite/` to an ignore file without checking Git. The docx run also used
`template.md` and listed deployment and encryption as Pending items although the
user named only the code as source. One sample per arm.

## DOCX template fidelity and punctuation (2026-11-12)

Requested addition: when a user names or supplies a DOCX template or example,
preserve its formatting standards in the output, including font, size, color,
weight, hierarchy, spacing, layout, and page furniture where present. Treat it as
a formatting reference, not factual evidence unless the user says otherwise. If
the template cannot be read or its styles cannot be reproduced, disclose the
constraint and limit the result to verifiable formatting. Avoid the em dash
character in authored prose.

Added `WRITE-DOCX-TEMPLATE` with a synthetic DOCX fixture whose styles specify
Arial, title 18 pt bold dark blue, Heading 1 14 pt bold dark blue, body 11 pt dark
gray, 1.15 line spacing, paragraph spacing, and one-inch page margins. The blind
case checks DOCX style fidelity, Markdown source delivery, and that template
content is not used as factual evidence. Behavioral baseline and
skill comparison: **Not Run**. The workspace has no model-runner evaluation;
fixture preparation and structural validation do not establish model behavior.

## PM and Tech Lead writing register (2026-11-13)

The user asked for writing that sounds like a product manager, project manager,
or Tech Lead: easy to understand, academically careful, and free of AI-style
filler. The skill already required professional Thai, direct prose, and factual
support, but did not define this reader-oriented register or distinguish it from
adding a management persona or unsupported decision framework.

Added a concise drafting rule: state status or decision, evidence, impact,
dependencies, and next action when relevant; connect conclusions to evidence;
define terms; prefer concrete verbs; remove filler and slogans; add role-oriented
sections only when requested and supported. This applies to style while preserving
the skill's evidence and scope requirements.

Added blind case `WRITE-VOICE`, which asks for a Thai status note from the existing
integration fixture. It checks reader fit, separate path descriptions, useful
impact and evidence gaps, restrained recommendations, and concise evidence-linked
language. The reviewer-only checks stay in `tests/scenarios/cases.json`.

Behavioral baseline/skill comparison: **Not Run**. The repository has no model
runner; the scenario is runnable through the existing preparation script. This
change is a testable style contract, not evidence that generated prose improved.
Next justified step: run `WRITE-VOICE` in fresh baseline and specialist contexts
with the same model, tools, and budget, then compare artifact text against the
blind checks. The required `RTK.md` referenced by workspace instructions was not
present in the workspace or its checked ancestors.
