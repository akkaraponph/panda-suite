# Evaluation guide

Separate structural correctness, host discovery, and useful task behavior. A valid
SKILL.md is not proof of a better model response. This suite has no custom model
runner or orchestration service.

## Structural and host checks

Run the commands in the root README. The tooling tests mutate temporary package
copies to check YAML parsing, duplicate keys, naming, reference boundaries,
manifest consistency, missing skills, vendor drift, blind-fixture preparation,
and collision-safe installation. Intentionally defective fixtures are not part of
the default tooling test discovery.

`tests/check_codex_discovery.py` uses the installed CLI's generated app-server
protocol to read the local portable plugin and list copied skills in a temporary
Git repository. It does not install a plugin globally or start a model task.
Claude's `plugin details` command similarly verifies component discovery.

## Functional cases

`scenarios/cases.json` contains reviewer expectations. **Do not give that file to
the task-performing agent.** `prepare-evaluation.py` copies only the chosen fixture
and writes its task prompt:

```sh
python3 scripts/prepare-evaluation.py --case B --arm baseline --destination /tmp/panda-case-B-baseline
python3 scripts/prepare-evaluation.py --case B --arm specialist --destination /tmp/panda-case-B-specialist
python3 scripts/prepare-evaluation.py --case B --arm lead --destination /tmp/panda-case-B-lead
```

Use new destinations; existing workspaces are never overwritten. Baseline receives
no skill instructions. Specialist and Lead prompts identify instructions to load
through the host; this is not a fake programmatic invocation.

| Case | Capability |
| --- | --- |
| A | Debugging an intentionally uncommitted transfer |
| B | Planning manager rejection against existing source |
| C | Executing dependent slug implementation/documentation tasks |
| D | Review of an authorization regression plus formatting change |
| E | Simplification preserving access control |
| F | Thai specification with current/proposed/open distinctions |
| G | Manual from supplied evidence without browser access |
| H | Focused explanation without a project workflow |
| I | Investigation-only payment boundary |
| J | Brainstorm alternatives without premature implementation |
| K | Accurate developer guide and executable example |
| L | Verify an authoritative but unsupported technical claim |
| M | Authorized execute/review/write handoff |

For a browser-enabled G variation, serve the local synthetic manual fixture and
observe its actual UI using available browser tools. Keep no-browser and observed
runs separate. A saved [observed manual](results/browser-manual/manual.md) shows
the bounded journey and actual capture.

The [Write refinement](../docs/panda-write-refinement.md) adds six `WRITE-*` cases
for per-integration accuracy, review-only scope, conservative updates, missing
deployment evidence, unavailable execution tools, and nonactivation.

## Run and score fairly

The [Research addition](../docs/panda-research.md) documents nine `RESEARCH-*`
cases, their synthetic local fixture, comparison protocol, and current Not Run
behavioral status. Their reviewer expectations remain in the scenario catalog.

Use a fresh context **per case and arm**, the same model/settings, inputs, tools,
budget, and external-access restrictions. Keep the task agent blind to expectations,
root-cause answers, other arms, and prior outputs. Record unavailable model settings.
Copy only fixtures, not the whole Suite repository, into task workspaces.

Save each final answer and actual command/tool evidence, loaded instruction paths,
source hashes before/after, and authorized output artifacts. A human or independent
reviewer should compare the answer with source and actual outcomes. Re-run delivered
implementations and examples; hashes show final-state boundaries, not absence of
transient historical changes. Task-agent summaries are not raw harness transcripts.

Rate each dimension as observed pass, partial, failure, or not applicable, with a
short evidence note:

- Correctness against all acceptance rules, including uncovered boundaries.
- Evidence quality and current/proposed distinctions.
- Completion of the requested artifact or work.
- Scope and authorization compliance.
- Verification honesty, especially failed and unrun checks.
- Usefulness for the intended reader.
- Routing/context overhead from actual loaded instructions, where observable.

Record elapsed time and token/context data only if the host exposes them. Distinguish
Claude's projected inventory token estimate from measured task consumption. Do not
infer savings from word counts. Do not invent numeric scores for dimensions that
were not observed. Preserve unfavorable results.

The bundled debugger's original evaluation rubric and answer key are archived at
`skills/panda-debugger/tests/evaluation.md`; its runnable fixtures deliberately
fail. Their failure is expected fixture behavior, not a Suite tooling regression.

The first exercise used grouped shared contexts and therefore cannot establish
causal improvement or independent repeatability. See the
[summary and independent audit](results/2026-11-07/summary.md). Subsequent runs
must label changed fixture inputs or revised instructions rather than silently
replacing earlier failures.

## v1.1.0 additions

Six `SEC-*` cases and six `PERF-*` cases cover positive findings, effective guards,
placeholders, stale/withdrawn advisories, failed scans, complexity and semantic
invariants, memory retention, N+1 batching, plan interpretation, unavailable tools,
applied optimization, and nonactivation. See [actual trial results and limits](../docs/v1.1.0.md).

## Lead recommendation refinement

The motivating conversation showed three response weaknesses: drafting a broad
partner skill before checking overlap with Lead, giving a finished draft during
idea exploration, and substituting another speculative skill after a challenge.
These are observed conversation outcomes, not controlled evidence that Lead's
instructions caused them. The refinement clarifies requested deliverable depth,
existing-coverage checks, and reassessment in Lead and its routing reference.

`LEAD-COVERAGE`, `LEAD-IDEAS`, and `LEAD-CHALLENGE` exercise those boundaries using
the synthetic `lead-recommendations` fixture. `LEAD-CREATE` guards against
overcorrection: an explicit artifact request still authorizes scoped creation.
Existing H and `EXP-LAB-NONTRIGGER` remain focused-question controls. Reviewer
expectations stay in `scenarios/cases.json`; task workspaces receive only the
fixture and prompt through `prepare-evaluation.py`.

Prepare baseline and Lead arms in fresh destinations using the existing protocol.
Compare original and revised Lead in separate fresh contexts with frozen fixture,
prompt, specialist versions, access, model/settings, and budget. Keep original
outputs and instruction snapshots. Check actual file changes for the creation and
read-only cases; grade recommendation quality against the supplied catalog rather
than requiring identical phrasing. The synthetic catalog is not a runtime plugin
inventory and does not prove host discovery.

Behavioral baseline, original/revised Lead comparison, and benefit measurements:
**Not Run**. The current authoring context has seen the reviewer expectations and
cannot serve as an independent task run. Structural checks and blind-workspace
preparation validate packaging only; they do not establish behavioral improvement.

Local checks on 2026-11-09: `.venv/bin/python scripts/validate-skills.py`
validated all 19 skills, references, manifests, and scenario coverage;
`.venv/bin/python -m unittest discover -s tests -p 'test_tooling.py' -v`
passed all 27 tests. A temporary preparation check exercised all four new cases
in baseline and Lead arms (eight workspaces), confirmed exact task prompts, and
confirmed only `capabilities.md` and `TASK.txt` were copied, excluding reviewer
keys. No model tasks or global installation were performed.

## Refactor candidate

The [Refactor design and protocol](../docs/panda-refactor.md) documents nineteen
new cases, paired green-suite controls, standalone/peer/routed arms and controlled
existing-workflow comparison. Reviewer checks live outside task fixtures:
`python3 -B tests/reviewer/check_refactor.py`. Local fixture validation is not a
model evaluation. All comparative behavioral arms remain **Not Run** until real
fresh-context trials with isolated inputs and recorded settings are available.

## Learn candidate

Ten `LEARN-*` cases exercise evidence-backed codebase teaching, guided checkpoints,
language comparisons, quick answers, inaccessible/ambiguous targets, runtime gaps,
read-only pressure, overview and routing exclusions. The
[Learn contract and protocol](../docs/panda-learn.md) separates fixture validation,
host discovery and actual model comparisons. Correct controls and reviewer keys
live outside task fixtures. Validate the uncovered retry requirement locally with
`python3 -B tests/reviewer/check_learn.py`; green ordinary tests are deliberately
insufficient to establish that requirement. See [actual trial answers and limits](results/learn/comparison.md).

## Craft composition

Eight `CRAFT-*` cases cover selected-specialist delivery, read-only investigation,
missing skills, green-suite contract gaps, conflicting requirements, unavailable
tools, exhausted specialist verification budgets, and nonactivation. See
[Craft contract and actual results](../docs/panda-craft.md). Reviewer-only
`reviewer/check_craft.py` distinguishes the faulty green-suite fixture from the
correct control and stays outside prepared task workspaces. Run cases in fresh
contexts; retained direct-specialist and Craft trial artifacts are a small
observation, not a reliability or improvement estimate.
