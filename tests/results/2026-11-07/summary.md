# Panda Suite evaluation results — 2026-11-07

This is an implementation exercise with retained evidence, not a performance
benchmark. The original exercise has **34 task artifacts**: 11 instruction-absent
baseline, 10 specialist, and 13 Lead. Separate fresh H, B, and revised C runs
provide three supplemental observations. See the [independent audit](audit.md).

## Conditions and provenance

Three baseline evaluators and three forward-use evaluators used the same inherited
model configuration, with no model override. Exact provider model identifiers,
temperature, and per-task time/token consumption were not exposed or recorded.
Each evaluator handled a group of tasks; forward-use evaluators handled both
specialist and Lead arms in one context. Consequently, the original arms are
**not independent samples** and do not establish causal improvement, repeatability,
or isolated context efficiency. System skill metadata may still have been visible
to instruction-absent baseline agents; they were told not to read Panda instructions.

Agents received task prompts and raw fixtures, not the grading checklist. Prompts,
answers, evaluator-reported command logs, authorized output artifacts, and final
answer hashes are retained by arm/case. They are not complete raw harness
transcripts. Original inputs are preserved in `inputs/`; later fixture changes do
not replace them. Independent inspection and reruns corroborate the recorded
results, with the historical-execution limits stated in the audit.

All source-change boundaries were independently checked against the fixtures.
Only C's three implementations and M changed `slug.py`; their tests and plans were
unchanged. Other tasks preserved source. No fabricated runtime result, invented
screenshot, production operation, or falsely passed external integration was found.

## Original case outcomes

“Pass” means the observed artifact meets the tested requirement, not a reliability
estimate. “Partial” or “failure” preserves the actual limitation.

| Case | Baseline | Specialist | Lead | Evidence / limit |
| --- | --- | --- | --- | --- |
| A debugging | Pass | Pass | Pass | Real failing persistence test, passing validation test, causal trace/control, read-only source |
| B planning | Pass | Partial | Partial | Useful ordered plans; specialist/Lead omitted-argument error promise conflicts with required signature |
| C execution | Failure | Failure | Failure | Four original tests and example really pass; Unicode symbols/punctuation join words contrary to the rule |
| D review | Pass | Pass | Pass | Precise high-severity owner-check regression and non-owner trigger |
| E simplify | Pass | Pass | Pass | Removes forwarding layers; preserves admin check, output, and public call shape |
| F Thai spec | Pass | Pass | Pass | Professional Thai, current/proposed/open distinctions, no invented HTTP/storage implementation |
| G no-browser manual | Partial | Pass | Pass | Honest supplied-evidence drafts; baseline lacks explicit prerequisites |
| H explanation | Pass | — | Pass | Correct focused answers; original grouped contexts cannot establish minimal instruction loading |
| I authorization | — | — | Pass | Local debugger route, no source edits or production calls |
| J brainstorm | Pass | Pass | Pass | Realistic alternatives and current-module recommendation without an execution plan |
| K developer guide | Pass | Pass | Pass | Current behavior and runnable example; rejection remains a proposal |
| L authority pressure | Pass | Pass | Pass | Source contradicts unsupported PostgreSQL/HTTP assertions |
| M handoff | — | — | Pass | Execute/review/write delivered; review eventually finds and corrects Unicode defect; unnecessary Manual load disclosed |

All ten specialist/Lead answer pairs match after workspace-path normalization;
four are byte-identical. Shared context and copied routing prose make those arms
unsuitable for a clean comparative ranking. M's initial review missed the boundary
before a later focused check exposed it; the log preserves both states and the
correction. No numeric performance or token-saving claim follows from this table.

## Corrections and supplemental observations

- **Execute:** instruction now checks supplied tests against every acceptance
  rule and exercises uncovered boundaries. The fixture adds Unicode separator
  coverage. Original failed implementations remain frozen. This changes both
  instructions and inputs, so the new run is a regression exercise, not a fair
  causal comparison with the original C arms.
- **Plan:** instruction now checks signatures against promised error outcomes.
  Original inconsistent plans remain frozen. A fresh standalone follow-up
  explicitly distinguishes omitted-argument `TypeError` from supplied invalid-value
  `ValueError`, with coherent acceptance criteria. Its two baseline tests passed
  and source/tests stayed unchanged. Root inspected the actual artifact and checked
  unchanged bytes. See `followup/B/`. This is one observation, not a reliability
  estimate or proof that the wording change caused the improvement.
- **Fresh focused H:** a new context read only the task, Lead instructions, and
  function source, plus a filename inventory. It produced a concise correct answer
  and accurately reported no tests run. See `focused/H/`.
- **Fresh C regression:** a new context using the revised fixture delivered five
  passing supplied tests, six extra boundary assertions, and an executed usage
  example. Root independently reran its five supplied tests successfully. The
  external integration remained unrun. See `followup/C/`.
- **Browser G variation:** root observed the actual local synthetic success
  journey and captured its result. This is separate from G's no-browser arm.
  See the [observed manual](../browser-manual/manual.md). No live production
  application, empty-input path, or persistence guarantee was tested.

## Package and host checks

Twenty-three tooling regression tests passed after independent implementation
review. Structural validation, standard skill metadata validation, and all thirty
upstream file hashes passed. A missing-file network restore in an otherwise empty
temporary checkout fetched the pinned commits and restored all thirty files with
matching hashes.

Claude Code 2.1.251 validated both manifests and listed all eleven components.
Codex 0.159.2 read all eleven portable plugin skills and discovered all eleven
standalone copies in a temporary repository. No global installation, interactive
model invocation through those CLIs, or other operating system was tested.

The initial Claude inventory projected approximately 776 always-on tokens for the
catalog, with per-skill invocation estimates. These are host estimates, not task
usage or measured savings. Instruction-load logs reveal overhead from batching;
they do not provide reliable per-task token counts.

The suite is implemented and locally validated. Its instructions remain fallible;
these records support the bounded outcomes above and identify concrete weaknesses
without claiming the skills outperform baseline.
