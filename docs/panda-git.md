# Panda Git: contract and evaluation

## Purpose and evidence

The supplied proposal asks for a distinct Git capability: classify actual changes,
apply Conventional Commits by default, separate review from execution, and preserve
repository safety. Existing Refactor, Craft and Release do not own that full workflow.
The proposal hypothesizes generic feat/fix selection and unsafe commits; it does not
provide an observed incident proving those failures. Trials below retain both the
successful baseline and an initial skill failure.

## Contract

`panda-git` discovers Git inspection, commit messages/execution, branching,
conflicts, history and recovery requests. Ordinary coding, explanation and release
readiness remain outside its primary trigger. Inputs are the repository or supplied
diff, intended paths/revisions, conventions, operation and current authorization.
Missing access or ambiguous scope yields a bounded proposal or a targeted question.

The entrypoint routes to four local references: inspection, commit conventions,
conflicts, and history/recovery. The proposed seven-reference tree is consolidated
to avoid tiny overlapping files. No runtime or inspection wrapper is introduced;
ordinary read-only Git commands already provide that capability. A short README
documents the user-requested invocation modes. A standalone copy works without Lead.

User conventions outrank repository conventions, then the default. Panda defaults
add a 100-character line maximum, preferred 72-character header, lowercase imperative
subject and both breaking markers. These are distinguished from the upstream
[Conventional Commits specification](https://www.conventionalcommits.org/en/v1.0.0/).
Metadata and folder structure follow the
[Agent Skills specification](https://agentskills.io/specification).

Outputs distinguish proposed, executed and verified operations. Review shorthand
is proposal-only; an explicit execution request, including existing conversational
authorization, permits the scoped commit without repeated approval. Separate push,
rewrite, tag and release authorization is retained. Inspect exact index content,
preserve unrelated staging/edits, exclude secrets and run normal hooks. Report
actual checks and blockers rather than claiming unobserved success.

Lead routes Git requests. Craft, Refactor and Execute optionally load this guidance
at their Git boundary, while retaining local safety and an unavailable-peer fallback.
There is no mandatory dependency or pretend programmatic skill invocation.

## Cases and protocol

Twelve `GIT-*` cases in `tests/scenarios/cases.json` cover breaking-change
classification, review, execution, mixed staging, repository convention override,
unverified issue references, failed hooks, missing evidence, unavailable tools,
remote ambiguity, recovery and nonactivation. Reviewer expectations remain outside
the fixture. Prepare baseline/specialist/Lead workspaces using the existing
`scripts/prepare-evaluation.py`; read only TASK.txt in a fresh task context.

The synthetic fixture's setup.py creates a new child repository on explicit request.
It stages removal of a public option, leaves an unrelated README draft unstaged,
and includes a green ordinary test that misses the removed caller contract.
`python3 -B tests/reviewer/check_git.py` independently verifies the violation and a
compatible original control. That check establishes fixture behavior, not agent quality.

Use a fresh context per case and arm, equivalent tools/model/settings/budget and
frozen inputs. Save actual answers, loaded instruction paths, commands/outcomes,
source/index/ref state and authorized artifacts. Task agents must not receive the
catalog's reviewer checks or this analysis. Compare correctness, scope, evidence,
completion and honest verification; measure cost only where the host exposes it.

## Actual results and limits

See [trial record](../tests/results/git/comparison.md) for the baseline, initial
specialist defect, revision and fresh-context regression. All other behavioral
cases and a Lead-routed behavior comparison are **Not Run**. One observed pair
cannot establish reliability, repeatability, token savings, speed or overall benefit.
Skill format and static host discovery do not prove interactive activation.
