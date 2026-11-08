# The right skill for the work ahead.

Panda Suite gives your coding agent focused instructions for the whole engineering journey. Explore an idea, investigate a bug, review a change, or write the guide your team needs.

Start with **Panda Lead** when you want help choosing a workflow. Go straight to a specialist when you know the task.

[Get started](installation.html) · [Browse the skills](skills.html)

## Your first request

Install the suite, open the project you want to work on, and select a skill in your agent. These examples use the **Codex plugin** names.

```text
$panda-suite:panda-lead Explain how authentication works in this project.
Use the source as evidence. Do not change files.
```

For a focused task, call the specialist directly:

```text
$panda-suite:panda-review Review the current diff for material defects.
Explain the trigger, impact, and location of each finding. Do not fix code.
```

Using Claude Code or standalone skills? See the [invocation reference](usage.html#invoke-a-skill).

## Choose the task, then the skill

| You want to… | Start here |
| --- | --- |
| Work out what to build | [Brainstorm](panda-brainstorm.html) or [Requirements](panda-requirements.html) |
| Check a technical claim | [Research](panda-research.html) |
| Understand what a change affects | [Impact](panda-impact.html) |
| Turn agreed work into tasks | [Plan](panda-plan.html) |
| Define a technical contract | [Spec](panda-spec.html) |
| Implement an authorized change | [Execute](panda-execute.html) |
| Investigate unexpected behavior | [Debugger](panda-debugger.html) |
| Check correctness and complexity | [Review](panda-review.html), [Test](panda-test.html), or [Simplify](panda-simplify.html) |
| Explain the system to others | [Write](panda-write.html) or [Manual](panda-manual.html) |
| Prepare a release handoff | [Release](panda-release.html) |
| Create or improve a skill | [Skill Lab](panda-skill-lab.html) |

## Give the agent a useful brief

Include the outcome, relevant files or URLs, constraints, and whether edits are allowed. Replace example paths with files in your own project.

```text
$panda-suite:panda-write Write docs/approvals-guide.md for new developers.
Use src/approvals and its tests. Include setup, one example, and actual errors.
Separate implemented behavior from proposals. You may edit documentation.
```

## Independent by design

Each specialist works on its own. Panda Lead selects the necessary activities and carries context between them; every task does not need every stage. Skills are Markdown instructions, not an agent service, and do not require multiple agents.

Investigation and review preserve application source unless you ask for changes. An implementation request authorizes relevant edits. Publication, deployment, destructive actions, and production changes need authorization covering those actions.

## Read in your language

The guides use English, and Write, Spec, and Manual support English or Thai requests. A [Thai project overview](thai.html) is also available.

## What has been verified?

The repository records host discovery and tooling checks separately from interactive invocation and behavioral evaluation. Read the [verification record](verification.html) and the [source and license notices](notices.html) for their scope and remaining gaps.
