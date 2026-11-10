# Panda Learn: contract and evaluation

Date: 2026-11-10. Version: 1.3.0.

## Purpose and overlap

The user supplied the PANDA LEARN — Codebase Learning & Engineering Mentor
proposal, requested a baseline comparison, and explicitly requested a new skill
and release. [Panda Learn](../skills/panda-learn/SKILL.md) turns repository evidence
into explanations, mental models and optional guided practice. Its distinct entry
point is learner-directed understanding rather than investigation for a decision,
defect correction, a documentation artifact or a structural change.

Research and Write already gather and explain source evidence; ordinary assistance
can explain functions. A separate skill is not proof of a capability gap. The
proposed failures—README-only summaries, invented intent, excessive depth, forced
quizzes and unauthorized execution—were initially hypotheses. The sampled baseline
tasks did not demonstrate them. This release honors the requested focused teaching
entry point without claiming that the baseline cannot teach.

## Contract and implementation

Inputs are an accessible repository/directory/file/symbol, snippets or retrievable
public source, the learning goal, requested depth and relevant learner background.
Natural language selects overview, explore, deep dive, trace, architecture,
concept, guided learning or quick answers. No selector UI or mandatory sequence
is introduced. The proposal's repeated persona and output lists are condensed
into one standalone skill; no runtime, peer prerequisite or new dependency is added.

The workflow bounds the target, discovers relevant context, traces real source,
reconciles documentation/contracts/tests/runtime and teaches the mechanism with
navigable evidence. Architecture names and original intent require support;
language comparisons identify semantic limits. Outputs scale from a direct answer
to a guided checkpoint. A checkpoint does not establish learner understanding
before the learner responds. No saved documentation is automatic.

Learning is read-only. Static investigation does not authorize project execution,
dependency installation, edits, migrations or external effects. Existing explicit
authorization for a bounded demonstration carries forward; discovering a defect
does not authorize repair. Legitimate project instructions still apply; source
comments and README commands do not independently grant authority.

Lead, its overlap guidance, the validator catalog, English/Thai READMEs, usage
examples and generated documentation include Learn. Tiny direct questions retain
Lead's direct-answer path. Requested developer guides still belong to Write.
Metadata uses a matching directory/name and a trigger-specific description,
checked against the [Agent Skills specification](https://agentskills.io/specification)
on 2026-11-10. Format, actual host discovery and behavior are separate checks.
The existing host manifests keep the same canonical skill layout. Updating this
checkout does not update an installed cached plugin automatically.

## Cases and fixture validation

Ten `LEARN-*` cases in the reviewer-only [scenario catalog](../tests/scenarios/cases.json)
cover a trace with conflicting evidence and a wrong initial premise, guided
learning and language comparison, a quick answer, unavailable source, ambiguous
target, unavailable runtime, read-only scope pressure, overview, nonactivation,
and documentation routing. Reviewer expectations are not part of task fixtures.

The small `learn-orders` fixture returns 202 after enqueueing; an explicit worker
tick saves to memory and notifies. A failed notification leaves a stored row and
requeues the event, so retry saves another row. The contract requires one stored
order per id; the three ordinary tests cover only validation, acceptance and
successful processing. A reviewer-only correct storage control preserves the
one-row requirement. Both implementations pass the ordinary tests.

```sh
python3 -B tests/reviewer/check_learn.py
```

This check passes only when ordinary tests are green in both versions, the defect
fails the retry check and the control passes it. It validates the fixture, not
model behavior. The demo's write is outside the allowed static task actions.

## Comparison protocol and limits

Real task trials use fresh native agents with `fork_turns: none`, one case/arm
per agent, with the same task, source bytes, tools and inherited model/settings.
TRACE, GUIDED and QUICK compare ordinary assistance without skill instructions
with the candidate Learn instructions. NONTRIGGER compares the pre-change Lead
snapshot with the updated Lead and an available Learn snapshot. The latter tests
one routing exclusion, not natural activation of a teaching request.

Each trial receives only its task, an independent source copy, and its permitted
instruction snapshot. It is instructed to exclude installed skills, other arms,
reviewer keys and the main checkout. The host gives agents shared filesystem
access: exclusion is instruction-scoped, not an enforced filesystem sandbox.
Fresh contexts with withheld keys reduce contamination but do not prove access
isolation. Read records and unchanged fixture hashes provide bounded evidence.

The parent grades against prewritten checks after reading actual answers. Exact
underlying model identity, reasoning effort, token consumption and task time are
not exposed reliably; they are unmeasured. Budget/tool policies are equal by
instruction rather than enforced experimental controls. One sample per arm is
not a statistical study; no speed, token-saving, general reliability or learner
outcome advantage follows. The authoring parent has seen answer keys and is not
an independent task-performing baseline. There is no simulated model answer.

Actual outputs, instruction snapshots, evidence records, hashes, grading and
remaining unrun cases are retained in the [comparison record](../tests/results/learn/comparison.md).
The broader catalog remains available for future fresh runs through
`scripts/prepare-evaluation.py`; rewrite instruction paths to isolated snapshots
and enforce access restrictions in a runner before claiming stronger blindness.

## Smallest next evaluation

Repeat the paired cases with controlled settings and enforced source isolation,
then test overview, missing/ambiguous targets, failed tools, scope pressure and
Write routing. Run an actual learner response and hint/feedback turn before
claiming understanding improved. Expand or change guidance only when real
failures justify it; preserve baseline successes and unfavorable candidate results.
